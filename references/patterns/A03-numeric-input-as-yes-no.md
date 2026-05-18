---
id: A03
name: numeric-input-as-yes-no
category: system-instructions
severity: low
applies_to: [migrate]
detection:
  - keyword: "Do not interpret 0 or 1 as yes or no"
    in: [instructions]
  - keyword: "numeric inputs such as 0 or 1"
    in: [instructions]
  - keyword: "DTMF"
    in: [instructions]
principle_refs: [P8]
---

# Numeric input as yes/no

## Why it matters

In voice telephony there is no DTMF keypad surfaced to the agent (unless the runtime explicitly forwards keypad input as text — rare). Rules guarding against "0 or 1 = yes/no" are dead code in voice. They take up token budget and create cognitive load for the LLM during every turn, for no benefit.

## Detection

Source has a directive like:
- "Do not interpret numeric inputs such as 0 or 1 as yes or no"
- "When asking the user to confirm or refuse, only accept explicit textual responses. Do not interpret numeric inputs such as 0 or 1 as yes or no."

This pattern coexists with A02 (confirmation rule) — usually they're sentences in the same paragraph.

## Chat example (before)

```
When asking the user to confirm or refuse, only accept explicit textual
responses. Do not interpret numeric inputs such as 0 or 1 as yes or no. If
the response is ambiguous or numeric-only, prompt the user again with a
clear question.
```

## Voice example (after) — recommended

Strip the rule entirely.

```
[deleted]
```

The rule about ambiguous responses is preserved by A02 (confirmation rule); the numeric-input clause is the only piece that's dead in voice.

## Voice example — alternatives

**Keep if multimodal voice-over-web with DTMF fallback:** if the platform is genuinely accepting DTMF input as a string ("user pressed 1" → text "1"), keep the rule but add a modality guard: "If DTMF input is forwarded as text, treat numeric strings as keypad presses, not affirmatives." Verify with the voice platform team before keeping.

## Anti-patterns

- **Keeping the rule "just in case".** It bloats every turn's prompt and the LLM has to evaluate it on irrelevant inputs (e.g., when the user says a phone number).
- **Replacing "0 or 1" with "zero or one" thinking it now applies to voice.** A user saying "zero" or "one" in voice is not confirming anything; the affirmative-detection in A02 handles legitimate ambiguity.

## Where it lives

`system.instructions` — usually a single sentence inside the broader confirmation rule paragraph. Edit out, leave the rest of A02 in place.
