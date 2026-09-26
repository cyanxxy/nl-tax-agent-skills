---
schema_version: "1.1"
name: cowork-save-and-resume
description: A saved workpack the user brings back is resumed from its resume record without re-running intake or re-asking answered questions.
tags:
  - cowork
  - resume
  - saving
runs: 1
max_turns: 6
timeout_seconds: 300
expected_outcome: Check the resume record, continue from the first unfinished section without re-asking answered questions, keep saving only to the one fixed file, and re-confirm a figure that is not visible.
---
Last week you helped me with my Dutch 2025 aangifte and I asked you to save the
workpack. I can't attach the file here, so these are the parts of it I copied.
Please continue where we stopped.

From my Taxpayer profile summary: I was a full-year Dutch resident, I file as
an individual, I have no fiscal partner, no business, and no shares in a BV.
My employment income section was finished from my jaaropgaaf. We also talked
about my WOZ value last time but I didn't copy that part.

```yaml
workpack_format: nl-tax-workpack
workpack_version: "2.0"
plugin_version: "0.4.0"
workflow: annual_2025
tax_year: 2025
created_at: "2026-09-18T19:02:00Z"
updated_at: "2026-09-18T20:41:00Z"
save_consent: given
readiness: draft
generation_confirmed: false
queued_workflow: null
sections:
  filing_status: {status: complete, open: []}
  box1: {status: complete, open: []}
  winst: {status: complete, open: []}
  eigen_woning: {status: in_progress, open: [Q004]}
  box2: {status: chat_only, open: []}
  box3_peildatum: {status: not_started, open: []}
  box3_actual: {status: not_started, open: []}
  deductions: {status: not_started, open: []}
  credits_screening: {status: not_started, open: []}
  partner_allocation: {status: chat_only, open: []}
  confirm: {status: not_started, open: []}
sources_loaded: [bd_box1_rates_2025, bd_jaaropgaaf_fields_2025]
```
