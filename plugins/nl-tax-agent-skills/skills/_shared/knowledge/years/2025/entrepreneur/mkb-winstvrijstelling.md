# Rule note: MKB-winstvrijstelling 2025

source_ids: bd_mkb_winstvrijstelling_2025, law_wet_inkomstenbelasting_2001
workflow: annual_return
tax_year: 2025
status: active
last_reviewed: "2026-07-06"
review_status: reviewed

## Rule

The MKB-winstvrijstelling (art. 3.79a Wet IB 2001) exempts a fixed percentage of
the profit from tax. It sits in its own paragraaf 3.2.5, after and separate from
the ondernemersaftrek (paragraaf 3.2.4).

These are reference notes for workpack preparation -- not final tax advice.

## Rate and base

- MKB-winstvrijstelling 2025: **12.7%**.
- Base = the joint amount of winst as ondernemer from one or more ondernemingen,
  **first reduced by investeringsaftrek such as KIA and then by the
  ondernemersaftrek**. The 12.7% is applied to that reduced amount.
- The 2025 rate (12.7%) is unchanged for 2026; it was 13.31% in 2024. Use only
  12.7% for the 2025 return.

## Conditions

- Granted to every ondernemer voor de inkomstenbelasting -- **no urencriterium**
  is required. Being an ondernemer is sufficient.
- Not granted over profit earned as a medegerechtigde or as a geldverstrekker.
- No application needed; it applies automatically and cannot be waived.

## Loss interaction

If the enterprise makes a loss, the 12.7% vrijstelling makes the fiscal loss
**smaller** (a disadvantage), because it applies to a negative amount too. When
it reduces a loss it does not count as a grondslagverminderende post for the
tariefsaanpassing (that correction needs a positive winst after investeringsaftrek
and ondernemersaftrek).

## Developer instruction

1. Compute in this order: winst uit onderneming, minus investeringsaftrek such as
   KIA (`investeringsaftrek.md`), minus ondernemersaftrek
   (`ondernemersaftrek.md`), then apply the 12.7% MKB-winstvrijstelling to the
   result.
2. Show the base explicitly (winst after investeringsaftrek and
   ondernemersaftrek) so the 12.7% is traceable. Never paraphrase the percentage
   from memory -- read it here.
3. The MKB-winstvrijstelling is personal to the ondernemer and cannot be
   allocated between fiscal partners.
