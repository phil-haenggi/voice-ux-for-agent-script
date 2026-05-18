---
id: C05
name: chat-ui-references
category: display-formatting
severity: high
applies_to: [migrate]
detection:
  - regex: '\bthis (chat|chat window|conversation window|window|page|screen)\b'
    in: [welcome, error, instructions, response_templates]
  - keyword: "scroll down"
    in: [response_templates]
  - keyword: "scroll up"
    in: [response_templates]
  - keyword: "above this message"
    in: [response_templates]
  - keyword: "below this message"
    in: [response_templates]
  - keyword: "the chat"
    in: [response_templates]
  - keyword: "transferring the chat"
    in: [response_templates]
principle_refs: [P5]
pattern_refs: [T-translate-5]
---

# Chat-specific UI references

## Why it matters

Phrases like "this chat window", "scroll up to see your previous order", "click the menu in the top-right" are dead weight in voice — there is no chat window, nothing to scroll, no menu icon. The user hears these and gets confused (am I missing a screen?), or annoyed (the agent is reading from a script that doesn't apply to me).

This pattern overlaps with C03 (interface verbs) but focuses specifically on **referential** language pointing at chat UI elements ("this", "above", "below", "the icon"). C03 covers actions (click, tap); C05 covers the things actions point at.

## Detection

Source contains:
- "this chat", "this chat window", "the chat window"
- "transferring the chat" / "downloading the chat"
- "scroll up", "scroll down", "scroll to find"
- "above", "below" (when used to reference earlier/later messages — context-dependent)
- "the icon", "the menu", "the dots", "the button"
- "in the top-left", "in the top-right", "on the screen"

## Chat example (before)

```
"If you'd like to download the transcript of this chat, now's your chance to
do so. Simply click the three dots on the top left of this chat window and
select 'Download chat'."
```

```
"Transferring the chat to a support executive."
```

```
"Scroll up to review the slots I shared earlier."
```

## Voice example (after) — recommended

**Strip the UI reference. Replace with what the agent will actually do:**

> "I'll put you through to a support adviser now — they'll have everything we've talked about. Ready?"

> "Putting you through now — please hold."

> "Earlier I mentioned slots on Tuesday and Wednesday — want me to go through them again?"

## Voice example — alternatives

**Multimodal voice-over-web with explicit framing:** if the platform genuinely shows the chat alongside the voice:

> "You can scroll up in the chat to see those, or I can read them again — what's easier?"

Couples with C03 — verify multimodal availability before relying.

## Anti-patterns

- **Translating "this chat" to "this conversation".** Better, but if the broader copy is still chat-shaped ("download this conversation"), the translation is cosmetic.
- **Stripping the UI reference but losing the action.** "Click the three dots and select 'Download chat'" → "Download chat" — strips the noise but the new sentence is still nonsense in voice. Replace with the alternate path: SMS/email a transcript post-call (Layer E), or just don't offer.
- **Referring to "earlier" without saying when.** Voice users don't have scrollback; "as I mentioned earlier" is fine if the earlier reference is recent and salient. If it's stale, just re-state.

## Where it lives

- Hand-off / escalation flows (the most common offender)
- Post-booking flows ("download a copy of your booking…")
- Help / how-to flows ("scroll up to see your previous slots")
- Error messages ("close this window and try again")

## Application order note

This pattern is part of the **final strip-chat-isms pass** (Application order step 7 in `README.md`), applied after all rewrites. Some chat-UI references appear inside instructions that earlier patterns have already rewritten — the final pass catches what's left.
