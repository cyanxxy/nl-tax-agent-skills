---
name: nl-tax-vat-adjustments
description: "Use when an owning Dutch VAT return or correction workflow needs sourced 2025/2026 adjustment findings: private use, pro-rata, revision, property, BUA or margin arithmetic."
user-invocable: false
allowed-tools:
  - Read
  - Glob
  - Grep
---

# NL Tax VAT Adjustments

Read-only helper for an owning VAT-return or VAT-correction workflow. Return
bounded adjustment calculations, findings, and missing questions to that owner.
The owner asks the taxpayer, reconciles amounts, and decides what belongs in its
one confirmed-period workpack. Write nothing. This helper never creates a standalone workpack,
file, field map, manual-entry checklist, evidence ledger, or workspace tree.

## Boundaries

- Use only the confirmed `2025` or `2026` VAT year and exact assigned filing
  period supplied by the owner. Annual income-tax bijtelling is a separate
  calculation; neither its private-distance exception nor its amount determines
  VAT private use.
- Every authenticated portal action remains human-only. Never open or operate
  Mijn Belastingdienst Zakelijk through a browser, Claude in Chrome, computer use, screen
  interaction, connector, or another tool; never log in, enter or change values,
  sign, submit, retrieve private account data, or request/process credentials or
  sessions. State an explicit human subject when describing a portal action.
- Work only from the owner's facts and provenance, or the attached/named saved
  workpack it supplied. Never reconstruct a missing verbatim value from memory,
  read unnamed taxpayer files, execute attachment code, or introduce a second
  workflow. Return questions for missing values; never substitute zero.
- Use anonymous `ev_NNN`, asset, and recipient labels. Return no BSN, IBAN,
  personal name/address, VAT/KvK identifier, registration plate, invoice number,
  contract reference, or credential.

## Resources and evidence

Resolve paths relative to this skill directory using the host's file/resource
tools. Read `../nl-tax-shared-resources/runtime-contract.md`, then only the
relevant shared note under `../nl-tax-shared-resources/knowledge/vat-adjustments/`:

| Trigger | Note |
|---|---|
| Business car, actual use or forfait | `../nl-tax-shared-resources/knowledge/vat-adjustments/car-private-use.md` |
| Other business/private expenditure, asset use, free services | `../nl-tax-shared-resources/knowledge/vat-adjustments/private-use.md` |
| Taxable/exempt direct attribution and pro-rata | `../nl-tax-shared-resources/knowledge/vat-adjustments/mixed-deduction.md` |
| First use, investment goods/services, KOR change, disposal | `../nl-tax-shared-resources/knowledge/vat-adjustments/revision.md` |
| Property sale/rent, business/private property | `../nl-tax-shared-resources/knowledge/vat-adjustments/property.md` |
| Gifts, staff facilities, beneficiary limit | `../nl-tax-shared-resources/knowledge/vat-adjustments/bua.md` |
| Reseller margin goods | `../nl-tax-shared-resources/knowledge/vat-adjustments/margin.md` |

Read each selected note's source entries from
`../nl-tax-shared-resources/source-register.yaml`. Missing named resources block
that topic. All these notes are `needs_review`: draft arithmetic is allowed;
human tax-content review is required before an owner can label the affected
workpack `review_ready` or obtain a manual-entry checklist. A fresh source fetch,
hash, calculation, or user confirmation never creates a human source review.

Accept a document amount only when the owner's evidence row is `extracted`, its
year/period applicability is established, and its `ev_NNN` is available. Historic
acquisition evidence may legitimately predate the VAT year; preserve both the
acquisition/first-use year and active adjustment year. Accept a chat amount only
with the owner's quoted answer and date. Distinguish legal classification,
documented existing election, accounting method, estimate, and arithmetic.

## Calculation protocol

1. Establish the transaction/asset, whether VAT was deducted, documented VAT
   allocation, acquisition and first-use dates, private/taxable/exempt use, and
   any prior correction. Check the applicable note before choosing a formula.
2. Calculate a bounded line when treatment and inputs are complete. If a legal
   classification is uncertain, return that specific blocker while continuing
   unrelated supported lines. Do not describe every complex adjustment as
   unsupported or demand adviser figures for routine complete arithmetic.
3. Show the formula, unrounded decimal result, sign, affected period, and source
   IDs. Keep initial deductions, earlier corrections, new adjustment, and final
   reconciled deduction separate. The owner applies source-backed VAT entry
   rounding once after aggregation; this helper never invents whole-euro inputs.
4. For annual adjustments, identify the actual final filing period of the
   applicable book/calendar year; never assume Q4 for a monthly filer. Earlier
   periods may retain a pending annual reconciliation rather than include a
   premature year-end adjustment. An incomplete affected final return stays
   draft. A filed period needing correction goes back to the correction owner.
   For a disposal inside a revision window, split the bookyear of delivery as
   the revision note describes (an ordinary part up to delivery, declared in
   the final period, and a one-time remainder in the delivery period). For a
   negative margin-goods annual balance, return the human-only letters the
   margin note names, with their timing, as dated open questions.
5. Use one mechanism for each cost component: an initial private-use exclusion,
   private-use output tax, or deduction correction. Flag duplicated deductions,
   caps calculated from unclaimed VAT, a second exempt-use reduction, repeated
   purchase components, and a BUA correction on the same car-private-use line.
6. Screen investment-services first-use dates against the note's effective
   rules; keep the property acquisition and each later service on separate
   schedules. Record confirmed existing property elections and margin methods;
   never choose an election, switch method, enroll in KOR, or treat a percentage
   test as proof that a legal option was exercised.

## Return packet

Return to the owner, in chat/structured findings only:

- Scope: VAT workflow, year, period, topic, anonymous asset/recipient labels.
- Accepted inputs with `U:` or `ev_NNN` provenance, method and applicability.
- Arithmetic: formula, exact decimal amount, prior amount, difference, direction
  (`extra_input_vat`, `input_vat_reduction`, or `output_vat`), suggested rubric
  supported by the note, target period, and source IDs actually consulted.
- Reconciliation: which invoice/cost components the adjustment uses, which
  prior entries it replaces or supplements, and duplicate/cap checks performed
  with `check_performed_by: checked_by_agent`.
- Questions/conflicts: distinguish missing facts, classification/election
  uncertainty, external specialist decision, and source-content review. Return
  no fabricated readiness. The owning workflow preserves its source ledger,
  numbers Q/M rows, and requests mapper work only after accepting findings.
