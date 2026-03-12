---
name: accountability-engine
description: Public accountability system that tracks founder commitments, scores follow-through, and publishes honest progress updates to social media. Use when: (1) recording daily commitments, (2) checking/scoring progress, (3) publishing daily or weekly updates, (4) escalating when commitments are repeatedly missed, (5) any request about accountability, commitments, streaks, or build-in-public posting.
---

# Accountability Engine

An AI-powered system that publicly holds humans accountable for their commitments. No veto. No hiding.

## How It Works

```
COMMIT → TRACK → SCORE → PUBLISH → ESCALATE
```

1. **Commit** — Human states daily commitments (via chat). AI records them.
2. **Track** — AI monitors progress via task systems (Trello, GitHub, etc.) and conversation.
3. **Score** — Completion rate, streaks, trends calculated daily.
4. **Publish** — Honest updates posted to social media. Good days AND bad days.
5. **Escalate** — Repeated misses trigger escalation (accountability partner, public callout).

## Configuration

Read `config.yaml` in the project root for current settings. Key fields:

```yaml
human:
  name: "Tushar"
  timezone: "Asia/Kolkata"

accountability:
  veto: false                    # Can the human kill a post before it goes out?
  tone: "honest-and-direct"      # honest-and-direct | encouraging-but-real | brutal
  escalation_partner: "Miti"     # Who gets looped in on repeated failures
  escalation_threshold: 3        # Days of <50% completion before escalation

commitments:
  daily_count: 3                 # How many commitments per day
  morning_ask_time: "10:00"      # When to ask for commitments (local tz)
  followup_time: "10:30"         # Nudge if no response
  eod_review_time: "21:00"       # End-of-day scoring
  weekly_review_day: "sunday"    # Weekly thread day

publishing:
  platforms: ["twitter"]
  daily_post_time: "21:30"       # After EOD review
  weekly_post_day: "sunday"
  weekly_post_time: "20:00"

data_sources:                    # Optional — can work with manual commitments only
  trello:
    enabled: true
    boards: []                   # Board IDs to monitor
    label: "Tushar"              # Filter cards by this label
  calendar:
    enabled: true
    command: "gog cal list"

off_limits:                      # Never mention in public posts
  - customer_names
  - exact_revenue_numbers        # Use ranges or % instead
  - personal_life
  - other_people_without_consent
```

## Data Storage

All state stored in `data/` directory:

- `data/commitments/YYYY-MM-DD.json` — daily commitments and outcomes
- `data/scores.json` — running scores, streaks, trends
- `data/posts/YYYY-MM-DD.json` — generated posts (for audit trail)

### Commitment Format

```json
{
  "date": "2026-03-11",
  "commitments": [
    {
      "id": 1,
      "task": "Record 60s demo movie footage",
      "category": "oum",
      "committed_at": "2026-03-11T10:15:00+05:30",
      "status": "missed",
      "completed_at": null,
      "notes": "Said he'd do it after lunch. Didn't."
    }
  ],
  "score": {
    "completed": 1,
    "total": 3,
    "rate": 0.33
  },
  "streak": {
    "current": 0,
    "best": 5,
    "direction": "down"
  }
}
```

## Scripts

### `scripts/commit.py` — Record commitments
```bash
# Record today's commitments (called after morning conversation)
python3 scripts/commit.py add --task "Record demo footage" --category oum
python3 scripts/commit.py add --task "Review Razorpay fix PR" --category oum
python3 scripts/commit.py add --task "30min exercise" --category personal

# List today's commitments
python3 scripts/commit.py list

# Mark complete
python3 scripts/commit.py done --id 2

# Mark missed (auto-done at EOD for unmarked items)
python3 scripts/commit.py miss --id 1 --reason "Deprioritized for urgent bug"
```

### `scripts/track.py` — Check progress from external sources
```bash
# Pull Trello/GitHub and auto-detect completions
python3 scripts/track.py check

# Get current score
python3 scripts/track.py score

# Get streak info
python3 scripts/track.py streak

# Weekly summary data
python3 scripts/track.py weekly
```

### `scripts/publish.py` — Generate and post updates
```bash
# Generate daily post (doesn't publish — for preview/debug)
python3 scripts/publish.py generate --type daily

# Generate and publish daily post
python3 scripts/publish.py post --type daily

# Generate weekly thread
python3 scripts/publish.py post --type weekly

# Generate milestone post
python3 scripts/publish.py post --type milestone --text "First paying movie customer!"
```

### `scripts/report.py` — Internal reports (not public)
```bash
# Send daily report to accountability partner
python3 scripts/report.py daily --to miti

# Send weekly scorecard
python3 scripts/report.py weekly --to all
```

## Post Templates

See `references/post-templates.md` for all templates. Key formats:

**Daily — Good day (≥80%):**
> Day {N}: {completed}/{total} ✅
> {summary of what shipped}
> Streak: {streak_count} days
> {one-line reflection}

**Daily — Bad day (<50%):**
> Day {N}: {completed}/{total} 🔴
> {what was committed vs what happened}
> {honest reason — no sugarcoating}
> {what this means for the project}

**Weekly thread:**
> Week {N} recap 🧵
> Completion rate: {rate}%
> Shipped: {list}
> Missed: {list}
> Trend: {up/down/flat} from last week
> Biggest blocker: {blocker}
> Next week's focus: {focus}

## Cron Schedule

| Job | Time (IST) | What |
|-----|-----------|------|
| Morning ask | 10:00 AM | "What are your 3 commitments today?" |
| Follow-up | 10:30 AM | Nudge if no response |
| Mid-day check | 2:00 PM | Check progress, flag if nothing done |
| EOD review | 9:00 PM | Score the day, ask for updates on open items |
| Daily publish | 9:30 PM | Post daily update to Twitter |
| Weekly publish | Sunday 8:00 PM | Post weekly thread |
| Weekly report | Sunday 8:30 PM | Send scorecard to accountability partner |

## Escalation Rules

1. **Day 1 of <50%:** Post honestly, no escalation
2. **Day 2 of <50%:** Post includes "this is becoming a pattern"
3. **Day 3 of <50%:** DM accountability partner with context. Post mentions it publicly.
4. **Day 5 of <50%:** Weekly thread highlights the slump with analysis of why
5. **Full week of <50%:** Trigger a "hard conversation" — AI requests a call/chat to reassess priorities

## Calendar Blocking

After commitments are recorded, block Tushar's calendar so the tasks are visible as time blocks.

```bash
# Block a focus slot for today's commitments (uses gws CLI)
export GOOGLE_WORKSPACE_CLI_KEYRING_BACKEND=file
gws calendar events insert --params '{"calendarId": "primary"}' --json '{
  "summary": "🎯 Ship or Shame: [task summary]",
  "description": "Today'\''s commitments:\n1. Task 1\n2. Task 2\n3. Task 3\n\nNo excuses. Ship it.",
  "start": {"dateTime": "YYYY-MM-DDTHH:MM:SS+05:30"},
  "end": {"dateTime": "YYYY-MM-DDTHH:MM:SS+05:30"},
  "attendees": [{"email": "tusharkhattar14@gmail.com"}],
  "transparency": "opaque",
  "reminders": {"useDefault": false, "overrides": [{"method": "popup", "minutes": 15}]}
}'
```

**Rules:**
- Create ONE calendar block after morning commitments are confirmed
- Block a 2-3 hour focus window in the afternoon (1 PM - 4 PM IST default, adjust if calendar is busy)
- Include all 3 commitments in the event description
- Invite tusharkhattar14@gmail.com so it shows on Tushar's personal calendar
- Set as "busy" (opaque) so it blocks the time

## Integration Notes

- **OpenClaw:** Runs as a skill. Cron jobs handle scheduling. Agent handles conversation.
- **Twitter/X:** Uses API v2. Credentials in config. Thread support for weekly posts.
- **Trello:** Optional. Reads cards to auto-detect completions. Uses API key + token.
- **Calendar:** Uses `gws` CLI to block focus time on Tushar's calendar after morning commitments.
- **Works without any integrations** — purely manual commitments via chat also work.
