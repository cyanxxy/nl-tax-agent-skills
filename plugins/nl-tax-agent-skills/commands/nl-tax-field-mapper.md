---
description: Convert an annual or provisional workpack into a manual-entry field map for the Mijn Belastingdienst portal, tracing every value to its source. Use after a workpack exists and the user wants to prepare data entry.
argument-hint: "[annual|provisional] [year]"
allowed-tools:
  - Read
  - Grep
  - Write
  - Edit
  - Bash(python3:*)
---

# NL Tax Field Mapper

Follow the bundled `nl-tax-field-mapper` workflow internally with arguments: `$ARGUMENTS`. Do not tell the user the skill name or command wrapper; report only the field-map result or the blocker that prevents it.
