"""Claim 3 attempt 1: source-table audit and faithful high-variance data generation.

This does not replace the released R/mFPCA pipeline.  It records whether the
literal jury wording is supported by the pinned manuscript/table and generates
the exact d=5, sigma=2, delta=0.1, ten-replicate stream family specified by the
released Gaussian generator.  Full Table-1 execution needs Rscript+funcharts.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper_source" / "main0.tex"
UPSTREAM = ROOT / "upstream" / "IDD-icml"
OUT = ROOT / "outputs" / "claim3_attempt1"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def table_rows(tex: str) -> list[dict[str, float]]:
    start = tex.index(r"\label{tab:gauss_full}")
    end = tex.index(r"\end{table*}", start)
    body = tex[start:end]
    # Fields before each LaTex ``\\pm`` are enough to assess the reported means.
    rows = []
    for line in body.splitlines():
        if not re.match(r"^\s*\d+\s*&", line) or r"\pm" not in line:
            continue
        columns = [column.strip() for column in line.split("&")]
        if len(columns) != 9:
            raise RuntimeError(f"unexpected Table gauss_full column count: {line}")
        d, sigma, delta = int(columns[0]), float(columns[1]), float(columns[2])
        means = []
        for column in columns[3:]:
            match = re.search(r"([0-9]+(?:\.[0-9]+)?)\s*(?:\$\s*)?\\pm", column)
            if match is None:
                raise RuntimeError(f"could not parse reported mean: {column}")
            means.append(float(match.group(1)))
        _hotelling, ours, h05, h1, h15, auto = means
        best = min(h05, h1, h15, auto)
        reduction = (best - ours) / best if best else 0.0
        rows.append({
            "d": d, "sigma": sigma, "delta": delta,
            "ours": ours, "best_logkde": best,
            "reduction_fraction": reduction,
        })
    if len(rows) != 18:
        raise RuntimeError(f"expected 18 Table gauss_full rows, parsed {len(rows)}")
    return rows


def generate_high_variance_streams(data_dir: Path) -> list[dict[str, object]]:
    sys.path.insert(0, str(UPSTREAM / "gaussian_translation" / "data_generation"))
    from generate_gaussian_data import generate_gaussian_phaseI_phaseII, recenter_phaseII_ic_to_phaseI_mean

    records = []
    d, sigma, delta1 = 5, 2.0, 0.1
    config = "gauss_shift_d5_sig2p00_del0p10"
    config_dir = data_dir / config
    config_dir.mkdir(parents=True, exist_ok=True)
    delta = np.full(d, delta1, dtype=float)
    for rep in range(10):
        seed = 42 + 1000 * d + 100 * int(round(10 * sigma)) + 10 * int(round(10 * delta1)) + rep
        prefix = f"{config}_rep{rep:02d}"
        phase_i, phase_ii_ic, phase_ii_oc = generate_gaussian_phaseI_phaseII(
            out_dir=config_dir,
            op_name=prefix,
            d=d,
            n_points=100,
            n_phaseI=200,
            n_phaseII_ic=200,
            n_phaseII_oc=200,
            sigma=sigma,
            delta=delta,
            random_state=seed,
        )
        recenter_phaseII_ic_to_phaseI_mean(phase_i, phase_ii_ic)
        phase_i_clouds = np.load(phase_i, allow_pickle=True)["phaseI"]
        phase_oc_clouds = np.load(phase_ii_oc, allow_pickle=True)["streams"]
        records.append({
            "rep": rep,
            "seed": seed,
            "phase_i": phase_i.name,
            "phase_ii_ic": phase_ii_ic.name,
            "phase_ii_oc": phase_ii_oc.name,
            "phase_i_shape": list(phase_i_clouds.shape),
            "phase_ii_oc_shape": list(phase_oc_clouds.shape),
            "mean_shift_norm": float(np.linalg.norm(np.vstack(phase_oc_clouds).mean(axis=0) - np.vstack(phase_i_clouds).mean(axis=0))),
            "sha256": {"phase_i": sha256(phase_i), "phase_ii_ic": sha256(phase_ii_ic), "phase_ii_oc": sha256(phase_ii_oc)},
        })
    return records


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    tex = PAPER.read_text()
    rows = table_rows(tex)
    high = [row for row in rows if row["sigma"] == 2.0]
    best_high = max(high, key=lambda row: row["reduction_fraction"])
    tagged_95 = [row for row in rows if row["reduction_fraction"] >= 0.95]

    # Full generated high-variance input is retained locally but not committed;
    # the manifest hashes make it reproducible from the pinned source generator.
    data_dir = OUT / "generated_data"
    generated = generate_high_variance_streams(data_dir)
    rscript = shutil.which("Rscript")
    runner = (UPSTREAM / "gaussian_translation" / "run_scripts_all.py").read_text()
    generator = (UPSTREAM / "gaussian_translation" / "data_generation" / "generate_gaussian_data.py").read_text()

    result = {
        "attempt": "claim_3_attempt_1",
        "scope": "source-faithful audit plus released high-variance generator",
        "table_full_rows": rows,
        "high_variance_sigma_2_rows": high,
        "maximum_reported_high_variance_reduction_fraction": best_high["reduction_fraction"],
        "maximum_reported_high_variance_reduction_percent": 100 * best_high["reduction_fraction"],
        "maximum_high_variance_row": best_high,
        "rows_with_reported_reduction_at_least_95_percent": tagged_95,
        "rscript_available": rscript is not None,
        "full_pipeline_blocker": None if rscript else "Rscript is absent; released IDD mFPCA runner invokes ot_mfpca_once.R and cannot execute Table 1.",
        "protocol_observations": {
            "paper_synthetic_calibration_length": 300,
            "released_generator_phase_i_length": 200,
            "released_generator_phase_ii_ic_length": 200,
            "released_generator_phase_ii_oc_length": 200,
            "released_generator_replications": 10,
            "released_generator_high_variance": "sigma=2.0",
            "released_runner_skips_dimensions_below_5": "if d < 5: continue" in runner,
            "table_contains_d1_and_d2": True,
            "bandwidth_grid": "[None, 0.5, 1.0, 1.5]",
            "source_files": {
                "manuscript": str(PAPER.relative_to(ROOT)),
                "runner": "upstream/IDD-icml/gaussian_translation/run_scripts_all.py",
                "generator": "upstream/IDD-icml/gaussian_translation/data_generation/generate_gaussian_data.py",
            },
        },
        "generated_high_variance_manifest": generated,
        "verdict": "falsified_source_table_scope",
        "verdict_reason": "The pinned full table's greatest high-variance (sigma=2) reduction against the best displayed Log-KDE bandwidth is 72.5%, not 95%; its >=95% table rows are low-variance/tied-delay rows. Full empirical reproduction remains unavailable without Rscript/funcharts.",
    }
    (OUT / "result.json").write_text(json.dumps(result, indent=2))
    print(json.dumps({
        "max_high_variance_reduction_percent": result["maximum_reported_high_variance_reduction_percent"],
        "max_high_variance_row": best_high,
        "rscript_available": result["rscript_available"],
        "generated_replicates": len(generated),
    }, indent=2))


if __name__ == "__main__":
    main()
