# Provisional Assessment Field Reference (Voorlopige Aanslag 2026)

source_ids: bd_provisional_request_2026, bd_box3_2026_provisional, bd_provisional_rates_2026, bd_eigenwoningforfait_2025_2026, bd_hypotheekrenteaftrek_conditions
workflow: provisional_assessment
tax_year: 2026
status: active
last_reviewed: "2026-05-15"
review_status: reviewed

This reference defines the known fields in the Dutch voorlopige aanslag request or change form for tax year 2026. Portal-prefilled personal rows are documented for portal awareness but are omitted from field-map output. All values are ESTIMATES of the current/upcoming year -- not actuals from a completed year. The provisional assessment has fewer fields and less detail than the annual return.

> **Provenance / freshness.** Labels reflect the 2026 Mijn Belastingdienst voorlopige aanslag as described in the cited Belastingdienst guidance (source_ids above); section names and field placement can change between filing seasons — confirm against the live portal before relying on exact label text.

---

## Contents

- Key Differences from Annual Return
- Personal Data (Persoonsgegevens)
- Income Estimates (Geschat inkomen) — Box 1
- Own Home Estimates (Geschatte eigen woning)
- Box 2 Estimates (Geschat aanmerkelijk belang)
- Box 3 Estimates (Geschat vermogen) — Fictitious Return ONLY
- Partner Allocation Estimates
- Deduction Estimates (Geschatte aftrekposten)
- Fields NOT Present in Provisional

## Key Differences from Annual Return

1. **All fields are estimates** -- every value is the taxpayer's best projection, not a confirmed amount from evidence.
2. **Fewer detail fields** -- the provisional form asks for totals, not breakdowns per employer or per account.
3. **Box 3 explanatory note only** -- use this note and no input fields: "Werkelijk rendement is not part of provisional 2026."
4. **Peildatum is 1 January 2026** -- not 1 January 2025 as in the annual return.
5. **No allocation of prior-year evidence** -- provisional estimates are forward-looking, not evidence-based.

---

## Personal Data (Persoonsgegevens)

| field_id | Label (NL) | Label (EN) | Section | Required | Evidence Type |
|---|---|---|---|---|---|
| `personal.bsn` | BSN (burgerservicenummer) | Citizen service number | Persoonsgegevens | required | Pre-filled by the portal; NOT manually entered; do NOT store |
| `personal.adres` | Adres | Address | Persoonsgegevens | required | Pre-filled after login |

### Notes on personal data
- BSN is not a field the taxpayer enters. The field mapper omits it entirely — it is not a data-entry field.
- Address is pre-filled after login. The field mapper omits it from both `fields` and `missing_fields`; the validator treats it as coverage-exempt.
- The provisional form has minimal personal data fields compared to the annual return.

---

## Income Estimates (Geschat inkomen) — Box 1

| field_id | Label (NL) | Label (EN) | Section | Required | Evidence Type |
|---|---|---|---|---|---|
| `box1.geschat_loon` | Geschat inkomen uit werk | Estimated employment income | Box 1 — Inkomen | conditional | Estimate based on current salary / `jaaropgaaf` prior year |
| `box1.geschat_pensioen` | Geschat pensioen | Estimated pension income | Box 1 — Inkomen | conditional | Estimate based on pension statements |
| `box1.geschatte_uitkeringen` | Geschatte uitkeringen | Estimated benefits | Box 1 — Inkomen | conditional | Estimate based on current benefit level |
| `box1.geschat_overig_inkomen` | Geschat overig inkomen | Estimated other income | Box 1 — Inkomen | conditional | Estimate / user-provided |

### Notes on income estimates
- These are the taxpayer's best estimates for the full year 2026. They may be based on current employment contracts, recent jaaropgaven, or known upcoming changes.
- The portal asks for total amounts, not per-employer breakdowns.

---

## Own Home Estimates (Geschatte eigen woning)

| field_id | Label (NL) | Label (EN) | Section | Required | Evidence Type |
|---|---|---|---|---|---|
| `eigenwoning.geschatte_woz_waarde` | Geschatte WOZ-waarde | Estimated WOZ property valuation | Eigen woning | conditional | Most recent `woz_beschikking` or estimate |
| `eigenwoning.geschatte_hypotheekrente` | Geschatte hypotheekrente | Estimated mortgage interest | Eigen woning | conditional | Current mortgage terms / `hypotheek_jaaroverzicht` |

### Notes on own-home estimates
- The WOZ-waarde for the provisional 2026 may not yet be known. Use the most recent WOZ-beschikking as a baseline estimate.
- Mortgage interest estimate is typically the annual interest based on current mortgage terms.

---

## Box 2 Estimates (Geschat aanmerkelijk belang)

All Box 2 values in a provisional 2026 field map are estimates or from-baseline values. Do not present them as annual actuals.

| field_id | Label (NL) | Label (EN) | Section | Required | Evidence Type |
|---|---|---|---|---|---|
| `box2.geschatte_reguliere_voordelen` | Geschatte reguliere voordelen | Estimated regular benefits | Box 2 — Aanmerkelijk belang | conditional | Estimate / prior-year dividend / baseline |
| `box2.geschatte_vervreemdingsvoordelen` | Geschatte vervreemdingsvoordelen | Estimated disposal benefits | Box 2 — Aanmerkelijk belang | conditional | Estimate / planned share sale / baseline |
| `box2.geschatte_kosten` | Geschatte kosten Box 2 | Estimated Box 2 costs | Box 2 — Aanmerkelijk belang | optional | Estimate / baseline |
| `box2.geschatte_ingehouden_dividendbelasting` | Geschatte ingehouden dividendbelasting | Estimated dividend withholding tax | Box 2 — Te verrekenen belasting | conditional | Estimate / dividend statement / baseline |
| `box2.geschat_fictief_regulier_voordeel_bv_lening` | Geschat fictief regulier voordeel bovenmatige lening BV | Estimated fictitious regular benefit for BV lending | Box 2 — Aanmerkelijk belang | conditional | Estimate / loan statement / manual review |

### Notes on box 2 estimates
- Regular benefits include dividends.
- Disposal benefits include estimated share-sale profit.
- Route valuation disputes, informal capital, non-arm's-length transfers, restructurings, treaty/nonresident issues, emigration, death, and corporate-tax-heavy DGA cases to manual review or unsupported.
- Fiscal-partner allocation uses `partner.verdeling_box2_inkomen` and should total 100% when applicable.

---

## Box 3 Estimates (Geschat vermogen) — Fictitious Return ONLY

| field_id | Label (NL) | Label (EN) | Section | Required | Evidence Type |
|---|---|---|---|---|---|
| `box3.geschatte_banktegoeden` | Geschatte banktegoeden op 1 januari 2026 | Estimated bank balances on 1 Jan 2026 | Box 3 — Bezittingen | conditional | Recent bank statements / estimate |
| `box3.geschatte_overige_bezittingen` | Geschatte overige bezittingen op 1 januari 2026 | Estimated other assets on 1 Jan 2026 | Box 3 — Bezittingen | conditional | Recent portfolio / estimate |
| `box3.geschatte_groene_beleggingen_spaartegoeden` | Geschatte groene beleggingen en groene spaartegoeden | Estimated green investments and green savings | Box 3 — Vrijstellingen | optional | Recent green fund / bank statements |
| `box3.geschat_contant_geld` | Geschat contant geld en cadeaubonnen | Estimated cash and gift cards | Box 3 — Bezittingen | optional | User estimate |
| `box3.geschatte_schulden` | Geschatte schulden op 1 januari 2026 | Estimated debts on 1 Jan 2026 | Box 3 — Schulden | conditional | Current debt levels / estimate |

### Box 3 note

Use only this explanatory note: "Werkelijk rendement is not part of provisional 2026."

The validation script rejects provisional field IDs or labels that try to add werkelijk-rendement inputs, calculations, or method choices.

### Notes on box 3 estimates
- Peildatum for the provisional 2026 is 1 January 2026.
- Only the fictitious return method (forfaitair rendement) applies. The portal computes the fictitious return from the asset estimates.
- The heffingsvrij vermogen is applied automatically by the portal.
- Green investments/savings and cash must be identifiable separately because exemptions can change the amount included in banktegoeden or overige bezittingen.

---

## Partner Allocation Estimates

| field_id | Label (NL) | Label (EN) | Section | Required | Evidence Type |
|---|---|---|---|---|---|
| `partner.verdeling_box2_inkomen` | Geschatte verdeling Box 2 inkomen | Estimated Box 2 income allocation | Partner | conditional | User choice / baseline |
| `partner.verdeling_box3_grondslag` | Verdeling grondslag sparen en beleggen | Box 3 base allocation | Partner | conditional | User choice |
| `partner.verdeling_eigenwoning_saldo` | Verdeling saldo eigen woning | Own-home balance allocation | Partner | conditional | User choice |
| `partner.verdeling_aftrekposten` | Verdeling aftrekposten | Deduction allocation | Partner | conditional | User choice |

### Notes on partner allocation estimates
- If there is a fiscal partner and the provisional form asks for allocation, map the allocation of the joint grondslag sparen en beleggen, not individual assets or debts.
- Allocation values are estimates for cash-flow planning. The final allocation is chosen again in the annual 2026 return.
- Box 2 allocation values are estimates or from-baseline and must total 100% when shown for fiscal partners.

---

## Deduction Estimates (Geschatte aftrekposten)

| field_id | Label (NL) | Label (EN) | Section | Required | Evidence Type |
|---|---|---|---|---|---|
| `aftrek.geschatte_alimentatie` | Geschatte alimentatie | Estimated alimony paid | Aftrekposten | conditional | Current alimony arrangement / estimate |
| `aftrek.geschatte_aftrekposten` | Geschatte overige aftrekposten | Estimated other deductions | Aftrekposten | conditional | Estimate based on prior year / current situation |

### Notes on deduction estimates
- The provisional form has fewer deduction fields than the annual return.
- Detailed breakdowns (zorgkosten, giften, lijfrentepremie) are typically combined into a single estimated deductions field or a small number of summary fields.
- Zorgkosten thresholds and lijfrente limits require manual review unless exact reviewed sources and all required inputs are available.
- The taxpayer should estimate conservatively to avoid underpayment.

---

## Fields NOT Present in Provisional

The following annual return fields have no equivalent in the provisional assessment:

| Annual field_id | Reason not in provisional |
|---|---|
| `box3.werkelijk_rendement_*` | Werkelijk rendement is not part of provisional 2026 |
| `aftrek.zorgkosten` | Rolled into general estimated deductions |
| `aftrek.giften_anbi` | Rolled into general estimated deductions |
| `aftrek.giften_cultureel` | Rolled into general estimated deductions |
| `aftrek.lijfrentepremie` | Rolled into general estimated deductions |
| `box1.loonheffing` | Not separately entered; the portal handles withholding |
