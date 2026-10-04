# VAT return preparation flow

## Sections and active resources

Track these exact Appendix A keys: `vat_scope`, `vat_transactions`,
`vat_input_tax`, `vat_reconciliation`, `confirm`. Each has status
`not_started | in_progress | complete | chat_only | deferred` and its open
Q-IDs. Fully sourced document inputs are `complete`; fully supplied chat
inputs are `chat_only`. A sourced not-applicable answer is complete. Neither
status removes a tax-treatment or source-review blocker.

Load the following directly when the active topic needs them; paths resolve
from this skill directory:

| Topic | Required knowledge |
|---|---|
| Scope, period, due date, sales rubrics and totals | `../nl-tax-shared-resources/knowledge/vat/return-and-rubrics.md` |
| Invoice timing, VAT records, business use and input tax | `../nl-tax-shared-resources/knowledge/vat/invoices-and-deduction.md` |
| KOR, foreign services and special-case screening | `../nl-tax-shared-resources/knowledge/vat/kor-and-special-cases.md` |
| Filed-period error | `../nl-tax-shared-resources/knowledge/vat/corrections.md`, then `../nl-tax-vat-correction/SKILL.md` |
| Small earlier-period correction carried into this return (sources `bd_vat_corrections`, `bd_vat_suppletie_explanation`) | `../nl-tax-shared-resources/knowledge/vat/corrections.md` |
| Bounded private use, pro-rata, revision, property, BUA, margin | `../nl-tax-vat-adjustments/SKILL.md` and its relevant named adjustment note |
| EU business-customer declaration | `../nl-tax-icp/SKILL.md` for a separate ICP workflow |
| Confirmed OSS/IOSS scheme | `../nl-tax-oss/SKILL.md` for a separate scheme workflow |

Record every actually consulted note's `source_ids` once in Sources used and
Appendix A `sources_loaded`. Match them in the source register, verify year
applicability and review metadata, and apply its freshness policy. Warn once
for a stale applicable source; keep it in human review. A note marked
`needs_review`, a missing content-review attestation, or an unreviewed required
rubric blocks review readiness and checklist generation. The safe output is
an explicitly marked draft that explains the remaining source-content review.

When reading shared documents, load
`../nl-tax-shared-resources/reference/evidence-types.md` and
`../nl-tax-shared-resources/reference/extraction-boundaries.md`. Read documents
where shared. Assign next `ev_NNN`, never renumber, use canonical types, and
record only needed dates/periods, descriptions, country/business status,
amounts, and labelled tax treatment. Do not extract identifiers. A chat input
is `user_chat`, named `chat YYYY-MM-DD`, with short quote/date. Conflicting
inputs keep both rows as `needs review`; ask which controls. Missing required
facts get stable Q-IDs and M-IDs. No amount is reconstructed from memory or
a summary; re-confirm it if no longer visible verbatim.

## Scope and timing

Confirm year, assigned period, exact dates covered, Netherlands establishment,
eenmanszaak/ZZP form, VAT-obligation status for that period, and whether the
period was already filed. A filed-period error routes to the correction skill
without changing the existing return file. KOR status needs confirmed
participation and effective dates; small turnover alone is never KOR.

Ask whether an earlier-period VAT correction within the small-correction
threshold of `corrections.md` must be included in this return. Include it only when
this return is the first (eerstvolgende) return after the error was
discovered, when the original period, rubric, sign and amount have
provenance (preferably that period's VAT correction workpack or the human's
own record), and when it has not already been carried into another return.
Add it to the rubric where it normally belongs, recorded as its own
carried-correction row with the original period named; never enter it as a
separate total or a single net correction field. A margin-globalisation
refund or a double-declared intra-Community acquisition is never carried
into a return; it is a letter route for human handling.

Confirm invoice-system or legally applicable cash-system treatment from the
knowledge note and taxpayer's records; do not assume receipt date controls.
Record due date only from the official period guidance or a human-supplied
notice, with provenance. For a past due date or missing filing/payment
confirmation, flag human follow-up without inventing a penalty or payment
reference. No-activity periods require an explicit nil-period confirmation
and the obligation check. A true nil period has no reportable turnover,
input VAT, reverse charge, acquisitions or adjustments; a zero net balance
alone is insufficient. Omission does not establish zero or remove filing.

Screen foreign sales, foreign supplier services, reverse charge, imports/EU
acquisitions, mixed exemption, margin, OSS/IOSS, property, and private use.
Routine foreign supplier services may be prepared only after country,
business/service status, place-of-supply/reverse-charge treatment and
deduction entitlement are confirmed under the named notes. Do not collapse
every foreign invoice into one rubric or assume corresponding full deduction.
An EU-supply/ICP obligation routes to `../nl-tax-icp/SKILL.md` for separate
preparation, with matched-coverage domestic VAT 3b reconciliation. Registered
OSS/IOSS preparation routes to `../nl-tax-oss/SKILL.md`; those foreign VAT
amounts do not silently become ordinary domestic VAT liabilities. Use one
owner at a time, preserving unresolved treatment and separate consent/ledgers.

Invoke `../nl-tax-vat-adjustments/SKILL.md` for an applicable adjustment. Supply
confirmed workflow/year/period, item or cost pool, acquisition/first-use dates,
accepted VAT treatment, relevant amounts/use shares, prior deductions and
provenance. Read only its applicable named note. Accept bounded complete
arithmetic with formula/sign/timing/source IDs; reconcile it in the correct
rubric without duplicate exempt/private-use exclusions or purchase components.
Missing classification/election/cost-basis evidence blocks that affected line,
while established other lines continue. For an adviser figure preserve its
period/rubric/sign/amount/derivation, rather than reconstructing an unsettled
basis. Annual adjustments belong in the actual final assigned period, not
Q4 automatically; retain future annual reconciliation as pending earlier.

## Transactions and input tax

For each relevant sales/purchase/credit-note group, record date/period basis,
net turnover, VAT charged or reverse-charged, applicable rubric, amount sign,
currency conversion source where needed, and provenance. Avoid duplicating
an invoice between groups, reporting inclusive turnover as exclusive, or
subtracting a credit note twice. Keep unresolved treatment as a blocker.
Bank receipts and income-tax profit are checks, not substitute VAT totals.

Deduct only input VAT supported by the notes and confirmed business use,
valid invoice/evidence, correct period and deduction entitlement. Distinguish
VAT shown on the supplier invoice from self-assessed reverse-charge VAT and
from deductible input VAT; they are separate facts. Never invent VAT for a
VAT-free/KOR supplier or infer deduction from payment alone. Keep confirmed
non-deductible VAT and unresolved adjustment classification visible.

## Reconciliation

The workflow owner, not the mapper, sums the transaction groups into each
applicable turnover/VAT rubric in `return-and-rubrics.md`. Audit every rubric:
sourced populated total, sourced zero/not applicable, or unresolved. Use
`vat.<rubric>.turnover` / `vat.<rubric>.vat` for rubric facts shared with the
mapper; use `../nl-tax-field-mapper/reference/vat-field-map.md` for exact applicable
identifiers. Do not invent a rubric, total identifier, or portal label.

Show source components and formulas for output VAT, reverse-charge VAT,
eligible input VAT, and the signed payable/refundable balance. Separate
unrounded record totals from the official whole-euro entry amounts and
document the allowed rounding policy from the note. An unresolved base or
negative-adjustment rounding method stays blocked until an adviser confirms
it; do not infer a universal floor/ceiling method. Never recalculate VAT from
a rounded entry base. Reconcile VAT control
accounts/bookkeeping totals and investigate each difference; never plug one
with an assumption. Prove that foreign VAT assessed and deducted is counted
once on each applicable side. A discrepancy stays draft with an open Q-ID.

## Final generation and mapping

Review the period, rubric figures, reconciliation, and remaining blockers.
Ask only a scoped generation question; the opening preparation request is
not final confirmation. Natural acceptance of that immediately preceding
question, or a direct request after reviewing the summary, is enough.

After confirmation, set `confirm: complete` and
`generation_confirmed: true`; load the output contract and template. All
required financial facts must be established or explicitly shown as missing
in a draft; source/treatment blockers never disappear by user acceptance.
Recompute the owner rollup before invoking the mapper. Readiness is
`review_ready` only when all sections are complete/chat_only, every required
source content and rubric schema is reviewed, and no missing fact,
unsupported computation, stale output, or blocking question remains.
Otherwise generation may produce only a clearly marked draft.

Invoke `../nl-tax-field-mapper/SKILL.md` for `vat_return`, passing year,
period, rubric facts, provenance, source-review blockers and owner readiness.
It alone composes/checks the map and shows its summary. Saving after mapping
requires rebuilding from recorded facts and every FM-* check, never copying
an unseen in-memory map. Offer saving next if due, then a human-only
checklist in a later reply only if its gates pass. The submit companion alone
authors a requested checklist; unresolved source review blocks that step.
