"""
Runs all smoke tests sequentially.
Stops at first failure so you can fix and continue.

Usage:
    python smoke_tests/run_all.py
    python smoke_tests/run_all.py --skip 4   # Apify ueberspringen
"""
import subprocess
import sys
from pathlib import Path

TESTS = [
    ("1", "test_01_claude.py", "Claude API"),
    ("2", "test_02_heygen.py", "HeyGen API"),
    ("3", "test_03_elevenlabs.py", "ElevenLabs (connectivity only)"),
    ("4", "test_04_apify.py", "Apify Instagram Scraper"),
    ("5", "test_05_whisper.py", "Whisper Transcription"),
    ("6", "test_06_telegram.py", "Telegram Bot"),
    ("7", "test_07_ffmpeg.py", "ffmpeg Composite"),
]

HERE = Path(__file__).parent


def main():
    skips = set()
    for i, arg in enumerate(sys.argv):
        if arg == "--skip" and i + 1 < len(sys.argv):
            skips.update(sys.argv[i + 1].split(","))

    print("=" * 60)
    print("Sophie Pipeline – Infrastructure Smoke Tests")
    print("=" * 60)

    results = []
    for num, script, name in TESTS:
        print(f"\n── Test {num}: {name} ────────────────────────────────")
        if num in skips:
            print(f"   ⏭️  Skipped")
            results.append((num, name, "skipped"))
            continue
        r = subprocess.run([sys.executable, str(HERE / script)], cwd=HERE)
        results.append((num, name, "pass" if r.returncode == 0 else "fail"))
        if r.returncode != 0:
            print(f"\n❌ Test {num} failed. Stopping here. Fix and re-run.")
            break

    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    for num, name, status in results:
        icon = {"pass": "✅", "fail": "❌", "skipped": "⏭️ "}[status]
        print(f"  {icon} Test {num}: {name}")

    if all(s == "pass" or s == "skipped" for _, _, s in results):
        print("\n🎉 Alle Tests bestanden. Bereit für Pipeline-Bau.")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
