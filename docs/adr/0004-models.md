# ADR 0004: Model choices

- Status: accepted
- Date: 2026-11-23

## Decision
| Task | Model | Why |
|---|---|---|
| Recommendation extraction from guideline sections | Claude Sonnet (`claude-sonnet-5-5`) | Structured output with tool use; quality matters here |
| Gap judgment (detectors A, B, B−) | Claude Sonnet (`claude-sonnet-5-5`) | Same model for every detector keeps the comparison fair |
| Entity-linking disambiguation among top-k candidates | Claude Haiku (`claude-haiku-5-5`) | High volume, simple choice, low cost |
| Embeddings | local `sentence-transformers` (bge-small) | No cost, deterministic, and the same embeddings for the baseline |
| Biomedical NER | OpenMed models (disease + pharma), revisions pinned in config | Open and reproducible; gives spans and labels, not codes |

- **Prompt caching** covers the system prompt, the graph schema and the guideline context, which repeat
  across patients.
- Model IDs live only in `medgraph/config.py`, and every run logs them.

## Consequences
Swapping a model is a one-line change, and the eval table records which models produced it.
