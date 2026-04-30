# Rule note: Wet inkomstenbelasting 2001 -- structural reference

source_id: law_wet_inkomstenbelasting_2001
workflow: all
tax_year: all
status: active
last_reviewed: "2026-04-30"
review_status: reviewed

## Rule

The Wet inkomstenbelasting 2001 (Wet IB 2001) is the primary Dutch income tax law. All income tax calculations, deductions, and filing obligations in this project derive from this law.

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
- Applies when a taxpayer holds 5% or more of shares in a BV or NV
- **Out of scope for v1 of this project**

### Box 3 -- Belastbaar inkomen uit sparen en beleggen

- Savings and investments
- Taxed on a fictitious return (forfaitair rendement) based on asset composition
- Alternative: actual return method (werkelijk rendement) available from 2025

## Key structural provisions

### Fiscal partnership (Chapter 2, Section 2.17)

- Fiscal partners may allocate certain income and deduction items between them
- Allocation must be consistent within each box
- Partnership can arise from marriage, registered partnership, or cohabitation contract with joint home ownership

### Heffingsvrij vermogen (box 3)

- Each taxpayer has a tax-free capital allowance in box 3
- Fiscal partners each receive their own allowance
- Specific amounts are year-dependent -- see year-specific knowledge files

### Eigenwoningregeling (own-home rules)

- Mortgage interest on the own home is deductible in box 1
- Eigenwoningforfait (imputed rental value) is added as income in box 1
- Rules for qualifying own-home debt are in Chapter 3, Section 3.6

### Persoonsgebonden aftrek (personal deductions)

- Specific care costs (specifieke zorgkosten)
- Study costs (until recently; check year-specific rules)
- Gifts (giften)
- Maintenance payments to ex-partner (alimentatie)
- These deductions are allocated across boxes in a specific order

## Project scope

This project covers box 1 and box 3 only. Box 2 (substantial interest) is out of scope for v1.

## Developer instruction

When building any income tax calculation or workpack:

1. Identify which box each income or deduction item belongs to
2. Apply box-specific rules -- do not mix box 1 and box 3 rules
3. Check fiscal partnership status before allowing allocation of items
4. Use year-specific knowledge files for rates, thresholds, and amounts
5. This file provides structural orientation only -- never use it as the source for specific numbers

## Common failure

Do not apply box 3 percentages or heffingsvrij vermogen amounts from this file. This is a structural reference only. Specific rates and amounts come from year-specific knowledge files under `_shared/knowledge/years/`.
