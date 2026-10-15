# A reward can improve while the task gets worse

**Posting tests:** [Handshake AI MTS, Evals](https://jobs.ashbyhq.com/handshake/ca392442-69eb-46f5-b367-37e43c832094) asks for evaluations resistant to shortcutting and reward hacking. [Baseten Post-Training Applied Researcher](https://jobs.ashbyhq.com/baseten/2d18b2aa-b6fc-4f1c-8936-33b03255a090) asks candidates to diagnose reward hacking and distinguish rewards that train from rewards that exploit. This project supplies a tiny **synthetic** policy-gradient failure case, not evidence of LLM RL or production model training.

## Test design

An agent has two actions on each addition task: return the correct plain answer, or return an incorrect answer beginning with `reason:`. A bad **proxy reward** checks only that prefix. An exact arithmetic **verifier reward** checks task success. The 200 training pairs and 100 held-out pairs are disjoint and chosen by a fixed seed. A Bernoulli policy starts at 50% exploit probability and receives 1,200 REINFORCE updates. Thirty random seeds measure sensitivity to training and held-out action draws. The verifier is used only in its own training arm and for final true-success measurement; the proxy-trained arm is never trained on the verifier.

## Result

| Policy | Mean proxy score on held-out pairs | Mean actual task success | Mean exploit probability |
|---|---:|---:|---:|
| Untrained | 0.508 | 0.492 | 0.500 |
| Trained on prefix proxy | **0.996** | **0.004** | 0.996 |
| Trained on exact verifier | 0.006 | **0.994** | 0.004 |

Values are averages over 30 runs of 100 held-out tasks each. These are synthetic draws from the same tiny task family, **not confidence intervals or evidence of generalization to agents or LLMs**. [Frozen machine-readable result](results.json) includes the protocol and range across seeds.

**Decision:** reject the prefix reward. A higher reward score here is actively misleading. Check the actual task outcome with a separate verifier and test a range of exploitable responses before using any proxy to train a real system. An exact checker is available for this toy arithmetic problem; most useful AI tasks need human judgment, calibrated graders, and adversarial tests, so the repaired arm is only an illustration.

## Reproduce

From the repository root with Python 3.10+ standard library:

```sh
python3 -m unittest discover -s projects/reward-proxy-stress -p 'test_*.py'
python3 projects/reward-proxy-stress/stress.py
```

The [code](stress.py) and six tests cover the frozen disjoint task split, the metric exploit, opposite training directions, held-out success collapse, and invalid-input rejection.
