#!/usr/bin/env python3
"""Fail closed unless the official-artifact schema audit is complete."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / ".openresearch" / "artifacts" / "claim5_official_artifact_probe" / "raw" / "result.json"


def main() -> int:
    result = json.loads(RESULT.read_text())
    failures = []
    expected = {"archival", "original", "preprocessed"}
    if set(result["representations"]) != expected:
        failures.append("not all official representations were audited")
    for name, item in result["representations"].items():
        if len(item["sha256"]) != 64 or item["bytes"] <= 0:
            failures.append(f"{name} lacks a complete content record")
        if set(item["parses"]) != {"comma", "tab"}:
            failures.append(f"{name} lacks both delimiter controls")
    checker = result["independent_checker"]
    if not checker["csv_sniffer_recorded"] or not checker["pandas_comma_and_tab_parsers_recorded"]:
        failures.append("independent schema checks are missing")
    if not result["negative_control"]["preprocessed_json_not_accepted_as_comment_stream"]:
        failures.append("preprocessed JSON negative control was accepted")
    if result["verdict"] != "BLOCKED":
        failures.append("schema discovery alone cannot resolve the paper claim")
    print(json.dumps({"claim": 5, "failures": failures, "official_artifact_probe": "FAIL" if failures else "PASS"}, sort_keys=True), flush=True)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
