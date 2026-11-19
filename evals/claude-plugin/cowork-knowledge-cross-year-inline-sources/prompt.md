---
schema_version: "1.1"
name: cowork-knowledge-cross-year-inline-sources
description: Cross-year Q&A compares 2025 annual and 2026 provisional Box 3 figures using inline official sources without loading internal helpers or starting intake.
tags:
  - cowork
  - knowledge
  - routing
runs: 1
max_turns: 12
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill, Edit, Write]
expected_outcome: Answer directly with both 2025 annual and 2026 provisional Box 3 figures clearly labeled by year and workflow, cite official Belastingdienst sources from the notes' inline Official sources sections, do not load workflow helpers or start intake, and write no file.
---
How did the Dutch Box 3 heffingsvrij vermogen (single person) and the
fictitious banktegoeden percentage change between the 2025 annual return and
the 2026 voorlopige aanslag? Please include the official Belastingdienst links.
