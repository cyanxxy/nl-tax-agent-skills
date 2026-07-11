# Claude and Cowork evaluation status — 0.1.7

## Native Claude evaluation

Claude Code `2.1.204` was checked on 2026-07-11. This command was attempted:

```text
claude plugin eval plugins/nl-tax-agent-skills --case 'cowork-*' --runs 3 --threshold 0.8 --output-dir evals/results/0.1.7
```

The installation reported that `plugin eval` is currently in early access. It
produced no case scores, aggregate JSON, or model-graded transcript. This is an
unavailable gate, not a pass.

The native prose suite now contains exactly five natural Cowork conversations:
informational guidance, annual preparation, a provisional change, annual Winst
scope, and an unsupported residency boundary. Their LLM graders allow valid
variation and do not require fixture names, case markers, exact phrases, fixed
question order, or predetermined files.

## Available validation

- Strict plugin and marketplace validation pass.
- Claude inventory reports 12 skills and approximately 637 always-on tokens;
  invoked-skill estimates are approximately 950–5,100 tokens.
- Both repository-root and standalone package test suites pass.
- The 21-case offline contract-library consistency check passes.
- The previous exact-output benchmark is retained only as a superseded summary
  in `plugin-eval-benchmark-0.1.7.md`.

## Deliberately pending

The redesigned five-conversation live benchmark has not been run in this
redesign step. The earlier run exhausted the available Codex usage allowance,
and immediately spending another series of model calls would repeat the mistake
that motivated the redesign. Run it only when measured agentic evidence is
needed, then grade transcripts with `agentic-rubric.json`.

A fresh-task Claude Cowork desktop UI smoke remains a separate human release
gate after installation. Static validation, CLI inventory, and offline contract
checks do not prove the UI experience.
