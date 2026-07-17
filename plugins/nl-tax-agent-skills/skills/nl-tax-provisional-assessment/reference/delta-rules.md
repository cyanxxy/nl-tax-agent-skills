# Delta Rules — Workpack Baseline and Estimate Comparison

## Contents

- Purpose
- Core concepts
- Delta categories
- Visual format
- Impact summary
- Important distinction
- Handling missing baseline data
- Partner changes

## Purpose

This document defines the baseline and current-estimate comparison used inside
provisional assessment workpacks. It helps the taxpayer see what changed and
discuss a possible direction without predicting the monthly amount. It is for
user understanding only -- the Belastingdienst recalculates from the complete
submitted data.

---

## Core concepts

### Baseline

The baseline is the starting point — the existing voorlopige aanslag or prior-year data that represents the last known tax position.

**Sources for the baseline:**
- Existing voorlopige aanslag beschikking (decision letter)
- Prior-year annual return data
- Earlier VVA (Verzoek Voorlopige Aanslag) submitted by the taxpayer
- EVA (Eerste Voorlopige Aanslag): a later **unsolicited** VA based on earlier data **may be issued**, but it is **not guaranteed**

**Rules:**
- If a beschikking is available in the evidence index, use it as the baseline
- If no beschikking is available, ask the user for the key figures from their current voorlopige aanslag
- If no existing voorlopige aanslag exists (request subflow), baseline is "none" — delta is not applicable
- Record the baseline source and date in the delta summary

### Forecast

The forecast is the user's current estimates for 2026 — the forward-looking projection of their tax position.

**Sources for the forecast:**
- User-provided estimates for all income categories
- The dedicated sourced, user-reviewed expected-profit forecast
  (`onderneming.geschatte_winst`) when applicable
- User-provided estimates for all deductions
- User-provided Box 3 assets and candidate debts as of 1 January 2026;
  only debts accepted after the official inclusion/exclusion screen enter the
  forecast total
- Amounts derived from evidence (e.g., mortgage annual statement projecting 2026 interest)

**Rules:**
- Every forecast amount must be labeled as "estimate"
- If an amount is derived from evidence, note the source but still label as "estimate" (evidence-based estimates are still forward-looking)
- The forecast must cover ALL categories, not just the ones that changed

### Delta

The delta is the difference between the baseline and the forecast. It shows
what changed; any cash-flow direction remains a reviewed, non-binding note.

**Rules:**
- Delta = Forecast minus Baseline
- Treat each sign only as a prompt for whole-workpack review. Income,
  deductions, withholding, credits, Box 2/3, partner allocation, and earlier
  provisional amounts can interact, so a single row never determines the
  payment/refund direction.
- Explain a possible direction only after reviewing the complete estimate and
  clearly label it as non-binding.
- Box 3 asset/debt changes require category and allocation review; do not infer
  the final effect from a gross asset or debt delta alone.
- The live portal and replacement beschikking, not these heuristics, determine
  the actual future cash flow.

---

## Delta categories

The delta summary must cover the following categories:

| Category                | Description                                    |
|-------------------------|------------------------------------------------|
| Employment income       | Loon uit dienstbetrekking                      |
| Pension/benefit income  | Pensioen, AOW, uitkeringen                     |
| Expected business profit | Dedicated `onderneming.geschatte_winst`; never fold into generic other income |
| Other income            | Non-business rental, foreign, other            |
| Eigenwoningforfait      | Own-home WOZ peildatum 1 January 2025 × reviewed 2026 percentage |
| Total deductible own-home costs | Mortgage interest + qualifying financing costs + periodic erfpacht/opstal/beklemming |
| Hillen deduction        | Separate reviewed component when applicable    |
| Box 1 own-home balance (`box1_own_home_balance`) | Eigenwoningforfait - total deductible own-home costs - Hillen deduction |
| Box 3 assets            | Total assets in categories I and II            |
| Box 3 qualifying debts  | Accepted qualifying debts in category III; unresolved candidates stay outside the delta total |
| Alimentatie             | Alimony payments                               |
| Other deductions        | Lijfrentepremie, specific care, gifts, other   |
| Partner changes         | Any change in partner status or partner data   |

---

## Visual format

The delta summary must present the comparison in a table format:

```
| Category               | Baseline      | Current Estimate | Delta         | Notes              |
|------------------------|---------------|------------------|---------------|--------------------|
| Employment income      | EUR XX,XXX    | EUR XX,XXX       | +/- EUR X,XXX | [reason if known]  |
| Pension/benefit income | EUR XX,XXX    | EUR XX,XXX       | +/- EUR X,XXX |                    |
| Expected business profit | EUR XX,XXX  | EUR XX,XXX       | +/- EUR X,XXX | dedicated forecast |
| Other income           | EUR XX,XXX    | EUR XX,XXX       | +/- EUR X,XXX |                    |
| Eigenwoningforfait     | EUR XX,XXX    | EUR XX,XXX       | +/- EUR X,XXX |                    |
| Total deductible own-home costs | EUR XX,XXX | EUR XX,XXX | +/- EUR X,XXX |                 |
| Hillen deduction       | EUR XX,XXX    | EUR XX,XXX       | +/- EUR X,XXX | if applicable      |
| Box 1 own-home balance (`box1_own_home_balance`) | EUR XX,XXX | EUR XX,XXX | +/- EUR X,XXX | |
| Box 3 assets           | EUR XX,XXX    | EUR XX,XXX       | +/- EUR X,XXX |                    |
| Box 3 qualifying debts | EUR XX,XXX    | EUR XX,XXX       | +/- EUR X,XXX | accepted rows only |
| Alimentatie            | EUR XX,XXX    | EUR XX,XXX       | +/- EUR X,XXX |                    |
| Other deductions       | EUR XX,XXX    | EUR XX,XXX       | +/- EUR X,XXX |                    |
```

**Notes column:** Include brief reasons for significant changes when the user has provided them (e.g., "salary increase", "mortgage paid off", "started pension").

---

## Impact summary

Below the delta table, include a plain-language summary of the expected impact:

- **If the reviewed estimate points upward:** "The prepared 2026 estimate is
  higher than the current baseline. The portal may therefore show a higher
  future payment or lower future refund."
- **If the reviewed estimate points downward:** "The prepared 2026 estimate is
  lower than the current baseline. The portal may therefore show a lower
  future payment or higher future refund."
- **If the reviewed estimate is similar:** "The prepared 2026 estimate is
  similar to the current baseline, but the portal can still produce a
  different monthly amount."

These are review directions, not predicted cash flows. The Belastingdienst
performs its own recalculation; only the live portal result and replacement
beschikking determine the actual future payment/refund amount and timing.

---

## Important distinction

The delta is for the taxpayer's understanding only. It is NOT submitted to the Belastingdienst. When changing a voorlopige aanslag:

- The Belastingdienst recalculates the entire assessment from the newly submitted data
- The Belastingdienst does not receive or process a "delta" — it receives the full new dataset
- The delta summary helps the taxpayer understand what changed and verify that the new workpack is correct
- The delta summary is a preparation and review tool, not a submission document

---

## Handling missing baseline data

If the baseline is incomplete (e.g., user cannot provide all figures from the existing beschikking):

1. Record which baseline fields are available and which are missing
2. Mark missing baseline fields as "unknown" in the delta table
3. Calculate delta only for categories where both baseline and forecast are available
4. Note in the assumptions section which baseline fields were unavailable
5. Do NOT guess or fabricate baseline values

---

## Partner changes

Partner-related deltas require special handling:

- **New partner:** Baseline has no partner data; forecast includes partner. Delta shows "N/A → EUR XX,XXX" for partner-related items
- **Partner left:** Baseline includes partner data; forecast has no partner. Delta shows "EUR XX,XXX → N/A" for partner-related items
- **Partner income changed:** Standard delta calculation applies
- **Box 3 allocation changed:** Show the allocation split change (e.g., "50/50 → 70/30")
