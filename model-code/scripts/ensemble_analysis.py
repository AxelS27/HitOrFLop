"""
Analisis & visualisasi Multi-Vote Ensemble.

Mendukung 2 strategi:
  - HARD VOTING: majority dari prediksi label 5 model
  - SOFT VOTING: rata-rata probabilitas HIT dari 5 model

Memakai model TUNED kalau ada (model-code/models/tuned/), fallback ke models/.

Output (model-code/docs/plots/):
  ensemble_01_compare_individual_vs_vote.png
  ensemble_02_confusion_hard_vote.png
  ensemble_03_confusion_soft_vote.png
  ensemble_04_roc_curves.png
  ensemble_05_agreement_heatmap.png
  ensemble_06_vote_distribution.png
  ensemble_07_consensus_categories.png
"""
import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                             confusion_matrix, roc_curve, auc)
import warnings
warnings.filterwarnings("ignore")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT, "data", "dataset.csv")
TUNED = os.path.join(ROOT, "models", "tuned")
BASE = os.path.join(ROOT, "models")
PLOTS = os.path.join(ROOT, "docs", "plots")
os.makedirs(PLOTS, exist_ok=True)

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
THRESHOLD = 15
MODEL_FILES = {
    "Decision Tree":  "decisiontree_model.pkl",
    "Random Forest":  "randomforest_model.pkl",
    "AdaBoost":       "adaboost_model.pkl",
    "KNN":            "knn_model.pkl",
    "XGBoost":        "xgboost_model.pkl",
}

# Pick tuned if available, else baseline
src = TUNED if os.path.exists(os.path.join(TUNED, "feature_scaler.pkl")) else BASE
print(f"Using models from: {src}")
scaler = joblib.load(os.path.join(src, "feature_scaler.pkl"))

# Load data & rebuild same split
df = pd.read_csv(DATA_PATH).dropna(subset=FEATURES + ["popularity"])
df = df[df["energy"] > 0.1]
df["is_hit"] = (df["popularity"] >= THRESHOLD).astype(int)
h = df[df.is_hit == 1]; f = df[df.is_hit == 0]
n = min(len(h), len(f))
bal = pd.concat([h.sample(n=n, random_state=42), f.sample(n=n, random_state=42)]).sample(frac=1, random_state=42)
X = bal[FEATURES]; y = bal["is_hit"].values
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
X_te_s = scaler.transform(X_te)

models = {}
for name, fn in MODEL_FILES.items():
    p = os.path.join(src, fn)
    if os.path.exists(p):
        models[name] = joblib.load(p)
        print(f"  loaded: {name}")

# Predict per-model
preds = {}; probas = {}
for name, m in models.items():
    preds[name] = m.predict(X_te_s)
    try:
        probas[name] = m.predict_proba(X_te_s)[:, 1]
    except Exception:
        probas[name] = preds[name].astype(float)

# Hard vote (majority)
P = np.stack(list(preds.values()))           # (n_models, n_samples)
hard_votes = P.sum(axis=0)                   # 0..n_models
hard_pred = (hard_votes >= int(np.ceil(len(models)/2))).astype(int)

# Soft vote (mean proba threshold 0.5)
PR = np.stack(list(probas.values()))
soft_proba = PR.mean(axis=0)
soft_pred = (soft_proba >= 0.5).astype(int)

def _m(yp):
    return [accuracy_score(y_te, yp), precision_score(y_te, yp),
            recall_score(y_te, yp), f1_score(y_te, yp)]

rows = []
for name, yp in preds.items():
    rows.append([name, *_m(yp)])
rows.append(["HARD VOTE", *_m(hard_pred)])
rows.append(["SOFT VOTE", *_m(soft_pred)])
metrics_df = pd.DataFrame(rows, columns=["Model", "Accuracy", "Precision", "Recall", "F1"])
print("\n=== Metrics ===")
print(metrics_df.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
metrics_df.to_csv(os.path.join(ROOT, "docs", "ensemble_metrics.csv"), index=False)


# =========================================================
# 1) Individual vs Vote — grouped bars
# =========================================================
sorted_df = metrics_df.sort_values("F1").reset_index(drop=True)
fig, ax = plt.subplots(figsize=(12, 6))
metric_cols = ["Accuracy", "Precision", "Recall", "F1"]
cols = ["#1DB954", "#1ED760", "#7CDC8C", "#B0F0BD"]
xi = np.arange(len(sorted_df)); w = 0.2
for i, (c, col) in enumerate(zip(metric_cols, cols)):
    bars = ax.barh(xi + (i-1.5)*w, sorted_df[c], w, color=col, edgecolor=BG, label=c)
    for b, v in zip(bars, sorted_df[c]):
        ax.text(v+0.005, b.get_y()+b.get_height()/2, f"{v:.3f}",
                va="center", fontsize=8, color=TEXT)
labels = []
for n_ in sorted_df["Model"]:
    if n_ in ("HARD VOTE", "SOFT VOTE"):
        labels.append(f"★ {n_}")
    else:
        labels.append(n_)
ax.set_yticks(xi); ax.set_yticklabels(labels, fontweight="bold")
ax.set_xlim(0, 1.05); ax.set_xlabel("Score")
ax.set_title("Individual Models vs Voting Ensemble", loc="left")
ax.legend(loc="lower right", facecolor=PANEL, edgecolor=MUTED, labelcolor=TEXT)
ax.grid(axis="y", visible=False)
plt.tight_layout()
plt.savefig(os.path.join(PLOTS, "ensemble_01_compare_individual_vs_vote.png"), dpi=160)
plt.close()
print("saved: ensemble_01_compare_individual_vs_vote.png")


# =========================================================
# 2) & 3) Confusion matrices for HARD and SOFT vote
# =========================================================
def plot_cm(yp, title, fname):
    cm = confusion_matrix(y_te, yp)
    cm_pct = cm.astype(float) / cm.sum() * 100
    fig, ax = plt.subplots(figsize=(7, 6))
    sns.heatmap(cm, annot=False, cmap="Greens", cbar=False,
                linewidths=2, linecolor=BG, square=True, ax=ax,
                xticklabels=["FLOP", "HIT"], yticklabels=["FLOP", "HIT"])
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            v = cm[i, j]; p = cm_pct[i, j]
            color = TEXT if v > cm.max() * 0.4 else "#222"
            ax.text(j+0.5, i+0.42, f"{v:,}", ha="center", va="center",
                    fontsize=22, fontweight="bold", color=color)
            ax.text(j+0.5, i+0.68, f"{p:.1f}%", ha="center", va="center",
                    fontsize=11, color=color)
    ax.set_xlabel("Predicted", fontweight="bold")
    ax.set_ylabel("Actual",    fontweight="bold")
    ax.set_title(title, loc="left", color=TEXT)
    for lbl in ax.get_xticklabels() + ax.get_yticklabels():
        lbl.set_fontweight("bold")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS, fname), dpi=160)
    plt.close()
    print(f"saved: {fname}")

plot_cm(hard_pred, "Confusion Matrix — Hard Voting Ensemble", "ensemble_02_confusion_hard_vote.png")
plot_cm(soft_pred, "Confusion Matrix — Soft Voting Ensemble", "ensemble_03_confusion_soft_vote.png")


# =========================================================
# 4) ROC curves — all models + soft vote
# =========================================================
fig, ax = plt.subplots(figsize=(8, 7))
palette = ["#1DB954", "#1ED760", "#FFD400", "#E0245E", "#5AC8FA", "#FFFFFF"]
items = list(probas.items()) + [("SOFT VOTE", soft_proba)]
for (name, pr), c in zip(items, palette):
    fpr, tpr, _ = roc_curve(y_te, pr)
    a = auc(fpr, tpr)
    lw = 3 if name == "SOFT VOTE" else 1.6
    ax.plot(fpr, tpr, color=c, lw=lw, label=f"{name} (AUC={a:.3f})")
ax.plot([0, 1], [0, 1], "--", color=MUTED, lw=1)
ax.set_xlabel("False Positive Rate")
ax.set_ylabel("True Positive Rate")
ax.set_title("ROC Curves — Individual Models vs Soft Vote", loc="left")
ax.legend(loc="lower right", facecolor=PANEL, edgecolor=MUTED, labelcolor=TEXT, fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(PLOTS, "ensemble_04_roc_curves.png"), dpi=160)
plt.close()
print("saved: ensemble_04_roc_curves.png")


# =========================================================
# 5) Agreement heatmap (pairwise % same prediction)
# =========================================================
names = list(preds.keys())
M = len(names)
agree = np.zeros((M, M))
for i in range(M):
    for j in range(M):
        agree[i, j] = (preds[names[i]] == preds[names[j]]).mean() * 100

fig, ax = plt.subplots(figsize=(7.5, 6.5))
sns.heatmap(agree, annot=True, fmt=".1f", cmap="Greens", vmin=50, vmax=100,
            xticklabels=names, yticklabels=names, linewidths=1, linecolor=BG,
            cbar_kws={"shrink": .8}, ax=ax, annot_kws={"color": "#111", "fontweight": "bold"})
ax.set_title("Model Agreement Heatmap (% predictions identik)", loc="left")
plt.xticks(rotation=20, ha="right")
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(PLOTS, "ensemble_05_agreement_heatmap.png"), dpi=160)
plt.close()
print("saved: ensemble_05_agreement_heatmap.png")


# =========================================================
# 6) Vote distribution histogram (#models voting HIT)
# =========================================================
fig, ax = plt.subplots(figsize=(9, 5.5))
vals, cnts = np.unique(hard_votes, return_counts=True)
bars = ax.bar(vals, cnts, color=[FLOP_C if v < np.ceil(M/2) else HIT_C for v in vals],
              edgecolor=BG, linewidth=2)
for b, v in zip(bars, cnts):
    ax.text(b.get_x()+b.get_width()/2, v, f"{v:,}",
            ha="center", va="bottom", fontweight="bold", color=TEXT)
ax.set_xlabel("Jumlah model yang vote HIT")
ax.set_ylabel("Jumlah lagu (test set)")
ax.set_title("Distribusi Voting — Berapa Model Sepakat HIT?", loc="left")
ax.set_xticks(range(M+1))
plt.tight_layout()
plt.savefig(os.path.join(PLOTS, "ensemble_06_vote_distribution.png"), dpi=160)
plt.close()
print("saved: ensemble_06_vote_distribution.png")


# =========================================================
# 7) Consensus categories pie/bar (ULTRA HIT / POTENTIAL / RISKY / FLOP)
# =========================================================
def cat(v):
    if v == M: return "ULTRA HIT"
    if v >= int(np.ceil(M/2)+1): return "POTENTIAL HIT"
    if v >= 1: return "RISKY"
    return "TOTAL FLOP"

categories = pd.Series([cat(v) for v in hard_votes]).value_counts()
order = ["ULTRA HIT", "POTENTIAL HIT", "RISKY", "TOTAL FLOP"]
categories = categories.reindex([c for c in order if c in categories.index])
colors_map = {"ULTRA HIT": "#FFD400", "POTENTIAL HIT": HIT_C, "RISKY": "#FF8C42", "TOTAL FLOP": FLOP_C}

fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))
# bar
axes[0].bar(categories.index, categories.values,
            color=[colors_map[c] for c in categories.index], edgecolor=BG, linewidth=2)
for i, v in enumerate(categories.values):
    axes[0].text(i, v, f"{v:,}\n({v/len(hard_votes)*100:.1f}%)",
                 ha="center", va="bottom", fontweight="bold", color=TEXT)
axes[0].set_title("Konsensus Voting per Kategori", loc="left")
axes[0].set_ylabel("Jumlah lagu")
axes[0].set_ylim(0, max(categories.values) * 1.18)

# pie
axes[1].pie(categories.values, labels=categories.index,
            colors=[colors_map[c] for c in categories.index],
            autopct="%1.1f%%", startangle=90,
            wedgeprops=dict(edgecolor=BG, linewidth=2),
            textprops=dict(color=TEXT, fontweight="bold"))
axes[1].set_title("Proporsi Konsensus", loc="left")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS, "ensemble_07_consensus_categories.png"), dpi=160)
plt.close()
print("saved: ensemble_07_consensus_categories.png")

print("\nDone.")
