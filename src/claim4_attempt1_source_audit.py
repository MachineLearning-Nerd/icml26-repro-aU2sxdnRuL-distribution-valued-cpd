"""Claim 4 attempt 1: source-faithful FlowCAP-II provenance audit.

This does not substitute synthetic data for the FlowCAP-II experiment.  It tests
whether the pinned paper and pinned public repository supply a coherent,
executable protocol for the literal live claim.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "evidence" / "claim4_attempt1" / "main0.tex"
UPSTREAM_README = ROOT / "upstream" / "IDD-icml" / "README.md"
UPSTREAM = ROOT / "upstream" / "IDD-icml"
OUT = ROOT / "outputs" / "claim4_attempt1_source_audit.json"


def main() -> None:
    paper = PAPER.read_text(encoding="utf-8")
    readme = UPSTREAM_README.read_text(encoding="utf-8")
    tracked = [str(path.relative_to(UPSTREAM)) for path in UPSTREAM.rglob("*") if path.is_file()]
    flowcap_paths = [path for path in tracked if any(token in path.lower() for token in ("flowcap", "aml", "cytometry"))]

    required_protocol_fragments = {
        "dimension_7": "distribution-valued stream in $\\mathcal{P}_2(\\mathbb{R}^7)$",
        "cells_per_measurement": "random subsample of $N=2,000$ cells",
        "healthy_calibration": "sequence of 300 healthy samples",
        "monitoring_length": "test stream of 300 samples",
        "aml_fraction": "injecting 80\\% AML-positive samples",
    }
    for name, fragment in required_protocol_fragments.items():
        if fragment not in paper:
            raise AssertionError(f"paper source lacks expected FlowCAP protocol fragment {name}: {fragment!r}")

    main_claims_arl1_one = "near-immediate detection ($\\mathrm{ARL}_1 \\approx 1$)" in paper
    appendix_arl1_two_to_three = "between $\\sim$2 and $\\sim$3" in paper
    hotelling_precision_below_point_four = "Hotelling's $T^2$ yields low precision ($<0.4$)" in paper
    hotelling_f1_below_point_four = "Hotelling's $T^2$ yields low F1" in paper or "Hotelling's $T^2$.*F1" in paper

    payload = {
        "attempt": "claim_4_attempt_1_source_and_release_audit",
        "paper_source": {
            "url": "https://export.arxiv.org/e-print/2602.07252",
            "main_tex_sha256": hashlib.sha256(PAPER.read_bytes()).hexdigest(),
            "flowcap_protocol_fragments": required_protocol_fragments,
        },
        "pinned_upstream": {
            "repository": "https://github.com/yyzeng43/IDD-icml",
            "commit": "c5b1db4060e5081e5c487f91792dc18c17603fd0",
            "flowcap_or_aml_or_cytometry_tracked_paths": flowcap_paths,
            "readme_mentions_flowcap": "FlowCAP" in readme,
            "readme_case_study": "Reddit COVID-vaccine monitoring" in readme,
        },
        "literal_claim_consistency": {
            "main_text_reports_arl1_approximately_1": main_claims_arl1_one,
            "appendix_reports_idd_arl1_between_2_and_3": appendix_arl1_two_to_three,
            "main_text_says_hotelling_precision_below_0_4": hotelling_precision_below_point_four,
            "main_text_explicitly_says_hotelling_f1_below_0_4": hotelling_f1_below_point_four,
        },
        "outcome": "falsified_literal_source_scope",
        "reason": (
            "The public code/release contains no FlowCAP/AML/cytometry data, loader, or runner, "
            "so no source-faithful CPU table reproduction is executable. More importantly, the live "
            "claim calls Hotelling T2 F1 <0.4, while the pinned main text states precision <0.4; "
            "the appendix also reports IDD ARL1 approximately 2--3, conflicting with the main-text "
            "approximately-1 wording. This source audit does not establish a dataset-level result."
        ),
        "next_action": "claim_4_attempt_2_locate_public_flowcap_data_and_reconstruct_protocol_only_if_exact_files_and_labels_are_available",
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
