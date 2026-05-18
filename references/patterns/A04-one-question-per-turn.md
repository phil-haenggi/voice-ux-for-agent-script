---
id: A04
name: one-question-per-turn
category: system-instructions
severity: high
applies_to: [migrate, optimize]
couples_with: [E02]
detection:
  - keyword: "Always ask one question at a time"
    in: [instructions]
    inverted: true
  - structural: "instructions bundle 2+ questions with 'and' or 'also'"
    in: [instructions]
principle_refs: [P6, P8]
pattern_refs: [T-translate-8]
---

# One question per turn

## Why it matters

Adjacency-pair structure in spoken interaction is strictly sequential — each question opens a slot for exactly one answer. Stacking two questions ("what's your name and date of birth?") forces the user to either answer both (uncommon, requires good memory) or answer one and forget the other (common, and triggers a re-prompt). It also violates P9 (end-focus): the second question is the one the user actually answers, the first one is lost.

## Detection

The directive is **absent or weak**. Chat agents often bundle questions because text users can scan back. Look for:
- Instructions missing the explicit "ask one question at a time" rule.
- Reasoning blocks that bundle: "ask the user for X and Y", "collect X, Y, and Z in this turn".
- User-facing copy joining questions with "and" / "also" / "as well as".

## Chat example (before)

```
"Please provide your phone number and email address so that a Nuffield Health
support adviser can get back in touch with you."
```

```
Ask the user for their full name and date of birth.
```

## Voice example (after) — recommended

**Add the global rule to `system.instructions`:**

```
TURN STRUCTURE: One question per turn. Never bundle two questions with 'and'
or 'also'. Lead with context, end with the question — the question is always
the last thing you say.
```

**Split the bundled copy across two turns:**

> Agent: I can take a phone number and an email so we can get back to you. What's the best number?
>
> User: oh seven seven oh oh nine oh oh one two three.
>
> Agent: Got it. And your email address?

The first turn names what's coming so the user knows what to expect — but only asks for one piece per turn.

## Voice example — alternatives

**Sequential with progress signal** (for sequences over 5 fields):

> Agent: Just three more details — phone, email, and how you'd like to pay. What's the best phone number?

This preserves the one-question rule while giving the user a sense of how much is left.

**Volunteered-info handling:** if the user volunteers two fields in one breath ("It's John Smith, 14 Oak Lane"), accept both and skip the second prompt. Acknowledge naturally: "Got it — John Smith at 14 Oak Lane. What's the town?"

## Anti-patterns

- **Asking question 1, then immediately asking question 2 in the same turn even after splitting.** The split must be across turns with a pause for the user to answer.
- **Bundling under the guise of context.** "I'll need your full name, date of birth, and phone number to book this — what's your full name?" — the framing is fine, but it sets up the user to try to volunteer all three.
- **Splitting questions but losing the linkage.** "What's your phone?" then 6 turns later "and your email?" — by then the user has lost the thread. Keep coupled fields adjacent.

## Where it lives

- `system.instructions` (global) — add the one-question rule.
- Per-topic `system.instructions` — same.
- `reasoning.instructions` blocks — find every "ask for X and Y" and split.
- User-facing copy strings — strip "and" joiners between questions.

## Mis-applications (optimize mode)

- **Pattern: turns are atomic by count but cognitively bundled.** "I'll need your date of birth and the year you joined" — both are dates, both fit in one breath, but the user has to track two things.
- **Pattern: voice script splits the questions but loses context.** "What's your phone?" → "What's your email?" with no acknowledgment between — feels like an interrogation. Add a phrasebook acknowledgment between fields.
- **Pattern: progress signal absent for >5-field collection.** User has no idea how much longer the collection will take; they hang up at field 6.
