# Provisional Assessment Field Reference (Voorlopige Aanslag 2026)

source_ids: bd_provisional_request_2026, bd_box3_2026_provisional, bd_provisional_rates_2026, bd_eigenwoningforfait_2025_2026, bd_hypotheekrenteaftrek_conditions
workflow: provisional_assessment
tax_year: 2026
status: active
last_reviewed: "2026-07-06"
review_status: reviewed

This reference defines the known fields in the Dutch voorlopige aanslag request or change form for tax year 2026. Portal-prefilled personal rows are documented for portal awareness but are omitted from field-map output. Amounts are forward-looking 2026 estimates or explicitly labeled baseline values -- not annual actuals from a completed year. The provisional assessment has fewer fields and less detail than the annual return.

This map is preparation-only. The taxpayer or an authorized human performs all
authenticated portal entry, review, signing, sending, or changes; the assistant
must not access or operate Mijn Belastingdienst.

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

1. **Amounts are estimates or explicit baselines** -- evidence can support a
   projection, but every current amount remains a taxpayer-reviewed 2026
   estimate; a carried beschikking amount stays labeled `from-baseline`.
2. **Fewer detail fields** -- the provisional form asks for totals, not breakdowns per employer or per account.
3. **Box 3 explanatory note only** -- use this note and no input fields: "Werkelijk rendement is not part of provisional 2026."
4. **Dates differ by section** -- Box 3 assets and qualifying debts use
   peildatum 1 January 2026; the own-home WOZ value uses peildatum
   **1 January 2025**.
5. **Prior-year facts are only baselines** -- evidence may support a
   forward-looking estimate, but do not copy a prior-year amount as if it were
   a 2026 actual or unchanged forecast without taxpayer review.

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
| `onderneming.geschatte_winst` | Geschatte winst uit onderneming | Expected profit from enterprise | Winst uit onderneming | conditional | Sourced, user-reviewed estimate / baseline; manual review required |

### Notes on income estimates
- These are the taxpayer's best estimates for the full year 2026. They may be based on current employment contracts, recent jaaropgaven, or known upcoming changes.
- The portal asks for total amounts, not per-employer breakdowns.
- **Business profit forecast:** use only `onderneming.geschatte_winst` for a
  sourced, user-reviewed full-year forecast in the `Winst uit onderneming`
  section. Set `manual_review_required: true`. Never substitute a generic
  other-income field and never add annual deductions, Zvw, cessation
  profit, or final tax. Preserve it in the workpack's Box 1 rollup and change
  delta even though the field map keeps it as its own portal section.
- **What that one figure means.** The form asks for the profit the taxpayer
  expects to earn as ondernemer in 2026, taken **before** the ondernemersaftrek
  and **before** the mkb-winstvrijstelling, **excluding** the btw payable and
  the btw reclaimable, and entered with a **minus sign** when a loss is
  expected. `_shared/knowledge/years/2026/provisional/winst-provisional-2026.md`
  is canonical for this semantic; never restate it from memory. An estimate that
  has already been reduced by an ondernemersfaciliteit is too low, because the
  portal applies those itself. There is exactly one business figure on the form:
  do not widen the field, do not split it per onderneming, and do not emit any
  other `onderneming.*` field. Ask for the figure rather than deriving it, and
  record a missing forecast as an open question instead of entering a zero.
- **A separate voorlopige aanslag Zvw exists.** An ondernemer normally receives
  two assessments: one for the inkomstenbelasting and premie
  volksverzekeringen, and another for the inkomensafhankelijke bijdrage
  Zorgverzekeringswet. They are separate documents with separate change routes.
  No reviewed source establishes whether a change to the income-tax voorlopige
  aanslag is coupled to the Zvw assessment, so raise this and require the
  taxpayer to check the Zvw assessment separately. Carry any resulting change as
  its own human-only action in the workpack: **you (the taxpayer) or an authorized
  human** change that assessment through its own route. It is never mapped: the
  income-tax field map MUST contain no Zvw field or value, including no Zvw
  `field_id`, label, note, amount, baseline, estimate, or manual-entry row.
  `_shared/knowledge/years/2026/provisional/zvw-provisional-2026.md` is
  canonical; its payment terms and timing are not established there, so route a
  timing question to manual review rather than reusing the income-tax dates.
- If the taxpayer reaches AOW age during 2026, preserve the reviewed transition
  month in the workpack and use the live portal result for affected rates and
  credits. Do not select a whole-year table from a legacy yes/no AOW flag.
- Alleenstaandeouderenkorting concerns entitlement to an AOW pension for a
  single person; never infer it from children or single-parent status.

---

## Own Home Estimates (Geschatte eigen woning)

| field_id | Label (NL) | Label (EN) | Section | Required | Evidence Type |
|---|---|---|---|---|---|
| `eigenwoning.geschatte_woz_waarde` | WOZ-waarde met peildatum 1 januari 2025 | Own-home WOZ value with reference date 1 Jan 2025 | Eigen woning | conditional | 2026 `woz_beschikking` or reviewed estimate for a 2026 purchase |
| `eigenwoning.geschatte_hypotheekrente` | Geschatte hypotheekrente | Estimated mortgage interest | Eigen woning | conditional | Current mortgage terms / `hypotheek_jaaroverzicht` |

### Notes on own-home estimates
- Use the WOZ value with peildatum 1 January 2025, normally shown on the
  municipal WOZ-beschikking issued in early 2026. For a 2026 purchase without
  that value, retain a reviewed estimate and manual-review note; do not carry
  the Box 3 peildatum into the own-home section.
- Mortgage interest estimate is typically the annual interest based on current mortgage terms.
- The workpack must preserve eigenwoningforfait, qualifying financing costs,
  periodic erfpacht/opstal/beklemming, total deductible own-home costs, any
  Hillen deduction, and `box1_own_home_balance` separately. If the live portal
  exposes more granular labels than this minimal field reference, review and
  map them there rather than dropping components or inventing a combined
  mortgage-only total.

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
| `box3.geschatte_schulden` | Geschatte kwalificerende schulden op 1 januari 2026 | Estimated qualifying Box 3 debts on 1 Jan 2026 | Box 3 — Schulden | conditional | Accepted rows after official debt inclusion/exclusion screen; unresolved rows require manual review |

### Box 3 note

Use only this explanatory note: "Werkelijk rendement is not part of provisional 2026."

The validation script rejects provisional field IDs or labels that try to add werkelijk-rendement inputs, calculations, or method choices.

### Notes on box 3 estimates
- Peildatum for the provisional 2026 is 1 January 2026.
- Only the fictitious return method (forfaitair rendement) applies. The portal computes the fictitious return from the asset estimates.
- The heffingsvrij vermogen is applied automatically by the portal.
- Green investments/savings and cash must be identifiable separately because exemptions can change the amount included in banktegoeden or overige bezittingen.
- A debt does not qualify merely because it is not an own-home mortgage. Record
  type and purpose, exclude Box 1/2 debts and published exclusions, and do not
  map unresolved debt into the accepted total.
- The official 2026 Box 3 page says 3 decimals in the general aandeel step but
  displays 2 decimals in examples. The workpack can show a labeled review
  estimate with its display convention; the live portal and resulting
  beschikking are authoritative.

---

## Partner Allocation Estimates

| field_id | Label (NL) | Label (EN) | Section | Required | Evidence Type |
|---|---|---|---|---|---|
| `partner.verdeling_box2_inkomen` | Geschatte verdeling Box 2 inkomen | Estimated Box 2 income allocation | Partner | conditional | Explicit taxpayer choice (`user_chat`) |
| `partner.verdeling_box3_grondslag` | Verdeling grondslag sparen en beleggen | Box 3 base allocation | Partner | conditional | Explicit taxpayer choice (`user_chat`) |
| `partner.verdeling_eigenwoning_saldo` | Verdeling saldo eigen woning | Own-home balance allocation | Partner | conditional | Explicit taxpayer choice (`user_chat`) |
| `partner.verdeling_aftrekposten` | Verdeling aftrekposten | Deduction allocation | Partner | conditional | Explicit taxpayer choice (`user_chat`) |

### Notes on partner allocation estimates
- If there is a fiscal partner and the provisional form asks for allocation, map the allocation of the joint grondslag sparen en beleggen, not individual assets or debts.
- Only map an allocation after the taxpayer explicitly confirms that choice in
  the current conversation. Record it with `source.type: user_chat`, the
  taxpayer's quote, `stated_at`, and `manual_review_required: true`. A baseline,
  calculated scenario, or assistant-generated comparison cannot select it; keep
  the field unresolved otherwise.
- Confirmed allocation values are provisional cash-flow inputs. The taxpayer
  chooses the final allocation again in the annual 2026 return.
- Confirmed Box 2 allocation values must total 100% when shown for fiscal partners.

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
| `onderneming.*` other than `onderneming.geschatte_winst` | Only the dedicated expected-profit forecast is supported in provisional 2026 |
| `onderneming.zelfstandigenaftrek` / `onderneming.startersaftrek` / `onderneming.ondernemersaftrek_totaal` / `onderneming.mkb_winstvrijstelling` / `onderneming.kleinschaligheidsinvesteringsaftrek` | Entrepreneur deductions are annual-2025 only; never applied in a provisional estimate |
| `aftrek.zorgkosten` | Rolled into general estimated deductions |
| `aftrek.giften_anbi` | Rolled into general estimated deductions |
| `aftrek.giften_cultureel` | Rolled into general estimated deductions |
| `aftrek.lijfrentepremie` | Rolled into general estimated deductions |
| `box1.loonheffing` | Not separately entered; the portal handles withholding |
