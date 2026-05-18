---
id: B03
name: error-message-voice-readable
category: welcome-and-static
severity: medium
applies_to: [migrate, optimize]
couples_with: [C01, C03]
detection:
  - regex: '<a |<br>|click|tap|refresh|reload'
    in: [error]
  - keyword: "try refreshing"
    in: [error]
  - keyword: "the page"
    in: [error]
principle_refs: [P3, P9]
pattern_refs: [T-translate-2, T-translate-3]
---

# Error message voice-readable

## Why it matters

Chat-error messages often advise the user to take screen-shaped recovery actions ("try refreshing", "click reload", "check your connection"). None of these work in voice — there's no page to refresh, no button to click. A voice user hearing "please try refreshing" is being asked to do something impossible.

Error messages also need to take the blame off the user (P3): "something went wrong on my end" rather than "we couldn't process your request" (which the user reads as their fault). And they should end with the next action (P9 end-focus): retry vs. transfer.

## Detection

Source `messages.error` (or per-topic error copy) contains:
- `<a>`, `<br>`, or other HTML
- "click", "tap", "refresh", "reload", "the page"
- Vague "something went wrong" with no recovery option
- "Please try again" with no specific affordance

## Chat example (before)

```
"Sorry, something went wrong on our end. Please try again, or ask me to
connect you with a support executive who can help."
```

(Already voice-leaning, but "ask me to connect you with a support executive" is chat-shaped phrasing.)

```
"An error occurred. Please refresh the page and try again."
```

## Voice example (after) — recommended

```
"Sorry — something went wrong on my end. I can try again, or put you through
to a support adviser. Which would you prefer?"
```

Three things changed:
1. **Blame shift** — "on my end" not "on our end" (more personal) and not "your request failed" (which blames the user).
2. **Specific options** — try again, or transfer. The user knows exactly what they can say next.
3. **Question at the end** — P9 end-focus.

## Voice example — alternatives

**Single-option recovery:** when only one path is sensible (e.g., the action genuinely cannot be retried), name it directly:

> "Sorry — that didn't go through. I'll put you over to a support adviser who can sort it. Hold on a moment."

**Specific repair for known failure:** if the error type is identifiable (e.g., postcode validator returned invalid):

> "Sorry, I didn't catch that — could you say your postcode again?"

(This is Tier-1 repair, not a system error — apply T-repair-tier-1.)

## Anti-patterns

- **"Please try again" with no specifics.** What does "try again" mean? Re-say the same thing? Re-speak a different way? Specify.
- **Apologising twice.** "Sorry, sorry — something went wrong, I'm so sorry…" — voice users don't need the redundancy.
- **Blaming the system to evade the user but in a way that breaks trust.** "There's an issue with our servers" — true, but unhelpful and seems like the agent is making excuses.
- **Reading a stack trace / error code.** "Error 500: internal server error" — never voice technical detail.

## Where it lives

`messages.error` (global) and any topic-level error copy (e.g., "If an error occurs while executing an action, always respond with: …" in `reasoning.instructions`).

## Mis-applications (optimize mode)

- **Pattern: voice-shaped error copy but still says "please try again" with no specifics.** Add the specific options.
- **Pattern: error copy ends with statement, not question.** P9 violation — flip to question form.
- **Pattern: error copy works for one error type but is reused for all errors.** Consider per-error-class copy (postcode validation vs. booking commit failure vs. no slots) — each has a different next-best action.
