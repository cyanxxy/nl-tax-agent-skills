## Phase 5.5 — Credits screening

Entry gate: load this file only after deductions is `complete`, `chat_only`, or
explicitly `deferred` with its open item recorded. Never preload this phase
while a deductions question is awaiting the user's reply.

Use household composition from `profile.yaml` as the start of a conversation,
not as a credit decision. For each credit below, record `candidate`, `not
applicable`, or `unresolved`, with the answered conditions and provenance. The
live return calculates the result.

Load `_shared/knowledge/years/2025/annual/credits.md`. Load
`_shared/knowledge/aow/aow-leeftijd.md` only if stored AOW-age facts must be
checked.

### Arbeidsinkomen when there is winst uit onderneming

`credits.md` is canonical for the arbeidskorting bands and for the components of
arbeidsinkomen. One component is easy to get wrong: the winst component of
arbeidsinkomen is the **winst uit onderneming before ondernemersaftrek and
before the MKB-winstvrijstelling** -- line B of the Phase 2A chain, and **not**
the belastbare winst that the bijdrage Zvw uses. Arbeidsinkomen is a
current-year figure: it sits at the same position in the chain as the lijfrente
premiegrondslag but is taken from a different year, so do not treat the two as
one amount.
`_shared/knowledge/years/2025/entrepreneur/winstberekening-2025.md` is canonical
for which line each downstream base is read off. Take the figure from Phase 2A
rather than recomputing it, and record which line it came from. Profit enjoyed
as a medegerechtigde or a winstdelende schuldeiser does not count towards
arbeidsinkomen. The same definition applies wherever arbeidsinkomen is used
below, including the IACK screen.

### 5.5.1 IACK (inkomensafhankelijke combinatiekorting)

Do not mark IACK from age alone. Ask and record:

- child born after 31 December 2012 (younger than 12 on 1 January 2025);
- child in the taxpayer's household for at least 6 months, or the exact
  co-parenting facts (at least 78 days during a 6-month period in a repeating
  rhythm with each parent);
- whether a failure of the 6-month test was solely because the child died;
- taxpayer's arbeidsinkomen and whether it exceeds EUR 6,145;
- fiscal-partner duration and both partners' arbeidsinkomen; with equal
  arbeidsinkomen, which partner is older.

Record co-parenting, the death exception, multiple partners, and unresolved
duration/income facts for manual portal review. Do not calculate the amount.

### 5.5.2 Ouderenkorting

Candidate only when the taxpayer has reached AOW age **by 31 December 2025**.

- Check `profile.yaml` → `person.aow_by_tax_year.2025.status`. Both
  `reaches_during_year` and `aow_all_year` satisfy the by-31-December screen;
  `below_all_year` does not. Keep that year's transition month for portal
  review and do not infer this from a legacy scalar alone.
- If the condition is met, flag the amount for official-portal review. Do not
  require AOW age for the whole year; reaching it by 31 December is the
  ouderenkorting condition.

### 5.5.3 Alleenstaande-ouderenkorting

Triggered only when the taxpayer is **entitled to an AOW benefit for a single
person**. Do not derive this from a household profile flag, living arrangement, or
fiscal-partner status; ask for the AOW entitlement and keep uncertain cases as
manual review.

### 5.5.4 Jonggehandicaptenkorting

Triggered only when the taxpayer receives or is entitled to a Wajong-uitkering
or Wajong work support **and does not receive the ouderenkorting**. A reported
young-disabled status is not enough unless it establishes that Wajong
entitlement or work support. Ask this dedicated question explicitly: "Do you
receive or have entitlement to Wajong or Wajong work support (sometimes
described as young-disabled status)?" Store it as
`annual.credits.young_disabled_status` with a yes/no value and chat provenance.
A broad answer such as "no other benefits or credits" does not answer this
question. Combine the answer with the ouderenkorting screen before setting the
trigger. Do not mark credits screening `complete` or `chat_only` until the
dedicated answer is recorded or this question is explicitly deferred.

### 5.5.5 Possible payout of unused algemene heffingskorting

Screen this only when the taxpayer has low/no income or an apparent unused
general credit. Ask whether:

- an unused portion remains after their own income tax and premiums;
- they were born before 1963;
- they had the same fiscal partner for more than 6 months (an election for
  full-year treatment does not replace actual duration), unless that partner
  died in 2025; and
- the partner is sufficiently liable for Dutch tax and premiums after the
  partner's own credits.

Record the result as manual portal review. Never assume the EUR 3,068 maximum
will be paid.

### 5.5.6 Output

Write the screening results to `workspace/annual/2025/notes/credits.yaml`. The template's Credits screening section emits these results verbatim.

---
