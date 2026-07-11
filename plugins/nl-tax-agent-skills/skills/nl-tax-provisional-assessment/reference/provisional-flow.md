# Provisional Flow — Subflow Routing and Generation

This is the common routing and output contract for the 2026 provisional-assessment workflow. Load this index when the workflow starts, then load exactly one active subflow file. If routing changes, stop using the old subflow and load exactly one newly active subflow.

## Overview

This document defines the routing logic, data collection steps, decision points, and output generation for each of the four provisional assessment subflows.

Across review/change output, state that a later **unsolicited** VA based on earlier data **may be issued**, but is **not guaranteed**. For a change, prepare and **verify** the **complete dataset**; all applicable categories are required, not only the changed item. **Moving abroad** routes to **residency review** and is **not a categorical stopzetten reason**.

## Subflow routing

```
User enters provisional skill
  │
  ├── workflow_candidate = provisional_2026_request
  │     → Request subflow
  │
  ├── workflow_candidate = provisional_2026_change
  │     → Change subflow
  │
  ├── workflow_candidate = provisional_2026_review
  │     → Review subflow
  │
  └── workflow_candidate = provisional_2026_stopzetten
        → Stopzetten subflow
              │
              ├── User receives monthly refund (teruggaaf)
              │     → Stopzetten guidance
              │
              └── User pays monthly amount (betaling) + amount is wrong
                    → REDIRECT to Change subflow
```

---

## Direct subflow links

- [Request subflow](subflows/request.md) — only when no 2026 provisional assessment exists yet.
- [Change subflow](subflows/change.md) — rebuild and verify the complete current dataset against a baseline.
- [Review subflow](subflows/review.md) — compare a current assessment with present facts.
- [Stopzetten subflow](subflows/stopzetten.md) — apply refund/payment routing and the cutoff rule.

Do not load multiple subflow files for comparison. Route first and load exactly one active file. A stopzetten payment case that redirects to change must update the workflow state before loading `subflows/change.md`.

## Common rules across all subflows

- All amounts are estimates unless explicitly labeled as from-baseline
- Box 2 amounts must be labeled as estimates or from-baseline.
- Box 3 uses the provisional fictitious method only. Include only the explanatory note: "Werkelijk rendement is not part of provisional 2026."
- Every workpack must include the "Not submission advice" footer
- Every workpack must list source_ids for all knowledge sources used
- Every workpack must include the assumptions section
- Output files go to `workspace/provisional/2026/` — never to `workspace/annual/`
