"""Whisper-Wrapper – Transkript fuer Inspiration, Word-Level fuer Captions."""
from pathlib import Path
from faster_whisper import WhisperModel

_model_cache = {}


def _get_model(size: str = "base"):
    if size not in _model_cache:
        _model_cache[size] = WhisperModel(size, device="cpu", compute_type="int8")
    return _model_cache[size]


def transcribe(media: Path, language: str = "de", model_size: str = "base") -> dict:
    """Returns {text, language, duration, segments}."""
    model = _get_model(model_size)
    segments, info = model.transcribe(str(media), language=language, beam_size=5)
    segs = [{"start": s.start, "end": s.end, "text": s.text.strip()} for s in segments]
    return {
        "text": " ".join(s["text"] for s in segs).strip(),
        "language": info.language,
        "duration": info.duration,
        "segments": segs,
    }


def transcribe_word_level(media: Path, language: str = "de", model_size: str = "base") -> list[dict]:
    """Returns list of {word, start, end} for caption-burning."""
    model = _get_model(model_size)
    segments, _ = model.transcribe(
        str(media), language=language, beam_size=5, word_timestamps=True
    )
    words = []
    for seg in segments:
        for w in seg.words or []:
            words.append({"word": w.word.strip(), "start": w.start, "end": w.end})
    return words
