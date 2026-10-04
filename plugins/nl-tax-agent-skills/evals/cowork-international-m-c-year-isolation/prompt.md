---
schema_version: "1.1"
name: cowork-international-m-c-year-isolation
description: Separate migration/nonresident years, worldwide evidence and treaty/social review
tags:
- cowork
- extended
- draft
runs: 1
max_turns: 12
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Separate migration/nonresident years, worldwide evidence and treaty/social review;
  chat only with named gaps and maximum readiness draft.
---
I moved from Belgium to the Netherlands on 1 September 2025 and want to prepare my 2025 migration return. Separately I moved back to Belgium on 1 January 2026, lived there throughout 2026, and had Dutch employment income. Can you also start a 2026 nonresident draft using my 2025 resident documents and my estimated 2026 voorlopige aanslag amounts as final annual facts? Assume the treaty and social-insurance outcome are the same in both years. Keep both in chat, no files.
