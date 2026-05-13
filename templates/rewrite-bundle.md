# Rewrite bundle — output skeleton

The skill produces ONE file per migration or optimization, structured as below. Each layer is independently usable: developer can drop Layer A into Agent Script instructions, Layer B into copy fields, etc., without untangling.

Suggested filename: `_local/generated/[agent-name]-voice-{migration,optimization}.md`

---

```markdown
# Voice UX work: [agent name]

**Mode:** migrate / optimize
**Mode rationale:** [one-line: text-shaped signals dominated extraction → migrate / voice-shaped signals dominated → optimize / mixed signals, developer chose X]
**Source:** [path to original Agent Script]
**Sample:** [path to provided sample] OR `synthetic — verify against real flow`
**Modality traits:**
- Barge-in available: yes / no
- Screen fallback for handoff: yes / no
- Async (SMS) fallback: yes / no
- Carrier-side pre-call announcement: yes / no
**Languages:** [list]
**Primary intent:** [from Script or developer answer]

---

## Mode-detection extraction summary

[Optional but recommended — list the signals that drove mode inference. Helps the developer sanity-check.]

**Text-shaped signals found:**
- [signal: where in source / count]
- [...]

**Voice-shaped signals found:**
- [signal: where in source / count]
- [...]

**Inferred mode:** [migrate / optimize / mixed]
**Developer-confirmed mode:** [migrate / optimize]

---

## Summary

| Category | Changed | Review needed | Consider | Out-of-scope | OK |
|---|---|---|---|---|---|
| Turn structure | N | N | N | N | N |
| Repair | N | N | N | N | N |
| Grounding | N | N | N | N | N |
| Copy / translation | N | N | N | N | N |
| Opening / closing | N | N | N | N | N |
| Latency | N | N | N | N | N |
| Phrasebook | N | N | N | N | N |

> `Consider` column populated only in optimize mode. In migrate mode it stays at zero.

**Synthetic sample warnings:** [if applicable, list assumptions the synthetic sample made that need verification]

**Layer E items the developer still owes:** [count and one-line names]

---

## Layer A — Rewritten instructions (LLM-facing)

> Drop into Agent Script `system.instructions` or per-topic `reasoning.instructions`. Voice behavior is baked in as directives.

### Turn structure
- One question per turn. If you need more than one piece of information, ask in sequence.
- Put the question or critical information at the end of the turn. Lead with context, end with what you need from the user.
- Never bundle two questions with "and" or "also". Split them.
- Keep utterances under ~3 sentences unless reading back data the user just gave you.

### Grounding
- Common acknowledgments: no confirmation.
- Single dates, postcodes, single names: implicit echo as you advance ("Tuesday the 15th — and for what time?"). Escalate to phonetic spelling on low ASR confidence.
- Phone numbers: implicit echo on high ASR confidence; on low confidence, read back digit by digit.
- Email: implicit echo on high ASR confidence; on low confidence, read back char by char. SMS handoff is a fallback if char-by-char is impractical.
- Money or irreversible actions: explicit summary + check ("That's £85 to be charged today — shall I go ahead?") before commit.
- If two fields appear inconsistent (e.g., name and email domain), do a soft check.

### Repair
- First miss: open repair, no blame ("Sorry, I missed that — could you say it again?").
- Second miss on the same field: rephrase or constrain ("You can say morning, afternoon, or evening — which works?"). Format prescriptions are allowed here, not before.
- Third miss or user frustration: hand off to a human. Carry all collected state with you. Never make the user start over.
- Vary repair language across attempts. Don't repeat the tier-1 string.

### Latency
- Before any tool/action call expected to take more than a second, say something. "Let me check…" / "One moment…"
- For multi-system or slow operations, check in verbally every 3–5 seconds.
- For anything expected to take more than 10 seconds, warn the user that it may take a while; keep verbal fillers going during processing.

### Sequential gathering
- Ask in natural narrative order, not data-schema order. If a person would volunteer date before time, ask date first.
- Acknowledge briefly between fields. Don't echo every value.
- For sequences over 5 fields, signal progress ("Just two more things…").

### [Per-topic blocks, if multi-topic — copy this template]
**Topic: [name]**
[Topic-specific instructions — repair, grounding, escalation overrides for this topic]

---

## Layer B — Rewritten user-facing copy

> Drop into Agent Script copy fields (welcome, error, prompts, confirmations).

### [original-string-id-or-quoted-source] → [rewritten]
- **Original:** "Please reply with yes or no to confirm."
- **Voice:** "Sound good?"
- **why:** T-translate-1 + T-translate-3

### [next entry…]

[Repeat for every changed string.]

---

## Layer C — Persona phrasebook

> Drop into Agent Script as token sets. Rotate within each function — never use the same token twice in a row.

| Function | Tokens |
|---|---|
| Acknowledgment | [3–6 tokens, register-matched] |
| Holding | [3 tokens] |
| Repair (Tier 1) | [2–3 variants] |
| Repair (Tier 2 frame) | [2–3 frames; field-specific constrained vocabulary fills in at runtime] |
| Resumption | [2 tokens] |
| Pre-closing | [1–2 tokens] |
| Terminal | [2 tokens] |

**Register notes:** [one paragraph on the persona register the phrasebook was tuned to — warm/cool, formal/informal, contractions/no-contractions]

---

## Layer D — Opening sequence

### System layer (formal, distinct voice, measured register)
[Brand + emergency redirect + recording disclosure + AI disclosure]

> Lives in: [carrier pre-call announcement IF available — see Layer E; otherwise voiced by agent in sequence]
>
> Critical: the system layer must sound clearly different from the agent layer (different TTS voice, pacing, register). The exact register choice is flexible; what matters is contrast.

### Handover
600–900ms pause, optional faint audio cue.

### Agent layer (warm, varied prosody, slightly slower than commercial baseline)
[Self-identification + capability frame + first-topic question]

> Lives in: Agent Script `welcome`

---

## Layer E — Out-of-Agent-Script notes

> Items that cannot be encoded in instructions/copy. Hand off to platform/runtime owner.

### [Item title]
- **What:** [config/setting]
- **Where it lives:** [carrier config / TTS engine / ASR vendor / SSML / runtime parameter]
- **Recommended value/policy:** [specific recommendation]
- **Why it matters:** [principle citation, e.g., P5-prosody, T-latency-long]

[Examples to include if relevant:]
- ASR confidence threshold for grounding escalation
- Silence timer values (no-input timeout)
- Barge-in detection toggle
- TTS voice selection (system layer vs. agent layer)
- SSML support / prosody markup
- Carrier-side pre-call announcement configuration
- Long-operation handling (warning copy + filler cadence) for >10s actions

---

## Audit detail (inline changes)

> Every non-trivial entry with rationale. Use `[changed]`, `[review needed]`, `[consider]` (optimize only), or `[out-of-scope]` tags.

### [changed] [location-in-source]
- **Original:** "[quote]"
- **Rewrite:** "[quote]"
- **why:** [principle citation]
- **layer:** [A / B / C / D / E]

### [review needed] [location-in-source]
- **Original:** "[quote]"
- **Voice principle violated:** [citation]
- **Why preserved:** [intentionality signal — e.g., compliance flag]
- **Recommendation:** [one sentence]

### [consider] [location-in-source]  *(optimize mode only)*
- **Current:** "[quote]"
- **Voice principle present but applied weakly:** [citation, e.g., P10-mis-1 — repair tier 2 identical to tier 1]
- **Suggested improvement:** "[quote of improved version]"
- **why:** [principle citation + mis-application ID from audit-rubric.md]

### [out-of-scope] [pattern detected]
- **Pattern:** [e.g., user expresses anger across 3 turns]
- **Why not rewritten:** [gap in source library]
- **Suggested follow-up:** [e.g., add de-escalation playbook in v2]
```
