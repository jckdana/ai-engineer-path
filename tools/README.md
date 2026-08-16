# tools/

Deterministic Python scripts. One job per script, no reasoning, no surprises.

## Contract

Every tool:

1. Is runnable standalone: `python tools/<name>.py --arg value`
2. Parses args with `argparse` and has a `--help` that explains itself
3. Prints **one JSON object to stdout** — this is what the agent reads
4. Prints progress and errors to **stderr** via `common.log`
5. Exits `0` on success, `1` on handled failure (`common.emit` / `common.fail`)
6. Reads secrets only from `.env` via `common.require_env` — never hardcoded, never passed as a CLI arg
7. Writes intermediates only to `.tmp/` via `common.tmp_path`

## Skeleton

```python
import argparse
from common import emit, fail, log, require_env, tmp_path


def main():
    parser = argparse.ArgumentParser(description="One line: what this does.")
    parser.add_argument("--input", required=True, help="...")
    args = parser.parse_args()

    api_key = require_env("SOME_API_KEY")
    log(f"Processing {args.input}...")

    # ... work ...

    emit(output_path=str(path), rows=len(rows))


if __name__ == "__main__":
    main()
```

## Rules of thumb

- If it needs a judgment call, it belongs in a workflow, not here.
- Make it idempotent and re-runnable where possible.
- Tools that spend money or credits: say so in the `--help` text and in the workflow.
- Fix the tool when it breaks, then update the workflow that calls it.
