#!/usr/bin/env python3
"""Fail-closed verifier for the faithful Claim 5 reconstruction route."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / ".openresearch" / "artifacts" / "claim5_reddit_reconstruction" / "raw"


def main() -> int:
    result = json.loads((RAW / "result.json").read_text())
    with (RAW / "daily_statistics.csv").open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    failures = []
    protocol = result["protocol"]
    checker = result["independent_checker"]
    if len(rows) != 100 or protocol["phase1_days"] != 50 or protocol["phase2_days"] != 50:
        failures.append("camera-ready official-comments 50+50 daily stream was not reconstructed")
    if protocol["embedding_dimension"] != 384 or protocol["pca_dimension"] != 20:
        failures.append("SBERT-384 to PCA-20 contract failed")
    if protocol["minimum_comments"] < 30:
        failures.append("a retained day violates the camera-ready 30-comment minimum")
    if checker["eigenvalue_max_abs_error"] > 1e-8 or checker["t2_max_abs_error"] > 1e-6 or checker["spe_max_abs_error"] > 1e-8:
        failures.append("independent Gram-matrix checker disagrees")
    if not result["negative_controls"]["identity_tangents_rejected"]:
        failures.append("identity-tangent control was not rejected")
    if not result["observed"]["idd_spe_alarms"]:
        failures.append("IDD reconstruction produced no testable alarms")
    shuffled = result["negative_controls"]["date_shuffle"]
    expected_matches = len(set(result["observed"]["idd_spe_alarms"]) & {"2021-03-02", "2021-04-30", "2021-05-03"})
    if shuffled["observed_response_date_matches"] != expected_matches:
        failures.append("date-shuffle control did not count alarm/event matches")
    output = {"claim": 5, "route_verifier": "FAIL" if failures else "PASS", "evidence_verdict": result["verdict"], "failures": failures}
    print(json.dumps(output, sort_keys=True), flush=True)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
