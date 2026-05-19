# Video Pipeline – Setup & Quick Start

> Automatisierte AI-Video-Produktion mit Sophie & Jonas als Hosts.

---

## Was diese Pipeline tut

Du gibst einen Topic ein. Pipeline liefert:

- ✅ Fertiges Reel-Video (1080×1920, 9:16, mit Captions, Animationen, Avatar)
- ✅ Thumbnail-Bild (Story-Format + Feed-Format)
- ✅ ManyChat-Flow für Comment-to-DM (optional)

**Zeitaufwand:** 5-10 Minuten Rechenzeit. Du bist nur 30 Sekunden involviert (Topic-Input + finaler Approve).

---

## Setup (einmalig, ~30 Min)

### 1. Python-Environment

```bash
cd ~/projects/video_pipeline
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Node.js Dependencies (für Puppeteer)

```bash
npm install puppeteer
```

### 3. ffmpeg installieren (falls noch nicht da)

```bash
brew install ffmpeg
```

### 4. Whisper für Captions

```bash
pip install faster-whisper
```

### 5. API Keys

Erstelle eine `.env`-Datei im Projekt-Root:

```env
ANTHROPIC_API_KEY=sk-ant-...
HEYGEN_API_KEY=...
ELEVENLABS_API_KEY=...
# Optional
HIGGSFIELD_API_KEY=...
MANYCHAT_API_KEY=...
```

API-Keys bekommst du in den jeweiligen Account-Settings.

### 6. Brand-Assets vorbereiten

Lade Tool-Logos in `brand_assets/tool_logos/`:
- claude.png
- higgsfield.png
- chatgpt.png
- heygen.png
- elevenlabs.png
- ... (siehe BRAND_STYLE.md für komplette Liste)

Alle PNGs mit Transparenz, mindestens 512×512px.

### 7. Persona-Reference-Bilder

In `brand_assets/persona_references/`:
- sophie_master.png (das Higgsfield-Master-Bild von Sophie)

### 8. Config validieren

```bash
python execution/config.py
```

Sollte ausgeben: `✅ Config OK`

---

## Erstes Video erstellen

### Befehl

```bash
python execution/pipeline.py \
  --topic "Warum 90% der KI-Implementierungen scheitern" \
  --persona sophie \
  --cta-keyword "KICHECK" \
  --lead-magnet "Checkliste mit 5 Fragen vor jeder KI-Implementierung"
```

### Was passiert

```
🚀 New run: 20260520_143022_warum_90_der_ki_imple...

📋 Stages to run: ['stage_01', 'stage_03', 'stage_04', 'stage_05', 'stage_06']

🤖 Stage 1: Generating script via Claude API...
✅ Stage 1 done: 134 words, ~52s

🎥 Stage 3: Rendering avatar video via HeyGen...
✅ Stage 3 done: HeyGen video rendered

🎨 Stage 4: Generating HTML animations...
✅ Stage 4 done: 5 animations created

🎬 Stage 5: Composite + captions...
✅ Stage 5 done: final.mp4 created

🖼️  Stage 6: Generating thumbnails...
✅ Stage 6 done: thumbnails created

──────────────────────────────────────────────────
✨ Pipeline complete: 20260520_143022_warum_90_der_ki_imple...
📁 Run-Ordner: runs/20260520_143022_warum_90_der_ki_imple
🎬 Final Video: runs/20260520_143022_.../final.mp4
🖼️  Thumbnail (Story): runs/20260520_143022_.../thumbnail.png
🖼️  Thumbnail (Feed): runs/20260520_143022_.../thumbnail_feed.png
──────────────────────────────────────────────────
```

---

## Pipeline-Resume nach Abbruch

Falls die Pipeline mittendrin abbricht (z.B. HeyGen-Timeout):

```bash
python execution/pipeline.py --resume 20260520_143022_warum_90_der_ki_imple
```

Pipeline liest `state.md`, ermittelt die letzte erfolgreiche Stage und macht ab dort weiter.

---

## Mit ManyChat (Phase 1.5)

Wenn ManyChat-Setup fertig ist:

```bash
python execution/pipeline.py \
  --topic "..." \
  --cta-keyword "KICHECK" \
  --with-manychat
```

Dann wird auch Stage 7 ausgeführt und ein Flow für das Keyword in deinem ManyChat-Account angelegt.

---

## Output verifizieren

Bevor du das Video postest, **immer** manuell prüfen:

1. **Final Video angucken** (`final.mp4`):
   - Lipsync ok?
   - Captions korrekt und gut lesbar?
   - Animationen passen zum Skript?
   - Audio-Qualität ok?

2. **Thumbnail prüfen** (`thumbnail.png`):
   - Logos korrekt erkannt?
   - Heading aussagekräftig?
   - Sophie im Bild gut sichtbar?

3. **Skript-Review** (`script.md`):
   - Macht inhaltlich Sinn?
   - Keine Halluzinationen?

Falls etwas nicht passt: Pipeline mit angepasstem Input neu starten oder einzelne Stages manuell tweaken.

---

## Phase-Plan

Aktuell **Phase 1**: Manuelle Trigger, basale Pipeline.

Phase 2 (~1 Woche): 
- Animations-Komponenten-Bibliothek vervollständigen
- Word-Level-Captions vs. Phrase-Captions
- Look-Library erweitern

Phase 3 (~1 Woche):
- Jonas als 2. Persona einbauen
- Influencer-Monitoring via Apify

Phase 4 (~1 Woche):
- Cloud-Hosting (Railway/Hetzner)
- Cross-Platform-Posting
- Dashboard für Review-Approval

---

## Troubleshooting

### Pipeline bricht in Stage 3 ab mit HeyGen-Timeout
- HeyGen API ist manchmal langsam. `--resume` nutzen, läuft normal weiter.

### ElevenLabs-Voice klingt komisch
- Settings in `PERSONAS.md` prüfen
- Style-Slider auf 0.25, Stability 0.5
- Skript auf "n"/"nem"/"ner" prüfen – wenn vorhanden, ist Stage 1 falsch gelaufen

### Animations laden nicht / Puppeteer-Fehler
- `npx puppeteer browsers install chrome` ausführen
- macOS: ggf. Headless-Berechtigungen in Security-Settings prüfen

### Captions sind falsch positioniert
- `BRAND_STYLE.md` → `CAPTION_Y_POSITION` anpassen
- Standard ist Y=760 (Trennlinie zwischen oben 40% und unten 60%)

---

## Architektur-Diagramm

```
┌─────────────────────────────────────────────────────────────────┐
│                   PIPELINE ORCHESTRATOR                          │
│                   (execution/pipeline.py)                        │
└──────────────────────────┬──────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┬─────────────────┐
        ▼                  ▼                  ▼                 ▼
   Stage 1            Stage 3             Stage 4         Stage 5/6
   Script-Gen         HeyGen              Animations      Composite + Thumb
   (Claude API)       (HeyGen API)        (Claude Code)   (ffmpeg)
        │                  │                  │                 │
        ▼                  ▼                  ▼                 ▼
   script.md          avatar_video.mp4   animations/*.mp4   final.mp4 + thumb.png
```

---

## Wichtige Files

| Datei | Zweck |
|---|---|
| `CLAUDE.md` | Master-Doku, von Claude Code als Kontext genutzt |
| `BRAND_STYLE.md` | Farben, Fonts, Animation-Patterns |
| `PERSONAS.md` | Sophie/Jonas Configs |
| `directives/01-07_*.md` | Detaillierte Stage-Anweisungen |
| `execution/pipeline.py` | Haupt-Orchestrator |
| `execution/config.py` | API-Keys, Konstanten |
| `runs/{id}/state.md` | Live-State pro Run (Self-Annealing) |

---

## Erste Schritte für Claude Code

Wenn du Claude Code im Projekt-Root öffnest, sag ihm:

> "Lies CLAUDE.md, BRAND_STYLE.md und PERSONAS.md. Implementiere danach die fehlenden 
> Stage-Module in execution/stages/ und execution/utils/, basierend auf den Specs in 
> directives/. Halte dich strikt an die Skript-Regeln in directive 01 und die 
> Brand-Style-Vorgaben."

Claude Code arbeitet sich dann durch die Stages, baut die Python-Module, testet sie 
einzeln und aktualisiert state.md (Self-Annealing).

---

**Letzte Aktualisierung der README:** Pipeline v1.0, Phase 1 Foundation
