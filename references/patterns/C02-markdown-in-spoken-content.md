---
id: C02
name: markdown-in-spoken-content
category: display-formatting
severity: high
applies_to: [migrate]
detection:
  - regex: '\*\*[^*]+\*\*'
    in: [welcome, error, instructions, response_templates]
  - regex: '_[^_]+_'
    in: [welcome, error, instructions, response_templates]
  - regex: '`[^`]+`'
    in: [welcome, error, instructions, response_templates]
  - regex: '^#{1,6}\s'
    in: [response_templates]
  - regex: '^\s*[-*]\s'
    in: [response_templates]
principle_refs: [P5]
pattern_refs: [T-translate-2]
---

# Markdown in spoken content

## Why it matters

TTS engines read most Markdown literally:
- `**bold**` → "asterisk asterisk bold asterisk asterisk"
- `_italic_` → "underscore italic underscore"
- `` `code` `` → "backtick code backtick"
- `### heading` → "hash hash hash heading"
- `- bullet` → "dash bullet" or, in some engines, "minus bullet"

Even when the engine is smart enough to skip the markers, Markdown structure (headings, bullets) doesn't translate to audible structure. Voice has no headings and no bullets — those are visual cues.

## Detection

Source contains any Markdown syntax in user-visible content:
- Bold: `**text**` or `__text__`
- Italic: `*text*` or `_text_`
- Code: `` `text` ``
- Headings: `# H1`, `## H2`, `### H3`
- Bullets: `- item`, `* item`
- Numbered list (covered also by A01): `1. item`

## Chat example (before)

```
"You've selected the following slot:
- **Consultant Name:** Dr Smith
- **Hospital:** Newcastle
- **Date and Time:** 16 May 2026 at 11:00 AM
- **Cost:** £250"
```

```
"### Booking Confirmed
Your appointment has been booked. **Cost:** £250."
```

## Voice example (after) — recommended

**Strip Markdown. Convert structure to spoken prose:**

> "That's Dr Smith at Newcastle, Thursday the sixteenth of May at eleven in the morning, two hundred and fifty pounds. Shall I take your details?"

**Replace headings with prose framing:**

> "Booked. That's Dr Smith at Newcastle, two hundred and fifty pounds. We'll send a confirmation by post and email."

## Voice example — alternatives

**SSML `<emphasis>` for bold:** if the engine supports SSML, replace `**X**` with `<emphasis>X</emphasis>` for vocal stress. Useful for prices, names, and dates.

```
"That's Dr Smith at <emphasis>Newcastle</emphasis>, Thursday the
<emphasis>sixteenth</emphasis> of May."
```

Verify in voice preview — emphasis behaviour varies by engine. Some engines treat all `<emphasis>` levels the same.

**Sequential prose for bullet structure:** when a list of details genuinely needs to be conveyed, voice it as a list-shaped sentence, but keep it ≤3 items:

> "We've got your name, your address, and your phone number — anything to update?"

Beyond 3 items, use progressive disclosure (one item per turn).

## Anti-patterns

- **Replacing `**` with quotation marks.** `**Cost:**` → `"Cost:"` — TTS reads the quotes.
- **Replacing bullets with semicolons.** `- A; - B; - C` runs together with no audible separation.
- **Keeping headings as questions.** `### What's next?` — heading marker stripped but the prose form is still fine. Watch for orphan `?` from headings becoming part of the next sentence.
- **Stripping Markdown but leaving the data structure.** "Consultant Name: Dr Smith Hospital: Newcastle Date and Time: 16 May …" — the labels are now audible noise.

## Where it lives

Anywhere user-visible: `messages`, `reasoning.instructions` blocks containing literal output, response templates.

Applied as part of the **final strip-chat-isms pass** alongside C01.
