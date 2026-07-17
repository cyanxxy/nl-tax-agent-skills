---
name: nl-tax-box2
description: Use when an owning Dutch tax workflow needs standard Box 2 facts and questions; use reviewed 2025 amounts for annual workpacks and labeled 2026 estimates or baseline amounts for provisional workpacks.
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
`../_shared/`. Read `../_shared/runtime-contract.md` first. Resolve bundled
files relative to this skill directory with the host's skill-resource or file
tools. Do not depend on shell visibility or vendor-specific environment
variables.

- `reference/box2-annual-2025.md`
- `reference/box2-provisional-2026.md`

Python is optional. Do not ask the taxpayer to install Python and do not make
completion depend on it. The agent owns classification, questions, and the
workpack. If an already-resolved bundled script is available, the agent may run
`scripts/calculate_box2_tax.py input.json` as a mechanical cross-check after it
has built an explicit, source-backed payload. The script validates before it
calculates and records `check_performed_by: checked_by_script`.

Whether or not the script is run, apply this same checklist and record
`check_performed_by: checked_by_agent` for the manual path:

1. Require explicit `workflow` and matching integer `tax_year`; never infer one
   from the other.
2. Require `substantial_interest_pct`, actual booleans for
   `resident_full_year` and `standard_ab_case`, and explicit source-backed
   values for `regular_benefits`, `disposal_benefit`, and `loss_setoff`.
3. Reject unknown payload fields instead of treating a misspelled amount as
   zero. Other amount fields may be included only when collected from evidence.
4. Stop before calculation for a non-standard residence/AB case or any complex
   marker listed under **Never**.
5. When `loss_setoff` is greater than zero, calculate only after a reviewer has
   confirmed it and the payload records `loss_setoff_reviewed: true` plus a
   non-empty `loss_setoff_source`; otherwise return it as a review question.
6. For a partner allocation, require an actual
   `full_year_fiscal_partner: true` boolean and percentages totaling 100%.
7. Apply the year-pinned lower bracket before the upper bracket, then apply
   Dutch dividend withholding tax as a credit. Treat the result as indicative.

Only run Python under the already-resolved plugin
`skills/nl-tax-box2/scripts/calculate_box2_tax.py` path and only if Bash can
access it. If Bash cannot see that path, continue with the manual checklist;
never copy the script into `workspace/`. Never execute a `.py` located under
`workspace/`, `uploads/`, or `evidence/`.

## Do

- Prepare standard full-year Dutch resident Box 2 inputs for manual Mijn Belastingdienst entry.
- Identify substantial-interest facts, generally direct or indirect holdings of at least 5%, including the fiscal partner context.
- Distinguish regular benefits, such as dividends, from disposal benefits, such as share-sale gains.
- Calculate disposal benefit as the official net disposal or transfer price minus acquisition price. If only gross proceeds are available, subtract disposal costs once to derive the net transfer price first.
- Include Dutch dividend withholding tax as a same-year credit in the indicative calculation.
- For full-year fiscal partners, support allocation splits that total 100%. The
  calculator returns no result unless the payload sets the actual boolean
  `full_year_fiscal_partner: true`. Do not present a partner split until
  full-year partnership is confirmed.
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

Authenticated-portal boundary: Do not use a browser, Claude in Chrome,
computer use, or screen interaction for portal login/authentication, data
entry, clicking controls, signing, sending, or submitting. Those actions remain
human-only even with taxpayer permission or available credentials.
