---
id: "01-04"
title: "Dictionaries and JSON"
module: "01"
core_minutes: 55
deep_minutes: 130
build: "A script that reads a JSON file of records, filters them by a field, and writes the results to a new JSON file."
resources:
  - title: "Python tutorial 5.5 — Dictionaries (keys, get, in, items)"
    url: "https://docs.python.org/3/tutorial/datastructures.html"
  - title: "Python tutorial 7.2.2 — Saving structured data with json (and why encoding='utf-8')"
    url: "https://docs.python.org/3/tutorial/inputoutput.html"
  - title: "The json module reference — load vs loads, dump vs dumps, the type conversion table"
    url: "https://docs.python.org/3/library/json.html"
  - title: "Introducing JSON — the whole format on one page"
    url: "https://www.json.org/json-en.html"
  - title: "Automate the Boring Stuff, chapter 7 — Dictionaries and Structuring Data (free online)"
    url: "https://automatetheboringstuff.com/3e/chapter7.html"
  - title: "Claude Messages API reference — a real JSON request and response, field by field"
    url: "https://platform.claude.com/docs/en/api/messages"
---

## Why this matters

You've already written a dictionary without being told. Look at the call in
your `ask` function:

```python
messages=[{"role": "user", "content": question}]
```

Those curly braces are a **dictionary**: a set of labelled values. `"role"` is
a label, `"user"` is the value stored under it. Every AI API you'll ever touch —
Claude, OpenAI, a CRM, Stripe, a Google Sheet — takes its input in this shape and
gives its output back in this shape. When you send the request, it travels over
the internet as **JSON**, which is the same shape written out as plain text.

This matters for money reasons. The most common small job a business will pay
for looks like: *"we have a pile of records (leads, orders, support tickets) —
pull out the ones that matter and put them somewhere useful."* That job is
dictionaries and JSON, start to finish. By the end of this lesson you'll have
built exactly that: a script that reads a file of support tickets, keeps the
urgent ones, and writes them out for someone else to act on.

## The mental model

A **dictionary** (`dict`) maps **keys** to **values**. A list finds things by
position (`items[0]`); a dict finds things by name (`ticket["customer"]`). Keys
are usually strings. Values can be anything — including lists and other dicts,
which is how real data gets its depth.

**JSON** (JavaScript Object Notation) is a text format for the same shapes. A
JSON *object* looks like a dict, a JSON *array* looks like a list. But there's
one idea the whole lesson turns on:

**JSON is text. A dict is a live object in your program's memory.** You can't
look up a key in a string; you can't save a live object to a file. So there is
always a conversion step at the boundary, and Python's built-in `json` module
does it:

- `json.load` / `json.loads` — JSON text **→** Python objects (reading)
- `json.dump` / `json.dumps` — Python objects **→** JSON text (writing)

The trailing `s` means *string*: `loads` reads from a string, `load` reads from
an open file. Same with `dumps` and `dump`.

<figure class="figure">
<svg viewBox="0 0 780 360" role="img" aria-label="A diagram of the boundary between JSON text and Python objects. On the left, a box labelled tickets.json, text on disk, shows a line of JSON with double-quoted keys, the word true in lowercase and the word null. On the right, a box labelled Python memory, live objects, shows the same record as a Python dict with True capitalised and None. Two accented arrows cross the boundary in the middle: the upper one, labelled json.load, goes from the file to memory; the lower one, labelled json.dump, goes from memory back to a file. A note says the conversion changes true to True and null to None. Below, a second row shows the same boundary for an API call: your dict passes through the SDK, which converts it to JSON, travels over the internet to Anthropic, and the JSON reply comes back through the SDK into a Python object you read with keys and dots.">
  <defs>
    <marker id="j-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="currentColor"/>
    </marker>
    <marker id="j-ar-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/>
    </marker>
  </defs>

  <g font-family="system-ui, sans-serif" font-size="12" fill="currentColor">

    <!-- Row 1: file <-> memory -->
    <text x="16" y="26" font-size="10.5" font-weight="600" opacity="0.75">TEXT ON DISK</text>
    <rect x="16" y="36" width="270" height="96" rx="8" fill="none" stroke="currentColor" stroke-width="1.6" opacity="0.6"/>
    <text x="30" y="58" font-family="ui-monospace, monospace" font-size="11" font-weight="600">tickets.json</text>
    <text x="30" y="82" font-family="ui-monospace, monospace" font-size="10.5">{"id": 101,</text>
    <text x="30" y="98" font-family="ui-monospace, monospace" font-size="10.5"> "open": true,</text>
    <text x="30" y="114" font-family="ui-monospace, monospace" font-size="10.5"> "notes": null}</text>
    <text x="196" y="98" font-size="9.5" opacity="0.65">just characters —</text>
    <text x="196" y="112" font-size="9.5" opacity="0.65">can't look up keys</text>

    <text x="764" y="26" text-anchor="end" font-size="10.5" font-weight="600" opacity="0.75">LIVE OBJECTS IN MEMORY</text>
    <rect x="494" y="36" width="270" height="96" rx="8" fill="none" stroke="currentColor" stroke-width="1.6" opacity="0.6"/>
    <text x="508" y="58" font-family="ui-monospace, monospace" font-size="11" font-weight="600">ticket  (a dict)</text>
    <text x="508" y="82" font-family="ui-monospace, monospace" font-size="10.5">{"id": 101,</text>
    <text x="508" y="98" font-family="ui-monospace, monospace" font-size="10.5"> "open": True,</text>
    <text x="508" y="114" font-family="ui-monospace, monospace" font-size="10.5"> "notes": None}</text>
    <text x="664" y="98" font-size="9.5" opacity="0.65">ticket["open"]</text>
    <text x="664" y="112" font-size="9.5" opacity="0.65">works here</text>

    <line x1="390" y1="30" x2="390" y2="150" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 4" opacity="0.45"/>
    <text x="390" y="166" text-anchor="middle" font-size="9.5" opacity="0.7">the boundary</text>

    <path d="M 292 64 L 488 64" fill="none" stroke="var(--accent)" stroke-width="2" marker-end="url(#j-ar-a)"/>
    <rect x="344" y="50" width="92" height="22" rx="5" fill="var(--accent-tint)" stroke="var(--accent)" stroke-width="1.4"/>
    <text x="390" y="65" text-anchor="middle" font-family="ui-monospace, monospace" font-size="11" fill="var(--accent)">json.load</text>

    <path d="M 488 110 L 292 110" fill="none" stroke="var(--accent)" stroke-width="2" marker-end="url(#j-ar-a)"/>
    <rect x="344" y="96" width="92" height="22" rx="5" fill="var(--accent-tint)" stroke="var(--accent)" stroke-width="1.4"/>
    <text x="390" y="111" text-anchor="middle" font-family="ui-monospace, monospace" font-size="11" fill="var(--accent)">json.dump</text>
    <text x="390" y="88" text-anchor="middle" font-size="9.5" opacity="0.7">true ↔ True · null ↔ None</text>

    <!-- Row 2: API round trip -->
    <text x="16" y="212" font-size="10.5" font-weight="600" opacity="0.75">THE SAME BOUNDARY, EVERY API CALL</text>

    <rect x="16" y="226" width="150" height="46" rx="7" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.6"/>
    <text x="91" y="245" text-anchor="middle" font-size="11" font-weight="600">your code</text>
    <text x="91" y="262" text-anchor="middle" font-family="ui-monospace, monospace" font-size="10">{"role": "user", ...}</text>

    <rect x="226" y="226" width="120" height="46" rx="7" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.6"/>
    <text x="286" y="245" text-anchor="middle" font-size="11" font-weight="600">SDK</text>
    <text x="286" y="262" text-anchor="middle" font-size="9.5" opacity="0.7">converts to JSON</text>

    <rect x="408" y="226" width="130" height="46" rx="7" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5 4" opacity="0.6"/>
    <text x="473" y="245" text-anchor="middle" font-size="11" font-weight="600">internet</text>
    <text x="473" y="262" text-anchor="middle" font-size="9.5" opacity="0.7">only text travels</text>

    <rect x="600" y="226" width="164" height="46" rx="7" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.6"/>
    <text x="682" y="245" text-anchor="middle" font-size="11" font-weight="600">Anthropic's API</text>
    <text x="682" y="262" text-anchor="middle" font-size="9.5" opacity="0.7">reads JSON, writes JSON</text>

    <path d="M 166 240 L 222 240" stroke="currentColor" stroke-width="1.5" marker-end="url(#j-ar)"/>
    <path d="M 346 240 L 404 240" stroke="currentColor" stroke-width="1.5" marker-end="url(#j-ar)"/>
    <path d="M 538 240 L 596 240" stroke="currentColor" stroke-width="1.5" marker-end="url(#j-ar)"/>
    <text x="375" y="232" text-anchor="middle" font-size="9" opacity="0.7">request</text>

    <path d="M 682 272 C 682 318, 560 318, 540 318 L 100 318 C 91 318, 91 300, 91 278" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#j-ar)"/>
    <text x="400" y="312" text-anchor="middle" font-size="9.5" opacity="0.7">response JSON → SDK → Python object</text>
    <text x="91" y="344" font-family="ui-monospace, monospace" font-size="10" text-anchor="start" opacity="0.85">message.usage.output_tokens</text>
  </g>
</svg>
<figcaption>JSON is how data travels and gets stored; dicts and lists are how your
program works with it. <code>json.load</code> and <code>json.dump</code> are the
only doors between the two. The Anthropic SDK does the same conversion for you on
every call — which is why your request is written as a dict.</figcaption>
</figure>

## In practice

Open a scratch file, `builds/01-04-play.py`. Type each block, run it, then
delete it and type the next.

### Making and reading a dict

```python
ticket = {"id": 101, "customer": "Dana", "priority": "high", "open": True}

print(ticket["customer"])
print(ticket["priority"])
```

```
Dana
high
```

Curly braces, `key: value` pairs, commas between pairs. Square brackets with a
key reads the value stored under it.

### Changing and adding

```python
ticket["priority"] = "low"        # key exists  → value replaced
ticket["assigned_to"] = "Jack"    # key is new  → pair added
print(ticket)
print(len(ticket))
```

```
{'id': 101, 'customer': 'Dana', 'priority': 'low', 'open': True, 'assigned_to': 'Jack'}
5
```

Same syntax for both. If the key exists, it's overwritten; if not, it's
created. A dict can't have the same key twice. `len` counts the pairs.

### The mistake you will make this week

Ask for a key that isn't there:

```python
ticket = {"id": 101, "customer": "Dana"}
print(ticket["email"])
```

```
Traceback (most recent call last):
  File "builds/01-04-play.py", line 2, in <module>
    print(ticket["email"])
          ~~~~~~^^^^^^^^^
KeyError: 'email'
```

A `KeyError` means *"that label doesn't exist in this dict"* — and it names the
missing key for you. Real data is messy: one record in fifty will be missing a
field, and square brackets will crash your whole script on it. Two ways to ask
safely:

```python
print(ticket.get("email"))
print(ticket.get("email", "no email on file"))
print("email" in ticket)
print("customer" in ticket)
```

```
None
no email on file
False
True
```

`.get(key)` returns `None` instead of crashing; `.get(key, fallback)` returns
your fallback. `in` checks whether a key exists. Rule of thumb: use `[]` when a
missing key *should* crash (it's a bug you want to see), and `.get()` when a
missing key is normal (it's data from outside).

### Looping over a dict

```python
ticket = {"id": 101, "customer": "Dana", "priority": "high"}

for key, value in ticket.items():
    print(f"{key}: {value}")
```

```
id: 101
customer: Dana
priority: high
```

`.items()` hands you each pair; the `for key, value in` unpacks both at once.

### Nesting — how API responses really look

Values can be lists and dicts. Here's a cut-down version of what the Claude API
actually sends back, written as a Python dict:

```python
message = {
    "role": "assistant",
    "content": [
        {"type": "text", "text": "Paris."}
    ],
    "usage": {"input_tokens": 14, "output_tokens": 4},
}

print(message["usage"]["output_tokens"])
print(message["content"][0]["text"])
```

```
4
Paris.
```

Read chained lookups left to right, one step at a time:
`message["content"]` is a list → `[0]` is its first item, a dict →
`["text"]` is the string inside. This is the single most useful skill in the
lesson. When you meet a new API, you print one response, trace the path to the
value you need, and write it as a chain like this.

> The Anthropic SDK gives you the reply as an object, so in your real script you
> write `message.usage.output_tokens` with dots instead of brackets. Same shape,
> same path — the SDK just converted the JSON for you.

### Crossing the boundary: `dumps` and `loads`

```python
import json

ticket = {"id": 101, "customer": "Dana", "open": True, "notes": None}

text = json.dumps(ticket)
print(text)
print(type(text))

back = json.loads(text)
print(back["open"])
print(type(back))
```

```
{"id": 101, "customer": "Dana", "open": true, "notes": null}
<class 'str'>
True
<class 'dict'>
```

Look closely at the first line: `True` became `true`, `None` became `null`, and
every string is in double quotes. That's JSON's spelling. `type` confirms it's
now just a `str` — you can't look up keys in it until `loads` turns it back into
a `dict`.

### JSON is stricter than Python

```python
import json

bad = "{'id': 101, 'customer': 'Dana'}"
json.loads(bad)
```

```
json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
```

That's a Python dict *printed*, not JSON. JSON demands double quotes. You'll
hit this when you copy output from `print(some_dict)` into a `.json` file —
`print` shows Python's spelling, `json.dumps` gives you JSON's. The error even
tells you the line and column to look at.

### Reading and writing files

The pattern you'll use for the rest of your career:

```python
import json

# Read
with open("builds/some-file.json", encoding="utf-8") as f:
    data = json.load(f)

# Write
with open("builds/other-file.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
```

- `with open(...) as f:` opens the file and closes it for you when the indented
  block ends, even if something crashes. (Files get their own lesson, 01-05.)
- `"w"` means write — it **replaces** the file if it already exists.
- `encoding="utf-8"` is what the Python docs tell you to use for JSON. Leave it
  off on Windows and Python reads with an older default encoding instead: a
  file containing *Zoë* loads as *ZoÃ«*. No error, just quietly wrong data.
- `indent=2` makes the output readable by a human. Without it, everything lands
  on one line.

## Build it

A client runs a small software company. Support tickets pile up in a JSON
export. They want a file containing **only the urgent ones — high priority and
still open** — so whoever's on call can start there.

**1.** Create `builds/01-04-tickets.json` with this content. This is data, so
copy-pasting it is fine:

```json
[
  {"id": 101, "customer": "Dana Reyes", "priority": "high", "status": "open", "subject": "Can't log in after password reset"},
  {"id": 102, "customer": "Marcus Lee", "priority": "low", "status": "open", "subject": "How do I change my invoice email?"},
  {"id": 103, "customer": "Priya Shah", "priority": "high", "status": "closed", "subject": "Double charged in August"},
  {"id": 104, "customer": "Tom Okafor", "priority": "medium", "status": "open", "subject": "Export to CSV is slow"},
  {"id": 105, "customer": "Ana Costa", "status": "open", "subject": "Feature idea: dark mode"},
  {"id": 106, "customer": "Sam Wright", "priority": "high", "status": "open", "subject": "Whole team locked out since this morning"},
  {"id": 107, "customer": "Lena Park", "priority": "HIGH", "status": "open", "subject": "Payment page shows an error"}
]
```

It's a JSON array of objects, so `json.load` will give you a **list of dicts**.
Two records are deliberately messy — this is what real exports look like. Find
them before you start.

**2.** Write `builds/01-04-filter.py`. Use functions, like lesson 01-03:

```python
# Reads support tickets from JSON, keeps the urgent open ones, writes them to a new file.
import json

INPUT_PATH = "builds/01-04-tickets.json"
OUTPUT_PATH = "builds/01-04-urgent.json"


def load_records(path):
    """Read a JSON file and return the Python object inside it."""
    ...


def is_urgent(ticket):
    """Return True if the ticket is high priority and still open."""
    ...


def save_records(records, path):
    """Write records to a JSON file, pretty-printed."""
    ...


tickets = load_records(INPUT_PATH)
urgent = []
# Loop over tickets; append the ones where is_urgent(...) is True.
...

save_records(urgent, OUTPUT_PATH)
print(f"Read {len(tickets)} tickets, kept {len(urgent)}, wrote {OUTPUT_PATH}")
```

Fill in each `...`. Hints, if you're stuck for more than ten minutes:

- `load_records` and `save_records` are the two halves of the file pattern
  above, with `return` on the load side.
- Write `is_urgent` with square brackets first — `ticket["priority"] == "high"`
  — and run it. Read the traceback. Which ticket broke it, and why? Fix it with
  `.get()`.
- Then check the output: is ticket 107 in it? It should be. `"HIGH"` isn't equal
  to `"high"`. You fixed exactly this in lesson 01-01 with a string method.

**Done when:**

- [ ] `python builds/01-04-filter.py` prints `Read 7 tickets, kept 3, wrote builds/01-04-urgent.json`.
- [ ] `builds/01-04-urgent.json` exists, is indented, and contains tickets 101, 106 and 107 — nothing else.
- [ ] Ticket 105 (no `priority` field) doesn't crash the script.
- [ ] No square-bracket lookup inside `is_urgent` can raise `KeyError`.
- [ ] Opening the output file in VS Code shows double quotes and lowercase `true`/`null` style — it's real JSON, not a printed dict.

## Free practice

Free, no credit card. Do these after the build task, not instead of it. Each is extra reps on this lesson's idea in a setting you didn't design yourself.

- **Exercism: [Inventory Management](https://exercism.org/tracks/python/exercises/inventory-management)** covers building, updating and
  deleting dict entries.
- **Exercism: [Mecha Munch Management](https://exercism.org/tracks/python/exercises/mecha-munch-management)** is harder. It covers `setdefault`,
  merging dicts, and sorting by items.
- **[JSONPlaceholder](https://jsonplaceholder.typicode.com/)** is a free fake API with no key. Use the
  standard library to pull real JSON over the network. After
  `import json, urllib.request`, run
  `json.load(urllib.request.urlopen("https://jsonplaceholder.typicode.com/todos"))`.
  Then run your build task's filter on it, keeping todos where `completed` is `False`.
- **Built in:** `python -m json.tool yourfile.json` pretty-prints a file, or tells you the exact
  line where it isn't valid JSON.

## Going deeper

- **Make the filter reusable.** Change `is_urgent(ticket)` into
  `matches(record, field, value)` so the same script can pull tickets by
  `status`, `customer`, or anything else. Call it three ways.
- **Count, don't just filter.** Build a dict that counts tickets per priority —
  `{"high": 3, "low": 1, ...}` — using `counts[p] = counts.get(p, 0) + 1`. Treat a
  missing priority as `"unset"`. This `.get(key, 0) + 1` line is one of the most
  common idioms in Python.
- **Sort the output.** Look up `sorted(..., key=...)` and write the urgent
  tickets out ordered by `id` descending (newest first).
- **Handle a broken input file.** Put a single quote in place of a double quote
  in a copy of the tickets file and run your script on it. Read the
  `JSONDecodeError` line and column, and find the typo from that alone.
- **Look at a real API response.** In your `01-03-ask.py`, after the call, add
  `print(json.dumps(message.to_dict(), indent=2))`. `to_dict()` is the SDK's way
  of handing you the response as a plain dict. Trace the path to the reply text
  and to `output_tokens` by hand, then compare it with the Messages API
  reference in the resources.
- **Update your default model.** Your scripts use `claude-opus-5`, which still
  works. The current Opus is `claude-opus-5-5`, and it's cheaper per token. Change
  the default in your `ask` function — one edit, because it's a function.
- **Put the model in the loop.** Combine this with 01-03: for each urgent
  ticket, call `ask` to write a one-sentence first reply, store it under a new
  key (`ticket["draft_reply"] = ...`), then save. That's a small, real,
  sellable workflow: triage plus drafted responses.

## Check yourself

<details markdown="1">
<summary>Your script crashes with <code>KeyError: 'phone'</code> on record 38 of 200. What does that tell you, and what are your two options?</summary>

Record 38 has no `phone` key — the other 37 did, so this is messy data, not a
typo in your code. If phone numbers are optional, use
`record.get("phone")` (or `.get("phone", "")`) so a missing one is handled. If
every record *must* have one, the crash is correct: keep the square brackets and
fix or report the bad record. The choice is about what the data is supposed to
guarantee.

</details>

<details markdown="1">
<summary>You <code>print(my_dict)</code>, copy the output into <code>data.json</code>, and <code>json.load</code> fails. Why, and what should you have done?</summary>

`print` shows Python's spelling: single quotes, `True`, `None`. JSON requires
double quotes, `true` and `null`, so the parser rejects it with
`JSONDecodeError`. Use `json.dumps(my_dict, indent=2)` to produce JSON text, or
better, write it straight to the file with `json.dump(my_dict, f, indent=2)`.

</details>

<details markdown="1">
<summary>Given <code>resp = {"results": [{"name": "Ana", "tags": ["vip", "eu"]}]}</code>, write the expression that gets <code>"eu"</code>.</summary>

`resp["results"][0]["tags"][1]`

Step by step: `resp["results"]` is a list → `[0]` is the first dict →
`["tags"]` is a list → `[1]` is its second item. Walking one bracket at a time
like this is how you'll read every unfamiliar API response.

</details>

<details markdown="1">
<summary>What's the difference between <code>json.load</code> and <code>json.loads</code>, and which does your build script need?</summary>

`json.load(f)` reads JSON from an open **file**; `json.loads(s)` reads JSON from
a **string** already in memory (the `s` is for *string*). The build reads a file,
so it uses `json.load` inside a `with open(...)` block — and `json.dump` to
write. You'd reach for `loads` when JSON arrives as text, like the body of a web
request.

</details>

<details markdown="1">
<summary>Your filter kept tickets 101 and 106 but missed 107, whose priority is <code>"HIGH"</code>. Fix <code>is_urgent</code> without listing every capitalisation.</summary>

Normalise before comparing:
`ticket.get("priority", "").lower() == "high"`. The `""` fallback matters —
without it, a missing priority gives `None`, and `None.lower()` raises
`AttributeError`. Cleaning a value *before* you compare it is a habit that
prevents a whole class of silent misses in real data.

</details>
