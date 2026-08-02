#!/usr/bin/env python3
"""Run the cumulative reproduction checks and print compute provenance."""

from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
import time


def available_cpus() -> int:
    if hasattr(os, "sched_getaffinity"):
        return len(os.sched_getaffinity(0))
    return os.cpu_count() or 1


def main() -> int:
    started = time.monotonic()
    metadata = {
        "estimated_cores": 4,
        "selected_flavor": "cpu-upgrade",
        "actual_logical_cpus": os.cpu_count(),
        "actual_available_cpus": available_cpus(),
        "machine": platform.machine(),
        "python": platform.python_version(),
        "gpu_requested": False,
    }
    print("CAMPAIGN_COMPUTE " + json.dumps(metadata, sort_keys=True), flush=True)
    result = subprocess.run([sys.executable, "-m", "pytest", "-q"], check=False)
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
