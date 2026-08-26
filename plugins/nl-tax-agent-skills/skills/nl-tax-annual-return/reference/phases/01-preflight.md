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
- **Winst uit onderneming (eenmanszaak / ZZP) is prepared end to end.** If the taxpayer is an IB-ondernemer with an eenmanszaak, set `business.has_onderneming: true`. Phase 2A runs the income-category pre-screen and then the ordered chain from the saldo fiscale winstberekening through investeringsaftrek, ondernemersaftrek and MKB-winstvrijstelling to the belastbare winst uit onderneming, which feeds the box 1 total. The annual field map reaches `review_ready` when the reviewed zakelijke schema covers every rubriek and question the case needs and no routing marker applies.
- Recognise and route every other IB business form rather than refusing it: vof, maatschap, man-vrouwfirma, cv, medegerechtigde, agrarische onderneming and zeescheepvaart are named in Phase 2A, and the surrounding return is still prepared. What stays terminal manual review is the **computation**: partnership profit-share allocation and KIA apportionment, medegerechtigde loss caps, DGA/BV winst, landbouwvrijstelling, zeevarenden, stakingswinst and doorschuiving, herinvesteringsreserve movements, oudedagsreserve wind-down, and terbeschikkingstelling. Those computations keep the blocked `annual_2025_entrepreneurs` candidate.
- Resultaat uit overige werkzaamheden is not winst uit onderneming, and it is not a dead end: prepare it in Phase 2.4 under `row-en-dba-2025.md`, with no ondernemersaftrek, MKB-winstvrijstelling or investeringsaftrek.

### 1.5 Living taxpayer confirmed

- Confirm the return is not for a deceased person
- If F-biljet scenario: stop -- unsupported case

### 1.6 No M-biljet required

- Confirm no immigration or emigration during 2025
- If M-biljet is required: stop -- unsupported case

### 1.7 Household composition

- Read `profile.yaml` → `person.date_of_birth`,
  `person.aow_by_tax_year.2025`, `partner.partner_date_of_birth`,
  `partner.aow_by_tax_year.2025`, `household.children_at_home_count`, and
  `household.children`. If an otherwise complete legacy profile has only
  scalar AOW fields, normalize them into the 2025 entry from the sourced DOB
  and reviewed AOW note; do not restart intake or use a legacy boolean as the
  three-state result.
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
using them and records only those actually consulted in
`sources_loaded_by_workflow.annual_2025`, mirrored in active `sources_loaded`. Never
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
- `_shared/knowledge/years/2025/entrepreneur/row-en-dba-2025.md` *(bd_bron_van_inkomen, bd_wat_zijn_inkomsten_overig_werk, bd_niet_in_loondienst_werken, bd_welke_kosten_bijverdiensten, bd_fisin2025_row, bd_handhaving_arbeidsrelaties, bd_geen_nieuwe_modelovereenkomsten)* — whenever self-employed or freelance income is present, including when the income-category screen lands on resultaat uit overige werkzaamheden rather than winst
- `_shared/knowledge/years/2025/entrepreneur/winstberekening-2025.md` *(bd_ondernemer_cijfers_aangifte_2025, bd_fisin_2025_h7, bd_fisin_2025_h8, bd_ola_ih2025_winstberekening, bd_verrekenen_ngz, bd_tariefsaanpassing_aftrekposten)* — the ordered profit chain; same condition as the other winst notes
- `_shared/knowledge/years/2025/entrepreneur/zakelijke-schema-2025.md` *(bd_ola_ih2025_wv_opbrengsten, bd_ola_ih2025_wv_afschrijvingen, bd_ola_ih2025_wv_overige_bedrijfskosten, bd_ola_ih2025_activa_materieel, bd_ola_ih2025_passiva_ondernemingsvermogen, bd_ola_ih2025_urencriterium_vraag)* — the aangifte rubrieken, questions and `onderneming.*` identifiers; same condition
- `_shared/knowledge/years/2025/entrepreneur/afschrijving-en-bedrijfsmiddelen-2025.md` *(bd_vermogensetikettering, bd_wat_is_afschrijven, bd_afschrijving_berekening, bd_afschrijving_bedrijfspand_2025, bd_herinvesteringsreserve, bd_egalisatiereserve)* — same condition
- `_shared/knowledge/years/2025/entrepreneur/vervoer-2025.md` *(bd_privegebruik_auto_ondernemer, bd_rittenregistratie, bd_uitsluitend_zakelijk_gebruik_bestelauto, bd_zakelijk_gebruik_privevervoermiddel, bd_privegebruik_andere_vervoermiddelen, wet_ib_3_20a_2025)* — only when a vehicle or travel figure enters the winst
- `_shared/knowledge/years/2025/entrepreneur/aanloopfase-en-starters-2025.md` *(bd_kosten_aanloopfase, bd_willekeurige_afschrijving_starters, law_uwa_2001, law_uitvoeringsregeling_ib_2001)* — only for a first business year, pre-start costs or assets, or a starter relief
- `_shared/knowledge/years/2025/entrepreneur/partner-en-meewerken-2025.md` *(bd_partner_gaat_meewerken, bd_meewerkaftrek_algemeen, bd_arbeidsbeloning_fiscale_partner, fisin2025_fiscaal_partnerschap)* — only when the fiscale partner works in the enterprise
- `_shared/knowledge/years/2025/entrepreneur/zvw-2025.md` *(bd_zvw_percentages_2025_2026, reg_zorgverzekering_h5_2025, bd_zvw_inkomensafhankelijke_bijdrage, bd_zvw_resultaat_overig_werk, bd_zvw_teruggaaf)* — the separate bijdrage aanslag; whenever there is winst uit onderneming or resultaat uit overige werkzaamheden
- `_shared/knowledge/years/2025/entrepreneur/inkomensvoorzieningen-2025.md` *(bd_aftrekken_lijfrentepremies, bd_hoe_bereken_ik_mijn_jaarruimte, bd_fisin2025_inkomensvoorzieningen_hfst15, bd_aov_voor_ondernemers, bd_aov_prive_aftrek, bd_extra_lijfrenteaftrek_staking_2025)* — lijfrente ruimte and AOV for an ondernemer; also read in Phase 5
- `_shared/knowledge/years/2025/entrepreneur/verlies-en-verrekening-2025.md` *(bd_verlies_uit_onderneming, bd_fisin_2025_h25, bd_verrekenen_ngz, bd_middeling_aanvragen, law_besluit_ngz_staking)* — only when the chain produces a loss or a niet-gerealiseerde zelfstandigenaftrek balance exists
- `_shared/knowledge/years/2025/entrepreneur/samenwerkingsverband-2025.md` *(bd_vof_rechtsvorm, bd_maatschap_rechtsvorm, bd_cv_rechtsvorm, bd_medegerechtigde, bd_tbs_bezittingen, fisin2025_beschikbaar_stellen)* — recognition and routing only; only when a business form beyond a single-handed eenmanszaak is present
- `_shared/knowledge/years/2025/entrepreneur/staking-2025.md` *(bd_u_staakt_uw_onderneming, bd_stakingswinst_berekenen, bd_gedeeltelijke_doorschuiving_of_staking, bd_desinvesteringsbijtelling_bij_staking, bd_oudedagsreserve_afrekenen, bd_stoppende_ondernemers)* — explain-and-route only; only when the onderneming ceased, was sold or was transferred
- `_shared/knowledge/years/2025/box3/fictitious.md` *(bd_box3_2025_calc, bd_fisin_box3_assets_debts_2025)*
- `_shared/knowledge/years/2025/box3/actual-return.md` *(bd_box3_2025_actual_return, bd_fisin_box3_actual_return_2025)*
- `_shared/knowledge/years/2025/box2/box2-rates.md` *(bd_box2_rates_2025_2026)* — only when the case has an aanmerkelijk belang (`box2.has_aanmerkelijk_belang` value `true`)
- `_shared/knowledge/years/2025/box2/box2-income-guidance.md` *(bd_box2_income_ab_guidance)* — same condition
- `_shared/knowledge/years/2025/box2/fisin-aanmerkelijk-belang.md` *(bd_fisin_aanmerkelijk_belang_2025)* — same condition
- `_shared/knowledge/own-home/eigenwoningforfait.md` *(bd_eigenwoningforfait_2025_2026, bd_eigenwoningforfait_multiple_homes)*
- `_shared/knowledge/own-home/hypotheekrenteaftrek.md` *(bd_hypotheekrenteaftrek_conditions, bd_own_home_deductible_costs, bd_temporary_two_homes_interest)*
- `_shared/knowledge/partners/fiscal-partnership.md` *(bd_fiscal_partnership)*

---
