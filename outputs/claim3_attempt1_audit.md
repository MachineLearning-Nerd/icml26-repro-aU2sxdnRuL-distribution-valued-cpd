# Claim 3 — Attempt 1: source-faithful Table-1 audit and high-variance input generation

## Exact live claim

> On Gaussian-translation synthetic streams, IDD achieves up to a 95% reduction in detection delay compared to the best-tuned Log-KDE baseline in high-variance settings, at matched ARL_0 (Table 1).

## Pinned sources and released protocol

- Manuscript source: `paper_source/main0.tex`, Table `tab:gauss_full` (lines 1479–1524), SHA retained in the paper source archive.
- Official implementation pin: `yyzeng43/IDD-icml@c5b1db4060e5081e5c487f91792dc18c17603fd0`.
- Full runner: `upstream/IDD-icml/gaussian_translation/run_scripts_all.py`.
- Generator: `upstream/IDD-icml/gaussian_translation/data_generation/generate_gaussian_data.py`.

The released generator specifies `d in {1,2,5}`, `sigma in {0.5,1,2}`, `delta1 in {0.1,0.5}`, 10 replications, 100 particles per distribution, 200 Phase-I distributions, and 200 IC plus 200 OC Phase-II distributions.  Its high-variance setting is `sigma=2.0`. The runner uses Log-KDE bandwidth grid `[auto, 0.5, 1.0, 1.5]` and takes the minimum displayed Log-KDE mean for this audit.

## Full-scale blocker

The released proposed-method runner calls `Rscript ot_mfpca_once.R`; `Rscript` is absent in this CPU environment, so the `funcharts` mFPCA stage cannot run. This blocks an execution that could reproduce the exact Table-1 IDD and matched-ARL comparison. It is an environment/source dependency blocker, not evidence that the method fails.

Two source inconsistencies are retained:

1. The manuscript states synthetic calibration length `n0=300`, while the released Gaussian generator sets `n_phaseI=200`.
2. The released runner skips `d<5`, but the displayed Table 1 includes `d=1` and `d=2` rows.

## Closest feasible CPU run

`src/claim3_attempt1_source_audit.py` imported the **released generator** and generated the entire `d=5, sigma=2.0, delta1=0.1` high-variance family: 10 deterministic replicates, each with 200 Phase-I, 200 IC, and 200 OC distributions of 100 points in five dimensions. It applies the source's IC recentering. The raw NPZ inputs remain under `outputs/claim3_attempt1/generated_data/`; `result.json` contains their per-file SHA-256 hashes, seeds, shapes, and realized mean-shift norms.

This is source-faithful generation, but it is not a full IDD-vs-Log-KDE Table-1 reproduction because the released R mFPCA dependency is unavailable. It is therefore **not** used to claim the table metric.

## Table evidence and matched-ARL sensitivity

The full table itself labels its numbers as `ARL_1 at matched ARL_0`, but no per-method ARL_0 values, threshold-tuning outputs, or raw alarms are released in the table. Consequently, source-table arithmetic alone cannot independently validate the matched-ARL condition.

Parsing all 18 rows of the pinned `tab:gauss_full` shows:

- The largest displayed high-variance (`sigma=2.0`) reduction against the **best** displayed Log-KDE bandwidth is **72.5%**, at `d=5, sigma=2.0, delta1=0.5`: IDD `1.1` versus best Log-KDE `4.0`.
- The table prints `up-arrow 95.1%`/similar annotations on low-variance (`sigma=0.5`, `delta=0.5`) rows, but IDD and every displayed Log-KDE bandwidth are all reported as `1.0`. Directly computing `(best Log-KDE - IDD) / best Log-KDE` gives zero there, not 95%.
- No row in the full table yields a computed IDD-over-best-Log-KDE reduction of 95% or more.

Thus the pinned table does not support the literal combination “up to 95%”, “versus best-tuned Log-KDE”, and “high-variance settings.” The source's own high-variance maximum in the displayed table is 72.5%, below 95%.

## Verdict

**Falsified (source-table scope).** The literal live claim is contradicted by the source's full displayed Table 1 arithmetic. This does **not** assert that the broader IDD method is ineffective; it only rejects the stated 95%-high-variance-best-tuned Table-1 result. The exact full experiment remains unavailable until the R/funcharts dependency can be executed.

## Artifacts

- `outputs/claim3_attempt1/result.json` — table parse, rows, protocol facts, raw-generator manifest, and verdict.
- `outputs/claim3_attempt1_run.log` — deterministic generation execution log.
- `outputs/claim3_attempt1_r_probe.log` — `Rscript` availability probe.
- `outputs/claim3_attempt1_matplotlib_install.log` — isolated environment dependency install log.
- `src/claim3_attempt1_source_audit.py` and `tests/test_claim3_attempt1.py` — executable audit and regression checks.
