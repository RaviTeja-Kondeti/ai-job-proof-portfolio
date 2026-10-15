# Project 10: experiment validity audit

**Job-post tests:** Can you define trustworthy online experiment standards, prevent a broken assignment from misleading a team, reduce variance using pre-period data, and state how interim looks affect the decision threshold?

Run `python3 audit.py` for a reproducible synthetic report and `python3 -m unittest test_audit.py` for quality checks. Users receive a stable hash assignment; the audit checks sample-ratio mismatch, raw and CUPED-adjusted effects, a predeclared Bonferroni threshold across planned looks, and a guardrail failure-rate difference.

This is a teaching-sized simulation. The normal approximations, pooled CUPED coefficient, and point-estimate guardrail need scrutiny before a consequential experiment. It does not replace a powered design, sequential confidence intervals, heterogeneous effects analysis, instrumentation QA, or real retention and revenue validation. No business impact is claimed.
