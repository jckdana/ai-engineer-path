---
id: "01-02"
title: "Lists, loops, and conditionals"
module: "01"
core_minutes: 55
deep_minutes: 120
build: "A script that reads a list of questions and sends each one to a model, printing results as it goes."
resources:
  - title: "Python tutorial — if, for, range, break and continue"
    url: "https://docs.python.org/3/tutorial/controlflow.html"
  - title: "Python tutorial — lists, list methods, comprehensions"
    url: "https://docs.python.org/3/tutorial/datastructures.html"
  - title: "Python docs — enumerate() and its start argument"
    url: "https://docs.python.org/3/library/functions.html#enumerate"
  - title: "Python docs — truth value testing (what counts as false)"
    url: "https://docs.python.org/3/library/stdtypes.html#truth-value-testing"
  - title: "Automate the Boring Stuff, chapter 6 — Lists (free online)"
    url: "https://automatetheboringstuff.com/3e/chapter6.html"
  - title: "Automate the Boring Stuff, chapter 2 — if-else and flow control (free online)"
    url: "https://automatetheboringstuff.com/3e/chapter2.html"
  - title: "Anthropic docs — rate limits, 429 errors, and the retry-after header"
    url: "https://platform.claude.com/docs/en/api/rate-limits"
---

## Why this matters

Everything you've written so far handled exactly one thing: one question, one
messy string, one answer. Nobody pays for that. The work people pay for is
*"here are two hundred support emails, categorise them"* or *"here are fifty
product descriptions, rewrite each one"* — one operation, applied over and over,
without you sitting there pressing enter.

That's what a loop is. And the moment you have a loop, you need the other half:
deciding what to do when an item is different from the rest. Some of those two
hundred emails will be blank. Some will be in another language. A loop that
can't skip, stop, or branch is a loop that crashes on item forty-three and loses
everything it did on items one through forty-two.

By the end of this you'll be able to take a list of anything, do work on each
item, keep the results, and handle the odd ones without falling over. You'll
also meet the one bug that eats beginners here: putting a line one indent too
far in, so it quietly runs two hundred times when it should have run once.

One warning specific to this lesson, because it's the first time it applies:
**a loop around an API call costs money on every pass.** Five questions is five
calls. A typo that puts your call inside two loops instead of one is a bill.
You'll build the habit of doing a dry run first.

## The mental model

A **list** is an ordered container: `["a", "b", "c"]`. A **for loop** hands you
its items one at a time, re-pointing a name at each item in turn — the same
"name pointing at a value" idea from last lesson, just happening repeatedly.

What makes or breaks the loop is **where each line sits**. Python has no
braces; indentation *is* the block. Lines indented under `for` are the **body**
and run once per item. Lines at the outer level run once, before or after the
whole loop. Getting that boundary wrong is not a syntax error — it's a silent
logic error, which is worse.

<figure class="figure">
<svg viewBox="0 0 760 320" role="img" aria-label="A diagram of one for loop. On the left, a list named questions holds three items and feeds into the loop. Above the loop, at the outer indentation level, an accented line reads results equals empty list, created once before the loop so it survives every pass. Below it the line for q in questions begins the loop, and a dashed vertical line marks the indentation boundary: everything to the right of it is the body and runs once per item. The body contains three stacked steps, q re-pointed at the next item, answer set to the model's reply for q, and results dot append of answer. An accented curve runs from the results equals empty list line down into the append step, showing that every pass appends to that same one list. An arrow loops from the body back up to the for line, labelled next item. When the list runs out, an arrow exits to a box holding results with three answers.">
  <defs>
    <marker id="l-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="currentColor"/>
    </marker>
    <marker id="l-ar-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/>
    </marker>
  </defs>

  <g font-family="system-ui, sans-serif" font-size="12" fill="currentColor">

    <!-- the list -->
    <text x="14" y="48" font-family="ui-monospace, monospace" font-size="11.5" font-weight="600">questions</text>
    <rect x="14" y="58" width="118" height="96" rx="7" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.55"/>
    <text x="26" y="82" font-family="ui-monospace, monospace" font-size="10" opacity="0.8">"What is X?"</text>
    <text x="26" y="108" font-family="ui-monospace, monospace" font-size="10" opacity="0.8">"Why Y?"</text>
    <text x="26" y="134" font-family="ui-monospace, monospace" font-size="10" opacity="0.8">"How Z?"</text>
    <text x="73" y="172" text-anchor="middle" font-size="9.5" opacity="0.7">3 items</text>

    <line x1="136" y1="106" x2="194" y2="106" stroke="currentColor" stroke-width="1.7" marker-end="url(#l-ar)"/>
    <text x="165" y="98" text-anchor="middle" font-size="9.5" opacity="0.7">feeds</text>

    <!-- the accumulator, outside the loop -->
    <rect x="206" y="16" width="170" height="28" rx="7" fill="var(--accent-tint)" stroke="var(--accent)" stroke-width="1.8"/>
    <text x="291" y="35" text-anchor="middle" font-family="ui-monospace, monospace" font-size="11.5" fill="var(--accent)">results = []</text>
    <text x="390" y="28" font-size="10.5" font-weight="600">created once, before the loop</text>
    <text x="390" y="43" font-size="10" opacity="0.65">outer level — so it survives every pass</text>

    <!-- the for line -->
    <text x="206" y="86" font-family="ui-monospace, monospace" font-size="12.5" font-weight="600">for q in questions:</text>

    <!-- indentation boundary -->
    <line x1="222" y1="96" x2="222" y2="282" stroke="currentColor" stroke-width="1.4" stroke-dasharray="5 5" opacity="0.4"/>
    <text x="228" y="298" font-size="9.5" opacity="0.7">right of this dashed line = indented = the body</text>

    <!-- body -->
    <rect x="236" y="102" width="300" height="152" rx="8" fill="none" stroke="currentColor" stroke-width="1.4" opacity="0.35"/>

    <rect x="252" y="116" width="268" height="30" rx="6" fill="none" stroke="currentColor" stroke-width="1.4" opacity="0.55"/>
    <text x="266" y="136" font-family="ui-monospace, monospace" font-size="10.5">q &#8594; the next item, this pass</text>

    <line x1="386" y1="146" x2="386" y2="158" stroke="currentColor" stroke-width="1.6" marker-end="url(#l-ar)"/>

    <rect x="252" y="160" width="268" height="30" rx="6" fill="none" stroke="currentColor" stroke-width="1.4" opacity="0.55"/>
    <text x="266" y="180" font-family="ui-monospace, monospace" font-size="10.5">answer = the reply for q</text>

    <line x1="386" y1="190" x2="386" y2="202" stroke="currentColor" stroke-width="1.6" marker-end="url(#l-ar)"/>

    <rect x="252" y="204" width="268" height="30" rx="6" fill="none" stroke="currentColor" stroke-width="1.4" opacity="0.55"/>
    <text x="266" y="224" font-family="ui-monospace, monospace" font-size="10.5">results.append(answer)</text>

    <text x="386" y="272" text-anchor="middle" font-size="10.5" opacity="0.7">the body — runs once per item</text>

    <!-- same list, appended each pass -->
    <path d="M 212 44 C 172 130, 172 224, 246 219" fill="none" stroke="var(--accent)" stroke-width="1.8" marker-end="url(#l-ar-a)"/>
    <text x="166" y="198" text-anchor="end" font-size="10" font-weight="600" fill="var(--accent)">the same one list,</text>
    <text x="166" y="212" text-anchor="end" font-size="10" opacity="0.65">appended on every pass</text>

    <!-- loop back -->
    <path d="M 536 178 C 606 176, 608 64, 470 64 L 358 64" fill="none" stroke="currentColor" stroke-width="1.7" marker-end="url(#l-ar)"/>
    <text x="512" y="56" text-anchor="middle" font-size="9.5" opacity="0.7">next item — body runs again</text>

    <!-- exit -->
    <line x1="536" y1="238" x2="596" y2="238" stroke="currentColor" stroke-width="1.7" marker-end="url(#l-ar)"/>
    <text x="566" y="230" text-anchor="middle" font-size="9.5" opacity="0.7">list exhausted</text>
    <rect x="604" y="220" width="142" height="36" rx="7" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.55"/>
    <text x="675" y="243" text-anchor="middle" font-family="ui-monospace, monospace" font-size="11">results</text>
    <text x="675" y="270" text-anchor="middle" font-size="9.5" opacity="0.7">3 answers</text>

  </g>
</svg>
<figcaption>The list is fed in one item at a time; the body runs once per item;
anything you want to keep must be created <em>outside</em> the body, or it gets
rebuilt from scratch on every pass. The indent is the only thing marking that
boundary, and Python will not warn you if you get it wrong.</figcaption>
</figure>

Three consequences worth carrying.

**Indentation is meaning, not style.** Moving one line four spaces to the right
changes how many times it runs. Nothing turns red.

**Lists are mutable — the opposite of strings.** Last lesson you learned that
`text.strip()` builds a *new* string and you must catch it with `=`. Lists work
the other way round: `results.append(x)` changes the list in place and gives you
back nothing at all. So the rule flips, and so does the mistake — writing
`results = results.append(x)` throws your whole list away.

**A loop's job is usually to fill something.** Create an empty list before it,
append inside it, use it after. That three-part shape — set up, loop, report —
is most of the batch scripts you'll ever write.

## In practice

Activate your venv so your prompt starts with `(.venv)`:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then start the shell — everything up to the build is worth doing here:

```powershell
python
```

### Lists hold things in order

```python
>>> questions = ["What is an API?", "What is a token?", "What is JSON?"]
>>> len(questions)
3
>>> questions[0]
'What is an API?'
>>> questions[2]
'What is JSON?'
>>> questions[-1]
'What is JSON?'
```

Positions start at **0**, not 1, so the last item of a three-item list is at
index `2`. `-1` means "the last one" and saves you doing the arithmetic. Ask for
a position that isn't there and Python tells you plainly:

```python
>>> questions[3]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: list index out of range
```

`IndexError` is one you'll see for real, usually because a list was shorter than
you assumed. The fix is nearly always to check `len()` rather than to guess.

### Lists change in place — strings don't

This is the flip from last lesson, so run it rather than reading it:

```python
>>> questions.append("What is a rate limit?")
>>> questions
['What is an API?', 'What is a token?', 'What is JSON?', 'What is a rate limit?']
```

Notice `.append()` printed nothing and you assigned nothing — yet the list
changed. That's what "mutable" means. Now the trap:

```python
>>> questions = questions.append("What is latency?")
>>> print(questions)
None
```

Your entire list is gone. `.append()` returns `None` (Python's word for "no
value at all"), and you just pointed `questions` at that `None`. Compare the two
rules side by side, because they are exact opposites and both hinge on one
character:

| Type | Method | Correct usage |
|---|---|---|
| `str` (immutable) | `.strip()`, `.lower()` | `text = text.strip()` — **must** catch the result |
| `list` (mutable) | `.append()`, `.sort()` | `items.append(x)` — **never** catch the result |

Rebuild the list before continuing:

```python
>>> questions = ["What is an API?", "What is a token?", "What is JSON?"]
```

### Your first loop

```python
>>> for q in questions:
...     print(q)
...
What is an API?
What is a token?
What is JSON?
```

Three things happened there. The line ends with a colon. The shell switched its
prompt to `...` because it's waiting for an indented block — type four spaces,
then the line. And you pressed enter on an empty line to say "block finished",
which is only needed in the shell, not in a file.

`q` is just a name you chose; it gets re-pointed at each item in turn. `for
question in questions:` would behave identically and read better — use names
that say what the thing is.

Indentation decides how often a line runs, and this is the whole lesson:

```python
>>> count = 0
>>> for q in questions:
...     count = count + 1
...
>>> count
3
```

Now move the setup line one indent inward and watch it break:

```python
>>> for q in questions:
...     count = 0
...     count = count + 1
...
>>> count
1
```

Three passes, and `count` is 1. `count = 0` ran at the top of *every* pass,
wiping the previous total. No error, no warning, just a wrong number — the same
family of silent failure as the missing `=` last lesson.

### The pattern you'll use constantly

Create an empty list outside, fill it inside, use it after:

```python
>>> lengths = []
>>> for q in questions:
...     lengths.append(len(q))
...
>>> lengths
[15, 17, 15]
```

Empty brackets `[]` make an empty list. Three passes, three appends, three
numbers. Move `lengths = []` inside the loop and you'd finish with one.

### Deciding inside the loop

`if` runs a block only when a condition is true. The comparison operators are
`==` (equal), `!=` (not equal), and `<`, `>`, `<=`, `>=`:

```python
>>> for q in questions:
...     if len(q) > 15:
...         print("long: ", q)
...     else:
...         print("short:", q)
...
short: What is an API?
long:  What is a token?
short: What is JSON?
```

Two levels of indent now: the `if` is inside the loop, and the `if`'s own body
is inside that. `elif` adds more branches, checked in order, and only the first
true one runs:

```python
>>> score = 72
>>> if score >= 90:
...     print("A")
... elif score >= 70:
...     print("B")
... elif score >= 50:
...     print("C")
... else:
...     print("F")
...
B
```

Note that `score >= 50` is also true — it never ran, because `elif` stops at the
first match. Order your branches from most specific to least.

### Empty things are false

You don't need `== ""` to check for empty text. Python treats empty values as
false in a condition:

```python
>>> bool("")
False
>>> bool("hello")
True
>>> bool([])
False
>>> bool(0)
False
```

Empty string, empty list, zero, and `None` are all "falsy"; nearly everything
else is truthy. So this reads well and handles the blank-input case:

```python
>>> answer = "   "
>>> if not answer.strip():
...     print("nothing was typed")
...
nothing was typed
```

`answer.strip()` builds a cleaned copy — which you deliberately *don't* keep
here, because you only want to test it — and `not` flips the result.
Whitespace-only input is a real thing that will reach your scripts.

### Skipping and stopping

`continue` abandons this pass and moves to the next item. `break` leaves the
loop entirely:

```python
>>> for q in ["first", "", "third"]:
...     if not q:
...         print("skipping a blank")
...         continue
...     print("asking:", q)
...
asking: first
skipping a blank
asking: third
```

Swap `continue` for `break` and the output stops after `skipping a blank` — the
third question never gets asked. For a loop that costs money per pass, knowing
which one you want is not academic.

### Numbering the passes

You'll want "question 2 of 5" in your output. Don't keep a counter by hand —
`enumerate()` gives you the position and the item together:

```python
>>> for i, q in enumerate(questions, start=1):
...     print(f"{i}/{len(questions)}: {q}")
...
1/3: What is an API?
2/3: What is a token?
3/3: What is JSON?
```

`enumerate` counts from 0 unless you tell it otherwise; `start=1` makes it read
naturally to a human. The two names before `in` unpack the pair it hands back.

Type `exit()` to leave the shell.

### Why the model's reply needed a loop too

Look again at the last three lines of your `00-05-ask.py`:

```python
for block in message.content:
    if block.type == "text":
        print(block.text)
```

You wrote a loop and a conditional in that lesson without being told what they
were. Now you can read it: `message.content` is a **list** of blocks, because a
reply can contain more than just text — with Claude Opus 5, thinking is on by
default, so a thinking block can sit in that list alongside the answer. Taking
`message.content[0].text` and hoping is exactly how a script breaks in a week.
Loop, check the type, use the ones you want.

In this lesson's build you'll do the same thing one level in: a loop over your
questions, and inside it a loop over the reply's blocks. Nesting isn't a new
idea — it's the same shape, indented once more.

## Build it

A script that asks a model several questions in a row, prints each answer as it
arrives, skips anything blank, and reports at the end.

**This one spends money** — three API calls, at `max_tokens=150` each. Small,
but real. Step 3 exists so you never run an untested loop against a paid API.

**1. Branch first:**

```powershell
git switch -c lesson/01-02
```

**2. Write `builds/01-02-ask-many.py`.** Start from this skeleton and fill in
the rest yourself:

```python
# Asks a model several questions in a row and reports on the batch.
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

questions = [
    "In one sentence, what is an API rate limit?",
    "In one sentence, what is a token?",
    "",
    "In one sentence, why do API keys go in .env files?",
]
```

Your script must then:

- create an empty `results` list, a `skipped` counter, and a running
  `total_output_tokens` counter — all **before** the loop
- loop over the questions with `enumerate(questions, start=1)` so you can print
  `Question 2 of 4` as it goes
- skip any question that is blank or whitespace-only with `continue`, printing
  that it was skipped and adding one to `skipped` — the blank must **not** reach
  the API
- for each real question, call the model with `max_tokens=150`, then build the
  answer text by looping over `message.content` and keeping the blocks whose
  `type` is `"text"`
- print the question and its answer as each one comes back, not all at the end
- append each answer to `results`, and add `message.usage.output_tokens` to your
  running total
- after the loop, print a summary: how many were asked, how many were skipped,
  and the total output tokens for the batch

Keep `max_tokens` at 150. Three short answers, not three essays.

**3. Dry run first — before you spend anything.** Comment out the line that
creates the client and the line that makes the call, and put a fake answer in
their place:

```python
    answer = f"(pretend answer to {q})"
```

Run it. Check the numbering is right, the blank is skipped, and the counts add
up. *Then* put the real call back. This is the habit: a loop around a paid call
gets proved on fake data first, every time.

**4. Run it for real, and watch the output appear.** Each answer arrives after a
visible pause — that's a real network round trip per pass, and it's why a batch
of two hundred is a very different thing from a batch of four.

**5. Commit and merge:**

```powershell
git add builds/01-02-ask-many.py
git commit -m "Add batch question script from lesson 01-02"
git switch main
git merge lesson/01-02
git branch -d lesson/01-02
git push
```

Done when:

- `python builds/01-02-ask-many.py` runs start to finish with no traceback
- Three questions were asked and answered; the blank one printed a skip message
  and made no API call
- Each answer printed as it arrived, numbered `1 of 4`, `2 of 4`, and so on
- The summary prints 3 asked, 1 skipped, and a total output-token count larger
  than any single answer's
- `len(results)` is 3, and you can say why it isn't 4
- You did the dry run before the real run
- `git log --oneline -3` shows your commit on `main`, and `git status` is clean

Then log it:

```powershell
python tools/progress_log.py --lesson-id 01-02 --status complete --minutes 55 --artifact ./builds/01-02-ask-many.py --note "what clicked"
python tools/site_build.py --open
```

## Going deeper

- Move `results = []` inside the loop, run the script, and watch the summary
  collapse to 1. Put it back. Do the same with the token total. Seeing your own
  script fail this way is worth more than reading about it.
- Add a cheap quality check: after each answer, `if len(answer) < 20:` print a
  warning that the reply looks suspiciously short. Real batch jobs need checks
  like this, because nobody reads two hundred outputs by hand.
- Ask the same question twice in the list and compare the two answers. They
  won't match word for word. That's not a bug — lesson 03-02 covers why.
- Wrap the API call in `try:` / `except anthropic.APIError as e:` so one failed
  question prints an error and the loop keeps going instead of losing the whole
  batch. Skim [Anthropic's rate limits page](https://platform.claude.com/docs/en/api/rate-limits)
  for what a 429 is and what the `retry-after` header tells you — a loop is
  exactly how people meet those limits for the first time.
- Read [chapter 6 of Automate the Boring Stuff](https://automatetheboringstuff.com/3e/chapter6.html)
  for lists, and [chapter 2](https://automatetheboringstuff.com/3e/chapter2.html)
  for flow control. Both free, both cover this ground with different examples.
- Learn `while`, the other loop, from the
  [control flow tutorial](https://docs.python.org/3/tutorial/controlflow.html):
  `for` runs once per item, `while` runs until a condition stops being true. You
  will use `for` ninety percent of the time.
- Meet the **list comprehension** in the
  [data structures tutorial](https://docs.python.org/3/tutorial/datastructures.html):
  `[len(q) for q in questions]` does in one line what your four-line loop did.
  It's everywhere in real AI code — learn to read it before you write it.
- **Worth knowing now, for later:** when a batch gets big, looping one call at a
  time is the slow, expensive way. The Message Batches API processes thousands
  of requests asynchronously at half the price. Your loop is the right tool at
  four questions and the wrong tool at four thousand.

## Check yourself

<details markdown="1"><summary>A script loops over 50 records and prints "processed 1 record" at the end. The loop body works fine. What single thing is almost certainly wrong, and where?</summary>

The counter is being created inside the loop body — something like `count = 0`
sitting one indent too far in. It resets at the top of every pass, so the final
value reflects the last pass only.

The fix is to move `count = 0` out to the same indentation level as the `for`
line, above it. General rule: **anything that must survive the loop has to be
born outside it.** Nothing raises an error here, which is why the symptom you
notice is a suspiciously small number rather than a traceback.

</details>

<details markdown="1"><summary>Last lesson the rule was "you must catch what a string method returns". This lesson, `items.append(x)` catches nothing. Are the two rules in conflict?</summary>

No — they follow from one fact: strings are immutable and lists are mutable.

A string method can't change the string, so it returns a new one and you must
catch it: `text = text.strip()`. A list method changes the list itself, so it
has nothing to hand back and returns `None`: `items.append(x)`.

Which means the mistake is mirrored too. Forgetting the `=` on a string leaves
your data untouched; adding an `=` to `.append()` (`items = items.append(x)`)
replaces your entire list with `None`. Same underlying question — does this
method change the thing or build a new one — with opposite answers.

</details>

<details markdown="1"><summary>You want to skip blank questions. Why is `if not q.strip():` better than `if q == "":`?</summary>

`q == ""` only matches a string of length zero. A question that is `"   "` or
`"\n"` — a stray spacebar, a line break, an empty-looking spreadsheet cell — is
not equal to `""`, so it sails through the check and gets sent to the API. You
pay for it and get a useless answer back.

`q.strip()` builds a copy with the whitespace removed from both ends. If nothing
is left, that copy is `""`, which is falsy, so `not` makes the condition true
and you skip. Drop the `.strip()` and you're back to catching only genuinely
empty strings.

Note that you don't assign the result of `.strip()` here, and that's deliberate:
you're testing it, not keeping it.

</details>

<details markdown="1"><summary>In your build, `continue` skips the blank question. If you'd used `break` instead, what exactly would the output have been, and why is the difference expensive?</summary>

`break` leaves the loop entirely, so the script would have asked questions 1 and
2, hit the blank at position 3, printed the skip message, and then **never asked
question 4**. The summary would say 2 asked instead of 3, and `results` would
hold 2 answers.

Expensive in both directions. In a batch of two hundred, one blank row silently
throws away the hundred and fifty items after it — and you get no traceback
saying so, just a short results list. In the other direction, a `continue` where
you needed a `break` keeps a loop running against a failing API, burning calls
that all error out.

</details>

<details markdown="1"><summary>Why does your script loop over `message.content` and check `block.type` instead of just using `message.content[0].text`?</summary>

Because `message.content` is a list of blocks, and text is not the only kind.
With Claude Opus 5 thinking is on by default, so a thinking block can sit in
that list; tool use adds other block types later on. `content[0]` is whatever
happened to come first, and `.text` on a block that has no `.text` is an
`AttributeError` — in production, at 2am, on the one reply that came back
differently.

Looping and checking `block.type == "text"` says what you actually want: the
text parts, however many there are and wherever they sit. It's the same
defensive habit as checking `len()` before indexing a list.

</details>
