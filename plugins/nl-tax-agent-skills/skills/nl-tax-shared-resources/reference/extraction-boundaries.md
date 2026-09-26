# Extraction Boundaries — reading tax documents

This document defines what the owning annual or provisional workflow may and
may not take from a document the user shares, and what it records in the
workpack's `## Documents and sources` table. Recording a document CLASSIFIES
it; it does not INTERPRET it for tax treatment. Tax treatment is decided in the
workflow's own tax sections, from reviewed knowledge notes.

Read each document where the user shared it. Never copy, move, rename, convert,
or rewrite it, and never recreate a PDF, image, or spreadsheet through a text
tool.

---

## The `Documents and sources` row

Record one row per document or chat value used:

`ev_NNN | document as named by the user | type | tax year | owner | location (page/section) | values taken | status`

- `ev_NNN`: the next unused ID (`ev_001`, `ev_002`, …). Never renumber a row.
- Document: the name the user gave or the attachment name; for a chat value,
  `chat YYYY-MM-DD` (the date it was stated).
- Type: the canonical token from
  `../nl-tax-shared-resources/reference/evidence-types.md`, or `user_chat` for
  a chat value.
- Values taken: only the labelled amounts and facts the workflow uses, each
  with a short quote when provenance needs one.
- Status: `extracted` or `needs review` (see "Classification certainty").

No file hashes, and no copied content beyond the short quote needed for
provenance. Workpack values from a row cite it as `F:<ev_NNN>`.

---

## What may be recorded

These fields are safe to record in a `Documents and sources` row and the
workpack sections that cite it:

| Field | Example | Notes |
|---|---|---|
| Document type | `jaaropgaaf`, `woz_beschikking` | Classification only |
| Tax year | `2025` | Calendar year the document covers |
| Institution name | `ABN AMRO`, `UWV`, `Gemeente Amsterdam` | Employer, bank, insurer, or authority |
| Summary totals | `bruto loon: 45000`, `WOZ-waarde: 320000` | Amounts visible on the face of the document |
| Account identifiers | `****1234` | Last 4 digits ONLY, and only when needed to tell two accounts at the same provider apart |
| Dates | `2025-01-01`, `peildatum: 01-01-2025` | Document dates, valuation dates, coverage periods |
| Owner indication | `taxpayer` or `partner` | Based on name on the document; the name itself is not recorded |

A provider name plus tax year identifies a document; no reference number is
needed.

---

## What may not be extracted or stored

These items must NOT appear in the conversation recap, the workpack, or any
other output:

| Prohibited item | Handling |
|---|---|
| Full BSN (burgerservicenummer) | Not extracted — record document type, year, and amounts instead |
| Full IBAN or account number | Not extracted — record the relevant amounts, not the account number |
| Policy, contract, or aanslag numbers (polisnummer, contractnummer, aanslagnummer, kenmerk) | Not extracted — identify the document by provider name and tax year |
| Personal medical details | Extract total amounts only (e.g. `totaal zorgkosten: 1200`), never diagnoses, treatments, or provider names beyond the insurer |
| Passwords or PINs | Never extract, never store |
| Photos of identity documents | Note only that an identity document is present — do not extract details |

---

## Classifying is not deciding

Reading and recording a document never decides tax treatment. These decisions
are made elsewhere:

| Decision | Where it is made |
|---|---|
| Whether an amount is deductible | The workflow's deductions section, from the reviewed note |
| Which box (1, 2, or 3) an item belongs to | The workflow's tax sections, from the reviewed notes |
| Selecting a partner allocation | The taxpayers, after scenario review |
| Whether a voorlopige aanslag amount is correct | The provisional workflow's delta review |
| Whether a gift qualifies for the giftenaftrek | The workflow's deductions section, from the reviewed note |
| Whether medical expenses exceed the drempel | The workflow's deductions section, from the reviewed note |
| How to split eigenwoningforfait between partners | The own-home section and the taxpayers' allocation choice |

A row may carry a short observation (for example "document mentions ANBI
status") but never a tax conclusion.

---

## Classification certainty

Set each row's status from how certain the classification and the values are:

| Certainty | Meaning | Row status |
|---|---|---|
| Clear | Document type is clear from content, naming, and structure | `extracted` (unless another issue applies) |
| Probable | Classification is likely but some ambiguity exists | `needs review`, with a note explaining the ambiguity |
| Uncertain | Document could be one of several types | `needs review`, with a note listing candidate types |
| Unclassifiable | No known type fits | type `other`, `needs review` |

### Factors that increase certainty
- File name matches a known pattern for the type
- Document header or title matches the type
- Expected fields are present and populated
- Tax year is clearly stated

### Factors that decrease certainty
- File name is generic (e.g. `scan001.pdf`)
- Document is in a language other than Dutch
- Multiple document types appear in one file
- Key fields are missing or illegible
- Document appears to be a draft or incomplete

Ask the user about a `needs review` row only when it matters to the active
section. When two documents, or a document and a chat value, disagree, keep
both rows, mark them `needs review`, describe the conflict, and ask which value
controls; never choose silently.

If a document cannot be read (corrupt, encrypted, or an unsupported format),
say so briefly, take no values from it, and ask for a readable copy or the
value in chat.

---

## Key principle

> Recording a document is a librarian's job, not a tax adviser's. The row says
> what the document is and what it shows; the tax section says what it means.
