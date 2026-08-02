#!/usr/bin/env python3
"""Fail-closed verifier for Claim 4's original-figure falsification."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / ".openresearch" / "artifacts" / "claim4_figure_falsification" / "raw"


def main() -> int:
    result = json.loads((RAW / "result.json").read_text())
    with (RAW / "digitized_points.csv").open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    extracted = result["extracted"]
    failures = []
    if result["verdict"] != "FALSIFIED":
        failures.append("predeclared figure-level falsification rule did not trigger")
    if extracted["idd_arl1_min"] <= 1.5:
        failures.append("a displayed IDD ARL1 point is within the generous approximately-1 bound")
    if not 0.70 <= extracted["idd_f1_max"] <= 0.85:
        failures.append("digitized maximum IDD F1 does not corroborate the approximately-0.75 clause")
    if extracted["hotelling_f1_max"] >= 0.4:
        failures.append("digitized Hotelling F1 is not below 0.4")
    if result["independent_checker"]["idd_arl1_marker_count"] < 5:
        failures.append("too few IDD ARL1 markers independently located")
    if not result["independent_checker"]["all_idd_arl1_above_2"]:
        failures.append("independent checker found an IDD delay at or below 2")
    if min(result["independent_checker"]["red_fill_patch_pixels"]) < 40:
        failures.append("filled-diamond identity check failed")
    if result["independent_checker"]["column_method_marker_count"] < 4:
        failures.append("independent column method found too few markers")
    if not result["independent_checker"]["column_method_all_above_2"]:
        failures.append("independent column method found an IDD delay at or below 2")
    if not result["negative_control"]["rejected"]:
        failures.append("wrong linear-axis negative control was not rejected")
    if len(rows) < 15:
        failures.append("raw digitized CSV is incomplete")
    output = {"claim": 4, "figure_falsification_verifier": "FAIL" if failures else "PASS", "failures": failures}
    print(json.dumps(output, sort_keys=True), flush=True)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
