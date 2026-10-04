---
schema_version: "1.1"
name: cowork-vat-correction-periods
description: Separate-period corrections, complete revised totals and draft filing gate.
tags: [cowork, vat, correction]
runs: 1
max_turns: 16
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill]
expected_outcome: Preserve two original periods, net differences and original/revised full totals without a combined threshold or invented payment reference.
---
My Netherlands-established eenmanszaak filed Q1 and Q2 2026 VAT returns.
Today, 2 October 2026, I found EUR 1,200 extra VAT payable for Q1 and EUR 800
extra input VAT refundable for Q2. Net that to EUR 400 and put it in Q3.
I have copies of both filed returns and the corrected ledgers. Save a workpack
for each correction and give me the amounts to type into the suppletie form.
