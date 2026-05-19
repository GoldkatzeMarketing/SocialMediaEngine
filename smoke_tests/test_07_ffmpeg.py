"""
Smoke Test 7: ffmpeg
- Validiert dass ffmpeg installiert ist
- Macht einen winzigen Composite-Test (2 farbige Bilder uebereinander stapeln)
- Kosten: $0
"""
import shutil
import subprocess
from pathlib import Path
from _helpers import ok, fail


def main():
    if not shutil.which("ffmpeg"):
        fail("ffmpeg nicht im PATH. Install: 'brew install ffmpeg' (Mac) oder 'apt install ffmpeg' (Linux).")
        return

    try:
        v = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, timeout=5)
        first_line = v.stdout.splitlines()[0]
        ok(f"ffmpeg gefunden: {first_line}")
    except Exception as e:
        fail("ffmpeg version check failed", e)
        return

    out = Path(__file__).parent / "_ffmpeg_test.mp4"
    try:
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", "color=c=white:s=1080x768:d=1",
            "-f", "lavfi", "-i", "color=c=#FF6B35:s=1080x1152:d=1",
            "-filter_complex", "[0:v][1:v]vstack=inputs=2[v]",
            "-map", "[v]",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-t", "1",
            str(out),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            fail(f"ffmpeg composite failed: {result.stderr[-500:]}")
            return
        size_kb = out.stat().st_size / 1024
        ok(f"Composite-Video erzeugt: {out.name} ({size_kb:.1f} KB)")
    except Exception as e:
        fail("ffmpeg composite test failed", e)


if __name__ == "__main__":
    main()
