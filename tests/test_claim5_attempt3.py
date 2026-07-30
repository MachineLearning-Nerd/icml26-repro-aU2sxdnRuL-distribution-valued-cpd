import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_arxiv_archive_recovers_figure_but_not_numeric_stream():
    result = json.loads((ROOT / "outputs" / "claim5_attempt3" / "arxiv_archive_audit.json").read_text())
    assert result["figure_asset_recovered"]
    assert not result["exact_embedding_stream_recovered"]
    assert not result["dated_numeric_alarm_series_recovered"]
    assert all(result["source_assertions"].values())
    assert result["verdict"] == "inconclusive_source_artifact_scope"
    assert (ROOT / "evidence" / "claim5_attempt3" / "reddit_figure4_source.pdf").is_file()
