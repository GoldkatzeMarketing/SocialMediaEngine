"""
Pipeline Konfiguration
======================
Lädt alle API-Keys und Konstanten aus Environment-Variablen.

Erstelle eine .env-Datei im Projekt-Root mit:
    ANTHROPIC_API_KEY=sk-ant-...
    HEYGEN_API_KEY=...
    ELEVENLABS_API_KEY=...
    HIGGSFIELD_API_KEY=...
    MANYCHAT_API_KEY=...
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# .env laden
load_dotenv()

# ── API Keys ──────────────────────────────────────────────────────────────
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
HEYGEN_API_KEY = os.getenv("HEYGEN_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
HIGGSFIELD_API_KEY = os.getenv("HIGGSFIELD_API_KEY")  # optional, Phase 2+
MANYCHAT_API_KEY = os.getenv("MANYCHAT_API_KEY")      # optional, Phase 1.5

# ── Pfade ─────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent.parent
RUNS_DIR = PROJECT_ROOT / "runs"
TEMPLATES_DIR = PROJECT_ROOT / "templates"
BRAND_ASSETS_DIR = PROJECT_ROOT / "brand_assets"
DIRECTIVES_DIR = PROJECT_ROOT / "directives"

# ── Persona-Defaults (overridebar in PERSONAS.md) ─────────────────────────
SOPHIE = {
    "avatar_group_id": "300122b0d08d4f8891c695cfb92aacad",
    "default_look_id": "7755410b9fd54f359ba89a6c5dbc17e8",
    "voice_id": "3020b907712a43dbb4a8b186c6144ffd",
    "voice_settings": {
        "engine_type": "elevenlabs",
        "model": "eleven_multilingual_v2",
        "similarity_boost": 0.6,
        "stability": 0.5,
        "style": 0.25,
        "use_speaker_boost": True,
        "speed": 1.0,
    },
    "look_mapping": {
        "tool_review": "7755410b9fd54f359ba89a6c5dbc17e8",       # AI Video Host
        "strategy_insight": None,                                  # Cafe Sipper (ID nachtragen)
        "authority_statement": None,                               # Speaker at Mic (ID nachtragen)
        "neutral": None,                                           # Sophie generic (ID nachtragen)
    },
}

JONAS = {
    # Phase 3 – noch nicht aktiv
    "avatar_group_id": None,
    "default_look_id": None,
    "voice_id": None,
    "voice_settings": SOPHIE["voice_settings"],  # gleicher Default
}

PERSONAS = {
    "sophie": SOPHIE,
    "jonas": JONAS,
}

# ── Pipeline-Settings ─────────────────────────────────────────────────────
VIDEO_OUTPUT_DIMENSION = {"width": 1080, "height": 1920}
ANIMATION_DIMENSION = {"width": 1080, "height": 768}   # obere 40%
AVATAR_CROP_DIMENSION = {"width": 1080, "height": 1152}  # untere 60%
CAPTION_Y_POSITION = 760  # px – auf der Trennlinie

# Brand-Style (synced mit BRAND_STYLE.md)
BRAND_COLORS = {
    "bg_base": "#FFFFFF",
    "accent": "#FF6B35",
    "text_primary": "#0A0A0A",
    "text_secondary": "#525252",
}

# Claude API Config
CLAUDE_MODEL = "claude-opus-4-7"  # Aktuelles Top-Modell
CLAUDE_MAX_TOKENS = 4000

# ── Validation ────────────────────────────────────────────────────────────
def validate_config():
    """Prüft, ob alle nötigen API-Keys gesetzt sind."""
    required = {
        "ANTHROPIC_API_KEY": ANTHROPIC_API_KEY,
        "HEYGEN_API_KEY": HEYGEN_API_KEY,
        "ELEVENLABS_API_KEY": ELEVENLABS_API_KEY,
    }
    missing = [k for k, v in required.items() if not v]
    if missing:
        raise EnvironmentError(f"Missing required env vars: {', '.join(missing)}")


if __name__ == "__main__":
    validate_config()
    print("✅ Config OK")
