# VAT correction output contract

Use `templates/vat-correction-workpack.md` for one original filed period.
A whole-year suppletie by a monthly or quarterly filer is a human-review
route that this contract never prepares; `Y` is only an annual assigned period.
Preserve its saved-file section order. Collection sections not reached may
hold `Not yet reviewed.`; generated output contains no fill instructions.
Chat shows filled Markdown only, never Appendix A/B YAML. Every amount/fact
has document `F:ev_NNN`, chat `U:"quote" (date)`, accepted `A:ID`, missing
`?`, or sourced `C:formula` provenance. Index user values, assumptions and
gaps; never use a missing baseline as zero.

## Readiness, map and resume record

An incomplete, unsupported, source-review or route blocker means `draft`
with `STATUS: DRAFT — N deferred section(s) — not for filing`; identify
source blockers even if N is zero. `review_ready` and `STATUS: COMPLETE
DRAFT FOR REVIEW — not for filing` require every applicable section
complete/chat_only plus all source-content/schema reviews and no blocker.
Banner, Appendix A and map use the same owner rollup. Agent checks never
promote draft. Pending source review prevents any manual-entry checklist.

Appendix A is one fenced YAML `nl-tax-workpack` record version `2.0` with
exactly the template keys, workflow `vat_correction_<year>_<period>`, explicit
`tax_year: 2025|2026`, and `period: Q1..Q4|M01..M12|Y` matching the original
period's profile and filename. `queued_workflow: null`. Sections are exactly
`vat_scope`, `vat_original`, `vat_reconciliation`, `vat_correction_route`,
and `confirm`. Facts belong in the body. `save_consent` defaults to
`not_given`; the written record uses `given` only after session consent.

The mapper alone owns Field map summary, Appendix B, its own gap rows and
their section Q-IDs. Appendix B is `not yet mapped` or its one current-schema
YAML map with `workflow: vat_correction`, original year and period. The
submit companion alone writes Manual-entry checklist after a permitted
explicit request; otherwise it reads `not requested`. The owner may only
add the shared STALE line to existing map/checklist sections after a change.

## Agent self-check

Check before presenting generation or writing. Fix structural errors and
report only taxpayer-relevant unresolved items:

For collection saves, check structure/provenance for established facts and
preserve uncollected original/corrected figures as open gaps or `Not yet
reviewed.` Full-figure, reconciliation and route checks gate review readiness.
Contextual final confirmation gates generated presentation; it does not
delay a consented partial draft save. Confirm the filename's original year and assigned period before
first writing; never invent facts to pass a check.

- Year/original period/assigned dates and actual submitted status are
  confirmed; every template section and record key is present in order.
- All ev-, A-, Q- and profile references resolve. Open questions matches
  section `open` lists; Sources used equals consulted `sources_loaded` with
  year/applicability and review status checked.
- A source-content review attestation covers every required note and rubric
  schema before `review_ready`; `needs_review`, missing or unreviewed notes
  remain draft blockers, even after fetching URLs or testing arithmetic.
- Original declarations are sourced and unchanged; corrected **full**
  applicable rubric totals include unchanged rubrics. Prior corrections have
  a confirmed baseline. Credit notes, output VAT, assessed foreign VAT and
  eligible input VAT are counted once under confirmed period/treatment.
- Original net balance, corrected net balance and signed VAT delta are
  separately sourced/derived, with raw vs official rounded figures clear.
  Control-account differences remain open rather than plugged.
- The sourced threshold measure applies to the original period's VAT
  correction magnitude, never turnover or a net of different periods; the
  inclusive small boundary and discovery timeline match corrections.md.
- Whether the original period's deadline had passed on the correction date
  is recorded with provenance, and the payment line matches that branch.
  Letter-route items (margin globalisation, double-declared intra-Community
  acquisition) and any rubric 3b letter are named for human handling.
- The map declares the chosen route in exactly one Appendix B notes line,
  `vat_correction_route: suppletie`, `next_return`, `letter` or
  `human_review`, matching the Correction route section. Only the
  `suppletie` route maps `vat.correction.previous_balance`.
- The small-route target period (the next return after discovery) and the
  carry-once components are distinct from corrected original full totals;
  no target return file is changed silently.
  Suppletie rows use revised full figures, never differences as totals.
  Zero-delta reporting treatment is confirmed rather than assumed.
- Bounded supported adjustments carry accepted treatment, helper formula,
  period and source IDs. Unsettled classification/elections remain blocked;
  adviser figures have year/period/rubric/sign/amount/derivation provenance.
  Separate ICP/OSS corrections never use this domestic correction threshold.
- Map/readiness agree with the owner; the previous balance is a suppletie
  entry row ("Totaalbedrag eerdere btw-aangifte over dit tijdvak"), while
  the corrected balance and the delta stay internal. No stale
  map/checklist is used; changed facts reset confirmation and require rebuild.
- No identifiers, file hashes, credential/session data, copied evidence or
  invented payment reference/instructions appear. Every portal action has an
  explicit human subject. Not submission advice names human-only review,
  entry, signing and submission in Mijn Belastingdienst Zakelijk.
