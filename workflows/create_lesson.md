# Create Lesson

**Objective:** Research and write one lesson page — concept, infographic, runnable code, a build
task, extensions and recall questions — and rebuild the site so it's ready to study. Done when the
lesson page renders correctly and Jack can start it immediately.

**When to use:** Jack says "write lesson 03-02", "write the next lesson", or sits down to study and
the next lesson doesn't exist yet.

## Inputs

| Input | Required | Description | Default |
|---|---|---|---|
| `lesson_id` | yes | Which lesson, e.g. `03-02` | the roadmap's next incomplete lesson |
| `depth` | no | `hybrid` (verify + 3–5 sources) or `deep` (primary sources, papers, wider reading) | hybrid |

If no id was given, run `python tools/site_build.py` and use the `next_lesson` field it returns.
Ask me for anything required that wasn't provided. Don't guess.

## Tools used

| Tool | Purpose | Costs money? |
|---|---|---|
| `tools/lesson_new.py` | Scaffolds the markdown file from the roadmap entry | No |
| `tools/site_build.py` | Renders the site | No |
| WebSearch / WebFetch | Research (built in, not a script) | No |
| `claude-api` skill | Current model IDs, pricing, API shape | No |

## Steps

1. Validate inputs — confirm `lesson_id` exists in `content/roadmap.json`.
2. **Research.** Hybrid: 3–6 searches to verify current model names, pricing, library versions and
   API shapes, plus 3–5 real links worth reading. Deep: add primary sources, official docs read in
   full via WebFetch, and papers where they genuinely help.
   **Anything touching Claude/Anthropic model IDs, pricing, or API parameters — load the
   `claude-api` skill and check. Never write those from memory; they change monthly.**
3. Run `python tools/lesson_new.py --lesson-id <id>`. Read the JSON on stdout — it returns the
   title, module, time budget and the build task from the roadmap.
4. Check the result. If `ok: false`, see **Failure handling** below.
5. Write the lesson body into the scaffolded file, replacing each `<!-- ... -->` hint. Keep the seven
   sections and their order — that shape is the pedagogy, not decoration.

   **Why this matters** — the hook. What can he do after this that he couldn't before? Concrete,
   plain language, no jargon. 2–3 short paragraphs.

   **The mental model** — the concept, plus **exactly one** infographic. Hand-authored inline SVG
   in a `<figure class="figure">` with a `<figcaption>`, `role="img"` and an `aria-label`. Draw the
   *mechanism* — where data flows, what talks to what, what changes between two options — never a
   labelled box that restates a noun. Structure in `currentColor`; `var(--accent)` reserved for the
   one element the lesson turns on. Label the arrows. Text 11–13px.

   **In practice** — annotated, runnable code he types himself. Small steps, each explained, output
   shown. Never a wall of code. Fence with a language for highlighting.

   **Build it** — the task in full, ending in a `Done when:` checklist of observable facts.

   **Free practice** — 1–3 free, no-credit-card tools that give extra hands-on reps on *this*
   lesson's idea: Exercism Python-track exercises matched to the concept, Python Tutor for
   stepping through code, browser sandboxes (Learn Git Branching), free API tiers or local models
   (Gemini free tier, Ollama), free datasets and no-key APIs (JSONPlaceholder). Say exactly what to
   do, in what order, and name any catch (data used for training, Windows quirks, locked
   exercises). Pick only what fits the lesson. Padding this section with generic links is
   worse than a single good one. Same WebFetch rule as resources.

   **Going deeper** — bullets, roughly ordered by difficulty, for a multi-hour session.

   **Check yourself** — 3–5 `<details markdown="1">` questions. Test *application*, not recall of
   definitions.

6. Fill in `resources:` in the frontmatter. **Every URL must be WebFetched successfully in this
   session before it goes in the file** — not merely remembered, and not merely seen in a search
   result snippet. A URL that reads plausibly is not a URL that resolves. If a fetch fails or the
   page is paywalled, find a free alternative or drop the resource; a broken link in a beginner's
   lesson costs more trust than a missing one.
7. Run `python tools/site_build.py --open`. If the lesson is missing from the output, the file is
   still all headings and comments — write the body.
8. Report back: the lesson title, the build task, the estimated time, and the page URL.

### Writing constraints

- **Assume no prior knowledge beyond earlier lessons.** Jack is a beginner at both programming and
  AI. First use of any term gets a plain-language definition.
- **The build task must be finishable in `core_minutes`.** If it isn't, cut scope — an unfinished
  build task breaks the streak logic and the habit.
- Second person, direct, no hype. Explain *why* before *how*.
- Prefer showing a mistake and its fix over stating a rule.

## Output

- **Deliverable:** `docs/lessons/<slug>.html`, reachable from the dashboard and, once pushed, live
  on GitHub Pages
- **Intermediates:** none — `content/lessons/<slug>.md` is durable source, not disposable

## Failure handling

| Symptom | Cause | Fix |
|---|---|---|
| `Lesson id ... is not in the roadmap` | Typo, or roadmap not installed | Check the `known_ids` list in the error payload |
| `already exists. Edit it, or pass --force` | Lesson was scaffolded before | Edit the existing file; only `--force` if genuinely restarting |
| Lesson missing from the built site | Body is still only headings + comments | `site_build.py` skips unwritten stubs by design — write the body |
| `frontmatter is not valid YAML` | Unescaped `:` or a stray `"` in a value | Wrap the value in double quotes; the tool escapes `"` to `'` on scaffold but not on later edits |
| `has no YAML frontmatter block` | The `---` header was deleted | Restore it; `id` is required and is the join key |

## Notes & learnings

Append here as you discover constraints, quirks, or better methods. Date each entry.

- 2026-08-15 — Built. `site_build.py` treats a file of only headings and HTML comments as
  unwritten and skips it, so scaffolding a lesson never puts a blank page on the site.
- 2026-08-15 — `<details>` needs `markdown="1"` for its body to render as markdown; without it the
  answer text passes through as raw text.
- 2026-08-15 — **Shipped a dead link in the very first lesson.** A PubMed URL for the Ericsson 1993
  deliberate-practice paper was written from memory; the id was wrong and the page 404'd. Jack
  found it, not me. Root cause: recalling a citation *feels* like knowing it, and academic URLs are
  exactly the shape that's easy to half-remember. Step 6 now requires a successful WebFetch of
  every URL before it's written. Also worth preferring: free full-text sources (PMC, official docs)
  over paywalled abstracts — a beginner who hits a paywall just stops reading.
- 2026-08-20 — Lesson 00-05 needed real API output to show. Installed `anthropic` into
  `.venv` and tried a probe call; `ANTHROPIC_API_KEY` in `.env` is present but **empty**
  (`len == 0`), so the SDK raised `TypeError: "Could not resolve authentication method..."`
  *before* any network request. Two takeaways: (a) that TypeError is the real, verified
  failure for a missing/blank key — a 401 `AuthenticationError` is a different failure that
  only happens once a key is actually sent, and the lesson now teaches the distinction;
  (b) when a live call isn't possible, model output shown in a lesson must be labelled as
  illustrative — it's nondeterministic anyway, so say so rather than implying a fixed answer.
  Uninstalled `anthropic` afterwards so the lesson's `pip install` step is a genuine install.
- 2026-10-04 — Added the **Free practice** section (Jack asked for free hands-on tools) and
  backfilled lessons 00-01 to 01-04. Verified free as of this date: Exercism (100% free; concept
  exercises like `little-sisters-vocab`, `card-games`, `making-the-grade`, `meltdown-mitigation`,
  `guidos-gorgeous-lasagna`, `currency-exchange`, `inventory-management`, `mecha-munch-management`),
  Python Tutor (no login), Learn Git Branching, MIT Missing Semester, Anki (free on Windows),
  JSONPlaceholder (no key), Gemini API free tier on Flash models (free-tier data may be used by
  Google — warn), Ollama (local models free; its cloud models mostly paid). Exercism's
  `docs/using/features/learning-mode` URL 404s, so don't link it. Good candidates to verify for
  later modules: SQLBolt / Kaggle datasets (06), Hugging Face free embeddings (09), Promptfoo (11),
  Neon/Supabase free Postgres (06/09), Render/Fly free tiers (14).
