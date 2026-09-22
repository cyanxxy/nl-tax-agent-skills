# Rule note: Winst uit onderneming in the voorlopige aanslag 2026

source_ids: ola_va2026_schatting_winst, ola_va2026_winst_als_ondernemer, bd_provisional_check_and_change_2026, bd_provisional_annual_renewal, bd_provisional_change_2026, bd_provisional_stopzetten_2026, bd_zelfstandigenaftrek_2026, bd_mkb_winstvrijstelling_2026, bd_tariefsaanpassing_aftrekposten, bd_privevervoermiddel_2026, bd_fisin2026_h8, bd_belastingrente_pay_ib, bd_belastingrente_percentages
workflow: provisional_assessment
tax_year: 2026
status: active
last_reviewed: "2026-08-15"
review_status: reviewed

## Rule

This note is canonical for the meaning of the single supported business field in
the 2026 voorlopige aanslag, `onderneming.geschatte_winst`, and for everything an
ondernemer needs in order to produce, sanity-check, and later correct that one
figure. It sits alongside `request-flow.md` and `change-flow.md` (which own the
subflow mechanics), `stopzetten-flow.md` (which owns the stop route),
`rates-and-credits.md` (which owns the 2026 box 1 brackets and heffingskortingen),
`review-flow.md`, and `vva-eva-baseline-delta.md`. It never produces a final tax
amount and it never produces annual accounts.

These are reference notes for workpack preparation -- not final tax advice.

## The one figure the form asks for

The Belastingdienst invulhulp for the "Winst als ondernemer" screen of the
Voorlopige aanslag 2026 form states the requested amount verbatim:

> "Maak een schatting van de winst die u als ondernemer behaalt in 2026. Het gaat
> hier om de winst voor ondernemersaftrek en de mkb-winstvrijstelling."

and, on the same screen:

> "Maak de schatting exclusief de btw die u moet afdragen en exclusief de btw die
> u kunt terugvragen."

That fixes the semantic of `onderneming.geschatte_winst` exactly:

| Property of the field | Value |
|---|---|
| What is estimated | The profit the taxpayer expects to earn as ondernemer in 2026 |
| Position in the chain | BEFORE the ondernemersaftrek and BEFORE the mkb-winstvrijstelling |
| Btw treatment | Excluding btw payable and excluding btw reclaimable |
| Expected loss | Entered as a negative amount, with a minus sign |
| Number of business figures on the form | One |

Do not reduce the estimate by the zelfstandigenaftrek, the startersaftrek, the
mkb-winstvrijstelling, or any other ondernemersfaciliteit before entering it. An
estimate that has already been reduced by those items is too low, and the
Belastingdienst will then apply them a second time.

### What the invulhulp says the estimate must take into account

The same invulhulp lists the items to take into account when making the estimate
(rendered here in plain ASCII):

- stakingswinst
- woningforfait for privegebruik of a woning
- privegebruik auto
- privegebruik van goederen
- vrijgestelde winstbestanddelen
- (willekeurige) afschrijving
- investeringsaftrek
- arbeidsbeloning aan de fiscale partner
- kosten die een zakelijk en een prive karakter hebben

Ask the taxpayer about each item that plausibly applies to them. Do not assume
an item is nil because the taxpayer did not mention it, and do not compute
stakingswinst -- see the manual-review boundaries below.

## What the voorlopige aanslag 2026 does NOT contain for an ondernemer

| Not on the form | Consequence |
|---|---|
| Balans (activa and passiva) | Never prepare or request one for this flow |
| Winst-en-verliesrekening | Never prepare or request one for this flow |
| An amount field for the ondernemersaftrek | The taxpayer types no deduction amount |
| An amount field for the mkb-winstvrijstelling | The taxpayer types no exemption amount |

The taxpayer supplies the one estimate; the Belastingdienst applies the
ondernemersaftrek and the mkb-winstvrijstelling itself when it calculates the
voorlopige aanslag. The form's help text describes the mkb-winstvrijstelling as
"een aftrekpost op uw winst als ondernemer na toepassing van de
ondernemersaftrek", which is consistent with that division of work.

The form does ask **eligibility questions** around the ondernemersaftrek. The
in-form help sets out the three conditions for having winst uit onderneming at
all: the onderneming is run for the taxpayer's account, the taxpayer can make
binding agreements for it, and the taxpayer is hoofdelijk aansprakelijk for its
debts. It also records that a medegerechtigde or geldverstrekker receives neither
ondernemersaftrek nor mkb-winstvrijstelling. Answer those questions from facts
the taxpayer confirms, never from an inference.

## 2026 sanity-check figures -- explanation and plausibility only

The figures below exist so the agent can explain to the taxpayer what the
Belastingdienst will do with the estimate, and so it can notice an estimate or a
rolled-forward amount that cannot be right. **None of these figures is entered on
the form, and none of them is subtracted from `onderneming.geschatte_winst`.**

| Item | 2026 value |
|---|---|
| Zelfstandigenaftrek | EUR 1,200 |
| Zelfstandigenaftrek, AOW-leeftijd reached at the start of the calendar year | EUR 600 |
| Startersaftrek (an increase of the zelfstandigenaftrek) | EUR 2,123 |
| Mkb-winstvrijstelling | 12.7% of the winst after the ondernemersaftrek |
| Tariefsaanpassing percentage | 11.94% |
| Maximum rate at which the covered deductions give relief | 37.56% |
| Income threshold above which the tariefsaanpassing applies | EUR 78,426 |
| Per-kilometre deduction for business kilometres in a prive-vervoermiddel | EUR 0.25 |

Notes on these rows:

- The zelfstandigenaftrek cannot exceed the winst before ondernemersaftrek,
  unless the taxpayer is entitled to the startersaftrek. An unused part is fixed
  by beschikking and can be settled in the following 9 years.
- The tariefsaanpassing threshold is compared with box 1 income excluding
  deductions. It covers the zelfstandigenaftrek, the aftrek speur- en
  ontwikkelingswerk, the meewerkaftrek, the startersaftrek bij
  arbeidsongeschiktheid, the stakingsaftrek, and the mkb-winstvrijstelling. The
  Belastingdienst calculates the reduction itself.
- The per-kilometre amount for a privately owned or privately rented vehicle
  (car, motorcycle, or bicycle) is EUR 0.25 for 2026, and fuel, insurance, tolls
  and parking are already inside it -- they cannot be deducted separately. The
  consolidated statute text as read on 21 February 2026 has not yet been brought
  into line with the Belastingdienst pages on this amount; the Belastingdienst
  2026 page governs. Recheck this figure before the 2026 season.
- Box 1 brackets and heffingskortingen for 2026 live in `rates-and-credits.md`.
  Read them there; do not restate them here.

## THE ROLLOVER TRAP

This is the highest-value check in the whole business path of the provisional
flow, and the agent must perform it explicitly.

**How a stale estimate arrives.** A taxpayer who already had a voorlopige
aanslag does not have to request a new one: "We verlengen uw voorlopige aanslag
automatisch voor het nieuwe jaar." A taxpayer who requests or changes one online
may also let the Belastingdienst pre-fill data from an earlier return, with the
Belastingdienst's own caveat "Controleer dus goed wat er al staat." Either way
the resulting 2026 figures rest on an earlier year, and the Belastingdienst
describes the voorlopige aanslag itself as "altijd een schatting" that stops
being right once the situation changes. None of the official pages states that a
carried-over business estimate is recalculated for the new year's
ondernemersaftrek.

**Why that matters so much for 2026.** The zelfstandigenaftrek has been running
down hard:

| Tax year | Zelfstandigenaftrek |
|---|---|
| 2025 | EUR 2,470 |
| 2026 | EUR 1,200 |

Both amounts are official. What the reviewed sources establish is that an
automatically generated voorlopige aanslag 2026 is built from an earlier year's
**income data**, and that the Belastingdienst calls a voorlopige aanslag an
estimate that stops being right once the situation changes. They do **not**
establish which year's zelfstandigenaftrek the 2026 calculation applies, so do
not tell the taxpayer their assessment carries an old deduction.

The supportable risk is the input, not the rate: a 2026 assessment resting on an
older year's profit can be materially wrong for 2026 on its own, and the sharp
year-on-year fall in the zelfstandigenaftrek means the tax on a given profit is
higher in 2026 than the same profit produced in 2025. Both push the same way --
an untouched rolled-forward assessment is likely to collect too little -- so the
estimate is worth reviewing. Frame it as a check, never as a finding about how
the Belastingdienst calculated the assessment.

**The check.** For every taxpayer whose 2026 voorlopige aanslag was extended
automatically or opened pre-filled, ask:

1. Which year's figures does the current voorlopige aanslag 2026 rest on?
2. What profit estimate does the current voorlopige aanslag 2026 use, and is it
   still the taxpayer's own best estimate for 2026?
3. Does the taxpayer's own reasoning about the amount still use a
   zelfstandigenaftrek from an earlier year?

Record the answers as facts with provenance. If the taxpayer cannot answer, say
so in the workpack as an open question -- never fill the gap with an assumption
and never enter a zero.

**One further carry-over rule.** A change made to the voorlopige aanslag 2025
after 15 October 2025 is not carried into 2026 automatically. If the taxpayer
made a late 2025 correction, the 2026 estimate must be re-derived from the
taxpayer's own current forecast rather than assumed to have followed.

## A voorlopige aanslag does not prevent belastingrente

The Belastingdienst page on paying belastingrente for the inkomstenbelasting
contains no rule under which holding a voorlopige aanslag prevents belastingrente
on the income tax. That mechanism exists for other taxes, not for the
inkomstenbelasting. What the reviewed sources do state:

- Belastingrente on the inkomstenbelasting runs from 1 July following the tax
  year, and filing extension does not move that start date.
- The belastingrente percentage for the inkomstenbelasting is 5% from
  1 January 2026.

So the honest framing for the taxpayer is: a well-estimated voorlopige aanslag
spreads the payment and avoids a single large final bill, and it reduces the
amount that could later carry interest -- but it is not an interest shield. Do
not tell the taxpayer that requesting or changing a voorlopige aanslag stops
belastingrente on the income tax.

## When the actual profit turns out very different from the estimate

The Belastingdienst names the ondernemer with fluctuating results explicitly and
points at the same screen: "Voorkom dat u straks belasting moet bijbetalen en
wijzig uw voorlopige aanslag. Doe dat in het scherm Winst uit onderneming. Maak
de schatting op basis van uw winst." Cessation during the year is named as a
second trigger, entered through the same screen. Changing is not compulsory:
"Wijzigen is niet verplicht, maar zo voorkomt u verrassingen."

### Choosing between wijzigen and stopzetten

| The taxpayer currently ... | Route |
|---|---|
| PAYS a monthly amount and the amount is wrong | **Change** the voorlopige aanslag. Stopzetten is not available |
| RECEIVES a monthly refund and no longer wants (part of) it | Stopzetten is available -- see `stopzetten-flow.md` |
| RECEIVES a monthly refund but the amount is simply wrong | **Change** the voorlopige aanslag |

Stopzetten is available only where the taxpayer receives a monthly refund. For an
ondernemer whose profit is coming in higher than the estimate, the monthly amount
is usually one the taxpayer pays, so the change route is the correct one, and
stopzetten must not be offered. Simply ceasing to pay is not a correction: the
existing beschikking still stands, so the amounts remain due and arrears can
build up. Do not present a later annual lump sum as a certainty either -- the
final position depends on the whole 2026 return.

### The complete-dataset rule on a change

A change to the 2026 voorlopige aanslag is prepared as a complete dataset, not as
a single edited line. See `change-flow.md`, which owns that rule. The business
estimate is one row inside it.

## Manual-review boundaries

Record the facts and route these to manual review; do not compute them in this
flow:

- Stakingswinst and any cessation, transfer, or restructuring of the onderneming.
- Any legal form other than a one-person business run for the taxpayer's own
  account -- vof, maatschap, man-vrouwfirma, and other samenwerkingsverbanden
  remain terminal for this flow.
- The niet-gerealiseerde zelfstandigenaftrek carry-forward.
- Investeringsaftrek amounts and willekeurige afschrijving amounts. The invulhulp
  says to take them into account in the estimate; the taxpayer supplies the
  amount, the plugin does not calculate it.
- The bijdrage Zorgverzekeringswet, which is a separate aanslag with its own
  voorlopige aanslag -- see `zvw-provisional-2026.md`.

## Developer instruction

1. Read this note before asking any business question in a 2026
   provisional request, change, or review. Never restate the field semantic from
   memory: the estimate is the winst BEFORE ondernemersaftrek and BEFORE
   mkb-winstvrijstelling, excluding btw, with a minus sign for a loss.
2. Collect exactly one business figure and record it as
   `onderneming.geschatte_winst` with provenance, the forecast basis, and
   `manual_review_required: true`. Never fold business profit into a generic
   other-income field, and never emit any other `onderneming.*` field.
3. Walk the taxpayer through the invulhulp item list above and ask which items
   apply. If the taxpayer does not know whether an item applies, record it as an
   open question. Never assume an item is nil, and never enter a zero the
   taxpayer has not given you.
4. Do not build a balans or a winst-en-verliesrekening, and do not ask for one.
   The 2026 voorlopige aanslag does not contain them.
5. Do not subtract the zelfstandigenaftrek, startersaftrek, or
   mkb-winstvrijstelling from the estimate. Use the sanity-check table only to
   explain what the Belastingdienst will do and to test whether an amount is
   plausible.
6. Run the rollover check on every taxpayer whose 2026 voorlopige aanslag was
   extended automatically or opened pre-filled: ask which year the figures come
   from, ask for the current estimate, and flag any calculation that still rests
   on a zelfstandigenaftrek above EUR 1,200 (above EUR 600 at AOW-leeftijd). Put
   the finding in the workpack in words the taxpayer can act on.
7. If the taxpayer made a change to the voorlopige aanslag 2025 after
   15 October 2025, ask for the current 2026 figures rather than treating the
   2025 change as carried over.
8. When the taxpayer asks whether a voorlopige aanslag stops belastingrente on
   the income tax, answer no, and explain the 1 July start date and the 5% rate
   from 1 January 2026 instead.
9. Route to the change subflow whenever the taxpayer pays monthly, including when
   they ask to "stop" the aanslag. Offer stopzetten only when the taxpayer
   confirms they receive a monthly refund.
10. Phrase every portal step with an explicit human subject: "You (the taxpayer)
    log in to Mijn Belastingdienst and open the Winst uit onderneming screen."
    This plugin never opens, operates, signs, or sends anything in Mijn
    Belastingdienst, and never asks for DigiD details.
11. Route stakingswinst, samenwerkingsverbanden, and the
    niet-gerealiseerde-zelfstandigenaftrek carry-forward to manual review, and
    say so in the workpack rather than producing a number.
12. This is a 2026 provisional note. Do not import figures, deduction sets, or
    outputs from any other tax year into this flow.
