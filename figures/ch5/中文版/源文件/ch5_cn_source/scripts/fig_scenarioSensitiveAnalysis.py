# -*- coding: utf-8 -*-
"""Rebuild Figure 5.10 from the existing five vector-rendered panels.

Only the colored scientific curves are sampled from the prior figure; all text,
axes, legends and layout are redrawn with the chapter-wide font convention.
"""
from pathlib import Path

import cnstyle
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT.parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)
PDF_METADATA = {"CreationDate": None, "ModDate": None}

IMAGE = Path(__file__).resolve().parent / "scen" / "full.png"
RGB = {
    "类别1": np.array([0, 143, 213]),
    "类别2": np.array([252, 79, 48]),
    "整体": np.array([229, 174, 56]),
}
STYLE = {
    "类别1": ("#008fd5", "s"),
    "类别2": ("#fc4f30", "o"),
    "整体": ("#e5ae38", None),
}
LEGEND_LABELS = {
    "类别1": "情况1",
    "类别2": "情况2",
    "整体": "情况3",
}

# Plotting-area bounds in the 200-dpi reference rendering: x0, y0, x1, y1.
AXES = [
    (140, 67, 1123, 706),
    (1323, 67, 2306, 706),
    (140, 901, 1123, 1540),
    (1323, 901, 2306, 1540),
    (735, 1735, 1711, 2374),
]
SUBTITLES = [
    "（a）出行距离小于10 km",
    "（b）出行距离为10–20 km",
    "（c）出行距离为20–30 km",
    "（d）出行距离为30–40 km",
    "（e）出行距离大于40 km",
]


def robust_quadratic(x, y):
    keep = np.isfinite(x) & np.isfinite(y)
    for _ in range(6):
        coeff = np.polyfit(x[keep], y[keep], 2)
        residual = y - np.polyval(coeff, x)
        med = np.median(residual[keep])
        mad = np.median(np.abs(residual[keep] - med)) + 1e-6
        keep = np.abs(residual - med) <= 3.5 * mad
    return coeff


def extract_curves(image, box):
    x0, y0, x1, y1 = box
    crop = image[y0:y1 + 1, x0:x1 + 1]
    curves = {}
    for name, color in RGB.items():
        dist2 = ((crop.astype(float) - color) ** 2).sum(axis=2)
        mask = dist2 < 1800
        px, py = [], []
        for column in range(mask.shape[1]):
            rows = np.flatnonzero(mask[:, column])
            if rows.size:
                px.append(column)
                py.append(float(np.median(rows)))
        px = np.asarray(px, float)
        py = np.asarray(py, float)
        x = 100.0 * px / (crop.shape[1] - 1)
        y = 1100.0 * (1.0 - py / (crop.shape[0] - 1))
        curves[name] = robust_quadratic(x, y)
    return curves


image = np.asarray(Image.open(IMAGE).convert("RGB"))
data = [extract_curves(image, box) for box in AXES]

fig = plt.figure(figsize=(14, 16.5), dpi=150)
grid = GridSpec(3, 4, hspace=0.62, wspace=0.55)
fig.subplots_adjust(left=0.08, right=0.98, top=0.98, bottom=0.08)
positions = [grid[0, 0:2], grid[0, 2:4], grid[1, 0:2], grid[1, 2:4], grid[2, 1:3]]

for position, subtitle, curves in zip(positions, SUBTITLES, data):
    ax = fig.add_subplot(position)
    ax.set_facecolor("#F0F0F0")
    xx = np.linspace(0, 100, 101)
    for name in ["类别1", "类别2", "整体"]:
        color, marker = STYLE[name]
        ax.plot(
            xx,
            np.polyval(curves[name], xx),
            color=color,
            linewidth=2.2,
            marker=marker,
            markersize=4.5 if marker else 0,
            markevery=10,
            label=LEGEND_LABELS[name],
        )
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 1100)
    ax.set_xticks([0, 20, 40, 60, 80, 100])
    ax.set_xticklabels(["0%", "20%", "40%", "60%", "80%", "100%"], fontsize=12)
    ax.set_yticks([0, 200, 400, 600, 800, 1000])
    ax.tick_params(axis="y", labelsize=12)
    ax.set_xlabel("MaaS方案出行时间水平", fontsize=13)
    ax.set_ylabel("转移至MaaS的人数", fontsize=13)
    ax.grid(True, color="white", linewidth=1.1)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.legend(fontsize=12, loc="center right", framealpha=0.9)
    ax.text(0.5, -0.27, subtitle, transform=ax.transAxes,
            ha="center", va="top", fontsize=16, fontweight="normal")

fig.savefig(OUT / "scenarioSensitiveAnalysis.pdf", bbox_inches="tight", metadata=PDF_METADATA)
fig.savefig(OUT / "scenarioSensitiveAnalysis.png", dpi=150, bbox_inches="tight")
print("saved scenarioSensitiveAnalysis")
