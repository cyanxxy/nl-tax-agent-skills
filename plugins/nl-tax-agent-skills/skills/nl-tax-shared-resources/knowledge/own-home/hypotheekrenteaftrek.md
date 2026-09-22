# Rule note: Hypotheekrenteaftrek and own-home deductible costs

source_ids: bd_hypotheekrenteaftrek_conditions, bd_hypotheek_oversluiten, bd_own_home_deductible_costs, bd_temporary_two_homes_interest
workflow: all
tax_year: all
status: active
last_reviewed: "2026-07-16"
review_status: reviewed

## Rule

Mortgage interest and certain own-home costs are deductible only when they relate to the eigenwoningschuld for the taxpayer's own home. The official filing environment performs the binding calculation; the workpack prepares source-backed notes and missing-info flags.

## Own-home calculation contract

- `total_deductible_own_home_costs = mortgage interest + qualifying financing costs + periodic erfpacht/opstal/beklemming`.
- Total deductible own-home costs include mortgage interest, qualifying financing costs, and periodic erfpacht, opstal, or beklemming.
- Hillen uses `total_deductible_own_home_costs`, not mortgage interest alone.
- `box1_own_home_balance = eigenwoningforfait - total_deductible_own_home_costs - hillen_deduction`.
- Tariefsaanpassing is separate from box1_own_home_balance: it is a tax-benefit adjustment and must not be added to taxable Box 1 income.
- Optional helper facts remain subject to agent verification. Missing evidence or uncertain qualification stays visible as manual review.
- One ordinary main residence may receive a review estimate. Two homes, sale/purchase overlap, temporary double-home deductions, divorce use, and other complex cases must collect facts and route to manual review.

## Mortgage interest conditions

For a mortgage or loan first taken out on or after 1 January 2013:

- The loan must be used to buy, improve, or maintain the own home, or to buy off the right of erfpacht.
- The loan must be repaid at least linearly or annuitair within 30 years.
- The maximum deduction period is 30 years from the date the mortgage or loan was taken out.

For an existing mortgage or loan increased on or after 1 January 2013:

- The 30-year period starts again for the increased part.
- The increased part must meet the post-2013 use and repayment conditions.
- The original loan keeps the conditions that already applied to it.

For a mortgage or loan taken out before 1 January 2013 and not later increased:

- The maximum deduction period is 30 years.
- If the loan already existed before 1 January 2001, the 30-year period starts on 1 January 2001.
- Existing conditions continue to apply.

Refinancing is not by itself a loss of the pre-2013 transitional treatment:

- If a pre-2013 own-home mortgage is refinanced for the **same outstanding
  amount**, the existing interest-deduction treatment continues, including for
  an interest-only mortgage. The original 30-year period does not restart.
- If the refinanced mortgage is increased, separate the preserved old balance
  from the increase. Interest on the increase qualifies only when that increase
  is used for the own home and is repaid within 30 years under the applicable
  post-2013 conditions; an interest-only increase does not qualify.
- Ask for the original start date, balance immediately before refinancing, new
  balance, use of any increase, and repayment terms. Do not use a generic
  "refinanced/changed" flag to disallow the preserved balance.

## Deductible and non-deductible costs

Deductible items can include:

- Mortgage interest on the eigenwoningschuld.
- One-off mortgage financing costs, such as mortgage-advice or intermediary fees, mortgage-deed notary costs, mortgage-deed cadastral fees, valuation costs for obtaining the loan, NHG application costs, and qualifying penalty interest.
- Periodic payments for erfpacht, opstal, or beklemming.

Do not deduct:

- Principal repayments.
- Maintenance and renovation costs.
- Purchase broker fees, transfer tax, VAT, purchase-deed notary costs, or purchase-deed cadastral fees.
- Costs of a bank guarantee for a deposit.
- Interest and costs on a loan that is not an eigenwoningschuld because of the bijleenregeling.

## Temporarily two homes

Two named exceptions can extend hypotheekrenteaftrek beyond the moment the taxpayer actually occupies a single home. The following conditions identify facts to collect; the workpack does not apply either exception automatically.

### Verkoopregeling (old home)

Mortgage interest on the **old** home stays deductible for the **year of moving plus the 3 subsequent calendar years**, provided all of the following hold for that period:

- The home is offered for sale ("staat te koop").
- The home is empty and is not rented out.
- The home was the taxpayer's hoofdverblijf in the year of moving or in one of the 3 preceding years.

After the year-of-moving + 3 years window expires, the home (and its mortgage) move to box 3.

### Aankoopregeling (new home)

Mortgage interest on the **new** home is deductible **before** the taxpayer occupies it, provided:

- The home is empty or under construction ("staat leeg of is in aanbouw").
- The taxpayer will start living there in the same year or within the **3 calendar years that follow**.

### Overbruggingshypotheek (bridge loan)

Interest on a bridge loan tied to the old-to-new transfer is deductible for the maximum term of the bridge loan. The bridge loan does not require mandatory repayment while waiting for the old home to be sold.

### Workpack handling for two-homes cases

When the taxpayer reports two homes during the tax year:

1. Collect which regime may apply to each home (verkoopregeling for the old, aankoopregeling for the new).
2. Collect move date, listing status, vacancy or rental status, expected move-in date, both mortgage statements, and any divorce-use arrangement. Record each fact with its `source` and `evidence_id` or `quote`.
3. Record possible deduction-window endpoints as review questions, not final filing conclusions.
4. Route every two-home, sale/purchase overlap, temporary double-home deduction, divorce-use, or other complex own-home outcome to manual review.

## Workpack handling

- Ask for the mortgage annual statement and, when relevant, the mortgage deed or amended loan agreement.
- Flag post-2013 mortgages for manual confirmation of linear or annuity repayment.
- For two-home situations, collect move date, old-home sale/listing status, vacancy/rental status, expected move-in date for the new home, and any divorce-use facts; route the result to manual review.
- Do not calculate a final filing value when qualification facts are missing; mark the item as missing or manual review.
