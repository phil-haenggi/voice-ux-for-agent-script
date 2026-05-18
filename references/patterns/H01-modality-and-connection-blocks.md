---
id: H01
name: modality-and-connection-blocks
category: configuration
severity: high
applies_to: [migrate]
couples_with: [I01, H03]
detection:
  - regex: '^connection messaging:'
    in: [config]
  - structural: "no `connection telephony:` block"
    in: [config]
  - structural: "no `modality voice:` block"
    in: [config]
principle_refs: [P4]
---

# Modality and connection blocks

## Why it matters

Chat agents typically have only `connection messaging:` configured. Voice agents need additional config:
- `connection telephony:` — declares telephony support and runtime parameters (adaptive response, etc.)
- `modality voice:` — voice settings (voice_id, speed, stability, similarity)
- Optionally `connection customer_web_client:` for voice-over-web multimodal

Without these, the agent will fail to deploy as a voice agent, or will deploy but use the platform default voice (which is usually not what you want for a branded experience).

This pattern is **deployment-blocking**: missing voice config means the agent doesn't function on voice channels at all. Apply early in Phase 5/7 (Application order step 1).

## Detection

Source `config:` block has only `connection messaging:`, with no `connection telephony:` and no `modality voice:`.

## Chat example (before)

```yaml
config:
    developer_name: "Customer_Support_Assistant_script"
    agent_label: "Customer Support Assistant"
    agent_type: "AgentforceServiceAgent"
    enable_enhanced_event_logs: True

connection messaging:
    adaptive_response_allowed: False
```

## Voice example (after) — recommended

**Add telephony connection and voice modality (couples with H03 for the voice-settings values):**

```yaml
config:
    developer_name: "Customer_Support_Assistant_voice"
    agent_label: "Customer Support Assistant (Voice)"
    agent_type: "AgentforceServiceAgent"
    enable_enhanced_event_logs: True

connection telephony:
    adaptive_response_allowed: True

modality voice:
    voice_id: "<voice_id_from_org_voice_library>"
    outbound_speed: 0.9
    outbound_stability: 0.85
    outbound_similarity: 0.85
```

If `connection messaging` is no longer needed (voice-only deployment), remove it. If multimodal (voice-over-web), keep both:

```yaml
connection telephony:
    adaptive_response_allowed: True
connection customer_web_client:
    adaptive_response_allowed: True
modality voice:
    voice_id: "..."
    outbound_speed: 0.9
    outbound_stability: 0.85
    outbound_similarity: 0.85
```

## Voice example — alternatives

**Voice-over-web only** (no telephony): use `connection customer_web_client:` alone, no `connection telephony:`. Voice settings still required.

**Multi-channel (chat + voice in one agent)**: keep `connection messaging` and add `connection telephony` + `modality voice`. The agent must handle both channels gracefully — most teams deploy two separate agents instead. Multi-channel coordination in one agent is a larger design problem.

## Anti-patterns

- **Adding `modality voice:` without `connection telephony:`.** Voice settings exist but the connection isn't declared — agent won't actually run on voice.
- **Configuring `voice_id` as a placeholder string ("REPLACE_ME") and forgetting to fill it in.** Deploy succeeds but the agent uses the platform default voice. Add to Layer E review checklist.
- **Setting `outbound_speed: 1.5` for "faster calls".** Above 1.1 is rarely intelligible. See H03.
- **Hard-coding `voice_id` from one org and deploying to a different org.** Voice IDs are org-scoped. Always verify the ID exists in the target org.

## Where it lives

`config:` block at the top of the `.agent` file. The `connection` and `modality` declarations are siblings of `config`.

## Application order

This pattern is the **first** to apply (step 1 in `README.md` Application order). Other patterns assume the voice connection / modality are present. Run this before any others.
