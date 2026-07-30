import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_empirical_ot_translation_invariants():
    subprocess.run(
        [sys.executable, str(ROOT / "src" / "claim1_attempt2_empirical.py")],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    result = json.loads((ROOT / "outputs" / "claim1_attempt2_empirical.json").read_text())
    assert result["scope"] == "toy"
    assert result["direct_translation_map_max_abs_error"] < 1e-10
    assert abs(result["direct_translation_w2_squared"] - 0.36) < 1e-10
    assert result["negative_control_passed"] is True
    assert result["claim_1_full_scope_verified"] is False
