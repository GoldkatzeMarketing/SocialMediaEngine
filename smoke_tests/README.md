# Smoke Tests

Validiert die Infrastruktur **bevor** wir die volle Pipeline bauen.
Jeder Test laeuft isoliert, druckt ✅ oder ❌, und stoppt bei Fehler.

## Setup (einmal)

```bash
# 1. Python-Env (in Projekt-Root)
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. .env anlegen
cp .env.example .env
# → .env mit deinen Keys fuellen

# 3. ffmpeg (falls nicht installiert)
brew install ffmpeg          # Mac
sudo apt install ffmpeg      # Linux
```

## Alle Tests

```bash
python smoke_tests/run_all.py
```

## Einzeln

```bash
python smoke_tests/test_01_claude.py
python smoke_tests/test_02_heygen.py
python smoke_tests/test_03_elevenlabs.py             # connectivity only
python smoke_tests/test_03_elevenlabs.py --generate  # voll, ~$0.02
python smoke_tests/test_04_apify.py                  # ~$0.01
python smoke_tests/test_05_whisper.py
python smoke_tests/test_06_telegram.py
python smoke_tests/test_07_ffmpeg.py
```

## Reihenfolge der Tests

| # | Was | Voraussetzung | Kosten |
|---|---|---|---|
| 1 | Claude API ping | `ANTHROPIC_API_KEY` | <$0.01 |
| 2 | HeyGen avatars + voices listen | `HEYGEN_API_KEY` | $0 |
| 3 | ElevenLabs voices listen (+ optional TTS) | `ELEVENLABS_API_KEY` | $0 oder $0.02 |
| 4 | Apify scrape 1 Reel | `APIFY_API_TOKEN` + `monitoring/instagram_channels.txt` | ~$0.01 |
| 5 | Whisper transcribiert Sample aus Test 3 oder 4 | `faster-whisper` installiert | $0 |
| 6 | Telegram-Bot sendet Test-Message | `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` | $0 |
| 7 | ffmpeg composite-Test | `ffmpeg` im PATH | $0 |

**Gesamtkosten Smoke-Test-Run:** ~$0.03

## End-to-End-Test (Inspiration → fertiges Sophie-MP4)

```bash
python smoke_tests/test_e2e_inspiration.py
```

Was passiert:

1. Erstes Profil aus `monitoring/instagram_channels.txt`
2. Apify scraped neuestes Reel
3. Whisper transkribiert das Reel (= Inspiration)
4. Claude generiert ein Sophie-Skript zum gleichen Thema
5. HeyGen rendert Avatar-Video (~4 min)
6. Pillow rendert statische Top-Karte (40% Brand-Layout)
7. ffmpeg stacked 40/60 + Whisper word-level Captions als ASS-Burn
8. Telegram bekommt das fertige MP4

**Output:** `runs/{timestamp}_smoke_{profile}/final.mp4`
**Kosten:** ~$0.40, **Dauer:** ~10-15 min

Voraussetzung: Tests 1-7 sind alle gruen.

## Bei Fehler

- Output durchlesen – jeder Test sagt was fehlt
- API-Key falsch / abgelaufen → in `.env` updaten
- Network / Firewall → von einem anderen Netz probieren
- Buffer ist NICHT dabei (kommt in Phase 1.5, wenn Pipeline-Output fertig ist)
