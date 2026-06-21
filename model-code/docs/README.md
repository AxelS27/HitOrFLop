# 🎵 Music Hit or Flop Predictor

A robust, ensemble-based machine learning pipeline designed to predict song success ("Hit" or "Flop") based on audio features. This system utilizes a **Consensus Voting Logic** from five optimized models ("The Big 5") and supports features like LUFS normalization and multi-source inputs.

---

## 📂 Project Structure
```text
├── data/               # Project Dataset (dataset.csv)
├── docs/               # Documentation & Test Results (README.md, TXT results)
├── models/             # Pre-trained .pkl models & Feature Scaler
├── scripts/            # Training & Batch Testing scripts
│   ├── train_5_models.py
│   └── test_5_models.py
├── src/                # Core Logic Modules
│   ├── librosa_extractor.py
│   └── predictor_api.py
├── testing_songs/      # Personal .mp3 and .wav files for testing
└── PROJECT_BACKUP/     # Secure copy of the original workspace
```

---

## 🚀 Key Features
- **The Big 5 Models:** Ensemble voting using RandomForest, AdaBoost, KNN, DecisionTree, and XGBoost (GPU Accelerated).
- **Consensus Logic:** Final results ranging from "Ultra Hit" to "Total Flop" based on majority model agreement.
- **Loudness Normalization:** Automatically standardizes audio to **-14.0 LUFS** (Spotify Target).
- **Flexible Input:** Supports local **.mp3**, **.wav**, and **YouTube Links** for real-world analysis.

---

## 🛠️ Getting Started

### 1. Installation
Install all required dependencies:
```bash
pip install librosa numpy pandas scikit-learn xgboost joblib pyloudnorm yt-dlp
```

### 2. How to Run (From Root Directory)

#### **A. Training the Ensemble:**
To retrain the models using `data/dataset.csv`:
```bash
python scripts/train_5_models.py
```

#### **B. Batch Testing Songs:**
To analyze all songs inside `testing_songs/`:
```bash
python scripts/test_5_models.py
```
*Individual model predictions and the final consensus verdict will be generated.*

---

## 📊 Methodology (The Core Logic)
1. **Audio Extraction:** Normalized to -14.0 LUFS for consistent input scale.
2. **Feature Mapping:** Converting audio signals into Tempo, Loudness, Key, Mode, and Energy.
3. **Voting System:** 
   - **5/5 Agreement:** ULTRA HIT 🌋
   - **3-4/5 Agreement:** POTENTIAL HIT 📈
   - **1-2/5 Agreement:** RISKY / MIXED ⚖️
   - **0/5 Agreement:** TOTAL FLOP 🧊

---

## 📚 Dataset Reference
This project uses the **"Spotify Tracks Dataset"** by Maharshi Pandya (Kaggle).
[Dataset Link](https://www.kaggle.com/datasets/maharshipandya/spotify-tracks-dataset)

---

## 👥 Contributors
- Farrell Axel Suwandi
- Fidel Cristopher
- Matthew Shallom Mcdccissa Siliton
- Michael James Eijah
