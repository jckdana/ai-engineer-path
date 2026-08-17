---
id: "00-03"
title: "Git and GitHub, properly"
module: "00"
core_minutes: 55
deep_minutes: 150
build: "A public GitHub repo with at least five commits and one branch merged."
resources:
  - title: "Pro Git — Recording changes to the repository"
    url: "https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository"
  - title: "Pro Git — Basic branching and merging"
    url: "https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging"
  - title: "GitHub docs — About remote repositories"
    url: "https://docs.github.com/en/get-started/git-basics/about-remote-repositories"
  - title: "Dangit, Git!?! — plain-English fixes for common mistakes"
    url: "https://dangitgit.com/"
  - title: "Learn Git Branching — interactive branching visualiser"
    url: "https://learngitbranching.js.org/"
---

## Why this matters

In lesson 00-01 you typed `git init`, `git add .`, `git commit` and were told what they
did in one line each. Since then you've been running `git add -A` and `git push` on
faith. This lesson is where that stops being a ritual and starts being a tool you
reach for deliberately.

Two things change once git clicks. First, you stop being afraid of your own code —
you can try a risky rewrite knowing that a working version is saved and one command
away. Beginners without git edit cautiously and keep folders called `project_v2_final`;
that caution costs more than any bug. Second, your work becomes visible. Every lesson
you ship lands in a public repo with a date on it, and that repo is the thing you show
someone when they ask what you can do.

By the end you'll be able to inspect exactly what's about to be saved, commit a
coherent change on purpose, work on a branch and merge it back, and — most usefully —
recover when you do the wrong thing.

## The mental model

Git is not a folder of backups. It's a chain of **snapshots**. A **commit** is one
snapshot of your whole project, plus a message and a pointer to the commit that came
before it. Follow those pointers backwards and you have your history.

The part that confuses everyone at first is that a change passes through *three*
places on your machine before it reaches GitHub, and the middle one — the **staging
area** — is invisible in your file explorer.

<figure class="figure">
<svg viewBox="0 0 740 250" role="img" aria-label="A change moves through four places: the working tree of edited files, the staging area holding what the next commit will contain, the local repository of committed history, and the remote copy on GitHub. git add, git commit and git push move a change forward one step each; git restore, git reset and git pull move information back the other way. git status reports on the first two places.">
  <defs>
    <marker id="g-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="currentColor"/>
    </marker>
    <marker id="g-ar-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/>
    </marker>
  </defs>

  <g font-family="system-ui, sans-serif" font-size="12" fill="currentColor">

    <!-- git status bracket over the first two boxes -->
    <path d="M6 84 L6 76 L338 76 L338 84" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
    <text x="172" y="66" text-anchor="middle" font-size="11" opacity="0.7">
      <tspan font-family="ui-monospace, monospace">git status</tspan> reports on these two
    </text>

    <!-- 1. working tree -->
    <rect x="6" y="100" width="134" height="74" rx="9" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.45"/>
    <text x="73" y="124" text-anchor="middle" font-weight="600">working tree</text>
    <text x="73" y="143" text-anchor="middle" font-size="10.5" opacity="0.65">your files, as you</text>
    <text x="73" y="157" text-anchor="middle" font-size="10.5" opacity="0.65">just edited them</text>

    <!-- 2. staging area -->
    <rect x="204" y="100" width="134" height="74" rx="9" fill="var(--accent-tint)" stroke="var(--accent)" stroke-width="1.8"/>
    <text x="271" y="124" text-anchor="middle" font-weight="600">staging area</text>
    <text x="271" y="143" text-anchor="middle" font-size="10.5" fill="var(--accent)">what the next</text>
    <text x="271" y="157" text-anchor="middle" font-size="10.5" fill="var(--accent)">commit will contain</text>

    <!-- 3. local repository -->
    <rect x="402" y="100" width="134" height="74" rx="9" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.45"/>
    <text x="469" y="124" text-anchor="middle" font-weight="600">local repository</text>
    <text x="469" y="143" text-anchor="middle" font-size="10.5" opacity="0.65">your history —</text>
    <text x="469" y="157" text-anchor="middle" font-size="10.5" opacity="0.65">works with no internet</text>

    <!-- 4. remote -->
    <rect x="600" y="100" width="134" height="74" rx="9" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.45"/>
    <text x="667" y="124" text-anchor="middle" font-weight="600">remote</text>
    <text x="667" y="143" text-anchor="middle" font-size="10.5" opacity="0.65">the copy on GitHub —</text>
    <text x="667" y="157" text-anchor="middle" font-size="10.5" opacity="0.65">backup and evidence</text>

    <!-- forward arrows -->
    <line x1="146" y1="137" x2="198" y2="137" stroke="var(--accent)" stroke-width="2" marker-end="url(#g-ar-a)"/>
    <text x="172" y="127" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10.5" font-weight="600" fill="var(--accent)">git add</text>

    <line x1="344" y1="137" x2="396" y2="137" stroke="currentColor" stroke-width="1.8" marker-end="url(#g-ar)"/>
    <text x="370" y="127" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10.5">git commit</text>

    <line x1="542" y1="137" x2="594" y2="137" stroke="currentColor" stroke-width="1.8" marker-end="url(#g-ar)"/>
    <text x="568" y="127" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10.5">git push</text>

    <!-- return arrows -->
    <line x1="198" y1="205" x2="146" y2="205" stroke="currentColor" stroke-width="1.4" stroke-dasharray="5 4" opacity="0.55" marker-end="url(#g-ar)"/>
    <text x="172" y="222" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10.5" opacity="0.7">git restore</text>

    <line x1="396" y1="205" x2="344" y2="205" stroke="currentColor" stroke-width="1.4" stroke-dasharray="5 4" opacity="0.55" marker-end="url(#g-ar)"/>
    <text x="370" y="222" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10.5" opacity="0.7">git reset</text>

    <line x1="594" y1="205" x2="542" y2="205" stroke="currentColor" stroke-width="1.4" stroke-dasharray="5 4" opacity="0.55" marker-end="url(#g-ar)"/>
    <text x="568" y="222" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10.5" opacity="0.7">git pull</text>

  </g>
</svg>
<figcaption>Every git command you'll use in the first month is a move between two of these boxes.
When a command confuses you, ask which box it reads from and which it writes to.</figcaption>
</figure>

Three things follow from that picture.

**Nothing is saved until you commit.** Editing a file changes box one only. `git add`
copies the current contents into box two; `git commit` turns box two into a permanent
snapshot in box three. Add a file, edit it again, and commit — the commit contains the
version you *added*, not the version on screen. That surprises people once.

**The staging area exists so a commit can be one idea.** You'll often finish a session
having fixed a bug *and* renamed a variable *and* added a note. Staging lets you commit
those separately, so your history reads as a sequence of decisions rather than a
sequence of days. This is why `git add -A` — "stage everything" — is a convenience, not
the normal case.

**A branch is a sticky note, not a copy of your files.** A branch is a name pointing at
one commit; committing moves the note forward. Creating a branch writes about forty
bytes, which is why branching is cheap and normal. `main` is just the note you started
with, and **HEAD** is git's word for "the note you're currently standing on."

## In practice

Open a terminal in this folder. Everything here runs against your real repo.

### Look before you touch

`git status` is the command you run more than every other command combined. It answers
"what's in box one, what's in box two, and where am I?"

```powershell
git status
```

```text
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   content/progress.json
        modified:   docs/index.html

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        requirements-frozen.txt

no changes added to commit (use "git add" to track/commit files)
```

Read the three parts. **Changes not staged** are edits git already knows about, sitting
in box one. **Untracked** means git has never seen this file at all — new files are
never included automatically, which is deliberate. And nothing is staged yet, so a
commit right now would contain nothing.

To see *what* changed, not just which files:

```powershell
git diff
```

Lines starting `-` were removed, `+` were added. Press `q` to exit the pager.

### Stage deliberately, then commit

Stage one file by name rather than everything:

```powershell
git add requirements-frozen.txt
git status
```

```text
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        new file:   requirements-frozen.txt

Changes not staged for commit:
        modified:   content/progress.json
```

The same file list, now split across two sections — that split *is* the staging area,
made visible. Commit what's staged:

```powershell
git commit -m "Add frozen requirements from lesson 00-02"
```

```text
[main 4f2a1c9] Add frozen requirements from lesson 00-02
 1 file changed, 24 insertions(+)
```

`4f2a1c9` is the start of the commit's ID, a hash of its contents. `-m` supplies the
message inline; without it git opens an editor, which is a common way for beginners to
get stuck in a program they can't exit.

**Write messages in the imperative, describing the change:** "Add frozen requirements",
not "changes" or "stuff". The test is whether it completes the sentence *"applying this
commit will…"*. You are writing to yourself in three months, and you will not remember.

Now stage and commit the rest, and read your history back:

```powershell
git add -A
git commit -m "Log lesson 00-02 session and rebuild site"
git log --oneline -5
```

```text
4f2a1c9 Log lesson 00-02 session and rebuild site
9d3b7e1 Add frozen requirements from lesson 00-02
3010796 Freeze to requirements-frozen.txt, not .tmp
af4d1ec Write lesson 00-02: your machine, your terminal, your editor
057eab8 Add the product track and pull selling work forward
```

That's the chain from the mental model, newest first.

### Branch, then merge

Make a branch and move onto it in one command:

```powershell
git switch -c lesson/00-03
```

```text
Switched to a new branch 'lesson/00-03'
```

`-c` means create. (You'll see `git checkout -b` in older tutorials — same effect;
`switch` is the newer command that does only this one job, so prefer it.) Your files
didn't change, because the branch points at the same commit you were already on.

Make a small change — create a file `notes/00-03-git-notes.md` with a line or two in
it — then commit it on this branch:

```powershell
git add notes/00-03-git-notes.md
git commit -m "Start git notes"
```

Go back to `main` and look at your folder:

```powershell
git switch main
```

`notes/` has vanished from the file explorer. It isn't lost — `main`'s sticky note is
still on the older commit, and git rewrote your working tree to match it. This is the
moment branches become real. Now bring the work in:

```powershell
git merge lesson/00-03
```

```text
Updating 4f2a1c9..b7c0e42
Fast-forward
 notes/00-03-git-notes.md | 3 +++
 1 file changed, 3 insertions(+)
```

**Fast-forward** means `main` hadn't moved since you branched, so git just slid the
sticky note forward — no merging was actually necessary. The file is back. Tidy up and
publish:

```powershell
git branch -d lesson/00-03
git push
```

Deleting the branch deletes the *name*, never the commits — they're on `main` now.

If `git push` asks you to sign in, that's normal: password authentication was removed
from GitHub years ago. Git for Windows ships with Credential Manager, which opens a
browser window for you to authorise once and then remembers.

### When it goes wrong

Everything below is routine, not an emergency. Run `git status` first every time — it
usually tells you the fix.

| Situation | Fix |
| --- | --- |
| Bad message on the last commit (not pushed) | `git commit --amend -m "better message"` |
| Staged a file you didn't mean to | `git restore --staged <file>` |
| Want to throw away edits to one file | `git restore <file>` — **destructive**, the edits are gone |
| Last commit was a mistake, keep the work | `git reset --soft HEAD~1` — undoes the commit, leaves files staged |
| `push` rejected: "remote contains work you do not have" | `git pull`, then push again |
| Genuinely lost | `git reflog` — lists every commit HEAD has pointed at, including "deleted" ones |

`git reflog` is the safety net worth knowing on day one: once something is committed,
it is very hard to actually lose, even when a command appears to have eaten it.

Two habits that prevent most of the trouble: commit small and often, and **never commit
secrets**. This repo's `.gitignore` already excludes `.env`, `.venv/` and
`credentials.json`, which is why your API keys will live in `.env` from lesson 00-05
onward. A key pushed to a public repo is compromised within minutes — scanners watch
for them — and deleting it in a later commit does not help, because the old commit is
still in the history.

## Build it

A public repo with at least five commits and one merged branch. You already have the
repo, so this is about the commits and the branch.

**1. Commit what's currently uncommitted**, as *two* separate commits, staging by name.
Run `git status` first and decide which files belong together. Two real messages.

**2. Create a branch** and switch to it:

```powershell
git switch -c lesson/00-03
```

**3. Make two commits on the branch.** Create `notes/00-03-git-notes.md` and write, in
your own words, what the staging area is for and what a branch actually is. Commit it.
Then add one more line — a git command you want to remember — and commit that
separately.

**4. Merge it back into `main`** and delete the branch:

```powershell
git switch main
git merge lesson/00-03
git branch -d lesson/00-03
```

**5. Push, and check it on GitHub.** Open your repo in a browser and confirm your
commit messages are there, on the commits page.

Done when:

- `git log --oneline` shows at least five commits with messages you'd understand in
  three months
- `git log --graph --oneline -10` shows your branch's commits on `main`
- `git status` prints `nothing to commit, working tree clean`
- `git branch` lists only `main`
- The commits are visible at `https://github.com/jckdana/ai-engineer-path/commits/main`
- `notes/00-03-git-notes.md` exists and is in your own words

Then log it:

```powershell
python tools/progress_log.py --lesson-id 00-03 --status complete --minutes 55 --artifact ./notes/00-03-git-notes.md --note "branched and merged for the first time"
python tools/site_build.py --open
```

## Going deeper

- Cause a **merge conflict** on purpose: branch, edit line one of a file, switch back to
  `main`, edit the same line differently, commit both, merge. Git writes `<<<<<<<`,
  `=======` and `>>>>>>>` markers into the file — your version above, theirs below.
  Delete the markers, leave the text you want, `git add` the file, `git commit`.
  Conflicts are frightening exactly once.
- Work through the first two levels of [Learn Git Branching](https://learngitbranching.js.org/).
  Seeing the commit graph move as you type is worth an hour of reading.
- Run `git log --graph --oneline --all` and compare it to what the visualiser draws.
- Open a **pull request** against your own repo: push a branch instead of merging
  locally, then use GitHub's interface to merge it. This is how every team you'll ever
  join actually works.
- Read [Recording changes to the repository](https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository)
  in full, then find out what `git add -p` does — it stages *parts* of a file, and it's
  the fastest way to understand why staging is separate from committing.
- Look up what a **detached HEAD** is, since you'll hit it eventually by running
  `git switch <commit-hash>`. Knowing the name makes the warning message readable.

## Check yourself

<details markdown="1"><summary>You've fixed a bug in `app.py` and, separately, rewritten a paragraph of `README.md`. You want two commits. What do you type?</summary>

`git add app.py`, then `git commit -m "Fix ..."`, then `git add README.md`, then
`git commit -m "Rewrite ..."`. Staging by name is the whole point of the staging area:
`git add -A` would sweep both into one commit and you'd lose the ability to describe —
or later undo — either change on its own.

</details>

<details markdown="1"><summary>You commit, then notice a typo in the message ten seconds later. You haven't pushed. What now, and would the answer change if you had pushed?</summary>

`git commit --amend -m "the corrected message"` replaces the last commit. It works
cleanly because nobody else has seen it.

If you'd already pushed, amending creates a *different* commit with a different hash,
so your local history and GitHub's would disagree and the push would be rejected. On a
solo repo you can force it; on a shared one you leave the typo. That asymmetry —
rewriting unpublished history is free, rewriting published history is rude — is the
rule behind most git etiquette.

</details>

<details markdown="1"><summary>You switch to another branch and half your project's files disappear from the file explorer. What happened?</summary>

Nothing bad. A branch points at a commit, and switching rewrites your working tree to
match that commit. Files created on the other branch don't exist in this snapshot, so
git removed them from disk. Switch back and they return. The commits were never
touched — only box one in the diagram changed.

</details>

<details markdown="1"><summary>`git push` fails with "Updates were rejected because the remote contains work that you do not have locally." What caused it, and what's the fix?</summary>

Something added commits to GitHub that your local repo doesn't know about — usually you
edited a file in GitHub's web interface, or pushed from another machine. Git refuses to
overwrite history it can't reconcile.

`git pull` fetches those commits and combines them with yours, then `git push` works.
Not `push --force`, which would delete the remote's commits.

</details>

<details markdown="1"><summary>You accidentally commit and push a `.env` file containing an API key. You immediately delete the file and push again. Are you safe?</summary>

No. The key is still in the earlier commit, which is still in the history, and anyone
can read it — automated scanners find public keys within minutes. The only real fix is
to **rotate the key**: revoke it at the provider and issue a new one. Purging it from
history is possible but secondary, because you must assume it was already copied.

Which is why `.gitignore` matters more than it looks: it's the mechanism that stops
this happening at all.

</details>
