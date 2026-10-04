---
schema_version: "1.1"
name: cowork-vat-small-correction-payment
description: A small correction paid with the next ordinary VAT return does not wait for a suppletie assessment.
tags:
  - cowork
  - vat
  - correction
runs: 1
max_turns: 12
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Explain the next-return route and its ordinary payment timing without waiting for a separate assessment.
---
I am a Netherlands-established ZZP, outside KOR, filing quarterly VAT returns.
On 1 October 2026 I found an omitted domestic sale in my filed Q2 2026 return.
I have checked the full figures: its payable balance should have been EUR 5,500
instead of EUR 5,000, all from EUR 500 of omitted VAT in rubric 1a. The Q2
deadline was 31 July 2026. No correction has been filed.

My Q3 return is the next return and is still unfiled. Its own payable balance
before this correction is EUR 1,200, and the assigned payment deadline is
31 October 2026. Do I pay the EUR 500 separately now, wait for an assessment,
or pay it with Q3? Explain the amount and timing. Keep this in chat and do not
save anything or access the portal.
