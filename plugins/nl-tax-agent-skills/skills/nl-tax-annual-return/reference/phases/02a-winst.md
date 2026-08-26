## Phase 2A — Winst uit onderneming

Prepare the business section for an IB-ondernemer with an eenmanszaak and derive
the belastbare winst uit onderneming, which feeds the box 1 income total in
Phase 2. If the taxpayer has no onderneming, emit the canonical "not applicable"
line and continue.

Invoke or inline `nl-tax-winst`. Require a finalized profit-and-loss statement
and finalized balance for 2025. Preserve their evidence provenance and append
only actually consulted entrepreneur `source_id`s to
`sources_loaded_by_workflow.annual_2025` and the active `sources_loaded` mirror.

Read every rate, percentage, cap, hour count and year count from the reviewed
knowledge notes named below. This phase file states the order and the questions;
the knowledge pack states the figures.

### 2A.1 Pre-screen: which income category the activity belongs to

Run this before any profit figure is collected. Load
`_shared/knowledge/years/2025/entrepreneur/row-en-dba-2025.md` and
`_shared/knowledge/years/2025/entrepreneur/ondernemer-criteria.md`.

- Apply the **bron van inkomen** screen first. Activity that is not a source of
  income at all produces neither winst nor resultaat, and neither its income nor
  its costs enter the return.
- Then separate the three categories: winst uit onderneming, loon uit
  dienstbetrekking, and resultaat uit overige werkzaamheden. A KvK registration
  or btw-ondernemerschap alone does not make someone an ondernemer voor de
  inkomstenbelasting.
- Record `business.has_onderneming` as `true`/`false` in the profile (the
  template's boolean enum). Ask the taxpayer; never infer the answer from an
  invoice, a trade name, or the absence of a jaaropgaaf.
- **Resultaat uit overige werkzaamheden is a prepared path, not a dead end.**
  When the screen places the activity there, set `business.has_onderneming` to
  `false`, emit the canonical "not applicable" line for this section, and prepare
  the ROW result in Phase 2 under `row-en-dba-2025.md`. Ondernemersaftrek,
  MKB-winstvrijstelling and investeringsaftrek never apply to a ROW result; the
  bijdrage Zvw does, per `zvw-2025.md`.
- Where the activity may be a dienstbetrekking, use `row-en-dba-2025.md` for the
  explain-only Wet DBA account. Do not judge the arbeidsrelatie for the taxpayer
  and do not draft or assess a modelovereenkomst.
- Record the urencriterium and verlaagd-urencriterium answers, the starter
  history, the S&O-verklaring, the meewerkende-partner hours, and the
  investeringen answer as the taxpayer's own answers, sourced from the
  urenadministratie and their history. An unanswered question is a gap, never a
  "no".

### 2A.2 Collect the chain inputs

Load `_shared/knowledge/years/2025/entrepreneur/winstberekening-2025.md`; it is
canonical for the order and names the component note behind each amount. Collect
these before starting the chain, each one as a question and never as an
assumption or a supplied zero:

- the saldo winst-en-verliesrekening for 2025 and the underlying omzet and
  kosten, organized under the rubrieken in `zakelijke-schema-2025.md`;
- the beperkt aftrekbare kosten and which of the two mutually exclusive routes
  the taxpayer elects (`winst-en-kosten.md`);
- any privegebruik onttrekking for a car, woning or fiets (`vervoer-2025.md`,
  `afschrijving-en-bedrijfsmiddelen-2025.md`);
- the depreciation schedule per asset, with acquisition cost, in-use date,
  useful life and residual value, plus the vermogensetikettering behind each
  asset (`afschrijving-en-bedrijfsmiddelen-2025.md`);
- aanloopkosten and pre-start assets for a first business year
  (`aanloopfase-en-starters-2025.md`);
- the qualifying investments and any disposals of assets on which
  investeringsaftrek was claimed (`investeringsaftrek.md`);
- which ondernemersaftrek components apply, including any startersaftrek
  entitlement (`ondernemersaftrek.md`, `partner-en-meewerken-2025.md`);
- any niet-gerealiseerde zelfstandigenaftrek from earlier years, with the
  beschikking (`verlies-en-verrekening-2025.md`);
- the opening and closing ondernemingsvermogen, priveonttrekkingen and
  -stortingen, asked as separate figures;
- any belastbaar loon or other box 1 income, which the loss set-off and the
  tariefsaanpassing threshold both need.

When an input is missing, ask for it, record it as an open question with the
evidence that would settle it, and stop that line. Do not continue the chain
past it with a placeholder.

Review material purchases and prepaid costs with two independent questions: the
tax cost basis, and whether the item or cost benefits only 2025 or more than one
year. A small-purchase threshold is not by itself a complete depreciation
decision; unresolved treatment stays a focused review question.

### 2A.3 Run the ordered chain

Run the lines strictly in order and print each with its amount, its derivation
and its provenance, so the arithmetic is traceable:

1. **Winst uit onderneming** -- saldo fiscale winstberekening after the fiscal
   corrections.
2. **Minus investeringsaftrek** (KIA, EIA, MIA), plus any
   desinvesteringsbijtelling.
3. **Minus ondernemersaftrek**.
4. **Minus the MKB-winstvrijstelling**.
5. **Belastbare winst uit onderneming** -- the result, which Phase 2 includes in
   the box 1 income total.
6. **Tariefsaanpassing** -- a separate belastingvermeerdering, never added to
   taxable box 1 income.

Two order rules must not be relaxed: the investeringsaftrek is subtracted before
the ondernemersaftrek, and the MKB-winstvrijstelling base is the amount after
both of them.

- Apply the **winst cap** at line 3 and check the starter exception before
  applying it. When the cap bites, compute the niet-gerealiseerde
  zelfstandigenaftrek, say that the Belastingdienst fixes it by beschikking and
  does not apply it automatically, and tell the taxpayer to keep the running
  balance.
- The MKB-winstvrijstelling applies whatever the sign of its base, so it
  **shrinks a loss**. Say so plainly rather than presenting it as a benefit.
- For the tariefsaanpassing, present the threshold, the percentage and the
  resulting maximum rate from the knowledge notes, say that ordinary business
  costs and the investeringsaftrek are not affected, and say that the aangifte
  computes the correction itself. Do not present an agent-computed correction as
  the amount that will be assessed.
- The aangifte computes the ondernemersaftrek components, the total
  ondernemersaftrek, the kleinschaligheidsinvesteringsaftrek, the
  MKB-winstvrijstelling and the belastbare winst itself. Keep those in the
  workpack narrative as expectations the taxpayer checks on screen, and never
  emit them as manual-entry field-map rows.

### 2A.4 Vermogensvergelijking self-check

Carry the reconciliation as an explicit workpack line: the Winstberekening
screen reproduces the profit from the movement in the ondernemingsvermogen, and
for an eenmanszaak it must agree with the saldo winst-en-verliesrekening.

- Ask for the opening and the closing ondernemingsvermogen as **two separate
  figures**, plus priveonttrekkingen en -stortingen, wijzigingen toelaatbare
  reserves, niet- of gedeeltelijk aftrekbare kosten en lasten, and vrijgestelde
  winstbestanddelen. Never carry a prior year's closing column forward and never
  enter zero for a column the taxpayer did not supply.
- Do not invent the signed formula and do not encode a balance tolerance; no
  official source states one. Do not apply an activa-equals-passiva check.
- Report a mismatch with the components it rests on and route it to manual
  review. Never adjust the saldo or a balance figure to force agreement.
- Flag the double-entry facts -- the onttrekking for a car, woning or fiets, and
  a herinvesteringsreserve used on a purchased asset -- so each is entered on
  both screens from a single workpack value.

### 2A.5 Downstream handoffs

Three bases come off different lines of the same chain. Label each with its line
in the workpack and re-read `winstberekening-2025.md` before emitting them.

- **Bijdrage Zvw** uses the **belastbare winst uit onderneming** (line 5). Say
  in the workpack that the ondernemer receives a **second, separate aanslag**
  for the inkomensafhankelijke bijdrage Zorgverzekeringswet alongside the
  aanslag inkomstenbelasting, and that the return covers both. Hand line 5 to
  `_shared/knowledge/years/2025/entrepreneur/zvw-2025.md` for the percentage,
  the maximumbijdrage-inkomen, the interaction with loon, and the treatment of
  an oudedagsreserve release. The bijdrage is never a business cost and never
  re-enters the chain.
- **Lijfrente premiegrondslag** uses the **winst before ondernemersaftrek** of
  the **preceding calendar year** -- for the 2025 return, the 2024 figure, which
  this 2025 chain does not produce. Ask the taxpayer for it separately; record
  this year's line 2 only as an input to the 2026 jaarruimte. Hand the question to
  `_shared/knowledge/years/2025/entrepreneur/inkomensvoorzieningen-2025.md` for
  the jaarruimte and reserveringsruimte, and record the result for Phase 5. AOV
  premiums belong there too; they are never a business cost.
- **Arbeidsinkomen for the arbeidskorting** uses that same line 2 figure. Pass
  it to Phase 5.5; profit enjoyed as a medegerechtigde or a winstdelende
  schuldeiser does not count towards it.

Do not compute the bijdrage Zvw or the lijfrente ruimte in this phase.

### 2A.6 Loss path

A negative belastbare winst uit onderneming is an ondernemingsverlies and leaves
this chain.

- Confirm it survives the MKB-winstvrijstelling, and say in the workpack that
  the exemption made the loss smaller.
- The loss is first set off within 2025 against the taxpayer's own positive box
  1 income, such as loon. Only what remains becomes a verlies uit werk en
  woning.
- Route the carry-back and carry-forward windows, the beschikking, the early
  loss set-off request, and the niet-gerealiseerde zelfstandigenaftrek
  settlement to
  `_shared/knowledge/years/2025/entrepreneur/verlies-en-verrekening-2025.md`.
- A loss year still requires a filed return. Never treat a loss as a reason to
  skip the aangifte.

### 2A.7 Per-form recognition and routing

Recognising a business form is no longer terminal. Name the form, say what it
does to the ondernemer tests, and continue preparing the parts of the return it
does not block, using
`_shared/knowledge/years/2025/entrepreneur/samenwerkingsverband-2025.md` and
`_shared/knowledge/years/2025/entrepreneur/staking-2025.md`.

Route to manual review, without producing a partial calculation:

- the **profit-share computation** of a samenwerkingsverband (vof, maatschap,
  man-vrouwfirma, cv) -- the winstaandeel, the KIA apportionment and the
  per-participant figures;
- the **loss caps** applying to a medegerechtigde or a profit-sharing
  geldverstrekker;
- **DGA or BV winst**;
- **agrarische ondernemingen** (landbouwvrijstelling);
- **zeevarenden** (zeescheepvaart);
- the **stakingswinst computation**, doorschuiving and the stakingslijfrente;
- any **herinvesteringsreserve** movement;
- the **oudedagsreserve wind-down computation**;
- **terbeschikkingstelling** of assets to a connected company or enterprise.

For each, record the collected facts, name the figure that could not be computed
and why, and hand it to professional review.

Where the fiscale partner works in the enterprise, use
`_shared/knowledge/years/2025/entrepreneur/partner-en-meewerken-2025.md` to pick
between meewerkaftrek, arbeidsbeloning, a real dienstbetrekking, and the partner
becoming medeondernemer. A real dienstbetrekking is payroll and stays manual
review. Winst uit onderneming is not a gemeenschappelijk inkomensbestanddeel, so
none of this is a partner-allocation choice.

### 2A.8 Field-map readiness

Derive readiness from the same rollup as the STATUS banner. The annual field map
reaches `readiness: review_ready` when the reviewed zakelijke schema covers
every business rubriek and question this case needs and no routing marker in
2A.7 applies. It stays `readiness: draft` with the blocker
`business-section schema review` when a needed rubriek, question or identifier
falls outside the reviewed schema, or when a routing marker applies.

Coverage is an explicit case audit, not an inference from totals. Review every
W&V, balance, private-movement, prior-year-set-off and entrepreneur-question row
in `zakelijke-schema-2025.md` and classify it as mapped, sourced not applicable,
or unresolved. Never turn an omitted yes/no question into `false`. Any unresolved
classification keeps the map draft even if a structural validator accepts the
minimum anchors.

Keep every `onderneming.*` row conditional or optional, never required, and
create manual-entry ids only for figures the taxpayer actually types.

### 2A.9 Preparation boundary

Preparation only. **You (the taxpayer) or an authorized human** open Mijn
Belastingdienst, type every value, review it, sign and send. This plugin never
opens or operates the portal. The zakelijk deel is never prefilled, so an empty
box carries no information: ask for the figure or record the gap, and never read
a blank as a zero.

---
