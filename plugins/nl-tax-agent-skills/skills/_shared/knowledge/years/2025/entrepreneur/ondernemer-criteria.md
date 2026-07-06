# Rule note: Ondernemerschap and urencriterium 2025

source_ids: bd_ondernemer_criteria_2025, bd_ondernemerscheck_2025, bd_urencriterium_2025, law_wet_inkomstenbelasting_2001
workflow: annual_return
tax_year: 2025
status: active
last_reviewed: "2026-07-04"
review_status: reviewed

## Rule

Entrepreneur support in the 2025 annual return covers the IB-ondernemer with an
**eenmanszaak** (sole proprietorship, the usual ZZP legal form) whose profit is
**winst uit onderneming** (afdeling 3.2 Wet IB 2001). Two questions decide which
income category and which deductions apply: (1) is the taxpayer an *ondernemer
voor de inkomstenbelasting*, and (2) do they meet the *urencriterium*. This note
is canonical for both tests; the amounts live in `ondernemersaftrek.md`,
`mkb-winstvrijstelling.md`, `investeringsaftrek.md`, and `winst-en-kosten.md`.

These are reference notes for workpack preparation -- not final tax advice.

## Three box 1 labour-income sources

For the inkomstenbelasting, work income falls into one of three sources, decided
per activity on the facts:

- **Winst uit onderneming** (afdeling 3.2) -- the taxpayer runs an onderneming
  and is an ondernemer. Gives access to ondernemersaftrek, MKB-winstvrijstelling,
  and investeringsaftrek.
- **Loon uit dienstbetrekking** (afdeling 3.3) -- employment; test this first.
- **Resultaat uit overige werkzaamheden** (afdeling 3.4, art. 3.90) -- the
  residual category for work that is neither belastbare winst nor belastbaar
  loon. Costs are computed the same way as for winst, but there is **no**
  ondernemersaftrek, no MKB-winstvrijstelling, and no investeringsaftrek.

Only winst uit onderneming is prepared as a standard entrepreneur case. Route
resultaat uit overige werkzaamheden to manual review (see `winst-en-kosten.md`).

## Ondernemer voor de inkomstenbelasting (art. 3.4 / 3.5)

The Belastingdienst weighs the whole of the circumstances -- no single factor is
decisive:

- **Winst** -- does the activity make (sufficient) profit; only a very small
  profit or structural losses points away from an onderneming.
- **Zelfstandigheid** -- if others determine how the work is organised and
  performed, independence is lacking.
- **Kapitaal** -- investment in equipment, advertising, staff, insurance.
- **Tijd** -- the hours spent must be capable of yielding a return.
- **Opdrachtgevers** -- several clients reduce dependence and raise independence.
- **Bekendheid naar buiten** -- advertising, website, social media, signage.
- **Ondernemersrisico** -- debtor/payment risk, dependence on supply and demand.
- **Aansprakelijkheid** for the debts of the enterprise.

A KvK registration on its own does NOT make someone an ondernemer for the
inkomstenbelasting, and being an ondernemer for the btw does not automatically
make someone an ondernemer for the inkomstenbelasting. The official
**OndernemersCheck** gives an indication only, not a binding ruling.

## Urencriterium (art. 3.6)

Most ondernemersaftrek components require the urencriterium. Two conditions:

- **At least 1,225 hours** per calendar year spent on work for one or more
  ondernemingen from which the taxpayer enjoys profit as ondernemer. The 1,225
  hours apply per calendar year with no pro-rata reduction for starting
  mid-year.
- **Grotendeels-criterium** -- more than 50% of total working time (onderneming
  plus employment plus overige werkzaamheden) must go to the onderneming(en).

**Starter exception:** the grotendeels-criterium does not apply if the taxpayer
was not an ondernemer in one or more of the five preceding calendar years (for
2025: not an ondernemer in one of 2020-2024). The 1,225-hours requirement itself
always remains.

**Which hours count:** all hours spent on the onderneming, including indirect
hours (making offertes, doing the administratie, building the business website)
-- not only billable hours. Hours in which the taxpayer is merely available
without performing work do not count. The taxpayer must be able to make the
hours plausible (agenda, offertes, urenbriefjes, facturen) if the inspecteur
asks; there is no hours log submitted with the return.

**Pregnancy:** hours during the period matching the employee zwangerschaps- en
bevallingsverlof (16 weeks in total) are treated as worked hours.

**Verlaagd urencriterium:** the same test with 1,225 hours replaced by **800
hours**. It is relevant only for the startersaftrek bij arbeidsongeschiktheid
(see `ondernemersaftrek.md`).

**Ongebruikelijk samenwerkingsverband:** hours for an onderneming in a
samenwerkingsverband with verbonden personen do not count when the taxpayer's
work is hoofdzakelijk (70% or more) of a supporting nature and such a
samenwerkingsverband between non-related persons would be unusual. This is a
partnership complication -- route it to manual review.

## Developer instruction

1. Establish ondernemer status before preparing any winst section. If the case
   is not clearly an eenmanszaak/ZZP with winst uit onderneming, or if the
   activity looks like resultaat uit overige werkzaamheden, record the facts and
   route to manual review instead of calculating.
2. Record whether the urencriterium (or the verlaagd urencriterium) is met as a
   yes/no fact in the workpack; it gates the zelfstandigenaftrek and related
   deductions in `ondernemersaftrek.md`. Do not compute an hours figure or infer
   it from age; ask the taxpayer.
3. Partnerships (VOF, maatschap, CV), medegerechtigdheid, DGA/BV profit,
   agrarische ondernemingen, and zeevarenden are out of standard scope -- route
   to manual review.
