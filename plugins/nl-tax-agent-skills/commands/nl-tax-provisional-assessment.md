---
description: Prepare a 2026 voorlopige aanslag workpack — request, change, review, or stopzetten — for manual Mijn Belastingdienst entry. Use after intake routes to a provisional_2026 flow. Fictitious box 3 only; never collects werkelijk rendement.
argument-hint: "[2026] [request|change|review|stopzetten|confirm]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - Bash(python3:*)
---

# NL Tax Provisional Assessment

Follow the bundled `nl-tax-provisional-assessment` workflow internally with arguments: `$ARGUMENTS`. Do not tell the user the skill name or command wrapper; start with the workflow's user-facing response.
