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
SCALER_PATH = os.path.join(MODELS_PATH, "audio_scaler.pkl")
FFMPEG_PATH = imageio_ffmpeg.get_ffmpeg_exe()

# FEATURE LIST (17 Librosa Features)
ALL_FEATURES = [
    'tempo', 'spectral_centroid', 'zcr', 'energy',
    'mfcc_1', 'mfcc_2', 'mfcc_3', 'mfcc_4', 'mfcc_5', 
    'mfcc_6', 'mfcc_7', 'mfcc_8', 'mfcc_9', 'mfcc_10', 
    'mfcc_11', 'mfcc_12', 'mfcc_13'
]

# Load Scaler
if os.path.exists(SCALER_PATH):
    scaler = joblib.load(SCALER_PATH)
else:
    scaler = None
    print("⚠️ WARNING: Scaler not found at", SCALER_PATH)

def extract_real_features(audio_path):
    """Directly extracts the 17 Librosa features used in training."""
    try:
        # Load 30 seconds
        y, sr = librosa.load(audio_path, duration=30)
        
        # 1. Base Features
        tempo_var, _ = librosa.beat.beat_track(y=y, sr=sr)
        tempo = float(tempo_var[0]) if isinstance(tempo_var, np.ndarray) else float(tempo_var)
        spectral_centroid = float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)))
        zcr = float(np.mean(librosa.feature.zero_crossing_rate(y)))
        rmse = float(np.mean(librosa.feature.rms(y=y)))
        
        # 2. MFCCs
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        mfcc_means = np.mean(mfccs, axis=1)
        
        feats = {
            'tempo': tempo,
            'spectral_centroid': spectral_centroid,
            'zcr': zcr,
            'energy': rmse,
        }
        for i, val in enumerate(mfcc_means):
            feats[f'mfcc_{i+1}'] = float(val)
            
        return feats
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
    if 'xgboost' in model_slug: model_filename = "xgboost_model.pkl"
    elif 'logistic' in model_slug: model_filename = "logistic_regression_model.pkl"
    elif 'svm' in model_slug: model_filename = "svm_model.pkl"
    elif 'random' in model_slug: model_filename = "random_forest_model.pkl"
    elif 'knn' in model_slug: model_filename = "knn_model.pkl"
    else: model_filename = "random_forest_model.pkl"
    
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
    df = pd.DataFrame([features_dict])[ALL_FEATURES]
    X_scaled = scaler.transform(df) if scaler else df
    
    # Check if model has predict_proba
    if hasattr(model, "predict_proba"):
        prob = model.predict_proba(X_scaled)[0][1]
    else:
        # Fallback for models without proba (though SVC has probability=True)
        prob = float(model.predict(X_scaled)[0])
        
    is_hit = prob > 0.5
    
    analysis = [
        {"feature": "Tempo", "value": f"{int(features_dict['tempo'])} BPM", "impact": "Fast pace" if features_dict['tempo'] > 120 else "Slow/Chill vibe"},
        {"feature": "Energy (RMS)", "value": f"{features_dict['energy']:.2f}", "impact": "High intensity" if features_dict['energy'] > 0.1 else "Soft/Acoustic"},
        {"feature": "Brightness", "value": f"{int(features_dict['spectral_centroid'])} Hz", "impact": "Bright/Poppy" if features_dict['spectral_centroid'] > 2000 else "Mellow/Dark"},
        {"feature": "Model", "value": model_name, "impact": "Prediction Engine"}
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
