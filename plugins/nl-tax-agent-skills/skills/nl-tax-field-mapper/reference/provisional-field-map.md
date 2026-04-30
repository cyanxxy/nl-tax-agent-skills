# Provisional Assessment Field Reference (Voorlopige Aanslag 2026)

This reference defines the known fields in the Dutch voorlopige aanslag request or change form for tax year 2026. All values are ESTIMATES of the current/upcoming year -- not actuals from a completed year. The provisional assessment has fewer fields and less detail than the annual return.

---

## Key Differences from Annual Return

1. **All fields are estimates** -- every value is the taxpayer's best projection, not a confirmed amount from evidence.
2. **Fewer detail fields** -- the provisional form asks for totals, not breakdowns per employer or per account.
3. **NO werkelijk rendement** -- the actual return (werkelijk rendement) field does NOT exist in the provisional assessment. This is a HARD RULE. Werkelijk rendement may become relevant when filing the annual 2026 return in 2027, but it is never part of the voorlopige aanslag.
4. **Peildatum is 1 January 2026** -- not 1 January 2025 as in the annual return.
5. **No allocation of prior-year evidence** -- provisional estimates are forward-looking, not evidence-based.

---

## Personal Data (Persoonsgegevens)

| field_id | Label (NL) | Label (EN) | Section | Required | Evidence Type |
|---|---|---|---|---|---|
| `personal.bsn` | BSN (burgerservicenummer) | Citizen service number | Persoonsgegevens | required | Login via DigiD; NOT manually entered; do NOT store |
| `personal.adres` | Adres | Address | Persoonsgegevens | required | Pre-filled after login |

### Notes on personal data
- BSN is used for portal login only. It is NOT a field the taxpayer enters -- DigiD authentication handles identity. The field mapper must NOT include BSN as a data-entry field.
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

## Box 3 Estimates (Geschat vermogen) — Fictitious Return ONLY

| field_id | Label (NL) | Label (EN) | Section | Required | Evidence Type |
|---|---|---|---|---|---|
| `box3.geschatte_banktegoeden` | Geschatte banktegoeden op 1 januari 2026 | Estimated bank balances on 1 Jan 2026 | Box 3 — Bezittingen | conditional | Recent bank statements / estimate |
| `box3.geschatte_overige_bezittingen` | Geschatte overige bezittingen op 1 januari 2026 | Estimated other assets on 1 Jan 2026 | Box 3 — Bezittingen | conditional | Recent portfolio / estimate |
| `box3.geschatte_schulden` | Geschatte schulden op 1 januari 2026 | Estimated debts on 1 Jan 2026 | Box 3 — Schulden | conditional | Current debt levels / estimate |

### HARD RULE: No werkelijk rendement in provisional

The following fields DO NOT EXIST in the provisional assessment and must NEVER appear in a provisional field map:

- `box3.werkelijk_rendement_rente` -- DOES NOT EXIST
- `box3.werkelijk_rendement_dividend` -- DOES NOT EXIST
- `box3.werkelijk_rendement_huur` -- DOES NOT EXIST
- `box3.werkelijk_rendement_waardeverandering` -- DOES NOT EXIST
- `box3.werkelijk_rendement_kosten` -- DOES NOT EXIST

Any field with `werkelijk_rendement` in its `field_id` is INVALID in a provisional field map. The validation script will reject it.

Werkelijk rendement may become relevant when filing the annual 2026 return in 2027, but it is never part of the voorlopige aanslag.

### Notes on box 3 estimates
- Peildatum for the provisional 2026 is 1 January 2026.
- Only the fictitious return method (forfaitair rendement) applies. The portal computes the fictitious return from the asset estimates.
- The heffingsvrij vermogen is applied automatically by the portal.

---

## Deduction Estimates (Geschatte aftrekposten)

| field_id | Label (NL) | Label (EN) | Section | Required | Evidence Type |
|---|---|---|---|---|---|
| `aftrek.geschatte_alimentatie` | Geschatte alimentatie | Estimated alimony paid | Aftrekposten | conditional | Current alimony arrangement / estimate |
| `aftrek.geschatte_aftrekposten` | Geschatte overige aftrekposten | Estimated other deductions | Aftrekposten | conditional | Estimate based on prior year / current situation |

### Notes on deduction estimates
- The provisional form has fewer deduction fields than the annual return.
- Detailed breakdowns (zorgkosten, giften, lijfrentepremie) are typically combined into a single estimated deductions field or a small number of summary fields.
- The taxpayer should estimate conservatively to avoid underpayment.

---

## Fields NOT Present in Provisional

The following annual return fields have no equivalent in the provisional assessment:

| Annual field_id | Reason not in provisional |
|---|---|
| `box3.werkelijk_rendement_*` | Werkelijk rendement is not part of the provisional calculation |
| `aftrek.zorgkosten` | Rolled into general estimated deductions |
| `aftrek.giften_anbi` | Rolled into general estimated deductions |
| `aftrek.giften_cultureel` | Rolled into general estimated deductions |
| `aftrek.lijfrentepremie` | Rolled into general estimated deductions |
| `partner.verdeling_*` | Allocation is simplified in provisional |
| `box1.loonheffing` | Not separately entered; the portal handles withholding |
