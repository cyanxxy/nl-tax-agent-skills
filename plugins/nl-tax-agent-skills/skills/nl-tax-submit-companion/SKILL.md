---
name: nl-tax-submit-companion
description: Build a manual Mijn Belastingdienst submission checklist from an existing workpack and field map — blockers first, then step-by-step entry. Use only when the user explicitly asks for a submission checklist (manual-only skill; never auto-invoked).
argument-hint: "[annual|provisional] [2025|2026]"
disable-model-invocation: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
---

# NL Tax Submit Companion

Create a step-by-step checklist from an existing workpack and field map. The taxpayer or an authorized representative performs every official action manually in Mijn Belastingdienst.

This skill is manual-only (`disable-model-invocation: true`; on Codex the same is set via `agents/openai.yaml`). Run it only when the user explicitly asks for a submission checklist.

## Read first

Resolve every `workspace/...` path against `workspace_root` from `session-progress.yaml` (or `profile.yaml`); never create a second `workspace/` tree. Resolve bundled files with host file tools (`Read` first, `Glob` or `Grep` if a path is not obvious). Do not use Bash to discover or read plugin files: in Cowork, shell commands run in an isolated VM that may not see the plugin cache even when `Read` and `Glob` can. If the host has already expanded `${CLAUDE_PLUGIN_ROOT}` or `${CLAUDE_SKILL_DIR}`, those absolute paths are fine for file tools; otherwise search within the loaded plugin/skill tree and resolve relative to this skill directory.

- The relevant workpack: `workspace/annual/2025/return-pack.md` or `workspace/provisional/2026/provisional-pack.md`.
- The matching `field-map.yaml` for annual, provisional request, or provisional change. For `provisional_2026_review`, read `workspace/provisional/2026/review-questions.md`; no field map is expected unless the review has routed to a change workpack.
- The relevant submit-step reference (`reference/annual-submit-steps.md`, `reference/provisional-submit-steps.md`, or `reference/stopzetten-submit-steps.md`).
- `templates/manual-submission-checklist.md`.
- `workspace/shared/missing-info.md` and `workspace/shared/assumptions.md`, if present.

## Output order — blockers first, then steps

Write `workspace/shared/manual-submission-checklist.md` in this order:

1. **Blockers (first).** Everything that must be resolved before the user opens Mijn Belastingdienst: unresolved `MISSING - enter manually` field-map rows, deferred items in `missing-info.md`, unconfirmed assumptions, every `manual_review_required` field, review questions marked open or change-needed, and — for a voorlopige aanslag **change** — the "prepare and verify the complete dataset; the change form requires all applicable categories, not only the changed item" reminder. If there are no blockers, say so explicitly.
2. **Pre-flight.** What to have ready: the evidence documents and the workpack open alongside the portal.
3. **Step-by-step entry.** The ordered screens/fields from the submit-step reference, each cross-referenced to its field-map row, with the value to type and its source code.
4. **Final review and submit.** The human checks to run before the user themselves presses submit.

Keep checklist wording task-focused. Do not add generic credential warning paragraphs; respond tersely if the user offers credentials.

## Partial inputs

If the workpack or field map is incomplete, do not refuse. Produce the checklist with the known steps and put every gap in the **Blockers** section so the user resolves it before filing.

## Worked example (brief)

User: "Give me the submission checklist for my 2025 return." → Read `return-pack.md` + `field-map.yaml`; find two `MISSING - enter manually` rows (WOZ-waarde, one giften amount) and one `manual_review_required` (tariefsaanpassing). Write the checklist with those three under **Blockers**, then pre-flight, then the box-by-box entry steps keyed to the field map, then the final-review list. End: "2 missing values and 1 review item block filing — resolve these first, then follow steps 1-9."

## Safety

Do not log in, submit, sign, automate the portal, ask for credentials, or process credentials. Mention authorization only when someone else helps the taxpayer file.
