# Directive 06 – Thumbnail-Generation

> **Stage 6** erstellt das Thumbnail-Bild für das Video. Format-konsistent zum 
> Reel-Aspect (1080×1920) sowie eine Feed-Variante (1080×1350).

---

## Input

- `runs/{run_id}/avatar_video.mp4` (für Persona-Frame-Extraktion)
- `runs/{run_id}/script.md` (für Heading + Tool-Logos)
- `brand_assets/tool_logos/*.png`
- `BRAND_STYLE.md`

---

## Process

### Schritt 1: Bestes Persona-Frame extrahieren

```bash
# Verschiedene Frames aus den ersten 8 Sekunden extrahieren
ffmpeg -i avatar_video.mp4 -ss 2 -vf "select='not(mod(n,30))',scale=1080:1920" -vframes 8 candidate_frame_%02d.png
```

Aus den 8 Kandidaten wählt Claude das beste:
- Augen offen, Blick zur Kamera
- Lippen geschlossen oder leicht lächelnd (kein "halb-Wort"-Mund)
- Gesicht im oberen Drittel des Frames (Logo-Cards brauchen Platz oben)

Logik:
```python
import cv2
# Eye detection + mouth-state check per Frame
# Score: eyes_open * face_centered * (1 - mouth_open_ratio)
best_frame = max(candidates, key=score_frame)
```

### Schritt 2: Tool-Logos aus Skript extrahieren

```python
# Aus script.md die `tools_mentioned` Metadata lesen
tools = script_metadata["tools_mentioned"]  # z.B. ["Claude Code", "Higgsfield"]

# Mapping zu Logo-Files
logo_map = {
    "Claude Code": "brand_assets/tool_logos/claude.png",
    "Higgsfield": "brand_assets/tool_logos/higgsfield.png",
    "ChatGPT": "brand_assets/tool_logos/chatgpt.png",
    # ... etc.
}

logo_files = [logo_map[t] for t in tools if t in logo_map][:4]  # max 4 Logos
```

### Schritt 3: Thumbnail-HTML rendern

Template: `templates/thumbnails/standard.html`

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@800;900&display=swap');
    
    body { margin: 0; padding: 0; }
    
    .thumbnail {
      width: 1080px;
      height: 1920px;
      position: relative;
      background: #FFFFFF;
      font-family: 'Inter', sans-serif;
      overflow: hidden;
    }
    
    .thumbnail__bg {
      position: absolute;
      inset: 0;
      background-image: url('{persona_frame}');
      background-size: cover;
      background-position: center top;
      /* Subtle white fade unten für Heading-Lesbarkeit */
      mask-image: linear-gradient(to bottom, black 60%, transparent 95%);
      -webkit-mask-image: linear-gradient(to bottom, black 60%, transparent 95%);
    }
    
    /* Logo-Cards */
    .logo-card {
      position: absolute;
      width: 220px;
      height: 220px;
      background: rgba(255, 255, 255, 0.75);
      backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 255, 255, 0.9);
      border-radius: 28px;
      box-shadow: 
        0 12px 40px rgba(255, 107, 53, 0.25),
        0 4px 16px rgba(0, 0, 0, 0.08);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 32px;
    }
    .logo-card img { max-width: 100%; max-height: 100%; object-fit: contain; }
    
    .logo-card--1 { top: 8%; left: 6%; transform: rotate(-6deg); }
    .logo-card--2 { top: 8%; right: 6%; transform: rotate(6deg); }
    .logo-card--3 { top: 28%; left: 2%; transform: rotate(-3deg); }
    .logo-card--4 { top: 28%; right: 2%; transform: rotate(3deg); }
    
    /* Heading */
    .heading {
      position: absolute;
      bottom: 220px;
      left: 60px;
      right: 60px;
      font-size: 110px;
      font-weight: 900;
      line-height: 0.95;
      letter-spacing: -0.03em;
      color: #0A0A0A;
      text-transform: uppercase;
    }
    
    .sub-cta {
      position: absolute;
      bottom: 140px;
      left: 60px;
      background: #FF6B35;
      color: #FFFFFF;
      font-size: 36px;
      font-weight: 800;
      padding: 16px 32px;
      border-radius: 12px;
      text-transform: uppercase;
      box-shadow: 0 8px 24px rgba(255, 107, 53, 0.4);
    }
  </style>
</head>
<body>
  <div class="thumbnail">
    <div class="thumbnail__bg"></div>
    
    {logo_cards_html}
    
    <h1 class="heading">{heading_text}</h1>
    <div class="sub-cta">{sub_cta_text}</div>
  </div>
</body>
</html>
```

### Schritt 4: HTML → PNG via Puppeteer

```javascript
// execution/utils/html_to_png.js
const puppeteer = require('puppeteer');

async function htmlToPng(htmlPath, outputPath, width=1080, height=1920) {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  await page.setViewport({ width, height });
  await page.goto(`file://${htmlPath}`);
  await page.waitForTimeout(500);
  await page.screenshot({ path: outputPath, type: 'png', omitBackground: false });
  await browser.close();
}
```

### Schritt 5: Feed-Variante (1080×1350)

Aus dem 1080×1920 Thumbnail wird die zentrale 1080×1350-Region gecroppt:

```bash
ffmpeg -i thumbnail.png -vf "crop=1080:1350:0:285" thumbnail_feed.png
```

---

## Heading-Generierung (Claude API)

```python
prompt = f"""
Schreibe einen Thumbnail-Heading für ein Tech-Video.

TOPIC: {topic}
SKRIPT-EXCERPT: {script_first_50_words}

REGELN:
- Max 3 Zeilen, jede max 15 Zeichen breit
- UPPERCASE
- Schwarzes Heading-Wort, dann nichts groß-buchstabieren extra
- Direkter Hook, kein "Wie", lieber "WARUM" oder Statement
- Plus ein 3-6-Wort Sub-CTA in Orange-Bar

Beispiele:
- Heading: "WARUM 90% SCHEITERN" / Sub-CTA: "DIE WAHRHEIT ÜBER KI"
- Heading: "CLAUDE CODE & HIGGSFIELD" / Sub-CTA: "WAS KANN MAN DAMIT MACHEN?"

Output:
{{
  "heading": "...",
  "sub_cta": "..."
}}
"""
```

---

## Output

- `runs/{run_id}/thumbnail.png` (1080×1920, Story/Reel-Format)
- `runs/{run_id}/thumbnail_feed.png` (1080×1350, Feed-Format)

### State-Update

```markdown
### Stage 6: Thumbnail
- Status: ✅ done
- Persona-Frame: aus Sek 4.2 extrahiert
- Logos verwendet: claude.png, higgsfield.png
- Heading: "CLAUDE CODE & HIGGSFIELD"
- Sub-CTA: "WAS KANN MAN DAMIT MACHEN?"
- Output: thumbnail.png + thumbnail_feed.png
```

---

## Validation

- [ ] Thumbnail 1080×1920 erstellt
- [ ] Feed-Variante 1080×1350 erstellt
- [ ] Persona im oberen Drittel sichtbar
- [ ] 2-4 Logo-Cards gerendert ohne Überschneidung
- [ ] Heading max 3 Zeilen, lesbar
- [ ] Orange CTA-Bar vorhanden
- [ ] Alle Farben innerhalb der Brand-Palette
