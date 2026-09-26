# Agentic and structural evaluation

This directory separates two different kinds of evidence. The live benchmark
evaluates an LLM-driven Cowork conversation. The offline fixture library checks
only hard structural contracts. Passing one does not imply passing the other.

Both follow the 0.4 conversation-first design
(`docs/maintainers/0.4-conversation-first-design.md`): nothing is written by
default, and only with the taxpayer's consent does the plugin keep exactly one
workpack file per workflow — `workspace/nl-tax-annual-2025-workpack.md` or
`workspace/nl-tax-provisional-2026-workpack.md` — holding the readable
workpack, the Appendix A resume record, and the Appendix B field map. There are
no profile, session, evidence-index, notes, or separate field-map, delta,
review-question, or checklist files.

## Agentic evaluation — primary behavior signal

`plugin-eval-benchmark.json` contains five natural user conversations:

1. an informational healthcare-cost question;
2. explicit annual-return preparation;
3. a provisional-assessment salary change;
4. annual entrepreneur/Winst preparation with an overreaching request; and
5. an unsupported part-year-resident case.

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
boundaries: nothing under `workspace/` except the two fixed workpack files, no
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

`../claude/cowork-*/` contains twelve first-party Claude cases using natural
prompts and LLM graders, including `cowork-save-and-resume` (continue from a
saved workpack's resume record without re-asking answered questions),
`cowork-stale-checklist-after-correction` (a corrected figure makes the field
map stale, so a checklist request shows only the stale blocker and asks once
to regenerate, never the old value), and no-write assertions on opening
turns. When native evaluation is available:

```bash
claude plugin eval plugins/nl-tax-agent-skills \
  --case 'cowork-*' \
  --runs 1 \
  --threshold 0.8 \
  --output-dir evals/results/latest
```

This still does not prove the Cowork desktop UI, marketplace update flow,
local/remote file selection, or available tools in a fresh task. Record a
separate human smoke after installation.

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
  the same value after amount normalization, every missing field appears as a
  `MISSING - enter manually` row with its Q-ID, no row names a field Appendix
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
