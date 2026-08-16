"""Scaffold a lesson markdown file from its roadmap entry.

Creates content/lessons/<id>-<slug>.md pre-filled with frontmatter and the
six-section skeleton, so the agent writes content instead of boilerplate.
The section order is load-bearing: it's the pedagogical shape of every lesson.

Usage:
    python tools/lesson_new.py --lesson-id 03-02
    python tools/lesson_new.py --lesson-id 03-02 --force
"""

import argparse

from common import LESSONS, ROADMAP_FILE, emit, fail, log, read_json, slugify

SKELETON = """---
id: "{id}"
title: "{title}"
module: "{module}"
core_minutes: {core_minutes}
deep_minutes: {deep_minutes}
build: "{build}"
resources: []
---

## Why this matters

<!-- The hook. What can you do after this that you couldn't before? Plain language,
     no jargon, ideally a concrete scenario. 2-3 short paragraphs. -->

## The mental model

<!-- The concept itself, plus exactly one inline-SVG infographic wrapped in
     <figure class="figure"> ... <figcaption>. Use currentColor / the CSS custom
     properties (var(--accent), var(--ink-2), var(--rule)) so it works in both themes. -->

## In practice

<!-- Annotated, runnable code the reader types themselves. Small steps, each one
     explained. Show the output. Never a wall of code without commentary. -->

## Build it

<!-- The task in full: what to build, and a checklist of what "done" means.
     Must be small enough to finish inside the core time budget. -->

## Going deeper

<!-- Optional extensions for a long session. Bullet list of concrete additions,
     roughly ordered by difficulty. -->

## Check yourself

<!-- 3-5 recall questions, each as:
<details><summary>Question text?</summary>

Answer.

</details>
-->
"""


def main():
    ap = argparse.ArgumentParser(description="Create a lesson markdown stub from the roadmap.")
    ap.add_argument("--lesson-id", required=True, help="Lesson id as it appears in roadmap.json")
    ap.add_argument("--force", action="store_true", help="Overwrite an existing lesson file")
    args = ap.parse_args()

    roadmap = read_json(ROADMAP_FILE)
    if roadmap is None:
        fail("No content/roadmap.json. Run tools/roadmap_init.py first.")

    for module in roadmap.get("modules", []):
        for lesson in module.get("lessons", []):
            if lesson["id"] == args.lesson_id:
                break
        else:
            continue
        break
    else:
        known = [l["id"] for m in roadmap.get("modules", []) for l in m.get("lessons", [])]
        fail(
            f"Lesson id '{args.lesson_id}' is not in the roadmap.",
            known_ids=known[:40],
        )

    slug = lesson.get("slug") or f"{lesson['id']}-{slugify(lesson['title'])}"
    path = LESSONS / f"{slug}.md"

    if path.exists() and not args.force:
        fail(f"{path} already exists. Edit it, or pass --force to start over.")

    # Quotes would break the YAML frontmatter's double-quoted scalars.
    def esc(s):
        return str(s).replace('"', "'")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        SKELETON.format(
            id=lesson["id"],
            title=esc(lesson["title"]),
            module=module["id"],
            core_minutes=lesson.get("core_minutes", 50),
            deep_minutes=lesson.get("deep_minutes", 0),
            build=esc(lesson.get("build", "")),
        ),
        encoding="utf-8",
    )
    log(f"Created {path}")

    emit(
        path=str(path),
        lesson_id=lesson["id"],
        title=lesson["title"],
        module=module["id"],
        module_title=module["title"],
        summary=lesson.get("summary", ""),
        core_minutes=lesson.get("core_minutes", 50),
        deep_minutes=lesson.get("deep_minutes", 0),
        build=lesson.get("build", ""),
        next_step="Write the lesson body, then: python tools/site_build.py --open",
    )


if __name__ == "__main__":
    main()
