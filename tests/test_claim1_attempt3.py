import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "src" / "claim1_attempt3_quantile_audit.py"
OUTPUT = ROOT / "outputs" / "claim1_attempt3_quantile_audit.json"


def test_clean_room_quantile_isometry_and_controls():
    subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True, capture_output=True, text=True)
    data = json.loads(OUTPUT.read_text())
    assert data["method"] == "clean_room_equal_weight_1d_quantile_transport"
    for family in data["families"].values():
        assert abs(family["radial_tangent_mean_square"] - family["quantile_w2_square"]) < 1e-14
        assert family["identity_control_gap"] > 1e-3
    controls = data["negative_controls"]
    assert controls["wrong_reference_gap"] > 1e-3
    assert controls["uncentered_gap"] > 1e-3
    assert data["independent_pca_t2_spe"]["t2"] > 0
    assert data["independent_pca_t2_spe"]["spe"] >= 0
