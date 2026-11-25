# Intent: See one patient's gaps and the evidence path in two minutes

- **Originator:** Paco
- **Date:** 2026-11-23
- **Status:** proposed
- **Product link:** "Users" in docs/product.md

## Problem
Tables convince engineers. A reviewer skimming a portfolio needs to see the idea work on one
patient.

## Desired outcome
Pick a patient and see the flags, their citations and the subgraph that links guideline section →
concept → patient resource.

## Why now
Last day, after the numbers exist.

## Out of scope
Auth, deployment, editing data.

## Open questions (Claude's scoping questions)
- Streamlit or static HTML? → Streamlit. A table only, if it gets cut.

## Success signal
Three scripted patients (G1, G3 via a stage code, a clean control) show correct flags and paths.
