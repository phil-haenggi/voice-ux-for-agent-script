---
id: D06
name: reference-numbers
category: input-collection
severity: medium
applies_to: [migrate]
detection:
  - keyword: "policy number"
    in: [instructions]
  - keyword: "pre-authorisation"
    in: [instructions]
  - keyword: "pre-auth"
    in: [instructions]
  - keyword: "reference number"
    in: [instructions]
  - keyword: "case number"
    in: [instructions]
  - keyword: "appointment ID"
    in: [instructions]
principle_refs: [P2, P10]
pattern_refs: [T-grounding-phone, T-repair-tier-2]
---

# Reference numbers (policy, pre-auth, IDs)

## Why it matters

Alphanumeric reference numbers (insurance policy numbers, pre-authorisation numbers, case IDs, claim numbers) are STT-hostile in the same ways as phone numbers, with one extra hazard: O/0 (letter-O / zero) ambiguity. "POL-O-2-3-4-5" can transcribe as "POL-zero-two-three-four-five" or "POL-O-23-45" depending on the engine.

Failure mode: the agent passes a wrong reference number to the booking API, the lookup fails, the caller has no idea why.

## Detection

Source collects any of:
- `policyNumber` / `policy_number`
- `preAuthorizationNumber` / `pre_auth_number`
- `caseNumber`
- `appointmentId`
- Free-text "reference" / "ID" fields

Without an explicit spell-confirm step.

## Chat example (before)

```
"Please provide your policy number."
```

(Trusts the chat input. In voice, this silently mishears.)

## Voice example (after) — recommended

**Single ask, digit-by-digit echo (these are always low-confidence cases):**

> Agent: And your policy number?
>
> Caller: POL-O-2-3-4-5.
>
> Agent: Just to confirm — P, O, L, then either letter-O or zero — was that letter-O or zero? [pause] Got it. P, O, L, letter-O, two, three, four, five. Right?

**Standardise "zero" vs "oh"** — pick one across the agent and stick. "Zero" is the safer choice for ID strings (less ambiguous than "oh").

**For long reference numbers — chunk into groups of 3-4 digits:**

> Agent: Just to confirm — that's three-three-three, four-five-six, seven-eight-nine. Right?

**Tier-1 repair:**

> Agent: Sorry, didn't catch that — could you say the policy number again?

**Tier-2 (chunked dictation):**

> Agent: Take it slowly, three or four characters at a time — what's the start?

## Voice example — alternatives

**Skip reference confirmation if the field is short and used only for display.** If the value flows to a confirmation email but isn't used for lookup, looser tolerance.

**Cross-modal lookup as fallback.** If the caller can't recall the number, offer SMS link to look up from email confirmation:

> Agent: No worries — I can text you a link to look it up if you'd prefer.

Verify the SMS integration before promising.

## Anti-patterns

- **Treating reference numbers like phone numbers.** Phone numbers are all-digits; reference numbers often mix letters and digits. The "oh / zero" ambiguity is more acute.
- **Reading characters concatenated.** "POL-23-45" runs as "pol twenty-three forty-five" in some engines. Read individually.
- **Saving without confirming.** A wrong policy number means the insurance check fails downstream — caller hits a confusing error in Phase 5 (booking commit) when the real cause was in Phase 2.
- **Reading "zero" as "oh" inconsistently across the same field.** Pick one read-out convention.

## Where it lives

- `Appointment_Management` Phase 2 step F (insurance branch).
- Any topic that collects case / appointment / claim IDs.
- Variables: `policy_number`, `pre_auth_number`, equivalents.
