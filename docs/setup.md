# Setup Guide

## Prerequisites

- **OpenClaw** running on any machine (Pi, VPS, laptop)
- **Python 3.9+** for scripts
- **Twitter/X Developer Account** (for public posting — optional, can start with markdown output)

## Quick Start

### 1. Copy the config

```bash
cp config.example.yaml config.yaml
```

Edit `config.yaml` with your details:
- Your name and timezone
- Accountability partner (if any)
- Veto preference (recommend: `false`)
- Twitter credentials (if posting publicly)

### 2. Install the skill

The `skill/` directory is an OpenClaw skill. Either:

**Option A:** Copy to your OpenClaw skills directory:
```bash
cp -r skill/ ~/.openclaw/workspace/skills/accountability-engine/
```

**Option B:** Add this repo's `skill/` to your OpenClaw config's `skills.load.extraDirs`.

### 3. Install dependencies

```bash
pip install tweepy pyyaml  # For Twitter posting
```

### 4. Set up cron jobs

In OpenClaw, create these cron jobs:

**Morning Ask (10:00 AM local):**
```
Task: "Ask the human for today's 3 commitments using the accountability-engine skill. Record them with commit.py."
Schedule: Daily at 10:00
Session: isolated agentTurn
Delivery: announce to chat
```

**EOD Review (9:00 PM local):**
```
Task: "Run end-of-day review using accountability-engine. Mark pending items as missed. Score the day. Generate and publish the daily post."
Schedule: Daily at 21:00
Session: isolated agentTurn
Delivery: announce to chat
```

**Weekly Review (Sunday 8:00 PM local):**
```
Task: "Generate weekly accountability report and thread using accountability-engine. Publish to Twitter. Send internal report to accountability partner."
Schedule: Sunday at 20:00
Session: isolated agentTurn
Delivery: announce to chat
```

### 5. Test it

```bash
# Record a test commitment
python3 skill/scripts/commit.py add --task "Test the accountability system" --category general

# Check the score
python3 skill/scripts/track.py score

# Generate a post (without publishing)
python3 skill/scripts/publish.py generate --type daily
```

### 6. Start Day 1

Tell your AI agent: "Let's start accountability. What are my 3 commitments today?"

## Without Twitter (Markdown Mode)

If you don't want to post publicly yet (or want to trial run):

1. Set `platforms: ["markdown"]` in config
2. Posts will be saved to `data/markdown-posts/` as `.md` files
3. You can manually post them, or use them as a blog

## Without OpenClaw

The scripts work standalone. You'd just need to:
1. Run `commit.py add` manually each morning
2. Run `commit.py done` when you complete things
3. Run `commit.py eod` at end of day
4. Run `publish.py post --type daily` to publish

The AI agent automation (asking you, nagging you, escalating) requires OpenClaw or a similar agent framework.

## File Structure After Setup

```
accountability-engine/
├── config.yaml           ← Your config
├── data/
│   ├── commitments/      ← Daily commitment files
│   │   ├── 2026-03-11.json
│   │   └── 2026-03-12.json
│   ├── scores.json       ← Running totals and streaks
│   ├── posts/            ← Generated posts (audit trail)
│   └── markdown-posts/   ← If using markdown adapter
├── skill/                ← OpenClaw skill
├── adapters/             ← Platform adapters
└── ...
```
