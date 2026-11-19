---
schema_version: "1.1"
name: cowork-annual-via-focused-section
description: VIA verify-and-complete focused section mode checks own-home arithmetic (including periodic erfpacht and separate tariefsaanpassing) without forcing a 14-phase full-return survey or writing files.
tags:
  - cowork
  - via
  - eigen-woning
runs: 1
max_turns: 12
timeout_seconds: 300
allowed_tools: [Read, Glob, Grep, Skill, Edit, Write]
expected_outcome: Verify the pre-filled 2025 eigen woning figures, include periodic erfpacht in total_deductible_own_home_costs, compute box1_own_home_balance of -EUR 8,600, keep tariefsaanpassing separate from taxable Box 1 income, stay focused on own-home rather than running a 14-phase interview, and write no file.
---
I already have my pre-filled 2025 Vooringevulde Aangifte (VIA) open in Mijn
Belastingdienst and just want help verifying ONLY the eigen woning section in
chat (no saved file). I am a full-year Dutch resident filing as a single
taxpayer with no fiscal partner. My 2025 jaaropgaaf fiscaal loon is EUR 90,000.
For my single main residence owned all of 2025 (linear mortgage started in
2020): WOZ-waarde (peildatum 1 Jan 2024) is EUR 400,000, mortgage interest paid
in 2025 is EUR 9,200, and periodic erfpacht paid in 2025 is EUR 800. Please
check the eigenwoningforfait, total deductible own-home costs, Box 1 own-home
balance, and whether tariefsaanpassing applies.
