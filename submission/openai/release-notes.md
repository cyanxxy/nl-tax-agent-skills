# OpenAI Plugin Directory release 0.2.0

NL Tax Agent Skills is a skills-only plugin for preparing source-traceable Dutch
individual income-tax workpacks for manual Mijn Belastingdienst entry. The
release supports annual 2025 preparation and 2026 voorlopige aanslag
request, change, review, and stopzetten workflows.

This release completes winst-uit-onderneming coverage for the annual 2025
return. The previous prep-only ceiling is retired: for a straightforward
eenmanszaak the workflow now determines the belastbare winst uit onderneming
from a finalized profit-and-loss statement and balance, following one canonical
ordered chain, and carries the result into the Box 1 total. Every other IB
business form is recognised and routed to manual review. The plugin never
computes a stakingswinst, a reserve movement, a terbeschikkingstellingsresultaat,
a medegerechtigde loss cap, or a per-vennoot winstaandeel.

Sixteen reviewed knowledge notes back that chain, covering profit computation
and fiscal corrections, depreciation and vermogensetikettering, vehicles and
private use, the bijdrage Zorgverzekeringswet, uitgaven voor
inkomensvoorzieningen, loss set-off, cessation, samenwerkingsverbanden,
resultaat uit overige werkzaamheden and the arbeidsrelatie, the meewerkende
partner, the aanloopfase and starters, and the business entry schema, plus
provisional-2026 winst and Zvw notes. Every rate and threshold cites a
registered official source.

Where official sources disagree, the note records the conflict and routes the
case to manual review instead of resolving it silently. That applies to the
desinvesteringsbijtelling threshold, the MIA/Vamil ceiling, the stakingslijfrente
age brackets, the exact EUR 450 small-purchase boundary, the zonnecelauto
qualification test, and the AOW-transition first-bracket series.

Field-map verification is now explicitly agent-and-human. The bundled validator
script has been removed from the plugin; the runtime check is the agent
checklist plus the taxpayer's review before manual entry. Field-map policy —
prohibitions, special identifiers, and readiness disqualifiers — is canonical in
`reference/field-map-rules.yaml`, which the agent applies directly on every
host, including hosts with no Python runtime. The repository's offline eval
grader loads the same file, so both readers apply one policy. An optional
renderer remains bundled. Nothing mechanical can promote a draft to
review-ready: completeness is established in the taxpayer conversation.

An annual business field map reaches review-ready only for a straightforward
eenmanszaak whose reviewed business schema is complete. Any other business form,
or a deduction screen the reviewed schema does not establish as form-computed,
keeps the map a draft with a named blocker.

The bijdrage Zorgverzekeringswet never appears as a field-map row in any
workflow: it arrives as a second, separate aanslag computed from the same
return, with no entry screen to type into. For the provisional flows it is
surfaced as a companion item the taxpayer checks separately, and no Zvw amount
is sized or merged. The provisional expected-profit field is specified as the
winst before ondernemersaftrek and mkb-winstvrijstelling, excluding btw, and
negative for a loss.

Annual 2025 and provisional 2026 remain rigorously separate, including the box 3
rule that provisional 2026 uses the fictitious method only and never collects or
computes werkelijk rendement.

The plugin has no connected apps, external authentication, portal automation,
filing, signing, or submission capability. That boundary applies even when
Chrome, computer use, connectors, credentials, or user permission are available:
the assistant creates an explicitly human-owned checklist, and the taxpayer or
an authorized human performs every authenticated portal action. The release
passes 438 repository tests and validates all 237 registered sources without
errors or warnings. Python remains optional.
