"""The product-eval regression gate must catch real drops and refuse unfair comparisons."""

from pathlib import Path

import pytest

from medgraph.evals.gate import GateError, compare, main
from medgraph.evals.results import BenchmarkResult, DetectorResult, Scores


def _result(
    graph_f1: float = 0.80,
    graph_citations: float = 0.90,
    split: str = "dev",
    n_patients: int = 50,
    include_vector: bool = True,
) -> BenchmarkResult:
    def det(f1: float, cit: float) -> DetectorResult:
        return DetectorResult(micro=Scores(precision=f1, recall=f1, f1=f1), citation_accuracy=cit)

    detectors = {"graph": det(graph_f1, graph_citations)}
    if include_vector:
        detectors["vector"] = det(0.55, 0.60)
    return BenchmarkResult.model_validate(
        {
            "split": split,
            "git_sha": "abc12345",
            "n_patients": n_patients,
            "detectors": {k: v.model_dump() for k, v in detectors.items()},
        }
    )


def test_passes_when_scores_hold() -> None:
    assert compare(_result(), _result(graph_f1=0.79)) == []


def test_flags_f1_drop_beyond_tolerance() -> None:
    regressions = compare(_result(), _result(graph_f1=0.70))
    assert len(regressions) == 1
    assert regressions[0].startswith("graph: micro F1")


def test_flags_citation_drop_beyond_tolerance() -> None:
    regressions = compare(_result(), _result(graph_citations=0.80))
    assert any("citation accuracy" in r for r in regressions)


def test_flags_detector_missing_from_current_run() -> None:
    assert compare(_result(), _result(include_vector=False)) == ["vector: missing from current run"]


def test_refuses_to_gate_on_test_split() -> None:
    with pytest.raises(GateError, match="only dev"):
        compare(_result(split="test"), _result(split="test"))


def test_refuses_different_patient_counts() -> None:
    with pytest.raises(GateError, match="patient counts differ"):
        compare(_result(), _result(n_patients=40))


def test_cli_fails_on_regression(tmp_path: Path) -> None:
    base, cur = tmp_path / "base.json", tmp_path / "cur.json"
    base.write_text(_result().model_dump_json())
    cur.write_text(_result(graph_f1=0.60).model_dump_json())
    assert main(["--baseline", str(base), "--current", str(cur)]) == 1


def test_cli_passes_without_baseline_yet(tmp_path: Path) -> None:
    assert main(["--baseline", str(tmp_path / "none.json"), "--current", str(tmp_path / "x")]) == 0
