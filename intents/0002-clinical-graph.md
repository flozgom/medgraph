# Intent: Query patients by concept family, not just exact codes

- **Originator:** Paco
- **Date:** 2026-11-23
- **Status:** proposed
- **Product link:** the "graph capability" column of the gap types in docs/product.md

## Problem
FHIR codes are precise leaves: "CKD stage 3", "empagliflozin 10 MG tablet". Guidelines speak in
families: "CKD", "SGLT2 inhibitors", "NSAIDs". Exact-code lookups miss the link, and so does
embedding similarity.

## Desired outcome
Patients, their conditions, labs and medications sit in a graph, connected to ontology concepts with
IS-A, ingredient and drug-class edges, so one query answers "patients with any CKD" or "patients on
any SGLT2 inhibitor".

## Why now
GraphRAG (0004) and the IS-A ablation depend on it.

## Out of scope
Full SNOMED load, a FHIR server, guideline content (0003).

## Open questions (Claude's scoping questions)
- Does Paco's SNOMED CSV include parent links? → OPEN. If not, use the RF2 relationships file.
- Where do drug classes come from? → NLM RxClass (RxNorm → ATC), cached locally.

## Success signal
A Cypher query for "any CKD" returns the stage 3 and stage 4 patients. One for "any SGLT2 inhibitor"
returns the patients on empagliflozin products. Both hold on the license-free fixture in CI.
