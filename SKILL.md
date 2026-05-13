---
name: voice-ux-for-agent-script
description: >
  Applies voice UX expertise to a Salesforce Agentforce Agent Script in either of
  two modes: **migrate** (text-based Script → voice-optimized Script) or
  **optimize** (existing voice Script → improved voice Script). Auto-detects mode
  from the source's text-shaped vs. voice-shaped signals; user confirms or
  overrides. Audits against 12 voice UX principles and operational telephony
  patterns (grounding policy, repair tiers, latency budget, persona phrasebook,
  two-voice opening). Produces a layered rewrite: rewritten LLM instructions
  with voice behavior baked in (repair, grounding, latency directives), rewritten
  user-facing copy, persona phrasebook, opening sequence, and out-of-Agent-Script
  notes for runtime/platform owners. In optimize mode, also flags principles
  applied weakly (`[consider]` tier — "phrasebook exists but only has 2 tokens",
  "repair tier 2 identical to tier 1"). Preserves original business logic;
  surfaces conflicts with voice best practice as `[review needed]` rather than
  silently overriding (lower preservation bar in optimize mode than in migrate).

  TRIGGER when: user asks to migrate, port, convert, or "make voice-ready" /
  "telephony-ready" an existing text-based Agent Script (migrate mode); user asks
  to audit, review, or optimize an existing voice Agent Script for voice UX
  issues (optimize mode); user has an Agentforce Agent Script and wants voice UX
  expertise applied.

  DO NOT TRIGGER when: building a voice agent from scratch with no source Script
  (use developing-agentforce); designing the agent persona/voice character
  (use agent-persona); running test specs against a voice agent (use
  testing-agentforce); analyzing production voice session traces (use
  observing-agentforce); configuring TTS voice casting, IVR menu structure, or
  ASR vendor settings (out of scope — surfaced in Layer E for handoff).
version: 0.2.0
date: 2026-05-13
author: phil-haenggi
tags: [salesforce, agentforce, agent-script, voice, telephony, migration, optimization, voice-ux, conversation-design, repair, grounding, latency, phrasebook, two-voice-opening, audit]
allowed-tools:
  - Read
  - Write
  - Edit
  - AskUserQuestion
  - Glob
  - Grep
---

# Voice UX for Agent Script

## How to Use

This skill takes an Agentforce Agent Script and applies voice UX expertise to it. Two modes:

- **Migrate mode** — source is a text-based Script. Output is a voice-optimized rewrite.
- **Optimize mode** — source is an existing voice Script. Output is an improved voice Script with weak applications of voice principles flagged and (where unambiguous) fixed.

Mode is auto-detected from extraction signals (text-shaped vs. voice-shaped patterns in the source) and confirmed with the developer. The output bundle is the same shape in both modes; the audit content differs.

**What it produces:**
- A migration/optimization bundle (`_local/generated/[agent-name]-voice-{migration,optimization}.md`) with five labeled layers (instructions, copy, phrasebook, opening, out-of-script notes) plus inline audit
- A synthetic sample (`_local/generated/[agent-name]-synthetic-sample.md`) when no real sample is provided

**What it does not do:** Build voice agents from scratch. Design the agent's persona/voice character. Run runtime QA. Configure TTS/ASR/IVR. Generate non-English copy. Resolve multi-intent or emotional-de-escalation patterns (gaps in the source library — flagged as `[out-of-scope]`).

## When to Use This Skill

- **Migrate:** Migrating a working text-based Agentforce Agent Script to voice (telephony or voice-over-web). Auditing a chat-based agent for voice UX issues without committing to a full rewrite.
- **Optimize:** Reviewing an existing voice Agent Script for voice UX quality. Catching mis-applied voice principles (repair tier 2 identical to tier 1, phrasebook with too few tokens, grounding policy treating phone numbers as low-stakes). Preparing a voice script for stakeholder review or handoff.

**Scope boundary:** This skill rewrites *what the agent says and how it behaves* for voice. It does not touch the agent's persona, topic structure, or actions/tools — those are unchanged. It does not configure runtime/platform settings — those are surfaced as Layer E recommendations.

## Reference Material

The skill consults three local references at runtime. Do not regenerate from external sources — read these.

- `references/voice-ux-principles.md` — 12 voice UX principles (P1–P12) with citation IDs, voice-vs-text contrasts, migration heuristics, and **common mis-applications for optimize mode**. Source of `why:` lines in audit.
- `references/telephony-patterns.md` — operational decision tables: 8 chat→voice translation rules (T-translate-1..8), grounding policy by field type (T-grounding), repair tier ladder (T-repair-tier-1..3), latency budget (T-latency), persona phrasebook scaffold (T-phrasebook), two-voice opening (T-opening). Each table has mis-application notes for optimize mode.
- `references/audit-rubric.md` — coverage contract mapping each principle and pattern to a check. Includes both presence checks (used in both modes) and **mis-application checks (optimize mode)**. Documents mode-dependent conflict thresholds.

## Phase 1 — Artifact Intake

**Required input:** Path to or contents of the source Agent Script (`.agent` file, YAML, or text instructions).

**Optional input:** Path to or contents of a sample conversation showing the main use case.

**Behavior:**
1. Read the source Script. Identify topics, actions, system instructions, welcome/error/copy strings.
2. If a sample is provided, read it.
3. If no sample is provided, **synthesize one** using `templates/synthetic-sample.md` as the skeleton. The synthesis adapts to mode (migrate → text-shaped sample, optimize → voice-shaped sample). Stamp it `synthetic — verify against real flow`, write it to `_local/generated/[agent-name]-synthetic-sample.md`, and **show it to the developer for review BEFORE proceeding**. The developer can edit, replace, or accept.

Do not proceed to Phase 2 until the sample (real or synthetic-and-acknowledged) is settled.

## Phase 2 — Automated Extraction (mode detection)

Before asking the developer anything, extract from the artifacts. Crucially, this phase **infers the mode**.

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

### Other extraction
Beyond mode signals, extract: audience tone, primary intents, action set with expected latency profile, existing grounding/repair logic, persona signals (acknowledgment patterns, discourse markers — feeds Layer C).

Surface what was inferred — including the proposed mode and the signals behind it — so the developer can correct.

## Phase 3 — Mode Confirmation + Gap-fill Diagnostic

Use `AskUserQuestion`. Always ask:

1. **Confirm mode:** Show the inferred mode and signals. Offer migrate / optimize / "let me explain". This question always fires; it gates the rest of the audit.

Then ask gaps the artifacts can't reveal (modality trait matrix):

2. **Barge-in available?** Will the platform allow the user to interrupt agent utterances?
3. **Screen fallback for handoff?** Can the agent transfer to a screen experience if voice fails?
4. **Async (SMS) fallback?** Is SMS available for tier-3 repair, email handoff, or callback links?
5. **Carrier-side pre-call announcement?** Can disclosures (recording, AI) play before the agent connects?

Additional gap questions if not inferable:
- Languages and audience constraints
- Confirmed primary use case if the Script is multi-intent

Skip any question whose answer is already visible in the Script or sample.

**Question format:** Batch independent questions into a single `AskUserQuestion` call. Use single-select for booleans, multi-select where multiple answers apply.

## Phase 4 — Audit + Rewrite

Run the audit per `references/audit-rubric.md`. For each row in the rubric, produce one of:

- `[changed]` — voice principle violated or absent, rewrite applied
- `[ok]` — principle already respected (counts in summary, not surfaced inline)
- `[review needed]` — voice principle violated AND original logic shows intentionality signal; preserve original, flag conflict
- `[consider]` *(optimize mode only)* — principle present but applied weakly; suggestion, no rewrite, no preservation
- `[out-of-scope]` — pattern detected that source library doesn't cover

### Conflict policy (mode-dependent — load-bearing, do not override)

**Strong intentionality signals** (preserve in BOTH modes):
- Explicit compliance/regulatory language ("PCI", "GDPR consent", "must record", "required by")
- Comment marking the directive as fixed
- Bundled question that asks for items legally bound together

**Weak intentionality signals** (preserve in MIGRATE only; flag in OPTIMIZE):
- Repeated assertion of the same rule across multiple turns
- Pattern repeated across topics

**No intentionality signal:** rewrite as `[changed]` in both modes.

The bar shift: in migrate mode, "the designer probably knew what they were doing" is the working assumption. In optimize mode, "the designer wants my opinion" is the working assumption.

### Optimize-mode-specific check class

Optimize mode adds **mis-application checks** (see `audit-rubric.md` for the full table): principle is present but applied wrong. Examples:
- P10-mis-1: Repair tier 2 prompt is identical/near-identical to tier 1 → `[consider]`
- P11-mis-1: Phrasebook has fewer than 3 tokens per function → `[consider]`
- P2-mis-1: Grounding policy treats phone/email/money as low-stakes → `[changed]`
- T-opening-mis-1: Two-voice opening system layer uses contractions → `[changed]`

Run mis-application checks in migrate mode too — they usually return `[ok]` (the principle isn't there to be mis-applied), but they catch half-migrated scripts.

## Phase 5 — Write Output

Use `templates/rewrite-bundle.md` as the skeleton. Write to `_local/generated/[agent-name]-voice-{migration,optimization}.md`.

The output frontmatter records the mode, the mode rationale (signals that drove the inference), and the developer's confirmation.

**Layer A — Rewritten instructions (LLM-facing):** Voice best practices baked in as directives. Includes turn structure rules, grounding policy by field type, repair escalation ladder as conditional behavior, latency communication patterns, sequential gathering rules. Opinionated text the LLM acts on at runtime.

**Layer B — Rewritten user-facing copy:** Every changed string with original quote, rewritten quote, principle citation. In optimize mode, mostly short; in migrate mode, often substantial.

**Layer C — Persona phrasebook:** 3–6 rotating tokens per function. In optimize mode, the existing phrasebook is the starting point; check coherence and completeness.

**Layer D — Opening sequence:** Two-voice structure if applicable. In optimize mode, audit the existing opening for system-layer contractions, agent-layer length, contrast, and handover pause.

**Layer E — Out-of-Agent-Script notes:** Items that cannot be encoded in instructions/copy.

**Inline audit section:** Every `[changed]`, `[review needed]`, `[consider]`, and `[out-of-scope]` entry with citation. Top-level summary table with counts per category and tag.

## Phase 6 — Hand-back

After writing, summarize for the developer:
- Mode used and why
- Counts: changed / review needed / consider / out-of-scope / ok per category
- Top 3 review-needed and consider items with one-line context
- Layer E item count (work still owed to platform/runtime owner)
- Synthetic-sample warnings if applicable
- Path to the migration/optimization bundle

Do not re-summarize the rewrite content — they can read it.

## What this skill does NOT do

- **Persona design** — use `agent-persona`. If extraction reveals the source has no coherent persona, recommend that skill but don't invoke it.
- **Topic / action / tool restructuring** — preserved as-is. If the audit reveals a topic structure that fundamentally fights voice (e.g., a single mega-topic that should be three), surface as `[review needed]` with a recommendation, do not refactor.
- **Multi-intent / context-switching mid-conversation** — gap in source library; flag as `[out-of-scope]`
- **Emotional de-escalation** — gap in source library; flag as `[out-of-scope]`
- **Multilingual generation** — flag languages in audit; do not generate non-English copy
- **Runtime/platform configuration** — surfaced as Layer E for human handoff
- **Voice agent QA / testing** — use `testing-agentforce`

## Verification (for skill maintenance)

Self-checks the skill should run before declaring the work complete:

1. **Mode detection:** Mode was inferred AND surfaced to the developer with the signals behind it. The developer confirmed (or overrode).
2. **Layer integrity:** Each layer (A–E) is independently usable. Developer can drop Layer A into instructions without untangling other layers.
3. **Citation coverage:** Every `[changed]`, `[review needed]`, and `[consider]` entry has a `why:` citation pointing to a specific principle ID or mis-application ID.
4. **Conflict policy:** No silent overrides of original business logic. If voice principle and original logic disagree AND strong intentionality signal present, output is `[review needed]` regardless of mode. If only weak intentionality signal, behavior matches the mode (preserve in migrate, flag in optimize).
5. **Optimize-mode mis-application coverage:** In optimize mode, every principle present in the source was checked against its mis-application list, not just its presence.
6. **Trait sensitivity:** Rewrites against the same Script with different modality traits produce meaningfully different Layer D and Layer E outputs.
7. **Synthetic-sample stamping:** If sample was synthesized, every artifact derived from it carries the `synthetic — verify against real flow` warning.

## File layout

```
voice-ux-for-agent-script/
├── SKILL.md                          # This file
├── README.md                         # External-facing brief
├── references/
│   ├── voice-ux-principles.md        # 12 principles + mis-applications
│   ├── telephony-patterns.md         # T-translate, T-grounding, T-repair, T-latency, T-phrasebook, T-opening + mis-applications
│   └── audit-rubric.md               # Coverage contract, mis-application checks, mode-dependent conflict policy, mode-detection signals
└── templates/
    ├── rewrite-bundle.md             # Output skeleton (Layers A–E, mode-aware)
    └── synthetic-sample.md           # Synthesized-sample skeleton (mode-aware)
```
