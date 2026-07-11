# Superseded exact-output benchmark — 0.1.7

## Status

This result is historical evidence, not the current evaluation design. On
2026-07-11 the previous benchmark attempted 21 fixture-reproduction scenarios
using Codex CLI `0.143.0` and `gpt-5.4` in full repository copies.

- 17 scenarios executed; all 17 passed the offline workspace verifier and the
  Python compile verifier.
- Four scenarios were rejected before model execution when the Codex account
  reached its usage limit. They were infrastructure-blocked, not observed
  plugin failures.
- The deterministic fixture library covered all 21 cases and passed its dataset
  consistency check.
- Seventeen valid samples averaged 584,311.94 cumulative input tokens and
  594,945.59 total tokens. These figures included cached multi-turn context and
  the copied repository/evaluation harness.

## Why it was superseded

The prompts named fixtures and case IDs, required an exact marker file, and
prescribed output artifacts. That measured template reproduction more strongly
than Cowork reasoning and caused the harness to copy far more context than a
normal plugin invocation.

The replacement `plugin-eval-benchmark.json` uses five natural conversations,
a minimal seed workspace, one hard-contract shell verifier, and the shared
`agentic-rubric.json`. Do not compare the historical cumulative token averages
directly with Claude package inventory or future minimal-workspace runs.

The full raw transient run directory was deliberately removed after this
summary was recorded.
