# Capability review and VAT extension — 2 October 2026

The existing plugin supports annual income tax 2025 (including a standard ZZP
business section) and provisional assessments 2026. ZZP VAT was missing as a
separate tax workflow. The extension adds two skills, period-specific workpacks,
source summaries and rubric mapping, while preserving the skills-only package.

## Added

- `nl-tax-vat-return`: Dutch resident-business period/accounting-system checks,
  invoice and credit-note reconciliation, input deduction evidence, confirmed
  ordinary domestic and received reverse-charge treatment, KOR screening,
  year-end adjustment screening, and final draft review.
- `nl-tax-vat-correction`: original filed versus revised full totals, discovery
  date, correction route, separate difference, non-overlapping period scope,
  and preparation, for one original period, of either the small-correction
  components for the human's next (eerstvolgende) VAT return or the human's
  suppletie, plus any letter-route item recorded for human handling. A
  whole-year suppletie is an official option the agent may mention, but this
  skill does not prepare it; for a filer without an annual filing period it is
  a human-review route. The `Y` period token means only an annual filing
  period assigned by the Belastingdienst.
- Intake, knowledge lookup, mapper and submit companion recognize VAT. The
  mapper remains sole field-map author. VAT belongs to the human's Mijn
  Belastingdienst Zakelijk; no authenticated actions are automated.
- One consented file per exact year/period; no income-tax amounts are reused
  as VAT turnover. Resume and stale-output rules apply to every period.
- Four rule notes under `knowledge/vat/`, each naming its official sources in
  its `source_ids` header, plus pending-review hashes, source staging,
  mechanical validation and behavioral scenarios. The full VAT source scope
  for human review is every `workflow_family: vat` entry in
  `source-register.yaml`; those entries also cover the seven
  `knowledge/vat-adjustments/` notes. Count them from the register rather than
  relying on a number written here, because review passes add sources.

## Extension added in the follow-up

The requested ICP/OSS, VAT-adjustment, migration/nonresident and annual 2026
preparation workflows are now implemented. See
[extended workflow review](extended-workflows-2026-10-02.md) for exact scope,
validation, boundaries and activation requirements. These are staged draft
routes; adding a preparation workflow does not attest its tax content.

## Remaining gaps

- Human tax-content review and exact schema review of every staged note.
- Real-host conversational smoke tests on Cowork, Claude Code, ChatGPT Work and
  Codex.
- Decisions about specific countries, treaties, elections and disputed
  valuations.
- F-biljet returns for a deceased person.
- The EU small-business scheme (EU-KOR), refunds of foreign VAT, imports and
  the artikel 23 import deferral.
- Specialist business computations and tax years after 2026.
- A real human recheck of the existing `bd_machtigen_authorization` source,
  whose freshness gate currently fails.

Direct authenticated filing stays human-only by design.

## Concrete VAT content review

The reviewer compares these files with every URL under their Official sources
section. `last_verified` records agent research, not human approval.
For staged VAT sources only, register `last_checked` also records public
source research (`last_checked_kind: agent_source_research`), with
`last_human_reviewed: null`. Existing active-source dates retain their human
review meaning; a source-research date never replaces that attestation.

| Note | Review focus |
|---|---|
| `knowledge/vat/return-and-rubrics.md` | Resident deadlines, applicable rubric columns, zero versus nil/exempt, ordinary reverse charge, whole-euro rounding and unnumbered total |
| `knowledge/vat/invoices-and-deduction.md` | Invoice/cash timing, received purchase invoices, valid evidence, foreign VAT, private/exempt and meal deductions |
| `knowledge/vat/kor-and-special-cases.md` | Actual KOR participation/effective dates, incidental obligations, transition review, ICP and year-end adjustments |
| `knowledge/vat/corrections.md` | Net correction threshold, discovery deadline, complete revised totals, previous-declared total, payment following assessment and already-filed corrections |

All notes and mirrored VAT metadata stay `needs_review`. The source register
marks them `content_stage: draft_only`; the supported-workflows file declares
eleven `draft_only_workflows`. Existing income-tax review requirements are
unchanged. The validators accept a staged note only with that explicit status;
the mapper rejects VAT `review_ready` while owner-mandatory sources are staged.
The VAT return and correction also depend on the seven
`knowledge/vat-adjustments/` notes (BUA, car private use, margin, mixed
deduction, private use, property and revision), which need the same review.

After actual human comparison and approval, maintainers record the review
identity/date and exact approved hashes, change note/metadata status to
`reviewed`, remove `content_stage: draft_only`, and promote the exact VAT
workflow/year declarations to `active_workflows`. Re-run the source, workflow,
knowledge, unit and offline-eval gates before the release version bump to
0.5.0 that publishing these skills requires.
Record the actual human review date in the register and replace its research
date classification at the same time.
