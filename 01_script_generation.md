# Directive 01 – Skript-Generierung

> **Stage 1** der Pipeline. Input: Topic. Output: Skript-Datei + Metadaten.

---

## Aufgabe

Generiere ein gesprochenes Video-Skript (45-65 Sek, ~120-160 Wörter) im Sophie- 
oder Jonas-Stil. Output ist eine `script.md` in `runs/{run_id}/`.

---

## Input

```yaml
topic: "Warum 90% der KI-Implementierungen scheitern"
persona: "sophie"  # oder "jonas"
cta_keyword: "KICHECK"  # optional, sonst auto-generiert
lead_magnet: "Checkliste mit 5 Fragen vor jeder KI-Implementierung"  # optional
energy_level: "standard"  # standard | high | calm
```

---

## Skript-Struktur

```
[HOOK – 0:00-0:05]
{Provokante Aussage, Pain-Point, Statistik oder Insider-Insight}
{Kann/sollte 1 UPPERCASE-Wort enthalten für ElevenLabs-Betonung}

[PROBLEM – 0:05-0:20]
{Erklärung warum das Problem existiert}
{Konkrete Beispiele, Metaphern}

[MISCONCEPTION – 0:20-0:30]
{Was die meisten falsch machen}
{1 UPPERCASE-Wort für die "Falsch!"-Betonung}

[LÖSUNG – 0:30-0:50]
{Konkrete Lösung mit Schritten}
{Klar formuliert, gerne mit Authority-Phrase wie "Wir sehen bei Kunden..."}

[CTA – 0:50-0:55]
{Comment-Trigger + Lead-Magnet}
"Kommentier {KEYWORD} und ich schick dir {Lead-Magnet}."
```

---

## STRENGE Skript-Regeln

### Sprach-Regeln

1. **Volle Artikel:** "ein", "einem", "einer" – NIE "n", "nem", "ner"
2. **Keine Gedankenstriche:** durch Punkte oder Kommas oder fließende Verbinder ersetzen
3. **Wort-Endungen können verkürzt werden:** "Stundn", "fangn", "machn", "Firmn", "Implementierungn", "verworfne", "altn" – das macht es natürlicher gesprochen
4. **Aber NIE Artikel verkürzen:** "einem Hammer" ✓ — "nem Hammer" ✗
5. **Max 15 Wörter pro Satz:** lange Sätze splitten
6. **Punkte statt Kommas** wo natürliche Sprechpausen sein sollen
7. **UPPERCASE für 1-3 Schlüsselwörter** im Skript – das wird von ElevenLabs als Betonung interpretiert

### Inhaltliche Regeln

1. **Hook in den ersten 3-5 Sekunden** muss einen Pain-Point oder Reveal-Trigger haben
2. **Konkrete Beispiele** statt abstrakter Phrasen ("Sie suchen sich ChatGPT" statt "die meisten suchen sich ein Tool")
3. **Eine Metapher pro Skript** die das Konzept greifbar macht (Beispiele: Rucksack, Hammer und Nägel, Werkzeugkasten)
4. **Soft Authority:** "Wir sehen bei Kunden...", "Erfolgreiche Implementierungen haben..." – nicht "Wir sind die Besten"
5. **Keine Hype-Wörter:** "revolutionär", "game-changing", "Insane" → vermeiden
6. **Du-Form, direkte Ansprache**

### UPPERCASE-Regeln für Betonung

- 1-3 Wörter pro Skript in CAPS
- Nie ganze Sätze
- Bei Kontrast-Aussagen: das Pivot-Wort ("Aber WARTE", "FALSCH")
- Bei Zahlen-Hooks: "90 PROZENT scheitern"
- Bei Schlüsselbegriffen: "Was WIRKLICH funktioniert..."
- CTA-Keyword IMMER in CAPS (z.B. "Kommentier KICHECK")

---

## Output-Format

### `script.md`

```markdown
# Skript: {Topic}

**Persona:** sophie | jonas  
**Energie-Level:** standard  
**CTA-Keyword:** KICHECK  
**Lead-Magnet:** {Beschreibung}  
**Voraussichtliche Sprechdauer:** ~55 Sek  
**Wort-Anzahl:** 140

---

## Sektion 1 – Hook (0:00-0:05)

90 Prozent aller KI-Implementierungn in Unternehmen scheitern und es liegt 
fast nie an der Technologie.

## Sektion 2 – Problem (0:05-0:20)

Die meistn Firmn fangn nämlich genau falschrum an. Sie suchn sich ein cooles 
Tool, zum Beispiel ChatGPT oder ein neues Agentic Framework, und überlegn 
dann was sie damit machn können. Das is wie ein Hammer der nach Nägeln 
sucht und am Ende landest du bei einem Chatbot den keiner brauch.

## Sektion 3 – Misconception (0:20-0:30)

Viele drückn jetzt /compact, wenn der Kontext voll wird. FALSCH. Compact 
fasst dein Chaos nur zusammen.

## Sektion 4 – Lösung (0:30-0:50)

Was WIRKLICH funktioniert is genau andersrum. Du fängst beim Problem an. 
Welcher Prozess in deiner Firma kostet jede Woche zwanzig Stunden und 
nervt alle? Erst dann fragst du dich welche KI das lösen könnte.

## Sektion 5 – CTA (0:50-0:55)

Kommentier KICHECK und ich schick dir unsre Checkliste mit den fünf Fragen 
die du dir vor jeder KI-Implementierung stelln solltst.

---

## Voll-Skript (für HeyGen direkt einsetzbar)

{Hier nochmal alle 5 Sektionen als ein zusammenhängender Block, fließend lesbar, 
ohne Sektion-Headers, ohne Zeitmarken}

---

## Metadata für nachfolgende Stages

```yaml
keywords_extracted:
  - "Claude Code"
  - "Higgsfield"
  - "MCP"

tools_mentioned:
  - "ChatGPT"
  - "Agentic Framework"

uppercase_words:
  - "FALSCH"
  - "WIRKLICH"
  - "KICHECK"

animation_sections:
  - section: 1
    suggested_template: "hook_counter"
    visual_concept: "90% Counter mit Orange-Glow"
  - section: 2
    suggested_template: "comparison_split"
    visual_concept: "Hammer sucht Nägel"
  - section: 3
    suggested_template: "quote_emphasis"
    visual_concept: "Compact-Befehl mit FALSCH-Overlay"
  - section: 4
    suggested_template: "process_flow"
    visual_concept: "Problem → KI-Auswahl-Workflow"
  - section: 5
    suggested_template: "cta_keyword"
    visual_concept: "KICHECK Comment-Bubble"

heygen_look_recommendation: "The AI Video Host"
thumbnail_heading: "WARUM 90% SCHEITERN"
thumbnail_sub_cta: "DIE WAHRHEIT ÜBER KI"
```
```

---

## Claude Prompt Template (für die Generierung)

```
Du bist ein Skript-Generator für die Video-Pipeline. Schreibe ein Skript 
nach folgenden Regeln:

PERSONA: {persona}
TOPIC: {topic}
CTA-KEYWORD: {cta_keyword}
LEAD-MAGNET: {lead_magnet}

SKRIPT-REGELN (aus directives/01_script_generation.md):

[Hier die Regeln aus dem oberen Abschnitt rein-pasten]

STRUKTUR: Hook → Problem → Misconception → Lösung → CTA
DAUER: 45-65 Sek (120-160 Wörter)
UPPERCASE: 1-3 Schlüsselwörter + immer das CTA-Keyword

Halte dich an alle Sprach-Regeln (volle Artikel, keine Gedankenstriche, 
phonetische Wort-Endungen ok, max 15 Wörter pro Satz).

Output: Markdown im Format wie in directives/01_script_generation.md spezifiziert.
```

---

## Validierungs-Checks

Vor Übergabe an Stage 2 prüft die Pipeline automatisch:

- [ ] Wort-Anzahl zwischen 120-160
- [ ] Keine Sätze über 15 Wörter
- [ ] Keine "n"/"nem"/"ner"-Artikel
- [ ] Keine Gedankenstriche im Skript
- [ ] Mindestens 1, maximal 3 UPPERCASE-Wörter (CTA-Keyword zählt extra)
- [ ] CTA-Sektion enthält das gewünschte Keyword
- [ ] 5 Sektionen vorhanden mit korrekten Zeit-Markern

Bei Fehler: Pipeline stoppt, Skript wird zur manuellen Review markiert.
