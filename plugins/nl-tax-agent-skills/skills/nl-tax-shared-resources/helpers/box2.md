# Helper: Box 2 Substantial Interest (Aanmerkelijk Belang)

Internal read-only helper module for `nl-tax-annual-return` and
`nl-tax-provisional-assessment`. Returns sourced Box 2 findings, indicative
bracket calculations, manual-review markers, and open-question packets to the
owning workflow. Writes nothing.

## Boundaries

- **Only inside an owning workflow.** Apply only when `nl-tax-annual-return` or
  `nl-tax-provisional-assessment` is active. Never write files, workpacks,
  field maps, or checklists.
- **Human-only portal & no identifiers.** Follow
  `../nl-tax-shared-resources/runtime-contract.md`: never operate Mijn
  Belastingdienst or record BSN, IBAN, share-register numbers,
  policy/contract/aanslag numbers, or credentials.
- **Annual and provisional stay separate.** `annual_2025` uses actual 2025
  evidence; `provisional_2026` uses clearly labeled estimates or `B:` baseline
  amounts. Never carry an annual amount into provisional facts without taxpayer
  review as a 2026 estimate.

## Canonical knowledge sources (never paraphrase rates)

Load only the notes matching the active workflow (resolve relative to the active
owning skill directory):

- **Annual 2025:**
  - `../nl-tax-shared-resources/knowledge/years/2025/box2/box2-rates.md` (2025 Box 2 bracket threshold and rates)
  - `../nl-tax-shared-resources/knowledge/years/2025/box2/box2-income-guidance.md` (regular benefits, disposal benefits, costs, dividend withholding)
  - `../nl-tax-shared-resources/knowledge/years/2025/box2/fisin-aanmerkelijk-belang.md` (5% threshold, excessive borrowing)
- **Provisional 2026:**
  - `../nl-tax-shared-resources/knowledge/years/2026/provisional/box2.md` (2026 provisional Box 2 bracket threshold, rates, and estimate rules)
  - `../nl-tax-shared-resources/knowledge/years/2026/provisional/fisin-aanmerkelijk-belang.md` (2026 substantial-interest & excessive-borrowing guidance)

Return every consulted `source_id` to the owning workflow for `Sources used` /
Appendix A `sources_loaded`.

## Pre-calculation checklist (record `check_performed_by: checked_by_agent`)

Before any Box 2 calculation:

1. Require explicit `workflow` (`annual_2025` or `provisional_2026`) and
   matching integer `tax_year` (`2025` or `2026`); never infer one from the
   other.
2. Require `substantial_interest_pct` (generally >= 5% directly or indirectly
   with a fiscal partner, across shares, profit-sharing certificates /
   `winstbewijzen`, options, or similar rights in a company), actual booleans
   `resident_full_year: true` and `standard_ab_case: true`, and explicit
   source-backed values for `regular_benefits`, `disposal_benefit`, and
   `loss_setoff`.
3. Never treat an unrecognized or missing amount field as zero. Re-confirm any
   value not visible verbatim in the conversation or saved workpack.
4. **Provisional 2026 disposal gates:** include an estimated 2026 disposal
   benefit **only when the taxpayer expects a sale or transfer** of
   substantial-interest shares or rights during 2026, using an estimated net
   transfer price only for an expected arm's-length transaction. If the
   expected transfer price or baseline-derived acquisition price is uncertain,
   stop standard calculation and route to manual review.
5. Stop standard calculation and route to manual review if ANY complex marker
   below applies.
6. **Loss handling:** negative Box 2 income or loss setoff is manual-review
   data. If `loss_setoff > 0`, calculate only when the inputs record
   `loss_setoff_reviewed: true` AND a non-empty `loss_setoff_source` (e.g.,
   assessment loss statement); otherwise return a review question.
7. **Fiscal partner allocation:** calculate a split ONLY when the inputs record
   the actual boolean `full_year_fiscal_partner: true` and partner percentages
   total 100%. Show each partner's allocated income and indicative tax
   separately; never rank or select a split.
8. **Bracket arithmetic (show every line explicitly):**
   - `disposal_benefit = net_transfer_price - acquisition_price` (if starting
     from gross proceeds, subtract disposal costs ONCE to obtain
     `net_transfer_price`; never deduct disposal costs twice).
   - `box2_taxable = regular_benefits - deductible_direct_costs + disposal_benefit - confirmed_loss_setoff`.
   - Apply the canonical year lower-bracket rate up to the canonical year
     threshold, then the canonical upper-bracket rate above it (from
     `box2-rates.md` for 2025 or `provisional/box2.md` for 2026).
   - Credit same-year Dutch dividend withholding tax against gross Box 2 tax; if
     the credit exceeds gross tax, present as refund-facing review data.
   - Label all results as indicative (and as estimates/baseline-derived in
     provisional 2026).

## Complex or manual-review markers (stop standard calculation)

Route out of standard calculation when any fact involves:
- Unclear holding percentage, share/rights class, options, or partner ownership
  chain
- Valuation dispute, non-arm's-length transfer, or related-party pricing
  uncertainty
- Emigration, immigration, treaty, nonresident, or part-year residency (use the
  residency/international route, not Box 2)
- Death during the tax year
- Restructuring, merger, demerger, share-for-share exchange, conversion,
  informal capital, or corporate-tax-heavy DGA issues
- Inherited or gifted substantial interest, uncertain historic acquisition price,
  or fictive disposal event
- Mixed or unclear legal/advisory/financing costs
- **Excessive borrowing from own BV (`wet excessief lenen`):** check against the
  canonical threshold in `fisin-aanmerkelijk-belang.md`. Always flag borrowing
  above or near the threshold for manual review because prior-year threshold
  adjustments, repayments, and qualifying home-loan exceptions change the
  usable amount; never compute a fictitious regular benefit without a
  reviewer-supplied amount and source.

## Question packet format

Return missing inputs to the owning workflow as:

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
  prompt_for_user: "What was the official net transfer price for the Box 2 share disposal? If you only have gross proceeds, provide gross proceeds and disposal costs separately."
  acceptable_sources: ["file", "user_chat"]
  evidence_hint: "share-sale agreement or settlement statement"
```
