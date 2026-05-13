# Telephony patterns reference

Operational patterns for chat→voice migration. Adapted from `Projects/nuffield health/cross cutting telephony patterns.md`. The skill consults this at runtime — do not regenerate, look up.

Citation prefix: **T** (e.g., `T-grounding`, `T-repair-tier-2`).

---

## T-translate — 8 chat→voice translation rules

Direct text-to-voice translation introduces text-shaped scaffolding that doesn't fit voice. Apply these rules to every user-facing string.

| ID | Category | Chat-form | Voice-form |
|---|---|---|---|
| T-translate-1 | Input-shape instructions | "Please reply with yes or no" | (just ask the question) |
| T-translate-2 | Interface verbs | "Click", "Type", "Select", "Submit" | Conversational equivalents |
| T-translate-3 | Transactional register | "Please provide your X" | "What's your X?" / "And your X?" |
| T-translate-4 | Format prescriptions | "in DD-MM-YYYY format" | (just ask; constrain only on repair) |
| T-translate-5 | Visual references | "as shown above", "see below" | Rephrase without visual cues |
| T-translate-6 | Numbered menus | "1. X 2. Y" | "X, or Y?" |
| T-translate-7 | Acknowledgment templates | "Thank you. Now please..." | Rotate varied acks (see T-phrasebook) |
| T-translate-8 | Bundled questions | "Confirm X and Y" | Split into separate turns |

### LLM prompt for batch copy translation

> Convert chatbot text copy to voice copy. Apply these principles:
>
> 1. **No input-shape instructions.** Don't tell users how to reply ("reply with yes/no", "type your answer", "choose one"). Let them speak naturally.
> 2. **No interface verbs.** Drop "click", "tap", "select", "submit", "enter". Use conversational equivalents.
> 3. **Conversational register, not transactional.** "Please provide X" → "What's X?". "You must" → "I'll need".
> 4. **No format prescriptions.** Drop "DD-MM-YYYY", "international format", "include country code". Parse naturally; constrain only in repair turns.
> 5. **Question at the end of the turn.** Strip preamble; end-focus.
> 6. **One question per turn.** Split bundled questions into separate turns.
> 7. **No visual references.** Drop "as shown", "see below", "listed are". Voice has no screen.
> 8. **Convert numbered menus to natural disjunctions.** "1. A, 2. B" → "A, or B?"
>
> For each input line, output: (a) the voice version, (b) a one-line note on which principles applied.

---

## T-grounding — Grounding policy by field type

Risk-stratified, not one-size-fits-all. Use as a decision table when rewriting confirmation logic.

| Field type | Default grounding | Trigger to escalate |
|---|---|---|
| Common acknowledgments | None | — |
| Low-stakes single values (date, single name, postcode) | Implicit echo | Low ASR confidence |
| Names | Implicit echo (high confidence) → phonetic (low confidence) | Cultural diversity, ASR confidence threshold |
| Phone numbers | Explicit digit-by-digit | Always |
| Email | SMS handoff (preferred) or explicit char-by-char | Always; SMS preferred |
| Money / irreversible actions | Explicit summary + check | Always |
| Apparent inconsistencies (e.g. name vs. email) | Soft check | Always |

**Implication for instructions (Layer A):** Encode grounding as conditional behavior keyed to field type. Don't write a flat "always confirm" rule — that produces over-confirmation on low-stakes fields and under-confirmation on irreversible ones.

**Common mis-applications (optimize mode):**
- Field-type policy exists but treats phone/email/money as low-stakes (implicit echo only).
- Over-confirms low-stakes fields with "Is that correct?" patterns.
- Confirms but then proceeds before the user can object (no pause for correction).
- "Always confirm" flat rule disguised as field-type policy — same behavior across all fields.

---

## T-repair — Repair tier ladder

| Tier | Trigger | Response shape |
|---|---|---|
| T-repair-tier-1 | First ASR no-match | Open repair: "Sorry, I missed that — could you say it again?" |
| T-repair-tier-2 | Second no-match on same field | Rephrase or constrain vocabulary ("You can say morning, afternoon, or evening — which works?") |
| T-repair-tier-3 | Third failure or user frustration | Human handoff with full state preservation |

**Telephony note:** Telephony lacks the typing-fallback that voice-over-web has; Tier 2 rephrasing and Tier 3 handoff carry more weight. State always travels with the handoff — the user never starts over.

**Format-prescription rule:** Format prescriptions ("could you say it as day, month, year?") and constrained vocabularies ("just yes or no") are legitimate **only at Tier 2**. They are anti-patterns as defaults (see T-translate-4).

**Common mis-applications (optimize mode):**
- Tier 2 prompt is just a rephrase of Tier 1 — no constraint, no candidate understanding.
- Tier 1 reprompt blames the user ("you weren't clear", "I didn't understand you") rather than the system.
- Tier 3 handoff exists but doesn't preserve state — the user has to start over with the human.
- Same reprompt string used across tiers (no escalation in language).
- Format prescription leaked into Tier 1 default (anti-pattern; only legitimate at Tier 2).

---

## T-latency — Latency budget

| Operation | Acceptable silence | Required affordance |
|---|---|---|
| T-latency-ack | Acknowledgment, simple confirmation | <1s | None |
| T-latency-lookup | Brief lookup (slot availability, basic record) | 1–3s | Pre-announce ("Let me check…") |
| T-latency-complex | Complex processing (multi-system) | 3–10s | Pre-announce + verbal filler every 3–5s |
| T-latency-long | Anything >10s | — | Pre-announce + offer call-back option |

**Implication for instructions (Layer A):** The LLM must say *something* before any non-trivial pause. Encode this as a behavioral rule, not a copy string.

**Common mis-applications (optimize mode):**
- Pre-announce exists for slow operations but missing for medium ones (1–3s lookups).
- Same pre-announce string used regardless of expected duration ("Let me check…" for both 1s and 12s operations).
- Verbal fillers absent for >3s operations (silent processing).
- No call-back option offered for >10s operations.

---

## T-phrasebook — Persona phrasebook scaffold

Rotating tokens prevent robotic repetition. Skill should select 3–6 per category, matching the agent's persona register.

| Function | Default tokens (rotate) |
|---|---|
| Acknowledgment | "Got it." / "Okay." / "Right." / "Thanks for that." / "Alright." |
| Holding | "One moment…" / "Let me check that…" / "Bear with me…" |
| Repair | "Sorry, I missed that — could you say it again?" / "Just to be sure…" |
| Resumption | "Okay, where were we — …" / "Right, so…" |
| Pre-closing | "Anything else before I let you go?" |
| Terminal | "Take care." / "Bye now." |

These are starting points. Adjust register (warmer/cooler, more/less formal) to match the source agent's persona.

**Common mis-applications (optimize mode):**
- Phrasebook defined but with fewer than 3 tokens per function — no real rotation possible.
- Tokens within a function mix registers (e.g., "Got it" + "Thank you so much" + "Right" — three different formality levels for the same purpose).
- Rotation defined but the LLM picks the same token every turn anyway because the instructions don't enforce variation.
- Phrasebook copied verbatim from the scaffold without adjustment to the agent's persona.

---

## T-opening — Two-voice opening structure

| Layer | Voice characteristics | Content |
|---|---|---|
| T-opening-system | Distinct TTS voice; formal, measured, no contractions | Brand, emergency redirect, recording disclosure, AI disclosure |
| T-opening-agent | Warm-clinical TTS voice; contractions, varied prosody, slightly slower than commercial baseline | Self-identification, capability frame, first-topic question |
| T-opening-handover | 600–900ms pause; optional faint audio cue | — |

**Carrier branching:**
- **If carrier-side pre-call announcement is available** (modality trait): system layer plays before the agent connects. Agent layer is shorter, no disclosure repetition.
- **If not available**: agent voices both layers in sequence with the handover pause.

**Implication for Layer D:** The opening is split across artifacts. System-layer content may live in carrier configuration (Layer E), agent-layer content lives in the Agent Script welcome.

**Common mis-applications (optimize mode):**
- System layer uses contractions ("we're recording your call") — breaks the formal/measured register that distinguishes it from the agent layer.
- Agent layer is too long (>5s spoken length), defeating the split.
- Two-voice structure defined but both layers use the same TTS voice — no auditory contrast for the user.
- System layer plays both via carrier AND agent (disclosure repetition), when carrier-side announcement is available.
- Handover pause absent or too short (<300ms) — no perceptual gap between layers.
