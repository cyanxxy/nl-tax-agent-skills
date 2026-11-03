#!/usr/bin/env python3
"""Validate cross-host invocation policy for the bundled skills.

Usage:
    python3 validate_invocation_policy.py <path-to-skills-dir>

Claude and Codex express invocation differently, so this validator names the
mapping instead of treating the two Claude flags as one:

- **Manual-only** (`disable-model-invocation: true`): the model never invokes
  the skill on Claude. Codex's equivalent is
  `policy.allow_implicit_invocation: false`.
- **Agent-only** (`user-invocable: false` without `disable-model-invocation`):
  hidden from the user's menu on Claude but model-invocable, so an owning
  workflow can invoke it as a skill. Codex has no agent-only mode. The
  OpenAI submission checklist requires that internal helpers never trigger
  implicitly, so Codex keeps `allow_implicit_invocation: false` and the
  owning workflow reaches the helper by explicit name or by reading its
  `SKILL.md` inline, as the runtime contract allows. This is a deliberate,
  reported divergence: Claude may pick an agent-only helper from its
  description, Codex may not.

On Codex the Claude frontmatter keys (`disable-model-invocation`,
`user-invocable`, `allowed-tools`) are NOT honored; `agents/openai.yaml` is the
only invocation control. This validator fails closed: every manual-only or
agent-only skill must ship `agents/openai.yaml` with
`policy.allow_implicit_invocation: false` and no `interface.default_prompt`
(a starter prompt in the Codex / ChatGPT skill picker would invite a user to
run an internal skill without its owning workflow).
"""

import os
import re
import sys


def _require_yaml():
    try:
        import yaml
    except ImportError:
        raise SystemExit(
            "PyYAML is required to validate invocation policy "
            "(python3 -m pip install pyyaml)."
        )
    return yaml


def parse_frontmatter(skill_md_path):
    """Return (frontmatter_dict, error) for a SKILL.md.

    Splits on fence LINES (a line that is exactly ``---``), not on the literal
    substring: a ``---`` inside a frontmatter value must not truncate the block,
    because a truncated parse could silently drop ``disable-model-invocation``
    and make this validator fail open. Unparseable frontmatter is reported as an
    error (fail closed), never skipped.
    """
    yaml = _require_yaml()
    with open(skill_md_path, "r", encoding="utf-8") as f:
        text = f.read()
    if not text.startswith("---"):
        return {}, None
    parts = re.split(r"^---[ \t]*$", text, maxsplit=2, flags=re.MULTILINE)
    if len(parts) < 3:
        return {}, "unterminated frontmatter block"
    try:
        data = yaml.safe_load(parts[1])
    except yaml.YAMLError as exc:
        return {}, f"invalid YAML frontmatter: {exc}"
    if not isinstance(data, dict):
        return {}, "frontmatter is not a mapping"
    return data, None


def _as_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"true", "yes", "1"}
    return None


def invocation_kind(frontmatter):
    """Return "manual_only", "agent_only", or None for a public skill."""
    if _as_bool(frontmatter.get("disable-model-invocation")) is True:
        return "manual_only"
    if _as_bool(frontmatter.get("user-invocable")) is False:
        return "agent_only"
    return None


def is_non_user_invocable(frontmatter):
    """True if the skill must NOT be implicitly invocable on Codex."""
    return invocation_kind(frontmatter) is not None


def openai_policy_ok(openai_yaml_path):
    """True if agents/openai.yaml sets policy.allow_implicit_invocation: false."""
    if not os.path.isfile(openai_yaml_path):
        return False, "missing agents/openai.yaml"
    yaml = _require_yaml()
    with open(openai_yaml_path, "r", encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            return False, f"agents/openai.yaml is invalid YAML: {exc}"
    if not isinstance(data, dict):
        return False, "agents/openai.yaml is not a mapping"
    policy = data.get("policy")
    if not isinstance(policy, dict):
        return False, "agents/openai.yaml has no policy block"
    if _as_bool(policy.get("allow_implicit_invocation")) is not False:
        return False, "policy.allow_implicit_invocation must be false"
    interface = data.get("interface")
    if interface is not None and not isinstance(interface, dict):
        return False, "agents/openai.yaml interface is not a mapping"
    if (interface or {}).get("default_prompt"):
        return False, "internal helpers must not define interface.default_prompt"
    return True, ""


def collect_errors(skills_dir):
    errors, kinds = collect_policy(skills_dir)
    return errors, sorted(kinds)


def collect_policy(skills_dir):
    """Return (errors, {skill: kind}) for every manual-only or agent-only skill."""
    errors = []
    kinds = {}
    for name in sorted(os.listdir(skills_dir)):
        skill_dir = os.path.join(skills_dir, name)
        skill_md = os.path.join(skill_dir, "SKILL.md")
        if not os.path.isfile(skill_md):
            continue
        frontmatter, fm_error = parse_frontmatter(skill_md)
        if fm_error is not None:
            # Fail closed: a SKILL.md we cannot parse might hide an invocation
            # restriction, so it is an error, not a skip.
            errors.append((name, f"SKILL.md frontmatter unreadable ({fm_error})"))
            continue
        kind = invocation_kind(frontmatter)
        if kind is None:
            continue
        kinds[name] = kind
        ok, reason = openai_policy_ok(os.path.join(skill_dir, "agents", "openai.yaml"))
        if not ok:
            errors.append((name, reason))
    return errors, kinds


def main():
    if "-h" in sys.argv[1:] or "--help" in sys.argv[1:]:
        print("validate_invocation_policy.py — check cross-host invocation policy for bundled skills")
        print("Usage: python3 validate_invocation_policy.py <path-to-skills-dir>")
        sys.exit(0)

    if len(sys.argv) < 2:
        print(
            "Usage: python3 validate_invocation_policy.py <path-to-skills-dir>",
            file=sys.stderr,
        )
        sys.exit(1)

    skills_dir = sys.argv[1]
    if not os.path.isdir(skills_dir):
        print(f"Error: skills dir not found: {skills_dir}", file=sys.stderr)
        sys.exit(1)

    errors, kinds = collect_policy(skills_dir)

    if errors:
        print("VALIDATION FAILED")
        print()
        print("Invocation-policy errors:")
        for name, reason in errors:
            print(f"  - {name}: {reason}")
    else:
        print("VALIDATION PASSED")

    manual = sorted(name for name, kind in kinds.items() if kind == "manual_only")
    agent = sorted(name for name, kind in kinds.items() if kind == "agent_only")
    print()
    print(f"Manual-only (no model invocation on any host): {', '.join(manual) or '(none)'}")
    print(f"Agent-only (Claude: model-invocable, hidden from the menu; Codex: "
          f"explicit or inline only): {', '.join(agent) or '(none)'}")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
