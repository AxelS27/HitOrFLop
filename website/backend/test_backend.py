import requests
url = "http://localhost:8000/predict"
data = {"model_name": "XGBoost", "spotify_link": "https://open.spotify.com/track/0VjIj9R9YfS3o6yH7mG7EB"}
response = requests.post(url, data=data)
print(response.status_code)
print(response.json())
