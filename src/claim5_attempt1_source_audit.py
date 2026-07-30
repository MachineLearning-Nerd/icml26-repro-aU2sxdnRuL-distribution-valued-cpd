"""Claim 5 attempt 1: source-faithful Reddit case-study availability audit.

This is intentionally not a proxy reproduction. It checks whether the pinned
release and the cited Harvard Dataverse record supply the exact input, embedding,
windowing, baseline outputs, and date/alarm artifacts needed to evaluate the
live qualitative event-alignment claim on CPU.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper_source" / "main0.tex"
UPSTREAM = ROOT / "upstream" / "IDD-icml"
RUNNER = UPSTREAM / "case_study" / "run_reddit_vax.py"
README = UPSTREAM / "README.md"
DATAVERSE = ROOT / "evidence" / "claim5_attempt1" / "dataverse_metadata.json"
OUT = ROOT / "outputs" / "claim5_attempt1_source_audit.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    paper = PAPER.read_text(encoding="utf-8")
    runner = RUNNER.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    dataverse = json.loads(DATAVERSE.read_text(encoding="utf-8"))
    files = dataverse["data"]["latestVersion"]["files"]
    target = next(
        entry for entry in files
        if entry["dataFile"]["filename"] == "SummaryResults_Covid_All.tab"
    )
    target_file = target["dataFile"]
    upstream_files = [str(path.relative_to(UPSTREAM)) for path in UPSTREAM.rglob("*") if path.is_file()]
    reddit_data_files = [
        path for path in upstream_files
        if "reddit" in path.lower() or "summaryresults_covid" in path.lower()
    ]

    paper_protocol = {
        "daily_batches": "aggregated user comments into daily batches" in paper,
        "minimum_30_comments": "fewer than 30 comments" in paper,
        "sbert_model": "all-MiniLM-L6-v2" in paper,
        "embedding_dimension_384": "384-dimensional embeddings" in paper,
        "pca_dimension_20": "d=20" in paper,
        "phase_dates": "Dec 2, 2020 -- Jan 30, 2021" in paper and "Jan 31 -- May 5, 2021" in paper,
        "jj_pause_date": "Apr 13" in paper and r"J\&J Pause" in paper,
        "qualitative_only": "Qualitative evaluation only" in paper,
    }
    runner_protocol = {
        "default_representation_is_sentiment3d": 'REPRESENTATIONS = ["sentiment3d"]' in runner,
        "pca20_is_optional": 'add "embed_pca20" when ready' in runner,
        "embedding_model_declared": 'EMBED_MODEL = "all-MiniLM-L6-v2"' in runner,
        "daily_windows": "make_daily_windows" in runner,
        "default_cutoff_is_jj_eua": 'CUTOFF_NAME = "jj_eua"' in runner,
        "jj_pause_marked": '"jj_pause":             pd.Timestamp("2021-04-13"' in runner,
        "all_phaseII_days_labeled_changed": "y_true_II = np.ones" in runner,
    }
    availability = {
        "dataverse_released": dataverse["data"]["latestVersion"]["versionState"] == "RELEASED",
        "target_file_name": target_file["filename"],
        "target_file_access_request": bool(target_file.get("fileAccessRequest")),
        "target_file_md5": target_file["md5"],
        "pinned_release_contains_reddit_raw_csv": any("SummaryResults_Covid_All" in path for path in reddit_data_files),
        "pinned_release_contains_precomputed_embeddings": any("embed" in path.lower() and path.lower().endswith((".npz", ".npy", ".csv")) for path in upstream_files),
        "pinned_release_contains_paper_figure_outputs": any("figure" in path.lower() and path.lower().endswith((".pdf", ".png", ".csv")) for path in upstream_files),
    }
    exact_run_possible = (
        availability["dataverse_released"]
        and not availability["target_file_access_request"]
        and availability["pinned_release_contains_reddit_raw_csv"]
        and availability["pinned_release_contains_precomputed_embeddings"]
    )
    payload = {
        "attempt": "claim_5_attempt_1_source_faithful_availability_audit",
        "claim": (
            "On Reddit vaccine-sentiment daily embedding streams (d=20, January-May 2021), "
            "IDD alarms align with real news events such as the April 13 J&J pause, while "
            "Euclidean-summary and moment-based baselines produce monotonic drift or noise unrelated to shocks."
        ),
        "sources": {
            "paper_source": "https://export.arxiv.org/e-print/2602.07252",
            "paper_source_sha256": sha256(PAPER),
            "pinned_author_repository": "https://github.com/yyzeng43/IDD-icml@c5b1db4060e5081e5c487f91792dc18c17603fd0",
            "dataverse_dataset": "https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/XJTBQM",
            "dataverse_metadata_sha256": sha256(DATAVERSE),
            "external_event_reference": "https://www.cdc.gov/mmwr/volumes/70/wr/mm7017e2.htm",
            "external_event_reference_note": "Retained as an official CDC contemporaneous J&J safety record; this audit does not infer alarm alignment from it.",
        },
        "paper_protocol": paper_protocol,
        "runner_protocol": runner_protocol,
        "availability": availability,
        "source_scope_findings": {
            "paper_describes_embedding_pca20": paper_protocol["sbert_model"] and paper_protocol["pca_dimension_20"],
            "pinned_runner_default_is_not_embedding_pca20": runner_protocol["default_representation_is_sentiment3d"],
            "runner_default_cutoff_differs_from_paper_revised_phase_dates": runner_protocol["default_cutoff_is_jj_eua"] and paper_protocol["phase_dates"],
            "runner_labels_all_phaseII_as_changed": runner_protocol["all_phaseII_days_labeled_changed"],
            "independent_event_alignment_computed": False,
        },
        "decision": {
            "cpu_source_faithful_run_executed": False,
            "exact_run_possible_from_released_inputs": exact_run_possible,
            "outcome": "inconclusive_source_faithful_data_and_outputs_unavailable",
            "reason": (
                "The paper documents a d=20 SBERT/PCA qualitative study, but the pinned runner defaults to "
                "3-D sentiment features and a different J&J-EUA cutoff. The cited released Dataverse metadata "
                "marks SummaryResults_Covid_All.tab as fileAccessRequest=true, and the pinned release contains no "
                "raw Reddit input, precomputed embeddings, result series, alarms, or Figure-4 outputs. Therefore "
                "the date/alarm alignment and baseline behavior cannot be independently recomputed on CPU. This is "
                "an availability/protocol finding, not a refutation of the underlying Reddit observations."
            ),
        },
    }
    required = ["daily_batches", "sbert_model", "pca_dimension_20", "phase_dates", "qualitative_only"]
    missing = [key for key in required if not paper_protocol[key]]
    if missing:
        raise AssertionError(f"missing expected paper protocol tokens: {missing}")
    if not runner_protocol["default_representation_is_sentiment3d"]:
        raise AssertionError("expected pinned runner sentiment3d default")
    if not availability["target_file_access_request"]:
        raise AssertionError("expected access-request restriction in authoritative metadata")
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
