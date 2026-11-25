"""Gold-label contract. Owned by the oracle and the benchmark; detectors must never import this."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field


class GapType(StrEnum):
    """Gold gap types (docs/product.md, spec 0001)."""

    G1 = "G1"  # metformin active with eGFR < 30
    G2 = "G2"  # T2DM, no HbA1c in 6 months
    G3 = "G3"  # CKD, no eGFR in 12 months
    G4 = "G4"  # diabetes + CKD, no UACR in 12 months
    G5 = "G5"  # T2DM + CKD (eGFR >= 20), no SGLT2 inhibitor
    G6 = "G6"  # CKD with active NSAID


class GoldGap(BaseModel):
    """One row of data/gold/gaps.jsonl, produced only by medgraph/gold/oracle.py."""

    patient_id: str
    gap_type: GapType
    evidence_fhir_ids: list[str] = Field(default_factory=list)
