#!/usr/bin/env python3
"""Audit every official Dataverse representation of the Reddit comments file."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import os
import urllib.error
import urllib.request
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / ".openresearch" / "artifacts" / "claim5_official_artifact_probe" / "raw"
BASE_URL = "https://dataverse.harvard.edu/api/access/datafile/6430672"
ENDPOINTS = {
    "archival": BASE_URL,
    "original": BASE_URL + "?format=original",
    "preprocessed": BASE_URL + "?format=prep",
}
USER_AGENT = "OpenResearch-Reproduction/1.0 (paper 2602.07252)"


def download(url: str) -> tuple[bytes, dict[str, str]]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            return response.read(), {
                "http_status": response.status,
                "content_type": response.headers.get("Content-Type", ""),
                "content_disposition": response.headers.get("Content-Disposition", ""),
            }
    except urllib.error.HTTPError as error:
        return error.read(), {
            "http_status": error.code,
            "content_type": error.headers.get("Content-Type", ""),
            "content_disposition": error.headers.get("Content-Disposition", ""),
            "error_reason": str(error.reason),
        }


def parse_delimited(content: bytes, separator: str) -> dict:
    try:
        frame = pd.read_csv(io.BytesIO(content), sep=separator, low_memory=False)
    except Exception as error:
        return {"ok": False, "error_type": type(error).__name__}
    columns = [str(column) for column in frame.columns]
    lowered = {column: column.lower() for column in columns}
    date_columns = [column for column, value in lowered.items() if any(key in value for key in ("date", "created", "utc", "time"))]
    text_columns = [column for column, value in lowered.items() if any(key in value for key in ("text", "body", "comment"))]
    return {
        "ok": True,
        "rows": int(len(frame)),
        "columns": columns,
        "date_columns": date_columns,
        "text_columns": text_columns,
    }


def sniff_delimiter(content: bytes) -> str | None:
    try:
        sample = content[:65536].decode("utf-8", errors="strict")
        return csv.Sniffer().sniff(sample, delimiters=",\t;|").delimiter
    except (UnicodeDecodeError, csv.Error):
        return None


def window_audit(content: bytes, parse: dict, separator: str) -> dict | None:
    if not parse.get("date_columns") or not parse.get("text_columns"):
        return None
    frame = pd.read_csv(io.BytesIO(content), sep=separator, low_memory=False)
    date_column = parse["date_columns"][0]
    text_column = parse["text_columns"][0]
    dates = pd.to_datetime(frame[date_column], utc=True, errors="coerce")
    valid = frame[dates.notna()].copy()
    valid["_day"] = dates[dates.notna()].dt.floor("D")
    valid = valid[valid[text_column].notna()]
    counts = valid.groupby("_day").size()
    retained = counts[counts >= 30]
    phase1 = retained[(retained.index >= "2020-12-02") & (retained.index < "2021-01-31")]
    phase2 = retained[(retained.index >= "2021-01-31") & (retained.index <= "2021-05-05")]
    return {
        "date_column": date_column,
        "text_column": text_column,
        "valid_rows": int(len(valid)),
        "minimum_comments": 30,
        "phase1_days": int(len(phase1)),
        "phase2_days": int(len(phase2)),
    }


def main() -> int:
    RAW.mkdir(parents=True, exist_ok=True)
    representations = {}
    actionable = []
    for name, url in ENDPOINTS.items():
        content, headers = download(url)
        path = RAW / f"{name}.bin"
        path.write_bytes(content)
        delimiter = sniff_delimiter(content)
        parses = {
            "comma": parse_delimited(content, ","),
            "tab": parse_delimited(content, "\t"),
        }
        best_name = max(
            (key for key, value in parses.items() if value.get("ok")),
            key=lambda key: len(parses[key]["columns"]),
            default=None,
        )
        audit = None
        if best_name is not None:
            separator = "," if best_name == "comma" else "\t"
            audit = window_audit(content, parses[best_name], separator)
            if audit is not None:
                actionable.append({"representation": name, **audit})
        representations[name] = {
            "url": url,
            "sha256": hashlib.sha256(content).hexdigest(),
            "md5": hashlib.md5(content).hexdigest(),
            "bytes": len(content),
            "headers": headers,
            "prefix_hex_16": content[:16].hex(),
            "sniffed_delimiter": delimiter,
            "parses": parses,
            "best_parse": best_name,
            "window_audit": audit,
        }
        print(
            "CLAIM5_OFFICIAL_FETCH "
            + json.dumps(
                {
                    "representation": name,
                    "http_status": headers["http_status"],
                    "bytes": len(content),
                    "sha256": representations[name]["sha256"],
                },
                sort_keys=True,
            ),
            flush=True,
        )

    result = {
        "claim": 5,
        "source": {
            "datafile_id": 6430672,
            "retrieval_user_agent": USER_AGENT,
            "dataverse_rule": "default is archival TSV; format=original requests the saved upload",
        },
        "representations": representations,
        "independent_checker": {
            "csv_sniffer_recorded": True,
            "pandas_comma_and_tab_parsers_recorded": True,
            "distinct_hash_count": len({item["sha256"] for item in representations.values()}),
        },
        "negative_control": {
            "preprocessed_json_not_accepted_as_comment_stream": not any(
                item["representation"] == "preprocessed" for item in actionable
            )
        },
        "actionable_comment_streams": actionable,
        "verdict": "BLOCKED",
        "reason": (
            "The official representations do not expose an exact 50+50 dated text stream."
            if not any(item["phase1_days"] == 50 and item["phase2_days"] == 50 for item in actionable)
            else "An exact dated text representation was located; a full reconstruction must run on a child node before Claim 5 can change."
        ),
        "compute": {
            "estimated_cores": 2,
            "selected_flavor": "cpu-upgrade",
            "actual_available_cpus": len(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else os.cpu_count(),
            "gpu_requested": False,
        },
    }
    (RAW / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("CLAIM5_OFFICIAL_ARTIFACT_PROBE " + json.dumps(result, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
