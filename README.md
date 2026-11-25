# MedGraph

**Guideline-aware care-gap detection with GraphRAG over FHIR and medical ontologies,** built with an
AI-native SDLC.

Clinical guidelines are prose, and patient records are coded. MedGraph links one guideline PDF to
SNOMED CT, LOINC and RxNorm, matches it against synthetic FHIR patients in a Neo4j graph, and flags
care gaps with citations (FHIR resource IDs + guideline section). It measures **vector RAG vs
GraphRAG** against a rule-oracle ground truth. See [`docs/product.md`](docs/product.md).

> Status: process scaffold in place; intents 0001–0006 proposed. Results table to come (intent 0005).

## How this repo is built
It follows [The AI-Native SDLC Playbook](https://claude.com/resources/articles/the-ai-native-sdlc-playbook):
each stage commits a **version-controlled artifact** that the next stage reads. Claude drafts each
artifact, and a human (Paco) keeps judgement at every gate.

```
intent.md ──► spec.md ──► plan.md ──► failing AC tests ──► code ──► verifier ──► PR review ──► merge
    ▲                                                                                         │
    └──────────── a wrong result or a bug becomes a new intent; a fix becomes a test ◄────────┘
```

| Stage | Play | In this repo |
|---|---|---|
| **1. Plan** | Capture intent | [`intents/_template.md`](intents/_template.md); features [`0001`–`0006`](intents/) traced to [`docs/product.md`](docs/product.md) |
| **2. Design** | Intent → spec with project skills | [`/spec-from-intent`](.claude/commands/spec-from-intent.md) applies [`data-contracts`](.claude/skills/data-contracts/SKILL.md), [`clinical-data-licensing`](.claude/skills/clinical-data-licensing/SKILL.md), [`eval-hygiene`](.claude/skills/eval-hygiene/SKILL.md) → [`specs/`](specs/). Decisions → [`docs/adr/`](docs/adr/) |
| **3. Build** | Plan mode first | [`/plan-from-spec`](.claude/commands/plan-from-spec.md) → [`plans/`](plans/); no code before the plan is accepted |
| | `CLAUDE.md` | [`CLAUDE.md`](CLAUDE.md): workflow, architecture rules, Corrections |
| | Hooks as guardrails | [`protect_paths`](.claude/hooks/protect_paths.py) (CI, hooks, SNOMED; `gold-lock`; `fix-mode`), [`no_secrets`](.claude/hooks/no_secrets.py) (keys, SNOMED RF2 content), [`git_gate`](.claude/hooks/git_gate.py) (no push to main, no staging `data/`), [`format_changed`](.claude/hooks/format_changed.py) |
| | Subagents | [`verifier`](.claude/agents/verifier.md): judges each AC, checks for leakage, never edits |
| **4. Test** | One feedback-loop command | `make check` (lint, types, license check, tests, hook self-test), the same locally and in [CI](.github/workflows/ci.yml) |
| | Failing test first | `test_ac<N>_…` per spec AC; [`/fix-bug`](.claude/commands/fix-bug.md) with tests locked |
| | Continuous agent evals | [`evals/tasks/`](evals/tasks) + [`run_evals.py`](scripts/run_evals.py) in [`evals.yml`](.github/workflows/evals.yml): run on any `CLAUDE.md` / `.claude/` change, gated at 80%. Seed tasks guard label leakage, SNOMED licensing and gold-lock |
| | Product evals | vector vs GraphRAG benchmark (intent 0005), with labels locked by `gold-lock`; [`make eval-gate`](medgraph/evals/gate.py) fails on an F1 or citation drop against the [`benchmarks/`](benchmarks/) baseline |
| **5. Deploy** | AI in PR review | [`REVIEW.md`](REVIEW.md) (with eval-hygiene and licensing passes); [`CODEOWNERS`](.github/CODEOWNERS): only a human approves |
| **6. Maintain** | Close the loop | _later_: benchmark regressions become intents, and agent mistakes become Corrections and agent evals |

The two kinds of "evals" are different things:
- **Product evals** (`medgraph/evals/`) measure the care-gap detectors. The dev split is gated
  against a baseline that only a human moves, and the test split is run once and reported.
- **Agent evals** (`evals/tasks/`) replay tasks in throwaway worktrees, to check that changes to
  `CLAUDE.md` or the skills don't make Claude worse at working here. They start from 3 guardrail
  seed tasks, and each feature PR adds one from its real work.

## Quick start
```bash
uv sync
make check
docker compose up -d
```

## Bring your own SNOMED CT
SNOMED CT is licensed and is **not** included. Put your release in `data/snomed/` (gitignored).
`make check` fails if SNOMED release content is ever committed. Tests run on a small fixture made of
Synthea-emitted codes.

## Limits
This is a reproducible proof of concept of an approach. It is not a clinical product: no clinical
validation, no EHR integration, and no EU MDR / SaMD compliance. All patient data is synthetic
(Synthea).
