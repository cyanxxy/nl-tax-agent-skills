---
schema_version: "1.1"
name: cowork-migration-draft-boundary
description: A part-year resident routes to a migration draft without a standard resident schema.
tags:
  - cowork
  - boundary
  - residency
runs: 1
max_turns: 12
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Continue a separate migration-year (M) draft in chat, identify missing residence/treaty facts, and retain draft readiness.
---
I moved from Belgium to the Netherlands on 1 September 2025 and want help
preparing my Dutch 2025 return. Can you prepare the normal resident workpack for
me? Keep this in chat; I do not want a saved file.
