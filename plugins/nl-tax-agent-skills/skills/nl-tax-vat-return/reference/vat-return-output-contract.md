# VAT return output contract

Use `templates/vat-workpack.md` for one year and assigned period. Keep every
`##` section in template order in a saved file; unopened collection sections
may hold `Not yet reviewed.` until generation. In chat show only filled
sections, no bracketed fill instructions or Appendix A/B YAML. Workpack facts
carry `F:ev_NNN`, `U:"quote" (YYYY-MM-DD)`, an accepted `A:ID`, `?`, or
`C:formula` derived from sourced rows. A `profile.<key>` reference points to a
sourced profile row. Record every U-value in its index and every missing
required value in Missing information and Open questions.

## Readiness and ownership

Use `STATUS: DRAFT — N deferred section(s) — not for filing` for incomplete
inputs or a source/treatment/schema blocker. State a source blocker beside
the banner even when `N` is zero. Use `STATUS: COMPLETE DRAFT FOR REVIEW —
not for filing` only after the section and source-review gates pass.
Appendix A, the banner and any map have identical readiness. All gate checks
record `check_performed_by: checked_by_agent` in the map; checks may reject
readiness and never promote it.

The owner writes all sections except Field map summary/Appendix B, the
mapper's own gap rows, and Manual-entry checklist. Only the mapper writes
those map sections; only the submit companion writes a requested checklist.
Before mapping, both map sections hold `not yet mapped`; before a permitted
explicit checklist request, the checklist holds `not requested`. Source
review pending means no checklist is generated. The owner's only edits to
existing map/checklist sections are the shared STALE line after a change.

## Resume record

Appendix A has one fenced YAML block, schema `nl-tax-workpack` version `2.0`,
with exactly the template keys. Set `workflow: vat_<year>_<period>`,
`tax_year: 2025|2026`, and `period: Q1..Q4|M01..M12|Y` matching confirmed
profile and filename. `queued_workflow` is `null`. The five section keys are
`vat_scope`, `vat_transactions`, `vat_input_tax`, `vat_reconciliation`, and
`confirm`. Facts stay in readable sections. `save_consent` starts
`not_given`; a written file records `given` only after session consent.

Appendix B is `not yet mapped` or exactly one mapper-owned YAML field map
using its current schema, `workflow: vat_return`, matching `tax_year` and
`period`. No annual, provisional, other-period or correction map belongs here.

## Agent self-check

Before showing generation or saving, check all applicable items; fix errors
and report only blockers the taxpayer needs to resolve:

During collection saves, apply structural/provenance checks to established
facts and preserve uncollected inputs as open gaps or `Not yet reviewed.`
Completeness and calculation checks determine the draft's visible gaps and
gate review readiness. Contextual final confirmation gates generated
presentation; it does not prevent a consented partial draft save. Confirm
the filename's year and assigned period before first writing; never invent
facts to satisfy a check.

- All template sections and Appendix A keys/statuses are present in order;
  year, period, filename, assigned-period confirmation and scope agree.
- Every used ev-ID, A-ID, Q-ID and profile key resolves; Q-IDs in Open
  questions equal the union of section `open` lists. Sources used exactly
  equals `sources_loaded`, with only applicable consulted sources.
- Every mandatory VAT note and rubric schema has source-content review
  attestation before `review_ready`; missing or `needs_review` resources are
  visible blockers. Fetching a page or checking a hash is never attestation.
- Every applicable rubric is sourced, sourced zero/not applicable, or open;
  turnover excludes VAT, credit notes are counted once, and the owner shows
  component formulas and official rounding separate from raw amounts.
- Period/invoice timing, deduction entitlement, KOR effective dates and any
  foreign-service treatment are confirmed. Nil returns use sourced zeroes.
  Complete bounded adjustments carry helper formulas, accepted treatment,
  source IDs and timing; unresolved classification/elections remain blocked.
  An adviser adjustment has provenance and confirmed period/rubric. ICP/OSS
  follow-up is separately prepared and no adjustment is counted twice.
- Net payable/refundable balance reconciles; unexplained differences stay
  draft. No invoice payment, bank balance, annual profit, or other-period
  amount silently substitutes for the VAT dataset. The one exception is a
  sourced small correction carried from an earlier period into this next
  return, recorded as its own row with its original period and added once
  to its normal rubric.
- Map summary/Appendix B state and readiness agree with the owner; no stale
  value is used. A change resets generation confirmation and marks any
  existing map and checklist stale until rebuilt by their owners.
- No identifier, copied evidence, file hash, credential, invented payment
  reference, or automatic KOR election is stored. Every portal action names
  the taxpayer or authorized human, and the standalone Not submission advice
  section names Mijn Belastingdienst Zakelijk and human-only entry/submission.
