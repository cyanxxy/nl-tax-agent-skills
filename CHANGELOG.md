# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.6] — 2026-07-04

Entrepreneur (winst uit onderneming) support for the 2025 annual return. A
straightforward IB-ondernemer with an eenmanszaak (the usual ZZP legal form) is
now a supported `annual_2025` case; complex business forms remain out of scope.
Every 2025 figure was researched and adversarially verified against
belastingdienst.nl and wetten.overheid.nl. Plugin manifests are bumped from
`0.1.5` to `0.1.6`.

### Added

- **Winst uit onderneming knowledge pack** — new `_shared/knowledge/years/2025/
  entrepreneur/` directory with six reviewed rule notes (ondernemer criteria and
  urencriterium, ondernemersaftrek, MKB-winstvrijstelling, investeringsaftrek,
  winst/kosten/administratie, and the entrepreneur aangifte), backed by 23 new
  Belastingdienst source-register entries.
- **`nl-tax-winst` background helper** — internal, annual-only helper that
  prepares the winst uit onderneming section (turnover → investeringsaftrek
  such as the KIA → ondernemersaftrek → MKB-winstvrijstelling), mirroring the
  box2/box3 helper contract.
- **Annual workflow** — new Phase 2A (Winst uit onderneming compilation), a new
  "Winst uit onderneming notes" output section (the workpack now has 20 required
  sections), and a `Winst uit onderneming` section in the annual field-map
  reference (`onderneming.*` fields, all conditional).
- **Intake routing** — a `business` profile section and a business-form screen
  that routes an eenmanszaak / ZZP into `annual_2025` while keeping partnerships
  (VOF/maatschap/CV), DGA/BV winst, agrarisch, zeevarenden, and cessation events
  on the narrowed blocked `annual_2025_entrepreneurs` candidate.
- **Evidence types** — a Business / Enterprise category (winst-en-verliesrekening,
  balans, factuur, urenadministratie, investering-factuur, KvK-uittreksel).
- **Tests and eval** — `tests/test_entrepreneur_unlock.py` plus a positive
  `annual/entrepreneur-zzp` fixture and offline-dataset case.

### Changed

- **Provisional guard** — `nl-tax-provisional-assessment` now explicitly refuses
  to prepare winst uit onderneming; entrepreneur support is annual-2025 only.
- **Blocked roadmap** — `annual_2025_entrepreneurs_roadmap` is narrowed from all
  business profit to complex business forms only.

## [0.1.5] — 2026-07-03

Bug fixes from a two-model code review (Claude + Codex) of all Python scripts,
with the encoded tax rules re-verified against belastingdienst.nl and
wetten.overheid.nl. Plugin manifests are bumped from `0.1.4` to `0.1.5`.

### Fixed

- **Box 3 asset parsing** — Dutch dot-thousands amounts (`50.000`) were parsed
  as `50.0` by the bare `float()` fallback, undervaluing assets 1000-fold;
  separator formats are now tried first.
- **Money math** — the box 3 annual and provisional calculators now compute in
  `Decimal` end-to-end; the box 1 own-home script rounds ROUND_HALF_UP via
  `Decimal` and rejects NaN/inf inputs. The tariefsaanpassing grondslag stays
  the gross aftrekbare kosten per art. 2.10 lid 2 (confirmed against the
  official Hillen example) and is now definitively "no" with zero deductible
  costs.
- **Fail-closed invocation-policy validator** — frontmatter is split on fence
  lines and unparseable frontmatter is an error, so a skill can no longer be
  silently dropped from the Codex-policy check.
- **Source-refresh allowlist** — `fetch_sources.py` now uses `urlparse` and
  requires HTTPS, rejecting userinfo tricks like
  `https://allowed.nl:pw@evil.com`.
- **Werkelijk-rendement gate** — the field-map validator now also scans
  `missing_fields` and top-level notes in provisional maps (explanatory
  redirect notes stay allowed); unknown CLI flags are rejected.
- **Box 2 hardening** — NaN/inf inputs raise clean errors, typo'd payload keys
  are flagged instead of silently defaulting to 0, the explicit-zero presence
  rule matches between validator and calculator, duplicate warnings are
  deduplicated, and `--taxpayer-pct` alone derives the partner percentage.
- **Robustness** — empty/malformed YAML and non-mapping entries now produce
  clean validation errors instead of tracebacks across the validators,
  `build_snapshots.py`, `render_field_map.py`, `validate_allocation.py`, and
  `summarize_box1_inputs.py`; the evidence indexer prunes hidden directories;
  the offline eval verifier escapes glob metacharacters, works from any
  working directory, and scans the output tree once per run.

### Added

- `tests/test_review_fixes.py` regression suite pinning every fix above,
  including the official 2026 Hillen/tariefsaanpassing example; the suite
  grows from 152 to 174 tests.

## [0.1.4] — 2026-07-02

This release resolves a full third-party review of v0.1.3 (4 critical, 16
major, 30 minor findings): tool-policy and cross-layer contract drift, register
and eval-fixture inconsistencies, script robustness, and a source re-attestation
verified against the official pages. Plugin manifests are bumped from `0.1.3`
to `0.1.4`.

### Fixed

- **`Glob` tool policy** — every SKILL.md body instructed `Glob`-based
  discovery while all 11 skills and 7 commands omitted `Glob` from
  `allowed-tools`, silently breaking bundled-file resolution on hosts that
  enforce the list. `Glob` is now allowed everywhere it is instructed.
- **Bundled-file discoverability** — `nl-tax-box1-home`, `nl-tax-box2`,
  `nl-tax-box3`, `nl-tax-partner-deductions`, and
  `nl-tax-provisional-assessment` now name their own `reference/` files and
  scripts explicitly instead of pointing at "the relevant references".
- **Annual field-map write timing** — `annual-flow.md` Phase 7 prepared AND
  wrote `field-map.yaml` while `SKILL.md` gated the same file behind the
  generation gate; Phase 7 now prepares only, and the write happens with
  `return-pack.md` in Phase 10 behind the gate.
- **Out-of-scope eval fixture** — now expects the specific blocked candidates
  (`annual_2025_migration_m_form`, `annual_2025_deceased_f_form`,
  `annual_2025_entrepreneurs`, `annual_2025_nonresident_c_form`) instead of
  contradicting the routing config with a generic `unsupported`.
- **`partner-box3-actual` fixture** — corrected the combined heffingsvrij
  vermogen to EUR 115,368, recomputed the actual-return total to include the
  fixture's own unrealized value declines, and removed a duplicate YAML key
  that silently dropped an assertion.
- **`source-staleness` fixture** — replaced the self-contradicting
  `does_not_block_workpack: false` with `blocks_workpack: false` and switched
  the setup to a production prose freshness policy.
- **Evidence taxonomy** — added `dividend_statement` and
  `share_sale_agreement`, the two types the Box 2 fixtures already used.
- **Knowledge notes** — AOW note no longer contradicts itself on how far the
  AOW age is fixed (67 through 2027; 67y3m for 2028–2031); credits note's
  non-AOW boundary corrected from "born after 1957" to born in 1959 or later,
  with 1958-born taxpayers flagged for transitional review; ODB compat files
  renamed to match their sources and the incorrect "Omgevingsloket" expansion
  corrected to Ondersteuning Digitaal Berichtenverkeer; multi-source
  `source_id:` headers normalized to `source_ids:`.
- **Gating literals** — `box2.has_aanmerkelijk_belang` condition unified to
  the profile template's `true`/`false`; the review-questions template
  workflow enum gains `provisional_2026_review`; the simple-resident fixture
  no longer expects a standalone annual `review-questions.md`.
- **Scripts** — `validate_own_home_inputs.py` reports clean CLI errors on
  malformed values and rejects negative amounts; `validate_field_map.py`
  recognizes the template's `updated_at`/`user_chat_values_index` keys and
  reports an unreadable field reference as a validation error instead of a
  traceback; `summarize_box3_provisional_2026.py`'s partner note reports the
  allowance actually applied and documents the `--heffingsvrij 0` semantics;
  `fetch_sources.py` usage docs show the required scope positional.
- **Shipped test suite** — the four tests reading dev-repo-only files
  (marketplace manifests, `.gitignore`, `CHANGELOG.md`) now skip cleanly in a
  standalone package run; a dead unknown-skill assertion now checks the
  stream the validator actually emits on.

### Added

- **Register coverage** — `bd_machtigen_authorization` is required by both
  active workflows (the workflows validator now treats `workflow: security`
  sources as all-workflow and enforces their presence); `knowledge_dirs`
  cover every required snapshot; `bd_invorderingsrente` is scoped all-year
  and required by the provisional workflow.
- **Blocked `annual_2026` workflow** — the most likely near-future request now
  has an explicit roadmap entry instead of falling through to generic
  `unsupported`.
- **Cross-skill state** — `stopzetten_direction` has a home in the taxpayer
  profile (`workflows.provisional_2026.stopzetten_direction`);
  `last_question_asked` added to the session-progress template (schema v1.3).
- **Runtime staleness warning** — annual and provisional skills warn once
  (naming stale `source_id`s) when the source pack is past its re-check
  cadence; staleness never blocks workpack generation.
- **Season-aware freshness gate** — "provisional assessment season (January)"
  policies are treated as calendar events: stale only when `last_checked`
  predates the most recent 1 January, instead of a 365-day fallback.
- **Workflow-gate attestation** — `supported-workflows.yaml`'s
  `last_reviewed` is now validated (missing/invalid/future = error).
- **Docs** — both READMEs document the eval fixtures, the repo-level offline
  eval harness, standalone test runs, script prerequisites (Python 3.8+,
  PyYAML), and the annual-2026 blocked workflow.

### Changed

- **Read cadence** — workpack skills re-read workspace state every turn but
  load bundled references and rate sheets once (re-read on resume), replacing
  the unrealistic mandatory-every-turn full reload; `sources_loaded` is
  deduplicated so the workpack's Sources Used section can list IDs exactly
  once.
- **Evidence intake** — host attachments are copied byte-faithfully via
  allowed tooling only, with an explicit index-in-place fallback when no
  faithful copy is possible; hashing uses an inline `python3 -c hashlib`
  command permitted by the skill's tool policy.
- **Source re-attestation** — all sources whose `last_checked` predated their
  snapshot's creation were re-verified against the official pages (box 1/2/3
  rates 2025 and 2026, heffingsvrij vermogen, belastingrente,
  invorderingsrente, AOW-leeftijd schedule) and re-attested at 2026-07-02;
  snapshot hashes and metadata rebuilt.

## [0.1.3] — 2026-07-01

This release removes the in-plugin security enforcement now owned by the host
environment, aligns the skills with Cowork's execution model, and applies a
second developer-audit pass (helper write contracts, script robustness,
documentation accuracy, and a source-freshness refresh). Plugin manifests are
bumped from `0.1.2` to `0.1.3`.

### Fixed

- **Helper write contracts** — the four background helpers (`nl-tax-box1-home`,
  `nl-tax-box2`, `nl-tax-box3`, `nl-tax-partner-deductions`) now declare `Write`
  and `Edit` in `allowed-tools`, matching the `workspace/shared/` notes files
  their contracts require them to write; clarified that helpers never update
  `session-progress.yaml` (the owning workflow skill owns session state).
- **Command wrappers** — all seven slash-command descriptions now match their
  SKILL.md descriptions, removing divergent duplicate registrations.
- **Permission patterns** — normalized `Bash(python3 …*.py:*)` mid-pattern
  globs (which never match under prefix-match permission rules) to
  `Bash(python3:*)` across skills and commands.
- **Taxpayer profile** — template v1.3 adds `box2.has_aanmerkelijk_belang`
  (the field the annual workflow and field mapper gate on); intake now records
  the Box 2 yes/no answer there with provenance.
- **Documentation accuracy** — annual SKILL phase count corrected to the 13
  phases of `annual-flow.md`; `sources_loaded` correctly described as a
  top-level `session-progress.yaml` key; intake may keep a volunteered
  `display_name` as an unverified label but never asks for names or BSN;
  deferred evidence provenance unified on `source: unknown` +
  `extraction_status: deferred`; `refresh-policy.md` rewritten to document the
  real freshness mechanism (free-text policy prose, cadence-keyword thresholds
  in the blocking validator, `source_type` thresholds in the fetch planner).
- **Script robustness** — `--help` on all manually-parsed scripts; clear
  errors instead of tracebacks on invalid YAML, non-numeric inputs, and
  read-only installs; absolute-path diagnostics in `summarize_box1_inputs.py`;
  `test_eval_verifier.py` skips gracefully when the offline verifier is not
  shipped with the package.
- **Packaging** — dropped the trailing slash in both manifests' `skills` path;
  bundled the Apache-2.0 `LICENSE` in the plugin package; made the package
  README self-contained (no repo-relative links) with a not-tax-advice
  disclaimer; removed the orphaned `methods/alef.md` knowledge note.

### Removed

- Removed all DigiD handling and references throughout the plugin — knowledge files,
  skills, workpacks, submission checklists, eval fixtures, and docs. The plugin never logs
  in or submits, so DigiD never enters its workflow. Repo hygiene and product-scope rules
  remain: the plugin still does not ask for BSN or credentials, while host-level
  sensitive-data handling owns enforcement.
- Removed the prompt-injection guardrail: the `security/prompt-injection.md` policy, the
  evidence indexer's `untrusted-content-policy.md` and its content-marker /
  `suspicious_content_detected` scanning, the "treat as data / never follow embedded
  instructions" instructions across skills, and the prompt-injection eval case. The host
  model (Claude/Codex) provides prompt-injection resistance.
- Removed the remaining in-plugin security/privacy enforcement — the host environment
  (notably Cowork's sandboxed VM and the host model) owns it. Dropped from
  `validate_field_map.py` the credential-keyword ban and the BSN/IBAN field-name and
  stored-value (elfproef / NL-IBAN) scan; dropped from `index_evidence.py` the
  symlink/real-path containment, file-count/size/depth resource limits, and
  macro/`active_content` flagging. Their unit tests were removed. What remains is product
  scope and tax correctness, not security: the tool still never logs in/signs/submits (the
  field-map validator still rejects browser/submission fields) and provisional 2026 never
  carries werkelijk rendement.

### Changed

- Updated skill path-resolution guidance for Claude Cowork: bundled plugin files are now
  resolved through host file tools (`Read`/`Glob`/`Grep`) instead of Bash-based
  `${CLAUDE_PLUGIN_ROOT}` discovery, with manual validation fallbacks when Cowork's isolated
  Bash VM cannot see bundled plugin scripts.
- Evidence-index schema: dropped `suspicious_content_detected` and `suspicious_count`
  (and `active_content_detected` / `active_content_count`, with the security-enforcement
  removal above).
- Cowork alignment: where the bundled validator/calculator scripts cannot run (the host
  Bash sandbox cannot reach the plugin package), skills now restate each script's guarantee
  declaratively — field-map structural checks, partner-allocation invariants, and evidence
  `file_sha256` via a host hash command or an explicit `null`.
- Source-refresh report schema: each source entry now also reports
  `staleness_threshold_days`, `age_days`, and `expires_on`.
- Field-map validator: required reference rows the portal pre-fills are exempt from the
  manual-entry coverage and readiness checks; widened pre-fill marker detection
  (`auto-fill`, `vooraf ingevuld`).

### Added

- Registered `bd_box3_2025_worked_examples` as a mandatory source for the annual-return and
  box 3 skills.
- Added the `box2` subsection to the provisional session-progress template so a fresh
  session matches the provisional workpack generation gate.
- Added Box 1 own-home rate-parity tests (eigenwoningforfait brackets, Hillenregeling, and
  tariefsaanpassing) that guard `validate_own_home_inputs.py` constants against the
  canonical knowledge notes, matching the existing box 2 / box 3 parity tests.
- Wired the `_shared/templates/` missing-info, assumptions, and
  review-questions registers into the annual and provisional flows as seeds.
- `evidence_files` for the partner Box 2 allocation eval fixture and a new
  `test_fixture_schema.py` suite enforcing one fixture shape and a documented
  workflow-label vocabulary.
- Source refresh pass (2026-07-01): re-verified 16 registered sources online
  and bumped `last_checked`; `regels_overheid_regelspraak` was unreachable and
  keeps its previous attestation.

## [0.1.2]

This release applies a verified audit pass: tax-content corrections, workflow
hardening, validator and tooling improvements, and documentation accuracy fixes.
Plugin manifests are bumped from `0.1.1` to `0.1.2`.

### Fixed

- **Annual 2025 own-home content** — corrected the eigen-woning
  tariefsaanpassing (aftrekbeperking) handling and the Hillen
  (geen of geringe eigenwoningschuld) rounding.
- **Penalties and interest** — corrected late-filing (verzuimboete),
  belastingrente, and invorderingsrente descriptions.
- **Tax credits** — corrected the gecombineerde heffingskorting and
  arbeidskorting treatment.
- **Field-map readiness** — added a readiness gate so a field map is only
  produced when the upstream workpack is complete.
- **Input hardening** — hardened Box 2, Box 3, and partner-allocation inputs
  against malformed or out-of-range values.
- **Evidence indexer** — added symlink containment, an explicit
  hash-failure status, stable evidence IDs, relative-path recording, and a
  macro flag for `.xls`/legacy Office files.
- **Source freshness** — corrected freshness-prose parsing and made
  stale `mandatory_for` sources block validation.
- **Source register** — added HTTPS URL validation for registered sources.

### Added

- Continuous integration workflow (`.github/workflows/ci.yml`) running the full
  validation gate on push and pull request.
- `requirements.txt` pinning `PyYAML>=6.0` for the validator and helper scripts.
- `SECURITY.md`, `PRIVACY.md`, and `TERMS.md` top-level project documents.
- `CHANGELOG.md` (this file).

### Changed

- **Source-refresh report schema** — `scripts/fetch_sources.py --fetch` now
  reports plan-only refresh intent with `refresh_plan_requested` and
  `operation`; the legacy `dry_run` and generic `mode` report keys were
  removed.
- Documentation accuracy: corrected cross-host wording (Codex progressive
  disclosure of skill `name`/`description`/path before loading the full
  `SKILL.md`, and the fact that Claude frontmatter invocation/tool keys are not
  honored on Codex), added a retention/cleanup pointer, and noted that host
  runtime behavior is not integration-tested and must be verified in the target
  host before release.
- Public workflow copy: command wrappers and first-turn intake/reporting
  instructions now keep skill invocation, workspace setup, and YAML state
  details out of user-facing responses.
- Added `author.url` to the Claude and Codex plugin manifests and the
  marketplace manifest, and repointed the Codex `privacyPolicyURL` and
  `termsOfServiceURL` at `PRIVACY.md` and `TERMS.md`.

## [0.1.1]

- Initial published plugin manifests for the `nl-tax-agent-skills` plugin.
