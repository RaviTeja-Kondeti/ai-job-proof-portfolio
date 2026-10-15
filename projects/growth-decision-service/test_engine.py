from datetime import datetime, timedelta, timezone
from io import BytesIO
import json
import unittest
import engine
from engine import DecisionEngine, Handler, POLICY_VERSION


NOW = datetime(2026, 10, 15, 0, 0, tzinfo=timezone.utc)


def request(decision_id="d1", observed_at=None):
    return {
        "decision_id": decision_id, "budget": 10,
        "observed_at": (observed_at or NOW - timedelta(hours=1)).isoformat(),
        "channels": {
            "search": {"consented": True, "cap": 8, "score": 0.9},
            "social": {"consented": True, "cap": 4, "score": 0.2},
        },
    }


class DecisionEngineTests(unittest.TestCase):
    def setUp(self):
        self.engine = DecisionEngine()

    def test_caps_budget_and_policy_record(self):
        result = self.engine.decide(request(), NOW)
        self.assertEqual(sum(result["allocation"].values()) + result["unspent"], 10)
        self.assertLessEqual(result["allocation"]["search"], 8)
        self.assertLessEqual(result["allocation"]["social"], 4)
        self.assertEqual(result["policy_version"], POLICY_VERSION)

    def test_stale_observation_uses_equal_priority_fallback(self):
        fresh = self.engine.decide(request("fresh"), NOW)
        stale = self.engine.decide(request("stale", NOW - timedelta(days=2)), NOW)
        self.assertEqual(stale["mode"], "stale_fallback")
        self.assertLess(stale["allocation"]["search"], fresh["allocation"]["search"])
        self.assertEqual(self.engine.fallbacks, 1)

    def test_consent_revocation_prevents_spend(self):
        req = request()
        req["channels"]["search"]["consented"] = False
        result = self.engine.decide(req, NOW)
        self.assertEqual(result["allocation"]["search"], 0)
        self.assertEqual(result["allocation"]["social"], 4)
        self.assertEqual(result["unspent"], 6)

    def test_duplicate_decision_id_is_idempotent_and_conflict_rejected(self):
        first = self.engine.decide(request(), NOW)
        self.assertEqual(self.engine.decide(request(), NOW), first)
        changed = request()
        changed["budget"] = 50
        with self.assertRaises(ValueError):
            self.engine.decide(changed, NOW)
        self.assertEqual(len(self.engine.decisions), 1)

    def test_future_and_implicit_consent_rejected(self):
        with self.assertRaises(ValueError):
            self.engine.decide(request(observed_at=NOW + timedelta(hours=1)), NOW)
        req = request()
        del req["channels"]["social"]["consented"]
        with self.assertRaises(ValueError):
            self.engine.decide(req, NOW)
        req = request()
        req["channels"]["search"]["score"] = float("nan")
        with self.assertRaises(ValueError):
            self.engine.decide(req, NOW)


class HttpHandlerTests(unittest.TestCase):
    def _call(self, path, payload=None):
        handler = object.__new__(Handler)
        handler.path = path
        handler.wfile = BytesIO()
        handler.send_response = lambda code: setattr(handler, "status_code", code)
        handler.send_header = lambda *_: None
        handler.end_headers = lambda: None
        if payload is not None:
            data = json.dumps(payload).encode()
            handler.rfile = BytesIO(data)
            handler.headers = {"Content-Length": str(len(data))}
            handler.do_POST()
        else:
            handler.do_GET()
        return handler.status_code, json.loads(handler.wfile.getvalue())

    def test_health_and_decision_endpoint_without_a_socket(self):
        engine.ENGINE = DecisionEngine()
        status, health = self._call("/health")
        self.assertEqual(status, 200)
        self.assertEqual(health["policy_version"], POLICY_VERSION)
        status, result = self._call("/decide", request("http-1"))
        self.assertEqual(status, 200)
        self.assertEqual(result["decision_id"], "http-1")

    def test_bad_post_returns_client_error(self):
        status, result = self._call("/decide", {"decision_id": "bad"})
        self.assertEqual(status, 400)
        self.assertIn("error", result)
        status, result = self._call("/decide", ["wrong-shape"])
        self.assertEqual(status, 400)
        self.assertIn("error", result)


if __name__ == "__main__":
    unittest.main()
