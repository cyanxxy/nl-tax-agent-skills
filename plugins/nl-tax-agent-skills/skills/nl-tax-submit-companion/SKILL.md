---
name: nl-tax-submit-companion
description: Use when a user wants a manual portal checklist.
disable-model-invocation: true
allowed-tools:
  - Read
  - Grep
  - Write
  - Edit
---

# NL Tax Submit Companion

Create a step-by-step checklist from an existing workpack and field map. The taxpayer or authorized representative performs every official action manually in Mijn Belastingdienst.

Load the relevant workpack, field map, DigiD policy, submit-step reference, and checklist template. Write `workspace/shared/manual-submission-checklist.md`.

Do not log in, submit, sign, automate the portal, ask for credentials, or process credentials. Mention DigiD Machtigen when someone else helps.
