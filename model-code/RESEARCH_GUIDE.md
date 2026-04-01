# 🧠 Music Predictor: Research Guide

A specialized machine learning infrastructure designed for emerging track recognition.

## 📊 Dataset Dynamics
- **Source**: Spotify Kaggle Track Dataset (110k+ entries).
- **Diversity**: Over 125 unique genres covered.
- **Balancing**: 50:50 Under-sampling technique applied.

## 🔬 Predictive Methodology

### 1. Acoustic DNA Threshold
Utilizing a **Popularity Threshold of 15** for emerging hit detection (optimized for indie/local tracks).

### 2. Multi-Vote Ensemble (Big 5)
Consensus from XGBoost, RandomForest, AdaBoost, KNN, and DecisionTree.

## 📂 Core Structure
- `scripts/`: Production training and testing.
- `models/`: Exported binary model artifacts.
- `MusicPredictor_Pipeline.ipynb`: Interactive data analysis notebook.

---
© 2026 AxelS27 | Research Guide
