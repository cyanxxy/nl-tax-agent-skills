# Provisional Output Contract — Required Sections and Validation Rules

## Contents

- Purpose
- Required sections
- Amount labeling rules
- Winst uit onderneming forecast rule
- Voorlopige aanslag Zorgverzekeringswet -- REQUIRED companion item
- Rollover-trap check -- REQUIRED
- Box 3 validation rule — CRITICAL
- Box 2 validation rule
- Field map requirements
- Change subflow validation rules
- Stopzetten validation rules
- Sources used section — REQUIRED
- Sources used
- Not submission advice footer — REQUIRED
- File output rules
- Validation checklist

## Purpose

This document defines the mandatory output sections, labeling requirements, and validation rules for every provisional assessment workpack. A workpack that violates any rule in this contract is invalid and must not be delivered.

---

## Required sections

Every provisional workpack (`workspace/provisional/2026/provisional-pack.md`) MUST contain all of the following sections from the template:

| Section                     | Required for subflow(s)                   |
|-----------------------------|-------------------------------------------|
| Subflow identifier          | all                                       |
| Scope                       | all                                       |
| Sources used                | all                                       |
| Existing baseline           | all (may be "No existing baseline" for request) |
| Current-year estimates      | request, change                           |
| Delta summary               | change                                    |
| Review questions            | review                                    |
| Stopzetten outcome          | stopzetten                                |
| Income estimate             | request, change                           |
| Winst uit onderneming forecast | request, change                        |
| Own-home estimate           | request, change                           |
| Box 2 provisional estimate  | request, change                           |
| Box 3 provisional estimate  | request, change                           |
| Deductions estimate         | request, change                           |
| Field map summary           | request, change                           |
| User-stated values index    | all                                       |
| Missing information         | all                                       |
| Assumptions                 | all                                       |
| Human review checklist      | all                                       |
| Not submission advice       | all                                       |

Sections not applicable to the current subflow must be explicitly marked as "N/A — not applicable for [subflow]" rather than omitted.

---

## Amount labeling rules

Every monetary amount in the workpack MUST be labeled with one of:

- **estimate** — a forward-looking projection provided by the taxpayer for 2026
- **from-baseline** — a value carried from an existing voorlopige aanslag or prior-year data

Do NOT present any amount without a label. Unlabeled amounts create ambiguity about whether they are actuals, estimates, or inherited values.

Box 2 provisional amounts MUST also be labeled this way. This applies to estimated regular benefits, estimated disposal benefits, estimated costs, estimated dividend withholding tax, estimated fictitious regular benefit from BV lending, and partner allocation values.

## Winst uit onderneming forecast rule

For an eenmanszaak/ZZP, the workpack may contain one sourced, user-reviewed
full-year forecast in the portal section `Winst uit onderneming`:
`onderneming.geschatte_winst`. It MUST carry provenance, an estimate or
from-baseline label, and manual review. Do not use the generic Box 1
other-income field as a business-profit substitute.

`_shared/knowledge/years/2026/provisional/winst-provisional-2026.md` is
canonical for this field and for every 2026 business figure named anywhere in
this contract. Read each figure there; never restate one from memory.

**Confirmed field semantics -- REQUIRED.** The workpack MUST record the estimate
on exactly these terms, and the agent MUST state them to the taxpayer before the
amount is recorded:

- the winst the taxpayer expects to earn as ondernemer in 2026;
- taken **before** the ondernemersaftrek and **before** the
  MKB-winstvrijstelling -- an estimate already reduced by either one is too low;
- excluding the btw payable and the btw reclaimable;
- an expected loss entered as a negative amount, with a minus sign;
- one business figure, and only one.

The provisional workpack MUST NOT prepare annual profit-and-loss or balance
accounts, zelfstandigenaftrek, startersaftrek, ondernemersaftrek,
MKB-winstvrijstelling, KIA, a bijdrage Zvw amount, cessation profit, or final
tax. The 2026 form has no amount field for any of them. Complex forms and events
route to terminal manual review.

When a forecast applies, it MUST also appear as its own row in the change
delta and in the Box 1 income-before-own-home rollup. A workpack that records
`onderneming.geschatte_winst` but drops it from those review totals is invalid.

### Examples

- "Employment income: EUR 45,000 (estimate)" — correct
- "Employment income: EUR 45,000 (from-baseline)" — correct
- "Employment income: EUR 45,000" — INVALID, missing label

---

## Voorlopige aanslag Zorgverzekeringswet -- REQUIRED companion item

`_shared/knowledge/years/2026/provisional/zvw-provisional-2026.md` is canonical
for the 2026 percentage, the maximumbijdrage-inkomen, and every other figure in
this section. Read them there; never restate one from memory, and never multiply
the percentage by the ceiling.

Where the taxpayer has winst uit onderneming or income from work performed
outside employment, the workpack MUST raise the inkomensafhankelijke bijdrage
Zorgverzekeringswet without waiting to be asked, and MUST record:

- that such a taxpayer receives **two** aanslagen -- one for the
  inkomstenbelasting/premie volksverzekeringen and a separate one for the
  bijdrage Zvw -- and may hold a separate **voorlopige aanslag
  Zorgverzekeringswet 2026** alongside the income-tax one;
- that the voorlopige aanslag Zvw has its **own change route**. No reviewed
  source establishes whether a change to the income-tax voorlopige aanslag is
  coupled to the Zvw assessment, so the taxpayer must check the Zvw assessment
  separately and the workpack records what they find;
- the answer to the direct question "Have you (the taxpayer) received a
  voorlopige aanslag Zorgverzekeringswet for 2026, and what income estimate does
  it use?", with provenance -- or an open row in Missing information when the
  taxpayer does not know. Never assume there is none and never enter a zero;
- a human-subject action line, for example: "You (the taxpayer) also check your
  voorlopige aanslag Zorgverzekeringswet 2026 in Mijn Belastingdienst and change
  it separately if its estimate is no longer right.";
- that the Zvw base is the belastbare winst, a different figure from
  `onderneming.geschatte_winst`, which is taken before the ondernemersaftrek and
  the MKB-winstvrijstelling;
- that the bijdrage Zvw is not deductible and is never subtracted from the
  profit estimate.

The Zvw is reported **alongside** the income-tax dataset and is never merged into
it. The workpack MUST NOT compute a bijdrage Zvw amount, MUST NOT emit a field,
portal instruction, or checklist row that has the taxpayer entering a Zvw amount
in the income-tax voorlopige-aanslag form, and MUST NOT state Zvw instalment,
deadline, payment, or refund timing. Those, and any exception regime, are
manual-review items; the Belastingdienst calculates the bijdrage.

The income-tax `field-map.yaml` MUST contain no Zvw field or value whatsoever:
no Zvw `field_id`, label, note, amount, baseline, estimate, or manual-entry row.
The separate assessment belongs only in the workpack companion section and the
human review action.

---

## Rollover-trap check -- REQUIRED

A voorlopige aanslag 2026 that the Belastingdienst extended automatically, or
that opened pre-filled from an earlier return, rests on an earlier year's
figures. No reviewed source states that a carried-over business estimate is
recalculated for the new year's ondernemersaftrek, and the zelfstandigenaftrek
has fallen sharply between the two years -- both amounts are in
`winst-provisional-2026.md`. A 2026 calculation still resting on the older,
higher zelfstandigenaftrek overstates the deduction, so the taxpayer pays too
little through the year and owes the difference when the final 2026 assessment
is made up.

For every taxpayer whose 2026 voorlopige aanslag was extended automatically or
opened pre-filled, the workpack MUST record the answers to:

1. Which year's figures does the current voorlopige aanslag 2026 rest on?
2. What profit estimate does it use, and is that still the taxpayer's own best
   estimate for 2026?
3. Does the taxpayer's own reasoning about the amount still use a
   zelfstandigenaftrek from an earlier year?

Flag any calculation that still rests on a zelfstandigenaftrek above the 2026
amount in `winst-provisional-2026.md`, and put the finding in words the taxpayer
can act on. An unanswered question stays an open row in Missing information;
never fill the gap with an assumption and never enter a zero.

A change made to the voorlopige aanslag 2025 after the cut-off date stated in
`winst-provisional-2026.md` is not carried into 2026 automatically. Where the
taxpayer made such a late correction, re-derive the 2026 estimate from their own
current forecast rather than assuming it followed.

---

## Box 3 validation rule — CRITICAL

**Box 3 MUST use the fictitious return method (forfaitair rendement) only.**

### FAIL conditions

The workpack MUST be rejected if any of the following are true:

- Werkelijk rendement is referenced as a data input
- Werkelijk rendement is requested from the user
- Werkelijk rendement is used in any calculation
- The workpack offers any method choice for box 3
- Box 3 calculation uses any method other than the three-category fictitious return

### Required box 3 structure

The box 3 section MUST follow this structure:

1. Categorie I: Banktegoeden — amount as of 1 January 2026
2. Categorie II: Overige bezittingen — amount as of 1 January 2026
3. Categorie III: qualifying Box 3 schulden — amount as of 1 January 2026,
   after the official inclusion/exclusion screen. A generic non-own-home debt
   is not accepted automatically; unresolved debts remain manual-review rows
   outside the totals
4. Aftrekbare schulden after the debt threshold
5. Belastbaar rendement
6. Rendementsgrondslag
7. Grondslag sparen en beleggen
8. Aandeel in rendementsgrondslag
9. Box 3 income
10. Box 3 tax at the rate from `box3-provisional.md`

The official 2026 page says 3 decimals in its general step but shows 2 decimals
in worked examples. If a review estimate displays the aandeel, the workpack
MUST identify the convention used and state that the live portal calculation
and resulting beschikking are authoritative; it must not claim either display
rule is the binding portal algorithm.

### Required box 3 note

Every workpack with a box 3 section MUST include:

> Werkelijk rendement is not part of provisional 2026.

No additional werkelijk-rendement input instructions, fields, calculations, or method-choice wording may be added.

---

## Box 2 validation rule

Standard Box 2 provisional preparation is supported for `provisional_2026` request and change flows.

The workpack and field map may include:

- `box2.geschatte_reguliere_voordelen`
- `box2.geschatte_vervreemdingsvoordelen`
- `box2.geschatte_kosten`
- `box2.geschatte_ingehouden_dividendbelasting`
- `box2.geschat_fictief_regulier_voordeel_bv_lening`
- `partner.verdeling_box2_inkomen`

Every Box 2 amount must be labeled as estimate or from-baseline. Route valuation disputes, emigration, death, restructurings, treaty/nonresident issues, informal capital, non-arm's-length transfers, and corporate-tax-heavy DGA facts to manual review or unsupported.

---

## Field map requirements

The `field-map.yaml` MUST conform to
`nl-tax-field-mapper/templates/field-map-template.yaml` and
`nl-tax-field-mapper/reference/provisional-field-map.md`; `field_id`s must come
from that provisional reference. Conformance is checked by the mapper's own
agent checklist in `nl-tax-field-mapper/reference/mapping-principles.md`,
applying the rule data in `nl-tax-field-mapper/reference/field-map-rules.yaml`;
the taxpayer's review before manual entry is the final check.

---

## Change subflow validation rules

### Full re-entry reminder — REQUIRED

Every change-subflow workpack MUST include this reminder:

> Prepare and verify the complete dataset; the change form requires all applicable categories, not only the changed item.

The reminder must appear:
- In the workpack body (not just in footnotes or appendices)
- Before the field map summary section

### Delta summary — REQUIRED

The change subflow MUST produce a delta summary file at `workspace/provisional/2026/delta-summary.md` containing:

- Baseline values (from existing voorlopige aanslag)
- Current estimate values (from user input)
- Delta per category (difference between baseline and current estimate)
- A non-binding possible direction for future payment/refund, or `uncertain`,
  plus the live-portal/replacement-beschikking caveat
- A separate expected-business-profit row when applicable
- Separate own-home component rows for eigenwoningforfait, total deductible
  own-home costs, any Hillen deduction, and `box1_own_home_balance`

A change-subflow workpack without a delta summary is invalid.

---

## Stopzetten validation rules

Moving abroad requires residency review and is **not a categorical stopzetten reason**. A workpack must route migration facts to the unsupported residency/migration path rather than producing a stopzetten outcome solely from the move.

For review/change context, an **unsolicited** VA from earlier data **may be issued**, but it is **not guaranteed**; do not present a later VA as automatic.

### Current-date cutoff gate -- REQUIRED

Before writing stopzetten instructions, compare the current date to 2026-10-01.
If the current date is on or after 2026-10-01, the workpack MUST NOT include a
stopzetten checklist. It must state that the 2026 stopzetten cutoff has passed
and route the user to review/change or to a separate filing-status review and,
when a return will be filed, annual settlement.

### Structured stopzetten body -- REQUIRED

Every stopzetten-subflow workpack MUST include a `Stopzetten outcome` section in
the body. For a refund case before the cutoff, it MUST include:

- current cash-flow direction: monthly refund
- current-date cutoff result
- the selected refund component and expected effect of stopping: deductions,
  IACK, or algemene heffingskorting
- a separate annual-filing-status note; stopzetten itself does not create a
  universal filing obligation
- manual checklist for the official stopzetten process

For non-stopzetten outcomes, the same section must explicitly state the route
chosen and must not include a refund-stop checklist.

### Payment user routing — REQUIRED

If the user currently PAYS a monthly amount and the amount is incorrect:

- The workpack MUST redirect to the change subflow
- The workpack MUST NOT provide stopzetten guidance for payment correction
- The workpack MUST explain that stopping payments does not reduce the tax obligation
- The session state MUST be mutated before continuing: set `active_workflow: provisional_2026_change`, set `provisional_2026.subflow: change`, copy the payment baseline into the `baseline` subsection, mark `stopzetten_direction` complete with `routed_to_change_payment_case`, and reset `confirm` to `not_started`. This avoids returning to stopzetten on the next turn.

### Refund user guidance — REQUIRED

If the user currently RECEIVES a monthly refund:

- The workpack MUST include a manual checklist for the official Mijn Belastingdienst stopzetten process
- For deductions and IACK, it MUST state that the stop is retroactive to
  1 January 2026 and show already-received amounts as a possible repayment
  controlled by a separate Belastingdienst notice
- For the algemene heffingskorting, it MUST record the chosen first day of the
  month and describe the payment effect as prospective from that selected/next
  payment month
- It MUST keep annual filing conditional on the taxpayer's separate filing
  obligation or choice/eligibility to file

---

## Sources used section — REQUIRED

Every workpack MUST list exactly the `source_id` values in
`session-progress.yaml` → `sources_loaded_by_workflow.provisional_2026`. Do not
copy IDs from the annual ledger; the same ID may appear in both only when it was
independently consulted for both workflows. This provides traceability and
allows verification against the knowledge base.

### Example

```
## Sources used
- bd_box3_2026_provisional
- bd_provisional_request_2026
- bd_provisional_rates_2026
```

---

## Not submission advice footer -- REQUIRED

Every workpack MUST end with the following footer:

> This workpack is a preparation aid. You, the taxpayer or an authorized human,
> must review the figures and perform all portal entry, signing, sending, or
> changes yourself. The assistant must not access or operate Mijn
> Belastingdienst.

A workpack without this footer is invalid.
Do not expand this footer into generic credential boilerplate.

---

## File output rules

| Output file                                       | Subflow(s)       | Required |
|---------------------------------------------------|------------------|----------|
| `workspace/provisional/2026/provisional-pack.md`  | all              | yes      |
| `workspace/provisional/2026/field-map.yaml`       | request, change  | yes      |
| `workspace/provisional/2026/delta-summary.md`     | change           | yes      |
| `workspace/provisional/2026/review-questions.md`  | review           | yes      |
| `workspace/provisional/2026/notes/<section>.yaml` | all              | working files |
| `workspace/shared/assumptions.md`                 | all              | yes      |

These are the deliverables and working files this skill writes; the
`notes/<section>.yaml` files are intermediate per-section working notes under the
skill's own year directory.

### Prohibited output locations

- `workspace/annual/**` — NEVER write to the annual workspace from the provisional skill
- Any path outside `workspace/` — workpack files belong in the workspace only

---

## Validation checklist

Before delivering any workpack, verify:

- [ ] All required sections are present for the applicable subflow
- [ ] User-stated values index lists every `U:` chat-stated value for spot-checking
- [ ] All amounts are labeled (estimate or from-baseline)
- [ ] Box 2 amounts are labeled estimate or from-baseline, when applicable
- [ ] Box 3 uses fictitious method only, with only the required explanatory note for werkelijk rendement
- [ ] Candidate Box 3 debts passed the official inclusion/exclusion screen; unresolved debts remain manual-review rows outside accepted totals
- [ ] Any displayed Box 3 aandeel records the estimate's rounding convention and defers to the live portal/beschikking
- [ ] AOW status is `below_all_year`, `reaches_during_year`, or `aow_all_year`; a transition-year month and manual portal result replace a whole-year table estimate
- [ ] Expected business profit, when applicable, is included in the Box 1 rollup and change delta
- [ ] `onderneming.geschatte_winst` is recorded and explained as the winst before
  ondernemersaftrek and before MKB-winstvrijstelling, excluding btw, with a minus
  sign for an expected loss, and the definition was stated to the taxpayer before
  the amount was recorded
- [ ] The separate voorlopige aanslag Zorgverzekeringswet is raised as a
  companion item with its own change route, no bijdrage amount is computed, and
  no Zvw row enters the income-tax dataset
- [ ] The rollover-trap check was performed when the 2026 voorlopige aanslag was
  extended automatically or opened pre-filled, and any zelfstandigenaftrek above
  the 2026 amount was flagged
- [ ] Own-home review shows the 1 January 2025 WOZ peildatum and all components of `box1_own_home_balance`
- [ ] IACK, ouderenkorting, alleenstaandeouderenkorting, jonggehandicaptenkorting, zorgkosten thresholds, and lijfrente limits are manual-review items unless exact reviewed sources and required inputs are registered
- [ ] Change subflow includes full re-entry reminder
- [ ] Change subflow includes delta summary file
- [ ] Review subflow includes `review-questions.md` following the review-questions template
- [ ] Stopzetten subflow includes a structured `Stopzetten outcome` body
- [ ] Stopzetten cutoff was evaluated against the current date before any checklist was included
- [ ] Stopzetten routes payment users to change subflow
- [ ] Stopzetten distinguishes retroactive deductions/IACK from the prospective monthly algemene-heffingskorting stop, keeps prior repayment in a separate notice, and treats annual filing as a separate question
- [ ] Sources used section lists exactly
  `sources_loaded_by_workflow.provisional_2026`, without copying the annual ledger
- [ ] Not submission advice footer is present
- [ ] No output files written to workspace/annual/
- [ ] Assumptions section is present and complete
- [ ] Missing information section is present
- [ ] Human review checklist is present
