# Human VAT return and correction steps

Load the matching VAT workpack and field map plus the notes it actually uses:
`../nl-tax-shared-resources/knowledge/vat/return-and-rubrics.md`,
`../nl-tax-shared-resources/knowledge/vat/invoices-and-deduction.md`, and,
for corrections, `../nl-tax-shared-resources/knowledge/vat/corrections.md`.
Use `../nl-tax-shared-resources/knowledge/vat/kor-and-special-cases.md` when
KOR or a scope question applies. For an accepted adjustment, also read the
actual `../nl-tax-shared-resources/knowledge/vat-adjustments/` notes and source entries recorded by its
owner/helper, rather than assuming an adviser-only unsupported calculation.
Separate ICP/OSS workpacks use `reference/extended-submit-steps.md`, not these
domestic VAT steps or suppletie threshold.

## Gate before entry values

If the workpack is unconfirmed/stale, a note has `review_status: needs_review`,
an exact rubric schema lacks review, or VAT period, special-case, KOR,
deduction, or reconciliation blockers remain,
show only **Blockers**, with no entry amounts or filing steps, and write no
checklist. `VAT source-content review` is a concrete blocker, not cleared by
the agent's checks. This rule takes precedence over the generic instruction
to show known steps for partial inputs. Return to the VAT owner for resolution.

## Return, once the gate clears

1. **You (the taxpayer):** check the assigned year and period and your filing
   invitation personally in Mijn Belastingdienst Zakelijk. Keep this period's
   workpack and evidence alongside it.
2. **You (the taxpayer):** compare each applicable current rubric with the
   checked field-map summary. Verify unfamiliar screen labels personally;
   do not enter internal calculation records or invent a total field.
3. **You (the taxpayer):** verify deduction eligibility, reverse-charge VAT,
   credit notes, established adjustments and source/entry rounding. Compare
   the official form's computed 5a and unnumbered net result with the
   workpack's reconciliation.
4. **You (the taxpayer):** resolve separate obligations identified in review,
   such as separately prepared ICP or registered OSS/IOSS, and compare their
   matching coverage without copying their foreign VAT into domestic rubrics.
5. **You (the taxpayer):** review, authorize and transmit personally. Keep the
   official confirmation. Use payment details from your actual notice/return
   and ensure payment is received by the confirmed due date.

## Correction, once the gate clears

For a correction to carry into the next return, the human checks the source
period, that the destination is the next (eerstvolgende) return after
discovery, each original-rubric adjustment, and that it has not already been
included. Continue with that destination return's owner;
this correction workpack never replaces the full destination return.

For a suppletie, **you (the taxpayer)** confirm the correction scope and the
discovery deadline, verify every corrected full rubric total (including
unchanged rubrics), and enter the earlier-declared net amount shown in the
checklist's "Totaalbedrag eerdere btw-aangifte over dit tijdvak" row. The
signed difference is a check result, not the corrected total. **You (the
taxpayer)** decide and transmit personally and keep the confirmation. For
additional tax payable: if the original period's deadline has not yet
passed, **you (the taxpayer)** pay before that deadline using that period's
genuine payment reference; otherwise **you (the taxpayer)** await the
naheffingsaanslag and pay using its details. Never invent a payment
reference or reuse an unrelated one. If the suppletie changes rubric 3b,
**you (the taxpayer)** also send the separate 3b letter to the Central
Liaison Office named in `corrections.md`.

An already incorrect suppletie (corrected by objection after its decision,
or by a new suppletie only when the earlier one produced no payment or
refund, per `corrections.md`), a margin-globalisation or double-declared
intra-Community acquisition refund (a letter route), an ICP-only adjustment
or a special scheme goes to the reviewed route/manual review; never
automatically prepare another submission. Every authenticated action belongs
to the human.
