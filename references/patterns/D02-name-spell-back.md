---
id: D02
name: name-spell-back
category: input-collection
severity: high
applies_to: [migrate]
detection:
  - keyword: "first name"
    in: [instructions]
  - keyword: "last name"
    in: [instructions]
  - keyword: "full name"
    in: [instructions]
  - structural: "name is collected without spell-back"
    in: [instructions]
principle_refs: [P2, P10]
pattern_refs: [T-grounding]
---

# Name spell-back

## Why it matters

Names appear on records. STT errors here cause downstream identity mismatches (booking under "Smith" when the patient is "Smyth"). Names are particularly STT-hostile because:
- Apostrophes and hyphens often go uncaptured ("O'Connor" → "Oconnor", "Smith-Jones" → "Smith Jones")
- Foreign-origin names mismatch local pronunciation models
- Common-sounding names blur ("Jon" / "John", "Anne" / "Ann", "Grey" / "Gray")
- Diacritics are typically stripped silently

Names are also high-stakes for trust: callers notice when their own name is misspelled in a confirmation email.

## Detection

Source has a topic that collects free-text names (first, last, or full) without an explicit spell-back step. Look for: `save_patient_name`, `patient_first_name`, `patient_last_name`, `patient_full_name`, or instructions that say "ask for the patient's name" without follow-up confirmation.

## Chat example (before)

```
| Ask the user for their full name and save it via save_patient_name.
```

(Trusts the chat input verbatim.)

## Voice example (after) — recommended

**Single ask, confirm only on low ASR confidence:**

> Agent: What's the name on the booking?
>
> Caller: Sarah Jones.
>
> Agent: Sarah Jones — got it.

**On low confidence — letter-by-letter spell-back of the surname:**

> Agent: What's the name on the booking?
>
> Caller: [unclear] Sarah Jones.
>
> Agent: Just to confirm — that's S, A, R, A, H, then J, O, N, E, S — is that right?

Pronounce apostrophes and hyphens explicitly:

> "That's O, apostrophe, C, O, N, N, O, R — is that right?"

> "That's S, M, I, T, H, hyphen, J, O, N, E, S?"

## Voice example — alternatives

**Spell-back only the surname.** Surname mismatches matter most for record-keeping; first names are lower-stakes.

**Skip spell-back if not on a medical/legal record.** If the name only appears in agent-side ack ("nice to meet you, Sarah") and not in any persisted system, skip the confirmation.

**CTI-seeded name (no collection needed).** If caller-line-ID matched a CRM contact, the agent already has the name — confirm rather than collect:

> Agent: I've got Sarah Jones on the account — is the booking for you, or for someone else?

## Anti-patterns

- **Spelling first AND last name on every booking by default.** Slow. Use confidence-driven escalation.
- **Reading the full spelled name back without pauses.** "S-A-R-A-H-J-O-N-E-S" runs together. Use pauses between syllables and between names.
- **Asking the caller to spell their name.** "Could you spell that for me?" — chat-shaped solution. If you need spelling, do the spelling yourself ("S, A, R, A, H — right?") so the caller is confirming, not labouring.
- **Silently accepting an obviously misheard name.** "Bunly" misheard as "Bonnie" — saving silently means the booking confirmation goes to the wrong person.

## Where it lives

Topic instructions where name is collected (typically `Appointment_Management` Phase 2 step A or earlier).
