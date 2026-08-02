#!/usr/bin/env python3
"""CPU reconstruction of the camera-ready Reddit IDD experiment."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import time
import urllib.request
from pathlib import Path

import numpy as np
import ot
import pandas as pd
import torch
from scipy.spatial.distance import cdist
from sentence_transformers import SentenceTransformer
from sklearn.cluster import MiniBatchKMeans
from sklearn.decomposition import PCA


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / ".openresearch" / "artifacts" / "claim5_reddit_reconstruction" / "raw"
DATA = RAW / "inputs" / "SummaryResults_Covid_Comments.tab"
DATA_URL = "https://dataverse.harvard.edu/api/access/datafile/6430672"
MODEL = "sentence-transformers/all-MiniLM-L6-v2"
MODEL_REVISION = "1110a243fdf4706b3f48f1d95db1a4f5529b4d41"
EXPECTED_DATA_MD5 = "a87e5821d516f5195e45a2bd911495a5"
SEED = 260207252
PAPER_ALARMS = {"2021-02-16", "2021-03-02", "2021-03-27", "2021-04-30", "2021-05-03"}
RESPONSE_DATES = {"2021-03-02", "2021-04-30", "2021-05-03"}


def available_cpus() -> int:
    if hasattr(os, "sched_getaffinity"):
        return len(os.sched_getaffinity(0))
    return os.cpu_count() or 1


def md5(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()


def ensure_data() -> None:
    if DATA.exists() and md5(DATA) == EXPECTED_DATA_MD5:
        return
    request = urllib.request.Request(
        DATA_URL,
        headers={"User-Agent": "OpenResearch-Reproduction/1.0 (paper 2602.07252)"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        content = response.read()
    actual = hashlib.md5(content).hexdigest()
    if actual != EXPECTED_DATA_MD5:
        raise RuntimeError(f"official comments input MD5 mismatch: {actual}")
    DATA.parent.mkdir(parents=True, exist_ok=True)
    DATA.write_bytes(content)


def load_windows() -> tuple[list[pd.Timestamp], list[list[str]], list[int]]:
    frame = pd.read_csv(DATA)
    frame["created_utc"] = pd.to_datetime(frame["created_utc"], utc=True, errors="coerce")
    frame = frame[frame["created_utc"].notna()].copy()
    # Route 6 uses the official comments-only file and camera-ready filtering.
    if "Parent" in frame:
        frame = frame[~frame["Parent"].astype(str).eq("1")].copy()
    frame["text"] = frame["text"].astype(str)
    frame = frame[~frame["text"].str.lower().isin(["[deleted]", "[removed]"])]
    frame = frame[frame["text"].str.len() > 0]
    frame["day"] = frame["created_utc"].dt.floor("D")
    rng = np.random.default_rng(0)
    groups = []
    for day, group in frame.groupby("day"):
        if len(group) < 30:
            continue
        texts = group["text"].tolist()
        if len(texts) > 500:
            selected = rng.choice(len(texts), size=500, replace=False)
            texts = [texts[index] for index in selected]
        groups.append((day, texts))
    groups.sort(key=lambda item: item[0])
    camera_start = pd.Timestamp("2020-12-02", tz="UTC")
    cutoff = pd.Timestamp("2021-01-31", tz="UTC")
    camera_end = pd.Timestamp("2021-05-05", tz="UTC")
    phase1 = [(d, texts) for d, texts in groups if camera_start <= d < cutoff]
    phase2 = [(d, texts) for d, texts in groups if cutoff <= d <= camera_end]
    retained_dates = {day for day, _ in groups}
    diagnostic = {
        "record_interpretation": "official Dataverse comments-only file; camera-ready minimum-30 fixed windows",
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
    if len(phase1) != 50 or len(phase2) != 50:
        raise RuntimeError(f"camera-ready official-comments stream is not 50+50: {len(phase1)}+{len(phase2)}")
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
    clouds = [projected[offsets[i]:offsets[i + 1]] for i in range(100)]
    return clouds, {
        "model": MODEL,
        "model_revision": MODEL_REVISION,
        "embedding_dimension": int(embeddings.shape[1]),
        "pca_dimension": 20,
        "phase1_pca_explained_variance": float(pca.explained_variance_ratio_.sum()),
        "comments_embedded": len(texts),
    }


def fit_barycenter(phase1: list[np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    pooled = np.vstack(phase1)
    initial = MiniBatchKMeans(n_clusters=64, random_state=SEED, n_init=1, batch_size=1024).fit(pooled).cluster_centers_
    weights = [np.full(len(cloud), 1.0 / len(cloud)) for cloud in phase1]
    bary_weights = np.full(len(initial), 1.0 / len(initial))
    barycenter = ot.lp.free_support_barycenter(
        phase1,
        weights,
        initial,
        b=bary_weights,
        weights=np.full(len(phase1), 1.0 / len(phase1)),
        numItermax=20,
        stopThr=1e-6,
        numThreads=1,
    )
    return np.asarray(barycenter, dtype=np.float64), bary_weights


def tangent_vector(barycenter: np.ndarray, bary_weights: np.ndarray, cloud: np.ndarray) -> np.ndarray:
    target_weights = np.full(len(cloud), 1.0 / len(cloud))
    cost = cdist(barycenter, cloud, metric="sqeuclidean")
    plan = ot.emd(bary_weights, target_weights, cost, numThreads=1)
    transported = plan @ cloud / bary_weights[:, None]
    tangent = (transported - barycenter) * np.sqrt(bary_weights[:, None])
    return tangent.ravel()


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
    torch.set_num_threads(min(32, available_cpus()))
    ensure_data()
    if md5(DATA) != EXPECTED_DATA_MD5:
        raise RuntimeError("official comments Dataverse input MD5 changed")
    dates, text_windows, sizes = load_windows()
    clouds, representation = embed_clouds(text_windows)
    barycenter, bary_weights = fit_barycenter(clouds[:50])
    tangents = np.vstack([tangent_vector(barycenter, bary_weights, cloud) for cloud in clouds])
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
        "verdict": "VERIFIED" if set(spe_alarms) == PAPER_ALARMS and len(hotelling_alarms) == 13 else "BLOCKED",
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
            "phase2_days": 50,
            "minimum_comments": min(sizes),
            "maximum_comments": max(sizes),
            "comments_per_day": sizes,
            "barycenter_support": 64,
            "ot_solver": "exact EMD with barycentric projection",
            "threshold_quantile": 0.95,
            "record_interpretation": "official SummaryResults_Covid_Comments; camera-ready MIN_PER_DAY=30 and fixed date windows",
            **representation,
        },
        "limits": {"spe": spe_limit, "t2": t2_limit, "hotelling_t2": hotelling_limit},
        "independent_checker": checker,
        "negative_controls": {
            "identity_tangents_rejected": identity_control_rejected,
            "date_shuffle": permutation_alignment(spe_alarms, phase2_dates),
        },
        "compute": {
            "estimated_cores": 32,
            "selected_flavor": "cpu-upgrade",
            "actual_available_cpus": available_cpus(),
            "gpu_requested": False,
            "runtime_seconds": round(time.monotonic() - started, 3),
        },
        "limitations": [
            "The authors' released Reddit runner imports an absent simulation package, so this is an equation-level reconstruction rather than byte-identical released execution.",
            "The 64-support free Wasserstein barycenter is deterministic but its support size is not specified in the paper.",
            "PCA is fit only on Phase I to prevent monitoring leakage; the paper does not state the PCA fitting scope.",
            "This route implements IDD and the Hotelling moment baseline, not unreleased F-CPD, NEWMA, or Scan-B configurations.",
            "This route uses the separate official comments-only Dataverse file and the camera-ready minimum-30 fixed windows; the pinned runner instead names the All file and defaults to minimum 20.",
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
