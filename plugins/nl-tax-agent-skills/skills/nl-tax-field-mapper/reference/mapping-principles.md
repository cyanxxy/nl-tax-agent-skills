# Mapping Principles — Workpack Data to Form Fields

source_ids: bd_annual_data_checklist_2025, bd_provisional_request_2026, bd_box3_2025_calc, bd_box3_2026_provisional
workflow: all
tax_year: all
status: active
last_reviewed: "2026-05-10"
review_status: reviewed

This reference defines how workpack findings are mapped to submission form fields. These principles apply to both annual and provisional field maps.

Only `nl-tax-field-mapper` creates or updates the canonical `field-map.yaml`
next to an annual or provisional workpack. Owning workflow skills pass their
workpack and context to the mapper; they never seed or rewrite the map. The most
recent mapper-validated file at the canonical workflow path is authoritative
for manual entry. Do not create duplicate field-map files, and preserve valid
sourced entries unless the current workpack/reference makes them obsolete.

---

## Contents

- Mapping cardinality
- Confidence scoring
- Source tracking
- Missing fields
- Fields the mapper omits
- Review flagging rules
- Workflow-specific rules
- Manual validation checklist

## Mapping cardinality

### One workpack finding to multiple form fields

A single piece of evidence may provide data for multiple fields. Examples:

- A **jaaropgaaf** provides: `box1.loon`, `box1.loonheffing`, and `box1.arbeidskorting_loon`
- A **hypotheek_jaaroverzicht** provides: `eigenwoning.hypotheekrente` and `eigenwoning.eigenwoningschuld`
- A **jaaroverzicht_bank** provides: `box3.banktegoeden` and (for werkelijk rendement) `box3.werkelijk_rendement_rente`

When this happens, each field entry references the same `evidence_id` but captures a different extracted value.

### Multiple evidence items to one form field

A single form field may require data from multiple sources. Examples:

- `box3.banktegoeden` requires balances from ALL bank accounts on the peildatum -- each from a separate `bankafschrift` or `jaaroverzicht_bank`
- `box1.loon` may combine salary from multiple employers, each with its own `jaaropgaaf`

When this happens, the field entry lists all contributing `evidence_id` values and notes how they were combined (typically summed).

---

## Confidence scoring

Every mapped field receives a confidence score from 0.0 to 1.0 indicating how reliable the mapping is.

### 0.9 to 1.0 — High confidence

- Value comes directly from classified evidence
- Evidence classification confidence is high (0.85+)
- The field-to-evidence mapping is unambiguous
- Example: employment income from a jaaropgaaf classified with 0.95 confidence

### 0.7 to 0.89 — Moderate confidence

- Value comes from evidence, but the classification has some uncertainty
- OR the value required minor interpretation (e.g., identifying which line item is the correct one)
- Example: bank balance from a statement where the account type is slightly ambiguous

### 0.5 to 0.69 — Low confidence

- Value is partially estimated or derived from indirect evidence
- OR the evidence covers a different period and was extrapolated
- OR multiple conflicting sources exist and one was chosen
- Example: estimated annual salary based on a recent payslip multiplied by 12

### Below 0.5 — Very low confidence

- Value is highly estimated with little supporting evidence
- OR the mapping is speculative (e.g., user mentioned an amount verbally without documentation)
- Manual review is CRITICAL for these fields
- Example: estimated other income based on a rough user statement

### Confidence inheritance

When a field's value derives from evidence, the field confidence cannot exceed the evidence classification confidence. If the evidence was classified with 0.80 confidence, the field confidence is at most 0.80 even if the mapping itself is straightforward.

---

## Source tracking

Every field must trace back to a source. Valid source types:

### `evidence`

The value comes from a document in the evidence index.

- `evidence_id`: required -- references an entry in `workspace/taxpayer/evidence-index.yaml`
- The evidence must exist and be classified
- The field mapper does not reclassify evidence -- it uses the classification as-is

### `estimate`

The value is an estimate provided by the taxpayer or derived from available information.

- `evidence_id`: null
- `profile_path`: optional -- path in the taxpayer profile where the estimate was recorded
- All provisional field values default to this source type unless backed by a baseline

### `baseline`

The value comes from an existing voorlopige aanslag or prior-year filing.

- `evidence_id`: optional -- references the beschikking in the evidence index
- Used primarily in provisional change/review subflows
- Represents the "before" value in a delta comparison

### `calculated`

The value was computed from other field values using tax rules.

- `evidence_id`: null
- The calculation logic must be noted (e.g., "eigenwoningforfait = WOZ-waarde * 0.35%")
- The input fields used in the calculation must be listed in `notes`

---

## Missing fields

Fields that are needed for the return/assessment but have no available data are listed in the `missing_fields` section of the field map. Each missing field includes:

| Attribute | Description |
|---|---|
| `field_id` | The field identifier from the field reference |
| `label` | Dutch label of the missing field |
| `reason` | Why the data is not available (e.g., "no jaaropgaaf uploaded", "user did not provide estimate") |
| `blocking` | Boolean -- true if the return cannot be filed without this data |

### Blocking vs non-blocking

- **Blocking:** the field is required and the return/assessment will be incomplete or rejected without it. Example: `box1.loon` when the taxpayer has employment income but no jaaropgaaf.
- **Non-blocking:** the field is optional or the taxpayer's situation may not require it. Example: `aftrek.giften_anbi` when no gift receipts were uploaded but the taxpayer may not have made donations.

Do not use `missing_fields` to satisfy reference coverage for portal-prefilled
personal/identifier rows such as BSN, name, address, date of birth, or IBAN.
Those rows are documented in the field reference for portal awareness, but the
field map omits them because the taxpayer confirms them in the portal rather
than entering sourced values from the workpack.

---

## Fields the mapper omits

The tool never logs in, signs, or submits, and the portal pre-fills identity
rows, so the mapper NEVER creates entries (in `fields` or `missing_fields`) for:

- **Portal credentials** -- username, password, SMS verification codes, or app authentication
- **Bank login credentials** -- these are for evidence collection, not form submission
- **Passwords or tokens** of any kind
- **Session identifiers** or portal navigation state
- **Portal-prefilled personal/identifier rows** -- BSN, IBAN, name, address, and date of birth

This is mapping scope, not a security control — the host environment owns
sensitive-data handling. The validator does still flag a browser/session/submission
(portal-automation) field if one slips into `fields`, because the tool is
prep-only.

### Prefilled personal/identifier fields: omit, never value

BSN, IBAN, name, address, and date of birth are not data-entry fields for this
mapper. The portal pre-fills or confirms them, so the mapper does not create
`fields` rows or `missing_fields` placeholders for them. The validator exempts
required portal-prefilled reference rows from coverage so they do not count as
unpopulated.

---

## Review flagging rules

A field is flagged as `manual_review_required: true` when any of the following apply:

1. Confidence is below 0.7
2. The source type is `estimate` and the value exceeds EUR 5,000
3. Multiple conflicting evidence items exist for the same field
4. The evidence item was flagged for review in the evidence index
5. The field involves a tax choice (e.g., werkelijk rendement vs forfaitair, partner allocation percentage)
6. The value was derived from a calculation with assumptions
7. The field is in a section the taxpayer did not explicitly confirm

---

## Workflow-specific rules

### Annual return fields

- Use evidence-based values wherever possible
- Include werkelijk rendement fields if data is available
- Apply peildatum 1 January 2025 for box 3
- Map all detail fields (per-employer, per-account)

### Provisional assessment fields

- All values are estimates by definition
- NEVER include werkelijk rendement fields
- Apply peildatum 1 January 2026 for box 3
- Map summary fields only (totals, not per-employer breakdowns)
- Set `manual_review_required: true` for any estimate exceeding the baseline by more than 20%

## Manual validation checklist

Use this checklist when the optional validator cannot run. The IDs are the
stable `CHECK_IDS` exposed by `scripts/validate_field_map.py`; complete every
item and record `check_performed_by: checked_by_agent` in the artifact.

- [ ] `FM-METADATA` — required metadata and the check trail are present and valid.
- [ ] `FM-WORKFLOW-YEAR` — workflow and tax year are the supported annual 2025 or provisional 2026 pair.
- [ ] `FM-STRUCTURE` — root, fields, and missing fields have the correct shape; field IDs are unique; no portal-automation fields exist.
- [ ] `FM-SOURCE` — every populated row has a valid source type and its required provenance fields.
- [ ] `FM-CONFIDENCE-FINITE` — confidence is numeric within 0–1 and numeric values are finite.
- [ ] `FM-REFERENCE-COVERAGE` — every required non-prefilled reference field appears in fields or missing fields.
- [ ] `FM-MISSING-READINESS` — unknown rows are also missing, at least one row is populated and sourced, and no required row or workflow blocker remains.
- [ ] `FM-PROVISIONAL-METHOD` — a provisional map contains no werkelijk-rendement field and uses only the allowed expected-profit treatment.
