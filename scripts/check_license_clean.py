"""Fail if tracked files contain licensed SNOMED CT release content or gold labels.

Run by `make check` locally and in CI: the enforced half of the clinical-data-licensing skill.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

RF2_HEADER = re.compile(
    r"id\teffectiveTime\tactive\tmoduleId|sourceId\tdestinationId\trelationshipGroup"
)
# Many lines that look like "<sctid>,<term>" or "<sctid>\t<term>" means a term dump.
TERM_ROW = re.compile(r"^\d{6,18}[\t,|]\s*[A-Za-z]", re.MULTILINE)
MAX_TERM_ROWS = 50
FORBIDDEN_PREFIXES = ("data/",)
FORBIDDEN_SUFFIXES = (".pdf",)


def tracked_files() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [line for line in out.stdout.splitlines() if line]


def main() -> int:
    problems: list[str] = []
    for rel in tracked_files():
        if rel.startswith(FORBIDDEN_PREFIXES) or rel.lower().endswith(FORBIDDEN_SUFFIXES):
            problems.append(f"{rel}: data/ and PDFs must never be committed")
            continue
        path = Path(rel)
        if not path.is_file() or path.stat().st_size > 5_000_000:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if RF2_HEADER.search(text):
            problems.append(f"{rel}: contains a SNOMED CT RF2 header")
        elif len(TERM_ROW.findall(text)) > MAX_TERM_ROWS:
            problems.append(f"{rel}: looks like a concept-id/term dump (> {MAX_TERM_ROWS} rows)")

    for problem in problems:
        print(f"license-check: {problem}", file=sys.stderr)
    if not problems:
        print("license-check: ok")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
