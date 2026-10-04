# Refresher: lessons 00-01 to 01-04

Everything taught so far, on one page, with the trap that goes with each idea. To review it:
cover the code, read the heading, and try to write the code from memory before you look.

---

## 1. Terminal, venv, packages (00-02)

```powershell
python --version                          # which Python
python -m venv .venv                      # make a virtual environment (once per project)
.venv\Scripts\Activate.ps1                # turn it on — prompt shows (.venv)
python -m pip install anthropic python-dotenv
python -m pip freeze > requirements-frozen.txt   # record exact versions
python -m pip install -r requirements.txt        # reinstall on a new machine
python builds/some-file.py                # run a script
code builds/some-file.py                  # open/create a file in VS Code
```

- **Why a venv:** each project gets its own packages, so updating one project can't
  break another.
- **Trap:** if you get `ModuleNotFoundError` for a package you know you installed, the venv
  probably isn't active.
- **Trap:** PowerShell is not Bash. A `\` at the end of a line doesn't continue the command,
  and `<something>` in a command is a placeholder you must replace. Keep commands on one line.

## 2. Git (00-03)

```powershell
git status                     # what changed? (run this constantly)
git diff                       # exactly what changed
git add <file>   /  git add -A # stage one file / everything
git commit -m "Say what and why"
git log --oneline -5           # recent history

git switch -c lesson/01-05     # new branch for the lesson
git switch main                # back to main
git merge lesson/01-05         # bring the branch's work in
git branch -d lesson/01-05     # delete the merged branch
git push                       # send to GitHub (updates the live site)
```

- **Rhythm:** branch, work, commit, switch to main, merge, delete the branch, push.
- **Trap:** a commit only contains what you staged with `git add`.

## 3. First program: print, variables, f-strings, input (00-04)

```python
name = "Jack"
lessons_done = 3
print(f"{name} has finished {lessons_done} lessons.")   # f-string: the f is required
print(f"After this one: {lessons_done + 1}")             # any expression inside {}

name = input("What's your name? ").strip().title()      # input() ALWAYS returns a string
age = int(input("Age? "))                               # convert before doing maths
```

- **Trap:** `"Lessons: " + 3` raises `TypeError`. Use an f-string instead.
- **Trap:** `print("{name}")` without the `f` prints `{name}` literally.
- **Reading errors:** start from the **bottom line** of a traceback. It names the error
  type, and the line just above it shows where it happened.

## 4. API key + first model call (00-05)

```python
# .env file (never committed):   ANTHROPIC_API_KEY=sk-ant-...
import anthropic
from dotenv import load_dotenv

load_dotenv()                       # copies .env into the environment — must come first
client = anthropic.Anthropic()      # finds the key itself

message = client.messages.create(
    model="claude-opus-5-5",        # current Opus; your old scripts say claude-opus-5
    max_tokens=300,                 # required; hard cap on reply length
    messages=[{"role": "user", "content": "Your question"}],
)

for block in message.content:       # content is a LIST of blocks — loop, don't [0]
    if block.type == "text":
        print(block.text)

print(message.stop_reason)          # "end_turn" = finished; "max_tokens" = CUT OFF
print(message.usage.input_tokens, message.usage.output_tokens)   # what you pay for
```

- **Check the key without showing it:** print its *length*, never the key itself.
- `git check-ignore -v .env` must print a line. If it prints nothing, your key is about
  to be committed.
- **`TypeError: Could not resolve authentication method`** means no key was found locally
  (forgot `load_dotenv()`, wrong folder, or blank key).
- **`401 AuthenticationError`** means a key *was* sent and was rejected (wrong, expired, or
  revoked).
- **Leaked key?** Revoke it in the Console immediately and make a new one. Don't debate it.
- `stop_reason == "max_tokens"` raises **no error**. You just get a truncated answer.

## 5. Types and strings (01-01)

```python
type("6")  # <class 'str'>      type(6)  # <class 'int'>
# str, int, float (7.5), bool (True/False — capital T/F)

text = "   Hello World   "
text.strip()            # shows a cleaned copy, then throws it away
text = text.strip()     # KEEP it: strings never change, you rebind the name

"HELLO".lower()   "hi".upper()   "hi there".title()   "hi there".capitalize()
"YES".lower() == "yes"           # compare text case-insensitively
"the  quick brown".split()       # ['the', 'quick', 'brown'] — no argument = any whitespace
" ".join("  messy   spacing ".split())   # 'messy spacing' — normalise spacing
"a, a".replace("a", "b")         # 'b, b'
"error" in "connection error"    # True
len("abc")  # 3 chars     len(["a", "b"])  # 2 items
```

- **Trap:** `cleaned.lower()` without `cleaned = ` gives no error and no change.
- **Trap:** `.strip(" Python")` strips a *set of characters*, not a word. Use
  `.removeprefix()` / `.removesuffix()` instead.
- **Trap:** `.split(" ")` with an argument creates empty strings wherever there are double
  spaces.

## 6. Lists, loops, conditionals (01-02)

```python
questions = ["What is an API?", "What is a token?", "What is JSON?"]
questions[0]     # first      questions[-1]   # last      questions[3]  # IndexError
questions.append("New one")   # lists change IN PLACE — never write x = x.append(...)

results = []                          # create OUTSIDE the loop
for i, q in enumerate(questions, start=1):
    if not q.strip():                 # empty / whitespace-only is falsy
        print("skipping a blank")
        continue                      # skip to next item   (break = leave loop entirely)
    print(f"{i}/{len(questions)}: {q}")
    results.append(q)                 # fill INSIDE the loop

score = 72
if score >= 90:   print("A")
elif score >= 70: print("B")          # first true branch wins; the rest are skipped
else:             print("F")
```

- **Strings vs lists:** `text = text.strip()` (must catch the result).
  `items.append(x)` (never catch the result, because it returns `None`).
- **Falsy values:** `""`, `[]`, `0`, `None`. Almost everything else is truthy.
- **Trap:** setting a counter (`count = 0`) *inside* the loop resets it on every pass.
- **Habit:** dry-run any loop around a paid API call with fake answers first.

## 7. Functions (01-03)

```python
def ask(question, model="claude-opus-5-5", max_tokens=500):
    """Send one question to the model and return the reply text."""   # docstring
    message = client.messages.create(
        model=model, max_tokens=max_tokens,
        messages=[{"role": "user", "content": question}],
    )
    parts = []
    for block in message.content:
        if block.type == "text":
            parts.append(block.text)
    return "".join(parts)             # RETURN gives the value back to the caller

answer = ask("Name three uses for a paperclip.")
short  = ask("Say hello in five words.", max_tokens=40)    # override one default
```

- **`print` vs `return`:** a function that only prints gives back `None`.
  `return` hands the value back so other code can use it.
- **Scope:** variables made inside a function don't exist outside it (`NameError`).
- **Trap:** never use a mutable default like `def f(x, bucket=[])`. Use `bucket=None`, then
  `if bucket is None: bucket = []`.
- `help(ask)` / `ask.__doc__` shows the docstring.

## 8. Dictionaries, JSON, files (01-04)

```python
ticket = {"id": 101, "customer": "Dana", "priority": "high"}
ticket["customer"]              # read (KeyError if missing)
ticket["priority"] = "low"      # change existing
ticket["assigned_to"] = "Jack"  # add new — same syntax
ticket.get("email")             # None instead of crashing
ticket.get("email", "")         # your fallback instead
"email" in ticket               # does the key exist?
for key, value in ticket.items():
    print(f"{key}: {value}")

message["content"][0]["text"]   # nested: read left to right, one step at a time

import json
text = json.dumps(ticket)       # dict -> JSON string  (True->true, None->null, "double quotes")
back = json.loads(text)         # JSON string -> dict

with open("builds/in.json", encoding="utf-8") as f:        # READ a file
    data = json.load(f)
with open("builds/out.json", "w", encoding="utf-8") as f:  # WRITE ("w" replaces the file)
    json.dump(data, f, indent=2)
```

- **`[]` vs `.get()`:** use `[]` when a missing key is a bug you want to see, and
  `.get()` when the data comes from outside and might be missing things.
- **`.get()` + string method:** `ticket.get("priority", "").lower()` works.
  `.get("priority")` with no fallback returns `None`, and `None.lower()` crashes.
- **`load`/`dump`** work with a file. **`loads`/`dumps`** (the s is for string) work with
  a string.
- **Trap:** `print(some_dict)` shows Python's spelling (single quotes, `True`), which is not
  valid JSON.
- **Trap:** leave off `encoding="utf-8"` on Windows and *Zoë* turns into *ZoÃ«*, with no
  error.

---

## Quick recall check

Answer these out loud without looking. If one stumps you, reread its section.

1. Why does `text.strip()` on its own line do nothing useful?
2. Why is `items = items.append(x)` a bug, while `text = text.strip()` is correct?
3. What's the difference between `stop_reason: max_tokens` and a `TypeError`?
4. A function prints the right answer but `result` is `None`. What's missing?
5. When should you use `ticket["priority"]` instead of `ticket.get("priority")`?
6. What do the `s` in `json.loads` and the `"w"` in `open(path, "w")` mean?
7. Your counter ends at 1 after looping over 10 items. Where did you put `count = 0`?
