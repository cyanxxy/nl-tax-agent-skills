# OpenAI Plugin Directory submission pack

This folder contains the reviewer-facing material for a **Skills only**
submission of NL Tax Agent Skills.

## Listing

- Plugin name: NL Tax Agent Skills
- Category: Productivity
- Website: https://github.com/cyanxxy/nl-tax-agent-skills
- Support: https://github.com/cyanxxy/nl-tax-agent-skills/issues
- Privacy: https://github.com/cyanxxy/nl-tax-agent-skills/blob/main/PRIVACY.md
- Terms: https://github.com/cyanxxy/nl-tax-agent-skills/blob/main/TERMS.md
- License: Apache-2.0
- Submission type: Skills only
- Authentication: None
- Required apps: None

## Build and upload bundle

The repository plugin keeps Claude-specific invocation metadata. Build the
OpenAI upload separately so Claude-only invocation frontmatter
(`argument-hint`, `allowed-tools`, `user-invocable`, and
`disable-model-invocation`) is removed without weakening Claude behavior:

```bash
python3 submission/openai/build_bundle.py
```

Upload `dist/openai/nl-tax-agent-skills.zip`. The builder includes the Codex
manifest, skills, scripts, templates, assets, license, and package README. It
excludes the Claude manifest, taxpayer workspaces, uploads, evidence, tests,
caches, repository-local evaluation output, and Git metadata.

## Reviewer material

- `test-cases.yaml` contains exactly five positive and three negative cases.
- `release-notes.md` contains the initial OpenAI release note.
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
- Capture genuine screenshots from a clean ChatGPT Work task after installing
  the final bundle; do not use mock screenshots as reviewer evidence.
- Run and record the smoke-test matrix below.
- Submit the Skills-only draft, address review feedback, and publish only after
  approval.

## Smoke-test matrix

| Surface | Required proof |
| --- | --- |
| ChatGPT Work web | Upload fixture documents, resume after a turn boundary, and produce reviewable project files without claiming local-computer access. |
| ChatGPT Work desktop | Use only a selected local test folder, persist progress, and produce a workpack. |
| Codex desktop | Install from the repository marketplace in a fresh task and verify the five public skills are discoverable. |
| Invocation policy | Verify internal helper, maintenance, and manual-submit skills do not trigger implicitly. |
| No-shell path | Complete a fixture with Python and shell unavailable, recording agent-performed checks. |
| Safety | Run all three negative cases and verify no login, filing, signing, unsupported-year workpack, or false completeness claim occurs. |

Record the app version, plan/workspace type, region, date, prompt, result, and
reviewer for every smoke run.
