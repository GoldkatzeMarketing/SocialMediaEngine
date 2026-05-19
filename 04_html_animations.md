# Directive 04 – HTML-Animationen (Top-Half)

> **Stage 4** generiert die animierten Visualisierungen für die obere Hälfte des 
> Split-Screen-Videos. Pro Skript 3-5 HTML-Animationen, die zu Brand-Style passen 
> (Weiß + Glas + Orange) und sich mit dem Skript-Timing synchronisieren.

---

## Input

- `script.md` aus Stage 1 (inklusive `animation_sections` Metadata)
- `BRAND_STYLE.md` für CSS-Variablen, Animation-Patterns, Typografie
- (Phase 2): `templates/animations/` mit fertigen Komponenten-Templates

---

## Process

### Schritt 1: Animations-Plan erstellen

Aus den 5 Skript-Sektionen wird pro Sektion **eine Animation** geplant:

| Sektion | Dauer | Template-Vorschlag | Visual-Konzept |
|---|---|---|---|
| 1. Hook | ~5s | `hook_counter` / `hook_glitch` | Zahl/Stat-Reveal oder Pain-Visual |
| 2. Problem | ~15s | `problem_stack` / `comparison_split` | Glas-Cards mit Pain-Points |
| 3. Misconception | ~10s | `quote_emphasis` | "FALSCH"-Reveal mit Orange |
| 4. Lösung | ~20s | `process_flow` / `tool_logos` | Lösungs-Workflow oder Tools |
| 5. CTA | ~5s | `cta_keyword` | Comment-Bubble mit CTA-Keyword |

Stage 1 hat in `animation_sections` bereits Vorschläge gemacht. Diese werden hier 
konkretisiert.

### Schritt 2: HTML-Generierung

Für jede Sektion wird ein HTML-File erstellt:
- Pfad: `runs/{run_id}/animations/{section_id}_{template}.html`
- Format: vollständige HTML-Datei (inline CSS+JS), 1080×768px Canvas
- Dauer: exakt passend zur Skript-Sektion (siehe Tabelle oben)

**Stile-Vorgaben aus BRAND_STYLE.md:**
- Background: weiß `#FFFFFF`
- Akzent: orange `#FF6B35`
- Text: schwarz `#0A0A0A`
- Komponenten: Glassmorphism mit `backdrop-filter: blur(24px)`
- Typo: Inter

### Schritt 3: HTML → MP4 Conversion via Puppeteer

```bash
node convert_html_to_mp4.js {input.html} {output.mp4} {duration_seconds}
```

`convert_html_to_mp4.js` Workflow:
1. Puppeteer startet Headless Chrome mit Viewport 1080×768
2. Lädt HTML-Datei
3. Capturet Frames mit 30fps für `duration_seconds`
4. Frames werden via ffmpeg zu MP4 zusammengefügt (H.264, ohne Audio)

---

## Komponenten-Templates (Phase 2 zu bauen)

In `templates/animations/` liegen 8 Basis-Templates:

### `hook_glitch.html`
- Code-Editor-Mockup mit fließenden Code-Snippets
- Glitch-Effekt nach 3 Sek
- "ERROR"-Overlay mit Glitch-Animation in Orange

### `hook_counter.html`
- Große schwarze Zahl, läuft von 0 auf Zielwert
- Orange-Glow-Pulse bei Erreichen
- Subtle Glass-Card im Hintergrund

### `problem_stack.html`
- 3-4 Glas-Cards stacken sich übereinander
- Pro Card ein Pain-Point als Text
- Sequenzielles Slide-In von rechts

### `comparison_split.html`
- Split-View links/rechts: "Vorher" vs "Nachher"
- Glas-Cards, Orange-Highlight auf dem Pivot

### `process_flow.html`
- 3-5 Schritte als Glas-Cards mit Pfeilen
- Sequenzielles Reveal
- Schlüsselwörter in Orange

### `tool_logos.html`
- 2-3 Tool-Logo-Glas-Cards mit "+" zwischen ihnen
- Logos aus `brand_assets/tool_logos/`
- Subtle Float-Animation

### `quote_emphasis.html`
- Großes Quote mit Orange-Highlight auf 1-2 Wörtern
- Word-by-Word-Reveal

### `cta_keyword.html`
- Comment-Bubble erscheint von unten
- CTA-Keyword in Orange + Bold + großer Font
- Pulsiert subtle

---

## Pro Sektion: Claude-Prompt zur HTML-Generierung

```
Du bist HTML-Animation-Generator für die Video-Pipeline.

INPUT:
- Sektion-Text: "{section_text}"
- Sektion-Dauer: {duration}s
- Suggested Template: {template_name}
- Visual-Konzept: {visual_concept}

OUTPUT: Eine vollständige HTML-Datei mit:
- Viewport 1080×768px
- Inline CSS (Brand-Style: weiß + orange + schwarz, Glassmorphism)
- Inline JS für Animationen (CSS-Animations bevorzugt)
- Keine externen Dependencies außer Google Fonts (Inter)
- Animation soll natürlich looped/enden über exakt {duration}s

WICHTIG:
- Nutze die CSS-Variablen aus BRAND_STYLE.md
- Glass-Cards mit backdrop-filter: blur(24px)
- Sanfte Easings (cubic-bezier(0.16, 1, 0.3, 1))
- Text in Schwarz, Schlüsselwörter in Orange
- Background-Weiß mit subtilem Noise oder Gradient-Shift für Lebendigkeit
- Schriftgrößen aus BRAND_STYLE.md
```

---

## Output

Pro Skript ein Ordner `runs/{run_id}/animations/` mit:
- `01_hook.html` + `01_hook.mp4` (5s)
- `02_problem.html` + `02_problem.mp4` (15s)
- `03_misconception.html` + `03_misconception.mp4` (10s)
- `04_loesung.html` + `04_loesung.mp4` (20s)
- `05_cta.html` + `05_cta.mp4` (5s)

Plus: `animations_meta.json` mit Timing-Info für Stage 5 (Composite):

```json
{
  "segments": [
    {"file": "01_hook.mp4", "start": 0.0, "duration": 5.0},
    {"file": "02_problem.mp4", "start": 5.0, "duration": 15.0},
    {"file": "03_misconception.mp4", "start": 20.0, "duration": 10.0},
    {"file": "04_loesung.mp4", "start": 30.0, "duration": 20.0},
    {"file": "05_cta.mp4", "start": 50.0, "duration": 5.0}
  ],
  "total_duration": 55.0
}
```

---

## Puppeteer-Script (Phase 1 Minimal-Version)

```javascript
// execution/utils/convert_html_to_mp4.js
const puppeteer = require('puppeteer');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

async function convertHtmlToMp4(htmlPath, outputPath, durationSec) {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1080, height: 768 });
  await page.goto(`file://${path.resolve(htmlPath)}`);
  await page.waitForTimeout(500);  // Initial load
  
  const framesDir = '/tmp/frames_' + Date.now();
  fs.mkdirSync(framesDir);
  
  const fps = 30;
  const totalFrames = Math.floor(durationSec * fps);
  
  for (let i = 0; i < totalFrames; i++) {
    await page.screenshot({
      path: `${framesDir}/frame_${String(i).padStart(5, '0')}.png`,
      type: 'png'
    });
    await page.waitForTimeout(1000 / fps);
  }
  
  await browser.close();
  
  // FFmpeg: frames → MP4
  return new Promise((resolve, reject) => {
    const ff = spawn('ffmpeg', [
      '-y',
      '-framerate', String(fps),
      '-i', `${framesDir}/frame_%05d.png`,
      '-c:v', 'libx264',
      '-pix_fmt', 'yuv420p',
      '-crf', '18',
      outputPath
    ]);
    ff.on('close', code => {
      // Cleanup frames
      fs.rmSync(framesDir, { recursive: true });
      code === 0 ? resolve(outputPath) : reject(`ffmpeg exit code ${code}`);
    });
  });
}

// CLI usage
const [,, htmlPath, outputPath, durationStr] = process.argv;
convertHtmlToMp4(htmlPath, outputPath, parseFloat(durationStr))
  .then(p => console.log('Done:', p))
  .catch(e => { console.error(e); process.exit(1); });
```

---

## State-Update

```markdown
### Stage 4: HTML-Animationen
- Status: ✅ done
- Animations erstellt: 5
- Total-Dauer: 55s
- Render-Zeit: 2m 30s
- Output: animations/ (5 MP4s + meta.json)
```
