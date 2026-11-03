# Rule note: Claude Code Agent Skills design patterns

source_ids: anthropic_agent_skills_overview, claude_code_skills
workflow: all
tax_year: all
status: active
last_reviewed: "2026-11-03"
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
- In Cowork, users normally describe the outcome in natural language and let the agent select the workflow skills
- Namespaced slash invocation such as `/nl-tax-agent-skills:nl-tax-intake annual` is an advanced Claude interface, not the required quickstart
- The agent may also invoke skills programmatically when a task matches a skill's description

## Execution context

- Cowork tasks may use local or remote execution environments; selected files, tools, and shell visibility depend on the active session
- Resolve bundled resources through host file tools. Treat Python helpers as optional accelerators and follow the documented agent check when the helper is unavailable

- `context: fork` runs the skill in an isolated subagent with no access to the parent conversation. The subagent receives the SKILL.md content as a one-shot prompt and returns a single summary. Only use this for stateless analysis tasks that need no user follow-up (e.g. summarizing a fixed input). Never use it for skills that ask the user questions, iterate on assumptions, or produce workpacks across multiple turns -- the subagent cannot read or reply to the user
- `disable-model-invocation: true` prevents Claude from invoking the skill and keeps its description out of context; only the user can run it (for maintenance or dangerous skills)
- `user-invocable: false` hides the skill from the `/` menu but keeps it model-invocable; use it for background helpers that only an owning workflow should call
- Setting both makes a skill unreachable through the Skill tool; reserve that for the `nl-tax-shared-resources` file bundle, which is read by path and never invoked

## Tool control

- `allowed-tools` pre-approves tools for use during skill execution
- This is NOT a security sandbox -- it is a convenience mechanism to avoid repeated approval prompts
- Only list tools the skill genuinely needs
- In Claude Code the pre-approval lasts only for the turn that invokes the skill

## Frontmatter portability

- The specification allows only `name`, `description`, `license`, `compatibility`, `metadata`, and `allowed-tools`. claude.ai skill uploads and the Skills API reject any other key
- `argument-hint`, `user-invocable`, and `disable-model-invocation` are Claude Code plugin keys. They are valid here because the plugin is plugin-only and never distributed as separate skill uploads
- `submission/openai/build_bundle.py` strips the Claude-only keys from the OpenAI bundle; CI runs `skills-ref validate` on that bundle and `claude plugin validate --strict` on the Claude plugin

## User guidance

- `argument-hint` provides the user with usage hints in the slash-command menu
- Keep hints short and actionable

## Shared resources

- The plugin is plugin-only: skills reach `nl-tax-shared-resources/` and sibling skills through `../` paths, so a skill does not work when installed or uploaded on its own. Every `SKILL.md` states this in its `compatibility` field
- Shared resources in `nl-tax-shared-resources/` are project-level, loaded on demand
- Knowledge files, templates, and registers in `nl-tax-shared-resources/` are available to all skills
- Skills reference shared resources by relative path from the skill directory. Claude Code may expose a current skill-directory path at runtime, but project instructions should prefer host-neutral relative paths.

## Developer instruction

When creating or modifying skills in this project:

1. Keep SKILL.md concise -- move detailed rules, rates, and procedures to knowledge files in `nl-tax-shared-resources/knowledge/`
2. Do NOT set `context: fork` on the workpack or intake skills. These are interactive workflows that need to ask the user follow-up questions and iterate across turns; a forked subagent cannot do that. Reserve `context: fork` for stateless one-shot analysis only
3. Set `disable-model-invocation: true` only for skills that modify source data or perform destructive operations. Background helpers use `user-invocable: false` alone
4. Declare `allowed-tools` as one space-separated string, as the Agent Skills specification defines it (for example `allowed-tools: Read Glob Grep Edit(./workspace/**)`). Skills pre-approve no `Bash` and no `Write`; `Edit(...)` rules cover every built-in tool that creates or changes files
5. Register any new external sources in `nl-tax-shared-resources/source-register.yaml`
6. Keep natural-language Cowork prompts as the primary usage path; document direct namespaced invocation only as an advanced path
7. Distinguish first-party Claude package validation from a human Cowork UI smoke test; one does not prove the other

## Common failure

Do not put year-specific rates or thresholds directly in SKILL.md. These change annually and belong in year-specific knowledge files under `nl-tax-shared-resources/knowledge/years/`.
