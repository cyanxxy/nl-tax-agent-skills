# Annual Income Tax Return Field Reference (Aangifte Inkomstenbelasting 2025)

source_ids: bd_annual_data_checklist_2025, bd_jaaropgaaf_fields_2025, bd_joint_filing_2025, bd_box3_2025_calc, bd_box3_2025_actual_return, bd_woz_value_annual_2025, bd_eigenwoningforfait_2025_2026, bd_hypotheekrenteaftrek_conditions, bd_fiscal_partnership, bd_ondernemersaftrek_2025, bd_startersaftrek_2025, bd_mkb_winstvrijstelling_2025, bd_kia_2025, bd_zakelijke_kosten_2025, bd_aangifte_ondernemers_2025
workflow: annual_return
tax_year: 2025
status: active
last_reviewed: "2026-07-06"
review_status: reviewed

This reference defines the known fields in the Dutch annual income tax return that the field mapper may produce. Portal-prefilled personal rows are documented for portal awareness but are omitted from field-map output. Each field includes an identifier, Dutch and English labels, the section it belongs to, whether it is required or conditional, and the evidence type that typically provides the value.

This map is preparation-only. The taxpayer or an authorized human performs all
authenticated portal entry, review, signing, and submission; the assistant
must not access or operate Mijn Belastingdienst.

> **Provenance / freshness.** Labels reflect the 2025 Mijn Belastingdienst aangifte as described in the cited Belastingdienst guidance (source_ids above); section names and field placement can change between filing seasons — confirm against the live portal before relying on exact label text.

---

## Contents

- Personal Data (Persoonsgegevens)
- Box 1 — Income from Work and Home (Inkomen uit werk en woning)
- Winst uit onderneming (Profit from enterprise) — Box 1
- Own Home (Eigen woning) — Box 1 Deduction
- Box 2 — Substantial Interest (Aanmerkelijk belang)
- Box 3 — Savings and Investments (Sparen en beleggen)
- Deductions (Aftrekposten / Persoonsgebonden aftrek)
- Partner Fields (Fiscaal partnerschap)

## Personal Data (Persoonsgegevens)

| field_id | Label (NL) | Label (EN) | Section | Required | Evidence Type |
|---|---|---|---|---|---|
| `personal.bsn` | BSN (burgerservicenummer) | Citizen service number | Persoonsgegevens | required | Pre-filled by portal; do NOT store in field map |
| `personal.naam` | Naam | Name | Persoonsgegevens | required | Pre-filled by portal |
| `personal.adres` | Adres | Address | Persoonsgegevens | required | Pre-filled by portal |
| `personal.geboortedatum` | Geboortedatum | Date of birth | Persoonsgegevens | required | Pre-filled by portal |
| `personal.fiscaal_partner` | Fiscaal partner | Fiscal partner | Persoonsgegevens | conditional | Profile / intake |

### Notes on personal data fields
- BSN is pre-filled in the online return after login. The field mapper omits it entirely — it is not a data-entry field.
- Name, address, and date of birth are pre-filled from the BRP (Basisregistratie Personen). The field mapper omits these rows from both `fields` and `missing_fields`; the validator treats them as coverage-exempt.
- Fiscal partner status must be confirmed by the taxpayer.

---

## Box 1 — Income from Work and Home (Inkomen uit werk en woning)

### Employment Income (Inkomen uit dienstbetrekking)

| field_id | Label (NL) | Label (EN) | Section | Required | Evidence Type |
|---|---|---|---|---|---|
| `box1.loon` | Loon / fiscaal loon (inkomen uit dienstbetrekking) | Taxable employment wage copied from the year statement | Box 1 — Werk | required | `jaaropgaaf` |
| `box1.loonheffing` | Ingehouden loonheffing | Withheld wage tax | Box 1 — Werk | required | `jaaropgaaf` |

> **Entry mode — confirm, don't blind-enter.** `box1.loon` and
> `box1.loonheffing` are normally **pre-filled** in the aangifte from the
> loonaangifteketen (VIA). The taxpayer's task is to **check that the pre-filled value
> matches the jaaropgaaf and correct it if wrong**, not to type it into a blank box.
> Render these as the value to confirm, and note "check it matches the VIA pre-fill".
> Copy `box1.loon` from the jaaropgaaf's `loon`/`fiscaal loon` amount exactly;
> never derive it by subtracting employee-insurance premiums. A displayed
> arbeidskorting is informational payroll reconciliation, not the wage basis or
> a standalone mapper field unless the live portal supplies an exact field.

### Pension Income (Pensioeninkomen)

| field_id | Label (NL) | Label (EN) | Section | Required | Evidence Type |
|---|---|---|---|---|---|
| `box1.pensioen` | Pensioen (bruto) | Pension income (gross) | Box 1 — Pensioen | conditional | `pensioenoverzicht` |
| `box1.pensioen_loonheffing` | Ingehouden loonheffing op pensioen | Withheld wage tax on pension | Box 1 — Pensioen | conditional | `pensioenoverzicht` |

### Benefits (Uitkeringen)

| field_id | Label (NL) | Label (EN) | Section | Required | Evidence Type |
|---|---|---|---|---|---|
| `box1.uitkeringen` | Uitkeringen (AOW, WW, WIA, etc.) | Benefits (state pension, unemployment, disability) | Box 1 — Uitkeringen | conditional | `uitkeringsspecificatie` |
| `box1.uitkeringen_loonheffing` | Ingehouden loonheffing op uitkeringen | Withheld wage tax on benefits | Box 1 — Uitkeringen | conditional | `uitkeringsspecificatie` |

### Other Box 1 Income

| field_id | Label (NL) | Label (EN) | Section | Required | Evidence Type |
|---|---|---|---|---|---|
| `box1.resultaat_overige_werkzaamheden` | Resultaat uit overige werkzaamheden | Income from other activities | Box 1 — Overig | manual review only | Various / user-provided |

Resultaat uit overige werkzaamheden is a manual-review marker in this workflow;
do not calculate it as standard support until reviewed sources are added.

---

## Winst uit onderneming (Profit from enterprise) — Box 1

Preparation-only for an IB-ondernemer with an eenmanszaak. Until a complete
reviewed zakelijke schema exists, an entrepreneur field map remains
`readiness: draft` with blocker `business-section schema review`. The workpack
organizes finalized profit-and-loss and balance evidence but does not emit
filing-ready business amounts. Complex forms and events are terminal review.

| field_id | Label (NL) | Label (EN) | Section | Required | Evidence Type |
|---|---|---|---|---|---|
| `business.has_onderneming` | Heeft onderneming | Has enterprise | Winst uit onderneming | conditional | `kvk_uittreksel` / user-provided |

### Notes on winst uit onderneming fields
- Only `business.has_onderneming` is represented. It is a routing/review hook,
  not a filing-ready business amount.
- No row is `required`; non-entrepreneurs use the canonical not-applicable hook.
- When `business.has_onderneming` is true, declare `readiness: draft`, require
  manual review, and include the blocker in top-level notes.

---

## Own Home (Eigen woning) — Box 1 Deduction

| field_id | Label (NL) | Label (EN) | Section | Required | Evidence Type |
|---|---|---|---|---|---|
| `eigenwoning.woz_waarde` | WOZ-waarde | WOZ property valuation | Eigen woning | conditional | `woz_beschikking` |
| `eigenwoning.eigenwoningforfait` | Eigenwoningforfait | Deemed rental value | Eigen woning | conditional | Calculated from WOZ |
| `eigenwoning.hypotheekrente` | Betaalde hypotheekrente | Mortgage interest paid | Eigen woning | conditional | `hypotheek_jaaroverzicht` |
| `eigenwoning.aftrekbare_kosten` | Aftrekbare kosten eigen woning | Deductible own-home costs | Eigen woning | conditional | Calculated |
| `eigenwoning.eigenwoningschuld` | Eigenwoningschuld (restschuld) | Mortgage debt (outstanding) | Eigen woning | conditional | `hypotheek_jaaroverzicht` |

### Notes on eigen woning fields
- Eigenwoningforfait is calculated as a percentage of the WOZ-waarde. The percentage depends on the WOZ value range (see `_shared/knowledge/years/2025/annual/own-home.md`).
- Hypotheekrente (mortgage interest) is deductible only for qualifying mortgages (annuitair or lineair for post-2013 mortgages).
- The net eigen woning result (eigenwoningforfait minus hypotheekrente) flows into box 1.

---

## Box 2 — Substantial Interest (Aanmerkelijk belang)

| field_id | Label (NL) | Label (EN) | Section | Required | Evidence Type |
|---|---|---|---|---|---|
| `box2.has_aanmerkelijk_belang` | Aanmerkelijk belang aanwezig | Has substantial interest | Box 2 — Aanmerkelijk belang | conditional | Profile / shareholder register / user-provided |
| `box2.reguliere_voordelen_bruto` | Reguliere voordelen bruto | Gross regular benefits | Box 2 — Reguliere voordelen | conditional | Dividend statement / BV records |
| `box2.kosten_reguliere_voordelen` | Kosten reguliere voordelen | Costs of regular benefits | Box 2 — Reguliere voordelen | optional | Expense evidence / user-provided |
| `box2.vervreemdingsprijs` | Vervreemdingsprijs | Net transfer price | Box 2 — Vervreemding | conditional | Sale agreement / notarial deed |
| `box2.verkrijgingsprijs` | Verkrijgingsprijs | Acquisition price | Box 2 — Vervreemding | conditional | Acquisition records / shareholder register |
| `box2.vervreemdingskosten` | Vervreemdingskosten | Disposal costs | Box 2 — Vervreemding | optional | Transaction evidence |
| `box2.vervreemdingsvoordeel` | Vervreemdingsvoordeel | Disposal benefit | Box 2 — Vervreemding | conditional | Calculated / manual review |
| `box2.fictief_regulier_voordeel_bv_lening` | Fictief regulier voordeel bovenmatige lening BV | Fictitious regular benefit for BV lending | Box 2 — Reguliere voordelen | conditional | Loan statement / manual review |
| `box2.ingehouden_dividendbelasting` | Ingehouden dividendbelasting | Dividend withholding tax | Box 2 — Te verrekenen belasting | conditional | Dividend statement |
| `box2.te_verrekenen_verlies_ab` | Te verrekenen verlies uit aanmerkelijk belang | Substantial-interest loss to set off | Box 2 — Verliesverrekening | conditional | Prior assessment / loss statement |

### Notes on box 2 fields
- Standard Box 2 preparation is supported for `annual_2025` when the taxpayer has straightforward aanmerkelijk-belang facts.
- Regular benefits include dividends. Disposal benefits include share-sale profit; the standard preparation formula is official net transfer price minus acquisition price. If evidence starts from gross sale proceeds, subtract disposal costs once to derive the net transfer price first.
- Dividend withholding tax may be credited when supported by evidence.
- Require manual review for valuation disputes, informal capital, non-arm's-length transfers, restructurings, treaty/nonresident issues, emigration, death, and corporate-tax-heavy DGA cases.

---

## Box 3 — Savings and Investments (Sparen en beleggen)

| field_id | Label (NL) | Label (EN) | Section | Required | Evidence Type |
|---|---|---|---|---|---|
| `box3.banktegoeden` | Banktegoeden op peildatum 1 januari 2025 | Bank balances on reference date | Box 3 — Bezittingen | conditional | `bankafschrift`, `jaaroverzicht_bank` |
| `box3.overige_bezittingen` | Overige bezittingen op peildatum 1 januari 2025 | Other assets on reference date | Box 3 — Bezittingen | conditional | `jaaroverzicht_beleggingen`, `crypto_overzicht`, `eigendom_bewijs` |
| `box3.groene_beleggingen_spaartegoeden` | Groene beleggingen en groene spaartegoeden | Green investments and green savings | Box 3 — Vrijstellingen | optional | `jaaroverzicht_groenfonds`, `jaaroverzicht_bank` |
| `box3.contant_geld` | Contant geld en cadeaubonnen | Cash and gift cards | Box 3 — Bezittingen | optional | User-provided / cash log |
| `box3.schulden` | Schulden op peildatum 1 januari 2025 | Debts on reference date | Box 3 — Schulden | conditional | `schuld_overzicht` |
| `box3.werkelijk_rendement_rente` | Ontvangen rente (werkelijk rendement) | Interest received (actual return) | Box 3 — Werkelijk rendement | optional | `jaaroverzicht_bank` |
| `box3.werkelijk_rendement_dividend` | Ontvangen dividend (werkelijk rendement) | Dividends received (actual return) | Box 3 — Werkelijk rendement | optional | `jaaroverzicht_beleggingen` |
| `box3.werkelijk_rendement_huur` | Huurinkomsten (werkelijk rendement) | Rental income (actual return) | Box 3 — Werkelijk rendement | optional | `huurcontract`, user-provided |
| `box3.werkelijk_rendement_waardeverandering` | Waardeveranderingen (werkelijk rendement) | Value changes (actual return) | Box 3 — Werkelijk rendement | optional | `jaaroverzicht_beleggingen` |
| `box3.werkelijk_rendement_box3_schuldrente` | Betaalde rente op box 3-schulden | Interest paid on box 3 debts | Box 3 — Werkelijk rendement | optional | `schuld_overzicht`, user-provided |
| `box3.werkelijk_rendement_woz_investment_correction` | WOZ-investeringcorrectie | Qualifying WOZ-value investment correction | Box 3 — Werkelijk rendement | optional | `woz_beschikking`, user-provided |

> **Crypto (2025).** Crypto-assets are valued at the market price on 1 January 2025
> and are part of `box3.overige_bezittingen` (same heffingsvrij vermogen and forfait).
> Note for the user: new for the 2025 aangifte, the online return has a dedicated
> **"Cryptobezittingen"** checkbox/section inside box 3 — tick it and enter the crypto
> value there. The tax treatment is unchanged; only the data-entry location is distinct.

### Notes on box 3 fields
- Peildatum for 2025 annual return is 1 January 2025.
- The annual return supports both the forfaitair calculation and actual-return
  data. The taxpayer chooses whether to supply the additional actual-return
  facts; this is not a tax-method election.
- When actual-return data is supplied, the 2025 portal performs both
  calculations and uses the favorable amount. The field map records supplied
  inputs and comparison evidence; it does not select a method.
- The heffingsvrij vermogen (EUR 57,684 single / EUR 115,368 partners) applies to the fictitious method; do not deduct it from werkelijk rendement.
- For fiscal partners, the actual return follows the same allocation percentage as the joint grondslag sparen en beleggen.
- Green investments/savings and cash must be identifiable separately because exemptions can change the amount included in banktegoeden or overige bezittingen.
- Do not map custody fees, transaction costs, management fees, maintenance costs, or adviser fees as deductible actual-return costs.

---

## Deductions (Aftrekposten / Persoonsgebonden aftrek)

| field_id | Label (NL) | Label (EN) | Section | Required | Evidence Type |
|---|---|---|---|---|---|
| `aftrek.alimentatie` | Betaalde partneralimentatie | Alimony paid (partner) | Aftrekposten | conditional | `alimentatie_overeenkomst` |
| `aftrek.zorgkosten` | Specifieke zorgkosten | Specific healthcare costs | Aftrekposten | conditional | `zorgkosten_overzicht` |
| `aftrek.giften_anbi` | Giften aan ANBI-instellingen | Gifts to ANBI institutions | Aftrekposten | conditional | `gift_receipt` |
| `aftrek.giften_cultureel` | Giften aan culturele instellingen | Gifts to cultural institutions | Aftrekposten | conditional | `gift_receipt` |
| `aftrek.lijfrentepremie` | Betaalde lijfrentepremie | Annuity premiums paid | Aftrekposten | conditional | `lijfrente_overzicht` |

### Notes on deduction fields
- Partneralimentatie is deductible; kinderalimentatie is NOT deductible.
- Specifieke zorgkosten have a drempel (threshold) that depends on income. Only calculate the amount above the threshold if exact reviewed 2025 threshold sources and inputs are available; otherwise mark manual review required.
- Giften have different rules for periodieke giften (no threshold, requires agreement) and gewone giften (threshold applies).
- Lijfrentepremie deduction is limited by jaarruimte and reserveringsruimte calculations. Only calculate the limit if exact reviewed 2025 rules and inputs are available; otherwise mark manual review required.

---

## Partner Fields (Fiscaal partnerschap)

| field_id | Label (NL) | Label (EN) | Section | Required | Evidence Type |
|---|---|---|---|---|---|
| `partner.bsn` | BSN partner | Partner citizen service number | Partner | conditional | Pre-filled by the portal; do NOT store |
| `partner.inkomen` | Inkomen partner | Partner income | Partner | conditional | Partner `jaaropgaaf` |
| `partner.verdeling_box3_grondslag` | Verdeling grondslag sparen en beleggen (percentage) | Box 3 base allocation percentage | Partner | conditional | User choice |
| `partner.verdeling_box2_inkomen` | Verdeling Box 2 inkomen (percentage) | Box 2 income allocation percentage | Partner | conditional | User choice |
| `partner.verdeling_eigenwoning` | Verdeling eigen woning (percentage) | Own-home allocation (percentage) | Partner | conditional | User choice |
| `partner.verdeling_aftrekposten` | Verdeling persoonsgebonden aftrek | Deduction allocation | Partner | conditional | User choice |

### Notes on partner fields
- Partner BSN is handled through the portal partner-link flow. The field mapper omits it entirely — it is not a data-entry field.
- Allocation choices (verdeling) determine how shared Box 2 income, the joint
  box 3 base, and deductions are split between partners. Box 2 allocation must
  total 100% for full-year fiscal partners. The mapper records only an explicit
  taxpayer choice with `U:` provenance; otherwise it leaves the allocation
  unresolved. It never ranks or selects a scenario.
- Fiscal partners may file together online or file separate returns. When they
  file separately, each return is signed by its own taxpayer. Where allocation
  is legally available, shared entries must remain consistent across both
  returns and total no more than 100% for each allocatable item. Part-year or
  separation cases require a manual eligibility check before mapping an
  allocation.
- Non-allocatable items (arbeidskorting, ondernemersaftrek) cannot be transferred to the partner.
