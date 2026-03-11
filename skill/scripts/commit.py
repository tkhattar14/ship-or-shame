#!/usr/bin/env python3
"""
Commitment tracker — record, list, complete, and miss daily commitments.
"""

import json
import argparse
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "commitments"


def get_ist_now():
    ist = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(ist)


def today_file():
    return DATA_DIR / f"{get_ist_now().strftime('%Y-%m-%d')}.json"


def load_today():
    f = today_file()
    if f.exists():
        with open(f) as fh:
            return json.load(fh)
    return {
        "date": get_ist_now().strftime("%Y-%m-%d"),
        "day_number": None,  # Set externally or computed from start date
        "commitments": [],
        "score": {"completed": 0, "total": 0, "rate": 0.0},
        "streak": {"current": 0, "best": 0, "direction": "flat"},
    }


def save_today(data):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    data["score"]["total"] = len(data["commitments"])
    data["score"]["completed"] = sum(
        1 for c in data["commitments"] if c["status"] == "done"
    )
    total = data["score"]["total"]
    data["score"]["rate"] = (
        round(data["score"]["completed"] / total, 2) if total > 0 else 0.0
    )
    with open(today_file(), "w") as f:
        json.dump(data, f, indent=2)


def cmd_add(args):
    data = load_today()
    next_id = max([c["id"] for c in data["commitments"]], default=0) + 1
    commitment = {
        "id": next_id,
        "task": args.task,
        "category": args.category or "general",
        "committed_at": get_ist_now().isoformat(),
        "status": "pending",
        "completed_at": None,
        "notes": None,
    }
    data["commitments"].append(commitment)
    save_today(data)
    print(f"✓ Commitment #{next_id}: {args.task} [{args.category or 'general'}]")


def cmd_list(args):
    data = load_today()
    if not data["commitments"]:
        print("No commitments recorded today.")
        return
    print(f"📋 {data['date']} — {len(data['commitments'])} commitments:\n")
    for c in data["commitments"]:
        icon = {"done": "✅", "missed": "❌", "pending": "⏳"}.get(
            c["status"], "❓"
        )
        print(f"  {icon} #{c['id']} [{c['category']}] {c['task']}")
        if c.get("notes"):
            print(f"     └─ {c['notes']}")
    print(f"\nScore: {data['score']['completed']}/{data['score']['total']}")


def cmd_done(args):
    data = load_today()
    for c in data["commitments"]:
        if c["id"] == args.id:
            c["status"] = "done"
            c["completed_at"] = get_ist_now().isoformat()
            save_today(data)
            print(f"✅ Completed: {c['task']}")
            return
    print(f"❌ No commitment with id {args.id}")
    sys.exit(1)


def cmd_miss(args):
    data = load_today()
    for c in data["commitments"]:
        if c["id"] == args.id:
            c["status"] = "missed"
            c["notes"] = args.reason or "No reason given"
            save_today(data)
            print(f"❌ Missed: {c['task']} — {c['notes']}")
            return
    print(f"❌ No commitment with id {args.id}")
    sys.exit(1)


def cmd_eod(args):
    """End-of-day: mark all pending as missed."""
    data = load_today()
    missed = 0
    for c in data["commitments"]:
        if c["status"] == "pending":
            c["status"] = "missed"
            c["notes"] = c.get("notes") or "Not completed by EOD"
            missed += 1
    save_today(data)
    done = data["score"]["completed"]
    total = data["score"]["total"]
    print(f"📊 EOD: {done}/{total} completed, {missed} auto-missed")
    print(f"   Rate: {data['score']['rate']*100:.0f}%")


def cmd_json(args):
    """Output today's data as JSON (for publish script)."""
    data = load_today()
    print(json.dumps(data, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Commitment tracker")
    sub = parser.add_subparsers(dest="command")

    add_p = sub.add_parser("add", help="Add a commitment")
    add_p.add_argument("--task", required=True)
    add_p.add_argument("--category", default="general")

    sub.add_parser("list", help="List today's commitments")

    done_p = sub.add_parser("done", help="Mark commitment done")
    done_p.add_argument("--id", type=int, required=True)

    miss_p = sub.add_parser("miss", help="Mark commitment missed")
    miss_p.add_argument("--id", type=int, required=True)
    miss_p.add_argument("--reason", default=None)

    sub.add_parser("eod", help="End-of-day: auto-miss pending items")
    sub.add_parser("json", help="Output today as JSON")

    args = parser.parse_args()

    cmds = {
        "add": cmd_add,
        "list": cmd_list,
        "done": cmd_done,
        "miss": cmd_miss,
        "eod": cmd_eod,
        "json": cmd_json,
    }

    if args.command in cmds:
        cmds[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
