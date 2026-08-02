import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_claim1_paper_scale_multivariate_pipeline():
    subprocess.run(
        [sys.executable, str(ROOT / "src" / "claim1_paper_scale.py")],
        cwd=ROOT,
        check=True,
    )
    subprocess.run(
        [sys.executable, str(ROOT / "src" / "verify_claim1_paper_scale.py")],
        cwd=ROOT,
        check=True,
    )
