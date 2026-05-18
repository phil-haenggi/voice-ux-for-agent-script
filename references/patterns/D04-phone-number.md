---
id: D04
name: phone-number
category: input-collection
severity: high
applies_to: [migrate, optimize]
detection:
  - keyword: "international format"
    in: [instructions, response_templates]
  - regex: '\+44|country code'
    in: [instructions, response_templates]
  - keyword: "phone number"
    in: [instructions]
  - keyword: "10 digits"
    in: [instructions, response_templates]
principle_refs: [P2, P10]
pattern_refs: [T-grounding-phone, T-repair-tier-2]
---

# Phone number

## Why it matters

Voice users don't know "international format". They say "oh seven seven oh oh, nine double oh, one two three" or "double four, seven seven oh oh…" or just the local form. Telling them to provide "international format starting with +44" is a chat-shaped instruction that voice users can't naturally produce.

Phone numbers are also high-stakes (callback contact, appointment SMS). STT errors on digit strings are the dominant error class — "oh"/"zero" ambiguity, "five"/"nine" confusion, dropped digits.

This is a textbook T-grounding-phone case: implicit echo on high confidence, explicit digit-by-digit on low confidence.

## Detection

Source has:
- Format prescription: "international format", "starting with +44", "country code"
- Length validation: "must be 10 digits", "ensure the number after the country code is 10 digits"
- Validation error voiced verbatim: "The phone number you provided appears to be invalid"

## Chat example (before)

```
"Please provide your phone number in international format (for example
+44 7716 543210), ensuring the number after the country code is 10 digits."
```

```
"The phone number you provided appears to be invalid. Please provide a valid
phone number in international format (for example +44 7716 543210), ensuring
the number after the country code is 10 digits."
```

## Voice example (after) — recommended

**Open ask, no format prescription:**

> Agent: And the best phone number to reach you on?
>
> Caller: Oh seven seven oh oh, nine double oh, one two three.

**Implicit echo on high confidence:**

> Agent: Got it — oh-seven-seven-double-zero, nine-double-zero, one-two-three.

**Explicit digit-by-digit read-back on low confidence (T-grounding-phone):**

> Agent: Just to confirm, that's oh, seven, seven, oh, oh, nine, oh, oh, one, two, three — is that right?

Group naturally — the UK convention groups as `07700 900 123` (5-3-3) or `0770 0 900 123`. Pause briefly between groups. Read every "0" as "oh" or "zero" consistently — pick one and stick.

**Tier-1 repair on miss:**

> Agent: Sorry, missed that — could you say the number again?

**Tier-2 (digit-by-digit, only on second miss):**

> Agent: Could you say it digit by digit, with the country code first if it's not UK?

## Voice example — alternatives

**Caller-line-ID auto-fill.** If the caller's number is already known (CTI passes it), confirm rather than collect:

> Agent: I've got the number you're calling from — is that the best one for the appointment, or shall I take a different one?

**Skip phone collection if not needed.** Some flows ask for phone reflexively. If the use case is purely on-call (no callback, no SMS), drop it.

**Verbal-fallback for partial misrecognition.** If the platform exposes per-digit confidence, only re-confirm the uncertain digits:

> Agent: I think I missed the third digit — was it oh-seven-seven, then [pause] — what comes next?

## Anti-patterns

- **Format prescription on first ask.** Voice users can't comply with "international format starting with +44". Drop.
- **Validation error read aloud.** "The phone number you provided appears to be invalid" is chat-language; voice should use Tier-1/Tier-2 repair instead.
- **Reading "oh" inconsistently.** "Oh" and "zero" both work but mixing them confuses ("oh seven seven zero zero") — pick one.
- **Reading without pauses.** "Oh-seven-seven-oh-oh-nine-oh-oh-one-two-three" runs together. Group with pauses.
- **Saving the raw STT output without normalising.** STT may capture "seven, seven, hundred, nine hundred, one twenty-three" — normalise to digits before storing.
- **Reading back digit-by-digit even on high confidence.** Slow. Use implicit echo unless confidence is low.

## Where it lives

- Phase 2 of booking topics.
- No-availability callback flow in Support Executive Assistance.
- Variables: `patient_phone`, `customerContactNumber`, `phone` (depending on script).
- Validation logic / save action.

## Mis-applications (optimize mode)

- **Pattern: voice script reads back the entire 11-digit number with no grouping.** Sounds like a string of digits, hard to verify. Group as "oh-seven-seven-double-zero, nine-double-zero, one-two-three".
- **Pattern: voice script confirms even on high confidence.** Slows every call. Add the confidence-driven branch.
- **Pattern: voice script accepts first capture without ANY echo.** No grounding. Implicit echo at minimum.
- **Pattern: voice script asks twice when the user provides "+44 then 10 digits" first time.** Caller already volunteered international form. Acknowledge and move on; don't repeat the prompt.
