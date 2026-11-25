"""PreToolUse hook: block edits to protected paths.

Exit code 2 blocks the tool call and sends stderr back to Claude as the reason.
- Always protected: CI workflows, hook config, the hooks themselves, agent eval tasks.
- Always protected: data/snomed/ (licensed raw release; read it, never write it).
- Gold labels and the oracle are protected while `.claude/gold-lock` exists (after spec 0001),
  so detector work can't move the goalposts.
- Tests are protected while `.claude/fix-mode` exists (bug fixes change the code, not the test).
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ALWAYS_PROTECTED = (
    ".github/workflows/",
    ".claude/settings.json",
    ".claude/hooks/",
    "evals/tasks/",
    "data/snomed/",
)
GOLD_LOCKED = ("medgraph/gold/", "data/gold/")
TESTS_DIR = "tests/"


def relative(path: str, root: Path) -> str:
    try:
        return Path(path).resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path


def blocked(message: str) -> int:
    print(message, file=sys.stderr)
    return 2


def main() -> int:
    payload = json.load(sys.stdin)
    file_path = payload.get("tool_input", {}).get("file_path", "")
    root = Path(os.environ.get("CLAUDE_PROJECT_DIR", payload.get("cwd", ".")))
    rel = relative(file_path, root)

    for protected in ALWAYS_PROTECTED:
        if rel.startswith(protected) or rel == protected.rstrip("/"):
            return blocked(
                f"Blocked: {rel} is protected. Propose the change in your summary "
                "for Paco to apply."
            )

    if rel.startswith(GOLD_LOCKED) and (root / ".claude" / "gold-lock").exists():
        return blocked(
            f"Blocked: gold-lock is on, so the oracle and gold labels are read-only ({rel}). "
            "If the ground truth is wrong, raise it as a new intent."
        )

    if rel.startswith(TESTS_DIR) and (root / ".claude" / "fix-mode").exists():
        return blocked(
            f"Blocked: fix-mode is on, so tests are read-only ({rel}). "
            "Make the existing failing test pass by changing medgraph/ only."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
