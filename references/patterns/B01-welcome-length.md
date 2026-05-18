---
id: B01
name: welcome-length
category: welcome-and-static
severity: high
applies_to: [migrate, optimize]
couples_with: [B02]
detection:
  - structural: "welcome message > ~7 seconds spoken length (~100 words)"
    in: [welcome]
  - regex: '<br>'
    in: [welcome]
  - structural: "welcome contains chat ID / transcript ID interpolation"
    in: [welcome]
principle_refs: [P4]
pattern_refs: [T-opening]
---

# Welcome length

## Why it matters

Voice openings have a hard 5–7 second budget (P4). After that, the user starts to feel they've been put on hold. Chat welcome messages routinely run 30+ seconds when read aloud — they pack identity, capabilities, regulatory disclaimers, privacy notes, emergency redirects, and the first question into one block. Voice users have already forgotten the disclaimers by the time the question arrives.

The fix is structural: split the welcome into two layers (T-opening) — a system layer for legal/regulatory content (recording, AI disclosure, emergency redirect) and an agent layer for self-identification + first question. Each layer has its own constraints.

## Detection

Source `messages.welcome` (or equivalent) contains any of:
- More than ~100 words
- Multiple sentences joined with `<br>`
- Chat-shaped interpolation: chat ID, transcript ID, "your chat ID is X"
- Privacy policy reference, disclaimers, "we don't offer emergency services"
- Credit-card / data warnings

## Chat example (before)

```
"Hi {!@variables.First_Name}, I'm your Nuffield Health virtual assistant.<br>
I can advise you about our services and book you in for a consultation, but I
can't give you specific medical advice or diagnoses.<br>
This chat isn't monitored and we don't offer emergency services, so if you
need urgent medical help, please call 111 or 999.<br>
Please don't share any credit card details or detailed medical information.
To find out how we use your data, see our privacy policy.<br>
Your chat ID is {!@variables.Transcript_Id_Formula}. Please keep this for
reference.<br>
How can I help you today?"
```

## Voice example (after) — recommended

**Two-layer opening (T-opening):**

**System layer** — formal, distinct TTS voice, no contractions, voiced first:

> "You've reached Nuffield Health. This call may be recorded for training and quality. You're speaking with our automated assistant. If this is a medical emergency, please hang up and call nine-nine-nine. For urgent medical help, call N-H-S one-one-one."

**Handover** — 600–900ms pause.

**Agent layer** — warm, varied prosody, contractions normal, voiced second:

> "Hi, you're through to the Nuffield Health booking line. I can help you book a consultation or answer questions about our services. What would you like to do?"

The agent layer is ~6 seconds at 140 wpm and ends with the question (P9 end-focus). The system layer carries the legal weight.

## Voice example — alternatives

**Carrier-side pre-call announcement:** if the platform supports it, the system layer plays before the agent connects. Agent layer is shorter (no disclosures repeated). Verify availability with the platform/CTI team — most don't have it by default.

**Single-layer short welcome (no system layer):** if there's no regulatory requirement for recording/AI disclosure in the jurisdiction, drop the system layer entirely:

> "Hi, you're through to Nuffield Health. I can help you book a consultation or answer questions. What would you like to do?"

Verify the regulatory minimum with legal/compliance — different markets have different requirements.

**Returning-caller variant:** if CTI provides a known caller, personalise:

> "Hi, welcome back to Nuffield Health. What can I help you with today?"

## Anti-patterns

- **Reading the chat-ID line.** "Your chat ID is X-Y-Z-1-2-3" is meaningless in voice — the user has no way to retain it without a screen.
- **Asking the question first, then disclosing.** P9 violation in the wrong direction — the user starts answering before they've heard the disclosure.
- **Repeating the AI disclosure on every turn.** Once is required (B02). After that it's noise.
- **Skipping the handover pause.** Without 600–900ms between layers the user perceives one long welcome and the layered structure collapses.

## Where it lives

`messages.welcome` (agent-layer content). System-layer content lives either in carrier config (Layer E item) or, if voiced by the agent in sequence, prepended to `messages.welcome` with the handover pause.

## Mis-applications (optimize mode)

- **Pattern: two-layer structure exists but both layers use the same TTS voice.** No perceptual contrast — the user hears one long welcome. Configure distinct voices (Layer E item).
- **Pattern: agent layer is short but system layer is too long (>13s).** Push the system layer to carrier-side.
- **Pattern: handover pause is <300ms.** No perceptual gap; the layers blend. Configure ≥600ms.
- **Pattern: agent layer doesn't end with a question.** P9 violation — fix the end-focus.
