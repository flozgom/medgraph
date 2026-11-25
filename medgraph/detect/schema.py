"""Shared detector output: every detector emits GapFlags, so all are scored identically.

Detectors must not import medgraph.gold (eval-hygiene skill, enforced by
tests/test_architecture.py).
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class GapFlag(BaseModel):
    """One detector claim: this patient has (or does not have) a gap against a guideline section."""

    patient_id: str
    recommendation_section_id: str = Field(description="Guideline section that the flag cites")
    description: str = Field(description="Short human-readable statement of the gap")
    gap: bool = True
    evidence_fhir_ids: list[str] = Field(
        default_factory=list, description="FHIR references as 'ResourceType/id'"
    )
    reason: str = ""
