# Rule note: Entrepreneur aangifte and evidence 2025

source_ids: bd_aangifte_ondernemers_2025, bd_ondernemer_cijfers_aangifte_2025, bd_ondernemer_voorbereiden_2025, bd_hoe_aangifte_doen_online_app_papier, bd_ib_aangifte_voor_ondernemers, bd_becon_uitstel_fiscaal_dienstverleners
workflow: annual_return
tax_year: 2025
status: active
last_reviewed: "2026-08-15"
review_status: reviewed

## Rule

An IB-ondernemer reports winst uit onderneming inside the ordinary aangifte
inkomstenbelasting. This note is canonical for how the entrepreneur return is
filed, which portal and channel are used, which deadline and uitstel route apply,
and which evidence the workpack should collect. The rubriek-by-rubriek inventory
of the zakelijk deel -- which lines exist in the winst-en-verliesrekening, which
lines exist on each side of the balans, which questions the form asks, and which
figures the aangifte computes rather than accepts -- is canonical in
`zakelijke-schema-2025.md`. Use that note as the checklist of what must be ready
before entry; use this note for channel, deadlines and evidence.

These are reference notes for workpack preparation -- not final tax advice.

## Portal and channel

- The aangifte inkomstenbelasting -- including the winst-uit-onderneming section
  -- is filed on **Mijn Belastingdienst** (mijn.belastingdienst.nl), the same
  particulieren portal used for a private return. Mijn Belastingdienst Zakelijk
  is for business taxes such as btw and loonheffingen, NOT for the income-tax
  return.
- **Online only.** Ondernemers must file **online**. A private taxpayer has three
  channels -- online, the aangifte-app, and paper -- and for an ondernemer two of
  them are closed: the aangifte-app is not available when the taxpayer had an
  onderneming, and the paper form is not available either. Within "online" the
  routes are Mijn Belastingdienst, fiscale software, or a fiscaal intermediair.
  State the rule as a rule; do not present the app as a fallback if the portal
  feels hard.
- **One exception, and only one.** An ondernemer in the Netherlands who lives
  abroad may also file on paper, on the **Aangifte C** form. Paper forms cannot be
  downloaded; you (the taxpayer) order one from the Belastingdienst. Raise this
  exception only after the taxpayer confirms they live outside the Netherlands --
  otherwise state the online-only rule without it.
- **The zakelijk deel is never prefilled.** State this to the taxpayer as a rule,
  not as a caveat. The vooraf ingevulde aangifte fills only the **privedeel**.
  The zakelijk deel -- the balans, the winst-en-verliesrekening, the
  ondernemersaftrek and the urencriterium answer -- arrives empty every year, and
  you (the taxpayer) enter every figure in it yourself. A taxpayer who expects the
  business figures to appear on their own will under-prepare, so say it before the
  workpack is built and use `zakelijke-schema-2025.md` as the inventory of what
  has to be ready.
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

That is the outline only. `zakelijke-schema-2025.md` is the canonical rubriek
inventory for the zakelijk deel: the individual opbrengsten, kosten, activa and
passiva lines, the entrepreneur questions the form asks, the priveonttrekkingen
and -stortingen, and the fields the same fact has to appear in twice. Present it
as a checklist -- the left-to-right screen order of the winstaangifte is not
published, so never present the rubrieken to the taxpayer as a numbered wizard
sequence.

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

### Becon-uitstel through a fiscal adviser

Becon-uitstel is a **distinct route**, not a longer version of the taxpayer's own
uitstel request. Ask early whether a fiscal adviser files the return, because the
answer decides which route the deadline conversation belongs to:

- The request is made by the adviser, not by the taxpayer. It requires a
  beconnummer and a PKI-certificaat in the adviser's own name, so a taxpayer
  without an adviser cannot use this route at all.
- After approval the uitstel runs to and including **30 April of the following
  year**, on condition that the adviser keeps to an inleverschema and files the
  client returns in batches across the uitstel period rather than at the end.
  The official wording gives that endpoint as a relative date and does not fix
  which calendar year it lands on for the 2025 return. Do not convert it into a
  specific date yourself: quote the rule and have the adviser confirm the actual
  uitsteldatum.
- The adviser, not the taxpayer, tracks progress against that inleverschema.
- An aanvullend-uitstel route exists on top of becon-uitstel, with its own request
  window and its own granted period. Those dates are not established for this
  return in the sources this note relies on: ask the adviser to confirm the
  uitsteldatum that actually applies, and never state an aanvullend-uitstel date
  to the taxpayer.
- Becon-uitstel changes the filing date, not the interest position. Uitstel of any
  kind postpones filing; belastingrente is still due over the period the aanslag
  is outstanding -- see `../annual/late-filing.md`.

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
4. State the online-only rule when the channel first comes up, and do not offer
   the aangifte-app or a paper form as an alternative. Raise the Aangifte C paper
   exception only after the taxpayer confirms they live outside the Netherlands.
5. State the never-prefilled rule before collecting figures: the vooraf ingevulde
   aangifte fills the privedeel only, and the taxpayer types the whole zakelijk
   deel. Do not let a workpack rest on figures the taxpayer expects to be
   prefilled.
6. Ask whether a fiscal adviser files the return. If yes, the deadline question is
   a becon-uitstel question and the adviser confirms the uitsteldatum -- do not
   apply the taxpayer's own 1 May 2026 request route to an adviser-filed return,
   and do not state an aanvullend-uitstel date.
7. Use `zakelijke-schema-2025.md` as the rubriek inventory when building the
   zakelijk deel, and present it as a checklist rather than a screen order.
