import joblib
import os
import numpy as np

class MusicHitPredictorAPI:
    """
    Backend API support for Single Model and Multi-Model Voting.
    """
    def __init__(self, models_dir='models', scaler_path='feature_scaler.pkl'):
        if not os.path.exists(scaler_path):
            raise FileNotFoundError(f"Scaler not found at {scaler_path}")
            
        self.scaler = joblib.load(scaler_path)
        self.models = {}
        
        if os.path.exists(models_dir):
            for f in os.listdir(models_dir):
                if f.endswith('_model.pkl'):
                    m_name = f.replace('_model.pkl', '').upper()
                    self.models[m_name] = joblib.load(os.path.join(models_dir, f))
        
        if not self.models:
            print("⚠️ Backend: No models loaded.")

    def get_available_models(self):
        return list(self.models.keys())

    def predict(self, features_dict, model_mode='VOTING', specific_model=None):
        """
        Main Prediction Interface.
        :param features_dict: (tempo, loudness, key, mode, energy)
        """
        feature_order = ['tempo', 'loudness', 'key', 'mode', 'energy']
        X = np.array([[features_dict[k] for k in feature_order]])
        X_scaled = self.scaler.transform(X)

        if model_mode == 'SINGLE' and specific_model:
            model = self.models.get(specific_model.upper())
            if not model:
                return {"error": f"Model {specific_model} not found."}
                
            pred = model.predict(X_scaled)[0]
            prob = model.predict_proba(X_scaled)[0][pred]
            return {
                "prediction": "HIT" if pred == 1 else "FLOP",
                "confidence": float(prob * 100),
                "model_used": specific_model.upper()
            }

        hit_count = 0
        total_models = len(self.models)
        detailed_results = {}
        
        for name, model in self.models.items():
            p = model.predict(X_scaled)[0]
            prob = model.predict_proba(X_scaled)[0][p]
            res = "HIT" if p == 1 else "FLOP"
            if p == 1: hit_count += 1
            detailed_results[name] = {"result": res, "confidence": float(prob * 100)}

        if hit_count == total_models:
            consensus = "ULTRA HIT"
        elif hit_count >= (total_models / 2 + 1):
            consensus = "POTENTIAL HIT"
        elif hit_count >= 1:
            consensus = "RISKY"
        else:
            consensus = "TOTAL FLOP"

        return {
            "consensus": consensus,
            "hit_ratio": f"{hit_count}/{total_models}",
            "detailed_results": detailed_results
        }
