# Anthropic ML/Research Engineer, Safeguards: statement-by-statement test map

Source: [Anthropic's employer posting](https://job-boards.greenhouse.io/anthropic/jobs/4949336008), reviewed October 14, 2026. Each row paraphrases a substantive company, role, responsibility, qualification, or application statement. **Planned** means there is no completed proof yet. General LLM evaluation code is linked only as partial support; it is not described as AI safety research.

| ID | Posting signal, paraphrased | Reviewer test | Small project | State / proof |
|---|---|---|---|---|
| C01 | AI should be reliable, interpretable, and steerable. | Can a safety intervention be explained and adjusted? | Interpretable safety classifier analysis | Planned |
| C02 | Systems should benefit users and society. | Are user and broader harm criteria explicit? | Multi-stakeholder safety impact assessment | Planned |
| C03 | Research, engineering, policy, and business must work together. | Can results be communicated across disciplines? | Cross-functional safeguards decision memo | Planned |
| R01 | Detect misuse and build defenses as capabilities change. | Can a detection system adapt without hidden regressions? | Versioned misuse-detection benchmark | Planned |
| R02 | Detect both single violations and coordinated activity. | Can an approach reason across individual and multi-event patterns? | Multi-turn anomaly detector | Planned |
| R03 | Protect user wellbeing across varied contexts. | Are false positives and user-impact tradeoffs measured? | Wellbeing and false-positive evaluation | Planned |
| R04 | Support responsible scaling commitments. | Can measurable gates and escalation decisions be tied to risk? | Safety release-gate simulation | Planned |
| R05 | Build misuse and anomaly classifiers at scale. | Can you train, evaluate, and operate a classifier with realistic metrics? | Synthetic misuse classifier | Planned; [small screening baseline](../projects/prompt-injection-screen/) is partial proof |
| R06 | Create synthetic training data and representative evaluations. | Does generated data cover failure modes without contaminating the test set? | Synthetic safety-data generator and holdout | Planned |
| R07 | Monitor harm across conversations and coordinated contexts. | Do aggregation rules find patterns a single message misses? | Cross-conversation signal aggregator | Planned |
| R08 | Threat-model and test agentic products. | Can you identify assets, trust boundaries, and attack paths? | Agent threat model and attack environment | Planned |
| R09 | Mitigate prompt injection. | Can untrusted tool or document text be prevented from changing agent instructions? | Prompt-injection defense harness | Planned; [screening baseline](../projects/prompt-injection-screen/) is only a detection component |
| R10 | Research automated red-teaming and adversarial robustness. | Can tests evolve beyond memorized attack strings? | Adaptive red-team evaluation | Planned |
| Q01 | 4+ years in relevant ML or research engineering. | Is actual tenure verifiable? | Verified experience timeline | Pending user-supplied work history; a portfolio project cannot prove tenure |
| Q02 | Python and practical ML systems matter. | Is the work reproducible and more than a notebook? | Packaged safety-ML service | Planned |
| Q03 | Work spans research experiments to production systems. | Can you justify a deployment path and monitor failures? | Research-to-production safety case study | Planned |
| Q04 | Misuse risk should motivate the work. | Can you identify concrete misuse risks and mitigation goals? | Misuse risk research brief | Planned |
| Q05 | Explain technical concepts to nontechnical partners. | Can a decision memo state uncertainty and tradeoffs clearly? | Nontechnical safeguards briefing | Planned |
| P01 | Language models and transformers are useful depth. | Can you probe actual model behavior rather than only regex matches? | Model-behavior probing suite | Planned |
| P02 | Classifiers, anomaly detection, and behavioral ML are valued. | Are precision, recall, calibration, and drift measured? | Behavioral classifier comparison | Planned |
| P03 | Adversarial ML and red-teaming are valuable. | Are attacks separated from training examples? | Held-out adversarial challenge set | Planned |
| P04 | Interpretability or probes can strengthen a candidacy. | Can you inspect why the model fired? | Feature-attribution and probe notebook | Planned |
| P05 | Reinforcement learning is another useful specialty. | Can you connect an RL technique to a safety objective? | Constrained policy-learning simulation | Planned |
| P06 | High-performance large-scale systems are relevant. | Can you measure throughput, latency, and operating cost? | Scalable inference load test | Planned |
| V01 | The company values empirical, collaborative, high-impact research. | Does the project ask a falsifiable question and expose limitations? | Replicable safety research report | Planned |
| V02 | Frequent research discussions and communication matter. | Can a technical critique lead to a changed experiment? | Research review and revision record | Planned |
| A01 | The application requests a short account of impactful AI safety work. | Can you describe **real** work and results without inflating a demo? | Evidence-linked safety work statement | Pending verified work history; do not substitute a synthetic portfolio for real employment impact |
| A02 | The application has an AI-use policy and asks why Anthropic. | Can you follow the stated policy and give a specific rationale? | Application-policy checklist and company research notes | Planned |

## Application checks

The posting lists $350k–$500k annual salary and SF/NYC locations with a hybrid expectation. It says visa sponsorship may be available, subject to role and candidate. The user's work authorization and education are unknown; verify before claiming eligibility. Form fields, arbitration text, and general legal notices are application steps, not technical accomplishments.
