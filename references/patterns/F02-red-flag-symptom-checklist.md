---
id: F02
name: red-flag-symptom-checklist
category: crisis-and-safety
severity: high
applies_to: [migrate, optimize]
detection:
  - structural: "topic reads a numbered checklist of symptoms"
    in: [instructions, response_templates]
  - keyword: "chest pain"
    in: [instructions, response_templates]
  - keyword: "experiencing any of the following symptoms"
    in: [instructions, response_templates]
principle_refs: [P1, P6]
---

# Red-flag symptom checklist

## Why it matters

Healthcare-booking agents commonly read a 9-item checklist of red-flag symptoms before allowing booking ("Are you experiencing chest pain, palpitations with breathlessness, sudden difficulty breathing, …?"). In chat the user can scan and tick mentally. In voice it's a 30+ second monologue of distressing medical conditions, ending in a yes/no the user has lost track of.

Two failure modes:
1. **Caller hangs up partway through.** The clinical safety check fails because the caller never confirmed.
2. **Caller says "yes" thinking they have to acknowledge it was read.** The agent then refuses booking and routes to NHS 999/111. Wrong outcome.

The fix is **two-step**: short summary check first, full list only if the caller asks. Most callers can identify whether they have an urgent symptom from a 4-item summary.

Note: substance is **clinical-governance** territory. The two-step structure must be signed off by clinical governance before deploy.

## Detection

Source has a topic that reads a long symptom list. Look for: 5+ items, "Are you experiencing any of the following symptoms?", phrases like "sudden onset chest pain".

## Chat example (before)

```
| Otherwise ask the user exactly: "Before we continue, are you currently
| experiencing any of the following symptoms? If yes, please do not continue
| your online booking and contact your GP or NHS 999/111.
| 1. Sudden onset chest pain/heaviness in your chest.
| 2. Heart palpitations with difficulty in breathing.
| 3. Sudden difficulty in breathing.
| 4. Seizure/fitting affecting consciousness and ongoing symptoms.
| 5. Severe allergic reaction with breathing difficulties or swelling of the
|    mouth.
| 6. Sudden onset neurological changes such as weakness, slurring of speech,
|    drowsiness, sudden onset severe headache in the back of the head or neck
|    stiffness with fever.
| 7. Uncontrollable bleeding or a significant injury/accident.
| 8. Pregnancy-related concerns.
| 9. Feeling suicidal – If you are considering harming yourself please contact
|    NHS111 or the Samaritans 116 123."
```

## Voice example (after) — recommended

**Two-step: short summary first, full list on caller request:**

**Step 1 (default):**

> "Before we book, a quick safety check — are you having any urgent symptoms right now, like chest pain, difficulty breathing, severe bleeding, or thoughts of self-harm?"

**Step 2 (only if caller asks "what counts" / "read me the full list"):**

> "There's chest pain or heaviness in the chest, palpitations with breathlessness, sudden difficulty breathing, or a seizure. [pause] There's also severe allergic reactions with breathing trouble, sudden weakness or slurred speech or a severe headache, uncontrollable bleeding or a major injury, pregnancy concerns, or thoughts of self-harm. [pause] Any of those — yes or no?"

Two chunks of 4 + 5 with a pause between, ending with explicit yes/no.

**On any "yes" — voice the urgent-symptoms response (couples with F01):**

> "Please don't book today. Contact your GP or call NHS one-one-one. If it's an emergency, call nine-nine-nine. If you're feeling suicidal, you can call the Samaritans free, any time — that's one-one-six, one-two-three. Take care."

## Voice example — alternatives

**Single open question, rely on LLM to detect symptoms in the reply:**

> "Before we book — anything urgent going on for you health-wise right now?"

Then the LLM scans the reply for any of the 9 symptoms (using internal mapping). Faster but less defensible — clinical governance may want the list voiced explicitly.

**Skip the safety check entirely in non-medical contexts.** This pattern is healthcare-specific. Don't apply it to non-medical booking flows.

## Anti-patterns

- **Reading the full 9-item numbered list.** Hostile and slow.
- **Asking yes/no without the substance.** "Are you experiencing any of the symptoms we list?" — what symptoms? The caller doesn't know.
- **Mixing the safety check with other booking questions.** "Quick safety check, and what's your postcode?" — bundles a safety-critical question with a routine one. Always isolate.
- **Trusting "no" as confirmation when the caller didn't seem to be listening.** If the caller responded too fast (<500ms), consider asking again at Tier-2.

## Where it lives

`reasoning.instructions` of the booking topic, gating Phase 1 entry (typically `Appointment_Management`).

## Mis-applications (optimize mode)

- **Pattern: voice script does the two-step but the full-list version isn't gated on caller request.** Reading the full list to every caller defeats the purpose.
- **Pattern: voice script offers the full list but doesn't chunk it.** 9 items in one breath is still hostile.
- **Pattern: short summary doesn't include "thoughts of self-harm".** Misses item 9 from the chat list. Re-include — it's the reason the crisis-redirect path even exists for this flow.
- **Pattern: voice script proceeds on "yeah" silently after the safety check.** Should be explicit yes/no with Tier-2 repair on ambiguity.
