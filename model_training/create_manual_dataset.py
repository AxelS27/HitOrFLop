import os
import json
import librosa
import numpy as np
import imageio_ffmpeg
from yt_dlp import YoutubeDL
import time

# Konfigurasi Lokasi
FFMPEG_PATH = imageio_ffmpeg.get_ffmpeg_exe()
JSON_FILE = "indo_music_sample.json"

def load_existing_data():
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, "r") as f:
                content = f.read().strip()
                if not content: return []
                return json.loads(content)
        except Exception as e:
            print(f"Info: Gagal baca JSON lama ({e}), mulai baru.")
            return []
    return []

def save_data(dataset):
    try:
        with open(JSON_FILE, "w") as f:
            json.dump(dataset, f, indent=4)
    except Exception as e:
        print(f"Error saving JSON: {e}")

def extract_audio_features(audio_path):
    try:
        y, sr = librosa.load(audio_path, duration=30)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        if isinstance(tempo, np.ndarray):
            tempo = tempo[0] if tempo.size > 0 else 0
        
        mfcc = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13), axis=1)
        spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
        zcr = np.mean(librosa.feature.zero_crossing_rate(y))
        rmse = np.mean(librosa.feature.rms(y=y))
        
        return {
            "tempo": float(tempo),
            "spectral_centroid": float(spectral_centroid),
            "zcr": float(zcr),
            "energy": float(rmse),
            **{f"mfcc_{i+1}": float(v) for i, v in enumerate(mfcc)}
        }
    except Exception as e:
        print(f"Error extracting audio: {e}")
        return None

def process_youtube_playlist(playlist_url, target_label, limit=20):
    print(f"\n📡 Memeriksa Playlist: {playlist_url}")
    ydl_opts_flat = {'extract_flat': True, 'quiet': True, 'playlist_end': limit}
    entries = []
    with YoutubeDL(ydl_opts_flat) as ydl:
        try:
            result = ydl.extract_info(playlist_url, download=False)
            if 'entries' in result:
                for entry in result['entries']:
                    if entry: entries.append({'id': entry['id'], 'title': entry['title'], 'target': target_label})
        except Exception as e:
            print(f"Error reading playlist: {e}")
            return

    dataset = load_existing_data()
    existing_ids = [d['youtube_id'] for d in dataset if 'youtube_id' in d]
    
    print(f"🔍 Playlist ini punya {len(entries)} lagu. Sudah ada {len(existing_ids)} di database total.")

    for entry in entries:
        if entry['id'] in existing_ids:
            print(f"⏩ SKIP: {entry['title']}")
            continue
            
        print(f"🎵 Memproses: {entry['title']}")
        out_filename = os.path.join(os.getcwd(), f"temp_{entry['id']}")
        ydl_opts_dl = {
            'format': 'bestaudio/best', 'quiet': True, 'outtmpl': out_filename,
            'ffmpeg_location': FFMPEG_PATH,
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '128'}],
        }

        with YoutubeDL(ydl_opts_dl) as ydl:
            try:
                ydl.download([f"https://www.youtube.com/watch?v={entry['id']}"])
                target_file = f"{out_filename}.mp3"
                if os.path.exists(target_file):
                    feat = extract_audio_features(target_file)
                    time.sleep(0.3)
                    try: os.remove(target_file)
                    except: pass
                    
                    if feat:
                        dataset.append({"title": entry['title'], "youtube_id": entry['id'], "target": entry['target'], **feat})
                        save_data(dataset)
                        print(f"✅ Tersimpan!")
            except Exception as e:
                print(f"Gagal: {e}")

if __name__ == "__main__":
    # KOLEKSI PLAYLIST INDO (Target: 200+ Lagu)
    HITS_PLAYLISTS = [
        "https://www.youtube.com/playlist?list=PL4fGSI1pDJn5QPpj0R4vVgRWk8sSq549G", # Hits Indo Spotify 2024
        "https://www.youtube.com/playlist?list=PL4fGSI1pDJn69m8_cMT6-5mI3XvWzW_vY", # Top Hits Indonesia
        "https://www.youtube.com/playlist?list=PLmndwJP2qZ1l-Y-mI3XvWzW_vYp9YjYsN", # Viral Indo
        "https://www.youtube.com/playlist?list=RDCLAK5uy_m-mCAt9Y_v_n7_Z_n2vYr_vYp9" # Pop Teranyar
    ]
    
    NON_HITS_PLAYLISTS = [
        "https://www.youtube.com/playlist?list=PLmndwJP2qZ1lS9WcAtb_rW_9v_n7_Z_n2", # Indie Indo
        "https://www.youtube.com/playlist?list=PLmndwJP2qZ1l0-eY3_n7X_Z_v_n7_Z_n2", # Underground / Niche
        "https://www.youtube.com/playlist?list=PLfGSI1pDJn5QPpj0R4vVgRWk8sSq549G", # Alternatif Niche
        "https://www.youtube.com/playlist?list=PLmndwJP2qZ1liLt4Qvwc1mkvR65oE3vAI"  # Old Non-Hits / Rare
    ]

    print(f"🚀 MEMULAI EKSTRAKSI 200 LAGU... GAS!")

    # Target 50 lagu per playlist untuk mencapai total 200+
    for pl in HITS_PLAYLISTS: 
        process_youtube_playlist(pl, 1, limit=50)
        
    for pl in NON_HITS_PLAYLISTS: 
        process_youtube_playlist(pl, 0, limit=50)
    
    print(f"\n✨ DATASET BERHASIL DIPERBARUI DENGAN TOTAL TERBARU!")
