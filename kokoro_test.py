import requests
import json

response = requests.post(
    "http://localhost:8880/dev/captioned_speech",
    json={
        "input": "Hola Amigos.  Este es el curso de guit",
        "voice": "bm_daniel",
        "response_format": "wav",
        "speed": 1.0,
        "lang_code": "es"
    }
)

# Save the audio
with open("output.wav", "wb") as f:
    f.write(response.content)

# Get the timestamps file
timestamps_path = response.headers.get("X-Timestamps-Path")
if timestamps_path:
    timestamps_response = requests.get(f"http://localhost:8880/dev/timestamps/{timestamps_path}")
    timestamps = json.loads(timestamps_response.text)
    print(json.dumps(timestamps, indent=2))
