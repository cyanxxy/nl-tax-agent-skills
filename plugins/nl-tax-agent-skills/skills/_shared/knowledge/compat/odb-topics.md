# Rule note: ODB compatibility awareness (future only, not v1)

source_id: odb_service_developers
workflow: all
tax_year: all
status: active
last_reviewed: "2026-04-30"
review_status: reviewed

## Rule

ODB (Omgevingsloket Data Belastingdienst) is the developer service portal operated by the Dutch Tax and Customs Administration. It provides technical specifications for software developers building tax filing software. This project does NOT implement ODB integration in v1, but this file exists for future compatibility awareness.

## What ODB provides

ODB offers technical documentation and specifications for:

- Electronic submission of tax returns and other messages to the Belastingdienst
- Retrieval of pre-filled return data (vooringevulde aangifte)
- Validation rules for electronic messages
- Test environments for software developers

## Relevant message types

### IH (Inkomstenbelasting)

- The message type for income tax returns
- Defines the XML schema for submitting a completed income tax return electronically
- Includes all fields, validations, and business rules that the Belastingdienst applies on receipt

### VIA (Vooringevulde Aangifte)

- The message type for retrieving pre-filled return data
- Allows authorized software to retrieve data the Belastingdienst already holds about a taxpayer (employer statements, bank interest reports, WOZ values)
- Requires proper authorization (DigiD Machtigen or beconnummer)

## Transport layer: Digipoort

- Digipoort is the government-wide transport infrastructure for electronic messages
- All ODB message exchanges go through Digipoort
- Requires PKIoverheid certificates for authentication
- Implements MSH (Message Service Handler) protocol

## v1 scope

- v1 does NOT implement ODB or Digipoort integration
- v1 produces workpacks for manual entry by the taxpayer in the Belastingdienst portal
- No electronic filing, no VIA retrieval, no Digipoort communication

## Developer instruction

This file exists for future reference only. When the project later adds electronic filing:

1. ODB specifications would define the XML message format for the IH berichtstroom
2. VIA retrieval could pre-populate taxpayer data, reducing manual input
3. Digipoort integration would require PKIoverheid certificates and MSH protocol handling
4. The field-mapper skill would need to map workpack fields to ODB XML elements

Do not build toward ODB compatibility in v1. Focus on producing correct, complete workpacks for manual entry.

## Common failure

Do not attempt to generate ODB-compatible XML in v1. The workpack format is designed for human readability and manual entry, not for electronic submission. Attempting to dual-purpose it will compromise both goals.
