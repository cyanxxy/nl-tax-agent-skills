# Annual Income-Tax Return Workpack -- 2025

## Scope

Tax year: 2025
Workflow: Annual income-tax return (aangifte inkomstenbelasting)
Taxpayer: [from profile]
Fiscal partner: [yes/no, from profile]
Created: [timestamp]

## Unsupported-case checks

- [ ] Full-year Dutch resident: [yes/no]
- [ ] Individual taxpayer (not business): [yes/no]
- [ ] Living taxpayer: [yes/no]
- [ ] No M-biljet required: [yes/no]

If any check is "no", this workpack should not have been generated. Stop and consult the intake skill.

## Sources used

[List of source_ids from source-register.yaml used in this workpack. Example:]

- bd_annual_return_landing_2025
- bd_annual_return_4_steps_2025
- bd_annual_data_checklist_2025
- bd_fisin_2025_index
- bd_box1_rates_2025
- bd_general_tax_credit_2025
- bd_labour_tax_credit_2025
- bd_own_home_deduction_cap_2025
- bd_box3_2025_calc
- bd_box3_2025_actual_return
- bd_fisin_box3_actual_return_2025
- bd_digid_machtigen
- law_wet_inkomstenbelasting_2001
- law_uitvoeringsregeling_ib_2001
- law_uitvoeringsbesluit_ib_2001
- regels_overheid_regelspraak

[Remove any source_ids that were not actually consulted. Add any additional source_ids that were used.]

## Taxpayer profile summary

[Summary from workspace/taxpayer/profile.yaml. Include:]

- Name: [taxpayer name]
- Date of birth: [date]
- Residency: full-year Dutch resident 2025
- Primary income type: [employment / pension / benefit / combination]
- Fiscal partner: [yes/no]
- Partner name: [if applicable]
- Address: [municipality, for WOZ reference]
- Special circumstances: [any flags from intake]

## Evidence summary

[Summary from workspace/taxpayer/evidence-index.yaml. Include:]

- Total evidence files indexed: [count]
- Files by category:
  - Income (jaaropgaven, pension statements): [count]
  - Own home (WOZ-beschikking, mortgage statement): [count]
  - Box 3 (bank statements, portfolio statements): [count]
  - Deductions (medical receipts, donation receipts): [count]
  - Other: [count]
- Files flagged for review: [count]
- Files with low classification confidence: [count]

## Income notes

### Employment income (loon uit dienstbetrekking)

| Employer | Gross salary | Loonheffing withheld | Evidence |
|----------|-------------|---------------------|----------|
| [name]   | EUR [amount] | EUR [amount]       | [evidence_id] |

[Add rows for each employer. If no employment income, state "Not applicable -- no employment income reported."]

### Pension income

| Provider | Type | Gross pension | Loonheffing withheld | Evidence |
|----------|------|--------------|---------------------|----------|
| [name]   | [employer pension / AOW] | EUR [amount] | EUR [amount] | [evidence_id] |

[Add rows for each pension provider. If no pension income, state "Not applicable."]

### Benefit income (uitkeringen)

| Provider | Benefit type | Gross amount | Loonheffing withheld | Evidence |
|----------|-------------|-------------|---------------------|----------|
| [UWV/SVB] | [WW/WIA/WAO/ZW/Anw/AKW] | EUR [amount] | EUR [amount] | [evidence_id] |

[Add rows for each benefit. If no benefit income, state "Not applicable."]

### Other box 1 income

| Description | Amount | Source |
|-------------|--------|--------|
| [e.g., alimentatie received, freelance income] | EUR [amount] | [evidence_id or assumption_id] |

[If no other income, state "Not applicable."]

### Box 1 income total

| Item | Amount |
|------|--------|
| Total gross employment income | EUR [amount] |
| Total gross pension income | EUR [amount] |
| Total gross benefit income | EUR [amount] |
| Total other box 1 income | EUR [amount] |
| **Total box 1 income (before deductions)** | **EUR [amount]** |
| Total loonheffing withheld | EUR [amount] |

## Own-home notes

[If no own home: "Not applicable -- the taxpayer does not own a primary residence. Skip to Box 3 notes."]

### WOZ-waarde

- WOZ-waarde (waardepeildatum 1 January 2024): EUR [amount]
- Source: [evidence_id or assumption_id]
- Bezwaar filed: [yes/no]

### Hypotheekrente

- Total mortgage interest paid in 2025: EUR [amount]
- Mortgage type: [annuitair / lineair / aflossingsvrij (pre-2013)]
- Outstanding balance 31 December 2025: EUR [amount]
- Source: [evidence_id]
- Deduction qualification: [confirmed / requires review]

### Eigenwoningforfait

- WOZ-waarde bracket: EUR [lower] to EUR [upper]
- Applicable percentage: [percentage]%
- Eigenwoningforfait: EUR [WOZ-waarde] x [percentage]% = EUR [amount]

### Tariefsaanpassing

[If taxpayer income is in schijf 3 (above EUR 76,817):]

- Portion of mortgage interest falling in schijf 3: EUR [amount]
- Tariefsaanpassing: EUR [amount] x (49.50% - 37.48%) = EUR [amount]
- Effective deduction rate for this portion: 37.48%

[If income is below schijf 3: "Not applicable -- income does not exceed the schijf 3 threshold."]

### Hillenregeling

[If eigenwoningforfait exceeds mortgage interest:]

- Excess eigenwoningforfait: EUR [eigenwoningforfait] - EUR [interest] = EUR [amount]
- Hillenregeling correction (76.67% in 2025): EUR [amount] x 76.67% = EUR [amount]
- Net eigenwoningforfait after Hillenregeling: EUR [amount]

[If mortgage interest exceeds eigenwoningforfait: "Not applicable -- mortgage interest exceeds the eigenwoningforfait."]

### Net own-home result

| Item | Amount |
|------|--------|
| Eigenwoningforfait | EUR [amount] |
| Minus: mortgage interest | EUR [amount] |
| Plus: tariefsaanpassing (if applicable) | EUR [amount] |
| Minus: Hillenregeling correction (if applicable) | EUR [amount] |
| **Net own-home result** | **EUR [amount]** |

[A negative result reduces box 1 taxable income.]

## Box 3 notes

### Assets on peildatum (1 January 2025)

#### Banktegoeden

| Account | Bank | Balance 1 Jan 2025 | Evidence |
|---------|------|-------------------|----------|
| [description] | [bank name] | EUR [amount] | [evidence_id] |

**Total banktegoeden (category I):** EUR [amount]

#### Overige bezittingen (investments, crypto, other)

| Asset | Type | Value 1 Jan 2025 | Evidence |
|-------|------|-----------------|----------|
| [description] | [investments / crypto / real estate / receivables / other] | EUR [amount] | [evidence_id] |

**Total overige bezittingen (category II):** EUR [amount]

### Schulden (non-mortgage debts)

| Debt | Type | Balance 1 Jan 2025 | Evidence |
|------|------|-------------------|----------|
| [description] | [consumer loan / student debt / other] | EUR [amount] | [evidence_id] |

**Total schulden (category III):** EUR [amount]

### Heffingsvrij vermogen

- Single taxpayer: EUR 57,000
- Fiscal partners (combined): EUR 114,000
- Applicable heffingsvrij vermogen: EUR [amount]

### Fictitious return calculation notes

| Step | Description | Amount |
|------|-------------|--------|
| 1 | Category I total (banktegoeden) | EUR [amount] |
| 2 | Category II total (overige bezittingen) | EUR [amount] |
| 3 | Category III total (schulden) | EUR [amount] |
| 4 | Total assets (I + II) | EUR [amount] |
| 5 | Net assets (I + II - III) | EUR [amount] |
| 6 | Weighted fictitious return: (I x 0.36% + II x 6.04% - III x 2.47%) / (I + II - III) | [percentage]% |
| 7 | Rendementsgrondslag: net assets - heffingsvrij vermogen | EUR [amount] |
| 8 | Forfaitair rendement: rendementsgrondslag x weighted % | EUR [amount] |
| 9 | Box 3 tax: forfaitair rendement x 36% | EUR [amount] |

### Actual return (werkelijk rendement) data collection

[Collect the following data for the actual return comparison. If data is not available, note the gap.]

| Income type | Amount 2025 | Evidence | Status |
|-------------|------------|----------|--------|
| Interest received (bank accounts) | EUR [amount] | [evidence_id] | [collected / missing] |
| Dividends received (before withholding tax) | EUR [amount] | [evidence_id] | [collected / missing] |
| Rental income (net of attributable costs) | EUR [amount] | [evidence_id] | [collected / missing] |
| Realized capital gains/losses | EUR [amount] | [evidence_id] | [collected / missing] |
| Unrealized value changes (listed securities) | EUR [amount] | [evidence_id] | [collected / missing] |
| Deductible costs (custody, transaction fees) | EUR [amount] | [evidence_id] | [collected / missing] |
| **Total actual return** | **EUR [amount]** | | |

[If all data is missing: "Actual return data not yet available. The fictitious method will apply by default. To evaluate the actual return option, provide the data listed above."]

### Comparison: fictitious vs actual

| Method | Box 3 income | Box 3 tax (at 36%) | Data status |
|--------|-------------|-------------------|-------------|
| Fictitious return (forfaitair rendement) | EUR [amount] | EUR [amount] | Complete |
| Actual return (werkelijk rendement) | EUR [amount] | EUR [amount] | [Complete / Partial / Missing] |

More favorable method: [fictitious / actual / cannot determine -- data incomplete]

Note: The final election between fictitious and actual return is made in the official Mijn Belastingdienst filing environment. This comparison is informational only and does not constitute a binding election.

### Partner allocation for box 3

[If no fiscal partner: "Not applicable -- no fiscal partner."]

[If fiscal partner:]

| Allocation | Taxpayer share | Partner share | Combined box 3 tax |
|------------|---------------|--------------|-------------------|
| Default (50/50) | EUR [amount] | EUR [amount] | EUR [amount] |
| Optimized ([X]% / [Y]%) | EUR [amount] | EUR [amount] | EUR [amount] |

Recommended allocation: [percentage split] -- results in EUR [amount] lower combined box 3 tax.

Note: The allocation percentage applies to the entire box 3 base (assets minus debts). Partners cannot allocate asset-by-asset. Both partners must use the same ratio in their respective returns.

## Deductions notes

### Alimentatie

[If not applicable: "Not applicable -- no partneralimentatie payments."]

- Total partneralimentatie paid in 2025: EUR [amount]
- Evidence: [evidence_id]
- Basis: [court order / divorce agreement / notarial deed]

Note: Kinderalimentatie (child maintenance) is NOT deductible.

### Zorgkosten (specific medical expenses)

[If not applicable: "Not applicable -- no qualifying medical expenses claimed."]

| Expense type | Gross amount | Reimbursed by insurance | Net qualifying amount | Evidence |
|-------------|-------------|------------------------|----------------------|----------|
| [type] | EUR [amount] | EUR [amount] | EUR [amount] | [evidence_id] |

- Total qualifying expenses: EUR [amount]
- Drempelinkomen (combined): EUR [amount]
- Drempel (threshold): EUR [amount] (approximately 1.65% of drempelinkomen)
- **Deductible zorgkosten (above drempel):** EUR [amount]

### Giften (charitable donations)

[If not applicable: "Not applicable -- no charitable donations claimed."]

#### Periodieke giften

| Recipient (ANBI) | Annual amount | Agreement type | Evidence |
|-------------------|--------------|----------------|----------|
| [name] | EUR [amount] | [notarial deed / written agreement] | [evidence_id] |

Total periodieke giften: EUR [amount] (fully deductible, no threshold or cap)

#### Gewone giften (incidental)

| Recipient (ANBI) | Amount | Cultural ANBI | Evidence |
|-------------------|--------|--------------|----------|
| [name] | EUR [amount] | [yes/no] | [evidence_id] |

- Total gewone giften: EUR [amount]
- Cultural ANBI multiplier applied: EUR [amount] (1.25x, max EUR 1,250 additional)
- Drempel (1% of drempelinkomen, min EUR 60): EUR [amount]
- Cap (10% of drempelinkomen): EUR [amount]
- **Deductible gewone giften:** EUR [amount]

### Lijfrentepremie

[If not applicable: "Not applicable -- no lijfrentepremie claimed."]

- Premiums paid in 2025: EUR [amount]
- Provider: [name]
- Evidence: [evidence_id]
- Jaarruimte available: EUR [amount]
- Reserveringsruimte available: EUR [amount]
- **Deductible lijfrentepremie:** EUR [amount]

### Other deductions

[If not applicable: "Not applicable -- no other deductions claimed."]

| Deduction | Amount | Evidence |
|-----------|--------|----------|
| [e.g., restant persoonsgebonden aftrek prior years] | EUR [amount] | [evidence_id or assumption_id] |

### Deductions total

| Deduction category | Amount |
|-------------------|--------|
| Alimentatie | EUR [amount] |
| Zorgkosten (above drempel) | EUR [amount] |
| Giften (periodiek + gewoon) | EUR [amount] |
| Lijfrentepremie | EUR [amount] |
| Other | EUR [amount] |
| **Total persoonsgebonden aftrek** | **EUR [amount]** |

Allocation order: box 1 first, then box 3, then box 2.

## Fiscal partner notes

[If no fiscal partner: "Not applicable -- the taxpayer does not have a fiscal partner for tax year 2025."]

### Partner status

- Fiscal partner: [yes/no]
- Basis: [married / registered partnership / cohabiting with qualifying conditions]
- Partner for full year 2025: [yes/no]
- Special circumstances: [e.g., partner has no income, partner is AOW-age]

### Allocation options

The following items can be freely allocated between partners:

| Item | Default allocation | Optimized allocation | Tax impact |
|------|-------------------|---------------------|------------|
| Eigen woning result | 50/50 | [recommendation] | EUR [savings] |
| Box 3 grondslag | 50/50 | [recommendation] | EUR [savings] |
| Persoonsgebonden aftrek | [to higher-rate partner] | [recommendation] | EUR [savings] |

Items that CANNOT be allocated:
- Arbeidskorting (personal, based on individual arbeidsinkomen)
- Ondernemersaftrek (personal to the ondernemer)
- MKB-winstvrijstelling (personal to the ondernemer)

### Recommended review points

- [ ] Verify which partner has the higher marginal tax rate
- [ ] Consider tariefsaanpassing impact on eigen woning allocation
- [ ] Consider heffingskorting phase-out impact on income allocation
- [ ] Review box 3 allocation for optimal combined result
- [ ] Confirm both partners will use the same box 3 allocation ratio

## Field map summary

The field map for this workpack is available at:
`workspace/annual/2025/field-map.yaml`

This field map maps each line item in this workpack to the corresponding field in the Belastingdienst online return. Use it as a guide when entering data in Mijn Belastingdienst.

Note: This field map is specific to the annual return 2025. It is separate from any provisional assessment field maps.

## Missing information

[From workspace/shared/missing-info.md, filtered for annual_2025]

### Critical (blocks accurate filing)

| ID | Description | How to resolve |
|----|-------------|---------------|
| [MI-001] | [description] | [resolution guidance] |

### Important (affects accuracy)

| ID | Description | How to resolve |
|----|-------------|---------------|
| [MI-002] | [description] | [resolution guidance] |

### Nice-to-have (minor impact)

| ID | Description | How to resolve |
|----|-------------|---------------|
| [MI-003] | [description] | [resolution guidance] |

Total missing items: [count]

## Assumptions

[From workspace/shared/assumptions.md, filtered for annual_2025]

| Assumption ID | Description | Impact if incorrect | Resolution |
|---------------|-------------|--------------------| -----------|
| [A001] | [what was assumed] | [what changes if wrong] | [how to confirm] |

Total assumptions: [count]

## Human review checklist

Before filing through Mijn Belastingdienst, review the following:

- [ ] All income sources accounted for -- compare with VIA pre-filled data
- [ ] Evidence matches reported amounts -- no unexplained discrepancies
- [ ] Box 3 peildatum values verified against bank/broker statements
- [ ] Box 3 method choice reviewed (fictitious vs actual return)
- [ ] Partner allocation reviewed and agreed with fiscal partner
- [ ] Deductions have supporting evidence retained for at least 5 years
- [ ] All assumptions reviewed and confirmed or corrected
- [ ] Missing information resolved or consciously accepted
- [ ] WOZ-waarde matches the gemeente beschikking
- [ ] Mortgage interest matches the jaaroverzicht hypotheek
- [ ] Loonheffing withheld matches jaaropgaven total
- [ ] Filing deadline verified (standard: 1 May 2026; with uitstel: 1 September 2026)

## Not submission advice

This workpack is a preparation aid. It does not constitute tax advice, does not file your return, and does not interact with the Belastingdienst. You must review all information and submit through the official Mijn Belastingdienst portal using your DigiD. Do not share DigiD credentials with this tool.

To file your return:
1. Log in at mijn.belastingdienst.nl with your DigiD
2. Check the pre-filled data (vooringevulde aangifte) against this workpack
3. Add or correct information as identified in this workpack
4. Review the calculated result, sign, and submit

If someone else is helping you file, they must be authorized through DigiD Machtigen. This tool does not act as your representative and cannot log in, sign, or submit on your behalf.
