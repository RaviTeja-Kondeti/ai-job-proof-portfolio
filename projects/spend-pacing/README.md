# Project 2: adaptive spend pacing

**Job-post test:** Can I adjust spend when feedback is noisy or delayed, without unstable swings or uncontrolled spending?

`pacing.py` implements a bounded proportional controller. It caps day-to-day changes and spend, respects the remaining budget, and reduces spending when the ROI signal is stale, missing, or invalid. `python3 pacing.py` prints a synthetic decision trace; `python3 -m unittest test_pacing.py` checks safety behavior.

The example deliberately treats observed ROI as an input, not as a causal estimate. Production use would require a vetted incremental value signal, conversion-delay modeling, consent checks, instrumentation, and rollback controls.
