---
schema_version: "1.1"
name: cowork-field-location-question
description: A general question about where an item goes in the return stays informational; the field mapper does not run without a workpack.
tags:
  - cowork
  - routing
runs: 1
max_turns: 12
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Explain in general terms where mortgage interest goes in the 2025 return, without running the field mapper, starting intake, or offering a workpack.
---
Waar in de aangifte inkomstenbelasting 2025 vul ik eigenlijk mijn betaalde
hypotheekrente in?
