# Key-Term Prompting — output skeleton

Generated as a side artifact when Phase 5 (or optional Phase 7) detects pattern H05. Like the pronunciation dictionary, this is a starter list for the human reviewer to verify and load into the org's STT vocabulary / context biasing configuration.

Suggested filename: `_local/generated/[agent-name]-key-term-prompting.md`

---

```markdown
# Key-Term Prompting — [agent-name]

> ⚠️ **Starter list — verify recognition with sample utterances before deploy.**
>
> These are domain-specific terms the caller is likely to **say** during the
> conversation. Loading them as STT context biasing (or "hot-words", "custom
> vocabulary") raises their prior probability during recognition. Test each
> with sample utterances in the platform's STT preview before deploy.

**Generated:** [YYYY-MM-DD]
**Source agent:** [path to .agent file]
**STT engine:** [confirm with platform team — Google Speech, ElevenLabs STT, AWS Transcribe, etc.]
**Format:** [confirm — plain word list, JSON, weighted hot-words, etc.]

---

## Term lists

### Insurers

```
AXA
Aviva
Bupa
Vitality
WPA
Cigna
Allianz
Healix
[...]
```

### Hospitals / locations

```
Newcastle
Guildford
Highgate
Chichester
Tunbridge Wells
[...]
```

### Specialities

```
Anaesthetics
Cardiology
Cardio-Thoracic Surgery
Dermatology
ENT
General Surgery
GP
Gynaecology
Medicine
Neurosurgery
Oncology
Ophthalmology
Oral & Maxillo-Facial Surgery
Orthopaedics
Paediatrics
Pathology
Plastic Surgery
Psychiatry
Radiology
Rheumatology
Sports Medicine
Urology
```

### Postcode patterns

UK postcode format hint: `^[A-Z]{1,2}[0-9]{1,2}[A-Z]?\s?[0-9][A-Z]{2}$`

If the platform supports regex-based biasing, add this. If not, the STT will need to be tested with sample postcodes — common errors include "GU" → "DU" / "G E U", "PZ" → "B Z" / "P Zee".

### Consultant names

[Generated from the org's consultant directory if accessible. Otherwise, leave empty and add to periodic refresh.]

---

## Verification checklist

- [ ] Test each insurer name with a sample utterance ("I have AXA insurance").
- [ ] Test each speciality with a sample utterance ("I want to see a cardiologist", "an orthopaedic appointment").
- [ ] Test postcode capture with 5-10 representative UK postcodes (different formats).
- [ ] If the platform has a per-call hot-words limit (e.g., 100 max), prioritise: postcodes > specialities > insurers > hospitals > consultants.
- [ ] Verify recognition confidence improves vs. baseline (without biasing).

---

## Coverage report

| Category | Term count | Loaded? | Verified? |
|---|---|---|---|
| Insurers | N | [ ] | [ ] |
| Hospitals | N | [ ] | [ ] |
| Specialities | N | [ ] | [ ] |
| Consultants | N | [ ] | [ ] |
| Postcode patterns | N | [ ] | [ ] |

---

## Refresh process

Add to a recurring refresh:
- New insurers / partner additions
- New consultants entering the network
- New hospital openings
- New specialities supported

Recommend re-generating this list quarterly — the STT engine's biasing only helps if the list reflects current vocabulary.

---

## Coupling with pronunciation dictionary

Terms in this list (caller-spoken) and the pronunciation dictionary (agent-spoken) should overlap meaningfully. If a term appears in only one list, that's worth investigating:
- Term in pronunciation dictionary but not in key-term prompting → caller may struggle to be understood when saying it back to the agent.
- Term in key-term prompting but not in pronunciation dictionary → agent may mispronounce the term it expects the caller to say.

Cross-check both lists before deploy.
```
