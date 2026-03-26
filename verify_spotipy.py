import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

dotenv_path = os.path.join("website", "backend", ".env")
load_dotenv(dotenv_path)

def verify_spotipy():
    try:
        client_credentials_manager = SpotifyClientCredentials()
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        
        # Try playlist: Top 50 Indonesia
        pid = "37i9dQZF1DX2hkHFfKWhWW"
        results = sp.playlist_tracks(pid, limit=1)
        print(f"✅ SUCCESS! Playlist Found: {results['items'][0]['track']['name']} by {results['items'][0]['track']['artists'][0]['name']}")
        
    except Exception as e:
        print(f"❌ API Access Failed: {e}")

if __name__ == "__main__":
    verify_spotipy()
