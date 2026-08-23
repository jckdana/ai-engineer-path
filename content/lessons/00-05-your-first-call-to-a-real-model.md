---
id: "00-05"
title: "Your first call to a real model"
module: "00"
core_minutes: 50
deep_minutes: 120
build: "A script that sends a question to Claude and prints the answer, with the API key loaded from .env and never committed."
resources:
  - title: "Claude docs — Get started (make your first API call)"
    url: "https://platform.claude.com/docs/en/get-started"
  - title: "Claude docs — Using the Messages API"
    url: "https://platform.claude.com/docs/en/build-with-claude/working-with-messages"
  - title: "Claude docs — Errors (what each status code means)"
    url: "https://platform.claude.com/docs/en/api/errors"
  - title: "Claude docs — Pricing (per-million-token rates)"
    url: "https://platform.claude.com/docs/en/about-claude/pricing"
  - title: "python-dotenv on PyPI — load_dotenv and .env files"
    url: "https://pypi.org/project/python-dotenv/"
  - title: "anthropic-sdk-python on GitHub — the SDK you're installing"
    url: "https://github.com/anthropics/anthropic-sdk-python"
---

## Why this matters

Everything you've done so far has run entirely on your own machine. This lesson is
the first time your code reaches out and talks to something else — a model running
in a data centre you don't own, over the internet, using a key that proves you're
allowed to.

That's the shape of nearly all AI engineering. You will not train models. You will
send carefully assembled text to someone else's model and do something useful with
what comes back. Everything later in this path — prompts, tools, RAG, agents,
evals — is a variation on the twenty lines you're about to write.

By the end you'll have an API key, know why it lives in a file git refuses to
commit, and have a script that asks Claude a question and prints the answer. You'll
also know what the response actually *is* — not a string, but an object with
several parts, one of which happens to be text.

## The mental model

Two separate things travel from your machine to Anthropic's servers, and keeping
them separate in your head prevents most of the confusion beginners hit.

The first is your **message** — the question, written in your code, safe to show
anyone. The second is your **API key** — a long secret string that identifies your
account and gets billed for the call. The key is *never* written in your code. It
sits in a file called `.env`, gets loaded into your program's environment when it
starts, and the SDK picks it up from there and attaches it as an HTTP header.
Your source file stays publishable; the secret stays out of git.

<figure class="figure">
<svg viewBox="0 0 760 400" role="img" aria-label="One API call has two inputs that travel by different routes. Your script holds the message: the model name, a max_tokens limit, and a list of messages. That goes out as an HTTPS POST request to api.anthropic.com. The API key travels separately: it sits in a gitignored .env file, load_dotenv reads it into the running program's environment, and the SDK attaches it to the same request as an x-api-key header, so the key is never written in your source file. The server replies with JSON, which the SDK turns into a Message object holding a list of content blocks, a usage token count, and a stop_reason.">
  <defs>
    <marker id="m5-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="currentColor"/>
    </marker>
    <marker id="m5-ar-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
      <path d="M0 0 L10 5 L0 10 z" fill="var(--accent)"/>
    </marker>
  </defs>

  <g font-family="system-ui, sans-serif" font-size="12" fill="currentColor">

    <!-- your script -->
    <rect x="14" y="104" width="196" height="104" rx="9" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.45"/>
    <text x="112" y="128" text-anchor="middle" font-weight="600">your script</text>
    <text x="30" y="150" font-family="ui-monospace, monospace" font-size="10" opacity="0.65">model="claude-opus-5"</text>
    <text x="30" y="166" font-family="ui-monospace, monospace" font-size="10" opacity="0.65">max_tokens=200</text>
    <text x="30" y="182" font-family="ui-monospace, monospace" font-size="10" opacity="0.65">messages=[{role, content}]</text>
    <text x="30" y="198" font-family="ui-monospace, monospace" font-size="10" opacity="0.65">— no key anywhere —</text>

    <!-- the server -->
    <rect x="550" y="104" width="196" height="104" rx="9" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.45"/>
    <text x="648" y="140" text-anchor="middle" font-family="ui-monospace, monospace" font-size="11" font-weight="600">api.anthropic.com</text>
    <text x="648" y="164" text-anchor="middle" font-size="10.5" opacity="0.65">checks the key,</text>
    <text x="648" y="180" text-anchor="middle" font-size="10.5" opacity="0.65">runs the model,</text>
    <text x="648" y="196" text-anchor="middle" font-size="10.5" opacity="0.65">bills your account</text>

    <!-- request arrow -->
    <line x1="214" y1="132" x2="544" y2="132" stroke="currentColor" stroke-width="1.5" marker-end="url(#m5-ar)"/>
    <text x="379" y="112" text-anchor="middle" font-size="11.5" font-weight="600">POST /v1/messages</text>
    <text x="379" y="126" text-anchor="middle" font-size="10.5" opacity="0.65">your question, as JSON</text>

    <!-- response arrow -->
    <line x1="544" y1="186" x2="214" y2="186" stroke="currentColor" stroke-width="1.5" marker-end="url(#m5-ar)"/>
    <text x="379" y="204" text-anchor="middle" font-size="11.5" font-weight="600">JSON response</text>

    <!-- the key's separate route -->
    <rect x="14" y="288" width="196" height="82" rx="9" fill="var(--accent-tint)" stroke="var(--accent)" stroke-width="1.8" stroke-dasharray="5 3"/>
    <text x="112" y="312" text-anchor="middle" font-family="ui-monospace, monospace" font-size="11" font-weight="600" fill="var(--accent)">.env</text>
    <text x="112" y="332" text-anchor="middle" font-family="ui-monospace, monospace" font-size="9.5" fill="var(--accent)">ANTHROPIC_API_KEY=sk-ant-…</text>
    <text x="112" y="352" text-anchor="middle" font-size="10" fill="var(--accent)">listed in .gitignore —</text>
    <text x="112" y="365" text-anchor="middle" font-size="10" fill="var(--accent)">git will not commit it</text>

    <!-- key path: .env -> environment -> header on the same request -->
    <path d="M210 322 L300 322 L300 258 L379 258 L379 146" fill="none" stroke="var(--accent)" stroke-width="1.8" marker-end="url(#m5-ar-a)"/>
    <text x="228" y="312" font-size="10.5" fill="var(--accent)">load_dotenv() → os.environ</text>
    <text x="392" y="252" font-size="10.5" fill="var(--accent)">SDK adds header</text>
    <text x="392" y="266" font-family="ui-monospace, monospace" font-size="10" fill="var(--accent)">x-api-key: sk-ant-…</text>

    <!-- what comes back -->
    <rect x="286" y="300" width="290" height="84" rx="9" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.45"/>
    <text x="431" y="322" text-anchor="middle" font-family="ui-monospace, monospace" font-size="11" font-weight="600">Message object</text>
    <text x="302" y="342" font-family="ui-monospace, monospace" font-size="10" opacity="0.65">.content  → a list of blocks, not a string</text>
    <text x="302" y="358" font-family="ui-monospace, monospace" font-size="10" opacity="0.65">.usage    → tokens in / tokens out</text>
    <text x="302" y="374" font-family="ui-monospace, monospace" font-size="10" opacity="0.65">.stop_reason → why it stopped</text>
    <path d="M300 196 L300 220 L431 220 L431 294" fill="none" stroke="currentColor" stroke-width="1.3" stroke-dasharray="4 3" opacity="0.55" marker-end="url(#m5-ar)"/>
    <text x="444" y="216" font-size="10.5" opacity="0.65">the SDK parses it for you</text>

  </g>
</svg>
<figcaption>One call, two routes. The message is written in your code; the key never is —
it travels from <code>.env</code> through your program's environment into an HTTP header the SDK
adds for you. That's what makes the script safe to commit.</figcaption>
</figure>

Three terms, plainly:

- An **API** (application programming interface) is a way for one program to ask
  another program to do something. Here it's a web address you send text to.
- An **API key** is a password for a program rather than a person. Anyone holding
  it can spend your money, which is why it never goes in a file git tracks.
- An **SDK** (software development kit) is a library that hides the tedious parts —
  building the HTTP request, setting headers, retrying, parsing JSON. You'll install
  Anthropic's Python SDK, called `anthropic`.

## In practice

### Get a key

Go to [platform.claude.com](https://platform.claude.com), make an account, then
open **Settings → API keys** and create one. Copy it immediately — the full value
is shown once and never again. It looks like `sk-ant-api03-` followed by a long
string.

The create dialog asks for three things. **Workspace** can stay `Default`.
**Name** should be something you'll recognise in six months — `ai-engineer-path`,
not `key1` — because the whole point of naming is knowing which key to revoke
without revoking the others. **Expires** offers everything from 3 hours to Never;
choose **30 days**.

Thirty days is a backstop for the mistake you haven't made yet. Right now you're
still building the habits that keep a key out of screenshots, chat messages, and
commits — an expiry date means any key that escapes stops working on its own.
`Never` is the right answer for a deployed service where an expiry means a 3am
outage, and that is not what you're doing. When the key does lapse, your script
starts failing with a `401` even though nothing in your code changed; make a new
key, paste it into `.env`, and you're going again in under a minute.

You'll also need a few dollars of credit under **Settings → Billing**. To calibrate:
Claude Opus 5 costs **$5 per million input tokens and $25 per million output tokens**.
A token is roughly ¾ of a word. The script in this lesson sends maybe 20 tokens and
gets back a couple hundred — call it half a cent per run. You would have to run it
several thousand times to spend a pound. Cost stops being trivial when you start
sending whole documents, which is lesson 02-05's subject.

### Put the key where git can't reach it

This repo already has a `.env` file. Open it in your editor:

```powershell
code .env
```

**Everything in this section happens inside that file, not at the terminal
prompt.** The two blocks below are file *contents* — lines you edit and save, not
commands you run. Typing `ANTHROPIC_API_KEY=sk-ant-...` at a PowerShell prompt
gets you `CommandNotFoundException`, because PowerShell reads it as a request to
run a program by that very long name. (In bash that syntax *would* set a
variable, which is why the mistake is an easy one to make.)

The file may already hold other projects' keys. Find the line beginning
`ANTHROPIC_API_KEY=` — it's waiting empty:

```text
ANTHROPIC_API_KEY=
```

Put your key immediately after that `=`, with no quotes and no spaces, and save:

```text
ANTHROPIC_API_KEY=sk-ant-api03-your-actual-key-here
```

If VS Code offers to enable `python.terminal.useEnvFile`, decline it. That
setting injects `.env` into every terminal you open, which would mean your key is
loaded whether a program asked for it or not — and it would quietly break the
experiment at the end of this lesson, where you *want* the missing key to cause a
visible error.

Now confirm the key loaded, without ever putting it on screen:

```powershell
python -c "from dotenv import load_dotenv; import os; load_dotenv(); k=os.getenv('ANTHROPIC_API_KEY'); print('loaded, length', len(k)) if k else print('NOT FOUND')"
```

You want `loaded, length 108` or thereabouts. `NOT FOUND` means the file didn't
save, or the variable name is misspelled. Checking a secret's *length* rather
than echoing its value is a habit worth keeping for good: the instant a key
appears on screen it exists in scrollback, screen recordings, and screenshots.

Before going further, prove to yourself that git will ignore it:

```powershell
git check-ignore -v .env
```

```text
.gitignore:2:.env       .env
```

That output means "line 2 of `.gitignore` is why `.env` is excluded". If the
command prints *nothing*, git is not ignoring the file and your next commit would
publish your key — stop and fix `.gitignore` first.

There's also a `.env.example` in the repo, which *is* committed. It lists the
variable names with empty values, so someone cloning your repo knows what to fill
in without ever seeing your secrets. That pair — a real `.env` that's ignored, an
example that isn't — is the standard arrangement across the industry.

**If a key ever does get out** — pasted into a chat, caught in a screenshot,
committed by accident — revoke it. Console → Settings → API keys → delete the
one that leaked, then create a replacement and update `.env`. Revocation is
instant and total: anything still using the old key starts getting `401`. This is
not a big deal *if you do it promptly*, and expensive if you don't; keys scraped
out of public repositories get used within minutes, billed to your card. Treat
"I think that key was visible somewhere" as sufficient reason to replace it. You
never need to be certain, because replacing a key costs you thirty seconds.

### Install the SDK

Make sure your virtual environment is active — your prompt should start with
`(.venv)`. If it doesn't:

```powershell
.venv\Scripts\Activate.ps1
```

Then install both libraries:

```powershell
pip install anthropic python-dotenv
```

`anthropic` is Anthropic's official Python SDK (it needs Python 3.10 or newer;
you have 3.14). `python-dotenv` is the small library that reads `.env` files.

Record what you installed, so the next person — including future you on a new
machine — can reproduce it:

```powershell
pip freeze > requirements-frozen.txt
```

### The call itself

Create the file:

```powershell
code builds/00-05-ask.py
```

Type this in. It's short, and every line earns its place:

```python
# Asks Claude a question and prints the answer.
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-opus-5",
    max_tokens=300,
    messages=[
        {"role": "user", "content": "In one sentence, what is an API key for?"}
    ],
)

for block in message.content:
    if block.type == "text":
        print(block.text)
```

Line by line:

- `load_dotenv()` reads `.env` and copies each `NAME=value` pair into
  `os.environ` — the set of variables your running program can see. It changes
  nothing on disk and nothing outside this process.
- `anthropic.Anthropic()` builds the client. You passed it no key: it looks for
  `ANTHROPIC_API_KEY` in the environment itself, which `load_dotenv()` just put
  there. This is why the order of those two lines matters.
- `messages` is a **list of dictionaries**. Each has a `role` and `content`. For
  now there's one, with the role `"user"` — you. Lesson 02-01 is entirely about
  this list.
- `max_tokens` is a hard ceiling on the *reply* length. It is required. Set it too
  low and the answer gets cut off mid-sentence.

Run it:

```powershell
python builds/00-05-ask.py
```

```text
An API key is a unique credential that identifies and authenticates your
application when it makes requests to a service, so the provider knows who is
calling and what they're allowed to do.
```

Your wording will be different from mine, and different again if you run it twice.
That's not a bug — a model is not a lookup table, and lesson 03-02 explains why.
Either way: you just paid a fraction of a penny for that. Congratulations.

### Why the loop, instead of `message.content[0].text`

You'll see `message.content[0].text` in a lot of tutorials, and it works right up
until it doesn't. `content` is a **list of content blocks**, and a block is not
always text — a response can also carry a thinking block, or later in this path,
a request to use a tool. Indexing at `[0]` assumes the first block is text and
crashes with an `AttributeError` when it isn't.

The loop with `if block.type == "text"` costs you two extra lines and never
breaks. Get in the habit now, while the habit is cheap.

### Look at the whole response

Add this to the bottom of your file to see what else came back:

```python
print()
print("stop_reason:", message.stop_reason)
print("input tokens:", message.usage.input_tokens)
print("output tokens:", message.usage.output_tokens)
```

```text
stop_reason: end_turn
input tokens: 18
output tokens: 41
```

`stop_reason: end_turn` means Claude finished on its own. The value you need to
recognise is `max_tokens` — that means your ceiling cut it off, and the reply you
got is *incomplete*. No error is raised. Nothing turns red. You just get a
truncated answer, and the only way to know is to check this field. Try it: set
`max_tokens=10`, run again, and watch the sentence stop mid-word.

The `usage` numbers are what you're billed on. Multiply them by the per-million
rates above and you have the exact cost of the call.

### Two failures worth causing on purpose

**Forget `load_dotenv()`** — comment the line out and run:

```text
Traceback (most recent call last):
  File "E:\Claude Knowledge\builds\00-05-ask.py", line 9, in <module>
    message = client.messages.create(
    ...
TypeError: "Could not resolve authentication method. Expected one of api_key,
auth_token, or credentials to be set. ..."
```

Read the bottom line: the SDK looked for a key and found nothing. Note that this
happens *before* any network request — the SDK refuses to send an unauthenticated
call. The same error appears if `.env` exists but the key is blank, or if you run
the script from a different folder where `load_dotenv()` finds no `.env` at all.

**Use a wrong key** — change one character in `.env` and run again. This time the
request does go out, and the server rejects it with HTTP **401**, which the SDK
raises as `anthropic.AuthenticationError`. Two different failures, two different
causes: `TypeError` means *no key was found locally*; `401` means *a key was sent
and Anthropic didn't accept it*. Telling them apart saves you twenty minutes the
first time it happens for real.

Put your key back afterwards.

## Build it

A script that sends a question to Claude and prints the answer, with the key
loaded from `.env` and never committed.

**1. Branch first:**

```powershell
git switch -c lesson/00-05
```

**2. Write `builds/00-05-ask.py`.** It must:

- load the key with `load_dotenv()` and create the client with no arguments
- ask a question you actually want the answer to — pick your own, not the one above
- use `input()` so the question is typed when the script runs, rather than
  hard-coded (you learned this last lesson)
- print the reply by looping over `message.content` and checking `block.type`
- print `stop_reason` and both token counts on their own lines afterwards
- start with a `#` comment saying what the file does

**3. Prove the key is safe.** Run `git status`. `.env` must not appear in it —
not as modified, not as untracked. If it does, do not commit; fix `.gitignore`
first.

**4. Run it three times:** once normally, once with `max_tokens=10` to see
`stop_reason: max_tokens`, and once with `load_dotenv()` commented out to see the
`TypeError`. Restore the working version before committing.

**5. Commit and merge:**

```powershell
git add builds/00-05-ask.py requirements-frozen.txt
git commit -m "Add first API call script from lesson 00-05"
git switch main
git merge lesson/00-05
git branch -d lesson/00-05
git push
```

Done when:

- `python builds/00-05-ask.py` asks you for a question and prints Claude's answer
- The word `sk-ant` appears nowhere in any file git is tracking — check with
  `git grep "sk-ant"`, which should print nothing
- `git status` shows `nothing to commit, working tree clean`, with `.env` absent
- You can say what `stop_reason: max_tokens` means and why it isn't an error
- You've seen the `TypeError` from a missing key and can explain how it differs
  from a 401

Then log it:

```powershell
python tools/progress_log.py --lesson-id 00-05 --status complete --minutes 50 --artifact ./builds/00-05-ask.py --note "first call to a real model"
python tools/site_build.py --open
```

That's module 00 finished. You have an environment, version control, a program you
wrote, and a working line to a frontier model. Module 01 goes back to Python
properly, because the next thing standing between you and useful software is
loops, dictionaries and functions — not the API.

## Going deeper

- Add a `system` prompt: pass `system="Answer in exactly two sentences."` alongside
  `messages`. Same question, different behaviour. That's lesson 02-02's whole
  subject, previewed in one line.
- Print the raw response with `print(message.to_dict())` and compare it to the JSON
  in [Using the Messages API](https://platform.claude.com/docs/en/build-with-claude/working-with-messages).
  Every attribute you've used is a key in that dictionary.
- Make the script report its own cost: multiply `usage.input_tokens` by 5/1,000,000
  and `usage.output_tokens` by 25/1,000,000, and print the total to six decimal
  places with `f"{cost:.6f}"`.
- Read the [errors page](https://platform.claude.com/docs/en/api/errors) and note
  which codes mean *your fault* (400, 401, 403) and which mean *try again* (429,
  500, 529). The SDK already retries the second group for you, twice, automatically.
- Swap `model="claude-opus-5"` for `model="claude-haiku-4-5"` — a smaller, faster,
  cheaper model at $1/$5 per million tokens. Ask both the same hard question and
  the same easy one. Where does the difference show up, and where doesn't it?
  Choosing between them for real is lesson 13-03.
- Look up what an environment variable actually is at the operating-system level.
  It explains why `.env` files exist at all, and why every cloud host configures
  secrets this way.

## Check yourself

<details markdown="1"><summary>Your script runs fine on your machine. You push it to a public GitHub repo and a stranger clones it. What breaks for them, and why is that the correct behaviour?</summary>

Their run fails with the `TypeError` about not resolving an authentication method,
because `.env` was never committed — they cloned your code but not your key.

That's exactly right. The key identifies *your* account and bills *your* card. Code
is meant to be shareable; credentials are not. What they should do is copy
`.env.example` to `.env` and fill in their own key, which is why that example file
is committed and the real one isn't.

</details>

<details markdown="1"><summary>You get back a confident, complete-sounding answer, but `stop_reason` says `max_tokens`. Is anything wrong?</summary>

Yes. `max_tokens` means Claude was still generating when your ceiling stopped it,
so the reply is cut short — even if it happens to end at a plausible point.

This is a bug with no traceback, the same category as the missing `f` on an
f-string in the last lesson. The program ran, nothing went red, and the output is
wrong. Checking `stop_reason` is how you catch it, and it's why every serious
script that calls a model checks it rather than assuming.

</details>

<details markdown="1"><summary>Why does `anthropic.Anthropic()` work when you passed it no API key at all?</summary>

Because the client looks for one in the environment — specifically for a variable
named `ANTHROPIC_API_KEY` — and `load_dotenv()` put it there a line earlier by
reading `.env`.

Nothing magic is happening: `.env` is a plain text file, `load_dotenv()` copies its
contents into `os.environ` for this process only, and the SDK reads from
`os.environ`. Swap the two lines around and it fails, because the client would look
before anything had been loaded.

</details>

<details markdown="1"><summary>A tutorial you find online uses `print(message.content[0].text)`. Why does that work in the tutorial and why shouldn't you copy it?</summary>

It works whenever the first block in the list happens to be a text block, which is
most of the time for a plain question.

It's fragile because `content` is a *list of blocks* and the block types vary — a
response can include thinking blocks, and later in this path, tool-use blocks.
The moment one of those lands first, `[0].text` raises an `AttributeError` in code
you wrote weeks earlier and haven't thought about since. Looping and checking
`block.type` never has that failure mode.

</details>

<details markdown="1"><summary>You changed one character of your key and now get `anthropic.AuthenticationError` instead of the `TypeError` you saw earlier. What does that swap tell you about where each failure happened?</summary>

The `TypeError` was raised on your own machine, before anything was sent — the SDK
found no key and refused to build a request. No network, no cost.

The `AuthenticationError` means a request *did* travel to `api.anthropic.com`, and
the server replied with HTTP 401 because the key it received isn't valid. The
failure moved from your side of the wire to theirs. That distinction — local
validation versus a server response — is worth carrying into every API you ever
use, because it tells you which half of the system to go and look at.

</details>
