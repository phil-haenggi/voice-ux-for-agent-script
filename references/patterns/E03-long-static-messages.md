---
id: E03
name: long-static-messages
category: output-presentation
severity: high
applies_to: [migrate, optimize]
couples_with: [C04]
detection:
  - structural: "static message > 30 seconds spoken length"
    in: [response_templates, instructions]
  - keyword: "Terms and Conditions"
    in: [response_templates, instructions]
  - keyword: "privacy policy"
    in: [response_templates, instructions]
  - keyword: "data sharing"
    in: [response_templates, instructions]
principle_refs: [P1, P3]
pattern_refs: [T-grounding-money]
---

# Long static messages

## Why it matters

Voice users will hang up or zone out during a 30-second monologue. Long static content (T&Cs, privacy disclaimers, regulatory statements) is the worst offender — it's the chat-shaped solution to a regulatory requirement, but reading it aloud is hostile.

Two competing constraints:
- **Compliance**: legal/regulatory may require explicit caller acknowledgment of certain content.
- **UX**: a 90-second T&Cs read is unacceptable.

The fix is **substance compression** + **paraphrased link**: voice the substantive obligations (cancellation policy, data sharing, key restrictions), reference the full text on the website, then ask for explicit yes/no. If SMS is available, send the full text; voice the compressed version. If not, voice the compressed version and accept regulatory risk in writing with legal.

## Detection

Source has any user-visible static block longer than ~30 seconds spoken (~80–100 words):
- T&Cs acceptance prompts
- Privacy policy text
- Multi-paragraph regulatory disclaimers
- Hard-coded medical disclaimers in specific topics
- Long apologies / explanations

## Chat example (before)

```
"OK, I have everything I need. Progressing further requires that you accept
our <a href=\"https://www.nuffieldhealth.com/terms/...\">Terms and
Conditions</a>. Do you wish to proceed?"
```

In chat, the link does the heavy lifting — the user clicks, reads, returns. In voice, the link doesn't exist (couples with C04).

A worse case: scripts that hard-code multi-paragraph T&Cs in the spoken content because the author tried to make the content "available" without a link. Reads as 60–90 seconds of legal prose.

## Voice example (after) — recommended

**Compressed substantive summary + explicit yes/no:**

> "Before I book, two quick things to agree to. Cancellations within twenty-four hours of the appointment are charged in full. Your details will be shared with the consultant and Nuffield Health to manage your care. The full terms are on the Nuffield Health website. Do you agree, yes or no?"

Three components:
1. **Substance**: voiced obligations (cancellation, data sharing).
2. **Pointer**: paraphrased reference to full text.
3. **Explicit consent**: yes/no, not "OK to proceed?".

**Legal/Compliance must sign off the compressed wording before deploy.** This is a Layer E item.

## Voice example — alternatives

**SMS handoff with audible substance:**

> "I'll text you a link to the full terms now. While you read, the key bits are: cancellations within twenty-four hours are charged in full, and your details get shared with the consultant for your care. Once you've had a look, just say 'I agree' to go ahead."

Verify SMS integration. Strongest from a compliance standpoint when the full text is delivered.

**Read aloud in full** (only when regulatory mandate is explicit and unmovable):

> Voice the full text in chunks ≤3 sentences each, with micro-pauses. Add a "still with me?" check halfway through.

Slow and hostile but legally defensible. Default only when legal absolutely requires.

**Skip if substance is informational, not consent-required.** "We use cookies on our website" is meaningless on voice and not consent-relevant on a phone call. Drop entirely.

## Anti-patterns

- **Reading the URL.** Couples with C04 — chat-shaped link doesn't translate.
- **Reading the full T&Cs verbatim.** 60+ seconds of legal prose. Compliance may demand it; UX hates it. Negotiate with legal.
- **Asking "OK?" instead of "Yes or no?".** "OK" is ambiguous (couples with A02). On consent commits, require explicit yes/no.
- **Including the link as fallback in the voice copy.** "Visit nuffieldhealth dot com slash terms slash blah" — meaningless to a caller without a screen.
- **Re-reading the T&Cs after a mid-flow FAQ detour.** Use light resumption ("Picking up where we were — ready to go through the terms?"), not the full re-read.

## Where it lives

- Phase 4 (T&Cs) of booking topics.
- Privacy/disclaimer paths in any topic.
- Crisis topic message (handled by F01, with different rules).

## Mis-applications (optimize mode)

- **Pattern: voice script compresses the T&Cs but the compression hasn't been signed off by Legal.** Dangerous. Add to Layer E review checklist.
- **Pattern: voice script compresses the T&Cs but doesn't reference the full text on the website.** Compliance gap — the caller is consenting without access to the full terms.
- **Pattern: voice script promises SMS but the integration isn't deployed.** Regression on every call. Verify Layer E item.
- **Pattern: voice script reads the substance but accepts "ok" as agreement.** A02 violation in a consent context — must be explicit yes/no.
