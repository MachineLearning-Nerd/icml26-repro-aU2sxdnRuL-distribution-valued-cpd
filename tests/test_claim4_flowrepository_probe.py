from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_historical_rejected_flowcap_probe_is_preserved():
    """Historical rejected baseline: the current Claim 4 verifier is figure-based."""
    assert (ROOT / "src" / "claim4_flowrepository_probe.py").is_file()
    assert (ROOT / "src" / "verify_claim4_flowrepository_probe.py").is_file()
