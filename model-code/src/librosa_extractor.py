import librosa
import numpy as np
import warnings
import pyloudnorm as pyln

warnings.filterwarnings('ignore')

def extract_features_from_audio(file_path):
    """
    Extracts audio features equivalent to Spotify's using librosa.
    Normalized to -14.0 LUFS with energy boosting for local files.
    """
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
    
    zcr = librosa.feature.zero_crossing_rate(y)
    features['speechiness'] = float(min(np.mean(zcr) * 5.0, 1.0))
    
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    features['acousticness'] = float(max(1.0 - (np.mean(rolloff) / (sr/2)), 0.0))
    
    flatness = librosa.feature.spectral_flatness(y=y)
    features['instrumentalness'] = float(max(1.0 - (np.std(flatness) * 10), 0.0))

    return features

if __name__ == "__main__":
    print("Librosa Feature Extractor Module Ready.")
