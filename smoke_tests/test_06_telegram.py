"""
Smoke Test 6: Telegram-Bot
- Schickt eine Test-Message an deine Chat-ID
- Kosten: $0

Setup:
1. In Telegram: @BotFather anschreiben, /newbot → Token
2. Bot anschreiben (irgendwas, z.B. /start)
3. https://api.telegram.org/bot<TOKEN>/getUpdates aufrufen → chat.id kopieren
4. TELEGRAM_BOT_TOKEN und TELEGRAM_CHAT_ID in .env eintragen
"""
import requests
from _helpers import require, ok, fail


def main():
    token = require("TELEGRAM_BOT_TOKEN")
    chat_id = require("TELEGRAM_CHAT_ID")

    try:
        r = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": "✅ Smoke Test: Sophie Pipeline Bot ist live.\n\nNeue Reels werden hier gemeldet.",
                "parse_mode": "Markdown",
            },
            timeout=15,
        )
        r.raise_for_status()
        data = r.json()
        if data.get("ok"):
            ok(f"Message gesendet (message_id: {data['result']['message_id']})")
            ok("Check dein Telegram!")
        else:
            fail(f"Telegram API antwortete mit Fehler: {data}")
    except Exception as e:
        fail("Telegram send failed", e)


if __name__ == "__main__":
    main()
