---
id: C01
name: html-tags-in-spoken-content
category: display-formatting
severity: high
applies_to: [migrate]
detection:
  - regex: '<br\s*/?>|<a\s|<b>|<strong>|<em>|<i>|<p>|<ol>|<ul>|<li>|<div>|<span>'
    in: [welcome, error, instructions, response_templates]
  - regex: '&quot;|&amp;|&lt;|&gt;'
    in: [welcome, error, instructions, response_templates]
principle_refs: [P5]
pattern_refs: [T-translate-2]
---

# HTML tags in spoken content

## Why it matters

TTS engines handle HTML inconsistently:
- Some read tags literally ("less-than B-R greater-than").
- Some skip tags but break sentence boundaries unexpectedly.
- Some collapse `<br>` to a comma, losing the intended pause.
- `<a href="…">text</a>` may read just the text, just the URL, or both.
- HTML entities (`&quot;`, `&amp;`) get read as their named form.

Behaviour varies by engine, by version, and sometimes by language. The only reliable approach is to strip all markup before it reaches the synthesiser.

## Detection

Source contains any HTML tag or HTML entity in user-visible content:
- `<br>`, `<br/>`, `<br />`
- `<a>`, `<b>`, `<strong>`, `<em>`, `<i>`, `<p>`
- `<ol>`, `<ul>`, `<li>`
- `<div>`, `<span>`
- HTML entities: `&quot;`, `&amp;`, `&lt;`, `&gt;`, `&nbsp;`

## Chat example (before)

```
"Here are the available slots:<br>
<b>Consultant: Dr Smith at Newcastle (£250 / 30 mins)</b><br>
<ol start=&quot;1&quot;>
<li>16 May 2026 at 9:00 AM (30 mins)</li>
</ol>"
```

```
"Progressing further requires that you accept our
<a href=\"https://www.nuffieldhealth.com/terms\" target=\"_blank\">Terms and
Conditions</a>. Do you wish to proceed?"
```

## Voice example (after) — recommended

**Strip all markup. Convert structure to spoken prose:**

> "Dr Smith at Newcastle has a slot on Thursday the sixteenth of May at nine in the morning, two hundred and fifty pounds for thirty minutes. Want that one?"

**For `<a>` tags — paraphrase the destination, never read the URL:**

> "Before I book, two quick things to agree to. Cancellations within twenty-four hours of the appointment are charged in full. Your details will be shared with the consultant and Nuffield Health to manage your care. The full terms are on the Nuffield Health website. Do you agree, yes or no?"

(See E03 for long-static-message handling — the T&Cs case is a longer pattern.)

## Voice example — alternatives

**Keep `<a>` only if multimodal voice-over-web with visual rendering.** Add an explicit modality guard: "If rendering visually, link is clickable; if voice-only, paraphrase." Verify with the platform.

**Convert `<br>` to SSML `<break>`:** `<break time="500ms"/>` — works on engines that accept SSML but adds a different markup the LLM has to emit consistently. Most flows are better with prose-shaped sentence breaks.

**Convert `<b>`/`<strong>` to SSML `<emphasis>`:** valid for engines that support SSML emphasis. Verify in voice preview — engine response varies.

## Anti-patterns

- **Stripping `<br>` to nothing (no pause).** Sentences run together without a breath. Replace with sentence-final punctuation (`.`, `?`) and let the engine do prosody.
- **Reading the URL.** "Visit nuffieldhealth dot com forward slash terms forward slash …" — no voice user can retain that. Either send via SMS (Layer E) or skip and rely on the spoken summary.
- **Stripping `<a>` text along with the tag.** `Accept our <a>Terms</a>. Do you agree?` becomes `Accept our . Do you agree?`. Strip the tag but keep the inner text.
- **Decoding entities to literal punctuation but not stripping the tag.** `<b>"Hello"</b>` becomes `"Hello"` (correct) only if `&quot;` is decoded AND `<b>` is stripped.

## Where it lives

Anywhere user-visible: `messages.welcome`, `messages.error`, `reasoning.instructions` blocks containing literal output, response templates, action `progress_indicator_message` (rarely affected but worth checking).

This is the **final pass** in the rewrite — applied after all other patterns (see Application order in `README.md`).
