# Publish error catalog

Known `sf agent publish authoring-bundle` errors and their fixes. Used by Phase 8 (publish-with-self-healing, optional).

## How the catalog is used

When `sf agent publish authoring-bundle` fails, the skill captures stderr and matches it against each entry's `match` regex/keyword. On match:
1. Surface the canonical fix to the developer with a one-line diff preview.
2. Apply the fix (or ask first, depending on severity).
3. Re-run publish.
4. If new error, re-match.

Bounded by `MAX_PUBLISH_ITERATIONS` (default 15). On exhaustion, surface remaining errors plus all attempted fixes for manual resolution.

## Error file format

```yaml
---
id: E001
name: locale-restricted-picklist
match:
  regex: "Agent Primary Language.*restricted picklist"
severity: blocking      # blocking | warning | informational
auto_fix: true          # whether the skill should apply without asking
---

# <error name>

## Symptom
<verbatim error string and where it appears>

## Root cause
<why this happens>

## Canonical fix
<concrete edit, with file path and old/new strings>

## Manual fallback
<if auto_fix fails, what the developer should check>
```

## Catalog (current)

| ID | Symptom | Auto-fix |
|---|---|---|
| E001 | `Agent Primary Language: bad value for restricted picklist field: en_GB` | yes |
| E002 | `Invocation Target: bad value for restricted picklist field: <ApexName>` | no — needs Apex/Flow deployment |
| E003 | `Cannot find bundle-meta.xml file for '<name>'` | yes |
| E004 | Agent opens in legacy Bot Builder instead of new Agentforce Builder | yes |
| E005 | `Cannot set properties of undefined (setting 'target')` (post-publish retrieve) | yes — re-run with `--skip-retrieve` |

## Adding entries

When you hit a publish error not in this list:
1. Capture the verbatim stderr string.
2. Identify the root cause (don't guess — verify with platform docs or by reproducing).
3. Write the canonical fix with the actual file path and edit.
4. Add an entry. Run a test deploy after the fix to confirm.
5. PR.

## What's NOT in scope

- **Schema/syntax errors in `.agent` files.** Those are caught by `sf agent validate authoring-bundle` before publish. Validation errors are handled in Phase 4 (audit), not Phase 8.
- **Org-level configuration (Connected Apps, OAuth, permissions).** These are pre-requisites; the skill doesn't auto-fix org config.
- **Network errors / transient platform errors.** Re-run publish; not a catalog issue.
