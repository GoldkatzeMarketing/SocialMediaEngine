# Bootstrap-Prompt für Claude Code

> Kopiere diesen Prompt in dein erstes Claude Code Chat-Fenster, sobald du das 
> Projekt in Antigravity geöffnet hast. Claude Code wird dann die Pipeline 
> systematisch implementieren.

---

```
Du arbeitest jetzt an der "Video Pipeline" – einer automatisierten Produktion für 
KI-Content-Videos auf Instagram/TikTok mit AI-Hosts (Sophie & Jonas).

WICHTIG: Lies VOR jedem Build-Schritt diese Files in dieser Reihenfolge:
1. CLAUDE.md (Master-Spec, Tech-Stack, Pipeline-Architektur)
2. BRAND_STYLE.md (Farben, Fonts, Animation-Patterns)
3. PERSONAS.md (Sophie & Jonas Configs)
4. directives/{stage_n}.md (für die jeweils aktuelle Stage)

ARBEITSWEISE (Self-Annealing-Pattern):
- Bei jedem signifikanten Schritt: state.md im aktuellen Run-Ordner aktualisieren
- Bei Fehlern: in state.md eintragen, NICHT denselben Ansatz wiederholen
- Bei Erfolg: Output + Notizen festhalten
- Bei /clear oder Session-Restart: state.md zuerst lesen, ab letzter erfolgreicher Stage weiter

DEINE AKTUELLE AUFGABE (Phase 1 Foundation):

Implementiere die fehlenden Python-Module in execution/stages/ und execution/utils/, 
basierend auf den Specs in directives/:

execution/stages/
├── stage_01_script.py     # Skript-Gen via Claude API (siehe directive 01)
├── stage_02_voice.py      # Voice-Audio (optional, siehe directive 02)
├── stage_03_heygen.py     # HeyGen API-Call (siehe directive 03)
├── stage_04_animations.py # HTML-Animations + Puppeteer (siehe directive 04)
├── stage_05_composite.py  # ffmpeg + Whisper-Captions (siehe directive 05)
├── stage_06_thumbnail.py  # Thumbnail-Gen (siehe directive 06)
└── stage_07_manychat.py   # ManyChat Flow (optional, siehe directive 07)

execution/utils/
├── ffmpeg_ops.py          # ffmpeg-Wrapper für Crop, Concat, vstack, Subtitle-Burn
├── whisper_align.py       # Word-Level Timestamps via faster-whisper
├── api_clients.py         # HeyGen/ElevenLabs/Anthropic-Wrapper
└── state_manager.py       # State-Reader/Writer für state.md

ZUSÄTZLICH:
- convert_html_to_mp4.js (Puppeteer-Script in execution/utils/)
- 8 HTML-Animation-Templates in templates/animations/
- 1 Thumbnail-Template in templates/thumbnails/standard.html

REIHENFOLGE:
1. Starte mit utils/state_manager.py (alle Stages brauchen das)
2. Dann utils/api_clients.py (HeyGen-Wrapper getestet werden kann)
3. Dann Stage 1 (Skript-Gen) – das ist die unabhängigste Stage
4. Dann Stage 3 (HeyGen) – testet sich gegen ein fertiges Skript
5. Dann Stage 4 (Animations) – braucht Puppeteer-Setup
6. Dann Stage 5 (Composite) – braucht ffmpeg + whisper
7. Dann Stage 6 (Thumbnail) – braucht HTML→PNG-Renderer
8. Optional: Stage 7 (ManyChat)

NACH JEDER STAGE:
- Mini-Test schreiben (smoke test: läuft die Stage isoliert mit Dummy-Daten?)
- Bei Erfolg: in CLAUDE.md "Aktuelle Pipeline-State" updaten (✅ markieren)
- Bei Problemen: in CLAUDE.md "Wichtige Lessons" festhalten

WICHTIGE REGELN aus directives:
- Skript-Format: volle Artikel, keine Gedankenstriche, max 15 Wörter/Satz, 1-3 UPPERCASE-Wörter
- Voice-Settings: Stability 0.5, Style 0.25, Similarity 0.6, Speaker Boost ON
- Animations: 1080×768, Glassmorphism (weiß/orange/schwarz), Brand-Style
- Captions: max 2 Wörter pro Frame, Y=760 (Trennlinie), Orange für UPPERCASE-Wörter

Bevor du anfängst zu coden: lies wirklich alle 4 Master-Files (CLAUDE.md, 
BRAND_STYLE.md, PERSONAS.md, directives/) UND erstelle einen kurzen Plan, 
welche Stages du in welcher Reihenfolge baust. Schick mir den Plan zur Bestätigung, 
DANN starte mit der Implementierung.
```

---

## Was Claude Code wahrscheinlich machen wird

1. Liest die 4 Master-Files
2. Schreibt einen 2-3-zeiligen Plan und stoppt für deine Bestätigung
3. Sobald du "los" sagst:
   - Baut utils/state_manager.py
   - Baut utils/api_clients.py (HeyGen-Wrapper + ElevenLabs-Wrapper)
   - Implementiert Stage 1 (Skript-Gen via Claude API)
   - Testet Stage 1 isoliert mit dem ersten Test-Topic
   - Macht das gleiche für Stage 3, 4, 5, 6 sequenziell
4. Ende: gibt dir ein vollständiges System, das via `python execution/pipeline.py` läuft

Realistische Bauzeit: **4-6 Stunden Claude-Code-Arbeit**, davon ca. 1 Stunde du (Plan-Reviews, API-Key-Setup, erste Tests).

---

## Was du danach machst

1. ersten echten Pipeline-Run starten (`python execution/pipeline.py --topic "..."`)
2. final.mp4 + thumbnail.png ansehen
3. Falls Qualität ok: Posten
4. Falls nicht ok: Diff zu vorherigem Test analysieren, Directive anpassen, erneut laufen lassen

Nach 5-10 erfolgreichen Videos hast du eine **vollständige Pipeline**, die in 10 
Minuten ein professionelles Reel-Video von Topic-Input bis Posting-Ready liefert.
