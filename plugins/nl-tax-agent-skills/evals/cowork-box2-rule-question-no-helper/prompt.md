---
schema_version: "1.1"
name: cowork-box2-rule-question-no-helper
description: A Box 2 rule question is answered informationally; no background helper runs without an owning workflow.
tags:
  - cowork
  - routing
runs: 1
max_turns: 12
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Answer how 2025 Box 2 dividend taxation works from the bundled notes, without invoking a background helper, starting intake, or offering a workpack.
---
Ik heb een eigen BV en keer mezelf dit jaar dividend uit. Hoe wordt dat
dividend in 2025 belast in box 2?
