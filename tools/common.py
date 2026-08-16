"""Shared helpers for tools/. Import, don't duplicate.

Every tool in this directory follows the same contract:
  - takes arguments via argparse
  - prints a single JSON object to stdout (so the agent can parse the result)
  - prints human-readable progress/errors to stderr
  - exits 0 on success, 1 on handled failure
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TMP = ROOT / ".tmp"
WORKFLOWS = ROOT / "workflows"

# Learning system. content/ is the durable source of truth; docs/ is regenerable output.
# The output dir is named docs/ because that is one of the two folders GitHub Pages
# will serve from a branch — it lets `git push` publish the site with no CI.
CONTENT = ROOT / "content"
LESSONS = CONTENT / "lessons"
ROADMAP_FILE = CONTENT / "roadmap.json"
PROGRESS_FILE = CONTENT / "progress.json"
SITE = ROOT / "docs"
TEMPLATES = ROOT / "templates"


def load_env():
    """Load ROOT/.env into os.environ. Safe to call more than once."""
    try:
        from dotenv import load_dotenv
    except ImportError:
        fail("python-dotenv is not installed. Run: pip install -r requirements.txt")
    load_dotenv(ROOT / ".env")


def require_env(*names):
    """Return the requested env vars, failing loudly if any are missing."""
    load_env()
    missing = [n for n in names if not os.environ.get(n)]
    if missing:
        fail(f"Missing required env var(s) in .env: {', '.join(missing)}")
    values = [os.environ[n] for n in names]
    return values[0] if len(values) == 1 else values


def tmp_path(name: str) -> Path:
    """Path inside .tmp/, parents created. Contents are disposable."""
    p = TMP / name
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def today() -> str:
    """Local calendar date as YYYY-MM-DD. Streaks are counted in local days."""
    return datetime.now().strftime("%Y-%m-%d")


def read_json(path: Path, default=None):
    """Parse a JSON file. Returns `default` if it doesn't exist; fails on bad JSON."""
    p = Path(path)
    if not p.exists():
        return default
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        fail(f"{p} is not valid JSON: {e}")


def write_json(path: Path, data) -> Path:
    """Write JSON with parents created. Returns the path."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return p


def slugify(text: str) -> str:
    """Filename-safe slug: lowercase, alphanumerics and dashes only."""
    out = []
    for ch in text.lower():
        if ch.isalnum():
            out.append(ch)
        elif out and out[-1] != "-":
            out.append("-")
    return "".join(out).strip("-") or "untitled"


def log(msg: str):
    print(msg, file=sys.stderr, flush=True)


def emit(**payload):
    """Print the tool's result as JSON on stdout and exit 0."""
    payload.setdefault("ok", True)
    print(json.dumps(payload, indent=2, default=str))
    sys.exit(0)


def fail(msg: str, **extra):
    """Print a JSON error on stdout and exit 1."""
    print(json.dumps({"ok": False, "error": msg, **extra}, indent=2, default=str))
    sys.exit(1)
