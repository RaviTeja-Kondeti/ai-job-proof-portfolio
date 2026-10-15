# Project 4: evidence-grounded LLM output evaluation

**Job-post test:** Can I test whether an AI-generated note is supported by source evidence, identify omissions, and route unsafe results to human review?

`synthetic_cases.json` contains invented structured encounter facts and candidate outputs. `evaluate.py` checks each claim against its cited fact, reports unsupported content and omissions, and creates a human-review queue. It deliberately catches a candidate note that invents a diagnosis and omits an allergy.

Run `python3 evaluate.py` and `python3 -m unittest test_evaluate.py` in this folder. This is an **evaluation harness**, not a medical note generator or validated clinical system. Exact string comparisons cannot establish clinical correctness; real deployment would require clinician-designed rubrics, representative and consented data, privacy controls, calibration, multilingual tests, and human oversight.
