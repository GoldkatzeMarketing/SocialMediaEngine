# Video Pipeline – KI-Content für Sophie & Jonas

> **Single Source of Truth** für die automatisierte Video-Produktions-Pipeline.
> Diese Datei wird von Claude Code bei jedem Run gelesen und selbst aktualisiert
> (Self-Annealing Pattern).

---

## 1. Projekt-Ziel

Vollautomatisierte Generierung von Short-Form-Videos (Instagram Reels, TikTok, LinkedIn) 
für eine AI-/Agentur-Brand. Jedes Video:

- Persona-Host (Sophie für Strategie, später Jonas für Tech)
- Skript basiert entweder auf **Topic-Input** vom Mitarbeiter ODER auf **Influencer-Monitoring** (Phase 2)
- Split-Screen-Output: 40% oben Animations-Video, 60% unten Talking-Head
- Captions auf der Kante zwischen oben und unten, max 2 Wörter pro Frame
- Thumbnail als separates Bild für Feed-Wiedererkennung
- Comment-to-DM-CTA (ManyChat-Integration)

**Output pro Run:** Eine fertige MP4-Datei (1080×1920, 30fps) + Thumbnail-PNG.

---

## 2. Tech-Stack

| Layer | Tool |
|---|---|
| Orchestration | Python 3.11+, FastAPI optional |
| LLM-Brain | Claude API (Anthropic SDK), Claude Code in Antigravity |
| Voice | ElevenLabs API (Voice "Ela – Empathetic & Warm") |
| Avatar-Video | HeyGen API |
| Animation-Generation | Claude Code → HTML → Puppeteer → MP4 |
| Background-Image-Generation | Higgsfield API (Soul 2, Nano Banana Pro) |
| Audio-Processing | ffmpeg, faster-whisper für Captions-Timing |
| Composite | ffmpeg |
| Lead-Magnet-Delivery | ManyChat API |
| Storage | Supabase (Projekt-Setup folgt) |
| Hosting | Lokal Mac mini, später Hetzner |

---

## 3. Stages – High Level

```
INPUT (Topic) 
  → STAGE 1: Skript-Generierung (Claude API)
  → STAGE 2: Voice-Audio (ElevenLabs)
  → STAGE 3: Talking-Head-Video (HeyGen)
  → STAGE 4: HTML-Animationen (Claude Code → MP4)
  → STAGE 5: Composite Split-Screen + Captions (ffmpeg)
  → STAGE 6: Thumbnail (Frame-Extract + Logo-Cards)
  → STAGE 7: Output + ManyChat-Flow (optional Phase 1.5)
OUTPUT (MP4 + Thumbnail + ManyChat-Trigger)
```

Jede Stage hat eine eigene Directive-Datei in `/directives/`. Stages laufen sequenziell, 
schreiben ihren Status in `/runs/{run_id}/state.md` (Self-Annealing).

---

## 4. Verzeichnis-Struktur

```
video_pipeline/
├── CLAUDE.md                          # Diese Datei
├── BRAND_STYLE.md                     # Brand-Guide (Farben, Fonts, Animation-Patterns)
├── PERSONAS.md                        # Sophie, Jonas: HeyGen-IDs, Voice-IDs, Look-Settings
├── directives/
│   ├── 01_script_generation.md
│   ├── 02_voice_audio.md
│   ├── 03_avatar_video.md
│   ├── 04_html_animations.md
│   ├── 05_composite.md
│   ├── 06_thumbnail.md
│   └── 07_manychat.md
├── templates/
│   ├── animations/                    # HTML-Component-Library (Phase 2)
│   ├── thumbnails/                    # Layout-Templates (Phase 2)
│   ├── pdf_lead_magnets/              # PDF-Vorlagen
│   └── manychat_flows/                # ManyChat-Flow-Templates
├── brand_assets/
│   ├── tool_logos/                    # PNG-Logos der Tools (Claude, Higgsfield, etc.)
│   ├── fonts/                         # Inter, Cabinet Grotesk etc.
│   └── persona_references/            # Sophie & Jonas Reference-Images
├── execution/
│   ├── pipeline.py                    # Haupt-Orchestrator
│   ├── stages/                        # Pro Stage eine Python-Datei
│   │   ├── stage_01_script.py
│   │   ├── stage_02_voice.py
│   │   ├── stage_03_heygen.py
│   │   ├── stage_04_animations.py
│   │   ├── stage_05_composite.py
│   │   ├── stage_06_thumbnail.py
│   │   └── stage_07_manychat.py
│   ├── utils/
│   │   ├── ffmpeg_ops.py
│   │   ├── whisper_align.py
│   │   ├── api_clients.py             # Wrapper für HeyGen/ElevenLabs/Higgsfield
│   │   └── state_manager.py           # Self-Annealing State-Updates
│   └── config.py                      # Env-Vars, API-Keys, Constants
├── runs/                              # Pro Video ein Subordner mit allen Assets
│   └── {timestamp}_{slug}/
│       ├── state.md                   # Self-Annealing Live-State
│       ├── script.md
│       ├── audio.mp3
│       ├── avatar_video.mp4
│       ├── animations/
│       │   ├── 01_hook.html
│       │   ├── 01_hook.mp4
│       │   └── ...
│       ├── final.mp4
│       ├── thumbnail.png
│       └── thumbnail_feed.png
└── .env                               # API-Keys (NICHT committen!)
```

---

## 5. Self-Annealing Pattern

Jeder Pipeline-Run erstellt `runs/{run_id}/state.md`. Diese Datei wird von 
JEDER Stage gelesen und nach Abschluss updated. Format:

```markdown
# Run State: {run_id}

## Topic
{Input-Topic vom Mitarbeiter}

## Persona
Sophie | Jonas

## Stage-Status

### Stage 1: Skript-Generierung
- Status: ✅ done / 🔄 in_progress / ❌ failed
- Output: script.md (Pfad)
- Timestamp: {iso}
- Notizen: {was Claude angemerkt hat}

### Stage 2: Voice-Audio
...

### Stage 3: Avatar-Video
...

## Aktive Datei(en)
{Was wird gerade bearbeitet}

## Was nicht funktioniert hat (Don't repeat)
{Liste aller fehlgeschlagenen Ansätze}

## Nächste Schritte
1. ...
2. ...
```

Bei Wiederaufnahme nach `/clear`: state.md zuerst einlesen, von letzter abgeschlossener
Stage fortsetzen.

---

## 6. Globaler Skript-Stil (für Stage 1 + Stage 2)

**Regeln, die in ALLEN Skripts gelten** (Detailregeln in `directives/01_script_generation.md`):

- Volle Artikel ("ein", "einem", "einer") – NIE "n", "nem", "ner"
- Punkte oder Kommas statt Gedankenstriche
- Wort-Endungen können verkürzt werden ("Stundn", "fangn", "machn"), Artikel nicht
- Max 15 Wörter pro Satz, sonst splitten
- 1-3 SCHLÜSSELWÖRTER pro Skript in UPPERCASE für ElevenLabs-Betonung
- Hook-Misconception-Lösung-CTA-Struktur (siehe Directive 01)
- 45-65 Sekunden gesprochene Länge (~120-160 Wörter)
- CTA: "Kommentier [KEYWORD] und ich schick dir [Lead-Magnet]."

---

## 7. ElevenLabs Voice-Settings (Standard)

Für ALLE Skripts in HeyGen über ElevenLabs:

```json
{
  "engine_type": "elevenlabs",
  "model": "eleven_multilingual_v2",
  "similarity_boost": 0.6,
  "stability": 0.5,
  "style": 0.25,
  "use_speaker_boost": true,
  "speed": 1.0
}
```

Abweichungen je nach Energie-Level (siehe directive 02).

---

## 8. Personas

**Sophie** – aktiv ab Start
- HeyGen Avatar Group ID: `300122b0d08d4f8891c695cfb92aacad`
- Default Look ID (AI Video Host): `7755410b9fd54f359ba89a6c5dbc17e8`
- Voice ID (ElevenLabs via HeyGen): `3020b907712a43dbb4a8b186c6144ffd`
- Themen: Strategie, Best Practices, Workflows, KI-Business-Themen, Tool-Reviews

**Jonas** – aktiv ab Phase 3
- Higgsfield Soul: noch nicht trainiert
- HeyGen Avatar: noch nicht angelegt
- Themen: Tech-Tiefe, Code-Tutorials, MCP-Reviews, Builder-Content

Details in `PERSONAS.md`.

---

## 9. Look-Mapping (Sophie → HeyGen-Look)

Pipeline wählt den passenden Look basierend auf Skript-Topic:

| Topic-Kategorie | HeyGen-Look |
|---|---|
| KI/Tool-Review, Tech-News, Software-Vorstellung | "The AI Video Host" |
| Strategie, Insights, Mindset, persönliche Erfahrung | "The Cafe Sipper" |
| Authority-Statements, Hot Takes, Tiefe Analysen | "The Speaker at the Mic" |
| Neutral / sonstiges | "Sophie" (generic) |

---

## 10. Brand-Style (Quick Reference)

**Animationen + Captions:**
- Background: Weiß (`#FFFFFF`)
- Akzent: Orange (`#FF6B35`)
- Text: Schwarz (`#0A0A0A`)
- Stil: Glassmorphism (weiße halbtransparente Cards mit Blur)
- Typo: Inter / Cabinet Grotesk

**Thumbnails:**
- Konsistent mit Animations-Style (Weiß + Glas + Orange)
- Persona-Bild + Logo-Cards in Glas-Style + großes schwarzes Heading + oranger CTA-Bar

Vollständige Details in `BRAND_STYLE.md`.

---

## 11. Pipeline starten

```bash
# Aus dem Projekt-Root:
python execution/pipeline.py --topic "Warum 90% der KI-Implementierungen scheitern" --persona sophie

# Mit zusätzlichem CTA-Keyword:
python execution/pipeline.py --topic "Self-Annealing in Claude Code" --persona sophie --cta-keyword "ANNEAL"

# Resume nach Abbruch:
python execution/pipeline.py --resume {run_id}
```

---

## 12. Phasen-Plan (Was kommt wann)

**Phase 1 (jetzt):** Manuelle Trigger-Pipeline. Du gibst Topic ein, Pipeline läuft End-to-End.
**Phase 2:** Animations-Komponenten-Bibliothek + Word-Level-Captions via Whisper.
**Phase 3:** Influencer-Monitoring (Apify) + automatischer Skript-Trigger + Jonas als 2. Persona.
**Phase 4:** Cloud-Hosting + Cross-Platform-Posting (IG + TikTok + LinkedIn) + Dashboard.

---

## 13. Aktuelle Pipeline-State (wird laufend updated)

**Build-Status:**
- ✅ HeyGen API integriert (manuelle Tests erfolgreich)
- ✅ ElevenLabs Voice "Ela" geklont und in HeyGen verknüpft
- ✅ Skript-Format definiert (UPPERCASE für Betonung, Artikel-Regel)
- ✅ ffmpeg Caption-Burning getestet
- 🔄 HTML-Animations-Library (steht aus)
- 🔄 Composite-Logic 40/60-Split (steht aus)
- 🔄 Thumbnail-Pipeline (steht aus)
- 🔄 ManyChat-Integration (steht aus, Phase 1.5)

**Erste Test-Videos (Referenz für Stil):**
- "Self-Annealing" (Skript-Style-Vorlage)
- "Warum 90% scheitern" (Voice + Lipsync-Baseline, mit Captions als Beispiel)

---

## 14. Wichtige Lessons aus den Tests

- ElevenLabs Multilingual v2 macht zu viele Atempausen bei langen Komma-Sätzen → kurze Sätze, Punkte
- Style-Slider >40% verstärkt Atempausen → Standard 25%
- "n", "nem", "ner" werden komisch ausgesprochen → immer volle Artikel
- Gedankenstriche machen zu lange Pausen → durch Punkte oder Kommas ersetzen
- UPPERCASE-Wörter werden betont → 1-3 pro Skript für Schlüsselwörter
- HeyGen Wan 2.7 hat 15s-Limit, HeyGen Standard nicht (deshalb HeyGen für lange Videos)
- Higgsfield kann CloudFront-Audio-Uploads von Sandbox aus nicht annehmen → Upload erfolgt user-seitig

---

## 15. Self-Annealing-Regel für Claude Code

Bei jeder größeren Aktion in dieser Pipeline:

1. **Lies zuerst** `CLAUDE.md` + ggf. `runs/{current_run}/state.md`
2. **Lies die relevante Directive** in `/directives/`
3. **Update state.md** vor und nach jeder Aktion
4. **Bei Fehlern:** in state.md eintragen, NICHT denselben Ansatz wiederholen
5. **Bei Erfolg:** Versuch + Output in state.md festhalten
6. **Bei `/clear`:** state.md zuerst einlesen, ab letzter erfolgreicher Stage weiter

---

**Letzte Aktualisierung:** {wird automatisch bei jedem Pipeline-Run gesetzt}
