# Project 16: delayed-outcome conversion and value forecast

**Source test:** [OpenAI's Machine Learning Engineer, Growth posting](https://openai.com/careers/machine-learning-engineer-growth-san-francisco/) asks for conversion and long-term value forecasts that guide marketing investment. Can a segment/channel forecast be evaluated without training on outcomes unavailable at the decision date?

Run `python3 forecast.py` and `python3 -m unittest test_forecast.py` from this directory. The script creates deterministic **synthetic** signup cohorts, fits a global baseline and a smoothed segment/channel model, and reports held-out Brier score for 7-day conversion and mean absolute error for 30-day value per signup. It prints segment slices and paired bootstrap intervals for the candidate-minus-baseline errors. Lower errors are better.

At decision day 100, only cohorts whose full 30-day label has matured are used to fit either model. Cohorts from day 100 onward form a future holdout once their outcomes mature by evaluation day 150. Tests assert the cutoff and that rewriting future outcomes cannot change training estimates. The 30-day value is only a bounded proxy, **not** lifetime value.

The data-generating process is deliberately simple, and both models see its same stable segment/channel structure. Any measured improvement is an exercise result, not evidence of real marketing lift or causal incrementality. A production version would need privacy/consent handling, real event and attribution quality, calibration and drift monitoring, holdout design, longer-term outcomes, and online testing before budget decisions.
