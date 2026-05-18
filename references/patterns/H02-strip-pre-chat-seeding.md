---
id: H02
name: strip-pre-chat-seeding
category: configuration
severity: high
applies_to: [migrate]
couples_with: [B04]
detection:
  - regex: 'before_reasoning:.*set\s+@variables\.\w+\s*=\s*@variables\.(First_Name|Last_Name|Postal_Code)'
    in: [topics]
  - structural: "topic before_reasoning copies linked variables to mutable ones"
    in: [topics]
principle_refs: [P12]
---

# Strip pre-chat seeding

## Why it matters

Chat agents have a pre-chat form that captures `First_Name`, `Last_Name`, `Postal_Code` etc. before the conversation. Topic `before_reasoning:` blocks then copy those linked variables into mutable `patient_first_name`, `patient_last_name`, etc.

In voice telephony, **there is no pre-chat form**. The linked variables are empty strings. The seeding executes but copies empty values, then downstream logic skips collection because the variables "exist" — and the agent ends up with empty patient details and fails at the booking commit.

Worst case: the seeding runs even when the runtime later populates the linked variables from CTI screen-pop, but the seeding has already fired with the empty values and won't re-fire.

This couples with B04 (welcome interpolation) — same root cause, different symptoms.

## Detection

Source has a topic with `before_reasoning:` blocks like:

```
before_reasoning:
    if @variables.new_postal_code == "" and @variables.validated_postal_code == "":
        set @variables.new_postal_code = @variables.Postal_Code
    if @variables.First_Name != "" and @variables.Last_Name != "":
       set @variables.patient_first_name = @variables.First_Name
       set @variables.patient_last_name = @variables.Last_Name
```

Specifically: copying `@variables.First_Name`, `@variables.Last_Name`, `@variables.Postal_Code` (linked, sourced from `@MessagingSession.*__c`) into mutable booking variables.

## Chat example (before)

```yaml
before_reasoning:
    if @variables.new_postal_code == "" and @variables.validated_postal_code == "":
        set @variables.new_postal_code = @variables.Postal_Code
    if @variables.First_Name != "" and @variables.Last_Name != "":
       set @variables.patient_first_name = @variables.First_Name
       set @variables.patient_last_name = @variables.Last_Name
```

## Voice example (after) — recommended

**Drop the seeding entirely. Collect via voice prompts.**

```yaml
before_reasoning:
    # Pre-chat seeding removed for voice channel.
    # patient_first_name, patient_last_name, validated_postal_code collected
    # during conversation per Phase 1 / Phase 2 instructions.
```

Or, if the file has no other `before_reasoning:` content, omit the block entirely.

The reasoning instructions then handle the empty case explicitly:

```
| VOICE CHANNEL — postcode and name may be empty when the caller arrives by
| phone. If validated_postal_code is empty, ask the caller for a postcode
| before slot search. If patient_first_name / patient_last_name are empty,
| collect during Phase 2.
```

## Voice example — alternatives

**Conditional seeding from CTI screen-pop:** if the runtime reliably forwards caller-line-ID + CRM lookup into `First_Name`/`Last_Name`, keep the seeding but add a guard to handle the empty case downstream:

```yaml
before_reasoning:
    if @variables.First_Name != "" and @variables.Last_Name != "":
       set @variables.patient_first_name = @variables.First_Name
       set @variables.patient_last_name = @variables.Last_Name
```

(Note: the original `Postal_Code` seeding line is dropped — postcode from CTI is rarely accurate for the caller's appointment-search needs.)

This alternative is the original behaviour minus the postcode line — safe because the `if` guard skips the assignment when the linked variables are empty.

**Multimodal voice-over-web** where pre-chat metadata may be passed: keep the seeding but verify the runtime contract.

## Anti-patterns

- **Keeping the seeding "just in case CTI populates".** When CTI doesn't, the empty values silently corrupt downstream state.
- **Removing the seeding but keeping the welcome that interpolates `First_Name`.** B04 violation. Apply both.
- **Seeding `validated_postal_code` directly from `Postal_Code`.** Skips the validation action — invalid postcode goes straight into the booking flow. Even when seeding, route through `Validate_Postal_Code`.

## Where it lives

`before_reasoning:` blocks of every topic that does this — typically `Appointment_Management` and sometimes `GeneralFAQ`. Audit every topic.

## Application order

Apply early (Application order step 1, alongside H01). Reasoning instructions reference seeded variables in many places — strip the seeding first so downstream patterns can rely on the empty case being handled in conversation.
