import librosa
import numpy as np
import joblib
import os
import glob
from librosa_extractor import extract_features_from_audio

def predict_multiple_models(file_path):
    # Load Scaler
    scaler = joblib.load('feature_scaler.pkl')
    
    # Load Big 5 Models from files
    model_dir = 'models'
    # Specify manual order to ensure consistency
    expected_models = ['randomforest', 'adaboost', 'knn', 'decisiontree', 'xgboost']
    
    # Extract Features
    try:
        features = extract_features_from_audio(file_path)
    except Exception as e:
        print(f"❌ GAGAL EKSTRAK: {e}")
        return None
        
    feature_order = ['tempo', 'loudness', 'key', 'mode', 'energy']
    X_input = np.array([[features[k] for k in feature_order]])
    X_scaled = scaler.transform(X_input)
    
    print(f"\n🎵 PREDIKSI LAGU: {os.path.basename(file_path)}")
    print("=" * 60)
    
    results = []
    hit_count = 0
    
    for m_name in expected_models:
        model_path = os.path.join(model_dir, f"{m_name}_model.pkl")
        if not os.path.exists(model_path):
            continue
            
        model = joblib.load(model_path)
        pred = model.predict(X_scaled)[0]
        prob = model.predict_proba(X_scaled)[0]
        confidence = prob[pred] * 100
        
        status = "🔥 HIT 🔥" if pred == 1 else "🧊 FLOP 🧊"
        if pred == 1: hit_count += 1
        
        print(f"[{m_name.upper():15}] Prediksi: {status:10} | Keyakinan: {confidence:5.2f}%")
        results.append({'model': m_name.upper(), 'prediksi': status, 'keyakinan': confidence})
    
    # Consensus Logic (Big 5 Edition)
    total_found = len(results)
    consensus = ""
    if hit_count == total_found:
        consensus = "🌋 ULTRA HIT (5/5 Model Sepakat!)"
    elif hit_count >= 3:
        consensus = f"📈 POTENTIAL HIT ({hit_count}/5 Model Setuju)"
    elif hit_count >= 1:
        consensus = f"⚖️ DISKUSI ({hit_count}/5 Model Setuju - Berisiko)"
    else:
        consensus = "🧊 TOTAL FLOP (0/5 Model Sepakat)"

    print("-" * 60)
    print(f"🗳️ KESIMPULAN AKHIR: {consensus}")
    print("=" * 60 + "\n")
    
    return {'results': results, 'consensus': consensus}

def main():
    songs = glob.glob(r'testing_song\*.mp3')
    
    final_output = []
    for s in songs:
        res = predict_multiple_models(s)
        if res:
            final_output.append({'song': os.path.basename(s), 'results': res['results'], 'consensus': res['consensus']})
            
    # Save the output to a text file
    with open('multi_model_test_results.txt', 'w', encoding='utf-8') as f:
        f.write("🏆 HASIL KONSENSUS THE BIG 5 MODEL (THRESHOLD: 15) 🏆\n")
        f.write("=" * 70 + "\n\n")
        for entry in final_output:
            f.write(f"LAGU: {entry['song']}\n")
            f.write("-" * 40 + "\n")
            for r in entry['results']:
                f.write(f"[{r['model']:15}] {r['prediksi']:10} | {r['keyakinan']:6.2f}%\n")
            f.write(f"\n🗳️ KESIMPULAN: {entry['consensus']}\n")
            f.write("=" * 70 + "\n\n")
    
    print("📜 HASIL LENGKAP TERSIMPAN DI multi_model_test_results.txt")

if __name__ == "__main__":
    main()
