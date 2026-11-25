"""PreToolUse hook on Bash: approval gates for git.

- Pushing to main or force-pushing is blocked: main changes only through a PR that Paco merges.
- `git add -f` and staging anything under data/ are blocked: that is where licensed SNOMED
  content, guideline PDFs and gold labels live.
"""

from __future__ import annotations

import json
import re
import sys

RULES = [
    (re.compile(r"\bgit\s+push\b.*\b(main|master)\b"), "pushing to main (open a PR instead)"),
    (re.compile(r"\bgit\s+push\b.*(\s--force\b|\s-f\b)"), "force-pushing"),
    (re.compile(r"\bgit\s+add\b.*(\s-f\b|\s--force\b)"), "force-adding ignored files"),
    (re.compile(r"\bgit\s+add\b.*(^|\s)\.?/?data/"), "staging data/ (licensed or generated)"),
]


def main() -> int:
    command = json.load(sys.stdin).get("tool_input", {}).get("command", "")
    for pattern, what in RULES:
        if pattern.search(command):
            print(f"Blocked: {what} needs a human. Ask Paco to do it.", file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
