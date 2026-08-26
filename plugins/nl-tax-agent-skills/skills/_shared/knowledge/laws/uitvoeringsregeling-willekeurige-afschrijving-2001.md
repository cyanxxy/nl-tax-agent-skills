# Rule note: Uitvoeringsregeling willekeurige afschrijving 2001 -- structural reference

source_id: law_uwa_2001
workflow: all
tax_year: all
status: active
last_reviewed: "2026-08-15"
review_status: reviewed

## Rule

The Uitvoeringsregeling willekeurige afschrijving 2001 (BWBR0012035) is the
ministerial regulation that gives effect to articles 3.31, 3.34, 3.36, 3.38 and
3.52 Wet inkomstenbelasting 2001. Willekeurige afschrijving lets the ondernemer
decide how and when the acquisition or production cost of a designated
bedrijfsmiddel is written off; the Wet IB 2001 states which categories may be
designated and this regulation states which assets are designated, how much of
their cost may be written off freely, and how long the terugname period of
article 3.38 Wet IB 2001 runs. This file is an article inventory and orientation
only. The operational conditions, ceilings, and manual-review boundaries used to
prepare a workpack live in the year-specific entrepreneur notes, in particular
`../years/2025/entrepreneur/afschrijving-en-bedrijfsmiddelen-2025.md` (general
scheme, exclusions, terugname) and
`../years/2025/entrepreneur/aanloopfase-en-starters-2025.md` (the startende
ondernemers variant).

These are reference notes for workpack preparation -- not final tax advice.

## Article inventory

The regulation was consulted in the version geldend van 1 January 2025. Only the
chapters below are still operative; the lapsed chapters are listed at the end so
that an old schedule is recognised rather than silently applied.

### Hoofdstuk 2 -- Milieu-bedrijfsmiddelen (Vamil), articles 2 to 5b

Hoofdstuk 2 governs the designation and notification procedure for the
milieu-bedrijfsmiddelen that may be written off freely under article 3.31
Wet IB 2001 (Vamil), alongside the RVO Milieulijst.

- **Article 2** -- aanmelding. Lid 1 requires the investment to be reported
  within a term of three months.
- **Article 4** -- what one melding must cover. Lid 2 requires the verplichtingen
  and voortbrengingskosten covered by a single melding to reach a stated combined
  minimum amount. The amount itself is a year figure and is not repeated in this
  note.

The free-depreciation share for a milieu-bedrijfsmiddel is set by article 3.31
Wet IB 2001, not by this regulation; read it from
`../years/2025/entrepreneur/investeringsaftrek.md`.

### Hoofdstuk 4, paragraaf 1 -- Investeringen door startende ondernemers, articles 7 to 9

- **Article 7** -- designation. Lid 1 designates as "andere aangewezen
  bedrijfsmiddelen" (article 3.34 lid 2 in conjunction with lid 3 Wet IB 2001)
  the assets for which the taxpayer entered into obligations or made
  voortbrengingskosten in a calendar year in which the verhoogde
  zelfstandigenaftrek of article 3.76 lid 3 Wet IB 2001 applies. Lid 2 adds the
  assets committed to in the immediately preceding aanloopjaar in which the
  zelfstandigenaftrek of article 3.76 lid 1 did not apply. Lid 3 restricts the
  paragraaf to assets whose acquisition or production costs are made in the
  context of an onderneming from which the taxpayer derives profit as ondernemer.
  Lid 4 declares articles 3.43 lid 2, 3.45 lid 1, 2 and 5, and 3.46 Wet IB 2001
  correspondingly applicable.
- **Article 8** -- annual ceiling and overlap. The willekeurige afschrijving is
  allowed only in so far as the combined acquisition and production costs in the
  calendar year do not exceed the maximum amount stated in the table of article
  3.41 lid 2 Wet IB 2001 over which kleinschaligheidsinvesteringsaftrek can be
  obtained, and it does not apply to assets already written off freely on another
  basis. The mapping of that cross-reference to one euro amount is **not
  established** in the reviewed sources: state the ceiling qualitatively and route
  the sizing to manual review.
- **Article 9** -- period. Sets the article 3.38 Wet IB 2001 period at five
  years, beginning with the start of the calendar year in which the obligations
  were entered into or the voortbrengingskosten were made.

### Hoofdstuk 4, paragraaf 2 -- Zeeschepen, articles 10 to 12

- **Article 11** -- ceiling. Caps the willekeurige afschrijving per calendar year
  at a stated share of the depreciable acquisition or production costs, allows it
  only in so far as the winst uit zeescheepvaart remains positive without it, and
  carries unused headroom to the next year.
- **Article 12** -- period. Sets the article 3.38 Wet IB 2001 period at ten
  years.

A zeeschip carries its own shipping conditions and its own terugname mechanics.
Route it to manual review rather than reasoning from the starters paragraaf.

### Hoofdstuk 4, paragraaf 3 -- the closed 2023 scheme, articles 13 to 15

- **Article 13** -- scope. Lid 1 covers only bedrijfsmiddelen for which the
  verplichtingen were entered into, or the voortbrengingskosten made, in calendar
  year 2023 and which were taken into use before 1 January 2026. Lid 2 excludes
  gebouwen, schepen, vliegtuigen, bromfietsen, motorrijwielen, personenauto's
  other than cars without CO2 emission and cars for beroepsvervoer, immateriele
  activa, dieren, public roads, paths, bridges and tunnels, assets mainly made
  available to third parties (short-term successive rental excepted), and assets
  already written off freely on another basis.
- **Article 14** -- ceiling. Allows the willekeurige afschrijving once only and
  at most 50% of the acquisition or production cost.
- **Article 15** -- period. Ends the article 3.38 Wet IB 2001 period on
  31 December 2025.

The scheme is closed to new investment: it never reaches an investment committed
to after calendar year 2023. Articles 13 and 15 carry a change flag without an
entry-into-force date, so recheck the paragraaf before the 2026 season.

### Lapsed chapters -- recognise, do not apply

- Hoofdstuk 3 and article 6 (arbo-bedrijfsmiddelen) lapsed per 1 January 2005.
- Articles 16 and 17 (continentaal plat), 18 to 20 (film) and 21 to 24 (nieuwe
  gebouwen in aangewezen gemeenten) lapsed per 1 January 2003.

## Relevance to this project

Only one variant is explained in a workpack rather than routed on sight: the
startende ondernemers variant of hoofdstuk 4 paragraaf 1, and even there the
annual ceiling is described qualitatively and the amount goes to manual review.
The Vamil variant, the zeeschepen variant, and any schedule that still runs under
the closed 2023 paragraaf are recognise-and-route items. Nothing in this
regulation is computed by the plugin.

## Developer instruction

When a taxpayer mentions willekeurige afschrijving, or an asset schedule shows a
depreciation amount larger than the ordinary maxima allow:

1. Ask which variant is in play before anything else: milieu-bedrijfsmiddel
   (Vamil), startende ondernemer, zeeschip, or a schedule started under the 2023
   paragraaf. The four variants have different designations, ceilings, and
   terugname periods and must never be blended.
2. Read the operational rules from
   `../years/2025/entrepreneur/afschrijving-en-bedrijfsmiddelen-2025.md` and, for
   the starters variant, `../years/2025/entrepreneur/aanloopfase-en-starters-2025.md`.
   Never take an amount, percentage, or threshold from this file -- it carries
   none.
3. For the starters variant, confirm with the taxpayer that the enterprise form
   and the startersaftrek conditions are met and that the asset was committed to
   in a qualifying year or in the immediately preceding aanloopjaar. Explain the
   scheme, state the ceiling qualitatively, and route the amount to manual review.
4. For a Vamil, zeeschepen, or 2023-paragraaf schedule, record the facts and route
   the whole schedule to manual review. Do not reconstruct an RVO melding, and do
   not confirm that a three-month notification term was met -- ask the taxpayer for
   the RVO confirmation instead.
5. Check the terugname period that applies to the variant (article 9 for the
   starters variant, article 12 for zeeschepen, article 15 for the closed 2023
   paragraaf) whenever an asset written off freely is rented out, sold, or put to
   another use, and route the correction to manual review.
6. If the taxpayer describes a scheme that matches one of the lapsed chapters,
   say that the chapter lapsed and route the schedule to manual review rather than
   applying it.
7. You (the taxpayer) enter every resulting figure in Mijn Belastingdienst. This
   plugin never opens or operates the portal.

## Common failure

Do not treat this file as the source for any ceiling, percentage, minimum, or
euro amount -- it deliberately states none, and the article 8 ceiling is expressed
only as a cross-reference to the kleinschaligheidsinvesteringsaftrek table of
article 3.41 lid 2 Wet IB 2001. Do not assume that a willekeurige afschrijving in
one variant is available in another, and do not extend the closed 2023 paragraaf
to an investment committed to after calendar year 2023.
