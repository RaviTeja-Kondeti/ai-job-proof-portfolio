# Project 18: index selection changes the search result

**Posting test:** [Exa's Research Engineer, Index Intelligence](https://jobs.ashbyhq.com/exa/67310301-d019-4290-9c79-e8d6e70d5d50) says a page-level signal matters only when it changes an indexing decision and makes search better. Can a budgeted selector improve downstream query coverage while avoiding duplicate and stale pages?

Run `python3 index_policy.py` and `python3 -m unittest test_select.py` here. The baseline greedily takes the largest predicted page values. The candidate considers predicted value, freshness, cost, and duplicate clusters under the same fixed indexing budget. A separate evaluator reads **hidden** query-coverage labels. The test changes every hidden label and verifies selection is unchanged, guarding against an easy leakage mistake.

Every page, prediction, cost, cluster, and relevance label is invented to demonstrate the evaluation chain. The fixture was shaped to make the candidate better, so the result is **not evidence of live search improvement**. There is no learned classifier, calibrated probability, real crawl, multilingual parsing, human labeling, web-scale cost model, or online query experiment. Those are separate tests in the [role map](../../job-maps/exa-index-intelligence.md).
