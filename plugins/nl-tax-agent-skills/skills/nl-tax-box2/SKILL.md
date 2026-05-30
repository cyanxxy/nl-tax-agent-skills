---
name: nl-tax-box2
description: Internal helper for nl-tax-annual-return and nl-tax-provisional-assessment — prepares Box 2 substantial-interest (aanmerkelijk belang) notes into workspace/shared/. Not a standalone workflow; invoked as a sub-step.
user-invocable: false
allowed-tools:
  - Read
  - Grep
  - Bash(python3 *.py:*)
---

# NL Tax Box 2

Background helper for Box 2 substantial-interest preparation notes.

Use this skill only for source-backed preparation support for:

- `annual_2025`: annual actual Box 2 inputs from taxpayer evidence.
- `provisional_2026`: estimated or baseline-derived Box 2 inputs for a provisional assessment.

Load the source notes before preparing outputs:

- `reference/box2-annual-2025.md`
- `reference/box2-provisional-2026.md`

Use the bundled scripts when structured JSON inputs are available:

- `scripts/validate_box2_inputs.py`
- `scripts/calculate_box2_tax.py`
- `scripts/summarize_box2_inputs.py`

## Do

- Prepare standard full-year Dutch resident Box 2 inputs for manual Mijn Belastingdienst entry.
- Identify substantial-interest facts, generally direct or indirect holdings of at least 5%, including the fiscal partner context.
- Distinguish regular benefits, such as dividends, from disposal benefits, such as share-sale gains.
- Calculate disposal benefit as the official net disposal or transfer price minus acquisition price. If only gross proceeds are available, subtract disposal costs once to derive the net transfer price first.
- Include Dutch dividend withholding tax as a same-year credit in the indicative calculation.
- For full-year fiscal partners, support allocation splits that total 100%.
- Flag losses, loss setoff, and excessive borrowing from an own BV for manual review.
- Label all `provisional_2026` amounts as estimates or baseline-derived.
- Keep outputs suitable for preparation workpacks and review questions.

## Never

- Do not log in, handle DigiD, automate a browser, sign, or submit anything.
- Do not claim that the helper gives binding tax advice or a final assessment.
- Do not use annual 2025 final-filing language for provisional 2026 estimates.
- Do not route complex substantial-interest cases as standard calculations.
- Do not handle valuation disputes, emigration, death, restructurings, treaty or nonresident issues, informal capital, non-arm's-length transfers, corporate-tax-heavy DGA cases, inherited or gifted substantial interests, fictive disposal events, or uncertain excessive-borrowing positions without manual review.
- Do not write field maps, annual/provisional workpack templates, source registers, supported workflow files, or shared eval data.

Write only Box 2 preparation notes or shared review questions under `workspace/shared/` when asked by an owning workflow. Do not write workpacks directly.

## Must NOT write to

This helper writes only under `workspace/shared/`. It must never write to:

- `workspace/annual/**`
- `workspace/provisional/**`

Only `nl-tax-annual-return` and `nl-tax-provisional-assessment` own those trees. On hosts that do not enforce `allowed-tools` (for example Codex, which reads only the SKILL.md body), treat this as a hard instruction, not just a tool restriction.
