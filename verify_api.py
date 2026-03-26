import os
import requests
from dotenv import load_dotenv

load_dotenv()

def verify():
    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
    
    # Get Token
    auth_url = "https://accounts.spotify.com/api/token"
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })
    
    if auth_response.status_code != 200:
        print(f"❌ Auth Failed: {auth_response.status_code} {auth_response.text}")
        return
        
    token = auth_response.json().get('access_token')
    print(f"✅ Token Obtained: {token[:10]}...")
    
    # Try Playlist
    playlist_id = "37i9dQZF1DX2hkHFfKWhWW" # Top 50 Indonesia
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit=5"
    headers = {"Authorization": f"Bearer {token}"}
    
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        print("✅ API Access Works! Successfully fetched playlist tracks.")
        tracks = r.json().get('items', [])
        for i, item in enumerate(tracks):
            t = item.get('track')
            if t:
                print(f"   {i+1}. {t['name']} - {t['artists'][0]['name']}")
    else:
        print(f"❌ API Access Failed: {r.status_code} {r.text}")

if __name__ == "__main__":
    verify()
