---
description: Developer-only maintenance — validate Dutch tax source registers and supported-workflow gates, rebuild reviewed snapshot metadata, and plan official-source refreshes. Not a taxpayer workflow; never reads or writes workspace/uploads/evidence.
argument-hint: "[annual|provisional|box3|all] [year]"
disable-model-invocation: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - Bash(python3:*)
---

# NL Tax Source Refresh

This is developer-only maintenance, not a taxpayer workflow. Run it only when a developer explicitly asks to validate or plan source refresh work; it must not read or write taxpayer workspace data.

Follow the bundled `nl-tax-source-refresh` maintenance workflow internally with arguments: `$ARGUMENTS`. Do not tell the user the skill name or command wrapper; report only the maintenance result.
