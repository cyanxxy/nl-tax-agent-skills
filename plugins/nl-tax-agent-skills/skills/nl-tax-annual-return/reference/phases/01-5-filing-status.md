## Phase 1.5 — Filing status and late-filing exposure

Before compiling income, establish the taxpayer's invitation-letter status and applicable deadline. This drives whether the workpack carries a top-level exposure section (see output contract § Filing status).

Load `_shared/knowledge/years/2025/annual/filing-flow.md` for deadlines and
extension routing. Do not load `late-filing.md` yet.

### 1.5.1 Determine filing status

Ask the user in one batch (at most 3 questions):

1. Have you already filed the 2025 return and, if so, on what date?
2. Did you receive an invitation letter (aangiftebrief), what deadline does it show, and did you request extension through the applicable route? If granted, what is the uitsteldatum?
3. If there was no invitation, what does the fully completed but unsubmitted
   return show (amount to pay or receive), do you have a right to an
   income-dependent scheme while the relevant assets exceed EUR 37,395 (EUR
   74,790 with a fiscal partner), and did you request an aangifte? If any part is
   unknown, record it as unresolved rather than guessing. Extension is
   unavailable on this branch.

After the conversation, record one of four evidence labels; do not select it
from a single yes/no answer:

- `invited`: an aangiftebrief exists; use its stated deadline.
- `no_letter_but_mandatory`: no letter, and the official completed return shows
  **EUR 58 or more to pay**, or the separate income-dependent-scheme and assets
  test applies. Use the reviewed guardrail: file before **14 July 2026**.
- `refund_claim_only`: no letter, **EUR 19 or more back**, and neither mandatory
  no-letter test applies. Submission claims the refund; do not call this an
  invitation-based obligation.
- `filing_obligation_unresolved`: the official calculation or the separate
  scheme/assets test is unresolved. Ask the taxpayer to finish the calculation
  without submitting; do not invent a deadline or late status.

The separate scheme/assets test applies when the taxpayer has a right to an
income-dependent scheme and the relevant assets of the taxpayer, partner, or
minor child(ren) exceed **EUR 37,395**, or **EUR 74,790 with a fiscal partner**.
Check both elements in the official environment; do not infer eligibility from
the asset figure alone.

Extension eligibility requires an invitation letter. With no invitation,
extension is unavailable. As of **16 July 2026**, the ordinary online window
that ended on **1 May 2026** is closed; the historical rule required a request
**before 1 May 2026**. Do not offer it as a current option. If
it was already granted, verify the confirmation (standard granted date:
**1 September 2026**, 4 months extra). If the invitation shows another date—a
still-future deadline—extension may be requested up to that printed date using
the official form; if it has passed, recommend prompt filing rather than an
unavailable extension.

Record under `workspace/annual/2025/notes/filing-status.yaml` with `source: user_chat`.
Do not accept the taxpayer's bare label "on time" as the classification basis.
Record the applicable invitation/no-invitation route, deadline or granted
extension date, and filing date/planned date needed to support that result.

### 1.5.2 Surface exposure

- **On time** (filed by the applicable invitation-letter deadline, mandatory
  no-letter guardrail, or granted uitsteldatum): no late-filing **penalty**
  exposure. Do not promise zero belastingrente: it may still apply when the
  return was received on or after 1 May or the Belastingdienst deviates from it.
- **Uitstel granted, return outstanding**: quote the uitsteldatum and note that belastingrente still accrues from 1 July 2026 if tax is owed. Use the rate from `late-filing.md` (5% from 1 January 2026).
- **Invited and late (deadline passed, no uitstel)**: show EUR 469 first / EUR
  6,709 repeated maximum only as potential exposure. Record herinnering,
  aanmaning, and the **10 werkdagen** (10-workday) response period.
- **No letter but mandatory and late**: do not use the invited-return escalation
  as the explanation. Ask whether and when an aangifte was requested and show
  the separate potential EUR 3,354 failure-to-request exposure, the 6-month
  request period, and the 2-week no-penalty grace only as official review facts.
  The Belastingdienst determines applicability.
- For either late route, show the applicable belastingrente facts, recommend
  filing as soon as possible, and cite `bd_verzuimboete` and
  `bd_belastingrente_ib`.

Load `_shared/knowledge/years/2025/annual/late-filing.md` only for the
granted-extension/outstanding or late branches above. An on-time case must not
load, stale-check, cite, or warn about penalty or interest sources.

If no applicable deadline is established, record `deadline_status: not established` and do not classify the return as on time or late.

Do not compute a final boete or rente amount; the Belastingdienst sets these on the aanslag.

---
