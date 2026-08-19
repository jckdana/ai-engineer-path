---
id: "00-04"
title: "Your first Python program"
module: "00"
core_minutes: 45
deep_minutes: 100
build: "A script that takes your name as input and prints a formatted greeting, committed to git."
resources:
  - title: "Python tutorial — An informal introduction to Python"
    url: "https://docs.python.org/3/tutorial/introduction.html"
  - title: "Python tutorial — Input and output (f-strings)"
    url: "https://docs.python.org/3/tutorial/inputoutput.html"
  - title: "Python tutorial — Errors and exceptions"
    url: "https://docs.python.org/3/tutorial/errors.html"
  - title: "Python docs — the input() built-in"
    url: "https://docs.python.org/3/library/functions.html#input"
  - title: "Automate the Boring Stuff, chapter 1 — Python basics (free online)"
    url: "https://automatetheboringstuff.com/3e/chapter1.html"
---

## Why this matters

You have Python installed, a virtual environment, and a repo with history. What you
don't have yet is a program you wrote. That changes in the next forty-five minutes.

The thing to take from this lesson isn't `print()` — you'll have that in five minutes.
It's the loop underneath every hour you'll spend from here on: **write a little, run it,
read what came back, adjust.** Beginners lose weeks because they treat a red error
message as a verdict on themselves rather than as the most useful output the computer
produces. An error is Python telling you, in a fixed and readable format, exactly which
line it choked on and why. Once you can read that, you're not stuck — you're debugging,
which is just programming with more information.

By the end you'll be able to run a Python file from the terminal, store values in
variables, build a piece of text out of those values, ask the person running the program
a question, and — when it breaks, which it will — look at the traceback and know where
to go.

## The mental model

A Python file is not a document the computer looks at. It's a list of instructions
carried out in **two distinct phases**, and knowing which phase you're in tells you what
an error means.

First Python reads the *entire file* and checks that it's grammatically valid Python.
Nothing runs during this phase. Only if the whole file parses does Python go back to the
top and start executing, one line at a time, top to bottom.

<figure class="figure">
<svg viewBox="0 0 740 300" role="img" aria-label="Running a Python file happens in two phases. Python first parses the whole file; if the grammar is wrong it stops with a SyntaxError and nothing runs, so no output appears at all. If parsing succeeds, Python executes the file line by line from the top, and each line can print to the terminal or read input from it. An error during this second phase produces a traceback, and any output printed before that point already really happened.">
  <defs>
    <marker id="p-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="currentColor"/>
    </marker>
    <marker id="p-ar-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/>
    </marker>
  </defs>

  <g font-family="system-ui, sans-serif" font-size="12" fill="currentColor">

    <!-- the file -->
    <rect x="8" y="86" width="146" height="96" rx="9" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.45"/>
    <text x="81" y="108" text-anchor="middle" font-family="ui-monospace, monospace" font-size="11.5" font-weight="600">greet.py</text>
    <text x="22" y="132" font-family="ui-monospace, monospace" font-size="10" opacity="0.6">name = input(...)</text>
    <text x="22" y="148" font-family="ui-monospace, monospace" font-size="10" opacity="0.6">print(f"Hi {name}")</text>
    <text x="22" y="164" font-family="ui-monospace, monospace" font-size="10" opacity="0.6">print("bye")</text>

    <!-- parse -->
    <rect x="214" y="86" width="146" height="96" rx="9" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.45"/>
    <text x="287" y="112" text-anchor="middle" font-weight="600">1. parse</text>
    <text x="287" y="132" text-anchor="middle" font-size="10.5" opacity="0.65">reads the whole file,</text>
    <text x="287" y="146" text-anchor="middle" font-size="10.5" opacity="0.65">checks the grammar,</text>
    <text x="287" y="160" text-anchor="middle" font-size="10.5" opacity="0.65">runs nothing</text>

    <!-- execute -->
    <rect x="420" y="86" width="146" height="96" rx="9" fill="var(--accent-tint)" stroke="var(--accent)" stroke-width="1.8"/>
    <text x="493" y="112" text-anchor="middle" font-weight="600">2. execute</text>
    <text x="493" y="132" text-anchor="middle" font-size="10.5" fill="var(--accent)">one line at a time,</text>
    <text x="493" y="146" text-anchor="middle" font-size="10.5" fill="var(--accent)">top to bottom,</text>
    <text x="493" y="160" text-anchor="middle" font-size="10.5" fill="var(--accent)">in order</text>

    <!-- terminal -->
    <rect x="606" y="86" width="126" height="96" rx="9" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.45"/>
    <text x="669" y="112" text-anchor="middle" font-weight="600">terminal</text>
    <text x="669" y="140" text-anchor="middle" font-size="10.5" opacity="0.65">what you see,</text>
    <text x="669" y="154" text-anchor="middle" font-size="10.5" opacity="0.65">what you type</text>

    <!-- forward arrows -->
    <line x1="160" y1="134" x2="208" y2="134" stroke="currentColor" stroke-width="1.8" marker-end="url(#p-ar)"/>
    <text x="184" y="124" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10">python</text>

    <line x1="366" y1="134" x2="414" y2="134" stroke="var(--accent)" stroke-width="2" marker-end="url(#p-ar-a)"/>
    <text x="390" y="124" text-anchor="middle" font-size="10.5" font-weight="600" fill="var(--accent)">valid</text>

    <line x1="572" y1="118" x2="600" y2="118" stroke="currentColor" stroke-width="1.6" marker-end="url(#p-ar)"/>
    <text x="586" y="108" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10">print</text>

    <line x1="600" y1="164" x2="572" y2="164" stroke="currentColor" stroke-width="1.6" marker-end="url(#p-ar)"/>
    <text x="586" y="180" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10">input</text>

    <!-- failure paths -->
    <line x1="287" y1="188" x2="287" y2="212" stroke="currentColor" stroke-width="1.4" stroke-dasharray="5 4" opacity="0.6" marker-end="url(#p-ar)"/>
    <text x="295" y="205" font-size="10" opacity="0.7">bad grammar</text>

    <line x1="493" y1="188" x2="493" y2="212" stroke="currentColor" stroke-width="1.4" stroke-dasharray="5 4" opacity="0.6" marker-end="url(#p-ar)"/>
    <text x="501" y="205" font-size="10" opacity="0.7">bad value</text>

    <rect x="176" y="214" width="196" height="62" rx="8" fill="none" stroke="currentColor" stroke-width="1.3" opacity="0.5"/>
    <text x="274" y="236" text-anchor="middle" font-family="ui-monospace, monospace" font-size="11" font-weight="600">SyntaxError</text>
    <text x="274" y="254" text-anchor="middle" font-size="10.5" opacity="0.7">nothing ran at all —</text>
    <text x="274" y="268" text-anchor="middle" font-size="10.5" opacity="0.7">you get no output</text>

    <rect x="404" y="214" width="230" height="62" rx="8" fill="none" stroke="currentColor" stroke-width="1.3" opacity="0.5"/>
    <text x="519" y="236" text-anchor="middle" font-family="ui-monospace, monospace" font-size="11" font-weight="600">Traceback</text>
    <text x="519" y="254" text-anchor="middle" font-size="10.5" opacity="0.7">the lines above it really ran —</text>
    <text x="519" y="268" text-anchor="middle" font-size="10.5" opacity="0.7">the last line names the problem</text>

  </g>
</svg>
<figcaption>Two phases, two kinds of failure. Whether any output appeared before the error
tells you which phase you were in — and that's the first question to ask when a program
misbehaves.</figcaption>
</figure>

Three consequences worth holding on to.

**A `SyntaxError` means you typed something that isn't Python**, not that your logic is
wrong. A missing colon, an unclosed bracket, a stray quote. Because nothing ran, you see
no output at all — even from lines *above* the mistake. That absence is itself a clue.

**Any other error happened mid-run**, so whatever printed before it genuinely happened.
Python then stops immediately: lines after the failure never execute.

**Order is everything.** Python has no idea what's coming later in the file. Use a
variable on line 2 that you only create on line 5 and you get a `NameError`, because on
line 2 that name genuinely didn't exist yet.

## In practice

Open a terminal in this folder and activate your venv from lesson 00-02 — your prompt
should start with `(.venv)`:

```powershell
.\.venv\Scripts\Activate.ps1
```

### The shell, for throwaway experiments

Type `python` on its own and you get the **interactive shell**: it runs a line the moment
you press Enter and shows the result. It's a scratchpad, not somewhere you write
programs.

```powershell
python
```

```text
Python 3.14.3 ...
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

`>>>` is Python waiting for you. Try these:

```python
>>> 2 + 2
4
>>> print("hello")
hello
>>> "hello"
'hello'
```

Notice the difference between the last two. `print("hello")` *displays* the text. Typing
`"hello"` on its own shows you how Python would *write it down* — with quotes, because
it's a string. Only the shell does that second thing; in a real script, nothing appears
unless you print it.

Type `exit()` and press Enter to get out.

### A file you can run again

Create the file — this is the program you'll keep. `builds/` already exists in this repo,
so you only need one command:

```powershell
code builds/00-04-greet.py
```

`code` opens a file in VS Code, creating it if it isn't there yet. If your terminal says
`code` isn't recognised, just make the file in VS Code's file explorer instead.

A note on typing these, since it bites everyone once: **each line in a code block here is
its own command.** Type it, press Enter, wait for the prompt to come back, then type the
next one. Pressing Enter is how you run a command in a terminal — there's no separate
"submit" step, and a newline can't be typed *into* a command. If you do want two commands
on one line, the separator is a semicolon: `mkdir notes; code notes/scratch.md`.

Type this in, and save with `Ctrl+S`:

```python
print("Hello, world.")
print("This file ran top to bottom.")
```

Run it from the terminal:

```powershell
python builds/00-04-greet.py
```

```text
Hello, world.
This file ran top to bottom.
```

Two lines of source, two lines of output, in order. That's the diagram, working.

### Variables and types

A **variable** is a name pointing at a value. `=` doesn't mean "equals" here — it means
"make this name refer to this value". Replace the file's contents with:

```python
name = "Jack"
lessons_done = 3

print(name)
print(lessons_done)
```

```text
Jack
3
```

`"Jack"` in quotes is a **string** — text. `3` without quotes is an **integer** — a
number. The difference isn't pedantry; it decides what operations mean:

```python
print("3" + "4")
print(3 + 4)
```

```text
34
7
```

`+` joins strings and adds numbers. Same symbol, different behaviour depending on the
types either side of it. Mixing the two is an error rather than a guess:

```python
print("Lessons: " + 3)
```

```text
Traceback (most recent call last):
  File "E:\Claude Knowledge\builds\00-04-greet.py", line 1, in <module>
    print("Lessons: " + 3)
          ~~~~~~~~~~~~^~~
TypeError: can only concatenate str (not "int") to str
```

**Read a traceback from the bottom up.** The last line is the actual problem —
`TypeError: can only concatenate str (not "int") to str` — and just above it is the file
and line number, with the offending code quoted and the `^` marks pointing at the part
that failed. Everything else is context. That bottom line is usually enough to fix it;
when it isn't, it's the exact phrase to paste into a search or into Claude.

### f-strings: the way to build text

You could convert the number by hand with `str(3)`, but nobody does that in practice. Put
an `f` in front of the opening quote and you can drop values straight into the text
inside `{}`:

```python
name = "Jack"
lessons_done = 3

print(f"{name} has finished {lessons_done} lessons.")
```

```text
Jack has finished 3 lessons.
```

An **f-string** (formatted string literal) evaluates whatever is inside each `{}` and
converts the result to text for you. Anything can go in there, not just a bare name:

```python
print(f"After this one: {lessons_done + 1}")
print(f"Shouted: {name.upper()}")
```

```text
After this one: 4
Shouted: JACK
```

Forget the `f` and you get exactly what you typed, braces included — a bug with no error
message at all, which is why it's worth seeing once:

```python
print("{name} has finished")
```

```text
{name} has finished
```

### Asking a question

`input()` prints a prompt, waits for the person to type a line and press Enter, and hands
back what they typed:

```python
name = input("What's your name? ")
print(f"Hello, {name}.")
```

```powershell
python builds/00-04-greet.py
```

```text
What's your name? Jack
Hello, Jack.
```

**`input()` always returns a string**, even when the person types digits. This is the
single most common beginner surprise:

```python
age = input("Age? ")
print(age + 1)
```

```text
Age? 30
Traceback (most recent call last):
  File "E:\Claude Knowledge\builds\00-04-greet.py", line 2, in <module>
    print(age + 1)
          ~~~~^~~
TypeError: can only concatenate str (not "int") to str
```

`"30"` is text that happens to look like a number. Convert it deliberately with `int()`:

```python
age = int(input("Age? "))
print(age + 1)
```

```text
Age? 30
31
```

And if they type `thirty`, `int()` refuses rather than guessing — `ValueError: invalid
literal for int() with base 10: 'thirty'`. Handling that gracefully is lesson 01-06's
job; for now, just learn to recognise the message.

### Tidying what people type

People type stray spaces. `.strip()` removes whitespace from both ends of a string, and
`.title()` capitalises each word:

```python
name = input("What's your name? ").strip().title()
print(f"Hello, {name}.")
```

Typing `"  jack  "` now gives `Hello, Jack.` Methods chain left to right: strip first,
then title-case whatever strip handed back.

## Build it

A script that asks for your name and prints a formatted greeting, committed to git.

**1. Branch first** — you learned this last lesson, so use it:

```powershell
git switch -c lesson/00-04
```

**2. Write `builds/00-04-greet.py`.** It must:

- ask for a name with `input()`, and clean it with `.strip()`
- ask for one number — how many lessons you've finished — and convert it with `int()`
- print a greeting of at least two lines using **f-strings**, one of which does a small
  calculation inside the braces (the lesson number you're on next, for instance)
- start with a one-line `#` comment saying what the file does

`#` starts a comment: Python ignores the rest of that line. Write it for yourself in
three months.

**3. Run it at least three times** — a normal name, a name with spaces around it, and
once typing a word instead of a number so you see the `ValueError` on purpose. Errors you
caused deliberately are much cheaper to read than ones that ambush you.

**4. Commit and merge:**

```powershell
git add builds/00-04-greet.py
git commit -m "Add greeting script from lesson 00-04"
git switch main
git merge lesson/00-04
git branch -d lesson/00-04
git push
```

Done when:

- `python builds/00-04-greet.py` runs, asks two questions, and prints your greeting
- Leading and trailing spaces in the name don't appear in the output
- At least one `{}` in your file contains a calculation, not just a variable name
- Typing `abc` at the number prompt produces a `ValueError`, and you can say in your own
  words which line caused it and why
- `git log --oneline -3` shows your commit on `main`
- `git status` prints `nothing to commit, working tree clean`

Then log it:

```powershell
python tools/progress_log.py --lesson-id 00-04 --status complete --minutes 45 --artifact ./builds/00-04-greet.py --note "first program I wrote myself"
python tools/site_build.py --open
```

## Going deeper

- Add a third question and print a number to two decimal places with `f"{value:.2f}"`.
  The part after the `:` is a **format specifier**; skim
  [Input and output](https://docs.python.org/3/tutorial/inputoutput.html) for what else
  can go there.
- Break your script on purpose, one way at a time, and note what each failure looks like:
  delete a closing bracket, misspell a variable name, remove the `int()`. Aim to predict
  `SyntaxError`, `NameError` and `TypeError` before you press Enter.
- Try `print(f"{name=}")` — the `=` inside the braces prints the variable's *name and its
  value*. It's the fastest debugging tool in the language.
- Read [Errors and exceptions](https://docs.python.org/3/tutorial/errors.html) as far as
  the end of section 8.2, then use `type()` to check what `input()` actually returns.
- Work through chapter 1 of
  [Automate the Boring Stuff](https://automatetheboringstuff.com/3e/chapter1.html), free
  online. Same ground, different examples — which is how you find out whether it stuck.
- Look up why `print` needs parentheses. The answer involves Python 2, and it explains a
  lot of the broken tutorial code you'll find online.

## Check yourself

<details markdown="1"><summary>Your script prints three lines, then hits an error. Someone says "so nothing ran." Are they right?</summary>

No. Output appeared, so the file parsed successfully and Python was already in the
execution phase — those three lines really ran, and any effects they had are real. The
error happened on a later line, and everything after it never ran.

The reverse case is the informative one: an error with *no* output at all usually means a
`SyntaxError`, where Python rejected the file before running a single line.

</details>

<details markdown="1"><summary>You write `total = input("How many? ") + 10` and get `TypeError: can only concatenate str (not "int") to str`. What's the fix, and why is Python being fussy rather than helpful?</summary>

`total = int(input("How many? ")) + 10`. `input()` always hands back a string, so you
asked Python to join `"5"` and `10`, which have no shared meaning for `+`.

Python refuses to guess because the guess would sometimes be wrong: `"5" + 10` could
reasonably mean `15` or `"510"`, and a program that quietly picks the wrong one is far
worse than one that stops and tells you. Making the conversion explicit puts your intent
in the code where you can see it.

</details>

<details markdown="1"><summary>`print("Hi {name}")` prints `Hi {name}` literally, and no error appears. What went wrong, and why is the absence of an error the interesting part?</summary>

The `f` is missing. Without it, the braces are just characters in a piece of text, so
Python did precisely what you asked.

It's interesting because it's a whole category of bug: the program is valid, it runs, and
it's wrong. No traceback will ever point at it — the only thing that catches it is you
looking at the output and noticing it isn't what you meant. Which is why the loop is "run
it and read what came back", not "run it until the red text stops".

</details>

<details markdown="1"><summary>A traceback is six lines long. Which line do you read first, and what is the rest for?</summary>

The last one. It names the exception type and describes the problem in a sentence —
`TypeError: can only concatenate...`, `NameError: name 'nmae' is not defined`. That's
usually enough to know what to fix.

The lines above give you *where*: file, line number, and the offending code. You read
upward only when the bottom line alone isn't enough. The phrase "most recent call last"
at the top is the hint — Python puts the important part at the bottom deliberately.

</details>

<details markdown="1"><summary>You put `print(greeting)` on line 2 and `greeting = "hi"` on line 5. Python is happy with the grammar of both lines. What happens when you run it?</summary>

`NameError: name 'greeting' is not defined`, pointing at line 2.

Parsing only checks that each line is well-formed Python, and `print(greeting)` is
perfectly well-formed — so the file passes phase one with no complaint. Phase two runs in
order, and when line 2 executes, nothing called `greeting` exists yet. Line 5 never gets
a chance, because Python stops at the error.

</details>
