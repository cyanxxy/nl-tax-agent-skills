---
name: nl-tax-partner-deductions
description: Use when partner or deduction allocation notes are needed.
user-invocable: false
allowed-tools:
  - Read
  - Grep
  - Bash(python3 *.py:*)
---

# NL Tax Partner Deductions

Background helper for fiscal-partner status and allocation notes used by manual-entry workpacks.

Load `workspace/taxpayer/profile.yaml`, `_shared/knowledge/security/prompt-injection.md`, and the relevant partner/deduction references. Use annual 2025 references for annual workpacks and provisional 2026 references for provisional estimates.

Write only:

- `workspace/shared/allocation-options.md`
- `workspace/shared/partner-deduction-review-questions.md`

Do not write annual/provisional workpacks, ask for partner DigiD, store full BSN/IBAN, or force unsupported partner cases into v1.
