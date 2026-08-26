## Phase 2 — Income compilation

Load `_shared/knowledge/years/2025/annual/box1-rates.md` when this phase starts.

Compile all box 1 income from evidence and user-provided data.

### 2.1 Employment income (loon uit dienstbetrekking)

- Match jaaropgaaf evidence items from the evidence index
- For each employer, copy the amount labelled **loon** or **fiscaal loon** on the
  jaaropgaaf exactly, plus the loonheffing withheld and employer name. Do not
  reconstruct taxable wage from a payslip-style gross amount and do not
  subtract employee-insurance premiums or other year-statement lines.
- The arbeidskorting shown on a jaaropgaaf is the credit already taken into
  account in payroll withholding. Retain it only as an informational
  reconciliation point; it is not the taxable-loon basis and is not a separate
  annual-return field unless the live portal presents an exact matching field.
- Flag if multiple employers are present (may affect tax calculation)
- Flag if any jaaropgaaf has low classification confidence or is marked for review
- If no jaaropgaaf is available but the profile indicates employment: ask for the values in chat (subsection then becomes `chat_only`) or mark the item as missing if the user defers

### 2.2 Pension income

- Match the **payment-year pension statement** showing taxable pension paid and
  withholding. A UPO is **accrual or projection context only** and must not be
  used as payment or withholding evidence.
- For each pension provider: extract gross pension, loonheffing withheld
- Distinguish between employer pension (pensioenuitkering) and AOW (from SVB)
- Use `profile.yaml` → `person.aow_by_tax_year.2025.status` to distinguish below
  AOW age all year, reaching AOW age during 2025, and AOW age for the whole
  year. Preserve `person.aow_by_tax_year.2025.transition_month`; do not select
  a whole-year rate table from a legacy scalar.

### 2.3 Benefit income (uitkeringen)

- Match UWV and SVB jaaropgaven evidence items
- Identify benefit type: WW, WIA/WAO, ZW, Anw, AKW. AKW is **not taxable box 1 income**; retain it only as household context and exclude it from taxable
  totals.
- Extract gross benefit amount and loonheffing withheld
- Do not apply a blanket arbeidskorting rule to benefits. For ZW (Ziektewet) and
  WAZO, eligibility is **conditional** and depends on the employment
  relationship (dienstbetrekking). Ask whether the taxpayer was still employed
  when the benefit was received; unresolved cases remain manual review.

### 2.3A Company car and stock options

- For a company car (auto van de zaak / bijtelling), record whether the taxpayer
  can substantiate **500 private kilometres or fewer**. Confirm the date of
  first admission, vehicle regime, emissions/fuel facts, catalogue value, and
  private-use evidence. If these are not known, withhold the rate and keep the
  outcome as manual review; do not present a default rate.
- For stock options, **tradability** is the **default tax point**. By default,
  taxation follows when acquired shares become tradable. Immediate-tradability
  cases and any election to use exercise as the tax point require the employer
  statement and manual review.
- For RSUs, restricted shares, employee shares, and other equity compensation,
  do not assume vesting is always the Dutch tax point. Collect the award type,
  grant/vesting/delivery/sale events, employer equity statement, payslip, and
  jaaropgaaf treatment. Unclear instruments, foreign payroll, or cross-border
  service periods remain manual review and outside standard totals.

### 2.4 Other box 1 income

- Check for **winst uit onderneming** (eenmanszaak / ZZP). If present, set `business.has_onderneming: true` and prepare it in Phase 2A, not here. Distinguish it from resultaat uit overige werkzaamheden: winst uit onderneming is the ondernemer case; resultaat uit overige werkzaamheden is the residual freelance case.
- Check for income from other activities (**resultaat uit overige
  werkzaamheden**). This is a prepared path, not a dead end: load
  `_shared/knowledge/years/2025/entrepreneur/row-en-dba-2025.md`, run its bron
  van inkomen pre-screen, and prepare the ROW result from the opbrengsten and
  the costs that note allows. Ondernemersaftrek, MKB-winstvrijstelling and
  investeringsaftrek are ondernemer facilities and never apply to a ROW result;
  the bijdrage Zvw does, per `zvw-2025.md`. Keep the canonical
  `business.has_onderneming: no` hook for the winst section, and route anything
  the note leaves open to manual review rather than estimating it.
- Check for alimentatie received (taxable as box 1 income) and route to manual review unless exact reviewed sources and field-map support have been added.
- Check for any other income sources mentioned in the profile or evidence and keep them out of standard calculations until source-backed.

### 2.5 Income summary

- Total the supported box 1 income sources. The **belastbare winst uit
  onderneming** derived in Phase 2A is one of them: include it in this total,
  cited to the Phase 2A chain, and include a prepared resultaat uit overige
  werkzaamheden alongside it. A business line still under a Phase 2A
  manual-review routing marker stays outside the total and is shown as a
  blocker row.
- Total all loonheffing withheld (this contributes to the official result; do
  not predict the refund or amount due from withholding alone)
- Note any income items without supporting evidence

---
