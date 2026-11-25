# Benchmarks

`dev-baseline.json` is the committed reference for the product-eval regression gate
(`make eval-gate`, `medgraph/evals/gate.py`). It is a `BenchmarkResult`
(`medgraph/evals/results.py`) from a dev-split run.

- It is created once intent 0005 is implemented. Until then the gate prints a notice and passes.
- **Only Paco moves the baseline** (the `protect_paths` hook blocks agent edits here). Move it when
  a PR deliberately improves the detectors, or when the cohort changes on purpose, and say why in
  the PR.
- The test split is never a baseline. It runs once and goes into the README.
