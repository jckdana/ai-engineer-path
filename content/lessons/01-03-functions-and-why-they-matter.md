---
id: "01-03"
title: "Functions and why they matter"
module: "01"
core_minutes: 50
deep_minutes: 120
build: "Refactor your model-calling script so the API call is a function with parameters and a docstring."
resources:
  - title: "Python tutorial — defining functions, default values, keyword arguments"
    url: "https://docs.python.org/3/tutorial/controlflow.html"
  - title: "Python FAQ — arguments vs parameters, and why default values are shared"
    url: "https://docs.python.org/3/faq/programming.html"
  - title: "PEP 257 — docstring conventions"
    url: "https://peps.python.org/pep-0257/"
  - title: "Automate the Boring Stuff, chapter 4 — Functions (free online)"
    url: "https://automatetheboringstuff.com/3e/chapter4.html"
  - title: "Python glossary — the exact definitions of parameter and argument"
    url: "https://docs.python.org/3/glossary.html"
---

## Why this matters

Look at the script you wrote in lesson 00-05. It asks the model one question.
Now imagine a client says: *"ask it these five questions, but use a different
model for the last two, and if any answer comes back empty, ask again."*

With the script as it stands, you'd copy-paste the API call four more times.
Then you'd change the model in two of the copies. Then you'd find a bug in how
you read the reply — and you'd have to fix it in five places, and you would miss
one. That is not a hypothetical; that is the single most common way beginner
code rots.

A function is the fix. You name a piece of work once, describe what varies about
it, and then call it by that name as many times as you like. Fix the bug once,
every caller gets the fix. This is also the moment your code becomes *testable*
and *sellable*: nobody buys a script, they buy a thing that reliably does a job,
and a "thing that does a job" is exactly what a function is.

## The mental model

A function has two boundaries, and almost every beginner bug lives at one of
them.

The first is **the way in**. When you define a function you list **parameters** —
names the function will use internally. When you call it you supply
**arguments** — the actual values. Python binds each argument to the matching
parameter name, and those names exist *only inside the function*. Python's own
glossary draws exactly this line: parameters are in the definition, arguments
are at the call.

The second is **the way out**. A function hands back exactly one value, using
`return`. The moment `return` runs, the function stops and the call expression
*becomes* that value. If you never write `return`, Python hands back `None` —
which is the cause of the classic "why is my variable None?" confusion.

And the part that surprises people: the names created inside a function are
thrown away when it returns. That's a feature. It means a function can't
accidentally clobber a variable somewhere else in your program.

<figure class="figure">
<svg viewBox="0 0 780 340" role="img" aria-label="A diagram of one function call. At the top left, the call site reads reply equals ask, open bracket, the string what is X, comma, max tokens equals 300. Two arrows carry those two arguments rightward and down into the function's parameter slots. The function definition box below is surrounded by a dashed boundary labelled names in here do not exist outside, and shows def ask, open bracket, question, comma, max tokens equals 500. Inside the box, the parameter question is now bound to the string what is X, and max tokens is bound to 300, with a note that the argument beat the default of 500. A third local name, message, is created inside the body and is marked local, discarded on return. An accented box reading return text sits at the lower right, and an accented arrow carries a single value from it back up and leftward to the call site. A note beside that arrow reads exactly one value comes back.">
  <defs>
    <marker id="f-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="currentColor"/>
    </marker>
    <marker id="f-ar-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/>
    </marker>
  </defs>

  <g font-family="system-ui, sans-serif" font-size="12" fill="currentColor">

    <text x="16" y="30" font-size="10.5" font-weight="600" opacity="0.75">THE CALL</text>
    <rect x="16" y="40" width="330" height="34" rx="7" fill="none" stroke="currentColor" stroke-width="1.6" opacity="0.6"/>
    <text x="30" y="62" font-family="ui-monospace, monospace" font-size="11.5">reply = ask(</text>
    <text x="112" y="62" font-family="ui-monospace, monospace" font-size="11.5" font-weight="600">"What is X?"</text>
    <text x="196" y="62" font-family="ui-monospace, monospace" font-size="11.5">, max_tokens=</text>
    <text x="292" y="62" font-family="ui-monospace, monospace" font-size="11.5" font-weight="600">300</text>
    <text x="316" y="62" font-family="ui-monospace, monospace" font-size="11.5">)</text>

    <path d="M 150 78 C 150 120, 250 118, 292 146" fill="none" stroke="currentColor" stroke-width="1.6" marker-end="url(#f-ar)"/>
    <text x="146" y="106" text-anchor="end" font-size="9.5" opacity="0.7">argument</text>
    <path d="M 300 78 C 320 116, 400 120, 430 146" fill="none" stroke="currentColor" stroke-width="1.6" marker-end="url(#f-ar)"/>
    <text x="372" y="106" font-size="9.5" opacity="0.7">argument</text>

    <rect x="246" y="150" width="392" height="162" rx="10" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6 5" opacity="0.45"/>
    <text x="442" y="330" text-anchor="middle" font-size="9.5" opacity="0.7">names in here do not exist outside</text>

    <text x="262" y="172" font-family="ui-monospace, monospace" font-size="11.5" font-weight="600">def ask(question, max_tokens=500):</text>

    <rect x="262" y="184" width="168" height="30" rx="6" fill="none" stroke="currentColor" stroke-width="1.4" opacity="0.6"/>
    <text x="274" y="203" font-family="ui-monospace, monospace" font-size="10.5">question = "What is X?"</text>

    <rect x="440" y="184" width="184" height="30" rx="6" fill="none" stroke="currentColor" stroke-width="1.4" opacity="0.6"/>
    <text x="452" y="203" font-family="ui-monospace, monospace" font-size="10.5">max_tokens = 300</text>
    <text x="452" y="228" font-size="9.5" opacity="0.65">the argument beat the default 500</text>

    <rect x="262" y="246" width="168" height="30" rx="6" fill="none" stroke="currentColor" stroke-width="1.4" opacity="0.4"/>
    <text x="274" y="265" font-family="ui-monospace, monospace" font-size="10.5" opacity="0.7">message = ...</text>
    <text x="274" y="290" font-size="9.5" opacity="0.65">local — discarded on return</text>

    <path d="M 556 246 C 606 212, 636 120, 300 96 L 206 88" fill="none" stroke="var(--accent)" stroke-width="2" marker-end="url(#f-ar-a)"/>
    <rect x="494" y="246" width="124" height="30" rx="6" fill="var(--accent-tint)" stroke="var(--accent)" stroke-width="1.8"/>
    <text x="556" y="265" text-anchor="middle" font-family="ui-monospace, monospace" font-size="11" fill="var(--accent)">return text</text>
    <text x="660" y="182" text-anchor="end" font-size="10.5" font-weight="600" fill="var(--accent)">exactly one value</text>
    <text x="660" y="196" text-anchor="end" font-size="10" opacity="0.65">comes back</text>
  </g>
</svg>
<figcaption>One call, both boundaries. Arguments flow in and get bound to parameter
names that live only inside the dashed box; <code>return</code> sends exactly one
value back out, and everything else the function made is thrown away.</figcaption>
</figure>

## In practice

Open a new file, `builds/01-03-ask.py`. Type these as you go — don't paste.

### The smallest possible function

```python
def greet():
    print("hello")

greet()
```

```
hello
```

`def` starts the definition. The indented lines are the **body**. Nothing runs
until you *call* it with `greet()` — defining a function and running it are two
separate events. Leave off the brackets and you get something odd but useful to
see once:

```python
print(greet)
```

```
<function greet at 0x000001C4A1F2B920>
```

That's the function object itself. `greet` is the thing; `greet()` is the act of
running it.

### Parameters make it reusable

```python
def greet(name):
    print(f"hello, {name}")

greet("Jack")
greet("Mum")
```

```
hello, Jack
hello, Mum
```

`name` is a **parameter**. `"Jack"` is an **argument**. One definition, two
different results — that's the whole point.

### `return` versus `print`

This trips up nearly everyone. Try both:

```python
def shout_print(text):
    print(text.upper())

def shout_return(text):
    return text.upper()

a = shout_print("hello")
b = shout_return("hello")

print("a is", a)
print("b is", b)
```

```
HELLO
a is None
b is HELLO
```

`shout_print` put something on the screen and handed back nothing, so `a` is
`None`. `shout_return` handed the value back, so `b` holds it and you can keep
working with it. **Printing shows a human. Returning gives your program
something to use.** You almost always want `return`.

`return` also stops the function immediately:

```python
def check(n):
    if n < 0:
        return "negative"
    return "zero or more"

print(check(-5))
print(check(3))
```

```
negative
zero or more
```

No `else` needed — if the first `return` runs, nothing after it does.

### Defaults and keyword arguments

```python
def ask(question, model="claude-opus-5", max_tokens=500):
    return f"[{model}, cap {max_tokens}] {question}"

print(ask("What is X?"))
print(ask("What is X?", max_tokens=50))
print(ask("What is X?", "claude-haiku-4-5"))
```

```
[claude-opus-5, cap 500] What is X?
[claude-opus-5, cap 50] What is X?
[claude-haiku-4-5, cap 500] What is X?
```

Parameters with defaults are optional. Naming them at the call site
(`max_tokens=50`) is a **keyword argument**, and it lets you skip past ones you
don't care about. Two rules worth memorising now:

- Parameters *with* defaults must come after parameters without them.
- Keyword arguments must come after positional ones at the call site.

### One mistake worth making on purpose

Never use a list or dict as a default value. Watch:

```python
def collect(item, bucket=[]):
    bucket.append(item)
    return bucket

print(collect("a"))
print(collect("b"))
print(collect("c"))
```

```
['a']
['a', 'b']
['a', 'b', 'c']
```

You expected `['b']` on the second call. The default was created **once, when
the function was defined** — so every call that relies on it shares the same
list. The Python FAQ documents this exact trap. The fix is always the same:

```python
def collect(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket

print(collect("a"))
print(collect("b"))
```

```
['a']
['b']
```

### Docstrings

A **docstring** is a string on the first line of the body. It's not a comment —
it stays attached to the function and tools can read it.

```python
def ask(question, max_tokens=500):
    """Send one question to the model and return the reply text."""
    return question.upper()

print(ask.__doc__)
help(ask)
```

```
Send one question to the model and return the reply text.
Help on function ask in module __main__:

ask(question, max_tokens=500)
    Send one question to the model and return the reply text.
```

PEP 257 is the convention: triple double quotes, and phrase it as a command
("Return the reply") rather than a description ("Returns the reply"). Don't
restate the parameter list — Python already shows that.

### Scope, seen once

```python
def f():
    inside = "local"
    return inside

print(f())
print(inside)
```

```
local
Traceback (most recent call last):
  File "builds/01-03-ask.py", line 6, in <module>
    print(inside)
          ^^^^^^
NameError: name 'inside' is not defined
```

That `NameError` is the dashed box in the diagram doing its job. `inside` never
existed outside the function.

## Build it

Refactor your lesson 00-05 script (`builds/00-05-ask.py`) so the API call lives
in a function. Save the new version as `builds/01-03-ask.py` — keep the old one,
so you can see how far you've come.

Your function should:

1. Be called `ask`.
2. Take the question as its first parameter.
3. Take `model` and `max_tokens` as parameters **with sensible defaults**, so
   `ask("something")` works with no other arguments.
4. Have a one-line docstring phrased as a command.
5. **Return** the reply text as a string. It must not `print` the reply — the
   caller decides what to do with it.
6. Be called at least twice at the bottom of the file, once relying on the
   defaults and once overriding `max_tokens` with a keyword argument.

A skeleton to fill in:

```python
# Asks a model a question through a reusable function.

import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()


def ask(question, model="claude-opus-5", max_tokens=500):
    """Send one question to the model and return the reply text."""
    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": question}],
    )
    # Pull the text out of the content blocks and hand it back.
    ...


print(ask("Name three uses for a paperclip."))
print(ask("Say hello in five words.", max_tokens=40))
```

The `...` is yours to finish. You already wrote that loop over
`message.content` in lesson 00-05 — the difference is that this time you
`return` the text instead of printing it.

> One naming note: in 00-05 you wrote `anthropic.Client()`. The documented name
> is `anthropic.Anthropic()`. Both work — `Client` is an older alias — but use
> `Anthropic()` from here on so your code matches the official docs.

**Done when:**

- [ ] `python builds/01-03-ask.py` prints two different answers.
- [ ] The word `print` appears nowhere inside the body of `ask`.
- [ ] `ask("anything")` runs without a second argument.
- [ ] `help(ask)` shows your docstring.
- [ ] Assigning the result works: `reply = ask("hi")` then `print(len(reply))`
      prints a number, not an error about `None`.

## Going deeper

- Add a `system` parameter defaulting to `None`, and only pass `system=` to the
  API when it isn't `None`.
- Write a second function `ask_many(questions)` that takes a list, calls `ask`
  once per item using the loop from 01-02, and returns a list of replies. Notice
  that you did not have to touch `ask` at all.
- Add a `retries=2` parameter: if the returned text is empty, call the API again
  up to that many times before giving up.
- Give the function type hints — `def ask(question: str, max_tokens: int = 500) -> str:` — and read what PEP 257 says about not duplicating the signature in
  the docstring.
- Move `ask` into its own file, `builds/askbot.py`, and `from askbot import ask`
  in a second script. This is the moment a function becomes a *tool*, which is
  exactly how everything in this repo's `tools/` directory is built.
- Read the Python FAQ section on why default values are shared, then find one
  legitimate use of that behaviour (hint: it's called memoisation).

## Check yourself

<details markdown="1">
<summary>You run <code>result = shout("hey")</code> and <code>result</code> is <code>None</code>, even though "HEY" appeared on screen. What single word is missing, and where?</summary>

`return`, in the body of `shout`. The function is printing the value instead of
handing it back, so the call evaluates to `None`. Change `print(text.upper())`
to `return text.upper()` — and if you want both, `return` the value and let the
*caller* print it.

</details>

<details markdown="1">
<summary>Why does <code>def ask(max_tokens=500, question):</code> refuse to run at all?</summary>

A parameter without a default can't follow one with a default — Python raises a
`SyntaxError` before the file executes. If it were allowed, a call like
`ask("hi")` would be ambiguous: Python couldn't tell whether `"hi"` was meant
for `max_tokens` or `question`. Put required parameters first:
`def ask(question, max_tokens=500):`.

</details>

<details markdown="1">
<summary>This function is supposed to start fresh each call, but doesn't. Fix it: <code>def log(msg, seen=[]):</code> then <code>seen.append(msg)</code> then <code>return seen</code>.</summary>

The default list is created once, when the `def` line runs — not once per call —
so every call shares it. Use `None` as the sentinel and build the list inside:

```python
def log(msg, seen=None):
    if seen is None:
        seen = []
    seen.append(msg)
    return seen
```

The same trap applies to `{}` and to any other mutable default.

</details>

<details markdown="1">
<summary>Inside <code>ask</code> you set <code>reply = "..."</code>. After the call, <code>print(reply)</code> raises <code>NameError</code>. Is this a bug?</summary>

No — it's the point. Names assigned inside a function live in that function's
local scope and are discarded when it returns. That's what stops a function from
silently overwriting variables elsewhere in your program. If you need the value
outside, `return` it and catch it: `reply = ask("hi")`.

</details>

<details markdown="1">
<summary>You want to call <code>ask</code> with the default model but a <code>max_tokens</code> of 50. Why does <code>ask("hi", 50)</code> do the wrong thing, and what should you write?</summary>

Positional arguments fill parameters in order, so `50` lands in `model` — the
second parameter — and you end up asking a model literally named `50`. Name the
one you want instead: `ask("hi", max_tokens=50)`. This is exactly what keyword
arguments are for, and it's why skipping over a middle parameter requires them.

</details>
