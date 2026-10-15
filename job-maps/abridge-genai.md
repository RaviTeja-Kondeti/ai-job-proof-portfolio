# Abridge Software Engineer, Generative AI: statement-by-statement test map

Source: [Abridge's employer posting](https://jobs.ashbyhq.com/abridge/897709b2-e03d-4574-8611-5cfd669adde9), reviewed October 14, 2026. This map paraphrases the substantive company, role, responsibility, and qualification statements. **Built** means runnable code exists; **planned** is an explicit gap. The clinical example contains only invented structured facts and is not a clinical product.

| ID | Posting signal, paraphrased | Reviewer test | Small project | State / proof |
|---|---|---|---|---|
| C01 | AI should make medical conversations easier to understand. | Does the output help a human verify what was said? | Source-linked note viewer | Planned |
| C02 | Notes are generated in real time and integrated into clinical systems. | Can the workflow meet latency and integration constraints? | Streaming note pipeline | Planned |
| C03 | Generated summaries are linked back to ground truth. | Can each statement be traced to evidence? | Grounded-output evaluation | **Built:** [code and tests](../projects/llm-evaluation/) |
| C04 | Auditable AI supports clinician trust. | Can a reviewer inspect unsupported or missing claims? | Human-review audit queue | Planned; [initial review flags](../projects/llm-evaluation/) are supporting evidence |
| C05 | Responsible deployment across health systems matters. | Are privacy, safety, and oversight explicit? | Clinical AI risk and privacy review | Planned |
| R01 | Build dependable LLM workflows for complex clinical context. | Does a workflow handle long and conflicting context? | Context-conflict resolution suite | Planned |
| R02 | Use agents, tools, and branching chains of LLM calls. | Can tool calls and recovery paths be tested? | Tool-using agent with failure injection | Planned |
| R03 | Integrate retrieval into the workflow. | Does retrieval improve factual grounding? | Evidence retrieval benchmark | Planned |
| R04 | Consistently produce clinically reliable output. | Are unsupported claims caught before release? | Grounded-output evaluation | **Built:** [code and tests](../projects/llm-evaluation/) |
| R05 | Design automated and human evaluation. | Can automated failures be routed to reviewers? | Reviewer queue and adjudication log | Planned; [initial review flags](../projects/llm-evaluation/) are supporting evidence |
| R06 | Test accuracy, robustness, and multilingual behavior. | Is quality measured on varied and adversarial cases? | Multilingual robustness set | Planned |
| R07 | Probe failure modes and realistic edge cases. | Can the system surface omissions, false claims, and conflicts? | Clinical failure-mode corpus | Planned; [two synthetic examples](../projects/llm-evaluation/synthetic_cases.json) are an initial seed |
| R08 | Use A/B testing and baselines for deployment decisions. | Is a new workflow measurably better than a baseline? | Paired workflow comparison | Planned |
| R09 | Use clinician feedback to improve models. | Can expert corrections become versioned eval data? | Clinician-feedback ingestion protocol | Planned |
| R10 | Own production latency, uptime, monitoring, guardrails, and versioning. | Could this operate safely beyond a notebook? | Versioned workflow service with observability | Planned |
| R11 | Build composable agents with retrieval, tools, reasoning, and structured output. | Are steps inspectable and testable independently? | Modular agent workflow | Planned |
| R12 | Optimize model choice, context length, latency, and cost. | Can quality/cost tradeoffs be measured? | Model-routing benchmark | Planned |
| R13 | Write modular code with graceful failure handling. | Do tests cover faults and safe degradation? | Agent fault-injection harness | Planned |
| R14 | Make architectural choices about workflow state and outputs. | Can you justify state, caching, and schema choices? | Architecture decision record with runnable prototype | Planned |
| R15 | Build benchmarks, human review, and experiments to find edge cases. | Does evaluation expose omissions and unsupported content? | Grounded-output evaluation | **Built:** [code and tests](../projects/llm-evaluation/) |
| R16 | Prototype with emerging models and techniques. | Can you compare a new approach against a fixed baseline? | Model capability comparison | Planned |
| Q01 | 3+ years of production systems, including 1–2+ in LLM or agents. | Is real tenure and deployment history documented? | Verified work timeline and production case studies | Pending user-supplied work history; a portfolio project cannot prove tenure |
| Q02 | LLM APIs, prompts, and orchestration patterns. | Can you show a real integration rather than only a mock? | Provider-backed workflow adapter | Planned; requires API access or safe local model |
| Q03 | Retrieval, vector search, function calling, or tools. | Can you measure retrieval quality and tool reliability? | Retrieval and tool-call evaluation | Planned |
| Q04 | Diverse evaluation sets, A/B tests, and subject-matter review. | Are quality claims grounded in representative data and expert criteria? | Evaluation governance package | Planned |
| Q05 | Strong Python and production engineering. | Can code be packaged, tested, profiled, and deployed? | Packaged async workflow service | Planned |
| Q06 | Fast iteration should coexist with engineering judgment. | Can you show when to ship and when to address risk or debt? | Release decision and technical-debt log | Planned |

## Application checks

The posting lists a US base range of $255k–$300k across mid, senior, and staff levels and expects at least three office days weekly in SF or NYC. The user says US location and onsite/hybrid work are acceptable. Exact level, education, work authorization, and genuine LLM production work remain unverified. These are application facts to check, not project achievements.
