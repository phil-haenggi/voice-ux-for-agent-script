---
name: migrating-text-to-voice
description: >
  Migrates a text-based Salesforce Agentforce Agent Script into a voice-optimized
  Agent Script. Ingests the existing Script plus an optional sample conversation,
  audits both against voice UX principles (12 from the conversation design library)
  and operational telephony patterns (grounding policy, repair tiers, latency
  budget, persona phrasebook, two-voice opening), and produces a layered rewrite:
  rewritten LLM instructions with voice behavior baked in (repair, grounding,
  latency directives), rewritten user-facing copy, persona phrasebook, opening
  sequence, and out-of-Agent-Script notes for runtime/platform owners. Preserves
  original business logic; surfaces conflicts with voice best practice as
  `review needed` rather than silently overriding.

  TRIGGER when: user asks to migrate, port, convert, or "make voice-ready" /
  "telephony-ready" an existing text-based Agent Script; user asks to audit a
  chat-based Agentforce agent for voice UX issues; user has a working text Agent
  Script and is starting voice work.

  DO NOT TRIGGER when: building a voice agent from scratch with no source Script
  (use developing-agentforce); designing the agent persona/voice character
  (use agent-persona); running test specs against a voice agent (use
  testing-agentforce); analyzing production voice session traces (use
  observing-agentforce); configuring TTS voice casting, IVR menu structure, or
  ASR vendor settings (out of scope — surfaced in Layer E for handoff).
version: 0.1.0
date: 2026-05-13
author: phil-haenggi
tags: [salesforce, agentforce, agent-script, voice, telephony, migration, voice-ux, conversation-design, repair, grounding, latency, phrasebook, two-voice-opening]
allowed-tools:
  - Read
  - Write
  - Edit
  - AskUserQuestion
  - Glob
  - Grep
---

# Text-to-Voice Migration

## How to Use

This skill takes a working text-based Agent Script and produces a voice-optimized rewrite. Provide the source Script (required) and a sample conversation (recommended). The skill audits both against voice UX principles, then writes a layered output bundle the developer can drop directly into the Agent Script — with voice behavior (repair, grounding, latency) baked into the LLM instructions, not surfaced as advisory tables.

**What it produces:**
- A migration bundle (`_local/generated/[agent-name]-voice-migration.md`) with five labeled layers (instructions, copy, phrasebook, opening, out-of-script notes) plus an inline audit
- A synthetic sample (`_local/generated/[agent-name]-synthetic-sample.md`) when no real sample is provided

**What it does not do:** Build voice agents from scratch. Design the agent's persona/voice character. Run runtime QA. Configure TTS/ASR/IVR. Generate non-English copy. Resolve multi-intent or emotional-de-escalation patterns (gaps in the source library — flagged as `out-of-scope`).

## When to Use This Skill

- Migrating a working text-based Agentforce Agent Script to voice (telephony or voice-over-web)
- Auditing a chat-based Agentforce agent for voice UX issues without committing to a full rewrite
- Preparing an Agent Script for telephony deployment when the current copy and instructions assume a screen and keyboard

**Scope boundary:** This skill rewrites *what the agent says and how it behaves* for voice. It does not touch the agent's persona, topic structure, or actions/tools — those are unchanged. It does not configure runtime/platform settings — those are surfaced as Layer E recommendations.

## Reference Material

The skill consults three local references at runtime. Do not regenerate from external sources — read these.

- `references/voice-ux-principles.md` — 12 voice UX principles (P1–P12) with citation IDs, voice-vs-text contrasts, and migration heuristics. Source of `why:` lines in audit.
- `references/telephony-patterns.md` — operational decision tables: 8 chat→voice translation rules (T-translate-1..8), grounding policy by field type (T-grounding), repair tier ladder (T-repair-tier-1..3), latency budget (T-latency), persona phrasebook scaffold (T-phrasebook), two-voice opening (T-opening).
- `references/audit-rubric.md` — coverage contract mapping each principle and pattern to a check the audit must perform. Drives audit completeness.

## Phase 1 — Artifact Intake

**Required input:** Path to or contents of the source Agent Script (`.agent` file, YAML, or text instructions).

**Optional input:** Path to or contents of a sample conversation showing the main use case.

**Behavior:**
1. Read the source Script. Identify topics, actions, system instructions, welcome/error/copy strings.
2. If a sample is provided, read it. Verify the sample exercises the primary intent the developer cares about.
3. If no sample is provided, **synthesize one** using `templates/synthetic-sample.md` as the skeleton. Generate a plausible 1-task conversation from the Script's stated capabilities, stamp it `synthetic — verify against real flow`, write it to `_local/generated/[agent-name]-synthetic-sample.md`, and **show it to the developer for review BEFORE proceeding to audit**. The developer can edit, replace, or accept.

Do not proceed to Phase 2 until the sample (real or synthetic-and-acknowledged) is settled.

## Phase 2 — Automated Extraction

Before asking the developer anything, extract from the artifacts:

- **Modality signals** — UI references ("click", "see below"), DTMF cues, screen affordances, links, file uploads → suggests current modality is text/web
- **Audience tone** — register, formality, contractions usage
- **Primary intents** — list of topics with descriptions
- **Action set** — tools/actions invoked, their expected latency profile
- **Existing grounding logic** — confirmation patterns, field-by-field handling
- **Existing repair logic** — error messages, escalation paths
- **Persona signals** — acknowledgment patterns, discourse markers (feeds Layer C)

Surface what was inferred to the developer so they can correct.

## Phase 3 — Gap-fill Diagnostic

Use `AskUserQuestion`. Ask **only** what the artifacts cannot reveal. Skip any question whose answer is already visible in the Script or sample.

Required gaps to fill (modality trait matrix):

1. **Barge-in available?** Will the platform allow the user to interrupt agent utterances?
2. **Screen fallback for handoff?** Can the agent transfer to a screen experience if voice fails?
3. **Async (SMS) fallback?** Is SMS available for tier-3 repair, email handoff, or callback links?
4. **Carrier-side pre-call announcement?** Can disclosures (recording, AI) play before the agent connects?

Additional gap questions if not inferable:
- Languages and audience constraints
- Confirmed primary use case if the Script is multi-intent

**Question format:** Batch independent questions into a single `AskUserQuestion` call. Use single-select for booleans, multi-select where multiple answers apply.

## Phase 4 — Audit + Rewrite

Run the audit per `references/audit-rubric.md`. For each row in the rubric, produce one of:
- `[changed]` — voice principle violated, rewrite applied
- `[ok]` — principle already respected (counts in summary, not surfaced inline)
- `[review needed]` — voice principle violated AND original logic shows intentionality signal (compliance, repeated assertion, regulatory flag); preserve original, flag conflict
- `[out-of-scope]` — pattern detected that source library doesn't cover; surface, do not rewrite

**Conflict policy** (this is load-bearing, do not override):

When the source Script directs behavior that contradicts a voice principle AND there's a signal of intentionality (compliance language, repeated assertion across turns, explicit business-rule comment), **preserve the original** and emit a `[review needed]` entry. Never silently rewrite around an intentional business rule. The developer makes the call per item.

Intentionality signals:
- Explicit compliance/regulatory language ("PCI", "GDPR consent", "must record", "required by")
- Same rule asserted across multiple turns or topics
- Comment marking the directive as fixed
- Bundled question that asks for items legally bound together

Single occurrence of suboptimal copy is NOT an intentionality signal.

## Phase 5 — Write Output

Use `templates/rewrite-bundle.md` as the skeleton. Write to `_local/generated/[agent-name]-voice-migration.md`.

**Layer A — Rewritten instructions (LLM-facing):** Voice best practices baked in as directives. Includes turn structure rules, grounding policy by field type, repair escalation ladder as conditional behavior, latency communication patterns, sequential gathering rules. This is opinionated text the LLM acts on at runtime — not a table for the developer to interpret.

**Layer B — Rewritten user-facing copy:** Every changed string with original quote, rewritten quote, principle citation. Apply T-translate-1..8 to every user-facing utterance.

**Layer C — Persona phrasebook:** 3–6 rotating tokens per function (acknowledgment, holding, repair, resumption, pre-closing, terminal). Match the source agent's register. Use T-phrasebook as scaffold; tune to persona signals from Phase 2.

**Layer D — Opening sequence:** Two-voice structure if applicable. System-layer content goes to Agent Script welcome OR Layer E (carrier pre-call), depending on trait matrix answer. Agent layer always goes to Agent Script welcome.

**Layer E — Out-of-Agent-Script notes:** Each item with what / where it lives / recommended value / why it matters. Include only items the rewrite implies (don't pad). Examples: ASR confidence threshold (if grounding escalation references it), silence timer values (if Phase 4 flagged unannounced latency), barge-in detection toggle (if Layer A relies on it), TTS voice selection (if two-voice opening is in play), SSML support (if P5-prosody recommendations were made), carrier-side pre-call announcement config (if trait matrix answered yes), call-back option config (if any T-latency-long flag).

**Inline audit section:** Every `[changed]`, `[review needed]`, and `[out-of-scope]` entry with citation. Top-level summary table with counts per category.

## Phase 6 — Hand-back

After writing, summarize for the developer:
- Counts: changed / review needed / out-of-scope / ok per category
- Top 3 review-needed items with one-line context
- Layer E item count (work still owed to platform/runtime owner)
- Synthetic-sample warnings if applicable
- Path to the migration bundle

Do not re-summarize the rewrite content — they can read it.

## What this skill does NOT do

- **Persona design** — use `agent-persona`. If the Phase 2 extraction reveals the source has no coherent persona, recommend that skill but don't invoke it.
- **Topic / action / tool restructuring** — preserved as-is. If the audit reveals a topic structure that fundamentally fights voice (e.g., a single mega-topic that should be three), surface as `[review needed]` with a recommendation, do not refactor.
- **Multi-intent / context-switching mid-conversation** — gap in source library; flag as `[out-of-scope]`
- **Emotional de-escalation** — gap in source library; flag as `[out-of-scope]`
- **Multilingual generation** — flag languages in audit; do not generate non-English copy
- **Runtime/platform configuration** — surfaced as Layer E for human handoff
- **Voice agent QA / testing** — use `testing-agentforce`

## Verification (for skill maintenance)

Self-checks the skill should run before declaring the migration complete:

1. **Layer integrity:** Each layer (A–E) is independently usable. Developer can drop Layer A into instructions without untangling other layers.
2. **Citation coverage:** Every `[changed]` entry has a `why:` citation pointing to a specific principle ID.
3. **Conflict policy:** No silent overrides of original business logic. If voice principle and original logic disagree AND intentionality signal present, output is `[review needed]` not `[changed]`.
4. **Trait sensitivity:** Rewrites against the same Script with different modality traits produce meaningfully different Layer D and Layer E outputs.
5. **Synthetic-sample stamping:** If sample was synthesized, every artifact derived from it carries the `synthetic — verify against real flow` warning.

## File layout

```
migrating-text-to-voice/
├── SKILL.md                          # This file
├── README.md                         # External-facing brief
├── references/
│   ├── voice-ux-principles.md        # 12 principles, citation IDs P1–P12
│   ├── telephony-patterns.md         # T-translate, T-grounding, T-repair, T-latency, T-phrasebook, T-opening
│   └── audit-rubric.md               # Coverage contract + conflict policy + out-of-scope detection
└── templates/
    ├── rewrite-bundle.md             # Output skeleton (Layers A–E)
    └── synthetic-sample.md           # Synthesized-sample skeleton with stamping
```
