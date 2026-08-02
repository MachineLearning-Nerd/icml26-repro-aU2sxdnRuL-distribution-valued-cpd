#!/usr/bin/env python3
"""Bounded primary-source probe of the FlowCAP-II archive."""

from __future__ import annotations

import hashlib
import http.cookiejar
import json
import os
import re
import ssl
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / ".openresearch" / "artifacts" / "claim4_flowcap" / "raw"
RECORD_URL = "https://flowrepository.org/id/FR-FCM-ZZYA"
DOWNLOAD_URL = "https://flowrepository.org/experiments/42/download_ziped_files"
CLIENT_ID = "FlowRepositoryRyzJl74CNkUp1Kpb"
API_URL = f"https://flowrepository.org/list/FR-FCM-ZZYA?client={CLIENT_ID}"
USER_AGENT = "OpenResearch-IDD-reproduction/1.0 (paper 2602.07252)"


def make_opener() -> tuple[urllib.request.OpenerDirector, http.cookiejar.CookieJar]:
    cookies = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cookies),
        urllib.request.HTTPSHandler(context=ssl._create_unverified_context()),
    )
    return opener, cookies


def fetch(opener: urllib.request.OpenerDirector, request: urllib.request.Request, limit: int) -> tuple[int, str, dict[str, str], bytes]:
    with opener.open(request, timeout=120) as response:
        body = response.read(limit)
        return response.status, response.geturl(), dict(response.headers.items()), body


def available_cpus() -> int:
    if hasattr(os, "sched_getaffinity"):
        return len(os.sched_getaffinity(0))
    return os.cpu_count() or 1


def main() -> int:
    started = time.monotonic()
    RAW.mkdir(parents=True, exist_ok=True)
    opener, cookies = make_opener()
    status, final_url, headers, html_bytes = fetch(
        opener,
        urllib.request.Request(RECORD_URL, headers={"User-Agent": USER_AGENT}),
        2_000_000,
    )
    html = html_bytes.decode("utf-8", errors="replace")
    all_fcs = sorted(set(re.findall(r"\b\d{4}\.FCS\b", html, flags=re.I)))
    aml_match = re.search(r"<th>[^<]*aml</th>\s*<td>(.*?)</td>", html, flags=re.I | re.S)
    aml_fcs = sorted(set(re.findall(r"\b\d{4}\.FCS\b", aml_match.group(1), flags=re.I))) if aml_match else []

    api_status, api_final_url, _, xml_bytes = fetch(
        opener,
        urllib.request.Request(API_URL, headers={"User-Agent": USER_AGENT}),
        20_000_000,
    )
    root = ET.fromstring(xml_bytes)
    files = []
    for node in root.iter():
        if node.tag.rsplit("}", 1)[-1] != "fcs-file":
            continue
        fields = {
            child.tag.rsplit("}", 1)[-1]: (child.text or "").strip()
            for child in node
        }
        if fields.get("file-name") and fields.get("url"):
            files.append(fields)
    if not files:
        raise RuntimeError("official API returned no FCS file records")

    range_request = urllib.request.Request(
        files[0]["url"],
        headers={"User-Agent": USER_AGENT, "Range": "bytes=0-1023"},
    )
    file_status, file_url, file_headers, prefix = fetch(opener, range_request, 1024)

    negative_status = None
    try:
        fetch(
            opener,
            urllib.request.Request(
                files[0]["url"] + ".openresearch-missing-control",
                headers={"User-Agent": USER_AGENT, "Range": "bytes=0-15"},
            ),
            16,
        )
    except urllib.error.HTTPError as error:
        negative_status = error.code

    result = {
        "verdict": "DATA_AVAILABLE" if prefix.startswith(b"PK") else "BLOCKED",
        "record": {
            "url": RECORD_URL,
            "retrieval_status": status,
            "final_url": final_url,
            "sha256": hashlib.sha256(html_bytes).hexdigest(),
            "bytes": len(html_bytes),
        },
        "manifest": {
            "fcs_files": len(all_fcs),
            "aml_fcs_files": len(aml_fcs),
            "healthy_fcs_files": len(all_fcs) - len(aml_fcs),
            "subjects_if_eight_panels_each": len(all_fcs) // 8,
            "aml_subjects_if_eight_panels_each": len(aml_fcs) // 8,
            "first_aml_file": aml_fcs[0] if aml_fcs else None,
            "last_aml_file": aml_fcs[-1] if aml_fcs else None,
        },
        "official_api": {
            "url": API_URL,
            "status": api_status,
            "final_url": api_final_url,
            "sha256": hashlib.sha256(xml_bytes).hexdigest(),
            "fcs_records": len(files),
            "total_declared_bytes": sum(int(item.get("file-size", 0)) for item in files),
            "records_with_md5": sum(bool(item.get("md5sum")) for item in files),
            "first_record": files[0],
            "session_cookie_count": len(cookies),
        },
        "file_probe": {
            "url": files[0]["url"],
            "status": file_status,
            "final_url": file_url,
            "content_type": file_headers.get("Content-Type"),
            "content_length": file_headers.get("Content-Length"),
            "content_range": file_headers.get("Content-Range"),
            "accept_ranges": file_headers.get("Accept-Ranges"),
            "prefix_bytes": len(prefix),
            "prefix_sha256": hashlib.sha256(prefix).hexdigest(),
            "fcs_header": prefix[:6].decode("ascii", errors="replace"),
        },
        "negative_control": {
            "nonexistent_experiment_http_status": negative_status,
            "rejected": negative_status in {404, 410},
        },
        "compute": {
            "estimated_cores": 2,
            "selected_flavor": "cpu-upgrade",
            "actual_available_cpus": available_cpus(),
            "gpu_requested": False,
            "runtime_seconds": round(time.monotonic() - started, 3),
        },
        "limitations": [
            "This bounded route establishes primary data availability and labels; it does not test Claim 4 performance.",
            "TLS verification is disabled because the primary server currently presents a certificate chain rejected by the job image; SHA-256 and exact URLs are recorded.",
            "Only the first 1,024 bytes of one directly addressed FCS file are requested before the full acquisition route is chosen.",
        ],
    }
    path = RAW / "probe.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("CLAIM4_PROBE " + json.dumps(result, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
