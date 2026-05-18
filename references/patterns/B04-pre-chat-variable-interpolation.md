---
id: B04
name: pre-chat-variable-interpolation
category: welcome-and-static
severity: high
applies_to: [migrate]
couples_with: [H02]
detection:
  - regex: '\{!@variables\.(First_Name|Last_Name|Postal_Code|Transcript_Id_Formula)\}'
    in: [welcome, error, instructions]
  - structural: "welcome interpolates a variable seeded from MessagingSession"
    in: [welcome]
principle_refs: [P12]
---

# Pre-chat variable interpolation in welcome

## Why it matters

Chat agents often have a pre-chat form that captures `First_Name`, `Postal_Code`, etc. before the conversation starts. The welcome interpolates them ("Hi {First_Name}, …"). On telephony, **there is no pre-chat form** — those linked variables are empty strings. The result: the welcome reads "Hi , I'm your assistant" with a noticeable gap, or the merge field renders as a literal placeholder if the variable scope is misconfigured.

Even when the variables are populated by CTI screen-pop (caller-line-ID matched to a CRM contact), they can be missing for unknown callers. The welcome must handle the empty case.

## Detection

Source `messages.welcome` contains `{!@variables.First_Name}`, `{!@variables.Last_Name}`, `{!@variables.Postal_Code}`, `{!@variables.Transcript_Id_Formula}`, or any other variable typed `linked` and sourced from `@MessagingSession.*__c`.

## Chat example (before)

```
"Hi {!@variables.First_Name}, I'm your Nuffield Health virtual assistant.
Your chat ID is {!@variables.Transcript_Id_Formula}. Please keep this for
reference."
```

Real failure mode in production: the welcome rendered as `Hi , I'm your assistant. Your chat ID is {!$Context.Transcript_Id_Formula}` — the merge field syntax was wrong AND the variable was empty in voice.

## Voice example (after) — recommended

**Strip the interpolation. Use a generic warm welcome:**

```
"Hi, you're through to the Nuffield Health booking line. I can help you book
a consultation or answer questions about our services. What would you like
to do?"
```

**If a name is required for the booking, collect it during conversation:**

> Agent: I can take a few details to book that for you. What's your full name?
>
> User: Sarah Jones.
>
> Agent: Got it, Sarah. What's your date of birth?

The transcript-ID line is dropped entirely — voice users have no way to retain a reference number heard once.

## Voice example — alternatives

**Conditional interpolation if CTI provides screen-pop reliably:**

```
| If patient_first_name is non-empty (from CTI screen-pop), voice:
|   "Hi {patient_first_name}, you're through to the Nuffield Health booking line. ..."
| Otherwise voice the generic welcome.
```

Verify the CTI reliability before using this branch — falling through to "Hi , …" is worse than a generic welcome.

**Reference number for the caller's records:** if a session reference is genuinely needed, send by SMS post-call (Layer E item) rather than reading aloud. If SMS isn't available, drop entirely — TTS-spoken reference numbers are not retainable.

## Anti-patterns

- **Keeping the interpolation "in case CTI populates it".** When it doesn't, the welcome is broken. Always handle the empty case.
- **Reading the transcript ID aloud.** No voice user has retained a multi-character reference number from a single TTS hearing. Drop it.
- **Reading the postcode back from `@variables.Postal_Code` without re-collecting.** Even if CTI provides a postcode, confirm before using it in slot search — the caller may be calling from a number registered to a different address.
- **Using `{!$Context.X}` syntax instead of `{!@variables.X}`.** This is a different bug (wrong merge syntax in source) but surfaces the same way: literal placeholder reaches the user. Fix in source regardless of channel.

## Where it lives

- `messages.welcome` — strip interpolations.
- `before_reasoning:` blocks that copy linked variables into mutable variables — drop entirely (couples with H02).
- Any topic instructions that reference `First_Name`, `Last_Name`, `Postal_Code` as if always populated.
