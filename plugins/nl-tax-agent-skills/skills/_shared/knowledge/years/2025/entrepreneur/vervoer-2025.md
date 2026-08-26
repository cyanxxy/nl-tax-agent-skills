# Rule note: Vervoer en autokosten 2025

source_ids: bd_bijtelling_auto_2025, bd_bijtelling_privegebruik_auto_2021, bd_bijtelling_privegebruik_auto_2022, bd_bijtelling_privegebruik_auto_2023, bd_bijtelling_privegebruik_auto_2024, bd_privegebruik_auto_ondernemer, bd_bijzondere_situaties_privegebruik_auto, bd_waarde_van_de_auto, bd_rittenregistratie, bd_uitsluitend_zakelijk_gebruik_bestelauto, bd_bestelauto_niet_prive_gebruiken, bd_verklaring_geen_privegebruik_auto, bd_keuzemogelijkheden_auto, bd_vermogensetikettering, bd_privevervoermiddel_2025, bd_zakelijk_gebruik_privevervoermiddel, bd_privegebruik_andere_vervoermiddelen, bd_overzicht_aftrekbare_zakelijke_kosten, bd_fisin2025_h6_winst_uit_onderneming, ola_ih2025_wa_privegebruik_auto, wet_ib_3_20_2025, wet_ib_3_20a_2025, wet_ib_3_14_2025, law_wet_inkomstenbelasting_2001
workflow: annual_return
tax_year: 2025
status: active
last_reviewed: "2026-08-15"
review_status: reviewed

## Rule

This note is canonical for every 2025 vehicle and travel figure used in the winst
uit onderneming of an IB-ondernemer: the classification of a car as
ondernemingsvermogen or privevermogen, the bijtelling privegebruik auto
(art. 3.20 Wet IB 2001), the rittenregistratie and the 500-kilometre test, the
bestelauto regimes, the fixed deduction per business kilometre for a private
vehicle (art. 3.15 lid 6 and art. 3.17 lid 1 b), the fiets van de zaak
(art. 3.20a), other vehicles on the balance sheet, public transport and air
travel, and geldboetes (art. 3.14). `winst-en-kosten.md` carries the general cost
rules, the beperkt aftrekbare kosten and the bewaarplicht and defers to this note
for vehicles; `investeringsaftrek.md` carries the investeringsaftrek exclusions
that apply to personenauto's; `ondernemersaftrek.md` and
`mkb-winstvrijstelling.md` are applied after the winst -- including every
correction in this note -- has been determined.

These are reference notes for workpack preparation -- not final tax advice.

## Car in the ondernemingsvermogen or in privevermogen

The ondernemer first decides, per car, on which side of the balance sheet the car
belongs. That is a vermogensetikettering question, and the answer is sometimes
forced.

| Fact about the car in 2025 | Classification |
|----------------------------|----------------|
| Business use is 90% or more | verplicht ondernemingsvermogen |
| More business kilometres than private kilometres AND not more than 500 private kilometres in the year | verplicht ondernemingsvermogen |
| Private use is 90% or more | verplicht privevermogen |
| Every other case | keuzevermogen -- the ondernemer chooses |

The general bedrijfsmiddel rule behind this is the same one: business use of 10%
or less makes an asset verplicht privevermogen, business use of 90% or more makes
it verplicht ondernemingsvermogen, and in between the ondernemer may choose. A
choice for keuzevermogen must stay within reasonable limits (binnen redelijke
grenzen). A made choice can generally be revised until the aanslag for the year of
the choice is irrevocably fixed; after that a change requires a bijzondere
omstandigheid.

The two routes are taxed very differently.

| | Car in the ondernemingsvermogen | Car in privevermogen |
|---|---|---|
| Actual costs (fuel, maintenance, insurance, motorrijtuigenbelasting, depreciation) | deductible as business costs | not deductible at all |
| Deduction for business trips | none on top of the actual costs | a fixed amount per business kilometre (see below) |
| Private use of the car | corrected by a bijtelling (onttrekking) added to the winst | no correction; the car is not in the winst |
| Sale or transfer of the car | boekwinst or boekverlies runs through the winst | outside the winst |

Two boundaries around this choice:

- Personenauto's that are not intended for beroepsvervoer are excluded from the
  investeringsaftrek. See `investeringsaftrek.md` before claiming KIA, EIA or MIA
  on any vehicle.
- The income-tax classification does not settle the btw treatment. The btw side
  is decided separately and is a manual-review item in this workflow.

Purchase and installation costs of a charging point (laadpaal) for an electric
car in the ondernemingsvermogen are deductible business costs and do not increase
the cataloguswaarde used for the bijtelling.

## Bijtelling privegebruik auto: car first admitted in 2025

When a car in the ondernemingsvermogen is also available for private use, a
bijtelling is added to the winst as an onttrekking. The base is the waarde van de
auto: the original cataloguswaarde including btw and bpm, plus accessories fitted
by or on behalf of the manufacturer or importer before the kenteken was granted.
The cataloguswaarde of most cars can be looked up on the RDW website.

For a car with a datum eerste toelating (DET) in 2025:

| Situation | Percentage of the cataloguswaarde |
|-----------|-----------------------------------|
| CO2 emission more than 0 g/km | 22% |
| CO2 emission 0 g/km, first EUR 30,000 of cataloguswaarde | 17% |
| CO2 emission 0 g/km, part above EUR 30,000 | 22% |
| Car with a motor that can run on hydrogen | 17% over the whole cataloguswaarde |
| Car driven fully by integrated solar cells | 17% over the whole cataloguswaarde -- MANUAL REVIEW, see below |

The statute expresses the same rule as a reduction: 22% reduced by 5% of the
waarde van de auto when the kentekenregister shows a CO2 emission of 0 g/km, with
the reduction capped at EUR 1,500. The EUR 1,500 cap is what produces the
EUR 30,000 cataloguswaarde ceiling; above that ceiling the standard 22% resumes
on the excess. For a hydrogen car, and for a car driven fully by integrated solar
cells, the cap on the reduction does not apply, so the reduced percentage runs
over the whole cataloguswaarde.

**Zonnecelauto is manual review.** The qualifying test for the solar-cell
exception is not settled across the reviewed sources. The Belastingdienst page
states that the solar cells must have a capacity of at least 1 kilowattpiek and
that the accupakket must not contain lead. Article 3.20 lid 2 states that the
accupakket must not contain lead and that the capacity of the solar panels in
wattpiek divided by consumption in watt-hours per kilometre must be at least 7.
Do not decide a claimed zonnecelauto in the workpack: record the claim, record
the car's technical data, and route the qualification to manual review. Hydrogen
cars are not affected by this and need no special routing.

### The 60-month lock

The percentage that applies at first admission is locked for **60 months**. The
period starts on the first day of the month following the month of the datum
eerste toelating -- for a car first admitted on 7 March 2025 the 60 months start
on 1 April 2025. During those 60 months the car keeps its own percentage even
when the rules change; once the period ends, the rules in force at that time
apply for the remaining months.

Because of that lock, cars first admitted in earlier years are still running
their own percentages inside the 2025 return:

| Datum eerste toelating | Reduced percentage at CO2 0 g/km | Cataloguswaarde ceiling | Part above the ceiling |
|------------------------|----------------------------------|-------------------------|------------------------|
| 2024 | 16% | EUR 30,000 | 22% |
| 2023 | 16% | EUR 30,000 | 22% |
| 2022 | 16% | EUR 35,000 | 22% |
| 2021 | 12% | EUR 40,000 | 22% |

General percentages that do not depend on a reduced-rate window:

| Datum eerste toelating | Percentage |
|------------------------|------------|
| 2017 or later | 22% |
| Before 2017 | 25% -- but see the age rule below before using this row |

**This table does not settle an old car.** A car first put into use more than
15 years before any day in 2025 falls under the youngtimer section below, not
under the 25% row: article 3.20 attaches its own regime to a car of that age,
and the reviewed sources do not settle either the base or the percentage. Read
the 25% row only for a car whose datum eerste toelating is before 2017 and
within 15 years; for anything older, follow the youngtimer section and route the
car position to manual review.

For a car with a datum eerste toelating before 2021, the reduced-rate window may
have ended during or before 2025 and the applicable percentage is not established
in this note. Collect the datum eerste toelating and the CO2 data and route the
percentage to manual review.

### Cap at the actual car costs, and the eigen bijdrage

- **Cap.** For an IB-ondernemer the onttrekking is never higher than the total
  car costs of the year, including depreciation. Where the car costs are lower
  than the computed bijtelling, the onttrekking equals the car costs and the net
  deductible car costs become nil. Worked example from the Belastingdienst:
  catalogusprijs EUR 50,000 gives a computed bijtelling of EUR 11,000; total car
  costs of EUR 8,000 cap the onttrekking at EUR 8,000.
- **Eigen bijdrage voor prive-gebruik.** The onttrekking is taken into account
  only insofar as it exceeds the amounts the ondernemer bore for own account in
  respect of the costs and charges of the car (art. 3.20 lid 4). Subtract those
  amounts from the computed bijtelling. The result is never negative.
- **Part of a year.** Apportion the bijtelling over the period the car was
  available, and convert the private kilometres actually driven to a full-year
  figure before applying the 500-kilometre test.
- **More than one car.** Compute per car and settle the total. For cars held at
  the same time the 500-kilometre test is applied per car. Where cars replace one
  another during the year, private kilometres are assessed together on an annual
  basis.
- **Actual private-use costs above the forfait.** The Belastingdienst states that
  where the actual costs of the private use exceed the normal bijtelling, the
  actual costs are settled against the car costs instead. Record the facts and
  route the sizing of such a case to manual review.

### Youngtimer: manual review, do not compute

A separate regime exists for an old car: from the moment the car passes a
statutory age threshold measured from its first use, the base switches from the
cataloguswaarde to the waarde in het economisch verkeer -- the price the car
would normally fetch on a sale -- and a different percentage applies. That
threshold and that percentage are not settled: article 3.20 lid 1 and article
3.20 lid 5 do not use the same age, and the Belastingdienst applies a transitional
rule on top. **Do not compute a youngtimer bijtelling in the workpack.**

Screening trigger only: if the car was first put into use more than 15 years
before any day in 2025, treat the whole car position as manual review, collect
the date of first use, the waarde in het economisch verkeer with its
substantiation, and the private-kilometre evidence, and hand the computation to
the taxpayer or an adviser.

## Rittenregistratie and the 500-kilometre test

No bijtelling is due only when the taxpayer can show that the car was used for
**not more than 500 private kilometres** on an annual basis. Failing that proof,
the car is treated as available for private use and the bijtelling applies. For
the inkomstenbelasting **woon-werkverkeer counts as business kilometres**, so
commuting does not consume the 500-kilometre allowance.

A sluitende rittenregistratie is the usual proof. It records, for the car: merk,
type, kenteken, and the period in which the car was used. It records, per trip:
the date, the odometer reading at the start and at the end, the departure and
arrival addresses, the route where it was not the most usual route, whether the
trip was business or private, and the prive-omrijkilometers where one trip mixes
business and private kilometres. Driving from the work address to an appointment
and back counts as two trips.

- With a system carrying the Keurmerk RitRegistratieSystemen the Belastingdienst
  assumes the log itself is sound, but may still test whether an individual trip
  was business or private.
- An ondernemer or resultaatgenieter who makes many work trips a day in a
  bestelauto may keep a simplified rittenregistratie, combined with the business
  addresses in the administratie. Private use during working hours and lunch
  breaks is not permitted under that simplification.
- A rijinstructeur only has to record the opening and closing odometer readings
  per working day.
- Proof by other means than a rittenregistratie is allowed; where nothing can be
  shown, the bijtelling must be settled against the car costs.

## Bestelauto

- **Ordinary bestelauto.** Nearly all bestelauto's follow the same bijtelling
  rules as a personenauto.
- **Bestelauto only suitable for goods transport.** A bestelauto that by its
  nature or fittings is exclusively or almost exclusively suitable for
  transporting goods falls outside the forfait (art. 3.20 lid 5). Signs of this
  are a driver's seat only, with the mounting points for a passenger seat ground
  off or welded shut. The private use is then corrected with the actual private
  kilometres times the actual cost per kilometre. Collect the kilometre split and
  the total van costs and route the calculation to manual review.
- **Verklaring uitsluitend zakelijk gebruik bestelauto.** With this verklaring
  there is no private-use correction in the winst and no rittenregistratie is
  required, and the verklaring is valid for an indefinite period (art. 3.20
  lid 6 to lid 10). Against that stands an absolute condition: zero private
  kilometres in the van, plus a duty to notify the Belastingdienst of changes in
  the business use. You (the taxpayer) file and withdraw the verklaring yourself
  in Mijn Belastingdienst Zakelijk; this plugin never opens or operates the
  portal and never files anything on your behalf.
- **Breach of the verklaring.** The Belastingdienst monitors business vans with
  cameras and may ask you to substantiate a trip made at an unusual time or to an
  unusual location, so the underlying evidence has to be kept. Where the business
  character of a trip is not proven, the starting point is that more than 500
  private kilometres were driven, the winst must take the private-use benefit
  into account, and a boete is possible. Withdraw the verklaring before driving
  the van privately, not afterwards.
- **Doorlopend afwisselend gebruik.** Where a bestelauto is used continuously and
  alternately by two or more employees, so that private use cannot be attributed
  to one person, the private use is settled by the employer through eindheffing
  in the loonheffingen rather than by a bijtelling per employee. That is a payroll
  route for employees. It does not replace the ondernemer's own private-use
  correction for a van in the ondernemingsvermogen, and no eindheffing amount is
  established in this note. Ask whether employees use the van, and route any
  eindheffing question to manual review.
- **Verklaring geen privegebruik auto is not available here.** That verklaring
  exists only for employees with a car from their employer. The Belastingdienst
  states explicitly that it is not intended for a zzp'er or eenmanszaak, or for
  someone with inkomsten uit overig werk. Never propose it to an IB-ondernemer for
  a car in their own ondernemingsvermogen.

## Prive-auto or other private vehicle used for business

When the ondernemer uses a vehicle that is private property or privately rented
-- a car, a motor or a fiets -- for business trips, the deduction from the winst
in 2025 is a fixed **EUR 0.23 per business kilometre**.

- That amount **includes all running costs**. Fuel, insurance, tolls and parking
  may not be deducted separately from the winst; they are already inside the
  EUR 0.23. Article 3.15 lid 6 first limits the costs relating to such a vehicle
  to that amount per kilometre, and article 3.17 lid 1 b sets the same amount as
  the maximum deduction.
- **Woon-werkverkeer counts as business kilometres** for the inkomstenbelasting,
  so commuting kilometres driven in the private vehicle are included in the
  deduction.
- The vehicle stays outside the ondernemingsvermogen. There is no depreciation,
  no book result on sale, and no bijtelling.
- Members of the taxpayer's household are treated as the taxpayer for this rule
  (art. 3.15 lid 7).

Ask for the number of business kilometres and how they were recorded. Where the
kilometre count is not supported by any record, flag it rather than accepting it.

## Fiets van de zaak

For a fiets in the ondernemingsvermogen that is also available for private use,
the onttrekking is **7% of the consumentenadviesprijs** of the fiets on an annual
basis (art. 3.20a). Details that decide the outcome:

- The waarde is the consumentenadviesprijs made publicly known in the Netherlands
  by the manufacturer or importer, including btw. Where no adviesprijs can be
  determined, take the adviesprijs of the most comparable fiets.
- A fiets that is also available for woon-werkverkeer is in any case deemed to be
  available for private use, so the 7% applies.
- Subtract the **eigen bijdrage**: the onttrekking is taken into account only
  insofar as it exceeds the amounts the ondernemer bore for own account in
  respect of the costs and charges of the fiets. The onttrekking is capped at
  those fiets costs and is never negative.
- A bromfiets counts as a fiets for this article when it is also driven by human
  muscle power and is fitted with an electric motor. A bromfiets without pedal
  drive is not a fiets for article 3.20a and follows the rule in the next
  section.

The onttrekking is reported as a buitengewone bate in the winst-en-verliesrekening
and the same amount is entered under priveonttrekkingen en -stortingen.

## Scooter, motor and other vehicles on the balance sheet -- explain only

For a vehicle other than a car or a fiets that belongs to the ondernemingsvermogen
-- for example a scooter or a motor -- the costs of the vehicle are deductible and
the private use is corrected with **the actual private kilometres times the actual
cost per kilometre**. There is no cataloguswaarde-based forfait for these
vehicles.

This note explains the method; it does not produce the number. Collect the total
vehicle costs of the year, the total kilometres, and the private kilometres, then
route the calculation and its substantiation to manual review.

## Openbaar vervoer, taxi and air travel

Business travel by openbaar vervoer, taxi or plane is deductible at **100% of the
actual costs**. Evidence is required: keep the train ticket, and with an
OV-chipkaart print out the journeys made. There is no fixed per-kilometre amount
for these trips and no drempel.

## Geldboetes and related costs

Geldboetes are **0% deductible**. Article 3.14 lid 1 onderdeel c Wet IB 2001
excludes from the winst: geldboeten imposed by a criminal court, sums paid to a
state to avoid prosecution, strafbeschikkingen, bestuurlijke boeten and comparable
foreign boeten, boeten imposed under statutory tuchtrecht, boeten imposed by an
institution of the European Union, and the costs referred to in artikel 234 lid 5
and artikel 235 lid 3 Gemeentewet -- the wheel-clamp and towing costs connected to
parkeerbelasting. Article 3.14 lid 1 onderdeel i adds dwangsommen under afdeling
5.3.2 Awb.

Traffic sanctions under the Wet administratiefrechtelijke handhaving
verkeersvoorschriften (Mulder sanctions) are not named separately in the article;
they sit inside the broader category of bestuurlijke boeten in onderdeel c and are
therefore not deductible either. Treat every traffic fine, the wheel-clamp cost
and the towing cost as non-deductible, whoever was driving and whether or not the
car belongs to the ondernemingsvermogen.

## Developer instruction

1. Open the vehicle section by asking, per vehicle: what kind of vehicle it is,
   whether it is on the balance sheet or private property, the datum eerste
   toelating, the CO2 emission and the fuel or energy type, the cataloguswaarde,
   the business and private kilometres, and how the kilometres were recorded.
   Never assume any of these, and never assume zero private kilometres.
2. Settle the classification before any figure. Apply the vermogensetikettering
   table above; only where the case is genuinely keuzevermogen does the ondernemer
   have a choice, and that choice has to be recorded with the reason.
3. For a car in the ondernemingsvermogen, read the percentage from the tables in
   this note and from nowhere else. Match on the datum eerste toelating, not on
   the year of purchase, and check whether the 60-month window is still running.
   Where the datum eerste toelating is before 2021, or where the datum eerste
   toelating is unknown, withhold the percentage and route the car to manual
   review.
4. Apply the corrections in this order: compute the bijtelling on the
   cataloguswaarde, apportion it if the car was available for only part of the
   year, subtract the eigen bijdrage the ondernemer bore for own account, and then
   cap the result at the total car costs of the year.
5. Route to manual review, without computing: any claimed zonnecelauto (R5), any
   car first put into use more than 15 years before a day in 2025 (R6), a
   bestelauto that is exclusively or almost exclusively suitable for goods
   transport, doorlopend afwisselend gebruik of a van by employees, a scooter or
   motor onttrekking, and any case where the actual costs of private use exceed
   the normal bijtelling.
6. Ask whether a complete rittenregistratie exists and what it shows in totals.
   Do not transcribe the log itself, addresses or kenteken data into the workpack;
   record only the totals needed for the 500-kilometre test and the fact that the
   evidence exists. Never collect a BSN.
7. For a privately owned or privately rented vehicle, apply EUR 0.23 per business
   kilometre for 2025 and check that no fuel, insurance, toll or parking cost has
   also been entered as a separate business cost. Read the per-kilometre amount
   from this note; evergreen Belastingdienst pages display the amount for the year
   they are current for.
8. Do not import a commuting deduction from the employment side of box 1 into the
   winst uit onderneming. The reisaftrek openbaar vervoer applies to loon, not to
   winst.
9. Every portal action stays with a person. Where a step needs Mijn
   Belastingdienst or Mijn Belastingdienst Zakelijk -- filing or withdrawing the
   Verklaring uitsluitend zakelijk gebruik bestelauto, checking a beschikking,
   entering the onttrekking -- write it as an instruction to the taxpayer: "You
   (the taxpayer) log in and ...". This plugin never logs in, opens the portal,
   enters values, or submits anything.
