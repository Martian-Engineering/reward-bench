# Jev pairwise pilot

`scripts/run_jev.py` evaluates a TypeSafe System One choice model on a seeded
sample of RewardBench v1's public `filtered` split. For each example, it sends
the user prompt and two candidate responses as choices A and B. It repeats the
question with the answer order reversed. Results contain both choices, the
benchmark's preferred answer, token use, and latency. The output is JSON Lines
and records only dataset IDs, not the prompt or candidate text.

```sh
uv run --no-project --with datasets python scripts/run_jev.py --dry-run
uv run --no-project --with datasets python scripts/run_jev.py \
  --output jev-rewardbench-pilot.jsonl
```

The live command reads `TYPESAFE_API_KEY` from the process environment and
defaults to `jev-1.13.0`. It selects ten examples each from `alpacaeval-hard`,
`llmbar-natural`, `xstest-should-respond`, and `math-prm` using seed 100.
`--subsets`, `--per-subset`, and `--seed` change the sample. The output path
must be new so a rerun cannot overwrite earlier results.

Report ordinary accuracy for each answer order separately. Also report the
fraction of examples answered correctly in both orders; this stricter number
shows how often a decision survives swapping A and B. The pilot does not
reproduce RewardBench's full-set weighted leaderboard score. The benchmark's
preferred answer reflects helpfulness, instruction following, factuality,
reasoning, or safety depending on its subset, not literary style alone.
