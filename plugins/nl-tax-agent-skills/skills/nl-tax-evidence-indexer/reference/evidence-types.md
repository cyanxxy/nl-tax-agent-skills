# Evidence Types — Dutch Tax Document Classification

This reference defines the evidence categories used by the NL Tax Evidence Indexer. Each type includes a description, typical extractable fields, relevant workflow, and common file naming patterns.

---

## Income & Employment

### jaaropgaaf
- **Description:** Annual salary statement from an employer, summarising gross salary, withheld wage tax (loonheffing), and social contributions for a calendar year.
- **Typical fields:** werkgever (employer name), loon (gross salary), loonheffing (wage tax withheld), arbeidskorting, ingehouden bijdrage ZVW, fiscaal loon, tax year.
- **Workflow:** annual / provisional (both)
- **Common naming patterns:** `jaaropgaaf*.pdf`, `jaaropgave*.pdf`, `loonopgave*.pdf`, `annual_salary*.pdf`

### pensioenoverzicht
- **Description:** Pension statement showing pension accrual, contributions, and/or pension income received during the year.
- **Typical fields:** pensioenuitvoerder (pension provider), bruto pensioen, ingehouden loonheffing, opgebouwd pensioen, AOW-franchise, tax year.
- **Workflow:** annual / provisional (both)
- **Common naming patterns:** `pensioen*.pdf`, `pension*.pdf`, `UPO*.pdf`

### uitkeringsspecificatie
- **Description:** Benefit statement from UWV, SVB, or municipality — covers AOW, WW, WIA, bijstand, and other social benefits.
- **Typical fields:** uitkeringsinstantie (benefit provider: UWV, SVB, gemeente), soort uitkering (benefit type), bruto uitkering, ingehouden loonheffing, tax year.
- **Workflow:** annual / provisional (both)
- **Common naming patterns:** `uitkering*.pdf`, `uwv*.pdf`, `svb*.pdf`, `aow*.pdf`, `ww_*.pdf`, `wia_*.pdf`, `bijstand*.pdf`

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
- **Description:** Alimony agreement or court order specifying payments to former partner and/or children.
- **Typical fields:** type alimentatie (partneralimentatie / kinderalimentatie), maandbedrag, ingangsdatum, einddatum, ontvangende partij.
- **Workflow:** annual
- **Common naming patterns:** `alimentatie*.pdf`, `alimony*.pdf`, `echtscheiding*.pdf`

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

---

## Catch-all

### other
- **Description:** Unclassified document that does not match any known evidence type. Requires manual review by the taxpayer.
- **Typical fields:** none predefined — extract what is visible.
- **Workflow:** both (unknown until classified)
- **Common naming patterns:** any file not matching the patterns above.
- **Note:** Always set `review_required: true` and `confidence: 0.0` for this type.
