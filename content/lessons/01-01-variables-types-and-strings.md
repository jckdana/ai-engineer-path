---
id: "01-01"
title: "Variables, types, and strings"
module: "01"
core_minutes: 50
deep_minutes: 110
build: "A script that cleans a messy string: strips whitespace, fixes capitalisation, counts words."
resources:
  - title: "Python docs — string methods (the full list)"
    url: "https://docs.python.org/3/library/stdtypes.html#string-methods"
  - title: "Python tutorial — text, indexing, slicing, immutability"
    url: "https://docs.python.org/3/tutorial/introduction.html"
  - title: "Python docs — type() and isinstance()"
    url: "https://docs.python.org/3/library/functions.html#type"
  - title: "Python reference — f-strings and replacement fields"
    url: "https://docs.python.org/3/reference/lexical_analysis.html#f-strings"
  - title: "Automate the Boring Stuff, chapter 8 — Strings and Text Editing (free online)"
    url: "https://automatetheboringstuff.com/3e/chapter8.html"
---

## Why this matters

Last lesson you sent a question to a model and got an answer back. Look closely at what
actually crossed the wire: a piece of text went out, and a piece of text came back.
That's the shape of nearly all AI work. Prompts are strings. Model replies are strings.
Scraped pages, CSV rows, log lines, user input — strings, all of them, and almost none
of them arrive clean.

So the skill this lesson buys you is unglamorous and used constantly: taking text that's
a mess — ragged spacing, shouty capitals, invisible characters on the end — and turning
it into something predictable enough to act on. Real text has trailing spaces you can't
see, `"YES"` where you expected `"yes"`, and three spaces where you expected one. If you
compare that text to something without cleaning it first, you get a wrong answer with no
error message, which is the most expensive kind of wrong.

By the end you'll know what type a value is and how to check, why `"3" + 4` is an error
rather than a guess, and — the part that trips up nearly everyone — why calling
`.strip()` on your text can leave it exactly as messy as before.

## The mental model

A variable is a **name pointing at a value**. That's not a metaphor, it's the mechanism,
and it explains the single most common bug beginners write.

Here's the fact that causes it: **strings in Python are immutable**. Once a string
exists, nothing can change it. So `.strip()`, `.lower()`, `.replace()` and every other
string method do *not* edit your text. They build a brand-new string and hand it back.
If you don't catch what they hand back, it's thrown away, and your variable still points
at the old messy value.

<figure class="figure">
<svg viewBox="0 0 760 306" role="img" aria-label="A comparison of two lines of code. In the first, text.strip() is written on its own line: the name text points at the original string with spaces, strip builds a new trimmed string, but because nothing catches the result the new string is discarded and text still points at the messy original. In the second, text is assigned the result of text.strip(): the same new string is built, but the equals sign re-points the name text at the new trimmed string, and the original becomes unreachable. Only the second line actually cleans the variable.">
  <defs>
    <marker id="s-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="currentColor"/>
    </marker>
    <marker id="s-ar-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/>
    </marker>
  </defs>

  <g font-family="system-ui, sans-serif" font-size="12" fill="currentColor">

    <!-- ROW A : result discarded -->
    <text x="14" y="40" font-family="ui-monospace, monospace" font-size="12.5" font-weight="600">text.strip()</text>
    <text x="14" y="58" font-size="10.5" opacity="0.65">no assignment</text>

    <rect x="150" y="30" width="62" height="32" rx="7" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.55"/>
    <text x="181" y="51" text-anchor="middle" font-family="ui-monospace, monospace" font-size="11.5">text</text>

    <line x1="216" y1="46" x2="256" y2="46" stroke="currentColor" stroke-width="1.7" marker-end="url(#s-ar)"/>
    <text x="236" y="37" text-anchor="middle" font-size="9.5" opacity="0.7">points at</text>

    <rect x="258" y="26" width="122" height="40" rx="7" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.55"/>
    <text x="319" y="51" text-anchor="middle" font-family="ui-monospace, monospace" font-size="11.5">"&#160;&#160;hello&#160;&#160;"</text>

    <line x1="384" y1="46" x2="440" y2="46" stroke="currentColor" stroke-width="1.7" marker-end="url(#s-ar)"/>
    <text x="412" y="37" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9.5">.strip()</text>
    <text x="412" y="61" text-anchor="middle" font-size="9.5" opacity="0.7">builds</text>

    <rect x="442" y="26" width="102" height="40" rx="7" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.55"/>
    <text x="493" y="51" text-anchor="middle" font-family="ui-monospace, monospace" font-size="11.5">"hello"</text>

    <line x1="548" y1="46" x2="596" y2="46" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5 4" opacity="0.6" marker-end="url(#s-ar)"/>
    <text x="572" y="37" text-anchor="middle" font-size="9.5" opacity="0.7">nothing</text>
    <text x="572" y="61" text-anchor="middle" font-size="9.5" opacity="0.7">catches it</text>

    <text x="604" y="42" font-size="11" font-weight="600" opacity="0.8">discarded</text>
    <text x="604" y="58" font-size="10.5" opacity="0.65">text is still messy</text>

    <line x1="14" y1="104" x2="746" y2="104" stroke="currentColor" stroke-width="1" opacity="0.25"/>

    <!-- ROW B : result kept -->
    <text x="14" y="170" font-family="ui-monospace, monospace" font-size="12.5" font-weight="600" fill="var(--accent)">text = text.strip()</text>
    <text x="14" y="188" font-size="10.5" opacity="0.65">assigned back</text>

    <rect x="150" y="160" width="62" height="32" rx="7" fill="var(--accent-tint)" stroke="var(--accent)" stroke-width="1.8"/>
    <text x="181" y="181" text-anchor="middle" font-family="ui-monospace, monospace" font-size="11.5" fill="var(--accent)">text</text>

    <line x1="216" y1="176" x2="256" y2="176" stroke="currentColor" stroke-width="1.4" stroke-dasharray="4 4" opacity="0.35"/>
    <line x1="230" y1="168" x2="242" y2="184" stroke="currentColor" stroke-width="1.6" opacity="0.5"/>
    <line x1="242" y1="168" x2="230" y2="184" stroke="currentColor" stroke-width="1.6" opacity="0.5"/>

    <rect x="258" y="156" width="122" height="40" rx="7" fill="none" stroke="currentColor" stroke-width="1.4" opacity="0.3"/>
    <text x="319" y="181" text-anchor="middle" font-family="ui-monospace, monospace" font-size="11.5" opacity="0.4">"&#160;&#160;hello&#160;&#160;"</text>
    <text x="319" y="212" text-anchor="middle" font-size="10" opacity="0.55">now unreachable</text>

    <line x1="384" y1="176" x2="440" y2="176" stroke="currentColor" stroke-width="1.7" marker-end="url(#s-ar)"/>
    <text x="412" y="167" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9.5">.strip()</text>
    <text x="412" y="191" text-anchor="middle" font-size="9.5" opacity="0.7">builds</text>

    <rect x="442" y="156" width="102" height="40" rx="7" fill="var(--accent-tint)" stroke="var(--accent)" stroke-width="1.8"/>
    <text x="493" y="181" text-anchor="middle" font-family="ui-monospace, monospace" font-size="11.5" fill="var(--accent)">"hello"</text>

    <path d="M 181 196 C 181 258, 400 268, 486 202" fill="none" stroke="var(--accent)" stroke-width="2" marker-end="url(#s-ar-a)"/>
    <text x="330" y="272" text-anchor="middle" font-size="11" font-weight="600" fill="var(--accent)">= re-points the name at the new string</text>

    <text x="604" y="172" font-size="11" font-weight="600" fill="var(--accent)">kept</text>
    <text x="604" y="188" font-size="10.5" opacity="0.65">text is now clean</text>

  </g>
</svg>
<figcaption>Both lines build the same trimmed string. The only difference is whether
anything catches it — and that difference is the whole bug. A string method never
changes the string you called it on.</figcaption>
</figure>

Two consequences worth carrying forward.

**A string method with no `=` in front of it is almost always a mistake.** The line runs,
Python raises nothing, and your data is untouched. There's no error to read, so the only
thing that catches it is printing the value and looking.

**Trying to edit a string in place is a hard error**, which is Python being consistent
rather than awkward:

```python
word = "python"
word[0] = "P"
```

```text
TypeError: 'str' object does not support item assignment
```

You don't modify a string. You build the string you wanted and point a name at it.

## In practice

Activate your venv so your prompt starts with `(.venv)`:

```powershell
.\.venv\Scripts\Activate.ps1
```

Start the interactive shell — this whole section is worth doing there, because it shows
you every result without needing `print()`:

```powershell
python
```

### Four types you'll meet constantly

```python
>>> name = "Jack"
>>> lessons = 6
>>> hours = 7.5
>>> finished = True
```

Those are the four basic types: `str` (text), `int` (whole number), `float` (number with
a decimal point), and `bool` (`True` or `False` — note the capitals; `true` is a
`NameError`). When you're unsure what you're holding, ask:

```python
>>> type(name)
<class 'str'>
>>> type(lessons)
<class 'int'>
>>> type(hours)
<class 'float'>
>>> type(finished)
<class 'bool'>
```

`type()` is a debugging tool you'll reach for constantly, because the confusing bugs are
nearly always "this isn't the type I thought it was". Quotes are what make the
difference, not the characters inside:

```python
>>> type(6)
<class 'int'>
>>> type("6")
<class 'str'>
>>> "6" + 6
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: can only concatenate str (not "int") to str
```

You met that error last lesson. Now you can name why: `+` means *join* between two
strings and *add* between two numbers, and Python refuses to pick one for you.

### Strings don't change — prove it to yourself

This is the lesson's core idea, so run it rather than reading it:

```python
>>> text = "   Hello World   "
>>> text.strip()
'Hello World'
>>> text
'   Hello World   '
```

Line two *showed* you a clean string. Line four proves `text` never changed — the shell
displayed the new string and then threw it away. Keep it and the picture changes:

```python
>>> text = text.strip()
>>> text
'Hello World'
```

Read `text = text.strip()` right-to-left: build a trimmed copy of whatever `text` points
at, then point `text` at that copy. The name is reused; the value is new.

### The cleaning toolkit

`.strip()` removes whitespace — spaces, tabs, newlines — from **both ends only**, never
the middle:

```python
>>> "   spacious   ".strip()
'spacious'
>>> "  a  b  ".strip()
'a  b'
```

Note the two spaces between `a` and `b` survived. Inner whitespace needs `.split()`,
which we'll get to in a moment.

`.strip()` also accepts characters to remove — and this is a genuine trap, worth seeing
once so it never costs you an hour:

```python
>>> "www.example.com".strip("cmowz.")
'example'
>>> "Monty Python".strip(" Python")
'M'
```

The argument is a **set of characters**, not a prefix. Python chewed `" Python"` off the
end letter by letter — the `n`, the `o`, the `h`, the `t`, the `y`, the space — and kept
going into `Monty` until it hit a character not in the set. To remove an actual prefix
or suffix, use `.removeprefix()` and `.removesuffix()` instead.

For case, you have four options and they differ in ways that matter:

```python
>>> "HELLO World".lower()
'hello world'
>>> "hello world".upper()
'HELLO WORLD'
>>> "hello world".capitalize()
'Hello world'
>>> "hello world".title()
'Hello World'
```

`.capitalize()` does the first letter of the *string*; `.title()` does the first letter
of every *word*. `.title()` also has a documented wart:

```python
>>> "don't stop".title()
"Don'T Stop"
```

It capitalises after any non-letter, and an apostrophe is a non-letter. Which is the
real lesson: `.title()` is fine for a name field, wrong for a sentence. Pick the method
that matches your data.

For **comparing** text, use `.lower()` — or better, `.casefold()`, which is built for
exactly that job and handles cases `.lower()` won't:

```python
>>> "YES" == "yes"
False
>>> "YES".lower() == "yes"
True
>>> "straße".lower()
'straße'
>>> "straße".casefold()
'strasse'
```

`==` on strings is exact, character for character. Nearly every "why didn't my check
match?" bug is a case difference or an invisible trailing space.

### Splitting text into words

`.split()` cuts a string into a **list** of pieces. Called with no argument, it splits on
any run of whitespace and drops the empties — which is exactly what you want for
counting words:

```python
>>> "the quick brown fox".split()
['the', 'quick', 'brown', 'fox']
>>> "   the   quick   brown   ".split()
['the', 'quick', 'brown']
```

Three spaces between words, and it still produced three clean pieces. Compare that with
passing a separator explicitly:

```python
>>> "the   quick".split(" ")
['the', '', '', 'quick']
```

With an argument, every single space is a cut, so the runs produced empty strings. **The
no-argument version is the one you want for words.** A list is the next lesson's topic;
for now the only thing you need from it is its length:

```python
>>> len("the quick brown fox".split())
4
>>> len("the quick brown fox")
19
```

`len()` on a list counts items; `len()` on a string counts characters, spaces included.
Same function, and what it counts depends on what you hand it.

`.join()` is `.split()` in reverse, and it's how you squash inner whitespace:

```python
>>> " ".join(["the", "quick"])
'the quick'
>>> " ".join("  the   quick   brown  ".split())
'the quick brown'
```

Read that last line inside-out: split on any whitespace (giving clean pieces), then glue
them back with exactly one space between each. That single expression normalises the
spacing of any text you'll ever be handed.

Two more you'll use weekly — `.replace()`, and `in` for asking whether text contains
something:

```python
>>> "spam, spam, spam".replace("spam", "eggs")
'eggs, eggs, eggs'
>>> "error" in "connection error: timed out"
True
```

Type `exit()` to leave the shell.

### Chaining, and where it stops being readable

Methods return strings, so you can call another one straight away:

```python
>>> "  JACK  ".strip().lower()
'jack'
```

That reads left to right: strip, then lowercase the result. Chaining three or four is
fine; chaining eight becomes a line nobody can debug, because when the output is wrong
you can't see which step did it. Break long chains into named steps — you'll do exactly
that in the build.

## Build it

A script that takes a deliberately messy piece of text and cleans it up, then reports on
what changed.

**1. Branch first:**

```powershell
git switch -c lesson/01-01
```

**2. Write `builds/01-01-clean.py`.** Start with this messy text pasted in as-is — the
`\t` is a tab and the `\n` is a line break, both of which count as whitespace:

```python
# Cleans a messy string and reports on what changed.

raw = "\n\t  the QUICK   brown fox    jumped over    the LAZY dog.  \n"
```

Your script must then:

- record the original character count with `len()` **before** cleaning anything
- produce a `cleaned` string that has no leading or trailing whitespace, has exactly one
  space between words, and is all lowercase — assigning each step to a name rather than
  writing one long chain
- count the words using `.split()` and `len()`
- count the characters in the cleaned string
- print a report using **f-strings**, showing the original text, the cleaned text, the
  word count, and how many characters were removed (a calculation inside the braces)
- print the original text *after* the cleaning is done, to prove for yourself that
  cleaning built a new string rather than altering `raw`

Wrap the two texts in your output like `f"[{raw}]"` — the brackets make the leftover
whitespace visible, which is the only way to see whitespace at all.

**3. Run it and read the output.** Then break it on purpose once: change one line from
`cleaned = cleaned.lower()` to just `cleaned.lower()`, run it again, and watch the
capitals survive with no error message. Put it back.

**4. Commit and merge:**

```powershell
git add builds/01-01-clean.py
git commit -m "Add string cleaner from lesson 01-01"
git switch main
git merge lesson/01-01
git branch -d lesson/01-01
git push
```

Done when:

- `python builds/01-01-clean.py` prints a report with no errors
- The cleaned text is `the quick brown fox jumped over the lazy dog.` — one space
  between every word, nothing on either end
- The word count prints `9`
- The report shows how many characters were removed, calculated inside an f-string
- Printing `raw` at the end still shows the original mess, and you can say why
- You saw the dropped-`=` version leave the text uppercase without raising an error
- `git log --oneline -3` shows your commit on `main`, and `git status` is clean

Then log it:

```powershell
python tools/progress_log.py --lesson-id 01-01 --status complete --minutes 50 --artifact ./builds/01-01-clean.py --note "what clicked"
python tools/site_build.py --open
```

## Going deeper

- Add a `.replace()` step that swaps a word, and use `in` to print whether the cleaned
  text contains `"fox"`.
- Take the messy text from `input()` instead of hard-coding it, and make sure your
  cleaning still works when someone types nothing but spaces. What does `len("".split())`
  give you, and is that the answer you wanted?
- Try slicing: `cleaned[0]`, `cleaned[:3]`, `cleaned[-1]`, `cleaned[::-1]`. Skim the
  [text section of the tutorial](https://docs.python.org/3/tutorial/introduction.html)
  for how the start and end positions work, then predict `cleaned[0:3]` before running it.
- Read through the [full list of string methods](https://docs.python.org/3/library/stdtypes.html#string-methods).
  Don't memorise it — just build a rough map of what exists, so later you search rather
  than reinvent. Look specifically at `.startswith()`, `.count()`, and `.removeprefix()`.
- Explore f-string format specifiers: `f"{3.14159:.2f}"`, `f"{cleaned!r}"` (which shows
  the string the way Python would write it, quotes and all — the fastest way to reveal
  hidden whitespace), and `f"{words=}"`. The
  [f-string reference](https://docs.python.org/3/reference/lexical_analysis.html#f-strings)
  covers all three.
- Work through [chapter 8 of Automate the Boring Stuff](https://automatetheboringstuff.com/3e/chapter8.html),
  free online. It covers the same methods plus escape sequences and multiline strings.
- **Worth knowing now, for later:** models don't read words, they read *tokens*, and a
  word count is not a token count. When you need a real number, the Anthropic API has a
  dedicated `count_tokens` endpoint that tells you exactly — you'll use it when cost and
  context limits start to matter. Never estimate tokens by counting words.

## Check yourself

<details markdown="1"><summary>You write `answer.strip()` then compare `answer == "yes"`, and it's `False` even though the user clearly typed yes. Give two separate reasons this could happen.</summary>

**One:** `answer.strip()` on its own line does nothing to `answer`. It built a trimmed
string and discarded it. The trailing whitespace is still there, so you're comparing
`"yes "` with `"yes"`. The fix is `answer = answer.strip()`.

**Two:** they typed `Yes` or `YES`. `==` on strings is exact, so case alone breaks it.
The fix is to compare `answer.lower() == "yes"` (or `.casefold()`).

Both failures are silent — no traceback, just a wrong answer — which is why cleaning
before comparing is a habit rather than a special case.

</details>

<details markdown="1"><summary>`"  a  b  ".strip()` gives `'a  b'`, not `'a b'`. Why, and what actually collapses the inner spaces?</summary>

`.strip()` only touches the two ends. It walks in from the left and in from the right,
removing whitespace until it hits something that isn't whitespace — and then it stops.
Anything between those two points is left exactly as it was.

To normalise the middle, split and rejoin: `" ".join("  a  b  ".split())` gives `'a b'`.
The no-argument `.split()` treats any run of whitespace as one separator and drops the
empty pieces, and `" ".join(...)` puts back exactly one space between each piece. As a
bonus it strips the ends too, so it does both jobs at once.

</details>

<details markdown="1"><summary>Someone cleans a filename with `"report.txt".strip(".txt")` and gets `'repor'`. What did they assume, and what should they have used?</summary>

They assumed the argument is a suffix to remove. It isn't — it's a **set of characters**.
Python removed any of `.`, `t`, `x` from each end repeatedly: it took `.txt` off the
right, then kept going and ate the final `t` of `report`, stopping at `r`.

The right tool is `"report.txt".removesuffix(".txt")`, which matches the exact string or
does nothing at all. Same trap as `"Monty Python".strip(" Python")` giving `'M'`.

</details>

<details markdown="1"><summary>You have `count = "12"` from somewhere and write `count + 1`. Predict the exact error, then explain why Python won't just do the sensible thing.</summary>

`TypeError: can only concatenate str (not "int") to str`.

`"12"` is text that looks like a number. `+` between two strings joins them and between
two numbers adds them, so Python has two plausible readings of `"12" + 1`: `13`, or
`"121"`. Both are defensible, which is precisely why guessing would be dangerous — a
program that silently picks the wrong one produces bad data that nothing flags.

Convert explicitly with `int(count) + 1`, and your intent is visible in the code. Use
`type(count)` to check when you're unsure what you're holding.

</details>

<details markdown="1"><summary>Your word counter returns 7 for a sentence you can see has 5 words. The text came from a web page. What's the most likely cause, and how would you find it in ten seconds?</summary>

Something you can't see is being counted as a word — most likely stray punctuation or
non-word fragments separated by whitespace, or line breaks and tabs splitting a word
across pieces.

The ten-second diagnosis is to stop guessing and look. Print the list itself rather than
its length — `print(text.split())` — and the pieces appear individually, in quotes. An
`f"{text!r}"` does the same job for the raw string, showing `\n` and `\t` explicitly
instead of rendering them invisibly.

The general habit: when a count is wrong, print the thing being counted, not the count.

</details>
