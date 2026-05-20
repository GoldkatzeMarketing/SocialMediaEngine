"""HeyGen-Avatar-Render – Sophie spricht das Skript."""
import os
import time
import urllib.request
from pathlib import Path
import requests

SOPHIE_LOOK_ID = "7755410b9fd54f359ba89a6c5dbc17e8"  # The AI Video Host
SOPHIE_VOICE_ID = "3020b907712a43dbb4a8b186c6144ffd"

VOICE_SETTINGS = {
    "engine_type": "elevenlabs",
    "model": "eleven_multilingual_v2",
    "similarity_boost": 0.6,
    "stability": 0.5,
    "style": 0.25,
    "use_speaker_boost": True,
}


def render(script_text: str, output_path: Path, look_id: str = SOPHIE_LOOK_ID,
           voice_id: str = SOPHIE_VOICE_ID, title: str = "Sophie Smoke Test",
           poll_interval: int = 15, timeout_seconds: int = 900) -> str:
    api_key = os.getenv("HEYGEN_API_KEY")
    if not api_key:
        raise EnvironmentError("HEYGEN_API_KEY missing in .env")

    headers = {"X-Api-Key": api_key, "Content-Type": "application/json"}
    payload = {
        "video_inputs": [
            {
                "character": {"type": "avatar", "avatar_id": look_id, "scale": 1.0},
                "voice": {
                    "type": "text",
                    "voice_id": voice_id,
                    "input_text": script_text,
                    "speed": 1.0,
                    "engine_settings": VOICE_SETTINGS,
                },
            }
        ],
        "dimension": {"width": 1080, "height": 1920},
        "aspect_ratio": "9:16",
        "title": title,
        "caption": False,
    }

    r = requests.post("https://api.heygen.com/v2/video/generate", headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    video_id = r.json()["data"]["video_id"]
    print(f"   HeyGen video_id: {video_id}")

    start = time.time()
    while time.time() - start < timeout_seconds:
        time.sleep(poll_interval)
        s = requests.get(
            f"https://api.heygen.com/v1/video_status.get?video_id={video_id}",
            headers={"X-Api-Key": api_key}, timeout=15,
        )
        s.raise_for_status()
        data = s.json()["data"]
        status = data["status"]
        elapsed = int(time.time() - start)
        print(f"   [{elapsed}s] status: {status}")
        if status == "completed":
            video_url = data["video_url"]
            urllib.request.urlretrieve(video_url, output_path)
            return video_id
        if status == "failed":
            raise RuntimeError(f"HeyGen render failed: {data.get('error', {})}")
    raise TimeoutError(f"HeyGen render timed out after {timeout_seconds}s (video_id={video_id})")
