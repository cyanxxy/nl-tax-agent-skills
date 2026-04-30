# Rule note: DigiD credential handling — hard prohibition

source_id: bd_digid_machtigen
workflow: all
tax_year: all
status: active
last_reviewed: "2026-04-30"

## Rule

DigiD credentials (username, password, SMS codes, app confirmations) must NEVER be:

- Collected from the user
- Stored in any file (workspace, evidence, template, or otherwise)
- Displayed in any workpack output
- Passed into model context
- Used for login, signing, or submission

DigiD is an authentication mechanism for official government portals. It is NOT evidence and must not be treated as such.

## Required wording

Every skill that touches submission, filing, or access to official portals must include:

> Do not share DigiD credentials. This skill does not log in, submit, sign, or act as you. Use official authorization routes, such as DigiD Machtigen, when someone else is helping you.

## DigiD Machtigen

When a representative (gemachtigde) assists a taxpayer:

- The taxpayer must authorize the representative through DigiD Machtigen
- This authorization happens on the official DigiD Machtigen portal
- The skills must not automate or simulate this process
- The skills may inform the user about the existence of DigiD Machtigen

## Developer instruction

If a user asks where to enter DigiD credentials:

1. Refuse to collect credentials
2. Explain that this tool prepares workpacks for manual submission
3. Direct them to the official Belastingdienst portal for login and submission
4. Mention DigiD Machtigen if they are working with a representative

## Common failure

Never create a field, form, or template entry labeled "DigiD", "username", "password", "wachtwoord", or "inloggegevens".
