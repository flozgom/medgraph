import json

from medgraph.detect.schema import GapFlag
from medgraph.gold.schema import GapType, GoldGap


def test_gapflag_round_trips_json() -> None:
    flag = GapFlag(
        patient_id="p1",
        recommendation_section_id="4.1.2",
        description="Metformin active with eGFR 24",
        evidence_fhir_ids=["MedicationRequest/abc", "Observation/def"],
    )
    assert GapFlag.model_validate_json(flag.model_dump_json()) == flag
    assert flag.gap is True


def test_goldgap_parses_jsonl_row() -> None:
    row = json.loads('{"patient_id": "p1", "gap_type": "G3", "evidence_fhir_ids": []}')
    gold = GoldGap.model_validate(row)
    assert gold.gap_type is GapType.G3
