---
id: G01
name: progress-message-required
category: latency-masking
severity: high
applies_to: [migrate, optimize]
detection:
  - structural: "action defined without progress_indicator_message"
    in: [actions]
  - regex: 'progress_indicator_message:\s*"(Loading|Processing)"'
    in: [actions]
principle_refs: [P7]
pattern_refs: [T-latency-pre-announce]
---

# Progress message required

## Why it matters

Voice latency without a verbal cue is interpreted as "the line dropped" or "the agent is stuck". Silence beyond ~700ms is perceptible; >1s triggers user remedial action ("hello? are you there?"). Every action call that takes more than a second needs a verbal pre-announce.

In Agent Script, `progress_indicator_message` is the field. In chat, it's a UI status string ("Validating postcode…"). In voice, it must be **conversational** ("just checking that postcode…") and the action invocation must `include_in_progress_indicator: True` so the runtime voices it during the wait.

## Detection

Source has actions with:
- No `progress_indicator_message` at all
- `progress_indicator_message: "Loading…"` or `"Processing"` (chat-shaped status, not voice-conversational)
- `include_in_progress_indicator: False` or absent (so the message never plays)
- `progress_indicator_message` set but the action is fast (<1s) — not strictly wrong, but unnecessary

## Chat example (before)

```yaml
Validate_Postal_Code:
    description: "..."
    target: "generatePromptResponse://Postal_Code_Validator"
```

(No progress message. In chat, fine — no audible gap. In voice, ~2 seconds of silence.)

```yaml
AgentForce_Appointment_Booking:
    target: "flow://AgentForce_Appointment_Booking"
    include_in_progress_indicator: True
    progress_indicator_message: "Booking Appointment"
```

(Has a message but it's chat-shaped — "Booking Appointment" reads as a status banner, not a sentence.)

## Voice example (after) — recommended

**Conversational message, `include_in_progress_indicator: True`:**

```yaml
Validate_Postal_Code:
    description: "..."
    target: "generatePromptResponse://Postal_Code_Validator"
    include_in_progress_indicator: True
    progress_indicator_message: "Just checking that postcode…"
```

```yaml
AgentForce_Appointment_Booking:
    target: "flow://AgentForce_Appointment_Booking"
    include_in_progress_indicator: True
    progress_indicator_message: "Booking that now — one moment…"
```

**Vary across actions (rotation):**
- Postcode validation: "Just checking that postcode…"
- Hospital lookup: "Let me find your nearest hospitals…"
- Slot search: "Let me check what's available…"
- Booking commit: "Right, booking that now — one moment…"
- Adviser availability: "Just checking who's free…"
- Case creation: "Setting that up for you…"

## Voice example — alternatives

**Generic conversational filler audio** (platform-handled): some voice platforms play a configured filler audio (background hold music, soft tone) during action calls. Configure once at platform level rather than per-action message.

**Pre-action narration in instructions** (couples with G02): for irreversible commits, narrate before the call rather than during, so the caller hears it before the action starts:

```
| Pre-announce: 'Right, booking that now — one moment…'.
| Then call confirm_booking.
```

This combines with the action's `progress_indicator_message` for a layered cue.

## Anti-patterns

- **No message at all.** Caller sits in silence; thinks the call dropped.
- **"Loading…".** Reads as a status word, not conversation. Use a phrasebook holding token.
- **"Processing" / "Please wait".** Same problem — chat status language.
- **`include_in_progress_indicator: False` while having a `progress_indicator_message`.** The message exists but never plays. Misleading config.
- **Same message for fast and slow operations.** "Let me check…" for both a 100ms cache hit and a 12-second multi-system join. The slow case needs warning ("This might take a few seconds — bear with me…").
- **Narrating the action's name.** "Calling Validate_Postal_Code". Implementation detail leak.

## Where it lives

Action definitions inside topic `actions:` blocks AND topic-level `actions:` blocks (per-topic action definitions).

## Mis-applications (optimize mode)

- **Pattern: voice script has progress messages on slow actions but not on medium ones.** A 1-3 second postcode validation gets missed because "it's not that slow". Everything > 1 second needs one.
- **Pattern: voice script has identical messages on all actions.** No rotation. The caller hears "Let me check…" 6 times in 30 seconds. Vary.
- **Pattern: voice script has progress messages but `include_in_progress_indicator: False`.** Misconfigured. Silent wait.
- **Pattern: progress message is too long.** "I'm just running a quick check on the system to find what's available — please bear with me, this may take a moment…" The progress message is itself longer than the wait. Keep <2 seconds spoken.
