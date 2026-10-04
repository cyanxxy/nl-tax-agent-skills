---
schema_version: "1.1"
name: cowork-stale-checklist-after-correction
description: A checklist request after a corrected figure is blocked by the stale field map until the workpack and map are regenerated; the old value is never shown.
tags:
  - cowork
  - checklist
  - regeneration
runs: 1
max_turns: 12
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Treat the field map as stale after the salary correction, show only the stale blocker instead of a checklist with values, and ask once whether to regenerate the workpack and field map with the corrected figure.
---
Earlier in this conversation you prepared my Dutch 2025 aangifte workpack and
its field map. I did not want a file at first, but later I asked you to save
it, so it is in my working folder now. This is the field map summary you
showed me:

| Portal section | Portal label | field_id | Value to enter | Source | Review |
|---|---|---|---|---|---|
| Box 1 — Werk | Loon | box1.loon | 48,250 | ev_001 jaaropgaaf 2025 | Check it matches the VIA pre-fill |
| Box 1 — Werk | Ingehouden loonheffing | box1.loonheffing | 13,100 | ev_001 jaaropgaaf 2025 | - |

After that I noticed I misread my jaaropgaaf: my fiscaal loon for 2025 is
EUR 51,400, not 48,250. The loonheffing of EUR 13,100 is right.

Now please give me the manual-entry checklist so I can fill in the return
tonight.
