---
id: "01-05"
title: "Files, paths, and the filesystem"
module: "01"
core_minutes: 50
deep_minutes: 110
build: "A script that walks a folder, reads every .txt file, and writes a summary index."
resources:
  - title: "pathlib — the official reference (Path, glob, rglob, read_text, mkdir)"
    url: "https://docs.python.org/3/library/pathlib.html"
  - title: "Python tutorial 7.2 — Reading and Writing Files (why encoding='utf-8', why with)"
    url: "https://docs.python.org/3/tutorial/inputoutput.html"
  - title: "Automate the Boring Stuff, chapter 10 — Reading and Writing Files (free online)"
    url: "https://automatetheboringstuff.com/3e/chapter10.html"
  - title: "Automate the Boring Stuff, chapter 11 — Organizing Files (free online)"
    url: "https://automatetheboringstuff.com/3e/chapter11.html"
  - title: "PEP 686 — Make UTF-8 mode default (why Windows reads files wrong today)"
    url: "https://peps.python.org/pep-0686/"
---

## Why this matters

Your ticket filter from 01-04 works. Now open a terminal, go into the `builds`
folder, and run it from there:

```powershell
cd builds
python 01-04-filter.py
```

```text
  File "C:\Claude\Claude Knowledge\builds\01-04-filter.py", line 10, in load_records
    with open(path, encoding="utf-8") as f:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'builds/01-04-tickets.json'
```

Same code, same files, and now it crashes. Nothing about the script changed.
What changed is *where you were standing when you ran it*. This is the most
common reason a script that "works on my machine" fails on a client's machine,
in a scheduled task, or on a server. Those places almost never run your script
from the folder you happened to be in.

Almost every paid AI job starts with *"we have a folder full of documents"*.
That means contracts, transcripts, support exports or notes. Before a model can
read any of them, your code has to find them, open them with the right encoding,
and write results somewhere predictable. By the end of this lesson you'll have
built the first half of a document Q&A system, the thing in your first
capstone: a script that finds every text file in a folder tree and indexes it.
It will work no matter where it's run from. (`cd ..` takes you back to the
project folder.)

## The mental model

A **path** is an address for a file. There are two kinds:

- An **absolute path** starts from the root of the drive:
  `C:\Claude\Claude Knowledge\builds\01-04-tickets.json`. It means the same thing
  from anywhere.
- A **relative path** has no drive letter: `builds/01-04-tickets.json`. On its
  own it's incomplete. Python glues it onto the **current working directory**
  (cwd), which is the folder your terminal was in when you typed `python`.

**The idea this lesson turns on:** a relative path is relative to *where you ran
the script from*, not to *where the script lives*. Those are usually the same
folder, which is why the bug hides until the day they aren't.

The fix is to anchor paths to the one location that never moves: the script's
own file. Python always knows it as `__file__`.

<figure class="figure">
<svg viewBox="0 0 780 340" role="img" aria-label="Three rows show how Python turns a path into a real file location. Row one: the terminal is in the project folder, Claude Knowledge. The relative path builds slash 01-04-tickets.json is glued onto that folder, giving Claude Knowledge, builds, 01-04-tickets.json, which exists. Row two: the terminal is inside the builds folder. The same relative path is glued onto builds, giving builds, builds, 01-04-tickets.json, which does not exist, so Python raises FileNotFoundError. Row three, highlighted: the path is built from Path of __file__ dot parent, the folder the script itself lives in, slash 01-04-tickets.json. It resolves to builds, 01-04-tickets.json from either terminal location, so it always works.">
  <defs>
    <marker id="p-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="currentColor"/>
    </marker>
    <marker id="p-ar-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/>
    </marker>
  </defs>

  <g font-family="system-ui, sans-serif" font-size="12" fill="currentColor">
    <text x="16" y="22" font-size="10.5" font-weight="600" opacity="0.75">WHERE YOU RAN IT FROM</text>
    <text x="345" y="22" text-anchor="middle" font-size="10.5" font-weight="600" opacity="0.75">THE PATH IN YOUR CODE</text>
    <text x="764" y="22" text-anchor="end" font-size="10.5" font-weight="600" opacity="0.75">WHERE PYTHON LOOKS</text>

    <!-- Row 1 -->
    <rect x="16" y="36" width="200" height="54" rx="8" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.6"/>
    <text x="30" y="57" font-size="11" font-weight="600">cwd = project folder</text>
    <text x="30" y="76" font-family="ui-monospace, monospace" font-size="10">…\Claude Knowledge</text>
    <path d="M 216 63 L 470 63" stroke="currentColor" stroke-width="1.5" marker-end="url(#p-ar)"/>
    <rect x="252" y="50" width="186" height="24" rx="5" fill="var(--surface)" stroke="currentColor" stroke-width="1" opacity="0.9"/>
    <text x="345" y="66" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10.5">"builds/01-04-tickets.json"</text>
    <rect x="474" y="36" width="290" height="54" rx="8" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.6"/>
    <text x="488" y="57" font-family="ui-monospace, monospace" font-size="10">…\Claude Knowledge\builds\</text>
    <text x="488" y="74" font-family="ui-monospace, monospace" font-size="10">01-04-tickets.json</text>
    <text x="752" y="66" text-anchor="end" font-size="11" font-weight="600">✓ found</text>

    <!-- Row 2 -->
    <rect x="16" y="112" width="200" height="54" rx="8" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.6"/>
    <text x="30" y="133" font-size="11" font-weight="600">cwd = inside builds</text>
    <text x="30" y="152" font-family="ui-monospace, monospace" font-size="10">…\Claude Knowledge\builds</text>
    <path d="M 216 139 L 470 139" stroke="currentColor" stroke-width="1.5" marker-end="url(#p-ar)"/>
    <rect x="252" y="126" width="186" height="24" rx="5" fill="var(--surface)" stroke="currentColor" stroke-width="1" opacity="0.9"/>
    <text x="345" y="142" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10.5">"builds/01-04-tickets.json"</text>
    <rect x="474" y="112" width="290" height="54" rx="8" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5 4" opacity="0.6"/>
    <text x="488" y="133" font-family="ui-monospace, monospace" font-size="10">…\builds\builds\</text>
    <text x="488" y="150" font-family="ui-monospace, monospace" font-size="10">01-04-tickets.json</text>
    <text x="752" y="133" text-anchor="end" font-size="11" font-weight="600">✗ no such folder</text>
    <text x="752" y="150" text-anchor="end" font-size="9.5" opacity="0.7">FileNotFoundError</text>

    <text x="345" y="186" text-anchor="middle" font-size="9.5" opacity="0.7">same string, different result: a relative path is glued onto the cwd</text>
    <line x1="16" y1="204" x2="764" y2="204" stroke="currentColor" stroke-width="1" stroke-dasharray="4 4" opacity="0.4"/>

    <!-- Row 3: the fix -->
    <text x="16" y="228" font-size="10.5" font-weight="600" fill="var(--accent)">THE FIX: ANCHOR TO THE SCRIPT ITSELF</text>
    <rect x="16" y="240" width="200" height="66" rx="8" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.6"/>
    <text x="30" y="262" font-size="11" font-weight="600">cwd = anywhere</text>
    <text x="30" y="280" font-size="9.5" opacity="0.7">project folder, builds,</text>
    <text x="30" y="294" font-size="9.5" opacity="0.7">a server, a scheduled task</text>
    <path d="M 216 273 L 470 273" stroke="var(--accent)" stroke-width="2" marker-end="url(#p-ar-a)"/>
    <rect x="228" y="250" width="234" height="46" rx="5" fill="var(--accent-tint)" stroke="var(--accent)" stroke-width="1.4"/>
    <text x="345" y="269" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10.5" fill="var(--accent)">Path(__file__).parent</text>
    <text x="345" y="286" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10.5" fill="var(--accent)">/ "01-04-tickets.json"</text>
    <rect x="474" y="240" width="290" height="66" rx="8" fill="none" stroke="var(--accent)" stroke-width="1.8"/>
    <text x="488" y="262" font-family="ui-monospace, monospace" font-size="10">…\Claude Knowledge\builds\</text>
    <text x="488" y="279" font-family="ui-monospace, monospace" font-size="10">01-04-tickets.json</text>
    <text x="752" y="298" text-anchor="end" font-size="11" font-weight="600" fill="var(--accent)">✓ always</text>
    <text x="345" y="328" text-anchor="middle" font-size="9.5" opacity="0.7">__file__ is where the script lives, and that never depends on where you stand</text>
  </g>
</svg>
<figcaption>A relative path is finished off by whatever folder the terminal is in,
so the same string can point at two different places. Building the path from
<code>Path(__file__).parent</code>, the script's own folder, gives one answer
from anywhere.</figcaption>
</figure>

Python's tool for all of this is **`pathlib`**, part of the standard library. It
gives you a `Path` object instead of a plain string. A `Path` knows how to join
itself with other parts, check whether the file exists, list a folder, and read
or write the file. It also uses the right slash for whichever operating system
it's on.

## In practice

Open a scratch file, `builds/01-05-play.py`. Type each block, run it, then
replace it with the next. Run everything from the project folder unless a step
says otherwise.

### Where am I, and where is my script?

```python
from pathlib import Path

print("cwd:   ", Path.cwd())
print("file:  ", Path(__file__))
print("folder:", Path(__file__).resolve().parent)
```

```text
cwd:    C:\Claude\Claude Knowledge
file:   C:\Claude\Claude Knowledge\builds\01-05-play.py
folder: C:\Claude\Claude Knowledge\builds
```

Now `cd builds`, run `python 01-05-play.py`, and compare. The `cwd` line
changes. The other two don't. That difference is the whole bug from the top of
the page.

- `Path.cwd()` is the folder you ran from. It belongs to the terminal, not to
  the script.
- `Path(__file__)` is this script's own location.
- `.resolve()` turns it into a complete absolute path. `.parent` goes up one
  level, from the file to the folder it's in.

`cd ..` to go back to the project folder.

### Building paths with `/`

```python
from pathlib import Path

HERE = Path(__file__).resolve().parent
p = HERE / "notes" / "a.txt"

print(p)
print(p.name)
print(p.stem)
print(p.suffix)
print(p.parent)
```

```text
C:\Claude\Claude Knowledge\builds\notes\a.txt
a.txt
a
.txt
C:\Claude\Claude Knowledge\builds\notes
```

The `/` between a `Path` and a string joins them. Here it isn't division. You
type forward slashes on every operating system, and `pathlib` prints whatever
the system uses. On Windows that's backslashes. `.name`, `.stem`, `.suffix` and
`.parent` pull a path apart, so you never need to slice strings to get at a
file's name or extension.

Writing a constant like `HERE` in capitals near the top of a script is a common
convention. It means "set once, never changed".

### Why you don't type Windows paths as plain strings

```python
print("C:\new\test.txt")
```

```text
C:
ew	est.txt
```

No error, just a wrong path. Inside a normal string a backslash starts an
**escape sequence**: `\n` is a new line and `\t` is a tab, which is exactly the
whitespace you cleaned in 01-01. Windows paths are full of backslashes, so they
walk straight into this. You have three ways out. Forward slashes work fine on
Windows. A raw string, `r"C:\new\test.txt"`, turns escapes off. Best of all is
building the path with `Path` and `/`, so you never type a separator at all.

### Reading and writing text

`Path` has shortcuts for the whole open, read and close routine:

```python
from pathlib import Path

HERE = Path(__file__).resolve().parent
note = HERE / "01-05-note.txt"

note.write_text("Zoë called about the invoice.\n", encoding="utf-8")
print(note.read_text(encoding="utf-8"))
print(note.read_text())
```

```text
Zoë called about the invoice.

ZoÃ« called about the invoice.
```

The third line is the trap from 01-04, and this time you've seen it. Without
`encoding=`, Python on Windows reads with an older default called `cp1252`, not
UTF-8. You get no error, just quietly broken text. Python 3.15 will make UTF-8
the default everywhere (PEP 686, in the resources). Until every machine you
touch runs that version, **always pass `encoding="utf-8"`**. Treat it as part of
the method name.

`write_text` **replaces** the file, just like `open(path, "w")`. Use
`read_text`/`write_text` for small files you handle all at once, and keep
`with open(...)` for when you need more control. They do the same job.

### Asking before you act

```python
from pathlib import Path

HERE = Path(__file__).resolve().parent

print((HERE / "01-04-tickets.json").exists())
print((HERE / "nope.json").exists())
print(HERE.is_dir())

out = HERE / "01-05-output"
out.mkdir()
out.mkdir()
```

```text
True
False
True
Traceback (most recent call last):
  ...
FileExistsError: [WinError 183] Cannot create a file when that file already exists: 'C:\\Claude\\Claude Knowledge\\builds\\01-05-output'
```

The first `mkdir()` worked and the second one crashed, because the folder was
already there. Replace both with:

```python
out.mkdir(parents=True, exist_ok=True)
```

`exist_ok=True` means "fine if it's already there". `parents=True` means "also
create any missing folders on the way". Together they make the line safe to run
any number of times. Scripts that are safe to re-run are scripts you can trust
in a schedule.

### Finding files: `iterdir`, `glob`, `rglob`

```python
from pathlib import Path

HERE = Path(__file__).resolve().parent

for p in sorted(HERE.iterdir()):
    print(p.name)

print("---")
for p in sorted(HERE.glob("*.py")):
    print(p.name)
```

`iterdir()` lists everything directly inside a folder, files and subfolders
alike. `glob("*.py")` keeps only the names that match a **pattern**. `*` means
"any characters", so `*.py` is "anything ending in .py". Neither one looks
inside subfolders.

To search the whole tree, use `rglob` (recursive glob):

```python
for p in sorted(HERE.rglob("*.txt")):
    print(p.relative_to(HERE))
```

`p.relative_to(HERE)` trims the long front of the path, so you see
`notes\a.txt` instead of the full `C:\...` address. That's better for printing
and for storing in a file someone else will read.

Two things about this that bite people:

- **Always wrap it in `sorted()`.** `glob` and `rglob` don't promise any order.
  Without sorting, the same folder can give a different order on another
  machine, and your output won't match from run to run.
- **On Windows, matching ignores capitals.** On your machine `*.txt` also
  matches `NOTES.TXT`. On a Mac or a Linux server it doesn't. Code that finds
  five files for you might find four on the client's server. If the difference
  matters, pass `case_sensitive=True` and make it the same everywhere.

## Build it

A client has a folder of notes and documents, some in subfolders. Before
anything AI touches them, they want an **index**: one file listing every text
document, with its size and first line, so a person or a later script knows
what's there.

**1. Branch first:**

```powershell
git switch -c lesson/01-05
```

**2. Make the sample folder.** Create `builds/01-05-make-docs.py` with this
content. It's setup, so copy-pasting is fine. Read it before you run it,
though, because every line uses something from this lesson:

```python
# Creates a small folder of sample documents for lesson 01-05. Safe to run twice.
from pathlib import Path

DOCS = Path(__file__).resolve().parent / "01-05-docs"

files = {
    "meeting-notes.txt": "Weekly sync at Café Luna\nShip the ticket filter by Friday.\nBudget approved for the team offsite.\n",
    "clients/acme.txt": "Acme Corp\nWants a weekly report of urgent tickets.\nBudget is 500 dollars a month.\n",
    "clients/zeta.txt": "Zeta Ltd\nInterested in a document Q&A bot.\n",
    "empty.txt": "",
    "README.md": "# Not a .txt file\nThe index should skip this one.\n",
}

for name, text in files.items():
    path = DOCS / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print("wrote", path.relative_to(DOCS))
```

Run it with `python builds/01-05-make-docs.py`. Open `builds/01-05-docs` in VS
Code's file explorer and check there's a `clients` subfolder, an empty file and
a `.md` file mixed in. Real folders are this messy.

**3. Write `builds/01-05-index.py`.** Start from this skeleton:

```python
# Walks a folder of documents, summarises every .txt file, and writes a JSON index.
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DOCS_DIR = HERE / "01-05-docs"
INDEX_PATH = HERE / "01-05-index.json"


def summarize(path):
    """Return a dict describing one text file."""
    ...


def save_index(entries, path):
    """Write the index as readable JSON."""
    ...


if not DOCS_DIR.is_dir():
    print(f"No folder at {DOCS_DIR}. Run 01-05-make-docs.py first.")
    raise SystemExit(1)

entries = []
# Find every .txt file in DOCS_DIR and its subfolders, in a stable order,
# and append summarize(path) for each one.
...

save_index(entries, INDEX_PATH)
total_words = sum(e["words"] for e in entries)
empty = sum(1 for e in entries if e["words"] == 0)
print(f"Indexed {len(entries)} files, {total_words} words, {empty} empty -> {INDEX_PATH}")
```

`summarize` must return a dict with four keys:

- `"file"` is the path relative to `DOCS_DIR`, as a string with forward
  slashes. Look up what `.as_posix()` does to a path.
- `"lines"` is the number of lines. `text.splitlines()` gives you a list of them.
- `"words"` is the word count, using the `.split()` trick from 01-01.
- `"first_line"` is the first line, or `""` if the file is empty. This is the
  `IndexError` you met in 01-02, waiting for you on `empty.txt`.

Two new things you'll see in the skeleton: `raise SystemExit(1)` stops the
script on purpose with a clear message, instead of crashing later on a confusing
one. The two `sum(...)` lines are a compact form of the loop-and-add pattern.
You don't need to write that form yet, just read it.

Hints, if you're stuck for more than ten minutes:

- `summarize` is `read_text` with an encoding, then `splitlines`, `split` and
  `len`, then a dict literal like the tickets in 01-04.
- `save_index` is the `json.dump` pattern from 01-04.
- Run it and open the index. Look at the first line of `meeting-notes.txt`. Does
  *Café* look right? If you see `Caf\u00e9`, that's `json.dump` escaping
  anything that isn't plain English letters. It's valid JSON, but unreadable for
  a person. Add `ensure_ascii=False` to the `json.dump` call. It's safe because
  you opened the file with `encoding="utf-8"`.

**4. Prove it works from anywhere.** Run it from the project folder, then
`cd builds` and run `python 01-05-index.py`, then `cd ..`. Both must print the
same line.

**5. Commit and merge:**

```powershell
git add builds/01-05-make-docs.py builds/01-05-index.py builds/01-05-docs builds/01-05-index.json
git commit -m "Add document indexer from lesson 01-05"
git switch main
git merge lesson/01-05
git branch -d lesson/01-05
git push
```

**Done when:**

- [ ] `python builds/01-05-index.py` prints `Indexed 4 files, 40 words, 1 empty -> ...` followed by the full path of the index.
- [ ] Running it from inside `builds` prints the same thing. No `FileNotFoundError`.
- [ ] `01-05-index.json` lists `clients/acme.txt`, `clients/zeta.txt`, `empty.txt` and `meeting-notes.txt`, in that order. `README.md` is not in it.
- [ ] `empty.txt` shows `"lines": 0`, `"words": 0` and `"first_line": ""`, and didn't crash anything.
- [ ] The first line of `meeting-notes.txt` reads `Weekly sync at Café Luna` in the JSON file, not `Caf\u00e9`.
- [ ] No string in `01-05-index.py` contains a backslash, and every path is built from `HERE`.

Then log it, as one line:

```powershell
python tools/progress_log.py --lesson-id 01-05 --status complete --minutes 50 --artifact ./builds/01-05-index.py --note "what clicked"
```

```powershell
python tools/site_build.py --open
```

Put in your real minutes, not the estimate.

## Free practice

These are free and need no credit card. Do them after the build task, not
instead of it.

- **[Project Gutenberg](https://www.gutenberg.org/ebooks/1342)** has thousands of
  free public-domain books as plain text. Download three, using the *Plain Text
  UTF-8* link on each book's page, into a new folder inside `01-05-docs`. Then
  re-run your indexer on them. Real files are long, and you'll see whether your
  word counts and first lines still make sense. Pride and Prejudice is about
  125,000 words.
- **[Automate the Boring Stuff, chapter 10](https://automatetheboringstuff.com/3e/chapter10.html)**
  covers this same ground with different examples, free online. Do the practice
  questions at the end without looking back at the chapter.
- **[Automate the Boring Stuff, chapter 11](https://automatetheboringstuff.com/3e/chapter11.html)**,
  the *Selective Copy* practice program: walk a folder tree and copy every file
  with a given extension into a new folder. That's your indexer plus one new
  function, `shutil.copy`. The chapter teaches the older `os.walk`. Try writing it
  with `rglob` instead.

Exercism has no file-handling exercises in its browser editor, which is why this
lesson doesn't use it.

## Going deeper

- **Fix 01-04 for real.** Change `INPUT_PATH` and `OUTPUT_PATH` in
  `01-04-filter.py` to build from `HERE`, then run it from inside `builds`. The
  crash from the top of this page should be gone. This is a two-line change, and
  every script you write from now on should start this way.
- **Make the folder a parameter.** Turn the main part of your script into a
  function, `build_index(docs_dir)`, that returns the entries list. Call it on
  `01-05-docs` and on `01-05-docs/clients` and compare.
- **Index more than `.txt`.** Include `.md` files too. Loop over a list of
  patterns, `["*.txt", "*.md"]`, and check the totals change by exactly the
  README's numbers.
- **Skip the junk.** Real folders contain `.git`, `__pycache__` and `.venv`. Run
  `rglob("*.py")` on your whole project folder and count how many results come
  from `.venv`. Then filter them out by checking `".venv" in p.parts`.
- **Survive a bad file.** Save one file in a different encoding, for example
  with `write_text(..., encoding="cp1252")` and a `ü` in it. Then watch your
  indexer crash with `UnicodeDecodeError`. Decide what should happen: skip and
  report it, or retry with another encoding. Lesson 01-06 is about exactly this
  kind of decision.
- **Put the model on it.** For each file, use your `ask` function from 01-03 to
  write a one-sentence summary, and store it under a `"summary"` key. Dry-run it
  with a fake summary first, the way you did in 01-02. That's an index a client
  would actually pay for, and the first half of capstone 18-01.

## Check yourself

<details markdown="1"><summary>Your script works when you run it from VS Code's terminal, but fails with <code>FileNotFoundError</code> when a scheduled task runs it every night. The file definitely exists. What's the most likely cause, and the fix?</summary>

The script uses a relative path, and the scheduled task runs it from a different
working directory, often `C:\Windows\System32`. Python glued the relative path
onto that folder and looked in the wrong place. Fix: build every path from
`Path(__file__).resolve().parent`, so it no longer depends on where it's run from.

</details>

<details markdown="1"><summary>A teammate writes <code>open("C:\reports\new_data.csv")</code>. What goes wrong, and why is there no error message pointing at it?</summary>

`\r` and `\n` inside a normal string are escape sequences, a carriage return and
a new line. So the string isn't the path they typed. Python opens (or fails to
find) a path containing invisible characters, and the error names a garbled
path rather than explaining why. Fix: use forward slashes, a raw string
`r"C:\reports\new_data.csv"`, or build it with `Path("C:/reports") / "new_data.csv"`.

</details>

<details markdown="1"><summary>Your indexer finds 5 files on your laptop and 4 on the client's Linux server, from an identical copy of the folder. What would you check first?</summary>

The case of a file extension. On Windows, `rglob("*.txt")` also matches
`NOTES.TXT`. On Linux it doesn't. Pass `case_sensitive=False` (or `True`) to
`rglob` so it behaves the same everywhere, or normalise names with
`p.suffix.lower() == ".txt"`.

</details>

<details markdown="1"><summary>Why does every <code>read_text</code> and <code>write_text</code> in this lesson pass <code>encoding="utf-8"</code>, when leaving it off gives no error?</summary>

Because no error is the problem. On Windows, the default is `cp1252`, so
non-English characters come back corrupted (`Zoë` becomes `ZoÃ«`) and nothing
tells you. Corrupted text then goes into your index, your database or your
prompt to a model. Passing the encoding explicitly makes the script behave the
same on every machine.

</details>

<details markdown="1"><summary>Your script calls <code>out.mkdir()</code>. It works the first time and crashes the second. Why does that matter more for a client's job than for your homework?</summary>

Client jobs run repeatedly: every night, after every upload, after a crash and a
restart. A script that only works on its first run fails on day two. Using
`mkdir(parents=True, exist_ok=True)` makes the step safe to re-run. Being safe
to repeat is a property you'll want in every step of every pipeline you build.

</details>
