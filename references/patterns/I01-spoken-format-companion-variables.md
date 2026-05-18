---
id: I01
name: spoken-format-companion-variables
category: variables
severity: high
applies_to: [migrate]
couples_with: [A06, D03]
detection:
  - structural: "value displayed to user differs from spoken-natural form (currency, dates, structured data)"
    in: [variables, response_templates]
principle_refs: [P2, P5]
---

# Spoken-format companion variables

## Why it matters

Many values stored in agent variables are in machine-readable form: ISO dates (`1990-01-01`), currency strings (`£250.00`), phone numbers in international format (`+441234567890`). In chat these display fine. In voice, reading them verbatim violates P5 (prosody) and breaks P2 (grounding — the user can't echo-confirm the form they spoke).

The fix is **companion variables**: alongside each "machine" variable, store a "spoken" version. The original variable goes to APIs (booking commit, save action); the spoken version is voiced to the caller.

Three primary cases:

| Underlying variable | Companion | Set by |
|---|---|---|
| `patient_dob` (ISO `1990-01-01`) | `patient_dob_spoken` ("first of January nineteen-ninety") | save action captures both |
| `appointmentCost` (`£250.00`) | `appointmentCostSpoken` ("two hundred and fifty pounds") | utility action `format_currency` |
| `patient_phone` (`+441234567890`) | `patient_phone_spoken` ("oh-seven-double-zero, nine-double-zero, one-two-three") | save action captures both, OR utility |
| `dateAndTime` (`2026-05-05 17:30:00`) | `dateAndTime_spoken` ("Tuesday the fifth of May at five-thirty") | utility action `format_datetime` |

## Detection

Variables exist for currency / dates / phones / structured data **without** spoken-form companions. Read-back in instructions references the underlying variable directly.

## Chat example (before)

```yaml
variables:
    patient_dob: mutable string = ""
        description: "Patient DOB stored in YYYY-MM-DD format."
    appointmentCost: mutable string = ""
        description: "Cost as £-prefixed string."
```

```
| Voice the summary: "DOB: {!@variables.patient_dob}, Cost: £{!@variables.appointmentCost}"
```

(In chat, `1990-01-01` and `£250.00` display fine. In voice, they read robotically.)

## Voice example (after) — recommended

**Add companion variables alongside the originals:**

```yaml
variables:
    patient_dob: mutable string = ""
        description: "ISO YYYY-MM-DD for the booking API. Always normalised."
    patient_dob_spoken: mutable string = ""
        description: "VOICE — DOB in the exact form the caller spoke (e.g. 'first of January nineteen-ninety'). Used for echo-confirmation in summary."

    appointmentCost: mutable string = ""
        description: "Raw cost as returned from the booking API (e.g. '£250.00'). Used internally."
    appointmentCostSpoken: mutable string = ""
        description: "VOICE — spoken form ('two hundred and fifty pounds') for read-back. Set immediately after appointmentCost via the format_currency utility."

    dateAndTime: mutable string = ""
        description: "Slot timestamp from the booking API."
    dateAndTime_spoken: mutable string = ""
        description: "VOICE — spoken form ('Tuesday the fifth of May at five-thirty in the afternoon')."
```

**Modify save actions to capture both** (couples with D03):

```yaml
save_patient_demographics_voice: @utils.setVariables
    description: "Store gender and DOB. Captures both ISO (patient_dob) and spoken form (patient_dob_spoken)."
    with patient_gender = ...
    with patient_dob = ...
    with patient_dob_spoken = ...
    with patient_age = -1
```

**Add utility actions for derived spoken forms:**

```yaml
format_currency: @actions.Format_Currency
    description: "Convert raw amount (e.g. '£250.00') to spoken form ('two hundred and fifty pounds'). Call after appointmentCost is set."
    with amount = @variables.appointmentCost
    set @variables.appointmentCostSpoken = @outputs.spokenForm
```

**Use the companion in user-visible read-back:**

```
| Voice the summary: "Born {!@variables.patient_dob_spoken}, on {!@variables.patient_phone_spoken}, booked for {!@variables.dateAndTime_spoken}, {!@variables.appointmentCostSpoken}."
```

## Voice example — alternatives

**Inline formatting in instructions** (no companion variable): the LLM is told "convert YYYY-MM-DD to spoken English" inline:

```
| When voicing the DOB, convert from YYYY-MM-DD to natural English ("first
| of January nineteen-ninety", not the ISO form).
```

Brittle — the LLM occasionally slips into ISO when prompts are long. Companion variables are more reliable.

**SSML `<say-as>` overrides** for currency / dates: works on engines that support SSML, adds markup the LLM has to emit consistently. Less robust than companions for high-stakes read-back.

## Anti-patterns

- **Storing only the spoken form.** The booking API needs ISO; without the underlying value, you can't commit.
- **Storing only the underlying form.** Saves the API call but every voice read-back has to re-format inline. The LLM messes up under prompt pressure.
- **Companion variable exists but instructions still reference the underlying one.** Audit every read-back; missing one creates a single-turn failure.
- **Naming the companion ambiguously.** `patient_dob_2`, `cost_alt` — name them with `_spoken` suffix consistently so audit can find them.

## Where it lives

`variables:` block. New utility actions (`format_currency`, `format_datetime`, etc.) added at topic-level `actions:` blocks where they're used.

## Application order

Apply at step 2 (Application order). After `connection`/`modality` (step 1), before any system instructions. The variables must exist before instructions reference them.

## Layer E follow-up

The utility actions (`format_currency`, `format_datetime`) need to be implemented as Apex classes or Flows in the org. The skill scaffolds the action declaration but the underlying Apex/Flow is platform work — surface in Layer E.
