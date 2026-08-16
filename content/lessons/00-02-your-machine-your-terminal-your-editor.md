---
id: "00-02"
title: "Your machine, your terminal, your editor"
module: "00"
core_minutes: 55
deep_minutes: 120
build: "A virtual environment you created yourself with three packages installed and a frozen requirements.txt."
resources:
  - title: "Python docs — Virtual Environments and Packages"
    url: "https://docs.python.org/3/tutorial/venv.html"
  - title: "VS Code — Python environments"
    url: "https://code.visualstudio.com/docs/python/environments"
  - title: "pip user guide — requirements files and pip freeze"
    url: "https://pip.pypa.io/en/stable/user_guide/"
  - title: "VS Code — Getting started with Python (beginner walkthrough)"
    url: "https://code.visualstudio.com/docs/python/python-tutorial"
---

## Why this matters

Last lesson you typed commands without being told what they were. This lesson closes
that gap. By the end you'll know what the terminal actually is, what happens when you
type `python`, and why every real Python project keeps its packages in a folder of its
own instead of dumping them on your machine.

That last part sounds like housekeeping. It isn't. It's the single most common way a
beginner's setup breaks: you install a package for one project, it quietly upgrades a
package another project depended on, and now something that worked last week doesn't.
The error message won't mention the upgrade. You'll lose an evening.

Virtual environments make that impossible, and they cost you one command per project.
You're going to make one today, and every project you build from here lives in one.

## The mental model

A **terminal** is a place to type commands instead of clicking. When you type
`python tools/site_build.py`, you're telling the computer to run the program called
`python`, handing it a file to execute. That's it — no magic.

But *which* `python`? Your machine could have several. The answer is a system setting
called **PATH**: a list of folders, searched top to bottom, and the first `python.exe`
found wins.

That one fact explains everything about virtual environments. A virtual environment —
a **venv** — is just a folder containing its own copy of Python and its own package
store. "Activating" it does one thing: it puts that folder at the *front* of PATH. From
then on, `python` and `pip` mean the project's copies, so anything you install lands in
the project, not on the machine.

<figure class="figure">
<svg viewBox="0 0 740 300" role="img" aria-label="Typing python is resolved through the PATH list, searched top to bottom. Activating a virtual environment inserts the project's Scripts folder at the top of PATH, so python resolves to the project's own interpreter and its own package store instead of the machine-wide one.">
  <defs>
    <marker id="p-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="currentColor"/>
    </marker>
    <marker id="p-ar-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/>
    </marker>
  </defs>

  <g font-family="system-ui, sans-serif" font-size="13" fill="currentColor">

    <!-- what you type -->
    <rect x="16" y="125" width="132" height="54" rx="9" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.45"/>
    <text x="82" y="147" text-anchor="middle" font-size="11.5" opacity="0.65">you type</text>
    <text x="82" y="167" text-anchor="middle" font-family="ui-monospace, monospace" font-weight="600">python</text>

    <line x1="152" y1="152" x2="192" y2="152" stroke="currentColor" stroke-width="1.6" marker-end="url(#p-ar)"/>
    <text x="172" y="141" text-anchor="middle" font-size="11" opacity="0.7">found in</text>

    <!-- PATH -->
    <text x="298" y="86" text-anchor="middle" font-size="11.5" opacity="0.7">PATH — searched top to bottom</text>
    <rect x="198" y="96" width="200" height="112" rx="9" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.45"/>

    <rect x="210" y="108" width="176" height="42" rx="6" fill="var(--accent-tint)" stroke="var(--accent)" stroke-width="1.8"/>
    <text x="298" y="125" text-anchor="middle" font-family="ui-monospace, monospace" font-size="11.5" font-weight="600">.venv\Scripts</text>
    <text x="298" y="141" text-anchor="middle" font-size="10.5" fill="var(--accent)">put here by activate</text>

    <rect x="210" y="156" width="176" height="42" rx="6" fill="none" stroke="currentColor" stroke-width="1.3" opacity="0.5"/>
    <text x="298" y="173" text-anchor="middle" font-family="ui-monospace, monospace" font-size="11.5">C:\Python314</text>
    <text x="298" y="189" text-anchor="middle" font-size="10.5" opacity="0.6">always there</text>

    <!-- branches -->
    <path d="M390 129 C 418 129, 418 74, 438 74" fill="none" stroke="var(--accent)" stroke-width="2" marker-end="url(#p-ar-a)"/>
    <text x="424" y="99" text-anchor="middle" font-size="11" fill="var(--accent)" font-weight="600">wins</text>

    <path d="M390 177 C 418 177, 418 236, 438 236" fill="none" stroke="currentColor" stroke-width="1.6"
          stroke-dasharray="5 4" opacity="0.55" marker-end="url(#p-ar)"/>
    <text x="432" y="209" text-anchor="middle" font-size="11" opacity="0.7">only if no venv</text>

    <!-- destinations -->
    <rect x="444" y="46" width="280" height="56" rx="9" fill="var(--accent-tint)" stroke="var(--accent)" stroke-width="1.8"/>
    <text x="584" y="68" text-anchor="middle" font-family="ui-monospace, monospace" font-size="11.5" font-weight="600">.venv\Lib\site-packages</text>
    <text x="584" y="87" text-anchor="middle" font-size="11" opacity="0.7">this project's packages only</text>

    <rect x="444" y="208" width="280" height="56" rx="9" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.45"/>
    <text x="584" y="230" text-anchor="middle" font-family="ui-monospace, monospace" font-size="11.5">C:\Python314\Lib\site-packages</text>
    <text x="584" y="249" text-anchor="middle" font-size="11" opacity="0.7">shared by every project — where clashes happen</text>

  </g>
</svg>
<figcaption>Activation doesn't install a new Python. It changes one list, so the same word you type
resolves somewhere else — and everything you install follows it there.</figcaption>
</figure>

Two consequences worth holding onto:

**A venv is disposable.** It's a folder. Delete it and rebuild it from
`requirements.txt` in thirty seconds. That's why `.venv/` is in this repo's
`.gitignore` — you never share the folder, you share the list of what's in it.

**Nothing is active until you activate it.** Open a new terminal and you're back on the
machine-wide Python. This trips up everyone once. The tell is a `ModuleNotFoundError`
for a package you know you installed.

## In practice

Open the terminal in VS Code with **Ctrl + `** (the key above Tab). Confirm you're in
the right folder — the prompt should end in `Claude Knowledge`.

First, check what you have. `--version` asks a program to identify itself:

```powershell
python --version
```

```text
Python 3.14.3
```

If instead you get "not recognized," Python isn't installed or isn't on PATH — install
it from [python.org/downloads](https://www.python.org/downloads/), and **tick "Add
python.exe to PATH"** on the first screen of the installer.

Now find out where that Python actually lives:

```powershell
python -c "import sys; print(sys.executable)"
```

```text
C:\Python314\python.exe
```

`-c` means "run this bit of code directly instead of a file." That path is the bottom
box in the diagram — the machine-wide Python. Everything you've installed so far went
next to it. Now you'll stop doing that.

Create a virtual environment. `-m venv` means "run the built-in module named venv," and
`.venv` is the folder to create:

```powershell
python -m venv .venv
```

It prints nothing, which is normal — Unix-style tools stay silent on success. A `.venv`
folder now exists. Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Your prompt changes to start with `(.venv)`. **That prefix is the whole feedback
mechanism** — it's how you know which Python you're talking to. Check that the change
took effect:

```powershell
python -c "import sys; print(sys.executable)"
```

```text
E:\Claude Knowledge\.venv\Scripts\python.exe
```

Same command, different answer. Nothing about Python changed — PATH did.

### The trap, on purpose

Now run the site builder:

```powershell
python tools/site_build.py
```

```text
ModuleNotFoundError: No module named 'jinja2'
```

**You didn't break anything.** Jinja2 is installed on the machine-wide Python; your new
venv is empty by design. This is isolation working exactly as advertised, and it's
worth seeing once so you recognise it later. Fix it by installing this project's
dependencies *into the venv*:

```powershell
python -m pip install -r requirements.txt
```

`-r` means "read the list from this file." Now `python tools/site_build.py` works again.

When you're finished with a venv, `deactivate` restores the old PATH. You rarely need
to — closing the terminal does the same thing.

| Command | What it does |
| --- | --- |
| `python -m venv .venv` | Create the environment. Once per project. |
| `.\.venv\Scripts\Activate.ps1` | Point PATH at it. Every new terminal. |
| `python -m pip install <name>` | Install one package into the active environment. |
| `python -m pip install -r requirements.txt` | Install everything on the list. |
| `python -m pip freeze` | Print exactly what's installed, with versions. |
| `python -m pip list` | Same idea, friendlier format. |
| `deactivate` | Undo activation. |

Use `python -m pip` rather than bare `pip`. Both usually work, but the long form is
unambiguous: it installs into *the Python you just checked*, which is the only thing
you can be sure about.

### One VS Code setting

Press **Ctrl + Shift + P**, type `Python: Select Interpreter`, and pick the one whose
path contains `.venv`. This tells VS Code to use your venv when you press the Run
button, and it will auto-activate in new terminals so you stop having to remember.

## Build it

**1. Create and activate a venv in this repo**, following the steps above. Install the
project's dependencies into it.

**2. Add three packages you'll use later**, so you've installed something by name rather
than from a list:

```powershell
python -m pip install rich httpx pytest
```

`rich` prints colour and tables in the terminal, `httpx` fetches things over the
internet, `pytest` runs tests. You'll meet all three properly later.

**3. Prove `rich` works**, and that it came from the venv:

```powershell
python -c "from rich import print; print('[bold green]venv works[/bold green]')"
```

**4. Freeze the environment** to a separate file, so you can compare it against the
project's own list:

```powershell
python -m pip freeze > .tmp/frozen.txt
```

The `>` sends the output into a file instead of the screen. Open `.tmp/frozen.txt` and
compare it with `requirements.txt`. Both list packages — but `requirements.txt` says
`jinja2>=3.1` ("at least this version") while the frozen file pins an exact one like
`jinja2==3.1.6`. Loose ranges are what a human writes; exact pins are what a machine
records. You want both, for different reasons.

**5. Select the interpreter in VS Code** (Ctrl + Shift + P → `Python: Select Interpreter`).

Done when:

- Your terminal prompt starts with `(.venv)`
- `python -c "import sys; print(sys.executable)"` prints a path inside `E:\Claude Knowledge\.venv`
- The `rich` line prints in green
- `.tmp/frozen.txt` exists and contains `rich`, `httpx` and `pytest`
- `python tools/site_build.py` runs without error while the venv is active

Then log it:

```powershell
python tools/progress_log.py --lesson-id 00-02 --status complete --minutes 55 --artifact ./.tmp/frozen.txt --note "made my first venv"
python tools/site_build.py --open
```

### If activation is blocked

If `Activate.ps1` fails with "running scripts is disabled on this system," Windows is
refusing to run script files. Allow locally-created ones for your account only:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

`RemoteSigned` means "scripts I made are fine; downloaded ones need a signature." It's
the setting Microsoft recommends for development machines. Then activate again.

## Going deeper

- Delete the `.venv` folder entirely, then rebuild it from scratch: create, activate,
  `install -r requirements.txt`. Doing this once removes the fear of breaking it, which
  is worth more than the ten minutes it takes.
- Run `python -m pip list` before and after installing one package, and diff the two
  lists. Some packages pull in others — those are **transitive dependencies**, and
  they're why `pip freeze` output is longer than what you asked for.
- Look inside `.venv\Lib\site-packages`. Every package is just a folder of Python files
  you could open and read. Open one. There's no black box under here.
- Read the `pip freeze` section of the [pip user guide](https://pip.pypa.io/en/stable/user_guide/)
  on repeatable installs, and form a view on when pinning exact versions helps and when
  it gets in the way.
- Find out what `python -m` actually means (the [venv docs](https://docs.python.org/3/tutorial/venv.html)
  use it constantly). Understanding `-m` explains why `python -m pip` is safer than `pip`.

## Check yourself

<details markdown="1"><summary>You open a fresh terminal, run your script, and get `ModuleNotFoundError` for a package you definitely installed yesterday. What's the first thing to check?</summary>

Whether the venv is active — look for `(.venv)` at the start of the prompt. A new
terminal starts unactivated, so `python` resolves to the machine-wide install, which
doesn't have your package. Activate and try again.

</details>

<details markdown="1"><summary>Why is `.venv/` in `.gitignore` when the whole point of git is to save your work?</summary>

Because the venv is derived, not authored. It's thousands of files, it's specific to
your OS, and it can be rebuilt exactly from `requirements.txt` in under a minute. You
commit the *recipe*, not the meal. Committing it would also make every diff unreadable.

</details>

<details markdown="1"><summary>`requirements.txt` says `jinja2>=3.1`. `pip freeze` says `jinja2==3.1.6`. Which is wrong?</summary>

Neither — they answer different questions. `>=3.1` is your *intent*: any version from
3.1 up should work. `==3.1.6` is a *fact*: this is what was installed when you froze
it. You write the first by hand; the second is a recording, useful when you need an
environment to come back identical.

</details>

<details markdown="1"><summary>You're helping a friend and they have no venv at all — everything installed machine-wide, and it currently works. What actually goes wrong later, and when?</summary>

Nothing, until their second project needs a different version of a package the first
one uses. Installing it upgrades or downgrades the shared copy, and the *first* project
breaks — with an error that says nothing about the install. The cost isn't the breakage,
it's that the cause is invisible and arrives weeks after the decision.

</details>

<details markdown="1"><summary>What does activation actually change on your computer?</summary>

One list: PATH. It inserts the venv's `Scripts` folder at the front, so `python` and
`pip` resolve there first. No new Python is installed and nothing is copied — the same
word you type simply finds a different program.

</details>
