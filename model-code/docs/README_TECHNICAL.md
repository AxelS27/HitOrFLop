# 🎵 Music Hit or Flop Predictor (Production & Inference Guide)

This guide focuses on **deploying and using** the pre-trained "Big 5" ensemble models. It is designed for easy integration with web backends and interacts seamlessly with AI coding assistants.

---

## 🛠️ Production Stack
- **Core:** Python 3.8+
- **Audio Processing:** `librosa`, `pyloudnorm`, `yt-dlp`
- **Model Inference:** `scikit-learn`, `xgboost`, `joblib`
- **Output:** JSON-based Consensus Voting Report

---

## 📂 Inference Structure
- **`models/`**: (CRITICAL) Contains pre-trained `.pkl` model files (RandomForest, AdaBoost, KNN, DecisionTree, XGBoost) and `feature_scaler.pkl`.
- **`src/librosa_extractor.py`**: Audio signal processing andLUFS normalization module.
- **`src/predictor_api.py`**: Main API Bridge to load models and run consensus predictions.

---

## 🔗 How to Connect to Backend (API Integration)

Use the `MusicHitPredictorAPI` class for a single interface to all models.

### **Quick Start Code (Python):**
```python
from src.predictor_api import MusicHitPredictorAPI
from src.librosa_extractor import extract_features_from_audio

# 1. Initialize (The predictor loads all 5 models and the scaler automatically)
predictor = MusicHitPredictorAPI(models_dir='models', scaler_path='models/feature_scaler.pkl')

# 2. Extract Features from an audio file (.mp3 / .wav)
audio_features = extract_features_from_audio("your_song_path.mp3")

# 3. Request Final Consensus Result
prediction_report = predictor.predict(audio_features, model_mode='VOTING')

# Accessing the results:
print(f"Consensus: {prediction_report['consensus']}")
print(f"Hit Ratio: {prediction_report['hit_ratio']}")
```

---

## 📊 Feature Definitions (System Logic)

The following 5 features are automatically extracted and passed to the models:
- **`tempo`**: Detected Beats Per Minute (BPM).
- **`loudness`**: Input audio normalized to -14.0 LUFS.
- **`key`**: Pitch class (0-11) as an integer.
- **`mode`**: Music modality (0 for Minor, 1 for Major).
- **`energy`**: A composite RMS-based intensity value (0.0 - 1.0).

---

## 🧪 Quick Test Tool

Run the following script to test all audio files in the `testing_songs/` folder and generate a textual summary:
```bash
python scripts/test_5_models.py
```
*Results will be updated in `docs/multi_model_test_results.txt`.*

---

## 💡 AI Prompt Reference for Backend Developers
If you are asking an AI to build a service:
- "Create a **FastAPI** POST endpoint that accepts an MP3 file, uses `MusicHitPredictorAPI` to run a **VOTING** prediction, and returns the full JSON response."
- "Write a script to fetch a YouTube URL using `yt-dlp`, extract its features, and print the consensus hit/flop prediction."

---

## 👥 Contributors
- Farrell Axel Suwandi, Fidel Cristopher, Matthew Shallom Mcdccissa Siliton, Michael James Eijah.
