# voice-ux-for-agent-script

Salesforce Agentforce skill: apply voice UX expertise to an Agent Script.

## What it does

Two modes:

- **Migrate** — takes a text-based Agent Script and produces a voice-optimized rewrite.
- **Optimize** — takes an existing voice Agent Script and improves it, flagging principles applied weakly (`[consider]` tier) and surfacing mis-applications (e.g., repair tier 2 identical to tier 1, phrasebook with too few tokens, grounding policy treating phone numbers as low-stakes).

Mode is auto-detected from the source's text-shaped vs. voice-shaped signals; the developer confirms or overrides. Both modes produce the same output shape; the audit content differs.

Voice UX best practices are baked directly into the LLM-facing instructions, not surfaced as advisory tables. Original business logic is preserved; conflicts with voice principles surface as `[review needed]` flags rather than silent overrides. The preservation bar is lower in optimize mode (the developer is asking for an opinion).

## What it produces

A single bundle (`_local/generated/[agent-name]-voice-{migration,optimization}.md`) with five labeled layers:

- **Layer A** — Rewritten LLM instructions (turn structure, repair ladder, grounding policy, latency directives)
- **Layer B** — Rewritten user-facing copy strings (welcome, errors, prompts, confirmations)
- **Layer C** — Persona phrasebook (rotating tokens for acknowledgment, holding, repair, resumption, closing)
- **Layer D** — Two-voice opening sequence
- **Layer E** — Out-of-Agent-Script notes (ASR thresholds, silence timers, TTS voice selection, carrier config — for handoff to platform/runtime owner)

Plus an inline audit citing each change to a specific principle, with tags: `[changed]`, `[review needed]`, `[consider]` (optimize only), `[out-of-scope]`.

## When to use

**Migrate mode:**
- You have a working text-based Agentforce Agent Script and want to deploy it on telephony or voice-over-web
- You want to audit a chat-based agent for voice UX issues without committing to a full rewrite

**Optimize mode:**
- You have a voice Agent Script and want a voice UX review
- You suspect voice principles are present but applied wrong (repair tier 2 doesn't actually constrain, phrasebook is sparse, grounding is uniform)
- You're preparing a voice script for stakeholder review or designer handoff

## When NOT to use

- Building a voice agent from scratch with no source script → use `developing-agentforce`
- Designing the agent's persona / voice character → use `agent-persona`
- Running test specs against a voice agent → use `testing-agentforce`
- Analyzing production voice session traces → use `observing-agentforce`
- Configuring TTS voice casting, IVR menus, ASR vendor settings → out of scope (surfaced in Layer E)

## Source material

The skill consults two authoritative references at runtime:

- **Voice UX library** — 12 voice UX principles (P1–P12): barge-in, grounding, no-input/no-match, openings/closings, prosody, sequential gathering, silence/latency, turn design, end-focus, repair, persona phrasebook, voice-to-screen handoff. Each principle includes a "common mis-applications (optimize mode)" subsection. Source: [conversation-design-library-v2](https://github.com/phil-haenggi/conversation-design-library-v2).
- **Cross-cutting telephony patterns** — operational decision tables for grounding policy, repair tiers, latency budget, persona phrasebook scaffold, two-voice opening structure, and 8 chat→voice translation rules. Each table includes mis-application notes for optimize mode.

## File layout

```
voice-ux-for-agent-script/
├── SKILL.md                          # Activation, phases, output contract
├── README.md                         # This file
├── references/
│   ├── voice-ux-principles.md        # 12 principles (P1–P12) + mis-applications
│   ├── telephony-patterns.md         # Operational tables + mis-applications
│   └── audit-rubric.md               # Coverage contract, mis-application checks, mode-dependent conflict policy, mode-detection signals
└── templates/
    ├── rewrite-bundle.md             # Output skeleton (Layers A–E, mode-aware)
    └── synthetic-sample.md           # Synthesized-sample skeleton (mode-aware)
```

## Status

v0.2.1 — refines criteria (openings, two-voice contrast, latency, grounding) following first review pass. v0.2.0 added optimize mode, mode auto-detection, mis-application checks, mode-dependent conflict policy. Renamed from `migrating-text-to-voice` (v0.1.0). Not yet validated against a real audit.
