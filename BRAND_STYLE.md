# BRAND_STYLE.md – Visual Identity Guide

> Single Source of Truth für Farben, Typografie, Animation-Patterns,
> Caption-Style und Thumbnail-Look.

---

## 1. Farb-Palette

```css
:root {
  /* Backgrounds */
  --bg-base: #FFFFFF;
  --bg-off-white: #FAFAF9;
  --bg-soft-grey: #F5F5F4;

  /* Akzent (Brand) */
  --accent: #FF6B35;
  --accent-light: #FF8A5C;
  --accent-dark: #E55A2B;
  --accent-soft: #FFF1EC;   /* Hintergrund-Tint, sehr dezent */

  /* Text */
  --text-primary: #0A0A0A;
  --text-secondary: #525252;
  --text-tertiary: #A3A3A3;

  /* Borders & Shadows */
  --border-subtle: rgba(0, 0, 0, 0.06);
  --border-glass: rgba(255, 255, 255, 0.8);
  --shadow-glass: 0 8px 32px rgba(0, 0, 0, 0.08);
  --shadow-elevated: 0 16px 48px rgba(0, 0, 0, 0.12);
}
```

---

## 2. Typografie

**Primary Display Font:** Inter (oder Cabinet Grotesk falls verfügbar)
**Fallback:** -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif

**Größen-Skala für Animation-Videos (1080×768 obere Hälfte):**

| Element | Größe | Weight | Letter-Spacing |
|---|---|---|---|
| Mega-Headline | 96-120px | 900 (Black) | -0.03em |
| Headline | 64-80px | 800 (ExtraBold) | -0.02em |
| Subheadline | 40-48px | 700 (Bold) | -0.01em |
| Body | 28-32px | 500 (Medium) | 0 |
| Caption | 22-24px | 600 (SemiBold) | 0 |
| Label | 18-20px | 600 (SemiBold) | 0.02em |

**Größen-Skala für Captions auf Video-Kante:**
- Schriftgröße: 56-64px
- Weight: 800 (ExtraBold)
- Letter-Spacing: -0.01em
- Maximal **2 Wörter pro Frame**

---

## 3. Glassmorphism-Komponente

### CSS-Snippet (Basis)

```css
.glass-card {
  background: rgba(255, 255, 255, 0.65);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.8);
  border-radius: 24px;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.9);
  padding: 32px 40px;
}

/* Orange-Akzent-Version (für CTAs, Highlights) */
.glass-card--accent {
  background: rgba(255, 107, 53, 0.12);
  border: 1px solid rgba(255, 107, 53, 0.3);
}

/* Dark-Glas (selten, für Kontrast) */
.glass-card--dark {
  background: rgba(10, 10, 10, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: white;
}
```

### Glass-Card-Varianten

- **Standard (weiß-transparent):** Default für alle Content-Cards
- **Accent (orange-tint):** Für Highlights, Quotes, betonte Aussagen
- **Dark:** Sehr selten, nur wenn ein Kontrast nötig ist (z.B. Code-Snippet-Display)

---

## 4. Animations-Patterns

### Standard-Animationen (max 5 pro Top-Half-Video)

**Pattern A: "Card Slide-In"**
- Glass-Card slidet von rechts/links/unten ins Frame
- Dauer: 400ms ease-out
- Subtle scale von 0.95 → 1.0 für Lebendigkeit

**Pattern B: "Number Counter"**
- Große schwarze Zahl, läuft von 0 hoch zum Zielwert
- Orange Glow-Pulse bei Erreichen
- Dauer: 800ms

**Pattern C: "Text Reveal (Word-by-Word)"**
- Wörter erscheinen sequenziell mit subtle fade + slight Y-translation
- 80-120ms delay zwischen Wörtern
- Keywords in Orange, Rest in Schwarz

**Pattern D: "Glass-Stack"**
- 2-3 Glass-Cards stacken übereinander mit leichtem Tilt
- Tool-Logos oder Argumente
- Hover/Cycle: Cards rotieren sanft

**Pattern E: "Highlight-Pulse"**
- Schlüsselwort wird mit Orange-Underline/Background hervorgehoben
- Subtle pulse-animation
- Genau auf dem Moment, wo Sophie das Wort spricht

### Generelle Animations-Regeln

- **Easing:** Immer `cubic-bezier(0.16, 1, 0.3, 1)` (sanft, organisch)
- **Background:** Immer leicht bewegt (langsamer Gradient-Shift oder dezenter Noise)
- **NIE:** harte Cuts, hektische Bewegungen, blinkende Elemente
- **Dauer pro Animation:** 2-6 Sekunden, passend zum Skript-Beat

---

## 5. Caption-Style (auf Video-Kante)

Position: Genau auf der Trennlinie zwischen oberer (40%) und unterer (60%) Bildhälfte, 
also bei Y-Pixel 768 von 1920 Gesamthöhe.

```css
.caption {
  position: absolute;
  bottom: 1152px;  /* = obere Hälfte */
  left: 50%;
  transform: translateX(-50%);
  
  /* Glassmorphism-Hintergrund für Caption */
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  padding: 12px 24px;
  
  /* Text */
  color: #0A0A0A;
  font-family: 'Inter', sans-serif;
  font-weight: 800;
  font-size: 56px;
  letter-spacing: -0.01em;
  text-transform: uppercase;
  white-space: nowrap;
  
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.caption .keyword {
  color: #FF6B35;
}
```

**Caption-Regeln:**
- Maximal **2 Wörter pro Frame**
- Schlüsselwörter (die in Skript UPPERCASE waren) in Orange
- Position fest auf Y=1152 (untere Kante der oberen 40%-Hälfte)
- Sanftes Fade-In (150ms), kein hartes Pop

---

## 6. Thumbnail-Style

### Layout-Specs (1080×1920 Story-Format, 1080×1350 Feed-Format)

```
┌─────────────────────────────────────┐
│                                     │  Oberer Bereich:
│   [Glas-Logo-Card]   [Glas-Logo-    │  - Persona-Bild als Background
│         ◊ 2-3 Cards mit Tools ◊     │  - 3-4 Glas-Logo-Cards um Kopf
│   [Glas-Logo-Card]   [Glas-Logo-    │  - Orange-Glow um Logo-Cards
│                                     │
│        ┌────────────────┐           │
│        │                │           │
│        │   PERSONA      │           │  Mittlerer Bereich:
│        │   IM SETTING   │           │  - Sophie/Jonas
│        │                │           │  - Frame aus Video
│        └────────────────┘           │
│                                     │
│   ┌──────────────────────────────┐  │
│   │  CLAUDE CODE & HIGGSFIELD    │  │  Unterer Bereich:
│   │                              │  │  - Großes schwarzes Heading
│   └──────────────────────────────┘  │  - Orange Sub-CTA-Bar
│   ┌──────────────────────────────┐  │
│   │  WAS KANN MAN DAMIT MACHEN?  │  │
│   └──────────────────────────────┘  │
└─────────────────────────────────────┘
```

### Thumbnail-CSS

```css
.thumbnail {
  width: 1080px;
  height: 1920px;
  position: relative;
  background: #FFFFFF;
  font-family: 'Inter', sans-serif;
  overflow: hidden;
}

.thumbnail__background {
  /* Persona-Bild als Background, etwas verblurrt oder gut sichtbar */
  position: absolute;
  inset: 0;
  background-image: url('persona_frame.png');
  background-size: cover;
  background-position: center;
}

.thumbnail__logo-card {
  position: absolute;
  width: 220px;
  height: 220px;
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.9);
  border-radius: 28px;
  box-shadow: 
    0 12px 40px rgba(255, 107, 53, 0.25),  /* Orange-Glow */
    0 4px 16px rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 32px;
}

.thumbnail__logo-card img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

/* Verschiedene Positionen für 3-4 Cards um den Kopf */
.thumbnail__logo-card--tl { top: 8%; left: 8%; transform: rotate(-6deg); }
.thumbnail__logo-card--tr { top: 8%; right: 8%; transform: rotate(6deg); }
.thumbnail__logo-card--ml { top: 28%; left: 4%; transform: rotate(-3deg); }
.thumbnail__logo-card--mr { top: 28%; right: 4%; transform: rotate(3deg); }

.thumbnail__heading {
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
  text-shadow: 0 2px 8px rgba(255, 255, 255, 0.8);
}

.thumbnail__sub-cta {
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
  letter-spacing: 0.01em;
  box-shadow: 0 8px 24px rgba(255, 107, 53, 0.4);
}
```

### Thumbnail-Logik in der Pipeline

1. **Persona-Frame:** Aus dem fertigen HeyGen-Video das beste Frame extrahieren (Sek 2-5)
2. **Tool-Logos identifizieren:** Claude API liest Skript, extrahiert genannte Tools
3. **Logo-Cards rendern:** 3-4 Glas-Cards mit den passenden Logos
4. **Heading & Sub-CTA:** Claude API generiert kurze 2-3-Wort-Heading + 4-6-Wort-Sub-Frage
5. **Composite via Python PIL oder HTML-zu-PNG via Puppeteer**

---

## 7. Logo-Library

**Standard-Tools (in `brand_assets/tool_logos/`):**

| Tool | Filename | Hinweis |
|---|---|---|
| Claude / Anthropic | `claude.png` | Asterisk-Logo + Wordmark |
| ChatGPT / OpenAI | `chatgpt.png` | Spirale |
| Higgsfield | `higgsfield.png` | H-Logo |
| HeyGen | `heygen.png` | |
| ElevenLabs | `elevenlabs.png` | |
| n8n | `n8n.png` | |
| Zapier | `zapier.png` | |
| Make | `make.png` | |
| Notion | `notion.png` | |
| Linear | `linear.png` | |
| Vercel | `vercel.png` | |
| Supabase | `supabase.png` | |
| GitHub | `github.png` | |
| VS Code | `vscode.png` | |
| Figma | `figma.png` | |
| Midjourney | `midjourney.png` | |
| Cursor | `cursor.png` | |
| Veo / Google AI | `veo.png` | |

**Anforderungen:**
- PNG mit Transparenz
- Mindestens 512×512px
- Quadratisches Aspect Ratio bevorzugt (Square-Cards)
- Falls Logo nicht quadratisch: in 512×512-Canvas zentriert

**Logo-Card-Generation:**
- Logo wird in eine Glas-Card mit Padding 40px gerendert
- Background-Tint dezent transparent
- Subtle Orange-Glow als Shadow

---

## 8. Animation-Templates (für Stage 4)

In `templates/animations/` liegen wiederverwendbare HTML-Komponenten. Pro Skript-Sektion 
wird die passendste gewählt.

**Verfügbare Templates (Phase 2 zu bauen):**

1. `hook_glitch.html` – Code-Editor mit Glitch-Effekt (für Tech-Hook)
2. `hook_counter.html` – Große animierte Zahl mit Orange-Glow (für Statistik-Hook)
3. `problem_stack.html` – Stack aus Glas-Cards mit Pain-Points
4. `comparison_split.html` – Vorher/Nachher als Split-Card
5. `process_flow.html` – Schritt-für-Schritt mit animierten Pfeilen
6. `tool_logos.html` – 2-3 Tool-Logo-Cards mit "+" zwischen ihnen
7. `quote_emphasis.html` – Großes Quote mit Orange-Highlight auf Schlüsselwörtern
8. `cta_keyword.html` – Comment-Bubble mit CTA-Keyword

Pro Skript-Sektion identifiziert Claude die passende Template + befüllt sie mit Content.

---

## 9. Visual-Consistency-Checks

Bevor ein Video ausgeliefert wird, prüft die Pipeline automatisch:

- [ ] Alle Animations-MP4s sind 1080×768 (obere 40%)
- [ ] Avatar-Video ist 1080×1152 (untere 60%)
- [ ] Captions-Position bei Y=1152±10px
- [ ] Verwendete Farben innerhalb der Brand-Palette
- [ ] Thumbnail 1080×1920 (Story) + 1080×1350 (Feed) generiert
- [ ] Logos verwendet sind in `brand_assets/tool_logos/` enthalten

---

**Diese Datei wird durch keinen Pipeline-Run automatisch updated. Änderungen am 
Brand-Style erfordern explizite Editierung.**
