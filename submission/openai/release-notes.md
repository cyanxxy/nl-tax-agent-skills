# OpenAI Plugin Directory release 0.1.12

NL Tax Agent Skills is a skills-only plugin for preparing source-traceable Dutch
individual income-tax workpacks for manual Mijn Belastingdienst entry. The
release supports annual 2025 preparation and 2026 voorlopige aanslag
request, change, review, and stopzetten workflows.

Finite-choice intake now prefers a return-capable native control or compact
in-chat form when the active surface provides one. Codex may render an inline
form only when submission posts a follow-up message to the same task; otherwise
the skills use the same short conversational fallback. The cross-host contract
also distinguishes native Claude/Cowork inputs from custom Cowork visuals and
from Claude Code's `AskUserQuestion` tool.

Structured selections keep ordinary `user_chat` provenance and are not written
to taxpayer state until they return to the agent as a user response. The
four-option fallback preserves separate 2026 request, change, review, and
stopzetten routing.

The human-only manual-entry checklist is now discoverable from explicit natural
language, including an unambiguous affirmative reply to the field mapper's
immediate checklist offer; no slash command or magic phrase is required. Annual,
provisional request, and provisional change checklists use their field maps,
while review and stopzetten checklists work from their own reviewed artifacts
without falsely requiring a map.

One natural-language request can now retain both supported workflows: annual
2025 runs first, then a selected provisional 2026 subflow starts collection
after validated annual outputs without requiring another activation phrase.
The two workflows keep independent sources, state, artifacts, and final
generation confirmations; annual values are never copied into a provisional
estimate automatically.

Reviewed request, change, and stopzetten source snapshots remain unchanged.
Runtime loading uses hash-traceable, mechanically reversible human-subject
projections so portal actions are always framed as taxpayer actions. The field
map validator also rejects selector, XPath, DOM-locator, and browser-locator
metadata in both populated and missing rows.

The plugin has no connected apps, external authentication, portal automation,
filing, signing, or submission capability. The strengthened Claude/Cowork
boundary applies even when Chrome, computer use, connectors, credentials, or
user permission are available: the assistant creates an explicitly human-owned
checklist, and the taxpayer or an authorized human performs every authenticated
portal action. Dedicated Cowork evaluations cover both natural-language
checklist activation and refusal of portal control. Python remains optional.
