# AI Engineer Path

A self-directed curriculum for going from beginner to AI engineer — and the system that keeps me
doing it.

Lessons are researched and written on demand, rendered as a static site with infographics and
runnable code. Every lesson ends in something built. Progress is tracked as a streak and a
portfolio, so consistency is visible and the evidence accumulates.

**Live site:** https://jckdana.github.io/ai-engineer-path

---

## The idea

Most self-taught curricula die in month two, because progress is invisible. You watch a tutorial,
feel like you understood it, and three weeks later can't write a line of it from memory.

So this system has one rule: **a lesson isn't done when you finish reading it, it's done when
something runs.** Every lesson ships an artifact. After six months that's not eighty pages of
notes — it's eighty small programs, which is a portfolio.

Two counters follow from that rule:

- a **streak**, which measures showing up (survives one missed day, not two)
- a **portfolio**, which measures what got built (only sessions that shipped something appear)

They're deliberately separate. You can have an honest reading day without inflating your evidence.

---

## Daily loop

```
                 ┌──────────────────────────────────────────┐
                 │                                          │
  ask Claude ──▶ lesson page ──▶ build it ──▶ log it ──▶ push
  "write the      read ~20min     ~20-30min    1 command   1 command
   next lesson"                   an artifact
```

**1. Get the lesson.** In Claude Code, from this folder:

```
write the next lesson
```

Claude reads the roadmap, researches the topic, writes the page, and rebuilds the site.

**2. Study it.** Open the site — locally at `docs/index.html`, or live on GitHub Pages. The
dashboard tells you what's next. Read the lesson, type the code, do the build task.

**3. Log it.** From this folder, in a terminal:

```bash
python tools/progress_log.py --lesson-id 00-01 --status complete \
    --minutes 45 --artifact ./builds/my_thing.py --note "what clicked"
python tools/site_build.py --open
```

The exact command, with the right lesson id already filled in, is printed at the bottom of every
lesson page. Or just tell Claude "I finished 00-01, took 45 minutes, built X" and it does it.

**4. Push.** Backs up the work and updates the live site:

```bash
git add -A
git commit -m "Session: 00-01"
git push
```

---

## Setup on a new machine

```bash
git clone https://github.com/jckdana/ai-engineer-path.git
cd ai-engineer-path
pip install -r requirements.txt
python tools/site_build.py --open
```

Needs Python 3.10+ and git. An `ANTHROPIC_API_KEY` in `.env` is needed from the API lessons
onward — copy `.env.example` to `.env` and fill it in. `.env` is gitignored and must stay that way.

---

## How it's built

This follows the **WAT framework** — Workflows, Agents, Tools — described in
[CLAUDE.md](CLAUDE.md). The split is the point: probabilistic AI does the reasoning,
deterministic Python does the execution.

| Layer | What it is | Where |
|---|---|---|
| **Workflows** | Markdown SOPs. What to do, in what order, and how to recover | [`workflows/`](workflows/) |
| **Agent** | Claude. Reads the workflow, researches, writes lessons, calls the tools | — |
| **Tools** | Python scripts. Validation, rendering, bookkeeping — anything that must be exact | [`tools/`](tools/) |

Claude writes the prose and picks what to teach. It never computes a streak or hand-writes HTML;
those are code, so they're always right.

### Directory map

```
content/            ← source of truth. Edit these.
  roadmap.json        the whole path: modules, lessons, build tasks
  progress.json       append-only session log; every stat derives from it
  lessons/*.md        one markdown file per lesson, YAML frontmatter + body

templates/          ← the design layer
  app.css             the entire stylesheet, light + dark
  *.html.j2           Jinja2 templates for each page type

tools/              ← deterministic execution
  common.py           shared paths + JSON helpers
  streak.py           streak math, shared by the two tools that need it
  roadmap_init.py     validate + install a roadmap
  lesson_new.py       scaffold a lesson file from its roadmap entry
  site_build.py       render everything into docs/
  progress_log.py     append a session record

workflows/          ← the SOPs Claude follows
builds/             ← where lesson artifacts live
docs/               ← GENERATED. Never hand-edit. GitHub Pages serves this.
.tmp/               ← disposable intermediates
```

### The tool contract

Every script in `tools/` behaves identically, which is what makes them safe to chain:

- arguments via `argparse`
- **exactly one JSON object on stdout** — so Claude can parse the result
- human-readable progress and errors on stderr
- exit `0` on success, `1` on handled failure with `{"ok": false, "error": "..."}`

### Data model

Lesson ids (`MM-NN`) are the join key between the roadmap, the progress log and the lesson
filenames. **They're permanent** — renaming one orphans its history rather than erroring.

`progress.json` is append-only. Streak, percentage, hours and the portfolio are all recomputed
from it at build time, so the dashboard can never drift out of sync with reality.

---

## The workflows

| Workflow | When |
|---|---|
| [`build_learning_roadmap.md`](workflows/build_learning_roadmap.md) | Once, at the start — research and install the full path |
| [`create_lesson.md`](workflows/create_lesson.md) | Every session — research and write one lesson |
| [`log_session_progress.md`](workflows/log_session_progress.md) | End of every session |
| [`refresh_roadmap.md`](workflows/refresh_roadmap.md) | Quarterly — AI tooling moves fast; re-check what's stale |

Each one carries a dated **Notes & learnings** section. When something breaks, the fix goes in the
tool and the lesson goes in the workflow, so the same mistake doesn't happen twice.

---

## Design notes

- **No build step, no npm, no framework.** Python renders static HTML. The point is to spend time
  learning, not maintaining the thing you learn with.
- **Infographics are hand-authored inline SVG**, themed with `currentColor` and CSS custom
  properties — works offline, adapts to light and dark, no runtime.
- **One chart palette**, a single sequential blue ramp, since every chart here plots one series.
  Status green is reserved for completion and never reused.
- **Unwritten lessons never publish.** A scaffolded file that's still only headings and comments is
  skipped by the renderer, so the site never shows a blank page.
