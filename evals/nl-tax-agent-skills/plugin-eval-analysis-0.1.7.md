# Plugin Eval Report: nl-tax-agent-skills

> **Agentic design extension:** all 5/5 local design checks pass: five natural
> scenarios, complete agreed-profile coverage, a 100-point rubric with hard
> failures, and a minimal workspace with one structural verifier. Plugin Eval's
> Markdown renderer does not render extension results; the schema-compatible
> payload is retained in `agentic-design-checks-0.1.7.json`. The core score
> below remains the unmodified aggregate static analyzer result and should not
> be read as the conversational rubric score.

## At a Glance
- Score: 0/100
- Grade: F
- Risk: high
- Checks: 2 fail, 16 warn, 2 info
- Active budget: 18559 tokens (excessive)
- Observed usage: not supplied

## Why It Matters
- 2 failing error checks are driving the highest-confidence problems.
- 16 warning signals still need cleanup before this feels polished.
- best-practice is the largest source of score loss at -58.5 points.
- Active budget pressure is high enough that token cost may dominate the user experience.
- No observed usage is attached yet, so budget conclusions are still based on static estimates.

## Fix First
- [fail/error] deferred_cost_tokens is excessive relative to the current Codex baseline. Why: Budget pressure matters because always-loaded or frequently-loaded text can make the workflow feel expensive fast. Fix: Reduce repeated instruction text and move detail into deferred supporting files.
- [fail/error] invoke_cost_tokens is excessive relative to the current Codex baseline. Why: Budget pressure matters because always-loaded or frequently-loaded text can make the workflow feel expensive fast. Fix: Reduce repeated instruction text and move detail into deferred supporting files.
- [warn/warning] trigger_cost_tokens is heavy relative to the current Codex baseline. Why: Budget pressure matters because always-loaded or frequently-loaded text can make the workflow feel expensive fast. Fix: Reduce repeated instruction text and move detail into deferred supporting files.

## Recommended Next Step
- Measure real token usage next
- Why: The static budget looks heavy, so live usage is the fastest way to confirm whether the cost is acceptable.
- Chat request: "Measure the real token usage of this plugin."
- Local command: `plugin-eval start ~/Downloads/Projects/Tax skill/plugins/nl-tax-agent-skills --request 'Measure the real token usage of this plugin.' --format markdown`

## Details
<details>
<summary>Watch next</summary>

- [warn/warning] The skill frontmatter contains keys outside the common Codex skill conventions. Why: Best-practice gaps usually do not break the workflow immediately, but they make the skill harder to understand and improve. Fix: Remove non-standard frontmatter keys or move the metadata into references.
- [warn/warning] The description does not clearly advertise when the skill should trigger. Why: Best-practice gaps usually do not break the workflow immediately, but they make the skill harder to understand and improve. Fix: Rewrite the description to include a clear 'Use when ...' trigger sentence.
- [warn/warning] The description does not clearly advertise when the skill should trigger. Why: Best-practice gaps usually do not break the workflow immediately, but they make the skill harder to understand and improve. Fix: Rewrite the description to include a clear 'Use when ...' trigger sentence.
</details>
<details>
<summary>Improvement brief</summary>

- Raise the evaluation from grade F (0/100) with a focus on the highest-signal structural and budget issues first.
- Goal: Remove non-standard frontmatter keys or move the metadata into references.
- Goal: Rewrite the description to include a clear 'Use when ...' trigger sentence.
- Measure: token-usage-observer
- Measure: task-outcome-scorecard
- Measure: tool-call-audit
- Measure: latency-efficiency
- Suggested prompt: Use the skill-creator guidance to improve nl-tax-agent-skills. Keep the structure compact and move bulky details into references or scripts. Define success measures with these toolsets: token-usage-observer, task-outcome-scorecard, tool-call-audit, latency-efficiency. Address invoke_cost_tokens-budget-high: invoke_cost_tokens is excessive relative to the current Codex baseline. Address deferred_cost_tokens-budget-high: deferred_cost_tokens is excessive relative to the current Codex baseline. Address skill:nl-tax-annual-return:frontmatter-extra-keys: The skill frontmatter contains keys outside the common Codex skill conventions. Address skill:nl-tax-box1-home:description-trigger-weak: The description does not clearly advertise when the skill should trigger. Address skill:nl-tax-box2:description-trigger-weak: The description does not clearly advertise when the skill should trigger. Address skill:nl-tax-box3:description-trigger-weak: The description does not clearly advertise when the skill should trigger. Address skill:nl-tax-evidence-indexer:frontmatter-extra-keys: The skill frontmatter contains keys outside the common Codex skill conventions. Address skill:nl-tax-field-mapper:frontmatter-extra-keys: The skill frontmatter contains keys outside the common Codex skill conventions.
</details>
<details>
<summary>Budgets and observed usage</summary>

- trigger_cost_tokens: 252 (heavy)
- invoke_cost_tokens: 18307 (excessive)
- deferred_cost_tokens: 301085 (excessive)
- explicit_only_invoke_cost_tokens: 10172 (heavy, unscored)
- total_tokens: 319644 (excessive)
- invocation_policy: 5 implicit skill(s), 7 explicit-only skill(s)

- No observed usage supplied.
</details>
<details>
<summary>Measurement plan</summary>

Combine cost, outcome, and trust signals so you can tell whether the skill or plugin is genuinely helping instead of only looking well-structured on paper.

- Token Usage Observer [high] Measure how many tokens the skill or plugin actually burns in representative runs. Signals: observed_usage_sample_count, observed_input_tokens_avg, observed_total_tokens_avg, estimate_vs_observed_input_ratio. Evidence: Responses API usage logs, Codex-like session exports, JSONL traces captured from local benchmarking harnesses.
- Task Outcome Scorecard [high] Measure whether the skill helps users finish the intended job with fewer retries and less cleanup. Signals: task_success_rate, first_pass_success_rate, retry_rate, human_override_rate. Evidence: Task run logs, Structured user acceptance checklist, Before/after comparison runs on the same prompts.
- Tool Call Audit [high] Check whether the agent uses the right tools, arguments, and sequencing when the skill is active. Signals: tool_call_success_rate, invalid_tool_argument_rate, recoverable_tool_failure_rate. Evidence: Tool invocation traces, Recorded sessions, Golden-path scenario replays.
- Latency And Efficiency [high] Track whether the skill speeds users up enough to justify its cost. Signals: p50_time_to_first_acceptable_answer_seconds, p95_time_to_task_completion_seconds, tokens_per_successful_run. Evidence: Benchmark harness timings, Manual stopwatch runs on canonical tasks, Responses API timestamps combined with usage logs.
- Human Rubric Review [medium] Capture clarity, trust, and usefulness signals that automated checks will miss. Signals: clarity_score_avg, confidence_score_avg, follow_up_question_rate. Evidence: Reviewer scorecards, Team rubric sheets, Annotated transcripts.
- Regression Suite [medium] Protect the repository behavior that the skill is supposed to improve. Signals: test_pass_rate, lint_pass_rate, regression_escape_count. Evidence: Unit and integration test runs, Coverage deltas, Snapshot or golden-file checks.
</details>
<details>
<summary>Use From Codex Chat</summary>

Start with a natural chat request, then let plugin-eval show the exact local command sequence behind it.

Start with this chat request: "Evaluate this plugin."
Why this path: Plugin Eval recommended Evaluate Plugin from the current local state for this plugin.
Quick local entrypoint: plugin-eval start ~/Downloads/Projects/Tax skill/plugins/nl-tax-agent-skills --request 'Evaluate this plugin.' --format markdown
Plugin Eval will run first: plugin-eval analyze ~/Downloads/Projects/Tax skill/plugins/nl-tax-agent-skills --format markdown

Other chat requests you can use:
- Full Plugin Analysis: say "Give me a full analysis of this plugin, including benchmark setup." -> plugin-eval analyze ~/Downloads/Projects/Tax skill/plugins/nl-tax-agent-skills --format markdown
- Evaluate Plugin: say "Evaluate this plugin." -> plugin-eval analyze ~/Downloads/Projects/Tax skill/plugins/nl-tax-agent-skills --format markdown
- Explain Token Budget: say "Explain the token budget for this plugin." -> plugin-eval explain-budget ~/Downloads/Projects/Tax skill/plugins/nl-tax-agent-skills --format markdown
- Measure Real Token Usage: say "Measure the real token usage of this plugin." -> plugin-eval init-benchmark ~/Downloads/Projects/Tax skill/plugins/nl-tax-agent-skills
- Benchmark With Starter Scenarios: say "Help me benchmark this plugin." -> plugin-eval init-benchmark ~/Downloads/Projects/Tax skill/plugins/nl-tax-agent-skills
- Start Here: say "What should I run next?" -> plugin-eval analyze ~/Downloads/Projects/Tax skill/plugins/nl-tax-agent-skills --format markdown
</details>
<details>
<summary>Checks</summary>

- [WARN] skill:nl-tax-annual-return:frontmatter-extra-keys: The skill frontmatter contains keys outside the common Codex skill conventions. Evidence: Unexpected key: argument-hint Remediation: Remove non-standard frontmatter keys or move the metadata into references.
- [WARN] skill:nl-tax-box1-home:description-trigger-weak: The description does not clearly advertise when the skill should trigger. Evidence: Descriptions are the primary auto-load surface in Codex. Remediation: Rewrite the description to include a clear 'Use when ...' trigger sentence.
- [WARN] skill:nl-tax-box2:description-trigger-weak: The description does not clearly advertise when the skill should trigger. Evidence: Descriptions are the primary auto-load surface in Codex. Remediation: Rewrite the description to include a clear 'Use when ...' trigger sentence.
- [WARN] skill:nl-tax-box3:description-trigger-weak: The description does not clearly advertise when the skill should trigger. Evidence: Descriptions are the primary auto-load surface in Codex. Remediation: Rewrite the description to include a clear 'Use when ...' trigger sentence.
- [WARN] skill:nl-tax-evidence-indexer:frontmatter-extra-keys: The skill frontmatter contains keys outside the common Codex skill conventions. Evidence: Unexpected key: argument-hint Remediation: Remove non-standard frontmatter keys or move the metadata into references.
- [WARN] skill:nl-tax-field-mapper:frontmatter-extra-keys: The skill frontmatter contains keys outside the common Codex skill conventions. Evidence: Unexpected key: argument-hint Remediation: Remove non-standard frontmatter keys or move the metadata into references.
- [WARN] skill:nl-tax-intake:frontmatter-extra-keys: The skill frontmatter contains keys outside the common Codex skill conventions. Evidence: Unexpected key: argument-hint Remediation: Remove non-standard frontmatter keys or move the metadata into references.
- [WARN] skill:nl-tax-partner-deductions:description-trigger-weak: The description does not clearly advertise when the skill should trigger. Evidence: Descriptions are the primary auto-load surface in Codex. Remediation: Rewrite the description to include a clear 'Use when ...' trigger sentence.
- [WARN] skill:nl-tax-provisional-assessment:frontmatter-extra-keys: The skill frontmatter contains keys outside the common Codex skill conventions. Evidence: Unexpected key: argument-hint Remediation: Remove non-standard frontmatter keys or move the metadata into references.
- [WARN] skill:nl-tax-source-refresh:frontmatter-extra-keys: The skill frontmatter contains keys outside the common Codex skill conventions. Evidence: Unexpected key: argument-hint Remediation: Remove non-standard frontmatter keys or move the metadata into references.
- [WARN] skill:nl-tax-submit-companion:frontmatter-extra-keys: The skill frontmatter contains keys outside the common Codex skill conventions. Evidence: Unexpected key: argument-hint Remediation: Remove non-standard frontmatter keys or move the metadata into references.
- [WARN] skill:nl-tax-submit-companion:description-trigger-weak: The description does not clearly advertise when the skill should trigger. Evidence: Descriptions are the primary auto-load surface in Codex. Remediation: Rewrite the description to include a clear 'Use when ...' trigger sentence.
- [WARN] skill:nl-tax-winst:description-trigger-weak: The description does not clearly advertise when the skill should trigger. Evidence: Descriptions are the primary auto-load surface in Codex. Remediation: Rewrite the description to include a clear 'Use when ...' trigger sentence.
- [WARN] trigger_cost_tokens-budget-high: trigger_cost_tokens is heavy relative to the current Codex baseline. Evidence: Value: 252 tokens Baseline samples: skills=32, plugins=175 Remediation: Reduce repeated instruction text and move detail into deferred supporting files.
- [FAIL] invoke_cost_tokens-budget-high: invoke_cost_tokens is excessive relative to the current Codex baseline. Evidence: Value: 18307 tokens Baseline samples: skills=32, plugins=175 Remediation: Reduce repeated instruction text and move detail into deferred supporting files.
- [FAIL] deferred_cost_tokens-budget-high: deferred_cost_tokens is excessive relative to the current Codex baseline. Evidence: Value: 301085 tokens Baseline samples: skills=32, plugins=175 Remediation: Reduce repeated instruction text and move detail into deferred supporting files.
- [WARN] py-complexity-high: At least one Python function has high cyclomatic complexity. Evidence: Max complexity: 272 Remediation: Split complex functions into smaller helpers or guard clauses.
- [WARN] py-function-length-high: At least one Python function is long enough to hurt readability. Evidence: Max function length: 117 lines Remediation: Break large functions into smaller helpers with clear names.
- [INFO] coverage-artifacts-unavailable: No coverage artifacts were found for this target. Evidence: plugins/nl-tax-agent-skills Remediation: Generate `lcov.info`, `coverage.xml`, or an Istanbul coverage JSON file if you want coverage scoring.
</details>
<details>
<summary>Metrics</summary>

- skill:nl-tax-annual-return:skill_line_count: 271 lines (good)
- skill:nl-tax-annual-return:description_length_chars: 168 chars (good)
- skill:nl-tax-annual-return:relative_link_count: 1 links (good)
- skill:nl-tax-annual-return:code_fence_count: 0 blocks (good)
- skill:nl-tax-annual-return:support_file_count: 17 files (good)
- skill:nl-tax-box1-home:skill_line_count: 102 lines (good)
- skill:nl-tax-box1-home:description_length_chars: 178 chars (good)
- skill:nl-tax-box1-home:relative_link_count: 0 links (good)
- skill:nl-tax-box1-home:code_fence_count: 1 blocks (good)
- skill:nl-tax-box1-home:support_file_count: 5 files (good)
- skill:nl-tax-box2:skill_line_count: 123 lines (good)
- skill:nl-tax-box2:description_length_chars: 187 chars (good)
- skill:nl-tax-box2:relative_link_count: 0 links (good)
- skill:nl-tax-box2:code_fence_count: 1 blocks (good)
- skill:nl-tax-box2:support_file_count: 4 files (good)
- skill:nl-tax-box3:skill_line_count: 106 lines (good)
- skill:nl-tax-box3:description_length_chars: 164 chars (good)
- skill:nl-tax-box3:relative_link_count: 0 links (good)
- skill:nl-tax-box3:code_fence_count: 2 blocks (good)
- skill:nl-tax-box3:support_file_count: 6 files (good)
- skill:nl-tax-evidence-indexer:skill_line_count: 166 lines (good)
- skill:nl-tax-evidence-indexer:description_length_chars: 173 chars (good)
- skill:nl-tax-evidence-indexer:relative_link_count: 0 links (good)
- skill:nl-tax-evidence-indexer:code_fence_count: 0 blocks (good)
- skill:nl-tax-evidence-indexer:support_file_count: 5 files (good)
- skill:nl-tax-field-mapper:skill_line_count: 204 lines (good)
- skill:nl-tax-field-mapper:description_length_chars: 157 chars (good)
- skill:nl-tax-field-mapper:relative_link_count: 0 links (good)
- skill:nl-tax-field-mapper:code_fence_count: 3 blocks (good)
- skill:nl-tax-field-mapper:support_file_count: 6 files (good)
- skill:nl-tax-intake:skill_line_count: 246 lines (good)
- skill:nl-tax-intake:description_length_chars: 172 chars (good)
- skill:nl-tax-intake:relative_link_count: 0 links (good)
- skill:nl-tax-intake:code_fence_count: 0 blocks (good)
- skill:nl-tax-intake:support_file_count: 3 files (good)
- skill:nl-tax-partner-deductions:skill_line_count: 100 lines (good)
- skill:nl-tax-partner-deductions:description_length_chars: 148 chars (good)
- skill:nl-tax-partner-deductions:relative_link_count: 0 links (good)
- skill:nl-tax-partner-deductions:code_fence_count: 2 blocks (good)
- skill:nl-tax-partner-deductions:support_file_count: 5 files (good)
- skill:nl-tax-provisional-assessment:skill_line_count: 232 lines (good)
- skill:nl-tax-provisional-assessment:description_length_chars: 162 chars (good)
- skill:nl-tax-provisional-assessment:relative_link_count: 0 links (good)
- skill:nl-tax-provisional-assessment:code_fence_count: 0 blocks (good)
- skill:nl-tax-provisional-assessment:support_file_count: 11 files (good)
- skill:nl-tax-source-refresh:skill_line_count: 42 lines (good)
- skill:nl-tax-source-refresh:description_length_chars: 178 chars (good)
- skill:nl-tax-source-refresh:relative_link_count: 0 links (good)
- skill:nl-tax-source-refresh:code_fence_count: 0 blocks (good)
- skill:nl-tax-source-refresh:support_file_count: 9 files (good)
- skill:nl-tax-submit-companion:skill_line_count: 52 lines (good)
- skill:nl-tax-submit-companion:description_length_chars: 190 chars (good)
- skill:nl-tax-submit-companion:relative_link_count: 0 links (good)
- skill:nl-tax-submit-companion:code_fence_count: 0 blocks (good)
- skill:nl-tax-submit-companion:support_file_count: 5 files (good)
- skill:nl-tax-winst:skill_line_count: 137 lines (good)
- skill:nl-tax-winst:description_length_chars: 194 chars (good)
- skill:nl-tax-winst:relative_link_count: 0 links (good)
- skill:nl-tax-winst:code_fence_count: 1 blocks (good)
- skill:nl-tax-winst:support_file_count: 3 files (good)
- plugin_skill_count: 12 skills (good)
- plugin_keyword_count: 7 keywords (good)
- plugin_default_prompt_count: 3 prompts (good)
- trigger_cost_tokens: 252 tokens (heavy)
- invoke_cost_tokens: 18307 tokens (excessive)
- deferred_cost_tokens: 301085 tokens (excessive)
- explicit_only_invoke_cost_tokens: 10172 tokens (heavy)
- py_file_count: 32 files (good)
- py_function_count: 516 functions (good)
- py_max_cyclomatic_complexity: 272 score (heavy)
- py_average_function_length: 17.28 lines (good)
- py_max_nesting_depth: 7 levels (heavy)
- py_comment_ratio: 0.029 ratio (moderate)
- py_test_file_count: 18 files (good)
- coverage_artifact_count: 0 files (info)
</details>
<details>
<summary>Score details</summary>

- Starting score: 100
- Total deductions: -100.25
- Final score: 0
- Risk: Contains 2 failing error checks (deferred_cost_tokens-budget-high, invoke_cost_tokens-budget-high).
- Risk: Overall score is below 70, which the evaluator treats as high risk.

- -14 points: deferred_cost_tokens-budget-high [fail/error] deferred_cost_tokens is excessive relative to the current Codex baseline.
- -14 points: invoke_cost_tokens-budget-high [fail/error] invoke_cost_tokens is excessive relative to the current Codex baseline.
- -4.5 points: py-complexity-high [warn/warning] At least one Python function has high cyclomatic complexity.
- -4.5 points: py-function-length-high [warn/warning] At least one Python function is long enough to hurt readability.
- -4.5 points: skill:nl-tax-annual-return:frontmatter-extra-keys [warn/warning] The skill frontmatter contains keys outside the common Codex skill conventions.
- -4.5 points: skill:nl-tax-box1-home:description-trigger-weak [warn/warning] The description does not clearly advertise when the skill should trigger.
- -4.5 points: skill:nl-tax-box2:description-trigger-weak [warn/warning] The description does not clearly advertise when the skill should trigger.
- -4.5 points: skill:nl-tax-box3:description-trigger-weak [warn/warning] The description does not clearly advertise when the skill should trigger.
- -4.5 points: skill:nl-tax-evidence-indexer:frontmatter-extra-keys [warn/warning] The skill frontmatter contains keys outside the common Codex skill conventions.
- -4.5 points: skill:nl-tax-field-mapper:frontmatter-extra-keys [warn/warning] The skill frontmatter contains keys outside the common Codex skill conventions.
- -4.5 points: skill:nl-tax-intake:frontmatter-extra-keys [warn/warning] The skill frontmatter contains keys outside the common Codex skill conventions.
- -4.5 points: skill:nl-tax-partner-deductions:description-trigger-weak [warn/warning] The description does not clearly advertise when the skill should trigger.
- -4.5 points: skill:nl-tax-provisional-assessment:frontmatter-extra-keys [warn/warning] The skill frontmatter contains keys outside the common Codex skill conventions.
- -4.5 points: skill:nl-tax-source-refresh:frontmatter-extra-keys [warn/warning] The skill frontmatter contains keys outside the common Codex skill conventions.
- -4.5 points: skill:nl-tax-submit-companion:description-trigger-weak [warn/warning] The description does not clearly advertise when the skill should trigger.
- -4.5 points: skill:nl-tax-submit-companion:frontmatter-extra-keys [warn/warning] The skill frontmatter contains keys outside the common Codex skill conventions.
- -4.5 points: skill:nl-tax-winst:description-trigger-weak [warn/warning] The description does not clearly advertise when the skill should trigger.
- -4.5 points: trigger_cost_tokens-budget-high [warn/warning] trigger_cost_tokens is heavy relative to the current Codex baseline.
- -0.25 points: coverage-artifacts-unavailable [info/info] No coverage artifacts were found for this target.

- best-practice: -58.5 points across 13 checks
- budget: -32.5 points across 3 checks
- complexity: -4.5 points across 1 check
- readability: -4.5 points across 1 check
- coverage: -0.25 points across 1 check
</details>
