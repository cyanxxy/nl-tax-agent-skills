# Rule note: Fiscal partnership

source_ids: bd_fiscal_partnership, bd_fiscal_partner_death_return, bd_fiscal_partner_separation
workflow: all
tax_year: all
status: active
last_reviewed: "2026-05-10"
review_status: reviewed

## Rule

Fiscal partnership determines whether taxpayers can file together and allocate certain income and deduction items. The official filing environment is binding; the workpack records source-backed status, choices, and review flags.

## Who is a fiscal partner

Married taxpayers and registered partners are fiscal partners from the moment of marriage or registered partnership. If they already lived together at the same address earlier in the same year, fiscal partnership starts from the moment they were registered together at that address.

Unmarried cohabitants can be fiscal partners when they are registered at the same address and meet at least one official condition, including a notarial cohabitation contract, a child together, recognition of the other person's child, pension-partner status, joint ownership of the home they both live in, a qualifying samengestelde-gezin situation, prior-year fiscal partnership, or qualifying parent-child or stepchild situations.

If the condition is met during the calendar year, fiscal partnership starts from the moment both people were registered at the same address. If they were already registered together at that address in the previous year, they are fiscal partners for the whole following calendar year.

## Whole-year choice

If taxpayers have a fiscal partner for only part of the year, they may choose in the income-tax return to be treated as fiscal partners for the whole year. If there are multiple fiscal partners after each other in the same year, the taxpayer can choose whole-year treatment with one of them.

## Allocatable items

Fiscal partners may allocate items such as:

- The own-home income and deduction balance.
- Aftrek wegens geen of geringe eigenwoningschuld.
- Income from substantial interest.
- The joint box 3 base.
- Paid partner alimony and other maintenance obligations.
- Specific healthcare costs.
- Gifts.
- Remaining personal deduction from previous years.

Every allocation must total 100% across both partners.

## Non-allocatable items

Do not allocate personal items such as:

- Wages, benefits, or pensions.
- Business profit.
- Public-transport travel deduction.
- Income from other activities.
- Income from made-available assets.
- Received alimony and other periodic payments.
- Income-provision deductions such as annuity premiums.
- Negative personal deductions.

## Separation

For married taxpayers or registered partners, fiscal partnership ends only when both official conditions are met: a divorce, legal-separation, or registered-partnership dissolution request has been submitted, and the taxpayers are no longer registered at the same address.

For unmarried cohabitants, fiscal partnership ends when they are no longer registered at the same address.

In the year a relationship ends, taxpayers may choose whole-year fiscal partnership for that year. The workpack must flag this as a taxpayer choice rather than assuming it automatically applies.

## Death of a partner

When a fiscal partner dies, the surviving partner can choose to be fiscal partner until the date of death or for the whole year of death. This choice affects both returns and can affect whether common deductions can still be allocated.

## Workpack handling

- Confirm civil status, registered address history, and which official condition applies.
- If fiscal partnership is only part-year, ask whether the taxpayer intends to choose whole-year treatment.
- For death, divorce, emigration, immigration, or multiple partner situations, flag the case for human review.
- Do not infer an optimal allocation automatically; present source-backed allocation options and require taxpayer review.
