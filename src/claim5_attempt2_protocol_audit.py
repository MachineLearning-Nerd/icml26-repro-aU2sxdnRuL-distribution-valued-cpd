"""Claim 5 Attempt 2: source-history and packaging/protocol availability audit."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence" / "claim5_attempt2"
OUTPUT = ROOT / "outputs" / "claim5_attempt2"


def main() -> None:
    commits = json.loads((EVIDENCE / "github_commits_runner.json").read_text())
    releases = json.loads((EVIDENCE / "github_releases.json").read_text())
    tags = json.loads((EVIDENCE / "github_tags.json").read_text())
    source = (ROOT / "upstream" / "IDD-icml" / "idd_core" / "ot_mfpca_flow.py").read_text()
    runner_log = (OUTPUT / "repaired_import_runner.log").read_text()
    result = {
        "runner_path_commits": [
            {"sha": row["sha"], "date": row["commit"]["author"]["date"], "message": row["commit"]["message"].splitlines()[0]}
            for row in commits
        ],
        "release_count": len(releases),
        "tag_count": len(tags),
        "missing_module_import": "from simulation.OT_KDE_Comp" in source,
        "isolated_import_repair_exit_code": int((OUTPUT / "repaired_import_exit_code.txt").read_text().strip()),
        "isolated_import_repair_still_fails": "ModuleNotFoundError: No module named 'simulation'" in runner_log,
        "paper_era_embedding_or_figure_outputs_recovered": False,
        "verdict": "inconclusive",
        "reason": "The public path history has one post-paper reproducibility-script commit and no releases/tags; the source imports an absent simulation package, and no recoverable paper-era embedding cache, dated alarm series, baseline output, or Figure-4 result is present.",
    }
    (OUTPUT / "protocol_history_audit.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
