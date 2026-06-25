# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
