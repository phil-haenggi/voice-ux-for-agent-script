# Audit rubric

Drives audit coverage. For each principle and pattern, defines what the audit must check, what triggers each tag, and how mode (migrate vs. optimize) affects the threshold.

Citation format in audit output: `why: P9-end-focus` or `why: T-translate-6 + P9-end-focus`. Always cite the most specific source.

---

## Coverage contract

The audit MUST visit each row below and produce one of:

| Tag | Meaning | Modes |
|---|---|---|
| `[changed]` | Voice principle violated or absent, rewrite applied | Both |
| `[ok]` | Principle respected (counts in summary, not surfaced inline) | Both |
| `[review needed]` | Principle violated AND intentionality signal present; preserve original, flag conflict | Both (threshold differs) |
| `[consider]` | Principle present but applied weakly; suggestion only — no rewrite, no preservation | **Optimize only** |
| `[out-of-scope]` | Pattern detected that source library doesn't cover | Both |

---

## Principle-driven checks (presence checks)

Used in both modes. These check whether a principle is *present at all*. In migrate mode, absence dominates. In optimize mode, absence is rarer but still possible (script started voice-shaped but missed a category).

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

## Mis-application checks (optimize mode only)

Used in optimize mode to detect principles that are *present but applied wrong*. These triggered `[consider]` (or `[changed]` if the mis-application is unambiguous, e.g., a clear copy bug).

In migrate mode, these checks usually don't fire — the principle isn't present yet to be mis-applied. Run them anyway in case the source is partially voice-shaped (half-migrated script).

| ID | Mis-application | Detection signal | Default tag |
|---|---|---|---|
| P10-mis-1 | Repair tier 2 directive exists but rephrasing is identical/near-identical to tier 1 | String similarity between tier 1 and tier 2 prompts >70%, OR tier 2 lacks constrained vocabulary or candidate understanding | `[consider]` |
| P10-mis-2 | Repair tier 3 escalation defined but doesn't preserve state | Tier 3 prompt restarts the conversation OR doesn't reference collected fields | `[changed]` |
| P11-mis-1 | Phrasebook exists but has fewer than 3 tokens per function | Token count < 3 in any function category | `[consider]` |
| P11-mis-2 | Phrasebook tokens mix registers (formal + casual in same function) | Heuristic: contractions in some tokens but not others within the same function category; or one token uses "thank you" while another uses "thanks" | `[consider]` |
| P11-mis-3 | Acknowledgment tokens never rotate (same one used every turn in sample) | Same token used in >3 consecutive turns in the sample | `[consider]` |
| P2-mis-1 | Grounding policy exists but treats high-stakes fields as low-stakes | Phone, email, money, or irreversible action uses implicit echo or no confirmation | `[changed]` |
| P2-mis-2 | Grounding policy over-confirms low-stakes fields | Date, postcode, single name uses explicit "Is that correct?" pattern | `[consider]` |
| T-opening-mis-1 | Two-voice opening exists but system layer uses contractions | "We're", "you're", "I'm" in system-layer content | `[changed]` |
| T-opening-mis-2 | Two-voice opening exists but agent layer is too long | Agent-layer utterance > ~5s spoken (~75 words) | `[consider]` |
| T-latency-mis-1 | Pre-announce exists for some actions but not all | Subset of tool/action calls have verbal lead-in; others don't | `[changed]` |
| T-latency-mis-2 | Pre-announce exists but is identical for short and long operations | Same "Let me check…" used regardless of expected duration | `[consider]` |
| P6-mis-1 | Sequential gathering exists but order doesn't match natural narrative | Field order matches data-schema (e.g., DOB before name) rather than how a person would volunteer | `[consider]` |
| P3-mis-1 | Reprompt language exists but doesn't vary across attempts | Same reprompt string used for tiers 1 and 2 | `[changed]` |
| P12-mis-1 | Handoff announcement exists but doesn't include what/where/why | Announcement names the modality but not the reason or destination | `[consider]` |

---

## Translation-rule checks (T-translate)

Used in both modes. In optimize mode these usually return `[ok]` for voice-source scripts, but catch text-shaped legacy regions in half-migrated scripts.

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

Used in both modes.

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

Threshold differs by mode.

### Migrate mode (default conservative)

When the source script's behavior is voice-suboptimal AND there is a signal it's intentional, preserve the original. Surface as `[review needed]` with:
- The original directive (quoted)
- The voice principle it conflicts with (cite ID)
- A one-sentence recommendation
- The signal that suggested intentionality

**Strong intentionality signals (preserve in both modes):**
- Explicit compliance/regulatory language ("PCI", "GDPR consent", "must record", "required by")
- Comment or instruction text marking the directive as fixed
- Bundled question that asks for items legally bound together (e.g., consent + identification)

**Weak intentionality signals (preserve in migrate mode, surface as `[review needed]` or `[consider]` in optimize mode):**
- Repeated assertion of the same rule across multiple turns
- Pattern repeated across topics

Do not infer intentionality from a single occurrence of suboptimal copy in either mode.

### Optimize mode (lower bar)

The developer is asking for an opinion. Be more willing to challenge.

- Strong intentionality signals → preserve as `[review needed]` (same as migrate).
- Weak intentionality signals → flag as `[review needed]` with a stronger recommendation, OR as `[consider]`. Do not preserve silently.
- No intentionality signal → rewrite as `[changed]`.

The bar shift means: in migrate mode, "the designer probably knew what they were doing" is the working assumption. In optimize mode, "the designer wants my opinion" is the working assumption.

---

## Out-of-scope detection

If the audit finds these patterns, flag as `[out-of-scope]` rather than rewrite (gap in source library):

- Multi-intent / context-switching mid-conversation
- Emotional de-escalation (angry/distressed user handling)
- Cascading error recovery (corrected field that has downstream impact)
- Multilingual / language-specific repair
- Agent-to-agent skill transfer

Surface in audit summary; do not block the rewrite.

---

## Mode-detection signals (for the extraction pass)

Used during automated extraction (Phase 3 of the intake flow) to infer mode. The extraction pass surfaces what it found and the proposed mode; the developer confirms in Phase 4.

### Text-shaped signals (suggests migrate mode)
- Interface verbs in copy ("click", "tap", "select", "submit") — T-translate-2
- Format prescriptions in default prompts ("DD-MM-YYYY", "international format") — T-translate-4
- Visual references ("as shown", "see below") — T-translate-5
- Numbered/bulleted menus in copy — T-translate-6
- Bundled questions joined by "and"/"also" — T-translate-8
- No repair tier directives in instructions
- No latency pre-announce patterns in instructions
- No phrasebook tokens defined
- No two-voice opening structure

### Voice-shaped signals (suggests optimize mode)
- Repair tier directives present (tier 1 / tier 2 / tier 3 referenced)
- Grounding-by-field-type policy present (different rules for phone vs. date)
- Latency pre-announce patterns present ("if X takes more than a second, say…")
- Phrasebook tokens defined (rotating acknowledgments)
- Two-voice opening structure present
- Absence of interface verbs in copy

### Mixed signals (half-migrated script)
If both signal sets are present (e.g., voice-shaped instructions but text-shaped copy strings), default the proposed mode to **optimize** and surface the mixed signals to the developer. Optimize mode's mis-application checks plus the T-translate checks will catch both shapes.
