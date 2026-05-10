# Rule note: Own home for voorlopige aanslag 2026

source_ids: bd_eigenwoningforfait_2025_2026, bd_own_home_deduction_cap_2026, bd_hypotheekrenteaftrek_conditions, bd_own_home_deductible_costs
workflow: provisional_assessment
tax_year: 2026
status: active
last_reviewed: "2026-05-10"
review_status: reviewed

## Rule

For the 2026 voorlopige aanslag, own-home values are estimates for tax year 2026. The workpack can prepare source-backed estimates, but the official Mijn Belastingdienst form performs the binding calculation.

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

If the current WOZ beschikking is not available when the provisional assessment is prepared, use the best available WOZ estimate and mark it as estimated.

## Aftrek wegens geen of geringe eigenwoningschuld

For 2026, 71.867% of the difference between the eigenwoningforfait and deductible own-home costs is taken into account as the aftrek wegens geen of geringe eigenwoningschuld.

Flag the calculation for manual review if the taxpayer has no mortgage interest or only low mortgage interest.

## Tariefsaanpassing eigen woning 2026

If box 1 income before deductions is higher than EUR 78,426 in 2026, the tariefsaanpassing can reduce the benefit from deductible own-home costs.

- The 2026 tariefsaanpassing percentage is 11.94%.
- In the highest bracket, deductible own-home costs are effectively capped at 37.56%.
- The official form calculates the final correction; the workpack should flag likely applicability and show the source-backed parameters.

## Mortgage interest estimates

Use current mortgage terms, expected 2026 payment schedules, and known interest-rate changes to estimate deductible mortgage interest. For post-2013 mortgages, flag manual confirmation that the loan is repaid at least linearly or annuitair within 30 years.

## Workpack handling

- Mark all own-home amounts as estimates.
- Do not reuse 2025 eigenwoningforfait thresholds or Hillen percentages.
- If projected values are missing, record missing information rather than carrying forward a previous-year value without a taxpayer-provided estimate.
