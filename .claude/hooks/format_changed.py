"""PostToolUse hook: format and lint only the file that just changed (fast, scoped)."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys


def ruff_cmd() -> list[str] | None:
    if shutil.which("ruff"):
        return ["ruff"]
    if shutil.which("uv"):
        return ["uv", "run", "--quiet", "ruff"]
    return None


def main() -> int:
    file_path = json.load(sys.stdin).get("tool_input", {}).get("file_path", "")
    ruff = ruff_cmd()
    if not file_path.endswith(".py") or ruff is None:
        return 0

    subprocess.run([*ruff, "format", "--quiet", file_path], check=False)
    lint = subprocess.run(
        [*ruff, "check", "--fix", "--quiet", file_path], capture_output=True, text=True
    )
    if lint.returncode != 0:
        # Exit 2 on PostToolUse feeds the problems back to Claude so it fixes them now.
        print(f"Lint issues remain in {file_path}:\n{lint.stdout}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
