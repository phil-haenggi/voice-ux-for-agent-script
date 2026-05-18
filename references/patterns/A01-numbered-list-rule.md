---
id: A01
name: numbered-list-rule
category: system-instructions
severity: high
applies_to: [migrate, optimize]
couples_with: [E01, C02]
detection:
  - regex: '<ol>|<li>|"\s*1\..*2\..*"'
    in: [welcome, error, instructions, response_templates]
  - keyword: "numbered list"
    in: [instructions]
  - keyword: "select option"
    in: [instructions]
principle_refs: [P6, P9]
pattern_refs: [T-translate-6, T-translate-1]
---

# Numbered list rule

## Why it matters

Voice users can't scan a list. Numbered options force the user to count from 1 and remember which number maps to which option. By the time the agent finishes reading "5", the user has forgotten "1". This is **end-focus violation** (P9) — the most important content (the choices themselves) is buried before the question. It also implicitly bundles N decisions into one turn, violating P6.

## Detection

Source contains either:
- HTML list markup (`<ol>`, `<li>`)
- Numbered-text patterns ("1. … 2. … 3. …")
- Instruction prose telling the agent to "use a numbered list", "present options as 1., 2., 3.", or "ask user to select option N"
- The phrase "providing the corresponding number" anywhere in instructions

## Chat example (before)

```
Here are the available slots:
1. 05 May 2026 at 5:30 PM
2. 05 May 2026 at 6:00 PM
3. 05 May 2026 at 6:30 PM
4. 12 May 2026 at 7:00 PM
Please select a slot by providing the corresponding number.
```

## Voice example (after) — recommended

**Progressive disclosure — group by salient axis (day), then narrow to time:**

> Agent: I've got slots on Tuesday the fifth of May, and Tuesday the twelfth. Which day suits you?
>
> User: The fifth.
>
> Agent: On Tuesday the fifth, I've got five-thirty, six o'clock, or six-thirty in the evening. Which works?

Accept natural responses: "the earliest", "the first one", "five-thirty", "the evening one". Never require slot numbers.

## Voice example — alternatives

**Top-match plus offer:** for low-decision-cost cases (single recommendation):
> Agent: The earliest is Tuesday the fifth at five-thirty, with Andrew McLeod at Newcastle. Want that, or hear other times?

**Sequential one-at-a-time:** when each option needs explanation:
> Agent: Tuesday the fifth at five-thirty — works for you? [pause for "no"]
> Agent: How about Tuesday the fifth at six o'clock?

**Cap at 2 items:** for binary choices:
> Agent: Tuesday at five-thirty, or Tuesday at six?

## Anti-patterns

- **Reading the numbers aloud.** "One, Tuesday at five-thirty. Two, Tuesday at six. Three…" — keeps the chat structure, sounds robotic, still violates P6.
- **Asking "which option?".** Forces the user to use chat-shaped vocabulary.
- **Reading all 10 slots and asking for a number.** Worst possible voice form — the user is asked to remember 10 things, then count.
- **Using ordinals as a numbered-list workaround.** "First, second, third, fourth…" reads marginally better than digits but still requires the user to count.

## Where it lives

- Global `system.instructions` — strip the rule "When presenting multiple options, always use a numbered list".
- Per-topic `system.instructions` — same.
- `reasoning.instructions` blocks that present slots, payment options, escalation menus, no-availability menus.
- Response templates that hard-code numbered output.

## Mis-applications (optimize mode)

- **Pattern: list converted to disjunction but still has 4+ items.** "Tuesday five-thirty, or six, or six-thirty, or seven, or twelve at seven." The disjunction shape is right but the count is too high — apply progressive disclosure.
- **Pattern: instructions say "ordered list" instead of "numbered list".** Same problem, different word — still triggers TTS to read enumeration.
- **Pattern: agent replaces numbers with letters.** "A, Tuesday at five-thirty. B, Tuesday at six." Same anti-pattern.
