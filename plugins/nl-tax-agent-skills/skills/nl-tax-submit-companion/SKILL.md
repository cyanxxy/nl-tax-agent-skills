---
name: nl-tax-submit-companion
description: Build a manual Mijn Belastingdienst submission checklist from an existing workpack and field map — blockers first, then step-by-step entry. Manual-only; never logs in or submits.
disable-model-invocation: true
allowed-tools:
  - Read
  - Grep
  - Write
  - Edit
---

# NL Tax Submit Companion

Create a step-by-step checklist from an existing workpack and field map. The taxpayer or an authorized representative performs every official action manually in Mijn Belastingdienst. This skill never logs in, submits, signs, or automates the portal.

This skill is manual-only (`disable-model-invocation: true`; on Codex the same is set via `agents/openai.yaml`). Run it only when the user explicitly asks for a submission checklist.

## Read first

Resolve every `workspace/...` path against `workspace_root` from `session-progress.yaml` (or `profile.yaml`); never create a second `workspace/` tree. If a bundled path does not resolve, get the plugin root with `echo "${CLAUDE_PLUGIN_ROOT}"` and resolve from `${CLAUDE_PLUGIN_ROOT}/skills/nl-tax-submit-companion/`.

- The relevant workpack: `workspace/annual/2025/return-pack.md` or `workspace/provisional/2026/provisional-pack.md`.
- The matching `field-map.yaml`.
- `reference/no-digid-policy.md` and the relevant submit-step reference (`reference/annual-submit-steps.md`, `reference/provisional-submit-steps.md`, or `reference/stopzetten-submit-steps.md`).
- `templates/manual-submission-checklist.md`.
- `workspace/shared/missing-info.md` and `workspace/shared/assumptions.md`, if present.

## Output order — blockers first, then steps

Write `workspace/shared/manual-submission-checklist.md` in this order:

1. **Blockers (first).** Everything that must be resolved before the user opens Mijn Belastingdienst: unresolved `MISSING - enter manually` field-map rows, deferred items in `missing-info.md`, unconfirmed assumptions, every `manual_review_required` field, and — for a voorlopige aanslag **change** — the "enter ALL data again; anything not re-entered defaults to zero" reminder. If there are no blockers, say so explicitly.
2. **Pre-flight.** What to have ready: DigiD on a separate device (never entered here), the evidence documents, and the workpack open alongside the portal.
3. **Step-by-step entry.** The ordered screens/fields from the submit-step reference, each cross-referenced to its field-map row, with the value to type and its source code.
4. **Final review and submit.** The human checks to run before the user themselves presses submit.

## Partial inputs

If the workpack or field map is incomplete, do not refuse. Produce the checklist with the known steps and put every gap in the **Blockers** section so the user resolves it before filing.

## Worked example (brief)

User: "Give me the submission checklist for my 2025 return." → Read `return-pack.md` + `field-map.yaml`; find two `MISSING - enter manually` rows (WOZ-waarde, one giften amount) and one `manual_review_required` (tariefsaanpassing). Write the checklist with those three under **Blockers**, then pre-flight, then the box-by-box entry steps keyed to the field map, then the final-review list. End: "2 missing values and 1 review item block filing — resolve these first, then follow steps 1-9."

## Safety

Do not log in, submit, sign, automate the portal, ask for credentials, or process credentials. DigiD is never collected, stored, or echoed. Mention DigiD Machtigen when someone else helps the taxpayer file.
