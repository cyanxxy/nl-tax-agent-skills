---
description: Refresh official Dutch tax source snapshots and validate the local knowledge pack. Developer-only.
argument-hint: "[annual|provisional|box3|all] [year]"
disable-model-invocation: true
allowed-tools: Read Grep Write Edit Bash(python ${CLAUDE_PLUGIN_ROOT}/skills/nl-tax-source-refresh/scripts/*.py *)
---

# NL Tax Source Refresh

Run the bundled `nl-tax-source-refresh` skill with these user arguments:

```text
$ARGUMENTS
```

If the host did not automatically load the skill, read and follow `${CLAUDE_PLUGIN_ROOT}/skills/nl-tax-source-refresh/SKILL.md` before acting. If `${CLAUDE_PLUGIN_ROOT}` is unavailable, locate this plugin's installed root containing `.claude-plugin/plugin.json` or `.codex-plugin/plugin.json`, then read `skills/nl-tax-source-refresh/SKILL.md` relative to that root.

This is developer-only source maintenance. Use the official-domain allowlist and source register, refresh or validate snapshots as requested, and keep unsupported future workflows blocked until exact official sources are registered and validators pass.
