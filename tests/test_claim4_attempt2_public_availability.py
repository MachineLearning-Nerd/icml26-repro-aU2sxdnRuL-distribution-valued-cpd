import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_public_availability_audit_is_reproducible():
    result = subprocess.run(
        [sys.executable, "src/claim4_attempt2_public_availability.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    payload = json.loads((ROOT / "outputs" / "claim4_attempt2_public_availability.json").read_text())
    assert payload["authoritative_observations"]["paper_acknowledges_direct_dataset_sharing"]
    assert payload["authoritative_observations"]["official_flowcap_page_is_coming_soon"]
    assert payload["authoritative_observations"]["pinned_author_repository_data_paths"] == []
    assert payload["reconstruction_decision"]["outcome"] == "inconclusive_public_data_and_protocol_unavailable"
    assert '"cpu_evaluation_run": false' in result.stdout
