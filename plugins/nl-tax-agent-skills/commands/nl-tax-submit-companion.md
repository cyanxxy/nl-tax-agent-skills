---
description: Build a manual Mijn Belastingdienst submission checklist from an existing workpack and field map — blockers first, then step-by-step entry. Use only when the user explicitly asks for a submission checklist (manual-only skill; never auto-invoked).
argument-hint: "[annual|provisional] [2025|2026]"
disable-model-invocation: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
---

# NL Tax Submit Companion

This is a manual-only checklist command. Run it only after the user explicitly asks for a submission checklist; do not log in, sign, submit, automate the portal, or handle credentials.

Follow the bundled `nl-tax-submit-companion` workflow internally with arguments: `$ARGUMENTS`. Do not tell the user the skill name or command wrapper; start with the checklist result or the blocker that prevents it.
