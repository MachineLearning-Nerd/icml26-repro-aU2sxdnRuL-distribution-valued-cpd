import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "src" / "claim1_falsification.py"
OUTPUT = ROOT / "outputs" / "claim1_falsification_scope.json"


def test_atomic_split_counterexample_matches_pinned_projection():
    subprocess.run([sys.executable, str(SCRIPT)], check=True, cwd=ROOT)
    result = json.loads(OUTPUT.read_text())
    assert result["pinned_upstream_projection"] == [[0.0]]
    assert result["source_tangent_norm_squared"] == 0.0
    assert result["coupling_w2_squared"] == 1.0
    assert result["equality_gap"] == 1.0
    assert result["deterministic_map_exists"] is False
