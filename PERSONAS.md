# PERSONAS.md – Host-Definitionen

> Konfiguration aller AI-Hosts. Pipeline liest diese Datei für HeyGen-IDs,
> Voice-Settings und Look-Mappings.

---

## Sophie

**Status:** ✅ Aktiv

### Identität
- **Name:** Sophie
- **Persönlichkeit:** Strategin, smart, südländische Eleganz, kompetent-warmer Vibe
- **Alter (visuell):** Anfang 30
- **Brand-Position:** Strategie, Best Practices, Tool-Reviews aus Business-Sicht, KI für Entscheider

### HeyGen-Konfiguration
- **Avatar Group ID:** `300122b0d08d4f8891c695cfb92aacad`
- **Default Look ID:** `7755410b9fd54f359ba89a6c5dbc17e8` ("The AI Video Host")
- **Voice ID (ElevenLabs-Bridge):** `3020b907712a43dbb4a8b186c6144ffd`

### Voice-Settings (ElevenLabs "Ela – Empathetic & Warm")
- Model: `eleven_multilingual_v2`
- Similarity Boost: `0.6`
- Stability: `0.5`
- Style: `0.25` (Default, kann je nach Skript bis 0.45 hochgesetzt werden)
- Speaker Boost: `true`
- Speed: `1.0`

### Look-Mapping (Topic → HeyGen-Look)
| Skript-Kategorie | Look-Name | Look-ID |
|---|---|---|
| Tool-Review, KI-News, Software | The AI Video Host | `7755410b9fd54f359ba89a6c5dbc17e8` |
| Strategie, Insight, persönlich | The Cafe Sipper | _(via API ermitteln)_ |
| Authority, Hot Take | The Speaker at the Mic | _(via API ermitteln)_ |
| Neutral / Fallback | Sophie (generic) | _(via API ermitteln)_ |

### Higgsfield Soul Character (für Thumbnails + Animation-Hooks falls nötig)
- Soul ID: noch nicht trainiert
- Reference Image: in `brand_assets/persona_references/sophie_master.png`

### Themen-Fit
✅ KI-Tools, Workflow-Automation, Business-Strategie, Builder-Insights, Tool-Vergleiche, 
   Trends, Lead-Generation-Best-Practices
❌ Hardcore-Code-Tutorials, Deep-Tech-Demos (das ist Jonas-Territorium)

### Skript-Ton
- Direkt, smart, "Geschäftsführerin-Energie"
- Wenig Filler, viele konkrete Beispiele
- "Wir sehen bei Kunden", "Erfolgreiche Implementierungen"
- Soft Authority, kein Hype

---

## Jonas

**Status:** ⏸ Geplant (Phase 3)

### Identität
- **Name:** Jonas
- **Persönlichkeit:** Nerdy Builder, authentisch, "Coder, dem du glaubst"
- **Alter (visuell):** Ende 20
- **Brand-Position:** Tech-Tiefe, Code-Tutorials, MCP-Reviews, Tool-Demos

### Visuelle Signature-Elemente
- Beanie (dunkel olive-grau)
- Statement-Brille (dicker schwarzer Acetatrahmen, oversized rectangular)
- Dunkler Hoodie
- Setting: Home-Office mit Code-Monitor, Bücherregal, Pflanzen

### HeyGen-Konfiguration
- **Avatar Group ID:** _(folgt)_
- **Looks:** _(folgt)_
- **Voice ID:** _(folgt – männliche deutsche ElevenLabs-Voice)_

### Voice-Settings (ElevenLabs)
- Model: `eleven_multilingual_v2`
- Voice: _(noch auszuwählen, gerne tief-warm-nerdy)_
- Similarity Boost: `0.6`
- Stability: `0.5`
- Style: `0.3` (etwas energetischer als Sophie für Tech-Content)
- Speaker Boost: `true`

### Themen-Fit
✅ Claude Code, MCPs, Agentic Workflows, Tool-Setups, Tech-Tutorials, Build-in-Public
❌ High-Level-Strategie, B2B-Lead-Generation-Talks (das ist Sophie-Territorium)

### Skript-Ton
- Enthusiastisch aber nicht überdreht
- Tech-Slang erlaubt ("der Endpoint", "MCP-Server", "API-Key")
- "Ich hab das mal getestet", "Schau dir das an"
- Builder-Authentizität

---

## Cross-Persona-Themen

Manche Themen können beide machen (z.B. "Higgsfield Photo Avatar Pipeline"). Default-Regel:
- Wenn Topic Code/Tool-Demo enthält → Jonas
- Wenn Topic Business-Value/ROI/Strategie enthält → Sophie
- Bei Doppel-Themen: 50/50 alternieren, damit beide Personas Reichweite bekommen
