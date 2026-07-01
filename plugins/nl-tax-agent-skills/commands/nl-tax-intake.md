---
description: First skill for any Dutch individual income-tax task — screens scope and routes to the right workflow. Use when the user wants to file the 2025 aangifte (annual return) or request, change, review, or stop a 2026 voorlopige aanslag, or mentions belastingaangifte, aangifte, or voorlopige aanslag.
argument-hint: "[annual|provisional|review|stopzetten]"
allowed-tools:
  - Read
  - Grep
  - Write
  - Edit
---

# NL Tax Intake

Follow the bundled `nl-tax-intake` workflow internally with arguments: `$ARGUMENTS`. Do not tell the user the skill name or command wrapper; start with the intake questions.
