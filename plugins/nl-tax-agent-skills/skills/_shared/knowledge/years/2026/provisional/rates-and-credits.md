# Rule note: Rates and credits for voorlopige aanslag 2026

source_id: bd_provisional_rates_2026
workflow: provisional_assessment
tax_year: 2026
status: active
last_reviewed: "2026-04-30"
review_status: reviewed

## Rule

The voorlopige aanslag 2026 is calculated using provisional tax rates and credits. These are the rates the Belastingdienst uses for the provisional assessment and may differ from the final rates applied at annual return time. All rates below are provisional and subject to verification when definitive 2026 rates are published.

## Box 1 rates 2026 (provisional)

Box 1 income (income from employment and home ownership) is taxed in progressive brackets:

### Schijf 1

- Taxable income: up to EUR ~38,441
- Rate: ~35.82%
- _Pending verification from 2026 source snapshot -- rate may differ from 2025_

### Schijf 2

- Taxable income: EUR ~38,441 to EUR ~76,817
- Rate: ~37.48%
- _Pending verification from 2026 source snapshot -- rate may differ from 2025_

### Schijf 3

- Taxable income: above EUR ~76,817
- Rate: ~49.50%
- _Pending verification from 2026 source snapshot -- rate may differ from 2025_

Note: for taxpayers who have reached the AOW age (pensioengerechtigde leeftijd), lower rates apply in the first bracket due to the absence of AOW premiums. This is not detailed here but must be accounted for in calculation logic.

## Heffingskortingen 2026 (provisional)

Tax credits reduce the calculated tax. The following are the key credits used in the provisional assessment:

### Algemene heffingskorting (general tax credit)

- Maximum amount: ~EUR 3,068
- _Pending verification from 2026 source snapshot_
- Phases out as income increases above a threshold
- The phase-out percentage and income threshold must be verified for 2026

### Arbeidskorting (employed person's tax credit)

- Maximum amount: ~EUR 5,599
- _Pending verification from 2026 source snapshot_
- Applies to income from employment or self-employment
- Builds up to the maximum and then phases out at higher incomes
- The build-up rate, phase-out rate, and income thresholds must be verified for 2026

### Other credits (where applicable)

- Inkomensafhankelijke combinatiekorting (income-dependent combination credit) -- for working parents with young children
- Jonggehandicaptenkorting (young disabled person's credit)
- Ouderenkorting (elderly person's credit) -- for taxpayers who have reached AOW age
- Alleenstaande ouderenkorting (single elderly person's credit)

Amounts and thresholds for these additional credits must be verified against the 2026 source snapshot.

## Important caveats

1. The provisional assessment uses ESTIMATED rates that may be adjusted when definitive rates are published
2. These are the rates the Belastingdienst applies when calculating the provisional assessment -- they are not necessarily the final rates
3. The 2026 rates may differ from 2025 rates -- do not assume they are identical
4. All amounts marked with ~ are approximate and pending verification

## Developer instruction

When using these rates for provisional assessment calculations:

1. Apply the bracket rates in order (progressive taxation)
2. Calculate heffingskortingen based on the taxpayer's specific situation (income level, employment status, age, family composition)
3. Account for AOW-age taxpayers who have different first-bracket rates
4. Always mark outputs as "provisional" and note that final rates may differ
5. If definitive 2026 rates become available, update this file and change all "pending verification" markers
6. Do not mix 2025 and 2026 rates in a single calculation

## Common failure

Do not present provisional rates as definitive. Every calculation using these rates must be accompanied by a note that the amounts are based on provisional rates and may change. Do not use 2025 rates for a 2026 provisional assessment without explicitly marking them as carried forward and unverified.
