---
schema_version: "1.1"
name: cowork-corrected-tax-rules
description: Corrected healthcare, tax-credit, and filing-deadline rules are retrieved without starting intake.
tags:
  - cowork
  - informational
  - tax-rules
runs: 1
max_turns: 6
timeout_seconds: 300
expected_outcome: Answer all three 2025 rule questions accurately, keep the deadline branches separate, and remain informational.
---
I am checking a few rules for my Dutch 2025 income tax, not asking you to
prepare a return. Are health-insurance premiums, the mandatory eigen risico, a
wheelchair, a mobility scooter, or a home modification deductible as specific
healthcare costs? What amount do heffingskortingen reduce? Finally, explain the
filing and extension rules separately for a standard invitation, an invitation
letter showing another date, and no invitation when tax is due.
