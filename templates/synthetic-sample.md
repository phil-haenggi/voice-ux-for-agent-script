# Synthetic sample — output skeleton

Used in either mode when no sample conversation was provided. The skill generates a plausible 1-task sample from the source Agent Script's stated capabilities, stamps it, and presents it to the developer for review BEFORE the audit runs. The developer can edit, replace, or accept.

**Mode-specific notes:**
- **Migrate mode:** Source is text-shaped. Synthesis assumes a user typing in chat, then translates to a plausible voice equivalent. The sample shows what the *current* (text) flow looks like — not what the rewrite will produce.
- **Optimize mode:** Source is voice-shaped. Synthesis assumes a phone or voice-over-web user. The sample reveals the script's current voice behavior (including any mis-applications the audit will flag).

Suggested filename: `_local/generated/[agent-name]-synthetic-sample.md`

---

```markdown
# Synthetic sample conversation

> **⚠️ SYNTHETIC — verify against real flow before relying on the audit.**
>
> This conversation was generated from the source Agent Script's stated capabilities. It represents what the script *says* it does, not what real users actually do. Edit any turn that doesn't match real flow, then re-run the audit.

**Mode:** migrate / optimize
**Source script:** [path]
**Source shape:** text-shaped / voice-shaped (per mode)
**Synthesis date:** [YYYY-MM-DD]
**Primary intent assumed:** [one-line summary]
**Capabilities used (from source):** [list of topics/actions exercised]

---

## Provenance per turn

Each turn cites which capability or instruction in the source script it derives from. If a turn has no provenance, it's an assumption — flagged inline.

| Turn | Speaker | Utterance | Source provenance |
|---|---|---|---|
| 1 | Agent | [opening] | system.welcome |
| 2 | User | [first-task input] | _assumed_ — typical opener for [intent] |
| 3 | Agent | [response] | topic:[name] / action:[name] |
| 4 | User | [follow-up] | _assumed_ — typical user volunteer pattern |
| ... | | | |

---

## Assumptions made (for developer review)

> Each item is something the synthesis had to invent. If any is wrong, edit the corresponding turn and re-run.

1. **Primary intent:** Assumed the user enters with [intent]. The source script supports multiple intents — confirm this is the most common.
2. **Field order:** Assumed the user volunteers [field A] before [field B]. Real users may volunteer in a different order.
3. **Repair path:** No repair was triggered in this sample. If real users frequently mishear or mis-speak [field X], add a repair turn.
4. **[other assumption]**

---

## Edits

> If you edit this file, mark which turns you changed:
>
> - [ ] Turn N: [reason]
> - [ ] Turn N: [reason]
>
> Then re-run the migration: it will use your edits.

---

## Next step

Once you've verified or edited the sample, the skill will run the audit + rewrite against THIS sample. If the synthetic sample is wrong, the audit will be wrong.

In optimize mode specifically: a synthetic sample for a voice-shaped script may inadvertently smooth over weaknesses the real flow has. If the script has weak repair, weak grounding, or unrotated phrasebook tokens, the synthesis should *expose* those — not paper over them. If the sample looks suspiciously perfect, that's a signal the synthesis is wrong, not that the script is good.
```
