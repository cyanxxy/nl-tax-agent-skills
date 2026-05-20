---
description: Prepare a Dutch voorlopige aanslag 2026 request, change, review, or stopzetten guidance package.
argument-hint: "[2026] [request|change|review|stopzetten]"
allowed-tools:
  - Read
  - Grep
  - Write
  - Edit
  - Bash(python3 *.py:*)
---

# NL Tax Provisional Assessment

Run the bundled `nl-tax-provisional-assessment` skill with these user arguments:

```text
$ARGUMENTS
```

If the host did not automatically load the skill, read and follow `${CLAUDE_PLUGIN_ROOT}/skills/nl-tax-provisional-assessment/SKILL.md` before acting. If `${CLAUDE_PLUGIN_ROOT}` is unavailable, locate this plugin's installed root containing `.claude-plugin/plugin.json` or `.codex-plugin/plugin.json`, then read `skills/nl-tax-provisional-assessment/SKILL.md` relative to that root.

Prepare only supported 2026 voorlopige-aanslag request, change, review, or stopzetten outputs. Keep provisional 2026 logic separate from annual-return logic, use estimates where required, and include only this explanatory note for Box 3 actual return questions: "Werkelijk rendement is not part of provisional 2026."
