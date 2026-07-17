---
name: nl-tax-submit-companion
description: Use when a user explicitly asks in natural language for a human-only manual-entry checklist from an existing annual or provisional workpack, or clearly accepts the mapper's immediate checklist offer.
argument-hint: "[annual|provisional] [2025|2026]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
---

# Manual-entry checklist

Create a Manual-entry checklist from an existing workpack and, where the
workflow produces one, its field map. The taxpayer or an authorized
representative performs every official action manually in Mijn Belastingdienst.

This skill is natural-language invocable only for explicit checklist intent.
Run it when the user directly asks for the checklist or gives an unambiguous
affirmative reply to the field mapper's immediately preceding checklist offer.
Do not run it merely because a field map exists, and never require a slash
command or magic phrase.

## Read first

Resolve every `workspace/...` path against `workspace_root` from
`session-progress.yaml` (or `profile.yaml`); never create a second `workspace/`
tree. Read `../_shared/runtime-contract.md` first. Resolve bundled files
relative to this skill directory with the host's skill-resource or file tools.
Do not depend on shell visibility or vendor-specific environment variables.

- The relevant workpack: `workspace/annual/2025/return-pack.md` or `workspace/provisional/2026/provisional-pack.md`.
- The matching `field-map.yaml` is required for annual, provisional request,
  and provisional change. It is not expected for `provisional_2026_review` or
  `provisional_2026_stopzetten`, so its absence is not a blocker for either
  workflow.
- For `provisional_2026_review`, read
  `workspace/provisional/2026/review-questions.md`. If that review has already
  routed to a generated change workpack, use the change workpack and its field
  map instead.
- The relevant submit-step reference (`reference/annual-submit-steps.md`, `reference/provisional-submit-steps.md`, or `reference/stopzetten-submit-steps.md`).
- `templates/manual-submission-checklist.md`.
- `workspace/shared/missing-info.md` and `workspace/shared/assumptions.md`, if present.

## Output order — blockers first, then steps

Write `workspace/shared/manual-submission-checklist.md` in this order:

1. **Blockers (first).** Everything that must be resolved before the user opens Mijn Belastingdienst: unresolved `MISSING - enter manually` rows and every `manual_review_required` row from an applicable field map; deferred items in `missing-info.md`; unconfirmed assumptions; review questions marked open or change-needed; and — for a voorlopige aanslag **change** — the "prepare and verify the complete dataset; the change form requires all applicable categories, not only the changed item" reminder. If there are no blockers, say so explicitly. Never report a missing field map as a blocker for review or stopzetten.
2. **Pre-flight.** What to have ready: the evidence documents and the workpack open alongside the portal, plus the field map when that workflow produces one.
3. **Step-by-step entry or review.** Use the ordered human steps from the
   relevant submit-step reference. Cross-reference values and source codes to
   field-map rows only for annual, provisional request, or provisional change.
   For review, use the review-question rows and route any change-needed item to
   the change flow; for stopzetten, use the stopzetten reference without
   inventing field-map rows.
4. **Final human review.** The checks the taxpayer performs before deciding
   whether to sign and submit personally.

Keep checklist wording task-focused. Do not add generic credential warning paragraphs; respond tersely if the user offers credentials.

## Partial inputs

If the workpack or an applicable field map is incomplete, do not refuse.
Produce the checklist with the known steps and put every actual gap in the
**Blockers** section so the user resolves it before filing. A field map remains
required for annual, provisional request, and provisional change; it is not an
input for provisional review or stopzetten.

## Worked example (brief)

User: "Give me the Manual-entry checklist for my 2025 return." → Read `return-pack.md` + `field-map.yaml`; find two `MISSING - enter manually` rows (WOZ-waarde, one giften amount) and one `manual_review_required` (tariefsaanpassing). Write the checklist with those three under **Blockers**, then pre-flight, then the box-by-box entry steps keyed to the field map, then the final-review list. End: "2 missing values and 1 review item block filing — resolve these first, then follow steps 1-9."

## Safety

Apply the authenticated-portal boundary in `../_shared/runtime-contract.md`.
Never open or navigate Mijn Belastingdienst with a browser, Claude in Chrome,
computer use, screen interaction, or another tool; never log in, enter or change
values, sign, send, or submit; and never ask for or process credentials. Write
every portal action with an explicit human subject. Mention authorization only
when someone else helps the taxpayer file.
