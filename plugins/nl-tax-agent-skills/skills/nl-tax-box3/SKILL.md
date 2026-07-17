---
name: nl-tax-box3
description: Use when an owning Dutch tax workflow needs Box 3 facts and questions; annual 2025 compares fictitious and actual return, while provisional 2026 uses the fictitious method only.
user-invocable: false
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(python3:*)
---

# NL Tax Box 3

Background helper for box 3 notes.

Annual 2025 must cover fictitious return and werkelijk-rendement data collection for user review. Provisional 2026 must use only the provisional fictitious method and must never ask for werkelijk rendement.

This helper participates in a conversational workflow. It does not assume all asset and debt inputs are pre-staged. When values are missing, return a structured open-question packet for the calling skill instead of inventing zeros.

This helper may be called through a Skill/Task tool or inlined by an owning workflow when no such tool exists. The same output contract applies either way.

## Hard rules

- Annual 2025: collect and compare fictitious return and werkelijk rendement when the user wants the actual-return comparison.
- Ask only branch-applicable annual inputs. A savings-only case needs the
  1 January balance for the fictitious method and actual 2025 interest for an
  actual-return comparison; it does not need a 31 December bank balance merely
  because the comparison was offered.
- Provisional 2026: use only the fictitious method.
- Never request werkelijk-rendement inputs in a provisional workflow.
- In provisional 2026, accept a debt into `schulden` only after the official
  inclusion/exclusion screen. Do not use "all debts except the own-home
  mortgage" as a shortcut; unresolved debts remain manual-review rows outside
  accepted totals.
- Compute only from values with a real source or an explicitly confirmed assumption.
- The agent classifies each row from the reviewed facts and official rules. Python
  never infers a category from a description, name, or keyword.
- Before arithmetic, represent every row with `category`, `status`, `value`, and
  `provenance`. Only `status: "accepted"` rows in `banktegoeden`,
  `overige_bezittingen`, or `schulden`, with finite non-negative values and
  non-empty provenance, enter trusted totals. Keep every other row in a
  rejected/manual-review table with a reason.
- The bundled scripts require `--partner-full-year-confirmed` alongside `--has_partner` before they double the heffingsvrij vermogen and the schulden drempel; `--has_partner` on its own raises an error. They also reject negative or non-finite amounts. Do not present a doubled allowance until full-year partnership is confirmed.

## Loading bundled files

`_shared/` is the plugin-shared folder at this skill's `../_shared/`. Resolve
bundled files relative to this skill directory with the host's skill-resource
or file tools. Read `../_shared/runtime-contract.md` first. Do not depend on
shell visibility or vendor-specific environment variables.

Bundled references — read the ones matching the active workflow before computing or asking anything:

- `reference/box3-annual-2025.md` — annual 2025 fictitious-method rules and rates
- `reference/box3-actual-2025.md` — annual 2025 werkelijk-rendement (actual return) data rules, for the annual comparison only
- `reference/box3-provisional-2026.md` — 2026 provisional fictitious-method rules (the only box 3 reference a provisional flow may use)

The knowledge files those references point at (`_shared/knowledge/years/2025/box3/*.md`, `_shared/knowledge/years/2026/provisional/box3-provisional.md`) stay canonical for every numeric value.

Only run Python under an already-resolved plugin `skills/.../scripts/` path (for this skill, `scripts/compare_box3_annual_2025.py` and `scripts/summarize_box3_provisional_2026.py`), and only if Bash can access that path. Python is optional: if Bash cannot see the plugin path, total accepted rows and apply the sourced arithmetic manually; never ask the taxpayer to install Python, never copy bundled scripts into `workspace/`, and never execute a `.py` located under `workspace/`, `uploads/`, or `evidence/`.

## Behavior

Resolve every `workspace/...` path against `workspace_root` from
`session-progress.yaml` (or `profile.yaml`); never create a second
`workspace/` tree.

For each needed input, check section notes and evidence first. If the value is unavailable, return a question packet entry to the calling workflow.

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

When the description alone is ambiguous, do not guess. A generic loan starts
like this until the user establishes whether it is a receivable, a liability,
or outside the standard case:

```yaml
- description: "Loan to friend"
  category: "unknown"
  status: "manual_review"
  value: 10000
  provenance: "U:<dated user statement>"
```

For the no-Python path, apply the same accepted-category, status, finite
non-negative value, and provenance checks, then record
`check_performed_by: "checked_by_agent"`. An optional script run records
`check_performed_by: "checked_by_script"`. Both paths preserve the accepted
rows and rejected/manual-review rows in the calling workflow's workpack.

Return structured facts and open questions to the owning workflow. Do not
persist any final artifact, including shared notes, question packets, session
state, workpacks, or field maps. The annual/provisional workflow owns all
workspace persistence and may read historical helper notes for resume
compatibility only.

Authenticated-portal boundary: Do not use a browser, Claude in Chrome,
computer use, or screen interaction for portal login/authentication, data
entry, clicking controls, signing, sending, or submitting. Those actions remain
human-only even with taxpayer permission or available credentials.
