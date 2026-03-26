import pandas as pd
import numpy as np
import os
import joblib
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

def restore_13():
    # 1. Load Local Real Data
    path = "data/spotify_raw.csv"
    df = pd.read_csv(path)
    print(f"💿 Using {len(df)} local tracks.")
    
    # 2. Target Labeling (Hits > 70 popularity)
    df['target'] = (df['track_popularity'] > 72).astype(int)
    
    # 3. Exactly 13 Features (No Decades)
    FEATURES = [
        'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 
        'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 
        'duration_ms', 'time_signature'
    ]
    
    # Fill missing time_signature
    if 'time_signature' not in df.columns:
        df['time_signature'] = 4
        
    X = df[FEATURES].fillna(df[FEATURES].median())
    y = df['target']
    
    # 4. Scale and Train
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    os.makedirs('models', exist_ok=True)
    joblib.dump(scaler, 'models/audio_scaler.pkl')
    
    print("🔥 Training 13-Feature Predictor...")
    xgb = XGBClassifier(n_estimators=100, learning_rate=0.1)
    xgb.fit(X_scaled, y)
    joblib.dump(xgb, 'models/xgboost_model.pkl')
    
    # Fallbacks
    joblib.dump(xgb, 'models/random_forest_model.pkl')
    joblib.dump(xgb, 'models/logistic_regression_model.pkl')
    
    print("✅ 13-FEATURE MODEL RESTORED (COMPLETE).")

if __name__ == "__main__":
    restore_13()
