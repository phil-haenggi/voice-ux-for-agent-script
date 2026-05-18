---
id: D01
name: postcode-collection
category: input-collection
severity: high
applies_to: [migrate, optimize]
detection:
  - keyword: "postcode"
    in: [instructions, response_templates]
  - keyword: "postal code"
    in: [instructions, response_templates]
  - structural: "postcode is collected without spell-confirm"
    in: [instructions]
principle_refs: [P2, P10]
pattern_refs: [T-grounding, T-repair-tier-2]
---

# Postcode collection

## Why it matters

UK postcodes (`GU7 1PZ`) are STT-hostile: alphanumeric, mix of letter and digit, similar-sounding letters (B/D/E/V, M/N), and identical-sounding digits (5/9, oh/zero). Mishears are common: "GU7 1PZ" → "DU7 1PZ", "QE7 1BZ", "G E U seven one P Z". Postcode is a routing-critical field — wrong postcode means hospital lookup fails, slot search returns wrong region, callback address is wrong.

This is a textbook T-grounding case for a low-confidence-triggered explicit confirmation.

## Detection

Source has a topic that collects postcode (`Validate_Postal_Code`, `save_postal_code`, `Postal_Code` variable references) without an explicit spell-confirm step in the reasoning instructions.

## Chat example (before)

```
"Please provide your postcode."
```

```
"Provided postal code is invalid, please provide a valid postal code"
```

(Both rely on the user's text input being correct — fine in chat, not in voice.)

## Voice example (after) — recommended

**Capture, normalise, implicit echo on high confidence:**

> Agent: What's your postcode?
>
> Caller: GU7 1PZ.
>
> Agent: G-U-seven, one-P-Z — got it.

**On low recognition confidence — explicit letter-by-letter confirmation:**

> Agent: What's your postcode?
>
> Caller: [unclear] D-U seven one B Z.
>
> Agent: Just to confirm, that's D-U-seven, one-B-Z — is that right?

Keep the inward / outward gap audible: pause briefly between the outward part (`GU7`) and the inward part (`1PZ`). Read letters individually ("G, U, seven") not concatenated ("gee-you-seven").

**Tier-1 repair on no-match:**

> Agent: Sorry, I didn't catch that — could you say your postcode again?

**Tier-2 repair on second miss (constrained format hint):**

> Agent: You can say it letter by letter — like G-U-seven, one-P-Z.

## Voice example — alternatives

**Skip explicit confirmation when ASR confidence is high.** If the platform exposes a confidence score, only confirm when below threshold (e.g., 0.75). When above, implicit echo is enough.

**Skip postcode entirely if not needed for routing.** Some flows ask for postcode out of habit — if the actual use is hospital search, the user could pick a hospital by name instead.

**Letter-by-letter on first ask** (most robust, slowest):

> Agent: What's your postcode? Take it letter by letter — like G, U, seven.

Use only when the audience profile suggests heavy ASR difficulty (older callers, dialect mismatch).

## Anti-patterns

- **Asking for postcode but accepting any input without confirmation.** "GU7 1PZ" gets transcribed as "QE7 1BZ", silently saves, hospital search returns nothing — caller gets a wrong-postcode-no-hospitals error and has no idea why.
- **Concatenated read-back ("gee-you-seven, one-pee-zee").** Some engines collapse hyphens. Verify in preview.
- **Reading "Z" as "zee" in en-GB.** Should be "zed". Configure pronunciation dictionary if engine defaults to American (Layer E item).
- **Reading "0" as "oh".** Standardise: "zero" for digits, "oh" only for letter-O. Mishears between O/0 are common.
- **Voicing the postcode validation error verbatim.** The chat error "Provided postal code is invalid, please provide a valid postal code" is a Tier-0 error with no escalation. Replace with Tier-1/Tier-2 repair language (no blame, varies across attempts).

## Where it lives

- Topic that calls `Validate_Postal_Code` (typically `Appointment_Management` and `GeneralFAQ`).
- The `before_reasoning:` block that seeds postcode from pre-chat may still exist; in voice, drop it (couples with H02 and B04).
- The Tier-1 / Tier-2 repair language goes in the `reasoning.instructions` of the same topic.

## Mis-applications (optimize mode)

- **Pattern: Tier-1 and Tier-2 repair language is identical.** The script has two attempts but both say "Sorry, didn't catch that". Tier-2 should add a constraint or hint.
- **Pattern: confirmation reads the postcode as one chunk ("GU71PZ").** Some engines pronounce concatenated postcodes badly. Insert hyphens or pauses.
- **Pattern: same-format prescription ("say it as letters and numbers") at Tier-1.** Format prescriptions are anti-patterns at Tier-1; only legitimate at Tier-2.
- **Pattern: postcode change mid-flow doesn't reset hospital lookup.** Caller updates postcode but the previous lookup result is reused. Reset the hospital cache on postcode change.
