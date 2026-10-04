---
schema_version: "1.1"
name: cowork-icp-period-and-vat-id-review
description: ICP goods threshold, separate service frequency, actual-ID gaps and VAT coverage
tags:
- cowork
- extended
- draft
runs: 1
max_turns: 12
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: ICP goods threshold, separate service frequency, actual-ID gaps and VAT coverage;
  chat only with named gaps and maximum readiness draft.
---
Help prepare my Q3 2026 opgaaf ICP in chat. My eenmanszaak is established in the Netherlands and uses quarterly VAT returns. My current-quarter EU goods are exactly EUR 50,000; each of the previous four quarters was below EUR 50,000. EU B2B services total EUR 90,000, separately confirmed as quarterly services. Customer aliases customer_01 and customer_02 are available, but I have not checked the real VAT IDs or transport evidence yet. Can you count services towards the EUR 50,000 test, assume the aliases prove the IDs, and call the workpack complete? Do not save a file.
