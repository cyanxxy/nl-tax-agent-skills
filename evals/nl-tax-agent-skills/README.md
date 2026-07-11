# Offline Evaluation

This directory contains the repo-local evaluation setup for `nl-tax-agent-skills`.
It is intentionally offline: benchmark prompts point at local YAML fixtures and
must not browse, refresh sources, log in, file, or collect portal credentials.
It lives outside the plugin package so development-only benchmark files are not
shipped to users or counted as plugin support context.

## Files

- `offline-dataset.yaml` defines the offline cases, fixture paths, benchmark
  prompts, expected files, and policy text checks.
- `verify_offline_workspace.py` verifies generated `workspace/**` outputs for
  the case written to `workspace/eval/current-case.txt`.
- `plugin-eval-benchmark.json` is the Plugin Eval benchmark config that
  runs real Codex CLI scenarios against the offline cases.

## Local Checks

List the cases:

```bash
python3 evals/nl-tax-agent-skills/verify_offline_workspace.py --list
```

Validate that every dataset fixture path still exists:

```bash
python3 evals/nl-tax-agent-skills/verify_offline_workspace.py --check-dataset
```

The `--all` command verifies generated outputs for every case, so it is mainly
useful inside a prepared workspace containing all expected `workspace/**`
artifacts. For normal Plugin Eval runs, the verifier reads
`workspace/eval/current-case.txt` and checks the single active case.

Run the Plugin Eval benchmark:

```bash
plugin-eval benchmark plugins/nl-tax-agent-skills \
  --config evals/nl-tax-agent-skills/plugin-eval-benchmark.json \
  --format markdown
```

Run the static Plugin Eval report:

```bash
plugin-eval analyze plugins/nl-tax-agent-skills \
  --format markdown
```

If `plugin-eval` is not on `PATH`, locate the bundled script dynamically instead of pinning a cache hash:

```bash
PLUGIN_EVAL_JS="$(
  find "${CODEX_HOME:-$HOME/.codex}/plugins/cache" \
    -path '*/plugin-eval/*/scripts/plugin-eval.js' \
    -type f \
    -print | head -n 1
)"
test -n "$PLUGIN_EVAL_JS"

node "$PLUGIN_EVAL_JS" benchmark plugins/nl-tax-agent-skills \
  --config evals/nl-tax-agent-skills/plugin-eval-benchmark.json \
  --format markdown

node "$PLUGIN_EVAL_JS" analyze plugins/nl-tax-agent-skills \
  --format markdown
```

## Static Eval Notes

The plugin intentionally keeps an offline source pack in the shipped bundle so
taxpayer-facing skills do not depend on live web lookup. Plugin Eval will still
flag deferred token cost for that source pack. Treat that as a release tradeoff,
not a reason to remove source-backed knowledge.

Plugin Eval's Python complexity check is a coarse file-level heuristic over the
helper scripts. Keep normal tests and validators as the functional gate.

Python is optional in taxpayer workflows. The supported maintainer runtime is
Python 3.10+, and the 14 helpers are grouped into four conceptual components:
evidence inventory/hash, field-map checks, source-pinned arithmetic checks, and
developer consistency/source maintenance. Evals should assess the LLM's
interpretation and artifact behavior, not assume a helper is available.
