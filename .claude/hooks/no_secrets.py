"""PreToolUse hook: keep credentials and licensed SNOMED CT content out of the diff."""

from __future__ import annotations

import json
import re
import sys

SECRETS = {
    "Anthropic API key": re.compile(r"sk-ant-[A-Za-z0-9_\-]{20,}"),
    "GitHub token": re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}"),
    "Hugging Face token": re.compile(r"hf_[A-Za-z0-9]{30,}"),
    "Private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "Generic secret assignment": re.compile(
        r"(?i)(password|secret|api_key|token)\s*=\s*['\"][^'\"]{8,}['\"]"
    ),
}
# RF2 release headers: a sign that SNOMED release content is being copied into the repo.
SNOMED_RF2 = re.compile(
    r"id\teffectiveTime\tactive\tmoduleId|sourceId\tdestinationId\trelationshipGroup"
)


def written_text(tool_input: dict) -> str:
    parts = [str(tool_input.get(key, "")) for key in ("content", "new_string")]
    parts += [str(e.get("new_string", "")) for e in tool_input.get("edits", [])]
    return "\n".join(parts)


def main() -> int:
    payload = json.load(sys.stdin)
    tool_input = payload.get("tool_input", {})
    file_path = str(tool_input.get("file_path", ""))
    text = written_text(tool_input)

    for name, pattern in SECRETS.items():
        if pattern.search(text):
            print(
                f"Blocked: looks like a {name}. Read secrets from environment variables "
                "(.env is gitignored); never write them into the repo.",
                file=sys.stderr,
            )
            return 2

    if SNOMED_RF2.search(text) and "/data/" not in file_path:
        print(
            "Blocked: this looks like SNOMED CT RF2 release content. SNOMED is licensed and lives "
            "only in data/snomed/ (gitignored). See the clinical-data-licensing skill.",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
