---
name: nl-tax-partner-deductions
description: Internal helper for nl-tax-annual-return and nl-tax-provisional-assessment — determines fiscal-partner status and allocation/deduction notes into workspace/shared/. Not a standalone workflow; invoked as a sub-step.
user-invocable: false
allowed-tools:
  - Read
  - Grep
  - Bash(python3 *.py:*)
---

# NL Tax Partner Deductions

Background helper for fiscal-partner status and allocation notes used by manual-entry workpacks.

Load `workspace/taxpayer/profile.yaml`, `_shared/knowledge/security/prompt-injection.md`, and the relevant partner/deduction references. Use annual 2025 references for annual workpacks and provisional 2026 references for provisional estimates.

Resolve every `workspace/...` path against `workspace_root` from `session-progress.yaml` (or `profile.yaml`); never create a second `workspace/` tree. `_shared/` is the plugin-shared folder at this skill's `../_shared/`.

This helper participates in a conversational workflow. It does not assume partner data or deduction amounts are pre-staged. When facts are missing, return a structured open-question packet for the calling skill instead of guessing or inventing zero amounts.

## Behavior

1. Distinguish legal partner status from allocation optimization.
2. Determine fiscal partner eligibility from sourced facts only.
3. Identify allocatable and non-allocatable items.
4. Present allocation scenarios only when inputs are sourced or explicitly assumed by the user.
5. Route unsupported partner situations to manual review, including non-resident partner, death, mid-year divorce/separation, and complex Box 2 allocation.

## Question packet

Append missing inputs to `workspace/shared/partner-deductions-open-questions.yaml`:

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

The calling skill asks these questions, records `source` plus `quote`/`evidence_id`, and re-invokes this helper.

Write only:

- `workspace/shared/allocation-options.md`
- `workspace/shared/partner-deduction-review-questions.md`
- `workspace/shared/partner-deductions-open-questions.yaml`

Do not write annual/provisional workpacks, ask for partner DigiD, store full BSN/IBAN, or force unsupported partner cases into v1.

## Must NOT write to

This helper writes only under `workspace/shared/`. It must never write to:

- `workspace/annual/**`
- `workspace/provisional/**`

Only `nl-tax-annual-return` and `nl-tax-provisional-assessment` own those trees. On hosts that do not enforce `allowed-tools` (for example Codex, which reads only the SKILL.md body), treat this as a hard instruction, not just a tool restriction.
