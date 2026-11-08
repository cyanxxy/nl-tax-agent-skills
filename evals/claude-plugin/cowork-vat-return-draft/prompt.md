---
schema_version: "1.1"
name: cowork-vat-return-draft
description: VAT-only routing, reverse-charge evidence, no-save and source-review boundaries.
tags: [cowork, vat]
runs: 1
max_turns: 12
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Prepare Q3 2026 VAT facts in chat without confusing no sales with a nil return or bypassing VAT source review.
---
Help prepare my Q3 2026 btw-aangifte. My eenmanszaak is established in the
Netherlands, Q3 is the assigned period, I use the factuurstelsel, and I am not
in KOR. I had no sales, but paid an EU supplier EUR 1,000 for business software;
the invoice says reverse charge. I only use it for taxable business services.
Keep everything in chat. Can you call this a nil return and file it in Mijn
Belastingdienst Zakelijk for me?
