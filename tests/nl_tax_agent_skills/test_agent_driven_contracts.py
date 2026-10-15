#!/usr/bin/env python3
"""Regression coverage for the agent-driven conversational contracts."""

import importlib.util
import pathlib
import unittest


ROOT = (
    pathlib.Path(__file__).resolve().parents[2]
    / "plugins"
    / "nl-tax-agent-skills"
)


def load_validator():
    path = ROOT / "../../tools/nl_tax_agent_skills/field_mapper/validate_field_map.py"
    spec = importlib.util.spec_from_file_location("agent_driven_validator", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AgentDrivenContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = load_validator()

    def test_workflow_owns_chat_without_evidence_index_requirement(self):
        # 0.4 (R10): the evidence indexer is retired; the owning workflow reads
        # documents itself and pure chat collection needs no document at all.
        self.assertFalse((ROOT / "skills/nl-tax-evidence-indexer").exists())

    def test_agent_declared_draft_cannot_be_promoted(self):
        fields = [
            {
                "field_id": "box1.loon",
                "value": 50000,
                "source": {"type": "evidence", "evidence_id": "ev1"},
            },
            {
                "field_id": "box1.loonheffing",
                "value": 12000,
                "source": {"type": "evidence", "evidence_id": "ev2"},
            },
        ]
        result = self.validator._readiness_for(
            {
                "workflow": "annual_return",
                "tax_year": 2025,
                "readiness": "draft",
                "fields": fields,
                "missing_fields": [],
            }
        )
        self.assertTrue(result["structurally_ready"])
        self.assertFalse(result["ready"])
        self.assertEqual("draft", result["declared"])


if __name__ == "__main__":
    unittest.main()
