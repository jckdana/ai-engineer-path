"""Streak math, shared by progress_log.py and site_build.py.

One rule, applied everywhere: a streak is a run of consecutive calendar days
that have at least one session. The current streak stays alive if the most
recent day is today *or* yesterday — you haven't broken it just because you
haven't studied yet this morning. Two clear days ends it.
"""

from datetime import date, timedelta


def _parse(dates):
    out = set()
    for d in dates:
        y, m, dd = (int(x) for x in str(d).split("-"))
        out.add(date(y, m, dd))
    return out


def current_streak(dates, ref=None) -> int:
    days = _parse(dates)
    if not days:
        return 0
    ref = ref or date.today()

    cursor = ref if ref in days else ref - timedelta(days=1)
    if cursor not in days:
        return 0

    n = 0
    while cursor in days:
        n += 1
        cursor -= timedelta(days=1)
    return n


def longest_streak(dates) -> int:
    days = sorted(_parse(dates))
    if not days:
        return 0

    best = run = 1
    for prev, cur in zip(days, days[1:]):
        run = run + 1 if cur - prev == timedelta(days=1) else 1
        best = max(best, run)
    return best


def streak_line(dates, streak: int, ref=None) -> str:
    """The human sentence under the hero number. Nudges without nagging."""
    days = _parse(dates)
    ref = ref or date.today()

    if not days:
        return "No sessions logged yet. The first one is the hard one."
    if streak == 0:
        gap = (ref - max(days)).days
        return f"Last session was {gap} days ago. Streaks restart at 1 — start one today."
    if ref in days:
        return "Logged today. Come back tomorrow to keep it."
    return "Yesterday counted. Log a session today to keep the run alive."
