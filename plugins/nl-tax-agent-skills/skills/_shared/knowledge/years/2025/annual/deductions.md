# Rule note: Common deductions for annual return 2025

source_ids: bd_fisin_2025_index, bd_giften_aftrek_2025, bd_zorgkosten_overzicht_2025
workflow: annual_return
tax_year: 2025
status: active
last_reviewed: "2026-05-15"
review_status: reviewed

## Rule

The Dutch income tax system provides several deduction categories that reduce taxable income. This note covers the main deductions relevant to the 2025 annual return. Most deductions fall under the persoonsgebonden aftrek (personal deductions) or are specific deductions within box 1.

These are reference notes for workpack preparation -- not final tax advice.

## Persoonsgebonden aftrek (personal deductions)

The persoonsgebonden aftrek is a collection of deductible items that are subtracted from total income. They are first applied to box 1, then box 3, then box 2 income (in that order). The main components are:

### Alimentatie (maintenance payments to ex-partner)

- Partneralimentatie paid to an ex-partner is deductible in full (no threshold or cap).
- Kinderalimentatie (child maintenance) is NOT deductible.
- The deduction applies to payments made under a court order, divorce agreement, or notarial deed.
- The recipient must report the alimentatie received as box 1 income.
- Evidence required: court order or agreement, plus proof of payments made (bank statements).

### Specifieke zorgkosten (specific healthcare costs)

Medical expenses that are not reimbursed by health insurance may be deductible, but only the portion that exceeds a drempel (threshold).

#### Qualifying expenses include:

- Prescribed medication (voorgeschreven medicijnen) not covered by basic insurance
- Medical aids and devices (hulpmiddelen) such as hearing aids, wheelchairs, prosthetics
- Extra costs of a medically prescribed diet (dieetkosten) -- standard amounts per diet type set by the Belastingdienst
- Travel by car to arts, ziekenhuis, or apotheek: EUR 0.23 per kilometer (parking, ferry, and toll costs separately). Travel by taxi or public transport: actual costs.
- Reiskosten ziekenbezoek (visiting a sick relative): EUR 0.23 per km, but only if (a) you shared a household with the sick person at the start of the illness, (b) the verpleging lasts longer than 1 month in total, and (c) the one-way distance home-to-place-of-care exceeds 10 km
- Costs of home modifications for medical reasons (aanpassingen woning)
- Extra clothing and bedding costs due to illness or disability (extra kleding en beddengoed)
- Prescribed therapies not covered by insurance

#### Threshold (drempel)

- The deductible amount is the total qualifying expenses minus the drempel.
- The drempel is income-dependent and must be calculated from the official 2025 specific-healthcare-costs table.
- This source pack does not yet contain a reviewed 2025 table for the exact zorgkosten drempel.
- Until that source is added, do not calculate the zorgkosten deduction in the workpack. List the gross qualifying expenses, record the evidence, and flag the exact drempel and deductible amount for manual review in Mijn Belastingdienst.
- Drempelinkomen = combined income of taxpayer and fiscal partner before persoonsgebonden aftrek.

#### Multiplier for specific costs

Certain specific zorgkosten are multiplied by a factor before applying the threshold. This effectively increases the deductible amount for those items.

### Giften (charitable donations)

Donations to ANBI-registered institutions (Algemeen Nut Beogende Instelling) and qualified cultural institutions (culturele ANBI) may be deductible. There are two categories:

#### Periodieke giften (periodic gifts)

- Regular donations committed for at least 5 years via a notarial deed or written agreement (schenkingsovereenkomst).
- No threshold (drempel) applies.
- Maximum deductible: EUR 1,500,000 per year, combined for taxpayer and fiscal partner, for 2025 and 2026 (was EUR 250,000 in 2024).
- Overgangsregeling: periodieke-gift agreements entered into before 4 October 2022 at 16:00 keep the unlimited deduction through tax year 2027.
- Evidence required: notarial deed or written agreement, plus proof of payments.

#### Gewone giften / eenmalige giften (incidental gifts)

- One-time or irregular donations to ANBI institutions.
- Threshold (drempel): 1% of drempelinkomen (with a minimum of EUR 60).
- Maximum: 10% of drempelinkomen.
- Only the amount between the threshold and the maximum is deductible.
- Gifts to cultural ANBI institutions may be multiplied by 1.25 (up to a maximum increase of EUR 1,250) before applying the threshold and cap.

### Studiekosten / scholingsuitgaven (education expenses)

- Do not claim or calculate education-expense deductions from this source pack unless a reviewed 2025 source-register entry for the specific education-expense rule has been added.
- If the user reports education expenses, list the expense and evidence as a manual-review item instead of treating it as deductible.

### Restant persoonsgebonden aftrek (carryforward from prior years)

- If the persoonsgebonden aftrek in a prior year exceeded the total income, the unused portion can be carried forward to subsequent years.
- The workpack should ask whether the taxpayer has unused deductions from prior years.

## Lijfrentepremie (annuity premium deduction)

Premiums paid for lijfrente (annuity insurance or bank savings for retirement) are deductible within limits.

### Jaarruimte (annual space)

- The annual deductible amount depends on the pension gap: the difference between the taxpayer's income and the pension already accrued through employer pension schemes.
- This source pack does not yet contain a reviewed 2025 source for the exact jaarruimte formula parameters, AOW franchise, or ceiling.
- Until that source is added, do not calculate jaarruimte in the workpack. List paid lijfrentepremies, factor A evidence, and the missing official calculation as manual-review items.

### Reserveringsruimte (carryback space)

- Unused jaarruimte from prior years may be usable under the official rules.
- This source pack does not yet contain reviewed 2025 reserveringsruimte limits.
- Until that source is added, do not calculate reserveringsruimte. Flag it for manual review in the official filing environment.

### Evidence required

- Annual statement from the lijfrente provider showing premiums paid.
- Factor A statement from the employer's pension scheme (for jaarruimte calculation).

## AOV premie (disability insurance for self-employed)

- Self-employed individuals (ZZP'ers / IB-ondernemers) who pay premiums for an arbeidsongeschiktheidsverzekering (disability insurance) can deduct these premiums.
- The premiums are deductible as costs of the enterprise (winst uit onderneming) or as income-related deduction.
- Evidence required: annual statement from the insurer.

## Partner allocation (verdeling aftrekposten)

Fiscal partners can allocate the following deductions between them in the most tax-efficient way:

### Allocatable items

- Persoonsgebonden aftrek components (alimentatie, zorgkosten, giften, etc.)
- Eigen woning: the net result can be allocated between partners
- Box 3: the joint grondslag sparen en beleggen can be allocated freely between partners

### Allocation strategy

- In general, allocate deductions to the partner with the highest marginal tax rate for maximum benefit.
- The tariefsaanpassing eigen woning (37.48% cap) may affect optimal allocation of the eigen woning result.
- The phase-out of heffingskortingen (algemene heffingskorting, arbeidskorting) also affects the optimal allocation.
- The workpack should model at least the default allocation and one optimized allocation for the taxpayer to compare.

### Items that CANNOT be allocated

- Arbeidskorting: based on individual arbeidsinkomen
- Ondernemersaftrek: personal to the ondernemer
- MKB-winstvrijstelling: personal to the ondernemer

## Common errors to flag in the workpack

1. Claiming kinderalimentatie as deductible (it is not).
2. Forgetting the drempel for zorgkosten and giften.
3. Double-counting costs already reimbursed by insurance.
4. Not verifying ANBI status of the charity before claiming giften.
5. Using the wrong drempelinkomen (should be combined income of both partners).
6. Forgetting restant persoonsgebonden aftrek from prior years.
7. Claiming studiekosten when the STAP-budget was already used for the same expense.

## Notes

- The persoonsgebonden aftrek is allocated in order: box 1 first, then box 3, then box 2. Since box 1 typically has the highest marginal rate, this ordering generally maximizes the tax benefit.
- For the 2025 return, collect all supporting documents as listed in evidence-checklist.md.
- The Belastingdienst may request proof (bewijsstukken) of deductions up to 5 years after filing. The taxpayer should retain all receipts and documentation.
- Deductions reduce taxable income, not tax payable directly. The actual tax benefit depends on the marginal rate at which the deduction is applied.
