---
id: H03
name: voice-settings
category: configuration
severity: high
applies_to: [migrate]
couples_with: [H01]
detection:
  - structural: "modality voice block has placeholder voice_id"
    in: [config]
  - structural: "modality voice block missing speed/stability/similarity"
    in: [config]
principle_refs: [P5]
---

# Voice settings (audience-driven)

## Why it matters

The voice the agent uses sets the entire register. Defaults are rarely right — they're either too commercial-energetic for clinical contexts or too neutral-monotone for retail. Voice settings should match the audience answers from Phase 3 of the audit (persona register, audience constraints).

Four parameters matter:

| Parameter | Range | Default | When to deviate |
|---|---|---|---|
| `voice_id` | org library | (must select) | Match accent / gender / age to audience |
| `outbound_speed` | 0.7–1.2 | 0.9 | Faster (1.0–1.1) for terse personas; slower (0.80–0.93) for warm/expansive or older audiences |
| `outbound_stability` | 0–1 | 0.85 | Lower (0.55–0.70) for expressive/encouraging; higher (0.85–0.95) for clinical/measured |
| `outbound_similarity` | 0–1 | 0.85 | Keep ≥0.75 — below this the voice drifts |

These are baseline values; tune with voice preview before deploying.

## Detection

Source `modality voice:` block (added by H01) has:
- `voice_id: "REPLACE_ME"` or absent
- Missing `outbound_speed`, `outbound_stability`, `outbound_similarity`
- Settings hardcoded from another org without verification

## Chat example (before)

(Not applicable — chat agents have no voice settings.)

## Voice example (after) — recommended

**Default for warm-clinical UK English (matches Nuffield example):**

```yaml
modality voice:
    voice_id: "<voice_id_from_org_library>"     # e.g., en-GB-Wavenet-B (Google) or similar
    outbound_speed: 0.9
    outbound_stability: 0.85
    outbound_similarity: 0.85
```

**For an encouraging / wellness-coach persona:**

```yaml
modality voice:
    voice_id: "<voice_id_from_org_library>"     # warmer voice
    outbound_speed: 0.92                         # very slightly slower
    outbound_stability: 0.65                     # more expressive
    outbound_similarity: 0.85
```

**For a formal / financial-services persona:**

```yaml
modality voice:
    voice_id: "<voice_id_from_org_library>"     # measured voice
    outbound_speed: 0.95
    outbound_stability: 0.90                     # less variation
    outbound_similarity: 0.88
```

## Voice example — alternatives

**Two-voice opening (couples with B01):** if implementing T-opening's two-voice structure, set the **agent layer** voice here. The **system layer** voice lives in carrier config (Layer E item) — different speaker, more formal.

**Per-locale voice IDs:** in multi-locale agents (`en_GB`, `fr_FR`), each locale needs its own voice ID. Some platforms surface this as a per-locale block; others require runtime selection.

## Anti-patterns

- **Leaving `voice_id` as a placeholder.** Deploy succeeds with platform default. Easy to miss until first voice preview.
- **`outbound_speed: 1.5` for "faster calls".** Above 1.1 is rarely intelligible. Above 1.2 is unusable.
- **`outbound_similarity` below 0.7.** The voice drifts from the original speaker — sounds different turn-to-turn.
- **`outbound_stability: 1.0`.** Monotone. Use 0.85 default and tune down for warmth, never up beyond 0.95.
- **Voice ID from one org used in another.** Voice IDs are org-scoped. Always look up the target org's voice library before setting.
- **Hardcoded voice ID in source-controlled `.agent`.** Better: use a config variable / environment substitution if the deployment target varies.

## Where it lives

`modality voice:` block (added by H01).

## Application order

Apply with H01 (Application order step 1). The voice settings need to be present before any later patterns reference voice behavior.

## Layer E follow-up

The voice IDs themselves come from the org's voice library. The skill cannot invent valid IDs — surface in Layer E:

> **Voice ID selection:** open Agentforce Builder → Voice Settings → pick a voice matching [audience profile]. Verify in voice preview before deploy. If two-voice opening is used, configure a distinct voice for the system layer in carrier config.
