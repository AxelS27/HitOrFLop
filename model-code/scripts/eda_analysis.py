"""
EDA — Exploratory Data Analysis untuk Music Hit Predictor.
Menghasilkan banyak plot untuk dipakai di slide presentasi.

Output (model-code/docs/plots/):
  eda_01_class_distribution.png       — distribusi HIT vs FLOP
  eda_02_popularity_hist.png          — histogram popularity + threshold line
  eda_03_feature_distributions.png    — distribusi tiap fitur (KDE per kelas)
  eda_04_boxplots_by_class.png        — boxplot fitur per kelas
  eda_05_correlation_heatmap.png      — korelasi antar fitur audio
  eda_06_pairplot_features.png        — pairplot fitur utama per kelas
  eda_07_top_genres.png               — top genre paling banyak
  eda_08_hit_rate_by_genre.png        — hit-rate per genre (top 20)
  eda_09_tempo_vs_energy.png          — scatter tempo vs energy, di-color HIT/FLOP
  eda_10_duration_explicit.png        — distribusi durasi + explicit ratio
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT, "data", "dataset.csv")
PLOTS = os.path.join(ROOT, "docs", "plots")
os.makedirs(PLOTS, exist_ok=True)

# Spotify-ish dark palette
BG = "#0A0A0A"; PANEL = "#181818"; ACCENT = "#1DB954"; ACCENT2 = "#1ED760"
HIT_C = "#1DB954"; FLOP_C = "#E0245E"
TEXT = "#FFFFFF"; MUTED = "#B3B3B3"

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": PANEL,
    "savefig.facecolor": BG, "axes.edgecolor": MUTED,
    "axes.labelcolor": TEXT, "xtick.color": MUTED, "ytick.color": MUTED,
    "text.color": TEXT, "font.size": 11, "axes.titlesize": 14,
    "axes.titleweight": "bold", "axes.grid": True, "grid.color": "#2A2A2A",
    "grid.linestyle": "--", "grid.linewidth": 0.6, "font.family": "DejaVu Sans",
})

FEATURES = ["tempo", "loudness", "key", "mode", "energy"]
EXTRA = ["danceability", "valence", "acousticness", "instrumentalness",
         "speechiness", "liveness", "duration_ms"]
THRESHOLD = 15

print("Loading dataset...")
df = pd.read_csv(DATA_PATH)
df = df.dropna(subset=FEATURES + ["popularity"])
df = df[df["energy"] > 0.1]
df["is_hit"] = (df["popularity"] >= THRESHOLD).astype(int)
df["label"] = df["is_hit"].map({1: "HIT", 0: "FLOP"})
print(f"  rows: {len(df):,}  | hits: {df.is_hit.sum():,}  | flops: {(1-df.is_hit).sum():,}")


def _save(fig, name):
    out = os.path.join(PLOTS, name)
    fig.tight_layout()
    fig.savefig(out, dpi=160)
    plt.close(fig)
    print(f"  saved: {name}")


# =========================================================
# 1. Class Distribution
# =========================================================
fig, ax = plt.subplots(figsize=(7, 5))
counts = df["label"].value_counts()
bars = ax.bar(counts.index, counts.values, color=[HIT_C if i == "HIT" else FLOP_C for i in counts.index],
              edgecolor=BG, linewidth=2)
for b, v in zip(bars, counts.values):
    ax.text(b.get_x() + b.get_width()/2, v, f"{v:,}\n({v/len(df)*100:.1f}%)",
            ha="center", va="bottom", fontweight="bold", fontsize=12, color=TEXT)
ax.set_title(f"Class Distribution (Threshold popularity ≥ {THRESHOLD})", loc="left")
ax.set_ylabel("Jumlah Lagu")
ax.set_ylim(0, max(counts.values) * 1.15)
_save(fig, "eda_01_class_distribution.png")


# =========================================================
# 2. Popularity histogram + threshold line
# =========================================================
fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(df["popularity"], bins=60, color=ACCENT, edgecolor=BG, alpha=0.9)
ax.axvline(THRESHOLD, color="#FFD400", linestyle="--", linewidth=2.5, label=f"Threshold = {THRESHOLD}")
ax.set_title("Distribusi Popularity Score Spotify", loc="left")
ax.set_xlabel("Popularity (0–100)"); ax.set_ylabel("Jumlah Lagu")
ax.legend(facecolor=PANEL, edgecolor=MUTED, labelcolor=TEXT)
_save(fig, "eda_02_popularity_hist.png")


# =========================================================
# 3. Feature distributions (KDE per class)
# =========================================================
plot_feats = ["tempo", "loudness", "energy", "danceability", "valence", "acousticness"]
fig, axes = plt.subplots(2, 3, figsize=(15, 8))
for ax, feat in zip(axes.flat, plot_feats):
    if feat not in df.columns: continue
    for cls, color in [("FLOP", FLOP_C), ("HIT", HIT_C)]:
        sub = df[df["label"] == cls][feat].dropna()
        ax.hist(sub, bins=40, alpha=0.55, color=color, label=cls, density=True, edgecolor=BG)
    ax.set_title(feat, color=TEXT, loc="left")
    ax.legend(facecolor=PANEL, edgecolor=MUTED, labelcolor=TEXT, fontsize=9)
fig.suptitle("Distribusi Fitur Audio per Kelas (HIT vs FLOP)", color=TEXT,
             fontweight="bold", fontsize=15, x=0.02, ha="left")
_save(fig, "eda_03_feature_distributions.png")


# =========================================================
# 4. Boxplots per class
# =========================================================
box_feats = ["tempo", "loudness", "energy", "danceability", "valence"]
fig, axes = plt.subplots(1, len(box_feats), figsize=(16, 5))
for ax, feat in zip(axes, box_feats):
    data = [df[df.is_hit == 0][feat].dropna(), df[df.is_hit == 1][feat].dropna()]
    bp = ax.boxplot(data, patch_artist=True, labels=["FLOP", "HIT"], widths=0.55,
                    medianprops=dict(color="#FFD400", linewidth=2))
    for patch, c in zip(bp["boxes"], [FLOP_C, HIT_C]):
        patch.set_facecolor(c); patch.set_edgecolor(BG); patch.set_alpha(0.85)
    ax.set_title(feat, loc="left")
fig.suptitle("Boxplot Fitur Audio — HIT vs FLOP", color=TEXT,
             fontweight="bold", fontsize=15, x=0.02, ha="left")
_save(fig, "eda_04_boxplots_by_class.png")


# =========================================================
# 5. Correlation heatmap
# =========================================================
corr_cols = [c for c in (FEATURES + EXTRA + ["popularity"]) if c in df.columns]
corr = df[corr_cols].corr()
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdYlGn", center=0,
            linewidths=1, linecolor=BG, ax=ax,
            cbar_kws={"shrink": .8}, annot_kws={"size": 9, "color": "#111"})
ax.set_title("Korelasi Antar Fitur Audio", loc="left", color=TEXT)
ax.tick_params(colors=TEXT)
_save(fig, "eda_05_correlation_heatmap.png")


# =========================================================
# 6. Pairplot of 4 key features (sampled, lightweight)
# =========================================================
sample_df = df.sample(n=min(3000, len(df)), random_state=42)
pair_feats = ["tempo", "loudness", "energy", "danceability"]
g = sns.pairplot(sample_df[pair_feats + ["label"]], hue="label",
                 palette={"HIT": HIT_C, "FLOP": FLOP_C},
                 plot_kws=dict(alpha=0.4, s=12, edgecolor="none"),
                 diag_kind="kde", height=2.2)
g.fig.suptitle("Pairplot Fitur Utama (3K sample)", y=1.02, color=TEXT, fontweight="bold")
for ax in g.axes.flat:
    if ax is None: continue
    ax.set_facecolor(PANEL)
    ax.tick_params(colors=MUTED, labelsize=8)
    for s in ax.spines.values(): s.set_color(MUTED)
    ax.title.set_color(TEXT); ax.xaxis.label.set_color(TEXT); ax.yaxis.label.set_color(TEXT)
g.fig.patch.set_facecolor(BG)
out = os.path.join(PLOTS, "eda_06_pairplot_features.png")
g.fig.savefig(out, dpi=140, facecolor=BG, bbox_inches="tight")
plt.close(g.fig)
print(f"  saved: eda_06_pairplot_features.png")


# =========================================================
# 7. Top genres
# =========================================================
if "track_genre" in df.columns:
    top = df["track_genre"].value_counts().head(20)
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.barh(top.index[::-1], top.values[::-1], color=ACCENT, edgecolor=BG)
    ax.set_title("Top 20 Genre (jumlah lagu)", loc="left")
    ax.set_xlabel("Jumlah Lagu")
    _save(fig, "eda_07_top_genres.png")

    # 8. Hit rate per genre
    hit_rate = df.groupby("track_genre")["is_hit"].agg(["mean", "count"])
    hit_rate = hit_rate[hit_rate["count"] >= 200].sort_values("mean", ascending=False).head(20)
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.barh(hit_rate.index[::-1], (hit_rate["mean"] * 100)[::-1],
            color=ACCENT2, edgecolor=BG)
    for i, (g_, row) in enumerate(hit_rate[::-1].iterrows()):
        ax.text(row["mean"]*100 + 0.5, i, f"{row['mean']*100:.1f}% (n={int(row['count'])})",
                va="center", fontsize=9, color=TEXT)
    ax.set_title("Top 20 Hit-Rate per Genre (min 200 lagu)", loc="left")
    ax.set_xlabel("% Hit")
    _save(fig, "eda_08_hit_rate_by_genre.png")


# =========================================================
# 9. Scatter tempo vs energy
# =========================================================
fig, ax = plt.subplots(figsize=(10, 6))
samp = df.sample(n=min(5000, len(df)), random_state=42)
for cls, c in [("FLOP", FLOP_C), ("HIT", HIT_C)]:
    sub = samp[samp.label == cls]
    ax.scatter(sub["tempo"], sub["energy"], s=10, alpha=0.45, c=c, label=cls, edgecolor="none")
ax.set_xlabel("Tempo (BPM)"); ax.set_ylabel("Energy")
ax.set_title("Tempo vs Energy — HIT vs FLOP (5K sample)", loc="left")
ax.legend(facecolor=PANEL, edgecolor=MUTED, labelcolor=TEXT)
_save(fig, "eda_09_tempo_vs_energy.png")


# =========================================================
# 10. Duration & explicit
# =========================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
if "duration_ms" in df.columns:
    dur_min = df["duration_ms"] / 60000
    axes[0].hist(dur_min[dur_min < 10], bins=60, color=ACCENT, edgecolor=BG, alpha=0.9)
    axes[0].set_xlabel("Durasi (menit)"); axes[0].set_ylabel("Jumlah Lagu")
    axes[0].set_title("Distribusi Durasi Lagu", loc="left")

if "explicit" in df.columns:
    expl = df.groupby("explicit")["is_hit"].mean() * 100
    bars = axes[1].bar(expl.index.astype(str), expl.values,
                       color=[FLOP_C, HIT_C], edgecolor=BG, linewidth=2)
    for b, v in zip(bars, expl.values):
        axes[1].text(b.get_x()+b.get_width()/2, v, f"{v:.1f}%",
                     ha="center", va="bottom", fontweight="bold", color=TEXT)
    axes[1].set_title("Hit-Rate: Explicit vs Non-Explicit", loc="left")
    axes[1].set_ylabel("% Hit")
    axes[1].set_xlabel("Explicit")
_save(fig, "eda_10_duration_explicit.png")

print("\nDone. All EDA plots saved.")
