# Rule note: Tax credits (heffingskortingen) for 2025

source_ids: bd_general_tax_credit_2025, bd_labour_tax_credit_2025, bd_tax_credit_payout_2025, bd_iack_2025, bd_heffingskortingen_aow_2025_2026, bd_jonggehandicaptenkorting_2025, bd_heffingskortingen_how_2025, bd_arbeidsinkomen_definition_2025
workflow: annual_return
tax_year: 2025
status: active
last_reviewed: "2026-06-23"
review_status: reviewed

## Rule

Tax credits (heffingskortingen) reduce the amount payable. They are subtracted from the **gecombineerde heffing** — the combined total of inkomstenbelasting plus premie volksverzekeringen (AOW/Anw/Wlz) — not from box-1 income tax alone. The amounts below are for tax year 2025 and apply to non-AOW-age taxpayers (born after 1957) unless otherwise stated.

These are reference notes for workpack preparation -- not final tax advice.

## Algemene heffingskorting (general tax credit)

The algemene heffingskorting depends on the taxpayer's verzamelinkomen: income in boxes 1, 2, and 3 after persoonsgebonden aftrekposten.

For taxpayers who do not reach AOW age in 2025:

| Verzamelinkomen | Algemene heffingskorting |
|---|---:|
| Up to and including EUR 28,406 | EUR 3,068 |
| EUR 28,407 up to and including EUR 76,817 | EUR 3,068 - 6.337% x (verzamelinkomen - EUR 28,406) |
| EUR 76,818 or more | EUR 0 |

For taxpayers who have the AOW age for the whole of 2025:

| Verzamelinkomen | Algemene heffingskorting |
|---|---:|
| Up to and including EUR 28,406 | EUR 1,536 |
| EUR 28,407 up to and including EUR 76,817 | EUR 1,536 - 3.170% x (verzamelinkomen - EUR 28,406) |
| EUR 76,818 or more | EUR 0 |

For taxpayers who reach AOW age during 2025, do not interpolate in the workpack. Flag this for manual review in Mijn Belastingdienst because the Belastingdienst calculates the adjusted amount in the official form.

### Phase-out mechanism

For verzamelinkomen above the phase-out start:
- Reduction = phase-out percentage x (verzamelinkomen - phase-out threshold)
- The credit cannot become negative; it floors at EUR 0

### AOW-age adjustment

For taxpayers who have the AOW age for the whole year, use the AOW table above. For taxpayers who reach AOW age during 2025, mark the exact amount as a manual-review item in the official form.

## Arbeidskorting (labour tax credit)

The arbeidskorting applies to taxpayers with income from work (arbeidsinkomen): employment, self-employment, and certain work-related uitkeringen. Whether a uitkering counts depends on the situation — see "What qualifies as arbeidsinkomen" below. It does NOT apply to pension income, AOW, WW, WIA/WAO, or alimentatie received. A blanket "no uitkering counts" is wrong: for example a Ziektewet-uitkering can count while the dienstbetrekking still exists.

For taxpayers who do not reach AOW age in 2025:

| Arbeidsinkomen | Arbeidskorting |
|---|---:|
| Up to and including EUR 12,169 | 8.053% x arbeidsinkomen |
| EUR 12,170 up to and including EUR 26,288 | EUR 980 + 30.030% x (arbeidsinkomen - EUR 12,169) |
| EUR 26,289 up to and including EUR 43,071 | EUR 5,220 + 2.258% x (arbeidsinkomen - EUR 26,288) |
| EUR 43,072 up to and including EUR 129,078 | EUR 5,599 - 6.510% x (arbeidsinkomen - EUR 43,071) |
| EUR 129,079 or more | EUR 0 |

For taxpayers who have the AOW age for the whole of 2025:

| Arbeidsinkomen | Arbeidskorting |
|---|---:|
| Up to and including EUR 12,169 | 4.029% x arbeidsinkomen |
| EUR 12,170 up to and including EUR 26,288 | EUR 491 + 15.023% x (arbeidsinkomen - EUR 12,169) |
| EUR 26,289 up to and including EUR 43,071 | EUR 2,612 + 1.130% x (arbeidsinkomen - EUR 26,288) |
| EUR 43,072 up to and including EUR 129,078 | EUR 2,802 - 3.257% x (arbeidsinkomen - EUR 43,071) |
| EUR 129,079 or more | EUR 0 |

For taxpayers who reach AOW age during 2025, mark the exact amount as a manual-review item in the official form.

### Phase-in and phase-out mechanism

The arbeidskorting has a multi-step calculation:
1. Low income range: the credit increases as a percentage of arbeidsinkomen
2. Middle income range: the credit continues increasing under the published table
3. High income range: from EUR 43,072 through EUR 129,078, the credit is reduced by the published phase-out formula
4. Zero point: from EUR 129,079, the credit is EUR 0

### What qualifies as arbeidsinkomen

- Gross salary from employment (loon)
- Profit from enterprise (winst uit onderneming) before ondernemersaftrek
- Income from other activities (resultaat uit overige werkzaamheden)
- A **Ziektewet-uitkering** IF the dienstbetrekking still exists at the time of the uitkering
- A **vrijwillige Ziektewetuitkering** always counts
- **WAZO** (pregnancy/maternity/calamity leave benefit) while still employed

The following do NOT qualify:
- Pension income (pensioen)
- AOW
- WW
- WIA, WAO
- A Ziektewet-uitkering from 2020 onward WITHOUT a dienstbetrekking
- Alimentatie received

### AOW-age adjustment

For taxpayers who have the AOW age for the whole year, use the AOW table above. For taxpayers who reach AOW age during 2025, mark the exact amount as a manual-review item in the official form.

## Other heffingskortingen

These credits use reviewed 2025 figures and may be calculated in the workpack when the eligibility conditions are met. Show the calculation step by step and require taxpayer review. The Belastingdienst online system applies these automatically; the workpack states the expected amount for verification.

### Inkomensafhankelijke combinatiekorting (IACK)

source: bd_iack_2025

For working parents with a child born after 31 December 2012 who is under 12 on 1 January 2025 and belongs to the household for at least 6 months. The taxpayer must have arbeidsinkomen above EUR 6,145 and either (a) no fiscal partner, or a fiscal partner for less than 6 months, or (b) a lower arbeidsinkomen than the fiscal partner.

| Arbeidsinkomen (non-AOW-age) | IACK 2025 |
|---|---:|
| Up to and including EUR 6,145 | EUR 0 |
| EUR 6,146 up to and including EUR 32,223 | 11.45% x (arbeidsinkomen - EUR 6,145) |
| EUR 32,224 or more | EUR 2,986 (maximum) |

- Only the partner with the lower arbeidsinkomen claims the IACK. If both partners' arbeidsinkomen is equal, only the older partner claims it.
- Payout of the IACK to the least-earning partner was abolished from 2023.
- Co-ouderschap (co-parenting) has specific day-count conditions (the child stays with each parent in a repeating rhythm). Flag co-parenting cases for manual review rather than auto-calculating.
- If the taxpayer reaches AOW age during 2025, the adjusted amount is calculated by the Belastingdienst — mark it as a manual-review item.

### Ouderenkorting

source: bd_heffingskortingen_aow_2025_2026

For taxpayers who have reached the AOW age by the end of 2025.

| Verzamelinkomen | Ouderenkorting 2025 |
|---|---:|
| Up to and including EUR 45,308 | EUR 2,035 |
| EUR 45,309 up to and including EUR 58,874 | EUR 2,035 - 15% x (verzamelinkomen - EUR 45,308) |
| EUR 58,875 or more | EUR 0 |

### Alleenstaande-ouderenkorting

source: bd_heffingskortingen_aow_2025_2026

- For taxpayers who receive (or are entitled to) an AOW benefit for a single person (alleenstaande).
- Fixed amount: EUR 531 for 2025 (EUR 540 for 2026).
- If a couple lives apart because one partner is in a care home, both may be entitled — flag for manual review.

### Jonggehandicaptenkorting

source: bd_jonggehandicaptenkorting_2025

- For taxpayers entitled to a Wajong benefit (or Wajong work support) who do not receive the ouderenkorting.
- Fixed amount: EUR 909 for 2025 (EUR 923 for 2026).
- Entitlement is enough; the benefit need not actually be paid out. The taxpayer must actively tick the Wajong question in the online return or the credit is lost — surface this as a review item.

### Levensloopverlofkorting

- Transitional arrangement for old levensloop savings; largely phased out. If the user reports an old levensloop balance, flag it for manual review.

## Applying credits in the workpack

1. Calculate the gross gecombineerde heffing (IB + premie volksverzekeringen) using the rates from box1-rates.md
2. Determine the algemene heffingskorting based on verzamelinkomen, not only box 1 income
3. Determine the arbeidskorting based on arbeidsinkomen only
4. Determine any other applicable credits
5. Net amount due = gross gecombineerde heffing (IB + premie volksverzekeringen) - total credits (minimum EUR 0; credits cannot create a refund on their own beyond the gross gecombineerde heffing, but combined with wage tax withholding they can result in a refund)

## Fiscal partner allocation

- The algemene heffingskorting is personal and cannot be allocated
- The arbeidskorting is personal and based on individual arbeidsinkomen
- Some credits (e.g., IACK) have specific partner allocation rules
- For the lesser-earning partner, payout of unused algemene heffingskorting requires BOTH: (a) the partner's algemene heffingskorting exceeds their own income tax due (so there is an unused portion), AND (b) the partner was born before 1963. In 2025, taxpayers born after 1962 receive no payout. Taxpayers born before 1963 may receive up to EUR 3,068 (the 2025 maximum), depending on their own income and the partner's tax due. Flag this as a manual-review item rather than assuming payout applies.

## Notes

- These amounts are for tax year 2025 only. Credits are indexed annually.
- The phase-out thresholds and percentages are set by the government each year in the Belastingplan.
- In the workpack, show the credit calculation step by step so the taxpayer can verify the amounts against the online return.
- The Belastingdienst's online system calculates credits automatically, but the workpack should include the expected amounts for verification.
- AOW-age taxpayers get lower credit amounts because the credits are proportionally reduced to reflect the lower premie volksverzekeringen they owe.
