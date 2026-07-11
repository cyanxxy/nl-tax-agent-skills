---
schema_version: "1.1"
name: cowork-casual-tax-question
description: A casual Dutch tax question must stay informational instead of starting intake.
tags:
  - cowork
  - routing
runs: 1
max_turns: 5
timeout_seconds: 300
expected_outcome: Answer the question directly and do not start a workpack or screening interview.
---
Ik betaalde in 2025 zelf voor voorgeschreven medicijnen die niet door mijn
zorgverzekering zijn vergoed. Kunnen zulke kosten aftrekbaar zijn?
