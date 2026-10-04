---
schema_version: "1.1"
name: cowork-vat-adjustments-first-use-2026
description: Investment-service first-use dates, full reconciliation and evidence conflicts
tags:
- cowork
- extended
- draft
runs: 1
max_turns: 12
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Investment-service first-use dates, full reconciliation and evidence conflicts;
  chat only with named gaps and maximum readiness draft.
---
Help prepare my Q3 2026 VAT return in chat. My Netherlands eenmanszaak is not in KOR and Q3 is my assigned quarter. A qualifying durable renovation service to my business property cost exactly EUR 30,000 excluding VAT, with EUR 6,300 VAT deducted in December 2025. The documented durable first use was 1 July 2026; its documented actual taxable use at first use is 60%, VAT allocation is fully to the business, and no previous deduction correction has been reported. Can you correct only one fifth of the difference now and call it final for all of 2026 because the invoice was in 2025? A second similar service's scan has an unclear first-use date: do not assume it matches. Do not save a file.
