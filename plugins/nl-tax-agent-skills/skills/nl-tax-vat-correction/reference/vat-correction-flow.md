# VAT correction preparation flow

## Sections and sources

Track exactly `vat_scope`, `vat_original`, `vat_reconciliation`,
`vat_correction_route`, and `confirm`. Use
`not_started | in_progress | complete | chat_only | deferred` with open
Q-IDs. Complete document input is `complete`; complete chat input is
`chat_only`; sourced not applicable is complete. These do not clear a
treatment/source-review blocker.

Read directly from this skill directory as each topic needs it:

- `../nl-tax-shared-resources/knowledge/vat/corrections.md` — original-period
  comparison, small correction/suppletie threshold and discovery timing.
- `../nl-tax-shared-resources/knowledge/vat/return-and-rubrics.md` — period,
  applicable rubric inventory, totals, whole-euro rounding and human portal.
- `../nl-tax-shared-resources/knowledge/vat/invoices-and-deduction.md` —
  timing and deduction when an invoice/error changes those facts.
- `../nl-tax-shared-resources/knowledge/vat/kor-and-special-cases.md` —
  KOR/foreign-service/special-case treatment when relevant.
- `../nl-tax-vat-adjustments/SKILL.md` — bounded private-use, pro-rata,
  revision, property, BUA and margin findings from its named notes.
- `../nl-tax-icp/SKILL.md` or `../nl-tax-oss/SKILL.md` — separate ICP/OSS
  correction owner when the error belongs to that reporting scheme.

Record only consulted `source_ids` in Sources used / `sources_loaded`;
confirm applicability, content-review status and freshness in the source
register. Missing resources block that topic. An unreviewed required note or
schema is a named `VAT source-content review` blocker. Apply stale-source
warnings once and retain them in human review. No network fetch, hash check,
taxpayer approval or arithmetic test can turn `needs_review` into reviewed.

Read shared evidence where provided, using
`../nl-tax-shared-resources/reference/evidence-types.md` and
`../nl-tax-shared-resources/reference/extraction-boundaries.md`. Keep next
`ev_NNN` stable, preserve conflicting rows as `needs review`, and ask which
controls. Chat inputs get `user_chat`, short quote and date. Stable Q-/M-IDs
record gaps. Never read private portal data or copy/convert evidence. If a
number is no longer visible verbatim, re-confirm it instead of reconstructing
it from a summary.

## Establish the correction case

Confirm original year and assigned period/dates, Netherlands-established
eenmanszaak/ZZP scope, actual filing status, any earlier corrections to that
same period, KOR status/effective dates and relevant treatment screens.
Distinguish a draft filing worksheet from evidence of the filed figures.
The human may provide the submitted-return printout or state its values;
this plugin does not retrieve it. Missing original declared values block
delta/routing readiness. Never reconstruct original VAT from a bank payment.
If the taxpayer reports "underpaid" or "overpaid", establish whether the
declared return figures were wrong or only the payment differed. Correct
declared figures with a payment discrepancy are a separate payment matter;
they do not justify inventing a return correction.

Ask discovery date, error description, affected invoices/rubrics and whether
the correction was already reported. Record a timeline and human follow-up
under the note's current correction timing. A missed timing question remains
visible; do not backdate discovery or promise no penalties/interest.
Establish from the deadline table in `return-and-rubrics.md`
(`bd_vat_return_deadlines`) or the human's own notice whether the original
period's filing and payment deadline had passed on the correction date, and
record the answer with provenance; it decides the route and payment
instructions in `corrections.md`.
For an unfiled period continue `../nl-tax-vat-return/SKILL.md` instead.

## Compare original with corrected full figures

Capture each applicable rubric's originally declared turnover/VAT and the
previously declared payable/refundable balance. Include earlier corrections
only with confirmed evidence and treatment from the note; do not silently choose
a baseline. Rebuild each corrected full rubric from valid records, including
every applicable unchanged rubric. Keep the original declaration immutable.
Use `vat.<rubric>.turnover` / `vat.<rubric>.vat` for the corrected full facts;
the map inventory is `../nl-tax-field-mapper/reference/vat-field-map.md`.

For each rubric show original, corrected and signed difference with source
components. Apply the invoice-period and deduction tests from their notes.
No invoice is counted twice. For a confirmed bounded adjustment, supply the
read-only VAT-adjustments helper with the original period, sourced complete
cost/use/first-use facts and prior corrections. Accept its formula, signed
result, correct-year timing and consulted source IDs into corrected full
rubrics once. Unknown classification/elections stay affected-line blockers;
complete routine private-use/pro-rata/revision arithmetic is supported.
An adviser-provided adjustment needs period/rubric/sign/amount/derivation;
its unsettled basis is not reconstructed. ICP and OSS/IOSS errors route to
their own correction owners, never the domestic small-correction threshold.
Annual adjustment timing uses the actual original final assigned period;
do not add a revised adjustment to every quarter or another return twice.

The owner computes the corrected net VAT balance from corrected complete
rubrics and a separate signed VAT delta against the confirmed original
balance. State the sign convention: positive = additional VAT to pay;
negative = additional refund/reduction. Keep raw calculation and official
whole-euro rounding distinct, applying `corrections.md` to the threshold
measure. Use `vat.total.balance` for the corrected derived display total,
`vat.correction.previous_balance` for the confirmed prior balance, and
`vat.correction.delta` for the derived comparison. The corrected balance
and the delta are internal facts; `vat.correction.previous_balance` is the
suppletie's entry row "Totaalbedrag eerdere btw-aangifte over dit tijdvak".
Do not assert a numbered total field such as 5c/5g. Reconcile original and
corrected totals to the records and leave unexplained differences open.

## Decide and explain the sourced route

For **this original period**, compare the correction magnitude to the
threshold in `corrections.md`, preserving its inclusive small-correction
boundary. Turnover difference alone is not the VAT correction amount.
Do not offset a large payable difference in one period against a refund in
another, or combine multiple periods to pass/fail that boundary. Multi-period
requests get distinct per-period workpacks and route checks. The official
whole-year suppletie option may be mentioned as an option for the human or
an adviser, but it is a human-review route here: never prepare a combined or
batched suppletie, and never record a monthly or quarterly filer's whole
year under the `Y` token, which means only an annual assigned period.
If the original period's deadline had not yet passed on the correction date,
follow `corrections.md` for that case and keep its open small-amount point
as a named human-review question.

- **Small next-return correction:** record the sourced route and each
  correction component. The target is the taxpayer's next (eerstvolgende)
  VAT return not yet filed after discovery; confirm its assigned period with
  the taxpayer and never choose any other later period. The target-period
  VAT return must add these components once to that period's own figures
  with provenance, through `../nl-tax-vat-return/SKILL.md`. Do not replace its full totals with this
  original-period correction delta or silently edit its workpack. If no
  later return is available, retain an unresolved route for human review.
- **Suppletie:** prepare the original period's corrected **full** rubric
  figures, including unchanged applicable rubrics, and keep prior balance
  and delta separate. The human checks the supported correction form and
  exact period personally in Mijn Belastingdienst Zakelijk. Never substitute
  differences into fields asking for corrected total amounts. If the
  corrected figures change rubric 3b, record that the human must also send
  the separate letter with the 3b change to the Central Liaison Office named
  in `corrections.md`; a change to 3b only needs that letter alone.
- **No net VAT delta:** show the underlying rubric differences and consult
  the note; do not infer that a filing correction is unnecessary merely from
  net zero or force it into the small route. Any unsettled reporting treatment
  remains a question for human review.
- **Letter route, outside both routes:** a margin-scheme annual-globalisation
  refund or a refund of an intra-Community acquisition declared in both the
  Netherlands and another EU member state uses neither the suppletie form nor
  the next return. Record it as a letter-route item for human handling; even
  a refund within the small-correction threshold may not be offset in the
  next return here.

The taxpayer or authorized human performs reporting and any payment actions.
For a **small next-return correction**, payment or refund follows the next
return's combined balance. Any payable balance is due by that return's ordinary
deadline, using its genuine payment instructions; there is no separate
suppletie assessment to await.
For a **suppletie**, if the original deadline had not passed on the correction
date, any additional VAT is paid by that deadline using that period's genuine
payment reference; otherwise the human awaits the naheffingsaanslag or
teruggaafbeschikking and uses its details. A letter-route refund follows the
tax office's response to the human's request. A wrong suppletie already filed is
handled as `corrections.md` describes (objection, or a new suppletie only
after a zero-outcome suppletie). Do not invent a kenmerk, notice, refund
date, due date or payment amount.

## Final review and mapping

Present original/revised totals, signed VAT delta, original-period threshold
measure, proposed sourced route, discovery timing and all unresolved items.
Ask one contextual generation question; a natural affirmative to that
immediately preceding question or direct request after the summary confirms
generation. The initial correction request does not. Set `confirm: complete`
and `generation_confirmed: true`; load the template/output contract and run
its checks. Unresolved facts may be shown only in an explicitly marked draft.

Recompute readiness before mapping. `review_ready` needs all applicable
sections complete/chat_only, reviewed required source content and schema,
confirmed original/revised values, clear route, reconciliation and no
blocker. Send the mapper `vat_correction`, year, original period, corrected
full rubric figures, baseline, signed delta, source metadata, owner
readiness and the chosen route (`suppletie`, `next_return`, `letter` or
`human_review`, from the `vat_correction_route` section). The map records that
route in exactly one notes line, `vat_correction_route: <route>`, and only the
`suppletie` route maps `vat.correction.previous_balance`. It alone
authors/checks the map. Small-route drafts must not
present suppletie totals as target-period entries; map only the supported
route-specific records, keeping comparisons internal.

After mapping, offer saving if due, then a human-only checklist in a later
reply only when its gates pass. A source-review or unresolved reporting
route blocker prevents checklist creation. First saving after mapping or
regenerating requires rebuilding the map from recorded facts and every FM-*
check. The owner alone changes facts/rollup, the mapper alone map content,
and the submit companion alone a requested checklist.
