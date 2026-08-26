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
| `box1.resultaat_overige_werkzaamheden` | Resultaat uit overige werkzaamheden | Result from other activities | Box 1 — Overig | conditional | `factuur`, payment statements, cost receipts / user-provided |

Resultaat uit overige werkzaamheden is a prepared path in this workflow, not a
routing marker. Prepare it from
`_shared/knowledge/years/2025/entrepreneur/row-en-dba-2025.md`, which is
canonical: run its bron van inkomen pre-screen first, then record the gross
inkomsten uit overig werk and the costs that note allows, and map the resulting
resultaat to this single row. The category decision itself (loon, winst uit
onderneming, or resultaat uit overige werkzaamheden) stays with the taxpayer.

- The resultaat is reported in the private part of the aangifte, never in the
  zakelijk deel, so no `onderneming.*` row belongs to it and there is no
  winst-en-verliesrekening or balans to map.
- The ondernemersfaciliteiten do not apply here: no ondernemersaftrek, no
  MKB-winstvrijstelling, no investeringsaftrek, no fiscale reserves. Never map a
  deduction row that only an ondernemer can claim, and do not ask for an hours
  count in order to settle this category.
- Costs, afschrijving, goed koopmansgebruik and the limited-deductible-cost
  drempel do apply, on the rules in
  `_shared/knowledge/years/2025/entrepreneur/winst-en-kosten.md` and
  `_shared/knowledge/years/2025/entrepreneur/afschrijving-en-bedrijfsmiddelen-2025.md`.
- A bijdrage Zvw is due on the resultaat and arrives as a **second, separate
  aanslag** alongside the aanslag inkomstenbelasting. One return feeds both;
  there is no Zvw entry screen and no Zvw field. Keep it in the workpack
  narrative and never create a field-map row for a bijdrage amount. Read
  `_shared/knowledge/years/2025/entrepreneur/zvw-2025.md` for the percentage and
  the maximumbijdrage-inkomen.
- Terbeschikkingstelling van bezittingen and the special categories that note
  names (gastouder, artiest, beroepssporter, kostgangers, pgb-zorg,
  vermogensbeheer beyond normal management) stay manual review only: record the
  facts and do not map a computed result.
- This income may not be divided between fiscal partners; do not map an
  allocation for it.

---

## Winst uit onderneming (Profit from enterprise) — Box 1

Preparation-only for an IB-ondernemer with an eenmanszaak. The rubrieken,
questions and identifiers below are taken from
`_shared/knowledge/years/2025/entrepreneur/zakelijke-schema-2025.md`, which stays
canonical for the schema and for the identifier naming scheme; the ordered chain
behind the figures is in
`_shared/knowledge/years/2025/entrepreneur/winstberekening-2025.md`. Amounts,
limits and thresholds stay in the sibling knowledge notes named below -- never
restate one here.

The zakelijk deel is **never pre-filled**, so an empty box carries no
information. Ask the taxpayer for the figure or record it in `missing_fields`;
never read a blank as a zero. Present these rows as a checklist of rubrieken and
questions: do not number them as portal steps and do not assert a screen order.
**You (the taxpayer) or an authorized human** open Mijn Belastingdienst and type
every value.

### Business routing hook

| field_id | Label (NL) | Label (EN) | Section | Required | Evidence Type |
|---|---|---|---|---|---|
| `business.has_onderneming` | Heeft onderneming | Has enterprise | Winst uit onderneming | conditional | `kvk_uittreksel` / user-provided |

### Internal business routing metadata -- never portal-entry rows

The annual map also carries the following two sourced control records in
`fields`. They are part of this authoritative identifier inventory only because
readiness and resume logic need them. They do **not** describe boxes in Mijn
Belastingdienst, must never appear in the human manual-entry checklist, and must
carry `entry_mode: internal_routing` in addition to the ordinary source record:

| field_id | Meaning | Allowed value |
|---|---|---|
| `business.legal_form` | Legal form established during intake | `eenmanszaak`, `vof`, `maatschap`, `cv`, `bv`, or `other` |
| `onderneming.routing.complex_case` | At least one Phase 2A computation boundary applies | `true` or `false`; an omitted or unanswered marker is never interpreted as `false` |

These records are not a substitute for the actual business-row coverage review.
They route the case; they do not prove that the winst-en-verliesrekening, balans,
private movements, or entrepreneur questions are complete.

### Winst-en-verliesrekening

| field_id | Label (NL) | Label (EN) | Section | Required | Evidence Type |
|---|---|---|---|---|---|
| `onderneming.wv.netto_omzet` | Netto-omzet | Net turnover | Winst uit onderneming -- Winst-en-verliesrekening | conditional | `winst_verlies_rekening`, `factuur` |
| `onderneming.wv.voorraadmutatie` | Wijzigingen in voorraden gereed product en onderhanden werk | Change in finished goods and work in progress | Winst uit onderneming -- Winst-en-verliesrekening | conditional | `winst_verlies_rekening` |
| `onderneming.wv.geactiveerde_productie` | Geactiveerde productie voor het eigen bedrijf | Own work capitalised | Winst uit onderneming -- Winst-en-verliesrekening | optional | `winst_verlies_rekening` |
| `onderneming.wv.overige_opbrengsten` | Overige opbrengsten | Other operating income | Winst uit onderneming -- Winst-en-verliesrekening | optional | `winst_verlies_rekening` |
| `onderneming.wv.inkoopkosten` | Inkoopkosten en uitbesteed werk | Cost of purchases and outsourced work | Winst uit onderneming -- Winst-en-verliesrekening | conditional | `winst_verlies_rekening`, `factuur` |
| `onderneming.wv.personeelskosten` | Personeelskosten | Personnel costs | Winst uit onderneming -- Winst-en-verliesrekening | conditional | `winst_verlies_rekening` |
| `onderneming.wv.arbeidsbeloning_partner` | Arbeidsbeloning aan de fiscale partner | Remuneration paid to the fiscal partner | Winst uit onderneming -- Winst-en-verliesrekening | conditional | `winst_verlies_rekening` / user-provided |
| `onderneming.wv.afschrijvingen` | Afschrijvingen | Depreciation | Winst uit onderneming -- Winst-en-verliesrekening | conditional | `winst_verlies_rekening`, `investering_factuur` |
| `onderneming.wv.huisvestingskosten` | Huisvestingskosten | Premises costs | Winst uit onderneming -- Winst-en-verliesrekening | conditional | `winst_verlies_rekening` |
| `onderneming.wv.auto_transportkosten` | Auto- en transportkosten | Vehicle and transport costs | Winst uit onderneming -- Winst-en-verliesrekening | conditional | `winst_verlies_rekening` |
| `onderneming.wv.verkoopkosten` | Verkoopkosten | Selling costs | Winst uit onderneming -- Winst-en-verliesrekening | optional | `winst_verlies_rekening` |
| `onderneming.wv.andere_kosten` | Andere kosten | Other operating costs | Winst uit onderneming -- Winst-en-verliesrekening | optional | `winst_verlies_rekening` |
| `onderneming.wv.waardeveranderingen` | Waardeveranderingen | Value changes and impairments | Winst uit onderneming -- Winst-en-verliesrekening | optional | `winst_verlies_rekening` / manual review |
| `onderneming.wv.financiele_baten_lasten` | Financiele baten en lasten | Financial income and expense | Winst uit onderneming -- Winst-en-verliesrekening | conditional | `winst_verlies_rekening` |
| `onderneming.wv.buitengewone_baten_lasten` | Buitengewone baten en lasten | Extraordinary income and expense | Winst uit onderneming -- Winst-en-verliesrekening | conditional | `winst_verlies_rekening` |
| `onderneming.wv.overige_buitengewone_baten` | Overige buitengewone baten | Other extraordinary income | Winst uit onderneming -- Winst-en-verliesrekening | conditional | `winst_verlies_rekening` / user-provided |
| `onderneming.wv.saldo` | Saldo fiscale winstberekening | Balance of the profit and loss account | Winst uit onderneming -- Winst-en-verliesrekening | optional | Derived by the form; figure to check on screen |

#### Notes on the winst-en-verliesrekening rows

- `onderneming.wv.saldo` is a total the form derives. Carry it as the figure the
  taxpayer checks on screen, never as an instruction to type a number.
- Business use of a **private** vehicle is a cost under
  `onderneming.wv.auto_transportkosten`, at the per-kilometre amount in
  `_shared/knowledge/years/2025/entrepreneur/vervoer-2025.md`. The **bijtelling**
  for private use of a business car is not a cost row: it belongs to
  `onderneming.wv.overige_buitengewone_baten` and to
  `onderneming.prive.onttrekking_auto`. Never map it under auto- en
  transportkosten.
- `onderneming.wv.arbeidsbeloning_partner` is filled only when the vergoeding to
  the fiscale partner reaches the threshold in
  `_shared/knowledge/years/2025/entrepreneur/ondernemersaftrek.md`; below it, the
  amount is not entered here.
- A werkruimte in the taxpayer's own home is usually not deductible; apply the
  test in `_shared/knowledge/years/2025/entrepreneur/winst-en-kosten.md` before
  mapping any part of `onderneming.wv.huisvestingskosten`.
- Dividend received in the enterprise is entered gross, including the
  dividendbelasting. An upward revaluation under
  `onderneming.wv.waardeveranderingen` carries a minus sign.
- For a gebouw in eigen gebruik the form also asks the bodemwaarde from the
  WOZ-beschikking; capture it with the depreciation evidence rather than as a
  separate manual-entry id.
- Where loon belonging to the opbrengsten of the onderneming and the loonheffing
  on it are present, route the treatment to manual review instead of mapping a
  row.

### Balans -- two columns per rubriek

Each rubriek is asked twice: begin boekjaar and einde boekjaar. Map the two
columns as two separate values.

| field_id | Label (NL) | Label (EN) | Section | Required | Evidence Type |
|---|---|---|---|---|---|
| `onderneming.balans.immateriele_vaste_activa_begin` / `onderneming.balans.immateriele_vaste_activa_eind` | Immateriele vaste activa | Intangible fixed assets | Winst uit onderneming -- Balans | optional | `balans` |
| `onderneming.balans.materiele_vaste_activa_begin` / `onderneming.balans.materiele_vaste_activa_eind` | Materiele vaste activa | Tangible fixed assets | Winst uit onderneming -- Balans | conditional | `balans`, `investering_factuur` |
| `onderneming.balans.financiele_vaste_activa_begin` / `onderneming.balans.financiele_vaste_activa_eind` | Financiele vaste activa | Financial fixed assets | Winst uit onderneming -- Balans | optional | `balans` |
| `onderneming.balans.voorraden_begin` / `onderneming.balans.voorraden_eind` | Voorraden | Inventories | Winst uit onderneming -- Balans | conditional | `balans` |
| `onderneming.balans.vorderingen_begin` / `onderneming.balans.vorderingen_eind` | Vorderingen | Receivables | Winst uit onderneming -- Balans | conditional | `balans` |
| `onderneming.balans.effecten_begin` / `onderneming.balans.effecten_eind` | Effecten | Securities | Winst uit onderneming -- Balans | optional | `balans` |
| `onderneming.balans.liquide_middelen_begin` / `onderneming.balans.liquide_middelen_eind` | Liquide middelen | Cash and bank balances | Winst uit onderneming -- Balans | conditional | `balans` |
| `onderneming.balans.ondernemingsvermogen_begin` / `onderneming.balans.ondernemingsvermogen_eind` | Ondernemingsvermogen | Business equity | Winst uit onderneming -- Balans | conditional | `balans` |
| `onderneming.balans.fiscale_reserves_begin` / `onderneming.balans.fiscale_reserves_eind` | Fiscale reserves (binnen het ondernemingsvermogen) | Tax-recognised reserves | Winst uit onderneming -- Balans | optional | `balans` / manual review |
| `onderneming.balans.voorzieningen_begin` / `onderneming.balans.voorzieningen_eind` | Voorzieningen | Provisions | Winst uit onderneming -- Balans | optional | `balans` |
| `onderneming.balans.langlopende_schulden_begin` / `onderneming.balans.langlopende_schulden_eind` | Langlopende schulden | Long-term liabilities | Winst uit onderneming -- Balans | conditional | `balans` |
| `onderneming.balans.kortlopende_schulden_begin` / `onderneming.balans.kortlopende_schulden_eind` | Kortlopende schulden | Short-term liabilities | Winst uit onderneming -- Balans | conditional | `balans` |

#### Notes on the balans rows

- Ask the taxpayer for the **begin** and the **eind** column separately, from the
  finalized jaarstukken. Do not carry a prior-year closing figure into the
  opening column, and do not enter zero for a column that was not supplied --
  record that column in `missing_fields`.
- The fiscale reserves (egalisatiereserve, herinvesteringsreserve,
  oudedagsreserve) sit **inside** the ondernemingsvermogen rubriek, not as a
  separate top-level passiva rubriek.
- Apply no activa-equals-passiva check and no tolerance. If the jaarstukken do
  not tie, record it as a question for the taxpayer or their accountant and do
  not resolve it.
- Voorzieningen and a herinvesteringsreserve are specified per item on the form.
  Record the specification facts; a herinvesteringsreserve movement is manual
  review, never a mapped calculation.
- The sub-field inventory for financiele vaste activa, effecten and liquide
  middelen is not captured in the reviewed schema. Ask the taxpayer to record the
  boxes the form actually presents and do not invent sub-categories.

### Entrepreneur questions

These rows carry answers, not amounts.

| field_id | Label (NL) | Label (EN) | Section | Required | Evidence Type |
|---|---|---|---|---|---|
| `onderneming.vraag.urencriterium` | Voldeed u aan het urencriterium? | Met the urencriterium for 2025 (yes/no) | Winst uit onderneming -- Vragen | conditional | `urenadministratie` / user-provided |
| `onderneming.vraag.verlaagd_urencriterium` | Voldeed u aan het verlaagd-urencriterium? | Met the reduced hours test (yes/no) | Winst uit onderneming -- Vragen | optional | `urenadministratie` / user-provided |
| `onderneming.vraag.starter_historie` | Startershistorie | Starter history: earlier years without IB-ondernemerschap, and how often the zelfstandigenaftrek was already applied | Winst uit onderneming -- Vragen | conditional | Prior aanslagen / user-provided |
| `onderneming.vraag.so_verklaring` | S&O-verklaring | Holds an RVO research-and-development statement for 2025 (yes/no) | Winst uit onderneming -- Vragen | optional | RVO verklaring / user-provided |
| `onderneming.vraag.meewerkende_partner_uren` | Uren meewerkende fiscale partner | Hours the fiscal partner worked in the enterprise | Winst uit onderneming -- Vragen | optional | `urenadministratie` / user-provided |
| `onderneming.vraag.investeringen` | Investeringen in bedrijfsmiddelen | Invested in business assets in 2025 (yes/no, with per-asset detail) | Winst uit onderneming -- Vragen | conditional | `investering_factuur` |

#### Notes on the question rows

- The hour tests, the starter conditions and the meewerkaftrek bands live in
  `_shared/knowledge/years/2025/entrepreneur/ondernemer-criteria.md` and
  `_shared/knowledge/years/2025/entrepreneur/ondernemersaftrek.md`. Read them
  there; do not restate a count in a mapped label or note.
- Ask the taxpayer for each answer. Never infer a "no", an absent starter
  history, or a nil hours count from missing evidence -- record the unanswered
  question in `missing_fields`.
- Per-asset investment detail, the per-asset minima and any
  desinvesteringsbijtelling stay in
  `_shared/knowledge/years/2025/entrepreneur/investeringsaftrek.md`.

### Priveonttrekkingen en -stortingen

| field_id | Label (NL) | Label (EN) | Section | Required | Evidence Type |
|---|---|---|---|---|---|
| `onderneming.prive.onttrekkingen` | Priveonttrekkingen | Private withdrawals | Winst uit onderneming -- Prive | conditional | `winst_verlies_rekening`, `balans` / user-provided |
| `onderneming.prive.stortingen` | Privestortingen | Private contributions | Winst uit onderneming -- Prive | conditional | `winst_verlies_rekening`, `balans` / user-provided |
| `onderneming.prive.onttrekking_auto` | Onttrekking privegebruik auto | Private use of a business car | Winst uit onderneming -- Prive | conditional | `winst_verlies_rekening` / user-provided |
| `onderneming.prive.onttrekking_woning` | Onttrekking privegebruik woning | Private use of a home held as business property | Winst uit onderneming -- Prive | conditional | `winst_verlies_rekening` / user-provided |
| `onderneming.prive.onttrekking_fiets` | Onttrekking privegebruik fiets | Private use of a business bicycle | Winst uit onderneming -- Prive | conditional | `winst_verlies_rekening` / user-provided |

#### Notes on the prive rows

- Never net onttrekkingen against stortingen before entry, and never treat a
  priveonttrekking as a business cost.
- The full sub-field inventory of this screen is not captured in the reviewed
  schema. Ask the taxpayer to record the boxes the form actually presents.
- The onttrekking amounts follow
  `_shared/knowledge/years/2025/entrepreneur/vervoer-2025.md` (auto, fiets) and
  `_shared/knowledge/years/2025/entrepreneur/winst-en-kosten.md` (woning).

### Double-entry rows -- one value, two screen paths

| Fact | Screen 1 | Screen 2 |
|---|---|---|
| `onderneming.prive.onttrekking_auto` | Winst-en-verliesrekening > Buitengewone baten en lasten > Overige buitengewone baten | Priveonttrekkingen en -stortingen |
| `onderneming.prive.onttrekking_woning` | Winst-en-verliesrekening > Buitengewone baten en lasten > Overige buitengewone baten | Priveonttrekkingen en -stortingen |
| `onderneming.prive.onttrekking_fiets` | Winst-en-verliesrekening > Buitengewone baten en lasten > Overige buitengewone baten | Priveonttrekkingen en -stortingen |
| Herinvesteringsreserve used on a purchased asset (manual review) | Winst-en-verliesrekening > Buitengewone lasten > Afboeking van de herinvesteringsreserve op gekochte activa | Balans > Passiva > Ondernemingsvermogen > herinvesteringsreserve |

Map each onttrekking **once** as a single value and print it **twice** in the
manual-entry checklist, once per screen path, so the taxpayer cannot enter one
and skip the other. Do not create a second field id for the same fact.

### What the aangifte computes -- never a manual-entry row

The taxpayer types figures and answers eligibility questions; the aangifte
computes the rest. Do **not** create a manual-entry field id for the belastbare
winst uit onderneming, for the zelfstandigenaftrek, the startersaftrek, the
aftrek voor speur- en ontwikkelingswerk, the meewerkaftrek, the startersaftrek
bij arbeidsongeschiktheid, the stakingsaftrek, the total ondernemersaftrek, the
MKB-winstvrijstelling, or the kleinschaligheidsinvesteringsaftrek.

- Present each of those as a computed expectation in the workpack narrative that
  the taxpayer checks against the screen, with the line it comes from in
  `_shared/knowledge/years/2025/entrepreneur/winstberekening-2025.md`.
- The belastbare winst uit onderneming feeds the box 1 income total in the
  workpack; it is still not a mapped entry box.
- Carry the vermogensvergelijking self-check as a workpack line: the
  winstberekening must reconcile to the saldo of the winst-en-verliesrekening.
  Report a difference; never adjust a mapped figure to force it.
- An ondernemer receives a **second, separate aanslag** for the
  inkomensafhankelijke bijdrage Zvw alongside the aanslag inkomstenbelasting.
  One return feeds both, there is no Zvw entry screen and no Zvw field: keep it
  in the workpack narrative and never create a field-map row for a bijdrage
  amount. `_shared/knowledge/years/2025/entrepreneur/zvw-2025.md` is canonical.

### Notes on winst uit onderneming fields

- Every `onderneming.*` row is `conditional` or `optional`, never `required`: a
  taxpayer without an onderneming has none of them. `business.has_onderneming`
  stays the routing hook, and non-entrepreneurs use the canonical
  not-applicable hook.
- Create manual-entry ids only for figures the taxpayer actually types. An id
  that is not in the schema above does not belong in the map; record the fact in
  the workpack instead.
- **Readiness.** The map reaches `readiness: review_ready` when the reviewed
  zakelijke schema covers every rubriek and question this case needs and no
  complex-business marker applies. Before declaring that state, audit **every**
  identifier in the W&V, balance, private-movement, prior-year-set-off and
  entrepreneur-question inventories above for this taxpayer. For each identifier,
  a map-level `notes` entry must record exactly one of `applicable_mapped`,
  `not_applicable_sourced`, or `unresolved`; include the source/profile path that
  supports every `not_applicable_sourced` decision. An omitted row or unanswered
  yes/no question is `unresolved`, never false and never not applicable. A single
  unresolved applicable-or-unknown row keeps the map `draft` independently of
  what an optional validator reports. It also stays `draft` with the blocker
  `business-section schema review`, recorded in top-level notes, when a needed
  rubriek, question or identifier falls outside the reviewed schema, or when a
  complex-business marker applies.
- **Complex-business markers.** Samenwerkingsverband (vof, maatschap,
  man-vrouwfirma, cv), medegerechtigde or profit-sharing geldverstrekker,
  DGA/BV winst, agrarische onderneming, zeevarenden, stakingswinst,
  herinvesteringsreserve, oudedagsreserve wind-down, and terbeschikkingstelling.
  Recognising and routing the form is in scope; computing those figures stays
  manual review only. Record the collected facts, name the figure that could not
  be computed, and hand it to professional review.
- A business case is no longer a standing reason to withhold `review_ready`.
  Conversely, the presence of a saldo, two equity anchors and an hours answer is
  never sufficient by itself to grant `review_ready`.

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
