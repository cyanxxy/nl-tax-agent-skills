## Manual-entry checklist

<!-- Content spec for the "## Manual-entry checklist" section of the workflow's
workpack. Show the same content in the conversation. Write it into the saved
workpack only while save consent is active in this conversation (checked in the
conversation, never from the file's save_consent), replacing "not requested"
or the previous checklist; never as a separate file. Never copy a value from
a stale map; when a sourced fact changes after generation, the owning workflow
adds the STALE line at the top of this section, and only regeneration followed
by a new checklist request removes it. Replace every [bracketed] instruction;
drop subsections that do not apply. -->

> **HUMAN-ONLY PORTAL STEPS.** You, the taxpayer or an authorized human,
> perform every portal step below on your own device. The assistant does not
> open or operate Mijn Belastingdienst, enter values, click controls, sign,
> send, or submit.

Workflow: [annual_2025 / provisional_2026_request / provisional_2026_change / provisional_2026_review / provisional_2026_stopzetten]
Prepared: [date]
Based on: [workpack STATUS; field map readiness, or "no field map for this subflow"]

### 1. Blockers: resolve these before you open the portal

[If `generation_confirmed` is false, or the Field map summary, Appendix B, or
this checklist carries a line that starts with STALE, list only the stale
blocker, "The field map predates the change to <fact> (<date>); the workpack
and field map must be regenerated before use.", and stop: no warnings, no
steps, and no values until regeneration re-runs the field mapper.
Otherwise list every item that must be resolved first, each with its ID:
- `MISSING - enter manually` rows and `manual_review_required` rows from the
  Field map summary;
- blocking Q-IDs in Open questions and M-IDs in Missing information;
- unconfirmed assumptions;
- for provisional_2026_review: Review questions rows that are open or whose
  recommended action is the change subflow;
- for a change: "Prepare and verify the complete dataset; the change form
  requires all applicable categories, not only the changed item.";
- for stopzetten: a passed 1 October 2026 cutoff.]
[If there are none, write "No blockers."]
[A field map is expected for annual, provisional request, and provisional
change only. Do not list a missing field map as a blocker for provisional
review or stopzetten.]

### 2. Warnings

[Low-confidence rows and user-accepted assumptions (A-IDs) you should verify
while entering values.]

### 3. Before you start

- [ ] You have this workpack open beside the portal, including the Field map summary when this workflow has one.
- [ ] You have the documents listed in Documents and sources at hand.
- [ ] [If fiscal partner: you know whether you file together or separately. Together, both partners review and sign. Separately, each partner signs their own return and the shared allocation entries stay consistent across both returns.]
- [ ] [If someone else files for you: their authorization has been checked.]

### 4. Steps

[Workflow-specific human steps from the matching submit-step reference, every
portal action with an explicit human subject such as "**You (the taxpayer):**".
Cross-reference field-map rows only for annual, provisional request, or
provisional change, printing a double-entry fact once per screen path:

| Step | Portal label | Value to enter | Source | field_id |
|---|---|---|---|---|

For review, use the Review questions rows.
For stopzetten, do not invent field-map rows.]

### 5. Final human review

- [ ] I compared every entered value with the Field map summary or the workpack.
- [ ] I resolved or consciously accepted every blocker and warning above.
- [ ] I reviewed the portal's own summary before deciding to sign and send.

### 6. After sending

- [ ] I saved the confirmation/receipt.
- [ ] I noted the date I sent it.
- [ ] If annual: I recorded the expected definitieve-aanslag timeframe.
- [ ] If provisional: I noted the response timing shown in Mijn Belastingdienst or the confirmation.
- [ ] I kept my documents for my records; for winst uit onderneming, I followed AWR article 52 (`law_awr_artikel_52`) via `nl-tax-shared-resources/knowledge/years/2025/entrepreneur/winst-en-kosten.md`.

### Authorization check

- [ ] I am submitting my own return
- [ ] OR: I am authorized to submit on behalf of the taxpayer
- [ ] I understand paper filing is outside this supported online workflow unless exact official guidance has been added for my case
