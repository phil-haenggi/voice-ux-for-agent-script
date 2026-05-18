---
id: A06
name: currency-spoken-form
category: system-instructions
severity: high
applies_to: [migrate, optimize]
couples_with: [I01]
detection:
  - regex: '£[0-9]'
    in: [instructions, response_templates, variables]
  - regex: '\$[0-9]'
    in: [instructions, response_templates, variables]
  - regex: '\bGBP\b|\bUSD\b|\bEUR\b'
    in: [instructions, response_templates]
  - regex: '\.00\b'
    in: [response_templates]
principle_refs: [P5, P9]
---

# Currency spoken form

## Why it matters

TTS engines are inconsistent with currency symbols. `£250` may read as "pound sign two five zero", "two hundred and fifty pounds", or just "two five zero" depending on engine and locale. `GBP 255.00` reads as "gee bee pee two hundred fifty point zero zero". Trailing `.00` reads as "point zero zero" — verbose and unnecessary for whole-pound amounts. Voice users hear money as **words** ("two hundred and fifty pounds"), not symbols.

Money is also a **high-stakes irreversible field** (T-grounding). Mishearing the price during a booking commit is a complaint waiting to happen. The voice form needs to be unambiguous at the syllable level.

## Detection

Source contains:
- Currency symbol followed by digits: `£250`, `$99`
- ISO currency code prefix: `GBP 255.00`, `USD 99.99`, `EUR 50`
- Trailing `.00` in display strings
- Variables holding raw amounts (e.g., `appointmentCost: "£250"`) without a spoken-form companion

## Chat example (before)

```yaml
"Cost: £{!@variables.appointmentCost}"
```

```
"You've selected the following slot: … Cost: £250.00"
```

```
"That'll be GBP 255.00 — please confirm."
```

## Voice example (after) — recommended

**Add the global rule to `system.instructions`:**

```
NUMBERS, NAMES, DATES, IRREVERSIBLE WORDS: Read prices as natural English
('two hundred and fifty pounds'), never with a digit-and-symbol form. Drop
trailing '.00' for whole-pound amounts. For pence amounts, say 'pounds and X
pence' (e.g., 'two hundred fifty pounds and ninety-nine pence').
```

**Add a spoken-form companion variable** (couples with I01):

```yaml
appointmentCost: mutable string = ""
    description: "Raw cost as returned from the booking API (e.g. '£250.00'). Used internally."
appointmentCostSpoken: mutable string = ""
    description: "Spoken-form cost ('two hundred and fifty pounds') for read-back. Set immediately after appointmentCost via the format_currency utility action."
```

**Use the spoken form in user-visible read-back:**

> Agent: That's Andrew McLeod at Newcastle, Tuesday the fifth of May at five-thirty, two hundred and fifty pounds. Shall I take your details?

## Voice example — alternatives

**Keep the symbol but rely on TTS engine reading.** Some engines (ElevenLabs, modern Polly) read `£250` correctly as "two hundred and fifty pounds" out of the box. Verify in voice preview before relying — and the result still depends on engine version.

**SSML say-as override:** wrap the amount in `<say-as interpret-as="currency" language="en-GB">£250.00</say-as>`. Works on most engines but adds markup the LLM has to emit consistently.

**Strip currency entirely:** in flows where the amount is also voiced separately ("two hundred and fifty pounds" in narration), leave the read-back digit-free. Avoid double-utterance.

## Anti-patterns

- **"two-hundred-fifty pounds".** Hyphenated; reads cleanly in some engines but as "two-hundred-dash-fifty" in others.
- **"£ two hundred and fifty pounds".** Mixing the symbol and the spelt-out form is the worst of both.
- **"two hundred fifty point zero zero pounds".** Don't read trailing `.00`. If the amount is `£250.50`, say "two hundred fifty pounds and fifty pence".
- **Different formats across topics.** One topic says "two-fifty pounds", another says "two hundred and fifty". Pick one and stick with it.

## Where it lives

- `system.instructions` (global) — add the rule.
- `variables:` block — add the spoken-form companion (`<name>Spoken`).
- Utility action — add `format_currency` (or similar) that sets the spoken variable from the raw one. Couples with I01.
- Response templates that read back amounts.

## Mis-applications (optimize mode)

- **Pattern: spoken-form variable exists but isn't used.** The agent still reads `£{!@variables.appointmentCost}` in the summary because the instruction wasn't updated. Audit every `appointmentCost` reference.
- **Pattern: spoken-form is hard-coded for one currency.** Moves to a market with `EUR` or `USD` and the formatter doesn't know. Make `format_currency` parameterised.
- **Pattern: rule says "never use £" but the API still returns £-prefixed strings.** The rule about display is right; the data flow needs the formatter to strip.
