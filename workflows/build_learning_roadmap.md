# Build Learning Roadmap

**Objective:** Research what an AI engineer actually needs to know right now, turn it into a
module/lesson tree, and install it as `content/roadmap.json` so the whole path is visible on the
roadmap page. Done when Jack has approved the tree and the site builds with every lesson listed.

**When to use:** Once, at the start. Also when Jack wants to restructure the path from scratch
(for an incremental correction use `refresh_roadmap.md` instead — it preserves more).

## Inputs

| Input | Required | Description | Default |
|---|---|---|---|
| `goal` | yes | The target role, in Jack's words | AI Engineer (technical depth) |
| `level` | yes | Starting point | Beginner at both programming and AI |
| `session_minutes` | no | Typical core session length | 50 |
| `horizon` | no | Rough months to job-ready | 6–9 |

Ask me for anything required that wasn't provided. Don't guess.

## Tools used

| Tool | Purpose | Costs money? |
|---|---|---|
| `tools/roadmap_init.py` | Validates and installs the roadmap; creates `progress.json` | No |
| `tools/site_build.py` | Renders the site | No |
| WebSearch / WebFetch | Research (built in, not a script) | No |

## Steps

1. Validate inputs — confirm goal, level and cadence. If any are missing, ask.
2. **Research before writing anything.** Aim for 8–15 searches across these angles:
   - Current AI/LLM engineer job postings — what's listed under "requirements", repeatedly.
   - Official docs for the tools that will actually be used (Anthropic docs, FastAPI, a vector
     store, an eval framework). Confirm they still exist and note current names.
   - What's changed in the last 6 months. This field moves fast; a roadmap written from memory
     will contain dead libraries. **Load the `claude-api` skill before writing any lesson that
     touches model IDs, pricing, or API shape** — never write those from memory.
   - Common failure modes for self-taught engineers, so weak spots get their own lessons.
3. Draft the tree. Constraints that matter:
   - Sequence so a real model gets called inside the first two weeks. Motivation dies in a
     fundamentals-only opening.
   - Every lesson gets a `build` — one concrete, checkable artifact, finishable inside
     `core_minutes`. If you can't name the artifact, the lesson is too vague; split it.
   - `core_minutes` 40–60. `deep_minutes` is the ceiling with extensions, usually 2–3×.
   - 5–7 lessons per module. Module `outcome` states what Jack can *do* afterward, not what
     he'll have "learned about".
   - Lesson ids are `MM-NN`, zero-padded, matching the module id.
4. **Show Jack the module titles, outcomes and lesson titles before installing.** This is the
   spine of the next six months — do not skip the review. Revise until he's happy.
5. Write the approved tree to `.tmp/roadmap_draft.json` in the schema below.
6. Run `python tools/roadmap_init.py --from .tmp/roadmap_draft.json`. Read the JSON on stdout.
   Add `--force` only when knowingly replacing an existing roadmap.
7. Check the result. If `ok: false`, see **Failure handling** below.
8. Run `python tools/site_build.py --open`.
9. Report back: module count, lesson count, the URL, and which lesson to write first.

### Roadmap schema

```json
{
  "title": "AI Engineer Path",
  "goal": "One sentence naming the outcome.",
  "modules": [
    {
      "id": "00",
      "title": "Getting set up",
      "outcome": "What he can do after this module.",
      "lessons": [
        {
          "id": "00-01",
          "title": "How to learn this without burning out",
          "summary": "One line — used when scaffolding the lesson.",
          "core_minutes": 40,
          "deep_minutes": 90,
          "build": "The concrete artifact this lesson produces."
        }
      ]
    }
  ]
}
```

`slug` is derived by the tool — don't set it.

## Output

- **Deliverable:** `content/roadmap.json` + the rebuilt site at `docs/index.html`
- **Intermediates:** `.tmp/roadmap_draft.json` — disposable

## Failure handling

| Symptom | Cause | Fix |
|---|---|---|
| `Duplicate lesson id` | Two lessons share an id | Renumber; ids must be unique across the whole roadmap, not just within a module |
| `roadmap.json already exists` | Guard against silent overwrite | Confirm with Jack, then re-run with `--force`. `progress.json` is preserved regardless |
| `core_minutes must be a positive integer` | String or 0 in the draft | Fix the draft JSON |
| `Roadmap needs a non-empty 'modules' array` | Malformed draft | Re-read the schema above |

## Notes & learnings

Append here as you discover constraints, quirks, or better methods. Date each entry.

- 2026-08-15 — Built. `roadmap_init.py` deliberately never touches an existing `progress.json`, so
  a roadmap replacement can't wipe study history. Lesson ids are the join key between roadmap,
  progress and lesson files — renaming an id orphans its history, so treat ids as permanent.
