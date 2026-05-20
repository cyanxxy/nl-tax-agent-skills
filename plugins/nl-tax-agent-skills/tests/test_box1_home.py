#!/usr/bin/env python3
"""Regression tests for deterministic Box 1 / own-home helper behavior."""

import importlib.util
import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_module(relative_path, name):
    module_path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class Box1OwnHomeTests(unittest.TestCase):
    def test_hillenregeling_matches_official_2025_example(self):
        module = load_module(
            "skills/nl-tax-box1-home/scripts/validate_own_home_inputs.py",
            "validate_own_home_inputs_hillen",
        )

        applies, correction, remaining = module.calculate_hillenregeling(
            eigenwoningforfait=1_200,
            mortgage_interest=1_000,
            tax_year=2025,
        )

        self.assertTrue(applies)
        self.assertEqual(correction, 154)
        self.assertAlmostEqual(remaining, 0.76667)


if __name__ == "__main__":
    unittest.main()
