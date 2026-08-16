"""Install a roadmap into content/ and initialize the progress file.

The roadmap itself is authored by the agent (see workflows/build_learning_roadmap.md)
and handed to this tool as a JSON file. This tool's job is validation: catch a
malformed or duplicate-id roadmap here rather than halfway through site_build.

Usage:
    python tools/roadmap_init.py --from .tmp/roadmap_draft.json
    python tools/roadmap_init.py --from .tmp/roadmap_draft.json --force
"""

import argparse

from common import (
    CONTENT,
    LESSONS,
    PROGRESS_FILE,
    ROADMAP_FILE,
    emit,
    fail,
    log,
    read_json,
    slugify,
    today,
    write_json,
)

LESSON_DEFAULTS = {"core_minutes": 50, "deep_minutes": 0, "build": "", "summary": ""}


def validate(data):
    """Return (modules, lesson_count) or fail loudly. Normalizes defaults in place."""
    if not isinstance(data, dict):
        fail("Roadmap must be a JSON object at the top level.")
    if not data.get("title"):
        fail("Roadmap is missing a 'title'.")

    modules = data.get("modules")
    if not isinstance(modules, list) or not modules:
        fail("Roadmap needs a non-empty 'modules' array.")

    seen_modules, seen_lessons = set(), set()
    count = 0

    for i, m in enumerate(modules):
        where = f"modules[{i}]"
        if not isinstance(m, dict):
            fail(f"{where} is not an object.")
        for key in ("id", "title"):
            if not m.get(key):
                fail(f"{where} is missing '{key}'.")
        if m["id"] in seen_modules:
            fail(f"Duplicate module id: {m['id']}")
        seen_modules.add(m["id"])
        m.setdefault("outcome", "")

        lessons = m.get("lessons")
        if not isinstance(lessons, list) or not lessons:
            fail(f"Module {m['id']} has no lessons.")

        for j, l in enumerate(lessons):
            lwhere = f"modules[{i}].lessons[{j}]"
            if not isinstance(l, dict):
                fail(f"{lwhere} is not an object.")
            for key in ("id", "title"):
                if not l.get(key):
                    fail(f"{lwhere} is missing '{key}'.")
            if l["id"] in seen_lessons:
                fail(f"Duplicate lesson id: {l['id']}")
            seen_lessons.add(l["id"])

            for key, default in LESSON_DEFAULTS.items():
                l.setdefault(key, default)
            if not isinstance(l["core_minutes"], int) or l["core_minutes"] <= 0:
                fail(f"{lwhere} core_minutes must be a positive integer.")
            l["slug"] = f"{l['id']}-{slugify(l['title'])}"
            count += 1

    return modules, count


def main():
    ap = argparse.ArgumentParser(description="Install a roadmap and init progress tracking.")
    ap.add_argument("--from", dest="src", required=True, help="Path to the roadmap JSON to install")
    ap.add_argument("--force", action="store_true", help="Overwrite an existing roadmap.json")
    args = ap.parse_args()

    data = read_json(args.src)
    if data is None:
        fail(f"No such file: {args.src}")

    modules, count = validate(data)
    log(f"Roadmap validated: {len(modules)} modules, {count} lessons.")

    if ROADMAP_FILE.exists() and not args.force:
        fail(
            f"{ROADMAP_FILE.name} already exists. Re-run with --force to overwrite. "
            "Note: progress.json is preserved either way."
        )

    data.setdefault("goal", "")
    data["installed_on"] = today()
    write_json(ROADMAP_FILE, data)
    LESSONS.mkdir(parents=True, exist_ok=True)

    # Progress survives roadmap replacement — a refreshed roadmap must not erase history.
    progress = read_json(PROGRESS_FILE)
    created_progress = progress is None
    if created_progress:
        write_json(PROGRESS_FILE, {"started_on": today(), "sessions": []})
        log("Created content/progress.json")
    else:
        log("Kept existing content/progress.json")

    emit(
        roadmap=str(ROADMAP_FILE),
        modules=len(modules),
        lessons=count,
        progress_created=created_progress,
        content_dir=str(CONTENT),
        next_step="python tools/site_build.py --open",
    )


if __name__ == "__main__":
    main()
