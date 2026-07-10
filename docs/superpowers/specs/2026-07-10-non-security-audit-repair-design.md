# NL Tax Agent Skills Non-Security Audit Repair Design

**Date:** 2026-07-10  
**Target release:** 0.1.7  
**Primary host:** Claude Cowork  
**Secondary hosts:** Claude Code and Codex

## Objective

Repair every confirmed non-security issue from the repository, tax-content,
Claude/Cowork, data, documentation, and behavioral audits while preserving the
product boundary: the LLM drives preparation and the taxpayer performs every
official portal action.

The release must be truthful about what it can prepare. Missing official rules
or incomplete form coverage become visible manual-review boundaries; they are
never filled with remembered formulas, generic defaults, or optimistic
readiness claims.

## Binding scope boundary

The user explicitly excluded all security and privacy fixes from this repair.
The following audited findings must remain unchanged in 0.1.7:

- source/snapshot path traversal and symlink containment;
- workflow output-path traversal;
- evidence-indexer symlink, FIFO, special-file, and resource-limit handling;
- broad `Bash(python3:*)` preapproval and inline Python execution;
- PII acceptance, storage minimization, attachment copying, and host-path
  disclosure;
- duplicate-key YAML rejection;
- Markdown/link/image injection hardening;
- atomic metadata writes and metadata-symlink handling;
- security-motivated numeric/resource denial-of-service hardening;
- new prompt-injection controls beyond the current preparation-only behavior.

No task may edit those behaviors incidentally. Existing tests that encode those
behaviors stay unchanged unless a non-security correction makes a narrow test
fixture update unavoidable.

Four findings that were mentioned as security-adjacent are still in scope
because they directly corrupt tax preparation:

- invalid or ambiguous Box 3 rows entering trusted totals;
- string booleans changing fiscal-partner decisions;
- Box 2 calculation bypassing eligibility validation;
- failed or wrong-year evidence satisfying Box 1 completeness.

## Product contract

The LLM owns:

- scope screening and conversational intake;
- evidence interpretation and confidence judgments;
- sourced tax-rule reasoning;
- focused follow-up questions;
- assumptions, missing-information, and provenance records;
- workpack assembly and field-map preparation;
- explaining what the taxpayer must review.

Python is optional at runtime. The complete conversational workflow, workpack,
and field map must remain usable when Cowork exposes no Python interpreter or
cannot mount bundled scripts into the shell environment.

Retained Python helpers are deterministic post-write checks. They may hash,
validate schemas, normalize already-classified input, or recompute simple
source-pinned arithmetic. They do not decide eligibility, classify ambiguous
tax treatment, invent missing values, optimize allocations, generate the
workpack, or claim that an output matches a live portal.

The taxpayer or an authorized representative alone opens Mijn Belastingdienst,
enters values, reviews the live calculation, signs, and submits. The
`nl-tax-submit-companion` name remains for compatibility, but its user-facing
title and description identify it as an explicit manual-entry checklist.

## Skill and artifact ownership

Public skill names and canonical output paths remain stable.

| Skill | Responsibility | Canonical writes |
|---|---|---|
| `nl-tax-intake` | Scope, routing, minimized interview state | taxpayer profile and intake/session state |
| `nl-tax-evidence-indexer` | Evidence inventory and LLM-led classification | evidence index and review questions |
| `nl-tax-annual-return` | Annual orchestration and 2025 workpack | annual workpack and annual session state |
| `nl-tax-provisional-assessment` | 2026 request/change/review/stop orchestration | provisional workpack, delta/review artifacts, provisional session state |
| `nl-tax-field-mapper` | One mapping contract for both workflows | annual or provisional `field-map.yaml` |
| `nl-tax-submit-companion` | Explicit manual-entry checklist | manual checklist only |
| `nl-tax-source-refresh` | Developer maintenance | source plans and reviewed-note metadata |
| Box 1, Box 2, Box 3, partner, winst helpers | Reusable reasoning and deterministic checks | no independently owned final artifact |

The annual and provisional skills orchestrate the mapper but do not duplicate
its mapping rules. Existing `workspace/shared/*-notes` files remain readable for
resume compatibility. New sessions persist helper-derived facts through the
owning annual/provisional workflow so a helper cannot compete with the
orchestrator for the same artifact.

`session-progress.yaml` gains a winst subsection and a schema-version bump. A
readiness banner derives from every applicable subsection, including winst, so
an entrepreneur workflow cannot appear complete when its business phase is
untracked.

Every cross-skill reference names the sibling skill explicitly. Relative
`templates/`, `reference/`, and `scripts/` paths may not be described as local
to annual/provisional when the target belongs to `nl-tax-field-mapper`.

## Claude and Cowork packaging

Delete the seven identically named legacy `commands/*.md` wrappers. Move their
useful `argument-hint` values into the corresponding `SKILL.md` frontmatter.
Claude must report exactly 12 unique skills rather than 19 competing entries.
The namespaced invocation names do not change.

Descriptions must trigger on preparation intent, not on a casual mention of
Dutch tax or a document name. An informational question must not initialize a
workspace. Explicit requests to prepare, organize, review, or index do trigger.

Use progressive disclosure:

- `SKILL.md` contains routing and phase orchestration;
- a workflow reads only the active phase section of its flow reference;
- output contracts and large templates load only when assembling output;
- annual and provisional source material never load together;
- helper descriptions stay concise while retaining distinguishing tax terms.

Documentation describes both current local and remote Cowork sessions. It does
not claim that Cowork is always a local Apple VM, that Cowork is no-code, that
bundled scripts are unsupported, or that plugin-cache visibility follows an
undocumented rule. Optional Python helpers require Python 3.10 or newer; their
absence never blocks the LLM workflow. The output records either
`checked_by_script` or `checked_by_agent` so the review trail is explicit.

Cowork is labeled supported only for behavior verified by first-party Claude
validation plus the repository's behavioral cases. Exact attachment mounts,
approval prompts, and Desktop/remote bridging stay in a manual smoke-test
checklist unless exercised in a real Cowork session.

## Tax-content corrections

### Healthcare

- Remove wheelchairs, scooters, and home modifications from deductible examples.
- Treat reimbursed costs, premiums, statutory excess, and unsupported categories
  according to the reviewed 2025 Belastingdienst categories.
- Keep threshold and multiplier calculations manual until a complete reviewed
  table and input contract exist.

Primary source: <https://www.belastingdienst.nl/wps/wcm/connect/nl/belastingaangifte/content/overzicht-zorgkosten-2025>

### Own home and Box 1

- Calculate the own-home income balance without adding
  `tariefsaanpassing aftrekposten` to Box 1 income.
- Present the rate adjustment separately as a tax-benefit adjustment.
- Use all qualifying deductible own-home costs in the Hillen comparison,
  including qualifying financing costs and periodic erfpacht/opstal/beklemming
  payments—not mortgage interest alone.
- Support a review estimate only for one ordinary main residence; route complex
  housing cases to manual review.
- Change the private-use car boundary to 500 kilometres or fewer and require
  first-admission/regime facts before presenting a rate.
- Replace the blanket stock-option exercise-date claim with the current
  tradability/election rule and make incomplete equity-compensation cases
  manual review.

Primary sources:

- <https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/prive/woning/eigenwoningforfait/geen_of_een_kleine_eigenwoningschuld/>
- <https://www.belastingdienst.nl/wps/wcm/connect/fisin/fisin2025/belastingberekening>

### Benefits and credits

- Do not treat AKW/kinderbijslag as taxable Box 1 income.
- Replace “benefits never count for arbeidskorting” with the reviewed ZW/WAZO
  exceptions and manual review when the employment relationship is unclear.
- Require a child to be younger than 12 on 1 January for the IACK screen.
- Base the elderly single-person credit screen on entitlement to the AOW
  single-person benefit, including relevant special cases—not on a generic
  single-parent flag.
- Treat a UPO as accrued/projected-pension context, not proof of taxable pension
  payments or withholding. Use a payment year statement for those amounts.
- Keep portal-calculated credit amounts authoritative unless the full reviewed
  formula and every required input are present.

### Gifts, AOV, and deductions

- Replace “periodic gifts have no cap” with the EUR 1.5 million cap and the
  reviewed transition condition.
- Do not treat periodic AOV premiums as ordinary business costs. Route qualifying
  premiums to the correct private income-provision category and leave ambiguous
  policy types for review.
- Permit allocation of a prior-year personal-deduction remainder for eligible
  whole-year fiscal partners.
- Present traceable allocation scenarios; never recommend the higher earner as a
  universal optimum.

### Deadlines and provisional assessments

- Use the deadline in the taxpayer's invitation letter when one exists.
- Describe 14 July only for the reviewed voluntary-filing/no-invitation case.
- Say a later unsolicited provisional assessment may be issued from earlier
  data; never state that it is automatic.
- Remove the unsupported universal claim that omitted change-form categories
  default to zero. Require preparation and verification of the complete dataset.
- Do not treat moving abroad as a categorical stopzetten reason; route migration
  and residency changes to the existing unsupported/manual path.

### Entrepreneur workflows

Annual 2025 entrepreneur support becomes preparation-only for the business
section. The LLM organizes finalized profit-and-loss, balance, hours,
investment, and deduction evidence and identifies missing business categories.
It does not claim a complete business return, determine final taxable business
profit, or mark the zakelijke field map `review_ready` without a complete,
reviewed schema.

The annual workpack must represent the official P&L and balance categories and
explain which figures remain adviser/portal review items. Straightforward
eenmanszaak preparation remains useful; partnerships, BV/DGA profit, ROW,
migration, agriculture, cessation, reserves, and complex asset/depreciation
cases stay terminal manual review.

For provisional 2026, prepare a sourced, user-reviewed expected-profit forecast
for the official `Winst uit onderneming` section. Do not map it to generic
“other income.” Do not calculate business accounts, entrepreneur deductions,
Zvw, cessation profit, or final tax.

Primary source: <https://www.belastingdienst.nl/wps/wcm/connect/nl/belastingaangifte/content/ondernemer-bekijk-welke-cijfers-u-nodig-hebt-voor-uw-aangifte-inkomstenbelasting>

## Optional Python tooling

The current 18-script surface is reduced conceptually to four optional
components:

1. evidence file inventory and hashing;
2. field-map validation and human-readable rendering;
3. small, source-pinned arithmetic checks for supported Box 1/2/3 and partner
   cases;
4. developer-only source/workflow consistency checks.

Remove the heuristic `summarize_box1_inputs.py`, `summarize_box2_inputs.py`, and
`classify_box3_assets.py` runtime roles. Evidence interpretation, missing-item
reasoning, and Box 3 classification belong to the LLM. Compatibility shims are
unnecessary because these scripts are internal and the public skill/output
contracts remain stable.

Fold Box 2 input validation into the Box 2 arithmetic checker so calculation
cannot bypass normalization. Keep separate arithmetic modules only where tax
year or method separation makes a single module harder to audit. Developer
source validators may remain separate files but are one maintenance component,
not taxpayer workflow dependencies.

When Python is unavailable, each skill follows a concise equivalent checklist
from its reference contract. It does not ask the user to install Python and does
not downgrade an otherwise complete workpack solely because a script could not
run.

### Deterministic correctness requirements

- Box 3 trusted totals include only accepted, unambiguous, finite,
  non-negative rows. A generic loan is `unknown` until the LLM establishes
  whether it is a receivable asset or a debt. Manual-review rows do not alter
  trusted totals.
- Partner/allocation validators require actual booleans and explicit partner
  status. String `"false"` never behaves as true.
- Box 2 validation requires a nonblank substantial-interest percentage and
  explicit standard-case/residency confirmation. The calculator consumes a
  validated normalized payload and cannot silently change workflow/year.
- Loss-setoff cases block the numeric Box 2 result until the required reviewed
  facts are present.
- Box 1 completeness counts only reviewed, successfully extracted evidence for
  the correct tax year. Failed, deferred, indexed-only, or wrong-year records
  remain gaps. This decision is made by the LLM from the evidence index after
  the heuristic summarizer is removed.
- Validators return clear errors for ordinary malformed artifact shapes touched
  by these tax-correctness paths. Security/resource-hardening cases listed in
  the excluded scope are not expanded.

## Source provenance and legal attribution

Snapshot metadata describes hashes of reviewed local rule notes—not archived
official page bodies. Rename the metadata field and all documentation from a
generic content hash to `reviewed_note_hash_sha256`. `last_checked` means a
human reviewed the cited official source on that date; it does not prove the
remote page has not changed since.

Source-refresh planning, validators, and documentation must distinguish:

- URL reachability;
- date last retrieved or inspected;
- human review/attestation;
- hash of the synthesized local note.

Correct legal attribution in the two generic law notes. In particular, cite
Wet IB 2001 article 3.112 for eigenwoningforfait and AWR article 52 for the
business-record retention duty rather than presenting a nearby regulation as
the direct source.

## Documentation and release consistency

Update root and plugin READMEs, CONTRIBUTING, CHANGELOG, manifests, the
Claude-platform note, eval documentation, and
`llm-agent-skill-plan.md`.

Required corrections include:

- lead the Cowork quickstart with a natural-language preparation request rather
  than a required command chain;
- fix the missing slash/namespace in the provisional example and the duplicate
  `cd` in the ZIP instructions;
- remove legacy-command precedence claims;
- align Python documentation and CI with Python 3.10+;
- state throughout that Python is optional in Cowork and is never a prerequisite
  for completing a taxpayer workflow;
- add winst to contributor layout and remove stale 0.1.2 examples;
- mark `llm-agent-skill-plan.md` as historical and provide an accurate current
  completion/status matrix;
- remove the outdated Cowork screenshot from the README and distributed plugin;
- point both Codex icon roles to one retained PNG and delete the duplicate;
- add Claude `displayName`, `homepage`, and `repository` metadata;
- bump Claude and Codex manifests together to 0.1.7;
- describe the source system as reviewed-note provenance, not remote-page
  snapshot verification.

Historical missing Git tags and the ignored stale local Claude worktree are not
modified: retroactive tags would misrepresent release state, and ignored
worktrees are user-owned local data. The release instructions gain an explicit
future tag check instead.

## Tests and behavioral evaluation

Every behavior change follows RED-GREEN-REFACTOR. A focused failing test or
behavioral case must fail for the expected reason before the corresponding
implementation or skill text changes.

Required deterministic tests:

- 12 unique Claude skills and no colliding commands;
- winst session-state coverage and readiness gating;
- valid sibling field-mapper paths;
- one writer for each final artifact;
- intent-based triggering text and lazy template/output-contract loading;
- every tax correction listed above, tied to an official `source_id` and year;
- Box 3 rejected-row totals and ambiguous-loan behavior;
- strict partner booleans;
- Box 2 validated-calculator contract;
- Box 1 evidence status/year completeness through LLM workflow contracts rather
  than a summarizer script;
- absence of the three retired heuristic script roles and references;
- parity between scripted and documented manual checks for retained optional
  validators;
- source metadata field semantics and legal attribution;
- Python 3.10 compilation and documentation parity;
- fixture, offline-dataset, and behavioral-benchmark case-set equality;
- manifest/version/README/package consistency.

Required model-level cases:

- a casual Dutch-tax question does not create workflow state;
- an explicit annual preparation request routes to intake;
- annual resume includes the winst phase;
- ordinary and entrepreneur annual outputs respect their different readiness
  boundaries;
- provisional entrepreneur profit maps to the correct section without annual
  deduction calculations;
- healthcare, benefit, credit, partner, and deadline answers follow the
  corrected official-source notes;
- annual and provisional Box 3 methods remain separated;
- stopzetten payment users route to change/review;
- stale-source warnings remain informative without claiming remote comparison.

Security-specific adversarial cases are not added or changed in this release.
`PRIVACY.md` and `SECURITY.md` are also left untouched so the implementation
does not drift into the explicitly excluded security/privacy scope.

## Acceptance gates

The release is complete only when fresh evidence shows:

1. All repository unit tests pass from both repository root and standalone
   plugin root.
2. The offline dataset passes and covers every shipped fixture intended for
   behavioral verification.
3. Source-register, knowledge-pack, supported-workflow, and invocation-policy
   validators pass.
4. `claude plugin validate --strict` passes for both the nested plugin and root
   marketplace.
5. `claude plugin details` reports 12 unique skills.
6. Plugin Eval routing/analysis completes, with diagnostic scores recorded but
   no tax data deleted merely to improve a static score.
7. A fresh agent forward-test passes the non-security behavioral cases without
   seeing the expected answer.
8. Package/link/version/Python checks pass and no workspace, evidence, cache, or
   stale screenshot files ship.
9. Independent reviewers find no unresolved critical or important
   non-security findings.
10. A requirement-by-requirement audit maps every item in this specification to
    current files, tests, or runtime output.

Exact Cowork UI behavior remains a manual smoke gate unless a signed-in Cowork
session is available for direct testing. If it cannot be exercised, the README
must say which first-party Claude validation was performed and which Cowork UI
behavior remains unverified.
