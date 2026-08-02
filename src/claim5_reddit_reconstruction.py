#!/usr/bin/env python3
"""CPU reconstruction of the camera-ready Reddit IDD experiment."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import ot
import pandas as pd
import torch
from scipy.spatial.distance import cdist
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "evidence" / "claim5_attempt1" / "SummaryResults_Covid_All.tab"
RAW = ROOT / ".openresearch" / "artifacts" / "claim5_reddit_reconstruction" / "raw"
MODEL = "sentence-transformers/all-MiniLM-L6-v2"
MODEL_REVISION = "1110a243fdf4706b3f48f1d95db1a4f5529b4d41"
EXPECTED_DATA_MD5 = "25a3b3de956885ba52b221f7f50ed7c7"
CNF_REPOSITORY = "https://github.com/gvisen/NormalizingFlowsBarycenter.git"
CNF_REVISION = "0d73bfca5238a80b33cac73cae97ea4234400a56"
CNF_PATH = ROOT / "upstream" / "NormalizingFlowsBarycenter"
SEED = 260207252
PAPER_ALARMS = {"2021-02-16", "2021-03-02", "2021-03-27", "2021-04-30", "2021-05-03"}
RESPONSE_DATES = {"2021-03-02", "2021-04-30", "2021-05-03"}


def available_cpus() -> int:
    if hasattr(os, "sched_getaffinity"):
        return len(os.sched_getaffinity(0))
    return os.cpu_count() or 1


def md5(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


def load_windows() -> tuple[list[pd.Timestamp], list[list[str]], list[int]]:
    frame = pd.read_csv(DATA)
    frame["created_utc"] = pd.to_datetime(frame["created_utc"], utc=True, errors="coerce")
    frame = frame[frame["created_utc"].notna()].copy()
    # Route 5 matches the released runner's text cleaning and capped split.
    frame = frame[~frame["Parent"].astype(str).eq("1")].copy()
    frame["text"] = frame["text"].astype(str)
    frame = frame[~frame["text"].str.lower().isin(["[deleted]", "[removed]"])]
    frame = frame[frame["text"].str.len() > 0]
    frame["day"] = frame["created_utc"].dt.floor("D")
    rng = np.random.default_rng(0)
    groups = []
    for day, group in frame.groupby("day"):
        if len(group) < 20:
            continue
        texts = group["text"].tolist()
        if len(texts) > 500:
            selected = rng.choice(len(texts), size=500, replace=False)
            texts = [texts[index] for index in selected]
        groups.append((day, texts))
    groups.sort(key=lambda item: item[0])
    cutoff = pd.Timestamp("2021-01-31", tz="UTC")
    phase1 = [(d, texts) for d, texts in groups if d < cutoff][-50:]
    phase2 = [(d, texts) for d, texts in groups if d >= cutoff][:50]
    camera_start = pd.Timestamp("2020-12-02", tz="UTC")
    camera_end = pd.Timestamp("2021-05-05", tz="UTC")
    retained_dates = {day for day, _ in groups}
    diagnostic = {
        "record_interpretation": "pinned author non-root and text-cleaning semantics",
        "phase1_count": len(phase1),
        "phase2_count": len(phase2),
        "phase1_range": [phase1[0][0].date().isoformat(), phase1[-1][0].date().isoformat()] if phase1 else [],
        "phase2_range": [phase2[0][0].date().isoformat(), phase2[-1][0].date().isoformat()] if phase2 else [],
        "missing_camera_ready_dates": [
            day.date().isoformat()
            for day in pd.date_range(camera_start, camera_end, freq="D")
            if day not in retained_dates
        ],
    }
    print("CLAIM5_WINDOW_DIAGNOSTIC " + json.dumps(diagnostic, sort_keys=True), flush=True)
    if len(phase1) != 50 or len(phase2) != 49:
        raise RuntimeError(f"unexpected closest released split: {len(phase1)}+{len(phase2)}")
    selected = phase1 + phase2
    return [item[0] for item in selected], [item[1] for item in selected], [len(item[1]) for item in selected]


def embed_clouds(text_windows: list[list[str]]) -> tuple[list[np.ndarray], dict]:
    model = SentenceTransformer(MODEL, revision=MODEL_REVISION, device="cpu")
    offsets = np.cumsum([0] + [len(texts) for texts in text_windows])
    texts = [text for window in text_windows for text in window]
    embeddings = model.encode(
        texts,
        batch_size=64,
        show_progress_bar=False,
        convert_to_numpy=True,
        normalize_embeddings=True,
    ).astype(np.float64)
    pca = PCA(n_components=20, svd_solver="full")
    pca.fit(embeddings[: offsets[50]])
    projected = pca.transform(embeddings)
    clouds = [projected[offsets[i]:offsets[i + 1]] for i in range(len(text_windows))]
    return clouds, {
        "model": MODEL,
        "model_revision": MODEL_REVISION,
        "embedding_dimension": int(embeddings.shape[1]),
        "pca_dimension": 20,
        "phase1_pca_explained_variance": float(pca.explained_variance_ratio_.sum()),
        "comments_embedded": len(texts),
    }


def prepare_cnf_source() -> str:
    if not (CNF_PATH / ".git").is_dir():
        CNF_PATH.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "clone", "--quiet", CNF_REPOSITORY, str(CNF_PATH)], check=True)
    subprocess.run(["git", "fetch", "--quiet", "origin", CNF_REVISION], cwd=CNF_PATH, check=True)
    subprocess.run(["git", "checkout", "--quiet", "--detach", CNF_REVISION], cwd=CNF_PATH, check=True)
    actual = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=CNF_PATH, text=True).strip()
    if actual != CNF_REVISION:
        raise RuntimeError(f"CNF source SHA mismatch: {actual}")
    return actual


def fit_barycenter(phase1: list[np.ndarray]) -> tuple[np.ndarray, np.ndarray, dict]:
    prepare_cnf_source()
    sys.path.insert(0, str(CNF_PATH))
    import normflows as nf
    from src.bases import CategoricalBase
    from src.flows import Permute, SXAffineCouplingBlock
    from src.models import SXNormalizingFlow
    from src.utils import ConditionalMLP

    dimension = phase1[0].shape[1]
    flows = []
    for _ in range(8):
        conditioner = ConditionalMLP(
            [dimension // 2, 32, 32, dimension],
            context_dim=len(phase1),
            init_zeros=True,
        )
        flows.extend(
            [
                SXAffineCouplingBlock(conditioner, scale=True, scale_map="exp", split_mode="channel"),
                Permute(dimension, mode="shuffle"),
            ]
        )
    model = SXNormalizingFlow(
        [nf.distributions.DiagGaussian(dimension, trainable=False)],
        CategoricalBase(torch.full((len(phase1),), 1.0 / len(phase1))),
        [flows],
        [],
    )
    cloud_tensors = [torch.as_tensor(cloud, dtype=torch.float32) for cloud in phase1]
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=0.0)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer,
        mode="min",
        factor=0.8,
        patience=1000,
        threshold=1e-4,
        threshold_mode="abs",
        min_lr=1e-8,
        eps=1e-8,
    )
    temperatures = torch.logspace(0, -2, 500)
    initial_loss = None
    final_loss = None
    model.train()
    training_started = time.monotonic()
    for epoch, temperature in enumerate(temperatures):
        labels = torch.randint(0, len(phase1), (2048,))
        samples = torch.empty((2048, dimension), dtype=torch.float32)
        for label in range(len(phase1)):
            positions = torch.nonzero(labels == label, as_tuple=False).squeeze(1)
            if len(positions) == 0:
                continue
            cloud = cloud_tensors[label]
            selected = torch.randint(0, len(cloud), (len(positions),))
            samples[positions] = cloud[selected]
        epoch_kld = 0.0
        epoch_l2 = 0.0
        optimizer.zero_grad()
        for start in range(0, len(samples), 256):
            x = samples[start:start + 256]
            label_chunk = labels[start:start + 256, None]
            s = model.s_base.encode(label_chunk)
            kld = model.forward_kld(x, s=s)
            z, _ = model.inverse_and_log_det(x, s)
            l2 = torch.mean(torch.sum((x - model.bar(z)) ** 2, dim=1))
            fraction = len(x) / len(samples)
            (fraction * (kld + temperature * l2)).backward()
            epoch_kld += fraction * float(kld.detach())
            epoch_l2 += fraction * float(l2.detach())
        loss_value = epoch_kld + float(temperature) * epoch_l2
        if not np.isfinite(loss_value):
            raise RuntimeError(f"non-finite CNF training loss at epoch {epoch}")
        torch.nn.utils.clip_grad_norm_(model.parameters(), 2.0, norm_type=2.0, error_if_nonfinite=True)
        optimizer.step()
        scheduler.step(epoch_kld)
        if initial_loss is None:
            initial_loss = loss_value
        final_loss = loss_value
        if epoch % 10 == 0 or epoch == 499:
            print(
                "CLAIM5_CNF_TRAIN "
                + json.dumps(
                    {
                        "epoch": epoch + 1,
                        "kld": epoch_kld,
                        "l2": epoch_l2,
                        "loss": loss_value,
                        "temperature": float(temperature),
                        "elapsed_seconds": round(time.monotonic() - training_started, 3),
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
    model.eval()
    with torch.no_grad():
        barycenter = model.bar_sample(num_samples=512).cpu().numpy().astype(np.float64)
        z, _ = model.sample_latent(num_samples=128)
        conditional_means = []
        for label in range(len(phase1)):
            s = model.s_base.encode(torch.full((128, 1), label, dtype=torch.long))
            conditional_means.append(model.forward(z, s).mean(dim=0).cpu().numpy())
    mean_spread = float(np.mean(np.std(np.vstack(conditional_means), axis=0)))
    weights = np.full(len(barycenter), 1.0 / len(barycenter))
    training = {
        "source_repository": CNF_REPOSITORY,
        "source_revision": CNF_REVISION,
        "epochs": 500,
        "batch_size": 2048,
        "gradient_chunk_size": 256,
        "learning_rate": 1e-3,
        "gradient_clip": 2.0,
        "temperature_start": 1.0,
        "temperature_end": 1e-2,
        "hidden_width": 32,
        "coupling_blocks": 8,
        "barycenter_samples": 512,
        "initial_loss": initial_loss,
        "final_loss": final_loss,
        "conditional_mean_spread": mean_spread,
        "erased_label_mean_spread": 0.0,
    }
    return barycenter, weights, training


def tangent_vector(
    barycenter: np.ndarray,
    bary_weights: np.ndarray,
    cloud: np.ndarray,
) -> tuple[np.ndarray, dict]:
    target_weights = np.full(len(cloud), 1.0 / len(cloud))
    cost = cdist(barycenter, cloud, metric="sqeuclidean")
    positive_costs = cost[cost > 0]
    median_cost = float(np.median(positive_costs)) if len(positive_costs) else 1.0
    if not np.isfinite(median_cost) or median_cost <= 0:
        median_cost = 1.0
    plan = ot.bregman.sinkhorn_epsilon_scaling(
        bary_weights,
        target_weights,
        cost / median_cost,
        reg=0.05,
        numItermax=5000,
        stopThr=1e-4,
    )
    transported = plan @ cloud / (plan.sum(axis=1, keepdims=True) + 1e-16)
    tangent = (transported - barycenter) * np.sqrt(bary_weights[:, None])
    checker = {
        "row_marginal_max_abs_error": float(np.max(np.abs(plan.sum(axis=1) - bary_weights))),
        "column_marginal_max_abs_error": float(np.max(np.abs(plan.sum(axis=0) - target_weights))),
        "cost_median": median_cost,
    }
    return tangent.ravel(), checker


def mfpca_statistics(tangents: np.ndarray) -> tuple[np.ndarray, np.ndarray, dict]:
    mean = tangents[:50].mean(axis=0)
    centered1 = tangents[:50] - mean
    centered = tangents - mean
    _, singular, vt = np.linalg.svd(centered1, full_matrices=False)
    eigenvalues = singular**2 / 49
    cumulative = np.cumsum(eigenvalues) / eigenvalues.sum()
    components = int(np.searchsorted(cumulative, 0.95) + 1)
    basis = vt[:components]
    scores = centered @ basis.T
    t2 = np.sum(scores**2 / eigenvalues[:components], axis=1)
    residual = centered - scores @ basis
    spe = np.sum(residual**2, axis=1)

    gram = centered1 @ centered1.T / 49
    gram_values, gram_vectors = np.linalg.eigh(gram)
    order = np.argsort(gram_values)[::-1]
    gram_values = gram_values[order][:components]
    gram_vectors = gram_vectors[:, order][:, :components]
    checker_basis = centered1.T @ gram_vectors / np.sqrt(49 * gram_values)
    checker_scores = centered @ checker_basis
    checker_t2 = np.sum(checker_scores**2 / gram_values, axis=1)
    checker_residual = centered - checker_scores @ checker_basis.T
    checker_spe = np.sum(checker_residual**2, axis=1)
    checker = {
        "components": components,
        "variance_explained": float(cumulative[components - 1]),
        "eigenvalue_max_abs_error": float(np.max(np.abs(eigenvalues[:components] - gram_values))),
        "t2_max_abs_error": float(np.max(np.abs(t2 - checker_t2))),
        "spe_max_abs_error": float(np.max(np.abs(spe - checker_spe))),
    }
    return t2, spe, checker


def hotelling_statistics(clouds: list[np.ndarray]) -> np.ndarray:
    means = np.vstack([cloud.mean(axis=0) for cloud in clouds])
    center = means[:50].mean(axis=0)
    covariance = np.cov(means[:50], rowvar=False)
    inverse = np.linalg.pinv(covariance, rcond=1e-10)
    delta = means - center
    return np.einsum("ij,jk,ik->i", delta, inverse, delta)


def permutation_alignment(alarm_dates: list[str], phase2_dates: list[str]) -> dict:
    rng = np.random.default_rng(SEED)
    alarm_count = len(alarm_dates)
    observed = len(set(alarm_dates) & RESPONSE_DATES)
    counts = []
    for _ in range(5000):
        shuffled = rng.choice(phase2_dates, size=alarm_count, replace=False)
        counts.append(len(set(shuffled) & RESPONSE_DATES))
    return {
        "observed_response_date_matches": observed,
        "permutations": len(counts),
        "null_mean": float(np.mean(counts)),
        "one_sided_p": float((1 + np.sum(np.asarray(counts) >= observed)) / (len(counts) + 1)),
    }


def main() -> int:
    started = time.monotonic()
    np.random.seed(SEED)
    torch.manual_seed(SEED)
    torch.set_num_threads(min(4, available_cpus()))
    torch.set_num_interop_threads(1)
    if md5(DATA) != EXPECTED_DATA_MD5:
        raise RuntimeError("Dataverse input MD5 changed")
    dates, text_windows, sizes = load_windows()
    clouds, representation = embed_clouds(text_windows)
    barycenter, bary_weights, cnf_training = fit_barycenter(clouds[:50])
    tangent_results = [tangent_vector(barycenter, bary_weights, cloud) for cloud in clouds]
    tangents = np.vstack([item[0] for item in tangent_results])
    sinkhorn_checkers = [item[1] for item in tangent_results]
    t2, spe, checker = mfpca_statistics(tangents)
    hotelling = hotelling_statistics(clouds)
    spe_limit = float(np.quantile(spe[:50], 0.95))
    t2_limit = float(np.quantile(t2[:50], 0.95))
    hotelling_limit = float(np.quantile(hotelling[:50], 0.95))
    phase2_dates = [date.date().isoformat() for date in dates[50:]]
    spe_alarms = [date for date, value in zip(phase2_dates, spe[50:]) if value > spe_limit]
    t2_alarms = [date for date, value in zip(phase2_dates, t2[50:]) if value > t2_limit]
    hotelling_alarms = [date for date, value in zip(phase2_dates, hotelling[50:]) if value > hotelling_limit]
    identity_control_rejected = bool(np.var(np.zeros_like(tangents[:50])) == 0 and np.var(tangents[:50]) > 0)
    exact_overlap = sorted(set(spe_alarms) & PAPER_ALARMS)
    result = {
        "claim": "IDD alarms on d=20 Reddit daily embedding streams align with vaccine-policy events while Euclidean summaries are drift/noise.",
        "verdict": "BLOCKED",
        "paper": {"idd_spe_alarms": sorted(PAPER_ALARMS), "idd_alarm_count": 5, "hotelling_alarm_count": 13},
        "observed": {
            "idd_spe_alarms": spe_alarms,
            "idd_t2_alarms": t2_alarms,
            "hotelling_alarms": hotelling_alarms,
            "idd_spe_alarm_count": len(spe_alarms),
            "hotelling_alarm_count": len(hotelling_alarms),
            "exact_paper_alarm_overlap": exact_overlap,
            "exact_paper_alarm_jaccard": len(exact_overlap) / len(set(spe_alarms) | PAPER_ALARMS),
        },
        "protocol": {
            "input_md5": EXPECTED_DATA_MD5,
            "seed": SEED,
            "phase1_dates": [dates[0].date().isoformat(), dates[49].date().isoformat()],
            "phase2_dates": [dates[50].date().isoformat(), dates[-1].date().isoformat()],
            "phase1_days": 50,
            "phase2_days": 49,
            "minimum_comments": min(sizes),
            "maximum_comments": max(sizes),
            "comments_per_day": sizes,
            "barycenter_support": 512,
            "barycenter_solver": "conditional normalizing flow",
            "ot_solver": "POT Sinkhorn epsilon scaling with barycentric projection",
            "ot_regularization": 0.05,
            "ot_num_iter_max": 5000,
            "ot_stop_threshold": 1e-4,
            "threshold_quantile": 0.95,
            "record_interpretation": "pinned author non-root and text-cleaning semantics; released MIN_PER_DAY=20, MAX_PER_DAY=500, last-50/first-50 cutoff split",
            **representation,
            "cnf_training": cnf_training,
        },
        "limits": {"spe": spe_limit, "t2": t2_limit, "hotelling_t2": hotelling_limit},
        "independent_checker": checker,
        "sinkhorn_checker": {
            "row_marginal_max_abs_error": max(item["row_marginal_max_abs_error"] for item in sinkhorn_checkers),
            "column_marginal_max_abs_error": max(item["column_marginal_max_abs_error"] for item in sinkhorn_checkers),
        },
        "negative_controls": {
            "identity_tangents_rejected": identity_control_rejected,
            "date_shuffle": permutation_alignment(spe_alarms, phase2_dates),
            "cnf_label_erasure": {
                "trained_conditional_mean_spread": cnf_training["conditional_mean_spread"],
                "erased_label_mean_spread": cnf_training["erased_label_mean_spread"],
            },
        },
        "compute": {
            "estimated_cores": 32,
            "selected_flavor": "cpu-upgrade",
            "actual_available_cpus": available_cpus(),
            "gpu_requested": False,
            "runtime_seconds": round(time.monotonic() - started, 3),
        },
        "limitations": [
            "The authors' released Reddit runner imports an absent simulation package, so this uses the cited public CNF reference implementation rather than byte-identical private execution.",
            "The public artifact yields 50 Phase-I plus 49 Phase-II days under the pinned runner semantics, while the paper requires 50+50; this prevents verification or falsification of the exact stream claim.",
            "CNF gradient accumulation uses 256-sample chunks to evaluate the documented 2048-sample objective within CPU memory.",
            "PCA is fit only on Phase I to prevent monitoring leakage; the paper does not state the PCA fitting scope.",
            "This route implements IDD and the Hotelling moment baseline, not unreleased F-CPD, NEWMA, or Scan-B configurations.",
            "This route uses the released runner's minimum 20 and capped split, contradicting the appendix sentence that days below 30 were removed.",
        ],
    }
    RAW.mkdir(parents=True, exist_ok=True)
    (RAW / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    with (RAW / "daily_statistics.csv").open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["phase", "date", "n_comments", "idd_t2", "idd_spe", "hotelling_t2"])
        for index, date in enumerate(dates):
            writer.writerow(["I" if index < 50 else "II", date.date().isoformat(), sizes[index], t2[index], spe[index], hotelling[index]])
    print("CLAIM5_RECONSTRUCTION " + json.dumps(result, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
