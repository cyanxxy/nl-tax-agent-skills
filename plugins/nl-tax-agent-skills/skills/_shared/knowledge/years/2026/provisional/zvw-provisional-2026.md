# Rule note: Bijdrage Zorgverzekeringswet and the voorlopige aanslag Zvw 2026

source_ids: bd_zvw_percentages_2025_2026, bd_zvw_provisional_aanslag_2026, bd_zvw_inkomensafhankelijke_bijdrage, bd_zvw_resultaat_overig_werk, bd_zvw_hoe_betalen, bd_zvw_werkgeversheffing_of_bijdrage_tabel, bd_zvw_teruggaaf, bd_fisin_zvw_2026, reg_zorgverzekering_h5_2026, wet_zvw_art41_49_2026, law_wet_inkomstenbelasting_2001
workflow: provisional_assessment
tax_year: 2026
status: active
last_reviewed: "2026-08-15"
review_status: reviewed

## Rule

This note is canonical for what the agent tells a 2026 provisional-assessment
taxpayer about the inkomensafhankelijke bijdrage Zorgverzekeringswet (Zvw): the
2026 percentage and ceiling, the fact that the bijdrage is levied by a separate
aanslag, and -- the point with the most practical value in this whole flow -- the
fact that there is a **separate voorlopige aanslag Zorgverzekeringswet with its
own change route**. It is a companion to `winst-provisional-2026.md`, which owns
the single income-tax profit estimate, and to `change-flow.md` and
`request-flow.md`, which own the income-tax subflow mechanics. This note does not
calculate a bijdrage amount and does not add a field to the income-tax
voorlopige-aanslag dataset.

These are reference notes for workpack preparation -- not final tax advice.

## Who pays the bijdrage themselves

An ondernemer, and anyone with income from work performed outside employment,
pays the bijdrage Zvw themselves rather than through a withholding agent. The
Belastingdienst's own comparison table puts both "Ondernemer" and "Freelancer" in
the same position: no werkgeversheffing Zvw, and yes to paying the bijdrage Zvw
themselves. Where the taxpayer has loon or a uitkering instead, the employer or
benefits agency handles it: "Uw inkomensafhankelijke bijdrage Zvw wordt geregeld
via uw werkgever of uitkeringsinstantie."

Legal basis (named here as basis only, with no figure taken from it): Zvw
art. 41 (both the inhoudingsplichtige and the verzekeringsplichtige owe an
inkomensafhankelijke bijdrage), art. 43 (the bijdrage-inkomen and its annual
cap), art. 45 (the bijdrage is a percentage of the bijdrage-inkomen, set by
ministerial regulation), art. 48 (the rijksbelastingdienst levies it), and
art. 49 lid 3 (levy by way of aanslag for the non-wage components).

## Percentages and ceiling for 2026

| Item | 2026 |
|---|---|
| Bijdrage Zvw paid by the verzekeringsplichtige through an aanslag Zvw (ondernemers, freelancers) | 4.85% |
| Bijdrage Zvw withheld by a withholding agent on income that carries no werkgeversheffing, such as pensioen, lijfrente and comparable uitkeringen | 4.85% |
| Werkgeversheffing Zvw owed by the employer over loon uit dienstbetrekking; nothing is withheld from the employee for it | 6.10% |
| Maximumbijdrage-inkomen | EUR 79,409 |

These figures are published by the Belastingdienst and fixed in the Regeling
zorgverzekering: art. 5.2 sets the 2026 maximum at EUR 79,409, art. 5.3 sets the
maximum bijdrage-inkomen at that same amount, art. 5.4 lid 1 sets the
werkgeversheffing percentage at 6.10 and art. 5.4 lid 2 sets the percentage for
the verzekeringsplichtige at 4.85.

On loon uit tegenwoordige dienstbetrekking the employer owes the 6.10%
werkgeversheffing and no bijdrage Zvw is withheld from the employee. Never tell a
taxpayer that their loon already carried a 4.85% employee deduction. Which
situations carry the werkgeversheffing and which carry the withheld bijdrage is
set out in the Belastingdienst table "Werkgeversheffing Zvw of bijdrage Zvw?";
route an unusual case, such as a directeur-grootaandeelhouder, to manual review.

**Do not print a maximum bijdrage amount.** The Belastingdienst publishes the
percentage and the ceiling, not the product of the two. The bijdrage is
calculated by the Belastingdienst on the aanslag; state the percentage and the
ceiling and stop there.

## The base is a different figure from the income-tax estimate

The bijdrage-inkomen of a taxpayer with business profit is the **belastbare winst
uit onderneming**, determined under the rules of afdeling 3.2 Wet IB 2001
(Zvw art. 43 lid 2 onderdeel b). That is the profit **after** the
ondernemersaftrek and the mkb-winstvrijstelling.

The income-tax voorlopige aanslag asks for the opposite figure: one estimate of
the winst **before** ondernemersaftrek and before mkb-winstvrijstelling (see
`winst-provisional-2026.md`). Keep the two apart when explaining anything to the
taxpayer, and never present the income-tax estimate as the Zvw base. This plugin
does not compute the belastbare winst in the provisional flow -- the point of
this section is only to stop the agent from equating the two figures.

The bijdrage-inkomen is set at a minimum of nil and capped at the annually fixed
maximum (Zvw art. 43 lid 3). A release of an oudedagsreserve that is voluntary
and matched by a lijfrente is carved out of the bijdrage-inkomen by
Zvw art. 43 lid 2 onderdeel b; a mandatory release is not. Any oudedagsreserve
fact is a manual-review item -- record it and do not size it.

## The bijdrage is levied by a SEPARATE aanslag

Two assessments follow, not one. The Belastingdienst states it plainly for people
with income outside employment: "ontvangt u van ons 2 aanslagen: 1 aanslag voor
de inkomstenbelasting/premie volksverzekeringen en een andere voor de bijdrage
Zvw." The 2026 Fiscale informatie chapter says the same about the provisional
stage: the Zvw assessment is received "naast uw (voorlopige) aanslag
inkomstenbelasting en premie volksverzekeringen".

One return feeds both: the taxpayer uses the same aangifte for the
inkomstenbelasting, and where they file online the bijdrage Zvw is calculated for
them. But the assessments themselves are separate documents.

## THERE IS A SEPARATE VOORLOPIGE AANSLAG ZORGVERZEKERINGSWET

This is the practical item that matters most, and the agent must raise it without
waiting to be asked.

- An ondernemer, or a person with income from work outside employment, "krijgt
  dan een voorlopige aanslag Zvw". It can be issued because winst uit onderneming
  or inkomsten uit overig werk were declared in an earlier year, and the
  Belastingdienst describes it as "een schatting op basis van deze inkomsten".
- The taxpayer finds it in Mijn Belastingdienst; it is also sent by post.
- It has its **own change route**. Where the taxpayer disagrees with it --
  the Belastingdienst names lower income than the estimate as the example -- they
  change that voorlopige aanslag online, through a separate "wijzigen" path for
  the voorlopige aanslag 2026.

**Check the Zvw assessment separately.** These are two separate aanslagen, each
with its own change route. No reviewed official page states whether changing the
income-tax voorlopige aanslag also updates the voorlopige aanslag Zvw, so do not
tell the taxpayer that it does or that it does not. Treat the Zvw assessment as
a second item to check in its own right: a taxpayer who lowers their expected
profit in the income-tax voorlopige aanslag should look at the voorlopige
aanslag Zvw as well, and change it through its own route if it still rests on
the higher income. Record what they find rather than predicting it.

The Belastingdienst's Zvw voorlopige-aanslag page carries no percentages, no
instalment rules and no payment deadlines, and does not state when the definitive
aanslag Zvw follows. Payment terms and timing for the voorlopige aanslag Zvw are
therefore **not established** in the reviewed sources. Do not carry the
income-tax instalment or refund timing across to the Zvw assessment. Ask the
taxpayer to read the dates printed on their own voorlopige aanslag Zvw, and route
any timing question to manual review.

## The shared ceiling when the taxpayer also has loon

The maximumbijdrage-inkomen is a single ceiling across the taxpayer's income, not
one ceiling per income source. Where the taxpayer also has loon on which the
employer already pays the werkgeversheffing, the Belastingdienst calculates the
4.85% only over the remaining income: "Dan berekenen wij de bijdrage Zvw van
4,85% alleen nog over uw andere inkomsten." Where levy is by aanslag, the cap is
reduced by the loon already taken into account (Zvw art. 43 lid 5).

The Belastingdienst's published 2026 worked example makes the mechanism concrete:

| Situation in the official 2026 example | Base for the bijdrage via aanslag |
|---|---|
| EUR 40,000 loon plus EUR 50,000 freelance income | EUR 39,409 |

Where the loon on its own already reaches the maximumbijdrage-inkomen, no further
bijdrage arises over the other income: "Over het inkomen dat boven het
maximumbijdrage-inkomen ligt, betaalt u geen bijdrage Zvw meer."

Use the example only as an illustration of the mechanism. Do not reuse its
numbers as the taxpayer's own base, and do not compute the taxpayer's base for
them.

A separate automatic refund exists where too much bijdrage was **withheld**
because several employers or benefits agencies withheld at the same time; it is
paid out in March or April of the following calendar year and the taxpayer need
do nothing. That route concerns withholding on loon, pensioen or uitkering -- not
profit paid by aanslag -- so do not offer it as a remedy for an overstated
voorlopige aanslag Zvw. The remedy there is to change the voorlopige aanslag Zvw.

## The bijdrage is not deductible

The inkomensafhankelijke bijdrage Zvw is not deductible. It is not a business
cost (Wet IB 2001 art. 3.16) and it is not an aftrekbare uitgave voor specifieke
zorgkosten (Wet IB 2001 art. 6.18). Never subtract it from the expected profit
estimate, and never present it as a deduction anywhere in the workpack. If the
taxpayer asks, say it plainly: the bijdrage is a cost the taxpayer bears, but it
is not a deductible one.

## Manual-review boundaries

Record the facts and route these to manual review; do not compute or predict them
here:

- The amount of the bijdrage Zvw, whether provisional or final.
- Instalments, deadlines, and payment or refund timing for the voorlopige aanslag
  Zvw -- not established in the reviewed sources.
- Any exception regime named in the 2026 Fiscale informatie chapter: militairen
  in actieve dienst, deelvissers whose care costs are borne to a significant
  degree by another, a correction for foreign statutory health premiums, and the
  reduction for part-year Dutch insurance.
- Any oudedagsreserve release and its effect on the bijdrage-inkomen.

## Developer instruction

1. Raise the Zvw proactively in every 2026 provisional flow where the taxpayer
   has winst uit onderneming or income from work outside employment. Do not wait
   for the taxpayer to ask; most taxpayers do not know the second aanslag exists.
2. Tell the taxpayer, in the workpack, that there are two separate aanslagen
   with separate change routes. No reviewed source establishes whether a change
   to the income-tax voorlopige aanslag is coupled to the Zvw assessment, so the
   taxpayer checks the Zvw assessment separately and records what they find.
3. Ask the taxpayer directly: "Have you (the taxpayer) received a voorlopige
   aanslag Zorgverzekeringswet for 2026, and what income estimate does it use?"
   Record the answer with provenance. If the taxpayer does not know, record it as
   an open question -- do not assume there is none and do not assume nil income.
4. Where the taxpayer is changing their income-tax voorlopige aanslag because
   their expected profit moved, add an explicit action line: "You (the taxpayer)
   also check your voorlopige aanslag Zorgverzekeringswet 2026 in Mijn
   Belastingdienst and change it separately if its estimate is no longer right."
5. Quote the 2026 percentage (4.85%) and the maximumbijdrage-inkomen
   (EUR 79,409) from this note when explaining the bijdrage. Read them here;
   never restate them from memory.
6. Never print a maximum bijdrage amount, and never multiply the percentage by
   the ceiling in taxpayer-facing output. The Belastingdienst calculates the
   bijdrage.
7. Never treat the single income-tax estimate `onderneming.geschatte_winst` as
   the Zvw base. The bijdrage-inkomen is the belastbare winst, after
   ondernemersaftrek and mkb-winstvrijstelling; the income-tax estimate is the
   figure before them.
8. Never subtract the bijdrage Zvw from the profit estimate and never present it
   as a deduction.
9. Do not emit a field, a portal instruction, or a checklist row that has the
   taxpayer entering a Zvw amount in the income-tax voorlopige-aanslag form. The
   income-tax form has no Zvw field. Its field map must contain no Zvw field or
   value at all: no Zvw `field_id`, label, note, amount, baseline, estimate, or
   manual-entry row.
10. Phrase every portal step with an explicit human subject. This plugin never
    opens, operates, signs, or sends anything in Mijn Belastingdienst, and never
    asks for DigiD details; the taxpayer performs every authenticated action.
11. This is a 2026 provisional note. Do not import figures or outputs from any
    other tax year into this flow.
