# Log Session Progress

**Objective:** Close out a study session — record what was built, advance the streak, rebuild the
site. Done when the dashboard reflects the session and Jack knows what's next.

**When to use:** Jack says he's finished a lesson, "log that", "I built X", or is backfilling a
session he forgot.

## Inputs

| Input | Required | Description | Default |
|---|---|---|---|
| `lesson_id` | yes | Which lesson | — |
| `minutes` | yes | Actual time spent | — |
| `status` | no | `complete` or `started` | complete |
| `artifact` | no | Path or URL of what he built | — |
| `note` | no | One line: what clicked, what didn't | — |
| `date` | no | `YYYY-MM-DD`, for backfilling | today |

Ask me for anything required that wasn't provided. Don't guess — in particular, don't estimate
`minutes`, and don't invent an `artifact` path.

## Tools used

| Tool | Purpose | Costs money? |
|---|---|---|
| `tools/progress_log.py` | Appends the session record | No |
| `tools/site_build.py` | Recomputes streak/progress and rerenders | No |

## Steps

1. Validate inputs — `lesson_id` and `minutes` are required. If Jack says he finished a lesson but
   hasn't mentioned what he built, **ask** before logging: the artifact is the point of the system,
   and a completion without one is worth querying rather than silently accepting.
2. If he genuinely didn't build anything, log it anyway without `--artifact`. It still counts
   toward the streak; it just won't appear on the portfolio. Say so, don't nag.
3. Run:
   `python tools/progress_log.py --lesson-id <id> --status <status> --minutes <n> --artifact <a> --note "<note>"`
   Read the JSON on stdout.
4. Check the result. If `ok: false`, see **Failure handling** below.
5. Run `python tools/site_build.py`.
6. Report back: the new streak, percent complete, what's next up, and whether that next lesson is
   already written. If it isn't, offer to write it now (`workflows/create_lesson.md`).

## Output

- **Deliverable:** updated `content/progress.json` + rebuilt `docs/`
- **Intermediates:** none

After a session, remind Jack to push if he hasn't:
`git add -A && git commit -m "Session: <lesson id>" && git push`
That both backs up the work and updates the live site. The public commit history is a second,
visible streak — worth keeping unbroken.

## Failure handling

| Symptom | Cause | Fix |
|---|---|---|
| `Lesson id ... is not in the roadmap` | Typo | Check `content/roadmap.json` |
| `--date must be YYYY-MM-DD` | Wrong date format | Reformat; no other format is accepted |
| `--minutes must be positive` | Zero or negative | Ask Jack for the real figure |
| Streak reads lower than expected | Two or more clear days between sessions | Working as designed — one clear day is forgiven, two is not. Backfill with `--date` if a real session went unlogged |

## Notes & learnings

Append here as you discover constraints, quirks, or better methods. Date each entry.

- 2026-08-15 — Built. `progress.json` is append-only and every dashboard number is recomputed from
  it at build time, so the two can never disagree. Logging the same lesson twice is harmless —
  completion is a set membership test, not a counter.
- 2026-08-15 — Streak rule: a run of consecutive days, alive if the most recent day is today *or*
  yesterday. Deliberately forgiving of one busy day, unforgiving of two.
