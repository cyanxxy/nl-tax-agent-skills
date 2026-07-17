# Rule note: Wet inkomstenbelasting 2001 -- structural reference

source_id: law_wet_inkomstenbelasting_2001
workflow: all
tax_year: all
status: active
last_reviewed: "2026-07-16"
review_status: reviewed

## Rule

The Wet inkomstenbelasting 2001 (Wet IB 2001) is the primary Dutch income-tax
statute. This file is orientation only: a filing position can also depend on the
applicable regulations, decrees, transitional law, case law, and year-specific
official guidance. Do not infer a complete eligibility rule from this summary.

## Three-box system

Dutch income tax is divided into three boxes, each with its own tax base and rate structure:

### Box 1 -- Belastbaar inkomen uit werk en woning

- Employment income (loon)
- Business profits (winst uit onderneming)
- Income from other activities (resultaat uit overige werkzaamheden)
- Periodic payments (periodieke uitkeringen)
- Own-home income (eigenwoningforfait minus mortgage interest)
- Personal deductions (persoonsgebonden aftrek)

### Box 2 -- Belastbaar inkomen uit aanmerkelijk belang

- Income from substantial interest in a company (dividend, capital gains)
- A 5% direct or indirect interest can trigger Box 2, but the statutory tests
  also distinguish classes of shares and cover certain options, profit-sharing
  certificates, cooperative membership rights, family attribution, and related
  positions. Use the reviewed Box 2 sources and keep non-standard facts for
  manual review rather than treating this bullet as the legal test.
- Standard full-year resident preparation is supported for active annual 2025 and provisional 2026 workflows; complex Box 2 facts stay manual review or unsupported.

### Box 3 -- Belastbaar inkomen uit sparen en beleggen

- Savings and investments
- The filing starts from the statutory/fictitious calculation based on asset
  composition. For 2025, the portal can also collect actual-return data and,
  when supplied, compares both calculations and uses the more favorable amount.

## Key structural provisions

### Fiscal partnership (Chapter 2, Section 2.17)

- Fiscal partners may allocate certain income and deduction items between them
- Allocation must be consistent within each box
- Partnership can arise from marriage, registered partnership, or several
  official cohabitation conditions. A cohabitation contract and joint home
  ownership are separate possible conditions, not one combined exhaustive test;
  use the dedicated fiscal-partnership note.

### Heffingsvrij vermogen (box 3)

- Each taxpayer has a tax-free capital allowance in box 3
- Fiscal partners each receive their own allowance
- Specific amounts are year-dependent -- see year-specific knowledge files

### Eigenwoningregeling (own-home rules)

- Interest is deductible only to the extent it relates to a qualifying
  eigenwoningschuld and the applicable use, repayment, and time conditions are met.
- Article 3.112 Wet IB 2001 defines the eigenwoningforfait and its WOZ-value
  table; the imputed rental value is added as income in box 1
- Rules for qualifying own-home debt are in Chapter 3, Section 3.6

### Persoonsgebonden aftrek (personal deductions)

- Specific care costs (specifieke zorgkosten)
- A narrow transitional prestatiebeurs exception may apply; ordinary study
  costs are not a general 2025 deduction. Use the year-specific note.
- Gifts (giften)
- Maintenance payments to ex-partner (alimentatie)
- These deductions are allocated across boxes in a specific order

## Project scope

This project covers Box 1, standard Box 2 preparation for active annual/provisional workflows, and Box 3. Complex Box 2 situations remain outside standard support until exact official-source-backed handling is added.

## Developer instruction

When building any income tax calculation or workpack:

1. Identify which box each income or deduction item belongs to
2. Apply box-specific rules -- do not mix Box 1, Box 2, and Box 3 rules
3. Check fiscal partnership status before allowing allocation of items
4. Use year-specific knowledge files for rates, thresholds, and amounts
5. This file provides structural orientation only -- never use it as the source for specific numbers

## Common failure

Do not apply box 3 percentages or heffingsvrij vermogen amounts from this file. This is a structural reference only. Specific rates and amounts come from year-specific knowledge files under `_shared/knowledge/years/`.
