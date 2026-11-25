---
name: clinical-data-licensing
description: Use when writing a spec, code, tests or fixtures that touch SNOMED CT, LOINC, RxNorm/ATC, guideline PDFs or patient data in MedGraph, to apply licensing and privacy rules.
---

# Clinical data licensing and privacy (owner: Paco)

1. **SNOMED CT is licensed.** Raw releases, term CSVs and derived subsets that contain terms live only
   in `data/snomed/` (gitignored). Never write SNOMED terms into `medgraph/`, `tests/` or `docs/`.
   Concept IDs are allowed in code and docs.
2. **Fixtures** use only the codes and display strings that Synthea emits, plus hand-written IS-A edges
   between those codes.
3. **Guideline PDFs** are downloaded by `scripts/fetch_guideline.sh` into `data/`. Short quoted
   recommendation sentences in specs and the README are fine; whole sections are not.
4. **LOINC**: a hand-picked subset in config is fine (LOINC license, with attribution in the README).
   **RxNorm/ATC** via the NLM RxNav API: cache to `data/`, and respect the rate limit.
5. **Patient data is synthetic only (Synthea).** No real PHI, ever, including in prompts and logs.
6. Any new external service (API, model download, dataset) goes in the spec under
   "⚠ Flagged for the product owner".

This skill is advisory. `scripts/check_license_clean.py` (run by `make check`) and the hooks
enforce rules 1–2.
