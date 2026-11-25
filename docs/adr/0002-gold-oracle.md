# ADR 0002: Ground truth from a hand-coded rule oracle plus planted gaps

- Status: accepted
- Date: 2026-11-23

## Context
Care-gap detection needs labelled data. Real labelled data is not available without PHI. Synthea
patients are synthetic, and their natural gaps are unknown.

## Decision
- `medgraph/gold/oracle.py` implements G1–G6 as deterministic Python rules over FHIR bundles. It is
  the "CQL" that the system tries to make unnecessary. It labels **every** patient, so gaps that
  Synthea creates naturally are counted.
- `medgraph/synthea/plant_gaps.py` mutates a seeded subset of bundles so that each gap type has
  enough positives, and records what it planted. The planted log is only a cross-check. The oracle
  output is the gold.
- Gold format: `data/gold/gaps.jsonl` with `{patient_id, gap_type, evidence_fhir_ids}`.

## Leakage controls
Detector prompts never include the oracle, the gap-type list or the planted log. They see only the
guideline, graph facts and patient data. Prompt iteration uses `dev` only.

## Consequences
The labels are reproducible and auditable. Their limit: the oracle encodes *our* reading of the
guideline, and the README says so.
