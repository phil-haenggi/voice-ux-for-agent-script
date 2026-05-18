---
id: C04
name: url-read-aloud
category: display-formatting
severity: high
applies_to: [migrate, optimize]
couples_with: [E03]
detection:
  - regex: 'https?://'
    in: [welcome, error, instructions, response_templates]
  - regex: '\{!@variables\.[A-Za-z_]+_Url\}'
    in: [welcome, error, instructions, response_templates]
  - keyword: "share your experience here"
    in: [response_templates]
principle_refs: [P12]
pattern_refs: [T-translate-2]
---

# URL read-aloud

## Why it matters

URLs read aloud are unintelligible and unusable. Even a "short" URL like `https://www.nuffieldhealth.com/feedback/csat?id=ABC123` becomes "h-t-t-p-s colon slash slash w-w-w dot nuffield-health dot com slash feedback slash c-s-a-t question-mark i-d equals A-B-C-1-2-3" — meaningless to a caller without a screen.

Common offending patterns: clickable T&Cs, CSAT survey links, "click here for more info", post-booking confirmation pages.

The fix is **cross-modal handoff** (P12): SMS, email, or carrier pre/post-call screen. If none is available, the URL must be voiced as paraphrase ("on our website") or dropped entirely.

## Detection

Source contains:
- Literal URLs (`http://`, `https://`)
- Variables ending in `_Url`, `_URL`, `_Link` referenced in user-visible content
- HTML `<a href="…">` tags (also caught by C01)
- Phrases that imply a URL is coming ("share your experience here:", "you can find more info at:")

## Chat example (before)

```
"Thank you for chatting with us! Your feedback helps us improve. Please take
a moment to share your experience here: {!@variables.CSAT_Survey_Url}"
```

```
"Progressing further requires that you accept our
<a href=\"https://www.nuffieldhealth.com/terms/...\">Terms and Conditions</a>.
Do you wish to proceed?"
```

```
"Visit https://www.nuffieldhealth.com/services for more information."
```

## Voice example (after) — recommended

**For CSAT URL — drop. Use SMS post-call (Layer E) if available:**

```
Pre-closing: "Anything else I can help with today?"
Terminal: "Right then — thanks for calling, take care."
[end call cleanly]
```

The CSAT survey arrives via SMS or email after call (configured at Layer E).

**For T&Cs URL — paraphrase the destination, voice the substance (couples with E03):**

> "Before I book, two quick things to agree to. Cancellations within twenty-four hours of the appointment are charged in full. Your details will be shared with the consultant and Nuffield Health to manage your care. The full terms are on the Nuffield Health website. Do you agree, yes or no?"

**For info URL — paraphrase as "on our website":**

> "You can find more on our website at nuffieldhealth dot com."

(Read the bare domain only — not the path, not the protocol.)

## Voice example — alternatives

**SMS handoff** (when SMS is available):

> "I'll text you a link to the terms — give me a second to send it. Got it. The link's on its way to your number ending five-five-five. Once you've had a look, just say 'I agree' to go ahead."

**Email handoff** (lower friction than SMS for some users):

> "I'll send that link to your email — same address you gave me earlier."

**Spoken short URL with phonetic spelling** (last resort):

> "Visit nuffieldhealth dot com slash feedback. That's n-u-f-f-i-e-l-d-h-e-a-l-t-h."

This is hostile to the caller. Use only when no other channel is available and the URL is genuinely short.

## Anti-patterns

- **Reading the protocol.** "h-t-t-p-s colon slash slash" — dead time.
- **Reading query strings.** `?id=abc&utm_source=voice` — utterly meaningless.
- **Saying "the link in the chat" / "click the link".** Couples with C03 — there is no chat.
- **Sending an SMS the platform doesn't support.** Verify SMS-out is wired before promising. Falling back to "wait, I can't actually text you" is worse than not offering.
- **Reading just the path.** "Slash feedback slash csat" — without the domain, the path is ungrounded.

## Where it lives

- `messages.welcome`, `messages.error`
- `reasoning.instructions` blocks that voice URLs (CSAT prompt, T&Cs, "more info" branches)
- Variables holding URLs (don't delete the variables — they may be used by SMS/email side channels — but stop reading them)

## Mis-applications (optimize mode)

- **Pattern: voice script paraphrases the URL but reads the bare domain awkwardly.** "n-u-double-f dot com" — verify TTS pronunciation; some engines stumble. Add to pronunciation dictionary if needed.
- **Pattern: voice script promises SMS handoff but the SMS integration isn't deployed.** Surfaces as customer complaint. Verify Layer E item E.9 is actually wired.
- **Pattern: voice script drops the URL but doesn't replace with the substance.** T&Cs case — caller now consents to nothing audible. Compliance gap.
