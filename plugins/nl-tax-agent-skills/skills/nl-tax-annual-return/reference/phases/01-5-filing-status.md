## Phase 1.5 — Filing status and late-filing exposure

Before compiling income, establish the taxpayer's invitation-letter status and applicable deadline. This drives whether the workpack carries a top-level exposure section (see output contract § Filing status).

Load `_shared/knowledge/years/2025/annual/filing-flow.md` for deadlines and
extension routing. Do not load `late-filing.md` yet.

### 1.5.1 Determine filing status

Ask the user in one batch (at most 3 questions):

1. Have you already filed the 2025 return and, if so, on what date?
2. Did you receive an invitation letter (aangiftebrief), what deadline does it show, and did you request extension through the applicable route? If granted, what is the uitsteldatum?
3. If there was no invitation, have you established that tax is due for 2025 and, if not yet filed, when do you plan to file? Extension is unavailable on this branch.

If an invitation letter exists, use its deadline. If there is no invitation and the taxpayer establishes that tax is due, use the reviewed voluntary-filing guardrail: file before **14 July 2026**. The 14 July 2026 date is conditional on that no-invitation/tax-due route. Otherwise do not invent a filing deadline.

Extension eligibility requires an invitation letter. With **no invitation**, extension is unavailable. For the standard online route, request extension **before 1 May 2026**; the granted extension normally adds **4 months**, making the standard extended date **1 September 2026**. If the invitation letter shows **another date**, request by that letter date using the **official form** route and use the granted uitsteldatum.

Record under `workspace/annual/2025/notes/filing-status.yaml` with `source: user_chat`.
Do not accept the taxpayer's bare label "on time" as the classification basis.
Record the applicable invitation/no-invitation route, deadline or granted
extension date, and filing date/planned date needed to support that result.

### 1.5.2 Surface exposure

- **On time** (filed by the applicable established invitation-letter deadline or conditional no-invitation/tax-due guardrail, or by the granted uitsteldatum): no exposure. The workpack will say "Filing status: on time."
- **Uitstel granted, return outstanding**: quote the uitsteldatum and note that belastingrente still accrues from 1 July 2026 if tax is owed. Use the rate from `late-filing.md` (5% from 1 January 2026).
- **Late (deadline passed, no uitstel)**: show the EUR 469 first / EUR 6,709 maximum amounts only as **potential exposure**. Missing the deadline alone does not impose a verzuimboete. Record whether the taxpayer received a **herinnering**, then an **aanmaning**, and whether the **10 werkdagen** period after the aanmaning expired while the return remained unfiled. The boete is conditional on that escalation. Also show the applicable belastingrente rate, recommend filing as soon as possible, and cite `bd_verzuimboete` and `bd_belastingrente_overview`.

Load `_shared/knowledge/years/2025/annual/late-filing.md` only for the
granted-extension/outstanding or late branches above. An on-time case must not
load, stale-check, cite, or warn about penalty or interest sources.

If no applicable deadline is established, record `deadline_status: not established` and do not classify the return as on time or late.

Do not compute a final boete or rente amount; the Belastingdienst sets these on the aanslag.

---
