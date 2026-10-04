# International return preparation flow

## Sections and resources

Track exact Appendix A section keys `international_scope`,
`residence_periods`, `income_assets`, `qualifying_status`, `social_insurance`,
`treaty_review`, `deductions_credits`, `reconciliation`, `confirm`.
Use `not_started | in_progress | complete | chat_only | deferred` with open
Q-IDs. Fully sourced document inputs are complete; complete chat inputs are
chat_only. Neither clears source-content or legal-treatment blockers.
Load `../nl-tax-shared-resources/reference/workflow-scopes.yaml` for the exact
year/form identity, section inventory and current readiness policy. Its
`maximum_readiness: draft` keeps every international workpack and map draft
until maintainers activate the exact scope and reviewed maps; human source
or schema review alone cannot override this ceiling.

Load only the active topic's named resource, relative to this skill directory:

| Topic | Knowledge note |
|---|---|
| 2025 M/C selection, filing status, residence timeline, currency conversion, 30%-ruling partial foreign tax liability choice, conserved income and revisierente | `../nl-tax-shared-resources/knowledge/international/scope-and-forms-2025.md` |
| Qualifying status, world-income measure and income statement | `../nl-tax-shared-resources/knowledge/international/qualification-2025.md` |
| Insurance periods, country allocation and treaty questions | `../nl-tax-shared-resources/knowledge/international/insurance-and-treaty-review.md` |
| Any 2026 international collection | `../nl-tax-shared-resources/knowledge/international/precollection-2026.md` |

Record actually consulted `source_ids` once in Sources used and Appendix A
`sources_loaded`; check their applicability, review metadata and freshness
in the source register. Warn once for a stale applicable source. A missing
note or attestation is a named `International source-content review` blocker;
an unreviewed required M/C inventory is `International form schema review`.
Do not infer review from a network fetch or user acceptance.

When reading evidence, load
`../nl-tax-shared-resources/reference/evidence-types.md` and
`../nl-tax-shared-resources/reference/extraction-boundaries.md`. Read each
document where supplied, assign stable next `ev_NNN` and canonical type,
and record only needed facts. Chat values use `user_chat`, short quote and
date. Preserve conflicting inputs as needs review and ask which controls.
Missing required facts get stable Q-/M-IDs. Do not reconstruct an amount that
is no longer visible verbatim.

## Scope and residence periods

Confirm tax year, migration/nonresident token, actual filing status,
invitation/deadline or other official basis, and any earlier return for the
same year. For 2025 distinguish M (migration during the year) from C (full
year abroad). Record the out-of-scope screens in the workpack's
Unsupported-case checks section: a deceased taxpayer's return (F-biljet),
another tax year than 2025 or 2026, and disputed treaty residence, a
government posting, a special pension or treaty issue, or an exit-tax issue
that stays an open review blocker. A full-year Netherlands resident with foreign income belongs
to `../nl-tax-annual-return/SKILL.md` for 2025 or
`../nl-tax-annual-return-2026/SKILL.md` for 2026. Preserve unresolved foreign
treatment for review. Do not create an M/C case merely because income came
from abroad.

Build a dated timeline covering the entire year: each country, exact start
and end date, immigration/emigration date, residence basis and provenance.
Confirm inclusive/exclusive boundaries so no date is omitted or counted twice.
Separate actual residence, domestic-law tax residence and treaty residence.
Keep overlapping homes, family ties, dual residence, government postings and
disputed dates open for an adviser/authority determination. A municipal
registration date is evidence, not an automatic legal conclusion.

Use the genuine invitation or notice for deadlines and extensions. Do not
apply the ordinary resident deadline or a five-year claim window as the
deadline for an invited M/C return. Past or missing deadlines require human
follow-up; do not invent penalties, interest amounts or payment references.
You may state the sourced C 2025 belastingrente warning and both sourced
C 2025 self-requested-return dates and their conflict from the 2025 scope
note, without calculating any interest.

For 2026 collect the same underlying evidence with dated actual/estimated
labels. Show `2026 annual international schema review`; do not assert a
published final M/C form, filing availability or screen labels. The 2026
provisional assessment is a separate workflow and does not establish final
annual-return facts or rules.

## Income, assets and preparation arithmetic

Collect each income group by category, country of source, work location when
relevant, covered dates, currency, gross amount, Dutch/foreign withholding,
and treatment provenance. Obtain separate residence-period figures rather
than allocating an annual amount by days merely because a move occurred.
For wages ask where duties were physically performed; payer country alone
does not determine the taxing right. Capture pensions, benefits, business
profit, other work, substantial interests and asset/debt categories when due.

For a 2025 emigration always ask about Dutch-accrued pension and lijfrente
aanspraken, pension or lijfrente capital moved to a foreign insurer,
eigen-woning capital insurance (kapitaalverzekering, spaarrekening or
beleggingsrecht eigen woning), substantial-interest shares held at the
emigration date, and any pension or lijfrente buy-out or other breach of its
conditions during the year. Follow the conserved income and revisierente
section of the 2025 scope note. Record the answers as a `conserved income` group under
`income_assets`. An unanswered item is a blocking open question, never zero
or not applicable. Do not calculate the conserverende aanslag or
revisierente.

For an immigration-year M return and for every C return, still ask these
items and record them in the same `conserved income` group: whether pension
or lijfrente capital was moved to a foreign insurer in 2025 (M questions 95c,
95e and 95f); whether a lijfrente continues with a non-admitted foreign
insurer after immigration (C question 60); whether a pension or lijfrente was
bought out or its conditions were breached in 2025 (revisierente: M question
94, C question 59); and, for a C return, onward emigration or a substantial
interest acquired as a nonresident (C question 60). Mark an item not
applicable only with a sourced answer for that item; otherwise it is an open
question.

Keep a full worldwide evidence inventory apart from the Dutch-reportable
inventory. Qualifying status does not make every worldwide item taxable in
the Netherlands. Separate gross income, taxable income, withholding,
deduction and relief; foreign withholding is not automatically a Dutch credit.
For assets retain applicable valuation dates, location, ownership share,
acquisition/disposal dates and associated debts. For a migration resident
period first ask whether an expat-ruling decision (30%-beschikking) existed
and whether the taxpayer makes the transitional choice for partial foreign
tax liability (scope note for 2025, precollection note for 2026). While the
choice is unresolved, keep foreign Box 2 and Box 3 items as worldwide
evidence, not as Dutch-reportable amounts. Screen both fictitious and
actual Box 3 evidence for 2025 M/C where applicable; never reuse a full-year
resident formula or generic day fraction for migration/nonresident Box 3.
The exact year/form rule and reviewed schema must cover any calculation.

Perform useful arithmetic only on confirmed complete groups: group total
= sum of sourced components; annual gross = sum of non-overlapping period
gross amounts; reconciliation difference = recorded total minus sourced
component total. Currency conversion needs the year/form note's confirmed
method, date, rate source and original currency. For 2025 the scope note
gives the M and C methods: the bank rate on the date of the income or
expense, and for Box 3 the ECB rate on the valuation, purchase, sale,
payment or receipt dates it names. No conversion from memory.
Record a confirmed adviser result with its derivation provenance without
recomputing an unsupported basis. Do not estimate final liability or relief
from an incomplete international collection.

## Qualification and deductions

Use the 2025 qualification note to collect qualifying-country periods,
complete world-income and Dutch-taxed measures, partner facts and the
income-statement status. Do not test qualification from salary alone or
automatically inherit last year's status. Only compute the sourced percentage
after every required category, exclusion and treaty treatment is established.
Label it a preparation test of one condition, not a residence or eligibility
decision. Pension/low-income exceptions, partner aggregation and country
exceptions need their own confirmed facts and professional review.

For the income statement distinguish requested, awaiting foreign authority,
received/confirmed, sent, previously provided with continuing eligibility,
and not yet established. Record no identifying fields or postal address.
The human obtains foreign authority certification and sends documents using
the current official instructions. A missing required statement remains open.
For 2026 follow its own note; never carry a 2025 statement requirement forward.

Collect own-home, pension contributions, personal deductions and credit
conditions with eligible residence/qualification and insurance periods.
Check whether the same benefit was available/claimed in the residence country.
Do not grant every resident deduction from a positive qualification percentage,
deny every benefit solely because that percentage is below the boundary,
or automatically elect partner status/allocation. Keep partner eligibility,
joint facts and any human-selected allocation separate.

## Insurance and treaty review

Collect exact mandatory-insurance periods for AOW/Anw/Wlz and relevant Zvw
status, work countries/dates, posting or EU applicable-legislation certificate/SVB decisions and evidence of
foreign coverage. Residence, income tax and mandatory insurance are separate.
Keep voluntary insurance distinct from mandatory insurance and an overseas
healthcare contribution distinct from ordinary Dutch Zvw liability. Never
infer insurance from a payslip withholding line, move date or qualification.

For each income/asset group record residence country, source/work country,
the asserted taxing right, exact treaty/article/version or official basis,
relief method and its evidence. The generic note is a screening aid, not a
country-specific treaty decision. Unconfirmed treaty classification,
tie-breaker, permanent establishment, special pension or exemption/credit
calculation remains `treaty_review` open. Continue unaffected collection.

## Final generation and mapping

Review facts, residence coverage, supported totals, qualification test,
statement status, insurance periods, deductions and all treaty/source/schema
gaps. Ask one contextual generation question. The opening request does not
authorize final generation. After acceptance set `confirm: complete` and
`generation_confirmed: true`, load the template/output contract, and run the
owner checks. Missing inputs may appear only in a clearly marked draft.

Readiness stays `draft` under the current scope policy. Only after maintainers
activate the exact scope and reviewed maps can readiness become `review_ready`
for 2025 when all applicable sections
are complete/chat_only, required source content and form inventory are
reviewed, figures reconcile and no legal/treatment/missing/stale blocker
remains. All 2026 precollection remains draft. The owner passes
`international_return`, year, `return_form`, sourced facts, calculations and
blockers to `../nl-tax-field-mapper/SKILL.md`; it alone maps exact supported
fields. Offer saving if due after mapping. Offer a human-only checklist only
when gates pass, in a later reply; the submit companion alone writes it.
