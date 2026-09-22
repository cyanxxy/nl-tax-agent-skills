# Rule note: Bron van inkomen, resultaat uit overige werkzaamheden en Wet DBA 2025

source_ids: bd_bron_van_inkomen, bd_ondernemer_criteria_2025, bd_ondernemerscheck_2025, bd_weet_wanneer_ondernemer, bd_fisin2025_h6_winst_uit_onderneming, bd_wat_zijn_inkomsten_overig_werk, bd_niet_in_loondienst_werken, bd_welke_kosten_bijverdiensten, bd_fisin2025_row, fisin2025_fiscaal_partnerschap, bd_beperkt_aftrekbare_kosten_2025, bd_zvw_resultaat_overig_werk, bd_wanneer_loondienst, bd_beoordeel_samen, bd_handhaving_arbeidsrelaties, bd_handhavingsplan_landing, bd_geen_nieuwe_modelovereenkomsten, bd_werken_met_modelovereenkomsten, bd_gevolgen_opdrachtnemer, law_wet_inkomstenbelasting_2001
workflow: annual_return
tax_year: 2025
status: active
last_reviewed: "2026-08-15"
review_status: reviewed

## Rule

This note is canonical for the question that comes **before** every other
entrepreneur note: which income category a self-employed person's 2025 income
belongs to, and what happens when the answer is not winst uit onderneming. It
covers the bron van inkomen pre-screen, the split between winst uit onderneming
(afdeling 3.2 Wet IB 2001), loon uit dienstbetrekking (afdeling 3.3) and
resultaat uit overige werkzaamheden (afdeling 3.4, art. 3.90), the full
preparation path for resultaat uit overige werkzaamheden, and an explain-only
account of the Wet DBA and schijnzelfstandigheid. The ondernemer criteria and the
urencriterium themselves stay in `ondernemer-criteria.md`; cost rules stay in
`winst-en-kosten.md`; depreciation and asset labelling stay in
`afschrijving-en-bedrijfsmiddelen-2025.md`; pre-start costs stay in
`aanloopfase-en-starters-2025.md`; the bijdrage Zvw stays in `zvw-2025.md`; the
deductions that only an ondernemer gets stay in `ondernemersaftrek.md`,
`mkb-winstvrijstelling.md` and `investeringsaftrek.md`; the ordered computation
stays in `winstberekening-2025.md`. Where this note and a component note both
mention an amount, the component note is canonical.

These are reference notes for workpack preparation -- not final tax advice.

---

# Part 1 -- Which income category the activity belongs to

## Step 0 -- the bron van inkomen pre-screen (mandatory, runs first)

Before any category question, the activity must be a **bron van inkomen** at all.
The Belastingdienst states three conditions:

| # | Condition | Belastingdienst wording |
|---|-----------|-------------------------|
| 1 | Deelname aan het economisch verkeer | activities performed for a vergoeding **outside the private sphere** |
| 2 | Voordeel is reasonably to be expected from the activities | an objective expectation of gain |
| 3 | The taxpayer also intends to make a voordeel | this intention **counts for less** than condition 2 |

There is **no bron van inkomen** when:

- the activity sits in the **hobbysfeer or de familiesfeer**; or
- the outlook is mainly losses. Where losses are structural and expected to stay
  that way, the Belastingdienst states plainly: "Dan is er geen sprake van een
  bron."

**The consequence cuts both ways.** Where the activities are not a bron van
inkomen, no income tax is due on them **and** the losses and costs cannot be
deducted. Both halves of that sentence must reach the taxpayer. A taxpayer who
hears only the first half will happily accept the verdict and then be surprised
that a loss-making year yields nothing.

Two further points on this screen:

- **Assessment is per activity.** The Belastingdienst assesses each separate
  activity; several activities form one bron only where there is sufficient
  connection between them ("Alleen bij voldoende samenhang kunnen uw
  activiteiten samen 1 bron van inkomen vormen").
- **Reimbursement-only work for family or friends** does not have to be declared
  where the taxpayer receives no more than the expenses they incurred.

**This verdict is never the agent's to assert.** Run the screen as questions,
record the taxpayer's answers and the reasoning in the workpack, and present the
outcome as something the taxpayer confirms or disputes. If the answers point away
from a bron van inkomen, do not silently drop the income or the costs from the
return -- surface the finding and route it to manual review.

## Step 1 -- the three box 1 labour-income sources

For the inkomstenbelasting, income from work falls into exactly one of three
sources, decided per activity on the facts:

| Source | Statutory home | Ondernemersfaciliteiten | Cost deduction | Canonical note |
|--------|----------------|-------------------------|----------------|----------------|
| **Loon uit dienstbetrekking** -- test this first | afdeling 3.3 Wet IB 2001 | none | none, apart from the forfaitaire reisaftrek openbaar vervoer | out of scope for this note |
| **Winst uit onderneming** | afdeling 3.2 Wet IB 2001 | ondernemersaftrek, MKB-winstvrijstelling, investeringsaftrek, fiscale reserves | yes, under goed koopmansgebruik | `winst-en-kosten.md`, `winstberekening-2025.md` |
| **Resultaat uit overige werkzaamheden** -- the residual category | afdeling 3.4, art. 3.90 Wet IB 2001 | **none** | yes, essentially the same rules as winst | Part 2 of this note |

Test order matters. Loon is tested first, because a dienstbetrekking excludes the
other two for that activity. Winst uit onderneming is tested next. Resultaat uit
overige werkzaamheden is what remains: work that is neither belastbare winst nor
belastbaar loon, but which is a bron van inkomen.

**Terminology.** The statute says *resultaat uit overige werkzaamheden*. The
taxpayer-facing Belastingdienst pages say *inkomsten uit overig werk* for the
gross income and *resultaat uit overig werk* for the balance after costs. These
are the same category. Accept whichever wording the taxpayer uses and record it
consistently in the workpack.

**One published bright line exists** for household work: working more than 3 days
per week in the household of the same person makes the income **loon**; 3 days or
fewer makes it **inkomsten uit overig werk**. This is the only numeric bright
line the reviewed 2025 material carries for the loon/resultaat boundary. Every
other boundary case is a weighing of facts.

## Step 2 -- winst uit onderneming: three cumulative requirements

Before the eight criteria are weighed, the Belastingdienst names three
requirements that must all be met for winst uit onderneming:

1. the onderneming is run **for your account** (voor uw rekening);
2. you can **make binding agreements** for the onderneming;
3. you are **hoofdelijk aansprakelijk** for the debts of the onderneming.

## Step 3 -- the eight ondernemer criteria

The Belastingdienst publishes eight assessment points, each phrased as a
question:

| # | Criterion | Belastingdienst question |
|---|-----------|--------------------------|
| 1 | Winst | Maakt u winst? Zo ja, hoeveel? |
| 2 | Zelfstandigheid | Hoe zelfstandig is uw onderneming? |
| 3 | Kapitaal | Beschikt u over kapitaal? |
| 4 | Tijd | Hoeveel tijd steekt u in uw activiteiten? |
| 5 | Opdrachtgevers | Wie zijn uw opdrachtgevers? |
| 6 | Bekendheid naar buiten | Hoe maakt u uw onderneming bekend naar buiten? |
| 7 | Ondernemersrisico | Loopt u ondernemersrisico? |
| 8 | Aansprakelijkheid | Bent u aansprakelijk voor de schulden van uw onderneming? |

The full list of factors and their weights is in `ondernemer-criteria.md`. Three
properties of this test are load-bearing for the agent:

- The criteria are weighed **in onderlinge samenhang** -- as a whole, not one at
  a time.
- The list is **not exhaustive**. The Belastingdienst does not present it as a
  closed set.
- **No single criterion is decisive**, and no scoring rule, weighting or
  threshold is published.

**Therefore: deciding a borderline case is MANUAL REVIEW.** The agent's job is to
surface the eight criteria, collect the taxpayer's facts against each of them,
state the consequences of each outcome in money terms, and ask. The agent does
not rule. Record the facts and the open question in the workpack and route the
decision to the taxpayer or their adviser.

The official **OndernemersCheck** gives an indication of the taxpayer's position
and what it means for the return -- it is not a ruling and it does not bind the
Belastingdienst. It is an interactive tool on belastingdienst.nl. You (the
taxpayer) run it yourself if you want to; this plugin does not run it for you and
does not treat its outcome as a decision.

## What does NOT decide IB-ondernemerschap

Each of these is a common and expensive misreading:

| Fact the taxpayer offers | What it actually establishes |
|--------------------------|------------------------------|
| Registration with the **Kamer van Koophandel** | Nothing for the inkomstenbelasting: "Uw inschrijving bij de Kamer van Koophandel betekent niet dat u ook ondernemer bent voor de inkomstenbelasting." |
| **Btw-ondernemerschap** (an omzetbelastingnummer, btw-aangiften, the KOR) | Only that the taxpayer independently exercises a beroep or bedrijf **for the btw**. The Belastingdienst states the divergence directly: without being an ondernemer for the inkomstenbelasting you can still be one for the btw. |
| **Not being in loondienst** | Only that. The absence of loondienst does not automatically make someone an ondernemer for the inkomstenbelasting or for the btw; that is assessed separately. |
| A **modelovereenkomst** | The employment relationship for the loonheffingen only. See Part 3. |

And the inverse trap: **not being an ondernemer does not make the income
untaxed.** The Belastingdienst states it with its own exclamation mark -- "ook
als u geen ondernemer bent voor de inkomstenbelasting, maar wel winst maakt,
moet u over deze inkomsten belasting betalen!" The income moves to resultaat uit
overige werkzaamheden; it does not disappear.

## Medegerechtigde and other forms outside standard scope

- A **medegerechtigde** (for example a commanditair vennoot) is typically not
  jointly liable and cannot make binding agreements for the onderneming. A
  medegerechtigde or geldverstrekker gets **no ondernemersaftrek and no
  MKB-winstvrijstelling**. Loss recognition for a medegerechtigde is capped at
  the invested capital, measured from 1 January 2001 at the earliest (art. 3.9
  Wet IB 2001).
- Partnerships (vof, maatschap, cv, man-vrouwfirma), DGA/BV profit, agrarische
  ondernemingen and zeevarenden stay outside standard preparation, as
  `ondernemer-criteria.md` already records.

Record the facts for these cases and route them to manual review. Do not
calculate.

---

# Part 2 -- Resultaat uit overige werkzaamheden as a prepared path

Resultaat uit overige werkzaamheden is **not a dead end**. It is a normal box 1
income category with a normal preparation path: gross income minus deductible
costs, reported in the private part of the aangifte inkomstenbelasting, with a
bijdrage Zvw on top. What it lacks is every relief that is reserved for an
ondernemer.

The mechanism is art. 3.95 lid 1 Wet IB 2001: the winstbepalingsregels are
declared applicable to the determination of the resultaat. The
ondernemersfaciliteiten sit **outside** that reference, so they do not carry
over.

## What resultaat uit overige werkzaamheden keeps

- **Cost deduction on the same rules as winst uit onderneming.** The
  Belastingdienst is explicit: "Uw winst wordt op dezelfde manier berekend als
  bij ondernemers", and the cost page addresses people with "winst uit
  onderneming of inkomsten uit overig werk" together. Read `winst-en-kosten.md`
  for the 2025 cost limits; it applies here unchanged except where this note says
  otherwise.
- **Goed koopmansgebruik** as the timing framework.
- **Afschrijving.** Costs above the small-purchase boundary for something used
  longer than one year are spread over the years of use, taking the residual
  value into account. The official pages conflict at **exactly EUR 450**;
  `afschrijving-en-bedrijfsmiddelen-2025.md` keeps that endpoint in manual review.
  The Belastingdienst's own worked example: a professional camera bought for
  EUR 6,000, expected residual value EUR 1,500, used 5 years, gives
  (EUR 6,000 - EUR 1,500) / 5 = **EUR 900 per year**. Read
  `afschrijving-en-bedrijfsmiddelen-2025.md` for the depreciation maxima, the
  gebouwen restrictions and the EUR 450 boundary; that note is canonical.
- **Vermogensetikettering.** The same labelling logic applies before anything is
  depreciated: **10% or less** business use makes the asset compulsorily private,
  **90% or more** makes it compulsorily business, and more than 10% but less than
  90% leaves a choice within reasonable limits.
- **Voorbereidingskosten / aanloopkosten.** Costs made to prepare the work --
  market exploration, obtaining advice -- are deductible where they are business
  costs. `aanloopfase-en-starters-2025.md` covers the mechanics, but note that
  the **starter reliefs** in that note (startersaftrek, startersaftrek bij
  arbeidsongeschiktheid, willekeurige afschrijving voor startende ondernemers)
  all require ondernemerschap or the urencriterium and therefore do **not** apply
  here. Whether any willekeurige afschrijving is available to a taxpayer with
  resultaat uit overige werkzaamheden is not established in the reviewed
  material -- route it to manual review rather than answering it.
- **The drempel for beperkt aftrekbare kosten and the 80% election.** The 2025
  drempel of EUR 5,700 for limited-deductible costs such as representatiekosten
  and certain relatiegeschenken, and the alternative of deducting 80% of those
  costs in the aangifte instead, both apply to people with inkomsten uit overig
  werk as well as to ondernemers. `winst-en-kosten.md` is canonical for the
  drempel.
- **The btw rule for cost amounts.** Deduct costs **excluding** btw where the btw
  is reclaimable in a btw-aangifte; deduct them **including** btw where it is
  not.

## What resultaat uit overige werkzaamheden loses -- and what that costs

| Relief | Available on winst uit onderneming | Available on resultaat uit overige werkzaamheden |
|--------|-----------------------------------|--------------------------------------------------|
| Ondernemersaftrek (zelfstandigenaftrek, startersaftrek, S&O-aftrek, meewerkaftrek, startersaftrek bij arbeidsongeschiktheid, stakingsaftrek) | yes, subject to the urencriterium | **no** |
| MKB-winstvrijstelling | yes, no urencriterium needed | **no** |
| Investeringsaftrek (KIA, EIA, MIA) | yes | **no** |
| Fiscale reserves (herinvesteringsreserve, kostenegalisatiereserve, oudedagsreserve overgangsrecht) | yes | **no** |
| Cost deduction, afschrijving, goed koopmansgebruik | yes | **yes** |

**This is the material consequence of failing the ondernemer test, and it should
be quantified for the taxpayer rather than described.** The shape of the loss on
a profitable year is:

1. the **zelfstandigenaftrek** disappears -- a fixed amount off the base, whose
   2025 value and conditions are canonical in `ondernemersaftrek.md`; plus
2. the **MKB-winstvrijstelling** disappears -- 12.7% of the remaining profit,
   canonical in `mkb-winstvrijstelling.md`; plus
3. any **investeringsaftrek** on assets bought in 2025 disappears, canonical in
   `investeringsaftrek.md`.

The change in taxable income can be shown from those three components, but the
change in tax is **not** that amount multiplied by one marginal box 1 rate.
Bracket crossings, the tariefsaanpassing for entrepreneur deductions, and
income-dependent credits can all change the result. Show the two taxable-income
chains side by side; use the full annual tax-and-credits calculation for any tax
comparison, and label an unresolved comparison for manual review rather than
publishing a single-rate estimate.

The Belastingdienst publishes one worked example of the same loss, in the context
of an assignment that turns out to be loondienst rather than resultaat uit
overige werkzaamheden. It is reproduced in Part 3 below. Use it to illustrate the
mechanism only; **never present its amounts as the taxpayer's own outcome.**

Note also that the **urencriterium is irrelevant** here. It gates reliefs that do
not exist in this category. Do not ask for an hours count in order to decide
resultaat uit overige werkzaamheden, and do not let a failed urencriterium be
mistaken for the reason the reliefs are missing -- the reason is the category.

Two downstream bases behave differently and must not be guessed:

- **Arbeidskorting.** `../annual/credits.md` is canonical and lists resultaat uit
  overige werkzaamheden as arbeidsinkomen; read it there rather than reasoning
  from the winst rule.
- **Lijfrente premiegrondslag.** `inkomensvoorzieningen-2025.md` is canonical and
  lists the **belastbaar resultaat uit overige werkzaamheden** as one of the four
  premiegrondslag components (art. 3.127 lid 3 Wet IB 2001); read the formula,
  the caps and the pension-accrual reduction there rather than reasoning from the
  winst rule. That note is written around an ondernemer, but this component
  applies to a resultaat uit overige werkzaamheden taxpayer whether or not there
  is any winst. Two points specific to this category: the components are taken
  from the **preceding** calendar year, so the 2025 jaarruimte needs the **2024**
  resultaat, never the 2025 figure; and the "before de ondernemersaftrek"
  adjustment is winst-specific -- do not carry it across, because this category
  has no ondernemersaftrek. Ask the taxpayer whether they paid lijfrentepremies
  in 2025 and route only the pension-accrual reduction to manual review, as that
  note directs.

## Special categories with their own 2025 limits

The Belastingdienst lists several kinds of work that produce resultaat uit
overige werkzaamheden and that each have their own subpage: gastouder, artiest or
beroepssporter, kostgangers, huishoudelijke werkzaamheden voor anderen,
pgb-zorg, ter beschikking stellen van bezittingen, and vermogensbeheer that goes
beyond normal management. The 2025 figures the reviewed material establishes:

| Item | 2025 |
|------|------|
| Kostgangers -- exempt part of the rent received | EUR 6,324 per year |
| Vrijwilligersregeling -- rate, 21 and older | EUR 5.60 per hour |
| Vrijwilligersregeling -- rate, under 21 | EUR 3.30 per hour |
| Vrijwilligersregeling -- ceiling per month | EUR 210 |
| Vrijwilligersregeling -- ceiling per calendar year | EUR 2,100 |
| Arbeidsbeloning from a fiscal partner's onderneming -- threshold at which it becomes the partner's inkomsten uit overig werk | EUR 5,000 |

- The arbeidsbeloning threshold works in both directions: at EUR 5,000 or more
  the whole amount is deductible for the paying partner and is inkomsten uit
  overig werk for the receiving partner; below EUR 5,000 it is neither
  deductible nor declared. `ondernemersaftrek.md` carries the same threshold for
  the meewerkaftrek -- keep the two consistent and do not apply both treatments
  to one payment.
- **Terbeschikkingstelling van bezittingen** (art. 3.91 and art. 3.92 Wet IB
  2001) is a separate regime with its own vrijstelling and its own Zvw
  treatment. It is out of scope for this note -- route it to manual review.
- Every other named category (gastouder, artiest, beroepssporter, pgb-zorg,
  vermogensbeheer) has rules this note does not carry. Record the facts and route
  to manual review.

## Bijdrage Zvw over the resultaat uit overig werk

The bijdrage Zorgverzekeringswet applies to resultaat uit overig werk just as it
applies to winst uit onderneming. `zvw-2025.md` is canonical for the percentage,
the maximumbijdrage-inkomen and the shared ceiling; read it there and do not
restate a percentage from memory. The points specific to this category:

- The Belastingdienst states it directly: "Over uw resultaat uit overig werk moet
  u, naast belasting, ook een bijdrage Zorgverzekeringswet (Zvw) betalen", and
  "Over uw resultaat uit overig werk moet u zelf de bijdrage Zvw betalen" where
  the taxpayer also has employment income.
- **Two assessments follow one return.** "Ontvangt u van ons 2 aanslagen: 1
  aanslag voor de inkomstenbelasting/premie volksverzekeringen en een andere voor
  de bijdrage Zvw." There is no separate Zvw form and no separate Zvw entry
  screen, so never create a field-map row asking the taxpayer to type a bijdrage
  Zvw amount.
- The bijdrage is charged on at most the maximumbijdrage-inkomen, and that
  ceiling is shared with any loon that already carried werkgeversheffing Zvw.
  Ask the taxpayer for the "loon Zorgverzekeringswet" on each 2025 jaaropgaaf.
  Never assume there was no loon.
- The base for this category is the **resultaat uit overige werkzaamheden**
  (art. 43 lid 2 onderdeel c Zorgverzekeringswet), from which
  terbeschikkingstelling income is excluded. `zvw-2025.md` carries the exclusion
  and is canonical for it.
- Tell the taxpayer plainly that a second payment obligation follows the return.
  Present the method, never a predicted assessment amount.

## Where the resultaat is reported, and what evidence is needed

- The resultaat is reported in the **private part of the aangifte
  inkomstenbelasting**, under inkomsten uit overig werk. It does **not** go in
  the zakelijk deel: there is no winst-en-verliesrekening and no balans to
  complete, so `zakelijke-schema-2025.md` does not apply to this category.
- The field mapper's identifier for the row is
  `box1.resultaat_overige_werkzaamheden`. The field-map reference under
  `nl-tax-field-mapper/reference/annual-field-map.md` is canonical for the row
  itself.
- No official page publishes the exact on-screen path or the exact screen order
  for this section. **Do not print a click path** and do not present the entry as
  a numbered wizard; present it as a checklist of what has to be ready.
- **Filing channel and deadlines** are the ordinary ones for a private return.
  `entrepreneur-aangifte.md` covers the portal, the channel and the dates; the
  ondernemers-only online-filing constraint in that note is tied to
  ondernemerschap and should not be asserted for this category.
- **No administratieplicht.** The Belastingdienst states "U bent niet verplicht
  om een administratie bij te houden" for inkomsten uit overig werk -- but it can
  ask for information, so receipts and invoices must be kept to prove that the
  costs were incurred and were business costs. A separate btw-administratieplicht
  can still apply where the taxpayer is a btw-ondernemer.
- Evidence to ask the taxpayer for: every invoice or payment statement for the
  income; receipts and invoices for the costs; for each asset used, the purchase
  invoice, the expected useful life, the expected residual value and the share of
  business use; and each 2025 jaaropgaaf if there was also loon.

## Fiscal-partner allocation

Bijverdiensten and income as freelancer, gastouder, artiest or beroepssporter are
on the Belastingdienst's list of items that **may not be divided** between fiscal
partners, alongside loon, uitkering, pensioen and winst uit onderneming.
Resultaat uit het beschikbaar stellen van bezittingen is likewise not divisible.
Do not offer an allocation scenario for this income.

---

# Part 3 -- Wet DBA and schijnzelfstandigheid (EXPLAIN-ONLY)

**This part is explanatory. The plugin never rules on an arbeidsrelatie, never
tells a taxpayer whether an assignment is loondienst, and never contacts an
opdrachtgever.** Its purpose is to make sure the taxpayer understands what the
DBA machinery does and does not decide, so that the wrong conclusion does not
end up in a 2025 return.

## What the joint assessment decides -- and what it does not

- The opdrachtgever and the zzp'er **assess the arbeidsrelatie together**: "U
  beoordeelt samen of er sprake is van loondienst." They are advised to re-check
  regularly, because the way they work together can change over time.
- What is being assessed is the **employment relationship for the
  loonheffingen** -- whether the opdrachtgever must withhold and pay
  loonheffingen, plus the labour-law consequences (continued pay during illness
  and holiday, dismissal rules).
- **It does not decide IB-ondernemerschap.** The Belastingdienst states the point
  in terms: the absence of loondienst does not automatically make the
  opdrachtnemer an ondernemer for the inkomstenbelasting or for the btw -- that
  has to be assessed separately, on the eight criteria in Part 1.
- The Belastingdienst will not judge an individual relationship by phone: "Onze
  medewerkers kunnen u daarop geen antwoord geven", because the facts and
  circumstances cannot be assessed properly over the telephone. The ministry of
  SZW's Webmodule Beoordeling Arbeidsrelatie exists for cases of doubt and is
  aimed at opdrachtgevers.

## The loondienst test, in outline

Three core characteristics must be present -- the **possibility of
werkgeversgezag**, the **obligation to perform (personal) labour**, and
**beloning for the work performed** -- but establishing those three alone is not
enough. All facts and circumstances matter, weighed in their **onderlinge
samenhang**. Factors the Belastingdienst names include: the nature and duration
of the work; how the work and the working hours are determined; the degree to
which the work and the worker are embedded in the opdrachtgever's organisation;
whether the work must be performed personally; how the agreements came about;
how the beloning is determined and paid and how high it is; the degree of
commercial risk; and the degree to which the opdrachtnemer behaves, or can
behave, as an ondernemer.

On gezag the Belastingdienst gives four diagnostic questions -- can the
opdrachtgever determine how, when, where and with whom the work is done; can it
set hours or days per week; does it interfere in collaboration with others; does
it give the same instructions as to its own employees. One or more "yes" is a
strong indication of a gezagsverhouding.

Two further points the agent must not lose:

- Even where there is no loondienst, a **fictieve dienstbetrekking** can still
  apply (gelijkgestelden, thuiswerkers, artiesten, stagiairs, meewerkende
  kinderen and others); some of these can be excluded by written agreement made
  before the first payment.
- **The same work can be loondienst for one person and not for another.** A
  colleague's outcome proves nothing about the taxpayer's.

## Handhaving from 1 January 2025 onward

| Period | Position published by the Belastingdienst |
|--------|-------------------------------------------|
| Up to 31 December 2024 | Handhavingsmoratorium in force |
| From 1 January 2025 | "Sinds 1 januari 2025 geldt het handhavingsmoratorium niet meer." The normal rules apply again |
| During 2025 | "In 2025 legden we nog geen verzuim- en vergrijpboetes op." |
| From 1 January 2026 | "Vanaf 1 januari 2026 kunnen we wel vergrijpboetes opleggen. We leggen in 2026 nog geen verzuimboetes op." |

- **Look-back limit:** corrections go back no further than 1 January 2025 --
  "Maar nooit verder terug dan 1 januari 2025." The exception is bad faith
  (kwaadwillendheid) or an earlier aanwijzing that was not followed sufficiently;
  in that case naheffing up to 5 years back is possible.
- **The instruments are aimed at the opdrachtgever.** Correctieverplichtingen,
  naheffingsaanslagen loonheffingen and boetes are addressed to the party that
  should have withheld. The Belastingdienst handhaving page covers the
  loonheffingen only and says nothing about the zzp'er's own aangifte
  inkomstenbelasting.
- The detail sits in two documents listed on the Belastingdienst's
  handhavingsplan download page: the **Handhavingsplan arbeidsrelaties 2026**
  (file name `handhavingsplan-arbeidsrelaties-lh0021z62fd.pdf`) and the **Memo
  handhaving arbeidsrelaties -- richtlijnen doorwerking IH en OB 2025-2026**.
  Both are PDFs on the Belastingdienst's separate download host, which is not an
  allowed source domain for this plugin; they are cited here through the landing
  page and named by title. From those documents: the zachte landing is partly
  extended through 2026 (no verzuimboetes, and a bedrijfsbezoek as the normal
  starting point), with those elements lapsing from 1 January 2027; the
  ingroeimodel runs until 2030, from when corrections up to 5 years back become
  possible again; and for corrections over 2025 the zachte landing continues, so
  no verzuim- or vergrijpboetes are imposed for that year. On doorwerking, the
  enforcement effort is aimed primarily at the loonheffingen in relation to
  opdrachtgevers; where an opdrachtnemer is drawn into regular income-tax or
  turnover-tax supervision, the assessment is directed as far as possible at the
  most recent open (winst)aangifte and at future returns.
- The doorwerking memo carries a version date of 18 December 2024 while its title
  names 2025-2026. Treat its content as the published position and recheck both
  documents before the 2026 season.

## What an arbeidsrelatie correction does to the ZZP'er's own return

The Belastingdienst distinguishes two situations, and they land differently:

**A. The parties determine upfront that the assignment is loondienst.** For that
assignment:

- the taxpayer is **not an ondernemer voor de inkomstenbelasting**;
- costs incurred for that assignment **may not be deducted**;
- the assignment does not count toward the **ondernemersaftrek** (the
  zelfstandigenaftrek is named), the **investeringsaftrek**, or the
  **MKB-winstvrijstelling**;
- for the btw, the taxpayer is not a btw-ondernemer for that assignment, may not
  charge btw on it, and cannot deduct btw paid for it. Where there is no other
  work as a btw-ondernemer, deregistration is done by letter to the
  Belastingdienst quoting the omzetbelastingnummer -- this applies even under the
  KOR, and anyone registered with KVK must notify KVK as well. Failing to
  deregister risks naheffingsaanslagen en boetes.

There is a narrow exception: the loondienst assignment can still count as an
ondernemingsactiviteit where **both** conditions hold -- it is strongly connected
with other work the taxpayer genuinely does as an ondernemer, **and** it is
subordinate to that work. Both limbs must be met. This is a weighing, so it is
**manual review**: record the facts and ask.

**B. The Belastingdienst establishes afterwards that there was loondienst.** The
taxpayer used entrepreneur schemes they were not entitled to, so too little
income tax was paid. The Belastingdienst's own published example, framed as a
check over 2025 carried out in the second half of 2026:

| Element | Amount in the Belastingdienst example |
|---------|---------------------------------------|
| Omzet | EUR 36,000 |
| Kosten | EUR 2,000 |
| Cost deduction withdrawn | EUR 2,000 |
| Zelfstandigenaftrek withdrawn | EUR 2,470 |
| MKB-winstvrijstelling withdrawn | EUR 4,005 |
| Total increase of the taxed base | EUR 8,475 |
| Inkomstenbelasting and premies underpaid | about EUR 3,245 |
| Bijdrage Zvw overpaid, as printed in the source | EUR 1,448 |

This is the Belastingdienst's illustration, not a formula and not a prediction.
Its Zvw row is internally inconsistent: EUR 1,448 is **not** 5.26% of EUR 8,475,
which is EUR 445.79. A bijdrage of EUR 1,448 at 5.26% corresponds to a base near
EUR 27,500 -- the order of the example's former taxable business profit, not the
increase in the income-tax base. If reproducing the illustration, state this
conflict and never describe EUR 1,448 as calculated over EUR 8,475 or substitute the
taxpayer's figures into it.

On the loonheffingen side of scenario B: the opdrachtgever must still withhold
and pay the loonbelasting and premie volksverzekeringen, and may ask the taxpayer
to repay that amount -- unless the taxpayer has already received a definitieve
aanslag inkomstenbelasting for that year, in which case it will not be asked,
though a refund of the bijdrage Zvw can then be requested. The opdrachtgever owes
the premies werknemersverzekeringen and the werkgeversheffing Zvw itself and the
taxpayer does not repay those, except that the opdrachtgever may ask for 50% of
the gedifferentieerde premie Werkhervattingskas and may ask the taxpayer to repay
belastingrente.

**What the agent does with all of this:** nothing automatic. If the taxpayer says
an assignment has been reclassified, or that a check is running, the 2025 figures
are no longer a routine preparation -- record the facts and route the return to
manual review. Do not recompute a return on the assumption that a reclassification
will or will not stand.

## A modelovereenkomst does not prove IB-ondernemerschap

This is the single most expensive misconception in this area, and it must be
corrected explicitly whenever a taxpayer offers a modelovereenkomst as proof of
entitlement to the zelfstandigenaftrek.

What a modelovereenkomst does:

- Working according to an approved modelovereenkomst means **there is no
  loondienst** -- "Als u werkt volgens een modelovereenkomst, is er geen sprake
  van loondienst." That is a statement about the **loonheffingen**.
- It gives certainty **only** where both parties actually work as described in
  the agreement. The Belastingdienst names the risk itself:
  "Modelovereenkomsten kunnen voor schijnzekerheid zorgen" -- the assessment
  follows the actual practice, not the paperwork.

What a modelovereenkomst does **not** do:

- It says nothing about ondernemerschap voor de inkomstenbelasting and nothing
  about the btw. The Belastingdienst's modelovereenkomst pages contain no
  statement on either.
- It therefore does **not** establish winst uit onderneming, does **not** create
  entitlement to the ondernemersaftrek, the MKB-winstvrijstelling or the
  investeringsaftrek, and does **not** answer the bron van inkomen question in
  Part 1.

Current status of the scheme:

- **No new modelovereenkomsten have been assessed since 6 September 2024**, and
  existing ones are no longer extended.
- Modelovereenkomsten that were approved and valid on 6 September 2024 may be
  used **up to and including 31 December 2029**. That end date applies even where
  the agreement itself states a different validity period.
- Using one has never been an obligation. Where the parties have jointly
  concluded there is no loondienst, a modelovereenkomst is one option, not a
  requirement.

---

## Developer instruction

1. **Run the bron van inkomen screen first, before any category question and
   before any figure is collected.** Ask about the three conditions, about the
   hobby- and familiesfeer, and about whether losses are structural. Record the
   taxpayer's answers verbatim in the workpack. Present the outcome as the
   taxpayer's to confirm; never assert it. If the answers point away from a bron,
   state both consequences -- the income is not taxed and the costs are not
   deductible -- and route to manual review.
2. **Test the categories in order: loon, then winst, then resultaat uit overige
   werkzaamheden as the residual.** Decide per activity, and ask whether several
   activities are connected before treating them as one bron.
3. **Do not decide a borderline ondernemer case.** Surface the eight criteria,
   collect the taxpayer's facts against each, state what each outcome costs in
   the reliefs listed in Part 2, and ask. Record the answer as a fact in the
   workpack. Route the decision itself to manual review.
4. **Never treat a KvK registration, an omzetbelastingnummer, the KOR, a
   modelovereenkomst, or the absence of loondienst as proof of
   IB-ondernemerschap.** If the taxpayer offers any of these as their reason for
   claiming the zelfstandigenaftrek, correct the point explicitly using the table
   in Part 1 and go back to the eight criteria.
5. **When the outcome is resultaat uit overige werkzaamheden, prepare it -- do
   not stop.** Collect the income and the costs, apply `winst-en-kosten.md` and
   `afschrijving-en-bedrijfsmiddelen-2025.md`, and produce the resultaat. Report
   it in the private part of the return under inkomsten uit overig werk, field
   `box1.resultaat_overige_werkzaamheden`. Do not open the zakelijke schema for
   this category and do not print a portal click path.
6. **Quantify the loss of the ondernemersfaciliteiten from the taxpayer's own
   figures.** Read the zelfstandigenaftrek amount from `ondernemersaftrek.md`,
   the 12.7% from `mkb-winstvrijstelling.md` and any investeringsaftrek from
   `investeringsaftrek.md`, and show the two outcomes side by side. Never quote a
   single euro figure for "what it costs" and never reuse the Belastingdienst's
   published example as the taxpayer's own result.
7. **Do not ask for an hours count in order to settle the resultaat uit overige
   werkzaamheden category.** The urencriterium gates reliefs that this category
   does not have. Ask for hours only when ondernemerschap is genuinely in play,
   per `ondernemer-criteria.md`.
8. **Always add the bijdrage Zvw to a resultaat uit overig werk case.** Read the
   percentage and the maximumbijdrage-inkomen from `zvw-2025.md`; never restate
   them from memory. Ask whether the taxpayer also had loon, pensioen or an
   uitkering in 2025 and, for each, ask for the "loon Zorgverzekeringswet" on the
   jaaropgaaf. Never assume there was none. Tell the taxpayer that two separate
   assessments follow the one return.
9. **Route these to manual review without calculating:** terbeschikkingstelling
   van bezittingen; gastouder, artiest, beroepssporter, pgb-zorg and
   vermogensbeheer cases; medegerechtigdheid; partnerships; and willekeurige
   afschrijving for a resultaat uit overige werkzaamheden taxpayer. For
   lijfrente, do not shelve the ruimte: follow `inkomensvoorzieningen-2025.md`,
   where the belastbaar resultaat uit overige werkzaamheden is a named
   premiegrondslag component and only the pension-accrual reduction goes to
   manual review. Ask for the **2024** resultaat, not the 2025 one.
10. **Do not offer a fiscal-partner allocation** for bijverdiensten or income as
    freelancer, gastouder, artiest or beroepssporter, nor for resultaat uit het
    beschikbaar stellen van bezittingen. These are not divisible.
11. **Treat Part 3 as explanation only.** Never state whether an assignment is
    loondienst, never assess an arbeidsrelatie, and never contact or act toward
    an opdrachtgever. Point the taxpayer at the joint assessment they and the
    opdrachtgever must make, and at the SZW Webmodule for cases of doubt. If a
    reclassification has happened or a check is running, record the facts and
    route the whole return to manual review rather than recomputing it on an
    assumption.
12. **Collect only the amounts, dates and descriptions the calculation needs.**
    Do not record a BSN, an aanslagnummer or a bank account number from any
    invoice, jaaropgaaf or assessment.
13. **The taxpayer performs every authenticated action.** You (the taxpayer) log
    in to Mijn Belastingdienst, open the return, type the figures and send it;
    you (the taxpayer) run the OndernemersCheck if you want its indication. This
    plugin never opens the portal, never logs in, never enters a value and never
    submits.
14. **Recheck before the 2026 season:** the handhaving timeline and the boete
    position in Part 3, both handhavingsplan documents named there, and the
    special-category limits in Part 2. All of them are reset or restated each
    year.
