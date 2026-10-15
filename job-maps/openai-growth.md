# OpenAI Machine Learning Engineer, Growth: statement-by-statement test map

Source: [OpenAI's employer posting](https://openai.com/careers/machine-learning-engineer-growth-san-francisco/), reviewed October 14, 2026. Each row paraphrases one substantive statement or closely related sentence from the posting. It records the evidence a reviewer could inspect. **Built** links lead to runnable proof; **planned** rows have no proof link yet. None of these projects substitutes for actual years of employment or claims real marketing impact.

| ID | Posting signal, paraphrased | Test a reviewer may apply | Small project | State / proof |
|---|---|---|---|---|
| T01 | Growth spans consumer and business users worldwide. | Can you reason about distinct segments and markets? | Segment and geography growth simulator | Planned |
| T02 | The team works across acquisition, activation, retention, and expansion. | Can you define the full funnel and avoid optimizing one step alone? | Full-funnel event model | Planned |
| T03 | Experimentation, data science, ML, and product engineering all shape growth. | Can you connect modeling to product decisions? | Model-to-product experiment loop | Planned |
| T04 | The aim is durable user value. | Can you optimize beyond a first conversion? | Cohort retention and lifetime-value model | Planned |
| T05 | The team partners with Product, Engineering, Data Science, Design, Finance, Lifecycle, and Marketing. | Can you explain a decision to each partner with different constraints? | Cross-functional decision memo and review record | Planned |
| T06 | The team prizes speed with rigorous measurement. | Can you move quickly without treating noisy metrics as truth? | Rapid experiment protocol and decision log | Planned |
| T07 | Privacy, reliability, and user trust are first-class constraints. | Can you show consent-aware data handling and safe failure behavior? | Consent and reliability audit | Planned |
| T08 | The role optimizes paid marketing investment with models and decision systems. | Can you turn estimated returns into constrained spend decisions? | Constrained budget allocator | **Built:** [code and tests](../projects/budget-allocation/) |
| T09 | Budget choices govern allocation, speed of spend, and reactions to changing performance. | Can you coordinate allocation and pacing without violating caps? | Joint allocation-and-pacing orchestrator | Planned |
| T10 | Decisions rely on noisy, delayed, incomplete signals. | Can you show how bad observations change a decision? | Delayed-signal stress test | Planned |
| T11 | ML, optimization, and experiments must support incremental growth within efficiency limits. | Can you separate predicted value from causal lift? | Incrementality holdout | **Built:** [code and tests](../projects/incrementality/) |
| T12 | Work runs from formulation and prototype through deployment, evaluation, and operation. | Can you own the full lifecycle and show an audit trail? | End-to-end decision service | Planned |
| R01 | Allocate across channels, campaigns, and markets using marginal returns. | Can you select the next dollar's best destination? | Marginal-return allocator | Planned; the [initial constrained allocator](../projects/budget-allocation/) is supporting evidence |
| R02 | Account for saturation, uncertainty, and business limits. | Do diminishing returns, uncertainty, floors, and caps alter choices? | Constrained budget allocator | **Built:** [code and tests](../projects/budget-allocation/) |
| R03 | Adjust spend responsively while avoiding unstable swings. | Does a controller respond within a change limit? | Adaptive spend pacing | **Built:** [code and tests](../projects/spend-pacing/) |
| R04 | Delayed or noisy feedback needs limits, monitoring, and safe fallback. | Does bad telemetry reduce risk instead of accelerating spend? | Telemetry fault and fallback harness | Planned; [pacing fallback tests](../projects/spend-pacing/) are supporting evidence |
| R05 | Forecast conversion and long-term value. | Can you model future outcomes and quantify forecast error? | Conversion and lifetime-value forecast | Planned |
| R06 | Model response saturation to locate the best next dollar. | Do response curves capture diminishing returns? | Saturation-curve estimation | Planned; [synthetic response curves](../projects/budget-allocation/) are supporting evidence |
| R07 | Evaluate policies with simulation and backtesting. | Can a candidate policy outperform a baseline on held-out historical periods? | Policy backtesting workbench | Planned |
| R08 | Run online experiments and measure incrementality. | Can you distinguish attribution from causal impact? | Randomized incrementality holdout | **Built:** [code and tests](../projects/incrementality/) |
| R09 | Validate whether offline gains translate to investment outcomes. | Can you reconcile offline and online results? | Offline-to-online calibration report | Planned |
| R10 | Build pipelines, training and inference workflows, and decision integrations. | Is the system reproducible and operable end to end? | Production-style ML pipeline | Planned |
| R11 | Check data quality, monitor models, and retrain when appropriate. | Can you detect stale/bad data and performance drift? | Data-quality and drift monitor | Planned |
| R12 | Treat consent and privacy thoughtfully. | Can you demonstrate exclusion and deletion rules in a pipeline? | Consent-aware feature store | Planned |
| R13 | Translate business goals into objectives and constraints. | Can you state the optimization problem and tradeoffs clearly? | Optimization specification and decision memo | Planned |
| R14 | Invite disagreement, respect, and inclusion in collaboration. | Can you show review practices that make assumptions and objections visible? | Design review and dissent log | Planned |
| Q01 | Experience may come from ML engineering, applied science, data science, or equivalent impact. | Is the actual five-year work history verifiable? | Verified experience timeline | Pending user-supplied resume or work history; a toy project cannot prove tenure |
| Q02 | Production quantitative systems must span data, deployment, tests, and monitoring. | Is there evidence beyond a notebook? | Deployed decision-system reference implementation | Planned |
| Q03 | Python, SQL, ML frameworks, and large data systems matter. | Can you write production-quality code and query data accurately? | SQL-and-Python large-data pipeline | Planned |
| Q04 | Optimization or control under uncertainty is expected. | Can you reason about constraints and feedback? | Robust optimization comparison | Planned; [allocation](../projects/budget-allocation/) and [pacing](../projects/spend-pacing/) are supporting evidence |
| Q05 | Models are evaluated with delayed or incomplete data while balancing causal impact and reliability. | Do you state what is unknown and when to abstain? | Missing-outcome and abstention study | Planned |
| Q06 | Ambiguous goals must become focused experiments and clear decisions. | Can you turn mixed results into a defensible recommendation? | Ambiguous-growth experiment brief | Planned |
| Q07 | The work should deploy AI responsibly for the company's mission. | Can you identify foreseeable harms and measurable guardrails? | Responsible-growth risk review | Planned |
| C01 | The company describes itself as an AI research and deployment organization. | Can your work bridge empirical research and real-world use? | Research-to-deployment case study | Planned |
| C02 | Safety and human needs are core to deployment. | Can you show how privacy and user outcomes constrain optimization? | User-impact and safety guardrail study | Planned |
| C03 | Broad perspectives and respectful collaboration are valued. | Can you show inclusive review and communication habits? | Accessible technical decision memo | Planned |

## Decision information from the rest of the page

The posting's SF hybrid schedule, compensation, equity, benefits, accommodations, applicant policies, and legal notices affect whether and how to apply. They are recorded as **application checks**, not fabricated technical accomplishments. The user has stated that any US location and onsite or hybrid work are acceptable. Compensation must be discussed as **base pay**, separately from equity and benefits.

## Immediate next proof work

Build R07 policy backtesting, R10 production-style pipeline, and R11 quality/drift monitoring so the existing demonstrations move beyond isolated algorithms. Obtain the user's real work history before writing any employment-based proof or resume links.
