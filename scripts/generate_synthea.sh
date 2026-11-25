#!/usr/bin/env bash
# Generate the Synthea FHIR R4 population (needs Java 17+). Output goes to data/synthea/ (gitignored).
set -euo pipefail
cd "$(dirname "$0")/.."
JAR=data/synthea/synthea-with-dependencies.jar
mkdir -p data/synthea
if [[ ! -f "$JAR" ]]; then
  curl -fsSL -o "$JAR" \
    https://github.com/synthetichealth/synthea/releases/download/master-branch-latest/synthea-with-dependencies.jar
fi
java -jar "$JAR" -p "${POPULATION:-1000}" -s 42 -cs 42 \
  --exporter.baseDirectory=data/synthea \
  --exporter.fhir.export=true \
  --exporter.hospital.fhir.export=false \
  --exporter.practitioner.fhir.export=false \
  --exporter.years_of_history=10
