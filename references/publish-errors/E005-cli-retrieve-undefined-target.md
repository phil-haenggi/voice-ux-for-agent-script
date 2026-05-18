---
id: E005
name: cli-retrieve-undefined-target
match:
  regex: "Cannot set properties of undefined \\(setting 'target'\\)"
severity: warning
auto_fix: true
---

# CLI retrieve: "Cannot set properties of undefined (setting 'target')"

## Symptom

```
 ──────────────── Publishing Agent ────────────────

 ✔ Validate Bundle
 ✔ Publish Agent
 ✘ Retrieve Metadata
 ◼ Deploy Metadata

Error (1): Failed to publish agent with the following errors:
Cannot set properties of undefined (setting 'target')
```

Note: `Validate Bundle` and `Publish Agent` both passed (✔). The error is on `Retrieve Metadata`, which is the **post-publish** step that downloads the org-side generated metadata back into the local DX project.

## Root cause

The publish itself completed — the agent **was** created in the org. The CLI then tries to retrieve the platform-generated metadata (BotDefinition, BotVersion, GenAiX records, etc.) and update the local `aiAuthoringBundles/<name>/` directory. Something in the retrieve step throws — typically because the org returned metadata in a shape the CLI version wasn't expecting (e.g., new field added by the platform, CLI version lagging behind).

The error message itself is from a CLI internal — `Cannot set properties of undefined` is a JavaScript runtime error in the retrieve code, not a Salesforce-platform error.

## Canonical fix

Confirm the agent exists in the org (it does — the publish step ✔'d):

```bash
sf data query --query "SELECT Id, DeveloperName, MasterLabel FROM BotDefinition WHERE DeveloperName = '<name>'" --target-org <org>
```

If the row exists with the expected `DeveloperName` and `MasterLabel`, the publish was successful. The retrieve failure is **client-side only** — no impact on what's deployed.

To avoid the error, re-run with `--skip-retrieve`:

```bash
sf agent publish authoring-bundle --api-name <name> --target-org <org> --skip-retrieve
```

This skips the local DX project sync. Fine for voice-migration workflows where the source `.agent` is the canonical artifact and the platform-generated supporting metadata isn't being edited locally.

## Manual fallback

If you do need the local DX project updated (e.g., to track platform-generated changes in source control):

1. Update Salesforce CLI: `sf update`. The retrieve bug is often fixed in a later CLI version.
2. After `--skip-retrieve` publish, manually retrieve:
   ```bash
   sf project retrieve start --metadata AIAuthoringBundle:<name> --target-org <org>
   ```
   Sometimes the standalone retrieve works where the integrated one fails.
3. As a last resort, retrieve the supporting metadata individually:
   ```bash
   sf project retrieve start --metadata Bot:<name> --target-org <org>
   sf project retrieve start --metadata GenAiPlannerBundle:<name> --target-org <org>
   ```

## Why the auto-fix is safe

Re-running with `--skip-retrieve` does not duplicate-publish the agent — the underlying RPC is idempotent on the same `--api-name`. It just publishes a new BotVersion (which is normal voice-migration workflow anyway).
