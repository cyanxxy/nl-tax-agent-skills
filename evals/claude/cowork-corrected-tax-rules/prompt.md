---
schema_version: "1.1"
name: cowork-corrected-tax-rules
description: Retrieve corrected healthcare, credit, and filing-deadline rules from the bundled notes.
tags:
  - cowork
  - tax-correctness
runs: 1
max_turns: 6
timeout_seconds: 300
expected_outcome: State the corrected healthcare exclusions, credit base, and conditional deadline branches accurately.
---
For my Dutch 2025 return, please answer three questions from the plugin's
bundled notes. Are my health-insurance premium, mandatory eigen risico,
wheelchair, mobility scooter, and home modification deductible as specifieke
zorgkosten? Do heffingskortingen reduce only box-1 income tax? Finally, what
filing and extension dates apply if I either have a normal invitation letter,
have a letter with another date, or received no invitation but know tax is due?
