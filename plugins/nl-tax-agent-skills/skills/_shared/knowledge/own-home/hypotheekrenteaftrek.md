# Rule note: Hypotheekrenteaftrek and own-home deductible costs

source_ids: bd_hypotheekrenteaftrek_conditions, bd_own_home_deductible_costs, bd_temporary_two_homes_interest
workflow: all
tax_year: all
status: active
last_reviewed: "2026-05-10"
review_status: reviewed

## Rule

Mortgage interest and certain own-home costs are deductible only when they relate to the eigenwoningschuld for the taxpayer's own home. The official filing environment performs the binding calculation; the workpack prepares source-backed notes and missing-info flags.

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

Two named exceptions extend hypotheekrenteaftrek beyond the moment the taxpayer actually occupies a single home. Apply the one that matches the facts; both can apply at once during a move.

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

1. Determine which regime applies to each home (verkoopregeling for the old, aankoopregeling for the new). Both can apply concurrently.
2. Confirm the conditions above against the user's facts (move date, listing status, vacancy, expected move-in date). Record each fact with its `source` and `evidence_id` or `quote`.
3. Compute the deduction window endpoints in absolute dates so the workpack can state plainly "interest on [address] is deductible through 31 December [year + 3]".
4. Only route to manual review when one of the conditions is genuinely ambiguous (e.g. partial-year letting, undocumented hoofdverblijf history, treaty/nonresident facts). A clean overlap of a few months that satisfies the conditions does NOT need manual review -- prepare it.

## Workpack handling

- Ask for the mortgage annual statement and, when relevant, the mortgage deed or amended loan agreement.
- Flag post-2013 mortgages for manual confirmation of linear or annuity repayment.
- For two-home situations, collect move date, old-home sale/listing status, vacancy/rental status, and expected move-in date for the new home.
- Do not calculate a final filing value when qualification facts are missing; mark the item as missing or manual review.
