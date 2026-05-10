---
description: Determine the correct Dutch tax workflow and create a taxpayer profile for annual return 2025 or voorlopige aanslag 2026.
argument-hint: "[annual|provisional|review|stopzetten]"
allowed-tools: Read, Grep, Write, Edit
---

# NL Tax Intake

Run the bundled `nl-tax-intake` skill with these user arguments:

```text
$ARGUMENTS
```

If the host did not automatically load the skill, read and follow `${CLAUDE_PLUGIN_ROOT}/skills/nl-tax-intake/SKILL.md` before acting. If `${CLAUDE_PLUGIN_ROOT}` is unavailable, locate this plugin's installed root containing `.claude-plugin/plugin.json` or `.codex-plugin/plugin.json`, then read `skills/nl-tax-intake/SKILL.md` relative to that root.

Use the plugin's supported-workflow gate and local source pack. Create or update `workspace/taxpayer/profile.yaml` and `workspace/shared/missing-info.md` as described by the skill. Do not prepare unsupported future-year workpacks from old rates or thresholds.
