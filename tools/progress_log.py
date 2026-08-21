"""Record a study session: streak, completion, and the thing you built.

Progress is an append-only list of session records. Every derived number
(streak, percent complete, portfolio) is recomputed from that list at build
time, so nothing here can drift out of sync.

Usage (PowerShell — one line each; `\` is bash and will not continue a line here):
    python tools/progress_log.py --lesson-id 03-02 --status complete --minutes 55 --artifact ./builds/tool_use_demo.py --note "tool_choice was the missing piece"
    python tools/progress_log.py --lesson-id 03-02 --status started --minutes 20
    python tools/progress_log.py --lesson-id 03-02 --status complete --minutes 50 --date 2026-08-14
"""

import argparse
from datetime import datetime

from common import (
    PROGRESS_FILE,
    ROADMAP_FILE,
    emit,
    fail,
    log,
    read_json,
    today,
    write_json,
)
from streak import current_streak, longest_streak


def main():
    ap = argparse.ArgumentParser(description="Log a study session.")
    ap.add_argument("--lesson-id", required=True)
    ap.add_argument("--status", choices=["started", "complete"], default="complete")
    ap.add_argument("--minutes", type=int, required=True, help="Minutes actually spent")
    ap.add_argument("--artifact", default="", help="Path or URL of what you built")
    ap.add_argument("--note", default="", help="What clicked, what didn't")
    ap.add_argument("--date", default="", help="YYYY-MM-DD; defaults to today")
    args = ap.parse_args()

    if args.minutes <= 0:
        fail("--minutes must be positive.")

    date = args.date or today()
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        fail(f"--date must be YYYY-MM-DD, got '{date}'.")

    roadmap = read_json(ROADMAP_FILE)
    if roadmap is None:
        fail("No content/roadmap.json. Run tools/roadmap_init.py first.")

    lookup = {
        l["id"]: (m, l)
        for m in roadmap.get("modules", [])
        for l in m.get("lessons", [])
    }
    if args.lesson_id not in lookup:
        fail(f"Lesson id '{args.lesson_id}' is not in the roadmap.")
    _module, lesson = lookup[args.lesson_id]

    if args.status == "complete" and not args.artifact:
        log("WARNING: completing a lesson with no --artifact. The build task is the point;")
        log("         the portfolio page only lists sessions that shipped something.")

    progress = read_json(PROGRESS_FILE) or {"started_on": date, "sessions": []}
    progress.setdefault("sessions", [])
    progress["sessions"].append(
        {
            "date": date,
            "lesson_id": args.lesson_id,
            "status": args.status,
            "minutes": args.minutes,
            "artifact": args.artifact,
            "note": args.note,
        }
    )
    progress["sessions"].sort(key=lambda s: (s["date"], s["lesson_id"]))
    write_json(PROGRESS_FILE, progress)

    dates = {s["date"] for s in progress["sessions"]}
    completed = {s["lesson_id"] for s in progress["sessions"] if s["status"] == "complete"}
    total = len(lookup)

    streak = current_streak(dates)
    log(f"Logged {args.minutes} min on {args.lesson_id} ({args.status}). Streak: {streak} day(s).")

    emit(
        lesson_id=args.lesson_id,
        lesson_title=lesson["title"],
        status=args.status,
        date=date,
        minutes=args.minutes,
        artifact=args.artifact,
        streak=streak,
        best_streak=longest_streak(dates),
        completed=len(completed),
        total=total,
        percent=round(100 * len(completed) / total) if total else 0,
        next_step="python tools/site_build.py --open",
    )


if __name__ == "__main__":
    main()
