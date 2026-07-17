# Rule note: Own home for voorlopige aanslag 2026

source_ids: bd_eigenwoningforfait_2025_2026, bd_eigenwoningforfait_multiple_homes, bd_own_home_deduction_cap_2026, bd_woz_value_provisional_2026, bd_hypotheekrenteaftrek_conditions, bd_own_home_deductible_costs, bd_temporary_two_homes_interest
workflow: provisional_assessment
tax_year: 2026
status: active
last_reviewed: "2026-07-16"
review_status: reviewed

## Rule

For the 2026 voorlopige aanslag, own-home values are estimates for tax year 2026. The workpack can prepare source-backed estimates, but the official Mijn Belastingdienst form performs the binding calculation.

## Own-home calculation contract

- `total_deductible_own_home_costs = mortgage interest + qualifying financing costs + periodic erfpacht/opstal/beklemming`.
- Total deductible own-home costs include mortgage interest, qualifying financing costs, and periodic erfpacht, opstal, or beklemming.
- Hillen uses `total_deductible_own_home_costs`, not mortgage interest alone.
- `box1_own_home_balance = eigenwoningforfait - total_deductible_own_home_costs - hillen_deduction`.
- Tariefsaanpassing is separate from box1_own_home_balance: it is a tax-benefit adjustment and must never be added to taxable Box 1 income.
- Optional helper outputs are review inputs. The agent verifies them against the 2026 estimate evidence and preserves missing or uncertain facts as manual review.
- One ordinary main residence may receive a review estimate. Two homes, sale/purchase overlap, temporary double-home deductions, divorce use, and other complex cases must collect facts and route to manual review.

## Eigenwoningforfait 2026

Use the 2026 eigenwoningforfait table from `_shared/knowledge/own-home/eigenwoningforfait.md`.

| WOZ-waarde | Eigenwoningforfait |
|---|---:|
| Up to and including EUR 12,500 | 0% |
| More than EUR 12,500 up to and including EUR 25,000 | 0.10% |
| More than EUR 25,000 up to and including EUR 50,000 | 0.20% |
| More than EUR 50,000 up to and including EUR 75,000 | 0.25% |
| More than EUR 75,000 up to and including EUR 1,350,000 | 0.35% |
| More than EUR 1,350,000 | EUR 4,725 + 2.35% of the WOZ value above EUR 1,350,000 |

Use the own home's **WOZ value with peildatum 1 January 2025** for the 2026
provisional assessment. This is normally on the WOZ-beschikking issued by the
municipality in early 2026. If the taxpayer buys the home during 2026 and that
value is unavailable, collect a user-reviewed estimate based on comparable
homes at 1 January 2025 or a recent appraisal, label it as an estimate, and
leave complex cases for manual portal review. Do not substitute the Box 3
peildatum of 1 January 2026 for this own-home WOZ date.

## Aftrek wegens geen of geringe eigenwoningschuld

For 2026, 71.867% of the difference between the eigenwoningforfait and total deductible own-home costs is taken into account as the aftrek wegens geen of geringe eigenwoningschuld. Total costs include mortgage interest, qualifying financing costs, and periodic erfpacht, opstal, or beklemming.

The 2026 percentage reflects the accelerated Hillenregeling phase-out from 2026 onward: the annual reduction increased from 3.33 percentage points to 4.8 percentage points. Do not extrapolate from the older one-thirtieth schedule.

Flag the calculation for manual review if the taxpayer has no or low total deductible own-home costs.

## Tariefsaanpassing eigen woning 2026

If box 1 income before deductions is higher than EUR 78,426 in 2026, the tariefsaanpassing can reduce the benefit from deductible own-home costs.

- The 2026 tariefsaanpassing percentage is 11.94%.
- In the highest bracket, deductible own-home costs are effectively capped at 37.56%.
- The official form calculates the final correction; the workpack should flag likely applicability and show the source-backed parameters.
- Keep the correction in a separate review table; it does not change `box1_own_home_balance`.

## Mortgage interest estimates

Use current mortgage terms, expected 2026 payment schedules, and known interest-rate changes to estimate deductible mortgage interest. For post-2013 mortgages, flag manual confirmation that the loan is repaid at least linearly or annuitair within 30 years.

Also inventory expected qualifying financing costs and periodic erfpacht/opstal/beklemming payments before deriving `total_deductible_own_home_costs`.

## Workpack handling

- Mark all own-home amounts as estimates.
- Preserve each component needed to review `box1_own_home_balance`: WOZ value
  (peildatum 1 January 2025), eigenwoningforfait, mortgage interest,
  qualifying financing costs, periodic erfpacht/opstal/beklemming, the total
  deductible own-home costs, and any Hillen deduction. Do not reduce the
  workpack to a mortgage-interest-only amount.
- For two homes or any other complex own-home situation, collect the relevant dates, addresses, occupancy/use, listing/rental, mortgage, and divorce facts and route the calculation to manual review.
- Do not reuse 2025 eigenwoningforfait thresholds or Hillen percentages.
- If projected values are missing, record missing information rather than carrying forward a previous-year value without a taxpayer-provided estimate.
