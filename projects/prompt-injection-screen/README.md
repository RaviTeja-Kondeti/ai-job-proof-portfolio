# Project 5: prompt-injection screening baseline

**Job-post test:** Can I build and evaluate a misuse signal while exposing its failures, especially when malicious instructions appear in untrusted content?

This project trains a transparent word-based Naive Bayes classifier on a tiny synthetic dataset and evaluates disjoint holdout cases. Run `python3 screen.py` and `python3 -m unittest test_screen.py` here. The output includes all confusion-matrix counts and the IDs of failures, so a reviewer can inspect where the baseline fails.

This is **not a production defense**. The corpus is small, English-only, manually constructed, and vulnerable to paraphrase and distribution shift. A deployment would require representative data, adversarial holdouts, calibration, human review, layered trust-boundary controls, and monitoring of both false positives and false negatives. The example contains no real user data or dangerous payloads.
