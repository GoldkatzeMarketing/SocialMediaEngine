# Directive 05 – Composite Split-Screen + Captions

> **Stage 5** kombiniert die HTML-Animationen (Top-Half, 40%) mit dem Avatar-Video 
> (Bottom-Half, 60%) und fügt Word-Level-Captions auf der Trennlinie ein.

---

## Input

- `runs/{run_id}/avatar_video.mp4` (1080×1920, ~30fps, mit Audio)
- `runs/{run_id}/animations/*.mp4` (jeweils 1080×768, ohne Audio)
- `runs/{run_id}/animations/animations_meta.json` (Timing)
- `runs/{run_id}/script.md` (für Caption-Text + Keywords)

---

## Aufbau des Final-Videos

```
1080×1920 Frame
├── 0-768px (40% obere Hälfte): Animations-Track
├── 768px (Trennlinie): Caption-Bar
└── 768-1920px (60% untere Hälfte): Avatar-Track (gecroppt vom Original-Avatar-Video)
```

Audio kommt vom Avatar-Video (Sophie spricht).

---

## Process

### Schritt 1: Animations-Track erstellen

Die 5 einzelnen Animations-MP4s müssen zu **einer Animations-Spur** zusammengefügt 
werden, exakt mit dem Timing aus `animations_meta.json`.

```bash
# Concat der einzelnen Animationen
ffmpeg \
  -i 01_hook.mp4 \
  -i 02_problem.mp4 \
  -i 03_misconception.mp4 \
  -i 04_loesung.mp4 \
  -i 05_cta.mp4 \
  -filter_complex \
    "[0:v][1:v][2:v][3:v][4:v]concat=n=5:v=1:a=0[outv]" \
  -map "[outv]" \
  -c:v libx264 -crf 18 \
  animations_track.mp4
```

### Schritt 2: Avatar-Track croppen

Vom 1080×1920 Avatar-Video die **untere 60%** = 1080×1152 px croppen.

```bash
ffmpeg -i avatar_video.mp4 \
  -filter:v "crop=1080:1152:0:768" \
  -c:a copy \
  avatar_cropped.mp4
```

### Schritt 3: Vertikal stacken

```bash
ffmpeg \
  -i animations_track.mp4 \
  -i avatar_cropped.mp4 \
  -filter_complex \
    "[0:v]scale=1080:768[top];\
     [1:v]scale=1080:1152[bottom];\
     [top][bottom]vstack=inputs=2[v]" \
  -map "[v]" -map 1:a \
  -c:v libx264 -crf 18 \
  -c:a copy \
  composite_no_captions.mp4
```

### Schritt 4: Word-Level Captions via Whisper

#### 4a: Whisper auf Avatar-Audio

```python
from faster_whisper import WhisperModel

model = WhisperModel("medium", device="cpu", compute_type="int8")
segments, info = model.transcribe(
    "avatar_video.mp4",  # Whisper kann direkt von MP4 lesen
    language="de",
    word_timestamps=True
)

# Output: pro Wort: {word, start, end}
words = []
for segment in segments:
    for w in segment.words:
        words.append({
            "word": w.word.strip(),
            "start": w.start,
            "end": w.end
        })
```

#### 4b: 2-Wort-Gruppierung

Captions werden in **maximal 2 Wörter pro Frame** gruppiert. Schlüsselwörter 
(UPPERCASE aus Skript) bleiben in Orange.

```python
def group_words_for_captions(words, max_words=2):
    captions = []
    i = 0
    while i < len(words):
        group = words[i:i + max_words]
        if not group:
            break
        text = " ".join(w["word"] for w in group)
        captions.append({
            "text": text,
            "start": group[0]["start"],
            "end": group[-1]["end"]
        })
        i += max_words
    return captions
```

#### 4c: ASS-Subtitle-File generieren (für komplexere Styling-Optionen als SRT)

```python
def make_ass_file(captions, keywords_orange, output_path):
    """
    keywords_orange: Liste der UPPERCASE-Schlüsselwörter aus Skript
                    – werden in Orange dargestellt
    """
    ass_header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, BorderStyle, Outline, Shadow, Alignment, MarginV, Encoding
Style: Default,Inter,56,&H000A0A0A,&HFFFFFFFF,&HFFFFFFFF,1,1,3,0,2,760,1
Style: Orange,Inter,56,&H000A6BFF,&HFFFFFFFF,&HFFFFFFFF,1,1,3,0,2,760,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    for cap in captions:
        text = cap["text"]
        # Prüfen ob ein Wort orange sein soll
        words = text.split()
        styled_parts = []
        for word in words:
            clean = word.strip(".,!?").upper()
            if clean in keywords_orange:
                styled_parts.append(f"{{\\c&H000A6BFF&}}{word}{{\\c&H000A0A0A&}}")
            else:
                styled_parts.append(word)
        styled_text = " ".join(styled_parts)
        
        start_ass = format_ass_time(cap["start"])
        end_ass = format_ass_time(cap["end"])
        events.append(f"Dialogue: 0,{start_ass},{end_ass},Default,,0,0,760,,{styled_text}")
    
    with open(output_path, 'w') as f:
        f.write(ass_header + "\n".join(events))

def format_ass_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"
```

**MarginV: 760** positioniert die Captions auf Y=760, direkt auf der Trennlinie 
zwischen oberer (768px) und unterer Hälfte. Anpassbar in BRAND_STYLE.md.

#### 4d: ASS in Video burnen

```bash
ffmpeg -i composite_no_captions.mp4 \
  -vf "ass=captions.ass" \
  -c:a copy \
  final.mp4
```

---

## Caption-Style (Brand-konform)

**Phase 1 (jetzt):** Caption-Text auf weißem Glas-Background. Realisierung über 
ASS + Box-Background:

```
Style: Default,Inter,56,&H000A0A0A,&HFFFFFFFF,&H80FFFFFF,1,3,3,0,2,760,1
                                              ^^^^^^^^^^ 
                                              Background mit Alpha
                                                ^^^^^^^^^
                                                BackColour
```

**Phase 2:** Glas-Background als separates Overlay (PNG mit Backdrop-Blur-Look), wird 
unter der Caption-Schicht eingeblendet während Captions aktiv sind. Realismus statt 
flachem Background.

---

## Output

- `runs/{run_id}/final.mp4` – das fertige Reel, 1080×1920, 30fps, mit Audio + Captions
- Größe: ~30-50 MB für 60s

### State-Update

```markdown
### Stage 5: Composite + Captions
- Status: ✅ done
- Composite-Methode: vstack + ass-subtitle-burn
- Captions: 27 Frames, Wort-Level via Whisper
- Output: final.mp4
- Größe: 42 MB
- Render-Zeit: 1m 15s
```

---

## Validation

- [ ] Finale Auflösung: 1080×1920
- [ ] Audio-Spur vom Avatar-Video erhalten
- [ ] Animations + Avatar synchron (kein Drift > 0.1s)
- [ ] Captions sichtbar, lesbar, korrekte Position
- [ ] UPPERCASE-Wörter in Orange
- [ ] Dauer entspricht ±0.5s der Skript-Sprechdauer
