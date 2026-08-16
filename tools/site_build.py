"""Render content/ into a browsable static site at docs/.

Everything in docs/ is generated: this tool rebuilds it from roadmap.json,
progress.json and the lesson markdown files. Run it after any change. It is
idempotent and takes no destructive action outside docs/.

The output is committed rather than gitignored, because GitHub Pages serves it
straight from the docs/ folder — so pushing publishes the site.

Usage:
    python tools/site_build.py
    python tools/site_build.py --open
"""

import argparse
import re
import shutil
import webbrowser
from datetime import date, datetime, timedelta
from urllib.parse import urlparse

from common import (
    LESSONS,
    PROGRESS_FILE,
    ROADMAP_FILE,
    SITE,
    TEMPLATES,
    emit,
    fail,
    log,
    read_json,
    slugify,
)
from streak import current_streak, longest_streak, streak_line

MD_EXTENSIONS = [
    "fenced_code",
    "codehilite",
    "tables",
    "attr_list",
    "sane_lists",
    "md_in_html",
    "smarty",
]
MD_CONFIG = {"codehilite": {"guess_lang": False, "cssclass": "codehilite"}}

# Minutes -> heatmap step. Deliberately coarse: five levels is all the eye reads.
HEAT_BREAKS = [(1, 1), (30, 2), (60, 3), (120, 4)]


def _require(module_name, pip_name):
    try:
        return __import__(module_name)
    except ImportError:
        fail(f"{pip_name} is not installed. Run: pip install -r requirements.txt")


# ----------------------------------------------------------------- content ---


def split_frontmatter(text, path):
    """Return (metadata dict, markdown body). Frontmatter is required."""
    yaml = _require("yaml", "pyyaml")
    if not text.startswith("---"):
        fail(f"{path.name} has no YAML frontmatter block.")
    parts = text.split("\n---", 1)
    if len(parts) != 2:
        fail(f"{path.name} has an unterminated frontmatter block.")
    try:
        meta = yaml.safe_load(parts[0].lstrip("-\n")) or {}
    except Exception as e:
        fail(f"{path.name}: frontmatter is not valid YAML: {e}")
    if not isinstance(meta, dict):
        fail(f"{path.name}: frontmatter must be a mapping.")
    return meta, parts[1].lstrip("\n")


def strip_comments(body):
    """Drop the HTML authoring hints from an unwritten stub so they never render."""
    return re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)


def has_content(body):
    """True if the author wrote prose, not just the skeleton's headings and hints.

    A fresh stub is nothing but `## headings` and <!-- comments -->, so both are
    discarded before asking whether anything is left.
    """
    prose = strip_comments(body)
    return any(
        line.strip() and not line.lstrip().startswith("#") for line in prose.splitlines()
    )


def load_lessons():
    """Map lesson_id -> {meta, body_md} for every written lesson file."""
    out = {}
    if not LESSONS.exists():
        return out
    for path in sorted(LESSONS.glob("*.md")):
        meta, body = split_frontmatter(path.read_text(encoding="utf-8"), path)
        lid = str(meta.get("id", "")).strip()
        if not lid:
            fail(f"{path.name}: frontmatter is missing 'id'.")
        # A scaffolded-but-unwritten file shouldn't masquerade as a finished lesson.
        prose = strip_comments(body)
        if not has_content(prose):
            log(f"  skipping {path.name} — scaffolded but not written yet")
            continue
        out[lid] = {"meta": meta, "body": prose, "path": path}
    return out


def render_markdown(body):
    markdown = _require("markdown", "markdown")
    html = markdown.markdown(body, extensions=MD_EXTENSIONS, extension_configs=MD_CONFIG)
    # Wide tables must scroll inside their own box rather than push the page sideways.
    html = html.replace("<table>", '<div class="table-scroll"><table>')
    html = html.replace("</table>", "</table></div>")
    return html


# -------------------------------------------------------------------- svg ---


def ring_svg(pct, done, total):
    """Progress meter. Track is a lighter step of the fill's own ramp."""
    size, stroke = 132, 13
    r = (size - stroke) / 2
    c = 2 * 3.141592653589793 * r
    filled = c * min(max(pct, 0), 100) / 100
    return f"""<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" role="img"
     aria-label="{pct} percent of the roadmap complete, {done} of {total} lessons">
  <circle cx="{size/2}" cy="{size/2}" r="{r}" fill="none"
          stroke="var(--accent-wash)" stroke-width="{stroke}"/>
  <circle cx="{size/2}" cy="{size/2}" r="{r}" fill="none"
          stroke="var(--accent)" stroke-width="{stroke}" stroke-linecap="round"
          stroke-dasharray="{filled:.2f} {c - filled:.2f}"
          transform="rotate(-90 {size/2} {size/2})"/>
  <text x="{size/2}" y="{size/2 - 2}" text-anchor="middle" dominant-baseline="central"
        font-family="system-ui, sans-serif" font-size="27" font-weight="620"
        letter-spacing="-0.5" fill="var(--ink)">{pct}%</text>
  <text x="{size/2}" y="{size/2 + 22}" text-anchor="middle" dominant-baseline="central"
        font-family="system-ui, sans-serif" font-size="11.5" fill="var(--muted)">of roadmap</text>
</svg>"""


def heatmap_svg(minutes_by_date, weeks=12, ref=None):
    """GitHub-style day grid. Sequential single hue; empty days are chrome, not data."""
    ref = ref or date.today()
    cell, gap = 13, 3.5
    step = cell + gap
    pad_left, pad_top = 26, 16

    # Columns are weeks running Monday->Sunday; the last column contains today.
    last_sunday = ref + timedelta(days=(6 - ref.weekday()))
    start = last_sunday - timedelta(weeks=weeks - 1, days=6)

    rects, month_labels, seen_months = [], [], set()
    for w in range(weeks):
        for d in range(7):
            day = start + timedelta(weeks=w, days=d)
            x = pad_left + w * step
            y = pad_top + d * step
            if day > ref:
                continue
            mins = minutes_by_date.get(day.isoformat(), 0)
            level = 0
            for threshold, lv in HEAT_BREAKS:
                if mins >= threshold:
                    level = lv
            label = f"{day.strftime('%a %d %b %Y')}: " + (
                f"{mins} min" if mins else "nothing logged"
            )
            rects.append(
                f'<rect x="{x}" y="{y:.1f}" width="{cell}" height="{cell}" rx="2.5" '
                f'fill="var(--heat-{level})"><title>{label}</title></rect>'
            )
        month = (start + timedelta(weeks=w)).strftime("%b")
        if month not in seen_months and w < weeks - 1:
            seen_months.add(month)
            month_labels.append(
                f'<text x="{pad_left + w * step}" y="10" font-size="10.5" '
                f'fill="var(--muted)" font-family="system-ui, sans-serif">{month}</text>'
            )

    for i, name in ((0, "Mon"), (2, "Wed"), (4, "Fri")):
        y = pad_top + i * step + cell / 2
        month_labels.append(
            f'<text x="0" y="{y:.1f}" font-size="10.5" fill="var(--muted)" '
            f'dominant-baseline="central" font-family="system-ui, sans-serif">{name}</text>'
        )

    w_total = pad_left + weeks * step
    h_total = pad_top + 7 * step
    return (
        f'<svg class="heatmap" viewBox="0 0 {w_total:.0f} {h_total:.0f}" '
        f'width="{w_total:.0f}" height="{h_total:.0f}" role="img" '
        f'aria-label="Study activity over the last {weeks} weeks">'
        + "".join(month_labels)
        + "".join(rects)
        + "</svg>"
    )


# ------------------------------------------------------------------ build ---


def artifact_href(artifact):
    """Links resolve from docs/*.html, one level above which is the repo root."""
    if not artifact:
        return ""
    if urlparse(artifact).scheme in ("http", "https"):
        return artifact
    return "../" + artifact.replace("\\", "/").lstrip("./")


def main():
    ap = argparse.ArgumentParser(description="Build the static learning site.")
    ap.add_argument("--open", action="store_true", help="Open the dashboard when done")
    args = ap.parse_args()

    jinja = _require("jinja2", "jinja2")
    pygments_formatters = __import__("pygments.formatters", fromlist=["HtmlFormatter"])

    roadmap = read_json(ROADMAP_FILE)
    if roadmap is None:
        fail("No content/roadmap.json. Run tools/roadmap_init.py first.")
    progress = read_json(PROGRESS_FILE) or {"sessions": []}
    sessions = progress.get("sessions", [])

    written = load_lessons()
    log(f"Found {len(written)} written lesson file(s).")

    completed = {s["lesson_id"] for s in sessions if s.get("status") == "complete"}
    minutes_by_date = {}
    for s in sessions:
        minutes_by_date[s["date"]] = minutes_by_date.get(s["date"], 0) + int(s.get("minutes", 0))
    dates = set(minutes_by_date)

    # --- assemble the ordered lesson list, deciding each one's state ---------
    modules, flat = [], []
    next_id = None
    for m in roadmap.get("modules", []):
        lessons = []
        for l in m.get("lessons", []):
            slug = l.get("slug") or f"{l['id']}-{slugify(l['title'])}"
            done = l["id"] in completed
            if not done and next_id is None:
                next_id = l["id"]
            item = {
                **l,
                "slug": slug,
                "written": l["id"] in written,
                "done": done,
                "state": "done" if done else "todo",
                "core_minutes": l.get("core_minutes", 50),
            }
            lessons.append(item)
            flat.append((m, item))
        modules.append(
            {
                **m,
                "lessons": lessons,
                "done": sum(1 for x in lessons if x["done"]),
            }
        )

    for _m, item in flat:
        if item["id"] == next_id:
            item["state"] = "next"

    total = len(flat)
    done_n = len(completed & {i["id"] for _m, i in flat})
    pct = round(100 * done_n / total) if total else 0
    total_minutes = sum(int(s.get("minutes", 0)) for s in sessions)

    stats = {
        "done": done_n,
        "total": total,
        "remaining": total - done_n,
        "pct": pct,
        "streak": current_streak(dates),
        "best_streak": longest_streak(dates),
        "hours": round(total_minutes / 60, 1),
        "sessions": len(sessions),
        "artifacts": sum(1 for s in sessions if s.get("artifact")),
    }

    by_id = {i["id"]: (m, i) for m, i in flat}
    next_lesson = by_id[next_id][1] if next_id else None

    # --- portfolio entries: newest first, only sessions that shipped --------
    entries = []
    for s in sorted(sessions, key=lambda s: s["date"], reverse=True):
        if not s.get("artifact"):
            continue
        m_i = by_id.get(s["lesson_id"])
        entries.append(
            {
                "date": s["date"],
                "title": m_i[1]["title"] if m_i else s["lesson_id"],
                "slug": m_i[1]["slug"] if m_i else "",
                "written": bool(m_i and m_i[1]["written"]),
                "build": m_i[1].get("build", "") if m_i else "",
                "note": s.get("note", ""),
                "artifact": s["artifact"],
                "artifact_href": artifact_href(s["artifact"]),
            }
        )

    # --- render --------------------------------------------------------------
    env = jinja.Environment(
        loader=jinja.FileSystemLoader(str(TEMPLATES)),
        autoescape=jinja.select_autoescape(["html", "j2"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    SITE.mkdir(parents=True, exist_ok=True)
    (SITE / "assets").mkdir(exist_ok=True)
    (SITE / "lessons").mkdir(exist_ok=True)

    base_ctx = {
        "site_title": roadmap.get("title", "Learning path"),
        "roadmap": roadmap,
        "stats": stats,
        "built_at": datetime.now().strftime("%d %b %Y, %H:%M"),
    }
    markup = jinja.Markup if hasattr(jinja, "Markup") else __import__("markupsafe").Markup

    def write(name, template, **ctx):
        path = SITE / name
        path.write_text(env.get_template(template).render(**base_ctx, **ctx), encoding="utf-8")
        return path

    write(
        "index.html",
        "index.html.j2",
        page="index",
        rel="",
        next_lesson=next_lesson,
        streak_line=streak_line(dates, stats["streak"]),
        ring_svg=markup(ring_svg(pct, done_n, total)),
        heatmap_svg=markup(heatmap_svg(minutes_by_date)),
        recent_builds=entries[:3],
    )
    write("roadmap.html", "roadmap.html.j2", page="roadmap", rel="", modules=modules)
    write("portfolio.html", "portfolio.html.j2", page="portfolio", rel="", entries=entries)

    completed_dates = {}
    for s in sessions:
        if s.get("status") == "complete":
            completed_dates.setdefault(s["lesson_id"], s["date"])

    pages = 0
    for idx, (module, item) in enumerate(flat):
        if not item["written"]:
            continue
        entry = written[item["id"]]
        meta = entry["meta"]
        lesson = {
            **item,
            "title": meta.get("title", item["title"]),
            "core_minutes": meta.get("core_minutes", item["core_minutes"]),
            "deep_minutes": meta.get("deep_minutes", item.get("deep_minutes", 0)),
            "build": meta.get("build", item.get("build", "")),
            "resources": [
                {**r, "domain": urlparse(r.get("url", "")).netloc.replace("www.", "")}
                for r in (meta.get("resources") or [])
                if r.get("url")
            ],
        }
        prev_item = flat[idx - 1][1] if idx > 0 else None
        next_item = flat[idx + 1][1] if idx + 1 < len(flat) else None

        path = SITE / "lessons" / f"{item['slug']}.html"
        path.write_text(
            env.get_template("lesson.html.j2").render(
                **base_ctx,
                page="lesson",
                rel="../",
                module=module,
                lesson=lesson,
                state=item["state"],
                completed_on=completed_dates.get(item["id"], ""),
                body=markup(render_markdown(entry["body"])),
                prev=prev_item,
                next=next_item,
            ),
            encoding="utf-8",
        )
        pages += 1

    # --- assets --------------------------------------------------------------
    shutil.copyfile(TEMPLATES / "app.css", SITE / "assets" / "app.css")

    HtmlFormatter = pygments_formatters.HtmlFormatter
    light = HtmlFormatter(style="friendly").get_style_defs(".codehilite")
    dark_sel = HtmlFormatter(style="native")
    code_css = "\n".join(
        [
            "/* Generated by tools/site_build.py — do not edit. */",
            light,
            '@media (prefers-color-scheme: dark) {',
            dark_sel.get_style_defs(':root:not([data-theme="light"]) .codehilite'),
            "}",
            dark_sel.get_style_defs(':root[data-theme="dark"] .codehilite'),
        ]
    )
    (SITE / "assets" / "code.css").write_text(code_css, encoding="utf-8")

    # Tell GitHub Pages to serve the files as-is rather than running Jekyll over them.
    # Written on every build so it survives deleting docs/ and rebuilding.
    (SITE / ".nojekyll").write_text("", encoding="utf-8")

    log(f"Built {pages} lesson page(s) + 3 index pages into {SITE}")

    index = SITE / "index.html"
    if args.open:
        webbrowser.open(index.resolve().as_uri())

    emit(
        site=str(SITE),
        index=str(index),
        url=index.resolve().as_uri(),
        lesson_pages=pages,
        lessons_total=total,
        lessons_written=len(written),
        lessons_complete=done_n,
        percent=pct,
        streak=stats["streak"],
        next_lesson=next_id,
    )


if __name__ == "__main__":
    main()
