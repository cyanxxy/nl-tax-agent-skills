# Rule note: Filing flow for annual return 2025

source_ids: bd_annual_return_landing_2025, bd_annual_return_4_steps_2025, bd_fisin_2025_index, bd_annual_deadline_2025, bd_annual_filing_obligation_2025, bd_annual_extension_2025, bd_annual_extension_eligibility_2025
workflow: annual_return
tax_year: 2025
status: active
last_reviewed: "2026-07-16"
review_status: reviewed

## Rule

The annual income tax return for 2025 (aangifte inkomstenbelasting 2025) is filed online at Mijn Belastingdienst. The Belastingdienst structures the filing process in four steps. This skill does NOT file the return -- it prepares a workpack that the taxpayer (or their representative) uses to complete the filing manually.

These are reference notes for workpack preparation -- not final tax advice.

## The four-step filing process

### Step 1: Prepare (Voorbereiden)

- The taxpayer gathers the required documents and data, including rekeningnummer, 2025 jaaropgaven, 2025 bank and investment overviews, crypto exchange overviews if relevant, WOZ-waarde with valuation date 1 January 2024, mortgage annual statement, and evidence for deductions.
- If filing on behalf of someone else, proper authorization must be in place first. See security/machtigen.md.

### Step 2: Open the return (De aangifte openen)

- The taxpayer logs in at Mijn Belastingdienst.
- In Mijn Belastingdienst, the taxpayer selects `Inkomstenbelasting` and then the relevant tax year.

### Step 3: Check pre-filled data (Controleren)

- The Belastingdienst pre-fills the return with data it has received from employers, banks, pension funds, mortgage lenders, and other third parties. This is called the vooringevulde aangifte (VIA).
- VIA data should be verified, not blindly trusted. Known issues include:
  - Delayed or missing employer data (jaaropgaaf not yet submitted by employer)
  - Incorrect or incomplete bank account balances for box 3
  - Missing foreign income
  - Outdated WOZ-waarde (gemeente may not have submitted updated value)
  - Missing deductible items (zorgkosten, giften) which are never pre-filled
- The taxpayer adds information that is missing from the VIA and corrects any pre-filled data that is wrong.
- Common additions include:
  - Deductible items: zorgkosten, giften, alimentatie, lijfrentepremie
  - Own home details if not pre-filled correctly (WOZ-waarde, mortgage interest)
  - Foreign income and tax credits
  - Additional income sources not reported via payroll
  - Box 3 assets not reported by Dutch financial institutions (foreign accounts, crypto, real estate abroad)
- The workpack groups additions and corrections by section (box 1, box 3, deductions) so the taxpayer can work through them systematically.

### Step 4: Review, sign, and submit (Ondertekenen en versturen)

- The taxpayer reviews the complete return, including the calculated tax result.
- The return is digitally signed and submitted.
- After submission, a bevestiging (confirmation) is provided with a timestamp and reference number.
- The taxpayer should save or print this confirmation.
- This skill cannot perform this step. The workpack includes a final checklist item: "Log in, enter the prepared data, review the calculated result, and submit."

## Filing deadline

- Record one of these review labels after asking the taxpayer and checking the
  completed-but-not-yet-submitted return in Mijn Belastingdienst. These labels
  organize evidence; they are not an automatic decision engine:
  - `invited`: an aangiftebrief exists. Filing is mandatory and the applicable
    deadline is the date in the letter.
  - `no_letter_but_mandatory`: no aangiftebrief exists, but the completed 2025
    return shows **EUR 58 or more to pay**, or the separate asset/scheme screen
    below applies. Submit before **14 July 2026**.
  - `refund_claim_only`: no aangiftebrief exists, the completed return shows
    **EUR 19 or more back**, and neither mandatory no-letter test applies. The
    taxpayer may submit to claim the refund; do not describe this as an
    invitation-based filing obligation.
  - `filing_obligation_unresolved`: no aangiftebrief exists and the return has
    not been completed far enough to establish the payable/refund result, or
    the asset/scheme facts are unresolved. Do not invent a deadline or label the
    taxpayer late; ask them to complete the official calculation without
    submitting and resolve the open facts.
- The separate asset/scheme screen makes filing mandatory without a letter when
  the taxpayer has a right to an income-dependent scheme (for example benefits
  or subsidized legal aid) and the relevant assets of the taxpayer, partner, or
  minor child(ren) exceed **EUR 37,395**, or **EUR 74,790 with a fiscal partner**.
  This applies even when the ordinary result is less than EUR 19 back or less
  than EUR 58 to pay. Ask about both parts; do not infer either from a bank total
  alone.
- A result below EUR 58 to pay or below EUR 19 back does not, by itself, settle
  the separate asset/scheme test.
- Extension eligibility requires an invitation letter. With **no invitation**,
  extension is unavailable.
- **Current as of 16 July 2026:** the ordinary online window closed on
  **1 May 2026**; historically the request had to be made **before 1 May 2026**.
  Do not tell the taxpayer they can still use it. If extension
  was already granted through that route, verify the confirmation; the standard
  granted date is **1 September 2026** (4 months extra).
- If the aangiftebrief shows another date—a different, still-future filing date—extension
  may be requested up to that printed date through the **official form** route;
  online extension is unavailable for this exception. Use the date in the
  decision. If that printed date has passed, do not present extension as still
  available; recommend filing promptly and reviewing official correspondence.
- Penalty screening differs by route. An invited return uses the
  reminder/aanmaning filing regime; a no-letter mandatory return can raise the
  separate failure-to-request-an-aangifte regime. Load `late-filing.md` before
  describing either exposure and never merge their amounts or conditions.
- Always use the date in the invitation letter or Mijn Belastingdienst rather than assuming a default date.

## Workpack purpose

This skill prepares a workpack containing:
1. A summary of all income, deductions, and assets to be entered
2. Verification checkpoints for VIA pre-filled data
3. Calculations for reference (e.g., box 1 tax, box 3 tax, heffingskortingen)
4. A section-by-section entry guide organized for preparation (the official online aangifte groups the same data into onderwerpen and lets you complete them in any order, so the workpack order is a preparation order, not a fixed website sequence)
5. A final submission checklist

The workpack is a preparation tool. The taxpayer retains full responsibility for the accuracy and completeness of the filed return.

## Notes

- Check VIA availability in the official filing environment before relying on pre-filled data. Filing before the pre-filled data is complete means more data may need to be entered manually.
- Fiscal partners can allocate certain income and deductions between them. The workpack should note allocation choices and their tax impact.
- The Belastingdienst may send a voorlopige aanslag (provisional assessment) based on the filed return. This is separate from the definitieve aanslag (final assessment) which may follow later.
