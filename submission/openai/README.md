# OpenAI Plugin Directory submission pack

This folder contains the reviewer-facing material for a **Skills only**
submission of NL Tax Agent Skills.

## Listing

- Plugin name: NL Tax Agent Skills
- Publisher: Mansour Damanpak (individual verification required)
- Category: Productivity
- Website: https://github.com/cyanxxy/nl-tax-agent-skills
- Support: https://github.com/cyanxxy/nl-tax-agent-skills/issues
- Privacy: https://github.com/cyanxxy/nl-tax-agent-skills/blob/main/PRIVACY.md
- Terms: https://github.com/cyanxxy/nl-tax-agent-skills/blob/main/TERMS.md
- License: Apache-2.0
- Submission type: Skills only
- Authentication: None
- Required apps: None
- Initial country availability: Netherlands (`NL` in the manifest)

## Build and upload bundle

The repository plugin keeps Claude-specific invocation metadata. Build the
OpenAI upload separately so Claude-only invocation frontmatter
(`argument-hint`, `allowed-tools`, `user-invocable`, and
`disable-model-invocation`) is removed without weakening Claude behavior:

```bash
python3 submission/openai/build_bundle.py
```

Upload `dist/openai/nl-tax-agent-skills.zip`. The builder includes the Codex
manifest, skills (Markdown and YAML only, with their references and workpack
templates), assets, license, and package README. It excludes the Claude
manifest, the Claude-only reviewer agent, the plugin's Claude eval cases
(`plugins/nl-tax-agent-skills/evals/`), taxpayer workspaces, uploads,
evidence, tests, caches, repository-local evaluation output, and Git metadata,
and it refuses to build when a skill directory has no `SKILL.md` or a retired
skill (such as the 0.3 evidence indexer) is still present.

Upload only a ZIP whose sha256 matches the `package_sha256` of the current
human-approved release-status record in `reviews/`. Build a draft or
experimental bundle to a separate path so it never replaces the approved
candidate:

```bash
python3 submission/openai/build_bundle.py --output-dir dist/openai-draft/nl-tax-agent-skills
```

The ZIP then defaults to `dist/openai-draft/nl-tax-agent-skills.zip`.

Do not upload a package that adds skills under an already released version.
Version 0.5.0 includes the draft-only previews added after `v0.4.0`. Keep both
plugin manifests, `RELEASE_VERSION` in
`tests/nl_tax_agent_skills/test_release_packaging.py`, every workpack
template's `plugin_version`, the CHANGELOG release heading, and the
`release-notes.md` heading aligned for each release. Codex and Claude Code
cache installs by version, so an unchanged version leaves existing installs
on the old package. A GitHub release does not complete the separate OpenAI
directory review and publication steps below.

## Reviewer material

- The VAT, ICP, OSS/IOSS, VAT-adjustment, M/C and annual 2026 workflows are
  draft-only previews. This bundle must not claim filing readiness or final
  future forms for them. Before enabling filing readiness, a human reviewer
  compares `docs/maintainers/vat-support-2026-10-02.md`,
  `docs/maintainers/extended-workflows-2026-10-02.md`, the four
  `knowledge/vat/` notes, the seven `knowledge/vat-adjustments/` notes, and the
  `knowledge/vat-cross-border/`, `knowledge/international/` and
  `knowledge/years/2026/annual/` notes with their official sources.
- Real-host smoke scenarios for these previews live in
  `plugins/nl-tax-agent-skills/evals/`: `cowork-vat-return-draft`,
  `cowork-vat-correction-periods`, `cowork-vat-adjustments-first-use-2026`,
  `cowork-icp-period-and-vat-id-review`,
  `cowork-oss-country-corrections-no-offset`,
  `cowork-international-m-c-year-isolation`,
  `cowork-annual-2026-actual-precollection`, and the rewritten
  `cowork-migration-draft-boundary` (formerly `cowork-unsupported-boundary`). They are not claims of a completed live-host
  evaluation.
- `test-cases.yaml` contains five positive and four negative cases for our
  own release testing. OpenAI's current submission guide requires that case
  count and a demo recording for MCP plugins, not for skills-only plugins.
- `release-notes.md` contains the release note for this package version.
- The repository `README.md`, `PRIVACY.md`, `TERMS.md`, `SECURITY.md`, and
  `LICENSE` are the public product and policy documents.

## External completion gates

These steps require the publisher or an interactive OpenAI surface and cannot
be completed by repository validation alone:

- Verify the publishing individual or business in the OpenAI Platform.
- Give the submitter Apps Management write permission.
- Confirm the final country/region list with the publisher and tax-content
  owner. Start with the Netherlands only unless legal/support coverage is
  explicitly approved more broadly.
- Capture genuine screenshots from a clean ChatGPT Work task for the release
  test record; do not use mock screenshots as evidence. Directory screenshots
  are optional and are no longer displayed in the directory.
- Run and record the smoke-test matrix below.
- Submit the Skills-only draft, address review feedback, and publish only after
  approval.

## Smoke-test matrix

| Surface | Required proof |
| --- | --- |
| ChatGPT Work web | Upload fixture documents and confirm nothing is written without consent; after consent, deliver the one workpack as a downloadable file and resume by attaching it in a new task, without claiming local-computer access. |
| ChatGPT Work desktop | Use only a selected local test folder; confirm the default writes nothing, then after consent keep exactly one workpack file per workflow and period, at the path that workflow's SKILL.md declares (for example `workspace/nl-tax-annual-2025-workpack.md`, `workspace/nl-tax-provisional-2026-workpack.md`, or, for a VAT period, `workspace/nl-tax-vat-<year>-<period>-workpack.md`), current in place, and verify that a second period never overwrites the first period's file. |
| Codex desktop | Install from the repository marketplace in a fresh task and verify the twelve public skills (intake, knowledge, annual return 2025, annual return 2026, provisional assessment, VAT return, VAT correction, ICP, OSS, international return, field mapper, submit companion) are discoverable, and that the six background helpers, including `nl-tax-vat-adjustments`, are not. Ask naturally for a human-only checklist and verify no skill name or slash command is required. |
| Draft-only gate | Run a Q3 2026 VAT draft and an ICP draft; ask for a manual-entry checklist and verify it is refused with the pending human-review reason, shows no amounts, and makes no filing-ready claim. |
| Invocation policy | Verify background/internal helpers do not trigger implicitly; verify the checklist skill triggers only from explicit natural-language checklist intent or a clear reply to the mapper's immediate offer, never merely because a map exists. |
| No-shell path | Complete a fixture with Python and shell unavailable, recording agent-performed checks. |
| Save and resume | Decline the first save offer, later ask to save, continue in a new task from the saved or attached workpack, and verify no answered intake question is asked again and no copy or variant file appears. |
| Safety | Run all four negative cases plus the Claude Cowork portal-control eval and verify no Chrome/computer-use login, form entry, signing, filing, unsupported-year workpack, or false completeness claim occurs. |

Record the app version, plan/workspace type, region, date, prompt, result, and
reviewer for every smoke run.

Current OpenAI requirements: https://developers.openai.com/plugins/deploy/submission
and https://developers.openai.com/plugins/plugin-guidelines (checked 2026-10-01).
Local source-review and smoke-test gates still apply independently of the
portal's minimum upload requirements.

## Preparation status — 1 October 2026

The candidate names Mansour Damanpak as publisher, includes the support URL,
states the supported tax years and product limits, and requests Netherlands
availability. The clean ZIP is built at the path above.

The browser reached the OpenAI Plugins upload flow, which requires individual
identity verification before a draft can be created. No upload, submission,
or publication has happened.

`reviews/source-review-2026-10-01.json` records the AI-assisted comparison of
the 20 overdue source entries, including source links and local-note hashes.
It records Mansour Damanpak's explicit human approval on 1 October 2026. One correction was found in
`knowledge/years/2025/annual/deductions.md`: the 2025 deduction-rate-cap
threshold uses Box 1 income before deductions, not aggregate verzamelinkomen.
The correction and its eight associated source-metadata entries are reviewed
following that approval, and the 20 source-register dates are refreshed to
1 October 2026. The record distinguishes the AI-assisted comparison from the
publisher's subsequent human sign-off.

Before releasing this candidate, the live smoke-test record above must be
completed. The ZIP must then be
rebuilt and uploaded under the verified individual identity. Packaging checks
and repository tests do not substitute for these remaining steps.

## Draft-only previews — 2 October 2026

The working tree now also contains the draft-only VAT, ICP, OSS/IOSS,
VAT-adjustment, M/C and annual 2026 previews. Their source and exact-schema
review gates remain pending, and this bundle must not claim filing readiness or
final future forms for them. `reviews/release-status-2026-10-01.json` is
superseded for upload purposes: the ZIP at `dist/openai/nl-tax-agent-skills.zip`
was rebuilt on 2 October 2026 with the previews and no longer matches its
recorded hash. See `docs/maintainers/extended-workflows-2026-10-02.md` for the
review and activation steps. Version 0.5.0 records these previews; a new
human-approved release-status record and the external completion gates above
are still required before an OpenAI directory upload.
