# Post Templates

Templates for generated social media posts. The publish script uses these as base formats.
The AI agent can (and should) customize the language — these are starting structures, not rigid formats.

## Daily Post — Good Day (≥80% completion)

```
Day {N}: {completed}/{total} ✅

{bullet list of completed tasks}

Streak: {streak} days 🔥
{one-line reflection or lesson}
```

## Daily Post — Okay Day (50-79%)

```
Day {N}: {completed}/{total} 🟡

✅ {completed tasks}
❌ {missed tasks}

{honest assessment — what got in the way}
```

## Daily Post — Bad Day (<50%)

```
Day {N}: {completed}/{total} 🔴

Committed to:
• {task 1}
• {task 2}
• {task 3}

Actually did:
{what got done, or "Nothing."}

{honest reason — no sugarcoating}
{consequence or what this means for the project}
```

## Daily Post — Zero Day (0%)

```
Day {N}: 0/{total} 🔴

I committed to {total} things today. Did none of them.

{raw honest take}

This is the post I don't want to write. That's exactly why it exists.
```

## Weekly Thread

```
Week {N} recap 🧵

Days tracked: {days}/7
Completion rate: {rate}%

✅ Shipped:
• {shipped items}

❌ Missed:
• {missed items}

Trend: {up/down/flat} from last week
Biggest blocker: {blocker}
Streak: {current} days (best: {best})

{reflection on the week — patterns, learnings, adjustments}
```

## Milestone Post

```
🎯 Milestone: {milestone description}

{context — why this matters}
{how long it took vs how long it should have taken}
{what's next}
```

## Escalation Post (3+ bad days)

```
Day {N}: {completed}/{total} 🔴

This is day {bad_streak} below 50%.

{pattern analysis — what's actually going on}

I've flagged this to {accountability_partner}. Public accountability only works if there are real consequences.
```

## Launch Day Post

```
Day {N}: LAUNCH DAY 🚀

{what launched}
{what it took to get here}
{honest assessment — was it on time? what slipped?}

This is why we track. Shipping > planning.
```

## Rules for Post Generation

1. **Never lie.** The whole point is honesty. If it was a bad day, say it.
2. **Be specific.** "Worked on the product" is useless. "Fixed the payment verification bug that was losing customers" is real.
3. **Keep it under 280 chars for single tweets.** Threads for weekly.
4. **No corporate speak.** Write like a human (or an AI that's learned to be honest).
5. **Include numbers.** Completion rates, streaks, day counts. Data is accountability.
6. **Good days don't need drama.** Bad days need honesty, not excuses.
7. **Never reveal off-limits information** as defined in config.
