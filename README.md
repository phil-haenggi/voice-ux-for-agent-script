# migrating-text-to-voice

Salesforce Agentforce skill: migrate a text-based Agent Script to a voice-optimized Agent Script.

## What it does

Takes an existing text-based Agent Script (and optionally a sample conversation) and produces an opinionated voice-optimized rewrite — with voice UX best practices baked directly into the LLM-facing instructions, not surfaced as advisory tables. Original business logic is preserved; conflicts with voice principles surface as `review needed` flags rather than silent overrides.

## What it produces

A single migration bundle (`_local/generated/[agent-name]-voice-migration.md`) with five labeled layers:

- **Layer A** — Rewritten LLM instructions (turn structure, repair ladder, grounding policy, latency directives)
- **Layer B** — Rewritten user-facing copy strings (welcome, errors, prompts, confirmations)
- **Layer C** — Persona phrasebook (rotating tokens for acknowledgment, holding, repair, resumption, closing)
- **Layer D** — Two-voice opening sequence
- **Layer E** — Out-of-Agent-Script notes (ASR thresholds, silence timers, TTS voice selection, carrier config — for handoff to platform/runtime owner)

Plus an inline audit citing each change to a specific principle.

## When to use

- You have a working text-based Agentforce Agent Script and want to deploy it on telephony or voice-over-web
- You want to audit a chat-based agent for voice UX issues without committing to a full rewrite

## When NOT to use

- Building a voice agent from scratch with no source script → use `developing-agentforce`
- Designing the agent's persona / voice character → use `agent-persona`
- Running test specs against a voice agent → use `testing-agentforce`
- Analyzing production voice session traces → use `observing-agentforce`
- Configuring TTS voice casting, IVR menus, ASR vendor settings → out of scope (surfaced in Layer E)

## Source material

The skill consults two authoritative references at runtime:

- **Voice UX library** — 12 voice UX principles (P1–P12): barge-in, grounding, no-input/no-match, openings/closings, prosody, sequential gathering, silence/latency, turn design, end-focus, repair, persona phrasebook, voice-to-screen handoff. Source: [conversation-design-library-v2](https://github.com/phil-haenggi/conversation-design-library-v2).
- **Cross-cutting telephony patterns** — operational decision tables for grounding policy, repair tiers, latency budget, persona phrasebook scaffold, two-voice opening structure, and 8 chat→voice translation rules.

## File layout

```
migrating-text-to-voice/
├── SKILL.md                          # Activation, phases, output contract
├── README.md                         # This file
├── references/
│   ├── voice-ux-principles.md        # 12 principles (P1–P12)
│   ├── telephony-patterns.md         # Operational tables (T-translate, T-grounding, T-repair, T-latency, T-phrasebook, T-opening)
│   └── audit-rubric.md               # Coverage contract + conflict policy
└── templates/
    ├── rewrite-bundle.md             # Output skeleton (Layers A–E)
    └── synthetic-sample.md           # Synthesized-sample skeleton with stamping
```

## Status

v0.1.0 — initial scaffold. Not yet validated against a real migration.
