"""Telegram-Notifier. No-op wenn keine Credentials gesetzt sind."""
import os
import requests
from pathlib import Path

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def text(msg: str):
    if not TOKEN or not CHAT_ID:
        print(f"[telegram skipped] {msg[:80]}")
        return
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"},
            timeout=10,
        )
        r.raise_for_status()
    except Exception as e:
        print(f"[telegram failed] {e}")


def video(path: Path, caption: str = ""):
    if not TOKEN or not CHAT_ID:
        print(f"[telegram skipped] video: {path}")
        return
    try:
        with open(path, "rb") as f:
            r = requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendVideo",
                data={"chat_id": CHAT_ID, "caption": caption, "parse_mode": "Markdown"},
                files={"video": f},
                timeout=120,
            )
            r.raise_for_status()
    except Exception as e:
        print(f"[telegram failed] {e}")
