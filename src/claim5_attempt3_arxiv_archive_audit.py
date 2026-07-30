#!/usr/bin/env python3
"""Recover and audit the authoritative arXiv source assets for Claim 5."""
from __future__ import annotations

import hashlib
import json
import tarfile
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence" / "claim5_attempt3"
ARCHIVE = EVIDENCE / "arxiv_source.tar"
ARCHIVE_URL = "https://arxiv.org/e-print/2602.07252"
ARCHIVE_SHA256 = "6d4af865d403a1c4f72ed3ef8057069212ac1633aa79410b4607b04a8b9edb87"
OUTPUT = ROOT / "outputs" / "claim5_attempt3" / "arxiv_archive_audit.json"

FIGURE_MEMBER = "arixv/figures/approachB_embed_pca20_D_first50_phase1_phase2_monitoring_manuscript.pdf"
TEX_MEMBER = "main0.tex"
README_MEMBER = "00README.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ensure_archive() -> None:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    if not ARCHIVE.exists():
        temporary = ARCHIVE.with_suffix(".tmp")
        with urlopen(ARCHIVE_URL, timeout=60) as response:
            temporary.write_bytes(response.read())
        temporary.replace(ARCHIVE)
    observed = sha256(ARCHIVE)
    if observed != ARCHIVE_SHA256:
        raise RuntimeError(f"arXiv archive SHA-256 mismatch: {observed}")


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    ensure_archive()
    with tarfile.open(ARCHIVE, "r:gz") as archive:
        members = {member.name for member in archive.getmembers() if member.isfile()}
        for required in (FIGURE_MEMBER, TEX_MEMBER, README_MEMBER):
            if required not in members:
                raise RuntimeError(f"missing expected arXiv source member: {required}")
        figure = archive.extractfile(FIGURE_MEMBER).read()
        tex = archive.extractfile(TEX_MEMBER).read().decode("utf-8", errors="replace")
        readme = json.loads(archive.extractfile(README_MEMBER).read())

    (EVIDENCE / "reddit_figure4_source.pdf").write_bytes(figure)
    figure_readme_refs = [
        item.get("filename")
        for item in readme.get("process", [])
        if isinstance(item, dict) and "reddit" in str(item.get("filename", "")).lower()
    ]
    required_text = {
        "protocol_384_to_20": "all-MiniLM-L6-v2" in tex and "384-dimensional" in tex and "d=20" in tex,
        "phase_dates": "December 2, 2020 to January 30, 2021" in tex and "January 31 to May 5, 2021" in tex,
        "april_13_event": "Apr 13" in tex and "J\\&J Pause" in tex,
        "source_records_april_30_not_april_13_alarm": "Apr 30 post-J\\&J-pause discourse reorganization" in tex,
        "source_records_sparse_gap": "sparse-data gap Apr 3 -- 28" in tex,
        "figure_caption_present": "Phase II monitoring of Reddit vaccine comments" in tex,
    }
    if not all(required_text.values()):
        missing = [key for key, value in required_text.items() if not value]
        raise RuntimeError(f"missing expected source assertions: {missing}")

    result = {
        "source": ARCHIVE_URL,
        "archive_sha256": sha256(ARCHIVE),
        "archive_member_count": len(members),
        "recovered_figure_member": FIGURE_MEMBER,
        "recovered_figure_sha256": hashlib.sha256(figure).hexdigest(),
        "readme_reddit_references": figure_readme_refs,
        "source_assertions": required_text,
        "exact_embedding_stream_recovered": False,
        "dated_numeric_alarm_series_recovered": False,
        "figure_asset_recovered": True,
        "verdict": "inconclusive_source_artifact_scope",
        "reason": (
            "The authoritative arXiv source recovers Figure-4 assets and the 384-D to PCA-20 protocol, "
            "and describes the Apr 30 post-J&J-pause reorganization after an Apr 3--28 sparse-data gap. "
            "This supports source-level event alignment but does not provide the released embedding/alarm series needed "
            "for an independent numeric rerun; the live claim is therefore inconclusive rather than falsified."
        ),
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
