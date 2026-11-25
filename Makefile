SPLIT ?= dev
RUN ?= uv run

.PHONY: check lint test license hooks agent-evals-check agent-evals install data graph extract eval eval-gate demo

# The single feedback-loop command: the only definition of "done". Same locally, for the agent,
# and in CI.
check: lint license test hooks agent-evals-check

lint:
	$(RUN) ruff check .
	$(RUN) ruff format --check .
	$(RUN) mypy

license:
	$(RUN) python scripts/check_license_clean.py

test:
	$(RUN) pytest -q

hooks:
	bash scripts/test_hooks.sh

# ---- Agent evals: is Claude still good at working in this repo? (Stage 4) -------------------
agent-evals-check:  ## validate task files only (cheap, part of check)
	$(RUN) python scripts/run_evals.py --dry-run

agent-evals:        ## replay evals/tasks with the claude CLI (costs API tokens)
	$(RUN) python scripts/run_evals.py --min-pass-rate 0.8

install:
	uv sync --all-extras

# ---- Pipeline targets (implemented by intents 0001-0006) ------------------------------------
data:      ## 0001: Synthea generate -> plant gaps -> oracle gold (needs Java 17+)
	./scripts/generate_synthea.sh
	$(RUN) python -m medgraph.synthea.plant_gaps
	$(RUN) python -m medgraph.gold.oracle

graph:     ## 0002: ontology subset + FHIR into Neo4j
	$(RUN) python -m medgraph.ingest.ontology
	$(RUN) python -m medgraph.ingest.fhir

extract:   ## 0003: guideline -> sections/chunks -> NER -> linking -> recommendations
	./scripts/fetch_guideline.sh
	$(RUN) python -m medgraph.ingest.guideline
	$(RUN) python -m medgraph.extract.recommendations

eval:      ## 0005: product evals, vector vs graph vs graph-no-isa -> runs/latest/results.json
	$(RUN) python -m medgraph.evals.run --split $(SPLIT)

eval-gate: ## product-eval regression gate: dev run vs benchmarks/dev-baseline.json
	$(MAKE) eval SPLIT=dev
	$(RUN) python -m medgraph.evals.gate

demo:      ## 0006
	$(RUN) streamlit run app/streamlit_app.py
