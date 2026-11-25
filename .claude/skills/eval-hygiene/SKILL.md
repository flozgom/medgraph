---
name: eval-hygiene
description: Use when writing a spec, code or prompts for the oracle, detectors or benchmark in MedGraph, so the comparison between vector RAG and GraphRAG stays fair and reproducible.
---

# Eval hygiene (owner: Paco)

1. **The labels are sacred.** Gold labels come only from `medgraph/gold/oracle.py`. Never edit
   `data/gold/` by hand. Once 0001 is done, `.claude/gold-lock` makes the oracle read-only.
2. **No leakage.** Detector code (`medgraph/detect/`) never imports `medgraph.gold`, and prompts never
   contain gap-type IDs (G1–G6), the oracle rules or the planted log. `tests/test_architecture.py`
   enforces the import rule.
3. **Dev for tuning, test once.** Prompt and retrieval changes are judged on `dev`. A test run is
   recorded in `runs/` and in the README, whatever the result.
4. **Same contract, same judge.** All detectors return `GapFlag` and use the same judge model (from
   config). Differences come from retrieval only.
5. **Every run is reproducible.** `runs/<timestamp>/` records the git SHA, model IDs, prompts,
   token counts and raw outputs.
6. **Regressions are gated on dev only.** `make eval-gate` compares dev results with
   `benchmarks/dev-baseline.json`. Never "fix" a gate failure by editing the baseline, the oracle or
   the tolerance. Explain the drop, or fix the detector.
7. **Report what you found.** If B does not beat A, the spec's success signal says so. Do not change
   metrics after seeing test results.
