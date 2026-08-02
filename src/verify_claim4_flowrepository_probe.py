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
    if result["archive_probe"]["zip_signature"] not in {"504b0304", "504b0506", "504b0708"}:
        failures.append("download endpoint did not return a ZIP archive")
    if not result["negative_control"]["rejected"]:
        failures.append("nonexistent accession control was not rejected")
    print(json.dumps({"claim": 4, "probe_verifier": "PASS" if not failures else "FAIL", "failures": failures}, sort_keys=True))
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
