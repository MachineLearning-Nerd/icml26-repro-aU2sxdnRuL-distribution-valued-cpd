"""Claim 4 attempt 2: authoritative-public-data availability audit.

This audit deliberately does not treat a missing public copy as a counterexample to
FlowCAP-II.  It records whether the paper's *exact* released protocol can be
reconstructed from authoritative public material.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper_source" / "main0.tex"
UPSTREAM = ROOT / "upstream" / "IDD-icml"
FLOWCAP_PAGE = ROOT / "evidence" / "claim4_attempt2" / "flowcap2_official.html"
OUT = ROOT / "outputs" / "claim4_attempt2_public_availability.json"


def main() -> None:
    paper = PAPER.read_text(encoding="utf-8")
    page = FLOWCAP_PAGE.read_text(encoding="utf-8")
    upstream_paths = [str(path.relative_to(UPSTREAM)) for path in UPSTREAM.rglob("*") if path.is_file()]
    data_paths = [
        path for path in upstream_paths
        if any(token in path.lower() for token in ("flowcap", "aml", "cytometry", ".fcs"))
    ]

    acknowledgement = "sharing the FlowCAP II dataset directly with us" in paper
    protocol_tokens = {
        "seven_dimensions": "d=7",
        "two_thousand_cells": "N=2,000",
        "healthy_subjects": "316 healthy donors",
        "aml_subjects": "43 AML patients",
        "calibration_samples": "sequence of 300 healthy samples",
        "monitoring_samples": "test stream of 300 samples",
        "aml_injection": "injecting 80\\% AML-positive samples",
    }
    missing_protocol = [name for name, token in protocol_tokens.items() if token not in paper]
    payload = {
        "attempt": "claim_4_attempt_2_authoritative_public_data_availability",
        "sources": {
            "paper_source": "https://export.arxiv.org/e-print/2602.07252",
            "paper_source_sha256": hashlib.sha256(PAPER.read_bytes()).hexdigest(),
            "official_flowcap_page": "https://flowcap.org/flowcap2/",
            "official_flowcap_page_sha256": hashlib.sha256(FLOWCAP_PAGE.read_bytes()).hexdigest(),
            "pinned_author_repository": "https://github.com/yyzeng43/IDD-icml@c5b1db4060e5081e5c487f91792dc18c17603fd0",
        },
        "authoritative_observations": {
            "paper_acknowledges_direct_dataset_sharing": acknowledgement,
            "official_flowcap_page_is_coming_soon": "Coming Soon" in page,
            "paper_protocol_fragments_missing": missing_protocol,
            "pinned_author_repository_data_paths": data_paths,
        },
        "reconstruction_decision": {
            "exact_public_files_available": False,
            "exact_public_labels_available": False,
            "exact_public_preprocessing_and_stream_script_available": False,
            "cpu_evaluation_run": False,
            "outcome": "inconclusive_public_data_and_protocol_unavailable",
            "reason": (
                "The paper itself says the FlowCAP-II data were shared directly by Dr. Ryan Brinkman; "
                "the official FlowCAP-II URL retrieved for this audit is a Coming Soon page; and the "
                "pinned author repository contains no FlowCAP/AML/cytometry/FCS files or runner. "
                "The paper describes aggregate cohort and stream parameters, but not public source files, "
                "per-measurement labels, preprocessing, random seed, or stream-construction code. "
                "A source-faithful CPU evaluation is therefore not executable. This is an availability "
                "finding, not a dataset-level refutation."
            ),
        },
    }
    if not acknowledgement:
        raise AssertionError("expected direct-sharing acknowledgement absent from paper source")
    if missing_protocol:
        raise AssertionError(f"expected protocol fragments absent: {missing_protocol}")
    if data_paths:
        raise AssertionError(f"unexpected FlowCAP-like paths in pinned repository: {data_paths}")
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
