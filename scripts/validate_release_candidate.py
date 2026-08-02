#!/usr/bin/env python3
"""Build and audit the evaluator-visible Space candidate from the judged revision."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlparse

from huggingface_hub import snapshot_download


ROOT = Path(__file__).resolve().parents[1]
ALLOWLIST = ROOT / "release" / "upload_allowlist.json"
PROTECTED = ROOT / "release" / "protected_judged_manifest.json"
MUTABLE_PROTECTED = {"README.md", "logbook.json"}
VERDICTS = {
    "current-claim-1": "VERIFIED",
    "current-claim-2": "FALSIFIED",
    "current-claim-3": "FALSIFIED",
    "current-claim-4": "FALSIFIED",
    "current-claim-5": "BLOCKED",
    "current-claim-6": "VERIFIED",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def committed_bytes(relative: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"HEAD:{relative}"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
    ).stdout


def copy_candidate(judged: Path, candidate: Path, entries: list[dict]) -> None:
    shutil.copytree(judged, candidate, dirs_exist_ok=True, ignore=shutil.ignore_patterns(".cache"))
    for entry in entries:
        content = committed_bytes(entry["source"])
        content.decode("utf-8")
        target = candidate / entry["target"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)


def walk_pages(node: dict, candidate: Path, opened: list[str]) -> None:
    page = candidate / node["file"]
    if not page.is_file():
        raise AssertionError(f"navigation target missing: {node['file']}")
    page.read_text()
    opened.append(node["file"])
    for child in node.get("children", []):
        walk_pages(child, candidate, opened)


def verify_current_pages(candidate: Path, entries: list[dict]) -> None:
    targets = {entry["target"] for entry in entries}
    for slug, verdict in VERDICTS.items():
        text = (candidate / "pages" / slug / "page.md").read_text()
        lowered = text.lower()
        required = ["exact claim", "raw", "code", "checker", "control", "fixed command", "limitation"]
        missing = [word for word in required if word not in lowered]
        if missing:
            raise AssertionError(f"{slug} visibility fields missing: {missing}")
        if verdict not in text:
            raise AssertionError(f"{slug} verdict missing")
        for match in re.findall(r"https://huggingface\.co/spaces/[^)]+/resolve/main/([^)]+)", text):
            target = unquote(urlparse(match).path)
            if target not in targets and not (candidate / target).is_file():
                raise AssertionError(f"{slug} raw target missing: {target}")


def verify_report(candidate: Path) -> None:
    report = (candidate / "reports" / "campaign" / "report.md").read_text()
    first_lines = [line for line in report.splitlines() if line.strip()]
    if not first_lines[0].startswith("# ") or "images/headline-flowcap.svg" not in first_lines[1]:
        raise AssertionError("report does not open with the headline evidence figure")
    for image in re.findall(r"!\[[^]]*\]\((images/[^)]+)\)", report):
        path = candidate / "reports" / "campaign" / image
        root = ET.parse(path).getroot()
        if not root.tag.endswith("svg") or not root.attrib.get("width") or not root.attrib.get("height"):
            raise AssertionError(f"invalid report image: {image}")


def verify_no_secrets(entries: list[dict]) -> None:
    patterns = [
        re.compile(r"hf_[A-Za-z0-9]{20,}"),
        re.compile(r"AKIA[0-9A-Z]{16}"),
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    ]
    for entry in entries:
        text = committed_bytes(entry["source"]).decode("utf-8")
        for pattern in patterns:
            if pattern.search(text):
                raise AssertionError(f"secret-like content in {entry['source']}")


def main() -> int:
    protected = json.loads(PROTECTED.read_text())
    entries = json.loads(ALLOWLIST.read_text())["entries"]
    targets = [entry["target"] for entry in entries]
    if len(targets) != len(set(targets)):
        raise AssertionError("upload allowlist contains duplicate targets")
    manifest_lines = (ROOT / "release" / "upload_manifest.sha256").read_text().splitlines()[1:]
    recorded = {line[66:]: line[:64] for line in manifest_lines if line}
    expected_sources = {entry["source"] for entry in entries} - {"release/upload_manifest.sha256"}
    if set(recorded) != expected_sources:
        raise AssertionError("static upload manifest does not match allowlist sources")
    for relative, expected in recorded.items():
        if hashlib.sha256(committed_bytes(relative)).hexdigest() != expected:
            raise AssertionError(f"static upload hash mismatch: {relative}")
    verify_no_secrets(entries)

    with tempfile.TemporaryDirectory(prefix="orx-judged-") as judged_dir, tempfile.TemporaryDirectory(prefix="orx-candidate-") as candidate_dir:
        judged = Path(judged_dir)
        candidate = Path(candidate_dir)
        snapshot_download(
            repo_id=protected["space_id"],
            repo_type="space",
            revision=protected["revision"],
            local_dir=judged,
        )
        for relative, expected in protected["files"].items():
            if sha256(judged / relative) != expected:
                raise AssertionError(f"judged source hash mismatch: {relative}")

        copy_candidate(judged, candidate, entries)
        candidate_files = {str(path.relative_to(candidate)) for path in candidate.rglob("*") if path.is_file() and ".cache" not in path.parts}
        if not set(protected["files"]).issubset(candidate_files):
            raise AssertionError("judged file set is not a subset of candidate")
        for relative, expected in protected["files"].items():
            if relative not in MUTABLE_PROTECTED and sha256(candidate / relative) != expected:
                raise AssertionError(f"protected historical file changed: {relative}")

        historical = ROOT / "release" / "historical_judged_881cb4"
        if sha256(historical / "README.md") != protected["files"]["README.md"]:
            raise AssertionError("historical README copy changed")
        if sha256(historical / "logbook.json") != protected["files"]["logbook.json"]:
            raise AssertionError("historical logbook copy changed")

        logbook = json.loads((candidate / "logbook.json").read_text())
        if logbook["space_id"] != protected["space_id"] or logbook["root"]["slug"] != "current-index":
            raise AssertionError("candidate canonical entrypoint is wrong")
        opened = []
        walk_pages(logbook["root"], candidate, opened)
        verify_current_pages(candidate, entries)
        verify_report(candidate)

        for raw in [
            ".openresearch/artifacts/claim1_paper_scale/raw/result.json",
            "outputs/claim2_attempt1_empirical_arl.json",
            "outputs/claim3_attempt1/result.json",
            ".openresearch/artifacts/claim4_figure_falsification/raw/result.json",
            ".openresearch/artifacts/claim5_reddit_reconstruction/raw/result.json",
            ".openresearch/artifacts/claim5_official_artifact_probe/raw/result.json",
            "outputs/claim6_attempt1/result.json",
        ]:
            json.loads((candidate / raw).read_text())

        manifest = {
            relative: sha256(candidate / relative)
            for relative in sorted(candidate_files)
        }
        result = {
            "candidate_files": len(candidate_files),
            "current_pages": VERDICTS,
            "judged_files_preserved": len(protected["files"]),
            "judged_file_set_is_subset": True,
            "navigation_files_opened": opened,
            "secret_scan": "PASS",
            "text_upload_files": len(entries),
            "upload_manifest": {entry["target"]: sha256(candidate / entry["target"]) for entry in entries},
            "candidate_tree_sha256": hashlib.sha256(json.dumps(manifest, sort_keys=True).encode()).hexdigest(),
            "verdict": "PASS",
        }
        print("RELEASE_CANDIDATE_AUDIT " + json.dumps(result, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
