#!/usr/bin/env python3
"""
Twitter/X adapter — posts tweets via API v2.
Requires: TWITTER_BEARER_TOKEN, TWITTER_API_KEY, TWITTER_API_SECRET,
          TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET in environment or config.

Usage:
  python3 twitter.py --text "Your tweet here"
  python3 twitter.py --text "Thread part 1" --thread "Thread part 2" --thread "Thread part 3"
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    import tweepy
    HAS_TWEEPY = True
except ImportError:
    HAS_TWEEPY = False


def load_config():
    """Load Twitter credentials from env, .bashrc, or config file."""
    config_path = Path(__file__).resolve().parent.parent / "config.yaml"

    # Try env first, fall back to parsing .bashrc (non-interactive shells skip exports)
    def get_env_or_bashrc(key):
        val = os.environ.get(key, "")
        if not val:
            bashrc = Path.home() / ".bashrc"
            try:
                for line in bashrc.read_text().splitlines():
                    if key in line and "export" in line:
                        val = line.split('"')[1] if '"' in line else ""
                        break
            except Exception:
                pass
        return val

    creds = {
        "api_key": get_env_or_bashrc("TWITTER_API_KEY"),
        "api_secret": get_env_or_bashrc("TWITTER_API_SECRET"),
        "access_token": get_env_or_bashrc("TWITTER_ACCESS_TOKEN"),
        "access_secret": get_env_or_bashrc("TWITTER_ACCESS_SECRET"),
        "bearer_token": get_env_or_bashrc("TWITTER_BEARER_TOKEN"),
    }

    # Try config file if env vars missing
    if not creds["api_key"] and config_path.exists():
        try:
            import yaml
            with open(config_path) as f:
                cfg = yaml.safe_load(f)
            twitter_cfg = cfg.get("publishing", {}).get("twitter", {})
            for key in creds:
                if not creds[key]:
                    creds[key] = twitter_cfg.get(key, "")
        except Exception:
            pass

    return creds


def post_tweet(text, reply_to=None):
    """Post a single tweet. Returns tweet ID."""
    if not HAS_TWEEPY:
        print("ERROR: tweepy not installed. Run: pip install tweepy", file=sys.stderr)
        sys.exit(1)

    creds = load_config()
    if not creds["api_key"] or not creds["access_token"]:
        print("ERROR: Twitter credentials not configured.", file=sys.stderr)
        print("Set TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET", file=sys.stderr)
        sys.exit(1)

    client = tweepy.Client(
        bearer_token=creds["bearer_token"],
        consumer_key=creds["api_key"],
        consumer_secret=creds["api_secret"],
        access_token=creds["access_token"],
        access_token_secret=creds["access_secret"],
    )

    kwargs = {"text": text}
    if reply_to:
        kwargs["in_reply_to_tweet_id"] = reply_to

    response = client.create_tweet(**kwargs)
    tweet_id = response.data["id"]
    print(f"✅ Posted tweet {tweet_id}")
    return tweet_id


def post_thread(texts):
    """Post a thread (list of texts). Each replies to the previous."""
    prev_id = None
    for i, text in enumerate(texts):
        prev_id = post_tweet(text, reply_to=prev_id)
        print(f"  Thread {i+1}/{len(texts)} posted")
    return prev_id


def main():
    parser = argparse.ArgumentParser(description="Post to Twitter/X")
    parser.add_argument("--text", required=True, help="Tweet text")
    parser.add_argument("--thread", action="append", help="Additional thread tweets")
    parser.add_argument("--dry-run", action="store_true", help="Print without posting")

    args = parser.parse_args()

    if args.dry_run:
        print(f"[DRY RUN] Tweet:\n{args.text}")
        if args.thread:
            for i, t in enumerate(args.thread):
                print(f"[DRY RUN] Thread {i+2}:\n{t}")
        return

    if args.thread:
        texts = [args.text] + args.thread
        post_thread(texts)
    else:
        post_tweet(args.text)


if __name__ == "__main__":
    main()
