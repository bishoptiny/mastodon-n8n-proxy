import requests
import sseclient
import json
from flask import Flask
import threading
import os

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
MASTODON_STREAM_URL = os.getenv('MASTODON_STREAM_URL')
N8N_WEBHOOK_URL = os.getenv('N8N_WEBHOOK_URL')

app = Flask(__name__)

def stream_mastodon():
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }
    response = requests.get(MASTODON_STREAM_URL, headers=headers, stream=True)
    client = sseclient.SSEClient(response)

    for event in client.events():
        if event.event == "notification":
            data = json.loads(event.data)
            if "weather" in data.get("status", {}).get("content", "").lower():
                requests.post(N8N_WEBHOOK_URL, json=data)

@app.route("/")
def home():
    return "Mastodon Proxy Running!"

if __name__ == "__main__":
    threading.Thread(target=stream_mastodon, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
