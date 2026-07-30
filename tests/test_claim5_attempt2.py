import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_history_audit_preserves_missing_artifact_limit():
    result = json.loads((ROOT / "outputs" / "claim5_attempt2" / "protocol_history_audit.json").read_text())
    assert result["release_count"] == 0
    assert result["tag_count"] == 0
    assert result["missing_module_import"]
    assert result["isolated_import_repair_exit_code"] != 0
    assert result["isolated_import_repair_still_fails"]
    assert not result["paper_era_embedding_or_figure_outputs_recovered"]
    assert result["verdict"] == "inconclusive"
