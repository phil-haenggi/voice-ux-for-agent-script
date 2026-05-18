---
id: E003
name: bundle-meta-filename
match:
  regex: "Cannot find bundle-meta\\.xml file"
severity: blocking
auto_fix: true
---

# Bundle meta filename

## Symptom

```
Compilation of the Agent Script file failed with the following errors:
- Cannot find bundle-meta.xml file for '<name>' at <path>/<name>.bundle-meta.xml
```

The validator can't find the metadata XML file. Often happens because the file was scaffolded with the metadata-API extension `.aiAuthoringBundle-meta.xml` but the validator expects `.bundle-meta.xml`.

## Root cause

The Agent Script CLI looks for the bundle metadata file with the `.bundle-meta.xml` suffix specifically. Other Salesforce CLI commands use `.aiAuthoringBundle-meta.xml` (the standard Metadata API extension for the type), causing confusion.

In practice, the Agent Script tooling expects `.bundle-meta.xml`; the standard metadata deploy expects `.aiAuthoringBundle-meta.xml`. Use the former for `sf agent` commands.

## Canonical fix

Rename the file:

```bash
cd force-app/main/default/aiAuthoringBundles/<name>/
mv <name>.aiAuthoringBundle-meta.xml <name>.bundle-meta.xml
```

Verify both files in the bundle directory:

```bash
ls force-app/main/default/aiAuthoringBundles/<name>/
# Expected:
# <name>.agent
# <name>.bundle-meta.xml
```

Re-run:

```bash
sf agent validate authoring-bundle --api-name <name> --target-org <org>
```

## Manual fallback

If the rename doesn't fix it, also verify:

1. The bundle directory name matches the `--api-name` (case-sensitive).
2. The `.agent` filename inside the bundle directory matches the `--api-name`.
3. The bundle-meta.xml has the right XML namespace and content. Minimum viable:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<AIAuthoringBundle xmlns="http://soap.sforce.com/2006/04/metadata">
    <masterLabel><human-readable label></masterLabel>
</AIAuthoringBundle>
```

If still failing, the issue may be a project-level `sfdx-project.json` misconfiguration (wrong `packageDirectories` entry).
