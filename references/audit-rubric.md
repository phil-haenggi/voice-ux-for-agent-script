# Audit rubric

Drives audit coverage. For each principle and pattern, defines what the audit must check, what triggers a `[changed]` entry, and what triggers a `[review needed]` entry (conflict policy).

Citation format in audit output: `why: P9-end-focus` or `why: T-translate-6 + P9-end-focus`. Always cite the most specific source.

---

## Coverage contract

The audit MUST visit each row below and produce one of:
- `[changed]` — voice principle violated, rewrite applied
- `[ok]` — principle already respected, no change (do not surface in inline audit; counts in summary)
- `[review needed]` — voice principle violated AND original logic is intentional (compliance, business rule); preserved with flag
- `[out-of-scope]` — pattern detected that the source library doesn't cover (see `voice-ux-principles.md` gaps)

---

## Principle-driven checks

| ID | Check | Triggers `[changed]` if… | Notes |
|---|---|---|---|
| P1 | Long monologues | Any single utterance > ~3 sentences without a question or pause point | Recommend chunking; flag barge-in concern (Layer E) |
| P2 | Confirmation strategy | "Is that correct?" pattern OR explicit confirmation on low-stakes fields OR no confirmation on irreversible | Cross-reference T-grounding for field-type policy |
| P3 | No-input/no-match | Error messages blame the user OR don't vary across attempts OR no escalation path | Map to T-repair tier |
| P4 | Opening length | Welcome/opening utterance > ~5s spoken (~75 words) | Split or shorten; consider T-opening two-voice |
| P4 | Closing | Flow ends without pre-closing token before terminal | Insert pre-closing from T-phrasebook |
| P5 | Prosody | Numbers, names, irreversible terms not marked for stress (where SSML supported) | Layer E recommendation, not in-script change |
| P6 | Sequential gathering | Two or more pieces of info requested in one turn | Split; re-order to natural narrative if data-schema order is unnatural |
| P7 | Latency | Action/tool call invoked without verbal pre-announce | Insert pre-announce per T-latency tier |
| P8 | Turn atomicity | Turn does framing + action + follow-up question in one breath | Split into atomic turns |
| P9 | End-focus | Question precedes context, OR critical info buried mid-turn | Reverse to put question/critical info last |
| P10 | Repair vocabulary | Same repair string used for tier 1, 2, 3 (no escalation) | Generate tiered variants |
| P11 | Phrasebook coherence | Acknowledgments mix registers OR exceed 6 unique tokens OR fewer than 3 | Build coherent token set per T-phrasebook |
| P12 | Handoff | Tier 3 escalation drops state, OR no announcement of handoff target | Add what/where/why announcement; route per modality trait matrix |

---

## Translation-rule checks (T-translate)

| ID | Trigger pattern (regex/heuristic) | Action |
|---|---|---|
| T-translate-1 | "reply with", "say yes or no", "type", "choose one" as default prompt | Strip; just ask |
| T-translate-2 | "click", "tap", "select", "submit", "press", "enter" as user-facing verb | Replace with conversational equivalent |
| T-translate-3 | "Please provide", "You must provide", "We require" | "What's your X?" / "I'll need" |
| T-translate-4 | Format prescriptions ("DD-MM-YYYY", "international format", "include @") in default prompts | Strip from default; allowed only in Tier 2 repair |
| T-translate-5 | "as shown", "see below", "listed are", "here are the options:" | Remove visual reference; rephrase |
| T-translate-6 | Numbered or bulleted menus in copy | Convert to "X, Y, or Z?" disjunction |
| T-translate-7 | Fixed acknowledgment template ("Thank you. Now please…") | Replace with rotating tokens from T-phrasebook |
| T-translate-8 | "and" / "also" / "as well as" joining two questions | Split into separate turns |

---

## Pattern checks (T-grounding, T-repair, T-latency)

| ID | Check | Action |
|---|---|---|
| T-grounding-low-stakes | Date / postcode / single name confirmed explicitly | Switch to implicit echo |
| T-grounding-phone | Phone number not digit-by-digit confirmed | Add explicit digit-by-digit |
| T-grounding-email | Email not SMS-handed-off (preferred) or char-by-char | Recommend SMS link if T-modality says SMS available; else char-by-char |
| T-grounding-money | Money/irreversible action without explicit summary | Add summary turn |
| T-repair-tier-1 | First-attempt repair language blames user | Replace with neutral open repair |
| T-repair-tier-2 | Second-attempt repair doesn't constrain or rephrase | Add constrained-vocabulary or candidate-understanding variant |
| T-repair-tier-3 | Third-attempt has no handoff or drops state | Add handoff per modality matrix; preserve state |
| T-latency-pre-announce | Tool/action call has no verbal lead-in | Insert "Let me check…" / "One moment…" per T-phrasebook |
| T-latency-long | Action expected to take >10s, no callback option | Add call-back offer |

---

## Conflict policy → `[review needed]`

When the source script's behavior is voice-suboptimal AND there is a signal it's intentional, do NOT rewrite. Surface as `[review needed]` with all of:
- The original directive (quoted)
- The voice principle it conflicts with (cite ID)
- A one-sentence recommendation
- The signal that suggested intentionality (e.g., "compliance", "regulatory", "policy", "always", or a business-rule comment in the script)

**Examples of intentionality signals:**
- Explicit compliance/regulatory language ("PCI", "GDPR consent", "must record")
- Repeated assertion of the same rule across multiple turns
- Comment or instruction text marking the directive as fixed
- Bundled question that asks for items that are legally bound together (e.g., consent + identification)

Do not infer intentionality from a single occurrence of suboptimal copy.

---

## Out-of-scope detection

If the audit finds these patterns, flag as `[out-of-scope]` rather than rewrite (gap in source library):

- Multi-intent / context-switching mid-conversation
- Emotional de-escalation (angry/distressed user handling)
- Cascading error recovery (corrected field that has downstream impact)
- Multilingual / language-specific repair
- Agent-to-agent skill transfer

Surface in audit summary; do not block the rewrite.
