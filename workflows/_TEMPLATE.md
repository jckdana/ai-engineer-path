# <Workflow Name>

**Objective:** One or two sentences. What does "done" look like?

**When to use:** The trigger — what the user asks for that leads here.

## Inputs

| Input | Required | Description | Default |
|---|---|---|---|
| `example_url` | yes | The page to pull from | — |
| `limit` | no | Max rows to process | 100 |

Ask me for anything required that wasn't provided. Don't guess.

## Tools used

| Tool | Purpose | Costs money? |
|---|---|---|
| `tools/example.py` | Does the thing | No |

## Steps

1. Validate inputs — confirm required values are present and well-formed.
2. Run `python tools/example.py --input <value>`. Read the JSON on stdout.
3. Check the result. If `ok: false`, see **Failure handling** below.
4. Write the deliverable to <cloud destination>.
5. Report back: what was produced, where it lives, anything notable.

## Output

- **Deliverable:** where the final artifact lands (Sheet, Slides, Doc — a link I can open)
- **Intermediates:** `.tmp/...` — disposable

## Failure handling

| Symptom | Cause | Fix |
|---|---|---|
| `Missing required env var` | Key not in `.env` | Ask me for it; never invent one |
| HTTP 429 | Rate limit | Back off, retry; if repeated, look for a batch endpoint and refactor the tool |

## Notes & learnings

Append here as you discover constraints, quirks, or better methods. Date each entry.

- YYYY-MM-DD — ...
