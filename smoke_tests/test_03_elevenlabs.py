"""
Smoke Test 3: ElevenLabs API
- Connectivity (list voices, kostenlos)
- Generiert OPTIONAL 2s Test-Audio (kostet ~$0.02)
- Aufruf mit --generate fuer den vollen Test
"""
import sys
from pathlib import Path
from _helpers import require, ok, fail


def main(generate: bool = False):
    api_key = require("ELEVENLABS_API_KEY")

    try:
        from elevenlabs.client import ElevenLabs
    except ImportError:
        fail("elevenlabs SDK not installed", ImportError("pip install -r requirements.txt"))

    try:
        client = ElevenLabs(api_key=api_key)
        voices = client.voices.get_all()
        ok(f"ElevenLabs API erreichbar. {len(voices.voices)} Voices im Account.")
        ela = [v for v in voices.voices if "ela" in (v.name or "").lower()]
        if ela:
            ok(f"Voice 'Ela' gefunden: {ela[0].voice_id}")
    except Exception as e:
        fail("ElevenLabs API call failed", e)
        return

    if not generate:
        print("ℹ️  Skipping audio generation. Run with --generate to test full TTS (~$0.02).")
        return

    try:
        audio_stream = client.text_to_speech.convert(
            voice_id=ela[0].voice_id if ela else voices.voices[0].voice_id,
            model_id="eleven_multilingual_v2",
            text="Hallo, das ist ein Test.",
            voice_settings={"stability": 0.5, "similarity_boost": 0.6, "style": 0.25, "use_speaker_boost": True},
        )
        out = Path(__file__).parent / "_test_output.mp3"
        with open(out, "wb") as f:
            for chunk in audio_stream:
                f.write(chunk)
        size_kb = out.stat().st_size / 1024
        ok(f"Audio generiert: {out.name} ({size_kb:.1f} KB)")
    except Exception as e:
        fail("ElevenLabs TTS failed", e)


if __name__ == "__main__":
    main(generate="--generate" in sys.argv)
