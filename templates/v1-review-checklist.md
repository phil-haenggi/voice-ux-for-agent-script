# V1 Review Checklist — output skeleton

Generated as a side artifact at the end of Phase 5 (or optional Phase 7 if generating a `.agent` file). Mandatory items the human reviewer must check before deploy. Annotated to reflect what was applied / skipped in this specific migration.

Suggested filename: `_local/generated/[agent-name]-v1-review-checklist.md`

---

```markdown
# V1 Review Checklist — [agent-name]

> ⚠️ **V1 baseline, not ship-ready.** Every item below is mandatory before deploy.
> Your business context, compliance requirements, and edge cases require human
> judgment. The skill produces a starting point, not a guarantee of correctness.

**Generated:** [YYYY-MM-DD]
**Source agent:** [path]
**Voice agent:** [path or bundle name]
**Mode:** migrate / optimize
**Modality traits:** barge-in: [y/n], screen fallback: [y/n], SMS: [y/n], carrier announcement: [y/n]

---

## 1. Voice settings (H03)

- [ ] `voice_id` set to a real ID from this org's voice library (not a placeholder)
- [ ] `outbound_speed`, `outbound_stability`, `outbound_similarity` tuned to persona register
- [ ] Voice tested in voice preview against representative utterances (welcome + 3 mid-flow turns)
- [ ] Two-voice opening contrast verified (if applicable — couples with B01)

## 2. Pronunciation Dictionary (H04)

- [ ] All starter terms loaded into Voice Settings → Pronunciation Dictionary
- [ ] Each term tested in voice preview in **sentence context** (not isolated)
- [ ] Domain term refresh process documented

## 3. Key-Term Prompting (H05)

- [ ] Hot-words / context biasing list loaded into the platform's STT config
- [ ] Recognition tested with sample utterances for the top 5 trickiest terms
- [ ] Postcode capture tested with 5+ representative postcodes

## 4. Crisis flow (F01)

- [ ] Crisis copy delivers in slowed prose (SSML rate ~85%)
- [ ] All helpline numbers spoken digit-by-digit (verified in preview)
- [ ] `crisis_detected` latch verified — every subsequent turn re-voices
- [ ] Agent never auto-terminates the call after crisis copy
- [ ] Live counsellor transfer (if offered) goes to a trained team, not the general queue

## 5. AI disclosure and recording notice (B02)

- [ ] AI disclosure present in welcome (system layer or agent layer)
- [ ] Recording-may-be-monitored disclosure complies with [jurisdiction]
- [ ] Caller can ask "am I talking to a person?" and get the right answer

## 6. T&Cs and consent (E03)

- [ ] T&Cs voice script signed off by Legal / Compliance
- [ ] Substantive obligations (cancellation, data sharing) audibly voiced
- [ ] Reference to full text on website included
- [ ] Explicit yes/no required (no "ok" / "sure" acceptance)

## 7. Spell-confirm coverage (D01–D06)

- [ ] Postcode: implicit echo on high confidence, letter-by-letter on low
- [ ] Phone: implicit echo / digit-by-digit logic verified
- [ ] Email: implicit echo / letter-by-letter / SMS handoff path tested
- [ ] DOB: spoken-form companion variable (`patient_dob_spoken`) used in summary
- [ ] Reference numbers (policy, pre-auth): "zero" vs "oh" convention consistent

## 8. Layer E (out-of-`.agent`) items

- [ ] TTS voice contrast for two-voice opening configured (if applicable)
- [ ] SSML support enabled at the runtime layer
- [ ] Barge-in detection threshold tuned
- [ ] Silence / no-input timer configured (4s default)
- [ ] ASR confidence threshold for grounding escalation (start at 0.75)
- [ ] CTI screen-pop mapping for `First_Name`, `Last_Name`, `Postal_Code` (if applicable)
- [ ] Carrier-side pre-call announcement configured (if applicable)
- [ ] CSAT delivery channel (SMS or email) wired up post-call
- [ ] State preservation on Tier-3 human handoff verified (every collected field surfaces in agent screen-pop)

## 9. Pilot testing

- [ ] At least 5 happy-path test calls completed
- [ ] At least 3 unhappy-path test calls (recognition failure, T&Cs decline, under-18, crisis)
- [ ] At least 1 mid-flow detour test (FAQ during booking)
- [ ] At least 1 transfer-to-human test
- [ ] Test results logged with date and reviewer name

## 10. Rollback plan

- [ ] Previous chat agent stays deployed (parallel rollout, not replacement)
- [ ] Voice agent activatable / deactivatable independently
- [ ] Documented rollback procedure if voice agent must be paused

---

## Items applied in this migration

[Auto-populated from the audit — list each `[changed]` entry here as a check.]

- [x] A01 — numbered list rule (system instructions)
- [x] B01 — welcome length (split to two-layer opening)
- [x] D01 — postcode collection (Tier-1/Tier-2 repair added)
- [...]

## Items skipped

[Auto-populated from `[review needed]` and developer overrides during walk-through.]

- [ ] F02 — red-flag symptom checklist kept as 9-item list (clinical governance review pending)

## Items flagged out-of-scope

- Multi-intent context-switch mid-booking — gap in voice library v1
- Emotional de-escalation patterns — gap in voice library v1

---

## Reviewer sign-off

| Section | Reviewer | Date | Notes |
|---|---|---|---|
| Voice settings | | | |
| Crisis flow | | | |
| T&Cs / Compliance | | | |
| Pilot testing | | | |
| Final approval | | | |
```
