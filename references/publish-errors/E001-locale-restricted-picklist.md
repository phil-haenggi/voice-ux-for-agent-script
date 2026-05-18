---
id: E001
name: locale-restricted-picklist
match:
  regex: "Agent Primary Language.*restricted picklist"
severity: blocking
auto_fix: true
---

# Locale restricted picklist

## Symptom

```
Failed to publish agent with the following errors:
There were custom validation error(s) encountered while saving the affected
record(s). The first validation error encountered was "Agent Primary Language:
bad value for restricted picklist field: en_GB".
```

The validator passes (the `.agent` script compiles), but the platform rejects the locale value when creating the `BotDefinition` record.

## Root cause

`BotDefinition.PrimaryLanguage` is a Salesforce restricted picklist. The accepted values are language-only codes: `en_US`, `fr`, `de`, `es`, `it`, `ja`, etc. Locale variants like `en_GB`, `en_AU`, `fr_CA`, `pt_BR` are NOT valid as primary language — they're only valid as `additional_locales`.

This commonly catches scripts where the source agent was authored with `default_locale: "en_GB"` because the brand or service is region-specific. The script still works, but the platform won't accept the regional code as primary.

## Canonical fix

Set primary to the language-only code; add the regional variant to `additional_locales`:

```yaml
language:
    default_locale: "en_US"      # was: "en_GB"
    additional_locales: "en_GB"  # was: "" (or other)
    all_additional_locales: False
```

Apply via `Edit` to the `.agent` file. Diff:

```diff
 language:
-    default_locale: "en_GB"
-    additional_locales: ""
+    default_locale: "en_US"
+    additional_locales: "en_GB"
     all_additional_locales: False
```

Then re-run:

```
sf agent publish authoring-bundle --api-name <name> --target-org <org>
```

## Manual fallback

If the regional locale isn't accepted as primary AND the customer requires the regional locale exclusively (no fallback to `en_US`):

1. Check the org's supported language list (Setup → Translation Workbench → Supported Languages).
2. Confirm with the platform team whether the org has a custom locale configuration.
3. If `en_GB` truly is required as primary, file a Salesforce platform support case — this is rarely customer-fixable.

In practice, `en_US` as primary with `en_GB` as additional locale gives equivalent runtime behaviour for English UK callers, and the customer-facing voice content (UK spellings, UK turns of phrase) is preserved through the agent's instructions and copy.
