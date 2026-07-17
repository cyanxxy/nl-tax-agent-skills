---
name: nl-tax-field-mapper
description: Use when the user explicitly wants a supported workpack mapped to source-traceable Mijn Belastingdienst fields.
argument-hint: "[annual|provisional] [year]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - AskUserQuestion
  - Bash(python3:*)
---

# NL Tax Field Mapper

Convert a reviewed workpack into a source-traceable manual-entry guide for the
official Belastingdienst portal. This skill is the sole writer of both canonical field-map artifacts:

- `workspace/annual/2025/field-map.yaml`
- `workspace/provisional/2026/field-map.yaml`

Annual and provisional workflows invoke it after confirmed workpack creation
and never write either map. Continue the same tax conversation; never announce
that an internal mapper skill or Python script is taking control.

## When to use

Use this skill when:

- `workspace/annual/2025/return-pack.md` exists and needs its annual map;
- `workspace/provisional/2026/provisional-pack.md` exists and needs its
  provisional map; or
- the user explicitly asks for a manual-entry field map from an existing
  supported workpack.

An owning annual/provisional workflow invokes this mapper automatically after
its explicitly confirmed workpack. That confirmation also authorizes the
canonical companion map, so no second mapping request is needed.

If the relevant workpack is absent, explain that it must be prepared first and
offer to continue the matching annual or provisional workflow.

## Required context

Read [`../_shared/runtime-contract.md`](../_shared/runtime-contract.md) first.
Resolve `workspace/...` against `workspace_root` in
`workspace/shared/session-progress.yaml` (or `profile.yaml`); never create a
second workspace tree. Bundled paths are relative to this skill directory and
must be resolved with host resource/file tools, not vendor-specific environment
variables or assumed shell visibility.

Before mapping, read all of
[`reference/mapper-flow.md`](reference/mapper-flow.md). It is the operating
procedure for source records, question packets, canonical-map updates,
validation, rendering, and the completion report. It delegates field policy to:

- [`reference/mapping-principles.md`](reference/mapping-principles.md) for
  provenance, confidence, omissions, readiness checks, and stable validation
  IDs;
- [`reference/annual-field-map.md`](reference/annual-field-map.md) for the 2025
  annual submission fields; or
- [`reference/provisional-field-map.md`](reference/provisional-field-map.md)
  for the 2026 provisional submission fields.

Then read session progress, the relevant workpack, and any existing canonical
map in the order defined by `mapper-flow.md`.

## Non-negotiable mapping contract

- Keep annual and provisional maps separate. Annual 2025 is backward-looking
  and evidence-based and may include actual-return input fields. Provisional
  2026 is forward-looking and estimate-based; no werkelijk-rendement input
  field or method choice exists.
- Set `tax_year` explicitly: `2025` with `annual_return`, or `2026` with
  `provisional_assessment`. Never leave it blank, `null`, or as a placeholder.
- Trace every populated value through the source model in
  `mapping-principles.md`. `user_chat` is first-class sourced input: preserve
  its verbatim quote and date and cross-index it in `user_chat_values_index`.
- Never invent a value or silently substitute zero. Represent an unsourced
  required data-entry value as `unknown`, an open question, and a missing-info
  item. A deferred optional question may remain outside `fields`, but it never
  makes the map ready.
- Omit portal credentials and portal-prefilled identity/identifier rows from
  both `fields` and `missing_fields`. This is mapping scope, not a scanner.
- Derive top-level `readiness` from the active rollup in
  `session-progress.yaml`. Use `review_ready` only when that workflow is
  complete without blocking or manual-review blockers; otherwise use `draft`.
  Structural checks may reject false readiness but never promote a draft.
- Preserve valid sourced entries when updating the canonical map unless the
  current workpack or field reference makes them obsolete. The most recently validated
  map at the canonical workflow path is authoritative; never create
  a `field-map-v2`, copy, merged map, or alternate path.

This is an agent-led, non-deterministic conversation, not a fixed questionnaire
or tax-decision engine. Select the next useful question from the evidence and
workflow state. Bundled scripts are optional structural aids; they do not
choose facts, tax positions, or readiness.

## Produce and check the manual-entry map

Follow `mapper-flow.md` to map the workpack, surface gaps, write the canonical
YAML, and present a human-readable manual-entry view. When gaps exist, also
update:

- `workspace/shared/field-map-open-questions.yaml`
- `workspace/shared/missing-info.md`

If `python3` and the resolved bundled paths are available, optionally validate
and render with:

```bash
python3 <resolved-plugin-root>/skills/nl-tax-field-mapper/scripts/validate_field_map.py <path-to-field-map.yaml>
python3 <resolved-plugin-root>/skills/nl-tax-field-mapper/scripts/render_field_map.py <path-to-field-map.yaml>
```

Structural validation without a readiness flag is the default and is the
correct check for every declared `draft`, including an intentionally draft map
with a business-schema or other manual-review blocker. Only for a map already
declared `review_ready`, add the stricter readiness assertion:

```bash
python3 <resolved-plugin-root>/skills/nl-tax-field-mapper/scripts/validate_field_map.py --require-ready <path-to-field-map.yaml>
```

Never use `--require-ready` to promote or fight an intentional draft. If either
script is unavailable, use the agent validation and direct-YAML rendering
fallbacks in `mapper-flow.md`; never skip the checks or copy a bundled script
into the workspace.

## Boundaries

- Write only the canonical map and the two shared gap artifacts under the
  resolved `workspace/` tree.
- Do not write workpacks or modify the evidence index or taxpayer profile.
- Keep maps preparation-only: never add browser-automation metadata such as
  selectors, XPath, CSS selectors, or DOM/browser locators.
- Only execute the already-resolved bundled `scripts/validate_field_map.py` and
  `scripts/render_field_map.py`. Never execute Python from `workspace/`,
  `uploads/`, or `evidence/`.

## End of turn

In two to four sentences, report the sourced-field count, the unknown or
low-confidence count, and the next decision: answer open questions or finalize
those rows as `MISSING - enter manually`.

After a canonical map is successfully created or updated:

- If this mapper was invoked from annual 2025 while a provisional 2026 workflow
  is `queued`, do not ask whether to create the annual checklist unless the
  user already requested that checklist in the current request. State, as a
  non-question, that the annual checklist remains available on request, then
  return to the annual owner for the atomic provisional handoff. A later bare
  “yes” must not be interpreted as accepting this non-question notice.
- Otherwise, offer to create the human-only manual-entry checklist. Do not
  invoke it merely because a map exists. If the user already asked for it in
  the current request, or gives an unambiguous affirmative reply to the
  immediately preceding offer, continue into the checklist without requiring
  a slash command or a second wording formula.

Authenticated-portal boundary: Never use a browser, Claude in Chrome, computer
use, screen interaction, a connector, or another tool to open or operate an
authenticated tax portal; never log in, enter or change values, click controls,
sign, send, submit, retrieve private account data, or ask for, accept, store, or
process credentials or sessions. Those actions remain human-only even with
taxpayer permission or available credentials.
