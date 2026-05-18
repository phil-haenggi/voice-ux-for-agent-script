# Fixture 02: postcode collection

## Patterns exercised

- **D01** — postcode-collection (Tier-1 / Tier-2 repair ladder, implicit-vs-explicit echo by ASR confidence)
- **G01** — progress-message-required (the `Validate_Postal_Code` action gets a conversational `progress_indicator_message`)
- **B03** — error-message-voice-readable (incidental: the chat-shaped "Provided postal code is invalid" error becomes voice-shaped repair)
- **C03** — interface-verbs (incidental: "Please provide your postcode" → "What's your postcode?")

## What the rewrite must do

1. Replace the chat ask ("Please provide your postcode") with a voice-shaped open question ("What's your postcode?").
2. Add Tier-1 + Tier-2 repair instructions (varied wording, no blame, format prescription only at Tier-2).
3. Add Tier-3 handoff with state preservation.
4. Add an explicit grounding policy: implicit echo on high ASR confidence, letter-by-letter on low.
5. Add `include_in_progress_indicator: True` and a conversational `progress_indicator_message` to `Validate_Postal_Code`.
6. Switch the action's `is_displayable` for `promptResponse` from `True` (chat showed it) to `False` (voice handles repair via instructions, doesn't echo the validator output verbatim).

## What the rewrite must NOT do

- Change the action `target:` (`generatePromptResponse://Postal_Code_Validator` stays).
- Remove the `save_postal_code` action declaration.
- Generate format prescriptions at Tier-1 (anti-pattern).
- Voice the literal "Provided postal code is invalid" verbatim (chat copy, not voice copy).

## Run notes

This fixture verifies that **per-action progress messages** get added correctly. The skill must edit `Validate_Postal_Code` to add `include_in_progress_indicator` AND `progress_indicator_message` AND (in this case) flip `is_displayable: True` to `False` because voice doesn't surface the validator's prompt output to the caller.
