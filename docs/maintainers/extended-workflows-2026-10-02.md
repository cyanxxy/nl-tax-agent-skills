# Extended preparation workflows — 2 October 2026

The follow-up implements ICP and OSS/IOSS preparation, bounded VAT adjustments,
M (migration) and C (nonresident) income-tax returns, and the resident annual
return 2026. All new tax notes are `needs_review`. They were researched from
official authorities on 2 October 2026, and no human attestation has been
fabricated. The register first added 66 sources beyond the initial 22 VAT
entries. The review pass of 2 October 2026 adds eight more source IDs:
`bd_vat_kor_conditions` and `bd_vat_kor_withdrawal`
(`knowledge/vat/kor-and-special-cases.md`), `bd_zakelijk_login_machtigen`
(`knowledge/vat/return-and-rubrics.md`), `law_uitvoeringsbeschikking_ob_1968`
(`knowledge/vat-adjustments/revision.md`), `eu_vat_directive_oss_currency`
(`knowledge/vat-cross-border/oss.md`), `bd_annual2026_box1_rates` and
`bd_annual2026_partial_foreign_liability`
(`knowledge/years/2026/annual/preparation.md`), and
`bd_intl_partial_foreign_liability`
(`knowledge/international/scope-and-forms-2025.md`). Separate source families
(`vat`, `vat_cross_border`, `international`, `annual_2026`) keep the reviewed
annual 2025 and provisional 2026 maps from absorbing the new tax rules.

## Scope and ownership

| Owner | Exact identity and saved file |
|---|---|
| nl-tax-icp | icp_<year>_<period>; nl-tax-icp-<year>-<period>-workpack.md |
| nl-tax-oss | oss_<scheme>_<year>_<period>; nl-tax-oss-<scheme>-<year>-<period>-workpack.md |
| nl-tax-international-return | international_<year>_<form>; nl-tax-international-<year>-<form>-workpack.md |
| nl-tax-annual-return-2026 | annual_2026; nl-tax-annual-2026-workpack.md |
| nl-tax-vat-adjustments | Read-only findings and calculations for the owning VAT period; no saved file |

Every path starts with `workspace/` and is written only with active save
consent in the current session. The shared
`reference/workflow-scopes.yaml` is a declarative contract for identities,
sections and templates; it is not a decision engine. No runtime scripts, MCP
servers or hooks are installed. Only the field mapper writes maps. While source
review is pending, the submit companion shows only the Blockers section, with
no amounts. The annual 2026 workflow collects actual evidence while the year is
still open.

VAT corrections stay one workpack per original period. A whole-year suppletie
is an official option the agent may mention, but these skills do not prepare
it: for a filer who does not have an annual filing period, a whole-year
suppletie is a human-review route. The `Y` period token means only an annual
filing period assigned by the Belastingdienst.

## Content review checklist

- ICP: the exact timing for goods and services, the EUR 50,000 frequency
  threshold including the exceptional two-month transition, the permit-based
  annual deadline, separate corrections, customer aliases with genuine VAT-ID
  verification by the human, and the bridge to VAT rubric 3b.
- OSS: registration, scheme and establishment eligibility; Union and non-Union
  quarters versus IOSS months; consignments of at most EUR 150; the EUR 10,000
  threshold conditions; destination rates; prior-period corrections; no
  negative offset between countries; nil returns; no input deduction; and the
  2026 IOSS customs-duty addendum.
- VAT adjustments: the car forfait, acquisition timing, the cap and actual
  commuting; direct allocation versus pro-rata; the full first-use adjustment
  and later-year 5-year or 10-year revision; inclusive EUR 30,000 investment
  services from first use in 2026; the relative 10% tolerance; the KOR
  transition; the BUA recipient threshold and contributions; individual versus
  global margins and loss-year decisions; and the boundaries of the property
  election.
- International: the 2025 M and C notes and routing, exact residence periods,
  Dutch-source versus worldwide income for qualifying status, the
  year-specific proof and 90% test, insurance periods, and country-specific
  treaty, exit and conservation items. The 2026 evidence collection cannot
  assume that final M or C screens will be available.
- Annual 2026: no substitution of the resident 2025 or provisional schema;
  the actual profit and capital bridge; the eligibility and deduction chain;
  year-end evidence; the 2026 Box 3 own-use property benefit; and whether a
  forfait is final or provisional. The conflict in the current public FISIN
  AOW table must be resolved before any AOW computation.

## Activation and validation

A specialist must compare each note with all cited official authorities and
record the actual reviewer, date and approved hashes. The source-domain
allowlist adds download.belastingdienst.nl (forms and explanatory PDFs),
stichtingenvereniging.belastingdienst.nl (rubric structure),
zoek.officielebekendmakingen.nl (official legal publications) and
vat-one-stop-shop.ec.europa.eu (European Commission OSS and IOSS guidance);
the review pass also needs eur-lex.europa.eu for
`eu_vat_directive_oss_currency`. Active resident sources keep their original
genuine review dates. Real source review alone does not unlock a draft scope:
maintainers must implement exact reviewed field schemas, update the scope
ceiling, the validator policy and the workflow declarations, and then run the
source, workflow, knowledge, invocation, unit, offline and real-host behavioral
checks before versioning or releasing. Full-year 2026 evidence cannot be
assumed before the year ends.

Releasing these skills also needs a version bump to 0.5.0 (see the
`[Unreleased]` CHANGELOG section), because 0.4.0 was tagged without them.

The existing `bd_machtigen_authorization` date is 1 July 2026, which is 93 days
old on 2 October 2026 against its 92-day policy; its knowledge gate stays failed
until an actual human recheck. Repository graders verify mechanics and
provenance consistency, not legal accuracy.

The Claude eval cases for these workflows live in
`plugins/nl-tax-agent-skills/evals/` (`cowork-icp-period-and-vat-id-review`,
`cowork-oss-country-corrections-no-offset`,
`cowork-vat-adjustments-first-use-2026`,
`cowork-international-m-c-year-isolation`,
`cowork-annual-2026-actual-precollection`, and the rewritten
`cowork-migration-draft-boundary`, formerly `cowork-unsupported-boundary`),
next to the VAT cases.

## Recorded mechanical result

These results were recorded on 2 October 2026, before the review pass; rerun
every gate after it. Final repository suite: 666 tests passed. Plugin-folder
suite: 665 tests passed before the final dependency-guard regression; 28
extension tests then passed from that folder after the guard. Source-register,
supported-workflows, invocation-policy, offline-dataset, compile and whitespace
checks passed. Both rebuilt archives contained 19 skills and no runtime Python,
scripts or hooks. New Claude and offline scenarios were validated structurally;
no native host run or human tax-content review is claimed. Knowledge validation
reported only the existing stale authorization source described above, with no
new missing, metadata, hash, source-ID or workflow errors. See the full
machine-readable record in
submission/openai/reviews/extended-workflows-validation-2026-10-02.json.
