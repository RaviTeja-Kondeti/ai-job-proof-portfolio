import importlib.util
import json
import sys
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("relational_privacy", Path(__file__).with_name("deidentify.py"))
module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = module
SPEC.loader.exec_module(module)


def tiny_data():
    customers = [
        {"customer_id": str(i), "name": f"Person {i}",
         "email": f"person{i}@example.test", "age": 25 + i, "state": "CA"}
        for i in range(3)
    ]
    orders = [{"order_id": "o1", "customer_id": "0", "amount": 100},
              {"order_id": "o2", "customer_id": "1", "amount": 200}]
    return customers, orders


class PrivacyTests(unittest.TestCase):
    def test_removes_direct_pii_and_keeps_joins_and_revenue(self):
        customers, orders = tiny_data()
        output = module.transform(customers, orders, module.DEMO_KEY)
        rendered = json.dumps(output)
        for raw in ("Person 0", "person0@example.test", "Person 1"):
            self.assertNotIn(raw, rendered)
        self.assertEqual(output["audit"]["orphan_orders"], 0)
        self.assertTrue(output["audit"]["revenue_cents_preserved"])
        self.assertEqual(output["orders"][0]["customer_token"],
                         output["customers"][0]["customer_token"])

    def test_key_and_entity_domain_change_pseudonyms(self):
        x = module.pseudonym("customer", "1", module.DEMO_KEY)
        self.assertEqual(x, module.pseudonym("customer", "1", module.DEMO_KEY))
        self.assertNotEqual(x, module.pseudonym("order", "1", module.DEMO_KEY))
        self.assertNotEqual(x, module.pseudonym("customer", "1", b"another-secret-key"))

    def test_small_quasi_cells_are_coarsened(self):
        output = module.demo()
        self.assertGreaterEqual(output["audit"]["minimum_quasi_cell_ignoring_tokens_and_orders"], 2)
        self.assertIn({"state": "*", "age_decade": "*"},
                      [{"state": c["state"], "age_decade": c["age_decade"]}
                       for c in output["customers"]])
        self.assertLess(output["audit"]["age_decade_retained_fraction"], 1)

    def test_single_rare_record_triggers_global_quasi_suppression(self):
        customers, orders = tiny_data()
        customers[2]["state"] = "WY"
        output = module.transform(customers, orders, module.DEMO_KEY)
        self.assertTrue(all(c["state"] == "*" and c["age_decade"] == "*"
                            for c in output["customers"]))

    def test_orphan_and_extra_field_fail_closed(self):
        customers, orders = tiny_data()
        with self.assertRaises(ValueError):
            module.transform(customers, [{**orders[0], "customer_id": "missing"}], module.DEMO_KEY)
        with self.assertRaises(ValueError):
            module.transform([{**customers[0], "phone": "555"}] + customers[1:],
                             orders, module.DEMO_KEY)

    def test_short_key_and_duplicate_ids_are_rejected(self):
        customers, orders = tiny_data()
        with self.assertRaises(ValueError):
            module.transform(customers, orders, b"short")
        with self.assertRaises(ValueError):
            module.transform(customers + [dict(customers[0])], orders, module.DEMO_KEY)


if __name__ == "__main__":
    unittest.main()
