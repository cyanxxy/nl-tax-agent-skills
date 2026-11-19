## Own-home notes

[If no own home: "Not applicable -- the taxpayer does not own a primary residence. Skip to Box 2 notes."]

One ordinary main residence may receive a review estimate. Two homes, sale/purchase overlap, temporary double-home deductions, divorce use, and other complex cases must collect facts and route to manual review. For those cases list the collected dates, addresses, use, occupancy, listing/rental status, WOZ evidence, and mortgage evidence; do not complete the standard calculation below.

### WOZ-waarde

- WOZ-waarde (waardepeildatum 1 January 2024): EUR [amount] -- Src: [F/U/A/?]
- Bezwaar filed: [yes/no] -- Src: [F/U/A/?]

### Deductible own-home costs

- Mortgage interest paid in 2025: EUR [amount] -- Src: [F/U/A/?]
- Qualifying financing costs paid in 2025: EUR [amount] -- Src: [F/U/A/?]
- Periodic erfpacht payments: EUR [amount] -- Src: [F/U/A/?]
- Periodic opstal payments: EUR [amount] -- Src: [F/U/A/?]
- Periodic beklemming payments: EUR [amount] -- Src: [F/U/A/?]
- `total_deductible_own_home_costs`: EUR [sum of mortgage interest, qualifying financing costs, and periodic erfpacht/opstal/beklemming] -- Src: C:cost-sum
- Mortgage type: [annuitair / lineair / aflossingsvrij (pre-2013)] -- Src: [F/U/A/?]
- Outstanding balance 31 December 2025: EUR [amount] -- Src: [F/U/A/?]
- Deduction qualification: [confirmed / requires review]

### Eigenwoningforfait

- WOZ-waarde bracket: EUR [lower] to EUR [upper]
- Applicable percentage: [percentage]%
- Eigenwoningforfait: EUR [WOZ-waarde] x [percentage]% = EUR [amount] -- Src: C:woz*pct

### Tariefsaanpassing

Tariefsaanpassing is separate from box1_own_home_balance: it is a tax-benefit adjustment and is never added to taxable Box 1 income.

[If taxpayer income is in the top bracket above [threshold from `box1-rates.md`]:]

- Portion of deductible own-home costs falling in schijf 3: EUR [amount] -- Src: C:...
- Tariefsaanpassing: EUR [amount] x ([top bracket rate from `box1-rates.md`] - [deduction-rate cap from `deductions.md`]) = EUR [amount] -- Src: C:...
- Effective deduction rate for this portion: [deduction-rate cap from `deductions.md`]

[If income is below schijf 3: "Not applicable -- income does not exceed the schijf 3 threshold."]

### Hillenregeling

[If eigenwoningforfait exceeds `total_deductible_own_home_costs`:]

- Excess eigenwoningforfait: EUR [eigenwoningforfait] - EUR [`total_deductible_own_home_costs`] = EUR [amount] -- Src: C:...
- Hillenregeling correction: EUR [amount] x [Hillen percentage from `own-home.md`] = EUR [amount] -- Src: C:...
- `hillen_deduction`: EUR [amount] -- Src: C:...

[If total deductible own-home costs equal or exceed eigenwoningforfait: "Not applicable -- total deductible own-home costs equal or exceed the eigenwoningforfait."]

### Net own-home result

| Item | Amount | Src |
|------|--------|-----|
| Eigenwoningforfait | EUR [amount] | C:above |
| Minus: `total_deductible_own_home_costs` | EUR [amount] | C:cost-sum |
| Minus: `hillen_deduction` (if applicable) | EUR [amount] | C:above |
| **`box1_own_home_balance`** | **EUR [amount]** | C:sum |

`box1_own_home_balance = eigenwoningforfait - total_deductible_own_home_costs - hillen_deduction`

[A negative balance reduces box 1 taxable income. Verify optional helper output against the cited evidence; if any cost qualification or complex-home fact is unresolved, preserve it as manual review.]

### Separate tax-benefit adjustment review

| Item | Amount | Src |
|------|--------|-----|
| Tariefsaanpassing (if applicable) | EUR [amount] | C:above |

[This review adjustment affects the tax benefit only and is not included in `box1_own_home_balance`.]
