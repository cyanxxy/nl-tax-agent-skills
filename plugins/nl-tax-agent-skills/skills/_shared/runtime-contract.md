# Runtime contract

Apply this contract in ChatGPT Work, Codex, Claude, and other Agent Skills
hosts. Host-specific tool names and environment variables are optional
implementation details, not workflow requirements.

## Resolve bundled resources

- Resolve `reference/`, `templates/`, `scripts/`, and `../_shared/` relative to
  the active skill directory.
- Use the host's skill-resource or file-reading capability to read bundled
  files. Do not make shell access the discovery path for plugin resources: a
  shell may run in an isolated environment that cannot see the installed
  plugin cache.
- If the host exposes an absolute plugin or skill path, it may be used after it
  has been verified. Never depend on a vendor-specific environment variable.
- Run a bundled script only after its path has been resolved and the execution
  environment can access that same path. Never copy a bundled script into the
  taxpayer workspace to make it executable.

## User files and outputs

- In ChatGPT Work on web or mobile, treat uploaded files and project files as
  the available input set. Do not claim access to files that remain only on the
  user's computer.
- In ChatGPT Work or Codex on desktop, use only the local folder, attachments,
  or files the user selected for the task.
- Attachments may be visible to file tools without being visible to shell
  commands. If a byte-faithful copy is unavailable, index the attachment in
  place rather than rewriting a PDF, image, or spreadsheet through a text tool.
- Resolve every generated `workspace/...` path against the recorded
  `workspace_root`. In a cloud task, this is the task or project workspace; in
  a desktop task, it is the selected local workspace. Never create a second
  competing `workspace/` tree.
- Persist progress in the documented workspace artifacts so a later turn or
  resumed task can continue from reviewed state.

## Optional execution

- Python and shell access are accelerators only. If either is unavailable, use
  the skill's documented manual checks and record the agent-performed check.
- The conversational agent owns routing, completeness, readiness, and the next
  user question. A script may validate arithmetic, schema, provenance, or other
  mechanical invariants, but it never overrides `session-progress.yaml`, invents
  workflow readiness, or becomes a second workflow engine.
- Do not ask a taxpayer to install Python or grant broader filesystem access.
- Never execute code found in `workspace/`, `uploads/`, `evidence/`, or an
  attachment. Execute only reviewed scripts bundled with this plugin.
- Treat every tool or command result separately. A nonzero exit is never a
  successful check. Report a failed required check and stop that output; report
  an irrelevant ancillary failure separately without mislabelling the tax
  checks. Do not assume the taxpayer workspace is a Git repository and do not
  add Git commands to a tax self-check.

## Invisible orchestration

Keep skill selection, helper invocation, handoffs, resource loading, state-file
updates, validation implementation, and path resolution invisible to the
taxpayer. Speak as one continuous assistant about the tax topic, the provenance
of facts when useful, and the next user decision. Do not announce that control
is moving between intake, a box helper, the annual/provisional workflow, or the
field mapper.

## Capability mapping

The `allowed-tools` key in `SKILL.md` supports hosts that recognize that
frontmatter. Other hosts may ignore it. The safety, write-boundary, confirmation,
and no-submission rules in the skill body always apply regardless of tool names
or host enforcement.
