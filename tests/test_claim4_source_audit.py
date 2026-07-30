import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_claim4_source_audit_records_protocol_and_literal_mismatch():
    subprocess.run([sys.executable, "src/claim4_attempt1_source_audit.py"], cwd=ROOT, check=True)
    result = json.loads((ROOT / "outputs" / "claim4_attempt1_source_audit.json").read_text())
    assert result["outcome"] == "falsified_literal_source_scope"
    assert result["paper_source"]["flowcap_protocol_fragments"]["dimension_7"]
    assert result["pinned_upstream"]["flowcap_or_aml_or_cytometry_tracked_paths"] == []
    consistency = result["literal_claim_consistency"]
    assert consistency["main_text_reports_arl1_approximately_1"]
    assert consistency["appendix_reports_idd_arl1_between_2_and_3"]
    assert consistency["main_text_says_hotelling_precision_below_0_4"]
    assert not consistency["main_text_explicitly_says_hotelling_f1_below_0_4"]
