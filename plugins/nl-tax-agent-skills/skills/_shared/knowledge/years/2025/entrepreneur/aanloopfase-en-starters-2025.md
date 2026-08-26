# Rule note: Aanloopfase en startende ondernemers 2025

source_ids: bd_kosten_aanloopfase, bd_urencriterium_2025, bd_startersaftrek_2025, bd_zelfstandigenaftrek_2025, bd_startersaftrek_ao_2025, bd_vermogensetikettering, bd_willekeurige_afschrijving_starters, bd_willekeurige_afschrijving_algemeen, law_uwa_2001, law_uitvoeringsregeling_ib_2001, law_wet_inkomstenbelasting_2001
workflow: annual_return
tax_year: 2025
status: active
last_reviewed: "2026-08-15"
review_status: reviewed

## Rule

This note is canonical for the starter-specific parts of the 2025 annual return:
costs made in the aanloopfase before the enterprise started, assets acquired
before the start, how the urencriterium works in a first partial year, the two
starter reliefs (startersaftrek and startersaftrek bij arbeidsongeschiktheid),
and willekeurige afschrijving voor startende ondernemers. The general
ondernemer test lives in `ondernemer-criteria.md`; the amounts and ordering of
the ondernemersaftrek live in `ondernemersaftrek.md`; ordinary cost rules live in
`winst-en-kosten.md`; the KIA and the other investeringsaftrek forms live in
`investeringsaftrek.md`; a loss created by the starter reliefs is handled in
`verlies-en-verrekening-2025.md`. This note is annual 2025 only.

These are reference notes for workpack preparation -- not final tax advice.

## Aanloopkosten -- costs made before the enterprise started

**Legal basis.** Art. 3.10 Wet IB 2001 delegates the rule; art. 5
Uitvoeringsregeling inkomstenbelasting 2001 contains the operative text.

Art. 5 in full: "Bij het bepalen van de winst van het eerste kalenderjaar als
ondernemer komt mede in aftrek het totale bedrag van de kosten en lasten die zijn
gemaakt in de vijf daaraan voorafgaande kalenderjaren en die verband houden met
het starten van de onderneming, voorzover: a. er in die periode geen opbrengsten
tegenover hebben gestaan en b. zij niet ten laste van het belastbaar inkomen uit
werk en woning kunnen of konden worden gebracht."

| Element              | Rule                                                          |
|----------------------|---------------------------------------------------------------|
| Look-back period     | the 5 calendar years immediately preceding the first calendar year as ondernemer |
| Deducted in          | the **first** calendar year as ondernemer, in one go            |
| Condition a          | no revenues stood against those costs during that period        |
| Condition b          | the costs could not be, and could not have been, charged against belastbaar inkomen uit werk en woning |
| Formal requirement   | neither art. 3.10 nor art. 5 prescribes a separate verzoek or a voor bezwaar vatbare beschikking |

- The deduction is taken when determining the profit of the first calendar year
  as ondernemer. It is not spread over the aanloop years and it is not obtained
  by reopening those earlier years.
- Consequence for a 2025 workpack: aanloopkosten belong in the 2025 return only
  when **2025 is the taxpayer's first calendar year as ondernemer**. In that case
  the look-back covers the calendar years 2020 through 2024. If the first year as
  ondernemer was earlier, the aanloopkosten belonged in that earlier year and
  cannot be moved into 2025.
- Which costs qualify: the Belastingdienst states that all costs made from a
  business viewpoint for an onderneming are deductible, and that this includes
  costs made with the clear intention of bringing an enterprise into being --
  "kosten dus die u hebt gemaakt voordat de onderneming van start ging". The
  examples named on that page are a marktverkenning and ingewonnen adviezen.
- Condition b is the trap in practice. If the activity was already a bron van
  inkomen and the costs were already deducted, for instance as costs against
  resultaat uit overige werkzaamheden, they cannot be claimed again as
  aanloopkosten. Ask what was reported in each of the five preceding years.
- The Belastingdienst page on the aanloopfase does not itself state the five-year
  limit and does not use the word "aanloopverliezen"; that period comes from
  art. 3.10 and art. 5. Cite the statute for the period, the page for the scope.
- Hours count too: hours spent on the enterprise before registering as an
  ondernemer count towards the minimum hours for, among other things, the
  zelfstandigenaftrek, provided the taxpayer kept an urenregistratie.
- Btw is a separate track: btw paid in the aanloopfase can, under conditions, be
  deducted as voorbelasting in the btw-aangifte. That is a btw question, not an
  inkomstenbelasting deduction, and it is out of scope for this workpack.

### Evidence to ask for

Ask the taxpayer for, per cost item: a dated invoice or receipt in their name,
what the cost was for and how it relates to starting this enterprise, the
calendar year in which it was made, whether anything was earned in that period
against it, and whether it was already deducted in an earlier return. Costs
without a document, or costs whose business purpose the taxpayer cannot explain,
are not entered as a figure -- they go to manual review.

## Assets acquired before the start

An asset bought before the enterprise started is not a running cost and is not
absorbed by the aanloopkosten deduction. It enters the enterprise as a
bedrijfsmiddel, and the first question is vermogensetikettering.

- **10% or less business use: verplicht privevermogen.**
- **90% or more business use: verplicht ondernemingsvermogen.**
- Anything in between is keuzevermogen: the ondernemer may generally choose, but
  the choice must stay "binnen redelijke grenzen".
- Cars follow their own variant: verplicht ondernemingsvermogen at 90% or more
  business use, or where the business kilometres exceed the private kilometres
  and no more than 500 private kilometres are driven per year; verplicht
  privevermogen at 90% or more private use; otherwise keuzevermogen.
- A keuzevermogen choice can generally be revised until the aanslag for the year
  of the choice is onherroepelijk; afterwards only on proof of a bijzondere
  omstandigheid.
- **Opening value is a manual-review item.** The retrieved official guidance
  states the labelling rules but does not state how a pre-start asset is valued
  when it is brought into the enterprise. Ask the taxpayer for the purchase
  invoice, the purchase date and the condition of the asset, record them, and
  route the opening value and the depreciation schedule to manual review. Do not
  invent an opening value and do not assume the historic purchase price.
- Depreciation itself follows `winst-en-kosten.md`; the willekeurige afschrijving
  variant for starters is at the end of this note.

## Urencriterium in a first partial year

**The 1,225 hours are absolute. They are not pro-rated for a mid-year start.**
This is the single most common starter misconception and the agent must correct
it before any zelfstandigenaftrek or startersaftrek is presented.

- Art. 3.6 lid 1: the urencriterium is spending at least 1,225 hours in the
  calendar year on work for one or more ondernemingen. The article contains no
  apportionment for a partial first year.
- The Belastingdienst states it plainly: "U mag niet de 1.225 uren herrekenen
  naar de periode dat u ondernemer bent." Its worked example is a business
  started on 1 July: six months as ondernemer, still at least 1,225 hours
  required.
- Second condition (the grotendeels test, art. 3.6 lid 1 sub a): more time must
  be spent on the onderneming(en) than on other work, for example loondienst.
- **Starter exemption from the grotendeels test** (art. 3.6 lid 1 sub b): the
  second condition does not apply where the taxpayer was not an ondernemer in one
  or more of the five preceding calendar years. **For 2025 that window is one of
  the years 2020 through 2024.** The 1,225-hour condition itself is never waived.
- The threshold is measured over all of the taxpayer's ondernemingen together.
- All hours spent on the enterprise count, not only billable hours -- writing
  quotes, doing the administration and building the business website count.
  Standby time in which no work is done does not count.
- Hours spent on the enterprise before registering as an ondernemer count as
  well, provided they are recorded (see the aanloopfase section above).
- Pregnancy interruption: non-worked hours over a total of 16 weeks still count
  as worked hours (art. 3.6 lid 5). This applies to the verlaagd urencriterium
  too.
- Samenwerkingsverband exclusion (art. 3.6 lid 2-4): hours do not count where the
  taxpayer performs 70% or more ondersteunende werkzaamheden in an ongebruikelijk
  samenwerkingsverband with verbonden personen, or where the samenwerkingsverband
  serves an enterprise from which only a verbonden persoon draws profit. Any
  samenwerkingsverband is a manual-review item.
- **Verlaagd urencriterium: at least 800 hours.** It is not an alternative to the
  1,225 hours in general -- it exists as a condition for the startersaftrek bij
  arbeidsongeschiktheid below.

## Startersaftrek (art. 3.76 lid 3)

The startersaftrek is not a separate ondernemersaftrek component; it is an
increase of the zelfstandigenaftrek.

| Element                          | 2025                                            |
|----------------------------------|-------------------------------------------------|
| Startersaftrek                   | **EUR 2,123** on top of the zelfstandigenaftrek  |
| At AOW-leeftijd at the start of the year | **EUR 1,062**                            |
| Frequency                        | at most 3 times in the first 5 years as ondernemer |

Cumulative conditions, all of which must hold:

1. Entitlement to the zelfstandigenaftrek -- so the full 1,225-hour urencriterium
   applies indirectly.
2. The taxpayer was not an ondernemer for the inkomstenbelasting in one or more
   of the five preceding calendar years (for 2025: in one or more of 2020
   through 2024).
3. The zelfstandigenaftrek was applied at most **twice** in those five preceding
   calendar years.
4. There was no geruisloze terugkeer uit een bv (art. 14c Wet Vpb 1969) in the
   calendar year itself or in one of the five preceding calendar years.

Further rules:

- **No opt-out.** The taxpayer cannot claim the zelfstandigenaftrek for a year
  while declining the startersaftrek; it is added automatically.
- The AOW halving of art. 3.76 lid 4 covers lid 2 and lid 3 together, so the
  startersaftrek is halved as well. The Belastingdienst publishes the AOW-age
  startersaftrek as **EUR 1,062**, and that is the figure to use rather than a
  self-computed half; `ondernemersaftrek.md` makes the same point. The AOW-age
  test itself is in `../../../aow/aow-leeftijd.md`.
- **The winst cap on the zelfstandigenaftrek is disapplied.** Art. 3.76 lid 5,
  second sentence: the cap "is niet van toepassing op een ondernemer die in
  aanmerking komt voor de verhoging van de zelfstandigenaftrek, bedoeld in het
  derde lid." So in a startersaftrek year the zelfstandigenaftrek and the
  startersaftrek together may exceed the winst and create a loss, and no
  niet-gerealiseerde zelfstandigenaftrek arises. The Belastingdienst confirms the
  outcome: the resulting loss is set off against other werk-en-woning income or
  against other years, which is `verlies-en-verrekening-2025.md`.
- Counting rule for condition 3: art. 3.76 lid 5 closes by providing that a year
  in which the winst cap reduced the zelfstandigenaftrek to nil still counts as a
  year in which the zelfstandigenaftrek was applied. A nil year is therefore not
  a free year.

## Startersaftrek bij arbeidsongeschiktheid (art. 3.78a)

A separate ondernemersaftrek component for a starting ondernemer who receives an
arbeidsongeschiktheidsuitkering and cannot reach the ordinary urencriterium.

| Prior use in the five preceding calendar years | Amount 2025      |
|------------------------------------------------|------------------|
| not applied in any of those years               | **EUR 12,000**   |
| applied in one of those years                   | **EUR 8,000**    |
| applied in two of those years                   | **EUR 4,000**    |

- **The amounts are keyed to prior use in the five preceding calendar years
  (art. 3.78a lid 4), not to a first, second and third year of business.** The
  Belastingdienst page phrases them as "het 1e, 2e en 3e jaar"; the statutory
  keying is the one to apply, and the difference matters when a year was skipped.
- Each amount is capped at the winst: "De aftrek kan niet hoger zijn dan uw
  winst."
- Conditions (art. 3.78a lid 1): the taxpayer was not an ondernemer in one or
  more of the five preceding calendar years; is entitled to an
  arbeidsongeschiktheidsuitkering; does not meet the urencriterium but does meet
  the **verlaagd urencriterium of 800 hours**; and **has not reached the
  AOW-leeftijd at the start of the calendar year**.
- Because the relief applies only where the 1,225-hour urencriterium is not met,
  and the zelfstandigenaftrek requires that same urencriterium (art. 3.76 lid 1),
  the two do not run together in one year. Confirm the actual hours with the
  taxpayer before choosing a route.
- Qualifying uitkeringen (art. 3.78a lid 2): WIA, WAO, WAZ, Wajong, an equivalent
  foreign statutory scheme, a scheme designated by ministerial regulation, or a
  periodieke uitkering or verstrekking from an insurance for invaliditeit or
  ongeval.
- Excluded (art. 3.78a lid 1, second sentence) where a voortzetting under art.
  14c Wet Vpb 1969 started in the calendar year or in one of the five preceding
  calendar years.

## Willekeurige afschrijving voor startende ondernemers -- explain only

**Do not compute this. Explain it, ask the taxpayer whether it is in play, and
route the amount to manual review.**

Status, stated honestly: the scheme is in force under the Uitvoeringsregeling
willekeurige afschrijving 2001 (hoofdstuk 4, paragraaf 1, art. 7-9) and has a
dedicated Belastingdienst page, but it is absent from the Fiscale informatie
chapters for both 2025 and 2026, and the annual maximum is described only by
reference to another table, so no reviewed amount is established here. Recheck
this with the Belastingdienst before the 2026 season.

What is established:

- **Access conditions, both required.** The enterprise is an eenmanszaak, a
  maatschap, a commanditaire vennootschap or a vennootschap onder firma, **and**
  the taxpayer meets the conditions for the startersaftrek above.
- **Eligible assets.** Bedrijfsmiddelen bought in the years in which the
  startersaftrek could be obtained, plus the immediately preceding aanloopjaar in
  which no zelfstandigenaftrek applied (art. 7 UWA 2001).
- **Excluded.** Assets that do not qualify for the investeringsaftrek, assets
  already written off freely on another basis, and assets made available to third
  parties. Short-term successive rental of items such as special tools, trailers
  and cherry-pickers does qualify.
- **Annual maximum.** Art. 8 UWA 2001 caps the investments per calendar year at
  the maximum amount of the kleinschaligheidsinvesteringsaftrek table
  (art. 3.41 lid 2 Wet IB 2001); the Belastingdienst repeats that the maximum "is
  gelijk aan het maximumbedrag voor de kleinschaligheidsinvesteringsaftrek". The
  mapping of that description to one euro amount is **not established** in the
  reviewed sources, so no amount is stated in this note. If the taxpayer invests
  more than the maximum, they choose which assets get the willekeurige
  afschrijving.
- **The KIA lower threshold does not apply here.** An asset too small to generate
  any kleinschaligheidsinvesteringsaftrek can still be written off freely. The
  KIA thresholds themselves are in `investeringsaftrek.md`.
- **Timing.** If the asset is put into use right after the investment,
  depreciation may start immediately; if not, depreciation in the investment year
  is limited to the amount actually paid in that year.
- **Floor.** The boekwaarde may not fall below the restwaarde.
- **Terugname.** Within **5 years** from the start of the investment calendar
  year (**10 years** for zeeschepen) the boekwaarde must be corrected if the
  asset is rented out, if a double-taxation arrangement applies to the profit
  made with it, or if it is used for a bosbedrijf. The difference between the old
  and the new boekwaarde is profit. Art. 9 UWA 2001 sets the art. 3.38 period at
  five years, art. 12 at ten years for zeeschepen.

## Manual-review boundaries

Record the facts, do not compute, and route to manual review:

1. The opening value and depreciation schedule of any asset brought into the
   enterprise at the start.
2. Any willekeurige afschrijving voor startende ondernemers amount.
3. Any samenwerkingsverband (vof, maatschap, cv), including the ongebruikelijk
   samenwerkingsverband hours exclusion and the allocation between participants.
4. Any geruisloze terugkeer uit een bv (art. 14c Wet Vpb 1969) in the year or the
   five preceding years, which blocks both the startersaftrek and the
   startersaftrek bij arbeidsongeschiktheid.
5. Whether an activity in the aanloop years was already a bron van inkomen or
   resultaat uit overige werkzaamheden, which decides condition b for the
   aanloopkosten.
6. Aanloopkosten without documentation.

## Developer instruction

1. Ask which calendar year was the taxpayer's **first** calendar year as
   ondernemer, and confirm it before doing anything else in this note. Only if
   that year is 2025 do aanloopkosten belong in this return.
2. Ask explicitly whether costs were made in 2020 through 2024 with the intention
   of starting this enterprise. Never assume the answer is zero and never fill in
   a placeholder. For each item, ask for the invoice, the year, whether anything
   was earned against it and whether it was already deducted in an earlier
   return.
3. Ask for the hours actually spent on the enterprise in 2025, including hours
   before registration, and ask whether an urenregistratie exists. State plainly
   that the 1,225 hours are **not** reduced for a mid-year start, and say it
   before presenting any zelfstandigenaftrek figure.
4. Check the grotendeels test separately: it is waived only where the taxpayer
   was not an ondernemer in one or more of 2020 through 2024. Ask about each of
   those years rather than inferring it.
5. Before applying the startersaftrek, walk through all four conditions with the
   taxpayer, including how many times the zelfstandigenaftrek was already applied
   in 2020 through 2024 and whether any geruisloze terugkeer uit een bv occurred.
   Read the amounts from this note; do not paraphrase them from memory.
6. When the startersaftrek applies, state that the winst cap on the
   zelfstandigenaftrek falls away, that the combined aftrek may exceed the winst,
   and hand the resulting loss to `verlies-en-verrekening-2025.md`. Do not create
   niet-gerealiseerde zelfstandigenaftrek in a startersaftrek year.
7. For the startersaftrek bij arbeidsongeschiktheid, ask how many times it was
   applied in the five preceding calendar years and pick the amount from that
   count, not from a first, second or third year of business. Confirm the
   uitkering, the 800 hours, and that the AOW-leeftijd had not been reached at
   the start of 2025.
8. For willekeurige afschrijving voor startende ondernemers: explain the scheme,
   ask whether the enterprise form and the startersaftrek conditions are met and
   which assets were bought in the eligible years, then stop. Never calculate an
   amount and never state an annual maximum figure -- route it to manual review.
9. Assets acquired before the start: collect purchase invoice, date, cost and the
   business and private use split, apply the 10% and 90% labelling rules, and
   route opening value and depreciation to manual review.
10. Every portal action stays with the human: you (the taxpayer) open Mijn
    Belastingdienst, enter the aanloopkosten, hours answer and starter reliefs,
    and submit. The plugin prepares and explains the figures and never logs in,
    enters, or sends anything.
