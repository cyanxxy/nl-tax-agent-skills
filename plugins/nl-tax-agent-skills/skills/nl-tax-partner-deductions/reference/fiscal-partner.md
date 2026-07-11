# Rule note: Fiscal partner rules (fiscaal partnerschap)

source_ids: bd_fiscal_partnership, bd_fiscal_partner_death_return, bd_fiscal_partner_separation
workflow: all
tax_year: all
status: active
last_reviewed: "2026-05-10"
review_status: reviewed

## Contents

- Rule
- Fiscal partner status
- What fiscal partnership affects
- Special situations
- Verification checklist
- Notes

## Rule

Fiscal partnership determines whether taxpayers can file together and allocate certain income and deduction items. The official return is binding; this reference prepares review notes and allocation options.

These are reference notes for workpack preparation -- not final tax advice.

## Fiscal partner status

### Married couples and registered partners

- Married taxpayers and registered partners are fiscal partners from the moment of marriage or registration.
- If they already lived together at the same registered address earlier in that year, fiscal partnership starts from that earlier same-address registration date.
- If fiscal partnership exists for only part of the year, the taxpayers may choose in the income-tax return to be treated as fiscal partners for the whole year.

### Unmarried cohabitants

Unmarried cohabitants can be fiscal partners when they are registered at the same address and meet at least one official condition, such as:

- A notarial cohabitation contract.
- A child together, or recognition of the other person's child.
- Pension-partner registration.
- Joint ownership of the home they both live in.
- A qualifying samengestelde-gezin situation.
- Fiscal partnership in the previous year.
- A qualifying parent-child or stepchild situation under the official age rules.

If the condition is met during the calendar year, fiscal partnership starts from the moment both people were registered at the same address. If they were already registered together at that address in the previous year, they are fiscal partners for the whole following calendar year.

## What fiscal partnership affects

### Allocatable items

The following items can be allocated between fiscal partners, with every allocation totaling 100%:

- The saldo of own-home income and deductions.
- Aftrek wegens geen of geringe eigenwoningschuld.
- Income from substantial interest.
- The joint box 3 base.
- Paid partner alimony and other maintenance obligations.
- Specific healthcare costs.
- Gifts.
- Remaining personal deduction from previous years.

### Non-allocatable items

The following items are personal and cannot be allocated:

- Employment income, benefits, and pensions.
- Business profit.
- Public-transport travel deduction.
- Income from other activities.
- Income from made-available assets.
- Received alimony and other periodic payments.
- Income-provision deductions such as annuity premiums.
- Negative personal deductions.

## Special situations

### Partner died during the year

If a fiscal partner dies, the surviving partner can choose to be fiscal partner until the date of death or for the whole year of death. This is a choice, not an automatic full-year rule. It affects both returns and can affect allocation of common deductions.

Flag for human review. Filing for a deceased partner may require a nabestaandenmachtiging or paper forms depending on the chosen route.

### Divorce or separation

For married taxpayers or registered partners, fiscal partnership ends only when both official conditions are met:

1. A divorce, legal-separation, or registered-partnership dissolution request has been submitted.
2. The taxpayers are no longer registered at the same address.

For unmarried cohabitants, fiscal partnership ends when they are no longer registered at the same address.

In the year a relationship ends, taxpayers may choose whole-year fiscal partnership for that year. The workpack must ask for this choice instead of assuming it.

### Multiple possible partners

The taxpayer can have only one fiscal partner at a time. If multiple people could qualify, follow the official ordering rules and flag the case for review.

### Emigration or immigration

If either partner emigrated or immigrated during the year, additional rules apply. This project treats those cases as unsupported unless a dedicated reviewed source pack is added.

## Verification checklist

When determining fiscal partnership, verify:

1. Civil status: married, registered partnership, unmarried, separated, divorced, or widowed.
2. Registered address history during the tax year and prior year.
3. For unmarried cohabitants: which official condition is met and on what date.
4. Whether fiscal partnership is full-year automatically or part-year with an optional whole-year choice.
5. Whether death, separation, multiple-partner, emigration, or immigration facts require human review.
6. Whether both partners use the same allocation choices and the allocations total 100%.

For each allocation scenario, the agent records the reviewed partner conclusion
as a real boolean `has_fiscal_partner` and classifies every row with an explicit
real boolean `allocatable`. A row name never determines that classification.
Check that `taxpayer_pct` and `partner_pct` are finite numbers from 0 through
100 and total 100. A non-allocatable row must be 100/0 or 0/100, and
`partner_pct` must be 0 when `has_fiscal_partner` is false. Record
`check_performed_by: checked_by_agent` for this manual check or
`check_performed_by: checked_by_script` after the optional helper checks the
same explicit payload.

## Notes

- Do not assume all married taxpayers are full-year fiscal partners in the year of marriage; start date depends on the official same-address and marriage/registration facts.
- Do not assume death creates mandatory full-year fiscal partnership; it creates a choice.
- Do not select an optimal allocation automatically. Present source-backed options with impact notes and require taxpayer review.
