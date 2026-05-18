---
id: E04
name: speciality-list-enumeration
category: output-presentation
severity: medium
applies_to: [migrate, optimize]
detection:
  - structural: "topic instructions enumerate 10+ specialities/categories"
    in: [instructions]
  - regex: 'Anaesthetics.*Cardiology.*Dermatology'
    in: [instructions]
principle_refs: [P1, P6]
---

# Speciality / category list enumeration

## Why it matters

Booking and information topics often list every supported speciality/category in instructions ("Anaesthetics, Cardiology, Cardio-Thoracic Surgery, Dermatology, ENT, …"). In chat this is harmless context for the LLM. In voice, two failure modes:

1. **The list is for the LLM and never voiced.** Source instruction says "NEVER display this list to the user" — fine in chat, but in voice the LLM occasionally leaks the list into the response. Each leak is a 30-second read.
2. **The list is voiced as a menu.** Worse — the LLM reads all 22 specialities and asks the user to pick. Hostile.

Most users know what they want ("a cardiologist", "an orthopaedic appointment"). The list exists to map their term to a canonical speciality. The mapping should be silent.

## Detection

Source has a topic instruction listing 10+ specialities (or categories, or insurer names, or any large enumerable set) followed by mapping logic.

## Chat example (before)

```
| Here are the specialities for which appointments can be booked: Anaesthetics,
| Cardiology, Cardio-Thoracic Surgery, Dermatology, ENT, General Surgery, GP,
| Gynaecology, Medicine, Neurosurgery, Oncology, Ophthalmology, Oral &
| Maxillo-Facial Surgery, Orthopaedics, Paediatrics, Pathology, Plastic Surgery,
| Psychiatry, Radiology, Rheumatology, Sports Medicine, Urology. NEVER display
| this list to the user. Accept the user's input and map it internally to the
| supported specialities.
```

## Voice example (after) — recommended

**Strengthen the silent-map directive. Add an explicit fallback for unsupported terms:**

```
| Supported specialities (NEVER read aloud — this is for internal mapping only):
| Anaesthetics, Cardiology, Cardio-Thoracic Surgery, Dermatology, ENT, General
| Surgery, GP, Gynaecology, Medicine, Neurosurgery, Oncology, Ophthalmology,
| Oral & Maxillo-Facial Surgery, Orthopaedics, Paediatrics, Pathology, Plastic
| Surgery, Psychiatry, Radiology, Rheumatology, Sports Medicine, Urology.
|
| Map the caller's term internally. If no match, voice EXACTLY: "That's not one
| I can book online. Want me to put you through to a support adviser who can
| help?"
```

**The agent never voices the supported list, even on no-match.**

## Voice example — alternatives

**Top-N most common as a fallback hint:**

> Agent: We see most callers for cardiology, dermatology, or orthopaedics — does any of those sound like what you need, or something else?

Use only as a hint when the caller is genuinely unsure. Never as a primary menu.

**Specialised topic for unfamiliar terms:** route low-frequency speciality requests to a separate human-handover path rather than trying to disambiguate in voice.

## Anti-patterns

- **Reading all 22 specialities.** The hostile-menu case.
- **Reading the supported list when the caller's term doesn't match.** "I don't have that — but here's what I do have: anaesthetics, cardiology, …" Equally hostile, just delayed.
- **Asking the caller to "pick one of our specialities".** Voice users don't know your taxonomy.
- **Splitting the list into smaller groups and reading them across multiple turns.** Same problem, distributed.

## Where it lives

`reasoning.instructions` of the topic that does the speciality mapping (typically `Appointment_Management` Phase 1).

## Mis-applications (optimize mode)

- **Pattern: voice script voiced the speciality list once in the past and the LLM still does it intermittently.** Strengthen the directive to "NEVER under any circumstances read this list".
- **Pattern: voice script's no-match copy lists the supported specialities.** Same anti-pattern, dressed as helpfulness. Replace with a clean transfer offer.
- **Pattern: voice script enumerates insurers, hospitals, or other large lists.** Same fix — silent map, transfer on no-match.
