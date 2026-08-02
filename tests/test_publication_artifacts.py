import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_marimo_notebook_and_release_candidate():
    subprocess.run(["marimo", "check", str(ROOT / "notebooks" / "reproduction.py")], cwd=ROOT, check=True)
    subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_release_candidate.py")], cwd=ROOT, check=True)
