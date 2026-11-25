"""Single source of truth for paths, model IDs and clinical codes.

Codes marked VERIFY must be checked against what Synthea actually emits (Day 1, step 5)
before the oracle is trusted.
"""

from __future__ import annotations

import os
from datetime import date
from pathlib import Path

# --- Paths -------------------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SYNTHEA_OUT = DATA / "synthea" / "fhir"
BUNDLES = DATA / "bundles"  # filtered + planted bundles, split into dev/ and test/
GOLD = DATA / "gold" / "gaps.jsonl"
PLANTED_LOG = DATA / "gold" / "planted.jsonl"
SNOMED_DIR = DATA / "snomed"  # gitignored, licensed: never commit
GUIDELINE_PDF = DATA / "guideline" / "guideline.pdf"
RECOMMENDATIONS = DATA / "recommendations.yaml"
RXCLASS_CACHE = DATA / "rxclass_cache.json"
RUNS = ROOT / "runs"

# --- Reproducibility ---------------------------------------------------------------------------
SEED = 42
REFERENCE_DATE = date(2026, 1, 1)  # "today" for every temporal rule; set to the Synthea end date
SPLITS = {"dev": 50, "test": 100}

# --- Neo4j -------------------------------------------------------------------------------------
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "medgraph-dev")

# --- Models (ADR 0004) -------------------------------------------------------------------------
MODEL_JUDGE = "claude-sonnet-5-5"
MODEL_EXTRACT = "claude-sonnet-5-5"
MODEL_LINK = "claude-haiku-5-5"
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
OPENMED_MODELS: dict[str, str] = {
    # Pick from the OpenMed HF org and pin the revisions (Day 3).
    "disease": "",
    "pharma": "",
}

# --- Code systems ------------------------------------------------------------------------------
SNOMED = "http://snomed.info/sct"
LOINC = "http://loinc.org"
RXNORM = "http://www.nlm.nih.gov/research/umls/rxnorm"
ATC = "http://www.whocc.no/atc"
IS_A_TYPE_ID = "116680003"

# --- Clinical concepts used by the oracle (VERIFY against Synthea output) ----------------------
SNOMED_T2DM = "44054006"  # Diabetes mellitus type 2
SNOMED_CKD = "709044004"  # Chronic kidney disease (parent of the stage codes)
SNOMED_CKD_STAGES = {
    "431855005",  # CKD stage 1
    "431856006",  # CKD stage 2
    "433144002",  # CKD stage 3
    "431857002",  # CKD stage 4
    "46177005",  # End-stage renal disease
}

LOINC_EGFR = {"33914-3", "62238-1", "98979-8"}  # VERIFY which ones Synthea emits
LOINC_HBA1C = {"4548-4"}
LOINC_UACR = {"14959-1", "9318-7"}  # VERIFY

RXNORM_METFORMIN_INGREDIENT = "6809"
ATC_SGLT2 = "A10BK"
ATC_NSAID = "M01A"

# --- Gap thresholds (spec.md) ------------------------------------------------------------------
EGFR_METFORMIN_STOP = 30.0
EGFR_SGLT2_MIN = 20.0
HBA1C_INTERVAL_DAYS = 183
EGFR_INTERVAL_DAYS = 365
UACR_INTERVAL_DAYS = 365
