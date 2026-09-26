## Phase 10 — Workpack assembly

### 10.1 Generation gate

Do not generate the workpack until every applicable annual section is
`complete`, `chat_only`, or `deferred`, every deferred item is recorded in
`Open questions` and `Missing information`, and no blocking deferred item
remains. A nonblocking deferred item may produce only the draft status allowed
by the output contract.

At final review, summarize the readiness status and what will be produced (the
workpack and its field map), then ask a scoped question such as: "Shall I
create the workpack and field map now?" Keep it the only question in that
reply, so a bare "yes" cannot be read as consent to anything else. Ask one
yes/no question per reply: never add the save offer or the checklist offer to
this reply. A save offer that is still due comes after generation and mapping
(10.6).

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
question. On confirmation, mark the `confirm` section `complete` and set
`generation_confirmed: true`.

If a sourced fact changes after generation, reset `confirm` to `not_started`
and `generation_confirmed` to `false`, recompute affected review values,
present the updated summary, and require fresh contextual confirmation before
regenerating the workpack or its field map. The `Field map summary`, Appendix
B, and any `Manual-entry checklist` are now stale. In the same reply, show the
visible line `STALE — predates the change to <fact> (<YYYY-MM-DD>); regenerate
before use.` for each of them that exists. When the workpack is saved, record
the changed fact in its section right away with a DRAFT banner, and put the
same line at the top of `Field map summary`, of Appendix B (above its `yaml`
block), and of a requested `Manual-entry checklist`. Adding that line is the
only edit this skill makes in the mapper's and the companion's sections; never
change their values. A stale map or checklist is a blocker: the submit
companion never copies a value from it. Only regeneration clears the marker:
after the fresh confirmation, regenerate the workpack and re-run
`nl-tax-field-mapper` (10.4), which rebuilds the map from the recorded facts
and replaces the stale summary and Appendix B. A stale checklist keeps its
marker until the taxpayer asks for the checklist again and the submit
companion rebuilds it from the regenerated map.

### 10.2 Use the template and output contract

Only after the gate opens, read `reference/annual-output-contract.md`, and
`templates/annual-workpack.md` unless it is already loaded for a saved
workpack. Fill every required section with the facts established in phases
1–9 and preserve the template's `Src` provenance. Reconcile the STATUS banner
and Appendix A with the annual section rollup exactly as the output contract
requires. `Field map summary` and Appendix B read `not yet mapped` until the
mapper runs; leave `Manual-entry checklist` to the submit companion.

### 10.3 Run the workpack self-check

Run every check in `reference/annual-output-contract.md` § "Workpack self-check": structural, content, cross-contamination, and safety. Keep the checklist invisible to the taxpayer; mention only a failed item that needs their input. If any item is "no", do not present or write the workpack — fix the gap or ask the user, then re-run.

### 10.4 Present, save, and map

Before mapping, recompute the annual rollup and Appendix A `readiness`. The
rollup is complete only when every applicable section is `complete` or
`chat_only`; otherwise the workpack stays a draft.

Present the generated workpack in the conversation as Markdown, or on a host
surface that creates no file. Presentation never writes: creating a
downloadable file counts as saving. In chat, render only filled sections: no
template fill notes, no bracketed instructions, and no Appendix A or Appendix B
YAML; cite each document by name with its ev ID, for example
`F:ev_003 (jaaropgaaf ING 2025)`.

Only while save consent is active in this conversation, also write it to
`workspace/nl-tax-annual-2025-workpack.md`, updating that file in place. Never
create a copy or a variant. When consent is active but the host has no
writable working folder, or the working folder may not outlast the session,
deliver the workpack as a downloadable file or document after mapping (below),
so the download includes the field map; without consent, create no file.

Then invoke `nl-tax-field-mapper`; it alone composes and checks the annual
field map using
`nl-tax-field-mapper/templates/field-map-template.yaml`,
`nl-tax-field-mapper/reference/mapping-principles.md`,
`nl-tax-field-mapper/reference/annual-field-map.md`, and
`nl-tax-field-mapper/reference/field-map-rules.yaml`. It shows the `Field map
summary` table in the conversation and, only when the workpack is saved, writes
that summary and the Appendix B `yaml` block into the file. Its YAML is
composed and checked but never printed in chat. The confirmed workpack
authorizes this companion map without a second activation or consent phrase.
In the conversation, the workpack's `Field map summary` section holds that
table once mapping has run.

An unsaved field map is not state. If the taxpayer agrees to save only after
mapping, the first save writes the whole workpack from the facts and
provenance recorded in this conversation, and the mapper rebuilds the map for
that save from those recorded facts, re-runs every FM-* check, and re-confirms
with the taxpayer any value no longer visible verbatim in the conversation
before it writes the `Field map summary` and Appendix B. A manual-entry
checklist already shown is carried over only when each of its values matches
the rebuilt map; otherwise it is written with the stale line from 10.1.
Regeneration after a changed fact rebuilds the map the same way.

Derive map readiness from the same rollup as Appendix A; the mapper's checklist
may reject a false declaration but never promotes a draft. Treat
structural/provenance errors and readiness mismatch as blocking.

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

### 10.5 Dual-workflow handoff

When the user asked for both workflows, `queued_workflow` records the queued
2026 subflow. Hand off only after the annual rollup is complete, the workpack
is generated, and the field map was composed and checked successfully. A map
that is `draft` solely because a declared workflow-specific manual-review
blocker applies still counts as successful after a complete rollup.

- If the rollup is not complete, or the field map fails its checks, do not
  partially hand off: annual stays the active workflow and 2026 stays queued.
  Tell the user which annual items remain open. A deferred annual question
  remains open and is never also answered.
- On a successful handoff, leave the annual workpack unchanged apart from
  clearing `queued_workflow`, and continue into 2026 collection under
  `nl-tax-provisional-assessment` without asking for a new activation phrase.
  Do not load 2026 resources before this point. The original request for both
  workflows authorizes starting collection; it does not satisfy the 2026
  final-generation confirmation.
- When 2026 collection starts, `queued_workflow` is cleared: if the annual
  workpack is saved, set it to `null` in Appendix A as the last annual write.
  An unsaved annual workpack records the handoff in the conversation only.
- Never copy an annual amount into 2026 facts. An annual actual may inform a
  2026 estimate only after the taxpayer reviews or states that estimate.
- If the taxpayer has not opted in to saving and has not said not to ask
  again (an earlier "no" does not suppress this point), the handoff reply's
  only question is the save offer, covering both files: "Want me to keep this
  2025 workpack as a file in your working folder so you can pick up later, and
  the 2026 one too once we start it? Otherwise everything stays in this
  conversation." This is the annual generation-point offer and also counts as
  the 2026 workflow-start offer, so the 2026 workflow does not repeat it; the
  first 2026 question comes in the next reply. A consent given earlier for the
  annual file extends to the 2026 file only if the user said so; otherwise the
  2026 workflow asks once, as its workflow-start offer.
- Do not ask an annual-checklist question at the handoff. State only that the
  annual checklist remains available on request, then make the next actual
  question a 2026-subflow question (after the save offer, when one is due). A
  bare "yes" can answer only the immediately preceding question; never
  reinterpret it as annual-checklist authorization.

### 10.6 Summary to user

After generating:
- Say where the workpack is: in this conversation, saved at
  `workspace/nl-tax-annual-2025-workpack.md`, or delivered as a download
- Report the count of missing information items and open questions
- Report the count of assumptions
- Remind the user to review the human review checklist
- Remind the user that you (the taxpayer) or an authorized human file through
  Mijn Belastingdienst
- Ask one yes/no question per reply. When no 2026 workflow is queued and the
  save offer is still due (not opted in, no "don't ask again"), the reply after
  generation and mapping asks only the save offer. The human-only manual-entry
  checklist offer comes in the reply after that, or in this reply when no save
  offer is due, and only after the field mapper reports success. An
  unambiguous acceptance of the checklist offer counts as an explicit
  natural-language checklist request.
- When consent is active but the working folder may not outlast the session,
  or the host has no writable working folder, deliver the download now, after
  mapping, and tell the taxpayer to keep it to resume.
- When a 2026 workflow is queued, follow 10.5 instead of asking the checklist
  question.
