# Annual Income Tax Return Field Reference (Aangifte Inkomstenbelasting 2025)

This reference defines the known fields in the Dutch annual income tax return that the field mapper produces. Each field includes an identifier, Dutch and English labels, the section it belongs to, whether it is required or conditional, and the evidence type that typically provides the value.

---

## Personal Data (Persoonsgegevens)

| field_id | Label (NL) | Label (EN) | Section | Required | Evidence Type |
|---|---|---|---|---|---|
| `personal.bsn` | BSN (burgerservicenummer) | Citizen service number | Persoonsgegevens | required | Pre-filled by portal; do NOT store in field map |
| `personal.naam` | Naam | Name | Persoonsgegevens | required | Pre-filled by portal |
| `personal.adres` | Adres | Address | Persoonsgegevens | required | Pre-filled by portal |
| `personal.geboortedatum` | Geboortedatum | Date of birth | Persoonsgegevens | required | Pre-filled by portal |
| `personal.fiscaal_partner` | Fiscaal partner | Fiscal partner | Persoonsgegevens | conditional | Profile / intake |

### Notes on personal data fields
- BSN is pre-filled in the online return after DigiD login. The field mapper notes that BSN is needed but NEVER stores the BSN value itself.
- Name, address, and date of birth are pre-filled from the BRP (Basisregistratie Personen).
- Fiscal partner status must be confirmed by the taxpayer.

---

## Box 1 — Income from Work and Home (Inkomen uit werk en woning)

### Employment Income (Inkomen uit dienstbetrekking)

| field_id | Label (NL) | Label (EN) | Section | Required | Evidence Type |
|---|---|---|---|---|---|
| `box1.loon` | Loon (inkomen uit dienstbetrekking) | Employment income (gross salary) | Box 1 — Werk | required | `jaaropgaaf` |
| `box1.loonheffing` | Ingehouden loonheffing | Withheld wage tax | Box 1 — Werk | required | `jaaropgaaf` |
| `box1.arbeidskorting_loon` | Loon voor arbeidskorting | Salary for employment tax credit | Box 1 — Werk | optional | `jaaropgaaf` |

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
| `box1.resultaat_overige_werkzaamheden` | Resultaat uit overige werkzaamheden | Income from other activities | Box 1 — Overig | conditional | Various / user-provided |

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

## Box 3 — Savings and Investments (Sparen en beleggen)

| field_id | Label (NL) | Label (EN) | Section | Required | Evidence Type |
|---|---|---|---|---|---|
| `box3.banktegoeden` | Banktegoeden op peildatum 1 januari 2025 | Bank balances on reference date | Box 3 — Bezittingen | conditional | `bankafschrift`, `jaaroverzicht_bank` |
| `box3.overige_bezittingen` | Overige bezittingen op peildatum 1 januari 2025 | Other assets on reference date | Box 3 — Bezittingen | conditional | `jaaroverzicht_beleggingen`, `crypto_overzicht`, `eigendom_bewijs` |
| `box3.schulden` | Schulden op peildatum 1 januari 2025 | Debts on reference date | Box 3 — Schulden | conditional | `schuld_overzicht` |
| `box3.werkelijk_rendement_rente` | Ontvangen rente (werkelijk rendement) | Interest received (actual return) | Box 3 — Werkelijk rendement | optional | `jaaroverzicht_bank` |
| `box3.werkelijk_rendement_dividend` | Ontvangen dividend (werkelijk rendement) | Dividends received (actual return) | Box 3 — Werkelijk rendement | optional | `jaaroverzicht_beleggingen` |
| `box3.werkelijk_rendement_huur` | Netto huurinkomsten (werkelijk rendement) | Net rental income (actual return) | Box 3 — Werkelijk rendement | optional | `huurcontract`, user-provided |
| `box3.werkelijk_rendement_waardeverandering` | Waardeveranderingen (werkelijk rendement) | Value changes (actual return) | Box 3 — Werkelijk rendement | optional | `jaaroverzicht_beleggingen` |
| `box3.werkelijk_rendement_kosten` | Aftrekbare kosten (werkelijk rendement) | Deductible costs (actual return) | Box 3 — Werkelijk rendement | optional | Various |

### Notes on box 3 fields
- Peildatum for 2025 annual return is 1 January 2025.
- The annual return supports BOTH fictitious return (forfaitair rendement) and actual return (werkelijk rendement). The field map collects data for both.
- Werkelijk rendement fields are optional -- the taxpayer may choose the fictitious method instead.
- The heffingsvrij vermogen (EUR 57,000 single / EUR 114,000 partners) is applied in the portal.

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
- Specifieke zorgkosten have a drempel (threshold) that depends on income. Only the amount above the threshold is deductible.
- Giften have different rules for periodieke giften (no threshold, requires agreement) and gewone giften (threshold applies).
- Lijfrentepremie deduction is limited by jaarruimte and reserveringsruimte calculations.

---

## Partner Fields (Fiscaal partnerschap)

| field_id | Label (NL) | Label (EN) | Section | Required | Evidence Type |
|---|---|---|---|---|---|
| `partner.bsn` | BSN partner | Partner citizen service number | Partner | conditional | Pre-filled after partner DigiD link; do NOT store |
| `partner.inkomen` | Inkomen partner | Partner income | Partner | conditional | Partner `jaaropgaaf` |
| `partner.verdeling_box3` | Verdeling box 3 (percentage) | Box 3 allocation (percentage) | Partner | conditional | User choice |
| `partner.verdeling_eigenwoning` | Verdeling eigen woning (percentage) | Own-home allocation (percentage) | Partner | conditional | User choice |
| `partner.verdeling_aftrekposten` | Verdeling persoonsgebonden aftrek | Deduction allocation | Partner | conditional | User choice |

### Notes on partner fields
- Partner BSN is entered via DigiD partner-link in the portal. The field mapper notes it is needed but NEVER stores the BSN value.
- Allocation choices (verdeling) determine how shared income, assets, and deductions are split between partners. The optimal split depends on individual tax positions.
- Non-allocatable items (arbeidskorting, ondernemersaftrek) cannot be transferred to the partner.
