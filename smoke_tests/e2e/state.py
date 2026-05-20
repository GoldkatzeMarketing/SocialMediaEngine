"""Run-Directory und state.md-Writer (Self-Annealing)."""
from datetime import datetime
from pathlib import Path
import re

PROJECT_ROOT = Path(__file__).parent.parent.parent
RUNS_DIR = PROJECT_ROOT / "runs"


def slugify(text: str, max_len: int = 30) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "_", text.lower()).strip("_")
    return s[:max_len] or "untitled"


def new_run(slug_hint: str = "smoke") -> Path:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = RUNS_DIR / f"{ts}_{slugify(slug_hint)}"
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "state.md").write_text(
        f"# Run State: {run_dir.name}\n\n"
        f"**Created:** {datetime.now().isoformat()}\n\n"
        f"## Stages\n\n"
    )
    return run_dir


def log_stage(run_dir: Path, stage: str, status: str, **fields):
    """Append stage log to state.md. status: ✅ done | 🔄 in_progress | ❌ failed"""
    lines = [f"\n### {stage}", f"- Status: {status}", f"- Timestamp: {datetime.now().isoformat()}"]
    for k, v in fields.items():
        lines.append(f"- {k}: {v}")
    with open(run_dir / "state.md", "a") as f:
        f.write("\n".join(lines) + "\n")
