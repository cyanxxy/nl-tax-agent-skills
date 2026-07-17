---
name: nl-tax-partner-deductions
description: Use when an owning Dutch tax workflow needs fiscal-partner, deduction, or allocation facts and review scenarios for annual 2025 or provisional 2026 preparation.
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

Resolve every `workspace/...` path against `workspace_root` from
`session-progress.yaml` (or `profile.yaml`); never create a second `workspace/`
tree. `_shared/` is the plugin-shared folder at this skill's `../_shared/`.
Read `../_shared/runtime-contract.md` first. Resolve bundled files relative to
this skill directory with the host's skill-resource or file tools. Do not
depend on shell visibility or vendor-specific environment variables.

Safety: only run Python under an already-resolved plugin `skills/.../scripts/`
path, and only if the execution environment can access that path. Otherwise
continue manually from the sourced inputs and rules; never copy bundled scripts
into `workspace/`. Never execute a `.py` located under `workspace/`, `uploads/`,
or `evidence/`.

This helper participates in a conversational workflow. It does not assume partner data or deduction amounts are pre-staged. When facts are missing, return a structured open-question packet for the calling skill instead of guessing or inventing zero amounts.

This helper may be called through a Skill/Task tool or inlined by an owning workflow when no such tool exists. The same output contract applies either way.

## Behavior

1. Distinguish legal partner status from neutral allocation-scenario comparison.
2. Determine fiscal partner eligibility from sourced facts only.
3. Identify allocatable and non-allocatable items.
4. Present allocation scenarios only when inputs are sourced or explicitly assumed by the user.
5. Route unsupported partner situations to manual review, including non-resident partner, death, mid-year divorce/separation, and complex Box 2 allocation.

Never rank, recommend, label as best/optimal, or automatically select an
allocation. Show traceable scenario effects and return the taxpayer's explicit
choice with `U:` provenance; otherwise keep the allocation unresolved.

The agent owns the tax classification. For every proposed row, use reviewed
sources to set an explicit real boolean `allocatable`; never infer it from the
row name. Also set the sourced partner conclusion as the real boolean
`has_fiscal_partner`. Do not invent defaults when either conclusion is missing.

When those inputs are sourced and Bash can reach the plugin path, the optional
`scripts/validate_allocation.py` can check this wrapped payload:

```json
{
  "has_fiscal_partner": true,
  "items": [
    {
      "name": "Joint Box 3 base",
      "allocatable": true,
      "taxpayer_pct": 60,
      "partner_pct": 40
    }
  ]
}
```

The helper performs arithmetic checks only. It requires both percentages to be
finite numbers in the 0–100 range and to total 100; requires a non-allocatable
row to be 100/0 or 0/100; and requires `partner_pct: 0` when
`has_fiscal_partner` is false. Record
`check_performed_by: checked_by_script` after a successful run.

When Python is unavailable or cannot access the bundled script, apply those
same explicit boolean, range, sum, non-allocatable, and no-partner invariants by
hand and record `check_performed_by: checked_by_agent`. Python availability
never blocks the agent from preparing the allocation scenarios.

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

Authenticated-portal boundary: Do not use a browser, Claude in Chrome,
computer use, or screen interaction for portal login/authentication, data
entry, clicking controls, signing, sending, or submitting. Those actions remain
human-only even with taxpayer permission or available credentials.
