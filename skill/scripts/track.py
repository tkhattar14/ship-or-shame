#!/usr/bin/env python3
"""
Progress tracker — score computation, streak tracking, trend analysis.
Optionally pulls from Trello/GitHub to auto-detect completions.
"""

import json
import sys
import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "commitments"
SCORES_FILE = Path(__file__).resolve().parent.parent.parent / "data" / "scores.json"


def get_ist_now():
    ist = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(ist)


def load_day(date_str):
    f = DATA_DIR / f"{date_str}.json"
    if f.exists():
        with open(f) as fh:
            return json.load(fh)
    return None


def load_scores():
    if SCORES_FILE.exists():
        with open(SCORES_FILE) as f:
            return json.load(f)
    return {
        "start_date": get_ist_now().strftime("%Y-%m-%d"),
        "current_streak": 0,
        "best_streak": 0,
        "total_days": 0,
        "total_committed": 0,
        "total_completed": 0,
        "weekly_rates": [],
        "last_updated": None,
    }


def save_scores(scores):
    SCORES_FILE.parent.mkdir(parents=True, exist_ok=True)
    scores["last_updated"] = get_ist_now().isoformat()
    with open(SCORES_FILE, "w") as f:
        json.dump(scores, f, indent=2)


def cmd_score(args):
    """Show today's score and overall stats."""
    today = get_ist_now().strftime("%Y-%m-%d")
    day_data = load_day(today)
    scores = load_scores()

    if day_data:
        s = day_data["score"]
        print(f"📊 Today ({today}):")
        print(f"   {s['completed']}/{s['total']} — {s['rate']*100:.0f}%")
    else:
        print(f"📊 No commitments recorded for {today}")

    print(f"\n📈 Overall:")
    print(f"   Days tracked: {scores['total_days']}")
    print(f"   Total completed: {scores['total_completed']}/{scores['total_committed']}")
    if scores["total_committed"] > 0:
        overall_rate = scores["total_completed"] / scores["total_committed"]
        print(f"   Overall rate: {overall_rate*100:.0f}%")
    print(f"   Current streak: {scores['current_streak']} days (≥70%)")
    print(f"   Best streak: {scores['best_streak']} days")


def cmd_streak(args):
    """Compute current and best streaks from historical data."""
    scores = load_scores()
    today = get_ist_now()

    current_streak = 0
    best_streak = 0
    temp_streak = 0

    # Walk backwards from yesterday
    for i in range(1, 365):
        date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        day_data = load_day(date)
        if not day_data or not day_data.get("commitments"):
            break
        rate = day_data["score"]["rate"]
        if rate >= 0.7:  # 70% = good day
            current_streak += 1
        else:
            break

    # Walk all days for best streak
    start = datetime.strptime(scores.get("start_date", today.strftime("%Y-%m-%d")), "%Y-%m-%d")
    start = start.replace(tzinfo=timezone(timedelta(hours=5, minutes=30)))
    day = start
    while day <= today:
        date_str = day.strftime("%Y-%m-%d")
        day_data = load_day(date_str)
        if day_data and day_data.get("commitments"):
            if day_data["score"]["rate"] >= 0.7:
                temp_streak += 1
                best_streak = max(best_streak, temp_streak)
            else:
                temp_streak = 0
        day += timedelta(days=1)

    # Check today
    today_data = load_day(today.strftime("%Y-%m-%d"))
    if today_data and today_data.get("commitments") and today_data["score"]["rate"] >= 0.7:
        current_streak += 1

    scores["current_streak"] = current_streak
    scores["best_streak"] = max(scores["best_streak"], best_streak)
    save_scores(scores)

    direction = "up" if current_streak > 2 else ("down" if current_streak == 0 else "flat")
    print(f"🔥 Current streak: {current_streak} days")
    print(f"🏆 Best streak: {scores['best_streak']} days")
    print(f"📈 Direction: {direction}")


def cmd_weekly(args):
    """Compute weekly summary stats."""
    today = get_ist_now()
    week_data = []

    for i in range(7):
        date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        day_data = load_day(date)
        if day_data and day_data.get("commitments"):
            week_data.append(day_data)

    if not week_data:
        print("No data for the past week.")
        return

    total_committed = sum(d["score"]["total"] for d in week_data)
    total_completed = sum(d["score"]["completed"] for d in week_data)
    rate = total_completed / total_committed if total_committed > 0 else 0

    # Separate first and second half for trend
    days_tracked = len(week_data)

    shipped = []
    missed = []
    for d in week_data:
        for c in d["commitments"]:
            if c["status"] == "done":
                shipped.append(c["task"])
            elif c["status"] == "missed":
                missed.append(c["task"])

    print(f"📊 Weekly Summary ({days_tracked} days tracked):")
    print(f"   Completion rate: {rate*100:.0f}%")
    print(f"   Completed: {total_completed}/{total_committed}")
    print(f"\n✅ Shipped ({len(shipped)}):")
    for s in shipped[:10]:
        print(f"   • {s}")
    print(f"\n❌ Missed ({len(missed)}):")
    for m in missed[:10]:
        print(f"   • {m}")

    # Output JSON for publish script
    if args.json if hasattr(args, 'json') else False:
        summary = {
            "days_tracked": days_tracked,
            "total_committed": total_committed,
            "total_completed": total_completed,
            "rate": rate,
            "shipped": shipped,
            "missed": missed,
        }
        print("\n" + json.dumps(summary, indent=2))


def cmd_update(args):
    """Update overall scores from today's data."""
    scores = load_scores()
    today = get_ist_now().strftime("%Y-%m-%d")
    day_data = load_day(today)

    if not day_data or not day_data.get("commitments"):
        print("No commitments today to update.")
        return

    scores["total_days"] += 1
    scores["total_committed"] += day_data["score"]["total"]
    scores["total_completed"] += day_data["score"]["completed"]
    save_scores(scores)
    print(f"✓ Scores updated for {today}")


def main():
    parser = argparse.ArgumentParser(description="Progress tracker")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("score", help="Show today's score and overall stats")
    sub.add_parser("streak", help="Compute and display streak info")
    weekly_p = sub.add_parser("weekly", help="Weekly summary")
    weekly_p.add_argument("--json", action="store_true")
    sub.add_parser("update", help="Update overall scores from today")

    args = parser.parse_args()

    cmds = {
        "score": cmd_score,
        "streak": cmd_streak,
        "weekly": cmd_weekly,
        "update": cmd_update,
    }

    if args.command in cmds:
        cmds[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
