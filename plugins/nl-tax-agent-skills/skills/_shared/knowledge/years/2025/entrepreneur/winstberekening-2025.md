# Rule note: Winstberekening -- ordered computation chain 2025

source_ids: bd_ondernemer_cijfers_aangifte_2025, bd_fisin_2025_h7, bd_fisin_2025_h8, bd_ola_ih2025_winstberekening, bd_kia_2025, bd_ondernemersaftrek_2025, bd_verrekenen_ngz, bd_mkb_winstvrijstelling_2025, bd_tariefsaanpassing_aftrekposten, bd_deduction_rate_cap_2025, bd_box1_rates_2025, bd_arbeidsinkomen_definition_2025, bd_zvw_inkomensafhankelijke_bijdrage, bd_verlies_uit_onderneming, bd_beperkt_aftrekbare_kosten_2025, law_wet_inkomstenbelasting_2001
workflow: annual_return
tax_year: 2025
status: active
last_reviewed: "2026-08-15"
review_status: reviewed

## Rule

This note is canonical for the **order** in which the 2025 entrepreneur figures
are combined: which amount is subtracted from which, which line each downstream
base is read off, and where the chain stops and manual review begins. It does not
restate the component rules. The amounts themselves stay in their own notes:
`winst-en-kosten.md` (turnover, costs, corrections), `investeringsaftrek.md`
(KIA, EIA, MIA), `ondernemersaftrek.md` (the five components and the winst cap),
`mkb-winstvrijstelling.md` (the 12.7% and its base), `zvw-2025.md` (the bijdrage
percentage and the maximumbijdrage-inkomen),
`inkomensvoorzieningen-2025.md` (lijfrente ruimte),
`verlies-en-verrekening-2025.md` (a negative outcome and the niet-gerealiseerde
zelfstandigenaftrek carry-forward), `zakelijke-schema-2025.md` (the aangifte
screens and rubriek inventory), `../annual/box1-rates.md` (box 1 brackets) and
`../annual/deductions.md` (the shared deduction-rate cap). Where this note and a
component note both mention a figure, the component note is canonical.

These are reference notes for workpack preparation -- not final tax advice.

## The chain at a glance

| Line | Step | Canonical note |
|------|------|----------------|
| A | Omzet minus zakelijke kosten under goed koopmansgebruik, after the fiscal corrections = **winst uit onderneming** (saldo fiscale winstberekening) | `winst-en-kosten.md` |
| B | A minus **investeringsaftrek** (KIA, EIA, MIA), plus any desinvesteringsbijtelling | `investeringsaftrek.md` |
| C | B minus **ondernemersaftrek** | `ondernemersaftrek.md` |
| D | C minus the **MKB-winstvrijstelling**, being 12.7% of C | `mkb-winstvrijstelling.md` |
| E | D = **belastbare winst uit onderneming**, a component of box 1 | `../annual/box1-rates.md` |
| F | **Tariefsaanpassing** on the grondslagverminderende posten in lines C and D, charged as a belastingvermeerdering | `../annual/deductions.md` |

Three downstream bases are read off **different lines**, and one of them off a
**different year**. This is the single most error-prone part of the chain:

| Downstream base | Read off | Canonical note |
|-----------------|----------|----------------|
| Zvw bijdrage-inkomen (winst component) | line **E** of this (2025) chain | `zvw-2025.md` |
| Lijfrente premiegrondslag (winst component) | line **B of the preceding calendar year** -- for the 2025 return, the **2024** winst uit onderneming voor ondernemersaftrek | `inkomensvoorzieningen-2025.md` |
| Arbeidsinkomen for the arbeidskorting (winst component) | line **B** of this (2025) chain | `../annual/credits.md` |

## Step 1 -- Line A: winst uit onderneming

Winst uit onderneming is turnover minus deductible business costs, determined
under goed koopmansgebruik (art. 3.8 Wet IB 2001). The starting figure is the
**saldo winst-en-verliesrekening** of the enterprise; the aangifte asks for it in
the zakelijk deel, which is never pre-filled (see `entrepreneur-aangifte.md`).

Before line A is fixed, apply the fiscal corrections that turn the commercial
result into the fiscal result. The amounts below are 2025 figures and stay
canonical in `winst-en-kosten.md`:

| Correction | 2025 treatment |
|------------|----------------|
| Voedsel, drank en genotmiddelen; representatie; congressen, seminars, symposia, excursies en studiereizen | the first **EUR 5,700** is not deductible; the excess is |
| Election instead of that drempel | deduct **80%** of those costs and do not apply the EUR 5,700 drempel -- one or the other, never both |
| Reis- en verblijfkosten for congressen and study trips | deduction capped at **EUR 1,500**, and the cap is disapplied when attending was necessary for the work |

Also correct for, without restating their rules here:

- Privegebruik of a business car, the woning in ondernemingsvermogen, and a fiets
  van de zaak: the onttrekking is added to the result (`winst-en-kosten.md`).
- Costs that are wholly non-deductible, including the ondernemer's own
  loonbelasting and premies volksverzekeringen.
- The **Zvw bijdrage is never a business cost** (art. 3.16 lid 2 onderdeel e). It
  never appears in line A, in either direction.
- **AOV premiums are never a business cost.** They belong to the uitgaven voor
  inkomensvoorzieningen and are handled outside this chain.

## Step 2 -- Line B: minus investeringsaftrek

The investeringsaftrek (art. 3.40 Wet IB 2001) comes ten laste van de winst
before the ondernemersaftrek is applied. Compute the KIA from the table in
`investeringsaftrek.md`; add EIA and MIA where an RVO verklaring supports them;
add back any desinvesteringsbijtelling. Line B is the result.

Line B is the amount the official definitions mean by "winst uit onderneming
voor de ondernemersaftrek". Neither the arbeidsinkomen definition nor the
lijfrente premiegrondslag definition carves the investeringsaftrek back out, so
both of those bases use the line B position and not line A. Which **year** that
position is read off differs: arbeidsinkomen takes this 2025 chain, the lijfrente
premiegrondslag the preceding year's -- see step 7.

## Step 3 -- Line C: minus ondernemersaftrek

Subtract the joint amount of the ondernemersaftrek components for which the
taxpayer qualifies: zelfstandigenaftrek (including the startersaftrek, which is
an increase of the zelfstandigenaftrek rather than a separate component), aftrek
voor speur- en ontwikkelingswerk, meewerkaftrek, startersaftrek bij
arbeidsongeschiktheid, and stakingsaftrek. Eligibility, amounts and the
urencriterium tests stay canonical in `ondernemersaftrek.md`.

### The winst cap and the starter exception

- The aftrek **cannot exceed the winst before ondernemersaftrek** -- that is,
  line B. Line C therefore does not go below nil on the strength of the
  zelfstandigenaftrek alone.
- **Exception:** when the taxpayer is entitled to the **startersaftrek**, the cap
  does not apply. The combined zelfstandigenaftrek plus startersaftrek may then
  exceed line B, so line C can be negative and the chain can produce a loss.
- The part of the zelfstandigenaftrek that the cap blocks becomes
  **niet-gerealiseerde zelfstandigenaftrek**. The Belastingdienst fixes it by
  beschikking on the aanslagbiljet, carries it forward, and does **not** apply it
  automatically -- the taxpayer must track the running balance and enter it in a
  later aangifte. `verlies-en-verrekening-2025.md` is canonical for the
  carry-forward window and the set-off condition.

The Belastingdienst's own worked example for 2025: winst before the
zelfstandigenaftrek of EUR 1,500 against an entitlement of EUR 2,470 gives an
aftrek capped at EUR 1,500, a winst after aftrek of EUR 0, and a
niet-gerealiseerde zelfstandigenaftrek of EUR 2,470 minus EUR 1,500 = EUR 970.

Note the two separate caps that are easy to confuse: the winst cap above is the
cap on the **zelfstandigenaftrek**; the startersaftrek bij arbeidsongeschiktheid
amounts and the stakingsaftrek carry their own caps, described in
`ondernemersaftrek.md`.

## Step 4 -- Line D: minus the MKB-winstvrijstelling

The MKB-winstvrijstelling (art. 3.79a Wet IB 2001) is **12.7%** in 2025. Its base
is **line C** -- the winst after both the investeringsaftrek and the
ondernemersaftrek. This order is load-bearing: taking 12.7% of line A or line B
overstates the exemption.

- No urencriterium is required; being an ondernemer voor de inkomstenbelasting is
  enough. It applies automatically and cannot be waived.
- **It shrinks a loss.** The 12.7% is applied to the amount at line C whatever its
  sign, so where line C is negative the exemption makes the fiscal loss smaller.
  That is a disadvantage, and the workpack should say so rather than presenting
  it as a benefit.
- It is personal to the ondernemer and cannot be allocated between fiscal
  partners.

## Step 5 -- Line E: belastbare winst uit onderneming

The amount left after line D is line E, the **belastbare winst uit onderneming**:
the joint amount of the winst enjoyed as ondernemer from one or more
ondernemingen, reduced by the ondernemersaftrek and the MKB-winstvrijstelling
(art. 3.2 Wet IB 2001). Lines D and E are the same amount under two names -- D is
the subtraction, E is the statutory label the rest of the return uses.

Line E is a component of the box 1 income, alongside belastbaar loon, belastbaar
resultaat uit overige werkzaamheden, and the belastbare inkomsten uit eigen
woning. `../annual/box1-rates.md` is canonical for the 2025 bracket structure and
`../annual/deductions.md` for the deduction-rate cap. Do not compute the tax due
inside this note.

## Step 6 -- Line F: the tariefsaanpassing correction

Where the inkomen uit werk en woning **before deductions** exceeds
**EUR 76,817** in 2025, a tariefsaanpassing applies to the
grondslagverminderende posten. The 2025 adjustment percentage is **12.02%**, and
the effect is that at most **37.48%** of those deductions is recovered instead of
the top-bracket rate.

- The correction is applied as a **belastingvermeerdering** on the aanslag, not by
  refusing or reducing the deduction itself. Lines C, D and E are unchanged by it.
- The ondernemersfaciliteiten in scope are exactly: zelfstandigenaftrek, aftrek
  speur- en ontwikkelingswerk, meewerkaftrek, startersaftrek bij
  arbeidsongeschiktheid, stakingsaftrek, and the MKB-winstvrijstelling. The
  ordinary startersaftrek is not listed separately because it is absorbed in the
  zelfstandigenaftrek line.
- **Ordinary business costs are NOT capped by the tariefsaanpassing.** Neither is
  the investeringsaftrek. Only the grondslagverminderende posten on the official
  list are reduced -- the costs in line A and the KIA, EIA and MIA in line B keep
  their full effect at the taxpayer's own rate.
- Persoonsgebonden aftrek, the aftrek kosten eigen woning and the
  terbeschikkingstellingsvrijstelling are on the same official list; they sit
  outside this chain and are handled in `../annual/deductions.md`.
- The aangifte computes the correction itself and shows it on the aanslag under
  "tariefsaanpassing". Present the inputs and the mechanism; do not present a
  self-computed correction as the amount that will be assessed.

## Step 7 -- Two different bases: Zvw and lijfrente

These two bases sit on **different lines**, and the lijfrente base on a
**different year's** chain. Getting them the same way round is the most likely
agent error in this note, so state both explicitly in the workpack.

- **Zvw bijdrage-inkomen** uses the **belastbare winst uit onderneming**, that is
  **line E -- after the ondernemersaftrek and after the MKB-winstvrijstelling**.
  Legal basis: art. 43 lid 2 onderdeel b Zorgverzekeringswet, which refers to the
  belastbare winst determined under afdeling 3.2 Wet IB 2001. The bijdrage over
  winst uit onderneming is levied by a separate aanslag alongside the aanslag
  inkomstenbelasting, and the return the taxpayer files covers both. The
  percentage, the maximumbijdrage-inkomen, the interaction with loon and the
  treatment of a FOR release stay canonical in `zvw-2025.md`.
- **Lijfrente premiegrondslag** uses the **winst uit onderneming voor de
  ondernemersaftrek** -- the line B position, before the ondernemersaftrek and
  therefore also before the MKB-winstvrijstelling -- but taken **from the
  preceding calendar year** (art. 3.127 lid 3 onderdeel a Wet IB 2001, which
  builds the premiegrondslag from the amounts "in het voorafgaande
  kalenderjaar"). For the 2025 return that is the **2024** figure, which this
  2025 chain does not produce: ask the taxpayer for it as a separate 2024 fact.
  This chain's own line B is the winst component of the **2026** premiegrondslag.
  The only exception is the staking election of art. 3.127 lid 5, and staking is
  a manual-review boundary of this chain. The percentages, the income cap, the
  franchise, the pension reduction, the timing rules and **the year the
  premiegrondslag is measured over** stay canonical in
  `inkomensvoorzieningen-2025.md`.

Within one year the line B position is the higher figure, so a lijfrente base and
a Zvw base drawn from the same year differ whenever the ondernemersaftrek or the
MKB-winstvrijstelling is positive. Do not use that as a cross-check here: the
lijfrente base is a 2024 amount and the Zvw base a 2025 amount, so the two are
not comparable. Never reuse one amount for the other.

## Step 8 -- Arbeidsinkomen for the arbeidskorting

The arbeidsinkomen used for the arbeidskorting takes the winst component as
**winst uit onderneming voor ondernemersaftrek en mkb-winstvrijstelling** -- again
**line B of this 2025 chain**, and not line E. Arbeidsinkomen is a current-year
figure, so although it sits at the same position in the chain as the lijfrente
premiegrondslag, it is taken from a **different year**. Do not treat the two as
one amount. Profit enjoyed as a medegerechtigde or as a winstdelende schuldeiser
does not count towards it. `../annual/credits.md` is canonical for the
arbeidskorting bands and for the other components of arbeidsinkomen, such as
belastbaar loon.

## Step 9 -- The vermogensvergelijking self-check

The online aangifte carries a **Winstberekening** screen that reproduces the
profit from the movement in the enterprise's capital and requires the two to
agree. For an eenmanszaak the figure it is compared against is the **saldo
winst-en-verliesrekening**; the screen states that the two amounts must be equal.
`zakelijke-schema-2025.md` is canonical for the screens and the rubriek
inventory; what follows is the chain-level use of the check. The screen draws on:

- **Ondernemingsvermogen** at the begin and the einde of the boekjaar, asked as
  two separate figures.
- **Priveonttrekkingen en -stortingen**.
- **Wijzigingen toelaatbare reserves**.
- **Niet- of gedeeltelijk aftrekbare kosten en lasten**.
- **Vrijgestelde winstbestanddelen**.

Use this as a reconciliation self-check on the workpack, not as a second way to
compute the profit:

- Collect all of the components above from the taxpayer's own bookkeeping. Ask
  for the opening and the closing ondernemingsvermogen **separately**; do not
  carry a prior year's closing figure forward on the agent's own initiative.
- The exact signed formula the screen uses is not published field by field. Do not
  invent one, and do not encode a tolerance for how closely activa and passiva
  must agree -- no official source states one.
- Where the reconciliation does not come out, report the mismatch and the
  components it rests on, and route it to manual review. Never adjust either the
  saldo winst-en-verliesrekening or a balance figure to force agreement.
- Some amounts are entered in two places in the aangifte -- for example the
  onttrekking for a car, woning or fiets appears both in the buitengewone baten
  and in the priveonttrekkingen. Flag those as double-entry points in the manual
  entry checklist.

## When the chain produces a loss

A negative line E is an ondernemingsverlies and leaves this note.

- Confirm first that the loss survives step 4: the MKB-winstvrijstelling reduces
  a negative line C, so line E is a smaller loss than line C.
- An ondernemingsverlies is first set off within the **same** year against
  positive box 1 income, such as loon. Only what remains becomes a verlies uit
  werk en woning.
- `verlies-en-verrekening-2025.md` is canonical for the carry-back and
  carry-forward windows, the beschikking, the voorlopige verliesverrekening, and
  the niet-gerealiseerde zelfstandigenaftrek carry-forward. Do not restate those
  rules or windows here.
- A loss year still requires a filed return. Do not treat a loss as a reason to
  skip the aangifte.

## Boundaries of this chain

The chain above is written for a single IB-ondernemer with one eenmanszaak. Stop
and route to manual review, recording the facts collected so far, when any of the
following is present:

- A **samenwerkingsverband** (vof, maatschap, man-vrouwfirma, cv) or
  buitenvennootschappelijk vermogen. The winstaandeel, the KIA apportionment and
  the per-partner figures are outside this chain.
- **Staking** of the whole or part of an onderneming, doorschuiving, a
  herinvesteringsreserve, or an oudedagsreserve movement.
- Profit enjoyed as a **medegerechtigde** or geldverstrekker: no ondernemersaftrek
  and no MKB-winstvrijstelling apply, so lines C and D do not run.
- A **niet-gerealiseerde zelfstandigenaftrek** balance from earlier years that the
  taxpayer cannot evidence with the beschikking.
- Any component amount the taxpayer cannot evidence at all.

## Developer instruction

1. **Collect these facts before starting the chain.** Each one is a question to
   the taxpayer, never an assumption, and never a zero the agent supplies:
   (a) the saldo winst-en-verliesrekening for 2025 and the underlying omzet and
   kosten; (b) the beperkt aftrekbare kosten and whether the taxpayer elects the
   EUR 5,700 drempel or the 80% route; (c) any privegebruik onttrekking for a car,
   woning or fiets; (d) the qualifying investments and any disposals of assets on
   which investeringsaftrek was claimed; (e) whether the urencriterium is met and
   which ondernemersaftrek components apply, including any startersaftrek
   entitlement; (f) any niet-gerealiseerde zelfstandigenaftrek from earlier years,
   with the beschikking; (g) the opening and closing ondernemingsvermogen,
   priveonttrekkingen and -stortingen; (h) any belastbaar loon or other box 1
   income, which the loss set-off and the tariefsaanpassing threshold both need.
2. **When a fact is missing, ask for it and stop that line.** Record it as an open
   question with the evidence that would settle it, leave the line unresolved in
   the workpack, and do not continue the chain past it with a placeholder. Never
   substitute zero, a prior year's figure, or an estimate for a missing input.
3. **Run the lines strictly in order A to F**, and print each line with its amount
   and the evidence it came from so the arithmetic is traceable. The two order
   rules that must not be relaxed: the investeringsaftrek is subtracted before the
   ondernemersaftrek, and the MKB-winstvrijstelling base is the amount **after
   both** of them.
4. **Read every rate and amount from the canonical note, not from memory.** The
   12.7%, the ondernemersaftrek amounts, the KIA table, the EUR 5,700 drempel and
   the EUR 1,500 cap each live in the note named in the table at the top.
5. **Apply the winst cap at line C** and check the starter exception before
   applying it. When the cap bites, compute the niet-gerealiseerde
   zelfstandigenaftrek, state that the Belastingdienst fixes it by beschikking and
   that it is not carried forward automatically, and tell the taxpayer to keep the
   running balance.
6. **State the tariefsaanpassing qualitatively when the threshold is in play.**
   Give the threshold, the percentage and the maximum rate from this note, say
   that ordinary business costs and the investeringsaftrek are not affected, and
   say that the aangifte computes the correction itself. Do not present an
   agent-computed correction as the assessed amount.
7. **Label the three downstream bases explicitly in the workpack**, each with the
   line **and the year** it comes from: Zvw from line E of 2025, arbeidsinkomen
   from line B of 2025, lijfrente premiegrondslag from line B of **2024**. Before
   emitting them, re-read this note's step 7 table; do not derive them from memory
   of a similar case, and never label this chain's 2025 line B as the lijfrente
   premiegrondslag.
8. **Do not compute the Zvw bijdrage or the lijfrente ruimte here.** Hand line E
   to `zvw-2025.md`. For the lijfrente, do **not** hand over this chain's line B:
   ask the taxpayer for the **2024** winst uit onderneming voor ondernemersaftrek
   as a separate fact and hand that to `inkomensvoorzieningen-2025.md`, which is
   canonical for the year. Record this chain's 2025 line B only as an input to the
   2026 jaarruimte. Let those notes supply the percentages and ceilings.
9. **On a negative line E, route to `verlies-en-verrekening-2025.md`** and say in
   the workpack that the MKB-winstvrijstelling made the loss smaller.
10. **Run the step 9 reconciliation as a check, and report a mismatch rather than
    resolving it.** Ask for the opening and closing ondernemingsvermogen as two
    separate figures. Do not encode a balance tolerance and do not invent the
    signed formula.
11. **Present the aangifte sections as a checklist, never as a numbered wizard
    order.** The left-to-right screen order of the winstaangifte is not published;
    only the reconciliation constraint above is.
12. **Keep the chain in the workpack narrative.** Do not emit the belastbare winst
    as a manual-entry field-map row -- the aangifte derives it from the figures the
    taxpayer types. If it appears in a field map at all, it is a calculated review
    row with its inputs named.
13. **Stop at the boundaries listed above** -- samenwerkingsverband, staking,
    medegerechtigde, unevidenced carry-forwards -- and hand the collected facts to
    manual review instead of finishing the chain.
14. **Preparation only.** This plugin never opens or operates Mijn
    Belastingdienst. Write portal steps with an explicit human subject, for
    example: "You (the taxpayer) open the zakelijk deel in Mijn Belastingdienst
    and enter the saldo winst-en-verliesrekening." Never collect a BSN.
15. **Recheck the 2025 amounts in this note before the 2026 season**, and treat
    the component notes as the place where any change is made first.
