# Agentic and structural evaluation

This directory separates two different kinds of evidence. The live benchmark
evaluates an LLM-driven Cowork conversation. The offline fixture library checks
only hard structural contracts. Passing one does not imply passing the other.

Both follow the 0.4 conversation-first design
(`docs/maintainers/0.4-conversation-first-design.md`): nothing is written by
default, and only with the taxpayer's consent does the plugin keep exactly one
workpack file per workflow identity, holding the readable workpack, the
Appendix A resume record, and the Appendix B field map. The income-tax
workflows use the fixed paths `workspace/nl-tax-annual-2025-workpack.md` and
`workspace/nl-tax-provisional-2026-workpack.md`. The draft-only extended
owners use one year/period-qualified path each, for example
`workspace/nl-tax-vat-2026-Q3-workpack.md`,
`workspace/nl-tax-vat-correction-2026-Q1-workpack.md` (one file per original
period), `workspace/nl-tax-icp-2026-Q3-workpack.md`,
`workspace/nl-tax-oss-union-2026-Q3-workpack.md`,
`workspace/nl-tax-international-2025-migration-workpack.md` and
`workspace/nl-tax-annual-2026-workpack.md`. There are no profile, session,
evidence-index, notes, or separate field-map, delta, review-question, or
checklist files.

## Agentic evaluation — primary behavior signal

`plugin-eval-benchmark.json` contains five natural user conversations:

1. an informational healthcare-cost question;
2. explicit annual-return preparation;
3. a provisional-assessment salary change;
4. annual entrepreneur/Winst preparation with an overreaching request; and
5. a part-year-resident case routed into a separate migration draft.

The prompts contain no fixture names, case IDs, marker files, expected file
lists, or prescribed question sequences. Each run starts from the minimal
`agentic-workspace/`; Plugin Eval installs the plugin into that isolated copy.

Apply `agentic-rubric.json` to the transcript, loaded resources, and any output
artifacts. It scores workflow reasoning, tax/source correctness, question
quality, uncertainty, usefulness, progressive context use, and agent ownership
of reasoning. Different wording and organization are valid. Hard failures cover
invented facts, cross-year/workflow mixing, false submission/final-calculation
claims, unsupported overreach, and delegating interpretation to a validator.

The only automated live-run verifier is
`agentic-workspace/.eval/verify-hard-contracts.sh`. It checks the 0.4 file
boundaries: nothing under `workspace/` except the two fixed income-tax
workpack files and the identity-scoped VAT, VAT-correction, ICP, OSS,
international and annual 2026 workpack paths, each only with a recorded
`save_consent: given` and a matching `workflow:` line; no
second `workspace/` tree or workpack copy, a recorded `save_consent: given`
(the record of consent given in the conversation, never itself an
authorization) and the file's own workflow in any workpack that exists, no cross-workflow file
reference, and no werkelijk-rendement collection in a provisional workpack. A
single-request run normally ends with no file at all, because saving needs the
user's consent. It deliberately does not score semantic quality.

Plugin Eval currently sends one natural user request per isolated Codex run. It
can assess the agent's first response, tool/resource choices, questions, and
artifacts, but it does not supply simulated taxpayer replies. Use the native
Claude cases or a human Cowork smoke for genuinely multi-turn follow-up quality,
including save consent and resume.

Run the focused benchmark only when live model evidence is needed:

```bash
plugin-eval benchmark plugins/nl-tax-agent-skills \
  --config evals/nl-tax-agent-skills/plugin-eval-benchmark.json \
  --format markdown
```

Do not expand this into one live run per fixture. Add a sixth scenario only when
it represents a materially different user journey that cannot be assessed by
the existing five profiles.

## Native Claude prose evaluation

The first-party Claude cases live inside the plugin package, at
`plugins/nl-tax-agent-skills/evals/cowork-*/`, because `claude plugin eval`
discovers cases only in the `evals/` directory of the plugin under test and
loads that plugin for them. A case kept outside the plugin runs against
baseline Claude Code with no plugin loaded. Each case has a natural prompt
(`prompt.md`) and an LLM grader (`graders/criteria.md`), including
`cowork-save-and-resume` (continue from a saved workpack's resume record
without re-asking answered questions), `cowork-stale-checklist-after-correction`
(a corrected figure makes the field map stale, so a checklist request shows
only the stale blocker and asks once to regenerate, never the old value), and
no-write assertions on opening turns.

Every `prompt.md` lists only the read-only tools
`allowed_tools: [Read, Glob, Grep, Skill]`, so the agent can load the plugin's
skills and read its knowledge notes. Files inside the plugin never grant
`Write`, `Edit` or `Bash`. The one case that must save files,
`cowork-vat-correction-periods`, gets its write tools from the operator grant
`--allow-tools Edit Write` on the command line. That grant applies to every
case in the run, so each no-save case carries `no-write.md` and `no-edit.md`,
`tool_used` graders with `min: 0` and `max: 0` on `Write` and on `Edit`, that
fail if the agent writes or edits a file before the user consents to saving.
Only `cowork-vat-correction-periods` (save consent in the prompt) and
`cowork-stale-checklist-after-correction` (the user says saving is already
active in this conversation) omit them. Without the grant, the correction
case's `file_exists` graders fail and the CLI warns that they cannot pass.

When native evaluation is available, run a quick check from the repository root:

```bash
claude plugin eval plugins/nl-tax-agent-skills \
  --trust-plugin \
  --case 'cowork-*' \
  --allow-tools Edit Write \
  --runs 1 \
  --threshold 1.0 \
  --no-publish \
  --output-dir evals/results/latest
```

All scored graders are required: a failed tax-rule or safety rubric must not
be offset by passing file-existence checks. Keep the threshold at `1.0`.
The single run above is a quick check; before release, use `--runs 3` with
the same threshold to check consistency across repeated agent responses.

To confirm discovery without spending anything, add `--max-cost-usd 0
--ablation none`: the output names `Plugin under test: "nl-tax-agent-skills"`
and stops before the first paid run. Never commit run results; keep them out
of `plugins/nl-tax-agent-skills/evals/results/` so they are not packaged.

Graders follow the plugin-eval guidance of one grader on the result and one
on the steps. `criteria.md` is the `llm` result grader on the final message.
The extended cases also have a `skill-fired.md` `tool_used: Skill` step
grader that passes when the owning skill (or the `nl-tax-intake` router that
hands off to it) was loaded; in a two-arm run it is a plugin-fired indicator
rather than part of the score. Because that indicator also passes when only
the router fires, each extended case adds an `owner-read.md` `tool_used: Read`
indicator (`arm: with-only`) whose `input_match` names the owning skill's
directory, for example `nl-tax-vat-return/`. It passes when the run read the
owner's SKILL.md through the intake handoff or the owner's own reference flow
after a direct Skill invocation. Owner routing stays invisible in the reply,
so the `criteria.md` rubrics judge only its visible effect, such as a separate
migration-year (M) draft, never internal workflow identifiers.
`cowork-vat-adjustments-first-use-2026` adds a
`helper-fired.md` indicator that the read-only `nl-tax-vat-adjustments`
helper was read. `cowork-vat-correction-periods` adds `file_exists` graders:
one saved correction workpack each for Q1 and Q2, and no Q3 or combined file.
The LLM criteria judge only what a correct first reply can show; they do not
require mapper internals, Appendix YAML or discussion of facts the prompt does
not contain.

This still does not prove the Cowork desktop UI, marketplace update flow,
local/remote file selection, or available tools in a fresh task. Record a
separate human smoke after installation.

The VAT cases (`cowork-vat-return-draft`, `cowork-vat-correction-periods`)
cover a draft period return and per-period corrections without a checklist.
The correction case prepares Q1 and Q2 as separate workpacks; a complete-year
suppletie may only be mentioned as an official option for a human or adviser
and is never prepared or batched. The extended cases cover ICP goods frequency
and actual customer-ID gaps (`cowork-icp-period-and-vat-id-review`), OSS
corrections and separate country refunds
(`cowork-oss-country-corrections-no-offset`), 2026 investment-service first
use (`cowork-vat-adjustments-first-use-2026`), M/C form and year isolation
(`cowork-international-m-c-year-isolation`), a part-year resident routed to a
migration draft (`cowork-migration-draft-boundary`), and actual annual-2026
precollection (`cowork-annual-2026-actual-precollection`). Their offline
fixtures require chat-only output and preserve file boundaries; tax-content
behavior is assessed from the natural prompt and the LLM or human grader.
These are draft-only previews: shipping the cases does not record a native
host evaluation run, and passing them does not make any extended workflow
filing-ready.

## Offline structural contracts — secondary regression signal

`offline-dataset.yaml` maps every shipped fixture to the files a finished test
workspace may hold and to a few structured expectations. It is a contract
library, not a prompt library: it contains no model instructions, no Markdown
prose assertions, and requires no case-marker file. For each case the verifier
checks that:

- the workspace holds exactly the expected workpacks (plus harness captures
  under `workspace/eval/`), with no 0.3 ledger path (`workspace/taxpayer/**`,
  `workspace/shared/**`, `workspace/annual/**`, `workspace/provisional/**`), no
  other file under `workspace/`, and no copy, variant, or second `workspace/`
  tree;
- seeded files — an attached saved workpack or a 0.3 ledger placed before the
  conversation (`seed_files` in the fixture, sources under `fixtures/seeds/`) —
  are byte-identical afterwards;
- every expected workpack passes the workpack grader
  (`tools/nl_tax_agent_skills/workpack/validate_workpack.py`): required
  sections in template order, the Appendix A resume record, the STATUS banner,
  `Documents and sources` rows for every `ev_NNN` reference, no BSN, IBAN, or
  file hash, and workflow separation — plus the case's resume-record
  expectations (`readiness`, `queued_workflow`, section statuses,
  `updated_at` later than `created_at` for a file kept current);
- a harness capture of the workpack as shown in the conversation
  (`presentation: chat`) passes the grader's chat mode instead: only filled
  sections in template order, no template fill notes, and never Appendix A,
  Appendix B, or any YAML block (the field map appears as its summary table).
  The capture is the workpack's final state in the conversation: for annual,
  provisional request, and provisional change it always holds
  `## Field map summary`, with the summary table once mapping has run;
- once a workpack is mapped, `## Field map summary` is the checked surface
  (review amendment A12): every manual-entry field in Appendix B appears with
  the same value after amount normalization, every missing manual-entry field
  appears as a `MISSING - enter manually` row with its Q-ID (an
  `internal_routing` gap, as in every annual 2026 and international map, is
  listed beneath the table by its Q-ID instead), no row names a field Appendix
  B lacks, and a requested, non-stale checklist shows the same values. A
  `STALE — predates the change to <fact> (<YYYY-MM-DD>); regenerate before
  use.` line is valid only while Appendix A `generation_confirmed` is `false`,
  and a mapped workpack with `generation_confirmed: false` must carry it
  (review amendment A10). `annual_stale_checklist_after_correction` covers the
  full sequence: decline save, generate, save later, correct a figure, request
  the checklist, resume, regenerate;
- Appendix B passes the field-map grader
  (`tools/nl_tax_agent_skills/field_mapper/validate_field_map.py`) when the
  case expects a field map, or reads `not yet mapped` when it must not (review
  and stopzetten never map);
- each workpack's `## Sources used` equals its Appendix A `sources_loaded`, and
  no ledger holds the other workflow's sources;
- text checks touch only the YAML appendices, and no generated file contains a
  password or wachtwoord value.

Use it to catch hard regressions in supported years, consent-gated saving,
annual/provisional separation, resume, source-bound fields, and unsupported
boundaries. It must not be used to demand exact prose, a fixed interview, or a
complete answer template from an agent.

List or validate the fixture library:

```bash
python3 evals/nl-tax-agent-skills/verify_offline_workspace.py --list
python3 evals/nl-tax-agent-skills/verify_offline_workspace.py --check-dataset
```

To verify an already prepared test workspace, select the structural contract
explicitly:

```bash
python3 evals/nl-tax-agent-skills/verify_offline_workspace.py \
  --workspace /path/to/test-workspace \
  --case annual_simple_resident
```

To grade one saved workpack directly:

```bash
python3 tools/nl_tax_agent_skills/workpack/validate_workpack.py --expect-saved \
  /path/to/workspace/nl-tax-annual-2025-workpack.md
```

There is intentionally no automatic case selection from generated output.

## Evaluation-design metric pack

The local metric pack validates the design rather than grading conversations:

```bash
plugin-eval analyze plugins/nl-tax-agent-skills \
  --metric-pack evals/nl-tax-agent-skills/agentic-metric-pack/manifest.json \
  --format markdown
```

It checks that the benchmark stays at five natural prompts, covers the agreed
profiles, uses a weighted rubric, and runs in a minimal workspace with only one
hard-contract verifier. Extension results do not overwrite Plugin Eval's core
static score.

## Static-analysis interpretation

The plugin intentionally ships an offline, source-cited knowledge pack. Core
Plugin Eval aggregates that supporting tree and multiple implicit skill bodies,
so its static deferred/invoke budget does not represent Claude Cowork's actual
always-on context. Compare it with `claude --plugin-dir ... plugin details`, and
state clearly whether any token figure is static, cumulative benchmark usage,
or Claude package inventory.

Taxpayer workflows need no Python: the installed plugin ships no scripts. The
supported maintainer runtime is Python 3.10+. The workpack grader, the
field-map grader, and the source-pinned arithmetic graders are repository tools
under `tools/nl_tax_agent_skills/`, next to seven developer
consistency/source-maintenance tools. Agentic evaluation must never assume a
grader owns tax interpretation.
