# Agentic and structural evaluation

This directory separates two different kinds of evidence. The live benchmark
evaluates an LLM-driven Cowork conversation. The offline fixture library checks
only hard structural contracts. Passing one does not imply passing the other.

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
`agentic-workspace/.eval/verify-hard-contracts.sh`. It checks canonical artifact
boundaries such as annual/provisional separation and mapper-owned field-map
paths. It deliberately does not score semantic quality.

Plugin Eval currently sends one natural user request per isolated Codex run. It
can assess the agent's first response, tool/resource choices, questions, and
artifacts, but it does not supply simulated taxpayer replies. Use the native
Claude cases or a human Cowork smoke for genuinely multi-turn follow-up quality.

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

`../claude/cowork-*/` contains five first-party Claude cases using natural
prompts and LLM graders. When native evaluation is available:

```bash
claude plugin eval plugins/nl-tax-agent-skills \
  --case 'cowork-*' \
  --runs 1 \
  --threshold 0.8 \
  --output-dir evals/results/0.1.7
```

This still does not prove the Cowork desktop UI, marketplace update flow,
local/remote file selection, or available tools in a fresh task. Record a
separate human smoke after installation.

## Offline structural contracts — secondary regression signal

`offline-dataset.yaml` maps all shipped fixtures to expected/forbidden paths and
a small set of structured YAML identifiers. It contains no Markdown prose
assertions. It is a contract library, not a prompt library: it contains no model
instructions and requires no case-marker file.

Use it to catch hard regressions in supported years, artifact ownership,
annual/provisional separation, source-bound fields, and unsupported boundaries.
It must not be used to demand exact prose, a fixed interview, or a complete
answer template from an agent.

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

Python is optional in taxpayer workflows. The supported maintainer runtime is
Python 3.10+, and the 14 helpers remain mechanical accelerators for inventory,
field-map checks, source-pinned arithmetic, and developer consistency. Agentic
evaluation must never assume a helper owns tax interpretation.

The earlier 21-run exact-output benchmark is documented in
`plugin-eval-benchmark-0.1.7.md` as historical evidence and is superseded by the
five-conversation design.
