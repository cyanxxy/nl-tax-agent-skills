# Provisional Output Contract — Required Sections and Validation Rules

## Contents

- Purpose
- Required sections
- Amount labeling rules
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

The provisional workpack MUST NOT prepare annual profit-and-loss or balance
accounts, zelfstandigenaftrek, startersaftrek, ondernemersaftrek,
MKB-winstvrijstelling, KIA, Zvw, cessation profit, or final tax. Complex forms
and events route to terminal manual review.

### Examples

- "Employment income: EUR 45,000 (estimate)" — correct
- "Employment income: EUR 45,000 (from-baseline)" — correct
- "Employment income: EUR 45,000" — INVALID, missing label

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
3. Categorie III: Schulden — amount as of 1 January 2026 (excluding eigenwoningschuld)
4. Aftrekbare schulden after the debt threshold
5. Belastbaar rendement
6. Rendementsgrondslag
7. Grondslag sparen en beleggen
8. Aandeel in rendementsgrondslag
9. Box 3 income
10. Box 3 tax at the rate from `box3-provisional.md`

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
from that provisional reference. Where Bash can reach the plugin path, confirm
conformance with `nl-tax-field-mapper/scripts/validate_field_map.py`; otherwise
verify it manually against
`nl-tax-field-mapper/reference/mapping-principles.md`. The script is a
convenience check, not the only way to satisfy the contract.

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
- Expected impact on monthly payment or refund

A change-subflow workpack without a delta summary is invalid.

---

## Stopzetten validation rules

Moving abroad requires residency review and is **not a categorical stopzetten reason**. A workpack must route migration facts to the unsupported residency/migration path rather than producing a stopzetten outcome solely from the move.

For review/change context, an **unsolicited** VA from earlier data **may be issued**, but it is **not guaranteed**; do not present a later VA as automatic.

### Current-date cutoff gate -- REQUIRED

Before writing stopzetten instructions, compare the current date to 2026-10-01.
If the current date is on or after 2026-10-01, the workpack MUST NOT include a
stopzetten checklist. It must state that the 2026 stopzetten cutoff has passed
and route the user to review/change or annual-return settlement as applicable.

### Structured stopzetten body -- REQUIRED

Every stopzetten-subflow workpack MUST include a `Stopzetten outcome` section in
the body. For a refund case before the cutoff, it MUST include:

- current cash-flow direction: monthly refund
- current-date cutoff result
- expected effect of stopping
- annual-return settlement note
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
- The workpack MUST explain the consequences (refunds stop, settlement at annual return)

---

## Sources used section — REQUIRED

Every workpack MUST list the `source_id` values of all knowledge sources used in producing the workpack. This provides traceability and allows verification against the knowledge base.

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

> This workpack is a preparation aid. Review all information against the official Mijn Belastingdienst portal before submitting or changing a voorlopige aanslag.

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
- [ ] IACK, ouderenkorting, alleenstaandeouderenkorting, jonggehandicaptenkorting, zorgkosten thresholds, and lijfrente limits are manual-review items unless exact reviewed sources and required inputs are registered
- [ ] Change subflow includes full re-entry reminder
- [ ] Change subflow includes delta summary file
- [ ] Review subflow includes `review-questions.md` following the review-questions template
- [ ] Stopzetten subflow includes a structured `Stopzetten outcome` body
- [ ] Stopzetten cutoff was evaluated against the current date before any checklist was included
- [ ] Stopzetten routes payment users to change subflow
- [ ] Sources used section lists all source_ids
- [ ] Not submission advice footer is present
- [ ] No output files written to workspace/annual/
- [ ] Assumptions section is present and complete
- [ ] Missing information section is present
- [ ] Human review checklist is present
