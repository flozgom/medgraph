"""Product-eval regression gate: compare the latest dev benchmark with the committed baseline.

Fails when any detector's micro F1 or citation accuracy drops by more than the tolerance.
Only the dev split can be gated: gating on test would mean tuning on test (eval-hygiene skill).
Updating the baseline is a human decision (`benchmarks/` is protected by the protect_paths hook).

Usage:
  python -m medgraph.evals.gate                      # runs/latest vs benchmarks/dev-baseline.json
  python -m medgraph.evals.gate --current X --baseline Y --max-f1-drop 0.03
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from medgraph.config import ROOT, RUNS
from medgraph.evals.results import BenchmarkResult

BASELINE = ROOT / "benchmarks" / "dev-baseline.json"
CURRENT = RUNS / "latest" / "results.json"


class GateError(ValueError):
    """The two results cannot be compared fairly."""


def compare(
    baseline: BenchmarkResult,
    current: BenchmarkResult,
    max_f1_drop: float = 0.03,
    max_citation_drop: float = 0.05,
) -> list[str]:
    """Return one message per regression; an empty list means the gate passes."""
    if baseline.split != "dev" or current.split != "dev":
        raise GateError("only dev results can be gated; test is run once and reported")
    if baseline.n_patients != current.n_patients:
        raise GateError(
            f"patient counts differ ({baseline.n_patients} vs {current.n_patients}): "
            "regenerate the baseline deliberately instead of comparing"
        )

    regressions: list[str] = []
    for name, base in baseline.detectors.items():
        cur = current.detectors.get(name)
        if cur is None:
            regressions.append(f"{name}: missing from current run")
            continue
        f1_drop = base.micro.f1 - cur.micro.f1
        if f1_drop > max_f1_drop:
            regressions.append(
                f"{name}: micro F1 {base.micro.f1:.3f} -> {cur.micro.f1:.3f} "
                f"(-{f1_drop:.3f} > {max_f1_drop})"
            )
        cit_drop = base.citation_accuracy - cur.citation_accuracy
        if cit_drop > max_citation_drop:
            regressions.append(
                f"{name}: citation accuracy {base.citation_accuracy:.3f} -> "
                f"{cur.citation_accuracy:.3f} (-{cit_drop:.3f} > {max_citation_drop})"
            )
    return regressions


def delta_table(baseline: BenchmarkResult, current: BenchmarkResult) -> str:
    lines = [
        "| detector | F1 base | F1 now | Δ | citations base | citations now |",
        "|---|---|---|---|---|---|",
    ]
    for name, cur in current.detectors.items():
        base = baseline.detectors.get(name)
        if base is None:
            lines.append(
                f"| {name} | new | {cur.micro.f1:.3f} | | new | {cur.citation_accuracy:.3f} |"
            )
            continue
        lines.append(
            f"| {name} | {base.micro.f1:.3f} | {cur.micro.f1:.3f} | "
            f"{cur.micro.f1 - base.micro.f1:+.3f} | {base.citation_accuracy:.3f} | "
            f"{cur.citation_accuracy:.3f} |"
        )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--current", type=Path, default=CURRENT)
    parser.add_argument("--baseline", type=Path, default=BASELINE)
    parser.add_argument("--max-f1-drop", type=float, default=0.03)
    parser.add_argument("--max-citation-drop", type=float, default=0.05)
    args = parser.parse_args(argv)

    if not args.baseline.exists():
        print(f"eval-gate: no baseline at {args.baseline} yet (created by Paco after intent 0005).")
        return 0
    if not args.current.exists():
        print(f"eval-gate: no current results at {args.current}. Run `make eval SPLIT=dev`.")
        return 1

    baseline = BenchmarkResult.model_validate_json(args.baseline.read_text())
    current = BenchmarkResult.model_validate_json(args.current.read_text())
    try:
        regressions = compare(baseline, current, args.max_f1_drop, args.max_citation_drop)
    except GateError as err:
        print(f"eval-gate: cannot compare: {err}", file=sys.stderr)
        return 1

    print(f"eval-gate: baseline {baseline.git_sha[:8]} vs current {current.git_sha[:8]}")
    print(delta_table(baseline, current))
    for message in regressions:
        print(f"REGRESSION {message}", file=sys.stderr)
    print("eval-gate: FAIL" if regressions else "eval-gate: PASS")
    return 1 if regressions else 0


if __name__ == "__main__":
    sys.exit(main())
