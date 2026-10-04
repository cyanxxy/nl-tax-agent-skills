# ICP and OSS conceptual mapping

Use shared `../nl-tax-shared-resources/reference/workflow-scopes.yaml` for exact
scope identity; the ICP/OSS owning flow selects its canonical knowledge note
and exact source IDs. Each separate return has its own workpack. Never map
registration IDs, genuine customer VAT IDs, invoice numbers or payment details.
These draft rows describe administration facts; no final portal schema is
attested and no manual-entry checklist is available. Root-level metadata uses
`workflow: icp_declaration` or `oss_return`, `tax_year` 2025 or 2026 and the matching period;
OSS also records scheme union|non_union|ioss. Quarter/month restrictions apply.

## ICP rows

Use unique local customer aliases, never identifiers embedded in field IDs:
`icp.row.<alias>.goods_amount`, `icp.row.<alias>.services_amount`,
`icp.row.<alias>.triangulation_amount`. Keep these concepts separate. Each
row has `dimensions.member_state` (official EU two-letter VAT country code).
Before complete customer verification it also needs sourced
`human_vat_id_verified` and dated `human_vat_id_verified_at`. Drafts may leave
verification unresolved with a visible blocker. A confirmation
means the human checked the genuine VAT ID/name/address using the official
process and retained evidence separately; it is not a fabricated validation.
A failed or missing check stays a gap. Use EL for Greece; XI is goods-only.
A correction carries original_period as YYYY_Qn / YYYY_Mnn / YYYY_Y, retaining
customer/country/type and signed difference without including the full VAT ID.

Every ICP row carries `dimensions.customer_alias`: the stable local customer
alias (lowercase letters, digits and underscores, never an identifier). It
equals the row alias when the customer has a single row group. A wrong-ID
correction is two rows with the same original_period: one with the old
customer_alias and a negative value, and one with the corrected
customer_alias and a positive value. The ICP rubric follows from the field
kind and original_period: goods and services rows are ICP rubric 3a when
current and ICP rubric 2a when correcting; triangulation rows are ICP rubric
3b when current and ICP rubric 2b when correcting.

Over identical date coverage, the current ICP rubric 3 total (ICP 3a plus
ICP 3b) must equal btw-aangifte rubric 3b; own-goods transfers appear in both.
Where ICP and VAT filing frequencies differ, bridge with the other periods'
sourced ICP rubric 3 totals instead of accepting a difference. ICP rubric 2
corrections and ICP rubric 4 and 5 call-off stock reports are outside this
comparison. A sourced supply of a new means of transport to a non-taxable
person is reported by the human to the Central Liaison Office by letter, not
on the ICP; its btw-aangifte rubric is a named specialist-review item, and any
difference it causes stays tied to that item. Apart from that item and a
cents or entry-rounding difference that the owner has explained and
recorded, any remaining difference is an open blocker, not an explained
timing difference. No VAT due is charged
on the ICP row.
Permit-based annual and threshold-triggered two-month transition facts need
the owner note; unsupported transitions stay manual review, never relabeled.

## OSS rows

Use unique row aliases `oss.row.<alias>.taxable_base` and
`oss.row.<alias>.vat_amount`. Their dimensions retain `scheme`, `member_state`
and `rate` (a percentage number greater than 0 and at most 100), plus
`supply_kind` (`goods` or `services`), with matching dimensions for a
base/VAT pair. Rates require actual destination-specific official source/evidence;
these notes do not create a universal foreign rate table. Consumption state,
dispatch/fixed-establishment context and tax point remain in sourced row notes.
Northern Ireland uses `member_state: XI` only on Union-scheme rows with
`supply_kind: goods`, under specialist review as the owner note
`../nl-tax-shared-resources/knowledge/vat-cross-border/oss.md` requires; never
map XI services or non-Union/IOSS XI rows, and never use GB.

Current-period rows have nonnegative base/VAT (credits/returns are treated under
the scheme's sourced correction rules). Prior-period correction rows identify
`original_period` and carry signed VAT difference only; no repurposed negative
current row, no cross-scheme transfer. Union/non_union quarterly, IOSS monthly.
Do not deduct input VAT in OSS or merge its liability into domestic VAT output.

Country totals use `oss.total.<lowercase_country>.current_vat`, `.corrections`,
`.balance`, `.payable` and `.refund`; overall amounts use `oss.total.payable`
and `oss.total.refund`. They are conceptual `oss.total.*` with
`entry_mode: internal_routing`. Sum country balances separately: a negative
country balance cannot offset tax owed to another country; payable is the sum
of positive balances, refunds remain separate. No invented final screen labels.
Keep all dimensions visible alongside the alias in the draft summary/notes.
The public sources have `needs_review`; all maps remain draft even if arithmetic
is complete. Real tax content and schema review cannot be inferred from a hash.

Each `oss.total.<country>.current_vat` equals the sum of that country's
current `oss.row.*.vat_amount` rows, and each `.corrections` equals the sum of
that country's correction rows (rows with `original_period`). Never book one
country's correction in another country's total.

Historical original-period metadata is separate from the active 2025/2026 scope.
ICP permits earlier 20xx declarations, with no OSS-style correction window.
OSS starts with 2021 Q3 for Union and non-Union and with 2021 M07 for IOSS.
Use original filed/accepted difference facts and applicable historic evidence;
never compute a full historical return with current rates. For an OSS
correction, record in the workpack notes the original period's due date (the
last day of the month after that period), the window end (that due date plus
three years) and this return's due date. The correction is in time only if
this return is submitted on or before the window end; the original return's
actual filing date is irrelevant. Otherwise route the correction to the
consumption state's process and keep a named blocker; never force it into the
current OSS return.
