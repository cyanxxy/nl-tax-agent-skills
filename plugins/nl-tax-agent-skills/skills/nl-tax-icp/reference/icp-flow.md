# ICP preparation flow

## Sections, sources and evidence

Appendix A keys: `icp_scope`, `icp_transactions`, `icp_corrections`,
`icp_reconciliation`, `confirm`. Each has status
`not_started | in_progress | complete | chat_only | deferred` and open Q-IDs.
Document-complete answers are complete; wholly sourced chat answers are
chat_only. Sourced not-applicable answers count; omitted answers do not.

Read `../nl-tax-shared-resources/knowledge/vat-cross-border/icp.md` and its
named entries in `../nl-tax-shared-resources/source-register.yaml`. For period
timing apply icp.md (source bd_vat_icp and the matching year's ICP
explanation): goods in the period of the invoice date, services in the period
in which the service was supplied, call-off stock in the period in which the
transport began. bd_vat_eu_supply_timing covers acquisitions from other EU
countries and is not authority for ICP supplies; route other unresolved timing
questions to specialist review.
Use the matching year's ICP explanation only; do not load the other year's
PDF source into Sources used. Record every applicable source actually relied
upon once in Sources used and Appendix A `sources_loaded`. Keep required
review/freshness blockers visible; successful access is never attestation.

For shared evidence read
`../nl-tax-shared-resources/reference/evidence-types.md` and
`../nl-tax-shared-resources/reference/extraction-boundaries.md`. Read files
where shared, assign next ev_NNN without renumbering and record only needed
tax facts. Chat inputs are user_chat with a short verbatim quote/date. Preserve
conflicts as needs review. Missing facts receive stable Q001/M001 IDs.

## Confirm coverage and actual customer checks

Establish year, exact period dates, goods/service filing frequencies,
Netherlands establishment, legal form, declaration assignment, already-filed
status, annual permit if relevant, goods turnover in the current and previous
four quarters, KOR/exemption and any special transactions. Apply the note's
threshold test using sourced goods totals only. A VAT quarter does not prove
an ICP quarter; a services declaration may have different coverage from goods.
Nonstandard two-month transitions stay blocked until specifically reviewed.
Record a sourced deadline and flag overdue/unresolved filing for the human.

Assign each distinct customer identity a stable alias such as customer_01.
Ask the human to confirm actual-ID verification date/result and matching
customer business status without supplying the number. Do not treat a country,
invoice label, alias or past successful check alone as valid verification
for the relevant supply. Failed/unavailable/unconfirmed checks stay blocking.
The human retains the actual IDs and enters them separately. Review goods
transport evidence and supplied reverse-charge/place-of-supply classification;
do not treat every EU invoice as an intracommunautaire transaction.

## Transaction grid and credit notes

For each alias/country/transaction kind collect invoice date, supply date,
period basis, net amount excluding VAT, supporting ev/U reference and confirmed
ICP treatment. Keep goods and services separate within a customer's subtotal;
Northern Ireland XI applies only to goods. Do not invent current foreign rates
or charge output VAT in an ICP amount grid.

Allocate goods/services according to the note, then aggregate each current
customer/kind once. Detect duplicate source invoices using the originals
without recording identifiers. Distinguish a current credit note reducing an
earlier valid sale from a correction of a wrongly filed statement; they use
different sections. Retain raw cents and any human-confirmed form precision/
rounding instead of inheriting a domestic VAT rounding algorithm.

Use owner fact IDs `icp.row.<alias>.goods_amount`,
`icp.row.<alias>.services_amount`, and, only for a reviewed special case,
`icp.row.<alias>.triangulation_amount`. Each row carries country and human-ID
verification status/date as dimensions/provenance, and the stable customer
alias as the `customer_alias` dimension. For multiple classified groups within
one customer, use a distinct non-identifying row alias whose `customer_alias`
names that customer; a row alias cannot fabricate another customer's identity. Do not invent a portal box label.

## Earlier statement errors

For every error collect the actual original filed period and amount, target
corrected amount, previously reported corrections and supporting evidence.
The original filed record controls; a prepared draft proves no filing. Compute
remaining signed delta = target corrected amount minus original filed amount
minus corrections already reported. Keep error correction rows out of current
ICP rubric 3 totals and out of the current btw-aangifte rubric 3b
reconciliation. They reconcile to
the affected original period and any separate VAT correction.

For a wrongly used customer identity, preserve old_alias and corrected_alias:
reverse the wrongly declared amount under the old identity and restore it
under the verified identity for the same original period. In the map these are
two correction rows whose `customer_alias` dimensions name the old and the
corrected customer alias. Check the two amounts
cancel at declaration-total level, while recognizing that a separate amount
error may also exist. Full IDs stay with the human. Record correction reason,
original period, signed delta and human verification in an auditable correction
grid. Do not also subtract the same event as a current credit note.

When the financial VAT return is also wrong, route the separate correction to
`../nl-tax-vat-correction/SKILL.md`; an ICP correction does not amend it.
Special triangulation errors stay under matching form review. The owner passes
correction data to the mapper with original-period dimensions; mapper reference
`../nl-tax-field-mapper/reference/cross-border-field-map.md` controls its IDs.

## Same-coverage reconciliation and confirmation

Show sum(goods current rows) + sum(services current rows) + any reviewed
special current rows = current ICP rubric 3 total. Compare it to sourced
btw-aangifte rubric 3b for exactly the same dates; the ICP rubric 3 total must
equal it, and own-goods transfers appear in both. If ICP is monthly and VAT quarterly, show the three
monthly ICP totals together against the quarter; the current single-month
workpack records the other months' sourced totals as comparison evidence,
without combining files or preparing another period. If goods and services
frequencies differ, show both coverage components. A prior-period correction
does not fill a current-period discrepancy. A sourced supply of a new means
of transport to a non-taxable person is reported by the human by letter to the
Central Liaison Office instead of on the ICP; its btw-aangifte rubric is a
named specialist-review item, and any difference it causes stays tied to that
item. Explain and record cents/entry rounding differences; any other
difference is an open blocker and the workpack stays draft.

Review verified identities, every row and original-period correction, coverage,
reconciliation and open questions. Ask a scoped generation question. After
acceptance set generation_confirmed true and confirm complete, then run
`reference/icp-output-contract.md`. Invoke
`../nl-tax-field-mapper/SKILL.md` with `icp_declaration`, year/period, row facts,
dimensions, correction facts, source blockers and owner readiness. It alone
produces the checked map. Pending human source review keeps readiness draft
even if arithmetic balances. Follow any due save offer separately; a checklist
offer comes only after permitted source/map gates.

## Historical correction facts

The active workpack remains 2025/2026. Original-period metadata may refer to
any earlier ICP declaration period. Preserve the original filed amount, the
corrected amount, the signed difference and the evidence, and correct it in
the next opgaaf ICP under ICP rubric 2a (ordinary goods and services) or ICP
rubric 2b (simplified triangulation). This does not enable preparing a full
historic declaration. Keep a missing historic fact open. OSS correction
windows and the OSS consumption-state route do not apply to ICP.
