---
schema_version: "1.1"
name: cowork-c-return-refund-interest
description: A late nonresident return with a prompt refund assessment does not automatically earn interest.
tags:
  - cowork
  - international
  - interest
runs: 1
max_turns: 12
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Explain why a refund assessed within thirteen weeks does not qualify for interest merely because the C return was filed after 1 May.
---
I lived outside the Netherlands for all of 2025. The Belastingdienst received
my Dutch C 2025 return on 1 July 2026 and issued the final assessment on
1 August 2026, accepting the return unchanged and refunding EUR 2,000. This
was my first assessment, not a reduction of a provisional assessment.

The C-form explanation says I receive interest if I get money back after
filing after 1 May. Does that mean they should have paid me interest? Explain
the relevant conditions without calculating interest, drafting an objection,
accessing my portal or saving a file.
