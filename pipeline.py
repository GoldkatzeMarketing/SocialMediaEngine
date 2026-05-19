"""
Video Pipeline Orchestrator
============================
Hauptscript der Pipeline. Orchestriert alle 7 Stages.

Verwendung:
    python execution/pipeline.py --topic "..." --persona sophie
    python execution/pipeline.py --resume <run_id>
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# Stages importieren
from stages.stage_01_script import generate_script
from stages.stage_02_voice import generate_voice_audio
from stages.stage_03_heygen import generate_avatar_video
from stages.stage_04_animations import generate_animations
from stages.stage_05_composite import composite_with_captions
from stages.stage_06_thumbnail import generate_thumbnail
from stages.stage_07_manychat import create_manychat_flow

from utils.state_manager import StateManager
from utils.api_clients import HeyGenClient, ElevenLabsClient
import config


# ──────────────────────────────────────────────────────────────────────────
def slugify(text):
    return "".join(c if c.isalnum() else "_" for c in text.lower())[:60]


def init_run(topic, persona, cta_keyword=None, lead_magnet=None):
    """Erstellt einen neuen Run-Ordner mit initialer state.md"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    slug = slugify(topic)
    run_id = f"{timestamp}_{slug}"
    run_dir = Path(f"runs/{run_id}")
    run_dir.mkdir(parents=True, exist_ok=True)
    
    state = StateManager(run_dir / "state.md")
    state.init(
        topic=topic,
        persona=persona,
        cta_keyword=cta_keyword or "auto-generated-later",
        lead_magnet=lead_magnet or "",
    )
    return run_id, run_dir, state


def resume_run(run_id):
    """Lädt einen bestehenden Run und ermittelt die letzte erfolgreiche Stage"""
    run_dir = Path(f"runs/{run_id}")
    if not run_dir.exists():
        raise FileNotFoundError(f"Run {run_id} not found")
    state = StateManager(run_dir / "state.md")
    state.load()
    return run_id, run_dir, state


# ──────────────────────────────────────────────────────────────────────────
def run_pipeline(topic=None, persona="sophie", cta_keyword=None, lead_magnet=None, 
                 resume_id=None, skip_manychat=True):
    """Master-Orchestrator"""
    
    if resume_id:
        run_id, run_dir, state = resume_run(resume_id)
        print(f"📂 Resuming run: {run_id}")
    else:
        if not topic:
            raise ValueError("Topic required for new run")
        run_id, run_dir, state = init_run(topic, persona, cta_keyword, lead_magnet)
        print(f"🚀 New run: {run_id}")
    
    stages_to_run = state.next_pending_stages()
    print(f"📋 Stages to run: {stages_to_run}")
    
    # ── STAGE 1: Script Generation ────────────────────────────────────────
    if "stage_01" in stages_to_run:
        state.start_stage("stage_01")
        script_data = generate_script(
            topic=state.get("topic"),
            persona=state.get("persona"),
            cta_keyword=state.get("cta_keyword"),
            lead_magnet=state.get("lead_magnet"),
            output_dir=run_dir,
        )
        state.complete_stage("stage_01", output={
            "script_file": str(run_dir / "script.md"),
            "word_count": script_data["word_count"],
            "estimated_duration_sec": script_data["estimated_duration_sec"],
            "uppercase_words": script_data["uppercase_words"],
            "tools_mentioned": script_data["tools_mentioned"],
            "heygen_look_recommendation": script_data["heygen_look_recommendation"],
            "thumbnail_heading": script_data["thumbnail_heading"],
            "thumbnail_sub_cta": script_data["thumbnail_sub_cta"],
        })
        print(f"✅ Stage 1 done: {script_data['word_count']} words, ~{script_data['estimated_duration_sec']}s")
    
    # ── STAGE 2: Voice Audio (OPTIONAL, skip by default) ──────────────────
    # Skipping in default flow – HeyGen handles voice in Stage 3
    
    # ── STAGE 3: HeyGen Avatar-Video ──────────────────────────────────────
    if "stage_03" in stages_to_run:
        state.start_stage("stage_03")
        video_path = generate_avatar_video(
            script_path=run_dir / "script.md",
            persona=state.get("persona"),
            look_recommendation=state.get_stage_output("stage_01", "heygen_look_recommendation"),
            output_path=run_dir / "avatar_video.mp4",
        )
        state.complete_stage("stage_03", output={
            "avatar_video": str(video_path),
        })
        print(f"✅ Stage 3 done: HeyGen video rendered")
    
    # ── STAGE 4: HTML Animations ──────────────────────────────────────────
    if "stage_04" in stages_to_run:
        state.start_stage("stage_04")
        animations_meta = generate_animations(
            script_path=run_dir / "script.md",
            output_dir=run_dir / "animations",
        )
        state.complete_stage("stage_04", output={
            "animations_dir": str(run_dir / "animations"),
            "segment_count": len(animations_meta["segments"]),
            "total_duration": animations_meta["total_duration"],
        })
        print(f"✅ Stage 4 done: {len(animations_meta['segments'])} animations created")
    
    # ── STAGE 5: Composite + Captions ─────────────────────────────────────
    if "stage_05" in stages_to_run:
        state.start_stage("stage_05")
        final_path = composite_with_captions(
            avatar_video=run_dir / "avatar_video.mp4",
            animations_dir=run_dir / "animations",
            script_path=run_dir / "script.md",
            uppercase_words=state.get_stage_output("stage_01", "uppercase_words"),
            output_path=run_dir / "final.mp4",
        )
        state.complete_stage("stage_05", output={
            "final_video": str(final_path),
        })
        print(f"✅ Stage 5 done: final.mp4 created")
    
    # ── STAGE 6: Thumbnail ────────────────────────────────────────────────
    if "stage_06" in stages_to_run:
        state.start_stage("stage_06")
        thumbnail_paths = generate_thumbnail(
            avatar_video=run_dir / "avatar_video.mp4",
            heading=state.get_stage_output("stage_01", "thumbnail_heading"),
            sub_cta=state.get_stage_output("stage_01", "thumbnail_sub_cta"),
            tools=state.get_stage_output("stage_01", "tools_mentioned"),
            output_dir=run_dir,
        )
        state.complete_stage("stage_06", output={
            "thumbnail": str(thumbnail_paths["story"]),
            "thumbnail_feed": str(thumbnail_paths["feed"]),
        })
        print(f"✅ Stage 6 done: thumbnails created")
    
    # ── STAGE 7: ManyChat (optional) ──────────────────────────────────────
    if "stage_07" in stages_to_run and not skip_manychat:
        state.start_stage("stage_07")
        flow_id = create_manychat_flow(
            keyword=state.get("cta_keyword"),
            lead_magnet=state.get("lead_magnet"),
        )
        state.complete_stage("stage_07", output={
            "manychat_flow_id": flow_id,
        })
        print(f"✅ Stage 7 done: ManyChat flow created (ID: {flow_id})")
    
    # ── DONE ──────────────────────────────────────────────────────────────
    print()
    print("─" * 60)
    print(f"✨ Pipeline complete: {run_id}")
    print(f"📁 Run-Ordner: {run_dir}")
    print(f"🎬 Final Video: {run_dir / 'final.mp4'}")
    print(f"🖼️  Thumbnail (Story): {run_dir / 'thumbnail.png'}")
    print(f"🖼️  Thumbnail (Feed): {run_dir / 'thumbnail_feed.png'}")
    print("─" * 60)
    
    return {
        "run_id": run_id,
        "final_video": str(run_dir / "final.mp4"),
        "thumbnail": str(run_dir / "thumbnail.png"),
        "thumbnail_feed": str(run_dir / "thumbnail_feed.png"),
    }


# ──────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Video Pipeline Orchestrator")
    parser.add_argument("--topic", type=str, help="Video-Topic")
    parser.add_argument("--persona", type=str, default="sophie", choices=["sophie", "jonas"])
    parser.add_argument("--cta-keyword", type=str, help="CTA-Keyword (z.B. KICHECK)")
    parser.add_argument("--lead-magnet", type=str, help="Beschreibung des Lead-Magnets")
    parser.add_argument("--resume", type=str, help="Run-ID zum Fortsetzen")
    parser.add_argument("--with-manychat", action="store_true", help="ManyChat-Flow automatisch erstellen")
    
    args = parser.parse_args()
    
    if not args.topic and not args.resume:
        parser.error("Either --topic or --resume required")
    
    run_pipeline(
        topic=args.topic,
        persona=args.persona,
        cta_keyword=args.cta_keyword,
        lead_magnet=args.lead_magnet,
        resume_id=args.resume,
        skip_manychat=not args.with_manychat,
    )
