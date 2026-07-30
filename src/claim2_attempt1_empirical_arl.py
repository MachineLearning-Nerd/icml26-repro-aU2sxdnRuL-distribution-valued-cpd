"""Claim 2 attempt 1: finite-sample empirical-quantile ARL audit.

This clean-room CPU audit follows the paper's Algorithm 1 structure at the
statistic level: fit fixed T2/SPE thresholds on a Phase-I reference sample,
then monitor independent Phase-II pairs until either chart exceeds its limit.
It tests the literal live claim against the source's stated finite-sample
corollary.  It is not a full IDD/mFPCA reproduction.
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"


def empirical_upper(values: np.ndarray, alpha: float) -> float:
    """Paper's k=ceil((1-alpha)n0) order statistic (one-indexed)."""
    n0 = len(values)
    k = int(np.ceil((1.0 - alpha) * n0))
    return float(np.sort(values)[k - 1])


def run_length(t2: np.ndarray, spe: np.ndarray, h_t2: float, h_spe: float) -> int:
    alarms = (t2 > h_t2) | (spe > h_spe)
    hit = np.flatnonzero(alarms)
    return int(hit[0]) + 1 if hit.size else len(alarms) + 1


def trial(rng: np.random.Generator, n0: int, horizon: int, alpha_t2: float, alpha_spe: float,
          threshold_scale: float = 1.0) -> tuple[int, float, float]:
    # Independent null statistic pair: each chart has a continuous chi-square(1)
    # null law.  Independence makes the union probability explicit and isolates
    # quantile calibration from the OT/mFPCA fitting layer.
    phase_i_t2 = rng.standard_normal(n0) ** 2
    phase_i_spe = rng.standard_normal(n0) ** 2
    h_t2 = threshold_scale * empirical_upper(phase_i_t2, alpha_t2)
    h_spe = threshold_scale * empirical_upper(phase_i_spe, alpha_spe)
    phase_ii_t2 = rng.standard_normal(horizon) ** 2
    phase_ii_spe = rng.standard_normal(horizon) ** 2
    return run_length(phase_ii_t2, phase_ii_spe, h_t2, h_spe), h_t2, h_spe


def main() -> None:
    n0, horizon, reps = 200, 5000, 4000
    alpha_t2 = alpha_spe = 0.01
    seed = 20260730
    rng = np.random.default_rng(seed)
    ordinary = np.array([trial(rng, n0, horizon, alpha_t2, alpha_spe)[0] for _ in range(reps)])
    # Intentional miscalibration control: halve limits, raising false-alarm risk.
    bad = np.array([trial(rng, n0, horizon, alpha_t2, alpha_spe, 0.5)[0] for _ in range(reps)])
    literal_bound = n0 + 1 + 1.0 / (alpha_t2 + alpha_spe)
    finite_sample_bound = n0 + 1 + 1.0 / (alpha_t2 + alpha_spe + 2.0 / (n0 + 1))
    payload = {
        "seed": seed,
        "null_model": "independent chi-square(1) T2 and SPE statistic pairs",
        "n0": n0,
        "horizon": horizon,
        "replications": reps,
        "alpha_T2": alpha_t2,
        "alpha_SPE": alpha_spe,
        "threshold_rule": "k=ceil((1-alpha)n0) empirical order statistic",
        "literal_live_claim_bound": literal_bound,
        "source_finite_sample_corollary_bound": finite_sample_bound,
        "ordinary": {
            "mean_monitoring_run_length": float(ordinary.mean()),
            "mean_global_arl_proxy": float(n0 + 1 + ordinary.mean()),
            "first_20_alarm_times": ordinary[:20].tolist(),
            "fraction_censored_at_horizon": float(np.mean(ordinary == horizon + 1)),
        },
        "miscalibrated_half_threshold_control": {
            "mean_monitoring_run_length": float(bad.mean()),
            "mean_global_arl_proxy": float(n0 + 1 + bad.mean()),
            "first_20_alarm_times": bad[:20].tolist(),
        },
    }
    OUT.mkdir(exist_ok=True)
    (OUT / "claim2_attempt1_empirical_arl.json").write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
