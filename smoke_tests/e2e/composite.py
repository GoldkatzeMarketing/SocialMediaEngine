"""Composite: Top-Karte (Pillow) + Avatar (40/60 vstack) + Word-Level-Captions (ASS-Burn)."""
import subprocess
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

TOP_W, TOP_H = 1080, 768
BOTTOM_W, BOTTOM_H = 1080, 1152
BRAND_WHITE = (255, 255, 255)
BRAND_ORANGE = (255, 107, 53)
BRAND_BLACK = (10, 10, 10)


def make_top_card(topic: str, output_path: Path):
    """Generates a static brand-styled card for the top 40%."""
    img = Image.new("RGB", (TOP_W, TOP_H), BRAND_WHITE)
    draw = ImageDraw.Draw(img)

    try:
        font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 84)
        font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
    except (OSError, IOError):
        try:
            font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 84)
            font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
        except (OSError, IOError):
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()

    draw.text((60, 80), "SOPHIE", fill=BRAND_ORANGE, font=font_small)
    draw.rectangle([(60, 130), (180, 138)], fill=BRAND_ORANGE)

    wrapped = textwrap.fill(topic, width=22)
    bbox = draw.multiline_textbbox((0, 0), wrapped, font=font_large)
    text_h = bbox[3] - bbox[1]
    y = (TOP_H - text_h) // 2 + 30
    draw.multiline_text((60, y), wrapped, fill=BRAND_BLACK, font=font_large, spacing=14)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, "PNG")


def get_duration(media: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(media)],
        capture_output=True, text=True, check=True,
    )
    return float(out.stdout.strip())


def stack_top_image_over_avatar(top_image: Path, avatar_video: Path, output: Path):
    """Top-Image als Standbild + Avatar gecroppt (untere 60%) = vstack 1080x1920."""
    duration = get_duration(avatar_video)
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-t", str(duration), "-i", str(top_image),
        "-i", str(avatar_video),
        "-filter_complex",
        f"[0:v]scale={TOP_W}:{TOP_H},setsar=1[top];"
        f"[1:v]crop={BOTTOM_W}:{BOTTOM_H}:0:768,setsar=1[bot];"
        f"[top][bot]vstack=inputs=2[v]",
        "-map", "[v]", "-map", "1:a",
        "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(output),
    ]
    subprocess.run(cmd, check=True, capture_output=True)


def _fmt_ass_time(sec: float) -> str:
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def make_ass_captions(words: list[dict], uppercase_keywords: list[str], output: Path,
                       max_words_per_caption: int = 2):
    """Generates an ASS subtitle file. 2 words per frame, orange for keywords."""
    keywords_set = {kw.upper() for kw in uppercase_keywords}

    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, BorderStyle, Outline, Shadow, Alignment, MarginV, Encoding
Style: Default,Inter,72,&H000A0A0A,&H00FFFFFF,&H80FFFFFF,1,3,4,0,2,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    events = []
    i = 0
    while i < len(words):
        group = words[i:i + max_words_per_caption]
        if not group:
            break
        parts = []
        for w in group:
            clean = "".join(c for c in w["word"] if c.isalnum()).upper()
            if clean in keywords_set:
                parts.append(f"{{\\c&H00356BFF&}}{w['word']}{{\\c&H000A0A0A&}}")
            else:
                parts.append(w["word"])
        text = " ".join(parts)
        start = _fmt_ass_time(group[0]["start"])
        end = _fmt_ass_time(group[-1]["end"])
        events.append(f"Dialogue: 0,{start},{end},Default,,0,0,1100,,{text}")
        i += max_words_per_caption

    output.write_text(header + "\n".join(events), encoding="utf-8")


def burn_captions(input_video: Path, ass_file: Path, output: Path):
    cmd = [
        "ffmpeg", "-y", "-i", str(input_video),
        "-vf", f"ass={ass_file}",
        "-c:a", "copy",
        str(output),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
