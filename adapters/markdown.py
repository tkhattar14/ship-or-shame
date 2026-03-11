#!/usr/bin/env python3
"""
Markdown adapter — saves posts as markdown files.
Useful as a fallback, blog source, or local accountability log.

Usage:
  python3 markdown.py --text "Post content" --type daily
"""

import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "markdown-posts"


def get_ist_now():
    ist = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(ist)


def save_post(text, post_type="daily"):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    now = get_ist_now()
    filename = f"{now.strftime('%Y-%m-%d')}-{post_type}.md"
    filepath = OUTPUT_DIR / filename

    content = f"---\ndate: {now.strftime('%Y-%m-%d')}\ntype: {post_type}\ngenerated: {now.isoformat()}\n---\n\n{text}\n"

    with open(filepath, "w") as f:
        f.write(content)

    print(f"✅ Saved to {filepath}")
    return filepath


def main():
    parser = argparse.ArgumentParser(description="Save post as markdown")
    parser.add_argument("--text", required=True)
    parser.add_argument("--type", default="daily", choices=["daily", "weekly", "milestone"])
    args = parser.parse_args()
    save_post(args.text, args.type)


if __name__ == "__main__":
    main()
