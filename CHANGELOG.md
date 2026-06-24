# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
