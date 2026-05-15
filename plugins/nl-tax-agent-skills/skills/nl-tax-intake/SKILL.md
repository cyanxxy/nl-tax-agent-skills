---
name: nl-tax-intake
description: Use when starting a Dutch tax task and routing the workflow.
allowed-tools:
  - Read
  - Grep
  - Write
  - Edit
---

# NL Tax Intake

Route the user to a supported workflow and create local profile files. The user will fill the official forms manually.

Load `_shared/supported-workflows.yaml`, security notes, `reference/filing-paths.md`, `reference/unsupported-cases.md`, and `templates/taxpayer-profile.yaml`.

Do:

1. Screen residency, taxpayer type, living status, fiscal partner status, requested year, and requested flow.
2. Allow only active supported workflows.
3. Route unsupported cases to `workflow_candidate: unsupported`.
4. Write `workspace/taxpayer/profile.yaml`, `workspace/shared/missing-info.md`, and `workspace/shared/assumptions.md`.

Never collect DigiD, log in, file, sign, submit, reuse old rates for future years, or write workpacks directly.
