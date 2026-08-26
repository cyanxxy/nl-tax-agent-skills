# Rule note: Ondernemerschap and urencriterium 2025

source_ids: bd_ondernemer_criteria_2025, bd_ondernemerscheck_2025, bd_urencriterium_2025, law_wet_inkomstenbelasting_2001
workflow: annual_return
tax_year: 2025
status: active
last_reviewed: "2026-08-15"
review_status: reviewed

## Rule

Entrepreneur support in the 2025 annual return covers the IB-ondernemer with an
**eenmanszaak** (sole proprietorship, the usual ZZP legal form) whose profit is
**winst uit onderneming** (afdeling 3.2 Wet IB 2001). Two questions decide which
income category and which deductions apply: (1) is the taxpayer an *ondernemer
voor de inkomstenbelasting*, and (2) do they meet the *urencriterium*. This note
is canonical for both tests; the amounts live in `ondernemersaftrek.md`,
`mkb-winstvrijstelling.md`, `investeringsaftrek.md`, and `winst-en-kosten.md`.
One screen runs even earlier than the ondernemer test -- the bron van inkomen
gate below, for which `row-en-dba-2025.md` is canonical. The order of the
computation that follows these tests is in `winstberekening-2025.md`.

These are reference notes for workpack preparation -- not final tax advice.

## Step 0 -- bron van inkomen, before either test

An activity only produces box 1 income at all if it is a **bron van inkomen**.
Three conditions apply: the taxpayer takes part in het economisch verkeer
(the activity is performed for a vergoeding, outside the private sphere), a
voordeel is reasonably to be expected from the activity, and the taxpayer intends
to make a voordeel -- this third condition weighs least.

There is **no** bron van inkomen when:

- the activity sits in the **hobbysfeer or the familiesfeer**; or
- the outlook is mainly losses, and those losses are structural and expected to
  stay that way.

**The consequence cuts both ways, and both halves must reach the taxpayer:** no
income tax is due on the activity, **and** its costs and losses are not
deductible. A taxpayer who hears only the first half will accept the verdict
happily and then be surprised that a loss-making year yields nothing.

The screen runs **per activity**; separate activities form one bron only where
there is sufficient connection between them. Work done for family or friends
against no more than a reimbursement of the expenses incurred does not have to be
declared.

This verdict is never the agent's to assert. Run the screen as questions, record
the taxpayer's answers and the reasoning in the workpack, and present the outcome
as something the taxpayer confirms or disputes. If the answers point away from a
bron van inkomen, surface the finding and route it to manual review -- do not
silently drop either the income or the costs from the return.
`row-en-dba-2025.md` is canonical for this pre-screen and carries the official
wording.

## Three box 1 labour-income sources

Once the activity is a bron van inkomen, work income falls into exactly one of
three sources for the inkomstenbelasting, decided per activity on the facts.
Test loon first: a dienstbetrekking excludes the other two for that activity.

- **Winst uit onderneming** (afdeling 3.2) -- the taxpayer runs an onderneming
  and is an ondernemer. Gives access to ondernemersaftrek, MKB-winstvrijstelling,
  and investeringsaftrek.
- **Loon uit dienstbetrekking** (afdeling 3.3) -- employment; test this first.
- **Resultaat uit overige werkzaamheden** (afdeling 3.4, art. 3.90) -- the
  residual category for work that is neither belastbare winst nor belastbaar
  loon. Costs are computed the same way as for winst, but there is **no**
  ondernemersaftrek, no MKB-winstvrijstelling, and no investeringsaftrek.

Winst uit onderneming is the standard entrepreneur case, prepared with the cost
rules in `winst-en-kosten.md`. **Resultaat uit overige werkzaamheden is a
prepared path of its own, not a dead end:** `row-en-dba-2025.md` carries the full
route -- income minus costs under art. 3.95 lid 1, the categories with their own
2025 limits, the bijdrage Zvw, where the resultaat is reported, and the
fiscal-partner allocation. Route such a case there rather than stopping at manual
review.

What does stay a manual-review decision is the **borderline call itself**: which
of the three sources an activity belongs to when the facts point both ways. The
eight criteria below are weighed as a whole, no single one decides, and no
scoring rule or threshold is published. Collect the facts against each criterion,
state what each outcome costs in money terms, and ask -- the agent does not rule.

Not being an ondernemer does not make the income untaxed. It moves to resultaat
uit overige werkzaamheden; it does not disappear.

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
  ondernemingen from which the taxpayer enjoys profit as ondernemer. **The 1,225
  hours are absolute and are never pro-rated for a mid-year start.** The
  Belastingdienst states it plainly -- "U mag niet de 1.225 uren herrekenen naar
  de periode dat u ondernemer bent" -- and its worked example is an enterprise
  started on 1 July, which still needs the full 1,225 hours in that calendar
  year. Art. 3.6 lid 1 contains no apportionment for a partial first year. This
  is the most common starter misconception; correct it before presenting any
  zelfstandigenaftrek. The threshold is measured over all of the taxpayer's
  ondernemingen together. See `aanloopfase-en-starters-2025.md` for the first
  partial year, including hours worked on the enterprise before registration.
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
samenwerkingsverband between non-related persons would be unusual. Both limbs
must be met. `samenwerkingsverband-2025.md` carries the two-part test and its
all-or-nothing consequence -- recognise and record the form there, then route the
decision itself to manual review.

## Developer instruction

1. Run the bron van inkomen screen first, as questions, and record the answers.
   If the activity looks like hobbysfeer, familiesfeer, or a structural loss with
   no prospect of a voordeel, say both halves of the consequence out loud (no tax
   on the income, no deduction for the costs) and route to manual review. Read
   `row-en-dba-2025.md` before running it.
2. Establish ondernemer status before preparing any winst section. If the case is
   not clearly an eenmanszaak/ZZP with winst uit onderneming, collect the facts
   against the eight criteria and ask; do not rule. If the activity is resultaat
   uit overige werkzaamheden, prepare it along `row-en-dba-2025.md` -- that is a
   real path, not a refusal.
3. Record whether the urencriterium (or the verlaagd urencriterium) is met as a
   yes/no fact in the workpack; it gates the zelfstandigenaftrek and related
   deductions in `ondernemersaftrek.md`. Do not compute an hours figure, infer it
   from age, or scale it down for a mid-year start; ask the taxpayer, and where
   the answer is not established say so rather than entering a number.
4. Where any samenwerkingsverband, medegerechtigdheid, or terbeschikkingstelling
   is in play -- vof, maatschap, cv, man-vrouwfirma, stille vennoot,
   profit-sharing geldverstrekker -- use the recognition table in
   `samenwerkingsverband-2025.md` to name the form, note what it does to the
   ondernemer tests and which reliefs fall away, then route the computation to
   manual review. Name the form and the next step; do not dead-end the taxpayer.
5. DGA/BV profit, agrarische ondernemingen, and zeevarenden stay out of standard
   scope -- record the facts and route to manual review.
6. Once both tests are settled, follow `winstberekening-2025.md` for the order in
   which the figures are combined.
