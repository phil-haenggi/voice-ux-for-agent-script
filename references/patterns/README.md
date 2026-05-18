# Pattern catalog

Per-file index of chat→voice migration patterns. Each pattern has a chat example, a recommended voice example, and at least one alternative.

This catalog is the **operational** source of truth used by the audit (Phase 4) and rewrite (Phase 5). The principle reference (`../voice-ux-principles.md`) is the **theoretical** source — patterns cite back to it.

## How the skill uses this catalog

1. **Phase 2 — extraction:** Skill loads only this `README.md` (cheap). Walks each pattern's `detection` block, scanning the source `.agent` and sample. Records hits.
2. **Phase 4 — audit:** Skill loads the body of each *hit* pattern (full content) and applies it. Patterns it didn't hit don't load.
3. **Phase 5 — rewrite:** Skill applies patterns in the order in `## Application order` below.
4. **Phase 6 — hand-back:** Findings cite both the pattern ID (e.g., `A01`) and the principle / telephony-pattern ID (e.g., `P9-end-focus`, `T-translate-6`).

Optional Phase 7/8 (`.agent` generation + publish-with-self-healing) consume the same catalog.

## Categories

| Code | Category | Patterns |
|---|---|---|
| A | system-instructions | A01–A07 |
| B | welcome-and-static | B01–B04 |
| C | display-formatting | C01–C05 |
| D | input-collection (spell-confirm) | D01–D06 |
| E | output-presentation | E01–E04 |
| F | crisis-and-safety | F01–F02 |
| G | latency-masking | G01–G02 |
| H | configuration | H01–H05 |
| I | variables | I01 |

## Pattern index

| ID | Name | Severity | Modes | Couples with |
|---|---|---|---|---|
| A01 | numbered-list-rule | high | migrate, optimize | E01, C02 |
| A02 | confirmation-rule | medium | migrate, optimize | — |
| A03 | numeric-input-as-yes-no | low | migrate | — |
| A04 | one-question-per-turn | high | migrate, optimize | E02 |
| A05 | congratulatory-language-ban | medium | migrate, optimize | — |
| A06 | currency-spoken-form | high | migrate, optimize | I01 |
| A07 | slot-selection-collapse | medium | migrate | E01 |
| B01 | welcome-length | high | migrate, optimize | B02 |
| B02 | welcome-ai-disclosure | high | migrate, optimize | B01 |
| B03 | error-message-voice-readable | medium | migrate, optimize | C01, C03 |
| B04 | pre-chat-variable-interpolation | high | migrate | H02 |
| C01 | html-tags-in-spoken-content | high | migrate | — |
| C02 | markdown-in-spoken-content | high | migrate | — |
| C03 | interface-verbs | high | migrate, optimize | — |
| C04 | url-read-aloud | high | migrate, optimize | E03 |
| C05 | chat-ui-references | high | migrate | — |
| D01 | postcode-collection | high | migrate, optimize | — |
| D02 | name-spell-back | high | migrate | — |
| D03 | date-of-birth | high | migrate, optimize | I01 |
| D04 | phone-number | high | migrate, optimize | — |
| D05 | email-address | medium | migrate | — |
| D06 | reference-numbers | medium | migrate | — |
| E01 | slot-list-presentation | high | migrate, optimize | A01 |
| E02 | summary-readback | high | migrate, optimize | A04 |
| E03 | long-static-messages | high | migrate, optimize | C04 |
| E04 | speciality-list-enumeration | medium | migrate, optimize | — |
| F01 | crisis-flow-no-hangup | high | migrate, optimize | — |
| F02 | red-flag-symptom-checklist | high | migrate, optimize | — |
| G01 | progress-message-required | high | migrate, optimize | — |
| G02 | pre-action-narration | medium | migrate, optimize | — |
| H01 | modality-and-connection-blocks | high | migrate | I01, H03 |
| H02 | strip-pre-chat-seeding | high | migrate | B04 |
| H03 | voice-settings | high | migrate | H01 |
| H04 | pronunciation-dictionary | medium | migrate, optimize | — |
| H05 | key-term-prompting | medium | migrate, optimize | — |
| I01 | spoken-format-companion-variables | high | migrate | A06 |

## Application order

When generating the voice agent (Phase 5 or optional Phase 7), apply patterns in this order so later passes don't overwrite earlier ones:

1. **Configuration** — H01 (`connection`, `modality voice:`), H02 (strip pre-chat seeding), H03 (voice settings).
2. **Variables** — I01 (add spoken-format companions).
3. **System instructions (global)** — A01–A07, B01–B04.
4. **Per-topic system instructions** — A01–A05 reapplied at topic scope.
5. **Per-topic reasoning instructions** — D, E, F, G categories.
6. **Action definitions** — G01 (`progress_indicator_message`).
7. **Strip chat-isms (final pass)** — C01–C05 over every user-visible string.

Patterns with `applies_after:` frontmatter override the default order locally.

## CRITICAL: Per-topic action declarations are NOT duplicates

Each `topic`'s `actions:` block is **scoped** — actions referenced in that topic's `reasoning.instructions` MUST be declared in that topic's `actions:` block. If two topics both call `Validate_Postal_Code`, the action MUST be declared in BOTH topics' `actions:` blocks. Do NOT deduplicate during voice migration. Removing a "duplicate" action declaration breaks publish.

## Coupling

Patterns that cite each other in `couples_with:` should be presented as a group in the findings report. Example: A01 (numbered-list-rule) almost always couples with E01 (slot-list-presentation) — finding one without the other is a bug. Phase 4 surfaces them together: "you have 8 findings clustered around list presentation — apply as a set, or walk through?"

## Adding a pattern

See `_schema.md` for the file format and contribution flow. Every new pattern must include:
- A chat example from a real or representative `.agent` source (never invented).
- A recommended voice example with concrete spoken words.
- At least one alternative.
- A fixture in `tests/fixtures/` exercising the pattern.
