# Evidence Types — Dutch Tax Document Classification

This reference defines the evidence categories used by the NL Tax Evidence Indexer. Each type includes a description, typical extractable fields, relevant workflow, and common file naming patterns.

---

Use these canonical `evidence_type` tokens exactly as headings below. Dutch display labels such as "WOZ-beschikking" or "voorlopige aanslag" may appear in notes, but the index value must stay snake_case (`woz_beschikking`, `voorlopige_aanslag_beschikking`, `definitieve_aanslag`).

## Contents

- Income & Employment
- Business / Enterprise (Winst uit onderneming)
- Banking & Savings
- Investments & Crypto
- Box 2 / Substantial Interest
- Property & Housing
- Deductions & Gifts
- Debts & Liabilities
- Tax Authority Documents
- Catch-all

## Income & Employment

### jaaropgaaf
- **Description:** Annual salary statement from an employer. For annual-return
  mapping, use the amount labelled `loon` or `fiscaal loon` exactly and the
  withheld loonheffing; do not reconstruct taxable wage from other lines.
- **Typical fields:** werkgever (employer name), loon/fiscaal loon (copy exact
  labelled amount), loonheffing (wage tax withheld), arbeidskorting already
  applied in payroll (informational only), ingehouden bijdrage Zvw, tax year.
- **Boundary:** Never subtract employee-insurance premiums or social-contribution
  lines from fiscaal loon. Do not map the displayed arbeidskorting as taxable
  wage or as a standalone annual-return field without an exact live-portal match.
- **Workflow:** annual / provisional (both)
- **Common naming patterns:** `jaaropgaaf*.pdf`, `jaaropgave*.pdf`, `loonopgave*.pdf`, `annual_salary*.pdf`

### pensioenoverzicht
- **Description:** Pension-related statement. Distinguish two subtypes before
  extracting tax fields: `payment_year_statement` for pension actually paid in
  the return year, and `upo_accrual` for a Uniform Pensioenoverzicht showing
  accrued/projected pension.
- **Typical fields:** a payment-year statement may support bruto belastbaar
  pensioen and ingehouden loonheffing; a UPO may support pension-accrual/factor-A
  context but **never** proves pension paid or withholding for the return year.
- **Review rule:** record `document_subtype`. If it is unclear, classify the
  item for manual review and do not extract payment/withholding fields.
- **Workflow:** annual / provisional (both)
- **Common naming patterns:** `pensioen*.pdf`, `pension*.pdf`, `UPO*.pdf`

### uitkeringsspecificatie
- **Description:** Benefit statement from UWV, SVB, or municipality — covers AOW, WW, WIA, bijstand, and other social benefits.
- **Typical fields:** uitkeringsinstantie (benefit provider: UWV, SVB, gemeente), soort uitkering (benefit type), bruto uitkering, ingehouden loonheffing, tax year.
- **Workflow:** annual / provisional (both)
- **Common naming patterns:** `uitkering*.pdf`, `uwv*.pdf`, `svb*.pdf`, `aow*.pdf`, `ww_*.pdf`, `wia_*.pdf`, `bijstand*.pdf`

---

## Business / Enterprise (Winst uit onderneming)

Evidence for an IB-ondernemer with an eenmanszaak / ZZP. Used by the annual
`nl-tax-winst` helper (Phase 2A). Collect only what the winst section needs; never
gather the BSN.

Three Belastingdienst documents that belong to a business case are listed under
**Tax Authority Documents** rather than here, because they are aanslag/beschikking
documents: `verliesbeschikking`,
`beschikking_niet_gerealiseerde_zelfstandigenaftrek`, and `zvw_aanslag`.

### jaarrekening
- **Description:** Complete annual accounts (jaarrekening / jaarstukken) for the
  enterprise, carrying both the winst-en-verliesrekening and the balans in a
  single document; usually produced by a boekhouder or a boekhoudprogramma.
- **Typical fields:** saldo winst-en-verliesrekening, omzet, kosten by category, afschrijvingen, activa en passiva at the begin and the einde of the boekjaar, ondernemingsvermogen, priveonttrekkingen en -stortingen, tax year.
- **Boundary:** When one file carries both statements, classify it as
  `jaarrekening`; that token takes precedence over `winst_verlies_rekening` and
  `balans`, which are for a document holding only one of the two statements.
  Record whether the jaarstukken are finalized -- a draft set is a review
  question, not a source of final figures.
- **Workflow:** annual
- **Common naming patterns:** `jaarrekening*.pdf`, `jaarstukken*.pdf`, `annual*accounts*.pdf`

### winst_verlies_rekening
- **Description:** Profit-and-loss statement (winst-en-verliesrekening) for the enterprise, usually from a boekhoudprogramma; the basis for winst uit onderneming.
- **Typical fields:** omzet (turnover), inkoopwaarde, zakelijke kosten by category, afschrijvingen, resultaat (winst/verlies), tax year.
- **Workflow:** annual
- **Common naming patterns:** `winst*verlies*.pdf`, `resultatenrekening*.pdf`, `w&v*.pdf`, `p&l*.pdf`, `jaarrekening*.pdf`

### balans
- **Description:** Balance sheet (balans) for the enterprise: activa and passiva at year-end.
- **Typical fields:** vaste activa, voorraden, vorderingen, liquide middelen, ondernemingsvermogen, voorzieningen, langlopende en kortlopende schulden, tax year.
- **Workflow:** annual
- **Common naming patterns:** `balans*.pdf`, `balance*sheet*.pdf`, `jaarrekening*.pdf`

### factuur
- **Description:** Sales or purchase invoice (factuur) supporting turnover or a deductible business cost.
- **Typical fields:** factuurdatum, bedrag excl. btw, btw, bedrag incl. btw, tegenpartij, omschrijving.
- **Workflow:** annual
- **Common naming patterns:** `factuur*.pdf`, `invoice*.pdf`, `verkoop*.pdf`, `inkoop*.pdf`

### urenadministratie
- **Description:** Hours administration supporting the urencriterium for the zelfstandigenaftrek and related deductions; use the threshold in `_shared/knowledge/years/2025/entrepreneur/ondernemer-criteria.md`.
- **Typical fields:** date, hours, activity (direct and indirect business hours), running total.
- **Workflow:** annual
- **Common naming patterns:** `uren*.xlsx`, `uren*.csv`, `urenregistratie*.pdf`, `hours*.xlsx`

### investering_factuur
- **Description:** Purchase invoice for a bedrijfsmiddel, used for depreciation and the kleinschaligheidsinvesteringsaftrek (KIA).
- **Typical fields:** aanschafdatum, aanschafwaarde, restwaarde, gebruiksduur, omschrijving bedrijfsmiddel.
- **Workflow:** annual
- **Common naming patterns:** `investering*.pdf`, `aanschaf*.pdf`, `activa*.pdf`

### kvk_uittreksel
- **Description:** KvK (Chamber of Commerce) extract confirming the registered eenmanszaak. Supports ondernemer status; it does not by itself make the taxpayer an ondernemer for the inkomstenbelasting.
- **Typical fields:** KvK-nummer, handelsnaam, rechtsvorm (eenmanszaak), startdatum, activiteiten (SBI).
- **Workflow:** annual
- **Common naming patterns:** `kvk*.pdf`, `uittreksel*.pdf`, `handelsregister*.pdf`

### kilometerregistratie
- **Description:** Kilometre record for business use of a **private** vehicle,
  supporting the per-kilometre business cost. The per-kilometre amount stays in
  `_shared/knowledge/years/2025/entrepreneur/vervoer-2025.md`.
- **Typical fields:** datum, vertrek- en aankomstadres, doel van de rit, zakelijke kilometers, running total, vervoermiddel.
- **Workflow:** annual
- **Common naming patterns:** `kilometer*.xlsx`, `km*registratie*.csv`, `kilometeradministratie*.pdf`

### rittenregistratie
- **Description:** Trip record for a car in the ondernemingsvermogen, supporting
  the taxpayer's position on private kilometres for the bijtelling. Required
  record content and the bijtelling rules stay in
  `_shared/knowledge/years/2025/entrepreneur/vervoer-2025.md`.
- **Typical fields:** datum, begin- en eindstand kilometerteller, vertrek- en aankomstadres, zakelijke of prive rit, afwijking van de gebruikelijke route, kenteken.
- **Boundary:** A rittenregistratie evidences the private-kilometre position; it
  does not by itself settle the bijtelling. Keep the treatment as an agent
  review question, and never read a missing record as zero private kilometres.
- **Workflow:** annual
- **Common naming patterns:** `ritten*.xlsx`, `rittenregistratie*.pdf`, `trip*log*.csv`

### woz_beschikking_bedrijfspand
- **Description:** WOZ valuation notice for a building held in the
  ondernemingsvermogen, used for the bodemwaarde that limits depreciation on the
  pand.
- **Typical fields:** gemeente, adres, WOZ-waarde, waardepeildatum, belastingjaar, object-aanduiding.
- **Boundary:** Distinct from `woz_beschikking`, which is the taxpayer's own
  home. Copy the labelled waardepeildatum and value exactly; the waardepeildatum
  the aangifte asks for stays in
  `_shared/knowledge/years/2025/entrepreneur/zakelijke-schema-2025.md`.
- **Workflow:** annual
- **Common naming patterns:** `woz*bedrijf*.pdf`, `woz*pand*.pdf`, `waardebeschikking*bedrijfspand*.pdf`

### rvo_beschikking
- **Description:** RVO decision supporting a research or investment facility --
  an S&O-verklaring for the aftrek speur- en ontwikkelingswerk, or an EIA / MIA /
  Vamil verklaring for a qualifying investment.
- **Typical fields:** type verklaring (S&O / EIA / MIA / Vamil), beschikkingsnummer, dagtekening, periode, goedgekeurd investeringsbedrag or toegekende S&O-uren, omschrijving bedrijfsmiddel.
- **Boundary:** The facility is only claimable with the matching RVO verklaring.
  Without one, record the gap as an open question; never assume a verklaring
  exists because the investment looks eligible.
- **Workflow:** annual
- **Common naming patterns:** `rvo*.pdf`, `so*verklaring*.pdf`, `eia*.pdf`, `mia*.pdf`, `vamil*.pdf`

### aov_jaaropgaaf
- **Description:** Annual statement for an arbeidsongeschiktheidsverzekering
  (AOV) held by the ondernemer, showing the premiums paid in the year.
- **Typical fields:** verzekeraar, polisnummer, betaalde premie, verzekerd bedrag, tax year.
- **Boundary:** AOV premiums are **never** a business cost. They belong to the
  uitgaven voor inkomensvoorzieningen in the privedeel, so do not index this
  document against a cost rubriek of the winst-en-verliesrekening.
- **Workflow:** annual
- **Common naming patterns:** `aov*.pdf`, `arbeidsongeschiktheid*.pdf`, `jaaropgaaf*aov*.pdf`

### lijfrente_jaaroverzicht
- **Description:** Annual statement from the insurer or bank for lijfrente
  premiums or inleg paid by the ondernemer, used for the jaarruimte and
  reserveringsruimte.
- **Typical fields:** aanbieder, polis- of rekeningnummer, betaalde premie of inleg, producttype, tax year.
- **Boundary:** Same document family as `lijfrente_overzicht` under Deductions &
  Gifts -- index the file once. Use `lijfrente_jaaroverzicht` for the
  ondernemer's annual statement feeding the jaarruimte and `lijfrente_overzicht`
  for a privedeel premium overview. The premiegrondslag comes off a specific
  line of the profit chain, not off this statement; take that line from
  `_shared/knowledge/years/2025/entrepreneur/inkomensvoorzieningen-2025.md`.
  Lijfrente premiums are never a business cost.
- **Workflow:** annual
- **Common naming patterns:** `lijfrente*jaaroverzicht*.pdf`, `jaaropgave*lijfrente*.pdf`, `banksparen*.pdf`

---

## Banking & Savings

### bankafschrift
- **Description:** Bank statement showing account balance on the peildatum (reference date, typically 1 January) for box 3 reporting.
- **Typical fields:** bank (institution name), rekeningnummer (last 4 digits only), saldo op peildatum, datum, valuta.
- **Workflow:** annual
- **Common naming patterns:** `bankafschrift*.pdf`, `rekeningoverzicht*.pdf`, `statement*.pdf`, `saldo*.pdf`

### jaaroverzicht_bank
- **Description:** Annual bank overview showing interest earned, average balances, and year-end balances across accounts.
- **Typical fields:** bank, rekeningnummer (last 4 digits only), ontvangen rente, betaalde rente, eindsaldo, beginsaldo, tax year.
- **Workflow:** annual
- **Common naming patterns:** `jaaroverzicht*.pdf`, `annual_overview*.pdf`, `fiscaal_overzicht*.pdf`

---

## Investments & Crypto

### jaaroverzicht_beleggingen
- **Description:** Investment portfolio year-end statement showing holdings, dividends, and total portfolio value.
- **Typical fields:** beleggingsinstelling (broker/bank), totale waarde, dividend ontvangen, kosten, beleggingsproducten, peildatum waarde, tax year.
- **Workflow:** annual
- **Common naming patterns:** `beleggingen*.pdf`, `portfolio*.pdf`, `investment*.pdf`, `effecten*.pdf`

### crypto_overzicht
- **Description:** Cryptocurrency holdings overview showing wallet balances and valuations on the peildatum.
- **Typical fields:** platform/exchange, crypto activa, waarde in EUR op peildatum, aantal eenheden, tax year.
- **Workflow:** annual
- **Common naming patterns:** `crypto*.pdf`, `crypto*.csv`, `bitcoin*.pdf`, `binance*.pdf`, `bitvavo*.pdf`

---

## Box 2 / Substantial Interest

### dividend_statement
- **Description:** Dividend statement from a company in which the taxpayer holds a substantial interest (aanmerkelijk belang) — gross regular benefit and withheld dividend tax for Box 2.
- **Typical fields:** vennootschap (company name), reguliere_voordelen_bruto (gross dividend), ingehouden dividendbelasting, uitkeringsdatum, tax year.
- **Workflow:** annual / provisional (both)
- **Common naming patterns:** `dividend*.pdf`, `dividendstatement*.pdf`, `dividendnota*.pdf`, `uitkering_bv*.pdf`

### share_sale_agreement
- **Description:** Share-sale or transfer agreement for a substantial-interest disposal — the source for Box 2 disposal-benefit fields.
- **Typical fields:** vennootschap, vervreemdingsprijs (net transfer price), verkrijgingsprijs (acquisition price), vervreemdingskosten, overdrachtsdatum, tax year.
- **Workflow:** annual
- **Common naming patterns:** `share*sale*.pdf`, `koopovereenkomst_aandelen*.pdf`, `verkoop_aandelen*.pdf`, `aandelenoverdracht*.pdf`

---

## Property & Housing

### woz_beschikking
- **Description:** WOZ property valuation notice issued by the municipality, used for eigenwoningforfait and box 3 reporting.
- **Typical fields:** gemeente, adres, WOZ-waarde, waardepeildatum, belastingjaar, object-aanduiding.
- **Workflow:** annual / provisional (both)
- **Common naming patterns:** `woz*.pdf`, `WOZ*.pdf`, `waardebeschikking*.pdf`, `ozb*.pdf`

### hypotheek_jaaroverzicht
- **Description:** Mortgage annual statement showing interest paid, principal repaid, and remaining debt for the year.
- **Typical fields:** geldverstrekker (lender), betaalde hypotheekrente, aflossing, restschuld per 31/12, restschuld per 1/1, oorspronkelijke hoofdsom, tax year.
- **Workflow:** annual / provisional (both)
- **Common naming patterns:** `hypotheek*.pdf`, `mortgage*.pdf`, `jaaroverzicht_hypotheek*.pdf`, `jaaropgave_hypotheek*.pdf`

### huurcontract
- **Description:** Rental contract for property owned by the taxpayer, relevant for box 3 rental income.
- **Typical fields:** verhuurder, huurder, adres, maandelijkse huur, ingangsdatum, einddatum.
- **Workflow:** annual
- **Common naming patterns:** `huurcontract*.pdf`, `huur*.pdf`, `rental*.pdf`

### eigendom_bewijs
- **Description:** Property ownership proof — deed, cadastral registration, or notarial deed for real estate holdings.
- **Typical fields:** adres, kadastrale aanduiding, eigendomspercentage, datum verkrijging, koopsom.
- **Workflow:** annual
- **Common naming patterns:** `eigendom*.pdf`, `akte*.pdf`, `koopakte*.pdf`, `kadaster*.pdf`

---

## Deductions & Gifts

### gift_receipt
- **Description:** Donation receipt from an ANBI (Algemeen Nut Beogende Instelling) or qualifying institution.
- **Typical fields:** naam instelling, RSIN/ANBI-nummer, bedrag gift, datum gift, type gift (periodiek/gewoon), tax year.
- **Workflow:** annual
- **Common naming patterns:** `gift*.pdf`, `donatie*.pdf`, `schenking*.pdf`, `ANBI*.pdf`

### zorgkosten_overzicht
- **Description:** Medical expense overview — may include own-risk payments, specific care costs, and travel for medical treatment.
- **Typical fields:** totaal zorgkosten, eigen risico betaald, specifieke zorgkosten, vergoeding zorgverzekeraar, tax year. Note: do NOT extract personal medical details beyond totals.
- **Workflow:** annual
- **Common naming patterns:** `zorgkosten*.pdf`, `medisch*.pdf`, `zorg*.pdf`, `eigen_risico*.pdf`

### alimentatie_overeenkomst
- **Description:** Evidence about maintenance payments to a former partner or
  children. This may be a court order, divorce/cohabitation agreement, notarial
  deed, or facts supporting an urgent moral obligation that can be enforced in
  court. Unclear enforceability remains a manual-review question.
- **Typical fields:** type alimentatie (partneralimentatie / kinderalimentatie), maandbedrag, ingangsdatum, einddatum, ontvangende partij.
- **Workflow:** annual
- **Common naming patterns:** `alimentatie*.pdf`, `alimony*.pdf`, `echtscheiding*.pdf`
- **Boundary:** Kinderalimentatie is not deductible. Classification as
  `alimentatie_overeenkomst` does not itself establish that partner maintenance
  qualifies; retain the obligation basis and payment proof for agent review.

### lijfrente_overzicht
- **Description:** Annuity premium overview — premiums paid for lijfrente products that may be deductible in box 1.
- **Typical fields:** verzekeraar/aanbieder, betaalde premie, type lijfrente, polisnummer, ingangsdatum, tax year.
- **Workflow:** annual
- **Common naming patterns:** `lijfrente*.pdf`, `annuity*.pdf`, `pensioenopbouw*.pdf`

---

## Debts & Liabilities

### schuld_overzicht
- **Description:** Debt overview for non-mortgage debts — personal loans, study debt (DUO), or other liabilities relevant for box 3.
- **Typical fields:** schuldeiser (creditor), hoofdsom, restschuld per peildatum, betaalde rente, type schuld, tax year.
- **Workflow:** annual
- **Common naming patterns:** `schuld*.pdf`, `lening*.pdf`, `duo*.pdf`, `studieschuld*.pdf`, `persoonlijke_lening*.pdf`

---

## Tax Authority Documents

### voorlopige_aanslag_beschikking
- **Description:** Existing voorlopige aanslag (provisional assessment) decision letter from the Belastingdienst for the current or prior tax year.
- **Typical fields:** belastingjaar, vastgesteld belastbaar inkomen, verschuldigde belasting, reeds betaald/ontvangen, te betalen/ontvangen, dagtekening.
- **Workflow:** provisional
- **Common naming patterns:** `voorlopige_aanslag*.pdf`, `va_*.pdf`, `provisional*.pdf`

### definitieve_aanslag
- **Description:** Final tax assessment from the Belastingdienst for a prior year — useful for verifying prior-year positions.
- **Typical fields:** belastingjaar, vastgesteld inkomen box 1/2/3, verschuldigde belasting, heffingskortingen, te betalen/ontvangen, dagtekening.
- **Workflow:** annual
- **Common naming patterns:** `definitieve_aanslag*.pdf`, `aanslag*.pdf`, `final_assessment*.pdf`

### zvw_aanslag
- **Description:** Aanslag inkomensafhankelijke bijdrage Zorgverzekeringswet --
  the **second, separate aanslag** an IB-ondernemer receives alongside the
  aanslag inkomstenbelasting. One return covers both.
- **Typical fields:** belastingjaar, bijdrage-inkomen, verschuldigde bijdrage, al betaald of ingehouden, te betalen/ontvangen, dagtekening.
- **Boundary:** Keep it distinct from `definitieve_aanslag` and
  `voorlopige_aanslag_beschikking`: it is a different aanslag with its own
  bijdrage-inkomen. The bijdrage is never a business cost, in either direction.
  Percentages and the maximumbijdrage-inkomen stay in
  `_shared/knowledge/years/2025/entrepreneur/zvw-2025.md`.
- **Workflow:** annual
- **Common naming patterns:** `zvw*.pdf`, `zorgverzekeringswet*.pdf`, `bijdrage*zvw*.pdf`

### verliesbeschikking
- **Description:** Belastingdienst decision fixing a verlies uit werk en woning
  or an ondernemingsverlies for a year, together with the balance still
  available for set-off.
- **Typical fields:** belastingjaar, vastgesteld verlies, reeds verrekend, resterend saldo, dagtekening.
- **Boundary:** A carry-forward loss is usable only when the taxpayer can
  evidence it with the beschikking. Without it, record the gap as an open
  question; never carry a loss forward on recollection or on an earlier
  workpack. The carry-back and carry-forward windows stay in
  `_shared/knowledge/years/2025/entrepreneur/verlies-en-verrekening-2025.md`.
- **Workflow:** annual
- **Common naming patterns:** `verliesbeschikking*.pdf`, `verlies*.pdf`, `beschikking*verlies*.pdf`

### beschikking_niet_gerealiseerde_zelfstandigenaftrek
- **Description:** Belastingdienst decision on the aanslagbiljet fixing the part
  of the zelfstandigenaftrek that the winst cap blocked, and carrying it forward.
- **Typical fields:** belastingjaar, vastgesteld bedrag niet-gerealiseerde zelfstandigenaftrek, reeds verrekend, resterend saldo, dagtekening.
- **Boundary:** The Belastingdienst does not apply this balance automatically --
  the taxpayer enters it in a later aangifte. Index the beschikking and record
  the running balance from it; never reconstruct the balance from an earlier
  workpack. The set-off condition stays in
  `_shared/knowledge/years/2025/entrepreneur/verlies-en-verrekening-2025.md`.
- **Workflow:** annual
- **Common naming patterns:** `niet*gerealiseerde*zelfstandigenaftrek*.pdf`, `ngz*.pdf`, `beschikking*zelfstandigenaftrek*.pdf`

---

## Catch-all

### other
- **Description:** Unclassified document that does not match any known evidence type. Requires manual review by the taxpayer.
- **Typical fields:** none predefined — extract what is visible.
- **Workflow:** both (unknown until classified)
- **Common naming patterns:** any file not matching the patterns above.
- **Note:** Always set `review_required: true` and `confidence: 0.0` for this type.
