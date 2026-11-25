---
name: data-contracts
description: Use when writing or reviewing a spec or code that adds a node, relationship, model field or code system in MedGraph, to apply the project's data-contract conventions.
---

# Data contracts in MedGraph

1. Data crossing module boundaries is a pydantic model: `GapFlag` (`medgraph/detect/schema.py`),
   `GoldGap` (`medgraph/gold/schema.py`). No loose dicts between modules.
2. Concepts are identified by `(system, code)`, using the system URIs in `medgraph/config.py`.
   Codes and thresholds live in config, never inline.
3. Neo4j writes are idempotent: `MERGE` on `fhir_id` for resources and on `(system, code)` for
   concepts. Loaders can run twice.
4. FHIR references are written `ResourceType/id`, the same in the graph, `GapFlag.evidence_fhir_ids`
   and the gold labels, so they compare as strings.
5. Dates compare against `config.REFERENCE_DATE`, never `date.today()`.
6. A spec lists every new node label, relationship or model field in a "Contract changes" table.
