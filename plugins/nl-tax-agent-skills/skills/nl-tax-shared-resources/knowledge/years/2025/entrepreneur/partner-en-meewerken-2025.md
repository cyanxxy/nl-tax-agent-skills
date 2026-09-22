# Rule note: Meewerkende fiscale partner 2025

source_ids: bd_partner_gaat_meewerken, bd_meewerkaftrek_algemeen, bd_meewerkaftrek_2025, bd_arbeidsbeloning_fiscale_partner, bd_fisin2025_row, bd_wat_zijn_inkomsten_overig_werk, fisin2025_fiscaal_partnerschap, bd_urencriterium_2025, bd_personeel_in_uw_onderneming, bd_aanmelden_werkgever, bd_vof_rechtsvorm, wetib_consolidated_2025, law_wet_inkomstenbelasting_2001
workflow: annual_return
tax_year: 2025
status: active
last_reviewed: "2026-08-15"
review_status: reviewed

## Rule

This note is canonical for the 2025 annual return in the situation where the
ondernemer's **fiscale partner works in the enterprise**. It covers the four
routes the Belastingdienst recognises -- meewerkaftrek, arbeidsbeloning, an echte
dienstbetrekking, and the partner becoming medeondernemer -- how the choice
between them is made, and what each route does on the partner's own side of the
return. It also fixes one point that is easy to get wrong: winst uit onderneming
is not a gemeenschappelijk inkomensbestanddeel, so nothing in this area is an
allocation choice between partners. The other ondernemersaftrek components and
their amounts stay canonical in `ondernemersaftrek.md`; the ordering of the
profit chain is in `winstberekening-2025.md`; the MKB-winstvrijstelling is in
`mkb-winstvrijstelling.md`; who counts as a fiscale partner at all is in
`../../../partners/fiscal-partnership.md`; the partnership route itself is in
`samenwerkingsverband-2025.md`. This note is annual 2025 only.

These are reference notes for workpack preparation -- not final tax advice.

## The four routes at a glance

| Route | Effect for the ondernemer | Effect for the fiscale partner | Handled here |
|-------|---------------------------|--------------------------------|--------------|
| 1. Meewerkaftrek (art. 3.78) | a percentage of the winst is deducted as part of the ondernemersaftrek | nothing is reported | yes, computable |
| 2. Arbeidsbeloning of EUR 5,000 or more (art. 3.16 lid 4 a contrario) | the payment is deductible from the winst | taxed as inkomsten uit overig werk | yes, once the amount is confirmed |
| 2b. Arbeidsbeloning below EUR 5,000 | **not** deductible | **not** reported as income | yes, and it is neutral on both sides |
| 3. Echte dienstbetrekking (arbeidsovereenkomst) | payroll: loonheffingen, not income tax | loon uit dienstbetrekking | no -- **manual review** |
| 4. Partner becomes medeondernemer | the rechtsvorm changes; both report their own winstaandeel | own winst uit onderneming | no -- see `samenwerkingsverband-2025.md` |

**The choice is free and is made per year.** The Belastingdienst states it
plainly: "U kunt elk jaar opnieuw kiezen voor meewerkaftrek of arbeidsbeloning."
A choice made for 2024 does not bind 2025, and a choice made for 2025 does not
bind later years.

Routes 1 and 2 are mutually exclusive within one year. The meewerkaftrek requires
that the partner works without a vergoeding, or for a vergoeding below
EUR 5,000; paying EUR 5,000 or more therefore rules out the meewerkaftrek for
that year, and the ondernemer takes the deduction of the payment instead.

## Route 1 -- Meewerkaftrek (art. 3.78 Wet IB 2001)

### Conditions, all four required

1. The taxpayer is an ondernemer voor de inkomstenbelasting
   (`ondernemer-criteria.md`).
2. The taxpayer meets the **urencriterium of 1,225 hours** in 2025. This is the
   ondernemer's own hour count, not the partner's, and it is not reduced for a
   part year. The full test is in `aanloopfase-en-starters-2025.md` and
   `ondernemer-criteria.md`.
3. The fiscale partner works in the enterprise **without a vergoeding, or for a
   vergoeding below EUR 5,000**.
4. The fiscale partner works **525 hours or more** in the enterprise in the
   calendar year.

The statutory text of art. 3.78 lid 1 is stricter on its face than the published
guidance: it speaks of a partner who works "zonder enige vergoeding". The
Belastingdienst's operative condition is the one in point 3 above, and it is
consistent with art. 3.16 lid 4, which denies the ondernemer any deduction for a
vergoeding below EUR 5,000. Apply the published condition.

### Hours bands and percentages, 2025

The percentage is applied to the winst. Band boundaries follow the statutory
columns "gelijk aan of meer dan" and "maar minder dan", so a boundary hour falls
in the higher band.

| Hours the fiscale partner works in the enterprise | Meewerkaftrek 2025 |
|---------------------------------------------------|--------------------|
| less than 525                                      | none               |
| at least 525 but less than 875                     | **1.25%** of the winst |
| at least 875 but less than 1,225                   | **2%** of the winst |
| at least 1,225 but less than 1,750                 | **3%** of the winst |
| 1,750 or more                                      | **4%** of the winst |

There is no partial credit below 525 hours, and there is no band above 4%.

### The winst base, and what is excluded from it

The base is the joint amount of winst the taxpayer enjoys **as ondernemer** from
the onderneming or ondernemingen in which the partner works. In the chain of
`winstberekening-2025.md` that is **line B** -- the winst after the
investeringsaftrek and before the ondernemersaftrek. It has to be before the
ondernemersaftrek, because the meewerkaftrek is itself one of the
ondernemersaftrek components.

Art. 3.78 lid 3 removes three items from that base:

| Excluded from the meewerkaftrek base |
|--------------------------------------|
| profit arising on **onteigening** (the replacement profit) |
| profit realised on the **(gedeeltelijke) staking** of an onderneming, including staking by death under art. 3.58 |
| profit on **moving vermogensbestanddelen abroad**, and the eindafrekening profit under art. 3.60 and art. 3.61 |

So in a year in which the enterprise is wholly or partly staked, the stakingswinst
does not enlarge the meewerkaftrek. Where a staking is in play, prepare the base
and route the split to manual review together with the staking itself
(`staking-2025.md`).

### Further rules

- **No meewerkaftrek over winst enjoyed as medegerechtigde.** If part of the
  taxpayer's winst comes from a medegerechtigdheid, that part is outside this
  deduction -- see `samenwerkingsverband-2025.md`.
- The meewerkaftrek is a component of the ondernemersaftrek, so it is a
  grondslagverminderende post subject to the tariefsaanpassing. Read that cap
  from `ondernemersaftrek.md` and `../annual/deductions.md`; do not restate it
  here.
- **The partner's hours must be made plausible.** The Belastingdienst requires
  that the taxpayer "aannemelijk kan maken" how many hours the partner worked.
  Ask for an urenregistratie or an equivalent record. Hours the taxpayer cannot
  substantiate are not entered as a figure.
- The partner reports nothing at all on this route. There is no counter-entry in
  the partner's return.

## Route 2 -- Arbeidsbeloning to the fiscale partner: the EUR 5,000 cliff

Where the partner is paid for the work but is **not** in an echte
dienstbetrekking, the payment is an arbeidsbeloning. Art. 3.16 lid 4 makes the
treatment a hard threshold, not a sliding scale:

| Arbeidsbeloning paid in 2025 | Ondernemer's side | Fiscale partner's side |
|------------------------------|-------------------|------------------------|
| **below EUR 5,000** | **not deductible** from the winst | **not income** -- the partner does not report it |
| **EUR 5,000 or more** | **fully deductible** from the winst | **taxed as inkomsten uit overig werk** |

The statutory text: "Bij het bepalen van de winst komen mede niet in aftrek
kosten en lasten die verband houden met vergoeding van arbeid door de partner
van de belastingplichtige, indien de vergoeding lager is dan EUR 5000."

Consequences the workpack must state plainly:

- **Below the threshold the payment is neutral on both sides.** It is not a
  deduction for the ondernemer and it is not income for the partner. Money can
  still move between the partners; it simply has no effect in either return. The
  alternative in that situation is the meewerkaftrek of route 1, and that is
  exactly how the Belastingdienst presents it.
- **At or above the threshold the payment is fully deductible**, not deductible
  only for the excess over EUR 5,000. There is no drempel here; EUR 5,000 is a
  cliff.
- On the partner's side the amount is **inkomsten uit overig werk** (resultaat
  uit overige werkzaamheden), not loon. The partner deducts the costs attaching
  to that work, and the balance is the resultaat uit overig werk. Over that
  resultaat the partner owes inkomstenbelasting and premie volksverzekeringen
  **and an inkomensafhankelijke bijdrage Zorgverzekeringswet**, which arrives as
  a separate aanslag. The Zvw rules and percentages stay canonical in
  `zvw-2025.md`.
- The partner's inkomsten uit overig werk are the partner's own income. They are
  not divisible between the partners -- see the section on gemeenschappelijke
  inkomensbestanddelen below.

### Is the amount reeel? -- manual review

The Belastingdienst attaches a substantive condition to the arbeidsbeloning:
"De hoogte van de beloning moet reeel zijn voor het werk dat uw partner doet."

**Whether a specific amount is reeel is a judgement, not a calculation. It is a
manual-review item.** Record the facts -- what the partner does, how many hours,
what the same work would cost from a third party, and the amount actually paid --
and hand the assessment to a human. Do not confirm an amount as reeel, and do not
suggest an amount that would clear the EUR 5,000 threshold.

### Evidence to ask for

The payment must be visible in the administration. Ask for:

- proof of how the partner was paid: a bank transfer to the partner, or a
  **schulderkenning** (a written statement that the ondernemer owes the partner
  the amount);
- the amount and the date or dates of payment in 2025;
- a record of the hours the partner worked and what the work consisted of, which
  the Belastingdienst recommends keeping;
- confirmation that the partner reported, or will report, the amount as
  inkomsten uit overig werk where it is EUR 5,000 or more.

An arbeidsbeloning that exists only as an intention, with no payment and no
schulderkenning, is not entered as a deduction.

## Route 3 -- Partner in an echte dienstbetrekking: MANUAL REVIEW

The ondernemer and the partner can conclude an **arbeidsovereenkomst**, putting
the partner in dienstbetrekking. **This route is out of automated scope. It is
payroll (loonheffingen), not income tax, and it is handled on a different
statute, a different registration and a different filing cadence.**

What is established, for explanation only:

- Only under a dienstbetrekking must the ondernemer withhold and pay
  **loonbelasting/premie volksverzekeringen and the inkomensafhankelijke bijdrage
  Zorgverzekeringswet**. Whether premies werknemersverzekeringen are also due
  depends on the arbeidsvoorwaarden and on whether there is a gezagsrelatie.
- The Belastingdienst names a condition for the meewerkende partner in
  dienstbetrekking: "Uw partner werkt onder dezelfde arbeidsvoorwaarden als uw
  andere werknemers."
- A meewerkende partner is on the Belastingdienst's own list of situations in
  which there may be **no** dienstbetrekking at all. Whether an arrangement is a
  dienstbetrekking is assessed on the facts; the criteria sit in the Handboek
  Loonheffingen, which is outside this knowledge pack.
- Becoming an employer triggers a separate obligation with its own deadline:
  registration as werkgever at the latest on the day the first employee starts.
  `samenwerkingsverband-2025.md` carries that handoff.

**Do not compute a loonheffing, do not compute a net or gross wage, and do not
present the wage as an ondernemersaftrek item.** Record that this route is in
play, record the wage cost as a business cost fact for the winstberekening, and
route the payroll consequences to manual review.

## Route 4 -- Partner becomes medeondernemer

The partners can carry on the enterprise together. The Belastingdienst is
explicit that this requires changing the legal form: "moet u de rechtsvorm van de
onderneming aanpassen." The usual form is a vof, and the man-vrouwfirma is named
as a special form of the vof. If both partners meet the ondernemer conditions,
each is an ondernemer voor de inkomstenbelasting in their own right and each can
use the ondernemersregelingen.

Two warnings before the agent presents this as an option:

1. Changing the rechtsvorm is in general treated as a **staking** of the existing
   ondernemersactiviteiten, with a balans and a settlement. See
   `samenwerkingsverband-2025.md` and `staking-2025.md`.
2. A vof between fiscal partners is exactly the setting in which the
   **ongebruikelijk samenwerkingsverband** rule bites, which can cost one partner
   the urencriterium and with it the ondernemersaftrek. That test is in
   `samenwerkingsverband-2025.md`.

Everything about this route -- the winstverdeling, the per-partner tests, the
staking on entry -- belongs to `samenwerkingsverband-2025.md`. Do not compute it
here.

## Winst uit onderneming is not a gemeenschappelijk inkomensbestanddeel

This is the point the agent must protect against a natural but wrong assumption.

- **Winst uit onderneming may not be divided between fiscal partners.** The
  Belastingdienst lists "winst uit onderneming" under "Wat mag u niet verdelen?".
  The profit belongs to the ondernemer who earned it, in full.
- **The ondernemersaftrek is strictly personal to the ondernemer.** Every
  component -- zelfstandigenaftrek, startersaftrek, aftrek voor speur- en
  ontwikkelingswerk, meewerkaftrek, startersaftrek bij arbeidsongeschiktheid,
  stakingsaftrek -- attaches to the person who meets its conditions and cannot be
  moved to the partner.
- **The MKB-winstvrijstelling is likewise strictly personal** and cannot be
  allocated between fiscal partners; `mkb-winstvrijstelling.md` says the same.
- Also not divisible: the partner's own **inkomsten uit overig werk**, and the
  **resultaat uit het beschikbaar stellen van bezittingen**
  (`samenwerkingsverband-2025.md` covers the terbeschikkingstellingsregeling).
- Filing a joint aangifte remains possible and useful -- some other items **are**
  divisible -- but the divisible and non-divisible lists live in
  `../../../partners/fiscal-partnership.md`, which stays canonical for them.
- If the partners were **not** fiscal partners for the whole of 2025, nothing may
  be divided at all: each reports only their own income and deductions.

The practical consequence: routes 1 and 2 are not two ways of allocating one
income figure. Route 1 gives the ondernemer a deduction and leaves the partner
with nothing to report; route 2 moves real income to the partner and taxes it
there. They produce different outcomes for both people, and the workpack should
present both before the taxpayer chooses.

## Manual-review boundaries

Record the facts, do not compute, and route to manual review:

1. Whether a specific arbeidsbeloning amount is **reeel** for the work done.
2. Any **echte dienstbetrekking** between the ondernemer and the partner, and
   every loonheffingen consequence that follows from it.
3. The partner becoming **medeondernemer**, including the rechtsvorm change and
   the staking that generally accompanies it.
4. Any year in which the enterprise is wholly or partly **staked**, because the
   stakingswinst is carved out of the meewerkaftrek base.
5. Any part of the winst enjoyed as **medegerechtigde**, which is outside the
   meewerkaftrek.
6. **Part-year fiscal partnership.** The retrieved guidance states that partners
   for only part of the year may divide nothing, but it does not state how the
   525-hour test and the EUR 5,000 threshold work across a part year. That
   mapping is not established here -- ask for the dates and route it to a human.
7. A partner who works in **more than one** of the taxpayer's ondernemingen, or
   in an onderneming of a samenwerkingsverband.

## Developer instruction

1. Establish first, by asking, that the person working in the enterprise **is**
   the taxpayer's fiscale partner for 2025, and for which part of the year. Use
   `../../../partners/fiscal-partnership.md` for the test. If the person is not a
   fiscale partner, none of this note applies -- that is ordinary staff or an
   ordinary opdrachtnemer.
2. Ask, do not assume, for: (a) the number of hours the partner worked in the
   enterprise in 2025 and whether a record exists; (b) whether anything was paid
   to the partner and how much; (c) how it was paid -- bank transfer or
   schulderkenning; (d) whether there is a written arbeidsovereenkomst. Never
   fill in zero hours or a zero payment because the taxpayer did not mention one.
3. Confirm the **ondernemer's own** urencriterium before presenting any
   meewerkaftrek figure. Without the 1,225 hours there is no meewerkaftrek, no
   matter how many hours the partner worked.
4. Read the band table in this note to pick the percentage. Apply it to line B of
   `winstberekening-2025.md`, after removing the three art. 3.78 lid 3 exclusions.
   Never paraphrase a percentage from memory and never interpolate between bands.
5. For an arbeidsbeloning, state the EUR 5,000 cliff explicitly in the workpack,
   including that below it the payment is neutral on **both** sides. Do not
   describe a sub-threshold payment as partly deductible.
6. Do not judge whether an arbeidsbeloning is reeel, and do not propose an amount.
   Present the facts and mark it for a human.
7. When both routes are open, present the comparison rather than choosing:
   what the meewerkaftrek would be at the partner's hour band, what the deduction
   would be at the arbeidsbeloning actually paid, and what the partner would owe
   in inkomstenbelasting, premie volksverzekeringen and Zvw on that amount. State
   that the choice can be made again next year.
8. If the partner is in an echte dienstbetrekking, stop the income-tax reasoning
   at the wage cost, say clearly that loonheffingen is a separate obligation on a
   separate cadence, and route it to manual review.
9. If the partners want to become medeondernemers, hand the whole question to
   `samenwerkingsverband-2025.md` and warn about the staking and the
   ongebruikelijk-samenwerkingsverband tests before the taxpayer commits.
10. Never present winst uit onderneming, the ondernemersaftrek or the
    MKB-winstvrijstelling as something the partners can split. If the taxpayer
    asks to shift profit to the partner, explain routes 1 to 4 and say that no
    allocation of the winst itself is possible.
11. Every portal action stays with the human: you (the taxpayer) open Mijn
    Belastingdienst, enter the meewerkaftrek hours or the arbeidsbeloning, enter
    the partner's inkomsten uit overig werk in the partner's own part of the
    return, and submit. The plugin prepares and explains the figures and never
    logs in, enters, or sends anything.
