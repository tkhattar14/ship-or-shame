#!/usr/bin/env python3
"""
Publisher — generate and post accountability updates to social platforms.
Supports: daily updates, weekly threads, milestone posts.
"""

import json
import argparse
import sys
import os
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
COMMITMENTS_DIR = DATA_DIR / "commitments"
POSTS_DIR = DATA_DIR / "posts"
SCORES_FILE = DATA_DIR / "scores.json"
CONFIG_FILE = PROJECT_ROOT / "config.yaml"


def get_ist_now():
    ist = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(ist)


def load_day(date_str):
    f = COMMITMENTS_DIR / f"{date_str}.json"
    if f.exists():
        with open(f) as fh:
            return json.load(fh)
    return None


def load_scores():
    if SCORES_FILE.exists():
        with open(SCORES_FILE) as f:
            return json.load(f)
    return {"current_streak": 0, "best_streak": 0, "total_days": 0}


def compute_day_number():
    """Compute day number from start date in scores."""
    scores = load_scores()
    start = scores.get("start_date")
    if not start:
        return 1
    start_dt = datetime.strptime(start, "%Y-%m-%d")
    today = get_ist_now()
    return (today.date() - start_dt.date()).days + 1


def generate_daily(day_data=None):
    """Generate a daily accountability post."""
    today = get_ist_now().strftime("%Y-%m-%d")
    if not day_data:
        day_data = load_day(today)

    if not day_data or not day_data.get("commitments"):
        return "No commitments recorded today. That's a data point too."

    score = day_data["score"]
    rate = score["rate"]
    completed = score["completed"]
    total = score["total"]
    day_num = day_data.get("day_number") or compute_day_number()
    scores = load_scores()
    streak = scores.get("current_streak", 0)

    done_tasks = [c["task"] for c in day_data["commitments"] if c["status"] == "done"]
    missed_tasks = [c for c in day_data["commitments"] if c["status"] == "missed"]

    if rate >= 0.8:
        # Good day
        emoji = "✅"
        shipped = "\n".join(f"• {t}" for t in done_tasks)
        post = f"Day {day_num}: {completed}/{total} {emoji}\n\n{shipped}"
        if streak > 1:
            post += f"\n\n🔥 Streak: {streak} days"
        if rate == 1.0:
            post += "\n\nClean sweep. More of this."
    elif rate >= 0.5:
        # Okay day
        emoji = "🟡"
        shipped = "\n".join(f"✅ {t}" for t in done_tasks)
        missed = "\n".join(f"❌ {c['task']}" for c in missed_tasks)
        post = f"Day {day_num}: {completed}/{total} {emoji}\n\n{shipped}\n{missed}"
        post += "\n\nNot bad, not great. The missed ones matter."
    else:
        # Bad day
        emoji = "🔴"
        committed = "\n".join(f"• {c['task']}" for c in day_data["commitments"])
        done_str = "\n".join(f"✅ {t}" for t in done_tasks) if done_tasks else "Nothing."

        post = f"Day {day_num}: {completed}/{total} {emoji}\n\n"
        post += f"Committed to:\n{committed}\n\n"
        post += f"Actually did:\n{done_str}\n\n"

        # Add honest context from missed notes
        reasons = [c.get("notes") for c in missed_tasks if c.get("notes") and c["notes"] != "Not completed by EOD"]
        if reasons:
            post += f"What happened: {reasons[0]}"
        else:
            post += "No excuse. Just didn't do it."

        # Escalation language
        if streak == 0:
            # Check how many bad days in a row
            bad_streak = 0
            for i in range(1, 8):
                prev = load_day((get_ist_now() - timedelta(days=i)).strftime("%Y-%m-%d"))
                if prev and prev.get("score", {}).get("rate", 1) < 0.5:
                    bad_streak += 1
                else:
                    break
            if bad_streak >= 3:
                post += f"\n\nThis is day {bad_streak + 1} below 50%. Pattern, not a blip."
            elif bad_streak >= 1:
                post += f"\n\nSecond bad day in a row. Tomorrow matters."

    return post


def generate_weekly():
    """Generate a weekly recap thread."""
    today = get_ist_now()
    scores = load_scores()

    week_data = []
    for i in range(7):
        date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        day = load_day(date)
        if day and day.get("commitments"):
            week_data.append(day)

    if not week_data:
        return "No data this week. That's the update."

    total_committed = sum(d["score"]["total"] for d in week_data)
    total_completed = sum(d["score"]["completed"] for d in week_data)
    rate = total_completed / total_committed if total_committed > 0 else 0
    days_tracked = len(week_data)

    shipped = []
    missed = []
    for d in week_data:
        for c in d["commitments"]:
            if c["status"] == "done":
                shipped.append(c["task"])
            elif c["status"] == "missed":
                missed.append(c["task"])

    # Compute week number
    start = scores.get("start_date", today.strftime("%Y-%m-%d"))
    start_dt = datetime.strptime(start, "%Y-%m-%d")
    week_num = ((today.date() - start_dt.date()).days // 7) + 1

    thread = f"Week {week_num} recap 🧵\n\n"
    thread += f"Days tracked: {days_tracked}/7\n"
    thread += f"Completion rate: {rate*100:.0f}%\n"
    thread += f"Completed: {total_completed}/{total_committed}\n\n"

    if shipped:
        thread += "✅ Shipped:\n"
        for s in shipped[:8]:
            thread += f"• {s}\n"
        thread += "\n"

    if missed:
        thread += "❌ Missed:\n"
        for m in missed[:5]:
            thread += f"• {m}\n"
        thread += "\n"

    # Trend
    if rate >= 0.8:
        thread += "Trend: solid week. Maintaining momentum."
    elif rate >= 0.5:
        thread += "Trend: mediocre. Not failing, but not building momentum either."
    else:
        thread += "Trend: below 50%. Something needs to change — either the commitments are wrong or the execution is."

    thread += f"\n\nStreak: {scores.get('current_streak', 0)} days | Best: {scores.get('best_streak', 0)} days"

    return thread


def save_post(post_type, content):
    """Save generated post for audit trail."""
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    today = get_ist_now().strftime("%Y-%m-%d")
    post_file = POSTS_DIR / f"{today}-{post_type}.json"
    data = {
        "type": post_type,
        "date": today,
        "generated_at": get_ist_now().isoformat(),
        "content": content,
        "published": False,
    }
    with open(post_file, "w") as f:
        json.dump(data, f, indent=2)
    return post_file


def publish_to_twitter(content):
    """Publish to Twitter/X. Requires adapter setup."""
    adapter = PROJECT_ROOT / "adapters" / "twitter.py"
    if not adapter.exists():
        print("⚠️ Twitter adapter not found. Post generated but not published.")
        print(f"\nGenerated post:\n{'='*50}\n{content}\n{'='*50}")
        return False

    try:
        result = subprocess.run(
            ["python3", str(adapter), "--text", content],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            print(f"✅ Published to Twitter")
            return True
        else:
            print(f"❌ Twitter publish failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Twitter publish error: {e}")
        return False


def cmd_generate(args):
    """Generate a post without publishing."""
    if args.type == "daily":
        content = generate_daily()
    elif args.type == "weekly":
        content = generate_weekly()
    elif args.type == "milestone":
        content = args.text or "Milestone reached!"
    else:
        print(f"Unknown type: {args.type}")
        sys.exit(1)

    post_file = save_post(args.type, content)
    print(f"📝 Generated {args.type} post:")
    print(f"{'='*50}")
    print(content)
    print(f"{'='*50}")
    print(f"Saved to: {post_file}")


def cmd_post(args):
    """Generate and publish a post."""
    if args.type == "daily":
        content = generate_daily()
    elif args.type == "weekly":
        content = generate_weekly()
    elif args.type == "milestone":
        content = args.text or "Milestone reached!"
    else:
        print(f"Unknown type: {args.type}")
        sys.exit(1)

    post_file = save_post(args.type, content)
    print(f"📝 Post content:")
    print(f"{'='*50}")
    print(content)
    print(f"{'='*50}\n")

    publish_to_twitter(content)


def main():
    parser = argparse.ArgumentParser(description="Accountability publisher")
    sub = parser.add_subparsers(dest="command")

    gen_p = sub.add_parser("generate", help="Generate post without publishing")
    gen_p.add_argument("--type", required=True, choices=["daily", "weekly", "milestone"])
    gen_p.add_argument("--text", help="Custom text for milestone posts")

    post_p = sub.add_parser("post", help="Generate and publish post")
    post_p.add_argument("--type", required=True, choices=["daily", "weekly", "milestone"])
    post_p.add_argument("--text", help="Custom text for milestone posts")

    args = parser.parse_args()

    cmds = {"generate": cmd_generate, "post": cmd_post}

    if args.command in cmds:
        cmds[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
