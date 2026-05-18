---
id: B02
name: welcome-ai-disclosure
category: welcome-and-static
severity: high
applies_to: [migrate, optimize]
couples_with: [B01]
detection:
  - structural: "welcome lacks any of: 'AI', 'virtual assistant', 'automated', 'bot'"
    in: [welcome]
principle_refs: [P4]
pattern_refs: [T-opening]
---

# Welcome AI disclosure

## Why it matters

Voice channels have no UI label, avatar, or "Bot" badge — the only way the user knows they're speaking to an AI is the agent telling them. Most jurisdictions now require AI disclosure on voice channels (EU AI Act, FTC guidance, several US states, UK ICO guidance for healthcare and financial services). It's also a trust requirement: callers expect to know if they're being recorded and if they're talking to a machine.

In chat the disclosure can be implicit (the chat window says "Virtual assistant"). In voice it must be in the spoken opening.

## Detection

Source `messages.welcome` (or equivalent) does NOT contain any of:
- "AI" / "AI assistant"
- "virtual assistant"
- "automated assistant" / "automated service"
- "bot"
- "this call may be recorded" (implies, but doesn't state, automated)

If none are present, the disclosure is missing.

## Chat example (before)

```
"Hi, I'm your Nuffield Health assistant. How can I help you today?"
```

(No disclosure that "assistant" means AI rather than a human service rep.)

## Voice example (after) — recommended

**Disclosure in the system layer (preferred — couples with B01):**

> System layer: "You've reached Nuffield Health. This call may be recorded for training and quality. You're speaking with our automated assistant."
>
> [600–900ms pause]
>
> Agent layer: "Hi, you're through to the Nuffield Health booking line. I can help you book a consultation or answer questions about our services. What would you like to do?"

**Disclosure in agent layer (single-layer welcome):**

> "Hi, you're through to Nuffield Health — you're speaking with our virtual assistant. I can help you book a consultation or answer questions. What would you like to do?"

## Voice example — alternatives

**"AI assistant" wording:** more direct, slightly less warm.
> "Hi, this is the Nuffield Health AI assistant."

**"Automated service":** more formal, financial-services register.
> "You've reached Nuffield Health's automated service line."

Pick the wording that matches the persona register (Layer C). Don't mix — pick one and use it consistently.

## Anti-patterns

- **Disclosure buried mid-sentence.** "Hi, welcome to Nuffield Health, where we offer a range of services and our AI assistant can help you book today." The disclosure is there but lost in the prose.
- **Disclosure only on first turn but not when the user explicitly asks "am I talking to a bot?".** Some compliance regimes require an in-conversation disclosure on demand. Add a global rule: "If the caller asks whether they're speaking to a person or a machine, voice 'I'm an automated assistant — I can help with [X], or put you through to a person if you'd prefer.'"
- **Disclosure in the system layer but the system layer plays before the call connects.** Carrier-side pre-call announcements may be considered insufficient by some regulators (caller may have started speaking, missed it). Verify with legal.
- **Implying agency the agent doesn't have.** "I'm your Nuffield Health agent" reads ambiguous — could be human or AI. Pick a word that's unambiguously machine.

## Where it lives

`messages.welcome` (agent layer) and the system-layer content (carrier config or prepended welcome). The disclosure may also appear in a separate `system.disclosure` field if the runtime supports it.

## Mis-applications (optimize mode)

- **Pattern: disclosure present but the wording reads as marketing not disclosure.** "Welcome to our AI-powered booking experience!" — uses the word AI but in a promotional register. Compliance audit may not accept this. Reword to direct disclosure ("you're speaking with our automated assistant").
- **Pattern: disclosure on call open but the agent later says "let me check with my team" or similar.** Implies a human team behind the AI. Fix by removing first-person plural references that imply colleagues.
