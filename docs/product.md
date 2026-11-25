# MedGraph product brief: guideline-aware care-gap detection

The **north star** that every intent points back to. Feature work flows through
`intents/` → `specs/` → `plans/` (see `CLAUDE.md`). This file changes only when the product
direction changes.

## Problem
Clinical guidelines are written in prose, and patient records are coded (FHIR with SNOMED CT, LOINC
and RxNorm). Today the two are bridged by a clinician reading the chart, or by engineers
hand-translating recommendations into rules (CQL / CDS Hooks). The rules are slow to write and
maintain, and they cover a small part of each guideline. Missed monitoring and contraindicated
prescriptions ("care gaps") are a known, measured quality problem. Plain LLM summaries don't close
the gap: they give no provenance and handle concept hierarchies ("is stage 3 CKD a kind of CKD?")
poorly.

## Goal
Show, with measurements, that **guideline prose + coded FHIR + an ontology graph** produces care-gap
flags that are more complete and better cited than vector RAG over the same sources.

## Users (notional)
A clinician or quality analyst who reviews a patient and wants every flag to carry evidence they can
check: the FHIR resource IDs and the guideline section. The secondary audience is a hiring manager
for LLM/AI engineer roles, who reads the README and the results table.

## Scope
- **Domain:** type 2 diabetes (T2DM) plus chronic kidney disease (CKD).
- **Guideline:** one public PDF (KDIGO 2022 *Diabetes Management in CKD*, or the ADA Standards of
  Care CKD section), downloaded by script and never committed.
- **Data:** Synthea FHIR R4, about 150 patients after filtering, split into **dev (50)** and
  **test (100)**.

### Gap types (detailed in spec 0001)
| id | Gap | Graph capability exercised |
|---|---|---|
| G1 | Metformin active while latest eGFR < 30 | multi-hop: drug → ingredient, lab threshold |
| G2 | T2DM with no HbA1c in the last 6 months | temporal + LOINC |
| G3 | CKD (any stage) with no eGFR in the last 12 months | SNOMED IS-A |
| G4 | Diabetes + CKD with no UACR in the last 12 months | IS-A on two conditions |
| G5 | T2DM + CKD (eGFR ≥ 20) not on any SGLT2 inhibitor | drug class (ATC A10BK) |
| G6 | CKD with an active NSAID | drug class (ATC M01A) + IS-A |

### Detectors compared
- **A: vector RAG**: a text summary of the patient plus the top-k guideline chunks go to Claude.
- **B: GraphRAG**: recommendations whose population subsumes a patient condition, plus templated
  Cypher facts, go to Claude, which judges each pair.
- **B−: ablation**: B with exact code matching only (no IS-A, no drug classes).

### Headline metrics
P/R/F1 per gap type against the rule oracle, citation accuracy, and tokens/USD/latency per patient.

## Non-goals
Clinical validity, multiple guidelines, EHR integration, EU MDR / SaMD compliance, real PHI, and a
production UI.

## Roadmap (about one week, intent per feature)
| # | Intent | Day | Depends on |
|---|---|---|---|
| 0001 | [Care-gap ground truth](../intents/0001-care-gap-ground-truth.md) | 1 | none |
| 0002 | [Clinical graph](../intents/0002-clinical-graph.md) | 2 | 0001 data |
| 0003 | [Guideline knowledge](../intents/0003-guideline-knowledge.md) | 3 | 0002 |
| 0004 | [Gap detectors](../intents/0004-gap-detectors.md) | 4 | 0002, 0003 |
| 0005 | [Benchmark report](../intents/0005-benchmark-report.md) | 5 | 0001, 0004 |
| 0006 | [Evidence demo](../intents/0006-evidence-demo.md) | 5 | 0004 |

**Cut list, in order:** Text2Cypher → bootstrap CIs → CI eval smoke → NER on chunks (link from
Claude-extracted mentions instead) → demo graph view (show a table instead).

Architecture decisions that cut across features live in `docs/adr/`.
