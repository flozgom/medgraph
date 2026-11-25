# Intent: Flag care gaps with evidence a clinician can check

- **Originator:** Paco
- **Date:** 2026-11-23
- **Status:** proposed
- **Product link:** "Detectors compared" in docs/product.md

## Problem
Even with a graph and recommendations, nothing yet says "this patient has this gap, and here are the
resources and the guideline section that show it".

## Desired outcome
Three detectors (vector RAG, GraphRAG, GraphRAG without IS-A) take a patient and return the same
`GapFlag` structure, citing FHIR IDs and a section ID. They see only the guideline, graph and
patient data, never the labels.

## Why now
They are what the benchmark (0005) measures.

## Out of scope
Text2Cypher (stretch), UI, tuning on test.

## Open questions (Claude's scoping questions)
- Judge each (patient, recommendation) pair separately, or all at once? → Per pair for GraphRAG.
  The baseline gets everything in one call, as vector RAG normally does.

## Success signal
On dev, all three run end to end for 50 patients and every flag parses and cites resources that
exist.
