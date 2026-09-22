# Rule note: Samenwerkingsverbanden en bijzondere ondernemingsvormen 2025

source_ids: bd_vof_rechtsvorm, bd_maatschap_rechtsvorm, bd_cv_rechtsvorm, bd_medegerechtigde, bd_fisin2025_h6_winst_uit_onderneming, bd_fisin_2025_h7, bd_urencriterium_2025, bd_kia_2025, bd_tbs_bezittingen, fisin2025_beschikbaar_stellen, bd_rechtsvorm_wijzigen, bd_u_staakt_uw_onderneming, bd_overdracht_medeondernemer_werknemer, bd_personeel_in_uw_onderneming, bd_aanmelden_werkgever, bd_aangifte_loonheffingen, wet_ib_3_3, wet_ib_3_4, wet_ib_3_9, wet_ib_3_41_2025, wet_ib_3_63, wetib_consolidated_2025, law_wet_inkomstenbelasting_2001
workflow: annual_return
tax_year: 2025
status: active
last_reviewed: "2026-08-15"
review_status: reviewed

## Rule

This note is canonical for **recognising and routing** every IB business form
beyond the single-handed eenmanszaak: the vennootschap onder firma, the
maatschap, the commanditaire vennootschap, the medegerechtigde and the
profit-sharing geldverstrekker, the ongebruikelijk samenwerkingsverband, the
terbeschikkingstellingsregeling, the agrarische onderneming, zeescheepvaart, and
the situation in which the enterprise employs staff. Its job is to let the agent
say correctly **which form is in play, what that form does to the ondernemer
tests, and where the question goes next.** It is deliberately **not** a
computation note: the profit computation for these forms stays outside automated
scope. The single-ondernemer profit chain is in `winstberekening-2025.md`; the
ondernemer test itself is in `ondernemer-criteria.md`; the ondernemersaftrek
amounts are in `ondernemersaftrek.md`; the KIA brackets are in
`investeringsaftrek.md`; the fiscal partner who merely works in the enterprise is
in `partner-en-meewerken-2025.md`; cessation is in `staking-2025.md`. This note
is annual 2025 only.

These are reference notes for workpack preparation -- not final tax advice.

## What this note does and does not do

| Task | In scope here |
|------|---------------|
| Recognise which form the taxpayer is in | yes |
| Explain what the form means for the ondernemer tests | yes |
| Say which reliefs survive and which fall away | yes |
| Collect the facts and evidence a human reviewer will need | yes |
| Compute a winstaandeel, a KIA share, a TBS resultaat or a stakingswinst | **no -- manual review** |
| Decide whether a samenwerkingsverband is ongebruikelijk | **no -- manual review** |
| Decide whether an arrangement is a dienstbetrekking | **no -- payroll, outside this pack** |

## Recognition table

Ask the questions in the Developer instruction first, then place the taxpayer in
exactly one row per income stream. A taxpayer can occupy more than one row at the
same time -- for example ondernemer in a vof and medegerechtigde in a cv.

| Form | Position | Income label | Ondernemersaftrek | MKB-winstvrijstelling | Route |
|------|----------|--------------|-------------------|-----------------------|-------|
| Eenmanszaak | ondernemer | winst uit onderneming | yes, if the tests are met | yes | `winstberekening-2025.md` |
| Vof -- vennoot | ondernemer, if the art. 3.4 tests are met | winst uit onderneming (own winstaandeel) | yes, tested per vennoot | yes | this note, then manual review for the split |
| Maatschap -- maat | ondernemer, if the art. 3.4 tests are met | winst uit onderneming (own winstaandeel) | yes, tested per maat | yes | this note, then manual review for the split |
| Cv -- beherend vennoot | ondernemer, if the art. 3.4 tests are met | winst uit onderneming | yes, tested per vennoot | yes | this note, then manual review for the split |
| Cv -- stille (commanditair) vennoot | **medegerechtigde**, not ondernemer | winst uit onderneming | **no** | **no** | manual review |
| Profit-sharing geldverstrekker (art. 3.3 lid 1 b) | medegerechtigde-like | winst uit onderneming | **no** | **no** | manual review |
| Verbonden persoon who makes a pand or a lening available | resultaatgenieter under art. 3.91 / 3.92 | resultaat uit overige werkzaamheden | **no** | **no**, but a 12% terbeschikkingstellingsvrijstelling applies | manual review |

The other two labels the taxpayer can end up in -- loon uit dienstbetrekking and
ordinary inkomsten uit overig werk -- are not business forms and are outside this
note.

## Vof, maatschap and cv -- the shared rules

### Each participant files their own aangifte

There is no partnership return. **Each vennoot or maat reports their own
winstaandeel in their own aangifte inkomstenbelasting.** The samenwerkingsverband
is not a rechtspersoon and is not itself a taxpayer for the inkomstenbelasting.

- **Vof:** "Elke vennoot die aan de eisen voor ondernemerschap voldoet, is
  ondernemer voor de inkomstenbelasting en kan gebruikmaken van de regelingen
  voor ondernemers." A three-person vof therefore produces three ondernemers for
  the inkomstenbelasting.
- **Maatschap:** carrying on a beroep together with maten, the standard examples
  being an artsenpraktijk and a tolkencentrum. "Maten die aan de eisen voor het
  ondernemerschap voldoen, zijn ondernemer voor de inkomstenbelasting."
- **Cv:** largely follows the vof rules, but alongside the beherende vennoten it
  has stille vennoten who "brengen geld in, maar bemoeien zich niet met de
  verdere gang van zaken van de onderneming". A beherend vennoot is an ondernemer
  for the inkomstenbelasting if he meets the ondernemer requirements; a stille
  vennoot is a medegerechtigde, treated separately below.

**Being a participant is not the same as being an ondernemer.** Art. 3.4 requires
both that the onderneming is carried on for the taxpayer's account **and** that
the taxpayer is directly bound for the obligations of that onderneming. Test each
participant against `ondernemer-criteria.md` individually; do not infer
ondernemerschap from the KVK registration.

### For the btw the samenwerkingsverband is the ondernemer

For the btw the vof, the maatschap and the cv are each the ondernemer as a whole,
and the individual vennoten or maten are not. The consequence taxpayers trip over
is that the same business is one ondernemer for the btw and several ondernemers
for the inkomstenbelasting. Btw itself is outside the workpack; say this only to
prevent the confusion.

### Aansprakelijkheid -- explain only

- Vof: not a rechtspersoon; "Elke vennoot is aansprakelijk voor alle schulden van
  de vof."
- Maatschap: not a rechtspersoon; each maat is liable for a proportionate share
  of all debts of the maatschap, **but for tax debts each maat is liable for all
  of them**.
- Cv: beherende vennoten are liable with their personal assets for all debts;
  stille vennoten risk the capital they contributed, unless they involve
  themselves in the running of the business or their name is used in the cv.

Liability is named here because it feeds the art. 3.4 test, not as legal advice.

### The winstverdeling

The winstverdeling is set by the agreement between the participants -- the
vof-contract, the maatschapscontract or the cv-akte -- and it typically reflects
what each participant brings in: labour, capital, goodwill, and the risk each
carries. Participants commonly take a fixed arbeidsbeloning or rentevergoeding
first, with the remaining overwinst divided by an agreed ratio.

**Honest limit: the retrieved official pages for the vof, the maatschap and the
cv say nothing about how a winstverdeling is determined or tested.** No reviewed
source establishes a benchmark for a defensible split. So:

- Ask for the written agreement and record the agreed split exactly as it stands.
- Ask whether the split changed during 2025 and from what date.
- Record any fixed arbeidsbeloning or rentevergoeding taken ahead of the
  overwinst.
- **Route the winstaandeel figure itself to manual review.** Do not construct a
  split, do not default to equal shares, and do not accept a split the taxpayer
  cannot point to in a document.

### Every ondernemer test runs per vennoot

This is the rule the agent must state before any relief is discussed, because the
natural assumption -- that the partnership qualifies and the participants inherit
it -- is wrong.

| Test or relief | Measured at | Consequence |
|----------------|-------------|-------------|
| Ondernemerschap (art. 3.4) | **per participant** | one vennoot can be an ondernemer while another is not |
| Urencriterium of 1,225 hours | **per participant**, on that person's own hours across all of their ondernemingen | one vennoot can meet it while another fails it |
| Zelfstandigenaftrek | **per participant**, and it needs that person's own urencriterium | can be available to one vennoot only |
| Startersaftrek | **per participant**, on that person's own history of earlier years | one vennoot can be a starter while the other is not |
| Aftrek voor speur- en ontwikkelingswerk | **per participant**, with that person's own S&O-verklaring and hours | not shared |
| MKB-winstvrijstelling | **per participant**, over that person's own winstaandeel | needs ondernemerschap but **not** the urencriterium |
| Meewerkaftrek | **per participant** | see `partner-en-meewerken-2025.md` |
| KIA and the other investeringsaftrek | **at the level of the samenwerkingsverband first**, then allocated | see the KIA section below |

Two vennoten in the same vof can therefore end up with materially different
outcomes on the same winst. Never copy one participant's relief position onto
another.

### Buitenvennootschappelijk vermogen

A participant can own assets personally that serve the samenwerkingsverband's
onderneming -- the classic cases are a pand, a car or equipment held in one
maat's own name while the practice uses it. That is **buitenvennootschappelijk
vermogen**: it is not part of the joint partnership assets, but it is part of
that participant's own ondernemingsvermogen.

- The revenues, costs and depreciation on such assets run through **that
  participant's own winstaandeel**, not through the joint result.
- The concept has an explicit statutory footing: art. 3.41 lid 3 Wet IB 2001
  names "buitenvennootschappelijke investeringen" and adds them to the
  partnership's investments for the KIA.
- Presentation follows from the fact that the winst-en-verliesrekening and the
  balans may be completed either at personal level ("op persoonlijk niveau") or
  at the level of the samenwerkingsverband. Which presentation the aangifte
  expects for a given participant is a question for
  `zakelijke-schema-2025.md` and, where it stays unclear, for manual review.
- Vermogensetikettering of the asset itself follows the ordinary rules in
  `afschrijving-en-bedrijfsmiddelen-2025.md`.
- **Boundary that must not be blurred:** buitenvennootschappelijk vermogen
  belongs to someone who is an **ondernemer in that samenwerkingsverband**. Where
  the owner is *not* a participant -- for instance the ondernemer's fiscale
  partner or a minor child -- the same pand or lening falls under the
  terbeschikkingstellingsregeling instead, with a completely different regime.
  Deciding which side of that line an asset falls on is **manual review**.

## KIA in a samenwerkingsverband

**A participant cannot compute their own KIA bracket from their own investment
alone.** This is the single most error-prone figure in a samenwerkingsverband and
the agent must refuse to shortcut it.

The mechanism, from art. 3.41 lid 3 Wet IB 2001 and the Belastingdienst's KIA
page:

1. **Aggregate first.** Take the investments of the samenwerkingsverband as a
   whole and add the taxpayer's own buitenvennootschappelijke investeringen. The
   Belastingdienst wording: the calculation looks "naar de totale investering van
   het samenwerkingsverband en niet naar de investering van elke onderneming
   afzonderlijk".
2. **Apply the bracket table to that total**, not to any individual share. The
   2025 brackets stay canonical in `investeringsaftrek.md`.
3. **Allocate the outcome pro rata.** The default rule: "Iedere firmant of vennoot
   neemt het deel van de investering voor zijn rekening dat in verhouding is met
   zijn deel in de (over)winst."

Because the KIA percentage falls as the total investment rises, aggregating first
generally produces a **smaller** deduction than computing each participant's KIA
on their own share. Computing per participant overstates the relief.

An alternative verdeelsleutel is allowed, but only if **all** of these hold:

- all vennoten divide according to the same criterion;
- the division rests on a reasonable basis -- the examples named are
  kapitaalsverhouding, aandelen in de stille reserves, aandelen in de winst, and
  gelijke delen;
- it applies to every form of investeringsaftrek, not only the KIA;
- it applies to all vennootschappelijke investeringen;
- the same split is used for the desinvesteringsbijtelling;
- a **joint request** stating the verdeelsleutel is filed before the aanslag of
  any one of the participants becomes irrevocable.

**Manual review.** Collect the total investments of the samenwerkingsverband, the
taxpayer's own buitenvennootschappelijke investeringen, the profit or overwinst
ratio, and whether a joint request for a different verdeelsleutel exists. Then
stop. Do not produce a KIA figure for a participant.

## Medegerechtigde and geldverstrekker -- manual review

### Who is in this box

Art. 3.3 lid 1 brings two further streams into belastbare winst uit onderneming:

- **onderdeel a:** profit enjoyed **as medegerechtigde** to the vermogen of an
  onderneming, otherwise than as ondernemer or as aandeelhouder. The standard
  example is the **commanditair vennoot** in a cv. Art. 3.3 lid 2 adds that the
  medegerechtigdheid need not extend to a possible liquidatiesaldo.
- **onderdeel b:** benefits from a **schuldvordering** on an ondernemer, where a
  lid 3 circumstance applies -- the claim "in feite functioneert als vermogen" of
  the business, or its remuneration "grotendeels afhankelijk is van de winst".
  Art. 3.3 lid 6 determines those benefits as if the schuldvordering were itself
  an onderneming.

The Belastingdienst draws the line clearly: "Bent u vennoot in een vof? Dan bent
u geen medegerechtigde, maar ondernemer." A medegerechtigde is typically not
jointly liable for the debts and cannot make binding agreements for the business,
which is why the art. 3.4 ondernemer test fails.

### What falls away, and what does not

| Item | Medegerechtigde or profit-sharing geldverstrekker |
|------|----------------------------------------------------|
| Income label | winst uit onderneming |
| Ondernemersaftrek (zelfstandigenaftrek, startersaftrek, S&O-aftrek, meewerkaftrek, startersaftrek bij arbeidsongeschiktheid, stakingsaftrek) | **not available** |
| MKB-winstvrijstelling | **not available** |
| Investeringsaftrek and willekeurige afschrijving | available to a stille vennoot in a cv |
| Loss recognition | **capped** by art. 3.9 |

The Belastingdienst is explicit on both sides of that table: "Als medegerechtigde
of geldverstrekker krijgt u geen ondernemersaftrek en mkb-winstvrijstelling",
while the cv page states that the stille vennoot "komt ook in aanmerking voor de
investeringsregelingen willekeurige afschrijving en investeringsaftrek" and that
"op de andere ondernemersregelingen heeft de stille vennoot geen recht". Do not
collapse those two statements into a blanket exclusion.

The consequence for a mixed taxpayer: where part of the winst is enjoyed as
medegerechtigde, that part must be identified and kept out of the ondernemersaftrek
base and out of the MKB-winstvrijstelling base. Splitting a mixed winst is
**manual review**.

### The art. 3.9 loss cap needs a running capital record

Art. 3.9 caps the losses a medegerechtigde may take:

- **Lid 1:** where the taxpayer's **cumulative** art. 3.3 profit -- the current
  year plus every preceding year in which art. 3.3 applied -- is negative and
  exceeds the lid 2 ceiling in absolute terms, the difference is added back to
  the profit of the year.
- **Lid 2:** the ceiling is the boekwaarde of the taxpayer's capital in the
  onderneming at the moment art. 3.3 first applied, reduced by the art. 3.53
  reserves at that moment, increased by later contributions at their value on
  contribution, and decreased by later withdrawals at their value on withdrawal.
- **Lid 3:** the amount added back under lid 1 is deducted from the following
  year's profit if art. 3.3 still applies to the taxpayer at the start of that
  year.
- The Belastingdienst states the earliest measuring point: the invested capital
  is measured from **1 January 2001** at the earliest.

**This cannot be produced from one year's figures.** It requires a running record
of the opening capital, every later contribution and every later withdrawal,
running back to the start of the medegerechtigdheid or to 1 January 2001,
whichever is later. Ask the taxpayer whether such a record exists and who holds
it, record what they have, and **route the cap to manual review.** Never treat an
uncapped loss as correct merely because the taxpayer reported a loss.

## Ongebruikelijk samenwerkingsverband -- manual review

### The two-part test

Art. 3.6 lid 2 onderdeel a disregards hours spent for a samenwerkingsverband with
**verbonden personen** when **both** limbs are satisfied:

1. the taxpayer's work for that samenwerkingsverband is **hoofdzakelijk van
   ondersteunende aard** -- the Belastingdienst quantifies "hoofdzakelijk" as
   **70% or more** ondersteunende werkzaamheden; **and**
2. it is **ongebruikelijk** that such a samenwerkingsverband is entered into
   between persons who are not each other's verbonden personen.

Both limbs must hold. Supporting work in an ordinary, arm's-length partnership is
not caught, and an unusual partnership in which the taxpayer does the core work
is not caught either.

- **Verbonden personen** (art. 3.6 lid 3): persons belonging to the taxpayer's
  household, and bloed- of aanverwanten in de rechte lijn or persons belonging to
  their household.
- The Belastingdienst's standard example is "een vof tussen een tandarts en een
  tandartsassistent" who are each other's partners.
- **A second, separate case** sits in art. 3.6 lid 2 onderdeel b, the
  ondermaatschap situation: the samenwerkingsverband relates to an onderneming
  from which a verbonden persoon derives winst **as ondernemer** while the
  taxpayer does not. Art. 3.6 lid 4 extends that to a samenwerkingsverband with an
  entity in which the taxpayer or a verbonden persoon holds an aanmerkelijk
  belang. Screen for this case as well; it does not require the 70% test.

### The consequence is all-or-nothing

When the test bites, the hours are disregarded for the urencriterium. **It is not
a proportional cut: the statute puts the work performed for that
samenwerkingsverband outside consideration as a whole, so the taxpayer does not
keep the non-supporting minority of the hours either.** The Belastingdienst's
shorter phrasing -- "tellen ondersteunende werkzaamheden niet mee voor het
urencriterium" -- reads as though only the supporting part drops out. The wider
statutory wording governs, and the gap between the two phrasings is one of the
reasons this test is manual review rather than a calculation.

What follows from failing the urencriterium, for that participant only:

| Relief | Effect of failing the urencriterium |
|--------|--------------------------------------|
| Zelfstandigenaftrek and the startersaftrek that increases it | **lost** |
| Aftrek voor speur- en ontwikkelingswerk | **lost** |
| Meewerkaftrek | **lost** |
| Ondernemersaftrek as a whole | **lost** -- "De partner die niet voldoet aan het urencriterium, komt niet in aanmerking voor ondernemersaftrek." |
| MKB-winstvrijstelling | **kept**, because it needs ondernemerschap but no urencriterium (`mkb-winstvrijstelling.md`) |
| Startersaftrek bij arbeidsongeschiktheid | keyed to the **verlaagd urencriterium of 800 hours**, so check it separately (`aanloopfase-en-starters-2025.md`) |

**Manual review.** Both limbs of the main test are judgements: what counts as
ondersteunend, and what a comparable arm's-length partnership would look like in
that trade. Record the facts -- who the participants are and how they are
related, what each of them actually does, how the hours divide between core and
supporting work, and why the partnership was set up this way -- and hand the
conclusion to a human. Do not declare a samenwerkingsverband usual or unusual,
and do not present a zelfstandigenaftrek figure while the test is open.

## Terbeschikkingstellingsregeling (art. 3.91 and art. 3.92) -- manual review

### When it applies

The regeling catches a **verbonden persoon who makes a vermogensbestanddeel
available**, with or without a vergoeding, to someone who uses it for belastbare
winst uit onderneming or belastbaar resultaat uit overige werkzaamheden, **or to
a samenwerkingsverband of which such a person is part** (art. 3.91 lid 1
onderdelen a and b). The typical cases in an IB enterprise are a **pand** and a
**lening**.

- **Verbonden persoon** for art. 3.91 lid 2 onderdeel b: the taxpayer's partner,
  and the minor children of the taxpayer or the partner.
- Art. 3.91 lid 3 extends the regeling to a bloed- of aanverwant in de rechte
  lijn who is not covered by lid 2 onderdeel b, but **only** where the
  terbeschikkingstelling is "in het maatschappelijke verkeer ongebruikelijk".
  Making an asset available with no vergoeding, or at an onzakelijk lage
  vergoeding, is what the Belastingdienst points at here.
- Assets named on the Belastingdienst page: een pand, een schuldvordering, een
  overeenkomst van levensverzekering, en een koopoptie. Art. 3.91 lid 2 onderdeel
  a adds spaarovereenkomsten, genotsrechten and rights or obligations to buy and
  sell; onderdeel d treats a borgtocht fee as a TBS voordeel.
- **Art. 3.92** covers the parallel case of an asset made available to a
  vennootschap in which the taxpayer or a verbonden persoon holds an aanmerkelijk
  belang, or to a samenwerkingsverband of which such a vennootschap is part. Art.
  3.92 lid 4 attributes an asset in an algehele gemeenschap van goederen half to
  each spouse.
- Carve-outs the Belastingdienst states: spouses in gemeenschap van goederen who
  **jointly** make an asset available to one spouse's own onderneming or
  werkzaamheid are not making a terbeschikkingstelling; under huwelijkse
  voorwaarden the opbrengsten are reported. Lending to your own bv in
  rekening-courant does not produce a TBS opbrengst where the loan is **not higher
  than EUR 17,500 during the whole year**, and no interest need then be charged.

### It has its own profit-determination regime

The income is **box 1 income as resultaat uit overige werkzaamheden**, not winst
uit onderneming, and art. 3.95 gives it a regime of its own by applying the winst
articles "alsof de werkzaamheid een onderneming vormt":

| Applies to a TBS-werkzaamheid | Does **not** apply |
|-------------------------------|--------------------|
| art. 3.10 aanloopkosten | investeringsaftrek (art. 3.40 to 3.52), so **no KIA, EIA or MIA** |
| art. 3.13 to 3.21, the vrijgestelde winstbestanddelen and the kostenaftrekbeperkingen | de ondernemersaftrek (art. 3.74 to 3.79) |
| art. 3.25 to 3.30a, goed koopmansgebruik, afschrijving and willekeurige afschrijving | de MKB-winstvrijstelling (art. 3.79a) |
| art. 3.55 to 3.62, the doorschuif- and omzettingsfaciliteiten | -- |
| art. 3.53 lid 1 a and b and lid 2, art. 3.54 herinvesteringsreserve and art. 3.64, added by art. 3.95 lid 2 for art. 3.91 and 3.92 werkzaamheden | -- |

Deductible against the opbrengsten are, among others, rente van schulden, the
costs of geldleningen taken out to acquire the bezittingen, and afschrijvingen
including those on onroerende zaken.

### The terbeschikkingstellingsvrijstelling is 12%

**The terbeschikkingstellingsvrijstelling is 12% of the joint amount of the
resultaat from art. 3.91 and art. 3.92 werkzaamheden** -- the opbrengsten less the
deductible costs. That is the statutory figure in art. 3.99b lid 2, and the
Fiscale informatie chapter on beschikbaar stellen van bezittingen states the same
for 2025: "U krijgt een vrijstelling van 12% van de inkomsten min de aftrekbare
kosten."

**Use 12%. Do not use 12.7%.** One official chapter on beschikbaar stellen van
bezittingen in a later edition prints 12.7%; that is the MKB-winstvrijstelling
percentage and it contradicts every version of art. 3.99b. Recheck art. 3.99b
before the next season, and never carry the MKB percentage across into this
vrijstelling.

Like the MKB-winstvrijstelling, the terbeschikkingstellingsvrijstelling is a
grondslagverminderende post for the tariefsaanpassing when the resultaat is
positive; that cap stays canonical in `../annual/deductions.md`.

### Obligations and exit

- **Administration:** keep an administratie of the assets made available, plus a
  balans and a resultatenrekening. These are sent only on request, not with the
  aangifte.
- **Arm's length:** where no vergoeding, or an onzakelijk lage vergoeding, was
  charged, the amount to report is what would have been received on arm's-length
  terms. Establishing that amount is **manual review**.
- **Ending the terbeschikkingstelling** is a taxable moment: the waarde in het
  economisch verkeer minus the boekwaarde, unless a doorschuiffaciliteit is
  applied. Triggers named by the Belastingdienst include sale, death, the asset
  ceasing to be used in the qualifying way, loss of the aanmerkelijk belang, and
  emigration.
- The resultaat uit het beschikbaar stellen van bezittingen is **not divisible**
  between fiscal partners; `partner-en-meewerken-2025.md` is canonical for what
  may and may not be divided.

**Manual review for the whole regeling.** Record who owns the asset, who uses it,
how the owner and the user are related, what was agreed, what was actually paid,
what the asset cost and when, and what debts and costs attach to it. Do not
compute a TBS resultaat and do not apply the 12% to a figure the agent
constructed.

## Agrarische ondernemingen and zeescheepvaart -- manual review

Two whole classes of enterprise carry their own regimes, their own exemptions and
their own screens in the aangifte. Recognise them, name them, and route them.

- **Agrarische onderneming.** The Fiscale informatie chapter on winst uit
  onderneming carries a separate section for the agrarische onderneming, and a
  separate section on vrijgestelde winstbestanddelen that names the
  **bosbouwvrijstelling**, the **landbouwvrijstelling**, the
  **kwijtscheldingswinstvrijstelling** and the spitsmijdenprojectvrijstelling.
  The landbouwvrijstelling turns on the difference between the waarde in het
  economisch verkeer and the agrarian waarde of land, which is a valuation
  question. **No amount, percentage or valuation rule is established in this
  note.** Ask whether land, a bedrijfswoning or agrarische voorraden are in the
  ondernemingsvermogen, record the answer, and route it to a human.
- **Zeescheepvaart.** The same chapter carries a separate section on winst uit
  zeescheepvaart under the **tonnageregeling**, a regime in which the profit is
  determined from the tonnage of the ship rather than from the ordinary
  winstberekening, and a separate section on the commanditair vennoot in
  film- and zeescheepvaart cv's. **Do not run the ordinary profit chain over a
  tonnageregeling enterprise.** Consequences outside the winstberekening,
  including for the inkomensafhankelijke bijdrage Zorgverzekeringswet, are not
  established here; `zvw-2025.md` stays canonical for the Zvw.

In both cases the workpack should say plainly that the enterprise falls in a
special regime, list the facts collected, and stop.

## Employing staff -- a separate obligation, explain only

Taking on staff does not change the income-tax return by itself. It creates a
**separate tax obligation with its own registration, its own number, its own
return and its own cadence.**

| Element | What is established |
|---------|---------------------|
| Registration deadline | at the latest on the day the first employee starts |
| Form, established in the Netherlands | "Melding Loonheffingen Aanmelding werkgever" |
| Form, established abroad | "Aanmelding Onderneming buitenland" |
| Loonheffingennummer | usually within 1 week; one Belastingdienst page states within 5 working days after the employee's start date |
| Aangiftebrief loonheffingen | states the aangiftetijdvakken, and is issued again every November |
| Sectorindeling letter, where premies werknemersverzekeringen are due | usually within 3 weeks, at most 8 weeks |
| Gedifferentieerde premie Whk percentage | within 4 weeks, and thereafter annually, usually in November or December |
| Loonaangifte cadence | every month or every 4 weeks |

Two facts that prevent wrong conclusions:

- **Getting help in the enterprise is not automatically a dienstbetrekking.** The
  Belastingdienst lists cases in which there may be none: a meewerkende partner, a
  meewerkend kind, uitzendkrachten and ingeleend personeel, ingeschakelde
  freelancers, leerlingen en stagiairs, dienstverleners aan huis and
  pseudowerknemers. The criteria sit in the Handboek Loonheffingen, which is
  outside this knowledge pack.
- **The two returns run on different clocks.** The loonaangifte is monthly or
  four-weekly; the aangifte inkomstenbelasting is annual. A late loonaangifte is
  not fixed by the annual return, and the annual return is not fixed by the
  loonaangifte.

**Explain-only handoff, and manual review for the income-tax consequences.** The
plugin does not compute a loonheffing, a sector premium or a Whk percentage, and
no such percentage is stated in this note. What does belong in the workpack is
the fact pattern: that staff were employed, over what period, and what the wage
and employer costs were, so the personeelskosten line and the related balans
items can be prepared under `zakelijke-schema-2025.md`. Route everything else to
a human or to a payroll adviser.

## Entering, leaving and dissolving a samenwerkingsverband

**Treat every change in the composition of a samenwerkingsverband as a possible
staking until a human says otherwise.** The Belastingdienst names three triggers:

1. bringing an eenmanszaak into a new or existing vof, maatschap, bv or nv;
2. a maat or vennoot **joining** your vof, cv or maatschap;
3. a maat or vennoot **dropping out**, by uittreding or by overlijden.

The stated general consequence: this is treated "in het algemeen als een staking
van uw ondernemersactiviteiten. Daarom moet u de balans opmaken en afrekenen",
and the new form counts "als een nieuw gestarte onderneming". Under conditions
there need be no settlement -- "Onder bepaalde voorwaarden hoeft u niet fiscaal
af te rekenen" -- and whether there is a staking at all "is afhankelijk van veel
factoren". A doorschuiffaciliteit is not automatic: a request must be filed with
the belastingkantoor that handles the taxpayer's inkomstenbelasting.

Related facts worth recording, all of them routed onward:

- **Doorschuiving to a medeondernemer** (art. 3.63): the acquirer must have been
  an ondernemer drawing profit from the onderneming within a samenwerkingsverband
  with the transferor, or an employee in that onderneming, for the **36 months**
  immediately preceding the transfer. The acquirer steps into the transferor's
  place and continues at the existing boekwaarden. A transfer of part of the
  onderneming also qualifies. The period can be shortened in special situations,
  for example arbeidsongeschiktheid or faillissement. The facility requires a
  request made with the transferor's aangifte.
- **Geruisloze omzetting into a bv** requires bringing in the whole onderneming,
  and the shares may not be sold for **3 years**.
- **Btw and loonheffingen follow their own track.** On a change of rechtsvorm or
  samenwerkingsverband there is a new onderneming for the btw, and a new
  btw-identificatienummer may follow that must be passed to EU suppliers
  immediately. A payroll administration must be closed and re-registered, and a
  new loonheffingennummer may follow. Both are outside the workpack; say they
  exist so the taxpayer does not overlook them.
- On immovable property in the ondernemingsvermogen, overdrachtsbelasting is in
  most cases not due -- an explain-only point, not a conclusion.

`staking-2025.md` is canonical for the staking itself, the stakingswinst and the
stakingsaftrek. This note only tells the agent to get the question there.

## Manual-review boundaries

Record the facts, do not compute, and route to manual review:

1. Any **winstaandeel** in a vof, maatschap or cv, and any change in the
   winstverdeling during the year.
2. The **KIA and any other investeringsaftrek** share in a samenwerkingsverband,
   including whether a joint request for a different verdeelsleutel exists.
3. Any **medegerechtigdheid** or profit-sharing geldverstrekking, and above all
   the **art. 3.9 loss cap** and the running capital record it needs.
4. Splitting a **mixed winst** between an ondernemer part and a medegerechtigde
   part.
5. Whether a samenwerkingsverband is **ongebruikelijk**, and whether the work is
   hoofdzakelijk ondersteunend.
6. Every **terbeschikkingstelling** under art. 3.91 or art. 3.92, including
   whether an asset is buitenvennootschappelijk vermogen or a TBS, the
   arm's-length vergoeding, and the exit value.
7. The presentation choice between a **personal** and a **samenwerkingsverband**
   level winst-en-verliesrekening and balans.
8. Any **agrarische onderneming** and any **zeescheepvaart** enterprise.
9. All **loonheffingen** consequences of employing staff.
10. **Entering, leaving or dissolving** a samenwerkingsverband, and any
    doorschuiffaciliteit request.

## Developer instruction

**Be honest with the taxpayer about what this note is for. Its job is
recognition, explanation and routing -- not computation.** Say so when a
samenwerkingsverband is detected, rather than producing figures that look
finished.

1. Screen for the form before anything else, by asking: does anyone else share in
   the profit of this enterprise; what does the KVK registration say; is there a
   written vof-, maatschap- or cv-contract; can you make binding agreements for
   the business; are you liable for its debts; do you own assets used by the
   business but held in your own name; does your fiscale partner, a minor child
   or a connected person make a pand or a lening available to it; did anyone join
   or leave during 2025; did the enterprise employ staff. Ask; never infer the
   answers from silence and never assume there is no samenwerkingsverband.
2. Place each income stream in exactly one row of the recognition table, and say
   out loud which row it is. If two rows are arguable -- ondernemer or
   medegerechtigde is the common one -- that is manual review, not a coin flip.
3. Test ondernemerschap, the urencriterium and every ondernemersaftrek component
   **per participant**, on that person's own facts. Never carry one participant's
   position across to another.
4. When the KIA comes up, state the aggregation rule before any number: the total
   is taken at the level of the samenwerkingsverband plus the taxpayer's
   buitenvennootschappelijke investeringen, the bracket is read off that total,
   and only then is the outcome allocated. Read the brackets from
   `investeringsaftrek.md`. Then stop and route the share to manual review.
5. For a medegerechtigde or a profit-sharing geldverstrekker, say plainly that
   the ondernemersaftrek and the MKB-winstvrijstelling are not available, that
   the investeringsregelingen can still be, and that the art. 3.9 loss cap needs
   a capital record running back to the start of the medegerechtigdheid or to
   1 January 2001, whichever is later. Ask whether that record exists.
6. For an ongebruikelijk samenwerkingsverband, walk both limbs of the test with
   the taxpayer, explain that the consequence is all-or-nothing for the hours of
   that samenwerkingsverband, and note that the MKB-winstvrijstelling survives a
   failed urencriterium while the ondernemersaftrek does not. Do not reach a
   conclusion on either limb.
7. For a terbeschikkingstelling, use **12%** for the vrijstelling and read it from
   this note. Never use 12.7% here. Collect the facts and route the resultaat to
   manual review rather than applying the percentage to a constructed figure.
8. For an agrarische onderneming or a zeescheepvaart enterprise, name the regime,
   state that this note establishes no amounts for it, and route it out. Do not
   run the ordinary profit chain over a tonnageregeling enterprise.
9. For staff, hand over the payroll obligation with its deadlines as listed, state
   that it runs on a different cadence from the annual return, and keep only the
   wage and employer cost facts for the winst-en-verliesrekening. State no premium
   percentage.
10. When anyone joined or left, or the samenwerkingsverband was dissolved, raise
    the staking question immediately, before presenting any relief, and hand it to
    `staking-2025.md` and to manual review.
11. Every portal action stays with the human: you (the taxpayer), and each other
    participant separately, open Mijn Belastingdienst, enter your own winstaandeel
    and your own reliefs in your own aangifte, and submit. The plugin prepares and
    explains the figures and never logs in, enters, or sends anything.
