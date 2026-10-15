# Joint allocation and spend pacing

**Posting test:** The [OpenAI Machine Learning Engineer, Growth role](https://openai.com/careers/machine-learning-engineer-growth-san-francisco/) connects budget allocation, pacing, and reactions to changing performance. This project combines the repository's [marginal-return allocator](../budget-allocation/) and [bounded pacing controller](../spend-pacing/) into one synthetic daily decision. It does not estimate causal lift or represent real campaign performance.

From the repository root, with Python 3.10+:

```sh
python3 -m unittest discover -s projects/joint-allocation-pacing -p 'test_*.py' -v
python3 projects/joint-allocation-pacing/orchestrate.py
```

The [orchestrator](orchestrate.py) gets each campaign's ROI feedback and previous spend. It constructs an allowable spend interval from campaign floors/caps and a 20% daily change limit. Stale or invalid feedback forces a rounded, bounded reduction; if that conflicts with a required floor, it pauses rather than exceeding the safe cap. The controller proposes a total daily spend. The allocator then distributes that total within all campaign intervals using risk-adjusted synthetic response curves. A budget below required floors pauses the decision instead of overspending.

In the checked-in [three-day result](results.json), the synthetic $10,000 budget leaves $900 unspent. When social-channel feedback is missing on day 2, its allocation falls from $800 to $700, while the total decision still respects the daily budget and other campaign bounds. Four [integration tests](test_orchestrate.py) check the budget identity, stale-signal behavior, campaign change bounds, infeasible-budget pause, and feedback schema.

**Limits:** The response curves and ROI inputs are invented, so the reported risk-adjusted value is a model score, not real conversions, dollars of return, or an incrementality estimate. The controller does not model delayed conversions, attribution bias, platform auction dynamics, shared campaign interactions, or online monitoring. A production decision would need randomized lift evidence, calibrated uncertainty, monitoring, consent handling, and a human-owned rollback path.
