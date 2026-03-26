import pandas as pd
import numpy as np
import os
import joblib
import json
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, f1_score

# 1. LOAD DATA
def train_arena():
    path = "indo_music_sample.json"
    if not os.path.exists(path):
        print(f"❌ ERROR: {path} not found!")
        return
        
    with open(path, 'r') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)
    print(f"✅ Loaded: {len(df)} tracks.")

    # 2. FEATURE SELECTION
    FEATURES = [
        'tempo', 'spectral_centroid', 'zcr', 'energy',
        'mfcc_1', 'mfcc_2', 'mfcc_3', 'mfcc_4', 'mfcc_5', 
        'mfcc_6', 'mfcc_7', 'mfcc_8', 'mfcc_9', 'mfcc_10', 
        'mfcc_11', 'mfcc_12', 'mfcc_13'
    ]

    X = df[FEATURES]
    y = df['target']

    # Split & Scale
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2026, stratify=y)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Balance (SMOTE)
    smote = SMOTE(random_state=2026)
    X_train_res, y_train_res = smote.fit_resample(X_train_scaled, y_train)

    # 3. MODELS
    models = {
        "XGBoost": XGBClassifier(eval_metric='logloss'),
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "SVM": SVC(probability=True, random_state=2026),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=2026),
        "KNN": KNeighborsClassifier(n_neighbors=5)
    }

    if not os.path.exists('models'): os.makedirs('models')
    joblib.dump(scaler, 'models/audio_scaler.pkl')

    for name, model in models.items():
        print(f"🔥 Training {name}...")
        model.fit(X_train_res, y_train_res)
        preds = model.predict(X_test_scaled)
        
        # Save
        filename = f"models/{name.lower().replace(' ', '_')}_model.pkl"
        joblib.dump(model, filename)
        
        acc = accuracy_score(y_test, preds)
        f1 = f1_score(y_test, preds)
        print(f"   📊 {name}: Accuracy={acc:.2%}, F1={f1:.2%}")

if __name__ == "__main__":
    train_arena()
