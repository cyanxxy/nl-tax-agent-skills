---
description: Convert Dutch annual return or voorlopige aanslag workpack findings into a manual-entry field map.
argument-hint: "[annual|provisional] [year]"
allowed-tools: Read Grep Write Edit Bash(python ${CLAUDE_PLUGIN_ROOT}/skills/nl-tax-field-mapper/scripts/*.py *)
---

# NL Tax Field Mapper

Run the bundled `nl-tax-field-mapper` skill with these user arguments:

```text
$ARGUMENTS
```

If the host did not automatically load the skill, read and follow `${CLAUDE_PLUGIN_ROOT}/skills/nl-tax-field-mapper/SKILL.md` before acting. If `${CLAUDE_PLUGIN_ROOT}` is unavailable, locate this plugin's installed root containing `.claude-plugin/plugin.json` or `.codex-plugin/plugin.json`, then read `skills/nl-tax-field-mapper/SKILL.md` relative to that root.

Convert an existing supported annual or provisional workpack into the manual-entry field map described by the skill. Use the bundled field references and mapping principles. Flag missing or low-confidence fields instead of inventing values.
