"""
Smoke Test 5: faster-whisper
- Validiert dass Whisper laeuft
- Erwartet eine MP3 oder MP4 aus Test 3 (ElevenLabs --generate) oder Test 4 (Apify Video-URL)
- Kosten: $0 (lokal)
"""
import sys
import urllib.request
from pathlib import Path
import json
from _helpers import ok, fail


def main():
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        fail("faster-whisper not installed", ImportError("pip install -r requirements.txt"))

    sample_audio = Path(__file__).parent / "_test_output.mp3"
    apify_sample = Path(__file__).parent / "_apify_sample.json"

    audio_file = None
    if sample_audio.exists():
        audio_file = sample_audio
        ok(f"Verwende ElevenLabs-Sample: {audio_file.name}")
    elif apify_sample.exists():
        data = json.loads(apify_sample.read_text())
        video_url = data.get("videoUrl")
        if not video_url:
            fail("Apify-Sample hat keine videoUrl. Run test_04 erneut oder test_03 --generate.")
            return
        ok(f"Lade Reel von {video_url[:60]}...")
        audio_file = Path(__file__).parent / "_apify_sample.mp4"
        try:
            urllib.request.urlretrieve(video_url, audio_file)
            ok(f"Download ok: {audio_file.stat().st_size / 1024:.1f} KB")
        except Exception as e:
            fail("Reel-Download failed (CDN-Link evtl. abgelaufen)", e)
            return
    else:
        fail("Keine Audio-Quelle. Run zuerst test_03_elevenlabs.py --generate oder test_04_apify.py.")
        return

    try:
        ok("Lade Whisper-Modell 'base' (~140MB beim ersten Mal)...")
        model = WhisperModel("base", device="cpu", compute_type="int8")
        ok("Modell geladen. Transkribiere...")
        segments, info = model.transcribe(str(audio_file), language="de", beam_size=5)
        segments = list(segments)
        text = " ".join(s.text for s in segments).strip()
        ok(f"Sprache erkannt: {info.language} (confidence {info.language_probability:.2f})")
        ok(f"Dauer: {info.duration:.1f}s")
        ok(f"Transkript ({len(segments)} segments):")
        print(f"   '{text[:200]}{'...' if len(text) > 200 else ''}'")
    except Exception as e:
        fail("Whisper transcription failed", e)


if __name__ == "__main__":
    main()
