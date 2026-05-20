---
name: nl-tax-provisional-assessment
description: Use when preparing a 2026 voorlopige aanslag manual-entry guide.
allowed-tools:
  - Read
  - Grep
  - Write
  - Edit
  - Bash(python3 *.py:*)
---

# NL Tax Provisional Assessment

Prepare local guidance for manually handling a 2026 voorlopige aanslag flow.

Load as needed: supported workflows, DigiD/prompt-injection security notes, 2026 provisional knowledge, provisional references, `templates/provisional-pack.md`, and profile.

## Do

1. Confirm an active `provisional_2026_*` workflow.
2. Use only 2026 provisional sources and label amounts as estimates.
3. Include standard Box 2 estimate preparation when applicable, with every Box 2 amount labeled as estimate or from-baseline.
4. Route complex Box 2 facts to manual review or unsupported: valuation disputes, emigration, death, restructurings, treaty/nonresident issues, informal capital, non-arm's-length transfers, and corporate-tax-heavy DGA cases.
5. For change/review, compare baseline and current estimates; remind the user to enter all data again.
6. For stopzetten, separate refund cases from payment-correction cases.
7. Write the relevant files under `workspace/provisional/2026/`.

## Never

- Do not request, calculate, or offer method choices for werkelijk rendement in provisional 2026.
- Do not write `workspace/annual/**`.
- Do not log in, submit, sign, automate forms, or handle DigiD.
