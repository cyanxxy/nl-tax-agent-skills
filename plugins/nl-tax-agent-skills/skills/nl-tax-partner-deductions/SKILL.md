---
name: nl-tax-partner-deductions
description: Internal helper for nl-tax-annual-return and nl-tax-provisional-assessment — returns fiscal-partner and allocation/deduction facts and questions. Not a standalone workflow; invoked as a sub-step.
user-invocable: false
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(python3:*)
---

# NL Tax Partner Deductions

Background helper for fiscal-partner status and allocation notes used by manual-entry workpacks.

Load `workspace/taxpayer/profile.yaml` and the relevant partner/deduction references:

- `reference/fiscal-partner.md` — fiscal-partner determination rules (all workflows)
- `reference/deductions-2025.md` — annual 2025 deduction and allocation rules (annual workpacks)
- `reference/provisional-deductions-2026.md` — 2026 provisional deduction estimate rules (provisional workpacks)

Use annual 2025 references for annual workpacks and provisional 2026 references for provisional estimates.

Resolve every `workspace/...` path against `workspace_root` from `session-progress.yaml` (or `profile.yaml`); never create a second `workspace/` tree. `_shared/` is the plugin-shared folder at this skill's `../_shared/`. Resolve bundled files with host file tools (`Read` first, `Glob` or `Grep` if a path is not obvious). Do not use Bash to discover or read plugin files: in Cowork, shell commands run in an isolated VM that may not see the plugin cache even when `Read` and `Glob` can. If the host has already expanded `${CLAUDE_PLUGIN_ROOT}` or `${CLAUDE_SKILL_DIR}`, those absolute paths are fine for file tools; otherwise search within the loaded plugin/skill tree and resolve relative to this skill directory.

Safety: only run Python under an already-resolved plugin `skills/.../scripts/` path, and only if Bash can access that path. If Bash cannot see the plugin path, continue manually from the sourced inputs and rules; never copy bundled scripts into `workspace/`. Never execute a `.py` located under `workspace/`, `uploads/`, or `evidence/`.

This helper participates in a conversational workflow. It does not assume partner data or deduction amounts are pre-staged. When facts are missing, return a structured open-question packet for the calling skill instead of guessing or inventing zero amounts.

This helper may be called through a Skill/Task tool or inlined by an owning workflow when no such tool exists. The same output contract applies either way.

## Behavior

1. Distinguish legal partner status from allocation optimization.
2. Determine fiscal partner eligibility from sourced facts only.
3. Identify allocatable and non-allocatable items.
4. Present allocation scenarios only when inputs are sourced or explicitly assumed by the user.
5. Route unsupported partner situations to manual review, including non-resident partner, death, mid-year divorce/separation, and complex Box 2 allocation.

When allocation inputs are sourced and Bash can reach the plugin path, run
`scripts/validate_allocation.py` to check the split. When it cannot (e.g. Cowork's
isolated VM), apply the same invariants by hand: each allocatable item's
`partner1_share + partner2_share` must equal its total (the split sums to 100%),
no share is negative or exceeds the total, non-allocatable/personal items go 100%
to one partner, and a partner-2 share is valid only when a fiscal partner has been
asserted.

## Question packet

Return missing inputs to the calling workflow in this shape:

```yaml
- question_id: "partner.eligibility.cohabitation_conditions"
  workflow: "annual_2025"
  section: "partner.eligibility"
  prompt_for_user: "Are you registered at the same address as your partner, and do you have a notarial cohabitation contract, joint home, joint child, or pension-partner status?"
  acceptable_sources: ["user_chat"]
  evidence_hint: null
- question_id: "annual.deductions.giften.amount"
  workflow: "annual_2025"
  section: "deductions.giften"
  prompt_for_user: "What was the total ANBI-qualifying donation amount in 2025? You can provide one total or attach receipts."
  acceptable_sources: ["file", "user_chat"]
  evidence_hint: "donation receipts"
```

The calling skill asks these questions, records `source` plus
`quote`/`evidence_id`, and re-invokes this helper.

Return structured facts and open questions to the owning workflow. Do not
persist any final artifact, including shared notes, question packets, session
state, workpacks, or field maps. The annual/provisional workflow owns all
workspace persistence and may read historical helper notes for resume
compatibility only. Do not force unsupported partner cases into v1.
