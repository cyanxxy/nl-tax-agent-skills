## Phase 10 — Workpack assembly

### 10.1 Generation gate

Do not write `workspace/annual/2025/return-pack.md` until all annual
subsections have status `complete`, `chat_only`, or `deferred`, every deferred
item is recorded, and no blocking deferred item remains. A nonblocking deferred
item may produce only the draft status allowed by the output contract.

At final review, summarize the readiness status and the two artifacts that will
be written, then ask a scoped question such as: "Shall I create the workpack and
field map now?"

Accept natural-language confirmation when either:

- the user directly asks to create, generate, or write the final workpack after
  reviewing the summary; or
- the user gives an unambiguous affirmative reply to that immediately preceding
  scoped question, including wording such as "yes", "go ahead", "looks good",
  or a natural Dutch equivalent.

The optional command `/nl-tax-agent-skills:nl-tax-annual-return confirm` is also
valid. Never require an exact phrase. Do not treat the opening request to prepare
a return, or an unrelated affirmative answer earlier in the conversation, as
final generation consent. If the answer is ambiguous, ask one short confirmation
question. Record the confirmed question in the `confirm` subsection.

If a sourced fact changes after generation, reset the `confirm` subsection to
`not_started`, recompute affected review values, present the updated summary,
and require fresh contextual confirmation before overwriting the canonical
workpack or field map.

### 10.2 Use the template and output contract

Only after the gate opens, read `templates/annual-return-pack.md` and
`reference/annual-output-contract.md`. Fill every required section with the
notes compiled in phases 1.5-9 and preserve the template's `Src` provenance.
Reconcile its STATUS banner with the active annual rollup exactly as required by
the output contract.

### 10.3 Run the workpack self-check

Run every check in `reference/annual-output-contract.md` § "Workpack self-check": structural, content, cross-contamination, and safety. Report each result yes/no in the assembly turn. If any item is "no", do not write the workpack — fix the gap or ask the user, then re-run.

### 10.4 Write, roll up, and map

Before mapping, recompute and persist the annual rollup. Set it `complete` only
when every applicable subsection is `complete` or `chat_only`; otherwise keep it
`in_progress`. Retain `active_skill: nl-tax-annual-return` through validation.

Write the completed workpack to `workspace/annual/2025/return-pack.md`. Then
invoke `nl-tax-field-mapper`; it alone writes and validates
`workspace/annual/2025/field-map.yaml` using
`nl-tax-field-mapper/templates/field-map-template.yaml`,
`nl-tax-field-mapper/reference/mapping-principles.md`,
`nl-tax-field-mapper/reference/annual-field-map.md`, and
`nl-tax-field-mapper/reference/field-map-rules.yaml`. Derive map readiness from
the same saved rollup; the mapper's checklist may reject a false declaration but
never promotes a draft. Treat structural/provenance errors and readiness mismatch
as blocking.

An entrepreneur map rolls up like any other. When the annual rollup is complete
and the reviewed zakelijke schema covers every business rubriek and question the
case needs, a map carrying `onderneming.*` rows reaches `readiness:
review_ready` in the ordinary way. Add the blocker `business-section schema
review` and keep the map `draft` only when a needed rubriek, question or
identifier falls outside the reviewed schema, or when a Phase 2A routing marker
applies (samenwerkingsverband profit share, medegerechtigde loss caps, DGA/BV
winst, agrarisch, zeevarenden, stakingswinst, herinvesteringsreserve,
oudedagsreserve wind-down, terbeschikkingstelling). A business case is no longer
a standing reason to withhold `review_ready`.

For a business map, require the mapper's per-identifier coverage notes before
accepting that rollup: every W&V, balance, private, prior-year-set-off and question
identifier must be mapped, sourced not applicable, or unresolved. Any unresolved
or omitted classification forces `draft`; the optional validator is only a
structural backstop and cannot waive this gate.

After successful mapping of a complete rollup, inspect the saved provisional
request before the final profile/session write. Then apply exactly one of these
ownership outcomes:

- If `workflows.provisional_2026.requested` is true and its status is `queued`,
  require its saved `subflow` and atomically set
  `workflows.annual_2025.status: complete`,
  `workflows.provisional_2026.status: in_progress`, derive
  `provisional_2026_<subflow>`, set that candidate as both the profile's
  `workflow_candidate` and session `active_workflow`, and set
  `active_skill: nl-tax-provisional-assessment`; update the profile and session
  `updated_at` values in the same write. Preserve
  `sections.annual_2025` and every annual artifact unchanged; leave
  `sections.provisional_2026.status` and its subsections `not_started` except
  for the subflow recorded by intake. Preserve
  `sources_loaded_by_workflow.annual_2025`, keep the provisional source list
  independent, and set the top-level `sources_loaded` mirror to
  `sources_loaded_by_workflow.provisional_2026`. Do not load provisional
  resources until this state update succeeds.
- Otherwise set `workflows.annual_2025.status: complete` and clear
  `active_skill` after successful mapping.

If the annual rollup is not complete, the field map fails validation, or the
provisional subflow is absent, do not partially hand off: keep
`active_workflow: annual_2025`, `active_skill: nl-tax-annual-return`, annual
profile status `in_progress`, and provisional profile status `queued`. A
deferred annual question remains open and is never also answered.

After a successful queued handoff, continue the 2026 collection naturally
under the provisional owner without asking for a new activation phrase. The
original request for both workflows does not satisfy the provisional
final-generation confirmation gate. Do not ask an annual-checklist question at
the handoff. State only that the annual checklist remains available on request,
then make the first actual question a provisional-subflow question. A bare
“yes” can answer only that immediately preceding provisional question; never
reinterpret it as annual-checklist authorization.

### 10.5 Summary to user

After writing:
- Confirm the workpack location
- Report the count of missing information items
- Report the count of assumptions made
- Remind the user to review the human review checklist
- Remind the user that filing happens through Mijn Belastingdienst
- When no provisional workflow is queued, offer to create the human-only
  manual-entry checklist after the field mapper reports success. An
  unambiguous affirmative reply to that immediate offer counts as an explicit
  natural-language checklist request.
- When a provisional workflow is queued, do not ask the checklist question.
  Mention in a non-question sentence that the annual checklist remains
  available on request, then immediately continue with a clearly scoped
  provisional-subflow question. Only a direct checklist request activates the
  annual checklist after that handoff.
