import joblib
import os

scaler_path = r"c:\Users\farre\OneDrive\Documents\Binus-Projects\MachineLearning\model_training\models\audio_scaler.pkl"
scaler = joblib.load(scaler_path)

if hasattr(scaler, "feature_names_in_"):
    print("Expected Features:")
    for f in scaler.feature_names_in_:
        print(f)
else:
    print("Scaler does not have feature_names_in_. Checking n_features_in_")
    print("Number of features:", scaler.n_features_in_)
