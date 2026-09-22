# Rule note: Rates and credits for voorlopige aanslag 2026

source_ids: bd_provisional_rates_2026, bd_box1_rates_2026, bd_fisin_2026_belastingberekening, bd_heffingskortingen_aow_2025_2026
workflow: provisional_assessment
tax_year: 2026
status: active
last_reviewed: "2026-07-16"
review_status: reviewed

## Rule

The voorlopige aanslag 2026 is calculated using the tax rates and credits published by the Belastingdienst for provisional-assessment calculations.

## Box 1 rates 2026 (provisional)

Box 1 income (income from employment and home ownership) is taxed in progressive brackets.

Before selecting a table, use the reviewed profile state rather than a yes/no
AOW flag:

- `below_all_year`: the taxpayer remains below AOW age throughout 2026.
- `reaches_during_year`: record the AOW transition month. The first-bracket
  rate is in the published month table below; do not use either whole-year
  table. Do not interpolate an affected credit: use the official online
  `Verzoek of wijziging voorlopige aanslag 2026` credit result and mark it for
  manual portal review.
- `aow_all_year`: the taxpayer has AOW age for all of 2026.

### Taxpayers below AOW age throughout 2026 (`below_all_year`)

| Schijf | Taxable income | Rate |
|---|---|---|
| 1 | Up to and including EUR 38,883 | 35.75% |
| 2 | More than EUR 38,883 up to and including EUR 78,426 | 37.56% |
| 3 | More than EUR 78,426 | 49.50% |

### Taxpayers who reach AOW age during 2026 (`reaches_during_year`)

Use the row for the month in which the taxpayer reaches AOW age. These
published percentages apply to the first bracket up to and including
EUR 38,883; brackets 2 and 3 remain 37.56% and 49.50%.

| AOW age reached in | First-bracket rate |
|---|---:|
| January | 17.85% |
| February | 19.34% |
| March | 20.83% |
| April | 22.32% |
| May | 23.81% |
| June | 25.30% |
| July | 26.80% |
| August | 28.29% |
| September | 29.78% |
| October | 31.27% |
| November | 32.76% |
| December | 34.25% |

**Two official pages disagree on six of these rows.** The Belastingdienst
belastingberekening page (`bd_fisin_2026_belastingberekening`) prints the series
above. The general box 1 tarieven page (`bd_box1_rates_2026`) prints April,
May, June, October, November and December each **0.01 percentage point higher**
(22.33, 23.82, 25.31, 31.28, 32.77, 34.26). The series above is used because it
is the one the belastingberekening reference gives and because it keeps the
convention both official 2025 pages use: for 2025 the box 1 tarieven page and
the belastingberekening page agree with each other, and both cut the third
decimal rather than rounding it up. Only the 2026 box 1 page departs from that.

The gap is at most 0.01 percentage point over the first bracket, so it changes a
voorlopige-aanslag estimate by a few euro at most. Do not present either series
as exact to the cent, and do not restate this as a taxpayer-facing choice: the
official filing environment applies its own percentage and remains binding.

### Taxpayers at AOW age throughout 2026, born on or after 1 January 1946

| Schijf | Taxable income | Rate |
|---|---|---|
| 1 | Up to and including EUR 38,883 | 17.85% |
| 2 | More than EUR 38,883 up to and including EUR 78,426 | 37.56% |
| 3 | More than EUR 78,426 | 49.50% |

### Taxpayers at AOW age throughout 2026, born before 1 January 1946

| Schijf | Taxable income | Rate |
|---|---|---|
| 1 | Up to and including EUR 41,123 | 17.85% |
| 2 | More than EUR 41,123 up to and including EUR 78,426 | 37.56% |
| 3 | More than EUR 78,426 | 49.50% |

## Box 3 rates 2026 (provisional)

| Parameter | Without fiscal partner | With fiscal partner |
|---|---:|---:|
| Heffingsvrij vermogen | EUR 59,357 | EUR 118,714 |

| Category | Return percentage |
|---|---:|
| Banktegoeden and cash | 1.28% |
| Overige bezittingen | 6.00% |
| Schulden | 2.70% |

Over the calculated box 3 income, the provisional 2026 box 3 tax rate is 36%.

## Heffingskortingen 2026 (provisional)

Tax credits reduce the calculated tax. The following are the key credits used in the provisional assessment:

The tables below for algemene heffingskorting, arbeidskorting, and IACK are the
published `below_all_year` tables. Do not apply them to `aow_all_year`. For
`reaches_during_year`, the transition month affects the credit and the official
portal result remains a manual-review item.

### Algemene heffingskorting (general tax credit)

For taxpayers below AOW age throughout 2026 (`below_all_year`):

| Verzamelinkomen | Algemene heffingskorting |
|---|---:|
| Up to and including EUR 29,736 | EUR 3,115 |
| More than EUR 29,736 up to and including EUR 78,426 | EUR 3,115 - 6.398% x (verzamelinkomen - EUR 29,736) |
| More than EUR 78,426 | EUR 0 |

### Arbeidskorting (employed person's tax credit)

For taxpayers below AOW age throughout 2026 (`below_all_year`):

| Arbeidsinkomen | Arbeidskorting |
|---|---:|
| Up to and including EUR 11,965 | 8.324% x arbeidsinkomen |
| More than EUR 11,965 up to and including EUR 25,845 | EUR 996 + 31.009% x (arbeidsinkomen - EUR 11,965) |
| More than EUR 25,845 up to and including EUR 45,592 | EUR 5,300 + 1.950% x (arbeidsinkomen - EUR 25,845) |
| More than EUR 45,592 up to and including EUR 132,920 | EUR 5,685 - 6.510% x (arbeidsinkomen - EUR 45,592) |
| More than EUR 132,920 | EUR 0 |

### Inkomensafhankelijke combinatiekorting

For taxpayers below AOW age throughout 2026 (`below_all_year`):

| Arbeidsinkomen | Inkomensafhankelijke combinatiekorting |
|---|---:|
| Up to and including EUR 6,239 | EUR 0 |
| More than EUR 6,239 up to and including EUR 32,710 | 11.45% x (arbeidsinkomen - EUR 6,239) |
| More than EUR 32,710 | EUR 3,032 |

### Ouderenkorting

Review this credit when the taxpayer reaches AOW age no later than
31 December 2026, including `reaches_during_year`. The portal calculates the
affected provisional result.

| Verzamelinkomen | Ouderenkorting |
|---|---:|
| Up to and including EUR 46,002 | EUR 2,067 |
| More than EUR 46,002 up to and including EUR 59,782 | EUR 2,067 - 15% x (verzamelinkomen - EUR 46,002) |
| More than EUR 59,782 | EUR 0 |

### Other credits

- Alleenstaandeouderenkorting: EUR 540. Despite its name, this is not a
  single-parent credit. Review whether the taxpayer receives or is entitled to
  an AOW pension for a single person for all or part of 2026; entitlement for
  even part of the year can qualify for the full annual credit (including the
  published limited exceptions); do not infer it from children, household
  composition, or `single_parent_status`. If entitlement is unresolved, check
  it with the SVB and keep the workpack item under manual review.
- Jonggehandicaptenkorting: EUR 923

## Important caveats

1. These are the rates the Belastingdienst applies when calculating the provisional assessment.
2. The percentages for 2026 banktegoeden and schulden are provisional for the provisional assessment and are expected to be finalized for the definitive 2026 annual assessment.
3. The 2026 rates differ from 2025 rates -- do not reuse 2025 values.

## Developer instruction

When using these rates for provisional assessment calculations:

1. Apply the bracket rates in order (progressive taxation)
2. Calculate heffingskortingen based on the taxpayer's specific situation (income level, employment status, age, family composition)
3. Use `below_all_year`, `reaches_during_year`, or `aow_all_year`; for a
   transition year use the published month-specific first-bracket rate and the
   official portal result for affected credits rather than selecting a
   whole-year table
4. Always mark outputs as a provisional-assessment calculation
5. When the definitive annual-return 2026 rates are published, update the annual 2026 source pack separately
6. Do not mix 2025 and 2026 rates in a single calculation

## Common failure

Do not use 2025 rates for a 2026 provisional assessment. Do not treat a
taxpayer who reaches AOW age during 2026 as if they were below AOW age or at
AOW age for the whole year. Do not treat single-parent status as entitlement
to alleenstaandeouderenkorting.
