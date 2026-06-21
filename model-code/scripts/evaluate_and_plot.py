"""
Evaluate the Big 5 models + generate 3 important plots for PPT support:
  1. Model performance comparison (Accuracy / Precision / Recall / F1)
  2. Confusion matrix of the best single model
  3. SHAP feature importance (global) on the best tree model

Outputs:
  model-code/docs/metrics_table.csv
  model-code/docs/plots/01_model_comparison.png
  model-code/docs/plots/02_confusion_matrix.png
  model-code/docs/plots/03_shap_feature_importance.png
"""
import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report,
)
import shap
import warnings
warnings.filterwarnings("ignore")

# ---------- paths ----------
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT, "data", "dataset.csv")
MODELS_PATH = os.path.join(ROOT, "models")
DOCS = os.path.join(ROOT, "docs")
PLOTS = os.path.join(DOCS, "plots")
os.makedirs(PLOTS, exist_ok=True)

# ---------- style (Spotify-ish dark for consistency w/ PPT) ----------
BG = "#0A0A0A"
PANEL = "#181818"
ACCENT = "#1DB954"
ACCENT2 = "#1ED760"
TEXT = "#FFFFFF"
MUTED = "#B3B3B3"

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": PANEL,
    "savefig.facecolor": BG, "axes.edgecolor": MUTED,
    "axes.labelcolor": TEXT, "xtick.color": MUTED, "ytick.color": MUTED,
    "text.color": TEXT, "font.size": 11, "axes.titlesize": 14,
    "axes.titleweight": "bold", "axes.grid": True, "grid.color": "#2A2A2A",
    "grid.linestyle": "--", "grid.linewidth": 0.6,
    "font.family": "DejaVu Sans",
})

FEATURES = ["tempo", "loudness", "key", "mode", "energy"]
THRESHOLD = 15

# ---------- load + preprocess (mirrors train_5_models.py) ----------
print("Loading & preprocessing dataset...")
df = pd.read_csv(DATA_PATH)
df = df.dropna(subset=FEATURES + ["popularity"])
df = df[df["energy"] > 0.1]
df["is_hit"] = (df["popularity"] >= THRESHOLD).astype(int)

df_h = df[df.is_hit == 1]
df_f = df[df.is_hit == 0]
n = min(len(df_h), len(df_f))
df_bal = (
    pd.concat([df_h.sample(n=n, random_state=42), df_f.sample(n=n, random_state=42)])
    .sample(frac=1, random_state=42)
    .reset_index(drop=True)
)
X = df_bal[FEATURES]
y = df_bal["is_hit"]
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Use the saved scaler so results match the pretrained .pkl models
scaler = joblib.load(os.path.join(MODELS_PATH, "feature_scaler.pkl"))
X_tr_s = scaler.transform(X_tr)
X_te_s = scaler.transform(X_te)

# ---------- load all 5 models ----------
MODEL_FILES = {
    "Decision Tree":  "decisiontree_model.pkl",
    "Random Forest":  "randomforest_model.pkl",
    "AdaBoost":       "adaboost_model.pkl",
    "KNN":            "knn_model.pkl",
    "XGBoost":        "xgboost_model.pkl",
}
models = {}
for name, fn in MODEL_FILES.items():
    p = os.path.join(MODELS_PATH, fn)
    if os.path.exists(p):
        models[name] = joblib.load(p)
        print(f"  loaded: {name}")

# ---------- compute metrics ----------
rows = []
preds_cache = {}
for name, m in models.items():
    yp = m.predict(X_te_s)
    preds_cache[name] = yp
    rows.append({
        "Model": name,
        "Accuracy":  accuracy_score(y_te, yp),
        "Precision": precision_score(y_te, yp),
        "Recall":    recall_score(y_te, yp),
        "F1":        f1_score(y_te, yp),
    })
metrics_df = pd.DataFrame(rows).sort_values("F1", ascending=False).reset_index(drop=True)
print("\n=== Metrics ===")
print(metrics_df.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
metrics_df.to_csv(os.path.join(DOCS, "metrics_table.csv"), index=False)

best_name = metrics_df.iloc[0]["Model"]
print(f"\nBest model: {best_name}")

# =============================================================
# PLOT 1 — Model performance comparison (grouped bar)
# =============================================================
fig, ax = plt.subplots(figsize=(11, 5.5))
metric_cols = ["Accuracy", "Precision", "Recall", "F1"]
colors = ["#1DB954", "#1ED760", "#7CDC8C", "#B0F0BD"]
m_sorted = metrics_df.sort_values("F1", ascending=True)
x = np.arange(len(m_sorted))
bar_w = 0.2
for i, (col, c) in enumerate(zip(metric_cols, colors)):
    bars = ax.barh(x + (i - 1.5) * bar_w, m_sorted[col], bar_w,
                   label=col, color=c, edgecolor=BG, linewidth=0.5)
    for b, v in zip(bars, m_sorted[col]):
        ax.text(v + 0.005, b.get_y() + b.get_height() / 2,
                f"{v:.3f}", va="center", fontsize=8, color=TEXT)

ax.set_yticks(x)
ax.set_yticklabels(m_sorted["Model"], fontweight="bold")
ax.set_xlim(0, 1.05)
ax.set_xlabel("Score")
ax.set_title("BIG 5 — Model Performance Comparison", color=TEXT, pad=14, loc="left")
ax.legend(loc="lower right", facecolor=PANEL, edgecolor=MUTED, labelcolor=TEXT)
ax.set_axisbelow(True)
ax.grid(axis="x")
ax.grid(axis="y", visible=False)
for spine in ax.spines.values():
    spine.set_color(MUTED)
plt.tight_layout()
out1 = os.path.join(PLOTS, "01_model_comparison.png")
plt.savefig(out1, dpi=160)
plt.close()
print(f"Saved: {out1}")

# =============================================================
# PLOT 2 — Confusion matrix (best model)
# =============================================================
yp_best = preds_cache[best_name]
cm = confusion_matrix(y_te, yp_best)
cm_pct = cm.astype(float) / cm.sum() * 100

fig, ax = plt.subplots(figsize=(7, 6))
sns.heatmap(
    cm, annot=False, fmt="d", cmap="Greens", cbar=False,
    linewidths=2, linecolor=BG, square=True, ax=ax,
    xticklabels=["FLOP", "HIT"], yticklabels=["FLOP", "HIT"],
)
# Custom annotations: count + percentage
for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        v = cm[i, j]; p = cm_pct[i, j]
        is_diag = (i == j)
        color = TEXT if (v > cm.max() * 0.4) else "#222222"
        ax.text(j + 0.5, i + 0.42, f"{v:,}", ha="center", va="center",
                fontsize=22, fontweight="bold", color=color)
        ax.text(j + 0.5, i + 0.68, f"{p:.1f}%", ha="center", va="center",
                fontsize=11, color=color)

ax.set_xlabel("Predicted", fontweight="bold")
ax.set_ylabel("Actual", fontweight="bold")
ax.set_title(f"Confusion Matrix — {best_name}", color=TEXT, pad=14, loc="left")
ax.tick_params(colors=TEXT, labelsize=12)
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontweight("bold")
plt.tight_layout()
out2 = os.path.join(PLOTS, "02_confusion_matrix.png")
plt.savefig(out2, dpi=160)
plt.close()
print(f"Saved: {out2}")

# =============================================================
# PLOT 3 — SHAP feature importance (global, best tree model)
# =============================================================
# Pick a tree-based model that SHAP TreeExplainer supports well.
preferred = ["Random Forest", "Decision Tree", "XGBoost"]
tree_name = next((n for n in preferred if n in models), best_name)
tree_model = models[tree_name]
print(f"Computing SHAP for: {tree_name}")

# subsample for speed
rng = np.random.default_rng(42)
idx = rng.choice(len(X_te_s), size=min(800, len(X_te_s)), replace=False)
X_sample = X_te_s[idx]

explainer = shap.TreeExplainer(tree_model)
shap_values = explainer.shap_values(X_sample)
# binary classifier may return list[2] (class 0, class 1) -> take Hit class
if isinstance(shap_values, list):
    shap_values = shap_values[1]
elif shap_values.ndim == 3:
    shap_values = shap_values[:, :, 1]

mean_abs = np.abs(shap_values).mean(axis=0)
order = np.argsort(mean_abs)
feat_sorted = [FEATURES[i] for i in order]
vals_sorted = mean_abs[order]

fig, ax = plt.subplots(figsize=(9.5, 5.5))
bar_colors = [ACCENT2 if i == len(vals_sorted) - 1 else ACCENT for i in range(len(vals_sorted))]
bars = ax.barh(feat_sorted, vals_sorted, color=bar_colors, edgecolor=BG)
for b, v in zip(bars, vals_sorted):
    ax.text(v + max(vals_sorted) * 0.01, b.get_y() + b.get_height() / 2,
            f"{v:.3f}", va="center", fontsize=11, fontweight="bold", color=TEXT)

ax.set_xlabel("Mean |SHAP value|  (impact on model output)", color=MUTED)
ax.set_title(f"SHAP Feature Importance — {tree_name}", color=TEXT, pad=14, loc="left")
ax.set_axisbelow(True)
ax.grid(axis="x")
ax.grid(axis="y", visible=False)
for spine in ax.spines.values():
    spine.set_color(MUTED)
plt.tight_layout()
out3 = os.path.join(PLOTS, "03_shap_feature_importance.png")
plt.savefig(out3, dpi=160)
plt.close()
print(f"Saved: {out3}")

# ---------- write classification report alongside ----------
with open(os.path.join(DOCS, "evaluation_report.txt"), "w", encoding="utf-8") as f:
    f.write("=" * 70 + "\n")
    f.write("BIG 5 — EVALUATION REPORT\n")
    f.write("=" * 70 + "\n\n")
    f.write(metrics_df.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    f.write("\n\n")
    for name, yp in preds_cache.items():
        f.write("-" * 70 + "\n")
        f.write(f"{name}\n")
        f.write("-" * 70 + "\n")
        f.write(classification_report(y_te, yp, target_names=["FLOP", "HIT"], digits=4))
        f.write("\n")

print("\nDone.")
