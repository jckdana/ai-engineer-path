# Walks a folder of documents, summarises every .txt file, and writes a JSON index.
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DOCS_DIR = HERE / "01-05-docs"
INDEX_PATH = HERE / "01-05-index.json"


def summarize(path):
    """Return a dict describing one text file."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    words = text.split()
    return {
        "file": path.relative_to(DOCS_DIR).as_posix(),
        "words": len(words),
        "lines": len(lines),
        "first_line": lines[0] if lines else "",
    }


def save_index(entries, path):
    """Write the index as readable JSON."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)


if not DOCS_DIR.is_dir():
    print(f"No folder at {DOCS_DIR}. Run 01-05-make-docs.py first.")
    raise SystemExit(1)

entries = []
# Find every .txt file in DOCS_DIR and its subfolders, in a stable order,
# and append summarize(path) for each one.
for path in sorted(DOCS_DIR.rglob("*.txt")):
    entries.append(summarize(path))

save_index(entries, INDEX_PATH)
total_words = sum(e["words"] for e in entries)
empty = sum(1 for e in entries if e["words"] == 0)
print(f"Indexed {len(entries)} files, {total_words} words, {empty} empty -> {INDEX_PATH}")