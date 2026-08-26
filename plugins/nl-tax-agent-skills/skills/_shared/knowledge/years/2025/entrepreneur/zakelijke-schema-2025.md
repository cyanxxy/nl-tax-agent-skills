# Rule note: Zakelijk deel van de aangifte 2025

source_ids: bd_aangifte_ondernemers_2025, bd_ondernemer_cijfers_aangifte_2025, bd_fisin_2025_h7, bd_ola_ih2025_wv_opbrengsten, bd_ola_ih2025_wv_afschrijvingen, bd_ola_ih2025_wv_overige_bedrijfskosten, bd_ola_ih2025_wv_buitengewoon, bd_ola_ih2025_activa_materieel, bd_ola_ih2025_passiva_ondernemingsvermogen, bd_ola_ih2025_winstberekening, bd_ola_ih2025_urencriterium_vraag
workflow: annual_return
tax_year: 2025
status: active
last_reviewed: "2026-08-15"
review_status: reviewed

## Rule

This note is canonical for the **shape** of the zakelijk deel of the 2025
aangifte inkomstenbelasting: which rubrieken the winst-en-verliesrekening and the
balans contain, which yes/no questions the form asks the ondernemer, where
priveonttrekkingen and -stortingen sit, which facts have to be entered twice, and
the `onderneming.*` field identifiers the field mapper uses for them. It is not
canonical for amounts: rates, percentages and thresholds stay in the sibling
notes -- `winst-en-kosten.md` (cost limits, werkruimte, car and per-kilometre
rules, bewaarplicht), `afschrijving-en-bedrijfsmiddelen-2025.md` (depreciation
maxima, the bodemwaarde and the afschrijvingsbeperking on gebouwen,
vermogensetikettering, the woningforfait, and the fiscale reserves),
`ondernemersaftrek.md`, `mkb-winstvrijstelling.md`, `investeringsaftrek.md`,
`ondernemer-criteria.md` (ondernemer status and the urencriterium), and
`entrepreneur-aangifte.md` (portal, channel, deadlines, evidence to collect).

These are reference notes for workpack preparation -- not final tax advice.

## The two-part return, and what is never prefilled

- The ondernemer's aangifte has a **privedeel** and a **zakelijk deel**. Both sit
  in the same aangifte inkomstenbelasting on Mijn Belastingdienst; see
  `entrepreneur-aangifte.md` for portal and channel.
- The vooraf ingevulde aangifte fills only the privedeel. The **zakelijk deel is
  never prefilled** -- balans, winst-en-verliesrekening, the ondernemersaftrek
  questions and the priveonttrekkingen all start empty and are typed in by the
  taxpayer from the finalized jaarstukken.
- Because nothing arrives prefilled, an empty box in the zakelijk deel carries no
  information. Never read a blank as a zero and never fill one in on that basis:
  ask the taxpayer for the figure, or record the gap.
- Preparation only. **You (the taxpayer) or an authorized human** open Mijn
  Belastingdienst, type every value, review it, sign and send. This plugin never
  opens or operates the portal.

## What the taxpayer enters, and what the aangifte computes

The division is load-bearing for the field map:

- **The taxpayer enters** the winst-en-verliesrekening rubrieken, the balans
  columns, the priveonttrekkingen and -stortingen, and the answers to the
  eligibility questions below.
- **The aangifte computes the zelfstandigenaftrek** from the eligibility
  answers. The Belastingdienst states it directly: the aangifte puts a number of
  questions to establish entitlement, and "wordt de zelfstandigenaftrek
  automatisch afgetrokken van uw winst". The startersaftrek is added to that
  amount rather than claimed separately, so it follows the same route. The
  MKB-winstvrijstelling likewise follows from the figures: the winst is first
  reduced by the ondernemersaftrek and the exemption percentage is applied to
  the result. The total ondernemersaftrek and the belastbare winst are sums of
  those outcomes.
- **Not established for the remaining deduction screens.** No reviewed official
  page states whether the aangifte derives the aftrek voor speur- en
  ontwikkelingswerk, the meewerkaftrek, the stakingsaftrek or the
  kleinschaligheidsinvesteringsaftrek from entered data, or asks the taxpayer
  for an amount. For the S&O-aftrek the Belastingdienst points at the RVO
  verklaring and says the deductible amount is stated in it, which reads more
  like an amount the taxpayer carries across than one the form derives. Do not
  assert either way. When a case actually claims one of these, tell the taxpayer
  to read what that screen asks and record what they report; keep the business
  field map `draft` with the `business-section schema review` blocker until the
  screen is established, because a manual-entry checklist that silently omits a
  box the form does ask for is worse than one that admits the gap.
- Therefore: do **not** create manual-entry field ids for the belastbare winst,
  the zelfstandigenaftrek, the startersaftrek, the total ondernemersaftrek, the
  MKB-winstvrijstelling, or the kleinschaligheidsinvesteringsaftrek. The first
  five are outputs of the form rather than boxes the taxpayer types into; the
  KIA is included because its screen is not established either way and inventing
  a manual-entry instruction for it would be a guess. Present each of them in
  the workpack narrative as a computed expectation the taxpayer checks against
  the screen, never as an instruction to enter a number.
- **One carve-out: the niet-gerealiseerde zelfstandigenaftrek.** The form
  derives the *base* zelfstandigenaftrek from the figures and the urencriterium
  answer, but it does not know a niet-gerealiseerde-zelfstandigenaftrek balance
  carried forward from an earlier year. That set-off takes effect as an increase
  of the zelfstandigenaftrek, and the Belastingdienst states that the taxpayer
  tracks what has already been settled and enters the amount in the aangifte --
  "dat gebeurt namelijk niet automatisch". Treat the NGZ set-off amount as a
  **taxpayer-entered figure with its own field id**, read off the NGZ
  beschikking. The prohibition above covers the computed zelfstandigenaftrek
  line, never this input. `verlies-en-verrekening-2025.md` and
  `ondernemersaftrek.md` are canonical for the balance, the 9-year window and
  the set-off condition; where the form presents the box is not established in
  this note, so have the taxpayer confirm the screen and record a gap rather
  than guessing a rubriek.

## Ordering: a checklist, not a wizard

The exact left-to-right screen order the online aangifte uses is **not
published**. Only a partial ordering is established, and it follows from where
the form takes figures from, not from any documented sequence:

- The **Winstberekening** screen shows the saldo of the winst-en-verliesrekening,
  and its sibling amounts come from Priveonttrekkingen en -stortingen,
  Wijzigingen toelaatbare reserves, Niet- of gedeeltelijk aftrekbare kosten en
  lasten, Vrijgestelde winstbestanddelen, and the Passiva/Ondernemingsvermogen
  begin- and eindbalans. Those inputs have to exist before the winstberekening
  reconciles.
- The **ondernemersaftrek** questions depend on the urencriterium answer.
- The **onttrekking** for private use of a car, a woning or a fiets is entered in
  two places, so neither screen is complete until the other agrees.

Present the zakelijk deel as a **checklist of rubrieken and questions**. Never
number the sections as portal steps, never tell the taxpayer "screen 3 of 9", and
never claim a section comes before or after another beyond the data dependencies
above. Section names and label wording can change between filing seasons --
recheck before the 2026 season.

## Winst-en-verliesrekening -- rubriek inventory

- **Opbrengsten.** Netto-omzet (bruto-omzet minus the btw charged on the turnover
  and minus discounts and the like); wijzigingen in voorraden gereed product en
  onderhanden werk; geactiveerde productie voor het eigen bedrijf; overige
  opbrengsten. The screen also carries fields for loon that belongs to the
  opbrengsten of this onderneming and the loonheffing withheld on it -- when the
  taxpayer has such loon, route the treatment to manual review rather than
  assuming where it belongs.
- **Inkoopkosten en uitbesteed werk.** Kosten van grond- en hulpstoffen;
  inkoopprijs van de verkopen; kosten van uitbesteed werk en andere externe
  kosten (which includes winstaandelen paid as consideration for a licence or a
  patent).
- **Personeelskosten.** Lonen en salarissen (the total brutolonen per the
  verzamelloonstaat); arbeidsbeloning aan de fiscale partner; sociale lasten;
  pensioenlasten; plus overige personeelskosten and received uitkeringen en
  subsidies. The arbeidsbeloning field is only filled when the vergoeding to the
  fiscale partner was **EUR 5,000 or more**; below that amount it is not entered
  here -- see `ondernemersaftrek.md`, where the same threshold governs the
  meewerkaftrek.
- **Afschrijvingen.** Asked per asset class: goodwill; overige immateriele vaste
  activa; gebouwen en terreinen; machines en installaties; productierechten;
  overige materiele vaste activa. Willekeurige afschrijvingen are included in
  these amounts. For a gebouw in eigen gebruik the form asks for the bodemwaarde
  taken from the **WOZ-beschikking 2025 with waardepeildatum 1 January 2024**.
  Depreciation ceilings, the bodemwaarde and the afschrijvingsbeperking on
  gebouwen live in `afschrijving-en-bedrijfsmiddelen-2025.md`.
- **Overige bedrijfskosten.** Auto- en transportkosten; huisvestingskosten (huur,
  gas, water, licht, opstalverzekering); onderhoudskosten van overige materiele
  vaste activa; verkoopkosten; and a free field Andere kosten for anything the
  other boxes on the screen do not cover. Two placement rules from the form's own
  help: business use of a **private** vehicle is a cost entered here at the
  per-kilometre amount in `winst-en-kosten.md`; the **bijtelling** for private use
  of a business car is **not** entered here -- it belongs under buitengewone
  baten (see the double-entry section). A werkruimte in the taxpayer's own home is
  usually not deductible; apply the test in `winst-en-kosten.md`.
- **Waardeveranderingen.** Overige waardeveranderingen van immateriele en
  materiele vaste activa; bijzondere waardeverminderingen van vlottende activa.
  An upward revaluation is entered with a minus sign.
- **Financiele baten en lasten.** Opbrengsten van overige vorderingen; rente op
  banktegoeden; ontvangen dividend; kwijtscheldingswinst; waardeverandering van
  vorderingen; waardeverandering van effecten; kosten van schulden, rentelasten
  en soortgelijke kosten. Dividend is entered **gross**, including the
  dividendbelasting, with a follow-up yes/no on Dutch dividendbelasting withheld.
- **Buitengewone baten en lasten.** Baten: the onttrekking for privegebruik of an
  auto, a woning or a fiets van de onderneming; opheffing of a positieve
  terugkeerreserve; boekwinst op activa; prijzengeld won by the ondernemer (with
  follow-up questions on kansspelbelasting). Lasten: afboeking van de
  herinvesteringsreserve op gekochte activa; boekverlies op activa; opheffing of
  a negatieve terugkeerreserve.
- **Saldo fiscale winstberekening.** The total of the rubrieken above. The form
  derives it; carry it in the workpack as a figure to check on screen, not as a
  box to type into.

## Balans -- rubriek inventory, two columns

The balans is asked in **two columns: begin boekjaar and einde boekjaar**. The
form's own wording for a debt rubriek is "vul in: de schulden ... aan het begin en
aan het einde van het boekjaar", and the same two-column layout runs through the
balans.

**Activa**

- Immateriele vaste activa: goodwill; vergunningen, concessies en intellectuele
  eigendommen; kosten van onderzoek en ontwikkeling (capitalised only for
  concrete technologies and products); productierechten voor agrariers.
- Materiele vaste activa: (bedrijfs)gebouwen en terreinen; machines en
  installaties; inventaris; auto's en overige transportmiddelen; vaste
  bedrijfsmiddelen in uitvoering en vooruitbetaalde bedragen. For machines and
  installations and for overige materiele vaste activa the form also asks the
  kosten van aanschaf of voortbrenging and the restwaarde. Buildings are specified
  separately with their bodemwaarde.
- Financiele vaste activa.
- Voorraden: grond- en hulpstoffen; onderhanden werk; gereed product en
  handelsgoederen; vooruitbetaald bedrag op voorraden. Onderhanden werk is its own
  field with voortschrijdende winstneming -- a half-finished job carries half the
  agreed price.
- Vorderingen: vordering omzetbelasting; kortlopende vorderingen op gelieerde
  maatschappijen; kortlopende vorderingen op participanten; vorderingen op
  handelsdebiteuren; overlopende activa. A vordering omzetbelasting must be
  specified across dit boekjaar / het vorige boekjaar / oudere boekjaren.
  Handelsvorderingen ask both the nominale waarde and the boekwaarde.
- Effecten.
- Liquide middelen.

**Passiva**

- Ondernemingsvermogen. The fiscale ondernemingsvermogen is stated as consisting
  of eigen vermogen, egalisatiereserve, herinvesteringsreserve and
  oudedagsreserve -- so the **fiscale reserves are entered inside the
  ondernemingsvermogen rubriek, not as a separate top-level passiva rubriek**.
  Eigen vermogen equals bezittingen minus schulden. Toevoegingen aan de
  oudedagsreserve are no longer possible; a decrease of the oudedagsreserve
  increases the eigen vermogen by the same amount (see `ondernemersaftrek.md` and
  `winst-en-kosten.md`). A herinvesteringsreserve is specified per vervreemd
  bedrijfsmiddel: omschrijving, jaar van vervreemding, (resterende) boekwinst,
  afschrijvingspercentage, and boekwaarde op het vervreemdingsmoment.
- Voorzieningen: garantievoorziening; lijfrentevoorziening; pensioenvoorziening;
  VUT-voorziening; milieuvoorziening. The garantievoorziening and the overige
  voorzieningen each need a specification per item (omschrijving, dotatie,
  onttrekking, boekwaarde einde boekjaar), and the form states that the total of
  the specification must equal the amount entered as boekwaarde einde boekjaar.
- Langlopende schulden: schulden aan kredietinstellingen; obligaties; onderhandse
  leningen; langlopende schulden aan gelieerde maatschappijen; langlopende
  schulden aan participanten. Interest-bearing debts at nominal value;
  interest-free or very-low-interest debts at contante waarde.
- Kortlopende schulden: schulden aan leveranciers en handelscrediteuren;
  omzetbelasting; loonheffingen; kortlopende schulden aan gelieerde
  maatschappijen; kortlopende schulden aan participanten; overlopende passiva.
  Omzetbelasting as a debt is specified across dit boekjaar / het vorige boekjaar
  / oudere boekjaren. Loonheffingen covers the last filed monthly return plus
  amounts found while preparing the jaarstukken.

### Two boundaries on the balans

- **The opening column is not assumed.** It is not established that the aangifte
  carries last year's closing balance into this year's opening balance; the form
  puts an aansluitvraag to the taxpayer instead. Always ask the taxpayer for
  **both** the begin- and the eindbalans column, from the finalized jaarstukken.
  Never copy a prior-year figure forward on the plugin's own initiative and never
  enter zero for an opening column that was not supplied.
- **No balance rule is imposed.** This note deliberately states no rule that the
  activa side must equal the passiva side, and no tolerance for a difference; no
  official page states one. If the taxpayer's own jaarstukken do not tie, that is
  a question for the taxpayer or their accountant -- record it, do not resolve it
  and do not treat it as a plugin check.

## Entrepreneur questions the form asks

These are answers, not amounts. The workpack must carry the taxpayer's own answer
to each, sourced from the urenadministratie and the taxpayer's history.

- **Urencriterium gehaald?** A yes/no: choose yes when the ondernemer spent at
  least **1,225 hours** in 2025 actually running the onderneming(en). The 1,225
  hours are **not** recalculated for a part year of entrepreneurship. Hours not
  worked over a total of 16 weeks of pregnancy count towards the criterion. The
  second condition (more time on the onderneming than on other work) and the
  starter exception to it live in `ondernemer-criteria.md`.
- **Verlaagd urencriterium?** A conditional follow-up: at least **800** but no
  more than 1,225 hours in 2025. Relevant only for the startersaftrek bij
  arbeidsongeschiktheid in `ondernemersaftrek.md`.
- **Starter history.** Whether the taxpayer was **not** an ondernemer voor de
  inkomstenbelasting in one or more of the five preceding calendar years, and how
  often the zelfstandigenaftrek has already been applied in those years. Ask for
  both facts; do not infer either from the absence of prior workpacks. Conditions
  are in `ondernemersaftrek.md`.
- **S&O-verklaring.** Whether an S&O-verklaring from RVO was issued for 2025, and
  whether at least **500** hours were spent on recognised speur- en
  ontwikkelingswerk. Amounts are in `ondernemersaftrek.md`.
- **Meewerkende partner -- hours.** The number of hours the fiscale partner
  worked in the onderneming, and whether the partner worked unpaid or for a
  vergoeding. The meewerkaftrek only starts to apply from **525** partner hours;
  the band table and the EUR 5,000 vergoeding boundary are in
  `ondernemersaftrek.md`.
- **Investeringen.** Whether the onderneming invested in bedrijfsmiddelen in
  2025, with the per-asset details needed for the investeringsaftrek. Amounts,
  per-asset minima, exclusions and the desinvesteringsbijtelling are in
  `investeringsaftrek.md`.

## Priveonttrekkingen en -stortingen

- The screen **Priveonttrekkingen en -stortingen** records what left the
  onderneming for private purposes and what the taxpayer put in from private
  funds. Private use of a business asset is recorded as a priveonttrekking.
- Its amounts feed the winstberekening below. The full sub-field inventory of
  this screen is not captured in this note -- ask the taxpayer to record each box
  the form actually presents, and do not invent sub-categories.
- Never treat priveonttrekkingen as a business cost, and never net onttrekkingen
  against stortingen before entry.

## Double-entry fields -- the same fact on two screens

These are the highest-value lines for the manual-entry checklist, because a
figure entered on one screen and forgotten on the other produces a return that
does not reconcile.

| Fact | Screen 1 | Screen 2 |
|---|---|---|
| Onttrekking privegebruik **auto** van de onderneming | Winst-en-verliesrekening > Buitengewone baten en lasten > Overige buitengewone baten | Priveonttrekkingen en -stortingen |
| Onttrekking privegebruik **woning** van de onderneming | Winst-en-verliesrekening > Buitengewone baten en lasten > Overige buitengewone baten | Priveonttrekkingen en -stortingen |
| Onttrekking privegebruik **fiets** van de onderneming | Winst-en-verliesrekening > Buitengewone baten en lasten > Overige buitengewone baten | Priveonttrekkingen en -stortingen |
| **Herinvesteringsreserve** used on a purchased asset | Winst-en-verliesrekening > Buitengewone lasten > Afboeking van de herinvesteringsreserve op gekochte activa | Balans > Passiva > Ondernemingsvermogen > herinvesteringsreserve, specified per vervreemd bedrijfsmiddel |

Rules that go with the table:

- The **same amount** goes in both places for each onttrekking. Put the figure in
  the workpack once, and print it twice in the manual-entry checklist with both
  screen paths, so the taxpayer cannot enter one and skip the other.
- The **fiets** onttrekking is the bijtelling: 7% of the consumentenadviesprijs
  minus the taxpayer's own contribution. The auto and woning amounts follow the
  bijtelling rules in `winst-en-kosten.md`; do not restate percentages here.
- The auto bijtelling must **not** be entered under Overige bedrijfskosten >
  auto- en transportkosten. That box is for the costs of the vehicle, not for the
  private-use addition.
- A herinvesteringsreserve is a multi-year balance-sheet item. Record the facts
  and route the sizing and the boekwaarde-eis to manual review; do not compute a
  reserve movement.

## Vermogensvergelijking -- the self-check

The **Winstberekening** screen is a vermogensvergelijking. It reconciles the
movement in the ondernemingsvermogen to the profit shown by the
winst-en-verliesrekening.

- Inputs shown on that screen come from: Priveonttrekkingen en -stortingen;
  Wijzigingen toelaatbare reserves; Niet- of gedeeltelijk aftrekbare kosten en
  lasten; Vrijgestelde winstbestanddelen; and the Passiva/Ondernemingsvermogen at
  begin and einde boekjaar.
- For an **eenmanszaak** the comparison figure is the **Saldo
  winst-en-verliesrekening** taken from the Winst-en-verliesrekening. The form
  states that this amount must be equal to the amount computed at Winstberekening.
- For a **samenwerkingsverband** the comparison figure is instead the Totaal
  winstaandeel from Kapitaal- en winstaandeel in het samenwerkingsverband, and a
  participant enters only their proportional share of each reserve. Partnerships
  (vof, maatschap, man-vrouwfirma) are outside the supported scope -- stop and
  route the whole business section to manual review.
- Carry this as an explicit self-check line in the workpack: the winstberekening
  must reconcile to the saldo of the winst-en-verliesrekening. If it does not,
  the jaarstukken and the entered figures disagree; report the difference to the
  taxpayer and do not adjust a figure to force the reconciliation.
- The sign convention for each adjustment on that screen is not established in
  this note. Take it from the form's own invulhulp on screen rather than deriving
  it.

## Field identifiers

Naming scheme: `onderneming.wv.<rubriek>` for the winst-en-verliesrekening,
`onderneming.balans.<rubriek>_begin` and `_eind` for the two balans columns,
`onderneming.vraag.<question>` for a yes/no or a count,
`onderneming.prive.<item>` for the priveonttrekkingen and -stortingen, and
`onderneming.verrekening.<item>` for an amount carried forward from an earlier
year. Every `onderneming.*` row is conditional or optional -- never required --
because a taxpayer without an onderneming has none of them.

### Winst-en-verliesrekening

| Rubriek (NL) | field_id | English gloss |
|---|---|---|
| Netto-omzet | `onderneming.wv.netto_omzet` | Net turnover |
| Wijzigingen in voorraden gereed product en onderhanden werk | `onderneming.wv.voorraadmutatie` | Change in finished goods and work in progress |
| Geactiveerde productie voor het eigen bedrijf | `onderneming.wv.geactiveerde_productie` | Own work capitalised |
| Overige opbrengsten | `onderneming.wv.overige_opbrengsten` | Other operating income |
| Inkoopkosten en uitbesteed werk | `onderneming.wv.inkoopkosten` | Cost of purchases and outsourced work |
| Personeelskosten | `onderneming.wv.personeelskosten` | Personnel costs |
| Arbeidsbeloning aan de fiscale partner | `onderneming.wv.arbeidsbeloning_partner` | Remuneration paid to the fiscal partner |
| Afschrijvingen | `onderneming.wv.afschrijvingen` | Depreciation |
| Huisvestingskosten | `onderneming.wv.huisvestingskosten` | Premises costs |
| Auto- en transportkosten | `onderneming.wv.auto_transportkosten` | Vehicle and transport costs |
| Verkoopkosten | `onderneming.wv.verkoopkosten` | Selling costs |
| Andere kosten | `onderneming.wv.andere_kosten` | Other operating costs |
| Waardeveranderingen | `onderneming.wv.waardeveranderingen` | Value changes and impairments |
| Financiele baten en lasten | `onderneming.wv.financiele_baten_lasten` | Financial income and expense |
| Buitengewone baten en lasten | `onderneming.wv.buitengewone_baten_lasten` | Extraordinary income and expense |
| Overige buitengewone baten | `onderneming.wv.overige_buitengewone_baten` | Other extraordinary income |
| Saldo fiscale winstberekening | `onderneming.wv.saldo` | Balance of the profit and loss account |

`onderneming.wv.saldo` is a total the form derives. Record it as a figure the
taxpayer checks on screen, never as a manual-entry instruction.

### Balans

Each rubriek takes two identifiers, one per column.

| Rubriek (NL) | field_id (begin / eind) | English gloss |
|---|---|---|
| Immateriele vaste activa | `onderneming.balans.immateriele_vaste_activa_begin` / `_eind` | Intangible fixed assets |
| Materiele vaste activa | `onderneming.balans.materiele_vaste_activa_begin` / `_eind` | Tangible fixed assets |
| Financiele vaste activa | `onderneming.balans.financiele_vaste_activa_begin` / `_eind` | Financial fixed assets |
| Voorraden | `onderneming.balans.voorraden_begin` / `_eind` | Inventories |
| Vorderingen | `onderneming.balans.vorderingen_begin` / `_eind` | Receivables |
| Effecten | `onderneming.balans.effecten_begin` / `_eind` | Securities |
| Liquide middelen | `onderneming.balans.liquide_middelen_begin` / `_eind` | Cash and bank balances |
| Ondernemingsvermogen | `onderneming.balans.ondernemingsvermogen_begin` / `_eind` | Business equity |
| Fiscale reserves (binnen het ondernemingsvermogen) | `onderneming.balans.fiscale_reserves_begin` / `_eind` | Tax-recognised reserves |
| Voorzieningen | `onderneming.balans.voorzieningen_begin` / `_eind` | Provisions |
| Langlopende schulden | `onderneming.balans.langlopende_schulden_begin` / `_eind` | Long-term liabilities |
| Kortlopende schulden | `onderneming.balans.kortlopende_schulden_begin` / `_eind` | Short-term liabilities |

### Vragen

| Vraag (NL) | field_id | English gloss |
|---|---|---|
| Voldeed u aan het urencriterium? | `onderneming.vraag.urencriterium` | Met the 1,225-hour test in 2025 (yes/no) |
| Voldeed u aan het verlaagd-urencriterium? | `onderneming.vraag.verlaagd_urencriterium` | Met the 800-hour reduced test (yes/no) |
| Startershistorie | `onderneming.vraag.starter_historie` | Non-entrepreneur in one of the five preceding years, and how often the zelfstandigenaftrek was applied |
| S&O-verklaring | `onderneming.vraag.so_verklaring` | Holds an RVO research-and-development statement for 2025 (yes/no) |
| Uren meewerkende fiscale partner | `onderneming.vraag.meewerkende_partner_uren` | Hours the fiscal partner worked in the enterprise |
| Investeringen in bedrijfsmiddelen | `onderneming.vraag.investeringen` | Invested in business assets in 2025 (yes/no, with per-asset detail) |

### Verrekening uit eerdere jaren

| Item (NL) | field_id | English gloss |
|---|---|---|
| Te verrekenen niet-gerealiseerde zelfstandigenaftrek | `onderneming.verrekening.niet_gerealiseerde_zelfstandigenaftrek` | Carried-forward unrealised self-employed deduction settled in 2025, from the beschikking |

This row is conditional, like every other `onderneming.*` row. Do not name it
`onderneming.zelfstandigenaftrek` -- that id stays forbidden.

### Priveonttrekkingen en -stortingen

| Item (NL) | field_id | English gloss |
|---|---|---|
| Priveonttrekkingen | `onderneming.prive.onttrekkingen` | Private withdrawals |
| Privestortingen | `onderneming.prive.stortingen` | Private contributions |
| Onttrekking privegebruik auto | `onderneming.prive.onttrekking_auto` | Private use of a business car |
| Onttrekking privegebruik woning | `onderneming.prive.onttrekking_woning` | Private use of a home held as business property |
| Onttrekking privegebruik fiets | `onderneming.prive.onttrekking_fiets` | Private use of a business bicycle |

The three onttrekking identifiers each appear twice in the manual-entry
checklist, once per screen path in the double-entry table above. They are one
value, not two.

## Developer instruction

1. Read this note before building the business section of a workpack or a field
   map. Read rates and thresholds from the sibling notes named in `## Rule`; this
   note is canonical only for the schema, the questions, and the identifiers.
2. Present the zakelijk deel as a **checklist** of rubrieken and questions. Do not
   number the sections as portal steps and do not assert a screen order beyond the
   data dependencies listed under "Ordering". Only a partial ordering is
   established.
3. Ask the taxpayer for the **begin** and **eind** column of every balans rubriek
   separately. Do not carry a prior-year closing figure into the opening column,
   and do not enter zero for a column the taxpayer has not supplied. Record a
   missing column as a gap.
4. Do not apply any activa-equals-passiva check or tolerance. If the supplied
   jaarstukken do not tie, report the difference to the taxpayer as a bookkeeping
   question and continue.
5. Create manual-entry field ids only for figures the taxpayer types. Do not
   create ids for the belastbare winst, the zelfstandigenaftrek, the
   startersaftrek, the S&O-aftrek, the meewerkaftrek, the stakingsaftrek, the
   total ondernemersaftrek, the MKB-winstvrijstelling, or the
   kleinschaligheidsinvesteringsaftrek. Show those in the workpack narrative as
   computed expectations the taxpayer verifies on screen. **Exception:** a
   carried-forward niet-gerealiseerde zelfstandigenaftrek IS a figure the
   taxpayer types. When the taxpayer carries a balance evidenced by the
   beschikking, create
   `onderneming.verrekening.niet_gerealiseerde_zelfstandigenaftrek` and print it
   on the manual-entry checklist; never suppress it under the
   zelfstandigenaftrek ban. If the beschikking cannot be produced, record the
   balance as not established and route it to manual review
   (`verlies-en-verrekening-2025.md`).
6. Keep every `onderneming.*` row conditional or optional in the field map, never
   required.
7. Print each double-entry fact twice in the manual-entry checklist, once per
   screen path, from a single value in the workpack. Explicitly warn that the
   auto bijtelling does not go under auto- en transportkosten.
8. Carry the vermogensvergelijking self-check as a workpack line: the
   winstberekening must reconcile to the saldo of the winst-en-verliesrekening.
   Report a difference; never adjust a figure to make it reconcile.
9. Ask the taxpayer for each entrepreneur question rather than inferring an
   answer, and never assume a zero, a "no", or an absent history. Record
   unanswered questions as gaps.
10. This note does not capture the sub-field inventory for financiele vaste
    activa, effecten, liquide middelen, or for the Priveonttrekkingen en
    -stortingen screen. Ask the taxpayer to record the boxes the form actually
    presents for those, and route anything unclear to manual review instead of
    inventing sub-categories.
11. Route to manual review, without computing: any samenwerkingsverband (vof,
    maatschap, man-vrouwfirma), any herinvesteringsreserve movement, any staking,
    and any waardeveranderingen or voorzieningen the taxpayer cannot substantiate
    from the finalized jaarstukken.
12. Keep this prep-only. Phrase every portal step with a human subject -- "You
    (the taxpayer) enter this in Mijn Belastingdienst" -- and never present the
    workpack as a filed or final return.
13. Label wording and section names can change between filing seasons. Recheck
    this inventory before the 2026 season and confirm anything the taxpayer sees
    on screen that does not match.
