# Pronunciation Dictionary — output skeleton

Generated as a side artifact when Phase 5 (or optional Phase 7) detects pattern H04. Not a full deliverable on its own — it's a starter list for the human reviewer to verify in voice preview before loading into the org's voice settings.

Suggested filename: `_local/generated/[agent-name]-pronunciation-dictionary.md`

---

```markdown
# Pronunciation Dictionary — [agent-name]

> ⚠️ **Starter list — verify in voice preview before deploy.**
>
> Every entry is a candidate based on terms found in the agent's user-visible
> content + topic instructions. The IPA / phoneme strings below are best-effort
> defaults; the actual TTS engine's interpretation may differ. Load these into
> Agentforce Builder → Voice Settings → Pronunciation Dictionary, then run a
> voice preview against representative utterances.

**Generated:** [YYYY-MM-DD]
**Source agent:** [path to .agent file]
**Voice settings reference:** [voice_id from H03, e.g. "en-GB-Wavenet-B"]
**Engine format:** [IPA / CMU / ARPAbet — confirm with platform team]

---

## Entries

### Brand and product names

| Term | IPA | Source location | Notes |
|---|---|---|---|
| [Brand1] | [phonemes] | system.welcome, multiple topics | Mispronounces by default — verify. |
| [Brand2] | [phonemes] | response_templates | Foreign origin; engine may default to source-language pronunciation. |

### Locations / hospitals

| Term | IPA | Source location | Notes |
|---|---|---|---|
| [City1] | [phonemes] | hospitals output | Stress varies. |
| [Town2] | [phonemes] | hospitals output | Often mispronounced in en-US engines. |

### Specialities / domain terms

| Term | IPA | Source location | Notes |
|---|---|---|---|
| [Speciality1] | [phonemes] | speciality list | Greek/Latin root — verify. |
| [Speciality2] | [phonemes] | speciality list | Hyphenated; engine may split. |

### Insurer / partner names

| Term | IPA | Source location | Notes |
|---|---|---|---|
| [Insurer1] | [phonemes] | find_insurer output | Acronym; spell-out vs. say-as. |

---

## Verification checklist

Before loading into the org:

- [ ] Test each term in voice preview with sample sentences.
- [ ] If the engine doesn't accept IPA, regenerate using the engine's required format (CMU/ARPAbet/etc.).
- [ ] Verify each term in the actual sentence context — pronunciation can shift in connected speech.
- [ ] Confirm the dictionary doesn't conflict with any user-spoken inputs (key-term prompting biases STT, pronunciation dictionary biases TTS — they should align).
- [ ] Add to a periodic refresh process — new consultants, new hospitals, new insurers will need additions.

---

## Coverage report

| Category | Total terms found | Listed in dictionary | Skipped (standard pronunciation) |
|---|---|---|---|
| Brands | N | N | N |
| Locations | N | N | N |
| Specialities | N | N | N |
| Insurers | N | N | N |

Terms skipped because their default pronunciation is acceptable: [list].

---

## Out of scope

- Caller-spoken vocabulary (STT bias) — see `key-term-prompting.md` for that side artifact.
- General-English vocabulary — only domain-specific terms enter this dictionary.
```
