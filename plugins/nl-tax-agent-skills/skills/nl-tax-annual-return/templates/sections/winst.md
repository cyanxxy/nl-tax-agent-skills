## Winst uit onderneming notes

[If no onderneming, emit exactly these two lines and skip the rest of this section:

> Not applicable -- no winst uit onderneming reported.
> business.has_onderneming: no
]

Require a finalized 2025 profit-and-loss statement and finalized 2025 balance,
then run the ordered chain below. Every amount comes from the reviewed
entrepreneur knowledge notes; this template never carries a rate of its own. A
missing input is a `?` row and an open question, never a zero.

### Income-category screen

- Bron van inkomen confirmed (the activity is a source of income): [yes/no/open question] -- Src: [F/U/A/?]
- Category: [winst uit onderneming / resultaat uit overige werkzaamheden / loon uit dienstbetrekking / open question] -- Src: [F/U/A/?]
- Ondernemer voor de inkomstenbelasting (eenmanszaak / ZZP): [yes/no/manual review] -- Src: [F/U/A/?]
- Urencriterium met: [yes/no/open question] -- Src: [F/U/A/?]
- Verlaagd urencriterium: [yes/no/not applicable/open question] -- Src: [F/U/A/?]
- Starter history, S&O-verklaring, meewerkende-partner hours, investeringen answer: [answers] -- Src: [F/U/A/?]

[Resultaat uit overige werkzaamheden is prepared under "Other box 1 income" in
the Income notes section, not here. If the category is ROW, emit the canonical
"not applicable" lines above and prepare it there.]

### Finalized accounts evidence

| Item | Status / evidence | Src |
|------|-------------------|-----|
| Finalized profit-and-loss statement for 2025 | [reviewed/missing/open question] | [F/U/?] |
| Finalized balance for 2025 (begin and eind column) | [reviewed/missing/open question] | [F/U/?] |

### Ordered profit chain

| Line | Step | Amount | Derivation | Src |
|------|------|--------|------------|-----|
| A | Winst uit onderneming (saldo fiscale winstberekening, after fiscal corrections) | EUR [amount] | [omzet minus kosten, corrections named] | [F/U/A/?] |
| B | Minus investeringsaftrek (KIA/EIA/MIA), plus any desinvesteringsbijtelling | EUR [amount] | C:A-investeringsaftrek | [F/U/A/?] |
| C | Minus ondernemersaftrek | EUR [amount] | C:B-ondernemersaftrek | [F/U/A/?] |
| D | Minus MKB-winstvrijstelling (base is line C) | EUR [amount] | C:C-mkb_vrijstelling | [F/U/A/?] |
| E | **Belastbare winst uit onderneming** | **EUR [amount]** | C:line D | C:chain |

Line E is a component of the Box 1 income total above. Two order rules are
load-bearing: the investeringsaftrek is subtracted before the ondernemersaftrek,
and the MKB-winstvrijstelling base is the amount after both.

- Winst cap on the ondernemersaftrek applied at line C: [applied / not applicable / starter exception applies] -- Src: [C/U/?]
- Niet-gerealiseerde zelfstandigenaftrek created in 2025: [EUR amount / none] -- Src: C:cap. The Belastingdienst fixes it by beschikking, does not apply it automatically, and you keep the running balance yourself.
- MKB-winstvrijstelling on a negative line C **shrinks the loss**: [applicable / not applicable] -- Src: C:sign

[The aangifte computes the ondernemersaftrek components, the total
ondernemersaftrek, the kleinschaligheidsinvesteringsaftrek, the
MKB-winstvrijstelling and the belastbare winst itself, from the figures and the
yes/no answers you type. The lines above are expectations to check on screen --
they are not manual-entry fields, and they never appear as `onderneming.*`
manual-entry rows in the field map.]

### Tariefsaanpassing on the ondernemersfaciliteiten

[If the inkomen uit werk en woning before deductions exceeds the threshold in
`winstberekening-2025.md`:]

- Grondslagverminderende posten in scope: [list from the knowledge note] -- Src: C:chain
- Threshold, adjustment percentage and resulting maximum rate: [from `winstberekening-2025.md`] -- Src: [source_id]
- Ordinary business costs and the investeringsaftrek are **not** affected.
- The aangifte computes this correction and shows it on the aanslag. It is a belastingvermeerdering, never added to taxable box 1 income.

[If the threshold is not in play: "Not applicable -- income before deductions does not exceed the threshold."]

### Vermogensvergelijking self-check

| Component | Amount | Src |
|-----------|--------|-----|
| Ondernemingsvermogen begin boekjaar | EUR [amount] | [F/U/?] |
| Ondernemingsvermogen einde boekjaar | EUR [amount] | [F/U/?] |
| Priveonttrekkingen | EUR [amount] | [F/U/?] |
| Privestortingen | EUR [amount] | [F/U/?] |
| Wijzigingen toelaatbare reserves | EUR [amount] | [F/U/?] |
| Niet- of gedeeltelijk aftrekbare kosten en lasten | EUR [amount] | [F/U/?] |
| Vrijgestelde winstbestanddelen | EUR [amount] | [F/U/?] |

- Reconciles to the saldo winst-en-verliesrekening: [yes / no -- difference EUR [amount], routed to manual review / open question] -- Src: C:reconciliation

[Ask for the begin and eind columns as two separate figures. Do not carry a
prior year's closing column forward, do not enter zero for a column that was not
supplied, do not invent the signed formula, and do not apply a balance tolerance
or an activa-equals-passiva check. Report a difference; never adjust a figure to
force agreement.]

Double-entry facts to enter on two screens from one value: [onttrekking privegebruik auto / woning / fiets; herinvesteringsreserve afboeking]. The auto bijtelling does **not** go under auto- en transportkosten.

### Bijdrage Zvw -- a second, separate aanslag

As an ondernemer you receive a **separate aanslag for the inkomensafhankelijke
bijdrage Zorgverzekeringswet** alongside the aanslag inkomstenbelasting. The
return you file covers both.

- Bijdrage-inkomen component from winst: line E, the belastbare winst uit onderneming -- Src: C:line E
- Percentage and maximumbijdrage-inkomen: [from `zvw-2025.md`] -- Src: [source_id]
- The bijdrage Zvw is never a business cost and never re-enters the profit chain.

### Downstream bases from other lines

| Base | Read off line | Amount | Src |
|------|---------------|--------|-----|
| Lijfrente premiegrondslag (winst component, preceding year) | B of 2024 | EUR [amount] | [F/U] |
| Arbeidsinkomen for the arbeidskorting (winst component) | B | EUR [amount] | C:line B |

[Never reuse the Zvw base for these, or these for the Zvw base. The lijfrente
ruimte itself is computed in the Deductions notes from
`inkomensvoorzieningen-2025.md`; the arbeidskorting is screened in Credits
screening.]

### Loss outcome

[If line E is negative:]

- Ondernemingsverlies 2025: EUR [amount] -- Src: C:line E
- The MKB-winstvrijstelling made this loss smaller: [yes] -- Src: C:sign
- Set off first within 2025 against your own positive box 1 income (such as loon): EUR [amount] -- Src: C:netting
- Remaining verlies uit werk en woning: [EUR amount / none] -- Src: C:netting. Carry-back and carry-forward windows, the beschikking, and the niet-gerealiseerde zelfstandigenaftrek settlement follow `verlies-en-verrekening-2025.md`.
- A loss year still requires a filed return.

[If line E is not negative: "Not applicable -- no ondernemingsverlies for 2025."]

### Form recognition and routing outcome

- Business form recognised: [eenmanszaak / vof / maatschap / man-vrouwfirma / cv / medegerechtigde or winstdelende geldverstrekker / agrarische onderneming / zeescheepvaart / other] -- Src: [F/U/A/?]
- Effect on the ondernemer tests: [statement from `samenwerkingsverband-2025.md`]
- Routing outcome: [chain completed / manual review, with the figure that could not be computed named]

Terminal manual-review computations: samenwerkingsverband profit share and KIA
apportionment, medegerechtigde loss caps, DGA/BV winst, agrarische ondernemingen
(landbouwvrijstelling), zeevarenden, stakingswinst and doorschuiving,
herinvesteringsreserve movements, the oudedagsreserve wind-down computation, and
terbeschikkingstelling. Recognising the form and preparing the rest of the
return is not terminal; record the facts, name the blocked figure, and route
only that figure.

Fiscale partner working in the enterprise: [not applicable / meewerkaftrek /
arbeidsbeloning / real dienstbetrekking -- manual review / medeondernemer --
manual review]. Winst uit onderneming is not a gemeenschappelijk
inkomensbestanddeel, so this is not a partner-allocation choice.

### Open business questions

| Area | Open review question | What would settle it | Src |
|------|----------------------|----------------------|-----|
| [rubriek / balans column / question] | [question] | [evidence] | [F/U/?] |
