# Voice UX principles reference

The 12 voice UX principles from the conversation design library. Use as the citation source for the audit's `why:` lines and as the audit rubric (see `audit-rubric.md`).

Source: https://github.com/phil-haenggi/conversation-design-library-v2 — `voice-ux-12-prompts` section.

Citation prefix: **P** (e.g., `P3-no-input`, `P10-repair`).

---

## P1 — Barge-In & Overlap Management

**Summary:** Normalize user interruption as a feature, not error. Chunk information with clear "safe points" for interruption; distinguish between transitional overlap (natural), corrective (user fixes), and competitive (user interrupts). Design enables user control without repeating key data when interrupted.

**Voice vs. text contrast:** Text scrolls; voice is linear and uninterruptible without design intent. "Inability to interrupt long agent utterances ranks among top voice UX frustrations."

**Migration heuristic:** Long monologues in chat (multi-paragraph answers, lists) must be chunked into interruptible units in voice. If a turn exceeds ~3 sentences, break it.

**Common mis-applications (optimize mode):** Chunking present but the chunks are still single utterances at runtime because there's no pause directive between them. Or chunks are short but lack a clear interruptible point ("safe place").

---

## P2 — Grounding & Confirmation

**Summary:** Scaffold confirmation with implicit (weave into next turn), explicit (restate for high-stakes), or graduated (escalate with risk) strategies. Avoid over-confirmation; use digit-by-digit verification for numbers; summarize all fields before irreversible actions.

**Voice vs. text contrast:** Text forms can show all values back at once; voice can't. Confirmation must be selectively allocated.

**Migration heuristic:** Replace "Is that correct?" with restatement that grounds *and* advances ("London, March 15th — sound right?"). See `telephony-patterns.md#T-grounding` for field-type policy.

**Before/after:**
- Text (fine): "London? March 15? Economy?" [checkboxes]
- Voice (fails): "London?" / "March 15th?" / "Economy?" [six turns]
- Fixed: "London, March 15th, economy. Shall I search?"

**Common mis-applications (optimize mode):** Grounding policy exists but doesn't escalate on low ASR confidence — phone numbers and emails skim past on implicit echo even when the recogniser was uncertain. Or money/irreversible actions get only implicit echo, with no explicit summary + check before commit. Or over-confirms low-stakes fields with explicit "Is that correct?" patterns. Or asks for confirmation but proceeds before the user can object.

---

## P3 — No-Input & No-Match Escalation

**Summary:** Pursue silence without blame ("I didn't catch that," not "You weren't clear"). Vary reprompts; escalate from open to closed options to modality shift after 2–3 failures; preserve context when handing off.

**Voice vs. text contrast:** Text has no silence to interpret; voice must distinguish silence from confusion from disengagement.

**Migration heuristic:** Map every error message in the source script to a tier (1/2/3, see `telephony-patterns.md#T-repair`). Reprompt language varies per attempt.

**Common mis-applications (optimize mode):** Reprompt strings exist but are identical across tiers — the structure is there but the language doesn't escalate. Or reprompts vary but still blame the user ("you weren't clear", "I need you to speak louder").

---

## P4 — Opening & Closing Sequences

**Summary:** Openings: ~5–7s, end with clear question. Closings: three-step negotiation (pre-closing → topic confirmation → terminal exchange). Both must feel collaborative, never abrupt or drop-call-like.

**Voice vs. text contrast:** Chat openings can be paragraph-length welcomes; voice must front-load identity + first question quickly (~5–7s). Chat closings can be one line; voice closings are negotiated.

**Migration heuristic:** Chat openings notably longer than ~7s spoken length should be split. Insert pre-closing token before terminal in any flow that ends a transaction.

**Common mis-applications (optimize mode):** Two-voice opening defined but the system and agent layers don't sound different — same TTS voice, same pacing, same register — so the user doesn't perceive a layer change. Or agent layer is too long, defeating the split. Or closing has a pre-closing token but no terminal exchange ("Bye now") — the call ends abruptly.

---

## P5 — Prosodic Design & Intonation

**Summary:** Intonation signals turn-taking and information structure; stress marks new vs. known information; pacing at 130–160 wpm for critical content. Use falling intonation for statements, rising for yes/no; lists rise on non-final items, fall on final.

**Voice vs. text contrast:** "The same words with different intonation can be a question, statement, surprise, or sarcasm." Text misses this entirely; voice must compensate.

**Migration heuristic:** Where SSML/prosody markup is supported (Layer E concern), recommend stress and pacing on numbers, names, and unfamiliar terms.

**Common mis-applications (optimize mode):** SSML present but applied generically — same `<prosody>` settings everywhere, no contrast between known/new information. Or stress applied to function words ("THE", "TO") rather than content words.

---

## P6 — Sequential Information Gathering

**Summary:** One question per turn, asked in natural narrative order (not data-schema order). Acknowledge briefly; leverage user-volunteered info; signal progress for sequences >5 fields.

**Voice vs. text contrast:** "Stacking multiple questions violates adjacency-pair structure." Text forms can ask many fields at once; voice adjacency pairs demand strict turn-by-turn sequencing.

**Migration heuristic:** Find every place the script asks for two or more pieces of info in one turn. Split. Reorder if data-schema order doesn't match how a person would volunteer it.

**Common mis-applications (optimize mode):** One-question-per-turn followed correctly, but field order matches the database schema rather than natural narrative (e.g., asking DOB before name, or postcode before address line 1). Or progress signaling absent for sequences >5 fields, leaving the user uncertain how much longer.

---

## P7 — Silence & Latency Management

**Summary:** Silences >700ms are perceptible; >1s trigger user remedial action. Pre-announce processing time; use acknowledgment bridges ("Let me check..."); use verbal fillers every 3–5s for longer waits. Never timeout silently.

**Voice vs. text contrast:** Text has no latency perception (spinner suffices); voice requires active communication during processing.

**Migration heuristic:** Audit every action/tool call in the source script. For each, ask: how long does this take? If >1s, the LLM must say *something* before invoking it. For multi-second processing, follow up with verbal fillers every 3–5s. See `telephony-patterns.md#T-latency`.

**Before/after:**
- Text (implicit): [spinning wheel]
- Voice (must be explicit): "Let me search... [pause] Comparing airlines... [pause] Cheapest is $845."

**Common mis-applications (optimize mode):** Pre-announce exists for some actions but not all — usually the slowest ones get covered, but a 2–3 second lookup gets missed. Or pre-announce is identical for every operation regardless of expected duration ("Let me check…" used for both a 1-second cache hit and a 12-second multi-system join). Or processing >3s has no verbal filler, so the user starts wondering if the line dropped.

---

## P8 — Turn Design & Progressivity

**Summary:** Each turn accomplishes *one* action and advances toward completion. Structure as: framing + core action + transition relevance place signaling turn-end. No multi-part requests.

**Voice vs. text contrast:** Text turns can pile on framing, action, and follow-up. Voice turns must be atomic.

**Migration heuristic:** "Multi-part" is anything that asks the user to track more than one thing. Split. Sequence in natural narrative order.

**Common mis-applications (optimize mode):** Turns are atomic by count but still cognitively multi-part — e.g., "I'll need your date of birth and the year you joined" framed as one question because both are dates. The user has to track two things.

---

## P9 — Turn-Final Placement & End-Focus

**Summary:** Put critical/novel information last (recency effect). Questions always at turn-end. Before eliciting a choice, present all options first.

**Voice vs. text contrast:** "Turn-final position carries highest perceptual weight in spoken interaction… spoken language is ephemeral — users cannot re-read." Text allows scanning; voice requires information architecture restructuring.

**Migration heuristic:** Reverse turns where the question comes before context. "What date works for you? I have slots Tuesday, Wednesday, Friday." → "I have slots Tuesday, Wednesday, Friday — what works?"

**Common mis-applications (optimize mode):** End-focus respected for questions, but critical confirmation data is buried mid-turn ("Right, I've booked your appointment for 3pm at the Highgate clinic, and I've sent you a text confirmation"). The user remembers "text confirmation" and forgets the time and location.

---

## P10 — Voice Conversation Repair

**Summary:** Four-level hierarchy: open repair (weakest) → question word + partial → candidate understanding → explicit correction (strongest). Never over-apologize; escalate after 3 failures to alternative modality.

**Voice vs. text contrast:** Text can show "we couldn't find that, please try again"; voice must repair *while* preserving conversational momentum.

**Migration heuristic:** See `telephony-patterns.md#T-repair`. Map each repair instance in the script to a tier; vary reprompt language across tiers.

**Before/after:**
- Turn 1: "Sorry, what was that?" [open]
- Turn 2: "Did you mean change it on the account, or update the number?" [targeted]
- Turn 3: "You mean cancel order 7-8-4-2?" [candidate]
- Turn 4+: "Can you spell that?" or "I'll text you a link" [modality shift]

**Common mis-applications (optimize mode):** Tier ladder defined but tier 2 is not actually a constraint or candidate understanding — it's just a rephrase of tier 1 ("Sorry, could you say that again?" → "Sorry, I didn't catch that — could you say it once more?"). Or tier 3 hands off but doesn't preserve state, forcing the user to restart.

---

## P11 — Voice Persona & Phrasebook

**Summary:** Select 3–6 acknowledgment tokens and use consistently. Avoid register mixing; map lexical choices to prosodic profiles. "Linguistic fingerprint" becomes brand identity in voice-only interfaces.

**Voice vs. text contrast:** Text can survive register mixing (the user re-reads); voice register inconsistency reads as fake or unstable.

**Migration heuristic:** Inventory acknowledgments and discourse markers across the source script. If they don't form a coherent set, build one. See `telephony-patterns.md#T-phrasebook`.

**Common mis-applications (optimize mode):** Phrasebook exists but has fewer than 3 tokens per function (no rotation possible). Or tokens mix registers within a function ("Got it" / "Thank you so much" / "Right" — three different formality levels for the same purpose). Or rotation is defined but the LLM picks the same token every turn anyway because the instructions don't enforce variation.

---

## P12 — Voice-to-Screen Handoff

**Summary:** Announce what/where/why before transitioning. Pre-populate all voice-collected data; preserve context with deep links. Offer voice-return option; frame as smart modality choice, not failure.

**Voice vs. text contrast:** Text-to-text handoffs are seamless; voice-to-screen requires explicit announcement and context bridging.

**Migration heuristic:** If the modality trait matrix says "screen fallback available", design handoff turns. If "SMS fallback", design SMS-link patterns. If neither, Tier 3 escalation must be human-handoff (see T-repair-tier-3).

**Common mis-applications (optimize mode):** Handoff exists but announces only the modality ("I'm sending you a text") without the what/where/why ("I'm sending you a link to upload your ID — once you've done that, I'll pick up where we left off"). Or handoff drops collected state, forcing the user to re-supply data on the new modality.

---

## Gaps in source library (not covered by P1–P12)

The library does not cover these. The skill should not invent rewrites for them in v1:

- Multi-intent / context-switching mid-conversation
- Emotion / de-escalation playbook
- Multi-turn cascading error recovery (downstream impact of corrected fields)
- Multilingual / accent-clash handling
- Agent-to-agent skill transfer

If the audit detects one of these patterns in the source, flag as `out-of-scope` rather than rewrite.
