# Review passes for Claude PR review

Run these passes in order. Report findings only. **Findings never approve a PR**: Paco merges.

## Severity
- **blocker**: wrong behaviour, label leakage, licensing breach, or a broken architecture rule in CLAUDE.md
- **major**: missing test for an acceptance criterion, a metric computed differently than the spec says
- **minor**: readability, naming
- **nit**: style. **Max 3 nits per PR.** Ruff already handles formatting.

## Pass 1: Correctness against spec and plan
- Does the diff satisfy every acceptance criterion in the linked `specs/` file?
- Did it follow the linked `plans/` file, or explain why not?
- Is there one test per AC, named `test_ac<N>_…`?

## Pass 2: Clinical-data bugs
- Off-by-one in time windows ("in the last 12 months"), uses of `date.today()` instead of
  `REFERENCE_DATE`, timezone-naive comparisons.
- "Latest" lab means the most recent by effective date, not file order.
- "Active" medication means status and period, not just the presence of a MedicationRequest.
- Units: eGFR in mL/min/1.73m², HbA1c in %. Watch for silent unit mismatches.

## Pass 3: Eval hygiene (`eval-hygiene` skill)
- Any import of `medgraph.gold` or any mention of G1–G6 in `medgraph/detect/` or prompts → **blocker**.
- Any change to the oracle or gold labels outside spec 0001 → **blocker**.
- Did prompt or retrieval tuning use test-split results? → **blocker**.
- Do runs record the SHA, model IDs, prompts and tokens?
- PR touches `detect/`, `extract/`, `ingest/` or prompts, but no `make eval-gate` output in the
  description → **major**. A gate FAIL with no explanation → **blocker**.
- A change to `benchmarks/dev-baseline.json` without a stated reason → **blocker**.
- Feature PR without a new or updated agent eval in `evals/tasks/` (or a reason) → **minor**.

## Pass 4: Licensing & privacy (`clinical-data-licensing` skill)
- SNOMED terms, RF2 content, PDFs or anything under `data/` in the diff → **blocker**.
- A new external service not listed in the spec → **major**.

## Pass 5: Architecture
- No new runtime dependency unless the spec allows it.
- Were tests weakened? Any deleted or loosened assertion is a **blocker**.

## Output format
`[severity] file:line: finding (suggested fix)`. End with: "Spec ACs met: X/Y".
If a mistake appears that CLAUDE.md should have prevented, suggest a one-line addition under
Corrections.
