# Extraction Boundaries — NL Tax Evidence Indexer

This document defines precisely what the evidence indexer may and may not extract, decide, or store. The indexer CLASSIFIES documents — it does not INTERPRET them for tax treatment.

---

## What the indexer MAY extract

These fields are safe to extract and store in the evidence index:

| Field | Example | Notes |
|---|---|---|
| Document type | `jaaropgaaf`, `woz_beschikking` | Classification only |
| Tax year | `2025` | Calendar year the document covers |
| Institution name | `ABN AMRO`, `UWV`, `Gemeente Amsterdam` | Employer, bank, insurer, or authority |
| Summary totals | `bruto loon: 45000`, `WOZ-waarde: 320000` | Amounts visible on the face of the document |
| Account identifiers | `****1234` | Last 4 digits ONLY of account numbers |
| Dates | `2025-01-01`, `peildatum: 01-01-2025` | Document dates, valuation dates, coverage periods |
| Document reference numbers | `kenmerk: BL/12345` | Belastingdienst case numbers, policy numbers |
| Owner indication | `taxpayer` or `partner` | Based on name on the document |

---

## What the indexer MAY NOT extract or store

These items must NOT appear in the evidence index or any output file:

| Prohibited item | Handling |
|---|---|
| Full BSN (burgerservicenummer) | Note `bsn_present: true` only — never store the number itself |
| Full IBAN | Note `iban_present: true` only — never store the full number |
| DigiD credentials | Never extract, never store, never reference. DigiD is NOT evidence |
| Personal medical details | Extract total amounts only (e.g. `totaal zorgkosten: 1200`), never diagnoses, treatments, or provider names beyond the insurer |
| Passwords or PINs | Never extract, never store |
| Photos of identity documents | Note `id_document_present: true` only — do not extract details |

---

## What the indexer MAY NOT decide

Tax treatment decisions are outside the scope of this skill. The indexer must NOT:

| Prohibited decision | Belongs to |
|---|---|
| Whether an amount is deductible | Annual return skill |
| Which box (1, 2, or 3) an item belongs to | Annual return skill |
| Optimal partner allocation | Annual return skill |
| Whether a voorlopige aanslag amount is correct | Provisional assessment skill |
| Whether a gift qualifies for the giftenaftrek | Annual return skill |
| Whether medical expenses exceed the drempel | Annual return skill |
| How to split eigenwoningforfait between partners | Annual return skill |

The indexer may note observations (e.g. `"notes": ["document mentions ANBI status"]`) but must not draw tax conclusions.

---

## Confidence scoring

Each indexed item receives a confidence score reflecting how certain the classification is:

| Score range | Meaning | Action |
|---|---|---|
| **0.90 - 1.00** | High confidence — document type is clear from content, naming, and structure | `review_required: false` (unless other flags are set) |
| **0.70 - 0.89** | Likely correct — classification is probable but some ambiguity exists | `review_required: true` with note explaining the ambiguity |
| **0.50 - 0.69** | Low confidence — document could be one of several types | `review_required: true` with note listing candidate types |
| **0.00 - 0.49** | Very low confidence or unclassifiable | `evidence_type: "other"`, `review_required: true` |

### Factors that increase confidence
- File name matches a known pattern for the type
- Document header or title matches the type
- Expected fields are present and populated
- Tax year is clearly stated

### Factors that decrease confidence
- File name is generic (e.g. `scan001.pdf`)
- Document is in a language other than Dutch
- Multiple document types appear in one file
- Key fields are missing or illegible
- Document appears to be a draft or incomplete

---

## Extraction status values

Each evidence item has an `extraction_status` field:

| Status | Meaning |
|---|---|
| `indexed_only` | File has been cataloged and hashed but content has not been read |
| `classified` | File content has been examined and an evidence type assigned |
| `extracted` | Summary fields have been extracted from the document |
| `failed` | File could not be read or processed (corrupt, encrypted, unsupported format) |

---

## Key principle

> The indexer is a librarian, not a tax advisor. It organizes and labels the evidence. It does not tell you what the evidence means for your tax return.
