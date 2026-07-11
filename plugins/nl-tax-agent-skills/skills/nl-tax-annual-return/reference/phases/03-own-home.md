## Phase 3 — Own-home compilation

Compile the eigen woning section if applicable.

### 3.1 Determine own-home status

- Check the profile for property ownership
- If no own home: skip this phase and note "geen eigen woning" in the workpack

### 3.2 WOZ-waarde

- Extract from WOZ-beschikking evidence item
- The 2025 return uses the WOZ-waarde with waardepeildatum 1 January 2024
- If WOZ-beschikking is not in evidence: ask the user for the value (subsection becomes `chat_only`) or mark missing
- If the taxpayer filed a bezwaar (objection): use the corrected value

### 3.3 Mortgage interest (hypotheekrente)

- Extract from jaaroverzicht hypotheek evidence item
- Record mortgage interest paid during 2025
- Itemize qualifying one-off financing costs and periodic erfpacht, opstal, or beklemming payments
- Set `total_deductible_own_home_costs` to mortgage interest plus qualifying financing costs plus periodic erfpacht/opstal/beklemming; do not use mortgage interest alone for Hillen
- Check mortgage type: annuitair/lineair (post-2013) or aflossingsvrij (pre-2013 transitional)
- Verify the mortgage qualifies for deduction (purchased, improved, or maintained the eigen woning)
- Record outstanding mortgage balance as of 31 December 2025

### 3.4 Tijdelijke twee woningen (verkoopregeling / aankoopregeling)

One ordinary main residence may receive a review estimate. Two homes, sale/purchase overlap, temporary double-home deductions, divorce use, and other complex cases must collect facts and route to manual review. Collect the move and registration dates, both addresses, WOZ evidence, mortgage statements, sale/listing and vacancy/rental status, expected occupancy, and any divorce-use arrangement; do not calculate or present a standard filing result for these cases.

### 3.5 Eigenwoningforfait calculation

- Apply the rate from `_shared/knowledge/own-home/eigenwoningforfait.md` based on the WOZ-waarde bracket — that file is canonical for the bracket table (the common middle bracket and its rate included)
- Show the calculation explicitly (WOZ-waarde * percentage)

### 3.6 Tariefsaanpassing

- Treat `tariefsaanpassing` as a separate tax-benefit adjustment; it is never part of `box1_own_home_balance` and is not added to taxable Box 1 income.
- If the taxpayer's box 1 income falls in the top bracket (threshold per `_shared/knowledge/years/2025/annual/box1-rates.md`):
  - Calculate the portion of deductible own-home costs that falls in the top bracket
  - Cap the effective deduction rate at the 2025 deduction-rate cap from `_shared/knowledge/years/2025/annual/deductions.md` (bd_own_home_deduction_cap_2025 / bd_deduction_rate_cap_2025)
  - Calculate the tariefsaanpassing amount (difference between the top bracket rate and the capped deduction rate)
- If income is below the top bracket: no tariefsaanpassing applies

### 3.7 Hillenregeling

- If the eigenwoningforfait exceeds `total_deductible_own_home_costs`:
  - Apply the Hillenregeling correction using the 2025 percentage from `_shared/knowledge/own-home/eigenwoningforfait.md`
  - The correction reduces the net positive eigenwoningforfait
- If total deductible own-home costs equal or exceed eigenwoningforfait: Hillenregeling does not apply

### 3.8 Net own-home result

- `box1_own_home_balance = eigenwoningforfait - total_deductible_own_home_costs - hillen_deduction`
- `total_deductible_own_home_costs` includes mortgage interest, qualifying financing costs, and periodic erfpacht, opstal, or beklemming.
- Total deductible own-home costs include mortgage interest, qualifying financing costs, and periodic erfpacht, opstal, or beklemming.
- Use the verified optional helper fields `total_deductible_own_home_costs`, `hillen_deduction`, and `box1_own_home_balance` when available. Otherwise the agent derives the review estimate from cited evidence and records missing or uncertain qualification facts for manual review.
- Add only `box1_own_home_balance` to taxable Box 1 income. Tariefsaanpassing is separate from box1_own_home_balance: keep it in a separate review table as a tax-benefit adjustment.

### 3.9 Partner handling for own home

- If fiscal partners co-own the property: allocate based on ownership shares (typically 50/50)
- Note that the net eigen woning result can be allocated differently for tax optimization
- Both partners must report their share in their individual return

---
