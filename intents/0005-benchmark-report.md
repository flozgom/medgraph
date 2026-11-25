# Intent: A measured, honest answer to "does the graph help?"

- **Originator:** Paco
- **Date:** 2026-11-23
- **Status:** proposed
- **Product link:** "Headline metrics" and "Goal" in docs/product.md

## Problem
Without a reproducible comparison, the project is "a medical chatbot". A hiring manager needs a
number they can trust.

## Desired outcome
One command scores the detectors on the test split. It reports P/R/F1 per gap type, citation
accuracy and cost/latency, saves everything under `runs/`, and puts the table in the README,
including results that go against GraphRAG.

The results contract (`medgraph/evals/results.py`) and the regression gate (`medgraph/evals/gate.py`)
already exist. This intent implements `medgraph/evals/run.py` to produce `BenchmarkResult` files, and
records the first dev baseline in `benchmarks/`.

## Why now
It is the deliverable the CV points to.

## Out of scope
Statistical significance beyond bootstrap CIs (and those are on the cut list).

## Open questions (Claude's scoping questions)
- What counts as a match? → Same patient, and the cited section maps to the gold gap's
  recommendation.

## Success signal
`make eval SPLIT=test` prints the table, and the README shows it with the commit and model IDs.
