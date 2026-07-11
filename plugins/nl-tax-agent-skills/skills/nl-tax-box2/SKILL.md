---
name: nl-tax-box2
description: Internal helper for nl-tax-annual-return and nl-tax-provisional-assessment — returns Box 2 facts and questions. Not a standalone workflow; invoked as a sub-step.
user-invocable: false
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(python3:*)
---

# NL Tax Box 2

Background helper for Box 2 substantial-interest preparation notes.

Use this skill only for source-backed preparation support for:

- `annual_2025`: annual actual Box 2 inputs from taxpayer evidence.
- `provisional_2026`: estimated or baseline-derived Box 2 inputs for a provisional assessment.

This helper may be called through a Skill/Task tool or inlined by an owning workflow when no such tool exists. The same output contract applies either way.

## Read first

Resolve every `workspace/...` path against `workspace_root` from
`session-progress.yaml` (or `profile.yaml`); never create a second
`workspace/` tree. `_shared/` is the plugin-shared folder at this skill's
`../_shared/`. Resolve bundled files with host file tools (`Read` first, `Glob`
or `Grep` if a path is not obvious). Do not use Bash to discover or read plugin
files: in Cowork, shell commands run in an isolated VM that may not see the
plugin cache even when `Read` and `Glob` can. If the host has already expanded
`${CLAUDE_PLUGIN_ROOT}` or `${CLAUDE_SKILL_DIR}`, those absolute paths are fine
for file tools; otherwise search within the loaded plugin/skill tree and resolve
relative to this skill directory.

- `reference/box2-annual-2025.md`
- `reference/box2-provisional-2026.md`

Run these bundled scripts when structured inputs are available. Each accepts either CLI flags or a JSON payload file (`calculate_box2_tax.py input.json`) with the keys documented in its docstring — `tax_year` (or `workflow`: `annual_2025` / `provisional_2026`), `regular_benefits`, `regular_costs`, `disposal_price` (or `gross_disposal_price` + `disposal_costs`), `acquisition_price`, `fictitious_regular_benefit_bv_loan`, `loss_setoff`, `dividend_withholding_tax`, and optional `partner_allocation` with `full_year_fiscal_partner: true`. Build the payload from values already collected in the box 2 notes; never invent inputs:

- `scripts/validate_box2_inputs.py`
- `scripts/calculate_box2_tax.py`
- `scripts/summarize_box2_inputs.py`

Only run Python under an already-resolved plugin `skills/.../scripts/` path (for this skill, the three scripts above), and only if Bash can access that path. If Bash cannot see the plugin path, continue manually from the sourced inputs and rules; never copy bundled scripts into `workspace/`. Never execute a `.py` located under `workspace/`, `uploads/`, or `evidence/`.

## Do

- Prepare standard full-year Dutch resident Box 2 inputs for manual Mijn Belastingdienst entry.
- Identify substantial-interest facts, generally direct or indirect holdings of at least 5%, including the fiscal partner context.
- Distinguish regular benefits, such as dividends, from disposal benefits, such as share-sale gains.
- Calculate disposal benefit as the official net disposal or transfer price minus acquisition price. If only gross proceeds are available, subtract disposal costs once to derive the net transfer price first.
- Include Dutch dividend withholding tax as a same-year credit in the indicative calculation.
- For full-year fiscal partners, support allocation splits that total 100%. The `calculate_box2_tax.py` calculator only computes a partner allocation when the payload sets `full_year_fiscal_partner: true`; otherwise it skips the allocation, records `partner_allocation_skipped`, and raises a `partner_status_unconfirmed` manual-review flag. Do not present a partner split until full-year partnership is confirmed.
- Flag losses, loss setoff, and excessive borrowing from an own BV for manual review.
- Label all `provisional_2026` amounts as estimates or baseline-derived.
- Keep outputs suitable for preparation workpacks and review questions.
- When facts are missing, return a structured question packet instead of inventing zeros.

## Question packet

Return missing inputs to the calling workflow in this shape:

```yaml
- question_id: "annual.box2.substantial_interest.status"
  workflow: "annual_2025"
  section: "box2.substantial_interest"
  prompt_for_user: "Did you or your fiscal partner hold a substantial interest (generally 5% or more) in a company in 2025?"
  acceptable_sources: ["file", "user_chat"]
  evidence_hint: "shareholder register, dividend statement, or sale agreement"
- question_id: "annual.box2.disposal.net_transfer_price"
  workflow: "annual_2025"
  section: "box2.disposal"
  prompt_for_user: "What was the official net transfer price for the Box 2 share disposal? If you only have gross proceeds, provide the gross amount and disposal costs separately."
  acceptable_sources: ["file", "user_chat"]
  evidence_hint: "share-sale agreement or settlement statement"
```

The calling skill asks these questions, records the answers with `source`, `quote`/`evidence_id`, and timestamp under its own annual or provisional notes tree, then re-runs this helper contract. Do not write caller-owned notes.

## Never

- Do not log in, automate a browser, sign, or submit anything.
- Do not claim that the helper gives binding tax advice or a final assessment.
- Do not use annual 2025 final-filing language for provisional 2026 estimates.
- Do not route complex substantial-interest cases as standard calculations.
- Do not handle valuation disputes, emigration, death, restructurings, treaty or nonresident issues, informal capital, non-arm's-length transfers, corporate-tax-heavy DGA cases, inherited or gifted substantial interests, fictive disposal events, or uncertain excessive-borrowing positions without manual review.
- Do not write field maps, annual/provisional workpack templates, source registers, supported workflow files, or shared eval data.

Return structured facts and open questions to the owning workflow. Do not
persist any final artifact, including shared notes, question packets, session
state, workpacks, or field maps. The annual/provisional workflow owns all
workspace persistence and may read historical helper notes for resume
compatibility only.
