# Rule note: Entrepreneur aangifte and evidence 2025

source_ids: bd_aangifte_ondernemers_2025, bd_ondernemer_cijfers_aangifte_2025, bd_ondernemer_voorbereiden_2025
workflow: annual_return
tax_year: 2025
status: active
last_reviewed: "2026-07-11"
review_status: reviewed

## Rule

An IB-ondernemer reports winst uit onderneming inside the ordinary aangifte
inkomstenbelasting. This note is canonical for how the entrepreneur return is
filed, which portal is used, and which evidence the workpack should collect.

These are reference notes for workpack preparation -- not final tax advice.

## Portal and channel

- The aangifte inkomstenbelasting -- including the winst-uit-onderneming section
  -- is filed on **Mijn Belastingdienst** (mijn.belastingdienst.nl), the same
  particulieren portal used for a private return. Mijn Belastingdienst Zakelijk
  is for business taxes such as btw and loonheffingen, NOT for the income-tax
  return.
- Ondernemers must file **online**; the aangifte-app is not available when the
  taxpayer had an onderneming. (Only an ondernemer living abroad may also file on
  paper.)
- The vooraf ingevulde aangifte fills only the **privedeel**; the zakelijk deel
  (balans, winst-en-verliesrekening, ondernemersaftrek) is never pre-filled and
  must be entered by the taxpayer.
- This plugin never logs in, signs, or submits. It prepares a workpack for manual
  entry in Mijn Belastingdienst.

## Structure of the winstaangifte

The ondernemer's return has two parts: a **privedeel** and a **zakelijk deel**.
The zakelijk deel requires:

- A **winst-en-verliesrekening** (business income and costs).
- A **balans** (activa: vaste activa, voorraden, vorderingen, liquide middelen;
  passiva: ondernemingsvermogen, voorzieningen, langlopende and kortlopende
  schulden).
- Eligibility answers for the ondernemersaftrek, including the urencriterium
  question, and any bijtelling for private use of a business car.

## Deadlines (2025 return, filed in 2026)

- If an invitation letter (aangiftebrief) exists, use the deadline shown in it
  and determine whether extension was requested through the applicable route.
- With **no invitation**, only when the taxpayer establishes that tax is due,
  use the conditional voluntary-filing guardrail of **14 July 2026**.
  Extension is unavailable on the no-invitation branch.
- For the standard online route, request extension **before 1 May 2026**; a
  granted extension normally adds **4 months**, making the standard extended
  date **1 September 2026**. If the invitation letter shows **another date**,
  request by that letter date using the **official form** route and use the
  granted uitsteldatum.
- Otherwise the deadline is not established: do not invent one and verify the
  position in Mijn Belastingdienst.
- Late filers without uitstel should file as soon as possible; a fiscal adviser
  can arrange becon-uitstel. Belastingrente and a verzuimboete may apply -- see
  `../annual/late-filing.md`.

## Evidence to collect

Collect (never the BSN, which the portal pre-fills):

- Jaarstukken: winst-en-verliesrekening and balans (from the bookkeeping).
- Sales and purchase invoices (facturen) and receipts for business costs.
- Bank jaaroverzicht (interest paid/received and balance at 31 December).
- Investment/purchase invoices for bedrijfsmiddelen (acquisition cost, residual
  value, useful life) for depreciation and investeringsaftrek.
- Urenadministratie supporting the urencriterium.
- Details of a business car used privately, and any AOV premie statement.

Where a boekhoudprogramma is used, the winst-en-verliesrekening and balans are
already available and can be taken over.

## Developer instruction

1. Name Mijn Belastingdienst as the portal for the entrepreneur return; do not
   name Mijn Belastingdienst Zakelijk.
2. Catalogue business evidence via `nl-tax-evidence-indexer`; request the
   jaarstukken, invoices, bank jaaroverzicht, and urenadministratie as gaps when
   missing, rather than assuming zeros.
3. Keep this prep-only: never present the workpack as a filed or final return.
