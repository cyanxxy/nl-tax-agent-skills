# Annual Return Workpack Generation Flow

Authoritative step-by-step flow for generating the 2025 annual income-tax return workpack. Each phase builds on the previous one. If a phase cannot be completed due to missing data, record the gap and proceed to the next phase. `SKILL.md` is the entry-point procedure; this file is the contract for the ordered workflow.

Every time you read a knowledge file or rate sheet, record the matching `source_id` from `_shared/source-register.yaml` in `session-progress.yaml` → `sources_loaded` — once per ID; never append a duplicate on a re-read. Only IDs in that list may appear in the workpack's "Sources used" section, and that section lists each ID exactly once.

---

## Contents

- Phase 1 — Pre-flight checks
- Phase 1.5 — Filing status and late-filing exposure
- Phase 2 — Income compilation
- Phase 2A — Winst uit onderneming compilation
- Phase 3 — Own-home compilation
- Phase 3A — Box 2 compilation
- Phase 4 — Box 3 compilation
- Phase 5 — Deductions compilation
- Phase 5.5 — Credits screening
- Phase 6 — Partner handling
- Phase 7 — Field map generation
- Phase 8 — Missing info compilation
- Phase 9 — Review question generation
- Phase 10 — Workpack assembly

## Phase 1 — Pre-flight checks

Before generating any workpack content, verify all prerequisites are met.

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
- If part-year or non-resident: stop -- this is an unsupported case

### 1.4 Taxpayer type confirmed

- Confirm the taxpayer is an individual filing an income-tax return.
- **Winst uit onderneming (eenmanszaak / ZZP) is supported.** If the taxpayer is an IB-ondernemer with an eenmanszaak, set `business.has_onderneming: true` in the profile and prepare the winst in Phase 2A. This does not stop the flow.
- Route to manual review or unsupported (do not prepare a standard winst section) for the complex business forms outside standard scope: partnerships (VOF, maatschap, CV) and profit-share allocation, medegerechtigdheid, DGA/BV winst, agrarische ondernemingen (landbouwvrijstelling), zeevarenden, and business-cessation events (staking, herinvesteringsreserve, oudedagsreserve wind-down). These keep the blocked `annual_2025_entrepreneurs` candidate.
- Resultaat uit overige werkzaamheden is not winst uit onderneming: keep it as manual-review data (see Phase 2.4); do not calculate it as a standard entrepreneur case.

### 1.5 Living taxpayer confirmed

- Confirm the return is not for a deceased person
- If F-biljet scenario: stop -- unsupported case

### 1.6 No M-biljet required

- Confirm no immigration or emigration during 2025
- If M-biljet is required: stop -- unsupported case

### 1.7 Household composition

- Read `profile.yaml` → `person.date_of_birth`, `partner.partner_date_of_birth`, `household.children_at_home_count`, `household.children`, `household.single_parent_status`, `person.aow_age_in_tax_year`, `partner.partner_aow_age_in_tax_year`
- If any of these are missing or `source: unknown` and the workflow needs them for credits screening (Phase 5.5), ask the user to fill them in now, in one batch of up to 3 questions. Do not ask for BSNs; ask for dates of birth and a yes/no on single-parent status.
- Persist answers back to `profile.yaml` with `source: user_chat` and a stated_at date. Mark `sections.intake.subsections.household_composition.status: complete` in `session-progress.yaml`.

### 1.8 Evidence index exists

- Read `workspace/taxpayer/evidence-index.yaml`
- If missing: warn the user that no evidence has been indexed -- the workpack will contain more gaps
- If partially indexed: proceed but flag uncovered categories

### 1.9 Box 2 scope check

- Standard Box 2 preparation is supported for `annual_2025` when the taxpayer has an aanmerkelijk belang and the facts are straightforward.
- Keep the case in scope for regular benefits such as dividends, disposal benefits such as share-sale profit, dividend withholding tax credit, loss carry-forward fields, and fiscal-partner allocation of Box 2 income.
- Route to manual review or unsupported for valuation disputes, emigration, death, restructurings, treaty/nonresident issues, informal capital, non-arm's-length transfers, and corporate-tax-heavy DGA cases.

### 1.10 Knowledge files available

Load every file in this list and append its `source_id` to `session-progress.yaml` → `sources_loaded` as you go. If any fails to load, stop and tell the user; do not paraphrase rates from memory.

- `_shared/knowledge/years/2025/annual/box1-rates.md` *(bd_box1_rates_2025)*
- `_shared/knowledge/years/2025/annual/credits.md` *(bd_general_tax_credit_2025, bd_labour_tax_credit_2025, bd_tax_credit_payout_2025, bd_heffingskortingen_how_2025, bd_arbeidsinkomen_definition_2025)*
- `_shared/knowledge/years/2025/annual/own-home.md` *(bd_own_home_deduction_cap_2025)*
- `_shared/knowledge/years/2025/annual/deductions.md` *(bd_giften_aftrek_2025, bd_zorgkosten_overzicht_2025, bd_deduction_rate_cap_2025)*
- `_shared/knowledge/years/2025/annual/late-filing.md` *(bd_verzuimboete, bd_belastingrente_overview, bd_belastingrente_ib, bd_invorderingsrente)*
- `_shared/knowledge/years/2025/annual/filing-flow.md` *(bd_annual_return_landing_2025, bd_annual_return_4_steps_2025, bd_annual_deadline_2025, bd_annual_extension_2025)*
- `_shared/knowledge/years/2025/annual/evidence-checklist.md` *(bd_annual_data_checklist_2025)*
- `_shared/knowledge/years/2025/entrepreneur/ondernemer-criteria.md` *(bd_ondernemer_criteria_2025, bd_ondernemerscheck_2025, bd_urencriterium_2025)* — only when the case has winst uit onderneming (`business.has_onderneming` value `true`)
- `_shared/knowledge/years/2025/entrepreneur/ondernemersaftrek.md` *(bd_ondernemersaftrek_2025, bd_zelfstandigenaftrek_2025, bd_startersaftrek_ao_2025, bd_startersaftrek_2025, bd_meewerkaftrek_2025, bd_stakingsaftrek_2025, bd_so_aftrek_2025)* — same condition
- `_shared/knowledge/years/2025/entrepreneur/mkb-winstvrijstelling.md` *(bd_mkb_winstvrijstelling_2025)* — same condition
- `_shared/knowledge/years/2025/entrepreneur/investeringsaftrek.md` *(bd_kia_2025, bd_eia_2025, bd_eia_mia_vamil_2025)* — same condition
- `_shared/knowledge/years/2025/entrepreneur/winst-en-kosten.md` *(bd_zakelijke_kosten_2025, bd_beperkt_aftrekbare_kosten_2025, bd_werkruimte_2025, bd_privevervoermiddel_2025, bd_oudedagsreserve_2025, bd_administratie_bewaren_2025)* — same condition
- `_shared/knowledge/years/2025/entrepreneur/entrepreneur-aangifte.md` *(bd_aangifte_ondernemers_2025, bd_ondernemer_cijfers_aangifte_2025, bd_ondernemer_voorbereiden_2025)* — same condition
- `_shared/knowledge/years/2025/box3/fictitious.md` *(bd_box3_2025_calc, bd_fisin_box3_assets_debts_2025)*
- `_shared/knowledge/years/2025/box3/actual-return.md` *(bd_box3_2025_actual_return, bd_fisin_box3_actual_return_2025)*
- `_shared/knowledge/years/2025/box2/box2-rates.md` *(bd_box2_rates_2025_2026)* — only when the case has an aanmerkelijk belang (`box2.has_aanmerkelijk_belang` value `true`)
- `_shared/knowledge/years/2025/box2/box2-income-guidance.md` *(bd_box2_income_ab_guidance)* — same condition
- `_shared/knowledge/years/2025/box2/fisin-aanmerkelijk-belang.md` *(bd_fisin_aanmerkelijk_belang_2025)* — same condition
- `_shared/knowledge/own-home/eigenwoningforfait.md` *(bd_eigenwoningforfait_2025_2026, bd_eigenwoningforfait_multiple_homes)*
- `_shared/knowledge/own-home/hypotheekrenteaftrek.md` *(bd_hypotheekrenteaftrek_conditions, bd_own_home_deductible_costs, bd_temporary_two_homes_interest)*
- `_shared/knowledge/partners/fiscal-partnership.md` *(bd_fiscal_partnership)*

---

## Phase 1.5 — Filing status and late-filing exposure

Before compiling income, establish where the taxpayer stands on the 1 May 2026 deadline. This drives whether the workpack carries a top-level exposure section (see output contract § Filing status).

### 1.5.1 Determine filing status

Ask the user (one batch, at most 3 questions):

1. Have you already filed the 2025 return? (yes / no)
2. Did you receive uitstel before 1 May 2026? (yes / no — if yes, what is the granted uitsteldatum?)
3. If not filed and no uitstel — when do you plan to file?

Record under `workspace/annual/2025/notes/filing-status.yaml` with `source: user_chat`.

### 1.5.2 Surface exposure

- **On time** (filed before 1 May 2026, or before granted uitsteldatum): no exposure. The workpack will say "Filing status: on time."
- **Uitstel granted, return outstanding**: quote the uitsteldatum and note that belastingrente still accrues from 1 July 2026 if tax is owed. Use the rate from `late-filing.md` (5% from 1 January 2026).
- **Late (deadline passed, no uitstel)**: surface the verzuimboete (EUR 469 first / EUR 6,709 max) and the belastingrente rate (5% from 1 January 2026). Recommend filing as soon as possible to shorten the belastingrente period; pay the eventual aanslag by its betaaltermijn to avoid invorderingsrente. Do not imply that paying the aanslag faster reduces belastingrente — that end date is fixed when the aanslag is issued. Cite `bd_verzuimboete` and `bd_belastingrente_overview`.

Do not compute a final boete or rente amount; the Belastingdienst sets these on the aanslag.

---

## Phase 2 — Income compilation

Compile all box 1 income from evidence and user-provided data.

### 2.1 Employment income (loon uit dienstbetrekking)

- Match jaaropgaaf evidence items from the evidence index
- For each employer: extract gross salary, loonheffing withheld, and employer name
- Flag if multiple employers are present (may affect tax calculation)
- Flag if any jaaropgaaf has low classification confidence or is marked for review
- If no jaaropgaaf is available but the profile indicates employment: ask for the values in chat (subsection then becomes `chat_only`) or mark the item as missing if the user defers

### 2.2 Pension income

- Match pension jaaroverzicht evidence items
- For each pension provider: extract gross pension, loonheffing withheld
- Distinguish between employer pension (pensioenuitkering) and AOW (from SVB)
- Note whether the taxpayer is at or above AOW age (affects tax rates and credits) — use `profile.yaml` → `person.aow_age_in_tax_year`

### 2.3 Benefit income (uitkeringen)

- Match UWV and SVB jaaropgaven evidence items
- Identify benefit type: WW, WIA/WAO, ZW, Anw, AKW
- Extract gross benefit amount and loonheffing withheld
- Note that benefit income qualifies for the algemene heffingskorting but NOT the arbeidskorting

### 2.4 Other box 1 income

- Check for **winst uit onderneming** (eenmanszaak / ZZP). If present, set `business.has_onderneming: true` and prepare it in Phase 2A, not here. Distinguish it from resultaat uit overige werkzaamheden: winst uit onderneming is the ondernemer case; resultaat uit overige werkzaamheden is the residual freelance case.
- Check for income from other activities (resultaat uit overige werkzaamheden) and record it as manual-review data; do not calculate or map it as standard Box 1 support without reviewed sources.
- Check for alimentatie received (taxable as box 1 income) and route to manual review unless exact reviewed sources and field-map support have been added.
- Check for any other income sources mentioned in the profile or evidence and keep them out of standard calculations until source-backed.

### 2.5 Income summary

- Total all box 1 income sources (the winst uit onderneming total from Phase 2A feeds this once it is prepared)
- Total all loonheffing withheld (this determines whether the taxpayer gets a refund or owes additional tax)
- Note any income items without supporting evidence

---

## Phase 2A — Winst uit onderneming compilation

Compile standard winst uit onderneming for the annual 2025 return when the taxpayer is an IB-ondernemer with an eenmanszaak (the usual ZZP legal form). If the taxpayer has no onderneming, emit the canonical "not applicable" line from the output contract and continue.

When the taxpayer has winst uit onderneming, invoke or inline `nl-tax-winst`, read the amounts from the entrepreneur knowledge notes under `_shared/knowledge/years/2025/entrepreneur/` — never paraphrase a rate, amount, or threshold from memory — and append the entrepreneur `source_id`s to `session-progress.yaml` → `sources_loaded` as their notes are loaded (this skill owns session state; the helper does not).

### 2A.1 Ondernemer status and urencriterium

- Confirm the taxpayer is an ondernemer voor de inkomstenbelasting with an eenmanszaak; a KvK registration or btw-ondernemerschap alone is not enough (see `ondernemer-criteria.md`).
- Record `business.has_onderneming` as `true`/`false` in the profile (the template's boolean enum); route to manual review when the status is unclear or when the income looks like resultaat uit overige werkzaamheden.
- Record whether the urencriterium (or, for the startersaftrek bij arbeidsongeschiktheid, the verlaagd urencriterium) is met; it gates the zelfstandigenaftrek and related components.

### 2A.2 Winst uit onderneming

- Collect turnover (omzet), total deductible business costs, and qualifying KIA investments. Apply the kleinschaligheidsinvesteringsaftrek from `investeringsaftrek.md` as an investeringsaftrek that reduces the winst before ondernemersaftrek.
- Apply the beperkt-aftrekbare-kosten threshold or the alternative percentage election (never both), and note werkruimte, business-car bijtelling, and the private-vehicle kilometre deduction where they apply, from `winst-en-kosten.md`.
- Map:
  - `onderneming.omzet`
  - `onderneming.kosten`
  - `onderneming.kleinschaligheidsinvesteringsaftrek`
  - `onderneming.winst_voor_ondernemersaftrek`

### 2A.3 Ondernemersaftrek

- Prepare only the components the case qualifies for: zelfstandigenaftrek (plus the startersaftrek increase where the starter conditions are met), aftrek voor speur- en ontwikkelingswerk, meewerkaftrek, and the startersaftrek bij arbeidsongeschiktheid. Read the 2025 amounts and conditions from `ondernemersaftrek.md`.
- Map:
  - `onderneming.zelfstandigenaftrek`
  - `onderneming.startersaftrek`
  - `onderneming.ondernemersaftrek_totaal`

### 2A.4 MKB-winstvrijstelling and belastbare winst

- Apply the MKB-winstvrijstelling to the winst after investeringsaftrek and ondernemersaftrek (`mkb-winstvrijstelling.md`).
- Map:
  - `onderneming.mkb_winstvrijstelling`
  - `onderneming.belastbare_winst`

### 2A.5 Manual-review triggers

- Require manual review for partnerships (VOF, maatschap, CV) and profit-share allocation, medegerechtigdheid, DGA/BV winst, agrarische ondernemingen, zeevarenden, staking/cessation events, herinvesteringsreserve, oudedagsreserve wind-down, and resultaat uit overige werkzaamheden.
- Do not calculate these complex positions; record the facts and ask for professional review. The MKB-winstvrijstelling and ondernemersaftrek are personal to the ondernemer and are not allocated between fiscal partners (see Phase 6.3).

---

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
- Record total deductible interest paid during 2025
- Check mortgage type: annuitair/lineair (post-2013) or aflossingsvrij (pre-2013 transitional)
- Verify the mortgage qualifies for deduction (purchased, improved, or maintained the eigen woning)
- Record outstanding mortgage balance as of 31 December 2025

### 3.4 Tijdelijke twee woningen (verkoopregeling / aankoopregeling)

If the taxpayer had two homes during 2025 (sold/bought in-year, or owns the new home and the old home has not sold):

- Read the "Temporarily two homes" section of `_shared/knowledge/own-home/hypotheekrenteaftrek.md` and apply the verkoopregeling and/or aankoopregeling.
- The verkoopregeling keeps interest on the **old** home deductible for **the year of moving plus the 3 subsequent calendar years**, provided the home is empty, for sale, not rented out, and was the hoofdverblijf in the year of moving or in one of the 3 preceding years.
- The aankoopregeling keeps interest on the **new** home deductible before occupancy, provided the home is empty or under construction and the taxpayer will live there in the same year or within the 3 calendar years that follow.
- Collect, in a single batch of up to 6 questions: move date, old-home address + WOZ + mortgage statement, new-home address + WOZ + mortgage statement, vacancy/listing status of the old home.
- Compute the deduction window endpoints in absolute dates and record them in the workpack ("interest on [old address] is deductible through 31 December [year + 3]").
- Only route to manual review when a condition is genuinely ambiguous (partial-year letting, undocumented hoofdverblijf history, treaty/nonresident facts). A clean overlap that satisfies the conditions does NOT need manual review.

### 3.5 Eigenwoningforfait calculation

- Apply the rate from `_shared/knowledge/own-home/eigenwoningforfait.md` based on the WOZ-waarde bracket — that file is canonical for the bracket table (the common middle bracket and its rate included)
- Show the calculation explicitly (WOZ-waarde * percentage)

### 3.6 Tariefsaanpassing

- If the taxpayer's box 1 income falls in the top bracket (threshold per `_shared/knowledge/years/2025/annual/box1-rates.md`):
  - Calculate the portion of deductible own-home costs that falls in the top bracket
  - Cap the effective deduction rate at the 2025 deduction-rate cap from `_shared/knowledge/years/2025/annual/deductions.md` (bd_own_home_deduction_cap_2025 / bd_deduction_rate_cap_2025)
  - Calculate the tariefsaanpassing amount (difference between the top bracket rate and the capped deduction rate)
- If income is below the top bracket: no tariefsaanpassing applies

### 3.7 Hillenregeling

- If the eigenwoningforfait exceeds the mortgage interest paid:
  - Apply the Hillenregeling correction using the 2025 percentage from `_shared/knowledge/own-home/eigenwoningforfait.md`
  - The correction reduces the net positive eigenwoningforfait
- If mortgage interest exceeds eigenwoningforfait: Hillenregeling does not apply

### 3.8 Net own-home result

- Net result = eigenwoningforfait minus mortgage interest (typically negative / a deduction)
- Adjusted for tariefsaanpassing and Hillenregeling if applicable
- This amount is added to box 1 income

### 3.9 Partner handling for own home

- If fiscal partners co-own the property: allocate based on ownership shares (typically 50/50)
- Note that the net eigen woning result can be allocated differently for tax optimization
- Both partners must report their share in their individual return

---

## Phase 3A — Box 2 compilation

Compile standard aanmerkelijk-belang data for the annual 2025 return when applicable. If the taxpayer has no Box 2 position, emit the canonical "not applicable" line from the output contract and continue.

When the taxpayer has an aanmerkelijk belang, read the rates from `_shared/knowledge/years/2025/box2/box2-rates.md` — never paraphrase the 24.5% / 31% box 2 bracket from memory — and append `bd_box2_rates_2025_2026`, `bd_box2_income_ab_guidance`, and `bd_fisin_aanmerkelijk_belang_2025` to `session-progress.yaml` → `sources_loaded`.

### 3A.1 Substantial-interest status

- Confirm whether the taxpayer has an aanmerkelijk belang.
- Standard threshold: generally 5%, assessed together with the fiscal partner where applicable.
- Record `box2.has_aanmerkelijk_belang` as `true`/`false` in the profile (the template's boolean enum); route to manual review when the status is unclear.

### 3A.2 Regular benefits

- Collect gross regular benefits, normally dividends from the substantial-interest company.
- Collect directly related costs of regular benefits.
- Collect dividend withholding tax that can be credited.
- Map:
  - `box2.reguliere_voordelen_bruto`
  - `box2.kosten_reguliere_voordelen`
  - `box2.ingehouden_dividendbelasting`

### 3A.3 Disposal benefits

- Collect net transfer price, acquisition price, and any disposal costs needed to reconcile gross sale proceeds to the official net transfer price.
- Disposal benefit is the official net transfer price minus acquisition price, unless manual review is required. If evidence starts from gross sale proceeds, subtract disposal costs once to derive the net transfer price first.
- Map:
  - `box2.vervreemdingsprijs`
  - `box2.verkrijgingsprijs`
  - `box2.vervreemdingskosten`
  - `box2.vervreemdingsvoordeel`

### 3A.4 Other standard Box 2 fields

- Collect any fictitious regular benefit from excess borrowing from the BV as `box2.fictief_regulier_voordeel_bv_lening`.
- Collect any substantial-interest loss available for setoff as `box2.te_verrekenen_verlies_ab`.
- If fiscal partners were full-year partners, record `partner.verdeling_box2_inkomen` and verify that the combined allocation totals 100%.

### 3A.5 Manual-review triggers

- Require manual review for valuation disputes, informal capital, non-arm's-length transfers, restructurings, treaty/nonresident issues, emigration, death, and corporate-tax-heavy DGA cases.
- Do not calculate complex Box 2 positions when these triggers appear; record the facts and ask for professional review.

---

## Phase 4 — Box 3 compilation

Compile savings and investment data for box 3. BOTH methods must be covered. Read the rates from `_shared/knowledge/years/2025/box3/fictitious.md` — never paraphrase from memory.

### 4.1 Assets on peildatum 1 January 2025

Collect values for each asset category:

#### Banktegoeden (category I)
- All savings accounts, current accounts, deposits, term deposits
- Cash only above the 2025 cash exemption, non-exempt green savings, premiedepots, VvE reserve shares, and money on notary/bailiff third-party accounts where applicable
- Source: bank statements or jaaropgaven with balance on 1 January 2025
- Match against evidence index items classified as bankafschrift or jaaropgaaf-bank

#### Overige bezittingen (category II)
- Investment portfolios (listed securities, mutual funds)
- Crypto-assets (valued at market price on 1 January 2025)
- Real estate not being the eigen woning (second homes, rental property)
- Receivables (vorderingen) -- loans to others, after checking official exceptions
- Other assets
- Source: portfolio year-end statements, crypto exchange statements

#### Schulden (category III)
- All debts EXCEPT mortgage debt on the eigen woning
- Consumer loans, study debts under the Wet studiefinanciering, other liabilities
- Note the debt threshold below which debts are not deductible

### 4.2 Assets on 31 December 2025

- Collect values for the same categories on 31 December 2025
- These are needed for the actual return calculation (mark-to-market)
- For the fictitious return, only the 1 January 2025 values are used

### 4.3 Fictitious return calculation

Follow the calculation method from `fictitious.md`:
1. Calculate aftrekbare schulden after the debt threshold
2. Calculate belastbaar rendement by category
3. Calculate rendementsgrondslag
4. Calculate grondslag sparen en beleggen after heffingsvrij vermogen
5. Calculate aandeel in de rendementsgrondslag
6. Calculate box 3 income and box 3 tax

Common failure: do NOT apply heffingsvrij vermogen before calculating belastbaar rendement.

### 4.4 Actual return data collection

Follow the data requirements from `actual-return.md`:
1. Actual interest received on bank accounts during 2025
2. Dividends received (before dividend withholding tax)
3. Bare rental income (kale huur) and other income from box 3 assets
4. Value changes for disposed box 3 assets, including sale proceeds and start-of-year or acquisition values
5. Value changes for retained or acquired box 3 assets, including investments, securities, crypto-assets, second homes, other box 3 real estate, and other assets where value changes count
6. Interest paid on box 3 debts
7. Qualifying WOZ-value investment correction data, if applicable

Do not deduct custody fees, transaction costs, management fees, maintenance costs, or adviser fees from actual return.

Do not deduct heffingsvrij vermogen from actual return. If fiscal partners choose a box 3 allocation, apply the same allocation percentage to actual return for the comparison.

If the taxpayer cannot provide actual return data: note that the fictitious method will apply by default.

### 4.5 Comparison: fictitious vs actual

- Present both calculations side by side
- Note which method results in lower box 3 tax
- Add a note that the final election is made in the official filing environment
- The workpack does not make a binding election

### 4.6 Partner allocation for box 3

- If fiscal partners: the joint grondslag sparen en beleggen can be freely allocated (0%-100%)
- The allocation applies to the entire joint box 3 base, not individual assets or debts
- Both partners must use the same allocation ratio
- Present simple scenarios such as 50/50, 100/0, and 0/100; do not select a binding allocation automatically

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
- Apply the zorgkosten drempel only if the exact reviewed 2025 table has been added to the source pack; otherwise flag the deductible amount for manual review
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
- Calculate jaarruimte and reserveringsruimte only if the exact reviewed 2025 source rules and required inputs are present; otherwise flag the limit and deductible amount for manual review
- Required inputs normally include employment income, pension accrual (factor A), and unused jaarruimte of prior years
- Evidence: annual statement from lijfrente provider, factor A statement from employer

### 5.5 Other deductions

- Studiekosten / scholingsuitgaven: collect only as a manual-review item unless a reviewed official source is added
- Restant persoonsgebonden aftrek from prior years
- Any other qualifying deductions from the profile or evidence

### 5.6 Deduction summary

- Total persoonsgebonden aftrek
- Note the allocation order: box 1 first, then box 3, then box 2
- If fiscal partners: note allocation options and model scenarios; do not assume the highest marginal-rate partner is always best. Partner allocation of these deductions is finalized in Phase 6 via `nl-tax-partner-deductions`.

---

## Phase 5.5 — Credits screening

Use household composition from `profile.yaml` to surface which credits apply. For each of the 4 credits below, emit one line in the workpack: either "Triggered: [reason]" or "Not applicable: [reason in one phrase]".

### 5.5.1 IACK (inkomensafhankelijke combinatiekorting)

Triggered when the taxpayer (or fiscal partner with lower arbeidsinkomen) had at least one child registered at the taxpayer's address who turned 12 or younger on 1 January 2025, AND the taxpayer met the minimum arbeidsinkomen threshold.

- Check `profile.yaml` → `household.children` for DOBs.
- If at least one child satisfies the age condition, mark IACK as a manual-review item; do not calculate the amount.

### 5.5.2 Ouderenkorting

Triggered when the taxpayer reaches AOW age in 2025.

- Check `profile.yaml` → `person.aow_age_in_tax_year`.
- If triggered, flag as manual review.

### 5.5.3 Alleenstaande-ouderenkorting

Triggered when the taxpayer reaches AOW age AND has `single_parent_status: true` AND has no fiscal partner.

### 5.5.4 Jonggehandicaptenkorting

Triggered when the taxpayer receives a Wajong-uitkering or holds young-disabled status. Ask the user explicitly; do not infer from age alone.

### 5.5.5 Output

Write the screening results to `workspace/annual/2025/notes/credits.yaml`. The template's Credits screening section emits these results verbatim.

---

## Phase 6 — Partner handling

If the taxpayer has a fiscal partner, compile the partner section.

Delegate the fiscal-partner determination and allocation modelling to the `nl-tax-partner-deductions` helper (matching the Helper delegation contract in `SKILL.md`): invoke it to fold partner status and the deduction-/box-allocation scenarios into `workspace/shared/allocation-options.md`, ask the user the questions it returns, then re-invoke it to finalize. Read `allocation-options.md` back before assembling the partner section. The helper writes only under `workspace/shared/`; this skill owns `workspace/annual/**`.

### 6.1 Partner status confirmation

- Confirm fiscal partner status on 31 December 2025 (or qualifying part-year partnership)
- Married, registered partnership, or cohabiting with qualifying conditions

### 6.2 Allocatable items

List all items that can be freely allocated between partners:
- Eigen woning result (net forfait minus interest)
- Box 2 income from aanmerkelijk belang, when full-year fiscal partner allocation applies
- Box 3 grondslag (assets minus debts)
- Persoonsgebonden aftrek components (alimentatie, zorgkosten, giften, etc.)

### 6.3 Non-allocatable items

List items that are personal and cannot be allocated:
- Arbeidskorting (based on individual arbeidsinkomen)
- Ondernemersaftrek (personal to the ondernemer)
- MKB-winstvrijstelling (personal to the ondernemer)

### 6.4 Allocation recommendations

- Identify each partner's marginal rate and affected credits
- Present allocation scenarios rather than choosing one automatically
- Consider the 2025 tariefsaanpassing/deduction-rate cap for listed deductions (37.48% cap)
- Consider the phase-out of heffingskortingen
- Present at least the default and one optimized allocation for review

---

## Phase 7 — Field map generation

### 7.1 Generate field map

Map each workpack line item to the corresponding field or section in the Belastingdienst online return form. Prepare the field-map content in this phase, but do NOT write `workspace/annual/2025/field-map.yaml` yet: that file is written together with `return-pack.md` in Phase 10.3, and only after the workpack generation gate in `SKILL.md` is satisfied (every annual subsection `complete`/`chat_only`/`deferred` plus the user's verbatim confirmation phrase). Until then, keep the prepared mappings in the phase notes.

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

Write or update `workspace/shared/missing-info.md` (seed from `_shared/templates/missing-info.md` on first write):
- Each item tagged with `workflow: annual_2025`
- Each item has a priority: critical (blocks filing), important (affects accuracy), nice-to-have
- Each item describes what is needed and where the taxpayer can obtain it

---

## Phase 9 — Review question generation

### 9.1 Generate review questions

Use the entry format from `_shared/templates/review-questions.md`. Create questions for each area of uncertainty:
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

Read the template from `templates/annual-return-pack.md`. Fill in every section with the data compiled in phases 1.5-9.

### 10.2 Run the workpack self-check

Run every check in `reference/annual-output-contract.md` § "Workpack self-check": structural, content, cross-contamination, and safety. Report each result yes/no in the assembly turn. If any item is "no", do not write the workpack — fix the gap or ask the user, then re-run.

### 10.3 Write the workpack

Write the completed workpack to `workspace/annual/2025/return-pack.md`. Write the field map (prepared in Phase 7) alongside as `workspace/annual/2025/field-map.yaml`. Both files sit behind the same generation gate in `SKILL.md`; neither is written before the gate opens.

### 10.4 Summary to user

After writing:
- Confirm the workpack location
- Report the count of missing information items
- Report the count of assumptions made
- Remind the user to review the human review checklist
- Remind the user that filing happens through Mijn Belastingdienst
