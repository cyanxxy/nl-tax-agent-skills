const fs = require("node:fs");
const path = require("node:path");

const here = __dirname;
const benchmark = JSON.parse(
  fs.readFileSync(path.resolve(here, "../plugin-eval-benchmark.json"), "utf8"),
);
const rubric = JSON.parse(
  fs.readFileSync(path.resolve(here, "../agentic-rubric.json"), "utf8"),
);

const scenarios = benchmark.scenarios || [];
const forbiddenPromptTerms = [
  "fixture",
  "current-case",
  "dataset case",
  "exact case",
  "expected file",
  "run offline",
];
const promptViolations = [];
for (const scenario of scenarios) {
  const lower = (scenario.userInput || "").toLowerCase();
  for (const term of forbiddenPromptTerms) {
    if (lower.includes(term)) promptViolations.push(`${scenario.id}: ${term}`);
  }
}

const requiredProfiles = new Set([
  "informational",
  "annual_preparation",
  "provisional_change",
  "entrepreneur_winst",
  "unsupported_boundary",
]);
const actualProfiles = new Set(scenarios.map((scenario) => scenario.rubricProfile));
const missingProfiles = [...requiredProfiles].filter((profile) => !actualProfiles.has(profile));
const totalWeight = (rubric.dimensions || []).reduce(
  (sum, dimension) => sum + Number(dimension.weight || 0),
  0,
);
const minimalWorkspace = benchmark.workspace?.sourcePath ===
  "evals/nl-tax-agent-skills/agentic-workspace";
const verifierCommands = benchmark.verifiers?.commands || [];
const oneHardVerifier = verifierCommands.length === 1 &&
  verifierCommands[0].includes("verify-hard-contracts.sh");

function check(id, status, message, evidence, remediation) {
  return {
    id,
    category: "agentic-eval-design",
    severity: status === "pass" ? "info" : "warning",
    status,
    message,
    evidence,
    remediation,
  };
}

const checks = [
  check(
    "agentic-five-scenario-scope",
    scenarios.length === 5 ? "pass" : "warn",
    "The live benchmark should stay focused on five representative conversations.",
    [`scenario_count=${scenarios.length}`],
    ["Use one informational, annual, provisional-change, entrepreneur, and unsupported scenario."],
  ),
  check(
    "agentic-natural-prompts",
    promptViolations.length === 0 ? "pass" : "warn",
    "Live prompts must sound like user requests rather than fixture instructions.",
    promptViolations.length ? promptViolations : ["No fixture, marker, exact-output, or dataset instructions found."],
    ["Remove evaluator implementation details from userInput."],
  ),
  check(
    "agentic-profile-coverage",
    missingProfiles.length === 0 && actualProfiles.size === 5 ? "pass" : "warn",
    "The benchmark should cover the five agreed agentic profiles once each.",
    missingProfiles.length ? [`missing=${missingProfiles.join(",")}`] : ["All five profiles are covered."],
    ["Add the missing profile without adding duplicate near-identical scenarios."],
  ),
  check(
    "agentic-weighted-rubric",
    totalWeight === 100 && (rubric.hardFails || []).length > 0 ? "pass" : "warn",
    "The shared rubric must have stable weighted dimensions and explicit hard fails.",
    [`dimension_count=${(rubric.dimensions || []).length}`, `total_weight=${totalWeight}`, `hard_fail_count=${(rubric.hardFails || []).length}`],
    ["Make dimension weights total 100 and retain explicit hard-fail conditions."],
  ),
  check(
    "agentic-minimal-harness",
    minimalWorkspace && oneHardVerifier ? "pass" : "warn",
    "Live evaluation should use a minimal workspace and only one hard-contract verifier.",
    [`workspace=${benchmark.workspace?.sourcePath}`, `verifier_count=${verifierCommands.length}`],
    ["Use agentic-workspace and keep semantic scoring in the LLM/human rubric."],
  ),
];

const passCount = checks.filter((item) => item.status === "pass").length;
process.stdout.write(JSON.stringify({
  checks,
  metrics: [
    {
      id: "agentic_scenario_count",
      category: "agentic-eval-design",
      value: scenarios.length,
      unit: "scenarios",
      band: scenarios.length === 5 ? "good" : "warn",
    },
    {
      id: "agentic_design_checks_passed",
      category: "agentic-eval-design",
      value: passCount,
      unit: "checks",
      band: passCount === checks.length ? "good" : "warn",
    },
  ],
  artifacts: [
    {
      id: "agentic-rubric",
      type: "rubric",
      label: "NL Tax agentic evaluation rubric",
      description: "Weighted human/LLM rubric for conversational plugin evaluation.",
      path: "../agentic-rubric.json",
    },
  ],
}, null, 2) + "\n");
