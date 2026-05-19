# Directive 03 – Avatar-Video via HeyGen

> **Stage 3** generiert das Talking-Head-Video. Persona spricht das Skript mit 
> ElevenLabs-Voice und HeyGen-Lipsync. Dies ist das Kern-Output für die 
> Unterhälfte des finalen Split-Screen-Videos.

---

## Input

- `script.md` aus Stage 1 (Voll-Skript)
- Persona-Konfiguration aus `PERSONAS.md`
- Look-Recommendation aus Skript-Metadata (Stage 1 hat es schon gewählt)

---

## HeyGen API Call

### Endpoint
`POST https://api.heygen.com/v2/video/generate`

### Payload (für Sophie als Default)

```json
{
  "video_inputs": [
    {
      "character": {
        "type": "avatar",
        "avatar_id": "{look_id from PERSONAS.md}",
        "scale": 1.0
      },
      "voice": {
        "type": "text",
        "voice_id": "3020b907712a43dbb4a8b186c6144ffd",
        "input_text": "{Voll-Skript-Text mit UPPERCASE-Wörtern}",
        "speed": 1.0,
        "engine_settings": {
          "engine_type": "elevenlabs",
          "model": "eleven_multilingual_v2",
          "similarity_boost": 0.6,
          "stability": 0.5,
          "style": 0.25,
          "use_speaker_boost": true
        }
      }
    }
  ],
  "dimension": {
    "width": 1080,
    "height": 1920
  },
  "aspect_ratio": "9:16",
  "title": "{topic}",
  "caption": false
}
```

**Wichtig:**
- **`caption: false`** – wir generieren Captions selbst in Stage 5
- **`engine_type: elevenlabs`** – nutzt direkt deine ElevenLabs-Voice, nicht HeyGen-Stock-TTS
- **Look-ID** kommt aus dem Look-Mapping in `PERSONAS.md`

### Polling

HeyGen rendert asynchron. Pipeline pollt alle 15 Sek:
```
GET https://api.heygen.com/v1/video_status.get?video_id={id}
```

Status-Werte:
- `pending` – queued
- `processing` – in render
- `completed` – ready, video_url verfügbar
- `failed` – failure_message prüfen

Bei `completed`: Video-URL fetchen und in `runs/{run_id}/avatar_video.mp4` speichern.

---

## Edge Cases

### Skript zu lang (>90 Sek)
HeyGen rendert das, aber für Reels >60 Sek schlecht. Pipeline warnt bei Skript-Wortzahl >180.

### ElevenLabs-Voice nicht verfügbar
Fallback auf HeyGen-Stock-Voice "Sophie default" (`3020b907712a43dbb4a8b186c6144ffd`).

### Render-Failure
Pipeline retried 1× mit identischer Payload. Bei erneutem Fail: Status in `state.md`, 
manuelle Review erforderlich.

---

## Output

- `runs/{run_id}/avatar_video.mp4` – 1080×1920, ~30fps, H.264, AAC-Audio
- Dauer entspricht Skript-Sprechdauer

### State-Update

```markdown
### Stage 3: Avatar-Video
- Status: ✅ done
- HeyGen Video ID: a5e47d16933b4d0db9c16172345b3ad4
- Look genutzt: "The AI Video Host"
- Dauer: 70.16s
- Output: avatar_video.mp4
- Render-Zeit: 4m 12s
```

---

## Python-Sketch

```python
import requests, time
from pathlib import Path

def render_avatar_video(script_text, look_id, voice_id, output_path):
    headers = {"X-Api-Key": config.HEYGEN_API_KEY}
    
    # Submit render
    payload = {
        "video_inputs": [{
            "character": {"type": "avatar", "avatar_id": look_id, "scale": 1.0},
            "voice": {
                "type": "text",
                "voice_id": voice_id,
                "input_text": script_text,
                "speed": 1.0,
                "engine_settings": {
                    "engine_type": "elevenlabs",
                    "model": "eleven_multilingual_v2",
                    "similarity_boost": 0.6,
                    "stability": 0.5,
                    "style": 0.25,
                    "use_speaker_boost": True
                }
            }
        }],
        "dimension": {"width": 1080, "height": 1920},
        "aspect_ratio": "9:16",
        "caption": False
    }
    
    r = requests.post(
        "https://api.heygen.com/v2/video/generate",
        headers=headers,
        json=payload
    )
    video_id = r.json()["data"]["video_id"]
    
    # Poll status
    while True:
        time.sleep(15)
        status_r = requests.get(
            f"https://api.heygen.com/v1/video_status.get?video_id={video_id}",
            headers=headers
        )
        status = status_r.json()["data"]
        if status["status"] == "completed":
            video_url = status["video_url"]
            break
        if status["status"] == "failed":
            raise Exception(f"HeyGen render failed: {status.get('error', {})}")
    
    # Download
    video_data = requests.get(video_url).content
    Path(output_path).write_bytes(video_data)
    return video_id
```
