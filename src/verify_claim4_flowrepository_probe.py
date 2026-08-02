#!/usr/bin/env python3
"""Fail-closed verifier for official FlowCAP-II data availability."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / ".openresearch" / "artifacts" / "claim4_flowcap" / "raw" / "probe.json"


def main() -> int:
    result = json.loads(RESULT.read_text())
    failures = []
    manifest = result["manifest"]
    if manifest["fcs_files"] != 2872 or manifest["aml_fcs_files"] != 344:
        failures.append("official manifest does not match 359 subjects and 43 AML subjects with eight panels")
    if result["record"]["retrieval_status"] != 200:
        failures.append("official record unavailable")
    if result["official_api"]["fcs_records"] != 2872:
        failures.append("official API did not return all FCS records")
    if result["official_api"]["records_with_md5"] != 2872:
        failures.append("official API omitted per-file integrity hashes")
    if not result["file_probe"]["fcs_header"].startswith("FCS"):
        failures.append("direct file endpoint did not return an FCS payload")
    if result["file_probe"]["prefix_bytes"] != result["file_probe"]["declared_bytes"]:
        failures.append("direct file byte count differs from the API record")
    if result["file_probe"]["full_md5"] != result["file_probe"]["declared_md5"]:
        failures.append("direct file MD5 differs from the API record")
    if not result["negative_control"]["rejected"]:
        failures.append("nonexistent direct-file control was not rejected")
    print(json.dumps({"claim": 4, "probe_verifier": "PASS" if not failures else "FAIL", "failures": failures}, sort_keys=True))
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
