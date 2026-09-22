# Rule note: Eigenwoningforfait 2025 and 2026

source_ids: bd_eigenwoningforfait_2025_2026, bd_eigenwoningforfait_multiple_homes, bd_woz_value_provisional_2026
workflow: all
tax_year: all
status: active
last_reviewed: "2026-07-16"
review_status: reviewed

## Rule

The eigenwoningforfait is the deemed owner-occupied-home income added to box 1 for a home that is the taxpayer's main residence. The Belastingdienst calculates it automatically in the official form; workpacks may include a source-backed estimate for review.

## Own-home balance contract

- `total_deductible_own_home_costs = mortgage interest + qualifying financing costs + periodic erfpacht/opstal/beklemming`.
- Total deductible own-home costs include mortgage interest, qualifying financing costs, and periodic erfpacht, opstal, or beklemming.
- Hillen compares eigenwoningforfait with `total_deductible_own_home_costs`, not mortgage interest alone.
- `box1_own_home_balance = eigenwoningforfait - total_deductible_own_home_costs - hillen_deduction`.
- Tariefsaanpassing is separate from box1_own_home_balance: it is a tax-benefit adjustment and is not taxable Box 1 income.
- The agent may use optional helper values as review inputs after verifying the cited evidence. Missing or uncertain qualification facts remain manual review.
- One ordinary main residence may receive a review estimate. Two homes, sale/purchase overlap, temporary double-home deductions, divorce use, and other complex cases must collect facts and route to manual review.

## 2025 table

| WOZ-waarde | Eigenwoningforfait |
|---|---:|
| Up to and including EUR 12,500 | 0% |
| More than EUR 12,500 up to and including EUR 25,000 | 0.10% |
| More than EUR 25,000 up to and including EUR 50,000 | 0.20% |
| More than EUR 50,000 up to and including EUR 75,000 | 0.25% |
| More than EUR 75,000 up to and including EUR 1,330,000 | 0.35% |
| More than EUR 1,330,000 | EUR 4,655 + 2.35% of the WOZ value above EUR 1,330,000 |

For 2025, the aftrek wegens geen of geringe eigenwoningschuld applies to 76.667% of the difference between eigenwoningforfait and deductible own-home costs.

## 2026 table

| WOZ-waarde | Eigenwoningforfait |
|---|---:|
| Up to and including EUR 12,500 | 0% |
| More than EUR 12,500 up to and including EUR 25,000 | 0.10% |
| More than EUR 25,000 up to and including EUR 50,000 | 0.20% |
| More than EUR 50,000 up to and including EUR 75,000 | 0.25% |
| More than EUR 75,000 up to and including EUR 1,350,000 | 0.35% |
| More than EUR 1,350,000 | EUR 4,725 + 2.35% of the WOZ value above EUR 1,350,000 |

For 2026, the aftrek wegens geen of geringe eigenwoningschuld applies to 71.867% of the difference between eigenwoningforfait and deductible own-home costs.

## Application notes

- The 2025 annual return uses the WOZ value with valuation date 1 January 2024.
- The 2026 provisional assessment uses the WOZ value for tax year 2026 with
  valuation date 1 January 2025. If that WOZ beschikking is not yet available,
  use the latest known value only as a labelled estimate and create a review
  item to replace it.
- For a moving year, calculate eigenwoningforfait for the period the taxpayer was registered at the home as their main residence.
- For a former home that is empty and for sale, or a new bought home that is empty or under construction before occupancy, the eigenwoningforfait can be EUR 0 for that period under the official moving-home rules.
- Those moving-home rules are fact-collection prompts in the workpack: any two-home, overlap, temporary double-home, or divorce-use case routes to manual review for the actual period and qualification outcome.
- Do not carry thresholds, fixed amounts, or Hillen percentages from one year to another.
- If the official form computes a different amount, the official form is binding and the workpack should record the difference as a review item.
