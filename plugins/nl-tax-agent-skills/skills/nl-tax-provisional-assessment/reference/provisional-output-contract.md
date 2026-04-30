# Provisional Output Contract — Required Sections and Validation Rules

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
| Income estimate             | request, change                           |
| Own-home estimate           | request, change                           |
| Box 3 provisional estimate  | request, change                           |
| Deductions estimate         | request, change                           |
| Field map summary           | request, change                           |
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

### Examples

- "Employment income: EUR 45,000 (estimate)" — correct
- "Employment income: EUR 45,000 (from-baseline)" — correct
- "Employment income: EUR 45,000" — INVALID, missing label

---

## Box 3 validation rule — CRITICAL

**Box 3 MUST use the fictitious return method (forfaitair rendement) only.**

### FAIL conditions

The workpack MUST be rejected if any of the following are true:

- Werkelijk rendement (actual return) is referenced as a data input
- Werkelijk rendement is collected from the user
- Werkelijk rendement is used in any calculation
- The workpack offers a choice between fictitious and actual return methods
- Box 3 calculation uses any method other than the three-category fictitious return

### Required box 3 structure

The box 3 section MUST follow this structure:

1. Categorie I: Banktegoeden — amount as of 1 January 2026
2. Categorie II: Overige bezittingen — amount as of 1 January 2026
3. Categorie III: Schulden — amount as of 1 January 2026 (excluding eigenwoningschuld)
4. Heffingsvrij vermogen — deducted from rendementsgrondslag
5. Weighted fictitious return percentage — calculated from category composition
6. Forfaitair rendement — rendementsgrondslag times weighted percentage
7. Box 3 tax — forfaitair rendement times 36%

### Required box 3 note

Every workpack with a box 3 section MUST include:

> For the 2026 voorlopige aanslag, use the box 3 categories and values required for the provisional fictitious calculation. Werkelijk rendement is not part of the provisional calculation; it may become relevant later in the annual 2026 return.

---

## Change subflow validation rules

### Full re-entry reminder — REQUIRED

Every change-subflow workpack MUST include this reminder:

> When changing your voorlopige aanslag, you must enter ALL data again — not only the items that changed. The new voorlopige aanslag replaces the previous one entirely.

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

### Payment user routing — REQUIRED

If the user currently PAYS a monthly amount and the amount is incorrect:

- The workpack MUST redirect to the change subflow
- The workpack MUST NOT provide stopzetten guidance for payment correction
- The workpack MUST explain that stopping payments does not reduce the tax obligation

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

## Not submission advice footer — REQUIRED

Every workpack MUST end with the following footer:

> This workpack is a preparation aid. It does not constitute tax advice, does not submit a request, and does not interact with the Belastingdienst. You must review all information and submit through the official Mijn Belastingdienst portal using your DigiD. Do not share DigiD credentials with this tool.

A workpack without this footer is invalid.

---

## File output rules

| Output file                                       | Subflow(s)       | Required |
|---------------------------------------------------|------------------|----------|
| `workspace/provisional/2026/provisional-pack.md`  | all              | yes      |
| `workspace/provisional/2026/field-map.yaml`       | request, change  | yes      |
| `workspace/provisional/2026/delta-summary.md`     | change           | yes      |
| `workspace/provisional/2026/review-questions.md`  | review           | yes      |
| `workspace/shared/assumptions.md`                 | all              | yes      |

### Prohibited output locations

- `workspace/annual/**` — NEVER write to the annual workspace from the provisional skill
- Any path outside `workspace/` — workpack files belong in the workspace only

---

## Validation checklist

Before delivering any workpack, verify:

- [ ] All required sections are present for the applicable subflow
- [ ] All amounts are labeled (estimate or from-baseline)
- [ ] Box 3 uses fictitious method only — no werkelijk rendement reference
- [ ] Change subflow includes full re-entry reminder
- [ ] Change subflow includes delta summary file
- [ ] Stopzetten routes payment users to change subflow
- [ ] Sources used section lists all source_ids
- [ ] Not submission advice footer is present
- [ ] No output files written to workspace/annual/
- [ ] Assumptions section is present and complete
- [ ] Missing information section is present
- [ ] Human review checklist is present
