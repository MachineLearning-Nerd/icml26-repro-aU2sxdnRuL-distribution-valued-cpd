import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_claim5_reddit_reconstruction():
    subprocess.run([sys.executable, str(ROOT / "src" / "claim5_reddit_reconstruction.py")], cwd=ROOT, check=True)
    subprocess.run([sys.executable, str(ROOT / "src" / "verify_claim5_reddit_reconstruction.py")], cwd=ROOT, check=True)
