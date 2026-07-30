import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_claim6_source_audit_and_dimension_control():
    subprocess.run([sys.executable, "src/claim6_attempt1_theorem_audit.py"], cwd=ROOT, check=True)
    result = json.loads((ROOT / "outputs" / "claim6_attempt1" / "result.json").read_text())
    assert result["verdict"] == "verified_scoped"
    assert len(result["epsilon_scaling_checks"]) == 9
    assert max(row["absolute_error"] for row in result["epsilon_scaling_checks"]) < 1e-12
    assert all(row["control_rejected"] for row in result["negative_controls"])
    assert "dimension-free" in " ".join(result["limitations"])
