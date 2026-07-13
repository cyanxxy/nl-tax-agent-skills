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
- **Winst uit onderneming (eenmanszaak / ZZP) is preparation-only.** If the taxpayer is an IB-ondernemer with an eenmanszaak, set `business.has_onderneming: true` and organize the finalized profit-and-loss statement, finalized balance, and review questions in Phase 2A. The annual field map stays `draft` with a business-section schema-review blocker.
- Route to manual review or unsupported (do not prepare a standard winst section) for the complex business forms outside standard scope: partnerships (VOF, maatschap, CV) and profit-share allocation, medegerechtigdheid, DGA/BV winst, agrarische ondernemingen (landbouwvrijstelling), zeevarenden, and business-cessation events (staking, herinvesteringsreserve, oudedagsreserve wind-down). These keep the blocked `annual_2025_entrepreneurs` candidate.
- Resultaat uit overige werkzaamheden is not winst uit onderneming: keep it as manual-review data (see Phase 2.4); do not calculate it as a standard entrepreneur case.

### 1.5 Living taxpayer confirmed

- Confirm the return is not for a deceased person
- If F-biljet scenario: stop -- unsupported case

### 1.6 No M-biljet required

- Confirm no immigration or emigration during 2025
- If M-biljet is required: stop -- unsupported case

### 1.7 Household composition

- Read `profile.yaml` → `person.date_of_birth`, `partner.partner_date_of_birth`, `household.children_at_home_count`, `household.children`, `person.aow_age_in_tax_year`, `partner.partner_aow_age_in_tax_year`
- If any of these are missing or `source: unknown` and the workflow needs them for credits screening (Phase 5.5), ask the user to fill them in now, in one batch of up to 3 questions. Do not ask for BSNs.
- Persist answers back to `profile.yaml` with `source: user_chat` and a stated_at date. Mark `sections.intake.subsections.household_composition.status: complete` in `session-progress.yaml`.

### 1.8 Evidence index exists

- Read `workspace/taxpayer/evidence-index.yaml`
- If missing: continue normally with chat collection. Say only that the user may
  provide amounts in chat or attach documents; absence of an evidence index is
  not itself a gap and never forces a draft.
- If partially indexed: proceed but flag uncovered categories

### 1.9 Box 2 scope check

- Standard Box 2 preparation is supported for `annual_2025` when the taxpayer has an aanmerkelijk belang and the facts are straightforward.
- Keep the case in scope for regular benefits such as dividends, disposal benefits such as share-sale profit, dividend withholding tax credit, loss carry-forward fields, and fiscal-partner allocation of Box 2 income.
- Route to manual review or unsupported for valuation disputes, emigration, death, restructurings, treaty/nonresident issues, informal capital, non-arm's-length transfers, and corporate-tax-heavy DGA cases.

### 1.10 Knowledge loading boundary

Do **not** load any file in the list below during preflight. It is a routing
inventory only: each later phase loads the applicable files immediately before
using them and records only those actually consulted in `sources_loaded`. Never
stale-check or warn about an inapplicable source. If an active phase cannot load
a required file, stop that phase and tell the user; do not paraphrase rates from
memory.

- `_shared/knowledge/years/2025/annual/box1-rates.md` *(bd_box1_rates_2025, bd_bijtelling_auto_2025, bd_stock_options_2025)*
- `_shared/knowledge/years/2025/annual/credits.md` *(bd_general_tax_credit_2025, bd_labour_tax_credit_2025, bd_tax_credit_payout_2025, bd_heffingskortingen_how_2025, bd_arbeidsinkomen_definition_2025)*
- `_shared/knowledge/years/2025/annual/own-home.md` *(bd_own_home_deduction_cap_2025)*
- `_shared/knowledge/years/2025/annual/deductions.md` *(bd_giften_aftrek_2025, bd_zorgkosten_overzicht_2025, bd_fisin_zorgkosten_2025, bd_vervoerskosten_ziekte_2025, bd_fisin_lijfrente_2025, bd_fisin_studiekosten_2025, bd_deduction_rate_cap_2025)*
- `_shared/knowledge/years/2025/annual/late-filing.md` *(bd_verzuimboete, bd_belastingrente_overview, bd_belastingrente_ib, bd_invorderingsrente)*
- `_shared/knowledge/years/2025/annual/filing-flow.md` *(bd_annual_return_landing_2025, bd_annual_return_4_steps_2025, bd_annual_deadline_2025, bd_annual_extension_2025, bd_annual_extension_eligibility_2025)*
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
