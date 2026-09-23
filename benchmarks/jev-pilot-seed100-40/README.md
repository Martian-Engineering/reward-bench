# Jev RewardBench pairwise pilot

Jev 1.13.0 judged 40 examples sampled from the official RewardBench v1
`filtered` split. Seed 100 selected ten examples from each subset. Every pair
was sent twice through TypeSafe System One: once with the benchmark's preferred
response as A and once as B. The model saw the user prompt and both candidate
responses. No API request failed.

| RewardBench subset | Preferred answer as A | Preferred answer as B | Correct in both orders |
| --- | ---: | ---: | ---: |
| AlpacaEval Hard | 10/10 | 10/10 | 10/10 |
| LLMBar Natural | 10/10 | 10/10 | 10/10 |
| XSTest Should Respond | 10/10 | 10/10 | 10/10 |
| PRM Math | 9/10 | 9/10 | 8/10 |
| **Total** | **39/40** | **39/40** | **38/40** |

The two order-sensitive examples were PRM Math IDs 4996 and 4885. Jev chose A
in both orders for one and B in both orders for the other. Across 80 calls, the
API reported 57,624 input tokens and 2,560 output tokens; mean request latency
was 233.5 ms.

These results describe a **40-example pilot**, not RewardBench's weighted
leaderboard score. The sample omits many benchmark subsets. Its 10/10 results
have little power to distinguish strong judges, and performance may change on
the full set. [Per-example results](results.jsonl) include IDs, choices, token
counts, and latency, without copying the benchmark's response text or a key.
