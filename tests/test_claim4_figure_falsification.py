import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_claim4_original_figure_falsification():
    subprocess.run([sys.executable, str(ROOT / "src" / "claim4_figure_falsification.py")], cwd=ROOT, check=True)
    subprocess.run([sys.executable, str(ROOT / "src" / "verify_claim4_figure_falsification.py")], cwd=ROOT, check=True)
