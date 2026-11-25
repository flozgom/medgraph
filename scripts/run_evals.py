"""Agent evals (playbook Stage 4: continuous evals).

Replays tasks (evals/tasks/*.yaml) against the current CLAUDE.md, skills and hooks, each in a
throwaway git worktree, and reports a pass rate. They check that changes to the agent's
configuration don't make Claude worse at working in this repo. This is different from the
product evals in medgraph/evals/, which measure the care-gap detectors.

Tasks come from real work: every feature PR (0001-0006) adds one, and every repeated agent
mistake adds one alongside its line under Corrections in CLAUDE.md.

Usage:
  python scripts/run_evals.py --dry-run            # validate task files (part of make check)
  python scripts/run_evals.py                      # run all (needs the claude CLI + API key)
  python scripts/run_evals.py --only 001 --min-pass-rate 0.8
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
TASKS = ROOT / "evals" / "tasks"
RESULTS = ROOT / "runs" / "agent-evals"
REQUIRED = ("id", "title", "source", "guards", "prompt", "success_command")


def load_task(path: Path) -> dict[str, str]:
    task = yaml.safe_load(path.read_text())
    if not isinstance(task, dict):
        raise ValueError(f"{path.name}: not a mapping")
    missing = [key for key in REQUIRED if not task.get(key)]
    if missing:
        raise ValueError(f"{path.name}: missing {missing}")
    if not path.name.startswith(f"{task['id']}-"):
        raise ValueError(f"{path.name}: file name must start with its id {task['id']!r}")
    return {key: str(value) for key, value in task.items()}


def run_task(task: dict[str, str]) -> bool:
    workdir = Path(tempfile.mkdtemp(prefix=f"medgraph-eval-{task['id']}-"))
    subprocess.run(["git", "worktree", "add", "--detach", str(workdir)], cwd=ROOT, check=True)
    try:
        if task.get("setup"):
            subprocess.run(task["setup"], shell=True, cwd=workdir, check=True)
        subprocess.run(
            [
                "claude",
                "-p",
                task["prompt"],
                "--permission-mode",
                "acceptEdits",
                "--max-turns",
                task.get("max_turns", "30"),
            ],
            cwd=workdir,
            check=False,
            timeout=1800,
        )
        result = subprocess.run(task["success_command"], shell=True, cwd=workdir, check=False)
        return result.returncode == 0
    finally:
        subprocess.run(
            ["git", "worktree", "remove", "--force", str(workdir)], cwd=ROOT, check=False
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--only", nargs="*", help="task ids to run")
    parser.add_argument("--min-pass-rate", type=float, default=0.8)
    args = parser.parse_args()

    try:
        tasks = [load_task(p) for p in sorted(TASKS.glob("*.yaml"))]
    except (ValueError, yaml.YAMLError) as err:
        print(f"agent-evals: invalid task file: {err}", file=sys.stderr)
        return 1
    if args.only:
        tasks = [t for t in tasks if t["id"] in args.only]

    if args.dry_run:
        for t in tasks:
            print(f"[{t['id']}] {t['title']}  (guards: {t['guards']})")
        print(f"agent-evals: {len(tasks)} task files valid")
        return 0

    if not tasks:
        print("agent-evals: no tasks to run", file=sys.stderr)
        return 1
    if shutil.which("claude") is None:
        print("agent-evals: `claude` CLI not found. Install Claude Code or use --dry-run.")
        return 1

    results = {t["id"]: run_task(t) for t in tasks}
    passed = sum(results.values())
    rate = passed / len(results)
    for tid, ok in results.items():
        print(f"[{tid}] {'PASS' if ok else 'FAIL'}")
    print(f"Pass rate: {passed}/{len(results)} = {rate:.0%} (gate: {args.min_pass_rate:.0%})")

    RESULTS.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    sha = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=False
    ).stdout.strip()
    (RESULTS / f"{stamp}.json").write_text(
        json.dumps({"git_sha": sha, "results": results, "pass_rate": rate}, indent=2)
    )
    return 0 if rate >= args.min_pass_rate else 1


if __name__ == "__main__":
    sys.exit(main())
