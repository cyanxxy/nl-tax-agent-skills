---
description: Create a manual submission checklist for Dutch annual return or voorlopige aanslag workflows without logging in, signing, submitting, or handling DigiD.
argument-hint: "[annual|provisional] [2025|2026]"
disable-model-invocation: true
allowed-tools:
  - Read
  - Grep
  - Write
  - Edit
---

# NL Tax Submit Companion

Follow the bundled `nl-tax-submit-companion` workflow internally with arguments: `$ARGUMENTS`. Do not tell the user the skill name or command wrapper; start with the checklist result or the blocker that prevents it.
