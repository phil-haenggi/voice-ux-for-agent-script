---
id: E002
name: invocation-target-restricted-picklist
match:
  regex: "Invocation Target.*restricted picklist"
severity: blocking
auto_fix: false
---

# Invocation target restricted picklist

## Symptom

```
Failed to publish agent with the following errors:
There were custom validation error(s) encountered while saving the affected
record(s). The first validation error encountered was "Invocation Target: bad
value for restricted picklist field: BusinessHoursUtil".
```

(Or `CXOneService`, or any other Apex class name / Flow API name.)

## Root cause

The org's `Bot...InvocationTarget` field is a restricted picklist that only accepts targets which **already exist** as deployable Apex classes / Flows / Prompt Templates in the target org. The `.agent` references an action with `target: "apex://BusinessHoursUtil"` (or `flow://...` / `generatePromptResponse://...`), but the named target isn't deployed in the org.

This is the most common publish failure when migrating a `.agent` file between orgs. The script compiles because the validator only checks script syntax, not target existence in the target org.

## Canonical fix (no auto-fix — three options for the developer)

The skill cannot auto-deploy missing Apex / Flows / Prompt Templates. Surface the three options to the developer:

### Option 1: Deploy the missing targets first (most realistic)

Find or write the underlying Apex class / Flow / Prompt Template, deploy it, then re-run publish.

```bash
# Identify the missing target from the error
# Locate the class/flow in source control or sandbox
sf project deploy start --metadata ApexClass:BusinessHoursUtil \
  --target-org <org>

# Then re-run agent publish
sf agent publish authoring-bundle --api-name <name> --target-org <org>
```

### Option 2: Remove the action that references the missing target

If the action isn't critical to the agent's flow (e.g., `BusinessHoursUtil` for adviser availability), remove the action declaration AND every reference to it in `reasoning.instructions`. This is what we did during the Nuffield deploy when CXOne wasn't available — the agent falls back to "advisers not available" handling.

Before:
```yaml
reasoning:
    instructions: ->
        | Step 3 — Business Hours: Call check_business_hours.
    actions:
        check_business_hours: @actions.Check_Current_Business_Hours
        # ...
    actions:
        Check_Current_Business_Hours:
            target: "apex://BusinessHoursUtil"
```

After:
```yaml
reasoning:
    instructions: ->
        | Step 3 — Adviser availability: assume not available, fall through to Step 5.
    # check_business_hours binding removed
    # Check_Current_Business_Hours definition removed
```

### Option 3: Replace the target with a stub

Point all references to a single minimal Apex class or Flow that exists in the target org and returns sensible defaults (e.g., always returns `True` for business hours, returns `0` for available agents). Lossy — slot search / booking / etc. won't work — but lets the script publish for end-to-end validation of the conversation flow.

## Manual fallback

If unsure which Apex / Flow to deploy:
1. Run `sf data query --query "SELECT Id, Name FROM ApexClass WHERE Name LIKE '<TargetName>%'" --target-org <org>` to check if a similar class exists.
2. Check the source org's metadata.
3. If the target genuinely doesn't exist and isn't being built, Option 2 (remove the action) is the safe default for sandbox demonstrations.

## Why no auto-fix

Each of the three options has business-logic implications. Option 2 silently disables a feature; Option 3 silently replaces real logic with stubs. Both should be a deliberate developer decision, not auto-applied.
