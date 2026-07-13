## Phase 5.5 — Credits screening

Use household composition from `profile.yaml` to surface which credits apply. For each of the 4 credits below, emit one line in the workpack: either "Triggered: [reason]" or "Not applicable: [reason in one phrase]".

Load `_shared/knowledge/years/2025/annual/credits.md`. Load
`_shared/knowledge/aow/aow-leeftijd.md` only if the stored deterministic AOW
screen must be checked or recomputed.

### 5.5.1 IACK (inkomensafhankelijke combinatiekorting)

Triggered when the taxpayer (or fiscal partner with lower arbeidsinkomen) had at least one child registered at the taxpayer's address who was **younger than 12 on 1 January 2025**, AND the taxpayer met the minimum arbeidsinkomen threshold.

- Check `profile.yaml` → `household.children` for DOBs.
- If at least one child satisfies the age condition, mark IACK as a manual-review item; do not calculate the amount.

### 5.5.2 Ouderenkorting

Triggered when the taxpayer reaches AOW age in 2025.

- Check `profile.yaml` → `person.aow_age_in_tax_year`.
- If triggered, flag as manual review.

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

### 5.5.5 Output

Write the screening results to `workspace/annual/2025/notes/credits.yaml`. The template's Credits screening section emits these results verbatim.

---
