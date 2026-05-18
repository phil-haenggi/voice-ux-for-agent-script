---
id: D05
name: email-address
category: input-collection
severity: medium
applies_to: [migrate]
detection:
  - keyword: "email address"
    in: [instructions]
  - keyword: "valid email"
    in: [response_templates]
  - regex: 'contain.*@.*symbol'
    in: [instructions]
  - keyword: "top-level domain"
    in: [instructions]
principle_refs: [P2, P12]
pattern_refs: [T-grounding-email]
---

# Email address

## Why it matters

Email is the hardest single field to capture in voice. The local part can include letters, digits, hyphens, dots, and underscores; the domain has its own delimiters; the TLD is rarely spoken explicitly ("dot com" vs. "dot co dot uk"). Caller speech rate matters: "j-dot-smith-at-gmail-dot-com" is barely intelligible at normal speed.

Three workable strategies, in order of cost:
1. **Cross-modal handoff** (cheapest UX): "I'll send a verification link — confirm there." Requires SMS/email integration.
2. **Implicit echo on high confidence, letter-by-letter on low.** Standard T-grounding-email.
3. **Letter-by-letter on first ask** (most robust, slowest). Use only when audience is older or accent-mismatch-prone.

## Detection

Source has email collection (`save_patient_email`, `patient_email` variable, `customerEmail` field) without spell-confirm logic. Sometimes accompanied by a strict format-validation rule ("must contain exactly one '@' symbol, a recognised TLD") — treat the format rule as Tier-2 only, not first ask.

## Chat example (before)

```
"Please provide your email address."
```

```
"The email address you provided appears to be invalid. Please provide a
valid email address (for example john.smith@example.com)."
```

## Voice example (after) — recommended

**Single ask, implicit echo on high confidence:**

> Agent: What's your email address?
>
> Caller: john dot smith at gmail dot com.
>
> Agent: J-O-H-N dot S-M-I-T-H, at gmail dot com — got it.

**On low confidence — explicit letter-by-letter for the local part, spell-out for the domain:**

> Agent: Just to confirm — J, O, H, N, dot, S, M, I, T, H, at gmail dot com — is that right?

**Tier-1 repair on miss:**

> Agent: Sorry, missed part of that — what's the email again?

**Tier-2 repair (constrained, second miss):**

> Agent: Could you say it letter by letter for the bit before the at-sign?

**Soft check on apparent inconsistency** (couples with E02 — name vs email mismatch):

> Agent: Quick check — I've got Sarah Jones as the patient and john dot smith at gmail dot com as the email. Is that the right email for this booking, or should it go somewhere else?

## Voice example — alternatives

**Skip email entirely; use phone only.** If the platform can SMS confirmations, email is redundant. Drop the field.

**Cross-modal handoff for verification:**

> Agent: I'll send a quick verification email — once you've clicked the link in it, just say "got it" and I'll continue.

Verify SMS/email integration before promising.

**Spell-back digit-by-digit including the domain:** for medical or legal records where any error is unacceptable.

> Agent: That's J-O-H-N, dot, S-M-I-T-H, at, G-M-A-I-L, dot, C-O-M — right?

## Anti-patterns

- **Reading the literal "@" symbol as "at-symbol".** Always use "at".
- **Reading "dot" inconsistently as "period" or "full stop".** Pick one — "dot" is the voice-UX standard.
- **Stating the format prescription on first ask.** "Must contain exactly one at-symbol, a domain, and a recognised top-level domain" — voice users can't reverse-parse this.
- **Validation error voiced verbatim.** "The email address you provided appears to be invalid" — replace with Tier-1 repair.
- **Asking the caller to spell it from the start when they're competent.** If the caller spoke clearly and the local part has obvious-letter content, implicit echo is enough.

## Where it lives

- Phase 2 of booking topics.
- No-availability callback flow.
- Variables: `patient_email`, `customerEmail`.
- Validation logic / save action.
