"""
Hyperparameter tuning untuk Big 5 models (RandomizedSearchCV).
Menyimpan model ter-tune ke models/tuned/ DAN menulis hasil tuning ke docs/.

Output:
  model-code/models/tuned/{model}_model.pkl
  model-code/models/tuned/feature_scaler.pkl
  model-code/docs/tuning_results.csv
  model-code/docs/plots/tuning_01_before_after.png
  model-code/docs/plots/tuning_02_best_params.png
"""
import os
import json
import time
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, RandomizedSearchCV, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from xgboost import XGBClassifier
import warnings
warnings.filterwarnings("ignore")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT, "data", "dataset.csv")
MODELS_DIR = os.path.join(ROOT, "models")
TUNED_DIR = os.path.join(MODELS_DIR, "tuned")
DOCS = os.path.join(ROOT, "docs")
PLOTS = os.path.join(DOCS, "plots")
os.makedirs(TUNED_DIR, exist_ok=True)
os.makedirs(PLOTS, exist_ok=True)

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

FEATURES = ["tempo", "loudness", "key", "mode", "energy"]
THRESHOLD = 15

print("Loading & preprocessing...")
df = pd.read_csv(DATA_PATH).dropna(subset=FEATURES + ["popularity"])
df = df[df["energy"] > 0.1]
df["is_hit"] = (df["popularity"] >= THRESHOLD).astype(int)
h = df[df.is_hit == 1]; f = df[df.is_hit == 0]
n = min(len(h), len(f))
bal = pd.concat([h.sample(n=n, random_state=42), f.sample(n=n, random_state=42)]).sample(frac=1, random_state=42)
X = bal[FEATURES]; y = bal["is_hit"]
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

scaler = StandardScaler()
X_tr_s = scaler.fit_transform(X_tr)
X_te_s = scaler.transform(X_te)
joblib.dump(scaler, os.path.join(TUNED_DIR, "feature_scaler.pkl"))

# Baseline models (default hyperparams) for "before" comparison
baseline = {
    "RandomForest":  RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
    "AdaBoost":      AdaBoostClassifier(n_estimators=100, random_state=42),
    "KNN":           KNeighborsClassifier(n_neighbors=5, n_jobs=-1),
    "DecisionTree":  DecisionTreeClassifier(max_depth=10, random_state=42),
    "XGBoost":       XGBClassifier(tree_method="hist", random_state=42,
                                   use_label_encoder=False, eval_metric="logloss"),
}

# Search spaces
search_spaces = {
    "RandomForest": (
        RandomForestClassifier(random_state=42, n_jobs=-1),
        {
            "n_estimators":      [100, 200, 300, 500],
            "max_depth":         [None, 8, 12, 16, 24],
            "min_samples_split": [2, 5, 10],
            "min_samples_leaf":  [1, 2, 4],
            "max_features":      ["sqrt", "log2", None],
        }, 25,
    ),
    "AdaBoost": (
        AdaBoostClassifier(random_state=42),
        {
            "n_estimators":  [50, 100, 200, 300, 500],
            "learning_rate": [0.01, 0.05, 0.1, 0.3, 0.5, 1.0],
        }, 20,
    ),
    "KNN": (
        KNeighborsClassifier(n_jobs=-1),
        {
            "n_neighbors": [3, 5, 7, 11, 15, 21, 31],
            "weights":     ["uniform", "distance"],
            "p":           [1, 2],
        }, 20,
    ),
    "DecisionTree": (
        DecisionTreeClassifier(random_state=42),
        {
            "max_depth":         [None, 5, 8, 12, 16, 24],
            "min_samples_split": [2, 5, 10, 20],
            "min_samples_leaf":  [1, 2, 4, 8],
            "criterion":         ["gini", "entropy"],
        }, 25,
    ),
    "XGBoost": (
        XGBClassifier(tree_method="hist", random_state=42,
                      use_label_encoder=False, eval_metric="logloss"),
        {
            "n_estimators":     [200, 400, 600, 800],
            "max_depth":        [3, 5, 7, 9, 12],
            "learning_rate":    [0.01, 0.05, 0.1, 0.2],
            "subsample":        [0.7, 0.85, 1.0],
            "colsample_bytree": [0.7, 0.85, 1.0],
            "reg_lambda":       [0.5, 1.0, 2.0, 5.0],
        }, 30,
    ),
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# Compute baseline metrics
def metrics(yp):
    return {
        "Accuracy":  accuracy_score(y_te, yp),
        "Precision": precision_score(y_te, yp),
        "Recall":    recall_score(y_te, yp),
        "F1":        f1_score(y_te, yp),
    }

rows = []
for name, model in baseline.items():
    print(f"  baseline: {name}")
    model.fit(X_tr_s, y_tr)
    m = metrics(model.predict(X_te_s))
    rows.append({"Model": name, "Stage": "Default", **m, "BestParams": "default"})

# Tuning loop
for name, (est, space, n_iter) in search_spaces.items():
    print(f"\n>>> Tuning {name}  (n_iter={n_iter}, cv=5)")
    t0 = time.time()
    rs = RandomizedSearchCV(
        est, space, n_iter=n_iter, cv=cv, scoring="f1",
        n_jobs=-1, random_state=42, verbose=1, refit=True,
    )
    rs.fit(X_tr_s, y_tr)
    dt = time.time() - t0
    print(f"  best CV-F1: {rs.best_score_:.4f}  | took {dt:.1f}s")
    print(f"  best params: {rs.best_params_}")

    best = rs.best_estimator_
    m = metrics(best.predict(X_te_s))
    rows.append({"Model": name, "Stage": "Tuned", **m,
                 "BestParams": json.dumps(rs.best_params_), "CV_F1": rs.best_score_,
                 "TuneTimeSec": round(dt, 1)})
    joblib.dump(best, os.path.join(TUNED_DIR, f"{name.lower()}_model.pkl"))

res = pd.DataFrame(rows)
res.to_csv(os.path.join(DOCS, "tuning_results.csv"), index=False)
print("\n=== Tuning Results ===")
print(res.to_string(index=False))

# =========================================================
# Plot 1 — Before vs After (F1 score)
# =========================================================
pivot = res.pivot_table(index="Model", columns="Stage", values="F1")
pivot = pivot[["Default", "Tuned"]]
fig, ax = plt.subplots(figsize=(11, 5.5))
x = np.arange(len(pivot)); w = 0.38
b1 = ax.bar(x - w/2, pivot["Default"], w, color="#888888", label="Default", edgecolor=BG)
b2 = ax.bar(x + w/2, pivot["Tuned"],   w, color=ACCENT,    label="Tuned",   edgecolor=BG)
for bars in (b1, b2):
    for b in bars:
        v = b.get_height()
        ax.text(b.get_x()+b.get_width()/2, v+0.005, f"{v:.3f}",
                ha="center", fontsize=10, fontweight="bold", color=TEXT)
ax.set_xticks(x); ax.set_xticklabels(pivot.index, fontweight="bold")
ax.set_ylim(0, min(1.0, pivot.values.max()*1.15))
ax.set_ylabel("F1 Score")
ax.set_title("Hyperparameter Tuning — Default vs Tuned (F1)", loc="left")
ax.legend(facecolor=PANEL, edgecolor=MUTED, labelcolor=TEXT)
plt.tight_layout()
plt.savefig(os.path.join(PLOTS, "tuning_01_before_after.png"), dpi=160)
plt.close()
print(f"saved: tuning_01_before_after.png")

# =========================================================
# Plot 2 — Improvement delta table-style visual
# =========================================================
deltas = (pivot["Tuned"] - pivot["Default"]).sort_values()
fig, ax = plt.subplots(figsize=(10, 5))
colors = [ACCENT2 if v >= 0 else "#E0245E" for v in deltas.values]
bars = ax.barh(deltas.index, deltas.values * 100, color=colors, edgecolor=BG)
for b, v in zip(bars, deltas.values * 100):
    ax.text(v + (0.05 if v >= 0 else -0.05), b.get_y()+b.get_height()/2,
            f"{v:+.2f} pp", va="center",
            ha="left" if v >= 0 else "right",
            fontweight="bold", color=TEXT, fontsize=11)
ax.axvline(0, color=MUTED, linewidth=1)
ax.set_xlabel("Δ F1 (percentage points)")
ax.set_title("F1 Improvement after Tuning", loc="left")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS, "tuning_02_improvement.png"), dpi=160)
plt.close()
print(f"saved: tuning_02_improvement.png")

print("\nDone. Tuned models saved to:", TUNED_DIR)
