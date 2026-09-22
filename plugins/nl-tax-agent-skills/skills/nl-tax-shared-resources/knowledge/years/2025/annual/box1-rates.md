# Rule note: Box 1 income tax rates for 2025

source_ids: bd_box1_rates_2025, bd_bijtelling_auto_2025, bd_stock_options_2025, bd_jaaropgaaf_fields_2025
workflow: annual_return
tax_year: 2025
status: active
last_reviewed: "2026-07-16"
review_status: reviewed

## Rule

Box 1 (inkomen uit werk en woning) income is taxed in progressive brackets (schijven). The rates below are the combined rates of inkomstenbelasting (IB) and premie volksverzekeringen (social insurance contributions: AOW, Anw, Wlz). These rates apply for tax year 2025.

These are reference notes for workpack preparation -- not final tax advice.

## Tax brackets for taxpayers who are 66 or younger in 2025

| Schijf | Taxable income (belastbaar inkomen) | Combined rate (IB + premie volksverzekeringen) |
|--------|-------------------------------------|-----------------------------------------------|
| 1      | Up to EUR 38,441                    | 35.82%                                        |
| 2      | Above EUR 38,441 up to and including EUR 76,817 | 37.48%                              |
| 3      | Above EUR 76,817                    | 49.50%                                        |

## Composition of the combined rates

The combined rate in schijf 1 (35.82%) consists of:
- Inkomstenbelasting component
- AOW premie: 17.90%
- Anw premie: 0.10%
- Wlz premie: 9.65%

The premie volksverzekeringen component applies only to schijf 1. In schijf 2 and schijf 3, the rate is purely inkomstenbelasting.

Note: the exact IB component of schijf 1 is the combined rate minus the premie components (35.82% - 17.90% - 0.10% - 9.65% = 8.17%).

## Tax brackets for taxpayers who reach AOW age during 2025

Taxpayers who reach AOW age during 2025 have an adjusted first-bracket rate. Do not derive this from the whole-year AOW table.

| AOW age reached in | First-bracket rate up to EUR 38,441 |
|---|---:|
| January | 17.92% |
| February | 19.41% |
| March | 20.90% |
| April | 22.39% |
| May | 23.88% |
| June | 25.37% |
| July | 26.87% |
| August | 28.36% |
| September | 29.85% |
| October | 31.34% |
| November | 32.83% |
| December | 34.32% |

For these taxpayers, schijf 2 and 3 use the same 2025 boundaries and rates as the official AOW-age table: more than EUR 38,441 up to and including EUR 76,817 at 37.48%, and more than EUR 76,817 at 49.50%.

## Tax brackets for taxpayers who have reached AOW age for all of 2025

AOW-age taxpayers pay a lower first-bracket rate because they no longer pay AOW premie. The first-bracket boundary differs for taxpayers born before 1 January 1946.

### Born before 1 January 1946

| Schijf | Taxable income (belastbaar inkomen) | Combined rate (IB + remaining premies) |
|--------|-------------------------------------|----------------------------------------|
| 1      | Up to EUR 40,502                    | 17.92%                                 |
| 2      | More than EUR 40,502 up to and including EUR 76,817 | 37.48% |
| 3      | More than EUR 76,817                | 49.50%                                 |

### Born on or after 1 January 1946 and already AOW-age before 2025

| Schijf | Taxable income (belastbaar inkomen) | Combined rate (IB + remaining premies) |
|--------|-------------------------------------|----------------------------------------|
| 1      | Up to EUR 38,441                    | 17.92%                                 |
| 2      | More than EUR 38,441 up to and including EUR 76,817 | 37.48% |
| 3      | More than EUR 76,817                | 49.50%                                 |

Note: the whole-year AOW first-bracket rate (17.92%) consists of the IB component (8.17%) plus Anw premie (0.10%) plus Wlz premie (9.65%). The AOW premie (17.90%) is not owed.

## Calculation example (non-AOW-age)

For a taxable box 1 income of EUR 60,000:
- First EUR 38,441 at 35.82% = EUR 13,770
- Remaining EUR 21,559 (EUR 60,000 - EUR 38,441) at 37.48% = EUR 8,080
- Gross box 1 tax before credits = EUR 21,850
- Heffingskortingen (tax credits) are then subtracted from this amount. See credits.md.

## Taxable income determination

Box 1 taxable income includes:
- Wages and salary (loon)
- Pension income (pensioenuitkeringen)
- Social benefits (uitkeringen: WW, WIA, AOW, Anw, bijstand)
- Profit from enterprise (winst uit onderneming), after ondernemersaftrek
- Income from other activities (resultaat uit overige werkzaamheden)
- Periodic payments received (alimentatie)
- Own home: eigenwoningforfait minus deductible mortgage interest (may be negative)
- Minus: persoonsgebonden aftrek (personal deductions allocated to box 1)

## Company car private-use addition 2025

If a taxpayer privately uses a company car or a car that belongs to business
assets, a private-use addition may be included in taxable Box 1 income unless
the taxpayer can show **500 private kilometres or fewer** for the year.

Before presenting any company-car rate in a taxpayer workpack, confirm the date
of first admission, vehicle regime, emissions/fuel facts, catalogue value, and
private-use evidence. If those facts are not known, withhold the rate and mark
the company-car outcome as manual review. The percentages below are reference
rules for cars first admitted in 2025, not a default for an unidentified car.

For cars first admitted in 2025, the reviewed official percentages are:

- 17% for zero-emission cars.
- 22% for cars with CO2 emissions above zero.
- The 17% rate applies without the EUR 30,000 cap only for hydrogen cars and
  cars fully powered by integrated solar cells that meet the official
  conditions.
- For other zero-emission cars, the 17% rate applies up to and including a
  catalogue value of EUR 30,000; the portion above EUR 30,000 uses 22%.

In standard employee cases this amount is normally already included in the
jaaropgaaf taxable wage. If it appears missing, disputed, or not supported by
the employer statement, flag it for manual review.

## Stock options and tradability

Claim-specific provenance: `bd_stock_options_2025`, the official Belastingdienst
*Handboek Loonheffingen 2025*, version March 2025, section on aandelenopties
([official PDF](https://download.belastingdienst.nl/belastingdienst/docs/handboek-loonheffingen-lh0221t51d.pdf)).

For employee stock options, tradability is the default tax point under the
reviewed rule: by default, taxation follows when the acquired shares become
tradable. Immediate-tradability cases and an election to use exercise as the
tax point require the agent to collect the employer statement and mark the
result for manual review. Do not infer the tax point merely from an exercise
date.

## Notes

- These are 2025 rates. Rates change annually; do not use these for other tax years.
- The bracket boundaries (EUR 38,441 and EUR 76,817) are indexed annually.
- For part-year tax residency, the brackets are not pro-rated; however, the premie volksverzekeringen may be pro-rated for the period of residency/insurance.
- The premie volksverzekeringen have a maximum income base equal to the top of schijf 1 (EUR 38,441). Above that threshold, only IB is owed.
- Box 1 tax is calculated before applying heffingskortingen (tax credits). The net tax payable is the gross tax minus applicable credits.
