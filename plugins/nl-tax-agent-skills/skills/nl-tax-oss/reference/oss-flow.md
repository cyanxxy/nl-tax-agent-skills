# OSS preparation flow

## Resources, statuses and sources

Track `oss_scope`, `oss_transactions`, `oss_corrections`,
`oss_reconciliation`, `confirm`, with statuses not_started, in_progress,
complete, chat_only or deferred and each section's open Q-IDs. Complete/chat_only
records whether sourced answers are established, not whether tax review cleared.

Read `../nl-tax-shared-resources/knowledge/vat-cross-border/oss.md` and the
applicable named entries in `../nl-tax-shared-resources/source-register.yaml`.
Use bd_oss_reporting, eu_oss_scope, eu_oss_registration and eu_oss_declare_pay
for ordinary scheme/period preparation. For non_union also consult
bd_oss_non_union and bd_oss_non_union_reporting; for threshold screening use
bd_oss_distance_threshold; for IOSS use bd_ioss_scope and
eu_ioss_explanatory_notes. Consult eu_ioss_customs_addendum_2026 only for
relevant 2026 IOSS taxable-base questions. Record only applicable sources
actually relied upon once in Sources used and sources_loaded. Future 2027
rules and 2026 customs treatment never establish a 2025 filing amount.
Required stale/unreviewed sources and form coverage stay visible blockers;
no successful fetch creates a human review attestation.

For shared documents use
`../nl-tax-shared-resources/reference/evidence-types.md` and
`../nl-tax-shared-resources/reference/extraction-boundaries.md`. Read evidence
where shared, assign stable ev_NNN IDs and record only necessary tax facts.
Chat inputs use user_chat, verbatim short quote/date. Preserve conflicting
inputs as needs review. Unknowns receive stable Q/M IDs and never become zero.

## Scheme and period

Confirm scheme registration, effective dates, identification state Netherlands,
business/fixed establishments, year/period/exact dates, prior filing status,
any intermediary appointment and screening outcome. Read the note's scheme
matrix; a Dutch-established ZZP does not qualify for non_union merely because
it sells abroad. The non_union workflow is for an actually eligible non-EU
supplier with Netherlands identification. If identification is elsewhere,
explain the separate national process and keep scope unresolved.

Union/non_union take calendar quarters, IOSS calendar months. Confirm active
registration and a sourced deadline, including nil-return and correction-only
periods. Never substitute the domestic VAT assignment. A period still in
progress is a forecast draft; it cannot be presented as a closed period ready
to file. Sourced no-sales plus no-corrections answers establish nil, while zero
net VAT alone does not. Registration termination, past deadline or official
notice needs human follow-up without invented penalties/payment instructions.

Screen threshold/current-and-prior-year figures, effective elections, KOR/
EU-KOR, type of customer, country place of supply, service establishments,
goods dispatch location, marketplace roles and registration overlap. Do not
automatically add every foreign consumer sale to OSS. Excluded/current
domestic or exempt transactions receive a separate evidenced exclusion row.
For IOSS confirm consignment intrinsic value, non-excise goods, import route,
payment-acceptance date and supplied base breakdown; include the 2026 customs
change screen when relevant without computing customs liabilities.

## Current transaction and rate grid

Use a stable group alias for each consumption-country/rate/supply-kind/origin
combination. Record supplier establishment/dispatch country as needed, correct
supply/payment basis, exclusive taxable base, currency, rate, VAT charged,
destination evidence, category-specific official rate evidence and human
confirmation date. Rates are facts with provenance, not guesses from a country.
For Union distinguish goods and services and relevant dispatch/establishment
origins. Non_union contains services; IOSS contains qualifying imported goods.

Aggregate transaction groups in original currency, show actual source VAT
and independently check base times verified rate where appropriate. Resolve
deviations instead of replacing actual accounting VAT with a formula.
For foreign currency show ECB period-end rate/date, quotation direction and
conversion formula; no bank FX charge or remembered rate substitutes for it.
Use the human-supplied ECB reference rate for the period's last day or, when
the ECB published none that day, the rate of the next ECB publication day, as
the note states; record which date applied. Never use an earlier date, a bank
rate or a remembered rate. Retain cents and confirm actual form precision;
do not import domestic VAT favorable whole-euro rounding.

Owner IDs are `oss.row.<alias>.taxable_base` and
`oss.row.<alias>.vat_amount`. Dimensions identify scheme, member_state
(consumption country), rate and supply_kind (goods or services), plus origin
where relevant. Northern Ireland consumers of Union-scheme goods use
member_state XI under the note's specialist-review question; Northern Ireland
services are not Union-scheme EU supplies, and GB is never a consumption
state.
Keep group aliases non-identifying. The mapper's own reference controls final
map syntax; labels are conceptual review labels until form coverage is reviewed.

## Corrections to previously filed periods

Collect original scheme/year/period, actual filed country VAT, changes already
reported in later returns, target corrected country VAT, error/credit-note
reason, date and evidence. A prepared file is not proof of a filed figure.
Remaining delta = target corrected VAT minus original declared VAT minus
prior reported correction deltas. The active current-period workpack records
that remaining delta separately, with original_period dimension and source
components. A correction cannot be moved to another scheme or consumption
country to make a balance look better.

Apply the note's later-return correction route and three-year window measured
from the original due date. After that window/ended registration route the
human to the consumption state's process. No domestic suppletie substitutes
for OSS correction. A later credit note belongs to its original supplied
period's correction, not both current negative turnover and correction.
An error found before filing is fixed in the unfiled current figures and does
not also create a prior-return correction. Record no-corrections only from a
sourced answer. Corrections use distinct non-identifying aliases and the mapper
reference `../nl-tax-field-mapper/reference/cross-border-field-map.md` for IDs.

## Country reconciliation and final review

For each consumption country show current base/VAT totals by verified rate,
then signed earlier-period VAT deltas separately. Balance(country) = current
VAT(country) + sum(corrections(country)). Payable = sum(max(0,balance(country)))
across countries. Show max(0,-balance(country)) separately for refund review
by that state; never reduce a different state's payable by it. Current-supply
VAT rows cannot be negative; negative corrections can be valid.

Reconcile source export totals, scheme exclusions, current grid, conversion,
country correction balances and accounting control totals. Input VAT never
reduces OSS payable. Demonstrate every included transaction appears once,
and preserve the separate domestic VAT/ICP follow-up rather than double-
reporting foreign VAT there. Differences, rate uncertainty, original-return
gaps or unverified scheme status stay draft.

Review those facts with the taxpayer and ask a scoped generation question.
After acceptance set confirm complete and generation_confirmed true, run
`reference/oss-output-contract.md` and invoke
`../nl-tax-field-mapper/SKILL.md` with oss_return, year/scheme/period, current
row facts/dimensions, original-period correction facts, provenance and owner
readiness. Only it creates the checked map. Pending source/form review cannot
be cleared by arithmetic or taxpayer acceptance. Follow due save and permitted
checklist offers in separate replies under the shared contract.

## Historical correction facts

The active workpack remains 2025/2026. Original-period metadata may refer to
an OSS or IOSS period since the scheme began (Union and non-Union from
2021 Q3, IOSS from 2021 M07). Preserve original filed figures, corrected
difference and rate/treatment evidence. This does not enable preparing a full
historic return or applying today's rate to old transactions. Keep a missing
historic fact open.

Record the original period's due date (the last day of the month after that
period), the window end (that due date plus three years) and this return's
due date. The correction is in time only if this return is submitted on or
before the window end; the original return's actual filing date is
irrelevant. Otherwise route the correction to the consumption state's process
and keep a named blocker; never force it into the current OSS return.
