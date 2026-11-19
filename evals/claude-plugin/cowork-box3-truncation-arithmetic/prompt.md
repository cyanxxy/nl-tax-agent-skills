---
schema_version: "1.1"
name: cowork-box3-truncation-arithmetic
description: Annual 2025 Box 3 preparation follows the official 6-step model with debt threshold and 2-decimal truncation toward zero on aandeel in de rendementsgrondslag.
tags:
  - cowork
  - arithmetic
  - box3
runs: 1
max_turns: 12
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill, Edit, Write]
expected_outcome: Show all 6 official 2025 Box 3 steps explicitly, subtract the EUR 3,800 debt threshold first, truncate aandeel to 59.88% (not 59.89%), mention the optional werkelijk rendement comparison without calling it an election, and write no file.
---
Help me check only the Box 3 section for my 2025 Dutch annual income-tax return
in chat (no saved file). I am a full-year Dutch resident filing as a single
individual with no fiscal partner. On 1 January 2025 I had EUR 100,000 in Dutch
savings accounts, EUR 50,000 in listed ETFs, and a EUR 10,000 personal consumer
loan (not a mortgage). I decline to supply actual-return figures for now; just
show me the step-by-step 2025 fictitious Box 3 breakdown.
