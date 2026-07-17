# Rule note: Agent-host capabilities and automation patterns

source_ids: openai_codex_subagents, openai_codex_plugin_manifest, openai_scheduled_tasks, claude_plugin_reference, claude_plugins_cowork, claude_cowork_overview, claude_cowork_scheduled_tasks
workflow: all
tax_year: all
status: active
last_reviewed: "2026-07-16"
review_status: reviewed

## Current host capabilities

Both ChatGPT Work/Codex and Claude Cowork can coordinate parallel subagents.
This plugin uses that capability only for bounded review of facts already
collected by the owning workflow. It does not split the taxpayer conversation
into independent owners and does not replace agent judgment with a fixed flow.

### Claude

- Claude plugins can package skills and specialized agents. Plugin-shipped
  agents are Markdown files under `agents/` and can carry a narrow tool list,
  model/effort settings, and a turn limit. The default plugin-root `agents/`
  directory is auto-discovered; use the manifest `agents` field only for
  supported custom agent-file paths, not to re-declare that default directory.
- Plugin skills work in Claude chat and Cowork. Plugin hooks and subagents run
  only in Cowork, so chat must fall back to the owning skill doing the review
  inline.
- Cowork itself can coordinate parallel workstreams. The packaged
  `nl-tax-specialist-reviewer` therefore handles an owner-specified section and
  returns findings to the owner, which keeps the taxpayer conversation and
  canonical workpack state.

### ChatGPT Work and Codex

- ChatGPT Work and Codex can spawn subagents in parallel and collect their
  results in the main task. Codex also has built-in agents and supports custom
  project agents from `.codex/agents/`.
- The Codex plugin manifest currently declares skills, MCP servers, apps, and
  hooks, but not plugin-packaged custom-agent files. Therefore the OpenAI bundle
  ships the shared reviewer contract in the owning skills and relies on the
  host's built-in subagent facility; it does not pretend that the Claude agent
  file is a portable Codex plugin component.
- A user or project may define its own Codex reviewer, but the tax
  plugin must also work without that optional host customization.

## Parallel specialist-review pattern

The only supported taxpayer-work pattern is:

1. One main workflow owns the conversation, questions, workspace state, and
   final workpack.
2. The owner may delegate independent, already-bounded checks such as evidence
   versus field-map reconciliation, Box 3 row review, or partner-allocation
   consistency.
3. Reviewers inspect the named material, may consult official sources or run
   optional mechanical checks, and return conflicts and missing facts without
   making filing choices.
4. The owner reconciles the findings, asks any necessary user question, and is
   the only writer and readiness decision-maker.

This is agentic parallel review, not a scripted interview, rules engine, or
multi-writer workflow. Reviewers increase coverage; they do not partition the
taxpayer case into autonomous owners.

## Scheduled tasks

Both host families offer scheduled/background tasks. When the user asks, useful
tax-work automations include deadline reminders, missing-document check-ins,
source-freshness reports, and resuming a saved draft for review. The task reads
the same conversation ledger and returns its result to the user; scheduling
does not replace the owning agent with a fixed questionnaire or rules engine.

A maintainer may also schedule source-staleness reports, tests, or platform-doc
checks against the repository.

Host constraints differ: ChatGPT desktop tasks can run against a local project
or isolated worktree while web tasks cannot retain a local folder. Cowork
remote schedules use account files/connectors; a schedule that needs a local
folder or local app runs locally instead. These host features are optional and
are not required for the plugin's normal interactive use.

## Developer instruction

- Prefer one or two high-value specialist reviews over broad fan-out; subagents
  consume additional tokens and their outputs still need owner reconciliation.
- Give each reviewer the workflow, year, exact question, logical file paths,
  and reviewed source IDs. If that scope cannot be stated, keep the check in the
  main agent.
- Do not add a Python state machine or fixed decision tree as a substitute for
  the owning agent.
