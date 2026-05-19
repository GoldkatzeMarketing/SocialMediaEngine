"""Shared helpers for smoke tests."""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(PROJECT_ROOT / ".env")


def require(var_name: str) -> str:
    value = os.getenv(var_name)
    if not value:
        print(f"❌ Missing env var: {var_name}")
        print(f"   Set it in {PROJECT_ROOT / '.env'} and try again.")
        sys.exit(1)
    return value


def ok(msg: str):
    print(f"✅ {msg}")


def fail(msg: str, exc: Exception | None = None):
    print(f"❌ {msg}")
    if exc:
        print(f"   {type(exc).__name__}: {exc}")
    sys.exit(1)
