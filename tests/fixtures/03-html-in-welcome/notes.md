# Fixture 03: HTML in welcome

## Patterns exercised

- **B01** — welcome-length (5+ sentence chat welcome → ≤7s spoken agent layer)
- **B02** — welcome-ai-disclosure (ensure "virtual assistant" or equivalent stays in)
- **B03** — error-message-voice-readable ("refresh the page" is screen-only)
- **B04** — pre-chat-variable-interpolation (`{First_Name}`, `{Transcript_Id_Formula}` stripped)
- **C01** — html-tags-in-spoken-content (`<br>`, `<a>` stripped)
- **C02** — markdown-in-spoken-content (`**bold**` stripped)
- **C03** — interface-verbs ("refresh the page" interface verb removed from error)
- **C04** — url-read-aloud (privacy policy URL paraphrased / dropped)
- **H01** — modality-and-connection-blocks (`connection telephony` + `modality voice:` added)

## What the rewrite must do

1. Welcome — strip the HTML, drop the chat-ID line, drop `{First_Name}` interpolation, paraphrase the URL, compress to a voice-readable greeting that still includes AI disclosure and ends with a question.
2. Error message — replace "refresh the page" (screen-only) with voice-shaped recovery options ending in a question.
3. Add `connection telephony:` and `modality voice:` blocks (H01 first-pass requirement).
4. Drop `connection messaging:` (voice-only deployment).
5. Update the developer-name and label to disambiguate from the chat agent (avoid duplicate-deploy clashes).

## What the rewrite must NOT do

- Keep the chat ID under any wording. There's no way for a voice caller to retain a multi-character reference number.
- Read the URL aloud, even paraphrased — for short branded URLs, prefer dropping or sending via SMS post-call.
- Generate an opening longer than ~7 seconds spoken (~100 words).
- Add SSML markup (out of scope here — separate Layer E item).

## Run notes

This fixture is the most "concentrated" — multiple categories firing on a small surface (welcome + error + config). It's intentionally small to keep diff review manageable; in a real migration the welcome rewrite often couples with Layer D two-voice opening, but that's a separate concern handled in the audit + bundle, not in the `.agent` file.

The welcome here uses a single-layer agent welcome (no system layer) because the input has no carrier-side announcement signal. If the source had a separate disclosure mechanism, the agent welcome could shed the AI-disclosure clause.
