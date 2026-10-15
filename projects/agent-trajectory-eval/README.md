# Project 12: agent trajectory evaluation

**Job-post test:** Can agent quality be measured through tool choice, arguments, recovery, policy compliance, and final state, rather than accepting a plausible final answer?

`python3 evaluate.py` scores six invented traces. Two deliberately have the expected final answer but fail because one used wrong arguments and another made an unauthorized purchase call. `python3 -m unittest test_evaluate.py` checks these failure cases and timeout recovery.

The traces are synthetic and hand-labeled. There is no running model, real tool integration, human adjudication, statistical uncertainty, or production policy enforcement. A deployment-grade suite would add replayable real traces with consent, graded argument equivalence, side-effect verification, adversarial cases, and confidence intervals.
