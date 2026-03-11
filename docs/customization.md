# Customization Guide

## Tone Presets

### `honest-and-direct` (default)
States facts. Calls out failures without cruelty. Celebrates wins without hype.
> Day 12: 1/3 🔴. Committed to fixing the payment bug, recording demo footage, and reviewing the pitch deck. Only finished the pitch deck review. Demo footage has been pending for 11 days. That's a pattern.

### `encouraging-but-real`
Acknowledges struggles while being honest. Better for people who shut down under harsh feedback.
> Day 12: 1/3 🟡. Got the pitch deck review done — that's progress. The payment bug and demo footage didn't happen today. The demo footage has been a recurring miss — worth asking why it keeps sliding.

### `brutal`
Maximum shame. No softening. For people who specifically want to be called out hard.
> Day 12: 1/3. Failed. Again. Demo footage: 11 days overdue. At this point you're not "busy" — you're avoiding it. Ship it tomorrow or admit you're not going to.

## Adapting for Different Roles

### Solo Founder (default)
- 3 commitments/day
- Public posting on Twitter
- Escalation to accountability partner
- Full autonomy over commitment selection

### Employee / Team Member
- Commitments pulled from sprint/kanban board
- Posts to team Slack channel instead of Twitter
- Escalation to manager
- Weekly report to team lead

### Creator / Content Maker
- Commitments focused on publishing (write, record, edit, post)
- Posts to the same platform as the content (meta-accountability)
- Streak emphasis (consistency matters more for creators)

### Student
- Commitments from syllabus / assignment tracker
- Posts to study group or accountability buddy
- Escalation to study partner

## Adding Platform Adapters

Create a new file in `adapters/`:

```python
#!/usr/bin/env python3
"""
{Platform} adapter
"""

def post(text, **kwargs):
    """Post text to {platform}. Returns post ID or URL."""
    # Your implementation here
    pass

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    args = parser.parse_args()
    post(args.text)
```

Then add the platform name to `publishing.platforms` in config.

## Adding Data Sources

Data sources auto-detect completions from external tools. To add one:

1. Write a function in `track.py` that checks the external source
2. Match external items to today's commitments by keyword or ID
3. Auto-mark matches as `done`

Example: GitHub adapter could check for merged PRs matching commitment descriptions.

## Off-Limits Configuration

The `off_limits` list in config defines topics that must never appear in public posts. The publish script checks generated content against these rules.

Common off-limits topics:
- `customer_names` — never name customers publicly
- `exact_revenue_numbers` — use ranges ("crossed ₹X") or percentages
- `personal_life` — keep it professional
- `other_people_without_consent` — don't name team members without asking
- `security_credentials` — obvious but worth stating
- `legal_matters` — anything under NDA or legal review

## Scoring Customization

Edit `skill/references/scoring.md` to adjust:
- Streak threshold (default: 70%)
- Escalation thresholds
- Commitment count limits
- Gaming prevention rules
