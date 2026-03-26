import os
import requests
from dotenv import load_dotenv

load_dotenv('.env')

client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')

# Step 1: Get Token
token_url = "https://accounts.spotify.com/api/token"
token_response = requests.post(token_url, data={"grant_type": "client_credentials"}, auth=(client_id, client_secret))
token = token_response.json().get('access_token')

# Step 2: Get Track Info
track_id = "3IPqpem3qYER2n1TFJNjL4"
info_url = f"https://api.spotify.com/v1/tracks/{track_id}"
info_response = requests.get(info_url, headers={"Authorization": f"Bearer {token}"})
data = info_response.json()
print(f"Track: {data['name']}")
print(f"Preview URL: {data.get('preview_url')}")
