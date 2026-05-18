---
id: F01
name: crisis-flow-no-hangup
category: crisis-and-safety
severity: high
applies_to: [migrate, optimize]
detection:
  - keyword: "self-harm"
    in: [instructions]
  - keyword: "suicidal"
    in: [instructions]
  - keyword: "Samaritans"
    in: [instructions, response_templates]
  - structural: "crisis topic ends conversation or transfers without latch"
    in: [instructions]
principle_refs: [P5, P9]
---

# Crisis flow — no hangup

## Why it matters

A caller in distress should not be hung up on. Chat agents often handle crisis topics by displaying a static support message and ending the session — fine on chat (the caller can re-engage by typing) but hostile in voice. Voice callers in crisis need:

1. **Audible support resources** voiced clearly with phone numbers digit-by-digit.
2. **A latch** — once crisis is detected, every subsequent turn re-voices the support message regardless of caller input.
3. **No agent-initiated termination.** The caller hangs up when ready; the agent never disconnects them.

This pattern is part safeguarding, part regulatory (some jurisdictions require specific helpline information). Substance is non-negotiable; only delivery shape adapts.

## Detection

Source has a `Self_Harm_and_Suicide_Prevention` topic (or equivalent) that:
- Voices a chat-shaped block with `<br>` tags and HTML
- Reads phone numbers as cardinals ("a hundred and sixteen one twenty-three")
- Doesn't latch (`crisis_detected` flag) so the message doesn't repeat
- Transfers or ends after the message

## Chat example (before)

```
| if @variables.crisis_detected == True:
|   | always respond exactly and only with this message: "Confidential advice
|   and support for your mental health is available for free, 24 hours a day,
|   from either the Samaritans by calling 116 123 or by texting 'SHOUT' to
|   85258 if you're struggling to cope.<br>You can get 24/7 crisis support by
|   calling 111. Please phone 999 or go to A&E for 24-hour emergency help with
|   suicidal ideas."
```

## Voice example (after) — recommended

**Voice the substance with digits read singly, slowed delivery:**

```
| if @variables.crisis_detected == True:
|   | Voice EXACTLY (slowed prose, falling intonation, digits spoken singly —
|   SSML rate ~85% configured at runtime layer):
|   "Free, confidential support is available any time. You can call the
|   Samaritans on one-one-six, one-two-three. You can text SHOUT — that's
|   S-H-O-U-T — to eight-five-two-five-eight. For urgent crisis support, call
|   one-one-one. For an emergency, call nine-nine-nine, or go to A and E."
|   Repeat this on every subsequent turn regardless of caller input. Do NOT
|   transfer, do NOT terminate the call.
```

Three critical changes:
1. **All phone numbers digit-by-digit** ("one-one-six, one-two-three" not "a hundred and sixteen one hundred and twenty-three").
2. **Latch via `crisis_detected`** — every turn re-voices, no matter what the caller says next.
3. **No transfer / no termination** — the caller stays on the line until they hang up.

## Voice example — alternatives

**Live transfer to a human counsellor** if available:

```
| In addition to the support message: "If you'd like, I can put you through to
| a person right now — would that help?" If yes, transfer with full state
| preserved. If no, latch and continue voicing the support message.
```

Verify counsellor availability and routing before promising. Do not promise live transfer if it isn't reliably available.

**SMS the helpline numbers** (in addition to voicing):

> "I've also texted those numbers to your phone so you have them later."

Reduces dependency on caller retention of digits.

## Anti-patterns

- **Reading "116 123" as "a hundred and sixteen one hundred and twenty-three".** Some TTS engines do this by default. Force digit-by-digit (configure pronunciation dictionary or use SSML `<say-as>` if engine supports).
- **Hanging up after the message.** Catastrophic. The caller in distress now feels rejected by the only voice they had.
- **Reading the message once and falling back to normal flow.** Without the latch, the agent may interpret a quiet "thank you" or distressed monosyllable as routing intent and resume booking.
- **Transferring to "support" (not crisis-trained advisers).** If transfer is offered, the destination must be a trained counsellor, not the general queue.
- **Reading the chat HTML literally.** `<br>` becomes "less-than B-R greater-than" on some engines.

## Where it lives

`Self_Harm_and_Suicide_Prevention` topic `reasoning.instructions`. The latch flag (`crisis_detected`) is set by `mark_crisis_detected` from either this topic or the global `topic_selector` when explicit self-harm intent is detected.

## Mis-applications (optimize mode)

- **Pattern: voice script reads the helpline numbers as cardinals.** Force digit-by-digit pronunciation.
- **Pattern: voice script latches but the latched message uses the unmodified chat text.** Same content, but without slowed delivery and digit-by-digit it reads cold. Apply the prosody adjustments.
- **Pattern: voice script handles crisis but emotional de-escalation patterns are absent.** This is `[out-of-scope]` for the voice library v1 — flag as a future v2 item.
- **Pattern: voice script latches on `crisis_detected` but the variable is reset elsewhere unintentionally.** Audit every reset_* action; `crisis_detected` should never be cleared in a session.
