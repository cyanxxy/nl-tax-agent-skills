# International workpack output contract

Use `templates/international-workpack.md` for one confirmed year/form. Keep
its section order in a saved file: `## How to use this file`, `## Scope`,
`## Unsupported-case checks`, `## Taxpayer profile summary`, then the
remaining template sections in template order. Collection drafts may contain `Not yet
reviewed.` and sourced gaps; first saving does not require complete financial
or legal treatment. Final generation shows unresolved items explicitly.
Chat renders filled Markdown only, without fill notes or Appendix A/B YAML.

Every fact/amount carries document `F:ev_NNN`, chat `U:"quote" (date)`,
accepted factual assumption `A:ID`, missing `?`, or `C:formula` from sourced
components. Legal residence, treaty rights and insurance eligibility cannot
be supplied by an assumed default. Open questions, missing information,
user-stated values and Sources used must match the body and resume record.

## Readiness and ownership

Use `STATUS: DRAFT — N deferred section(s) — not for filing` for incomplete
collection or any source, form, residence, qualification, insurance, treaty,
reconciliation or stale blocker. State named blockers even if N is zero.
Every 2026 workpack also states `2026 precollection only — final annual M/C
schema not established`. Load
`../nl-tax-shared-resources/reference/workflow-scopes.yaml`: its current
`maximum_readiness: draft` keeps all international workpacks and maps draft.
Human source/schema review alone cannot override that ceiling. Only after
maintainers activate the exact scope with reviewed maps are `review_ready`
and `STATUS: COMPLETE DRAFT FOR REVIEW — not for filing` possible for 2025,
after every review and completeness gate passes. Banner, Appendix A and map
share owner readiness.

The owner writes all sections except mapper-owned Field map summary,
Appendix B and the mapper's own gap rows/section Q-IDs, and companion-owned
Manual-entry checklist. Before those steps use `not yet mapped` and
`not requested`. Only the shared STALE line may be added by the owner to
existing map/checklist sections; do not change their values. No manual-entry
checklist is generated while source/schema review is pending or for 2026
precollection. The Human review checklist is review questions, not portal
entry instructions or entry amounts.

## Resume record

Appendix A has one fenced YAML record with exactly the template keys,
`workpack_format: nl-tax-workpack`, `workpack_version: "2.0"`, workflow
`international_<year>_<form>`, `tax_year: 2025|2026`, and
`return_form: migration|nonresident` matching profile and filename.
`queued_workflow: null`. Sections are exactly `international_scope`,
`residence_periods`, `income_assets`, `qualifying_status`, `social_insurance`,
`treaty_review`, `deductions_credits`, `reconciliation`, `confirm`.
Statuses are `not_started | in_progress | complete | chat_only | deferred`
with `open` Q-ID lists. Facts remain in readable sections.

Recorded `save_consent` defaults to `not_given`; only active conversation
consent permits a file, which records `given`. `generation_confirmed` is
true only after contextual confirmation and false after a changed sourced
fact. Appendix B is `not yet mapped` or one mapper-authored current-schema
map using `workflow: international_return`, matching year/form; never an
annual resident or provisional map.

## Owner checks

Before saving or showing generated output, fix structural errors and show
taxpayer-relevant unresolved items. Partial collection saves need the
structural/provenance checks; financial completeness and legal-treatment
checks determine readiness rather than permission to save a draft.

- Year/form/file and the nine section keys agree; all template sections and
  record keys are present in order; 2026 carries the precollection banner.
- Every ev-, A-, Q-/M- and profile reference resolves. Open questions equals
  the section `open` lists; Sources used equals actual `sources_loaded` with
  applicability, freshness and review status checked.
- Unsupported-case checks record the deceased-taxpayer, other-year and
  disputed-residence or special-treaty screens with their sources or open
  blockers.
- For a 2025 emigration the conserved-income group under `income_assets` is
  answered with sources or carries a blocking open question; it is never
  zero or not applicable without a source. For an immigration-year M return
  and every C return the same group records the foreign-insurer, revisierente
  and (for C) onward-emigration or nonresident substantial-interest items,
  each answered with a source or left as an open question; the group is never
  marked not applicable as a whole. A resident period with an
  unresolved 30%-ruling partial-foreign-tax-liability choice keeps foreign
  Box 2 and Box 3 items out of the Dutch-reportable inventory.
- Full-year timeline is confirmed or its exact gaps/overlaps are open; actual,
  domestic-law and treaty residence are not conflated. Form selection and
  filing/deadline basis are sourced or unresolved.
- Income groups and residence intervals are not double-counted. Gross,
  withholding, taxable amounts, worldwide measures and relief stay separate.
  Components, conversion, timing and qualifying formula inputs are sourced;
  missing categories/zeroes are explicit, never implied.
- Insurance periods, qualification conditions, income-statement status,
  deductions, partner facts and country-specific treaty bases are confirmed
  or visible blockers. No automatic residence, treaty or eligibility result.
- Supported arithmetic reconciles. No generic full-year/day fraction, final
  tax estimate, relief calculation or foreign withholding credit substitutes
  for a missing rule or input. 2025 formulas/labels are not used for 2026.
- Required notes and exact form inventory have human content-review
  attestation before review readiness; research/agent checks cannot provide
  it. The current scope policy permits the requested readiness and maintainers
  have activated its reviewed maps. Map/banner/record agree; stale outputs
  cannot be used.
- No identifiers, credential/session data, copied evidence, file hashes or
  invented payment instructions appear. Every portal action names a human.
  The standalone Not submission advice section retains the portal boundary.
