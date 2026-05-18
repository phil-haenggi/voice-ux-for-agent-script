---
id: E01
name: slot-list-presentation
category: output-presentation
severity: high
applies_to: [migrate, optimize]
couples_with: [A01]
detection:
  - structural: "topic presents 3+ slots/options as a list"
    in: [instructions]
  - regex: '<ol|<li>|<b>Consultant'
    in: [instructions, response_templates]
  - keyword: "Please select a slot"
    in: [instructions]
  - keyword: "providing the corresponding number"
    in: [instructions]
principle_refs: [P1, P6, P9]
pattern_refs: [T-translate-6, T-translate-1]
---

# Slot/option list presentation

## Why it matters

Voice users can't scan a list. Reading 4+ time-stamped slots and asking the caller to remember a number maps the chat UX to voice with no adaptation. By the time the caller hears "option 4: Tuesday the twelfth at seven", they've forgotten "option 1: Tuesday the fifth at five-thirty".

The fix is **progressive disclosure**: narrow by salient axis (day → time → consultant) one decision at a time. A01 (numbered-list rule) is the system-level rule; E01 is the operational pattern for slot lists specifically.

## Detection

Source has:
- A topic that presents 3+ slots
- Slot list structured as a numbered or HTML list
- Closing copy like "Please select a slot by providing the corresponding number"
- HTML markup wrapping consultant headers (`<b>Consultant: …</b>`)

## Chat example (before)

```
"Here are the available slots with Cardiology consultants near your location:
<b>Consultant: Andrew McLeod at Newcastle Hospital (£250.00 / 30 min)</b>
<ol start=\"1\">
<li>05 May 2026 at 5:30 PM</li>
<li>05 May 2026 at 6:00 PM</li>
<li>05 May 2026 at 6:30 PM</li>
<li>12 May 2026 at 7:00 PM</li>
</ol>
Please select a slot by providing the corresponding number."
```

## Voice example (after) — recommended

**Progressive disclosure — group by day first, then narrow times:**

> Turn 1 (group by day):
> Agent: I've got slots on Tuesday the fifth of May, and Tuesday the twelfth. Which day suits you?
>
> User: The fifth.
>
> Turn 2 (narrow times for chosen day, max 3-4):
> Agent: On Tuesday the fifth, I've got five-thirty, six o'clock, or six-thirty in the evening. Which one?
>
> User: Five-thirty.
>
> Turn 3 (read-back after pick — couples with A07):
> Agent: That's Andrew McLeod at Newcastle, Tuesday the fifth of May at five-thirty in the afternoon, two hundred and fifty pounds. Shall I take your details?

Accept natural references: "the earliest", "the first one", "the evening one", "five-thirty". Map to slot internally.

**If multiple consultants on the chosen day — narrow consultant first, then times:**

> Agent: On Tuesday the fifth, I've got slots with Andrew McLeod or with Sarah Patel. Who would you like?

## Voice example — alternatives

**Top-match plus "hear more":** when one slot is the obvious recommendation:

> Agent: The earliest is Tuesday at five-thirty with Andrew McLeod at Newcastle. Want that one, or hear other times?

**Sequential one-at-a-time** (when each slot needs explanation):

> Agent: Tuesday the fifth at five-thirty — works for you?
>
> [if no]
>
> Agent: Six o'clock?

**Single-day flow** (skip day-narrowing if all slots fall on one day):

> Agent: I've got three on Tuesday the fifth — five-thirty, six, or six-thirty. Which?

## Anti-patterns

- **Reading all slots in one turn ("Tuesday at 5:30, Tuesday at 6, Tuesday at 6:30, Tuesday at 7…").** P1 (chunking) violation. The caller has forgotten the first slot by slot 4.
- **Asking for a slot number after voicing the slots.** "…please give me the corresponding number." There's nothing to correspond to in voice.
- **Reading the price for every slot.** "Tuesday at 5:30, two hundred and fifty pounds. Tuesday at 6, two hundred and fifty pounds." Tedious. Voice price once during read-back of the chosen slot (couples with A06).
- **Reading the consultant header and times in one breath without pause.** "Andrew McLeod at Newcastle Hospital, two hundred and fifty pounds for thirty minutes, Tuesday at five-thirty, six o'clock, six-thirty…" Loses structure.
- **Skipping the read-back after pick.** P9 / T-grounding violation — without read-back, no implicit echo of the selection.

## Where it lives

`reasoning.instructions` of the slot-presenting topic (typically `Appointment_Management` Phase 1).

## Mis-applications (optimize mode)

- **Pattern: voice script does day grouping but reads all times in the day group.** "On Tuesday I've got five-thirty, six, six-thirty, seven, seven-thirty." Cap at 3-4. If more, ask "want me to read more?" before continuing.
- **Pattern: progressive disclosure exists but the read-back after pick is missing.** No grounding loop.
- **Pattern: voice script accepts "the second one" but not "five-thirty".** Should accept either — natural-language reference is what voice users do.
- **Pattern: voice script repeats the entire slot list on Tier-1 repair.** Caller said "the second one"; agent says "Sorry, didn't catch that — let me read them again: I've got Tuesday the fifth at five-thirty, six, six-thirty…". Just ask for the time directly.
