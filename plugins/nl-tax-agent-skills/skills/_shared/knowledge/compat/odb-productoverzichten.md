# Rule note: ODB product overview (future reference only)

source_id: odb_topics_streams
workflow: all
tax_year: all
status: active
last_reviewed: "2026-04-30"
review_status: reviewed

## Rule

The ODB product overview lists all message types (berichtstromen) available for software developers integrating with the Belastingdienst. This project does NOT use these streams in v1 -- this file exists so future developers know where to look when adding electronic filing.

## Relevant streams for this project (future)

### IH aangifte -- income tax return submission

- Berichtstroom for submitting a completed inkomstenbelasting return
- Defines the full XML schema for all income tax fields
- Includes validation rules that mirror the Belastingdienst's own intake checks
- Submission triggers the formal assessment process (definitieve aanslag)

### VIA -- pre-filled return data retrieval

- Berichtstroom for retrieving vooringevulde aangifte data
- Returns data the Belastingdienst already holds: employer annual statements (jaaropgaven), bank interest reports, WOZ values, healthcare insurance data
- Data is per taxpayer per tax year
- Useful for pre-populating workpacks and reducing manual input errors

### VA -- voorlopige aanslag request/change

- Berichtstroom for requesting or changing a provisional assessment
- Allows electronic submission of the same data a taxpayer would enter on the Belastingdienst portal
- Relevant for the provisional-assessment skill if electronic filing is added

## Stream characteristics

Each berichtstroom has:

- Its own XML schema (XSD) defining allowed elements and data types
- Validation rules (schematron or business rules) that must pass before the message is accepted
- Version numbering tied to the tax year and filing season
- Test endpoints in the ODB pre-production environment

## v1 scope

- v1 does NOT use these streams
- Workpacks are designed for manual entry in the Belastingdienst online portal
- No XML generation, no Digipoort transport, no VIA retrieval

## Developer instruction

This file is a reference map for future development. When the project adds electronic filing:

1. Start with the IH aangifte stream -- it is the most directly relevant
2. VIA retrieval would be the highest-value addition for user experience (less manual data entry)
3. VA stream is relevant only if the provisional-assessment skill moves to electronic submission
4. Obtain current XSD schemas from ODB before starting any integration work -- schemas are versioned per tax year
5. Use the ODB pre-production environment for all testing

Do not reference these streams in v1 skill logic. They are documented here purely for architectural awareness.

## Common failure

Do not assume ODB schemas are stable across tax years. Each year may bring schema changes reflecting legislative amendments. Always verify the current schema version before starting integration work for a new tax year.
