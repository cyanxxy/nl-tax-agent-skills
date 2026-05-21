---
description: Refresh official Dutch tax source snapshots and validate the local knowledge pack. Developer-only.
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

Use the bundled `nl-tax-source-refresh` skill, forwarding any arguments: `$ARGUMENTS`
