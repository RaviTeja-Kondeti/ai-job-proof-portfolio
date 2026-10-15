"""Synthetic relational pseudonymization with conservative quasi-field coarsening."""

from __future__ import annotations

import hashlib
import hmac
import json
from collections import Counter

CUSTOMER_FIELDS = frozenset({"customer_id", "name", "email", "age", "state"})
ORDER_FIELDS = frozenset({"order_id", "customer_id", "amount"})
DEMO_KEY = b"PUBLIC-DEMO-KEY-NEVER-USE-ON-REAL-DATA"


def pseudonym(kind: str, raw_id: str, key: bytes) -> str:
    if not isinstance(key, bytes) or len(key) < 16:
        raise ValueError("A secret byte key of at least 16 bytes is required")
    if not isinstance(raw_id, str) or not raw_id:
        raise ValueError("ID must be a nonempty string")
    digest = hmac.new(key, f"{kind}:{raw_id}".encode(), hashlib.sha256).hexdigest()
    return digest[:24]


def validate(customers: list[dict], orders: list[dict]) -> None:
    if not customers or not orders:
        raise ValueError("Both tables need rows")
    ids, order_ids = set(), set()
    for customer in customers:
        if set(customer) != CUSTOMER_FIELDS:
            raise ValueError("Unexpected customer fields")
        cid = customer["customer_id"]
        if not isinstance(cid, str) or not cid or cid in ids:
            raise ValueError("Duplicate or invalid customer ID")
        ids.add(cid)
        if not (isinstance(customer["name"], str) and isinstance(customer["email"], str)
                and isinstance(customer["age"], int) and not isinstance(customer["age"], bool)
                and 0 <= customer["age"] <= 120
                and isinstance(customer["state"], str) and len(customer["state"]) == 2):
            raise ValueError("Invalid customer row")
    for order in orders:
        if set(order) != ORDER_FIELDS:
            raise ValueError("Unexpected order fields")
        oid = order["order_id"]
        if not isinstance(oid, str) or not oid or oid in order_ids:
            raise ValueError("Duplicate or invalid order ID")
        order_ids.add(oid)
        if order["customer_id"] not in ids:
            raise ValueError("Orphan order")
        if (not isinstance(order["amount"], int) or isinstance(order["amount"], bool)
                or order["amount"] < 0):
            raise ValueError("Amount must be nonnegative integer cents")


def coarsen(customers: list[dict], minimum: int) -> dict[str, tuple[str, str]]:
    if not isinstance(minimum, int) or minimum < 2 or minimum > len(customers):
        raise ValueError("Cell minimum must be between 2 and the customer count")
    state_counts = Counter(c["state"] for c in customers)
    state_decade = Counter((c["state"], c["age"] // 10 * 10) for c in customers)
    unsafe_age_states = {state for (state, _), count in state_decade.items()
                         if count < minimum}
    values = {}
    for customer in customers:
        state = customer["state"]
        if state_counts[state] < minimum:
            values[customer["customer_id"]] = ("*", "*")
        elif state in unsafe_age_states:
            values[customer["customer_id"]] = (state, "*")
        else:
            values[customer["customer_id"]] = (state, str(customer["age"] // 10 * 10))
    cells = Counter(values.values())
    if any(count < minimum for count in cells.values()):
        # If only one rare-state record is in the common suppression pool,
        # reveal no quasi fields at all rather than claiming a small cell safe.
        return {cid: ("*", "*") for cid in values}
    return values


def transform(customers: list[dict], orders: list[dict], key: bytes,
              minimum: int = 2) -> dict:
    validate(customers, orders)
    generalized = coarsen(customers, minimum)
    ids = {c["customer_id"]: pseudonym("customer", c["customer_id"], key)
           for c in customers}
    known_tokens = set(ids.values())
    if len(known_tokens) != len(ids):
        raise ValueError("Customer-token collision")
    masked_customers = [
        {"customer_token": ids[c["customer_id"]],
         "state": generalized[c["customer_id"]][0],
         "age_decade": generalized[c["customer_id"]][1]}
        for c in customers
    ]
    masked_orders = [
        {"order_token": pseudonym("order", o["order_id"], key),
         "customer_token": ids[o["customer_id"]],
         "amount_cents": o["amount"]}
        for o in orders
    ]
    if len({o["order_token"] for o in masked_orders}) != len(masked_orders):
        raise ValueError("Order-token collision")
    cells = Counter((c["state"], c["age_decade"]) for c in masked_customers)
    output = {"customers": masked_customers, "orders": masked_orders,
              "audit": {
                  "customers": len(masked_customers), "orders": len(masked_orders),
                  "orphan_orders": sum(o["customer_token"] not in known_tokens
                                       for o in masked_orders),
                  "revenue_cents_preserved": sum(o["amount"] for o in orders)
                                              == sum(o["amount_cents"] for o in masked_orders),
                  "minimum_quasi_cell_ignoring_tokens_and_orders": min(cells.values()),
                  "state_retained_fraction": sum(c["state"] != "*" for c in masked_customers)
                                             / len(customers),
                  "age_decade_retained_fraction": sum(c["age_decade"] != "*"
                                                       for c in masked_customers) / len(customers),
              }}
    if output["audit"]["orphan_orders"] or min(cells.values()) < minimum:
        raise AssertionError("Relational or quasi-cell check failed")
    return output


def demo() -> dict:
    places = [
        ("CA", 22), ("CA", 24), ("CA", 35),
        ("NY", 28), ("NY", 29), ("NY", 41), ("NY", 43),
        ("WY", 52), ("AK", 61),
    ]
    customers = [
        {"customer_id": f"c{i}", "name": f"Synthetic Person {i}",
         "email": f"synthetic{i}@example.test", "age": age, "state": state}
        for i, (state, age) in enumerate(places)
    ]
    orders = [
        {"order_id": f"o{i}", "customer_id": f"c{i % len(customers)}",
         "amount": (i + 1) * 125}
        for i in range(12)
    ]
    return transform(customers, orders, DEMO_KEY)


if __name__ == "__main__":
    print(json.dumps(demo(), indent=2, sort_keys=True))
