# Annual Return Workpack Generation Flow

Detailed step-by-step flow for generating the 2025 annual income-tax return workpack. Each phase builds on the previous one. If a phase cannot be completed due to missing data, record the gap and proceed to the next phase.

---

## Phase 1 — Pre-flight checks

Before generating any workpack content, verify that all prerequisites are met.

### 1.1 Profile exists

- Read `workspace/taxpayer/profile.yaml`
- Confirm the file exists and is parseable
- If missing: stop and instruct the user to run the intake skill first

### 1.2 Workflow confirmation

- Confirm `workflow_candidate: annual_2025` in the profile
- If the workflow is provisional, stopzetten, or unsupported: stop and explain the mismatch
- If the workflow is not set: stop and instruct the user to complete intake

### 1.3 Residency confirmed

- Confirm full-year Dutch residency for 2025
- Check for `residency: full_year_nl` or equivalent in the profile
- If part-year or non-resident: stop -- this is an unsupported case (see unsupported-cases.md)

### 1.4 Taxpayer type confirmed

- Confirm the taxpayer is an individual with employment/pension/benefit income as primary
- If IB-onderneming is the primary income source: stop -- unsupported case
- Minor side business alongside employment may still be in scope -- assess and note

### 1.5 Living taxpayer confirmed

- Confirm the return is not for a deceased person
- If F-biljet scenario: stop -- unsupported case

### 1.6 No M-biljet required

- Confirm no immigration or emigration during 2025
- If M-biljet is required: stop -- unsupported case

### 1.7 Evidence index exists

- Read `workspace/taxpayer/evidence-index.yaml`
- If missing: warn the user that no evidence has been indexed -- the workpack will contain more gaps
- If partially indexed: proceed but flag uncovered categories

### 1.8 Knowledge files available

- Verify that the annual 2025 knowledge directory exists and contains expected files
- Read all files under `${CLAUDE_SKILL_DIR}/../_shared/knowledge/years/2025/annual/`
- Read all files under `${CLAUDE_SKILL_DIR}/../_shared/knowledge/years/2025/box3/`
- Read security knowledge: `digid.md`, `prompt-injection.md`

---

## Phase 2 — Income compilation

Compile all box 1 income from evidence and user-provided data.

### 2.1 Employment income (loon uit dienstbetrekking)

- Match jaaropgaaf evidence items from the evidence index
- For each employer: extract gross salary, loonheffing withheld, and employer name
- Flag if multiple employers are present (may affect tax calculation)
- Flag if any jaaropgaaf has low classification confidence or is marked for review
- If no jaaropgaaf is available but the profile indicates employment: add to missing info

### 2.2 Pension income

- Match pension jaaroverzicht evidence items
- For each pension provider: extract gross pension, loonheffing withheld
- Distinguish between employer pension (pensioenuitkering) and AOW (from SVB)
- Note whether the taxpayer is at or above AOW age (affects tax rates and credits)

### 2.3 Benefit income (uitkeringen)

- Match UWV and SVB jaaropgaven evidence items
- Identify benefit type: WW, WIA/WAO, ZW, Anw, AKW
- Extract gross benefit amount and loonheffing withheld
- Note that benefit income qualifies for the algemene heffingskorting but NOT the arbeidskorting

### 2.4 Other box 1 income

- Check for income from other activities (resultaat uit overige werkzaamheden)
- Check for alimentatie received (taxable as box 1 income)
- Check for any other income sources mentioned in the profile or evidence

### 2.5 Income summary

- Total all box 1 income sources
- Total all loonheffing withheld (this determines whether the taxpayer gets a refund or owes additional tax)
- Note any income items without supporting evidence

---

## Phase 3 — Own-home compilation

Compile the eigen woning section if applicable.

### 3.1 Determine own-home status

- Check the profile for property ownership
- If no own home: skip this phase and note "geen eigen woning" in the workpack

### 3.2 WOZ-waarde

- Extract from WOZ-beschikking evidence item
- The 2025 return uses the WOZ-waarde with waardepeildatum 1 January 2024
- If WOZ-beschikking is not in evidence: add to missing info
- If the taxpayer filed a bezwaar (objection): use the corrected value

### 3.3 Mortgage interest (hypotheekrente)

- Extract from jaaroverzicht hypotheek evidence item
- Record total deductible interest paid during 2025
- Check mortgage type: annuitair/lineair (post-2013) or aflossingsvrij (pre-2013 transitional)
- Verify the mortgage qualifies for deduction (purchased, improved, or maintained the eigen woning)
- Record outstanding mortgage balance as of 31 December 2025

### 3.4 Eigenwoningforfait calculation

- Apply the rate from `own-home.md` based on the WOZ-waarde bracket
- Most common: 0.35% for WOZ between EUR 75,000 and EUR 1,310,000
- Show the calculation explicitly (WOZ-waarde * percentage)

### 3.5 Tariefsaanpassing

- If the taxpayer's box 1 income falls in schijf 3 (above EUR 76,817):
  - Calculate the portion of mortgage interest deduction that falls in schijf 3
  - The effective deduction rate is capped at 37.48%
  - Calculate the tariefsaanpassing amount (difference between 49.50% and 37.48%)
- If income is below schijf 3: no tariefsaanpassing applies

### 3.6 Hillenregeling

- If the eigenwoningforfait exceeds the mortgage interest paid:
  - Apply the Hillenregeling correction (76.67% in 2025, year 7 of phase-out)
  - The correction reduces the net positive eigenwoningforfait
- If mortgage interest exceeds eigenwoningforfait: Hillenregeling does not apply

### 3.7 Net own-home result

- Net result = eigenwoningforfait minus mortgage interest (typically negative / a deduction)
- Adjusted for tariefsaanpassing and Hillenregeling if applicable
- This amount is added to box 1 income

### 3.8 Partner handling for own home

- If fiscal partners co-own the property: allocate based on ownership shares (typically 50/50)
- Note that the net eigen woning result can be allocated differently for tax optimization
- Both partners must report their share in their individual return

---

## Phase 4 — Box 3 compilation

Compile savings and investment data for box 3. BOTH methods must be covered.

### 4.1 Assets on peildatum 1 January 2025

Collect values for each asset category:

#### Banktegoeden (category I)
- All savings accounts, current accounts, deposits, term deposits
- Source: bank statements or jaaropgaven with balance on 1 January 2025
- Match against evidence index items classified as bankafschrift or jaaropgaaf-bank

#### Overige bezittingen (category II)
- Investment portfolios (listed securities, mutual funds)
- Crypto-assets (valued at market price on 1 January 2025)
- Real estate not being the eigen woning (second homes, rental property)
- Receivables (vorderingen) -- loans to others
- Other assets
- Source: portfolio year-end statements, crypto exchange statements

#### Schulden (category III)
- All debts EXCEPT mortgage debt on the eigen woning
- Consumer loans, student debt, other liabilities
- Note the debt threshold below which debts are not deductible

### 4.2 Assets on 31 December 2025

- Collect values for the same categories on 31 December 2025
- These are needed for the actual return calculation (mark-to-market)
- For the fictitious return, only the 1 January 2025 values are used

### 4.3 Fictitious return calculation

Follow the calculation method from `fictitious.md`:
1. Total per category on 1 January 2025
2. Calculate weighted fictitious return percentage
3. Determine rendementsgrondslag (total assets minus debts minus heffingsvrij vermogen)
4. Calculate forfaitair rendement = rendementsgrondslag * weighted percentage
5. Calculate box 3 tax = forfaitair rendement * 36%

Common failure: do NOT apply heffingsvrij vermogen before calculating the weighted percentage.

### 4.4 Actual return data collection

Follow the data requirements from `actual-return.md`:
1. Actual interest received on bank accounts during 2025
2. Dividends received (before dividend withholding tax)
3. Rental income (net of directly attributable costs)
4. Realized capital gains and losses
5. Unrealized value changes (mark-to-market for listed securities)
6. Deductible costs (custody fees, transaction costs)

If the taxpayer cannot provide actual return data: note that the fictitious method will apply by default.

### 4.5 Comparison: fictitious vs actual

- Present both calculations side by side
- Note which method results in lower box 3 tax
- Add a note that the final election is made in the official filing environment
- The workpack does not make a binding election

### 4.6 Partner allocation for box 3

- If fiscal partners: box 3 assets and debts can be freely allocated (0%-100%)
- The allocation applies to the ENTIRE box 3 base (not asset-by-asset)
- Both partners must use the same allocation ratio
- Compute the optimal split that minimizes combined box 3 tax
- Present the default (50/50) and the optimized allocation

---

## Phase 5 — Deductions compilation

Compile all deductible items from evidence and user-provided data.

### 5.1 Alimentatie

- Check for partneralimentatie payments (deductible)
- Verify: kinderalimentatie is NOT deductible -- flag if the user attempts to claim it
- Evidence: court order or divorce agreement, plus bank statements showing payments
- Record: total annual amount, evidence_id, assumption_id if amount is estimated

### 5.2 Specifieke zorgkosten (medical expenses)

- Collect qualifying medical expenses not reimbursed by insurance
- Apply the drempel (income-dependent threshold, approximately 1.65% of drempelinkomen)
- Drempelinkomen = combined income of both partners before persoonsgebonden aftrek
- Only the amount above the drempel is deductible
- Note the multiplier for certain specific zorgkosten categories
- Evidence: receipts, insurance reimbursement statements

### 5.3 Giften (charitable donations)

- Distinguish between periodieke giften (no threshold, no cap) and gewone giften (with threshold and cap)
- Periodieke giften: verify notarial deed or written agreement for 5+ years
- Gewone giften: threshold 1% of drempelinkomen (min EUR 60), cap 10% of drempelinkomen
- Cultural ANBI multiplier: 1.25x up to EUR 1,250 additional
- Verify ANBI registration of recipient organizations
- Evidence: receipts, bank statements, ANBI registration confirmation

### 5.4 Lijfrentepremie (annuity premium)

- Collect premiums paid for lijfrente products
- Calculate jaarruimte based on employment income and pension accrual (factor A)
- Check reserveringsruimte from unused jaarruimte of prior 7 years
- Evidence: annual statement from lijfrente provider, factor A statement from employer

### 5.5 Other deductions

- Studiekosten / scholingsuitgaven (if still deductible for 2025)
- Restant persoonsgebonden aftrek from prior years
- Any other qualifying deductions from the profile or evidence

### 5.6 Deduction summary

- Total persoonsgebonden aftrek
- Note the allocation order: box 1 first, then box 3, then box 2
- If fiscal partners: note allocation options (allocate to highest marginal rate)

---

## Phase 6 — Partner handling

If the taxpayer has a fiscal partner, compile the partner section.

### 6.1 Partner status confirmation

- Confirm fiscal partner status on 31 December 2025 (or qualifying part-year partnership)
- Married, registered partnership, or cohabiting with qualifying conditions

### 6.2 Allocatable items

List all items that can be freely allocated between partners:
- Eigen woning result (net forfait minus interest)
- Box 3 grondslag (assets minus debts)
- Persoonsgebonden aftrek components (alimentatie, zorgkosten, giften, etc.)

### 6.3 Non-allocatable items

List items that are personal and cannot be allocated:
- Arbeidskorting (based on individual arbeidsinkomen)
- Ondernemersaftrek (personal to the ondernemer)
- MKB-winstvrijstelling (personal to the ondernemer)

### 6.4 Allocation recommendations

- Identify the partner with the higher marginal tax rate
- Recommend allocating deductions to the higher-rate partner
- Consider the tariefsaanpassing for eigen woning (37.48% cap)
- Consider the phase-out of heffingskortingen
- Present at least the default and one optimized allocation for review

---

## Phase 7 — Field map generation

### 7.1 Generate field map

Map each workpack line item to the corresponding field or section in the Belastingdienst online return form. Write to `workspace/annual/2025/field-map.yaml`.

### 7.2 Separation from provisional

The annual field map must be entirely separate from any provisional field maps. Do not reference or reuse provisional-2026 field mappings.

---

## Phase 8 — Missing info compilation

### 8.1 Collect all gaps

Review every section for data gaps:
- Income sources without evidence
- Asset values without bank statements
- Deduction claims without receipts
- Profile information that was assumed rather than confirmed

### 8.2 Write missing info

Write or update `workspace/shared/missing-info.md`:
- Each item tagged with `workflow: annual_2025`
- Each item has a priority: critical (blocks filing), important (affects accuracy), nice-to-have
- Each item describes what is needed and where the taxpayer can obtain it

---

## Phase 9 — Review question generation

### 9.1 Generate review questions

Create questions for each area of uncertainty:
- "Can you confirm the WOZ-waarde on your beschikking is EUR [amount]?"
- "Did you receive any income from other sources not yet mentioned?"
- "Do you have the actual interest statements from your bank for 2025?"

### 9.2 Prioritize questions

Order questions by impact on the return:
1. Items that affect whether filing is possible
2. Items that affect the tax amount significantly
3. Items that affect accuracy but have smaller impact

---

## Phase 10 — Workpack assembly

### 10.1 Use the template

Read the template from `templates/annual-return-pack.md`. Fill in every section with the data compiled in phases 2-9.

### 10.2 Validate against the output contract

Check the completed workpack against `reference/annual-output-contract.md`:
- All required sections present
- All amounts have source attribution
- All assumptions listed
- Both box 3 methods covered
- "Not submission advice" section present
- No provisional-2026 wording present

### 10.3 Write the workpack

Write the completed workpack to `workspace/annual/2025/return-pack.md`.

### 10.4 Summary to user

After writing:
- Confirm the workpack location
- Report the count of missing information items
- Report the count of assumptions made
- Remind the user to review the human review checklist
- Remind the user that filing happens through Mijn Belastingdienst with their DigiD
