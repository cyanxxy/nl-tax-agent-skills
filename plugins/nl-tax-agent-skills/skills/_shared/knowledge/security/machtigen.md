# Rule note: Authorization and representation (Machtigen)

source_id: bd_digid_machtigen
workflow: all
tax_year: all
status: active
last_reviewed: "2026-04-30"

## Rule

When someone other than the taxpayer is preparing or submitting a tax return or voorlopige aanslag, proper authorization must be in place through official channels.

## Authorization routes

### DigiD Machtigen
- A taxpayer can authorize another person to handle tax matters on their behalf
- This is done through the official DigiD Machtigen service
- The authorization must be set up BEFORE the representative can act
- Skills may inform users about this service but must not automate it

### Bewindvoerder / Curator
- Court-appointed administrators have separate authorization procedures
- These are outside v1 scope — route to professional advice

### Belastingconsulent / Adviseur
- Tax advisers typically use their own professional authorization
- This is handled through the Belastingdienst's intermediary portal
- Outside v1 scope for automation — route to their professional workflow

## What skills may do

- Inform the user that DigiD Machtigen exists
- Explain that authorization must happen through official channels
- Include "check authorization" as a step in submission checklists
- Note in the workpack when a representative scenario is detected

## What skills must NOT do

- Collect or store authorization credentials
- Simulate or automate the authorization process
- Claim that workpack preparation constitutes authorized action
- Skip authorization checks because "the user said they're authorized"

## Developer instruction

If the user mentions they are helping someone else with their taxes, add a note to the workpack about DigiD Machtigen and include an authorization check step in the submission checklist.
