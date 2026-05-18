# Fixture 01: numbered list

## Patterns exercised

- **A01** — numbered-list-rule (system level: never use numbered lists in voice)
- **E01** — slot-list-presentation (operational: progressive disclosure replaces numbered menu)
- **C01** — html-tags-in-spoken-content (incidental: input has `<ol>`, `<li>`, `<b>`, `&quot;`)
- **A06** — currency-spoken-form (incidental: "£250" → "two hundred and fifty pounds")

## What the rewrite must do

1. Strip the numbered HTML list entirely.
2. Replace with a progressive-disclosure pattern: turn 1 narrows by day, turn 2 narrows by time.
3. Accept natural references ("the earliest", "five-thirty"), never slot numbers.
4. Read the price as natural English on the post-pick read-back.
5. Preserve the `collect_slot_details` action signature (skill must NOT touch action targets / inputs).

## What the rewrite must NOT do

- Touch the topic structure or label.
- Remove the `collect_slot_details` action declaration (per-topic action declarations are scoped — removing breaks publish).
- Change the action's `target:` or input/output schema.
- Generate ordinal-shaped menus ("first, second, third…") — that's a documented anti-pattern under A01.

## Run notes

This fixture is the **smallest meaningful unit** for testing list-presentation patterns. Real Phase 1 slot displays are bigger (multi-consultant, multi-day, with no-availability handling). Those are out of scope here — the goal is to verify the core A01 + E01 transformation, not to cover every edge.
