# Rule note: Staking van de onderneming 2025

source_ids: bd_u_staakt_uw_onderneming, bd_stakingswinst_berekenen, bd_gedeeltelijke_doorschuiving_of_staking, bd_stakingsaftrek_2025, bd_stakingsaftrek_algemeen, bd_extra_lijfrenteaftrek_staking_2025, bd_desinvesteringsbijtelling_bij_staking, bd_doorschuiven_nieuwe_bestaande_onderneming, bd_overdracht_medeondernemer_werknemer, bd_oudedagsreserve_afrekenen, bd_rechtsvorm_wijzigen, bd_waar_moet_ik_me_uitschrijven, bd_btw_onderneming_wijzigen_of_beeindigen, bd_administratie_bewaren_2025, bd_loondienst_na_ondernemerschap, bd_urencriterium_2025, bd_stoppende_ondernemers, bd_fisin2025_h6_winst_uit_onderneming, law_wet_inkomstenbelasting_2001
workflow: annual_return
tax_year: 2025
status: active
last_reviewed: "2026-08-15"
review_status: reviewed

## Rule

This note is canonical for **recognising, explaining and routing** a staking
(cessation, sale or transfer of an onderneming) in the 2025 annual return. It is
deliberately **explain-only for the computation**: it tells the agent what a
staking is, what falls into the stakingswinst, which reliefs and
doorschuiffaciliteiten exist, what the taxpayer must arrange on deregistration,
and where every one of those items stops being preparable and becomes a
manual-review item. Nothing in this note authorises the agent to compute a
stakingswinst, a doorschuif outcome or a stakingslijfrente. The ordinary profit
of the year is computed in `winstberekening-2025.md` and `winst-en-kosten.md`;
the stakingsaftrek also appears as a component in `ondernemersaftrek.md`; the
stakingslijfrente maxima and the reeds opgebouwde voorzieningen are in
`inkomensvoorzieningen-2025.md`; the desinvesteringsbijtelling threshold and
percentage are in `investeringsaftrek.md`; the herinvesteringsreserve and the
kostenegalisatiereserve are in `afschrijving-en-bedrijfsmiddelen-2025.md`; the
oudedagsreserve run-down is in `winst-en-kosten.md`; the urencriterium is in
`ondernemer-criteria.md`. This note is annual 2025 only.

These are reference notes for workpack preparation -- not final tax advice.

## The explain-only boundary -- read this before anything else

- Belastingdienst guidance on ceasing a business tells the taxpayer plainly not
  to arrange everything alone and to get proper advice ("Laat u goed adviseren").
  Determining a stakingswinst is a fact-intensive valuation exercise that turns
  on the economic value of every asset, the goodwill actually realised, the
  reserves standing on the balance sheet and the history of earlier facilities.
  This plugin does not perform it.
- The agent's job in a staking year is: **recognise** the event, **explain** the
  components in the taxpayer's own words, **collect and record** the facts and
  documents, and **route** the computation to a tax adviser or accountant.
- Do not produce: a stakingswinst amount, a stille-reserve or goodwill valuation,
  a stakingsbalans, a doorschuif outcome, a stakingslijfrente premium, or a
  figure for the release of a fiscale reserve. Record the inputs instead.
- Never tell the taxpayer that a component is nil. Ask whether it exists and
  record the answer, including "not established yet".

## What counts as a staking

A staking is broader than closing the doors. All of the following fall under it:

| Situation | Treatment |
|-----------|-----------|
| You actually stop the business activities | staking |
| You sell the whole business | staking |
| You sell part of the business | gedeeltelijke staking (see below) |
| You transfer the business, for example to a child or an employee | staking -- transfer is treated as bedrijfsbeeindiging |
| The legal form or the samenwerkingsverband changes | in general a staking -- see the legal-form section |
| The ondernemer dies | staking by death (art. 3.58 Wet IB 2001) |

- There is no such thing as pausing. Temporarily stopping is not available: the
  tax obligations of the onderneming cannot be suspended for a while.
- Ceasing the business does not end the 2025 filing duty. You (the taxpayer)
  still file the 2025 aangifte inkomstenbelasting as an ondernemer, and you
  continue to file any return you are invited to file until the Belastingdienst
  confirms that your registration has been removed -- also for a period in which
  you had no activities at all.

## What the stakingswinst consists of

Stakingswinst is the profit realised as a direct result of ceasing (part of) the
onderneming: the difference between the boekwaarde of the onderneming and its
werkelijke waarde at the moment of transfer or cessation. On a sale it is the
difference between the verkoopprijs and the boekwaarde; on a move of assets into
private ownership it is the difference between the waarde in het economisch
verkeer and the boekwaarde.

Four groups make it up.

1. **Stille reserves.** The difference between the real value of a bedrijfsmiddel
   and its boekwaarde, typically because a bedrijfspand or a machine was
   depreciated below its real value. Stock and bedrijfsmiddelen that are given
   away or taken into private use must be settled in the same way, at their value
   at the moment of the change.
2. **Goodwill.** Goodwill built up inside the business normally carries no
   boekwaarde of its own, so a goodwill component in the transfer price falls
   into the stakingswinst in full. Ask whether the price contains a goodwill
   element and route the valuation to manual review. Note that purchased goodwill
   sitting on the balance sheet has its own boekwaarde and its own depreciation
   history in `afschrijving-en-bedrijfsmiddelen-2025.md`.
3. **The release of fiscale reserves.** Reserves on the balance sheet are lifted
   at cessation and added to the stakingswinst: the kostenegalisatiereserve, the
   herinvesteringsreserve, the oudedagsreserve, and a terugkeerreserve after an
   earlier geruisloze terugkeer out of a bv. On a gedeeltelijke staking a
   proportionate part is released. The mechanics of the first two reserves are in
   `afschrijving-en-bedrijfsmiddelen-2025.md`; the oudedagsreserve has its own
   section below.
4. **The desinvesteringsbijtelling.** Where a bedrijfsmiddel on which
   investeringsaftrek was claimed is sold, given away or taken into private use
   at the staking, and that happens within **5 years** after the **start** of the
   calendar year in which the investment was made, the stakingswinst must be
   increased by the desinvesteringsbijtelling. The disposal threshold, the
   percentage and the cap at the earlier deduction are stated in
   `investeringsaftrek.md` -- read them there, do not restate them from memory.

Boundaries to keep explicit:

- **The ordinary jaarwinst of the staking year is not stakingswinst.** The
  reliefs and the doorschuiffaciliteiten below attach to the stakingswinst only,
  never to the normal profit earned in the year the business stopped. Keep the
  two apart in the workpack.
- Stakingsaftrek and the extra lijfrentepremieaftrek apply only to profit earned
  as an ondernemer, never to profit earned as a medegerechtigde.
- A **stakingsbalans** is drawn up at the cessation date and the accounts run up
  to that date. Preparing it is manual review; the Fiscale informatie chapter on
  winst uit onderneming treats stakingswinst, stakingsbalans and
  desinvesteringsbijtelling together in its doorschuiven-of-staken section.

## Stakingsaftrek (art. 3.79 Wet IB 2001)

| Element | 2025 |
|---------|------|
| Stakingsaftrek | equal to the stakingswinst, but no more than **EUR 3,630** |
| Lifetime maximum | **EUR 3,630**, once in a lifetime |
| Reduction | the maximum is reduced -- but not below nil -- by stakingsaftrek enjoyed in earlier years |
| Unused remainder | stays available for a later staking |
| Whole ondernemingen only | art. 3.79 lid 1 covers profit made with or at the staking of one or more **gehele** ondernemingen |
| After a geruisloze doorschuiving | no stakingsaftrek if the onderneming has been continued geruisloos for **less than 3 years** |
| Medegerechtigde | no stakingsaftrek over profit earned as a medegerechtigde |

- The aftrek is capped twice over: at the stakingswinst actually realised, and at
  the EUR 3,630 lifetime ceiling as reduced by earlier use. Both caps bite; the
  lower one wins.
- Art. 3.79 lid 3: where the ondernemer continues a business that came to them
  under a doorschuiving on dissolution of a huwelijksgemeenschap (art. 3.59
  lid 2), on death (art. 3.62) or from another ondernemer (art. 3.63), the aftrek
  applies to gains from that business only if the business has been run for their
  account for at least three years.
- Art. 10a.29 lid 7: where a geruisloze doorschuiving or omzetting makes an
  oudedagsreserve fall free, stakingsaftrek can still apply, provided that without
  the doorschuiving there would have been a staking of a whole onderneming -- and
  subject to the same three-year condition.
- The article sets **no urencriterium condition** for the stakingsaftrek, unlike
  the zelfstandigenaftrek, the S&O-aftrek and the meewerkaftrek. Do not add one.
- **Ask the taxpayer whether stakingsaftrek has ever been claimed before, in any
  earlier year.** The lifetime ceiling cannot be applied without that answer, and
  it is not visible in the current year's figures. If the taxpayer does not know,
  record the question as open and route it -- do not treat earlier use as nil.

## Gedeeltelijke staking versus volledige staking

The distinction changes which reliefs are available, and the official pages give
no criteria for drawing the line. Treat the classification itself as manual
review.

| Item | Volledige staking | Gedeeltelijke staking |
|------|-------------------|-----------------------|
| Stakingsaftrek (art. 3.79) | available, subject to the caps above | not available -- the article requires one or more **gehele** ondernemingen |
| Extra lijfrentepremieaftrek (art. 3.129) | available | available -- the article and the Belastingdienst page both cover ceasing part of an onderneming |
| Fiscale reserves | released in full | a proportionate part is released |
| Oudedagsreserve | ends | ends in part |
| Doorschuiffaciliteiten | available in the listed cases | art. 3.63 lid 3 covers the transfer of **part** of a business, whether or not what is left behind is still an onderneming |

- The Belastingdienst page on (gedeeltelijke) doorschuiving or staking states no
  test for distinguishing a partial cessation from a full one, and says nothing
  about a maat or vennoot joining or leaving. Record the facts -- what was sold,
  what remains, whether the remaining activity is still carried on for the
  taxpayer's account -- and let the adviser classify.
- Never assert that a partial cessation has occurred because the taxpayer
  "stopped a line of work". Ask what happened to the assets, the clients and the
  contracts, and record the answers.

## Doorschuiffaciliteiten -- keep manual review

Under a doorschuiffaciliteit the tax claim on the stakingswinst is passed on
instead of settled: the successor continues with the existing boekwaarden and the
meerwaarde is not taxed at the staking. Every one of these requires a formal
verzoek, and two of them require a joint verzoek. None of them is automatic.

| Facility | What it covers | Term | Verzoek |
|----------|----------------|------|---------|
| Art. 3.62 -- staking door overlijden | acquirers under erfrecht or huwelijksvermogensrecht who directly continue or co-continue the onderneming; art. 3.58 then stays out of application | no term expressed in months | requested by the continuers **with the deceased taxpayer's return** |
| Art. 3.63 -- doorschuiving naar ondernemers | transfer to a medeondernemer who drew profit from the business as an ondernemer, or to a natural person who worked in it as an employee | the samenwerkingsverband or the employment must have run for the **36 months** immediately preceding the transfer; the term can be shortened by ministeriele regeling, for instance on arbeidsongeschiktheid or faillissement | **joint** verzoek by the transferor and the successor, filed with the transferor's return |
| Art. 3.64 -- doorschuiving via te conserveren inkomen | staking profit attributable to bedrijfsmiddelen and to a herinvesteringsreserve, where the taxpayer reinvests in another business from which they draw profit | reinvestment in the staking year or within **12 months** after the staking; extendable on request where the nature of the assets requires longer or special circumstances delayed it, provided a start has been made | verzoek made with the return; the Belastingdienst asks for it at the latest when the return for the staking year is filed |
| Art. 3.65 -- geruisloze omzetting in an nv or bv | continuing the business as an nv or bv; the founders must be entirely or almost entirely entitled to the share capital in the same proportion as they were to the business assets, and the ministeriele voorwaarden must be met | the shares may not be sold for **3 years** | verzoek by the taxpayer; the inspecteur decides by a beschikking that contains the conditions |

Further points that must survive into any explanation:

- Art. 3.64 rolls over the claim on **stakingswinst only**, never on the ordinary
  profit of the staking year. The permitted variants are all bedrijfsmiddelen
  plus the herinvesteringsreserve, one or more bedrijfsmiddelen plus that
  reserve, all bedrijfsmiddelen, one or more bedrijfsmiddelen, or only the
  herinvesteringsreserve.
- Art. 3.62 and art. 3.63 rollovers make the successor step into the transferor's
  place for the determination of profit -- the successor inherits the boekwaarden
  and the history, which is exactly why the three-year condition on the
  stakingsaftrek exists.
- Art. 10a.29 lid 6: a geruisloze omzetting does **not** carry an oudedagsreserve
  across into the bv. Lid 3, 4 and 5 give separate rollovers of the reserve on
  dissolution of the huwelijksgemeenschap, on death and on transfer to the
  partner. Where the medeondernemer or werknemer taking over the business is also
  the partner, the oudedagsreserve can be transferred under conditions, and
  **both** of you must file a verzoek.
- Where the successor has not yet paid the purchase price in full, uitstel van
  betaling can exist. That is a collection matter between the taxpayer and the
  Belastingdienst; record it as a question for the adviser.
- **Manual-review boundary:** the agent never decides that a facility applies,
  never drafts the verzoek, and never states the rolled-over amount. It records
  which facility the facts point at, which term is at stake, whose signature the
  verzoek needs, and that the verzoek belongs with the return.

## Stakingslijfrente -- explain only

- Art. 3.129 Wet IB 2001 lets an ondernemer who ceases an onderneming or part of
  one convert stakingswinst into a lijfrente and deduct the premium as an uitgave
  voor inkomensvoorzieningen. The deduction is capped by the stakingswinst
  realised, by a statutory maximum keyed to age and circumstances, and reduced by
  the reeds opgebouwde voorzieningen.
- The published maxima for 2025, the reeds opgebouwde voorzieningen list and the
  payment window are in `inkomensvoorzieningen-2025.md`. Read them there; this
  note does not repeat them.
- **Sizing a stakingslijfrente needs a pension history**, not just this year's
  figures: business and professional pension entitlements built at the expense of
  the winst, rights to bedrijfsbeeindigingsvergoedingen, the oudedagsreserve
  balance at the start of the year, lijfrente premiums and deposits deducted in
  earlier years, and amounts already used in an earlier conversion of
  stakingswinst. The agent cannot reconstruct that from a single year's
  administration.
- **Recorded conflict in the age brackets (risk R7).** The Belastingdienst year
  page keys the brackets to "62 jaar of ouder" and "tussen 52 jaar en 62 jaar";
  the Fiscale informatie chapter writes "61 jaar en 10 maanden of ouder"; the
  statute expresses the same brackets as at most five years and at most fifteen
  years below the AOW-leeftijd. **The Belastingdienst year pages are the wording
  used in this knowledge pack.** Tell the taxpayer that the published wordings do
  not match, keep the sizing manual, and recheck the brackets before the 2026
  season.
- The published amounts are ceilings, not entitlements. Never present a maximum
  as the amount this taxpayer can deduct.

## Oudedagsreserve at staking (overgangsrecht art. 10a.29)

- Building up an oudedagsreserve (FOR) has not been possible since 1 January
  2023. A reserve that existed at the end of 2022 may stay on the balance sheet
  and is wound down under the old artikelen 3.70 to 3.73 as they read on
  31 December 2022, kept alive by the overgangsrecht in art. 10a.29 Wet IB 2001.
- At staking the reserve is lifted and the amounts on which tax was deferred are
  added to the profit. Where the reserve is used to buy a lijfrente, the premium
  is deductible from the inkomen uit werk en woning, and the taxation shifts to
  the future lijfrente payments. Do not present that as a guaranteed net-nil
  outcome for this taxpayer.
- The mandatory release outside a full settlement reaches only the **excess** of
  the reserve over the ondernemingsvermogen, and only in the listed situations --
  whole or partial staking, having reached the AOW-leeftijd on 1 January of the
  year, or failing the urencriterium in both this and the preceding calendar year.
  Computing that excess requires the ondernemingsvermogen as the old art. 3.71
  defined it and is manual review.
- A voluntary release matched by a lijfrente purchase and a mandatory release are
  not treated the same way for the Zorgverzekeringswet. Record which one occurred
  and read `zvw-2025.md`.
- The conversion premium has its own six-month election in the return; the window
  and the deadline are in `inkomensvoorzieningen-2025.md`.
- **Ask whether an oudedagsreserve stood on the opening balance sheet, and for
  its balance at the start of the year.** Never assume the reserve is nil, and
  never compute the release.

## Change of legal form or partnership -- manual review

The Belastingdienst treats a change of rechtsvorm or samenwerkingsverband **in
general as a staking of your entrepreneurial activities**: the balance sheet is
drawn up and settled, and the new form counts as a newly started onderneming.
Whether there is in fact a staking depends on many factors, and under conditions
there is no need to settle.

Triggers:

- You bring your eenmanszaak into a newly formed or existing vof, maatschap, bv
  or nv.
- A maat or vennoot joins your vof, cv or maatschap.
- A maat of your maatschap or a vennoot of your vof or cv falls away, for
  instance by uittreding or overlijden.

Consequences that reach beyond the inkomstenbelasting:

- **Btw.** A change of rechtsvorm or samenwerkingsverband means a **new
  onderneming for the btw**. A new btw-identificatienummer may follow, and you
  (the taxpayer) must pass it to your suppliers in other EU countries
  immediately.
- **Loonheffingen.** The payroll administration must be closed off and
  re-registered, and a new loonheffingennummer may follow.
- **Overdrachtsbelasting.** For onroerende zaken in the business assets there is
  usually no overdrachtsbelasting on such a change, but this is a separate
  assessment.
- **Geruisloze omzetting into a bv** requires bringing in the whole onderneming,
  and the shares may not be sold for 3 years.
- Any doorschuiffaciliteit here needs a verzoek to the belastingkantoor that
  handles your inkomstenbelasting.

**Manual-review boundary:** partnerships and legal-form changes are outside the
preparable scope of this plugin. The agent records the change, the date, the
parties and the three consequence areas above, then routes the whole case --
including the question whether a staking occurred at all -- to a tax adviser.

## Stopping mid-year and going into loondienst

- In the year you stop, you (the taxpayer) still file the aangifte
  inkomstenbelasting **as an ondernemer**, and you report two kinds of income:
  the winst over the part of the year in which you were an entrepreneur --
  including any stakingswinst -- and the loon from the employment, on which the
  employer withheld loonheffingen and which is often already filled in.
- Aftrekposten can still apply in the stopping year. Check them one by one and
  watch the hours actually spent; do not drop them because the year was partial,
  and do not grant them because the year started as a normal business year.
- **The urencriterium is not recomputed and not pro-rated.** The ondernemersaftrek
  requires at least **1,225 hours** in the calendar year spent on the
  onderneming(en). You may not recalculate the 1,225 hours to the period in which
  you were an ondernemer. The threshold is absolute, whether the business ran for
  two months or twelve. The second condition -- more time on the onderneming than
  on other work such as loondienst -- and the starter exception are in
  `ondernemer-criteria.md`.
- Ask for the hours administration for the whole calendar year, not for the
  trading period, and record the total actually reached rather than an estimate.

## Deregistration checklist -- an explicit human subject throughout

Every step below is performed by the taxpayer or an authorised human. This plugin
never opens or operates a portal, never logs in, and never files or signs
anything.

1. **KVK.** If your onderneming is registered at KVK, you (the taxpayer)
   deregister it at KVK, and KVK passes that on to the Belastingdienst. How you
   deregister depends on the rechtsvorm; KVK publishes a checklist for stopping a
   business.
2. **Belastingdienst.** If your onderneming is **not** registered at KVK, you
   notify the Belastingdienst in writing yourself that you are stopping. Take the
   postal address and the details from the Belastingdienst page on where to
   deregister; state the numbers the page asks for.
3. **Wait for the confirmation of the afvoer.** You receive a confirmation that
   your loonheffingennummer and/or your btw-identificatienummer has been removed.
   Deregistration takes time: **until you have that confirmation, you keep filing
   every return you are invited to file, even if you had no activities.** Not
   filing risks naheffingsaanslagen and boetes.
4. **The final btw-aangifte.** Do not forget it. Stock and business assets that
   you do not hand over move to your private assets, which counts as a supply by
   you as an ondernemer to yourself as a private person; where btw was deducted on
   purchase, btw is due on that deemed supply, valued at the value of the goods at
   the moment you start using them privately. No btw is charged on the transfer of
   an algemeenheid van goederen -- a business or an independent part of it that
   the buyer continues.
5. **Onroerende zaken.** Btw herziening can apply where btw was paid on purchase
   and the property is sold within **10 years**. On the transfer of a totality of
   goods no revision is needed at that moment; the revision period continues with
   the acquirer.
6. **Eenloketsysteem (One Stop Shop).** If you used it, deregister there before
   the KVK deregistration and before your eHerkenning access ends, otherwise the
   final OSS filings can become impossible.
7. **Close the administration** and prepare the accounts up to the cessation date.
8. **Bewaarplicht.** Keep the administratie for **7 years** (basisgegevens such
   as the grootboek, the debtor and creditor administration, the stock
   administration, the purchase and sales administration and the loonadministratie),
   and **10 years** for data on onroerende zaken and for eenloketsysteem data. The
   duty survives the end of the business; keep the hours administration that
   supports the urencriterium for the same period.

## Developer instruction

1. **Detect the event first.** Ask whether the taxpayer sold, transferred, ceased
   or partly ceased an onderneming during 2025, whether a maat or vennoot joined
   or left, whether the rechtsvorm changed, and whether an ondernemer died. A yes
   to any of these makes the whole return a manual-review case for the winst
   part; say so at once rather than at the end.
2. **Never compute a stakingswinst.** Do not value stille reserves or goodwill,
   do not build a stakingsbalans, do not release a reserve, do not net a
   doorschuiving. Produce a facts-and-documents record and a clear statement that
   the computation belongs with a tax adviser or accountant.
3. **Collect these facts explicitly**, one question at a time, and record "not
   established" where the taxpayer does not know: the cessation or transfer date;
   what was sold and what remains; the buyer or successor and their relationship
   to the taxpayer; whether the price contains goodwill; which fiscale reserves
   stood on the opening balance sheet and their balances; which bedrijfsmiddelen
   carried investeringsaftrek and in which year; which assets moved into private
   ownership; and the taxpayer's date of birth and health status where a
   stakingslijfrente is in play.
4. **Ask whether stakingsaftrek was claimed in any earlier year.** Read the
   EUR 3,630 maximum from the table above rather than from memory, present it as a
   ceiling capped at the stakingswinst and reduced by earlier use, and record the
   three-year condition after a geruisloze voortzetting. Never state a
   stakingsaftrek amount without the stakingswinst, which this plugin does not
   compute.
5. **Route every doorschuiffaciliteit to manual review**, but name the one the
   facts point at, state the term (36 months, 12 months, the 3-year share lock)
   and state whose verzoek is needed and that it belongs with the return. Do not
   assert that a facility applies and do not draft it.
6. **Keep the stakingslijfrente explain-only.** Point at
   `inkomensvoorzieningen-2025.md` for the maxima, tell the taxpayer the age
   brackets are published in wordings that do not match each other, say that the
   Belastingdienst year pages are the wording used here, and ask for the pension
   history rather than estimating it.
7. **Ask about the oudedagsreserve separately** -- whether one stood on the
   opening balance sheet and what its balance was at the start of the year -- and
   record whether any release was voluntary or mandatory, because `zvw-2025.md`
   needs that answer. Never assume the reserve is nil.
8. **Do not restate figures owned elsewhere.** The desinvesteringsbijtelling
   threshold and percentage come from `investeringsaftrek.md`; the reserve
   mechanics from `afschrijving-en-bedrijfsmiddelen-2025.md`; the stakingslijfrente
   maxima from `inkomensvoorzieningen-2025.md`; the urencriterium conditions from
   `ondernemer-criteria.md`.
9. **In a stopping year, hold the urencriterium at 1,225 hours.** If the taxpayer
   or a document suggests pro-rating it to the trading period, correct that
   explicitly and record the full-year hours.
10. **Portal and deregistration steps always name a human subject.** Write "You
    (the taxpayer) deregister at KVK", "You file the final btw-aangifte". The
    plugin never opens Mijn Belastingdienst, never logs in, never enters or
    submits anything, and never performs a deregistration.
11. **Collect only what the record needs.** Do not record a BSN, and do not copy
    bank account numbers or counterparty identifiers out of a sale agreement,
    beschikking or balance sheet.
12. **Recheck before the 2026 season.** The stakingsaftrek maximum, the
    stakingslijfrente maxima and the age-bracket wording are reset and republished
    each year; the doorschuif terms and the bewaarplicht are not year figures but
    confirm them when the reviewed sources are refreshed.
