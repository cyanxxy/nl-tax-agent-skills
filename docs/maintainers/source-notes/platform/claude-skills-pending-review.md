# Pending corrections: Claude Code Agent Skills design patterns

corrects: platform/claude-skills.md
source_ids: anthropic_agent_skills_overview, claude_code_skills
review_status: pending_human_review
proposed: "2026-11-03"

These corrections were drafted against the live Claude Code skills and plugin
reference pages and the agentskills.io specification on 2026-11-03. They are
**not human-reviewed**. `claude-skills.md` keeps its reviewed text and hash
until a maintainer reviews these points, merges them into that note, and
re-records its hash. Until then, where the two disagree, follow this file.

## Discovery and invocation

- `disable-model-invocation: true` stops Claude from invoking the skill and
  keeps its description out of context; only the user can run it. Use it for
  maintenance or dangerous skills.
- `user-invocable: false` hides the skill from the `/` menu but keeps it
  model-invocable. The background helpers use it alone so an owning workflow
  can invoke them.
- Setting both makes a skill unreachable through the Skill tool. Only the
  `nl-tax-shared-resources` file bundle, read by path and never invoked, sets
  both.
- Developer instruction 3 in the reviewed note should read: set
  `disable-model-invocation: true` only for skills that modify source data or
  perform destructive operations; background helpers use `user-invocable:
  false` alone.

## Tool control

- Declare `allowed-tools` as one space-separated string, as the specification
  defines it (for example `allowed-tools: Read Glob Grep Edit(./workspace/**)`).
  This replaces developer instruction 4, which asked for a YAML list.
- Skills pre-approve no `Bash` and no `Write`, so the `python3` advice for
  `Bash(...)` patterns no longer applies. `Edit(...)` rules cover every
  built-in tool that creates or changes files.
- In Claude Code the pre-approval lasts only for the turn that invokes the
  skill.

## Frontmatter portability

- The specification allows only `name`, `description`, `license`,
  `compatibility`, `metadata`, and `allowed-tools`. claude.ai skill uploads and
  the Skills API reject any other key.
- `argument-hint`, `user-invocable`, and `disable-model-invocation` are Claude
  Code plugin keys. They are valid here because the plugin is plugin-only and
  never distributed as separate skill uploads.
- The plugin is plugin-only: skills reach `nl-tax-shared-resources/` and
  sibling skills through `../` paths. Every `SKILL.md` states this in its
  `compatibility` field.
- `submission/openai/build_bundle.py` strips the Claude-only keys from the
  OpenAI bundle. CI runs `claude plugin validate --strict` on the plugin and
  marketplace, and `skills-ref validate` on the OpenAI bundle and on a
  spec-only copy of the Claude plugin skills.
