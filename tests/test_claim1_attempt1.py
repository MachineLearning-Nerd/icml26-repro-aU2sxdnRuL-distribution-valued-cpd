import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from claim1_attempt1 import run


def test_radial_translation_identity_and_negative_control():
    result = run()
    assert result["absolute_error"] < 1e-14
    assert result["negative_control_identity_norm_sq"] == 0.0
    assert result["negative_control_separation"] > 0.5


def test_tangent_pca_monitor_produces_finite_statistics():
    result = run()
    assert result["hotelling_t2_rank1"] > 0.0
    assert result["spe_rank1"] >= 0.0
