---
id: C03
name: interface-verbs
category: display-formatting
severity: high
applies_to: [migrate, optimize]
detection:
  - regex: '\b(click|tap|press|select|submit|enter|choose|pick option|the button|the icon|scroll|swipe)\b'
    in: [welcome, error, instructions, response_templates]
  - regex: '\bthe (chat|window|screen|page|three dots|menu)\b'
    in: [welcome, error, instructions, response_templates]
principle_refs: [P5]
pattern_refs: [T-translate-2]
---

# Interface verbs

## Why it matters

Voice has no interface. Words like "click", "tap", "select", "submit", "press", "enter", "scroll", "swipe" — and references to UI elements like "button", "icon", "menu", "the three dots", "the chat window" — make no sense to a voice user. They reveal that the script was authored for chat and not adapted.

In the worst cases the agent literally tells the caller to do something impossible: "click the three dots on the top left of this chat window and select 'Download chat'" — heard on a phone call where there is no screen.

## Detection

Source contains any of:
- Verbs: `click`, `tap`, `press`, `select`, `submit`, `enter` (in the input sense), `choose option`, `pick option`, `scroll`, `swipe`
- UI nouns: `the button`, `the icon`, `the menu`, `the three dots`, `the page`, `the screen`, `the chat window`, `the input box`
- Visual references: `as shown`, `see below`, `listed are`, `here are the options`

## Chat example (before)

```
"If you'd like to download the transcript of this chat, now's your chance to
do so. Simply click the three dots on the top left of this chat window and
select 'Download chat'. Are you happy for me to transfer you now?"
```

```
"Please select your payment method:
1. Insurance
2. Self Pay
Click the corresponding number."
```

```
"Submit your details below."
```

## Voice example (after) — recommended

**Replace with conversational equivalents:**

> "I'll put you through to a support adviser now — they'll have everything we've talked about. Ready?"

> "Self-pay, or insurance?"

> "Just say the details and I'll take them down."

## Voice example — alternatives

**Multimodal voice-over-web with explicit framing:** if the platform genuinely shows a UI alongside the voice, frame both modalities:

> "You can say it, or tap the option on screen — either works."

Verify that the UI is reliably visible to all callers (some launch in voice-only mode).

## Anti-patterns

- **Translating "click" to "say".** "Click your option" → "Say your option" — better, but still chat-shaped. Just ask the question naturally: "Which would you like?"
- **Keeping "select" because it sounds neutral.** "Select your payment method" reads as a UI verb in voice. Use "What payment method?" or "Self-pay or insurance?".
- **Replacing the verb but keeping the structure.** "Press 1 for insurance, press 2 for self-pay" → "Say 1 for insurance, say 2 for self-pay" — replaces interface verbs but keeps the numbered-menu anti-pattern (couples with A01).
- **Reading aloud "submit", "submit-button", "form".** All chat/web language. Strip.

## Where it lives

Everywhere — but especially:
- Topic transition messages ("transferring the chat" → "putting you through").
- Hand-off / escalation flows ("download the transcript", "click the three dots").
- T&Cs and consent flows ("submit your acceptance" → "do you agree?").
- Action-call narration ("clicking through to the booking system" — should never be voiced; use G02 pre-action narration instead).

## Mis-applications (optimize mode)

- **Pattern: voice script removed obvious interface verbs but kept references like "your screen" or "the page".** Re-scan for UI nouns, not just verbs.
- **Pattern: voice script uses "tap or say" for multimodal, but the platform is voice-only.** Drop "tap or" — it's misleading.
