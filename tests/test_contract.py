import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_live_contract_has_six_nonempty_claims():
    claims = json.loads((ROOT / "contract" / "live_claims.json").read_text())
    assert len(claims) == 6
    assert all(claim["text"].strip() for claim in claims)

def test_manifest_matches_target_id_and_score_ceiling():
    manifest = json.loads((ROOT / "contract" / "contract_manifest.json").read_text())
    assert manifest["openreview_id"] == "aU2sxdnRuL"
    assert manifest["max_points"] == 12
