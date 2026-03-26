import requests

def test():
    # Attempting to predict with a real Spotify track link
    url = "http://127.0.0.1:8001/predict"
    data = {"spotify_url": "https://open.spotify.com/track/4u87VfT1ZpP6g3jU1vS8yV"} # Use a common hit
    
    try:
        r = requests.post(url, data=data)
        print("Response:", r.json())
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test()
