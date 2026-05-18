---
id: A07
name: slot-selection-collapse
category: system-instructions
severity: medium
applies_to: [migrate]
couples_with: [E01]
detection:
  - structural: "topic has confirm-then-act sequence on slot selection"
    in: [instructions]
  - keyword: "Display selected slot summary"
    in: [instructions]
  - keyword: "ask user to confirm"
    in: [instructions]
principle_refs: [P8, P9]
---

# Slot/option selection collapse

## Why it matters

Chat booking flows commonly have a three-step pattern: (1) display the selected slot summary, (2) ask the user to confirm, (3) call the slot-details action. In chat this is friendly redundancy — the user can re-read the summary. In voice it's three turns where one would do, and the second turn ("is that right?") almost always gets a redundant confirmation. The user's selection is already a confirmation; an extra "are you sure?" turn slows the call without adding signal.

Note: this rule applies to **slot selection**, not to **booking commit**. Final commit (`AgentForce_Appointment_Booking`, payment, T&Cs acceptance) is irreversible and still gets explicit summary + check (T-grounding).

## Detection

Source has a topic with this sequence:

```
- Caller picks a slot (e.g., "the second one")
- Agent displays selected slot summary
- Agent asks "Is this correct?" / "Confirm to proceed?"
- Agent calls collect_slot_details
```

The middle "ask to confirm" is what this pattern strips.

## Chat example (before)

```
| As soon as user selects a slot, display the selected slot summary:
|   "You've selected: Dr Smith at Newcastle, Tuesday at 5:30, £250."
| Then ask: "Is this correct?"
| If user confirms, call collect_slot_details.
```

## Voice example (after) — recommended

**Collapse the redundant confirmation. Acknowledge the pick and move on:**

```
| As soon as the caller picks a slot, immediately call collect_slot_details
| with the picked option. While the action runs, voice ONE acknowledgment
| from the phrasebook ('Got it.', 'Right.'). After the action returns, voice
| a single read-back in spoken English: "That's [consultantName] at
| [hospital], [dateAndTime_spoken], [appointmentCost_spoken] — shall I take
| your details?" The caller's pick is their confirmation; the read-back
| serves as implicit echo (T-grounding for low-stakes pre-commit fields).
```

> Caller: The earliest one.
>
> Agent: Got it. [collect_slot_details runs] That's Andrew McLeod at Newcastle, Tuesday the fifth at five-thirty, two hundred and fifty pounds. Shall I take your details?

## Voice example — alternatives

**Skip even "Got it." for compactness:** if the action call is fast (<1s), drop the acknowledgment entirely:

> Caller: The earliest one.
>
> Agent: That's Andrew McLeod at Newcastle, Tuesday the fifth at five-thirty, two hundred and fifty pounds. Shall I take your details?

**Add explicit confirmation only at high-value commits.** Keep the confirm-then-act pattern for booking commit / payment / T&Cs — those are irreversible and need explicit yes/no.

## Anti-patterns

- **Reading the summary, then asking "is this correct?", then calling the action.** The voice equivalent of the chat pattern — too many turns.
- **Calling the action silently with no acknowledgment AND no read-back.** The user is left wondering if anything happened during the latency. Either acknowledge before the call, or read back after.
- **Reading the summary as a numbered list ("1. Consultant: …, 2. Hospital: …").** Stacks A07 with A01 / E01 anti-patterns. Use prose.

## Where it lives

`reasoning.instructions` of the slot-selection topic (typically `Appointment_Management` Phase 1). The pattern lives near the `collect_slot_details` invocation.

## Mis-applications (optimize mode)

Optimize mode rarely sees this — voice scripts that already collapsed the confirmation usually got it right. If detected, it's almost always because the script was migrated by removing the chat copy but leaving the chat structure. Look for a still-present "is that correct?" on slot pick (vs. on commit).
