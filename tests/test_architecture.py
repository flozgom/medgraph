"""Architecture rules from CLAUDE.md that must always hold (eval-hygiene: no label leakage)."""

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DETECT = ROOT / "medgraph" / "detect"
GAP_ID = re.compile(r"\bG[1-6]\b")


def _imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text())
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return names


def test_detectors_never_import_gold() -> None:
    for path in DETECT.rglob("*.py"):
        leaked = {name for name in _imports(path) if name.startswith("medgraph.gold")}
        assert not leaked, f"{path.relative_to(ROOT)} imports {leaked}"


def test_detector_code_and_prompts_never_mention_gap_ids() -> None:
    for path in [*DETECT.rglob("*.py"), *DETECT.rglob("*.md"), *DETECT.rglob("*.txt")]:
        hits = GAP_ID.findall(path.read_text())
        assert not hits, f"{path.relative_to(ROOT)} mentions gold gap ids {hits}"
