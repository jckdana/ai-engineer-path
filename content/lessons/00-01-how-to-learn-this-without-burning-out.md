---
id: "00-01"
title: "How to learn this without burning out"
module: "00"
core_minutes: 40
deep_minutes: 90
build: "Log your first session and commit the repo to git."
resources:
  - title: "Revisiting deliberate practice — what the evidence actually shows"
    url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC6731745/"
  - title: "Spaced practice, and why cramming loses"
    url: "https://citl.indiana.edu/teaching-resources/evidence-based/spaced-practice.html"
  - title: "Pro Git — About version control"
    url: "https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control"
---

## Why this matters

Most people who set out to learn AI engineering quit in month two. Not because it's
too hard — because they can't tell whether they're making progress. They watch a
tutorial, feel like they understood it, and three weeks later can't write a line of
it from memory. That gap between *feeling* competent and *being* competent is the
thing that kills momentum.

This lesson is the shortest one you'll do, and it's the one that decides whether the
other seventy-nine happen. You're going to set up a loop where progress is visible
and undeniable, because it's measured in things that exist rather than hours spent.

By the end you'll have logged a session, seen your streak start, and put this whole
repo under version control — which, conveniently, is also your first real use of git.

## The mental model

Reading a lesson doesn't teach you anything durable. Building something with it does.
So this system treats reading as the *setup* and the build task as the *lesson* — a
lesson isn't finished when you reach the bottom of the page, it's finished when
something runs.

That single rule is what makes the rest work. Because every lesson ends in an
artifact, the log of your sessions is automatically a log of things you made. Six
months in, you don't have eighty pages of notes — you have eighty small programs.

<figure class="figure">
<svg viewBox="0 0 720 240" role="img" aria-label="The study loop: reading feeds a build task, which produces an artifact; logging it advances both a streak and a portfolio, and the streak is what brings you back tomorrow.">
  <defs>
    <marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="currentColor"/>
    </marker>
    <marker id="ar-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/>
    </marker>
  </defs>

  <g font-family="system-ui, sans-serif" font-size="13" fill="currentColor">

    <!-- main row -->
    <rect x="20"  y="110" width="140" height="56" rx="9" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.45"/>
    <text x="90"  y="132" text-anchor="middle" font-weight="600">Read</text>
    <text x="90"  y="151" text-anchor="middle" font-size="11.5" opacity="0.65">~20 minutes</text>

    <rect x="200" y="110" width="140" height="56" rx="9" fill="var(--accent-tint)" stroke="var(--accent)" stroke-width="1.8"/>
    <text x="270" y="132" text-anchor="middle" font-weight="600">Build</text>
    <text x="270" y="151" text-anchor="middle" font-size="11.5" opacity="0.65">~20 minutes</text>

    <rect x="380" y="110" width="140" height="56" rx="9" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.45"/>
    <text x="450" y="132" text-anchor="middle" font-weight="600">Log it</text>
    <text x="450" y="151" text-anchor="middle" font-size="11.5" opacity="0.65">~1 minute</text>

    <!-- outputs -->
    <rect x="560" y="54"  width="140" height="48" rx="9" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.45"/>
    <text x="630" y="83"  text-anchor="middle" font-weight="600">Streak</text>

    <rect x="560" y="174" width="140" height="48" rx="9" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.45"/>
    <text x="630" y="203" text-anchor="middle" font-weight="600">Portfolio</text>

    <!-- flow -->
    <line x1="164" y1="138" x2="194" y2="138" stroke="currentColor" stroke-width="1.6" marker-end="url(#ar)"/>
    <line x1="344" y1="138" x2="374" y2="138" stroke="var(--accent)" stroke-width="2" marker-end="url(#ar-a)"/>
    <text x="359" y="103" text-anchor="middle" font-size="11" fill="var(--accent)" font-weight="600">an artifact</text>

    <path d="M524 132 C 545 132, 545 78, 554 78" fill="none" stroke="currentColor" stroke-width="1.6" marker-end="url(#ar)"/>
    <path d="M524 144 C 545 144, 545 198, 554 198" fill="none" stroke="currentColor" stroke-width="1.6" marker-end="url(#ar)"/>

    <!-- feedback -->
    <path d="M630 50 C 630 8, 90 8, 90 106" fill="none" stroke="currentColor" stroke-width="1.6"
          stroke-dasharray="5 4" opacity="0.6" marker-end="url(#ar)"/>
    <text x="360" y="24" text-anchor="middle" font-size="11.5" opacity="0.7">brings you back tomorrow</text>

  </g>
</svg>
<figcaption>The build step is the only one that creates something. Everything to its right is
a consequence of it — which is why a lesson you only read doesn't count as done.</figcaption>
</figure>

Three things follow from this diagram, and they're worth stating plainly:

**A short session that ships beats a long one that doesn't.** Twenty minutes ending in
a working script moves you further than two hours of reading. If you only have twenty
minutes, do the build task and skim the rest.

**Missing a day is fine. Missing three is the problem.** The streak counter gives you a
one-day grace period on purpose — it survives a busy Tuesday. What it won't survive is
a weekend of avoidance, and that's deliberate: two clear days is the point where people
quietly stop.

**Confusion is the signal you're in the right place.** If a lesson feels obvious you're
probably not learning much. The build task is where you find out what you actually
understood.

## In practice

Everything in this system runs from the repo root as a single command. There are only
three you need, and you'll use them in this order.

Ask Claude to write the next lesson for you:

```text
write lesson 00-02
```

That reads the roadmap, researches the topic, and produces the page. When you've
finished a lesson and its build task, log it:

```bash
python tools/progress_log.py --lesson-id 00-01 --status complete \
    --minutes 40 --artifact ./README.md --note "set up the loop"
```

Then rebuild the site so the dashboard reflects it:

```bash
python tools/site_build.py --open
```

That's the whole interface. The flags are worth knowing:

| Flag | What it does |
| --- | --- |
| `--lesson-id` | Which lesson. Must match an id in the roadmap. |
| `--status` | `complete` when the build task runs; `started` if you got partway. |
| `--minutes` | Actual time spent. Drives the heatmap intensity, nothing else. |
| `--artifact` | Path or URL of what you built. **No artifact, no portfolio entry.** |
| `--note` | One line to your future self. What clicked, what didn't. |
| `--date` | Backfill a session you forgot to log. Defaults to today. |

A session with no `--artifact` still counts toward your streak — sometimes a lesson
is genuinely just reading. But it won't appear on the portfolio page, and that
asymmetry is intentional.

## Build it

Two small things, both of which you'll use every day from here on.

**1. Put this repo under version control.** From the repo root:

```bash
git init
git add .
git commit -m "Set up AI engineer learning system"
```

If `git` isn't recognised, install it from [git-scm.com](https://git-scm.com/downloads),
close your terminal, and open a new one.

**2. Log this session.**

```bash
python tools/progress_log.py --lesson-id 00-01 --status complete \
    --minutes 40 --artifact ./README.md --note "first session"
python tools/site_build.py --open
```

Done when:

- `git log` shows one commit
- The dashboard reads **1 day** streak
- The roadmap page shows lesson 00-01 with a green dot and a **Done** tag
- The portfolio page has exactly one entry on it

## Going deeper

- Write a short `README.md` at the repo root saying what you're doing and why. In six
  months it's the first thing anyone reads when you share this.
- Create a free GitHub account, make an empty repository, and push this one to it.
  Public is better — visible consistency is worth more than a polished private repo.
- Open `content/progress.json` and read it. It's just a list of sessions; every number
  on the dashboard is computed from it. Understanding that file means you'll never
  wonder whether the dashboard is lying to you.
- Decide your actual schedule and write it down — which days, what time, where. "When I
  get a chance" is how this dies.

## Check yourself

<details markdown="1"><summary>When is a lesson finished?</summary>

When the build task runs — not when you reach the bottom of the page. Reading is the
setup; the artifact is the evidence.

</details>

<details markdown="1"><summary>You studied Monday and Tuesday, skipped Wednesday, and it's now Thursday morning. What's your streak?</summary>

Two. The current streak survives one clear day, so Monday–Tuesday still counts on
Thursday morning. If you don't log anything Thursday either, it resets to zero.

</details>

<details markdown="1"><summary>Why does logging a session without an artifact still count toward the streak, but not the portfolio?</summary>

Because they measure different things. The streak measures showing up, which is a
habit. The portfolio measures what you can prove you built, which is a skill. Keeping
them separate means you can have an honest reading day without inflating your
evidence.

</details>

<details markdown="1"><summary>You have twenty minutes today instead of the usual hour. What do you do?</summary>

The build task, and skim the rest. A short session that produces something beats a
long one that produces nothing — and it keeps the streak alive.

</details>
