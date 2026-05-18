---
id: A02
name: confirmation-rule
category: system-instructions
severity: medium
applies_to: [migrate, optimize]
detection:
  - keyword: "Never proceed on a vague response"
    in: [instructions]
  - keyword: "do not interpret 'yes'"
    in: [instructions]
  - keyword: "only accept explicit textual responses"
    in: [instructions]
principle_refs: [P2, P10]
pattern_refs: [T-grounding]
---

# Confirmation rule (vague vs. natural)

## Why it matters

Voice callers speak in natural affirmatives — "yeah", "sure", "go ahead", "that's right", "perfect" — and natural negatives — "nah", "not really", "no thanks". Forcing a literal "yes" or "no" feels broken and slows the flow. The legitimate concern (don't proceed on ambiguity) is real, but the chat-shaped solution (treat all single-word affirmatives as ambiguous) is wrong for voice. The right rule is field-type-aware grounding (T-grounding): explicit re-confirmation only on irreversible actions.

## Detection

Source contains a directive like:
- "Never proceed on a vague response such as 'yes', 'no', or 'sure'"
- "do not interpret 'yes' or 'no' as confirmation"
- "only accept explicit textual responses"
- "If the response is ambiguous or numeric-only, prompt the user again"

These almost always appear in the global `system.instructions` of healthcare/booking agents.

## Chat example (before)

```
CRITICAL RULE: Never proceed on a vague response such as 'yes', 'no', or 'sure'
when a specific choice is needed. When asking the user to confirm or refuse,
only accept explicit textual responses. Do not interpret numeric inputs such as
0 or 1 as yes or no. If the response is ambiguous or numeric-only, prompt the
user again with a clear question.
```

## Voice example (after) — recommended

```
Accept any natural affirmative ('yes', 'yeah', 'sure', 'go ahead', 'that's
right', 'please do') as confirmation, and any natural negative ('no', 'nah',
'not really', 'no thanks') as refusal — when the user's intent is unambiguous
in context. Re-prompt only when the reply is genuinely ambiguous between two
specific choices the agent just offered. For irreversible actions (booking
commit, T&Cs acceptance, payment, age confirmation), always require an
explicit yes/no — apply a candidate-understanding repair on anything else.
```

## Voice example — alternatives

**Strict only at commit:** keep the strict rule, but scope it to irreversible turns. Everywhere else, accept natural language. This preserves the original author's caution while making routine confirmations smooth.

**Whitelist + ambiguity list:** define an explicit ambiguous-words list ("ok", "alright", "fine", "sure" — these mean neither yes nor no in context) and trigger Tier-2 repair only on those. Affirmatives and negatives outside the list pass through.

## Anti-patterns

- **Treating "ok" as confirmation.** "OK" is genuinely ambiguous in voice — it's often a continuer, not a yes. The rule should keep "ok" in the ambiguous bucket.
- **Treating "ok" as refusal.** Same — neither.
- **Accepting "sure" on irreversible commits.** Booking confirmations, age checks, T&Cs — these still need explicit yes/no with a candidate-understanding loop.
- **Stripping the rule entirely.** Without any guidance, the agent will accept anything as confirmation. Replace, don't delete.

## Where it lives

`system.instructions` (global) and per-topic `system.instructions` where it's been duplicated.

## Mis-applications (optimize mode)

- **Pattern: voice script accepts "ok" as yes everywhere.** Common when migrating in a hurry. Run the candidate-understanding repair on "ok" in irreversible-action turns.
- **Pattern: voice script keeps the strict chat rule globally.** Annoying for the user; surfaces as `[changed]` even in optimize mode unless there's a strong intentionality signal.
- **Pattern: voice script has the right rule but doesn't define what "ambiguous" means.** The LLM defaults inconsistently. Add the explicit ambiguous-words list.
