#!/usr/bin/env python3
"""Publish the gated text allowlist to the existing protected Space."""

from __future__ import annotations

import json
from pathlib import Path

from huggingface_hub import CommitOperationAdd, HfApi


ROOT = Path(__file__).resolve().parents[1]
ALLOWLIST = ROOT / "release" / "upload_allowlist.json"
PROTECTED = ROOT / "release" / "protected_judged_manifest.json"


def main() -> int:
    protected = json.loads(PROTECTED.read_text())
    entries = json.loads(ALLOWLIST.read_text())["entries"]
    api = HfApi()
    info = api.repo_info(protected["space_id"], repo_type="space")
    if info.sha != protected["revision"]:
        raise RuntimeError(f"Space head changed unexpectedly: {info.sha}")
    operations = []
    for entry in entries:
        source = ROOT / entry["source"]
        source.read_bytes().decode("utf-8")
        operations.append(CommitOperationAdd(path_in_repo=entry["target"], path_or_fileobj=str(source)))
    commit = api.create_commit(
        repo_id=protected["space_id"],
        repo_type="space",
        operations=operations,
        commit_message="Publish claim-by-claim CPU reproduction evidence",
        parent_commit=protected["revision"],
    )
    print(json.dumps({"published_revision": commit.oid, "space_id": protected["space_id"], "text_files": len(operations)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
