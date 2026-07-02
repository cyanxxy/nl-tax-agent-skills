# Rule note: AOW-leeftijd (Dutch state-pension age) for routing

source_ids: svb_aow_leeftijd, rijksoverheid_aow_leeftijd
workflow: all
tax_year: all
status: active
last_reviewed: "2026-07-02"
review_status: reviewed

## Rule

The AOW-leeftijd (Dutch state-pension age) determines whether a taxpayer reaches AOW age in or before a tax year. This routes which box 1 rate table applies (the reduced pensioner first-bracket rate, lower premie volksverzekeringen, lower heffingskortingen) and which elderly credits apply (ouderenkorting, alleenstaande-ouderenkorting). These are reference notes for workpack preparation — not an AOW entitlement determination.

## AOW-leeftijd by year

- **2025: 67 years.**
- **2026: 67 years.**
- The AOW age does **not** rise in 2027 (it stays 67). It rises to **67 years and 3 months in 2028** and stays 67 years and 3 months through **2031**.
- The AOW age is fixed for everyone born **before 1 October 1964**; for later birth dates it is provisional and follows CBS life-expectancy figures, set at least 5 years in advance.
- A person's exact AOW date depends on their date of birth (the SVB publishes the personal date and pays AOW monthly, around the 23rd).

## How to use in the workpack

1. From the taxpayer's date of birth and the tax year, determine whether they have the AOW age for the **whole** year, reach it **during** the year, or are **below** it.
2. **Whole year at AOW age** → use the AOW-age box 1 rate and heffingskorting tables (see `years/2025/annual/box1-rates.md` and `years/2025/annual/credits.md`), and consider ouderenkorting / alleenstaande-ouderenkorting.
3. **Reaches AOW age during the year** → do not interpolate in the workpack; the Belastingdienst calculates the month-dependent transitional amount. Flag the box 1 rate and any affected heffingskortingen as manual-review items.
4. **Below AOW age** → use the standard (non-AOW) tables.

## Developer instruction

Intake derives `aow_age_in_tax_year` from the date of birth and stores it with `source: assumption` so the user can correct it. Never collect or store the AOW administration number or BSN.

## Common failure

Do not assume a fixed age of 67 for future years — 67 applies only through 2027; for 2028-2031 the AOW age is fixed at 67 years and 3 months, and beyond 2031 it is provisional. For tax years 2025 and 2026 specifically it is 67.
