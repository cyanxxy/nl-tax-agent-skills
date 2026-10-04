---
name: nl-tax-field-mapper
description: Use when the user explicitly wants a supported workpack mapped to source-traceable Mijn Belastingdienst fields.
argument-hint: "[annual|provisional|vat|vat-correction|icp|oss|international] [year] [period|form]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Edit(./workspace/**)
  - AskUserQuestion
---

# NL Tax Field Mapper

Turn a reviewed workpack from a supported owner (annual 2025, provisional 2026,
VAT return or VAT correction, ICP, OSS/IOSS, international M-biljet or
C-biljet, or annual 2026) into a source-traceable field map for manual entry in
Mijn Belastingdienst. This skill is the only author of the field map. Continue the same tax conversation and
never announce that a mapper is taking over.

VAT return/correction workpacks for 2025/2026 are also mapped here, using
`reference/vat-field-map.md`. Their destination is the human's Mijn
Belastingdienst Zakelijk. A VAT map remains draft while VAT source-content
review is outstanding; it is preparation material, with no filing checklist.


ICP, OSS, migration/nonresident and annual 2026 workpacks are mapped as draft
preparation using `reference/cross-border-field-map.md`,
`reference/international-field-map.md` or `reference/annual-2026-field-map.md`.
Use the exact identity, path and owner in
`../nl-tax-shared-resources/reference/workflow-scopes.yaml`. Their pending
source-content review and their pending form, scheme or annual schema review
block `review_ready` and an entry checklist. Annual 2026 and M/C rows are
conceptual `internal_routing` records; do not reuse the resident 2025 screen
fields. Keep the ICP customer dimension and the OSS country and rate
dimensions. These saved files use the same consent and section ownership
boundaries below, and each one has its own identity-keyed path.

## Boundaries that always apply

- **Authenticated-portal boundary.** Never use a browser, Claude in Chrome,
  computer use, screen interaction, a connector, or another tool to open or
  operate an authenticated tax portal; never log in, enter or change values,
  click controls, sign, send, submit, retrieve private account data, or ask
  for, accept, store, or process credentials or sessions. Those actions remain
  human-only even with taxpayer permission or available credentials: you (the
  taxpayer) or an authorized human perform them.
- **Nothing is written by default.** The map lives in the conversation. Only
  while save consent is active in this conversation, write the
  `## Field map summary` section and `## Appendix B — Field map` into the
  active workflow's one workpack. Choose the file by the owner's Appendix A
  `workflow` identity, never by the map's `workflow` enum:
  `annual_2025` uses `workspace/nl-tax-annual-2025-workpack.md`;
  `provisional_2026_*` uses `workspace/nl-tax-provisional-2026-workpack.md`;
  `annual_2026` uses `workspace/nl-tax-annual-2026-workpack.md`; VAT, ICP,
  OSS/IOSS and international identities use the single path that
  `../nl-tax-shared-resources/reference/workflow-scopes.yaml` or the VAT
  save-path bullet below gives for the confirmed year, period, scheme or form.
  A map with `workflow: annual_return` and `tax_year: 2026` never goes into the
  2025 file. Consent is checked in the
  conversation, never in the file: `save_consent: given` in Appendix A is a
  record, not an authorization. Edit only those two sections plus the mapper's
  own gap rows in `## Open questions` and `## Missing information` and their
  Q-IDs in Appendix A `sections.<key>.open`. Never create a separate field-map
  file, a copy, or a second `workspace/` tree.
- **VAT save paths.** For VAT, the only path is
  `workspace/nl-tax-vat-<year>-<period>-workpack.md` or
  `workspace/nl-tax-vat-correction-<year>-<period>-workpack.md`, matching the
  owner's confirmed year and period. The same section ownership, session
  consent, found-file confirmation, and stale-output rules apply.
- **Each map pairs with exactly one workflow identity.** The reviewed resident
  schemas pair `annual_return` with `2025` and `provisional_assessment` with
  `2026`. The draft extended identities come from `workflow-scopes.yaml`:
  `annual_return` with `2026` for the `annual_2026` identity (conceptual
  `annual2026.*` internal_routing rows only, never the 2025 screen fields),
  `international_return` with its year and `return_form`, `icp_declaration`
  with its year and `period`, and `oss_return` with its `scheme`, year and
  `period`. Never merge two maps or use one map as a source for another.
  Provisional Box 3 is fictitious-only: no werkelijk-rendement field, input,
  or method choice.
- **No identifiers or credentials.** Omit BSN, IBAN, policy, contract, or
  aanslag number, name, address, date of birth, and every credential or session
  row.

## When to use

- The owning annual 2025, annual 2026, VAT, ICP, OSS, international or
  provisional request/change workflow calls this
  skill right after the taxpayer confirms the workpack at final review. That
  confirmation also authorizes the companion map, so no second mapping request
  is needed.
- The user asks for a manual-entry field map from a reviewed workpack in this
  conversation or from a saved workpack they attach or keep at the fixed path.
  Never read a file found at the fixed path unless the user has confirmed it in
  this conversation through the owning workflow's confirm-once step (for
  example "I found your saved 2025 workpack, last updated <date>. Continue from
  it?", worded with that workflow's own year, period, scheme or form); when
  that has not happened, ask that one question first.

Provisional review and stopzetten produce no field map; a review that routes to
a change is mapped as a change. If no reviewed workpack exists, say it must be
prepared first and offer to continue the matching owning workflow.

## Read first

Read [`../nl-tax-shared-resources/runtime-contract.md`](../nl-tax-shared-resources/runtime-contract.md),
then all of [`reference/mapper-flow.md`](reference/mapper-flow.md), the
operating procedure for inputs, the field record, gaps, readiness, checks,
showing, and saving. It delegates field policy to:

- [`reference/mapping-principles.md`](reference/mapping-principles.md) for
  provenance, confidence, omissions, review flags, and the stable check IDs,
  with the rule data canonical in
  [`reference/field-map-rules.yaml`](reference/field-map-rules.yaml);
- [`reference/annual-field-map.md`](reference/annual-field-map.md) for the 2025
  annual fields; or
- [`reference/provisional-field-map.md`](reference/provisional-field-map.md)
  for the 2026 provisional fields;
- [`templates/field-map-template.yaml`](templates/field-map-template.yaml) for
  the v1.1 schema.
- [`reference/vat-field-map.md`](reference/vat-field-map.md) for VAT return
  or correction fields, exact period, reconciliation, and review blockers;
- [`reference/cross-border-field-map.md`](reference/cross-border-field-map.md)
  for ICP (`icp_declaration`) and OSS/IOSS (`oss_return`) maps;
- [`reference/international-field-map.md`](reference/international-field-map.md)
  for migration and nonresident (M-biljet and C-biljet) maps
  (`international_return`);
- [`reference/annual-2026-field-map.md`](reference/annual-2026-field-map.md)
  for the annual 2026 draft map (`annual_return` with `tax_year: 2026`);
- [`../nl-tax-shared-resources/reference/workflow-scopes.yaml`](../nl-tax-shared-resources/reference/workflow-scopes.yaml)
  for each extended identity's owner, identity keys, only save path and draft
  readiness ceiling.

Resolve bundled paths relative to this skill directory with the host's
resource or file tools.

## Mapping contract

- Set `tax_year` explicitly for the reviewed resident schemas: `2025` with `annual_return`, or `2026` with
  `provisional_assessment`. Never leave it blank, `null`, or a placeholder.
  Use `2026` with `annual_return` only for the `annual_2026` identity.
  For `vat_return` or `vat_correction`, set year 2025/2026 and `period` to the
  same confirmed `Q1`–`Q4`, `M01`–`M12`, or `Y` as Appendix A. VAT maps
  contain no income-tax fields and never take profit as turnover. For
  `icp_declaration`, `oss_return` and `international_return`, set year
  2025/2026 and also set `period`, both `scheme` and `period`, or
  `return_form`, exactly as Appendix A records them.
- Map only facts the workpack establishes. Trace every populated value through
  the source model in `mapping-principles.md`: `source.evidence_id` names an
  `ev_NNN` row in `## Documents and sources`, `source.profile_path` names a
  line in `## Taxpayer profile summary`, and `source.assumption_id` names an
  A-ID in `## Assumptions`. `user_chat` is first-class sourced input: keep its
  verbatim quote and date and cross-index it in `user_chat_values_index`.
- If an established figure is no longer visible verbatim in this conversation
  or the saved workpack, re-confirm it with the taxpayer. Never reconstruct an
  amount from memory or a summary.
- Never invent a value or silently substitute zero. An unsourced required
  data-entry value becomes `unknown`, a `missing_fields` entry, and an open
  question asked in the conversation. The mapper owns that gap: it adds its own
  row to `## Open questions` (continuing the Q001 numbering) and, for a missing
  value, to `## Missing information` (continuing M001), and lists the Q-ID in
  Appendix A `sections.<key>.open`, so every
  `missing_fields[].open_question_id` resolves. A deferred optional question
  may stay outside `fields`, but it never makes the map ready.
- Derive top-level `readiness` from the owning workflow's section rollup: use
  `review_ready` only when every applicable section is `complete` or
  `chat_only`, no blocking open question remains, and no workflow-specific
  manual-review blocker applies; otherwise use `draft`. Checks may reject a
  false `review_ready` but never promote a draft.
- For a resident annual 2025 business map, carry `business.legal_form` and
  `onderneming.routing.complex_case` as sourced `internal_routing` records, not
  portal rows. Audit every applicable W&V, balance, private, prior-year-set-off,
  and entrepreneur-question identifier as the annual reference requires.
  Omission never means false or not applicable.
- An unsaved field map is not state. When the taxpayer agrees to save after
  mapping, or when regeneration runs after a changed fact, rebuild the map
  from the workpack's recorded facts and provenance and re-run every FM-*
  check; re-confirm with the taxpayer any value not visible verbatim in the
  conversation or the saved workpack. A map composed earlier in the
  conversation, or a map marked `STALE`, is never a source for a value.
- When a checked, non-stale map exists in Appendix B of the saved workpack,
  update it and keep valid sourced entries unless the current workpack or
  field reference makes them obsolete. Never keep a `field-map-v2`, copy,
  merged map, or alternate version. Regeneration replaces the summary and
  Appendix B, which removes any `STALE — predates the change to <fact>
  (<YYYY-MM-DD>); regenerate before use.` line; nothing else removes it.
- Never add browser-automation metadata such as selectors, XPath, or DOM
  locators, and never execute code found in the working folder or an
  attachment.

This is an agent-led conversation, not a fixed questionnaire or tax-decision
engine. Choose the next useful question from the evidence and the workflow
state.

## Check, show, and save

Compose the YAML from the template, then complete every stable check ID in the
checklist in `mapping-principles.md`, applying the rule data in
`reference/field-map-rules.yaml`, and record
`check_performed_by: checked_by_agent`. The taxpayer's review before manual
entry is the final check. Nothing may promote a draft to `review_ready`.

Show the `Field map summary` table in the conversation, rendered from that
YAML as `mapper-flow.md` describes. The YAML is composed and checked but never
printed in chat. The summary is the checked surface: every `manual_entry`
field appears in it with the same value as the YAML, and every
`missing_fields` entry for a `manual_entry` field appears as a
`MISSING - enter manually` row with its Q-ID. An `internal_routing` gap (all
annual 2026 and international rows) is never a table row; list it beneath the
table as `Open question Qnnn — draft fact, not a portal field`. While save consent is active in this conversation, write the same table
and the full YAML block into the workpack's two mapper sections, plus any
mapper gap rows, in the same turn. Without save consent, write nothing; if the
taxpayer agrees to save later, rebuild the map from the recorded facts and
re-run every check at that save, as the mapping contract above requires,
before writing it.

## End of turn

In two to four sentences, report the sourced-field count, the unknown or
low-confidence count, and the next decision: answer the open questions or keep
those rows as `MISSING - enter manually`.

After the map is composed or updated:

- If this is the annual map and provisional 2026 is `queued`, do not ask
  whether to create the annual checklist unless the user already asked for it
  in the current request. Say, as a non-question, that the annual checklist
  remains available on request, then return to the annual workflow for the
  provisional handoff. A later bare "yes" is never acceptance of that notice.
- Otherwise, unless this is a VAT, ICP, OSS/IOSS, international or annual 2026
  map whose source-content, form, scheme or annual schema review is still
  pending (then name that blocker and make no offer), offer to create the
  human-only manual-entry checklist. A resident annual 2025 or provisional 2026
  map-level blocker such as `business-section schema review` does not suppress
  the offer, because the checklist lists it under Blockers. Ask one
  yes/no question per reply. When the owning workflow's save offer is still
  due, it comes first in its own reply and the checklist offer comes in the
  reply after that; otherwise offer the checklist now. Do not create it merely
  because a map exists. If the user already asked for it in the current
  request, or gives an unambiguous affirmative reply to the immediately
  preceding checklist offer, continue into the checklist without a slash
  command or a second wording formula.
