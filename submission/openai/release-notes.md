# Initial OpenAI Plugin Directory submission

NL Tax Agent Skills is a skills-only plugin for preparing source-traceable Dutch
individual income-tax workpacks for manual Mijn Belastingdienst entry. The
initial submission supports annual 2025 preparation and 2026 voorlopige aanslag
request, change, review, and stopzetten workflows.

This build adds a shared runtime contract for ChatGPT Work web/mobile, ChatGPT
Work desktop, and Codex; OpenAI-specific public-skill metadata and invocation
policies; explicit cloud-versus-local file handling; and reviewer test cases.
The plugin has no connected apps, external authentication, portal automation,
filing, signing, or submission capability. Python remains optional.
