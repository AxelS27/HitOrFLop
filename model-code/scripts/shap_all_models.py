"""
Generate SHAP feature importance for ALL 5 models in one comparison grid.

Outputs:
  model-code/docs/plots/04_shap_all_models.png   (2x3 grid, mean |SHAP|)
  model-code/docs/plots/05_shap_beeswarm_rf.png  (detailed beeswarm for best model)
"""
import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import shap
import warnings
warnings.filterwarnings("ignore")

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "dataset.csv")
MODELS = os.path.join(ROOT, "models")
PLOTS = os.path.join(ROOT, "docs", "plots")
os.makedirs(PLOTS, exist_ok=True)

BG = "#0A0A0A"; PANEL = "#181818"; ACCENT = "#1DB954"; ACCENT2 = "#1ED760"
TEXT = "#FFFFFF"; MUTED = "#B3B3B3"
plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": PANEL, "savefig.facecolor": BG,
    "axes.edgecolor": MUTED, "axes.labelcolor": TEXT,
    "xtick.color": MUTED, "ytick.color": MUTED, "text.color": TEXT,
    "font.size": 10, "axes.titlesize": 13, "axes.titleweight": "bold",
    "axes.grid": True, "grid.color": "#2A2A2A", "grid.linestyle": "--", "grid.linewidth": 0.6,
})

FEATURES = ["tempo", "loudness", "key", "mode", "energy"]
THRESHOLD = 15

# ---------- preprocess (mirror training) ----------
print("Loading dataset...")
df = pd.read_csv(DATA).dropna(subset=FEATURES + ["popularity"])
df = df[df["energy"] > 0.1]
df["is_hit"] = (df["popularity"] >= THRESHOLD).astype(int)
df_h = df[df.is_hit == 1]; df_f = df[df.is_hit == 0]
n = min(len(df_h), len(df_f))
df_bal = pd.concat([df_h.sample(n=n, random_state=42), df_f.sample(n=n, random_state=42)])
df_bal = df_bal.sample(frac=1, random_state=42).reset_index(drop=True)
X = df_bal[FEATURES]; y = df_bal["is_hit"]
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

scaler = joblib.load(os.path.join(MODELS, "feature_scaler.pkl"))
X_tr_s = scaler.transform(X_tr)
X_te_s = scaler.transform(X_te)

# ---------- load 4 saved models ----------
rf  = joblib.load(os.path.join(MODELS, "randomforest_model.pkl"))
dt  = joblib.load(os.path.join(MODELS, "decisiontree_model.pkl"))
ab  = joblib.load(os.path.join(MODELS, "adaboost_model.pkl"))
knn = joblib.load(os.path.join(MODELS, "knn_model.pkl"))

# XGBoost: retrain fresh (workaround for pickle/version mismatch with SHAP)
print("Retraining XGBoost locally (for SHAP compatibility)...")
xgb = XGBClassifier(tree_method="hist", random_state=42, eval_metric="logloss")
xgb.fit(X_tr_s, y_tr)

# ---------- compute SHAP for each ----------
rng = np.random.default_rng(42)
idx = rng.choice(len(X_te_s), size=min(500, len(X_te_s)), replace=False)
X_sample = X_te_s[idx]

def shap_class1(values):
    """Normalize SHAP output to (n_samples, n_features) for the HIT class."""
    if isinstance(values, list):
        return np.array(values[1])
    arr = np.array(values)
    if arr.ndim == 3:
        return arr[:, :, 1]
    return arr

results = {}

print("SHAP: Random Forest...")
sv = shap.TreeExplainer(rf).shap_values(X_sample)
results["Random Forest"] = np.abs(shap_class1(sv)).mean(axis=0)

print("SHAP: Decision Tree...")
sv = shap.TreeExplainer(dt).shap_values(X_sample)
results["Decision Tree"] = np.abs(shap_class1(sv)).mean(axis=0)

print("SHAP: AdaBoost...")
try:
    sv = shap.TreeExplainer(ab).shap_values(X_sample)
    results["AdaBoost"] = np.abs(shap_class1(sv)).mean(axis=0)
except Exception as e:
    print(f"  TreeExplainer failed ({e}), falling back to KernelExplainer...")
    bg = shap.sample(X_tr_s, 50, random_state=42)
    expl = shap.KernelExplainer(ab.predict_proba, bg)
    sv = expl.shap_values(X_sample[:150], nsamples=100, silent=True)
    results["AdaBoost"] = np.abs(shap_class1(sv)).mean(axis=0)

print("SHAP: XGBoost...")
try:
    sv = shap.TreeExplainer(xgb).shap_values(X_sample)
    results["XGBoost"] = np.abs(shap_class1(sv)).mean(axis=0)
except Exception as e:
    print(f"  TreeExplainer failed ({e}), falling back to KernelExplainer...")
    bg = shap.sample(X_tr_s, 50, random_state=42)
    expl = shap.KernelExplainer(xgb.predict_proba, bg)
    sv = expl.shap_values(X_sample[:150], nsamples=100, silent=True)
    results["XGBoost"] = np.abs(shap_class1(sv)).mean(axis=0)

print("SHAP: KNN (KernelExplainer, may take ~1-2 min)...")
bg = shap.sample(X_tr_s, 50, random_state=42)
expl = shap.KernelExplainer(knn.predict_proba, bg)
sv = expl.shap_values(X_sample[:150], nsamples=100, silent=True)
results["KNN"] = np.abs(shap_class1(sv)).mean(axis=0)

# ---------- table summary ----------
summary = pd.DataFrame(results, index=FEATURES).T
print("\nMean |SHAP value| per feature:")
print(summary.round(4).to_string())
summary.to_csv(os.path.join(ROOT, "docs", "shap_importance_table.csv"))

# =============================================================
# PLOT 04 — SHAP bar grid (2x3, one panel per model)
# =============================================================
fig, axes = plt.subplots(2, 3, figsize=(15, 8))
fig.suptitle("SHAP Feature Importance  —  All 5 Models",
             fontsize=18, fontweight="bold", color=TEXT, y=0.98)

model_order = ["Random Forest", "XGBoost", "AdaBoost",
               "Decision Tree", "KNN"]

for i, ax in enumerate(axes.flat):
    if i >= len(model_order):
        ax.axis("off")
        continue
    name = model_order[i]
    vals = results[name]
    order = np.argsort(vals)
    feats = [FEATURES[j] for j in order]
    sorted_vals = vals[order]

    colors = [ACCENT2 if k == len(sorted_vals) - 1 else ACCENT for k in range(len(sorted_vals))]
    bars = ax.barh(feats, sorted_vals, color=colors, edgecolor=BG, linewidth=0.5)
    for b, v in zip(bars, sorted_vals):
        ax.text(v + max(sorted_vals) * 0.02, b.get_y() + b.get_height() / 2,
                f"{v:.3f}", va="center", fontsize=9, color=TEXT, fontweight="bold")

    ax.set_title(name, color=ACCENT, fontsize=13, loc="left", pad=8)
    ax.set_xlim(0, max(sorted_vals) * 1.25)
    ax.set_axisbelow(True)
    ax.grid(axis="x"); ax.grid(axis="y", visible=False)
    for sp in ax.spines.values():
        sp.set_color(MUTED)
    ax.tick_params(labelsize=10)

# subtitle below suptitle
fig.text(0.5, 0.935, "Top feature highlighted in lighter green  •  HIT class",
         ha="center", color=MUTED, fontsize=11, style="italic")

plt.tight_layout(rect=[0, 0, 1, 0.92])
out_a = os.path.join(PLOTS, "04_shap_all_models.png")
plt.savefig(out_a, dpi=160)
plt.close()
print(f"\nSaved: {out_a}")

# =============================================================
# PLOT 05 — SHAP beeswarm for Random Forest (best model)
# =============================================================
print("Generating SHAP beeswarm (Random Forest)...")
sv_rf = shap_class1(shap.TreeExplainer(rf).shap_values(X_sample))

# Use shap's summary_plot but capture & restyle
plt.figure(figsize=(10, 6))
shap.summary_plot(
    sv_rf, X_sample, feature_names=FEATURES,
    show=False, plot_size=(10, 6), color_bar=True, cmap="cool",
)
fig = plt.gcf()
ax = plt.gca()
fig.patch.set_facecolor(BG)
ax.set_facecolor(PANEL)
ax.set_title("SHAP Beeswarm — Random Forest  (Per-Sample Feature Impact on HIT class)",
             color=TEXT, fontsize=14, fontweight="bold", loc="left", pad=14)
ax.tick_params(colors=TEXT)
for sp in ax.spines.values():
    sp.set_color(MUTED)
ax.set_xlabel(ax.get_xlabel(), color=TEXT)
for label in ax.get_yticklabels() + ax.get_xticklabels():
    label.set_color(TEXT)
plt.tight_layout()
out_b = os.path.join(PLOTS, "05_shap_beeswarm_rf.png")
plt.savefig(out_b, dpi=160, facecolor=BG)
plt.close()
print(f"Saved: {out_b}")
print("\nDone.")
