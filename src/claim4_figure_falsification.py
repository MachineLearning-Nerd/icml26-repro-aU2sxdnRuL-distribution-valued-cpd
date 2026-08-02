#!/usr/bin/env python3
"""Digitize the camera-ready FlowCAP figure from the pinned arXiv source."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import os
import tarfile
import time
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ARCHIVE = ROOT / "paper_source" / "source.tar"
FIGURE_MEMBER = "figures/tradeoff_F1_vs_ARL0_singlecol.png"
EXPECTED_ARCHIVE_SHA256 = "6d4af865d403a1c4f72ed3ef8057069212ac1633aa79410b4607b04a8b9edb87"
EXPECTED_FIGURE_SHA256 = "e788172329eb5886009265a37733a037a158efecf7e85089a790cc8bd1af363a"
RAW = ROOT / ".openresearch" / "artifacts" / "claim4_figure_falsification" / "raw"


def available_cpus() -> int:
    if hasattr(os, "sched_getaffinity"):
        return len(os.sched_getaffinity(0))
    return os.cpu_count() or 1


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_figure() -> tuple[np.ndarray, bytes]:
    archive_bytes = SOURCE_ARCHIVE.read_bytes()
    if sha256(archive_bytes) != EXPECTED_ARCHIVE_SHA256:
        raise RuntimeError("pinned arXiv source archive hash changed")
    with tarfile.open(fileobj=io.BytesIO(archive_bytes)) as archive:
        figure_bytes = archive.extractfile(FIGURE_MEMBER).read()
    if sha256(figure_bytes) != EXPECTED_FIGURE_SHA256:
        raise RuntimeError("camera-ready FlowCAP figure hash changed")
    return np.asarray(Image.open(io.BytesIO(figure_bytes)).convert("RGB")), figure_bytes


def color_mask(image: np.ndarray, rgb: tuple[int, int, int], tolerance: int = 12) -> np.ndarray:
    target = np.asarray(rgb, dtype=np.int16)
    return np.max(np.abs(image.astype(np.int16) - target), axis=2) <= tolerance


def grouped(indices: np.ndarray, max_gap: int = 1) -> list[np.ndarray]:
    if len(indices) == 0:
        return []
    cuts = np.where(np.diff(indices) > max_gap)[0] + 1
    return list(np.split(indices, cuts))


def grid_rows(image: np.ndarray, x0: int, x1: int, y0: int, y1: int) -> list[float]:
    crop = image[y0:y1, x0:x1].astype(np.int16)
    neutral = (np.ptp(crop, axis=2) <= 2) & (crop.mean(axis=2) >= 160) & (crop.mean(axis=2) <= 248)
    counts = neutral.sum(axis=1)
    candidates = np.where(counts >= 0.55 * (x1 - x0))[0]
    return [float(y0 + group.mean()) for group in grouped(candidates) if len(group) <= 8]


def filled_diamond_centers(mask: np.ndarray, bounds: tuple[int, int, int, int]) -> list[tuple[float, float]]:
    x0, x1, y0, y1 = bounds
    crop = mask[y0:y1, x0:x1]
    dense_columns = np.where(crop.sum(axis=0) >= 13)[0]
    centers = []
    for group in grouped(dense_columns, max_gap=2):
        if len(group) < 4:
            continue
        lo = max(0, int(group[0]) - 3)
        hi = min(crop.shape[1], int(group[-1]) + 4)
        ys, xs = np.where(crop[:, lo:hi])
        if len(xs) < 80:
            continue
        centers.append((x0 + lo + float(np.median(xs)), y0 + float(np.median(ys))))
    return centers


def dense_filled_diamond_centers(mask: np.ndarray, bounds: tuple[int, int, int, int]) -> list[tuple[float, float]]:
    """Erode away connecting lines and outline markers, retaining filled diamonds."""
    x0, x1, y0, y1 = bounds
    crop = mask[y0:y1, x0:x1]
    eroded = ndimage.binary_erosion(crop, structure=np.ones((9, 9), dtype=bool))
    labels, count = ndimage.label(eroded)
    centers = []
    for label_id in range(1, count + 1):
        ys, xs = np.where(labels == label_id)
        if len(xs) < 8:
            continue
        cx, cy = int(round(float(xs.mean()))), int(round(float(ys.mean())))
        patch = crop[max(0, cy - 7):cy + 8, max(0, cx - 7):cx + 8]
        if patch.sum() < 140:
            continue
        centers.append((float(x0 + cx), float(y0 + cy)))
    return sorted(centers)


def outline_square_centers(mask: np.ndarray, bounds: tuple[int, int, int, int]) -> list[tuple[float, float]]:
    x0, x1, y0, y1 = bounds
    crop = mask[y0:y1, x0:x1]
    spans = np.zeros(crop.shape[1], dtype=int)
    for column in range(crop.shape[1]):
        rows = np.where(crop[:, column])[0]
        if len(rows):
            spans[column] = int(rows.max() - rows.min())
    marker_columns = np.where(spans >= 16)[0]
    centers = []
    for group in grouped(marker_columns, max_gap=2):
        if len(group) < 3:
            continue
        lo = max(0, int(group[0]) - 3)
        hi = min(crop.shape[1], int(group[-1]) + 4)
        ys, xs = np.where(crop[:, lo:hi])
        if len(xs) < 30:
            continue
        centers.append((x0 + lo + float(np.median(xs)), y0 + (float(ys.min()) + float(ys.max())) / 2))
    return centers


def nearest(rows: list[float], target: float, tolerance: float = 12) -> float:
    value = min(rows, key=lambda row: abs(row - target))
    if abs(value - target) > tolerance:
        raise RuntimeError(f"grid calibration row missing near {target}: {rows}")
    return value


def main() -> int:
    started = time.monotonic()
    RAW.mkdir(parents=True, exist_ok=True)
    image, figure_bytes = load_figure()
    if tuple(image.shape) != (601, 1232, 3):
        raise RuntimeError(f"unexpected figure dimensions: {image.shape}")

    # These bounds isolate the two axes. The legend is deliberately outside both crops.
    f1_bounds = (184, 545, 135, 500)
    arl1_bounds = (688, 1048, 135, 500)
    f1_rows = grid_rows(image, *f1_bounds)
    arl1_rows = grid_rows(image, *arl1_bounds)
    # Use internal gridlines because black axes spines can cover the 0 and 1 gridlines.
    f1_y08 = nearest(f1_rows, 207)
    f1_y02 = nearest(f1_rows, 426)
    f1_y0 = f1_y08 + (0.8 / 0.6) * (f1_y02 - f1_y08)
    f1_y1 = f1_y08 - (0.2 / 0.6) * (f1_y02 - f1_y08)
    arl1_y10 = nearest(arl1_rows, 356)
    arl1_y100 = nearest(arl1_rows, 143)

    red = color_mask(image, (214, 39, 40))
    orange = color_mask(image, (255, 127, 14))
    ours_f1_pixels = dense_filled_diamond_centers(red, f1_bounds)
    ours_arl1_pixels = dense_filled_diamond_centers(red, arl1_bounds)
    independent_arl1_pixels = filled_diamond_centers(red, arl1_bounds)
    hotelling_f1_pixels = outline_square_centers(orange, f1_bounds)

    def f1_value(y: float) -> float:
        return (f1_y0 - y) / (f1_y0 - f1_y1)

    def arl1_value(y: float) -> float:
        log10_value = 1.0 + (arl1_y10 - y) / (arl1_y10 - arl1_y100)
        return 10.0**log10_value

    ours_f1 = [f1_value(y) for _, y in ours_f1_pixels]
    ours_arl1 = [arl1_value(y) for _, y in ours_arl1_pixels]
    independent_arl1 = [arl1_value(y) for _, y in independent_arl1_pixels]
    hotelling_f1 = [f1_value(y) for _, y in hotelling_f1_pixels]

    # Negative control: a linear reading of a log-labelled axis is invalid here.
    linear_control = [10.0 + (arl1_y10 - y) * 90.0 / (arl1_y10 - arl1_y100) for _, y in ours_arl1_pixels]
    control_rejected = any(value <= 0 for value in linear_control)

    rows = []
    for method, metric, pixels, values in [
        ("IDD", "F1", ours_f1_pixels, ours_f1),
        ("IDD", "ARL1", ours_arl1_pixels, ours_arl1),
        ("HotellingT2", "F1", hotelling_f1_pixels, hotelling_f1),
    ]:
        for index, ((x, y), value) in enumerate(zip(pixels, values)):
            rows.append({"method": method, "metric": metric, "point": index, "pixel_x": x, "pixel_y": y, "value": value})

    result = {
        "claim": "On 7-D FlowCAP-II, IDD has F1 approximately 0.75 and ARL1 approximately 1, versus Hotelling T2 F1 below 0.4.",
        "contract": {
            "approximate_1_generous_upper_bound": 1.5,
            "falsification_rule": "FALSIFIED if every displayed IDD ARL1 point is above 1.5 after log-axis digitization.",
            "scope": "camera-ready paper claim and its original plotted evidence; not an independent raw-data rerun",
        },
        "source": {
            "archive_sha256": EXPECTED_ARCHIVE_SHA256,
            "figure_member": FIGURE_MEMBER,
            "figure_sha256": sha256(figure_bytes),
            "figure_shape": list(image.shape),
            "anchors": ["main0.tex:986", "main0.tex:998-1000", "main0.tex:1751", "main0.tex:1798-1810"],
        },
        "calibration": {
            "f1_grid_rows": f1_rows,
            "f1_zero_row": f1_y0,
            "f1_one_row": f1_y1,
            "arl1_grid_rows": arl1_rows,
            "arl1_10_row": arl1_y10,
            "arl1_100_row": arl1_y100,
        },
        "extracted": {
            "idd_f1": ours_f1,
            "idd_arl1": ours_arl1,
            "hotelling_f1": hotelling_f1,
            "idd_f1_max": max(ours_f1),
            "idd_arl1_min": min(ours_arl1),
            "idd_arl1_max": max(ours_arl1),
            "hotelling_f1_max": max(hotelling_f1),
        },
        "independent_checker": {
            "idd_arl1_marker_count": len(ours_arl1_pixels),
            "all_idd_arl1_above_2": all(value > 2.0 for value in ours_arl1),
            "red_fill_patch_pixels": [int(red[max(0, int(y) - 7):int(y) + 8, max(0, int(x) - 7):int(x) + 8].sum()) for x, y in ours_arl1_pixels],
            "column_method_marker_count": len(independent_arl1_pixels),
            "column_method_values": independent_arl1,
            "column_method_all_above_2": all(value > 2.0 for value in independent_arl1),
            "minimum_range_endpoint_gap": abs(min(ours_arl1) - min(independent_arl1)),
            "maximum_range_endpoint_gap": abs(max(ours_arl1) - max(independent_arl1)),
        },
        "negative_control": {
            "wrong_linear_axis_values": linear_control,
            "rejected": control_rejected,
            "reason": "A linear interpretation of the explicitly logarithmic ARL1 axis produces non-positive delays.",
        },
        "compute": {
            "estimated_cores": 2,
            "selected_flavor": "cpu-upgrade",
            "actual_available_cpus": available_cpus(),
            "gpu_requested": False,
            "runtime_seconds": round(time.monotonic() - started, 3),
        },
        "verdict": "FALSIFIED" if min(ours_arl1) > 1.5 else "NOT_FALSIFIED",
        "limitations": [
            "This is a quantitative audit of the paper's own original PNG, not a rerun from FlowCAP FCS files.",
            "The word approximately has no tolerance in the paper; the contract uses a generous 50% upper tolerance before inspecting coordinates.",
            "Raw FCS access remains authentication-blocked, so unrelated implementation or sampling claims are not verified here.",
        ],
    }
    (RAW / "result.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    with (RAW / "digitized_points.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["method", "metric", "point", "pixel_x", "pixel_y", "value"])
        writer.writeheader()
        writer.writerows(rows)
    print("CLAIM4_FIGURE_RESULT " + json.dumps(result, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
