# Rule note: Rates and credits for voorlopige aanslag 2026

source_id: bd_provisional_rates_2026
workflow: provisional_assessment
tax_year: 2026
status: active
last_reviewed: "2026-04-30"
review_status: reviewed

## Rule

The voorlopige aanslag 2026 is calculated using the tax rates and credits published by the Belastingdienst for provisional-assessment calculations.

## Box 1 rates 2026 (provisional)

Box 1 income (income from employment and home ownership) is taxed in progressive brackets.

### Taxpayers who have not reached AOW age in 2026

| Schijf | Taxable income | Rate |
|---|---|---|
| 1 | Up to and including EUR 38,883 | 35.75% |
| 2 | More than EUR 38,883 up to and including EUR 78,426 | 37.56% |
| 3 | More than EUR 78,426 | 49.50% |

### Taxpayers who reached AOW age and were born on or after 1 January 1946

| Schijf | Taxable income | Rate |
|---|---|---|
| 1 | Up to and including EUR 38,883 | 17.85% |
| 2 | More than EUR 38,883 up to and including EUR 78,426 | 37.56% |
| 3 | More than EUR 78,426 | 49.50% |

### Taxpayers who reached AOW age and were born before 1 January 1946

| Schijf | Taxable income | Rate |
|---|---|---|
| 1 | Up to and including EUR 41,123 | 17.85% |
| 2 | From EUR 41,123 up to and including EUR 78,426 | 37.56% |
| 3 | From EUR 78,426 | 49.50% |

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

### Algemene heffingskorting (general tax credit)

For taxpayers who have not reached AOW age:

| Verzamelinkomen | Algemene heffingskorting |
|---|---:|
| Up to EUR 29,736 | EUR 3,115 |
| From EUR 29,736 up to EUR 78,426 | EUR 3,115 - 6.398% x (verzamelinkomen - EUR 29,736) |
| From EUR 78,426 | EUR 0 |

### Arbeidskorting (employed person's tax credit)

For taxpayers who have not reached AOW age:

| Arbeidsinkomen | Arbeidskorting |
|---|---:|
| Up to EUR 11,965 | 8.324% x arbeidsinkomen |
| From EUR 11,965 up to EUR 25,845 | EUR 996 + 31.009% x (arbeidsinkomen - EUR 11,965) |
| From EUR 25,845 up to EUR 45,592 | EUR 5,300 + 1.950% x (arbeidsinkomen - EUR 25,845) |
| From EUR 45,592 up to EUR 132,920 | EUR 5,685 - 6.510% x (arbeidsinkomen - EUR 45,592) |
| From EUR 132,920 | EUR 0 |

### Inkomensafhankelijke combinatiekorting

For taxpayers who have not reached AOW age:

| Arbeidsinkomen | Inkomensafhankelijke combinatiekorting |
|---|---:|
| Up to EUR 6,239 | EUR 0 |
| From EUR 6,239 up to EUR 32,710 | 11.45% x (arbeidsinkomen - EUR 6,239) |
| From EUR 32,710 | EUR 3,032 |

### Ouderenkorting

| Verzamelinkomen | Ouderenkorting |
|---|---:|
| Up to EUR 46,002 | EUR 2,067 |
| From EUR 46,002 up to EUR 59,782 | EUR 2,067 - 15% x (verzamelinkomen - EUR 46,002) |
| From EUR 59,782 | EUR 0 |

### Other credits

- Alleenstaandeouderenkorting: EUR 540
- Jonggehandicaptenkorting: EUR 923

## Important caveats

1. These are the rates the Belastingdienst applies when calculating the provisional assessment.
2. The percentages for 2026 banktegoeden and schulden are provisional for the provisional assessment and are expected to be finalized for the definitive 2026 annual assessment.
3. The 2026 rates differ from 2025 rates -- do not reuse 2025 values.

## Developer instruction

When using these rates for provisional assessment calculations:

1. Apply the bracket rates in order (progressive taxation)
2. Calculate heffingskortingen based on the taxpayer's specific situation (income level, employment status, age, family composition)
3. Account for AOW-age taxpayers who have different first-bracket rates
4. Always mark outputs as a provisional-assessment calculation
5. When the definitive annual-return 2026 rates are published, update the annual 2026 source pack separately
6. Do not mix 2025 and 2026 rates in a single calculation

## Common failure

Do not use 2025 rates for a 2026 provisional assessment. Do not apply the not-yet-AOW brackets to an AOW-age taxpayer.
