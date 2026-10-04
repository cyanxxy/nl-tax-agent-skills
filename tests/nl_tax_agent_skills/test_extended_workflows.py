"""Meaningful isolation and draft-ceiling regressions for preparation extensions."""

import copy
from decimal import Decimal
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


REPO = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "extended_workflow_tests", REPO / "tools/nl_tax_agent_skills/extended/validate_extended.py"
)
EXT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = EXT
SPEC.loader.exec_module(EXT)
PLUGIN = REPO / "plugins/nl-tax-agent-skills"


def load(relative, name):
    spec = importlib.util.spec_from_file_location(name, REPO / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


MAP = load("tools/nl_tax_agent_skills/field_mapper/validate_field_map.py", "extended_map_integration")
WORKPACK = load("tools/nl_tax_agent_skills/workpack/validate_workpack.py", "extended_workpack_integration")
SAMPLES = load("tests/nl_tax_agent_skills/workpack_samples.py", "extended_workpack_samples")


def workpack(kind, workflow, field_map=None, record_changes=None):
    identity = EXT.parse_resume_identity(workflow)
    SAMPLES.TEMPLATES[kind] = PLUGIN / EXT.SCOPES[kind]["template"]
    overrides = {key: value for key, value in identity.items() if key != "kind"}
    overrides.update(record_changes or {})
    text = SAMPLES.build_workpack(
        kind, workflow=workflow, sources=(), field_map=field_map,
        documents=(("ev_001", "chat 2026-10-02", "user_chat", str(identity["tax_year"]),
                    "taxpayer", "chat", "confirmed example administration figures", "extracted"),),
        record_overrides=overrides,
    )
    for key, value in identity.items():
        text = text.replace("{" + key + "}", str(value))
    return text.replace("{year}", str(identity["tax_year"])).replace("{form}", identity.get("return_form", ""))


def row(fid, value=100, dimensions=None, internal=False):
    result = {
        "field_id": fid, "label": fid, "value": value,
        "entry_mode": "internal_routing" if internal else "manual_entry",
        "source": {"type": "evidence", "evidence_id": "ev_001"},
        "confidence": 0.9, "manual_review_required": True, "notes": [],
    }
    if dimensions is not None:
        result["dimensions"] = dimensions
    return result


def data(kind="icp"):
    result = {
        "field_map_version": "1.1", "tax_year": 2026,
        "readiness": "draft", "check_performed_by": "checked_by_agent",
        "created_at": "2026-10-02T12:00:00Z", "updated_at": "2026-10-02T12:00:00Z",
        "missing_fields": [], "user_chat_values_index": [], "notes": [],
    }
    if kind == "icp":
        result.update(workflow="icp_declaration", period="Q3", fields=[row(
            "icp.row.customer_01.services_amount", dimensions={"member_state": "DE", "customer_alias": "customer_01"}
        )])
    elif kind == "oss":
        result.update(workflow="oss_return", scheme="union", period="Q3", fields=[row(
            "oss.row.group_01.vat_amount", dimensions={"scheme": "union", "member_state": "DE", "rate": 19}
        )])
    elif kind == "international":
        result.update(workflow="international_return", return_form="migration", fields=[row(
            "international.residence.departure_date", value="2026-03-14", internal=True
        )])
    else:
        result.update(workflow="annual_return", fields=[row(
            "annual2026.box1.wage", internal=True
        )])
    return result


class ExtendedIdentityTests(unittest.TestCase):
    def test_supported_identity_is_exact_and_scheme_specific(self):
        examples = {
            "annual_2026": {"kind": "annual_2026", "tax_year": 2026},
            "icp_2025_Y": {"kind": "icp", "tax_year": 2025, "period": "Y"},
            "oss_non_union_2026_Q3": {"kind": "oss", "tax_year": 2026, "scheme": "non_union", "period": "Q3"},
            "oss_ioss_2025_M01": {"kind": "oss", "tax_year": 2025, "scheme": "ioss", "period": "M01"},
            "international_2026_nonresident": {"kind": "international", "tax_year": 2026, "return_form": "nonresident"},
        }
        for workflow, expected in examples.items():
            with self.subTest(workflow=workflow):
                self.assertEqual(EXT.parse_resume_identity(workflow), expected)

    def test_resume_rejects_cross_scheme_period_and_normalization(self):
        for workflow in ("annual_2025", "icp_2027_Q1", "icp_2026_M1", "icp_2026_Q3 ",
                         "oss_union_2026_M09", "oss_ioss_2026_Q3", "oss_ioss_2026_Y",
                         "oss_non_union_2026_Q5", "international_2026_M", None, []):
            with self.subTest(workflow=workflow):
                self.assertIsNone(EXT.parse_resume_identity(workflow))

    def test_map_pair_rejects_boolean_float_and_cross_year(self):
        for tax_year in (True, False, 2026.0, "2026.0", 2027):
            candidate = data()
            candidate["tax_year"] = tax_year
            with self.subTest(tax_year=tax_year):
                self.assertIsNone(EXT.scope_for_map(candidate))
                self.assertTrue(EXT.validate_map(candidate))

    def test_ordinary_annual_2025_is_unaffected(self):
        candidate = data("annual")
        candidate.update(tax_year=2025, readiness="review_ready")
        self.assertIsNone(EXT.scope_for_map(candidate))
        self.assertEqual(EXT.validate_map(candidate), [])
        self.assertEqual(EXT.review_readiness_blockers(candidate, PLUGIN), [])

    def test_irrelevant_identity_keys_are_rejected(self):
        for kind, key, value in (("annual", "period", "Q3"), ("icp", "scheme", "union"),
                                 ("international", "period", "Q3"), ("oss", "return_form", "migration")):
            candidate = data(kind)
            candidate[key] = value
            with self.subTest(kind=kind, key=key):
                self.assertTrue(any("unexpected identity" in error for error in EXT.validate_map(candidate)))


class ExtendedMapBoundaryTests(unittest.TestCase):
    def test_all_new_scopes_accept_draft_and_reject_false_ready(self):
        for kind in ("icp", "oss", "international", "annual"):
            candidate = data(kind)
            with self.subTest(kind=kind):
                self.assertEqual(EXT.validate_map(candidate), [])
                candidate["readiness"] = "review_ready"
                self.assertTrue(any("remain draft" in error for error in EXT.validate_map(candidate)))

    def test_readiness_blocker_does_not_need_period_metadata(self):
        for workflow, tax_year in (("annual_return", 2026), ("icp_declaration", 2025),
                                   ("oss_return", 2026), ("international_return", 2025)):
            blockers = EXT.review_readiness_blockers({"workflow": workflow, "tax_year": tax_year}, PLUGIN)
            with self.subTest(workflow=workflow):
                self.assertTrue(blockers)
                self.assertIn("draft-only", blockers[0])

    def test_international_and_annual_do_not_invent_portal_boxes(self):
        for kind in ("international", "annual"):
            candidate = data(kind)
            candidate["fields"][0]["entry_mode"] = "manual_entry"
            with self.subTest(kind=kind):
                self.assertTrue(any("internal_routing" in error for error in EXT.validate_map(candidate)))

    def test_cross_workflow_ids_and_fake_calculated_boxes_are_rejected(self):
        for kind, fid in (("icp", "vat.3b.turnover"), ("oss", "oss.total.final_screen"),
                          ("international", "annual2026.box1.wage"), ("annual", "box3.bank")):
            candidate = data(kind)
            candidate["fields"][0]["field_id"] = fid
            candidate["missing_fields"] = [{"field_id": fid}]
            with self.subTest(kind=kind):
                errors = EXT.validate_map(candidate)
                self.assertTrue(any("unsupported field_id" in error for error in errors))
                self.assertTrue(any("unsupported missing field_id" in error for error in errors))

    def test_duplicate_rows_cannot_count_twice(self):
        candidate = data()
        candidate["fields"].append(copy.deepcopy(candidate["fields"][0]))
        self.assertTrue(any("duplicate" in error for error in EXT.validate_map(candidate)))

    def test_numeric_strings_boolean_nonfinite_and_fractional_cents_are_rejected(self):
        for value in ("100", True, float("nan"), float("inf"), Decimal("0.001")):
            candidate = data("oss")
            candidate["fields"][0]["value"] = value
            with self.subTest(value=value):
                self.assertTrue(EXT.validate_map(candidate))
        candidate["fields"][0]["value"] = Decimal("12.3400")
        self.assertEqual(EXT.validate_map(candidate), [])

    def test_large_finite_decimal_does_not_crash_precision_check(self):
        candidate = data()
        candidate["fields"][0]["value"] = Decimal("1E+999999")
        self.assertEqual(EXT.validate_map(candidate), [])

    def test_icp_alias_is_not_actual_id_verification_and_xi_services_fail(self):
        candidate = data()
        dimensions = candidate["fields"][0]["dimensions"]
        dimensions.update(human_vat_id_verified="customer_01")
        self.assertTrue(any("Boolean" in error for error in EXT.validate_map(candidate)))
        dimensions.update(human_vat_id_verified=True, human_vat_id_verified_at="2026-02-30")
        self.assertTrue(any("dated human" in error for error in EXT.validate_map(candidate)))
        dimensions.update(human_vat_id_verified_at="2026-10-02", member_state="XI")
        self.assertTrue(any("Northern Ireland" in error for error in EXT.validate_map(candidate)))
        candidate["fields"][0]["field_id"] = "icp.row.customer_01.goods_amount"
        self.assertEqual(EXT.validate_map(candidate), [])

    def test_sensitive_identifier_dimension_is_rejected(self):
        candidate = data()
        candidate["fields"][0]["dimensions"]["customer_vat_id"] = "human-retained"
        self.assertTrue(any("identifiers" in error for error in EXT.validate_map(candidate)))

    def test_oss_scheme_and_rate_must_be_dimensions_not_country_guesses(self):
        for change in ({"scheme": "ioss"}, {"rate": None}, {"rate": "19"}, {"rate": True},
                       {"rate": 0}, {"rate": 101}, {"member_state": "germany"}):
            candidate = data("oss")
            candidate["fields"][0]["dimensions"].update(change)
            with self.subTest(change=change):
                self.assertTrue(EXT.validate_map(candidate))

    def test_negative_current_oss_requires_original_period_correction(self):
        candidate = data("oss")
        candidate["fields"][0]["value"] = -50
        self.assertTrue(any("cannot be negative" in error for error in EXT.validate_map(candidate)))
        candidate["fields"][0]["dimensions"]["original_period"] = "2026_Q2"
        candidate["fields"][0]["dimensions"].pop("rate")
        self.assertEqual(EXT.validate_map(candidate), [])

    def test_oss_correction_cannot_be_current_base_or_wrong_period(self):
        candidate = data("oss")
        dimensions = candidate["fields"][0]["dimensions"]
        for period in ("2026_Q3", "2026_Q4", "2027_Q1", "2026_M02", "Q2"):
            dimensions["original_period"] = period
            with self.subTest(period=period):
                self.assertTrue(any("original_period" in error for error in EXT.validate_map(candidate)))
        dimensions["original_period"] = "2026_Q2"
        candidate["fields"][0]["field_id"] = "oss.row.credit_01.taxable_base"
        self.assertTrue(any("signed VAT delta" in error for error in EXT.validate_map(candidate)))

    def test_icp_frequency_change_correction_uses_nonoverlapping_coverage(self):
        candidate = data()
        candidate["period"] = "M07"
        candidate["fields"][0]["dimensions"]["original_period"] = "2026_Q1"
        self.assertEqual(EXT.validate_map(candidate), [])
        candidate["fields"][0]["dimensions"]["original_period"] = "2026_Q3"
        self.assertTrue(any("non-overlapping" in error for error in EXT.validate_map(candidate)))

    def test_historical_correction_metadata_does_not_create_old_return_scope(self):
        candidate = data("oss")
        dimensions = candidate["fields"][0]["dimensions"]
        dimensions["original_period"] = "2024_Q4"
        self.assertEqual(EXT.validate_map(candidate), [])
        # 2021 Q3 was due 31 October 2021, so its window closed on 31 October
        # 2024; a 2026 Q3 return is provably outside it.
        dimensions["original_period"] = "2021_Q3"
        self.assertTrue(any("three-year correction window" in error for error in EXT.validate_map(candidate)))
        dimensions["original_period"] = "2021_Q2"
        errors = EXT.validate_map(candidate)
        self.assertTrue(any("OSS starts July 2021" in error for error in errors))
        self.assertFalse(any("three-year correction window" in error for error in errors))
        candidate.update(scheme="ioss", period="M09")
        dimensions.update(scheme="ioss", original_period="2021_M07")
        self.assertTrue(any("three-year correction window" in error for error in EXT.validate_map(candidate)))
        dimensions["original_period"] = "2021_M06"
        self.assertTrue(any("OSS starts July 2021" in error for error in EXT.validate_map(candidate)))
        candidate = data("icp")
        candidate["fields"][0]["dimensions"]["original_period"] = "2024_Y"
        self.assertEqual(EXT.validate_map(candidate), [])
        self.assertIsNone(EXT.parse_resume_identity("icp_2024_Y"))
        self.assertIsNone(EXT.parse_resume_identity("oss_union_2024_Q4"))

    def test_oss_window_runs_from_original_due_date_not_filing_date(self):
        candidate = data("oss")
        candidate.update(tax_year=2025, period="Q2")
        dimensions = candidate["fields"][0]["dimensions"]
        # 2022 Q3 was due 31 October 2022; the window ends 31 October 2025,
        # after the 2025 Q2 period end, so the correction can still be in time.
        dimensions["original_period"] = "2022_Q3"
        self.assertEqual(EXT.validate_map(candidate), [])
        # 2022 Q1 was due 30 April 2022; the window closed 30 April 2025, before
        # the 2026 Q3 period ends.
        candidate.update(tax_year=2026, period="Q3")
        dimensions["original_period"] = "2022_Q1"
        self.assertTrue(any("three-year correction window" in error for error in EXT.validate_map(candidate)))
        # IOSS January 2023 was due 28 February 2023; the window ends
        # 28 February 2026, the same day the 2026 M02 period ends. That return
        # can be filed at the earliest on 1 March 2026, so it is provably late.
        candidate.update(scheme="ioss", period="M02", tax_year=2026)
        dimensions.update(scheme="ioss", original_period="2023_M01")
        self.assertTrue(any("three-year correction window" in error for error in EXT.validate_map(candidate)))
        # One month earlier (2026 M01 ends 31 January 2026) can still be in time.
        candidate.update(period="M01")
        self.assertFalse(any("three-year correction window" in error for error in EXT.validate_map(candidate)))

    def test_oss_window_handles_29_february_due_date(self):
        from datetime import date
        # IOSS January 2024 was due 29 February 2024; 2027 has no 29 February.
        self.assertEqual(EXT._oss_correction_window_end(date(2024, 1, 31)), date(2027, 2, 28))
        self.assertEqual(EXT._oss_correction_window_end(date(2025, 12, 31)), date(2029, 1, 31))

    def test_non_ascii_digits_are_not_normalized(self):
        self.assertIsNone(EXT._year("\uff12\uff10\uff12\uff16"))
        self.assertFalse(EXT._valid_iso_date("\uff12\uff10\uff12\uff16-10-02"))
        candidate = data("oss")
        candidate["tax_year"] = "\uff12\uff10\uff12\uff16"
        self.assertIsNone(EXT.scope_for_map(candidate))

    def test_icp_rows_require_customer_alias_and_wrong_id_pair_is_traceable(self):
        candidate = data()
        candidate["fields"][0]["dimensions"].pop("customer_alias")
        self.assertTrue(any("customer_alias" in error for error in EXT.validate_map(candidate)))
        candidate["fields"][0]["dimensions"]["customer_alias"] = "NL123456789B01"
        self.assertTrue(any("customer_alias" in error for error in EXT.validate_map(candidate)))
        # A lowercased VAT ID is still an identifier, in the dimension or in the
        # field-id alias segment.
        for identifier in ("de123456789", "nl123456789b01", "ie1234567wa", "atu12345678"):
            with self.subTest(identifier=identifier):
                candidate = data()
                candidate["fields"][0]["dimensions"]["customer_alias"] = identifier
                self.assertTrue(any("never an identifier" in error for error in EXT.validate_map(candidate)))
                candidate = data()
                candidate["fields"][0]["field_id"] = f"icp.row.{identifier}.services_amount"
                self.assertTrue(any("never an identifier" in error for error in EXT.validate_map(candidate)))
        candidate = data()
        candidate["fields"][0]["dimensions"]["customer_alias"] = "customer_01"
        self.assertEqual(EXT.validate_map(candidate), [])
        candidate = data()
        candidate["fields"] += [
            row("icp.row.corr_old_01.services_amount", -100,
                {"member_state": "DE", "customer_alias": "customer_01", "original_period": "2026_Q2"}),
            row("icp.row.corr_new_01.services_amount", 100,
                {"member_state": "DE", "customer_alias": "customer_02", "original_period": "2026_Q2"}),
        ]
        self.assertEqual(EXT.validate_map(candidate), [])

    def test_oss_xi_is_union_goods_only(self):
        candidate = data("oss")
        candidate["fields"] = [row("oss.row.ni_goods.vat_amount", 20, {
            "scheme": "union", "member_state": "XI", "rate": 20, "supply_kind": "goods"})]
        candidate["fields"] += [row(fid, value=value, internal=True) for fid, value in {
            "oss.total.xi.current_vat": 20, "oss.total.xi.corrections": 0, "oss.total.xi.balance": 20,
            "oss.total.xi.payable": 20, "oss.total.xi.refund": 0,
            "oss.total.payable": 20, "oss.total.refund": 0,
        }.items()]
        self.assertEqual(EXT.validate_map(candidate), [])
        candidate["fields"][0]["dimensions"]["supply_kind"] = "services"
        errors = EXT.validate_map(candidate)
        self.assertTrue(any("Union-scheme goods" in error for error in errors))
        self.assertTrue(any("oss.total.xi: unsupported" in error for error in errors))
        candidate["fields"][0]["dimensions"].update(supply_kind="goods", scheme="ioss")
        candidate.update(scheme="ioss", period="M09")
        self.assertTrue(any("Union-scheme goods" in error for error in EXT.validate_map(candidate)))

    def test_malformed_container_shapes_do_not_crash(self):
        for value in (None, [], "draft"):
            self.assertTrue(EXT.validate_map(value))
        for kind, key, value in (("oss", "scheme", []), ("international", "return_form", []),
                                 ("icp", "fields", {}), ("oss", "missing_fields", {})):
            candidate = data(kind)
            candidate[key] = value
            with self.subTest(kind=kind, key=key):
                self.assertTrue(EXT.validate_map(candidate))

    def test_country_refund_never_offsets_another_country_payable(self):
        candidate = data("oss")
        candidate["fields"] += [
            row("oss.row.corr_de.vat_amount", -150, {"scheme": "union", "member_state": "DE", "original_period": "2026_Q2"}),
            row("oss.row.group_be.vat_amount", 100, {"scheme": "union", "member_state": "BE", "rate": 21}),
        ]
        candidate["fields"] += [row(fid, value=value, internal=True) for fid, value in {
            "oss.total.de.current_vat": 100, "oss.total.de.corrections": -150,
            "oss.total.de.balance": -50, "oss.total.de.payable": 0, "oss.total.de.refund": 50,
            "oss.total.be.current_vat": 100, "oss.total.be.corrections": 0,
            "oss.total.be.balance": 100, "oss.total.be.payable": 100, "oss.total.be.refund": 0,
            "oss.total.payable": 100, "oss.total.refund": 50,
        }.items()]
        self.assertEqual(EXT.validate_map(candidate), [])
        next(field for field in candidate["fields"] if field["field_id"] == "oss.total.payable")["value"] = 50
        self.assertTrue(any("remain separate" in error for error in EXT.validate_map(candidate)))
        next(field for field in candidate["fields"] if field["field_id"] == "oss.total.payable")["entry_mode"] = "manual_entry"
        self.assertTrue(any("never a portal entry" in error for error in EXT.validate_map(candidate)))

    def test_country_totals_must_tie_to_that_countrys_rows(self):
        def build(totals):
            candidate = data("oss")
            candidate["fields"][0]["value"] = 190
            candidate["fields"] += [
                row("oss.row.group_be.vat_amount", 210, {"scheme": "union", "member_state": "BE", "rate": 21}),
                row("oss.row.corr_de.vat_amount", -240, {"scheme": "union", "member_state": "DE", "original_period": "2024_Q4"}),
            ]
            candidate["fields"] += [row(fid, value=value, internal=True) for fid, value in totals.items()]
            return candidate
        correct = {
            "oss.total.de.current_vat": 190, "oss.total.de.corrections": -240, "oss.total.de.balance": -50,
            "oss.total.de.payable": 0, "oss.total.de.refund": 50,
            "oss.total.be.current_vat": 210, "oss.total.be.corrections": 0, "oss.total.be.balance": 210,
            "oss.total.be.payable": 210, "oss.total.be.refund": 0,
            "oss.total.payable": 210, "oss.total.refund": 50,
        }
        self.assertEqual(EXT.validate_map(build(correct)), [])
        errors, _ = MAP.validate(build(correct))
        self.assertEqual(errors, [])
        # The German correction booked under Belgium offsets Belgium's payable.
        offset = dict(correct)
        offset.update({"oss.total.de.corrections": 0, "oss.total.de.balance": 190, "oss.total.de.payable": 190,
                       "oss.total.de.refund": 0, "oss.total.be.corrections": -240, "oss.total.be.balance": -30,
                       "oss.total.be.payable": 0, "oss.total.be.refund": 30,
                       "oss.total.payable": 190, "oss.total.refund": 30})
        errors = EXT.validate_map(build(offset))
        self.assertTrue(any("oss.total.de.corrections must equal" in error for error in errors))
        self.assertTrue(any("oss.total.be.corrections must equal" in error for error in errors))
        errors, _ = MAP.validate(build(offset))
        self.assertTrue(errors)
        misstated = dict(correct)
        misstated.update({"oss.total.de.current_vat": 999, "oss.total.de.balance": 759,
                          "oss.total.de.payable": 759, "oss.total.de.refund": 0,
                          "oss.total.payable": 969, "oss.total.refund": 0})
        self.assertTrue(any("oss.total.de.current_vat must equal" in error for error in EXT.validate_map(build(misstated))))

    def test_country_with_rows_needs_its_own_totals(self):
        # A Belgian row without Belgian totals would drop out of the overall payable.
        candidate = data("oss")
        candidate["fields"][0]["value"] = 190
        candidate["fields"] += [row("oss.row.group_be.vat_amount", 210, {"scheme": "union", "member_state": "BE", "rate": 21})]
        candidate["fields"] += [row(fid, value=value, internal=True) for fid, value in {
            "oss.total.de.current_vat": 190, "oss.total.de.corrections": 0, "oss.total.de.balance": 190,
            "oss.total.de.payable": 190, "oss.total.de.refund": 0, "oss.total.payable": 190,
        }.items()]
        errors = EXT.validate_map(candidate)
        self.assertTrue(any("oss.total.be.current_vat missing" in error for error in errors))
        errors, _ = MAP.validate(candidate)
        self.assertTrue(errors)
        # A German correction with the German corrections total omitted.
        candidate = data("oss")
        candidate["fields"][0]["value"] = 190
        candidate["fields"] += [row("oss.row.corr_de.vat_amount", -240, {"scheme": "union", "member_state": "DE", "original_period": "2024_Q4"})]
        candidate["fields"] += [row(fid, value=value, internal=True) for fid, value in {
            "oss.total.de.current_vat": 190, "oss.total.de.balance": 190,
            "oss.total.de.payable": 190, "oss.total.payable": 190,
        }.items()]
        self.assertTrue(any("oss.total.de.corrections missing" in error for error in EXT.validate_map(candidate)))
        # A draft with rows and no totals at all is left to the owner.
        candidate = data("oss")
        self.assertEqual(EXT.validate_map(candidate), [])

    def test_country_totals_skip_row_tie_while_a_row_amount_is_open(self):
        candidate = data("oss")
        candidate["fields"][0]["value"] = None
        candidate["fields"] += [row(fid, value=value, internal=True) for fid, value in {
            "oss.total.de.current_vat": 5000, "oss.total.de.corrections": 0, "oss.total.de.balance": 5000,
        }.items()]
        self.assertEqual(EXT.validate_map(candidate), [])
        candidate["fields"][0]["value"] = 100
        self.assertTrue(any("current_vat must equal" in error for error in EXT.validate_map(candidate)))


class ExtendedIntegrationTests(unittest.TestCase):
    IDENTITIES = (
        ("annual_2026", "annual_2026", "annual"),
        ("icp", "icp_2026_Q3", "icp"),
        ("oss", "oss_union_2026_Q3", "oss"),
        ("international", "international_2026_migration", "international"),
    )

    def test_shared_field_mapper_accepts_draft_and_rejects_ready_extensions(self):
        for kind in ("icp", "oss", "international", "annual"):
            candidate = data(kind)
            with self.subTest(kind=kind):
                errors, _ = MAP.validate(candidate)
                self.assertEqual(errors, [])
                candidate["readiness"] = "review_ready"
                errors, _ = MAP.validate(candidate)
                self.assertTrue(errors)

    def test_workpack_identity_path_title_and_section_keys_are_isolated(self):
        for kind, workflow, _ in self.IDENTITIES:
            identity = EXT.parse_resume_identity(workflow)
            scope = EXT.SCOPES[kind]
            path = scope["path"].format(year=identity["tax_year"], **{key: identity[key] for key in scope["identity_keys"]})
            title = WORKPACK.parse_markdown(workpack(kind, workflow)).title
            with self.subTest(kind=kind):
                self.assertEqual(WORKPACK.kind_for_workflow(workflow), kind)
                self.assertEqual(WORKPACK.kind_for_path(path), kind)
                self.assertEqual(WORKPACK.kind_for_title(title), kind)
                required, optional = WORKPACK.expected_section_keys(str(PLUGIN), workflow)
                self.assertEqual(required, frozenset(scope["sections"]))
                self.assertEqual(optional, frozenset())
        self.assertEqual(WORKPACK.kind_for_workflow("provisional_2026_request"), "provisional")
        self.assertEqual(WORKPACK.kind_for_path("workspace/nl-tax-annual-2026-workpack.md"), "annual_2026")

    def test_real_templates_produce_valid_partial_drafts_with_maps(self):
        for kind, workflow, map_kind in self.IDENTITIES:
            with self.subTest(kind=kind):
                report = WORKPACK.validate_workpack_text(workpack(kind, workflow, data(map_kind)), expect_saved=True)
                self.assertEqual(report.kind, kind)
                self.assertEqual(report.errors, [])

    def test_map_scheme_period_year_and_form_must_match_resume_record(self):
        cases = (("oss", "oss_union_2026_Q3", "oss", "scheme", "ioss"),
                 ("icp", "icp_2026_Q3", "icp", "period", "Q2"),
                 ("international", "international_2026_migration", "international", "return_form", "nonresident"),
                 ("annual_2026", "annual_2026", "annual", "tax_year", 2025))
        for kind, workflow, map_kind, key, wrong in cases:
            candidate = data(map_kind)
            candidate[key] = wrong
            with self.subTest(kind=kind, key=key):
                report = WORKPACK.validate_workpack_text(workpack(kind, workflow, candidate))
                self.assertTrue(report.errors)
                self.assertTrue(any("match" in error or "tax_year" in error for error in report.errors))

    def test_filename_rejects_other_scheme_period_and_form(self):
        for kind, workflow, filename in (("icp", "icp_2026_Q3", "nl-tax-icp-2026-Q2-workpack.md"),
                                        ("oss", "oss_union_2026_Q3", "nl-tax-oss-ioss-2026-M09-workpack.md"),
                                        ("international", "international_2026_migration", "nl-tax-international-2026-nonresident-workpack.md")):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / filename
                path.write_text(workpack(kind, workflow), encoding="utf-8")
                report = WORKPACK.validate_workpack_file(path)
                self.assertTrue(any("filename" in error for error in report.errors))

    def test_appendix_cannot_switch_scheme_or_return_form(self):
        for kind, workflow, changes in (("oss", "oss_union_2026_Q3", {"scheme": "non_union"}),
                                        ("international", "international_2026_migration", {"return_form": "nonresident"})):
            with self.subTest(kind=kind):
                report = WORKPACK.validate_workpack_text(workpack(kind, workflow, record_changes=changes))
                self.assertTrue(any("must match its workflow" in error for error in report.errors))


class ChatSourceYearTests(unittest.TestCase):
    IDENTITIES = (
        ("vat", "vat_{year}_Q3"),
        ("vat_correction", "vat_correction_{year}_Q3"),
        ("icp", "icp_{year}_Q3"),
        ("oss", "oss_union_{year}_Q3"),
        ("international", "international_{year}_nonresident"),
    )
    REGISTER = {
        f"bd_test_{year}": {"workflow": "all", "tax_year": year}
        for year in (2025, 2026)
    }

    def chat_workpack(self, kind, workflow, source_id):
        if kind in {"vat", "vat_correction"}:
            text = SAMPLES.build_workpack(kind, workflow=workflow, sources=())
        else:
            text = workpack(kind, workflow)
        text = SAMPLES.replace_section(text, "Sources used", "- " + source_id)
        for heading in ("Appendix A — Resume record", "Appendix B — Field map", "Manual-entry checklist"):
            text = SAMPLES.remove_section(text, heading)
        return SAMPLES.strip_fill_notes(text)

    def test_chat_accepts_sources_for_the_displayed_year(self):
        with patch.object(WORKPACK, "source_register", return_value=self.REGISTER):
            for kind, identity in self.IDENTITIES:
                for year in (2025, 2026):
                    with self.subTest(kind=kind, year=year):
                        text = self.chat_workpack(kind, identity.format(year=year), f"bd_test_{year}")
                        report = WORKPACK.validate_workpack_text(text, expected_kind=kind, presentation="chat")
                        self.assertEqual(report.errors, [])

    def test_chat_rejects_sources_from_the_other_supported_year(self):
        with patch.object(WORKPACK, "source_register", return_value=self.REGISTER):
            for kind, identity in self.IDENTITIES:
                for year, other_year in ((2025, 2026), (2026, 2025)):
                    with self.subTest(kind=kind, year=year):
                        source_id = f"bd_test_{other_year}"
                        text = self.chat_workpack(kind, identity.format(year=year), source_id)
                        report = WORKPACK.validate_workpack_text(text, expected_kind=kind, presentation="chat")
                        self.assertEqual(report.errors, [
                            f"{kind} workpack lists {source_id}, a source from another tax year"
                        ])


class StagedSourceDependencyTests(unittest.TestCase):
    def test_an_active_owner_cannot_silently_omit_a_staged_required_source(self):
        validator = load(
            "tools/nl_tax_agent_skills/source_maintenance/scripts/validate_supported_workflows.py",
            "extended_source_dependency_test",
        )
        base = {"id": "reviewed_base", "workflow_family": "vat",
                "mandatory_for": ["nl-tax-vat-return"]}
        pending = {"id": "pending_adjustment", "workflow_family": "vat",
                   "content_stage": "draft_only", "mandatory_for": ["nl-tax-vat-return"]}
        workflow = {"workflow": "vat_return", "tax_year": 2026, "status": "active",
                    "required_source_ids": ["reviewed_base"]}
        errors = validator.validate_required_sources(
            workflow, "future_vat", "vat_return", 2026,
            {"reviewed_base": base, "pending_adjustment": pending}, str(PLUGIN),
        )
        self.assertTrue(any("missing mandatory source_id: pending_adjustment" in error for error in errors), errors)
        workflow["required_source_ids"].append("pending_adjustment")
        errors = validator.validate_required_sources(
            workflow, "future_vat", "vat_return", 2026,
            {"reviewed_base": base, "pending_adjustment": pending}, str(PLUGIN),
        )
        self.assertTrue(any("active workflow cannot use draft-only source_id" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
