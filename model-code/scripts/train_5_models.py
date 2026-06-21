import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

def main():
    print("🚀 Training Big 5 Ensemble (Threshold=15)...")
    if not os.path.exists('dataset.csv'):
        print("❌ Error: dataset.csv not found!")
        return
        
    df = pd.read_csv('dataset.csv')
    features = ['tempo', 'loudness', 'key', 'mode', 'energy']
    
    # 1. Preprocessing
    df = df.dropna(subset=features + ['popularity'])
    df = df[df['energy'] > 0.1]
    
    THRESHOLD = 15
    df['is_hit'] = (df['popularity'] >= THRESHOLD).astype(int)
    
    # 2. Resampling (Balanced Classes)
    df_hits = df[df['is_hit'] == 1]
    df_flops = df[df['is_hit'] == 0]
    min_samples = min(len(df_hits), len(df_flops))
    
    df_balanced = pd.concat([
        df_hits.sample(n=min_samples, random_state=42),
        df_flops.sample(n=min_samples, random_state=42)
    ]).sample(frac=1, random_state=42).reset_index(drop=True)
    
    X = df_balanced[features]
    y = df_balanced['is_hit']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # 3. Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    joblib.dump(scaler, 'feature_scaler.pkl')

    # 4. Model Training
    models_def = {
        "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
        "AdaBoost": AdaBoostClassifier(n_estimators=100, random_state=42), 
        "KNN": KNeighborsClassifier(n_neighbors=5, n_jobs=-1),
        "DecisionTree": DecisionTreeClassifier(max_depth=10, random_state=42),
        "XGBoost": XGBClassifier(tree_method='hist', device='cuda', random_state=42)
    }

    if not os.path.exists('models'): os.makedirs('models')

    for name, model in models_def.items():
        print(f"🧠 Learning: {name}...")
        if name == "XGBoost":
            try:
                model.fit(X_train_scaled, y_train)
            except:
                model.set_params(device='cpu')
                model.fit(X_train_scaled, y_train)
        else:
            model.fit(X_train_scaled, y_train)
        
        y_pred = model.predict(X_test_scaled)
        print(f"✅ {name} Accuracy: {accuracy_score(y_test, y_pred):.4f}")
        joblib.dump(model, f'models/{name.lower()}_model.pkl')

    print("\n🏆 Training Completed.")

if __name__ == "__main__":
    main()
