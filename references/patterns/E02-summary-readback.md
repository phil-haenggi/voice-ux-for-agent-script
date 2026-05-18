---
id: E02
name: summary-readback
category: output-presentation
severity: high
applies_to: [migrate, optimize]
couples_with: [A04, D03]
detection:
  - structural: "summary uses labelled-list format (Name: X, Email: Y...)"
    in: [instructions, response_templates]
  - regex: '\*\*Name:\*\*|\*\*Email:\*\*|\*\*DOB:\*\*'
    in: [response_templates]
  - keyword: "Here is a summary"
    in: [response_templates]
principle_refs: [P2, P9]
pattern_refs: [T-grounding-money]
---

# Summary read-back

## Why it matters

Chat summaries are labelled lists ("Name: X, Email: Y, Phone: Z, …") that a chat user can scan. Voice users hear the labels as redundant noise — every "Name:" / "Email:" / "DOB:" is dead time before the actual value. Worse, the labels signal **schema, not story**: the caller is being asked to verify a database row instead of a booking.

The voice fix is **prose**: read the values in the order and form a person would say them naturally, ending with the question (P9). Email full read-back also raises a privacy concern on speakerphone — consider partial masking.

This pattern also enforces D03 (DOB read-back in spoken form, not ISO).

## Detection

Source has a Phase 3 (or equivalent) summary that:
- Uses labelled fields ("Full Name:", "Email:", "DOB:", "Phone:", "Payment:")
- Renders as Markdown bullets, numbered list, or HTML
- Reads the ISO DOB form directly
- Reads the full email aloud

## Chat example (before)

```
"Here is a summary of the details collected:
- **Full Name:** Bunly Lay
- **Address:** Main Street 12, London
- **Email:** John.smith@gmail.com
- **Gender:** Male
- **DOB:** 1990-01-01
- **Phone:** +441234567890
- **Payment:** Self Pay
Is everything correct?"
```

## Voice example (after) — recommended

**Read as natural prose, lead with the appointment, use the spoken DOB:**

> "Right, let me read that back. Bunly Lay, born first of January nineteen-ninety, on the number ending two-three. The booking's with Andrew McLeod at Newcastle, Tuesday the fifth of May at five-thirty, two hundred and fifty pounds. Self-pay. All correct?"

Order matters: lead with what the caller cares about most (the appointment), then identity, then payment. Terminate with the explicit yes/no — this is an irreversible-action checkpoint (T-grounding-money).

## Voice example — alternatives

**Full read-back when privacy isn't a concern** (internal use, no speakerphone risk):

> "Bunly Lay, first of January nineteen-ninety, oh-seven-double-zero, nine-double-zero, one-two-three, john dot smith at gmail dot com, fourteen Main Street in London. Booked with Andrew McLeod at Newcastle, Tuesday at five-thirty, two-fifty self-pay. All correct?"

Loses privacy protection but covers everything.

**Send summary via SMS/email** (cross-modal, T-grounding):

> "I'll text the full booking details now — once you've had a look, just say 'all correct' and I'll book."

Verify SMS integration. Useful when the booking has many fields.

**Skip non-critical fields:**
- Email: "on your usual email" (if known) or omit.
- Address: read only city ("at your London address") if line 1 is sensitive.
- Phone: last 3 digits only ("on the number ending 210").

## Anti-patterns

- **Reading the labels.** "Name colon Bunly Lay, Email colon John dot Smith…" The labels are the chat-shaped scaffolding; voice has prose.
- **Reading the DOB in ISO.** "Nineteen-ninety, oh-one, oh-one." Use `patient_dob_spoken`. (Couples with D03.)
- **Reading the full email.** Privacy violation on speakerphone, also boring. Use partial mask, "your usual email", or skip.
- **Reading the phone number digit-by-digit in the summary.** It's already been confirmed at capture (D04). Last 3 digits is enough at summary time.
- **Asking "is everything correct?" without reading the values.** Caller has nothing to verify against. Read first, then ask.
- **Asking after the values without explicit yes/no.** "All correct?" works; "Looks good?" works. "Anything you want to change?" is wishy-washy — the caller may say "no, looks fine" meaning "no changes" but the agent treats as decline.

## Where it lives

`reasoning.instructions` of the summary phase (typically `Appointment_Management` Phase 3).

## Mis-applications (optimize mode)

- **Pattern: voice script drops labels but still reads all 7 fields in flat order.** Better than chat but still verbose. Lead with the most important; mask non-critical.
- **Pattern: voice script reads the DOB in spoken form but the next phase (T&Cs) re-reads it as ISO.** Audit every read-back.
- **Pattern: voice script reads the email "to be safe" even though the caller is in public.** No privacy guard. Default to partial.
- **Pattern: voice script asks "is that right?" after each field instead of one summary check.** Slow — the summary is one check, not seven.
