---
name: nl-tax-box3
description: Use when Box 3 method notes are needed.
user-invocable: false
allowed-tools:
  - Read
  - Grep
  - Bash(python3 *.py:*)
---

# NL Tax Box 3

Background helper for box 3 notes.

Annual 2025 must cover fictitious return and werkelijk-rendement data collection for user review. Provisional 2026 must use only the provisional fictitious method and must never ask for werkelijk rendement.

This helper participates in a conversational workflow. It does not assume all asset and debt inputs are pre-staged. When values are missing, return a structured open-question packet for the calling skill instead of inventing zeros.

## Hard rules

- Annual 2025: collect and compare fictitious return and werkelijk rendement when the user wants the actual-return comparison.
- Provisional 2026: use only the fictitious method.
- Never request werkelijk-rendement inputs in a provisional workflow.
- Compute only from values with a real source or an explicitly confirmed assumption.

## Behavior

Resolve every `workspace/...` path against `workspace_root` from
`session-progress.yaml` (or `profile.yaml`); never create a second
`workspace/` tree.

For each needed input, check section notes and evidence first. If the value is unavailable, append a question packet entry to `workspace/shared/box3-open-questions.yaml`.

```yaml
- question_id: "annual.box3.peildatum_2025.banktegoeden_total"
  workflow: "annual_2025"
  section: "box3.peildatum"
  prompt_for_user: "What was the total balance across all bank and savings accounts on 1 January 2025? You can also attach bank statements."
  acceptable_sources: ["file", "user_chat"]
  evidence_hint: "bank statement around 1 January 2025"
- question_id: "provisional.box3.peildatum_2026.overige_bezittingen_total"
  workflow: "provisional_2026"
  section: "box3.peildatum"
  prompt_for_user: "What is your estimate for overige bezittingen on 1 January 2026?"
  acceptable_sources: ["file", "user_chat"]
  evidence_hint: "portfolio statement or estimate"
```

If a provisional user asks about actual return, answer that werkelijk rendement is not part of the 2026 voorlopige aanslag and may become relevant when filing the annual 2026 return in 2027.

Write only `workspace/shared/box3-notes.md`, `workspace/shared/box3-open-questions.yaml`, and `workspace/shared/box3-review-questions.md`. Do not write workpacks directly.
