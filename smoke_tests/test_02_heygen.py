"""
Smoke Test 2: HeyGen API
- Connectivity-Check (list avatars, kostenlos)
- Validiert dass Sophie's Avatar-Group + Voice existieren
- Kosten: $0
"""
import requests
from _helpers import require, ok, fail

SOPHIE_AVATAR_GROUP_ID = "300122b0d08d4f8891c695cfb92aacad"
SOPHIE_VOICE_ID = "3020b907712a43dbb4a8b186c6144ffd"


def main():
    api_key = require("HEYGEN_API_KEY")
    headers = {"X-Api-Key": api_key, "Accept": "application/json"}

    try:
        r = requests.get("https://api.heygen.com/v2/avatars", headers=headers, timeout=15)
        r.raise_for_status()
        avatars = r.json().get("data", {}).get("avatars", [])
        ok(f"HeyGen API erreichbar. {len(avatars)} Avatare im Account.")
    except Exception as e:
        fail("HeyGen API call failed", e)
        return

    try:
        r = requests.get(
            f"https://api.heygen.com/v2/avatar_group/{SOPHIE_AVATAR_GROUP_ID}/avatars",
            headers=headers,
            timeout=15,
        )
        r.raise_for_status()
        looks = r.json().get("data", {}).get("avatar_list", [])
        ok(f"Sophie Avatar-Group gefunden mit {len(looks)} Looks.")
        for look in looks[:5]:
            print(f"   - {look.get('avatar_name', 'unbenannt')} (ID: {look.get('avatar_id', '?')[:8]}...)")
    except Exception as e:
        fail("Sophie Avatar-Group nicht zugaenglich", e)

    try:
        r = requests.get("https://api.heygen.com/v2/voices", headers=headers, timeout=15)
        r.raise_for_status()
        voices = r.json().get("data", {}).get("voices", [])
        match = [v for v in voices if v.get("voice_id") == SOPHIE_VOICE_ID]
        if match:
            v = match[0]
            ok(f"Sophie Voice 'Ela' gefunden: {v.get('name', '?')} ({v.get('language', '?')})")
        else:
            print(f"⚠️  Voice {SOPHIE_VOICE_ID} nicht in Voice-Liste (eventuell custom voice nicht hier gelistet)")
    except Exception as e:
        fail("HeyGen voices list failed", e)


if __name__ == "__main__":
    main()
