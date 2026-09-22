# Rule note: MKB-winstvrijstelling 2025

source_ids: bd_mkb_winstvrijstelling_2025, bd_mkb_winstvrijstelling_general, law_wet_inkomstenbelasting_2001
workflow: annual_return
tax_year: 2025
status: active
last_reviewed: "2026-08-15"
review_status: reviewed

## Rule

The MKB-winstvrijstelling (art. 3.79a Wet IB 2001) exempts a fixed percentage of
the profit from tax. It sits in its own paragraaf 3.2.5, after and separate from
the ondernemersaftrek (paragraaf 3.2.4). This note is canonical for the 2025
percentage, for the base it is applied to, and for the fact that the aangifte
applies it without taxpayer entry. Where this step sits in the full 2025
computation -- which line it is subtracted from and which downstream bases are
read off which line -- is in `winstberekening-2025.md`; the two amounts that
reduce the base before it are in `investeringsaftrek.md` and
`ondernemersaftrek.md`. Where this note and `winstberekening-2025.md` both
mention the percentage, this note is canonical.

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

## The aangifte applies the vrijstelling itself

- The Belastingdienst states that the vrijstelling does not have to be requested
  and that it takes the vrijstelling into account in the aangifte
  inkomstenbelasting itself ("Wij houden in uw aangifte inkomstenbelasting
  automatisch rekening met de vrijstelling").
- Consequence for the workpack: **there is no MKB-winstvrijstelling entry field.**
  The taxpayer never types the 12.7%, the exempt amount, or the profit after the
  vrijstelling into a form. Present the amount in the workpack narrative as a
  check on the outcome, never as a manual-entry row in a field map.
- The same holds for the winst and for the two amounts that reduce the base
  before it. The aangifte derives the saldo of the winstberekening, the
  ondernemersaftrek and its five components, and the
  kleinschaligheidsinvesteringsaftrek from the figures and the answers, so none
  of them is a manual-entry row either. What the taxpayer does enter are those
  underlying inputs: the winst-en-verliesrekening rubrieken, the balans columns,
  the priveonttrekkingen en -stortingen, the per-asset investment details, and
  the urencriterium, starter, S&O and meewerkende-partner answers. Get those
  right and the vrijstelling follows. `zakelijke-schema-2025.md` is canonical
  for the entry-versus-computed division.
- Use the computed amount as a reconciliation check. You (the taxpayer) can
  compare it against the figure the aangifte shows on screen. If the two do not
  match, the base is wrong -- recheck the winst, the investeringsaftrek and the
  ondernemersaftrek in `winstberekening-2025.md` before changing anything else.
- This statement is about the aangifte inkomstenbelasting only. Do not extend it
  to any other form or any other year.

## Bases measured before and after this step

Two downstream 2025 bases are measured at different points of the chain, and
confusing them is the most common error around this vrijstelling:

| Downstream base | Measured | Canonical note |
|-----------------|----------|----------------|
| Zvw bijdrage-inkomen (winst component) | **after** the MKB-winstvrijstelling -- it is the belastbare winst uit onderneming of art. 3.2 Wet IB 2001, so both the ondernemersaftrek and this vrijstelling have already reduced it | `zvw-2025.md` |
| Lijfrente premiegrondslag (winst component) | **before** the ondernemersaftrek (art. 3.127 lid 3 onderdeel a Wet IB 2001), and therefore before this vrijstelling as well | `inkomensvoorzieningen-2025.md` |

The legal basis on the Zvw side is art. 43 Zorgverzekeringswet, which defines the
bijdrage-inkomen. The Zvw percentage and the maximumbijdrage-inkomen stay in
`zvw-2025.md` and are never restated here; the lijfrente ruimte figures stay in
`inkomensvoorzieningen-2025.md`.

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
   result. For the ordered chain as a whole, and for which line each downstream
   base is read off, read `winstberekening-2025.md`.
2. Show the base explicitly (winst after investeringsaftrek and
   ondernemersaftrek) so the 12.7% is traceable. Never paraphrase the percentage
   from memory -- read it here.
3. The MKB-winstvrijstelling is personal to the ondernemer and cannot be
   allocated between fiscal partners.
4. Never emit a manual-entry field for the MKB-winstvrijstelling and never tell
   the taxpayer to type it anywhere. The aangifte applies it itself. If the
   workpack shows the amount, label it as a computed check, not as an entry. The
   same prohibition applies to the ondernemersaftrek components and the
   kleinschaligheidsinvesteringsaftrek -- see `zakelijke-schema-2025.md`.
5. When the workpack also covers the Zvw bijdrage or a lijfrente deduction, state
   in the narrative which line each base is read off (Zvw after this vrijstelling,
   lijfrente premiegrondslag before the ondernemersaftrek) and read the figures
   themselves from `zvw-2025.md` and `inkomensvoorzieningen-2025.md`. Do not
   reuse this vrijstelling's base for either of them.
6. Profit earned as a medegerechtigde or as a geldverstrekker is outside this
   vrijstelling. Ask the taxpayer whether any part of the profit was earned in
   one of those capacities rather than as ondernemer; if the answer is yes, or is
   not established, split out that part and route it to manual review.
