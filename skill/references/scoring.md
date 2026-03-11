# Scoring System

## Daily Score

```
rate = completed / total_commitments
```

| Rate | Label | Emoji | Streak Impact |
|------|-------|-------|---------------|
| 100% | Perfect | ✅ | +1 streak |
| 80-99% | Good | ✅ | +1 streak |
| 70-79% | Decent | 🟡 | +1 streak |
| 50-69% | Below target | 🟡 | Resets streak |
| 1-49% | Bad | 🔴 | Resets streak |
| 0% | Zero day | 🔴 | Resets streak |

## Streaks

A **streak** is consecutive days with ≥70% completion.

- **Current streak:** Days in a row at ≥70%
- **Best streak:** All-time record
- **Streak direction:** `up` (>2 days), `flat` (1-2 days), `down` (0 days)

Streaks are motivating. Breaking one should feel like losing something.

## Weekly Rate

```
weekly_rate = total_completed_this_week / total_committed_this_week
```

Weekly rate matters more than any single day. One bad day in a good week is fine. Five mediocre days is a problem.

## Trend Detection

Compare current week to previous week:

| Change | Label |
|--------|-------|
| +10% or more | 📈 Improving |
| -5% to +10% | ➡️ Steady |
| -10% to -5% | 📉 Slipping |
| -10% or worse | 🚨 Declining |

## Escalation Thresholds

| Trigger | Action |
|---------|--------|
| 1 day <50% | Honest post, no escalation |
| 2 days <50% | Post mentions "becoming a pattern" |
| 3 days <50% | DM accountability partner |
| 5 days <50% | Weekly post highlights the slump |
| 7 days <50% | Request hard conversation / priority reset |

## Commitment Quality Rules

To prevent gaming the system:

1. **Minimum 2 commitments per day** — you can't score 100% on 1 easy task
2. **Maximum 5 commitments per day** — you can't dilute with trivial items
3. **At least 1 must be a "hard" task** — something you'd rather avoid
4. **No retroactive additions** — can't add a task after doing it just to boost score
5. **Commitments set by 10:30 AM** — after that, it's a zero-commitment day (which gets posted)
