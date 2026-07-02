# Rule note: Claude Code Agent Skills design patterns

source_ids: anthropic_agent_skills_overview, claude_code_skills
workflow: all
tax_year: all
status: active
last_reviewed: "2026-05-13"
review_status: reviewed

## Rule

Claude Code Agent Skills follow a standard structure and set of conventions. All skills in this project must conform to these patterns.

## Skill structure

- Skills live in sibling skill directories as `<skill-name>/SKILL.md`
- Skill directories may include: `reference/`, `templates/`, `examples/`, `scripts/`
- Skills are discovered from frontmatter (name, description)
- SKILL.md body should be concise; detailed knowledge belongs in supporting files

## Discovery and invocation

- Skills are discovered automatically from their frontmatter fields (name, description)
- Users invoke skills via slash commands in the Claude Code interface
- The agent may also invoke skills programmatically when a task matches a skill's description

## Execution context

- `context: fork` runs the skill in an isolated subagent with no access to the parent conversation. The subagent receives the SKILL.md content as a one-shot prompt and returns a single summary. Only use this for stateless analysis tasks that need no user follow-up (e.g. summarizing a fixed input). Never use it for skills that ask the user questions, iterate on assumptions, or produce workpacks across multiple turns -- the subagent cannot read or reply to the user
- `disable-model-invocation: true` prevents auto-invocation (for maintenance or dangerous skills)
- `user-invocable: false` hides from slash-command menu but allows model invocation

## Tool control

- `allowed-tools` pre-approves tools for use during skill execution
- This is NOT a security sandbox -- it is a convenience mechanism to avoid repeated approval prompts
- Only list tools the skill genuinely needs

## User guidance

- `argument-hint` provides the user with usage hints in the slash-command menu
- Keep hints short and actionable

## Shared resources

- Shared resources in `_shared/` are project-level, loaded on demand
- Knowledge files, templates, and registers in `_shared/` are available to all skills
- Skills reference shared resources by relative path from the skill directory. Claude Code may expose a current skill-directory path at runtime, but project instructions should prefer host-neutral relative paths.

## Developer instruction

When creating or modifying skills in this project:

1. Keep SKILL.md concise -- move detailed rules, rates, and procedures to knowledge files in `_shared/knowledge/`
2. Do NOT set `context: fork` on the workpack or intake skills. These are interactive workflows that need to ask the user follow-up questions and iterate across turns; a forked subagent cannot do that. Reserve `context: fork` for stateless one-shot analysis only
3. Set `disable-model-invocation: true` for skills that modify source data or perform destructive operations
4. Always declare `allowed-tools` as a YAML list (space-separated strings also work, but lists are unambiguous). Use `python3` (not `python`) in `Bash(...)` patterns -- macOS does not ship a bare `python` interpreter
5. Register any new external sources in `_shared/source-register.yaml`

## Common failure

Do not put year-specific rates or thresholds directly in SKILL.md. These change annually and belong in year-specific knowledge files under `_shared/knowledge/years/`.
