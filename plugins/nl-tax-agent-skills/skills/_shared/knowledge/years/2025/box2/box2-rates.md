# Rule note: Box 2 rates 2025 and 2026

source_id: bd_box2_rates_2025_2026
workflow: annual_return, provisional_assessment
tax_years: 2025, 2026
status: active
last_reviewed: "2026-05-20"
review_status: reviewed

## Rule

Box 2 covers taxable income from a substantial interest (aanmerkelijk belang).
For manual workpacks, calculate the Box 2 tax only after separating regular
benefits and disposal benefits and after applying any partner allocation.

## Rates

For tax year 2025:

- 24.5% on Box 2 income up to and including EUR 67,804
- 31% on Box 2 income above EUR 67,804

For tax year 2026:

- 24.5% on Box 2 income up to and including EUR 68,843
- 31% on Box 2 income above EUR 68,843

## Fiscal partners

Box 2 income is taxed per return, and each partner's return has its own 24.5%
bracket up to the individual threshold (EUR 67,804 in 2025 / EUR 68,843 in 2026).
Across both returns the combined 24.5% bracket therefore covers twice the
individual threshold (EUR 135,608 in 2025 / EUR 137,686 in 2026), but only when
the Box 2 income is split across both partners' returns. Allocating 100% to one
partner does NOT double that return's 24.5% bracket -- the per-return threshold
still applies. Model the split when partners have substantial Box 2 income.

## Developer instruction

Use this shared official rate source for both the 2025 annual-return workpack
and the 2026 provisional-assessment workpack. Do not substitute Box 1 or Box 3
rates. Do not automate portal access, DigiD use, or filing submission; prepare
manual workpack calculations and evidence prompts only.
