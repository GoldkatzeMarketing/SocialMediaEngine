# Directive 07 – ManyChat-Integration

> **Stage 7** (Phase 1.5, optional) registriert für jedes Video automatisch einen 
> ManyChat-Flow, der das CTA-Keyword überwacht und das Lead-Magnet-PDF per DM ausliefert.

---

## Voraussetzung

- ManyChat Pro Account (für API-Zugriff)
- Instagram-Account verbunden in ManyChat
- API-Key in `.env`: `MANYCHAT_API_KEY`
- Lead-Magnet-PDF in `templates/pdf_lead_magnets/{topic_slug}.pdf` vorhanden

---

## Input

- CTA-Keyword aus Skript (z.B. "KICHECK")
- Lead-Magnet-Pfad
- Optional: Calendly-Link für Soft-Pitch

---

## Process

### Schritt 1: Lead-Magnet zu ManyChat-Asset hochladen

```python
import requests

def upload_pdf_to_manychat(pdf_path):
    files = {'file': open(pdf_path, 'rb')}
    headers = {'Authorization': f'Bearer {config.MANYCHAT_API_KEY}'}
    r = requests.post(
        'https://api.manychat.com/fb/page/uploadFile',
        files=files,
        headers=headers
    )
    return r.json()['data']['file_id']
```

### Schritt 2: Flow erstellen

```python
def create_keyword_flow(keyword, pdf_file_id, lead_magnet_title):
    headers = {
        'Authorization': f'Bearer {config.MANYCHAT_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    # Flow-Definition
    flow_data = {
        "name": f"Auto-DM: {keyword}",
        "triggers": [
            {
                "type": "keyword",
                "keyword": keyword.lower(),
                "match_type": "contains",
                "channel": "instagram_comment"
            }
        ],
        "messages": [
            {
                "delay": 0,
                "type": "text",
                "text": f"Hey! 👋 Hier ist deine {lead_magnet_title}, wie versprochen!"
            },
            {
                "delay": 2,
                "type": "file",
                "file_id": pdf_file_id
            },
            {
                "delay": 15,
                "type": "text",
                "text": "Brauchst du Hilfe bei der Umsetzung? Wir bauen sowas in 2-3 Wochen schlüsselfertig. Schreib uns, wenn das interessant ist. 🚀"
            }
        ]
    }
    
    r = requests.post(
        'https://api.manychat.com/fb/page/createFlow',
        json=flow_data,
        headers=headers
    )
    return r.json()['data']['flow_id']
```

### Schritt 3: Flow mit Comment-Trigger aktivieren

```python
def activate_comment_trigger(flow_id, video_post_url=None):
    """
    video_post_url: optional, falls bekannt - dann nur Comments auf diesem Post triggern
    """
    headers = {'Authorization': f'Bearer {config.MANYCHAT_API_KEY}'}
    payload = {
        "flow_id": flow_id,
        "active": True,
        "scope": "specific_post" if video_post_url else "all_posts",
        "post_url": video_post_url
    }
    requests.post(
        'https://api.manychat.com/fb/page/updateFlow',
        json=payload,
        headers=headers
    )
```

---

## State-Update

```markdown
### Stage 7: ManyChat-Integration
- Status: ✅ done
- Keyword: KICHECK
- Lead-Magnet: ki_implementation_checklist.pdf
- Flow-ID: 12345678
- Activated: true (all_posts scope)
```

---

## Wichtig: Manueller Schritt nach Posting

Sobald das Video auf Instagram gepostet ist, muss der Mitarbeiter:
1. Die Post-URL kopieren
2. In ManyChat den Flow auf "specific_post" scope einschränken (oder via API mit `post_url`)
3. Das schützt vor falschen Triggern auf anderen Posts mit ähnlichem Keyword

Optional automatisierbar: Wenn Pipeline auch Posting macht (Phase 4), kann sie 
post_url direkt in `activate_comment_trigger` einsetzen.

---

## Validierung

- [ ] PDF erfolgreich hochgeladen
- [ ] Flow erstellt und aktiv
- [ ] Test-Comment mit Keyword löst DM aus (manueller Check vor Live-Posting)
