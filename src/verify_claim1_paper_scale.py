#!/usr/bin/env python3
"""Fail-closed verifier for the paper-scale Claim 1 artifact."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / ".openresearch" / "artifacts" / "claim1_paper_scale" / "raw" / "result.json"


def main() -> int:
    result = json.loads(RESULT.read_text())
    failures = []
    if result["dimensions"] != 5 or result["phase_i_distributions"] != 300:
        failures.append("not the predeclared multivariate paper scale")
    if result["points_per_distribution"] != 300 or result["phase_ii_distributions"] != 300:
        failures.append("stream dimensions changed")
    if max(a["absolute_error"] for a in result["assignment_audits"]) > 1e-9:
        failures.append("radial identity disagrees with independently solved OT")
    if min(a["identity_assignments"] for a in result["assignment_audits"]) != 300:
        failures.append("constructed Brenier map was not the solved empirical OT map")
    checker = result["independent_checker"]
    if checker["eigenvalue_max_abs_error"] > 1e-9:
        failures.append("independent covariance spectrum mismatch")
    if checker["t2_max_abs_error"] > 1e-7 or checker["spe_max_abs_error"] > 1e-9:
        failures.append("independent T2/SPE mismatch")
    if not all(control["rejected"] for control in result["negative_controls"].values()):
        failures.append("a negative control was not rejected")
    if result["changed_half_alarm_rates"]["either"] < 0.9:
        failures.append("two-chart monitor did not detect the predeclared shift")
    verdict = "PASS" if not failures else "FAIL"
    print(json.dumps({"claim": 1, "verifier": verdict, "failures": failures}, sort_keys=True))
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
