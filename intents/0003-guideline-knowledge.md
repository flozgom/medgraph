# Intent: Turn guideline prose into recommendations linked to codes

- **Originator:** Paco
- **Date:** 2026-11-23
- **Status:** proposed
- **Product link:** "guideline prose + coded FHIR" in docs/product.md

## Problem
A guideline PDF says "avoid metformin when eGFR < 30". Nothing connects that sentence to RxNorm
6809 or to a LOINC eGFR code, so no system can apply it to a patient with a citation.

## Desired outcome
Each relevant recommendation becomes a structured record: population concepts, action, target
concept, threshold or interval, and source section. It is linked to the graph and reviewed by a
human before use. Guideline chunks are also searchable by embedding, for the vector baseline.

## Why now
Both detectors (0004) read from it.

## Out of scope
More than one guideline, automatic acceptance without review.

## Open questions (Claude's scoping questions)
- Which guideline: KDIGO 2022 or the ADA CKD section? → OPEN (Paco decides on license and access).
- NER from OpenMed, or entity mentions from Claude? → OpenMed first. Claude mentions are the cut-list
  fallback.

## Success signal
The reviewed `recommendations.yaml` covers the 6 recommendations behind G1–G6, with the right concepts
and thresholds.
