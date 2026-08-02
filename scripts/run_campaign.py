#!/usr/bin/env python3
"""Run the cumulative reproduction checks and print compute provenance."""

from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / "upstream" / "IDD-icml"
UPSTREAM_URL = "https://github.com/yyzeng43/IDD-icml.git"
UPSTREAM_SHA = "c5b1db4060e5081e5c487f91792dc18c17603fd0"


def available_cpus() -> int:
    if hasattr(os, "sched_getaffinity"):
        return len(os.sched_getaffinity(0))
    return os.cpu_count() or 1


def output(*command: str, cwd: Path = ROOT) -> str:
    return subprocess.check_output(command, cwd=cwd, text=True).strip()


def prepare_upstream() -> str:
    if not (UPSTREAM / ".git").is_dir():
        UPSTREAM.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["git", "clone", "--quiet", UPSTREAM_URL, str(UPSTREAM)],
            cwd=ROOT,
            check=True,
        )
    subprocess.run(
        ["git", "fetch", "--quiet", "origin", UPSTREAM_SHA],
        cwd=UPSTREAM,
        check=True,
    )
    subprocess.run(
        ["git", "checkout", "--quiet", "--detach", UPSTREAM_SHA],
        cwd=UPSTREAM,
        check=True,
    )
    actual = output("git", "rev-parse", "HEAD", cwd=UPSTREAM)
    if actual != UPSTREAM_SHA:
        raise RuntimeError(f"upstream SHA mismatch: {actual}")
    return actual


def main() -> int:
    started = time.monotonic()
    upstream_sha = prepare_upstream()
    metadata = {
        "campaign_git_sha": output("git", "rev-parse", "HEAD"),
        "estimated_cores": 4,
        "selected_flavor": "cpu-upgrade",
        "actual_logical_cpus": os.cpu_count(),
        "actual_available_cpus": available_cpus(),
        "machine": platform.machine(),
        "python": platform.python_version(),
        "gpu_requested": False,
        "upstream_git_sha": upstream_sha,
    }
    print("CAMPAIGN_COMPUTE " + json.dumps(metadata, sort_keys=True), flush=True)
    result = subprocess.run([sys.executable, "-m", "pytest", "-q", "-s"], check=False)
    print(
        "CAMPAIGN_RESULT "
        + json.dumps(
            {
                "exit_code": result.returncode,
                "runtime_seconds": round(time.monotonic() - started, 3),
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
