import os
import joblib
import pandas as pd
import numpy as np
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import librosa
import tempfile
from dotenv import load_dotenv
from yt_dlp import YoutubeDL
import imageio_ffmpeg
import time
import pyloudnorm as pyln
import warnings
warnings.filterwarnings('ignore')

# Load Environment Variables
load_dotenv()

app = FastAPI(title="Music Hit Predictor API (YouTube Engine)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
MODELS_PATH = os.path.join(os.path.dirname(__file__), "models")
# FEATURE LIST (5 specific features from model-code)
ALL_FEATURES = ['tempo', 'loudness', 'key', 'mode', 'energy']
SCALER_PATH = os.path.join(MODELS_PATH, "feature_scaler.pkl")

# Load Scaler
if os.path.exists(SCALER_PATH):
    scaler = joblib.load(SCALER_PATH)
else:
    scaler = None
    print("⚠️ WARNING: Scaler not found at", SCALER_PATH)

FFMPEG_PATH = imageio_ffmpeg.get_ffmpeg_exe()

def extract_real_features(file_path):
    """
    Extracts audio features equivalent to Spotify's using librosa.
    Normalized to -14.0 LUFS with energy boosting for local files.
    """
    try:
        y, sr = librosa.load(file_path, sr=22050, mono=True)
        
        try:
            meter = pyln.Meter(sr)
            lufs_current = meter.integrated_loudness(y)
            y = pyln.normalize.loudness(y, lufs_current, -14.0)
        except Exception:
            pass

        features = {}
        features['duration_ms'] = float(librosa.get_duration(y=y, sr=sr) * 1000)
        
        tempo_array = librosa.feature.tempo(y=y, sr=sr)
        features['tempo'] = float(tempo_array[0])
        
        rms = librosa.feature.rms(y=y)
        features['loudness'] = -14.0 

        chromagram = librosa.feature.chroma_cqt(y=y, sr=sr)
        chroma_vals = np.sum(chromagram, axis=1)
        key_idx = np.argmax(chroma_vals)
        features['key'] = int(key_idx)
        
        maj_profile = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
        min_profile = [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]
        
        maj_profile = np.roll(maj_profile, key_idx)
        min_profile = np.roll(min_profile, key_idx)
        
        maj_corr = np.corrcoef(chroma_vals, maj_profile)[0,1]
        min_corr = np.corrcoef(chroma_vals, min_profile)[0,1]
        features['mode'] = 1 if maj_corr > min_corr else 0
        
        rms_mean = np.mean(rms)
        features['energy'] = float(min(rms_mean * 4.5, 1.0))
        
        # Adding some missing fields used in visualization if needed (though model only uses 5)
        features['spectral_centroid'] = float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)))
        
        return features
    except Exception as e:
        print(f"Extraction error: {e}")
        return None

def get_audio_from_youtube(url_or_query):
    """Downloads audio from YouTube and returns metadata + path."""
    out_filename = os.path.join(tempfile.gettempdir(), f"yt_{int(time.time())}")
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': out_filename,
        'ffmpeg_location': FFMPEG_PATH,
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '128'}],
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url_or_query, download=True)
            return {
                "path": f"{out_filename}.mp3",
                "title": info.get('title', 'Unknown YouTube Track')
            }
        except Exception as e:
            print(f"YouTube Error: {e}")
            return None

@app.post("/predict")
async def predict(
    model_name: str = Form(...),
    file: UploadFile = File(None),
    youtube_url: str = Form(None)
):
    # 1. Select Model
    model_slug = model_name.lower()
    is_voting = 'multi-vote' in model_slug or 'ensemble' in model_slug or 'voting' in model_slug
    
    if is_voting:
        model_files = ["xgboost_model.pkl", "randomforest_model.pkl", "knn_model.pkl", "adaboost_model.pkl", "decisiontree_model.pkl"]
        models = []
        for f in model_files:
            p = os.path.join(MODELS_PATH, f)
            if os.path.exists(p): models.append(joblib.load(p))
        if not models:
            raise HTTPException(status_code=404, detail="No models found for voting")
    else:
        if 'xgboost' in model_slug: model_filename = "xgboost_model.pkl"
        elif 'random' in model_slug: model_filename = "randomforest_model.pkl"
        elif 'knn' in model_slug: model_filename = "knn_model.pkl"
        elif 'adaboost' in model_slug: model_filename = "adaboost_model.pkl"
        elif 'decision' in model_slug or 'tree' in model_slug: model_filename = "decisiontree_model.pkl"
        else: model_filename = "xgboost_model.pkl"
        
        model_path = os.path.join(MODELS_PATH, model_filename)
        if not os.path.exists(model_path):
            raise HTTPException(status_code=404, detail=f"Model file {model_filename} not found")
        model = joblib.load(model_path)
    
    features_dict = None
    track_display_name = "Unknown Track"

    # 2. Extract Data
    if file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
            tmp.write(await file.read())
            features_dict = extract_real_features(tmp.name)
            track_display_name = file.filename
        try: os.unlink(tmp.name)
        except: pass
        
    elif youtube_url:
        yt_data = get_audio_from_youtube(youtube_url)
        if yt_data:
            track_display_name = yt_data['title']
            features_dict = extract_real_features(yt_data['path'])
            try: os.remove(yt_data['path'])
            except: pass
    
    if not features_dict:
        raise HTTPException(status_code=500, detail="Failed to process audio source")

    # 3. Scale & Predict
    df_input = pd.DataFrame([features_dict])[ALL_FEATURES]
    X_scaled = scaler.transform(df_input) if scaler else df_input
    
    if is_voting:
        hits = 0
        for m in models:
            if m.predict(X_scaled)[0] == 1: hits += 1
        prob = hits / len(models)
    else:
        # Check if model has predict_proba
        if hasattr(model, "predict_proba"):
            prob = model.predict_proba(X_scaled)[0][1]
        else:
            prob = float(model.predict(X_scaled)[0])
        
    is_hit = prob >= 0.5
    
    analysis = [
        {"feature": "Tempo", "value": f"{int(features_dict['tempo'])} BPM", "impact": "Fast pace" if features_dict['tempo'] > 120 else "Slow/Chill vibe"},
        {"feature": "Energy", "value": f"{features_dict['energy']:.2f}", "impact": "High intensity" if features_dict['energy'] > 0.5 else "Soft/Acoustic"},
        {"feature": "Loudness", "value": f"{features_dict['loudness']:.1f} dB", "impact": "Normalized Focus"},
        {"feature": "Model", "value": "Multi-Vote Model (Exclusive 🔥)" if is_voting else model_name, "impact": "Prediction Engine"}
    ]
    
    return {
        "isHit": bool(is_hit),
        "probability": round(float(prob) * 100, 1),
        "trackName": track_display_name,
        "model": model_name,
        "features": features_dict,
        "analysis": analysis
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
