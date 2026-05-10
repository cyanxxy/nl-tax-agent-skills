---
description: Prepare a Dutch annual income-tax return 2025 workpack from taxpayer profile, evidence index, and local annual tax knowledge.
argument-hint: "[2025]"
allowed-tools: Read Grep Write Edit Bash(python ${CLAUDE_PLUGIN_ROOT}/skills/nl-tax-annual-return/scripts/*.py *)
---

# NL Tax Annual Return

Run the bundled `nl-tax-annual-return` skill with these user arguments:

```text
$ARGUMENTS
```

If the host did not automatically load the skill, read and follow `${CLAUDE_PLUGIN_ROOT}/skills/nl-tax-annual-return/SKILL.md` before acting. If `${CLAUDE_PLUGIN_ROOT}` is unavailable, locate this plugin's installed root containing `.claude-plugin/plugin.json` or `.codex-plugin/plugin.json`, then read `skills/nl-tax-annual-return/SKILL.md` relative to that root.

Prepare only the supported 2025 annual-return workpack. Read the taxpayer profile, evidence index, and local 2025 source-backed knowledge. Write the annual workpack and related field-map outputs described by the skill. Do not file, sign, submit, log in, or handle DigiD credentials.
