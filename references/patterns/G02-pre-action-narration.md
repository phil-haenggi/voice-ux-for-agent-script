---
id: G02
name: pre-action-narration
category: latency-masking
severity: medium
applies_to: [migrate, optimize]
detection:
  - structural: "irreversible commit action called without pre-action narration"
    in: [instructions]
  - keyword: "confirm_booking"
    in: [instructions]
  - keyword: "AgentForce_Appointment_Booking"
    in: [instructions]
  - keyword: "create_case"
    in: [instructions]
principle_refs: [P7, P9]
pattern_refs: [T-latency-pre-announce, T-latency-complex]
---

# Pre-action narration (irreversible commits)

## Why it matters

For high-stakes irreversible actions (booking commit, payment commit, case creation), the caller benefits from a narration **before** the call starts, in addition to the `progress_indicator_message` (G01) during the call. Narration gives the caller a final moment to interrupt if something is wrong, and frames the action so the caller understands why the upcoming silence exists.

For multi-second commits, also include verbal fillers every 3–5 seconds and a "may take a moment longer" warning at ~10 seconds.

## Detection

Source calls irreversible actions (`confirm_booking`, `create_case`, `payment_commit`) without an immediately preceding narration line in the reasoning instructions.

## Chat example (before)

```
| Invoke confirm_booking immediately only if patient_age >= 18.
| If the booking action returns a valid appointmentId with a success status,
| invoke mark_booking_confirmed.
```

(In chat, the user sees a spinner. In voice, silence.)

## Voice example (after) — recommended

**Narrate before the call. Add verbal-filler logic for slow operations:**

```
| Pre-announce: 'Right, booking that now — one moment…'.
| Invoke confirm_booking only if patient_age >= 18.
| If the call hasn't returned within 3 seconds, voice a verbal filler from the
| phrasebook ('Still going through…', 'Still on it…') every 3–5 seconds. If
| approaching 10 seconds, voice a 'may take a moment longer' warning ('This is
| taking a moment — bear with me.').
| On success, call mark_booking_confirmed.
| On failure, voice the booking-failure copy and offer transfer.
```

**For payment / T&Cs commit:**

```
| Pre-announce: 'OK, booking that for you now — one moment…'.
| Then call confirm_booking.
```

## Voice example — alternatives

**Combine narration with summary read-back:** the narration can re-state the booked thing, doubling as final implicit echo:

> "Right, booking Andrew McLeod at Newcastle, Tuesday at five-thirty, two hundred and fifty pounds — one moment."

Useful when there's a pause between summary confirmation and commit (e.g., T&Cs in between). Re-grounds the caller on what's about to happen.

**Skip narration for fast (<1s) commits.** Some actions are genuinely fast — narrating them is overkill. The `progress_indicator_message` alone is enough.

## Anti-patterns

- **Narrating the implementation.** "Calling AgentForce_Appointment_Booking" — never expose internals.
- **Narrating after the call starts.** Defeats the purpose; narration must precede the action so the caller hears it before the silence.
- **Narrating every action including fast ones.** "Just checking the postcode now — one moment… [200ms] — just checking the hospitals — one moment… [300ms]" — overkill. Narrate only multi-second / irreversible actions.
- **Narration that's longer than the action.** "I'm now going to take all your details, send them to our booking system, validate them with the consultant's calendar, and create your appointment record — one moment please." The narration is 10 seconds; the action is 2 seconds.
- **No verbal filler during long actions.** Caller hears the narration, then 8 seconds of silence — assumes the call dropped.

## Where it lives

`reasoning.instructions` of the topic that calls the irreversible action — typically Phase 5 of booking topics.

## Mis-applications (optimize mode)

- **Pattern: narration exists for booking commit but not for case creation.** Both should have it.
- **Pattern: narration is identical for fast and slow commits.** Vary based on expected duration.
- **Pattern: narration uses chat-shaped tone ("Processing your request now").** Use phrasebook conversational tokens.
- **Pattern: voice script has narration but no verbal filler logic for long operations.** Add filler every 3-5s and a warning at 10s.
