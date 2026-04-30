# Rule note: Filing flow for annual return 2025

source_ids: bd_annual_return_landing_2025, bd_annual_return_4_steps_2025, bd_fisin_2025_index
workflow: annual-return
tax_year: 2025
status: active
last_reviewed: "2026-04-30"
review_status: reviewed

## Rule

The annual income tax return for 2025 (aangifte inkomstenbelasting 2025) is filed online at Mijn Belastingdienst. The Belastingdienst structures the filing process in four steps. This skill does NOT file the return -- it prepares a workpack that the taxpayer (or their representative) uses to complete the filing manually.

These are reference notes for workpack preparation -- not final tax advice.

## The four-step filing process

### Step 1: Log in (Inloggen)

- The taxpayer logs in at Mijn Belastingdienst using DigiD.
- DigiD is the government's digital identity system. This skill must never collect, store, or process DigiD credentials. See security/digid.md.
- If filing on behalf of someone else, proper authorization via DigiD Machtigen must be in place first. See security/machtigen.md.

### Step 2: Check pre-filled data (Vooringevulde aangifte controleren)

- The Belastingdienst pre-fills the return with data it has received from employers, banks, pension funds, mortgage lenders, and other third parties. This is called the vooringevulde aangifte (VIA).
- VIA data should be verified, not blindly trusted. Known issues include:
  - Delayed or missing employer data (jaaropgaaf not yet submitted by employer)
  - Incorrect or incomplete bank account balances for box 3
  - Missing foreign income
  - Outdated WOZ-waarde (gemeente may not have submitted updated value)
  - Missing deductible items (zorgkosten, giften) which are never pre-filled
- The workpack prepared by this skill includes verification checkpoints: each item in the workpack is paired with the corresponding VIA field so the taxpayer can compare.

### Step 3: Add or correct information (Aanvullen en corrigeren)

- The taxpayer adds information that is missing from the VIA and corrects any pre-filled data that is wrong.
- Common additions include:
  - Deductible items: zorgkosten, giften, alimentatie, lijfrentepremie
  - Own home details if not pre-filled correctly (WOZ-waarde, mortgage interest)
  - Foreign income and tax credits
  - Additional income sources not reported via payroll
  - Box 3 assets not reported by Dutch financial institutions (foreign accounts, crypto, real estate abroad)
- The workpack groups additions and corrections by section (box 1, box 3, deductions) so the taxpayer can work through them systematically.

### Step 4: Review, sign, and submit (Controleren, ondertekenen en versturen)

- The taxpayer reviews the complete return, including the calculated tax result.
- The return is digitally signed via DigiD and submitted.
- After submission, a bevestiging (confirmation) is provided with a timestamp and reference number.
- The taxpayer should save or print this confirmation.
- This skill cannot perform this step. The workpack includes a final checklist item: "Log in, enter the prepared data, review the calculated result, and submit."

## Filing deadline

- The standard deadline for filing the 2025 annual return is 1 May 2026.
- The taxpayer can request an extension (uitstel) through Mijn Belastingdienst or via a tax adviser. Extensions typically grant until 1 September 2026.
- If the taxpayer receives a blue envelope (aangiftebrief) or a digital notification, the deadline stated in that notice applies.
- Late filing may result in a verzuimboete (penalty for late filing).
- For returns filed in 2026 for tax year 2025: verify the exact deadline on the Belastingdienst website, as it may shift if 1 May falls on a weekend or public holiday.

## Workpack purpose

This skill prepares a workpack containing:
1. A summary of all income, deductions, and assets to be entered
2. Verification checkpoints for VIA pre-filled data
3. Calculations for reference (e.g., box 1 tax, box 3 tax, heffingskortingen)
4. A section-by-section entry guide matching the online filing form
5. A final submission checklist

The workpack is a preparation tool. The taxpayer retains full responsibility for the accuracy and completeness of the filed return.

## Notes

- VIA data typically becomes available from approximately 1 March of the filing year (2026 for tax year 2025). Filing before that date means more data may need to be entered manually.
- Fiscal partners can allocate certain income and deductions between them. The workpack should note allocation choices and their tax impact.
- The Belastingdienst may send a voorlopige aanslag (provisional assessment) based on the filed return. This is separate from the definitieve aanslag (final assessment) which may follow later.
