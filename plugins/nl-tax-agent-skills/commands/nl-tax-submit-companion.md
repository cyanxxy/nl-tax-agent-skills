---
description: Create a manual submission checklist for Dutch annual return or voorlopige aanslag workflows without logging in, signing, submitting, or handling DigiD.
argument-hint: "[annual|provisional] [2025|2026]"
disable-model-invocation: true
allowed-tools: Read, Grep, Write, Edit
---

# NL Tax Submit Companion

Run the bundled `nl-tax-submit-companion` skill with these user arguments:

```text
$ARGUMENTS
```

If the host did not automatically load the skill, read and follow `${CLAUDE_PLUGIN_ROOT}/skills/nl-tax-submit-companion/SKILL.md` before acting. If `${CLAUDE_PLUGIN_ROOT}` is unavailable, locate this plugin's installed root containing `.claude-plugin/plugin.json` or `.codex-plugin/plugin.json`, then read `skills/nl-tax-submit-companion/SKILL.md` relative to that root.

This is manual-only guidance. Create `workspace/shared/manual-submission-checklist.md` from the existing workpack and field map. Do not log in, sign, submit, automate Mijn Belastingdienst, request DigiD credentials, store DigiD credentials, or process DigiD credentials.
