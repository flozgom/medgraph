# MedGraph: notes for Claude (and new joiners)

Guideline-aware **care-gap detection** POC: guideline PDF → recommendations linked to
SNOMED/LOINC/RxNorm → matched against Synthea FHIR patients in Neo4j → care-gap flags with
citations. The headline result is **vector RAG vs GraphRAG**, scored against a rule oracle.
The product brief is `docs/product.md`. Cross-cutting decisions are in `docs/adr/`.

## Commands
- `make check`: lint + types + license check + tests + hook self-test + agent-eval task validation.
  **The only definition of "done".** Must exit 0.
- `docker compose up -d`: Neo4j on bolt://localhost:7687 (neo4j / medgraph-dev).
- Pipeline: `make data` (0001) · `make graph` (0002) · `make extract` (0003) · `make eval SPLIT=dev` (0005).

## Two kinds of evals (don't mix them up)
- **Product evals** (`medgraph/evals/`): do the care-gap detectors work? `make eval SPLIT=dev` writes
  `runs/latest/results.json`. `make eval-gate` fails if F1 or citation accuracy drops against
  `benchmarks/dev-baseline.json`. PRs that touch `detect/`, `extract/`, `ingest/` or prompts paste
  the gate output. Only Paco moves the baseline.
- **Agent evals** (`evals/tasks/`, `make agent-evals`): is Claude still good at working in this repo?
  They replay tasks in throwaway worktrees, and CI runs them when `CLAUDE.md` or `.claude/` changes.
  Each feature PR adds one task from its real work. Each new Correction below gets a task too.
  Task files are protected, so propose new ones in the PR summary.

## How work flows here
intent (`intents/`) → spec (`specs/`) → plan (`plans/`) → failing AC tests → code → `verifier` → PR
(`REVIEW.md`).
- Intents are `proposed` until Paco accepts them. `/spec-from-intent NNNN` runs only on accepted ones.
- `/plan-from-spec NNNN` runs only on approved specs. **Never write code without an accepted plan.**
  Start sessions in plan mode.
- The number NNNN is shared: `intents/0001-x.md` ↔ `specs/0001-x.md` ↔ `plans/0001-x.md`.
- One feature per branch/PR. The PR description links intent → spec → plan.

## Architecture rules
- `medgraph/detect/` never imports `medgraph.gold`, and never mentions G1–G6 (enforced by
  `tests/test_architecture.py`).
- Data crossing modules is pydantic: `GapFlag` (`detect/schema.py`), `GoldGap` (`gold/schema.py`).
- Codes, thresholds, model IDs and paths live only in `medgraph/config.py`.
- Neo4j writes are idempotent (`MERGE` on `fhir_id` / `(system, code)`).
- Dates compare against `config.REFERENCE_DATE`, never `date.today()`.
- No new runtime dependency without a spec that says so. Heavy ML deps go in optional extras.

## Data rules (enforced by hooks and `make check`)
- **SNOMED CT is licensed.** It lives only in `data/snomed/` (gitignored). Never write its terms into
  the repo. Concept IDs are fine.
- Nothing under `data/` and no PDFs are ever committed.
- Tune on `dev` only. `test` runs are recorded in `runs/` and the README, whatever the result.

## Testing rules
- Name acceptance tests `test_ac<N>_…` after the spec's criteria. Write them first and see them fail.
- Bug fix → `/fix-bug`, with a failing test first.
- Never delete, skip or loosen an existing assertion to make something pass. Stop and report instead.
- Tests that need Neo4j or the Claude API are marked `neo4j` / `llm` and excluded from `make check`.

## Guardrail switches
- `.claude/gold-lock`: the oracle and gold labels become read-only. Turn it on once 0001 merges.
- `.claude/fix-mode`: `tests/` becomes read-only during `/fix-bug`.

## Corrections (added when Claude made the same mistake twice)
- _none yet_
