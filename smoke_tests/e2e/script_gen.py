"""Claude-Skript-Generator. Liest directives/01_script_generation.md fuer die Regeln."""
import os
import re
from pathlib import Path
from anthropic import Anthropic

PROJECT_ROOT = Path(__file__).parent.parent.parent
DIRECTIVE = PROJECT_ROOT / "directives" / "01_script_generation.md"

SYSTEM_PROMPT = """Du bist Skript-Generator für die "Sophie"-Video-Pipeline.

Sophie ist eine KI/Strategie-Persona, die kurze Reels (45-65s, ~120-160 Wörter)
auf Deutsch spricht. Stil: Authority + Klarheit, du-Form, ohne Hype-Sprache.

Du bekommst als Inspiration das TRANSKRIPT eines fremden Reels.
Du schreibst KEIN Copy-Paste, sondern Sophies eigene Sicht auf das Thema:
gleiche Domäne, Sophies Framing, ihre Beispiele.

KRITISCHE SPRACH-REGELN (für ElevenLabs-TTS):
- Volle Artikel: "ein", "einem", "einer" – NIE "n", "nem", "ner"
- Keine Gedankenstriche, stattdessen Punkte oder Kommas
- Wort-Endungen dürfen verkürzt werden ("Stundn", "fangn", "machn", "Firmn")
- Max 15 Wörter pro Satz, sonst splitten
- 1-3 SCHLÜSSELWÖRTER pro Skript in UPPERCASE für Betonung
- CTA-Keyword IMMER in UPPERCASE
- Keine Hype-Wörter ("revolutionär", "game-changing", "insane")

STRUKTUR (5 Sektionen):
1. Hook (0-5s): Pain-Point oder Reveal
2. Problem (5-20s): warum es existiert, mit Beispiel oder Metapher
3. Misconception (20-30s): was die meisten falsch machen
4. Lösung (30-50s): konkrete Antwort
5. CTA (50-55s): "Kommentier {KEYWORD} und ich schick dir {Lead-Magnet}"

OUTPUT-FORMAT: Pures Markdown nach dem Template unten. Keine Erklärungen davor/danach.
"""

OUTPUT_TEMPLATE = """# Skript: {topic}

**Persona:** sophie
**CTA-Keyword:** {cta_keyword}
**Lead-Magnet:** {lead_magnet}
**Voraussichtliche Sprechdauer:** ~55 Sek

## Sektion 1 – Hook
{...}

## Sektion 2 – Problem
{...}

## Sektion 3 – Misconception
{...}

## Sektion 4 – Lösung
{...}

## Sektion 5 – CTA
Kommentier {CTA_KEYWORD} und ich schick dir {...}.

## Voll-Skript
{Alle 5 Sektionen als ein fliessender Block fuer HeyGen}

## Metadata
- uppercase_words: [WORT1, WORT2, CTA_KEYWORD]
- thumbnail_heading: "..."
"""


def generate_script(inspiration_transcript: str, source_caption: str = "") -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError("ANTHROPIC_API_KEY missing in .env")

    client = Anthropic(api_key=api_key)

    user_msg = f"""Hier ist ein Reel-Transkript eines anderen Creators als Inspiration:

TRANSKRIPT:
\"\"\"
{inspiration_transcript}
\"\"\"

CAPTION (falls hilfreich):
\"\"\"
{source_caption}
\"\"\"

Aufgaben:
1. Extrahiere das Kern-Thema (1 Satz).
2. Schreibe Sophies eigenes 55-Sek-Skript zum gleichen Thema, Sophie-Stil.
3. Wähle ein CTA-Keyword (1 Wort, UPPERCASE, themen-passend).
4. Schlage einen Lead-Magnet vor (1 Satz Beschreibung).

OUTPUT exakt in diesem Markdown-Format:

```
# Skript: <Topic-Satz>

**Persona:** sophie
**CTA-Keyword:** <KEYWORD>
**Lead-Magnet:** <Beschreibung>
**Voraussichtliche Sprechdauer:** ~55 Sek

## Sektion 1 – Hook (0:00-0:05)
<...>

## Sektion 2 – Problem (0:05-0:20)
<...>

## Sektion 3 – Misconception (0:20-0:30)
<...>

## Sektion 4 – Lösung (0:30-0:50)
<...>

## Sektion 5 – CTA (0:50-0:55)
Kommentier <KEYWORD> und ich schick dir <Lead-Magnet>.

## Voll-Skript
<Alle 5 Sektionen zusammen als 1 Block, fuer HeyGen direkt einsetzbar>

## Metadata
uppercase_words: [WORT1, WORT2, KEYWORD]
thumbnail_heading: "<...>"
```
"""

    resp = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=2500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_msg}],
    )
    return resp.content[0].text.strip()


def extract_voll_skript(markdown: str) -> str:
    """Holt den Voll-Skript-Block fuer HeyGen-Input."""
    m = re.search(r"## Voll-Skript\s*\n+(.+?)(?=\n##|\Z)", markdown, re.DOTALL)
    if not m:
        raise ValueError("Voll-Skript section not found in generated script")
    return m.group(1).strip()


def extract_uppercase_keywords(markdown: str) -> list[str]:
    """Holt UPPERCASE-Woerter aus Metadata fuer Caption-Highlight."""
    m = re.search(r"uppercase_words:\s*\[(.+?)\]", markdown)
    if not m:
        return []
    return [w.strip().strip('"').strip("'").upper() for w in m.group(1).split(",")]


def extract_topic(markdown: str) -> str:
    m = re.search(r"^#\s*Skript:\s*(.+)$", markdown, re.MULTILINE)
    return m.group(1).strip() if m else "Untitled"
