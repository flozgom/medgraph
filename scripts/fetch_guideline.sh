#!/usr/bin/env bash
# Download the guideline PDF into data/guideline/. It is never committed (copyright).
set -euo pipefail
cd "$(dirname "$0")/.."
: "${GUIDELINE_URL:?set GUIDELINE_URL to the chosen public guideline PDF (see intents/0003)}"
mkdir -p data/guideline
curl -fsSL -o data/guideline/guideline.pdf "$GUIDELINE_URL"
echo "saved data/guideline/guideline.pdf"
