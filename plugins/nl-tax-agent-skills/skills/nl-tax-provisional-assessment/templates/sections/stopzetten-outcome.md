## Stopzetten outcome

[For stopzetten, and for a change reached through the stopzetten payment-case
redirect. For request/review and any other change, replace this section's body
with "N/A — not applicable for this subflow"; do not omit the heading.]

If the taxpayer is **moving abroad**, record: "Residency review required; moving abroad is **not a categorical stopzetten reason**." The provisional 2026 migration boundary applies and is terminal for this provisional workflow: do not emit a refund-stop checklist solely because of the move, and tell the taxpayer to adjust or stop the voorlopige aanslag personally or with an adviser. An annual M or C precollection draft is a separate workflow and does not change or stop the voorlopige aanslag.

### Current-date cutoff gate

| Item | Value | Src |
|------|-------|-----|
| Current date used for cutoff | [YYYY-MM-DD] | [system/user] |
| Stopzetten cutoff | 2026-10-01 | C:bd_provisional_stopzetten_2026 |
| Cutoff result | [before cutoff / cutoff passed] | C:date_compare |

If the current date is on or after 2026-10-01, do not generate a stopzetten checklist. State that the 2026 stopzetten cutoff has passed and route the user to review/change or to a separate filing-status review and, when a return will be filed, annual settlement.

### Cash-flow direction and route

| Item | Value | Src |
|------|-------|-----|
| Current monthly direction | [refund / payment / unknown] | [F/U/?] |
| Route chosen | [stop refund / change VA (payment case) / no action] | C:decision |
| Reason | [short reason] | [F/U/C] |
| Refund component | [deductions / IACK / algemene heffingskorting / unknown] | [F/U/?] |
| Effective date | [2026-01-01 / selected first day of month / unknown] | [F/U/C/?] |
| Amount already received in 2026 | EUR [amount / unknown] | [F/U/?] |
| Separate repayment notice | [expected for paid deductions/IACK / not applicable / unresolved] | C:review |
| 2026 annual filing status | [required / not required / unresolved / plans to file] | [F/U/?] |

### Refund-stop checklist

[Include only when the taxpayer receives a monthly refund and the current-date cutoff gate is before 2026-10-01.]

> **HUMAN-ONLY PORTAL STEPS.** The taxpayer or an authorized human performs any
> authenticated portal action below personally. The assistant must not open or
> operate the portal, click controls, confirm, send, or submit.

- [ ] I confirmed the current VA pays a monthly refund
- [ ] I confirmed the current date is before 2026-10-01
- [ ] I identified whether the selected refund concerns deductions, IACK, or the algemene heffingskorting
- [ ] For deductions/IACK: I confirmed the effect is retroactive to 1 January 2026 and prior payments may be reclaimed in a separate notice
- [ ] For algemene heffingskorting: I confirmed the selected first day of a month and prospective payment effect from that selected/next payment month
- [ ] I checked the 2026 annual filing obligation separately; stopzetten itself does not make filing universally required
- [ ] I used the official Mijn Belastingdienst stopzetten form personally for my 2026 monthly refund
- [ ] I kept the confirmation for my records

### Payment-case redirect

[Include only when the taxpayer pays monthly and the amount is wrong.]

Stopping payments does not reduce the tax obligation, and simply ceasing
payments can create arrears under the current beschikking. Route to the change
subflow and carry the payment baseline forward there; do not include the
refund-stop checklist.
