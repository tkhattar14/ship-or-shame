# Ship or Shame 🚢🔴

> Founders without investors have no one to answer to. That's freedom — and it's the most common reason startups die slowly.

**An AI that publicly posts whether you shipped or not. Every day. No veto. No hiding.**

## What It Does

```
COMMIT → TRACK → SCORE → PUBLISH → ESCALATE
```

1. **Every morning**, the AI asks: "What are your 3 commitments today?"
2. **Throughout the day**, it tracks progress (optionally from Trello, GitHub, etc.)
3. **Every evening**, it scores your day: done or not done
4. **Then it posts the truth** to Twitter/X — good days AND bad days
5. **If you slip repeatedly**, it escalates to your accountability partner

## Why

- Private to-do lists have zero social pressure
- Productivity apps don't create consequences
- An AI can't be sweet-talked into letting you off the hook
- Public commitment is the strongest forcing function that doesn't involve money

## The No-Veto Default

The recommended configuration is **no veto** — the AI posts without your approval.

This is uncomfortable. That's the point.

If you can kill uncomfortable posts, you'll kill exactly the ones that create accountability.

## How It Works

Built as an [OpenClaw](https://github.com/openclaw/openclaw) skill, but the scripts work standalone too.

```
accountability-engine/
├── skill/                 # OpenClaw skill (SKILL.md + scripts)
│   ├── SKILL.md           # Agent instructions
│   ├── scripts/
│   │   ├── commit.py      # Record & manage daily commitments
│   │   ├── track.py       # Score computation, streaks, trends
│   │   ├── publish.py     # Generate & post updates
│   │   └── report.py      # Internal reports (not public)
│   └── references/
│       ├── post-templates.md
│       └── scoring.md
├── adapters/
│   ├── twitter.py         # Twitter/X posting
│   └── markdown.py        # Local markdown output (fallback/blog)
├── config.example.yaml    # Configuration template
├── examples/              # Real configs from real founders
└── docs/
    ├── philosophy.md      # Why this exists
    ├── setup.md           # Getting started
    └── customization.md   # Adapting for your use case
```

## Quick Start

```bash
# 1. Configure
cp config.example.yaml config.yaml
# Edit config.yaml with your details

# 2. Record commitments
python3 skill/scripts/commit.py add --task "Ship the landing page update" --category product
python3 skill/scripts/commit.py add --task "Record demo video" --category marketing
python3 skill/scripts/commit.py add --task "Review Q1 financials" --category ops

# 3. Mark completions
python3 skill/scripts/commit.py done --id 1

# 4. End of day
python3 skill/scripts/commit.py eod

# 5. Publish
python3 skill/scripts/publish.py post --type daily
```

## What Posts Look Like

**Good day:**
> Day 15: 3/3 ✅
> • Shipped the payment verification fix
> • Recorded 60s demo footage for ads
> • Reviewed and approved marketing copy
>
> 🔥 Streak: 5 days

**Bad day:**
> Day 18: 0/3 🔴
>
> Committed to recording demo footage (day 11 overdue), fixing the checkout flow, and reviewing the pitch deck.
>
> Did none of them. No excuse. Just didn't do it.
>
> This is day 3 below 50%. Pattern, not a blip.

## Designed For

- **Solo founders** with no board or investors (primary use case)
- **Indie hackers** building in public
- **Small teams** who want transparent execution tracking
- **Anyone** who needs external accountability and is willing to be honest about it

## Built By

Created by [Tushar](https://github.com/tkhattar14) and [Ted](https://github.com/tkhattar14) (his AI cofounder) at [Once Upon Me](https://onceuponme.co) — because they needed it themselves.

This is the system we actually use. Our config is in `examples/tushar-config.yaml`. Our posts are real.

## Contributing

This is open source because accountability should be accessible to everyone. PRs welcome for:
- New platform adapters (LinkedIn, Mastodon, Bluesky, Slack)
- New data source integrations (Linear, Notion, Asana, GitHub Issues)
- Improved scoring algorithms
- Better post generation
- Documentation and examples

## Origin Story

Built by [Tushar](https://github.com/tkhattar14) and Ted (his AI cofounder) at [Once Upon Me](https://onceuponme.co) because Tushar kept missing deadlines and nothing happened. So he gave his AI cofounder a Twitter account and said "post the truth — no veto."

This repo is the system. Our config is real. Our posts are real. The shame is real.

## License

MIT — use it, fork it, hold yourself accountable.

---

*Ship or shame. There is no third option.*
