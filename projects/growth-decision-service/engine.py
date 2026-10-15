"""In-memory reference decision engine with explicit safety constraints."""

from datetime import datetime, timedelta, timezone
import json
import math
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

POLICY_VERSION = "growth-policy-v1"
CHANNELS = ("search", "social")


class DecisionEngine:
    def __init__(self):
        self._seen = {}
        self.decisions = []
        self.fallbacks = 0

    def decide(self, request: dict, now: datetime | None = None) -> dict:
        if not isinstance(request, dict):
            raise ValueError("Request must be a JSON object")
        now = now or datetime.now(timezone.utc)
        if now.tzinfo is None:
            raise ValueError("Clock must be timezone-aware")
        decision_id = request.get("decision_id")
        if not isinstance(decision_id, str) or not decision_id:
            raise ValueError("decision_id is required")
        fingerprint = json.dumps(request, sort_keys=True, separators=(",", ":"))
        if decision_id in self._seen:
            previous_fingerprint, previous_result = self._seen[decision_id]
            if previous_fingerprint != fingerprint:
                raise ValueError("decision_id reused with different request")
            return previous_result
        budget = request.get("budget")
        if type(budget) is not int or budget < 0:
            raise ValueError("budget must be a nonnegative integer")
        channels = request.get("channels")
        if not isinstance(channels, dict) or set(channels) != set(CHANNELS):
            raise ValueError("Both named channels are required")
        for name in CHANNELS:
            row = channels[name]
            if not isinstance(row, dict):
                raise ValueError("Channel settings must be objects")
            if not isinstance(row.get("consented"), bool):
                raise ValueError("Consent must be explicit")
            if type(row.get("cap")) is not int or row["cap"] < 0:
                raise ValueError("Channel cap must be nonnegative")
            if (type(row.get("score")) not in (int, float)
                    or not math.isfinite(row["score"]) or row["score"] < 0):
                raise ValueError("Score must be nonnegative")
        try:
            observed_at = datetime.fromisoformat(request["observed_at"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError("observed_at must be an ISO timestamp") from exc
        if observed_at.tzinfo is None or observed_at > now:
            raise ValueError("Observation time must be timezone-aware and not future")

        stale = now - observed_at > timedelta(hours=24)
        eligible = [name for name in CHANNELS
                    if channels[name]["consented"] and channels[name]["cap"] > 0]
        allocation = {name: 0 for name in CHANNELS}
        remaining = budget
        # Stale observations fall back to deterministic equal-priority allocation.
        order = sorted(eligible) if stale else sorted(
            eligible, key=lambda name: (-channels[name]["score"], name))
        if stale:
            while remaining > 0 and order:
                progressed = False
                for name in order:
                    if allocation[name] < channels[name]["cap"] and remaining:
                        allocation[name] += 1
                        remaining -= 1
                        progressed = True
                if not progressed:
                    break
        else:
            for name in order:
                take = min(remaining, channels[name]["cap"])
                allocation[name] = take
                remaining -= take
        if stale and eligible:
            self.fallbacks += 1
        result = {
            "decision_id": decision_id,
            "policy_version": POLICY_VERSION,
            "mode": "hold" if not eligible else ("stale_fallback" if stale else "scored"),
            "allocation": allocation,
            "unspent": remaining,
            "observed_at": observed_at.isoformat(),
        }
        self._seen[decision_id] = (fingerprint, result)
        self.decisions.append(result)
        return result


ENGINE = DecisionEngine()


class Handler(BaseHTTPRequestHandler):
    def _json(self, status: int, payload: dict):
        data = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/health":
            self._json(200, {"status": "ok", "policy_version": POLICY_VERSION})
        elif self.path == "/metrics":
            self._json(200, {"decisions": len(ENGINE.decisions),
                             "stale_fallbacks": ENGINE.fallbacks})
        else:
            self._json(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/decide":
            self._json(404, {"error": "not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 65536:
                raise ValueError("Invalid request size")
            request = json.loads(self.rfile.read(length))
            self._json(200, ENGINE.decide(request))
        except (ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
            self._json(400, {"error": str(exc)})


if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", 8765), Handler).serve_forever()
