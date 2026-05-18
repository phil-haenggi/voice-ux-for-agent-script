# Pattern file schema

Every file in `references/patterns/` (except `README.md` and files starting with `_`) MUST follow this shape. The schema is enforced by `scripts/lint-patterns.sh` (run before commit).

## Frontmatter (YAML)

```yaml
---
id: A01                                  # required — unique, matches filename prefix
name: numbered-list-rule                 # required — kebab-case, matches filename
category: system-instructions            # required — one of the 9 categories below
severity: high                           # required — high | medium | low
applies_to: [migrate, optimize]          # required — which mode(s) trigger this
couples_with: [E01, C01]                 # optional — patterns that travel with this one
applies_after: [H01]                     # optional — patterns that must run before this
detection:                               # required — at least one entry
  - regex: '<ol>|<li>|"1\..*2\."'
    in: [welcome, error, instructions]   # which sections to search
  - keyword: "numbered list"
    in: [instructions]
principle_refs: [P6, P9]                 # optional — voice-ux-principles.md citations
pattern_refs: [T-translate-6]            # optional — telephony-patterns.md citations
---
```

### Field reference

| Field | Required | Type | Notes |
|---|---|---|---|
| `id` | yes | string | Format: `<Category><nn>` (e.g., `A01`, `D03`). Must match filename. |
| `name` | yes | string | kebab-case slug. Matches filename body. |
| `category` | yes | enum | See category list below. |
| `severity` | yes | enum | `high` (always rewrite if detected), `medium` (rewrite unless intentionality signal), `low` (`[consider]` in optimize, default-rewrite in migrate). |
| `applies_to` | yes | list | Subset of `[migrate, optimize]`. |
| `couples_with` | no | list of IDs | Other pattern IDs that should be applied as a group. Phase 4 batches these in the findings report. |
| `applies_after` | no | list of IDs | Patterns that must run before this one. Drives the codegen pass order. |
| `detection` | yes | list | One or more detectors. Each has `regex` OR `keyword` OR `structural` (a free-text rule for the LLM), plus optional `in:` listing which sections of the `.agent` file to search. |
| `principle_refs` | no | list of P-IDs | Voice UX principle citations from `references/voice-ux-principles.md`. |
| `pattern_refs` | no | list of T-IDs | Telephony pattern citations from `references/telephony-patterns.md`. |

### Categories

| Category | Code | What it covers |
|---|---|---|
| `system-instructions` | A | Global / per-topic LLM instructions |
| `welcome-and-static` | B | `welcome` and `error` messages |
| `display-formatting` | C | HTML, markdown, click/tap, URLs, chat-window references |
| `input-collection` | D | Spell-confirm loops for postcode, name, DOB, phone, refs |
| `output-presentation` | E | Slot lists, summaries, long messages, speciality lists |
| `crisis-and-safety` | F | Crisis flow, symptom checklists, no-hangup |
| `latency-masking` | G | Progress messages, pre-action narration |
| `configuration` | H | `connection`, `modality voice:`, voice settings |
| `variables` | I | Spoken-format companion variables, pre-chat seeding |

## Body sections (Markdown)

After the frontmatter, the body MUST contain these sections in order. Section headings are exact (`## Why it matters`, etc.) so the lint script can find them.

```markdown
# <pattern name in title case>

## Why it matters
<1–3 sentences. Cite voice-vs-text contrast, regulatory concern, or UX principle.>

## Detection
<How to find this pattern in the source. May restate frontmatter detection rules in human-readable form, plus edge cases.>

## Chat example (before)

> The verbatim chat-shaped string or block.

## Voice example (after) — recommended

> The voice rewrite. Concrete words the agent says.

## Voice example — alternatives
<List 1–3 alternatives, each with a one-line "when to use" rationale.>

## Anti-patterns
<Common mistakes when applying this pattern. Optional but encouraged.>

## Where it lives
<Exact .agent file location: `system.instructions`, topic instructions, action definitions, etc.>

## Mis-applications (optimize mode)
<Optional. Only required if `applies_to` includes `optimize`. Examples of "principle-present-but-applied-weakly" patterns.>
```

Sections marked optional may be omitted, but their headings, if present, must match exactly.

## Filename

`<id>-<name>.md`. Examples:
- `A01-numbered-list-rule.md`
- `D03-date-of-birth.md`
- `H02-pre-chat-seeding.md`

## Validation

Before committing a new pattern, run:

```bash
scripts/lint-patterns.sh
```

The lint checks:
1. Filename matches `id` and `name` in frontmatter.
2. All required frontmatter fields are present.
3. `category` matches the category code in `id` (e.g., `A01` must have `category: system-instructions`).
4. Every `couples_with` and `applies_after` reference resolves to an existing pattern file.
5. Every required body section heading is present.
6. Every `regex` in `detection` compiles.
7. `principle_refs` resolve in `voice-ux-principles.md`; `pattern_refs` resolve in `telephony-patterns.md`.
8. No two pattern files share an `id`.

## Contribution flow

1. Identify the gap (an unhandled chat-ism, or an underspecified existing pattern).
2. Pick the next free `id` in the right category.
3. Copy `_schema.md` as a starting point or copy the closest existing pattern file.
4. Write the chat example from a real (or representative) `.agent` source — never invent.
5. Write the voice example with the spoken words an agent would actually say.
6. Run the lint.
7. PR: include a fixture in `tests/fixtures/` that exercises the new pattern (input snippet + expected rewrite snippet).
