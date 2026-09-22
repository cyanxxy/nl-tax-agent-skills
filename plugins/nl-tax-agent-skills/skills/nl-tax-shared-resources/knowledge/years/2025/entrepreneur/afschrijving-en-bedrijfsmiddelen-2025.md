# Rule note: Afschrijving en bedrijfsmiddelen 2025

source_ids: bd_vermogensetikettering, bd_wat_is_afschrijven, bd_afschrijving_berekening, bd_afschrijving_bedrijfspand, bd_afschrijving_bedrijfspand_2025, bd_ola_ih2025_wv_afschrijvingen, bd_fisin_2025_h7, bd_zakelijke_kosten_een_jaar_2025, bd_zakelijke_kosten_meerdere_jaren_2025, bd_willekeurige_afschrijving_algemeen, bd_willekeurige_afschrijving_starters, bd_herinvesteringsreserve, bd_egalisatiereserve, bd_privegebruik_woning, bd_bijtelling_woning_2025, law_uwa_2001, law_wet_inkomstenbelasting_2001
workflow: annual_return
tax_year: 2025
status: active
last_reviewed: "2026-08-15"
review_status: reviewed

## Rule

A bedrijfsmiddel is a durable asset that the enterprise uses over several years
and does not hold for resale -- gebouwen, machines, auto's, inventaris, and
immaterial items such as vergunningen. Its cost is not deducted in full in the
year of purchase; it is spread over the years of use through afschrijving
(art. 3.30 Wet IB 2001). Before anything can be depreciated, the asset must be
labelled as business or private property (vermogensetikettering). This note is
canonical for the 2025 labelling thresholds, the depreciation maxima and their
inputs, the EUR 450 small-purchase rule, the afschrijvingsbeperking on gebouwen,
the woningforfait when the home belongs to the ondernemingsvermogen, and the
routing of fiscale reserves and willekeurige afschrijving. Running costs, the
werkruimte tests, and the car bijtelling live in `winst-en-kosten.md`; the extra
investment deductions and the desinvesteringsbijtelling live in
`investeringsaftrek.md`; the deductions taken after the winst is determined live
in `ondernemersaftrek.md` and `mkb-winstvrijstelling.md`. The rubrieken that
carry these figures into the aangifte are inventoried in
`zakelijke-schema-2025.md`.

These are reference notes for workpack preparation -- not final tax advice.

## Vermogensetikettering: screening thresholds

The share of business use decides whether the ondernemer has a choice at all.
The Belastingdienst states the thresholds as follows.

| Business use of the bedrijfsmiddel | Label                                                         |
|------------------------------------|---------------------------------------------------------------|
| 10% or less                        | verplicht privevermogen                                        |
| more than 10% and less than 90%    | keuzevermogen -- the ondernemer chooses, within reasonable limits |
| 90% or more                        | verplicht ondernemingsvermogen                                 |

A car has its own set of tests:

| Situation for a car                                                                     | Label                          |
|-----------------------------------------------------------------------------------------|--------------------------------|
| 90% or more business use                                                                  | verplicht ondernemingsvermogen |
| more business kilometres than private kilometres AND at most 500 private kilometres in the year | verplicht ondernemingsvermogen |
| 90% or more private use                                                                   | verplicht privevermogen        |
| every other case                                                                          | keuzevermogen                  |

- **Herziening window.** A choice made for keuzevermogen can generally still be
  revised until the aanslag for the year in which the choice was made stands
  onherroepelijk -- that is, until no bezwaar or beroep is possible any more
  within the applicable term. After that moment the label can only be changed if
  the taxpayer demonstrates a bijzondere omstandigheid.
- Because of that window, a labelling choice is in practice irreversible once the
  aanslag is onherroepelijk. Treat it accordingly.
- Where an asset in the ondernemingsvermogen is also used privately, the private
  use is recorded as a priveonttrekking rather than left out of the accounts.

**Manual review boundary.** Surface the thresholds above as a screening question
and record the answer. Labelling a specific mixed-use asset -- above all a pand
or a car -- is a manual-review item: the consequences run for years, the choice
is effectively irreversible once the aanslag is onherroepelijk, and the sources
give no splitsbaarheid criteria for a pand that is partly business and partly
eigen woning. Record the facts, state the thresholds, and route the decision to
manual review.

## Duurzaam overtollige liquide middelen (explain only)

Liquid funds that the enterprise does not need for its bedrijfsvoering, for
planned investments, or to absorb future business risks are duurzaam overtollig.
The Belastingdienst states that duurzaam overtollige liquide middelen must be
transferred to privevermogen, where they then fall in box 3. The same applies to
funds used to buy crypto that the business does not need. This is a common trap
for a ZZP'er who leaves a large balance sitting on the business bank account.

Explain the rule and ask the taxpayer about the size and purpose of the business
balance. Do not classify a specific balance as duurzaam overtollig in the
workpack -- whether funds are still needed for the enterprise is a facts test;
route it to manual review.

## Afschrijving: what it is and how much

Afschrijven means spreading the cost of a bedrijfsmiddel over the years in which
the enterprise uses it. The Belastingdienst states the annual amount as:

    afschrijving per jaar = (aanschafkosten - restwaarde) : vermoedelijke gebruiksduur

- **Aanschafkosten** are the purchase price plus the costs of acquiring the asset
  and making it ready for use.
- **Restwaarde** is the value the bedrijfsmiddel is expected to still have at the
  moment it can no longer be used.
- **Vermoedelijke gebruiksduur** is in principle the technical life of the asset.
  The shorter economic life may be used instead; the economic life has ended when
  the asset has no economic use left for the enterprise even though it is
  technically still in good order.

Statutory and published maxima that cap the outcome of that formula:

| Bedrijfsmiddel                                        | Maximum depreciation per year                          |
|-------------------------------------------------------|--------------------------------------------------------|
| ordinary bedrijfsmiddelen                              | 20% of the original aanschaf- or voortbrengingskosten  |
| acquired goodwill                                      | 10% per year                                           |
| vergunningen, concessies, and comparable rights        | 20% per year                                           |

- **Pro rata in the year the asset enters use.** If the bedrijfsmiddel was in use
  for only part of the year, depreciation is taken only over that part of the
  year. The Belastingdienst handbook expresses the same rule as: a purchase
  halfway through the year allows half of the annual maximum.
- The aangifte asks for the depreciation split by asset class: goodwill, overige
  immateriele vaste activa, gebouwen en terreinen, machines en installaties,
  productierechten, and overige materiele vaste activa. Willekeurige
  afschrijvingen are reported inside those same lines. The full rubriek
  inventory is in `zakelijke-schema-2025.md`.
- Bedrijfsmiddelen that were already on the balance sheet on 1 January 2007 fall
  under a separate transitional depreciation regime (art. 10a.3 Wet IB 2001).
  Route such a schedule to manual review rather than applying the ordinary
  maxima to it.

## The EUR 450 small-purchase rule

- A bedrijfsmiddel bought for **less than EUR 450** is deducted in one go as
  costs instead of being depreciated (voorwerpen van geringe waarde,
  art. 3.30 lid 4 Wet IB 2001).
- **Btw variant.** If the btw on the purchase can be reclaimed, apply the
  EUR 450 test to the price excluding btw. If there is no right to btw deduction
  -- for example because the ondernemer only performs exempt services -- apply
  the test to the price including btw.
- **Exactly EUR 450 is not established.** The Belastingdienst wording differs
  between pages: two pages describe assets costing "minder dan EUR 450" while the
  vermogensetikettering page describes an aanschafwaarde of "EUR 450 of minder".
  A purchase at exactly EUR 450 therefore has no settled treatment in the
  sources -- route it to manual review and recheck the wording before the next
  filing season.
- **Price alone does not decide.** The EUR 450 rule is an exception for
  low-value items, not the test for whether something is a bedrijfsmiddel. Costs
  paid for something that benefits several years are spread over those years even
  when nothing tangible is acquired -- multi-year rent or lease payments,
  multi-year insurance, interest paid ahead, or a campaign whose benefit runs
  past the year end. Ask both the cost basis and the expected period of benefit.

## Afschrijvingsbeperking op gebouwen (explain only)

A gebouw may be depreciated only down to its bodemwaarde (art. 3.30a Wet IB
2001). Depreciation stops once the boekwaarde has reached that floor.

- **Bodemwaarde now in force:** since 2024 the bodemwaarde for all bedrijfspanden
  is **100% of the WOZ-waarde**. The bodemwaarde is a fiscal concept: it is not
  the value of the land and it is not the restwaarde.
- **WOZ basis for the 2025 return:** use the WOZ-beschikking 2025, which carries
  waardepeildatum **1 January 2024**.
- **Transitional rule:** for a gebouw taken into own use before 1 January 2024 on
  which fewer than three years of depreciation have been taken, 50% of the
  WOZ-waarde may still be used as the bodemwaarde until three years after the
  gebouw was taken into use.
- **Grond is never depreciated.** The Belastingdienst expresses the annual amount
  for a pand as (aanschafwaarde - grondwaarde - restwaarde) divided by the
  gebruiksduur. The gebruiksduur of a pand is usually 30 to 50 years.
- There is no obligation to write a building back up: a gebouw in eigen gebruik
  whose boekwaarde on 1 January 2024 was below 100% of the WOZ-waarde does not
  have to be revalued, and a building already depreciated to or below its
  bodemwaarde keeps its prior year-end boekwaarde.

**Manual review boundary.** Explain the bodemwaarde rule and collect the WOZ
figure, but do not build or rebuild a pand depreciation schedule. Splitting the
purchase price between grond and opstal, setting the restwaarde over a 30 to 50
year life, mede-eigendom, and transactions with connected persons are all
manual-review items. You (the taxpayer) look up the WOZ-beschikking and enter the
final figures yourself in Mijn Belastingdienst.

## Privegebruik woning: woningforfait (art. 3.19 Wet IB 2001)

When the taxpayer lives in a pand that is the hoofdverblijf and that pand belongs
to the ondernemingsvermogen, a woningforfait is added to the winst as an
onttrekking. The forfait is a percentage of the WOZ-waarde of the woongedeelte.

| Woningwaarde (WOZ-waarde of the woongedeelte) | Onttrekking op jaarbasis 2025                                 |
|-----------------------------------------------|---------------------------------------------------------------|
| EUR 0 up to and including EUR 12,500           | 0.65%                                                         |
| EUR 12,501 up to and including EUR 25,000      | 0.85%                                                         |
| EUR 25,001 up to and including EUR 50,000      | 0.95%                                                         |
| EUR 50,001 up to and including EUR 75,000      | 1.05%                                                         |
| EUR 75,001 up to and including EUR 1,330,000   | 1.20%                                                         |
| more than EUR 1,330,000                        | EUR 15,960 plus 2.35% of the woningwaarde above EUR 1,330,000 |

- **Part-year availability** is apportioned: living in the pand for six months
  gives six twelfths of the forfait.
- **WOZ sourcing:** use the WOZ-beschikking from the municipality for the
  calendar year of the onttrekking, and add separately assessed bijgebouwen such
  as a garage where they belong to the woning. For new-build without a
  WOZ-beschikking, the value is estimated by reference to comparable homes. While
  an objection is pending, the value on the beschikking is used. Where there is no
  WOZ-beschikking at all, the waarde in het economisch verkeer is used; for a
  woonboot with a municipal OZB-beschikking, that value is used.
- **Rented pand carve-out.** The forfait of art. 3.19 lid 1 does not apply to a
  woning held through a huurrecht in the ondernemingsvermogen whose costs are
  wholly or partly non-deductible under art. 3.16 lid 13.
- **Unreconciled interaction -- route to manual review.** Art. 3.16 lid 14
  denies the costs of a woning in the ondernemingsvermogen that serves as
  hoofdverblijf where those costs would not have been deductible had the woning
  been private, while art. 3.19 lid 5 b keeps a non-qualifying werkruimte inside
  the "woning" for the forfait. The retrieved sources do not reconcile how the
  woningwaarde is then carved up when the same pand holds a qualifying
  zelfstandige werkruimte. That position is not established: collect the facts,
  state both articles, and route the split to manual review.
- The werkruimte tests themselves, for a home that belongs to privevermogen, are
  in `winst-en-kosten.md`.

## Fiscale reserves -- keep manual review

Both reserves below are recognisable from the balance sheet and from the
taxpayer's own description. Recognise them, record the facts, and route them.
Never compute a dotatie or an afboeking in the workpack.

### Herinvesteringsreserve (art. 3.54 Wet IB 2001)

- Condition: on balansdatum the ondernemer must have an intention to reinvest in
  a bedrijfsmiddel.
- **Boekwaarde-eis:** writing the reserve off against a new bedrijfsmiddel may
  not push that asset's boekwaarde below the boekwaarde of the disposed asset.
  Any remainder can be written off against a later investment within the term,
  and the afboeking reduces the depreciation base of the new asset.
- **Economic-function line:** for assets that are not depreciated, or that are
  depreciated over more than ten years, an afboeking is required only when the
  newly acquired asset has the same economic function as the disposed asset. A
  boekwinst on, for instance, a computer cannot be written off against a pand.
- **Three-year window:** the reserve, or what is left of it, is added back to the
  winst once the intention to reinvest is abandoned, and in any case once three
  years have passed after the boekjaar in which the reserve was formed without a
  reinvestment. An extension exists only where the nature of the bedrijfsmiddelen
  requires a longer period, or where the reinvestment was delayed by special
  circumstances and acquisition or production has already started.
- Within a samenwerkingsverband the movement is reported pro rata to the
  participant's share; since 2024 wider possibilities exist on partial staking
  caused by overheidsingrijpen.

### Kostenegalisatiereserve (art. 3.53 Wet IB 2001)

- Purpose: costs caused by this boekjaar's business operations that only lead to
  a peak in expenditure in a future year -- the classic case is major maintenance
  on buildings or ships every ten years or so.
- Four cumulative conditions from case law: the costs are spent in the future;
  they are a consequence of running the enterprise in the year of the dotatie;
  costs caused in a given year lead to a peak in expenditure in a coming year;
  and it is reasonably certain that the expenditure will be made.
- Scope limit: it must concern future expenditure on **costs**, not the future
  acquisition or improvement of bedrijfsmiddelen.
- Sizing a dotatie requires a reasonable forward estimate, and future cost
  increases may not be taken into account -- which is exactly why sizing stays
  manual. Actual costs are charged against the reserve; a surplus falls into the
  winst; extra costs are deductible at once; and the reserve is released when its
  purpose lapses, for example on sale or loss of the asset.

## Willekeurige afschrijving -- keep manual review

Willekeurig afschrijven means that, alongside the ordinary afschrijving, the
ondernemer decides how and when a bedrijfsmiddel is written off; it yields a
liquidity and interest advantage. The boekwaarde may never fall below the
restwaarde. If the asset is taken into use straight after the investment,
depreciation may start immediately; if not, it is capped at the amount actually
paid during the investment year.

- Excluded from the scheme: gebouwen en woonschepen, bromfietsen en
  motorrijwielen, personenauto's other than taxi's, dieren, wegen, paden, bruggen
  and tunnels, immateriele activa such as goodwill, octrooien and vergunningen,
  and assets made available to third parties -- with short-term successive rental
  items excepted.
- **Terugname:** where the asset is rented out within five years of the start of
  the investment calendar year, the willekeurige afschrijving must be reversed;
  the difference between the old and the new boekwaarde is winst. For zeeschepen
  the window is ten years.
- **Variants other than the starters scheme are manual review.** The Vamil
  variant for milieubedrijfsmiddelen (its free-depreciation percentage sits in
  `investeringsaftrek.md`) and the zeeschepen variant both carry their own
  ceilings, RVO or shipping conditions, and terugname mechanics. Route them.
- **The temporary 2023 scheme is closed.** It covered only assets for which the
  obligations were entered into, or the voortbrengingskosten made, in calendar
  year 2023, and required the asset to be taken into use before 1 January 2026
  (art. 13-15 Uitvoeringsregeling willekeurige afschrijving 2001). If an asset in
  the 2025 accounts was committed to in 2023 under that scheme, route the
  schedule to manual review; do not extend the scheme to any later investment.
- **Startende ondernemer variant.** It exists in its own right, is restricted to
  an eenmanszaak, maatschap, commanditaire vennootschap or vennootschap onder
  firma that meets the startersaftrek conditions, and applies to assets bought in
  a year in which the startersaftrek could be claimed or in the aanloopjaar
  before it. The Belastingdienst describes the annual ceiling only as the maximum
  amount of the kleinschaligheidsinvesteringsaftrek; the mapping of that wording
  to a specific euro amount is **not established** in the sources. State the
  ceiling qualitatively, never as a number, and route the sizing to manual
  review.

## Developer instruction

1. Read every rate, percentage, and threshold in this file at runtime. Never
   paraphrase the depreciation maxima, the EUR 450 boundary, the bodemwaarde
   rule, or the woningforfait table from memory.
2. **Screening questions to ask the taxpayer, in this order.** (a) Which assets
   does the enterprise use, and what did each cost? (b) For each asset, roughly
   what share of the use is business and what share is private? (c) Is any asset
   a pand or a car? (d) Is the taxpayer's home wholly or partly in the
   ondernemingsvermogen? (e) Does the business bank account hold funds beyond
   what the enterprise needs for its operations, planned investments, and risk
   buffer? Record every answer as given. If an answer is missing, record it as
   unresolved and route that asset to manual review -- never enter a value the
   taxpayer has not confirmed and never treat silence as a nil answer.
3. Apply the vermogensetikettering thresholds only as a screen that tells the
   taxpayer whether a choice exists. The labelling of a specific mixed-use asset,
   above all a pand or a car, goes to manual review, and the workpack must say why:
   once the aanslag for the year of the choice stands onherroepelijk, the label
   can only be changed on proof of a bijzondere omstandigheid.
4. For every purchase, ask both the cost basis and how long the enterprise
   expects to benefit from it. Confirm whether the btw on it is reclaimable
   before applying the EUR 450 test, and apply the test to the price excluding
   btw when it is and including btw when it is not. A purchase at exactly
   EUR 450 goes to manual review. If several items were bought together and work
   as one whole, ask whether the taxpayer treats them as one bedrijfsmiddel and
   route the classification to manual review when the combined cost crosses the
   EUR 450 line.
5. To review a depreciation schedule, collect: aanschafkosten, the costs of
   making the asset ready for use, expected restwaarde, expected gebruiksduur,
   and the date the asset entered use. Pro-rate the first year over the part of
   the year in which the asset was in use. If any of those inputs is unresolved,
   keep the finalized accounts' treatment and flag the schedule for manual review
   instead of inventing one.
6. Gebouwen are explain-only. State that depreciation stops at the bodemwaarde,
   that the bodemwaarde is 100% of the WOZ-waarde, that grond is never
   depreciated, and that the WOZ-beschikking 2025 with waardepeildatum
   1 January 2024 is the one to use for this return. Then route the schedule
   itself to manual review.
7. Apply the woningforfait only after confirming that the pand is the taxpayer's
   hoofdverblijf and belongs to the ondernemingsvermogen, and after obtaining the
   WOZ-waarde of the woongedeelte. Apportion for part-year availability. Where a
   qualifying zelfstandige werkruimte sits in the same pand, record that the
   interaction between art. 3.16 lid 14 and art. 3.19 lid 5 b is not established
   in the sources and route the split to manual review.
8. Treat a herinvesteringsreserve or a kostenegalisatiereserve as recognise-and-route.
   Carry the balance-sheet figures across from the finalized accounts, state the
   conditions from this note so the taxpayer can see why the item matters, and
   compute no dotatie and no afboeking.
9. Willekeurige afschrijving other than the startende-ondernemer variant is
   manual review. Do not compute a starters ceiling either -- the euro mapping is
   not established here.
10. Record every manual-review item as an explicit line in the workpack with the
    facts collected and the reason it was routed. You (the taxpayer) enter and
    check all final figures yourself in Mijn Belastingdienst; this workpack never
    does that for you.
