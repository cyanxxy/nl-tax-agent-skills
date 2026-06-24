---
description: Validate or plan official Dutch tax source snapshot refreshes. Developer-only.
argument-hint: "[annual|provisional|box3|all] [year]"
disable-model-invocation: true
allowed-tools:
  - Read
  - Grep
  - Write
  - Edit
  - Bash(python3 *.py:*)
---

# NL Tax Source Refresh

Follow the bundled `nl-tax-source-refresh` maintenance workflow internally with arguments: `$ARGUMENTS`. Do not tell the user the skill name or command wrapper; report only the maintenance result.
