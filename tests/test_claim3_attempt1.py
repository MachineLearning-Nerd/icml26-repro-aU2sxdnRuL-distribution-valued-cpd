from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from claim3_attempt1_source_audit import table_rows  # noqa: E402


def test_full_table_high_variance_max_is_not_95_percent():
    rows = table_rows((ROOT / "paper_source" / "main0.tex").read_text())
    high = [row for row in rows if row["sigma"] == 2.0]
    best = max(high, key=lambda row: row["reduction_fraction"])
    assert len(rows) == 18
    assert best == {
        "d": 5,
        "sigma": 2.0,
        "delta": 0.5,
        "ours": 1.1,
        "best_logkde": 4.0,
        "reduction_fraction": 0.725,
    }
    assert best["reduction_fraction"] < 0.95


def test_table_means_contain_no_95_percent_idd_over_best_logkde_gain():
    rows = table_rows((ROOT / "paper_source" / "main0.tex").read_text())
    assert not [row for row in rows if row["reduction_fraction"] >= 0.95]
    tied_low_variance = [
        row for row in rows
        if row["sigma"] == 0.5 and row["delta"] == 0.5
    ]
    assert tied_low_variance
    assert all(row["ours"] == row["best_logkde"] == 1.0 for row in tied_low_variance)
