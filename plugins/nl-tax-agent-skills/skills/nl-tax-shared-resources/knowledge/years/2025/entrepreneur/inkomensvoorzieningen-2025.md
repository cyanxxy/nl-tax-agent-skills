# Rule note: Uitgaven voor inkomensvoorzieningen 2025

source_ids: bd_aftrekken_lijfrentepremies, bd_hoe_bereken_ik_mijn_jaarruimte, bd_fisin_lijfrente_2025, wet_ib2001_2025_geldend, wet_ib2001_2023_art3127, bd_extra_lijfrenteaftrek_staking_2025, bd_aov_voor_ondernemers, bd_aov_prive_aftrek, bd_oudedagsreserve_2025, wet_ib2001_2022_for_artikelen, wetten_ib_10a_29_for_overgangsrecht, law_wet_inkomstenbelasting_2001
workflow: annual_return
tax_year: 2025
status: active
last_reviewed: "2026-08-15"
review_status: reviewed

## Rule

This note is canonical for the 2025 uitgaven voor inkomensvoorzieningen of an
ondernemer voor de inkomstenbelasting: the lijfrentepremieaftrek within the
jaarruimte and the reserveringsruimte, arbeidsongeschiktheidsverzekering (AOV)
premiums, the run-down of an oudedagsreserve built up before 2023, and the extra
lijfrentepremieaftrek on staking. All of these are **private** box 1 deductions
taken after the winst has been determined; none of them is a business cost. The
winst side lives in `winst-en-kosten.md`, the profit-reducing facilities in
`investeringsaftrek.md`, `ondernemersaftrek.md` and `mkb-winstvrijstelling.md`,
and the Zorgverzekeringswet consequences of an oudedagsreserve release in
`zvw-2025.md`.

These are reference notes for workpack preparation -- not final tax advice.

## Jaarruimte 2025

| Element | 2025 |
|---------|------|
| Jaarruimte percentage of the premiegrondslag | 30% |
| Maximum premiegrondslag taken into account | EUR 137,800 |
| Drempelbedrag (AOW-franchise) subtracted from it | EUR 18,475 |

- **Formula** (art. 3.127 lid 1 and lid 3 Wet IB 2001): take the premiegrondslag
  of the **preceding** calendar year, take at most EUR 137,800 of it, subtract
  EUR 18,475, take 30% of the result, then subtract the pension-accrual
  reduction. The 2025 jaarruimte therefore depends on the taxpayer's 2024
  situation.
- **Premiegrondslag components**, all from the preceding calendar year: the
  winst uit onderneming **before the ondernemersaftrek**, the belastbaar loon,
  the belastbaar resultaat uit overige werkzaamheden, and the belastbare
  periodieke uitkeringen en verstrekkingen.
- Because the winst component is taken before the ondernemersaftrek, it is also
  before the MKB-winstvrijstelling. It is a **different figure** from the
  belastbare winst uit onderneming that forms the Zvw base in `zvw-2025.md`.
  `winstberekening-2025.md` sets out the profit chain and names which line each
  base is read off. Never reuse one for the other, and never reuse the 2025
  winst where the rule asks for 2024.
- The deduction requires a **pensioentekort** and requires the taxpayer to pay
  the premiums or make the deposits personally. Pension contributions withheld
  by an employer are not separately deductible, but a pensioentekort can exist
  even while pension is being accrued in employment.
- **Age limit:** there is no jaarruimte if, at the start of the calendar year,
  the taxpayer had reached the AOW-leeftijd plus five years. Read the
  AOW-leeftijd from `../../../aow/aow-leeftijd.md` and confirm the date of birth
  with the taxpayer. The reviewed material states no 2025 cut-off date of birth,
  so do not state one; where the taxpayer is near the limit, route the test to
  manual review.
- The maximum deduction applies to **all lijfrente products together**, not per
  product or per provider.
- **Do not publish a single "maximum jaarruimte" euro figure.** No official
  source publishes the product of 30% and (EUR 137,800 minus EUR 18,475) for
  2025. Present the formula and this taxpayer's computed result.

### Pension-accrual reduction -- manual review

- Main rule for 2025 (art. 3.127 lid 4 Wet IB 2001): subtract the pension
  premiums actually paid in the preceding calendar year for ouderdomspensioen
  and qualifying partnerpensioen, excluding the art. 38s compensation premie,
  plus nettopensioen premiums divided by the nettofactor.
- Transitional rule preserved by art. 10a.25 lid 1 Wet IB 2001 for a taxpayer
  whose scheme has not moved to the Wet toekomst pensioenen: subtract **6.27**
  times the preceding year's aangroei of the annual pension entitlement
  (factor A).
- Three situations arise in practice -- a scheme already under the Wet toekomst
  pensioenen, a scheme still on the pre-Wtp basis, and a scheme that
  transitioned during the reference year. The reviewed material does not settle
  the third. **Route the reduction to manual review.** Ask the taxpayer for the
  2024 Uniform Pensioenoverzicht (UPO) and the pension premiums paid in 2024,
  and point them at the Belastingdienst hulpmiddel lijfrentepremie, which they
  run themselves.

## Reserveringsruimte 2025

| Element | 2025 |
|---------|------|
| Maximum amount of unused room that may be brought forward | EUR 42,108 |
| Look-back period | the ten preceding calendar years, 2015 through 2024 |

- Unused jaarruimte from the ten preceding calendar years may be brought into
  2025, **oldest year first**, up to EUR 42,108 on top of the 2025 jaarruimte
  (art. 3.127 lid 2 Wet IB 2001).
- It is granted **on request in the aangifte**; it is not automatic. You (the
  taxpayer) claim it in the return yourself.
- Where both are available, use the reserveringsruimte before the current-year
  jaarruimte: the oldest year drops out of the look-back each year and cannot be
  recovered afterwards.
- A premium paid above the total available room is not deductible, in 2025 or in
  any later year. The excess does not carry forward.

## Timing: the year of payment only

- **Art. 3.130 lid 1 Wet IB 2001:** lijfrente premiums are deductible at the
  moment they are paid or settled, and only insofar as the settlement does not
  leave an amount owed. The Belastingdienst states the same rule plainly:
  premiums and deposits may be deducted only in the year in which they were
  paid.
- **There is no general terugwenteling.** A premium paid in 2026 is a 2026
  premium. It cannot be pulled back into the 2025 return because it was paid
  before 1 April 2026 or before 1 July 2026. This corrects a widespread
  misconception: say it explicitly whenever a taxpayer refers to a "1 April
  deadline" or a "1 July deadline" for ordinary lijfrente premiums.
- The six-month window in **art. 3.130 lid 2** is narrow and covers only staking
  and oudedagsreserve situations:
  - stakingslijfrente premiums under art. 3.129 Wet IB 2001;
  - premiums under art. 3.127 lid 5, the election to use the staking-year
    figures for the premiegrondslag;
  - premiums matching the conversion of an oudedagsreserve, through art. 10a.29
    lid 14 Wet IB 2001.
  For tax year 2025 this means paid or settled **before 1 July 2026**, and only
  by an election made in the 2025 aangifte. It is never automatic.
- Ask the taxpayer for the payment date of every premium and deposit, with bank
  evidence. Do not accept a policy year, a premium-notice date or an invoice
  date as the payment date.

## AOV premiums

- An AOV premium is an **uitgave voor inkomensvoorzieningen** (art. 3.124 lid 1
  onderdeel c Wet IB 2001). Even when the policy is taken out as an ondernemer,
  the premium is **never** a business cost and is never subtracted in the winst
  calculation. See also `winst-en-kosten.md`.
- Deductible where the policy provides periodieke uitkeringen on invaliditeit,
  ziekte or ongeval **and** the taxpayer is personally verzekeringnemer,
  verzekerde and begunstigde. In a maatschap or vof the deduction is also
  possible where the samenwerkingsverband took out the policy. Where a third
  party who is not an employer took out the policy, the taxpayer must owe the
  premium to the insurer personally, evidenced by a
  premieverschuldigdheidsclausule in the taxpayer's own name.
- **Not deductible:** a policy that pays the insured sum in one go; a periodic
  payment whose total amount is fixed in advance; premiums an employer already
  handles in the loonheffing or deducts from the gross wage; the verplichte
  Ziektewet and WIA premiums; and Zorgverzekeringswet premiums (see
  `zvw-2025.md`).
- **The payout mirrors the deduction.**
  - Premium deductible -> the periodic benefit is reported as inkomsten uit
    vroegere dienstbetrekking, **not** as winst uit onderneming. The insurer
    withholds loonbelasting, which is credited as a voorheffing.
  - Premium not deductible (lump-sum policy) -> the lump sum is not reported in
    box 1, but the money counts towards the box 3 vermogen.
- Premiums that could not be deducted can later reduce the taxation of the
  payouts under the saldomethode, using a saldoverklaring that must reach the
  insurer before it pays out. Treat the saldomethode as manual review.
- Ask which policy the taxpayer actually holds and read the policy type from the
  insurer's annual statement. Do not classify an AOV from its product name.

## Oudedagsreserve: overgangsrecht only

- Building up an oudedagsreserve has not been possible **since 1 January 2023**:
  art. 3.67 through 3.73 and art. 3.128 Wet IB 2001 are vervallen. Never add to
  a reserve for 2025 and never present a dotatie percentage or dotatie maximum.
- A reserve that existed on **31 December 2022** (or at the end of the last
  boekjaar that began before 1 January 2023) may stay on the balance sheet. For
  that reserve the old artikelen 3.70, 3.71, 3.72 lid 2 and 3, and 3.73 remain
  in force as they read on 31 December 2022 (art. 10a.29 lid 1). Only the
  wind-down remains.
- **Wind-down triggers** (old art. 3.70 lid 1):
  - **Voluntary:** an amount chosen by the taxpayer, at most equal to the
    lijfrente premiums counted as uitgaven voor inkomensvoorzieningen in the
    same calendar year.
  - **Mandatory:** the amount by which the reserve exceeds the
    ondernemingsvermogen at the **end** of the calendar year, but only if one of
    these applies -- the onderneming or part of it was staked in the year; the
    taxpayer had reached the AOW-leeftijd on 1 January of the year; or the
    taxpayer failed the urencriterium in **both** this and the preceding
    calendar year.
  - **Death:** settlement is required and the reserve is added to the belastbare
    winst, unless the partner continues the onderneming and takes over the
    reserve, which requires a request filed with the aangifte.
- Every afname is added to the winst (old art. 3.70 lid 2). The matching
  lijfrente premium is deducted on the private side, so a voluntary release
  converted into a lijfrente is in principle balanced overall -- do not present
  that as a guaranteed net-nil outcome for this taxpayer.
- **Computing the mandatory release is manual review.** It requires the
  ondernemingsvermogen as defined in old art. 3.71: the boekwaarde of the
  business assets less the art. 3.53 reserves other than the oudedagsreserve
  itself, less a positive terugkeerreserve and plus a negative one, measured at
  the end of the calendar year. Do not derive it from a draft balance sheet, and
  never assume the reserve or the excess is nil.
- The conversion premium is capped at the amount of the afname under old
  art. 3.70 lid 1 onderdeel a (art. 10a.29 lid 12). A premium paid within six
  months after the end of 2025 may, by election in the 2025 return, be
  attributed to 2025 (art. 10a.29 lid 14) -- so **before 1 July 2026** -- and
  the converted amount must be added to the 2025 winst uit onderneming.
- A geruisloze omzetting into a bv does not carry the reserve across
  (art. 10a.29 lid 6). Where a geruisloze doorschuiving or omzetting makes the
  reserve fall free, stakingsaftrek can apply; see `ondernemersaftrek.md`.
- The Zorgverzekeringswet treatment of a voluntary release differs from that of
  a mandatory release; see `zvw-2025.md` and record which one occurred. The
  balance-sheet side of the reserve is in `winst-en-kosten.md`.

## Stakingslijfrente -- explain only

- **Art. 3.129 Wet IB 2001:** an ondernemer who ceases an onderneming or **part**
  of one in the calendar year may count lijfrente premiums up to the profit
  realised with or at that staking, capped by the maximum below and reduced by
  the reeds opgebouwde voorzieningen.
- Maxima published by the Belastingdienst for 2025:

| Situation | Maximum 2025 |
|-----------|--------------|
| Staking by an ondernemer aged 62 or older; staking by an invalide ondernemer; staking of the onderneming through death | EUR 566,197 |
| Staking by an ondernemer aged between 52 and 62; staking where the lijfrente payments start immediately | EUR 283,110 |
| All other cases | EUR 141,564 |

- **Recorded conflict in the age brackets.** The Belastingdienst 2025 rate page
  keys the brackets to "62 jaar of ouder" and "tussen 52 jaar en 62 jaar"; the
  Fiscale informatie 2025 chapter writes "61 jaar en 10 maanden of ouder"; the
  statute expresses the same brackets as at most five years and at most fifteen
  years below the AOW-leeftijd. Use the Belastingdienst year-page wording
  reproduced in the table, tell the taxpayer the published wordings do not
  match, and keep the sizing manual.
- "Invalide ondernemer" means at least 45% arbeidsongeschikt: unable to earn at
  least 55% of what comparable healthy taxpayers earn, already so over the past
  year or likely over the coming year, with the lijfrente instalments starting
  within six months of the cessation.
- **Reeds opgebouwde voorzieningen** to subtract: the value of bedrijfs- and
  beroepspensioen entitlements built at the expense of the winst; rights to
  bedrijfsbeeindigingsvergoedingen and the like; the balance of the
  oudedagsreserve at the start of the calendar year; lijfrente premiums deducted
  from 2001 onwards, excluding the basisaftrek lijfrentepremie up to and
  including 2002; deducted deposits on a lijfrenterekening or beleggingsrecht;
  and amounts already deducted through an earlier conversion of stakingswinst.
- These amounts are **ceilings, not entitlements**. The actual deduction is also
  limited by the stakingswinst realised.
- The premium or deposit must be paid before **1 July 2026** for the deduction
  to fall in 2025, by election in the 2025 return.
- A lijfrenteverzekering may be taken out with the successor of the onderneming;
  a lijfrenterekening with that successor is not possible.
- **Do not compute a stakingslijfrente.** Record the facts -- date and scope of
  the staking, date of birth, health status, existing provisions -- and route
  the sizing to manual review. Staking is a manual-review event throughout this
  plugin; see also `ondernemersaftrek.md` for the stakingsaftrek.

## Payout-form limits (explain only)

| Limit | 2025 |
|-------|------|
| Tijdelijke oudedagslijfrente -- maximum annual instalment | EUR 26,781 |
| Afkoop of a small lijfrenterekening or beleggingsrecht allowed up to a value of | EUR 5,429 |
| Overbruggingslijfrente (pre-2006 balances only) -- maximum annual instalment | EUR 63,288 |

- These are payout-phase limits from art. 3.125 and art. 3.126a Wet IB 2001.
  They do not enlarge the jaarruimte or the reserveringsruimte. Explain them
  when a taxpayer asks; never use them in a deduction calculation.
- Where the instalments of a lijfrenterekening or beleggingsrecht exceed the
  tijdelijke-oudedagslijfrente amount, art. 3.126a imposes a minimum payout
  term. That minimum term is not established in this note; if a taxpayer asks
  for it, confirm it on the current Belastingdienst page or route the question
  to manual review rather than stating a number.
- A refund or reversal of previously deducted premiums, and a breach of the
  lijfrente conditions such as gift, sale, pledge, loan, afkoop or
  deblokkering, is treated as negatieve uitgaven voor inkomensvoorzieningen.
  Route any such event to manual review.

## Negative guard: basisverzekering arbeidsongeschiktheid zelfstandigen

- The **basisverzekering arbeidsongeschiktheid zelfstandigen (BAZ) does not
  appear anywhere in the official 2025 guidance.** The Fiscale informatie 2025
  chapter lists the deductible categories -- lijfrentepremies as a pension
  top-up, the same for nabestaandenpensioen, a lijfrente for an adult invalide
  (klein)kind, and arbeidsongeschiktheidsverzekeringen -- and no BAZ. This 2025
  annual-return note does not use later-year guidance to prove a 2025 position.
- **Never model a BAZ premium.** Do not add it to a workpack, do not estimate
  it, do not deduct it, and never quote a rate or a premium for it.
- If the taxpayer raises it, for example after reading about a proposed scheme,
  record the question, say plainly that no such compulsory insurance appears in
  the reviewed official guidance for 2025, and route it to manual review.

## Developer instruction

1. Read every figure from the tables above. Never restate a percentage,
   franchise or cap from memory, and never print a computed "maximum jaarruimte"
   as though it were an official published amount -- show the formula and this
   taxpayer's own result.
2. Ask the taxpayer for the 2024 figures the premiegrondslag needs: winst uit
   onderneming **before** the ondernemersaftrek, belastbaar loon, belastbaar
   resultaat uit overige werkzaamheden, and belastbare periodieke uitkeringen en
   verstrekkingen. Ask for each one separately; never assume a component is
   zero.
3. Ask for the exact payment date of every premium and deposit and deduct only
   what was paid in 2025. When the taxpayer mentions a 1 April or 1 July
   deadline for ordinary premiums, correct it: there is no general
   terugwenteling, and the six-month window covers only the staking and
   oudedagsreserve cases listed above.
4. Route the pension-accrual reduction to manual review. Ask for the 2024
   Uniform Pensioenoverzicht and the pension premiums paid in 2024, and let the
   taxpayer run the Belastingdienst hulpmiddel lijfrentepremie.
5. Ask whether the taxpayer holds an AOV and, if so, whether it pays
   periodically or as a lump sum and who is verzekeringnemer, verzekerde and
   begunstigde. Never place an AOV premium in the winst calculation, and confirm
   the payout treatment matches the premium treatment.
6. Ask whether an oudedagsreserve stood on the 2025 opening balance sheet. If it
   did, ask whether it decreased during 2025 and why. Never assume it is zero,
   never compute a mandatory release, and record whether any release was
   voluntary or mandatory because `zvw-2025.md` needs that answer.
7. Treat every staking fact as manual review. Record the facts and the recorded
   age-bracket conflict; do not size a stakingslijfrente.
8. Never model a BAZ premium, and never present the reserveringsruimte or a
   payout-form limit as an entitlement.
9. You (the taxpayer) enter the lijfrente amounts and claim the
   reserveringsruimte yourself in Mijn Belastingdienst. This plugin prepares the
   figures and the evidence list only; it never opens the portal, logs in, or
   submits anything.
10. Collect only the amounts and dates the calculation needs. Do not record a
    BSN, a policy number or an account number from an insurer statement,
    jaaropgaaf or pension overview.
11. Recheck the jaarruimte figures, the reserveringsruimte cap, the
    stakingslijfrente maxima and the payout-form limits before the 2026 season;
    all of them are reset each year.
