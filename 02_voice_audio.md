# Directive 02 – Voice-Audio (Optional Stage)

> **Stage 2** ist OPTIONAL. HeyGen kann ElevenLabs direkt aufrufen, ohne dass wir 
> Audio separat generieren. Diese Stage ist nur für **Sonderfälle**:
> - Audio-Preview vor HeyGen-Render (Skript-Review)
> - Audio für separate Use Cases (Podcasts, Reels mit anderem Video)
> - Voice-Tuning-Tests

In **Standard-Pipeline-Runs** wird diese Stage geskippt und Stage 3 (HeyGen) generiert 
Voice + Video in einem Schritt.

---

## Wenn Stage 2 läuft

### Input
- `script.md` aus Stage 1 (Voll-Skript-Sektion)
- Persona-Voice-ID aus `PERSONAS.md`

### Process
1. Voll-Skript-Text extrahieren (kein Markdown, keine Sektion-Headers)
2. ElevenLabs API mit Voice-Settings aus `PERSONAS.md` aufrufen
3. MP3 in `runs/{run_id}/audio.mp3` speichern

### Output
- `audio.mp3` – 44.1kHz mono, ~125kbps
- Dauer ca. 45-65 Sek

### State-Update
```markdown
### Stage 2: Voice-Audio
- Status: ✅ done
- Output: audio.mp3
- Dauer: 57.2s
- ElevenLabs-Request-ID: {id}
```

### Python-Sketch

```python
from elevenlabs import generate, save, voices, set_api_key

set_api_key(config.ELEVENLABS_API_KEY)

audio = generate(
    text=full_script_text,
    voice="Ela",  # oder voice_id direkt
    model="eleven_multilingual_v2",
    voice_settings={
        "stability": 0.5,
        "similarity_boost": 0.6,
        "style": 0.25,
        "use_speaker_boost": True,
    },
)
save(audio, f"runs/{run_id}/audio.mp3")
```
