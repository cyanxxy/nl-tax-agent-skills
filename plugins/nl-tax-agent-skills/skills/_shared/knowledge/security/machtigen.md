# Rule note: Authorization and representation (Machtigen)

source_id: bd_machtigen_authorization
workflow: all
tax_year: all
status: active
last_reviewed: "2026-04-30"
review_status: reviewed

## Rule

When someone other than the taxpayer is preparing or submitting a tax return or voorlopige aanslag, proper authorization must be in place through official channels.

## Authorization routes

### Representative authorization

- A taxpayer can authorize another person to handle tax matters on their behalf
- This is done through the official authorization service
- The authorization must be set up BEFORE the representative can act
- Skills may include an authorization check but must not automate it

### Bewindvoerder / Curator
- Court-appointed administrators have separate authorization procedures
- These are outside v1 scope — route to professional advice

### Belastingconsulent / Adviseur
- Tax advisers typically use their own professional authorization
- This is handled through the Belastingdienst's intermediary portal
- Outside v1 scope for automation — route to their professional workflow

## What skills may do

- Inform the user that official authorization may be required
- Explain that authorization must happen through official channels
- Include "check authorization" as a step in submission checklists
- Note in the workpack when a representative scenario is detected

## What skills must NOT do

- Collect or store authorization credentials
- Simulate or automate the authorization process
- Claim that workpack preparation constitutes authorized action
- Skip authorization checks because "the user said they're authorized"

## Developer instruction

If the user mentions they are helping someone else with their taxes, include an authorization check step in the submission checklist.
