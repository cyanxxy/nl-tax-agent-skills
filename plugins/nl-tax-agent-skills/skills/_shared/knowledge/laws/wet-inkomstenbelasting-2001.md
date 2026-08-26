# Rule note: Wet inkomstenbelasting 2001 -- structural reference

source_id: law_wet_inkomstenbelasting_2001
workflow: all
tax_year: all
status: active
last_reviewed: "2026-08-15"
review_status: reviewed

## Rule

The Wet inkomstenbelasting 2001 (Wet IB 2001) is the primary Dutch income-tax
statute. This file is orientation only: a filing position can also depend on the
applicable regulations, decrees, transitional law, case law, and year-specific
official guidance. Do not infer a complete eligibility rule from this summary.

These are reference notes for workpack preparation -- not final tax advice.

## Three-box system

Dutch income tax is divided into three boxes, each with its own tax base and rate structure:

### Box 1 -- Belastbaar inkomen uit werk en woning

- Employment income (loon)
- Business profits (winst uit onderneming)
- Income from other activities (resultaat uit overige werkzaamheden)
- Periodic payments (periodieke uitkeringen)
- Own-home income (eigenwoningforfait minus mortgage interest)
- Personal deductions (persoonsgebonden aftrek)

### Box 2 -- Belastbaar inkomen uit aanmerkelijk belang

- Income from substantial interest in a company (dividend, capital gains)
- A 5% direct or indirect interest can trigger Box 2, but the statutory tests
  also distinguish classes of shares and cover certain options, profit-sharing
  certificates, cooperative membership rights, family attribution, and related
  positions. Use the reviewed Box 2 sources and keep non-standard facts for
  manual review rather than treating this bullet as the legal test.
- Standard full-year resident preparation is supported for active annual 2025 and provisional 2026 workflows; complex Box 2 facts stay manual review or unsupported.

### Box 3 -- Belastbaar inkomen uit sparen en beleggen

- Savings and investments
- The filing starts from the statutory/fictitious calculation based on asset
  composition. For 2025, the portal can also collect actual-return data and,
  when supplied, compares both calculations and uses the more favorable amount.

## Key structural provisions

### Fiscal partnership (Chapter 2, Section 2.17)

- Fiscal partners may allocate certain income and deduction items between them
- Allocation must be consistent within each box
- Partnership can arise from marriage, registered partnership, or several
  official cohabitation conditions. A cohabitation contract and joint home
  ownership are separate possible conditions, not one combined exhaustive test;
  use the dedicated fiscal-partnership note.

### Heffingsvrij vermogen (box 3)

- Each taxpayer has a tax-free capital allowance in box 3
- Fiscal partners each receive their own allowance
- Specific amounts are year-dependent -- see year-specific knowledge files

### Eigenwoningregeling (own-home rules)

- Interest is deductible only to the extent it relates to a qualifying
  eigenwoningschuld and the applicable use, repayment, and time conditions are met.
- Article 3.112 Wet IB 2001 defines the eigenwoningforfait and its WOZ-value
  table; the imputed rental value is added as income in box 1
- Rules for qualifying own-home debt are in Chapter 3, Section 3.6

### Persoonsgebonden aftrek (personal deductions)

- Specific care costs (specifieke zorgkosten)
- A narrow transitional prestatiebeurs exception may apply; ordinary study
  costs are not a general 2025 deduction. Use the year-specific note.
- Gifts (giften)
- Maintenance payments to ex-partner (alimentatie)
- These deductions are allocated across boxes in a specific order

## Project scope

This project covers Box 1, standard Box 2 preparation for active annual/provisional workflows, and Box 3. Complex Box 2 situations remain outside standard support until exact official-source-backed handling is added.

## Article inventory for entrepreneur support

This inventory names the articles the entrepreneur (ZZP) preparation relies on
and states what each governs. It carries **no rates, percentages, thresholds, or
euro amounts**: those are year-dependent and live in the year-specific notes
under `../years/`. Where an article's detailed text is not summarised here, treat
the article as an orientation pointer and route the facts to manual review rather
than reconstructing the rule.

### Chapter 2 -- tarief and the deduction-rate cap

- **2.10** -- the box 1 tariff table (belastbaar inkomen uit werk en woning).
  Lid 2 is the tariefsaanpassing: the tax is increased by a percentage of the
  amount by which the belastbaar inkomen uit werk en woning plus the deducted
  grondslagverminderende posten exceeds the last first-column amount of the lid 1
  table, capped at that same percentage of the deducted posten. The lid 2 base is
  the **gross** amount of the grondslagverminderende posten that were deducted,
  not a net saldo. Lid 3 lists those posten exhaustively: the ondernemersaftrek
  (3.74), the MKB-winstvrijstelling (3.79a) where the profit reduced by the
  ondernemersaftrek is positive, the terbeschikkingstellingsvrijstelling (3.99b)
  where the resultaat is positive, the aftrekbare kosten met betrekking tot een
  eigen woning (3.120), and the persoonsgebonden aftrek (6.1). Ordinary business
  costs are **not** on that list.
- **2.10a** -- the parallel tariff table for taxpayers born before 1 January
  1946, with the same tariefsaanpassing mechanism and the same percentage as
  article 2.10 lid 2.

### Afdeling 3.2, paragraaf 3.2.1 -- who is an ondernemer

- **3.3** -- medegerechtigden en schuldeisers. Lid 1 sub a brings profit enjoyed
  as medegerechtigde tot het vermogen van een onderneming into the belastbare
  winst uit onderneming; lid 1 sub b covers benefits from a schuldvordering on an
  ondernemer where a lid 3 circumstance applies (the claim in fact functions as
  business capital, or its remuneration largely depends on the profit).
- **3.4** -- begrip ondernemer. Two cumulative elements: the onderneming is
  carried on for the taxpayer's account **and** the taxpayer is directly bound
  (rechtstreeks verbonden) for obligations concerning it. The second element is
  what separates the ondernemer from the medegerechtigde.
- **3.5** -- zelfstandig uitgeoefend beroep. Extending definitions: a
  self-employed profession counts as an onderneming and its practitioner as an
  ondernemer.
- **3.6** -- urencriterium. Lid 1 requires a minimum number of hours spent in the
  calendar year on one or more ondernemingen from which the taxpayer draws profit
  as ondernemer, plus either (a) the grotendeels test against afdeling 3.3 and
  3.4 activities or (b) the starter exception for someone who was not an
  ondernemer in one or more of the five preceding calendar years. Lid 2 to 4
  disregard hours worked for a samenwerkingsverband with verbonden personen where
  the work is mainly supportive and such an arrangement would be ongebruikelijk,
  or where it relates to a verbonden persoon's onderneming. Lid 5 deems the
  activities uninterrupted for the pregnancy and maternity period. The article
  contains **no** pro-rating of the hours norm for a partial first year.

### Paragraaf 3.2.2 -- determining the winst

- **3.9** -- maximum verlies medegerechtigden. Caps the cumulative article 3.3
  loss at the taxpayer's invested capital, measured from the moment article 3.3
  first applied, with the excess added back to that year's profit and deducted
  again in the following year while article 3.3 still applies.
- **3.10** -- verliezen uit de aanloopfase. A delegation provision: it allows a
  ministerial regulation to let the ondernemer deduct the net remaining costs and
  charges made in the five calendar years immediately preceding the first
  calendar year as ondernemer that relate to starting the onderneming and could
  not be charged against the belastbaar inkomen uit werk en woning. The operative
  rules sit in article 5 Uitvoeringsregeling inkomstenbelasting 2001.
- **3.14** -- van aftrek uitgesloten algemene kosten. Lid 1 excludes, among
  others, costs of het voeren van een zekere staat, representative vaartuigen,
  criminal and administrative fines and comparable foreign penalties, costs
  connected with crimes for which the taxpayer has been irrevocably convicted or
  has accepted a strafbeschikking, weapons and munitions, certain animals,
  bribery payments, and dwangsommen. Lid 4 adds back such costs taken in any of
  the five preceding years once the conviction becomes irrevocable.
- **3.15** -- in aftrek beperkte algemene kosten. Lid 1 makes costs connected
  with food, drink and genotmiddelen, representatie, and congresses, seminars,
  symposia, excursions and study trips non-deductible up to a fixed threshold
  amount, with lid 2 pulling the related travel and accommodation into the same
  posten. Lid 5 offers an election in the aangifte to deduct a fixed percentage
  of those costs instead of applying the threshold. Lid 6 first limits the costs
  of a privately owned or privately rented vehicle to a fixed amount per
  kilometre.
- **3.16** -- van aftrek uitgesloten kosten ten behoeve van de belastingplichtige.
  Lid 1 is the werkruimte rule for a workspace in a home outside the
  ondernemingsvermogen: deduction only where the werkruimte is a naar
  verkeersopvatting zelfstandig gedeelte of the dwelling **and** the income tests
  of onderdeel a or b are met. Lid 2 excludes a home telephone subscription,
  literature other than vakliteratuur, clothing other than werkkleding, personal
  care, the levied inkomensafhankelijke bijdrage Zorgverzekeringswet, and course
  and congress travel and accommodation above a fixed cap. Lid 3 excludes
  privately owned or rented instruments, sound and image equipment, tools and
  computers. Lid 4 refuses deduction of remuneration for work by the taxpayer's
  partner below a fixed threshold -- an all-or-nothing test. Lid 5 defines
  werkkleding and lid 6 delegates further rules to a ministerial regulation,
  which is article 7 Uitvoeringsregeling inkomstenbelasting 2001. Lid 8
  disapplies the course and congress cap where the nature of the work makes
  attendance necessary. Lid 13 and 14 extend the werkruimte logic to a rented and
  to an owned dwelling that does belong to the ondernemingsvermogen.
- **3.17** -- in aftrek beperkte kosten ten behoeve van de belastingplichtige.
  Applies on top of articles 3.14, 3.15 and 3.16. Lid 1 a covers a move
  (removal costs of the inboedel plus a fixed forfait) and housing outside the
  place of residence for at most two years; lid 1 b limits a privately owned or
  privately rented vehicle to a fixed amount per kilometre; lid 1 c allows a
  gebruiksvergoeding for a privately owned non-vehicle asset by reference to the
  box 3 percentage of article 5.2 lid 2 applied to its value, or a proportionate
  part of the rent for a privately rented asset.
- **3.18** -- premies for a verplichte beroeps- of bedrijfstakpensioenregeling,
  deductible from the winst within the Wet op de loonbelasting 1964 normeringen.
  Lid 4 onderdeel d takes the pensioengevend loon from the winst uit onderneming
  before the ondernemersaftrek of the third preceding calendar year.
- **3.19** -- bijtelling privegebruik woning. Where a dwelling in the
  ondernemingsvermogen is at the disposal of the taxpayer or a household member
  other than temporarily as hoofdverblijf, an onttrekking is set from the lid 2
  table applied to the woningwaarde; lid 3 takes that value from the WOZ-waarde
  for the calendar year of the onttrekking. Lid 5 b keeps a **non-qualifying**
  werkruimte inside the dwelling for the forfait.
- **3.20** -- bijtelling privegebruik auto. A percentage of the waarde van de
  auto is taken as an onttrekking; lid 2 reduces it for a car with no CO2
  emission up to a maximum reduction, with the cap lifted for a hydrogen car and
  for a car with integrated solar panels meeting the statutory conditions. Lid 3
  treats woon-werkverkeer as business use and sets the onttrekking at nil where
  it is shown that the car is used for not more than 500 private kilometres per
  year. Lid 4 reduces the onttrekking by amounts the taxpayer bore for own
  account. Lid 5 defines auto and waarde van de auto and values an older car at
  the waarde in het economisch verkeer -- the age boundary in lid 1 and the age
  used in lid 5 are not identical in the current text, so route a youngtimer to
  manual review. Lid 6 to 10 govern the verklaring uitsluitend zakelijk gebruik
  bestelauto; lid 11 sets the 60-month lock on the lid 2 reduction.
- **3.20a** -- bijtelling privegebruik fiets. A fixed percentage of the waarde
  van de fiets as an onttrekking where a bicycle is also available for private
  use, availability for woon-werkverkeer being enough to trigger it; reduced by
  the taxpayer's own contributions; lid 3 includes a pedal-driven electric
  bromfiets; lid 4 takes the value from the manufacturer's or importer's publicly
  announced consumentenadviesprijs.
- **3.25 to 3.29** -- jaarwinst. The yearly allocation of the totaalwinst under
  goed koopmansgebruik, applied along a duurzame gedragslijn, together with the
  valuation and cost-allocation rules that support it. Article 3.26 is applied
  correspondingly by article 3.53 lid 2 to the egalisatiereserve. The individual
  texts of 3.26 to 3.29 are not summarised here; route a valuation or timing
  question that turns on them to manual review.
- **3.30** -- afschrijving op bedrijfsmiddelen. Lid 2 sets separate annual maxima
  for goodwill and for other bedrijfsmiddelen, expressed as a share of the
  aanschaffings- or voortbrengingskosten. Lid 3 allows voortbrengingskosten of
  immateriele activa to be written off in full in the year of voortbrenging;
  lid 4 writes off voorwerpen van geringe waarde in full in the year of
  acquisition.
- **3.30a** -- afschrijvingsbeperking gebouwen. Lid 1 allows depreciation on a
  gebouw only while the boekwaarde exceeds the bodemwaarde, and caps it at the
  difference. Lid 2 treats the gebouw, its ondergrond and its aanhorigheden as
  **one** bedrijfsmiddel, with separable werktuigen as a separate bedrijfsmiddel.
  Lid 3 defines the bodemwaarde of a gebouw as its WOZ-waarde.
- **3.31 and 3.34 to 3.39** -- willekeurige afschrijving: the milieu-variant
  (3.31), the designation of other bedrijfsmiddelen, the moment depreciation may
  start, the melding, and the terugname. The designating rules are in the
  Uitvoeringsregeling willekeurige afschrijving 2001 -- see
  `uitvoeringsregeling-willekeurige-afschrijving-2001.md`.

### Paragraaf 3.2.2 -- investeringsaftrek and desinvesteringsbijtelling

- **3.40** -- names the three forms of investeringsaftrek:
  kleinschaligheidsinvesteringsaftrek, energie-investeringsaftrek, and
  milieu-investeringsaftrek.
- **3.41** -- kleinschaligheidsinvesteringsaftrek. Lid 1 grants it per onderneming
  and only where the taxpayer elects it in the aangifte; lid 2 holds the bracket
  table; lid 3 aggregates the investments of a samenwerkingsverband with the
  taxpayer's buitenvennootschappelijke investeringen and then apportions the
  outcome.
- **3.42** -- energie-investeringsaftrek: the percentage and the annual ceiling on
  the energie-investeringen taken into account.
- **3.42a** -- milieu-investeringsaftrek: the percentages for the Milieulijst
  categories.
- **3.43** -- begrip investeren: entering into obligations for the acquisition or
  improvement of a bedrijfsmiddel and making voortbrengingskosten, in so far as
  borne by the taxpayer. Lid 2 lets the Minister equate a change of destination
  with investing.
- **3.44 to 3.46** -- the exclusions and the per-asset minimums. Article 3.45
  lists the excluded bedrijfsmiddelen and sets a separate minimum
  investeringsbedrag per bedrijfsmiddel for the KIA (lid 2 b) and for the EIA and
  MIA (lid 4 b), and excludes from the KIA assets intended to be made available to
  third parties (lid 2 a). Article 3.46 refuses investeringsaftrek for obligations
  entered into with household members, close relatives, and companies in which the
  taxpayer holds a qualifying interest. The detailed text of article 3.44 is not
  summarised here.
- **3.47** -- desinvesteringsbijtelling. Lid 1 triggers it where in one calendar
  year goods are disposed of for combined transfer prices above a threshold, and
  applies the same percentage as the earlier investeringsaftrek. Lid 2 limits it
  to a disposal within five years of the **start** of the calendar year of the
  investment and caps it at the investment amount on which aftrek was taken.
  Lid 3 to 5 treat withdrawal from the onderneming, certain changes of
  destination, and a reversal, reduction or refund as a disposal. Lid 6 is the
  fictieve desinvestering: the investment is undone where less than a quarter of
  the investment amount is paid within twelve months of entering the obligation
  (unless the asset is already in use), or where the asset is not put into use
  within three years after the start of the investment year.

### Paragraaf 3.2.2 -- fiscale reserves and doorschuifregelingen

- **3.53** -- the reserves that may be formed at the expense of the winst.
  Onderdeel a is the egalisatiereserve for the even spreading of costs and
  charges; lid 2 applies article 3.26 lid 1 and 2 correspondingly.
- **3.54** -- herinvesteringsreserve. Lid 1 allows the disposal gain to be
  reserved when determining the profit of the disposal year, provided and for as
  long as the herinvesteringsvoornemen exists. The replacement asset may be
  acquired or produced in the disposal year or in the following three years; that
  replacement window is not a later window for forming the reserve. Lid 2 holds
  the boekwaarde-eis; lid 5 requires release no later than the third year after
  the year in which the reserve arose.
- **3.63** -- doorschuiving naar ondernemers. On a joint request filed with the
  transferor's aangifte, the onderneming counts as not staked. Lid 4 requires the
  business to have been part of a samenwerkingsverband with the successor for the
  36 months immediately preceding the transfer, with the successor drawing profit
  from it as ondernemer; lid 5 offers the alternative of a transfer to a natural
  person who was an employee in that onderneming for the same 36 months. Lid 3
  covers a transfer of part of an onderneming.
- **3.64** -- doorschuiving via te conserveren inkomen naar een andere
  onderneming. On request with the aangifte, staking profit attributable to
  bedrijfsmiddelen and to herinvesteringsreserves is determined separately and
  treated as te conserveren inkomen, provided reinvestment is made plausible in
  the staking year or within twelve months of the staking; lid 3 allows an
  extension of that term in defined circumstances.
- **3.65** -- geruisloze omzetting in an NV or BV. On request the onderneming is
  deemed not to have been staked, provided the founders are entitled in the share
  capital in substantially the same proportion as before and the Minister's
  conditions are met; lid 3 puts those conditions in a voor bezwaar vatbare
  beschikking.
- Staking by death and the related rollover sit in articles 3.58 and 3.62. Every
  staking, doorschuiving, and omzetting is a manual-review event in this project.

### Paragraaf 3.2.4 and 3.2.5 -- ondernemersaftrek and MKB-winstvrijstelling

- **3.74** -- composition of the ondernemersaftrek: zelfstandigenaftrek, aftrek
  voor speur- en ontwikkelingswerk, meewerkaftrek, startersaftrek bij
  arbeidsongeschiktheid, and stakingsaftrek.
- **3.76** -- zelfstandigenaftrek. Lid 1 reserves it for the ondernemer who meets
  the urencriterium; lid 2 holds the amount; lid 3 is the startersaftrek, an
  **increase** of the zelfstandigenaftrek for an ondernemer who was not an
  ondernemer in one or more of the five preceding calendar years and for whom the
  zelfstandigenaftrek was applied at most twice in that period, excluded after a
  geruisloze terugkeer under article 14c Wet Vpb 1969; lid 4 halves the amount at
  AOW-leeftijd; lid 5 caps the aftrek at the winst except where lid 3 applies and
  turns the excess into niet gerealiseerde zelfstandigenaftrek; lid 6 fixes that
  amount by voor bezwaar vatbare beschikking; lid 7 carries it forward for the
  following nine calendar years, oldest first; lid 10 defines winst as the joint
  profit enjoyed as ondernemer from one or more ondernemingen.
- **3.77** -- aftrek voor speur- en ontwikkelingswerk: a base amount with a
  separate increase for starters, conditional on the urencriterium, an
  S&O-verklaring, and a minimum number of hours spent on recognised speur- en
  ontwikkelingswerk.
- **3.78** -- meewerkaftrek. Lid 1 requires the urencriterium and a partner who
  works in the onderneming without any vergoeding; lid 2 holds the bracket table
  keyed to the partner's hours; lid 3 defines the winst base and removes
  replacement profit after onteigening, staking profit including staking by death,
  and eindafrekening profit from it.
- **3.78a** -- startersaftrek bij arbeidsongeschiktheid. For an ondernemer who was
  not an ondernemer in one or more of the five preceding calendar years, is
  entitled to a listed arbeidsongeschiktheidsuitkering or Wajong support, fails
  the urencriterium but meets the verlaagd-urencriterium of lid 3, and has not
  reached AOW-leeftijd at the start of the year. Lid 4 keys the amount to how
  often the aftrek was applied in the five preceding calendar years, each capped
  at the winst.
- **3.79** -- stakingsaftrek. Lid 1 applies only to profit made with or on the
  staking of one or more **whole** ondernemingen. Lid 3 refuses it for a business
  continued under a doorschuiving that has not been carried on for the taxpayer's
  account for at least three years. Lid 4 makes the maximum a lifetime ceiling,
  reduced but not below nil by earlier stakingsaftrek. The article sets no
  urencriterium.
- **3.79a** -- MKB-winstvrijstelling. A percentage of the joint winst enjoyed as
  ondernemer from one or more ondernemingen **after** the ondernemersaftrek. The
  provision sets no urencriterium and no sign restriction, so it also shrinks a
  loss.

### Afdeling 3.4 -- resultaat uit overige werkzaamheden and terbeschikkingstelling

- **3.90** -- belastbaar resultaat uit overige werkzaamheden: residual, arising
  only where an activity produces neither belastbare winst uit onderneming nor
  belastbaar loon, reduced by the terbeschikkingstellingsvrijstelling.
- **3.91** -- terbeschikkingstelling to a verbonden persoon. Lid 1 a and b treat
  making assets available, with or without remuneration, to a verbonden persoon
  who uses them for belastbare winst or belastbaar resultaat as a werkzaamheid.
  Lid 2 a equates certain claims, savings agreements, life-insurance positions,
  genotsrechten, and purchase and sale rights; lid 2 b defines verbonden persoon
  as the partner and the minor children of the taxpayer or the partner; lid 2 d
  treats a borgtocht fee as a TBS voordeel; lid 3 extends the rule to a
  direct-line relative where the terbeschikkingstelling is ongebruikelijk.
- **3.92** -- terbeschikkingstelling to a vennootschap in which the taxpayer or a
  verbonden persoon holds an aanmerkelijk belang, with the same ongebruikelijkheid
  extension in lid 3. Lid 4 attributes an asset in a gemeenschap van goederen half
  to each spouse.
- **3.94** -- resultaat: the joint advantages obtained with a werkzaamheid, under
  whatever name or form.
- **3.95** -- bepaling van het resultaat. Lid 1 applies articles 3.10, 3.13 to
  3.21, 3.25 to 3.30a and 3.55 to 3.62 by analogy as if the werkzaamheid were an
  onderneming; lid 2 adds article 3.53 lid 1 a and b and lid 2, article 3.54 and
  article 3.64 for terbeschikkingstelling werkzaamheden. By omission a
  werkzaamheid gets **no** investeringsaftrek, **no** ondernemersaftrek and **no**
  MKB-winstvrijstelling.
- **3.96** -- excludes from the resultaat, in onderdeel b, the advantages obtained
  for work in the partner's onderneming where the remuneration is non-deductible
  there under article 3.16 lid 4 -- the exact mirror of that deduction ban.
- **3.99b** -- terbeschikkingstellingsvrijstelling: a percentage of the joint
  resultaat from articles 3.91 and 3.92 werkzaamheden, excluding article 3.91
  lid 1 onderdeel c. Read the percentage from the year note; official sources have
  disagreed about it, so never paraphrase it from memory.

### Afdeling 3.6 -- eigen woning boundary for a business workspace

- **3.111** -- eigen woning. The definition excludes a naar verkeersopvatting
  zelfstandig gedeelte of a building, ship or woonwagen that is used in an
  onderneming of the taxpayer or a household member and for which an amount can be
  charged against that profit, used for resultaat uit een of meer werkzaamheden,
  or used in a vennootschap in which an aanmerkelijk belang is held. A qualifying
  zelfstandige werkruimte in a privately owned home is therefore carved out of the
  box 1 eigen woning.

### Afdeling 3.7 -- uitgaven voor inkomensvoorzieningen

- **3.124** -- what counts as uitgaven voor inkomensvoorzieningen, including in
  lid 1 onderdeel c the premiums for entitlements to periodic payments in respect
  of invaliditeit, ziekte of ongeval payable to the taxpayer.
- **3.125** -- the lijfrente forms taken out with an insurer, including the
  tijdelijke oudedagslijfrente and its cap on the annual termijnen.
- **3.126a** -- the equivalent for a lijfrenterekening or lijfrentebeleggingsrecht,
  with the same tijdelijke-oudedagslijfrente threshold and, in lid 5, the
  afkoop of a small balance.
- **3.127** -- jaarruimte. Lid 1 sets it as a percentage of the premiegrondslag
  and denies it once the taxpayer has passed a defined age at the start of the
  calendar year. Lid 2 is the reserveringsruimte: unused room from the preceding
  ten calendar years, on request in the aangifte, oldest year first, up to a
  maximum. Lid 3 builds the premiegrondslag from the preceding calendar year's
  **winst uit onderneming before the ondernemersaftrek**, belastbare loon,
  belastbaar resultaat uit overige werkzaamheden and belastbare periodieke
  uitkeringen, subject to an income cap and reduced by a franchise. Lid 4 is the
  pension-accrual reduction. Lid 5 lets a staking year use that year's own figures
  on request.
- **3.128** -- omzetting oudedagsreserve in lijfrente: **vervallen** per 1 January
  2023.
- **3.129** -- omzetting stakingswinst in lijfrente. Lid 1 allows premiums up to
  the profit realised with or on the staking of an onderneming or part of it;
  lid 2 holds three maxima keyed to how close the ondernemer is to the AOW
  pension age, to a 45%-or-more arbeidsongeschiktheid with instalments starting
  within six months, and to the death of the ondernemer; lid 3 reduces the room by
  the reeds opgebouwde voorzieningen; lid 5 defines the arbeidsongeschiktheid
  test. Official sources have disagreed about how the age brackets are expressed;
  sizing a stakingslijfrente stays manual review.
- **3.130** -- timing. Lid 1 makes premiums deductible in the year they are paid
  or settled. Lid 2 is the only general carry-back: premiums under article 3.127
  lid 5 and article 3.129 paid or settled within six months after the end of the
  calendar year may, by election in the aangifte, be attributed to that year.
  There is no general terugwenteling for ordinary jaarruimte premiums.

### Afdeling 3.13 and 3.14 -- verliesverrekening and middeling

- **3.148** -- verlies. Lid 1 makes a negative inkomen uit werk en woning a verlies
  uit werk en woning; lid 2 makes a negative belastbare winst uit onderneming an
  ondernemingsverlies, but never larger than the verlies uit werk en woning of the
  same year.
- **3.150** -- verrekening. Lid 1 sets off the verlies uit werk en woning against
  the incomes of the three preceding and the nine following calendar years; lid 5
  fixes the order (oldest loss against oldest income). Lid 3 and 4 extend the
  carry-back to eight years, on election in the aangifte, for an ondernemingsverlies
  of a taxpayer with a gemoedsbezwaren exemption, in so far as it stems from damage
  that comparable taxpayers usually insure. Lid 6 lets an unused loss from
  allocated gemeenschappelijke inkomensbestanddelen pass to the partner only where
  the partnership ends by death. Lid 7 ring-fences an article 14c Wet Vpb 1969
  ondernemingsverlies against the profit of the continued onderneming.
- **3.151 to 3.153** -- formalisation. The loss and the ondernemingsverlies are
  fixed by voor bezwaar vatbare beschikking and shown separately on the
  aanslagbiljet (3.151), the carry-back is effected by a beschikking reducing the
  earlier aanslag (3.152), and the carry-forward is likewise formalised by
  beschikking issued with the aanslag of the year of set-off (3.153).
- **Afdeling 3.14 (middeling), articles 3.154 and 3.155** -- **vervallen** per
  1 January 2023. Only the headings and the expiry marker remain.

### Chapter 10A -- overgangsrecht used by entrepreneur support

- **10a.3** -- transitional depreciation regime for goodwill, other
  bedrijfsmiddelen and gebouwen for which the verplichtingen were entered into
  before 1 January 2007. Route such a schedule to manual review rather than
  applying the ordinary article 3.30 maxima to it.
- **10a.24** -- keeps the pre-Wet toekomst pensioenen normeringen of article 3.18
  applicable to a pre-Wtp beroeps- of bedrijfstakpensioenregeling. The article is
  marked to lapse on 1 January 2028.
- **10a.25** -- pre-Wtp jaarruimte. Lid 1 keeps the pension-accrual reduction of
  article 3.127 lid 4 as it read on 31 December 2023 applicable to a taxpayer
  still accruing under article 38q Wet op de loonbelasting 1964; lid 2 gives a
  separate formula for schemes with a premie per dienstjaar under article 38r.
- **10a.28** -- middeling. Keeps the old afdeling 3.14 applicable only to requests
  for a middelingsteruggaaf over a middelingstijdvak that contains calendar year
  2022 or an earlier year.
- **10a.29** -- oudedagsreserve. Building up an oudedagsreserve ended with the
  repeal of articles 3.67 to 3.73 per 1 January 2023; lid 1 keeps old articles
  3.70 and 3.71, and named parts of old articles 3.72 and 3.73, in force as they
  read on 31 December 2022 for a reserve that existed at that date, so only the
  wind-down continues. Lid 3, 4 and
  5 allow a rollover on dissolution of the huwelijksgemeenschap, on death, and on
  transfer of the onderneming to the partner; lid 6 excludes the geruisloze
  omzetting of article 3.65; lid 12 allows deduction of lijfrente premiums up to
  the decrease of the reserve; lid 13 counts the reserve as reeds opgebouwde
  voorzieningen for article 3.129; lid 14 allows the six-month election of article
  3.130 lid 2 for those premiums. The article names no euro amounts or
  percentages.

## Developer instruction

When building any income tax calculation or workpack:

1. Identify which box each income or deduction item belongs to
2. Apply box-specific rules -- do not mix Box 1, Box 2, and Box 3 rules
3. Check fiscal partnership status before allowing allocation of items
4. Use year-specific knowledge files for rates, thresholds, and amounts
5. This file provides structural orientation only -- never use it as the source for specific numbers
6. Use the article inventory above to name the legal basis of a workpack line and
   to find the right year note. Cite the article; take every amount, percentage,
   threshold and bracket from the year note.
7. Ask the taxpayer for the facts each article turns on -- hours worked, business
   versus private use, who is a verbonden persoon, when an asset was bought and
   taken into use, which calendar year was the first year as ondernemer. Never
   assume a value, and never assume zero.
8. Keep the order of operations that the articles impose: winst uit onderneming
   (paragraaf 3.2.2), then investeringsaftrek, then the ondernemersaftrek of
   article 3.74, then the MKB-winstvrijstelling of article 3.79a, and only then
   the article 2.10 lid 2 tariefsaanpassing on the gross grondslagverminderende
   posten.
9. Treat as manual review: staking and any doorschuiving or omzetting under
   articles 3.58 to 3.65, a samenwerkingsverband, a terbeschikkingstelling under
   articles 3.91 and 3.92, a youngtimer under article 3.20, a pre-2007 schedule
   under article 10a.3, and any oudedagsreserve movement under article 10a.29.
10. Where this inventory says an article's detailed text is not summarised, do not
    reconstruct the rule. Record the facts and route them to manual review.
11. You (the taxpayer) enter every figure in Mijn Belastingdienst yourself. This
    plugin prepares and explains; it never opens or operates the portal.

## Common failure

Do not apply box 3 percentages or heffingsvrij vermogen amounts from this file. This is a structural reference only. Specific rates and amounts come from year-specific knowledge files under `_shared/knowledge/years/`.
