import json
from pathlib import Path
import unittest
from evaluate import evaluate_case, evaluate_dataset


class EvaluationTests(unittest.TestCase):
    def setUp(self):
        self.cases = json.loads(Path(__file__).with_name("synthetic_cases.json").read_text())

    def test_supported_case_passes(self):
        result = evaluate_case(self.cases[0])
        self.assertFalse(result["requires_human_review"])
        self.assertEqual(result["supported_claims"], 3)

    def test_invented_diagnosis_is_flagged(self):
        result = evaluate_case(self.cases[1])
        self.assertTrue(result["requires_human_review"])
        self.assertEqual(result["unsupported_claims"][0]["concept"], "diagnosis")
        self.assertIn("allergy", result["omitted_expected_concepts"])

    def test_wrong_citation_fails_even_if_value_exists_elsewhere(self):
        case = dict(self.cases[0])
        case["candidate_claims"] = [{"concept": "fever", "value": "denied", "citations": ["f1"]}]
        self.assertEqual(evaluate_case(case)["supported_claims"], 0)

    def test_missing_citation_requires_review(self):
        case = dict(self.cases[0])
        case["candidate_claims"] = [{"concept": "symptom", "value": "cough for three days"}]
        self.assertIn("symptom", evaluate_case(case)["claims_without_citations"])

    def test_dataset_report(self):
        result = evaluate_dataset(self.cases)
        self.assertEqual(result["dataset_size"], 2)
        self.assertEqual(result["human_review_cases"], 1)


if __name__ == "__main__":
    unittest.main()
