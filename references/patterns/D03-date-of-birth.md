---
id: D03
name: date-of-birth
category: input-collection
severity: high
applies_to: [migrate, optimize]
couples_with: [I01]
detection:
  - keyword: "DD-MM-YYYY"
    in: [instructions, response_templates]
  - keyword: "YYYY-MM-DD"
    in: [response_templates]
  - keyword: "date of birth"
    in: [instructions]
  - keyword: "DOB"
    in: [instructions]
  - regex: '\bin DD-MM-YYYY format\b'
    in: [instructions, response_templates]
principle_refs: [P2, P9]
pattern_refs: [T-grounding, T-translate-4]
---

# Date of birth

## Why it matters

Voice users say dates in natural language: "third of June, ninety", "first of January nineteen-ninety", "fourteen-oh-three-eighty-three". Asking them for "DD-MM-YYYY format" is a chat-shaped format prescription that voice users can't comply with — they don't speak punctuation.

DOB is also gated to **age checks** (under-18 routing) and downstream record matching. Mishearing a year is both a safeguarding risk and a data-integrity risk.

The cardinal voice-UX rule: **echo the DOB in the format the caller spoke it**, not the format the API stores it in. If the caller said "first of January nineteen-ninety", read it back as "first of January nineteen-ninety" — never "1990-01-01" (ISO, observed in the real Nuffield sample) or "01-01-1990" if they spoke it as words.

## Detection

Source has:
- DOB format prescription on first ask: "in DD-MM-YYYY format", "for example 01-01-1990"
- Strict-format rejection on parse: "If the user provides the date in any other format, reject it"
- Summary read-back that uses the ISO form (`patient_dob` storing `YYYY-MM-DD` and being voiced verbatim)
- Lack of a `patient_dob_spoken` (or equivalent) variable

## Chat example (before)

```
"Please provide your date of birth in DD-MM-YYYY format (for example
01-01-1990)."
```

```
"DOB: 1990-01-01"  [in summary read-back, after caller said "first of
January nineteen-ninety"]
```

## Voice example (after) — recommended

**Capture two forms (couples with I01):**

```yaml
patient_dob: mutable string = ""
    description: "ISO YYYY-MM-DD for the booking API. Always normalised."
patient_dob_spoken: mutable string = ""
    description: "The caller's spoken form ('first of January nineteen-ninety') for echo-confirmation."
```

**Single open ask, no format prescription:**

> Agent: And your date of birth?
>
> Caller: First of January, nineteen-ninety.
>
> Agent: First of January nineteen-ninety — got it.

**Tier-1 repair on miss:**

> Agent: Sorry, didn't catch that — your date of birth?

**Tier-2 (constrained, only on second miss):**

> Agent: You can say it as day, month, year — like first of January nineteen-ninety.

**Echo back in the format the caller spoke** (P9 + T-grounding):

> Agent: First of January nineteen-ninety — right?

**Summary read-back uses `patient_dob_spoken`, not `patient_dob`:**

> Agent: Right, let me read that back. Sarah Jones, born first of January nineteen-ninety, on oh-seven-double-zero, nine-double-zero, one-two-three…

## Voice example — alternatives

**Skip spell-confirm when no age gating.** If DOB is non-critical and the system tolerates misreads, accept best-effort.

**Two-digit year disambiguation.** Caller says "ninety" — could be 1990 or 1890 or 2090 (rare). Default to 19xx for ages 18+ only if recent (post-1900). Add: "Sorry, just to confirm — nineteen-ninety, not eighteen-ninety, right?" only when ambiguous.

## Anti-patterns

- **Format prescription on first ask.** "Please give me DOB in DD-MM-YYYY format" — voice users can't comply.
- **Storing ISO and reading back ISO.** "Nineteen-ninety, oh-one, oh-one" — robotic, unmatchable to what the caller said. Breaks the echo-confirmation loop (P2).
- **Reading the year as digits.** "Nineteen-nine-zero" instead of "nineteen-ninety". Use natural year reading.
- **Reading the day as ordinal even when caller said cardinal.** Caller: "January one, nineteen-ninety." Agent: "First of January, nineteen-ninety." Mismatched form — caller may not recognise it as their own input. Mirror what they said.
- **Age recalculation that uses an old `patient_age`.** When the caller corrects DOB mid-flow, reset `patient_age` to -1 and re-run `calculate_patient_age` before any age-gated decision.

## Where it lives

- Phase 2 of booking topics (typically `Appointment_Management`).
- Summary read-back / Phase 3.
- Variables block (add `patient_dob_spoken` companion).
- Save action (modified to write both: `save_patient_demographics_voice` writes `patient_dob` ISO and `patient_dob_spoken` raw).

## Mis-applications (optimize mode)

- **Pattern: spoken-form variable exists but the summary still reads the ISO form.** Audit every read-back for `patient_dob` references; replace with `patient_dob_spoken`.
- **Pattern: voice script accepts natural-language input but normalises silently to ISO and reads back the ISO.** Same problem at the read-back layer. The fix is in the read-back, not the input.
- **Pattern: voice script does Tier-1 spell-confirm but doesn't escalate format prescription to Tier-2.** Format prescriptions are legitimate at Tier-2 — that's where they belong, not Tier-1 default.
