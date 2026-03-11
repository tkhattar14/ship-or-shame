#!/usr/bin/env python3
"""
Internal reporter — generates reports for accountability partners.
Not for public posting — see publish.py for that.
"""

import json
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
    return {"current_streak": 0, "best_streak": 0}


def generate_daily_report():
    """Generate daily internal report."""
    today = get_ist_now().strftime("%Y-%m-%d")
    data = load_day(today)
    scores = load_scores()

    if not data or not data.get("commitments"):
        return f"📊 Daily Report — {today}\n\nNo commitments recorded today."

    s = data["score"]
    report = f"📊 Daily Report — {today}\n\n"
    report += f"Score: {s['completed']}/{s['total']} ({s['rate']*100:.0f}%)\n"
    report += f"Streak: {scores.get('current_streak', 0)} days\n\n"

    for c in data["commitments"]:
        icon = {"done": "✅", "missed": "❌", "pending": "⏳"}.get(c["status"], "❓")
        report += f"{icon} {c['task']}"
        if c.get("notes") and c["status"] == "missed":
            report += f" — {c['notes']}"
        report += "\n"

    # Assessment
    report += "\n"
    if s["rate"] >= 0.8:
        report += "Assessment: Good day. Commitments delivered."
    elif s["rate"] >= 0.5:
        report += "Assessment: Partial delivery. Needs improvement."
    else:
        report += "Assessment: Below expectations. Intervention may be needed."

    return report


def generate_weekly_report():
    """Generate weekly internal scorecard."""
    today = get_ist_now()
    scores = load_scores()

    report = f"📊 Weekly Scorecard — w/e {today.strftime('%Y-%m-%d')}\n\n"

    daily_scores = []
    all_shipped = []
    all_missed = []

    for i in range(7):
        date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        day = load_day(date)
        if day and day.get("commitments"):
            rate = day["score"]["rate"]
            emoji = "🟢" if rate >= 0.8 else ("🟡" if rate >= 0.5 else "🔴")
            day_name = (today - timedelta(days=i)).strftime("%a")
            report += f"  {emoji} {day_name} {date}: {day['score']['completed']}/{day['score']['total']} ({rate*100:.0f}%)\n"
            daily_scores.append(rate)
            for c in day["commitments"]:
                if c["status"] == "done":
                    all_shipped.append(c["task"])
                elif c["status"] == "missed":
                    all_missed.append(c["task"])
        else:
            day_name = (today - timedelta(days=i)).strftime("%a")
            report += f"  ⬜ {day_name} {date}: No data\n"

    avg_rate = sum(daily_scores) / len(daily_scores) if daily_scores else 0
    report += f"\nWeek average: {avg_rate*100:.0f}%\n"
    report += f"Current streak: {scores.get('current_streak', 0)} days\n"
    report += f"Best streak: {scores.get('best_streak', 0)} days\n"

    report += f"\n✅ Shipped ({len(all_shipped)}):\n"
    for s in all_shipped[:10]:
        report += f"  • {s}\n"

    if all_missed:
        report += f"\n❌ Missed ({len(all_missed)}):\n"
        for m in all_missed[:10]:
            report += f"  • {m}\n"

    # Overall assessment
    report += "\n"
    if avg_rate >= 0.8:
        report += "🟢 Overall: Strong week. Keep this up."
    elif avg_rate >= 0.6:
        report += "🟡 Overall: Decent but inconsistent. Identify what's causing the drops."
    elif avg_rate >= 0.4:
        report += "🟠 Overall: Below target. Need to either reduce commitments or increase execution."
    else:
        report += "🔴 Overall: Critical. Less than half of commitments met. Time for an honest conversation about priorities."

    return report


def main():
    parser = argparse.ArgumentParser(description="Internal accountability reports")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("daily", help="Generate daily report")
    sub.add_parser("weekly", help="Generate weekly scorecard")

    args = parser.parse_args()

    if args.command == "daily":
        print(generate_daily_report())
    elif args.command == "weekly":
        print(generate_weekly_report())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
