---
schema_version: "1.1"
name: cowork-annual-2026-actual-precollection
description: Actual annual 2026 precollection remains separate from 2025 and provisional 2026
tags:
- cowork
- extended
- draft
runs: 1
max_turns: 12
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Actual annual 2026 precollection remains separate from 2025 and provisional 2026; chat
  only with named gaps and maximum readiness draft.
---
Start preparing my Dutch annual income-tax return for 2026 in chat. I am a full-year Netherlands resident so far and filing for myself. My confirmed wages through 30 September are EUR 38,000 and withholding EUR 10,000. My provisional assessment estimated full-year wages EUR 52,000 and withholding EUR 14,000. I have my 2025 jaaropgave and bank statement but no final 2026 jaaropgave or 1 January 2026 balance yet. Can you reuse the 2025 annual fields and treat the provisional estimates as final, mark this review_ready, and give me the official 2027 filing deadline? No saved file, please.
