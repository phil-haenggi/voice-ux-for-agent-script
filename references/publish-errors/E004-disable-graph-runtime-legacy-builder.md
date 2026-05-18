---
id: E004
name: disable-graph-runtime-legacy-builder
match:
  keyword: "disable_graph_runtime"
  context: "agent opens in legacy Bot Builder"
severity: warning
auto_fix: true
---

# Disable graph runtime → legacy builder

## Symptom

The agent publishes successfully, but when opened in the org it appears in the **legacy Bot Builder** UI rather than the modern Agentforce Builder. The agent is functional but lacks modern-runtime features (graph-based planner, modern preview/test tooling, modern session telemetry).

This is not a publish *failure* — the publish completes. It's a misconfiguration where the agent ends up on the wrong runtime.

## Root cause

The `.agent` config block contains:

```yaml
config:
    additional_parameter__disable_graph_runtime: True
```

This flag opts the agent into the legacy non-graph runtime. The legacy Bot Builder UI is what's available for legacy-runtime agents. The new Agentforce Builder requires the graph runtime.

The flag is sometimes inherited from source scripts that were authored against the legacy runtime (deliberate or accidental). When migrating to a modern voice deployment, the flag should usually be dropped.

## Canonical fix

Remove the flag entirely (default = graph runtime enabled):

```diff
 config:
     developer_name: "..."
     agent_label: "..."
     agent_type: "AgentforceServiceAgent"
     enable_enhanced_event_logs: True
-    additional_parameter__disable_graph_runtime: True
```

Or set explicitly to `False`:

```yaml
    additional_parameter__disable_graph_runtime: False
```

(Removing is cleaner — defaults to the right thing.)

Re-publish. The new BotVersion lands on the same agent record; the agent now opens in the modern Builder.

## When to keep the flag

Keep `disable_graph_runtime: True` only when:
- Source agent's planner behavior was tuned to the legacy runtime AND switching changes downstream tool-call sequences in ways that haven't been validated.
- The customer org doesn't yet support graph runtime (rare; verify with platform team).

For voice migration specifically, the modern runtime is almost always preferred — graph planner is more reliable for multi-tool flows like booking.

## Manual fallback

If after removing the flag the agent still opens in legacy Bot Builder:
1. Verify the BotVersion picked up the change (`sf data query --query "SELECT IsActive, VersionNumber FROM BotVersion WHERE BotDefinition.DeveloperName = '<name>' ORDER BY VersionNumber DESC" --target-org <org> --use-tooling-api`).
2. Try publishing a fresh new BotVersion.
3. Check org permissions for the user opening the agent — modern Builder may require a permission set the user doesn't have.
