"""Benchmark results contract (intent 0005). `make eval` writes one BenchmarkResult per run to
runs/<timestamp>/results.json and runs/latest/results.json; the regression gate reads it."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

DetectorName = Literal["vector", "graph", "graph_no_isa"]


class Scores(BaseModel):
    precision: float = Field(ge=0, le=1)
    recall: float = Field(ge=0, le=1)
    f1: float = Field(ge=0, le=1)


class DetectorResult(BaseModel):
    micro: Scores
    per_gap: dict[str, Scores] = Field(default_factory=dict)
    citation_accuracy: float = Field(ge=0, le=1)
    usd_per_patient: float = 0.0
    latency_s_per_patient: float = 0.0


class BenchmarkResult(BaseModel):
    split: Literal["dev", "test"]
    git_sha: str
    n_patients: int
    models: dict[str, str] = Field(default_factory=dict)
    detectors: dict[DetectorName, DetectorResult]
