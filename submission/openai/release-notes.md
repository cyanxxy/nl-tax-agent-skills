# OpenAI Plugin Directory release 0.1.11

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

The plugin has no connected apps, external authentication, portal automation,
filing, signing, or submission capability. Python remains optional.
