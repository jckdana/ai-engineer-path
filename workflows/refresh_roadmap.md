# Refresh Roadmap

**Objective:** Re-check the unwritten parts of the roadmap against what's actually true now, and
flag written lessons whose content has gone stale. Done when Jack has a short, honest list of
what changed and has approved any edits.

**When to use:** Roughly quarterly, or when Jack notices a lesson referencing something that no
longer exists (a renamed model, a dead library, a changed price).

## Inputs

| Input | Required | Description | Default |
|---|---|---|---|
| `since` | no | Date of the last refresh | `installed_on` in `content/roadmap.json` |
| `scope` | no | `upcoming` (unwritten lessons only) or `all` (also audit written ones) | upcoming |

Ask me for anything required that wasn't provided. Don't guess.

## Tools used

| Tool | Purpose | Costs money? |
|---|---|---|
| `tools/roadmap_init.py` | Reinstalls the edited roadmap | No |
| `tools/site_build.py` | Renders the site | No |
| WebSearch / WebFetch | Research (built in, not a script) | No |
| `claude-api` skill | Current model IDs, pricing, API shape | No |

## Steps

1. Read `content/roadmap.json` and `content/progress.json`. Note which lessons are complete —
   **completed lessons are history and are never renumbered or removed.**
2. Research what's changed since `since`:
   - Model lineups, IDs and pricing (load the `claude-api` skill — don't answer from memory).
   - Libraries named in upcoming lessons: still maintained? renamed? superseded?
   - Any genuinely new practice that deserves its own lesson, and any lesson the field has
     made irrelevant.
3. If `scope` is `all`, grep the written lessons in `content/lessons/` for model IDs, version
   numbers, prices and library names, and check each against step 2.
4. Produce a short diff-style report for Jack — **do not edit anything yet**:
   - Lessons to add, with where they slot in
   - Lessons to retitle or rescope
   - Lessons to drop (only unwritten, uncompleted ones)
   - Written lessons with stale facts, and the specific line that's wrong
5. On approval, edit `.tmp/roadmap_draft.json` and run
   `python tools/roadmap_init.py --from .tmp/roadmap_draft.json --force`.
   **Keep every existing lesson id stable** — ids are the join key to `progress.json` and to the
   lesson filenames. New lessons take new ids, even if that breaks numerical order within a module.
6. Check the result. If `ok: false`, see **Failure handling** below.
7. For each stale written lesson, edit its markdown directly — don't rescaffold, that would
   discard the writing.
8. Run `python tools/site_build.py --open`.
9. Report back: what changed, what was left alone, and the date of this refresh.

## Output

- **Deliverable:** updated `content/roadmap.json`, edited lesson files, rebuilt `docs/`
- **Intermediates:** `.tmp/roadmap_draft.json` — disposable

## Failure handling

| Symptom | Cause | Fix |
|---|---|---|
| A completed lesson vanished from the roadmap page | Its id was changed or removed | Restore the original id. Progress records survive, but they orphan without a matching roadmap entry |
| A lesson page persists after removal from the roadmap | `docs/lessons/` isn't pruned on rebuild | Delete the stale `.html` by hand, or delete `docs/` entirely and rebuild |
| `Duplicate lesson id` | A new lesson reused an id | Give it a fresh one; ids need not be contiguous |

## Notes & learnings

Append here as you discover constraints, quirks, or better methods. Date each entry.

- 2026-08-15 — Built. Lesson ids are permanent. `progress.json`, the lesson filename slug and the
  roadmap all join on them; renaming an id silently orphans study history rather than erroring.
- 2026-08-15 — `site_build.py` writes but never deletes inside `docs/`. Removing a lesson leaves an
  orphan HTML file until `docs/` is deleted and rebuilt. Harmless locally (nothing links to it) but
  it stays live on GitHub Pages until cleaned, so do a clean rebuild after any removal.
