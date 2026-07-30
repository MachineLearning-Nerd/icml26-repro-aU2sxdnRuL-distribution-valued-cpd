import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_claim5_attempt1_source_availability_audit():
    subprocess.run(
        [sys.executable, "src/claim5_attempt1_source_audit.py"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    result = json.loads((ROOT / "outputs" / "claim5_attempt1_source_audit.json").read_text())
    assert result["paper_protocol"]["pca_dimension_20"]
    assert result["runner_protocol"]["default_representation_is_sentiment3d"]
    assert result["availability"]["target_file_access_request"]
    assert not result["decision"]["cpu_source_faithful_run_executed"]
    assert result["decision"]["outcome"] == "inconclusive_source_faithful_data_and_outputs_unavailable"
