# ICP output contract

Use `templates/icp-workpack.md` for exactly one year/period. Save every `##`
heading in template order. During collection unopened sections can read
`Not yet reviewed.`; chat shows only filled Markdown sections and never
Appendix A/B YAML. Every amount, classification and verified-zero answer has
F:ev_NNN, U:short quote/date, accepted A:ID or C:sourced formula provenance.
Unknown facts remain ? with linked Q/M rows. Accepted assumptions cannot
establish an actual-ID verification, filing assignment or special treatment.

The owner writes everything except the mapper's Field map summary, Appendix B
and own gap rows, and the companion's Manual-entry checklist. Those start as
`not yet mapped` and `not requested`. Source review pending prevents a
manual-entry checklist. After a change only the shared STALE line may be added
to those sections by the owner.

Appendix A is one YAML block using nl-tax-workpack version 2.0, with exactly
the template keys. Set workflow `icp_<year>_<period>`, tax_year 2025 or 2026,
period Q1..Q4/M01..M12/Y, queued_workflow null and the five section keys
icp_scope, icp_transactions, icp_corrections, icp_reconciliation, confirm.
Sources used equals sources_loaded, without duplicates or other-year sources.
Filename, profile, map and record must agree. Appendix B is not yet mapped
or exactly one mapper-owned current-schema `icp_declaration` YAML block for
the same year/period.

Use `STATUS: DRAFT — N deferred section(s) — not for filing` for missing
facts, unverified actual IDs, unexplained reconciliation or pending source/form
review. Name each review blocker even when N is zero. The shipped scope keeps
readiness draft even after section/source checks pass; never set review_ready
or COMPLETE DRAFT FOR REVIEW while this ceiling applies. Every status surface
agrees. Explicitly state that
actual customer IDs must be supplied by the human from their administration;
the file never becomes a self-contained filing dataset.

## Agent checks

At consented partial saves check structure/provenance and retain uncollected
facts as gaps. At generation also check completeness/calculations. Record
check_performed_by checked_by_agent in the mapper output, never a human
attestation or a check that promotes readiness.

- Scope/year/coverage/frequency are sourced and consistent; annual ICP has
  permit evidence; goods lookback and two-month transition were checked.
- Actual-ID verification has dated human provenance per alias; its absence is
  blocking. No actual identifiers, evidence copies or file hashes are stored.
- Goods/services/credit notes are allocated by the correct basis and counted
  once; specials have their classification and form-coverage review or remain
  deferred. No invoice summary, profit or bank balance substitutes for rows.
- Earlier errors use signed deltas net of already reported corrections;
  wrong-ID reversal/restoration use the original period and separate aliases.
  Error rows and current credit notes are not duplicated.
- Current ICP rubric 3 totals (ICP 3a plus ICP 3b) equal btw-aangifte rubric
  3b over identical dates; monthly/quarterly differences use a coverage
  bridge, not a balancing plug. A sourced new-means-of-transport supply is
  reported by letter, not on the ICP; its btw-aangifte rubric and any
  difference it causes stay a named specialist-review item. Apart from that
  item and an explained, recorded cents or entry-rounding difference, any
  remaining difference stays an open blocker. Raw cents and confirmed form
  rounding remain distinct.
- All ev/A/Q/M references resolve; Open questions equals section open IDs;
  consulted applicable Sources used equals sources_loaded. Note review and
  form coverage gates stay blocking until actual human review exists.
- Generation confirmation, readiness and map agree; stale values are never
  used. Only the mapper authors maps and only an explicitly requested,
  permitted submit companion authors checklists.
- Every portal action has a human subject and the standalone Not submission
  advice section names Mijn Belastingdienst Zakelijk and human-only entry,
  signing and submission.

Current shared workflow-scopes.yaml maximum_readiness is draft; retain this
ceiling even if individual evidence, source-content or schema checks are
complete. Only a maintainer activation of the exact scope/reviewed map can
change it. Do not offer a checklist containing entry amounts in this bundle.
