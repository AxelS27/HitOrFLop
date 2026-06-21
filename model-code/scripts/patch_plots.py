"""Regenerate 2 plots flagged by deck QA:
1. tuning_02_improvement.png — negative-bar label overlapped the y-axis label.
2. eda_05_correlation_heatmap.png — 13x13 cells illegible; rebuild as 6x6
   (model features + popularity) with larger annotations.
"""
import os, json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
PLOTS = os.path.join(DOCS, "plots")

BG = "#0A0A0A"; PANEL = "#181818"; ACCENT = "#1DB954"; ACCENT2 = "#1ED760"
TEXT = "#FFFFFF"; MUTED = "#B3B3B3"
plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": PANEL,
    "savefig.facecolor": BG, "axes.edgecolor": MUTED,
    "axes.labelcolor": TEXT, "xtick.color": MUTED, "ytick.color": MUTED,
    "text.color": TEXT, "font.size": 11, "axes.titlesize": 14,
    "axes.titleweight": "bold", "axes.grid": True, "grid.color": "#2A2A2A",
    "grid.linestyle": "--", "grid.linewidth": 0.6, "font.family": "DejaVu Sans",
})

# ---------- 1. tuning improvement ----------
res = pd.read_csv(os.path.join(DOCS, "tuning_results.csv"))
pivot = res.pivot_table(index="Model", columns="Stage", values="F1")
deltas = ((pivot["Tuned"] - pivot["Default"]) * 100).sort_values()

fig, ax = plt.subplots(figsize=(10, 5))
colors = [ACCENT2 if v >= 0 else "#E0245E" for v in deltas.values]
bars = ax.barh(deltas.index, deltas.values, color=colors, edgecolor=BG)
for b, v in zip(bars, deltas.values):
    if v >= 0:
        ax.text(v + 0.12, b.get_y() + b.get_height()/2, f"+{v:.2f} pp",
                va="center", ha="left", fontweight="bold", color=TEXT, fontsize=11)
    else:
        # place label to the RIGHT of the zero line so it never hits axis labels
        ax.text(0.12, b.get_y() + b.get_height()/2, f"{v:.2f} pp",
                va="center", ha="left", fontweight="bold", color="#E0245E", fontsize=11)
ax.axvline(0, color=MUTED, linewidth=1)
ax.set_xlim(deltas.min() - 1.2, deltas.max() + 1.6)
ax.set_xlabel("Δ F1 (percentage points)")
ax.set_title("F1 Improvement after Tuning", loc="left")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS, "tuning_02_improvement.png"), dpi=160)
plt.close()
print("ok: tuning_02_improvement.png")

# ---------- 2. compact correlation heatmap ----------
df = pd.read_csv(os.path.join(ROOT, "data", "dataset.csv"))
FEATS = ["tempo", "loudness", "key", "mode", "energy", "popularity"]
df = df.dropna(subset=FEATS)
df = df[df["energy"] > 0.1]
corr = df[FEATS].corr()

fig, ax = plt.subplots(figsize=(8, 6.4))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdYlGn", center=0,
            linewidths=1.5, linecolor=BG, ax=ax, vmin=-1, vmax=1,
            cbar_kws={"shrink": .85},
            annot_kws={"size": 14, "color": "#111", "weight": "bold"})
ax.set_title("Korelasi Fitur Model + Popularity", loc="left", color=TEXT)
ax.tick_params(colors=TEXT, labelsize=12)
plt.xticks(rotation=20, ha="right")
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(PLOTS, "eda_05_correlation_heatmap.png"), dpi=160)
plt.close()
print("ok: eda_05_correlation_heatmap.png")

# print correlations used in slide text
print(corr.round(2).to_string())
