import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_official_flowcap_archive_probe():
    subprocess.run([sys.executable, str(ROOT / "src" / "claim4_flowrepository_probe.py")], cwd=ROOT, check=True)
    subprocess.run([sys.executable, str(ROOT / "src" / "verify_claim4_flowrepository_probe.py")], cwd=ROOT, check=True)
