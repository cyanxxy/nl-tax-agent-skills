# Rule note: Verlies uit onderneming en verliesverrekening 2025

source_ids: bd_verlies_uit_onderneming, bd_fisin_2025_h25, bd_verrekenen_ngz, bd_middeling_aanvragen, bd_middeling_teruggaaf, bd_zelfstandigenaftrek_2025, law_besluit_ngz_staking, law_wet_inkomstenbelasting_2001
workflow: annual_return
tax_year: 2025
status: active
last_reviewed: "2026-08-15"
review_status: reviewed

## Rule

This note is canonical for what happens to a negative result in the 2025 annual
return: how an ondernemingsverlies is absorbed inside 2025 itself, how a
remaining verlies uit werk en woning is carried back and forward, how the
Belastingdienst fixes both by beschikking, and how niet-gerealiseerde
zelfstandigenaftrek (NGZ) is created and later settled. It also records that
middeling is abolished, so the agent refuses a middeling request for 2025
instead of quietly skipping it. The amounts that produce the loss are computed
in `winst-en-kosten.md`, `investeringsaftrek.md`, `ondernemersaftrek.md` and
`mkb-winstvrijstelling.md`; the winst cap that creates NGZ is stated in
`ondernemersaftrek.md` and the starter case that disapplies that cap is in
`aanloopfase-en-starters-2025.md`. This note is annual 2025 only.

These are reference notes for workpack preparation -- not final tax advice.

## Step 1 -- netting inside 2025 comes first

A business loss is not carried anywhere until the rest of box 1 for the same
year has absorbed it.

- A negative result from the onderneming is first set off against the taxpayer's
  own positive box 1 income of the same calendar year, such as loon. Only what
  remains after that netting is a verlies uit werk en woning that can travel to
  another year. The Belastingdienst illustrates this on the verlies uit
  onderneming page with a loss partly absorbed by loon of the same year.
- Art. 3.148 lid 1 Wet IB 2001: a negative inkomen uit werk en woning is a
  verlies uit werk en woning. Lid 2: a negative belastbare winst uit onderneming
  counts as ondernemingsverlies, but never for more than the verlies uit werk en
  woning of that same year. The ondernemingsverlies is therefore a subset of the
  box 1 loss, not a second, separate loss.
- A box 1 loss is never set off against box 2 (aanmerkelijk belang) or box 3
  (sparen en beleggen) results.
- Losses are strictly personal. A loss cannot be set off against the income of
  the fiscal partner. The single statutory exception (art. 3.150 lid 6, an
  unused loss arising from the allocation of gemeenschappelijke
  inkomensbestanddelen where the partnership ends by the taxpayer's death) is a
  manual-review item.

## Step 2 -- carry-back and carry-forward of a 2025 loss

| Element                          | Rule in force for a 2025 loss                        |
|----------------------------------|------------------------------------------------------|
| Carry-back                       | the 3 preceding calendar years                        |
| Carry-forward                    | the 9 following calendar years                        |
| Sequence between the two         | the 3 preceding years first, then the 9 following     |
| Sequence inside the carry-back   | oldest year first                                     |
| Set-off order in general         | in the order the losses arose and the incomes were enjoyed |

- Art. 3.150 lid 1: "Het verlies uit werk en woning wordt verrekend met de
  inkomens uit werk en woning van de drie voorafgaande en de negen volgende
  kalenderjaren." Lid 5 fixes the order: losses are used in the order in which
  they arose, against incomes in the order in which they were enjoyed.
- Applying that to a loss of the 2025 tax year: the three preceding years are
  2022, 2023 and 2024, and the nine following years run from 2026 through 2034.
- Looking the other way, positive 2025 income can absorb losses from earlier
  years. For the aangifte inkomstenbelasting 2025 the offsettable loss years run
  over the period 2016 through 2024.
- Set-off is not optional and not free-form: the taxpayer cannot choose to skip a
  year to save the loss for a better one.

## Step 3 -- the verliesbeschikking

A loss is only usable once the inspecteur has set it by beschikking. Until then
there is no amount to carry anywhere.

- Art. 3.151 lid 1: the inspecteur fixes the verlies uit werk en woning "bij voor
  bezwaar vatbare beschikking". Lid 2: the ondernemingsverlies is fixed in that
  same beschikking. Lid 3: both amounts are stated separately on the
  aanslagbiljet.
- Carry-back is effected by a separate voor bezwaar vatbare beschikking reducing
  the earlier year's aanslag (art. 3.152 lid 1), issued at the same time as the
  aanslag for the loss year (lid 2). Carry-forward is likewise formalised by
  beschikking, issued with the aanslag of the year against which the loss is set
  off (art. 3.153 lid 1-3).
- Both the loss beschikking and the verrekening beschikking are open to bezwaar.
- Art. 3.151 lid 4-6 allows herziening if the loss was set too high, except where
  the inspecteur knew or could reasonably have known the relevant fact and the
  taxpayer did not act te kwader trouw.
- The remaining offsettable loss is shown on the verliesbeschikking received with
  the definitieve aanslag. That document, not the agent's own arithmetic, is the
  source of any carried-forward amount used in the 2025 workpack.
- Art. 3.152 lid 3: where no aanslag exists for a preceding year that the
  carry-back would reach, the inspecteur invites the taxpayer to file a return
  for that year.

## Step 4 -- voorlopige verliesverrekening (capped at 80%)

The taxpayer can ask for part of the carry-back to be paid out before the
definitieve aanslag for the loss year exists.

- The request is made in writing when the return for the loss year is filed, and
  is itself fixed by beschikking.
- Condition stated by the Belastingdienst: "U doet aangifte over het
  verliesjaar."
- The aanslag of the year the loss is set off against must already be
  definitief.
- Order within the carry-back: first the third preceding year, then the second
  preceding year, then the preceding year.
- **Cap: at most 80% of the declared loss is settled this way.** The remaining
  part waits for the definitieve aanslag.
- The earlier voorlopige verliesverrekening is taken into account when the
  definitieve aanslag for the loss year is set, so it is an advance, not an extra
  entitlement.

## Step 5 -- verdamping

Losses that cannot be set off within the carry-back and carry-forward periods
verdampen: they lapse and are gone. Nothing extends the nine-year forward period
except the gemoedsbezwaren variant in the manual-review section below. Record
the year each carried-forward loss arose so the expiry year is visible in the
workpack.

## A loss year still requires a return

Filing does not become optional because the year was negative:

- The verlies uit werk en woning and the ondernemingsverlies are set by
  beschikking, and that beschikking is issued with the aanslag for the loss year
  (art. 3.151, art. 3.152 lid 2). No return means no aanslag, no beschikking and
  therefore no usable loss.
- Voorlopige verliesverrekening explicitly requires a return over the loss year.
- Whether the taxpayer has an invitation to file (aangiftebrief) and what
  deadline applies is in `../annual/filing-flow.md`; a loss does not change those
  rules.

## Niet-gerealiseerde zelfstandigenaftrek (NGZ)

NGZ is a separate carry-forward from the loss rules above. It is created by the
winst cap on the zelfstandigenaftrek, not by a loss.

- **How it arises.** Art. 3.76 lid 5: the zelfstandigenaftrek is no more than the
  amount of the winst. The part that cannot be used because of that cap is
  designated niet-gerealiseerde zelfstandigenaftrek. Where the taxpayer is
  entitled to the startersaftrek increase of art. 3.76 lid 3, the cap does not
  apply at all, so no NGZ arises in that year -- see
  `aanloopfase-en-starters-2025.md`.
- **Official worked example (2025).** Winst before the zelfstandigenaftrek
  EUR 1,500; entitlement to the zelfstandigenaftrek EUR 2,470; the aftrek is
  capped at EUR 1,500 so the winst after aftrek is EUR 0; the niet-gerealiseerde
  zelfstandigenaftrek is EUR 2,470 minus EUR 1,500 = **EUR 970**. The EUR 2,470
  is the 2025 zelfstandigenaftrek from `ondernemersaftrek.md`.
- **Set by beschikking.** Art. 3.76 lid 6: the inspecteur fixes the NGZ amount
  "bij voor bezwaar vatbare beschikking", shown separately on the aanslagbiljet.
- **Carry-forward.** Art. 3.76 lid 7: NGZ is settled in the following **nine**
  calendar years, in the order in which it arose (oldest first), by taking an
  increase of the zelfstandigenaftrek in those years.
- **Only in a year with enough winst.** The increase in a later year is at most
  the amount by which that year's winst exceeds that year's zelfstandigenaftrek.
  Set-off therefore also requires entitlement to the zelfstandigenaftrek in the
  set-off year, and so the urencriterium in that year.
- **Not automatic.** The Belastingdienst states that the taxpayer must track what
  has already been settled and enter the amount in the aangifte, "dat gebeurt
  namelijk niet automatisch". The agent must ask for the NGZ beschikking and read
  the balance off it.
- Art. 3.76 lid 8-9: a later set-off is itself formalised by voor bezwaar vatbare
  beschikking issued with the aanslag of the set-off year, stated separately on
  the aanslagbiljet.
- Art. 3.76 lid 5, closing sentence: if the cap reduces the zelfstandigenaftrek
  to nil, that calendar year still counts as a year in which the
  zelfstandigenaftrek was applied when counting the startersaftrek conditions.
- Art. 3.76 lid 10: "winst" for this article is the combined profit the taxpayer
  enjoys as ondernemer from one or more ondernemingen.

## Middeling is abolished -- refuse the request

Middeling is not available for 2025 and the agent must say so explicitly rather
than ignoring the request.

- Afdeling 3.14 Wet IB 2001 (art. 3.154 and art. 3.155) is marked "Vervallen per
  01-01-2023". No substantive text remains.
- Art. 10a.28 keeps the old afdeling 3.14 alive only "op verzoeken om een
  middelingsteruggaaf over een middelingstijdvak waartoe het kalenderjaar 2022 of
  een daaraan voorafgaand kalenderjaar behoort". A middelingstijdvak is three
  consecutive calendar years, so the latest possible tijdvak is **2022-2023-2024**
  and no tijdvak beginning in 2023 or later qualifies.
- Consequence: **2025 can never be part of a middelingstijdvak, and neither can
  2026.** Do not build, estimate or promise a middeling result in a 2025
  workpack.
- Residual period facts, for explaining the refusal accurately:

| Element                    | Rule                                                          |
|----------------------------|---------------------------------------------------------------|
| Last possible tijdvak      | 2022, 2023 and 2024                                            |
| Structure                  | 3 consecutive calendar years; a year may be used only once     |
| Precondition               | all three years must have a definitieve aanslag                |
| Drempelbedrag              | EUR 545; only the excess above it is refunded                  |
| Deadline                   | at most 36 months after the last definitieve aanslag of the 3 years becomes final |
| When an aanslag is final   | once the bezwaartermijn of 6 weeks has passed                  |
| Decision term              | within 8 weeks of receipt of the request                       |
| A loss year in the sum     | negative income counts as EUR 0 in the middeling calculation   |

- The request is a paper form that you (the taxpayer) sign and post to your
  belastingkantoor. The plugin never files it and never signs anything.

## Manual-review boundaries

Record the facts, do not compute, and route these to manual review:

1. **Gemoedsbezwaren -- the 8-year carry-back.** Art. 3.150 lid 3-4: for a
   taxpayer with a gemoedsbezwaren exemption under art. 64 lid 1 sub a Wfsv who
   elects this in the aangifte, the three-year carry-back term is extended to
   eight years, but only for ondernemingsverliezen attributable to costs of
   damage from risks that comparable taxpayers usually insure. Both the exemption
   and the attribution of the loss to such damage are facts to confirm with the
   taxpayer, not to assume.
2. **Art. 14c ring-fencing.** Art. 3.150 lid 7: an ondernemingsverlies deemed
   incurred by the continuing shareholder under art. 14c lid 3 Wet Vpb 1969
   (geruisloze terugkeer uit een bv) is set off "uitsluitend met de winst uit de
   voortgezette onderneming". A loss inside this ring-fence is not general box 1
   loss and must never be netted against loon or other box 1 income.
3. **An unknown historical NGZ balance.** If the taxpayer cannot produce the NGZ
   beschikking, do not reconstruct the balance from old profit figures and do not
   enter a figure. Ask the taxpayer to retrieve the beschikking; if it cannot be
   retrieved, mark the NGZ as not established and leave it out of the workpack
   totals with an explicit note.
4. **NGZ after death of the ondernemer.** A besluit (BWBR0037558) approves that
   where the ondernemer dies, the business is thereby staked and the urencriterium
   is failed in that year, the carried-forward NGZ may still be deducted from the
   profit made with or on staking of the whole onderneming, only so far as that
   stakingswinst is sufficient, and not from the jaarwinst of the year of staking.
   This is a bereavement and staking case: manual review.
5. **Partner-related loss transfer** on the death of the taxpayer
   (art. 3.150 lid 6).

## Developer instruction

1. Ask the taxpayer directly whether 2025 produced a negative result, and ask for
   any verliesbeschikking and NGZ beschikking they already hold. Never assume the
   answer is zero and never assume no earlier loss exists.
2. Net a 2025 ondernemingsverlies against the taxpayer's own other positive
   box 1 income of 2025 first, and show that netting step in the workpack before
   any carry-back or carry-forward is discussed. Never net against box 2 or
   box 3, and never against the fiscal partner's income.
3. Present the carry-back and carry-forward as the 3-then-9 sequence with oldest
   year first, and state the expiry year of every carried-forward loss so
   verdamping is visible. Read the periods from this note; do not paraphrase them
   from memory.
4. Treat any carried-forward loss amount as data that comes from the
   verliesbeschikking. If the taxpayer cannot supply the beschikking, record the
   loss as not established and route it to manual review rather than estimating
   it.
5. If the taxpayer asks about getting money back early, explain voorlopige
   verliesverrekening: it is requested in writing with the return for the loss
   year, the earlier year's aanslag must already be definitief, the order is
   third preceding year first, and at most 80% of the declared loss is settled.
   Do not present the 80% as the final outcome.
6. Tell the taxpayer that a loss year still needs a return, because the loss only
   becomes usable once it is set by beschikking with the aanslag for that year.
7. For NGZ: read the balance off the beschikking, apply it only in a year whose
   winst exceeds that year's zelfstandigenaftrek, settle oldest first, and state
   that the amount is not applied automatically -- you (the taxpayer) enter it
   yourself in the aangifte in Mijn Belastingdienst. Read the zelfstandigenaftrek
   amount for the year in question from that year's own knowledge note; do not
   carry the 2025 amount into another year.
8. If the taxpayer asks for middeling, refuse and explain: the regeling lapsed on
   1 January 2023 and the last possible period is 2022-2023-2024, so 2025 and
   2026 can never be included. Do not silently drop the request, and do not
   produce a middeling estimate.
9. Route the gemoedsbezwaren 8-year variant, art. 14c ring-fenced losses, an
   unretrievable NGZ balance, and the NGZ-at-death case to manual review with the
   facts recorded.
10. Every portal action stays with the human: you (the taxpayer) open Mijn
    Belastingdienst, enter the loss and NGZ figures, and submit. The plugin
    prepares the figures and never logs in, enters, or sends anything.
