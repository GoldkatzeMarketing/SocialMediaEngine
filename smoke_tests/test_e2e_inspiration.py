"""
End-to-End Smoke Test: vom Instagram-Reel zum fertigen Sophie-MP4.

Schritte:
  1. Erstes Profil aus monitoring/instagram_channels.txt
  2. Apify: neuestes Reel scrapen + Video downloaden
  3. Whisper: Reel transkribieren (Inspiration)
  4. Claude: Sophie-Skript aus Inspiration generieren
  5. HeyGen: Avatar-Video rendern (Sophie, Voice Ela)
  6. Pillow: statische Top-Karte
  7. ffmpeg: 40/60 Composite + Word-Level-Captions (Whisper + ASS-Burn)
  8. Telegram-Notification mit fertiger MP4

Kosten ca. $0.40, Dauer ca. 10-15 min.

Usage:
    python smoke_tests/test_e2e_inspiration.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(PROJECT_ROOT / ".env")

from e2e import scraper, transcriber, script_gen, avatar, composite, notify, state

CHANNELS_FILE = PROJECT_ROOT / "monitoring" / "instagram_channels.txt"


def first_profile_from_watchlist() -> str:
    if not CHANNELS_FILE.exists():
        raise FileNotFoundError(f"{CHANNELS_FILE} fehlt")
    for line in CHANNELS_FILE.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            return line
    raise RuntimeError("Keine Profile in monitoring/instagram_channels.txt")


def step(num: int, title: str):
    print(f"\n── [{num}/8] {title} ─────────────────────────────")


def main():
    print("=" * 60)
    print("Sophie Pipeline – End-to-End Smoke Test")
    print("=" * 60)

    # 1. Watchlist
    step(1, "Profil aus Watchlist")
    profile_url = first_profile_from_watchlist()
    print(f"   → {profile_url}")
    run_dir = state.new_run(slug_hint=f"smoke_{profile_url.rstrip('/').split('/')[-1]}")
    print(f"   Run-Dir: {run_dir}")
    notify.text(f"🚀 Smoke-Test gestartet\nProfil: `{profile_url}`\nRun: `{run_dir.name}`")

    # 2. Apify Scrape + Download
    step(2, "Apify – neuestes Reel scrapen")
    try:
        reel = scraper.get_latest_reel(profile_url)
    except Exception as e:
        state.log_stage(run_dir, "Stage 2: Apify Scrape", "❌ failed", error=str(e))
        notify.text(f"❌ Apify-Scrape failed: {e}")
        raise
    short = reel.get("shortCode", "?")
    reel_url = f"https://www.instagram.com/reel/{short}/"
    print(f"   shortCode: {short}")
    print(f"   videoUrl: {reel.get('videoUrl', '')[:80]}")
    (run_dir / "source_reel.json").write_text(json.dumps(reel, indent=2, default=str))

    print("   Downloading reel...")
    reel_video = scraper.download_video(reel["videoUrl"], run_dir / "source_reel.mp4")
    print(f"   Saved: {reel_video.name} ({reel_video.stat().st_size / 1024:.1f} KB)")
    state.log_stage(run_dir, "Stage 2: Apify Scrape", "✅ done",
                    shortCode=short, source_url=reel_url)

    # 3. Whisper – Inspiration-Transkript
    step(3, "Whisper – Transkript der Inspiration")
    transcript = transcriber.transcribe(reel_video, language="de", model_size="base")
    print(f"   Sprache: {transcript['language']}, Dauer: {transcript['duration']:.1f}s")
    print(f"   Text: '{transcript['text'][:150]}...'")
    (run_dir / "inspiration_transcript.txt").write_text(transcript["text"])
    state.log_stage(run_dir, "Stage 3: Whisper Inspiration", "✅ done",
                    duration=f"{transcript['duration']:.1f}s",
                    chars=len(transcript["text"]))
    notify.text(f"📝 *Inspiration-Transkript*\n```\n{transcript['text'][:500]}\n```")

    # 4. Claude – Skript-Generierung
    step(4, "Claude – Sophie-Skript generieren")
    script_md = script_gen.generate_script(
        inspiration_transcript=transcript["text"],
        source_caption=reel.get("caption") or "",
    )
    (run_dir / "script.md").write_text(script_md)
    voll_skript = script_gen.extract_voll_skript(script_md)
    uppercase_keywords = script_gen.extract_uppercase_keywords(script_md)
    topic = script_gen.extract_topic(script_md)
    print(f"   Topic: {topic}")
    print(f"   UPPERCASE: {uppercase_keywords}")
    print(f"   Voll-Skript: {len(voll_skript.split())} Woerter")
    state.log_stage(run_dir, "Stage 4: Skript-Generierung", "✅ done",
                    topic=topic, words=len(voll_skript.split()),
                    uppercase=", ".join(uppercase_keywords))
    notify.text(f"✍️ *Skript fertig*\n*Topic:* {topic}\n*Keywords:* {', '.join(uppercase_keywords)}\n\n```\n{voll_skript[:800]}\n```")

    # 5. HeyGen – Avatar-Render
    step(5, "HeyGen – Avatar-Render (~4 min)")
    notify.text("🎬 HeyGen rendert Sophie... (~4 min)")
    avatar_video = run_dir / "avatar_video.mp4"
    try:
        video_id = avatar.render(voll_skript, avatar_video, title=topic[:50])
    except Exception as e:
        state.log_stage(run_dir, "Stage 5: HeyGen Render", "❌ failed", error=str(e))
        notify.text(f"❌ HeyGen render failed: {e}")
        raise
    print(f"   Saved: {avatar_video.name} ({avatar_video.stat().st_size / 1024 / 1024:.1f} MB)")
    state.log_stage(run_dir, "Stage 5: HeyGen Render", "✅ done",
                    video_id=video_id, file=avatar_video.name)

    # 6. Top-Karte
    step(6, "Pillow – Top-Karte rendern")
    top_image = run_dir / "top_card.png"
    composite.make_top_card(topic, top_image)
    print(f"   Saved: {top_image.name}")
    state.log_stage(run_dir, "Stage 6: Top-Karte", "✅ done", file=top_image.name)

    # 7. Composite + Captions
    step(7, "ffmpeg – Composite + Captions")
    composite_no_caps = run_dir / "composite_no_captions.mp4"
    composite.stack_top_image_over_avatar(top_image, avatar_video, composite_no_caps)
    print(f"   Composite: {composite_no_caps.name}")

    print("   Whisper word-level on avatar audio...")
    words = transcriber.transcribe_word_level(avatar_video, language="de", model_size="base")
    print(f"   {len(words)} Woerter timing-extrahiert")

    ass_file = run_dir / "captions.ass"
    composite.make_ass_captions(words, uppercase_keywords, ass_file)
    print(f"   ASS: {ass_file.name}")

    final = run_dir / "final.mp4"
    composite.burn_captions(composite_no_caps, ass_file, final)
    final_size_mb = final.stat().st_size / 1024 / 1024
    print(f"   Final: {final.name} ({final_size_mb:.1f} MB)")
    state.log_stage(run_dir, "Stage 7: Composite + Captions", "✅ done",
                    captions=len(words) // 2, final_size_mb=f"{final_size_mb:.1f}")

    # 8. Telegram + Done
    step(8, "Telegram – Final-Video senden")
    notify.video(final, caption=f"✅ Done.\n*{topic}*\nRun: `{run_dir.name}`")
    notify.text(f"🎉 Smoke-Test fertig\nFinal: `{final}`\nRun-State: `{run_dir / 'state.md'}`")

    print("\n" + "=" * 60)
    print(f"✅ Done. Final video: {final}")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Pipeline aborted: {type(e).__name__}: {e}")
        sys.exit(1)
