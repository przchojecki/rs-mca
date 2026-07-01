#!/usr/bin/env python3
"""Verify the F_17^32 M3 regular-window status ledger.

This is an audit ledger for the Paper D v9 M3 work.  It combines the existing
regular-window plan, generic all-row-set nonsingularity certificate, synthetic
rank-witness families, and fixed top-window v9 packet into one compact status
object.  It deliberately does not claim an actual-row MCA bound.
"""

from __future__ import annotations

import argparse
import json
from hashlib import sha256
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_VERSION = "f17-32-m3-regular-window-status-v1"
AGREEMENT_MIN = 385
AGREEMENT_MAX = 426
TOP_WINDOW_MIN = 421
TOP_WINDOW_MAX = 426
ROOT_UNION = [0]
TWO128 = 2**128

PLAN_REF = (
    "experimental/data/certificates/hankel-regular-window-f17-385-426/"
    "f17_32_n512_k256_regular_window_plan.json"
)
GENERIC_REF = (
    "experimental/data/certificates/hankel-f17-32-generic-regular-minor/"
    "f17_32_n512_k256_m3_generic_all_row_set_regular_minor_certificate.json"
)
FAMILY_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank-witness-family/"
    "f17_32_n512_k256_m3_rank_witness_family_certificate.json"
)
LOW_RANK_FAMILY_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank2-family/"
    "f17_32_n512_k256_m3_low_rank2_family_certificate.json"
)
TOP_PACKET_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-fixed-top-window/"
    "f17_32_n512_k256_a421_426_fixed_prefix92_packet.json"
)
LINE_VALUE_LIFT_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-line-value-lift/"
    "f17_32_n512_k256_a421_426_fixed_prefix92_line_values.json"
)
SUBGROUP_SECTION_REF = (
    "experimental/data/certificates/subgroup-syndrome-section/"
    "subgroup_syndrome_section_certificate.json"
)
SYNDROME_REALIZABILITY_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-syndrome-realizability/"
    "f17_32_n512_k256_m3_syndrome_realizability_certificate.json"
)
ZERO_SLOPE_SUBTRACTION_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-zero-slope-subtraction/"
    "f17_32_n512_k256_a421_426_zero_slope_subtraction.json"
)
EXTENSION_DENOMINATOR_AUDIT_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-extension-denominator-audit/"
    "f17_32_n512_k256_a421_426_extension_denominator_audit.json"
)
PROJECTIVE_ENDPOINT_AUDIT_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-projective-endpoint-audit/"
    "f17_32_n512_k256_a421_426_projective_endpoint_audit.json"
)
PROPORTIONAL_LEMMA_REF = (
    "experimental/data/certificates/hankel-proportional-pencil-tangent-lemma/"
    "hankel_proportional_pencil_tangent_lemma_certificate.json"
)
OUTPUT_PATH = ROOT / (
    "experimental/data/certificates/hankel-f17-32-m3-regular-window-status/"
    "f17_32_n512_k256_m3_regular_window_status.json"
)


def load_json(ref: str) -> dict[str, Any]:
    return json.loads((ROOT / ref).read_text(encoding="utf-8"))


def sha256_file(ref: str) -> str:
    return sha256((ROOT / ref).read_bytes()).hexdigest()


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def artifact_record(name: str, ref: str, schema_version: str) -> dict[str, Any]:
    data = load_json(ref)
    require(data.get("schema_version") == schema_version, f"{name}: schema mismatch")
    return {
        "name": name,
        "ref": ref,
        "schema_version": schema_version,
        "sha256": sha256_file(ref),
        "status": data.get("status"),
    }


def top_window_by_agreement(packet: dict[str, Any]) -> dict[int, dict[str, Any]]:
    return {int(item["A"]): item for item in packet["exact_agreements"]}


def validate_inputs(
    plan: dict[str, Any],
    generic: dict[str, Any],
    family: dict[str, Any],
    low_rank_family: dict[str, Any],
    top_packet: dict[str, Any],
    line_value_lift: dict[str, Any],
    subgroup_section: dict[str, Any],
    syndrome_realizability: dict[str, Any],
    zero_slope_subtraction: dict[str, Any],
    extension_denominator_audit: dict[str, Any],
    projective_endpoint_audit: dict[str, Any],
    proportional_lemma: dict[str, Any],
) -> None:
    require(plan["window"]["A_min"] == AGREEMENT_MIN, "plan A_min mismatch")
    require(plan["window"]["A_max"] == AGREEMENT_MAX, "plan A_max mismatch")
    require(plan["budget_context"]["degree_bound_sum"] == 4515, "bad degree sum")
    require(generic["claim"]["degree_sum"] == 4515, "generic degree sum mismatch")
    require(
        generic["claim"]["regular_window"] == {"A_min": AGREEMENT_MIN, "A_max": AGREEMENT_MAX},
        "generic window mismatch",
    )
    require(len(generic["agreements"]) == 42, "generic agreement count mismatch")
    require(len(family["agreements"]) == 42, "family agreement count mismatch")
    require(
        family["claim"]["closed_form_root_union"] == ROOT_UNION,
        "family root union mismatch",
    )
    require(
        low_rank_family["schema_version"] == "f17-32-m3-low-rank2-family-v4",
        "low-rank family schema mismatch",
    )
    require(
        low_rank_family["endpoint_conventions"]["finite_budget_numerator"]
        == 17**32 // TWO128,
        "low-rank family finite budget mismatch",
    )
    require(
        low_rank_family["endpoint_conventions"]["projective_budget_numerator"]
        == (17**32 + 1) // TWO128,
        "low-rank family projective budget mismatch",
    )
    require(
        low_rank_family["agreement_range"] == [AGREEMENT_MIN, AGREEMENT_MAX],
        "low-rank family window mismatch",
    )
    require(
        low_rank_family["aggregate"]["agreement_count"] == 42,
        "low-rank family agreement count mismatch",
    )
    require(
        low_rank_family["aggregate"]["per_agreement_degree_bound"] == 2,
        "low-rank family per-agreement bound mismatch",
    )
    require(
        low_rank_family["aggregate"]["degree_bound_sum"] == 84,
        "low-rank family degree-bound aggregate mismatch",
    )
    require(
        low_rank_family["aggregate"]["exact_regular_root_count_sum"] == 40,
        "low-rank family exact-root aggregate mismatch",
    )
    require(
        low_rank_family["aggregate"]["split_quadratic_rows"] == 20
        and low_rank_family["aggregate"]["nonsquare_quadratic_rows"] == 22,
        "low-rank family split/nonsquare count mismatch",
    )
    require(
        low_rank_family["aggregate"]["projective_infinity_contribution_sum"] == 0,
        "low-rank family projective contribution mismatch",
    )
    require(
        low_rank_family["aggregate"]["common_code_line_tangent_overlap_sum"] == 0,
        "low-rank family tangent overlap mismatch",
    )
    require(
        low_rank_family["aggregate"]["finite_roots_checked_for_common_code_line"]
        == low_rank_family["aggregate"]["exact_regular_root_count_sum"],
        "low-rank family tangent check coverage mismatch",
    )
    require(
        low_rank_family["aggregate"]["exact_regular_roots_after_common_code_line"]
        == 40,
        "low-rank family post-tangent root count mismatch",
    )
    require(
        low_rank_family["aggregate"]["max_projective_regular_roots_per_agreement"]
        == 2,
        "low-rank family max projective roots mismatch",
    )
    require(
        low_rank_family["aggregate"]["all_rows_within_finite_budget"] is True
        and low_rank_family["aggregate"]["all_rows_within_projective_budget"] is True,
        "low-rank family budget status mismatch",
    )
    require(
        low_rank_family["aggregate"]["generic_degree_bound_sum_for_window"]
        == plan["budget_context"]["degree_bound_sum"],
        "low-rank family generic degree sum mismatch",
    )
    require(
        len(low_rank_family["records"]) == 42,
        "low-rank family record count mismatch",
    )
    require(
        low_rank_family["endpoint_crosscheck"]["agreement"] == AGREEMENT_MAX
        and low_rank_family["endpoint_crosscheck"]["coefficients_match"] is True
        and low_rank_family["endpoint_crosscheck"]["sidecar_match"] is True,
        "low-rank family endpoint cross-check mismatch",
    )
    require(
        low_rank_family["endpoint_crosscheck"]["roots_match"] is True
        and low_rank_family["endpoint_crosscheck"]["root_certificate_match"] is True
        and low_rank_family["endpoint_crosscheck"][
            "quadratic_certificate_match"
        ]
        is True,
        "low-rank family endpoint root cross-check mismatch",
    )
    require(
        top_packet["exact_agreements"][0]["A"] == TOP_WINDOW_MIN
        and top_packet["exact_agreements"][-1]["A"] == TOP_WINDOW_MAX,
        "top-window packet range mismatch",
    )
    require(top_packet["root_union"] == ROOT_UNION, "top-window root union mismatch")
    require(
        top_packet["declared_aperiodic_numerator"] == 1,
        "top-window numerator mismatch",
    )
    require(
        line_value_lift["source_packet"]["fixed_top_window_input_ref"]
        == top_packet["extractor"]["input_ref"],
        "line-value lift input ref mismatch",
    )
    require(
        line_value_lift["source_packet"]["fixed_top_window_packet_ref"] == TOP_PACKET_REF,
        "line-value lift packet ref mismatch",
    )
    require(
        line_value_lift["syndrome_replay"]["matches_fixed_top_window_input"] is True,
        "line-value lift does not replay the fixed input",
    )
    section_cases = {case["name"]: case for case in subgroup_section["cases"]}
    require(
        "F17_32_H512_fixed_top_window" in section_cases,
        "subgroup section lacks the F17^32 fixed top-window case",
    )
    require(
        section_cases["F17_32_H512_fixed_top_window"]["line_value_lift_ref"]
        == LINE_VALUE_LIFT_REF,
        "subgroup section does not reference the line-value lift",
    )
    require(
        syndrome_realizability["schema_version"]
        == "f17-32-m3-syndrome-realizability-v1",
        "syndrome realizability schema mismatch",
    )
    require(
        syndrome_realizability["source_artifacts"]["subgroup_syndrome_section"]["ref"]
        == SUBGROUP_SECTION_REF,
        "syndrome realizability subgroup-section ref mismatch",
    )
    require(
        syndrome_realizability["row"]["domain_hash"] == plan["row"]["domain_hash"],
        "syndrome realizability domain mismatch",
    )
    require(
        syndrome_realizability["summary"]["regular_window"]
        == {"A_min": AGREEMENT_MIN, "A_max": AGREEMENT_MAX},
        "syndrome realizability window mismatch",
    )
    require(
        syndrome_realizability["summary"]["visible_syndrome_length"] == 256,
        "syndrome realizability length mismatch",
    )
    require(
        syndrome_realizability["summary"]["pencil_realizability"]
        == "surjective onto all length-256 u,v syndrome pencils",
        "syndrome realizability summary mismatch",
    )
    require(
        len(syndrome_realizability["per_agreement"]) == 42,
        "syndrome realizability agreement count mismatch",
    )
    require(
        zero_slope_subtraction["schema_version"]
        == "f17-32-m3-zero-slope-subtraction-v1",
        "zero-slope subtraction schema mismatch",
    )
    require(
        zero_slope_subtraction["source_artifacts"]["fixed_top_window_packet"]["ref"]
        == TOP_PACKET_REF,
        "zero-slope subtraction top-packet ref mismatch",
    )
    require(
        zero_slope_subtraction["source_artifacts"]["line_value_lift"]["ref"]
        == LINE_VALUE_LIFT_REF,
        "zero-slope subtraction line-value ref mismatch",
    )
    require(
        zero_slope_subtraction["summary"][
            "deduped_aperiodic_numerator_after_removed_ledgers"
        ]
        == 0,
        "zero-slope subtraction residual numerator mismatch",
    )
    require(
        extension_denominator_audit["schema_version"]
        == "f17-32-m3-extension-denominator-audit-v1",
        "extension denominator audit schema mismatch",
    )
    require(
        extension_denominator_audit["source_artifacts"]["line_value_lift"]["ref"]
        == LINE_VALUE_LIFT_REF,
        "extension denominator audit line-value ref mismatch",
    )
    require(
        extension_denominator_audit["field_ledgers"][
            "finite_affine_slope_denominator"
        ]
        == 17**32,
        "extension denominator audit q_line mismatch",
    )
    require(
        extension_denominator_audit["line_value_classification"]["g"][
            "nonbase_values"
        ]
        == 512,
        "extension denominator audit did not classify g as extension-valued",
    )
    require(
        projective_endpoint_audit["schema_version"]
        == "f17-32-m3-projective-endpoint-audit-v1",
        "projective endpoint audit schema mismatch",
    )
    require(
        projective_endpoint_audit["source_artifacts"]["fixed_top_window_packet"][
            "ref"
        ]
        == TOP_PACKET_REF,
        "projective endpoint audit top-packet ref mismatch",
    )
    require(
        projective_endpoint_audit["summary"][
            "projective_infinity_contribution_before_removed_ledgers"
        ]
        == 0,
        "projective endpoint audit infinity contribution mismatch",
    )
    require(
        projective_endpoint_audit["summary"][
            "deduped_aperiodic_numerator_after_removed_ledgers"
        ]
        == 0,
        "projective endpoint audit residual numerator mismatch",
    )
    require(
        proportional_lemma["schema_version"]
        == "m1-hankel-proportional-pencil-tangent-lemma-v2",
        "proportional lemma schema mismatch",
    )
    require(
        proportional_lemma["status"] == "PROVED / AUDIT",
        "proportional lemma status mismatch",
    )
    require(
        proportional_lemma["theorem"]["v9_residual_label"]
        == "single_slope; tangent when full syndrome proportional",
        "proportional lemma residual label mismatch",
    )
    require(
        proportional_lemma["consequence_for_packets"][
            "if_full_syndrome_proportional"
        ]
        == "charge {-c} to tangent/common-code-line",
        "proportional lemma full-syndrome consequence mismatch",
    )
    require(
        proportional_lemma["consequence_for_packets"][
            "if_only_window_proportional"
        ]
        == "do not charge to tangent without a tail check",
        "proportional lemma tail-check consequence mismatch",
    )
    require(
        proportional_lemma["f17_32_replay"]["checked_residual_after_tangent"] == [],
        "proportional lemma F17^32 replay residual mismatch",
    )


def per_agreement_records(
    plan: dict[str, Any],
    generic: dict[str, Any],
    family: dict[str, Any],
    low_rank_family: dict[str, Any],
    top_packet: dict[str, Any],
    syndrome_realizability: dict[str, Any],
    zero_slope_subtraction: dict[str, Any],
    projective_endpoint_audit: dict[str, Any],
) -> list[dict[str, Any]]:
    plan_by_a = {int(item["A"]): item for item in plan["per_agreement"]}
    generic_by_a = {int(item["A"]): item for item in generic["agreements"]}
    family_by_a = {int(item["A"]): item for item in family["agreements"]}
    low_rank_family_by_a = {
        int(item["A"]): item for item in low_rank_family["records"]
    }
    realizability_by_a = {
        int(item["A"]): item for item in syndrome_realizability["per_agreement"]
    }
    top_by_a = top_window_by_agreement(top_packet)
    zero_subtraction_by_a = {
        int(item["A"]): item for item in zero_slope_subtraction["per_agreement"]
    }
    projective_by_a = {
        int(item["A"]): item for item in projective_endpoint_audit["per_agreement"]
    }
    finite_budget = int(plan["budget_context"]["budget_numerator"])
    projective_budget = int(
        projective_endpoint_audit["endpoint_conventions"][
            "projective_budget_numerator"
        ]
    )
    require(finite_budget == 17**32 // TWO128, "finite budget mismatch")
    require(projective_budget == (17**32 + 1) // TWO128, "projective budget mismatch")
    records = []
    for agreement in range(AGREEMENT_MIN, AGREEMENT_MAX + 1):
        plan_item = plan_by_a[agreement]
        generic_item = generic_by_a[agreement]
        family_item = family_by_a[agreement]
        low_rank_item = low_rank_family_by_a[agreement]
        realizability_item = realizability_by_a[agreement]
        top_item = top_by_a.get(agreement)
        require(plan_item["degree_bound"] == generic_item["generic_degree"], f"A={agreement}: degree mismatch")
        require(
            family_item["synthetic_roots"] == ROOT_UNION,
            f"A={agreement}: synthetic roots mismatch",
        )
        require(
            low_rank_item["degree_bound"] == 2
            and low_rank_item["root_status"] in {"exact_split", "exact_nonsquare"}
            and low_rank_item["root_count"] in {0, 2},
            f"A={agreement}: low-rank family status mismatch",
        )
        if low_rank_item["root_status"] == "exact_split":
            require(
                low_rank_item["root_count"] == 2
                and low_rank_item["quadratic_root_certificate"]["kind"]
                == "quadratic_discriminant_split",
                f"A={agreement}: split low-rank row mismatch",
            )
        else:
            require(
                low_rank_item["root_count"] == 0
                and low_rank_item["quadratic_root_certificate"]["kind"]
                == "quadratic_discriminant_nonsquare",
                f"A={agreement}: nonsquare low-rank row mismatch",
            )
        require(
            low_rank_item["projective_infinity"]["status"] == "empty"
            and low_rank_item["projective_infinity"]["contribution"] == 0,
            f"A={agreement}: low-rank projective endpoint mismatch",
        )
        require(
            low_rank_item["regular_budget_table"]["within_finite_budget"] is True
            and low_rank_item["regular_budget_table"]["within_projective_budget"]
            is True
            and low_rank_item["regular_budget_table"]["projective_regular_roots"]
            == low_rank_item["root_count"],
            f"A={agreement}: low-rank budget table mismatch",
        )
        require(
            low_rank_item["tangent_common_code_line_audit"]["overlap_count"] == 0
            and low_rank_item["tangent_common_code_line_audit"][
                "finite_roots_checked"
            ]
            == low_rank_item["root_count"],
            f"A={agreement}: low-rank tangent audit mismatch",
        )
        for witness in low_rank_item["tangent_common_code_line_audit"][
            "witnesses"
        ]:
            require(
                witness["status"] == "not_common_code_line"
                and witness["syndrome_index"] == 0,
                f"A={agreement}: bad tangent non-overlap witness",
            )
        require(
            realizability_item["visible_syndrome_length"] == 256
            and realizability_item["section_applies"] is True,
            f"A={agreement}: syndrome realizability mismatch",
        )
        visible_window_length = plan_item["t"] + plan_item["j"]
        require(
            visible_window_length == plan["row"]["syndrome_length"] == 256,
            f"A={agreement}: visible window is not the full stored syndrome",
        )
        if top_item is not None:
            b_ap_regular_before = top_item["extractor_audit"]["root_count"]
            require(
                b_ap_regular_before == 1,
                f"A={agreement}: top-window root count mismatch",
            )
            zero_subtraction_item = zero_subtraction_by_a[agreement]
            require(
                zero_subtraction_item["B_ap_after_removed_ledgers"] == 0,
                f"A={agreement}: zero-slope residual mismatch",
            )
            require(
                zero_subtraction_item["overlap_regular_tangent_roots"] == ROOT_UNION,
                f"A={agreement}: zero-slope overlap mismatch",
            )
            require(
                zero_subtraction_item["B_tan_common_code_line"] == 1,
                f"A={agreement}: tangent subtraction count mismatch",
            )
            require(
                zero_subtraction_item["B_quot_support"] == 0
                and zero_subtraction_item["B_quot_image"] == 0
                and zero_subtraction_item["B_ext"] == 0,
                f"A={agreement}: nonzero quotient/extension subtraction count",
            )
            projective_item = projective_by_a[agreement]
            require(
                projective_item["projective_infinity"]["contribution"] == 0,
                f"A={agreement}: projective endpoint contribution mismatch",
            )
            require(
                projective_item["top_degree"] == top_item["j"] + 1,
                f"A={agreement}: projective top degree mismatch",
            )
            deduped_finite = zero_subtraction_item[
                "deduped_total_upper_for_synthetic_packet"
            ]
            deduped_projective = (
                deduped_finite
                + projective_item["projective_infinity"]["contribution"]
            )
            require(
                deduped_finite == 1 and deduped_projective == 1,
                f"A={agreement}: fixed synthetic M4 total mismatch",
            )
            require(
                deduped_finite <= finite_budget
                and deduped_projective <= projective_budget,
                f"A={agreement}: fixed synthetic M4 table exceeds budget",
            )
            fixed_top_window_m4_table = {
                "B_tan": zero_subtraction_item["B_tan_common_code_line"],
                "B_quot_support": zero_subtraction_item["B_quot_support"],
                "B_quot_image": zero_subtraction_item["B_quot_image"],
                "B_ap_regular_before_removed": b_ap_regular_before,
                "B_ap_after_removed": zero_subtraction_item[
                    "B_ap_after_removed_ledgers"
                ],
                "B_ext": zero_subtraction_item["B_ext"],
                "B_projective_infinity": projective_item["projective_infinity"][
                    "contribution"
                ],
                "deduped_total_upper_finite_affine": deduped_finite,
                "deduped_total_upper_projective": deduped_projective,
                "finite_budget_numerator": finite_budget,
                "projective_budget_numerator": projective_budget,
                "finite_budget_gap": finite_budget - deduped_finite,
                "projective_budget_gap": projective_budget - deduped_projective,
                "safe_against_budget": True,
                "claim_status": "fixed_synthetic_packet_only",
            }
        else:
            zero_subtraction_item = None
            projective_item = None
            fixed_top_window_m4_table = None
        records.append(
            {
                "A": agreement,
                "j": plan_item["j"],
                "t": plan_item["t"],
                "minor_size": plan_item["minor_size"],
                "degree_bound": plan_item["degree_bound"],
                "generic_status": "all maximal row-set minors are generically nonzero",
                "generic_all_row_set_count": generic_item["all_row_set_atlas"]["count"],
                "synthetic_family_status": "closed-form u=0 prefix witness has exact root union {0}",
                "synthetic_root_union": ROOT_UNION,
                "synthetic_low_rank2_family_status": (
                    "rank-2 prefix update witness has an exact "
                    "split/nonsquare quadratic root certificate"
                ),
                "synthetic_low_rank2_root_bound": low_rank_item["degree_bound"],
                "synthetic_low_rank2_root_count": low_rank_item["root_count"],
                "synthetic_low_rank2_root_status": low_rank_item["root_status"],
                "synthetic_low_rank2_projective_infinity_contribution": 0,
                "synthetic_low_rank2_projective_regular_roots": low_rank_item[
                    "regular_budget_table"
                ]["projective_regular_roots"],
                "synthetic_low_rank2_projective_budget_gap": low_rank_item[
                    "regular_budget_table"
                ]["projective_budget_gap"],
                "synthetic_low_rank2_B_tan_common_code_line": 0,
                "synthetic_low_rank2_roots_after_common_code_line": low_rank_item[
                    "regular_budget_table"
                ]["regular_roots_after_common_code_line"],
                "synthetic_low_rank2_tangent_witness_moment": 0,
                "synthetic_low_rank2_sidecar_hash": low_rank_item["sidecar_hash"],
                "syndrome_pencil_realizability": (
                    "all length-256 u,v syndrome pencils are realized by explicit "
                    "line values on H"
                ),
                "syndrome_realizability_certificate": SYNDROME_REALIZABILITY_REF,
                "fixed_top_window_v9_packet": TOP_PACKET_REF if top_item is not None else None,
                "fixed_top_window_line_value_lift": LINE_VALUE_LIFT_REF
                if top_item is not None
                else None,
                "fixed_top_window_zero_slope_subtraction": ZERO_SLOPE_SUBTRACTION_REF
                if top_item is not None
                else None,
                "fixed_top_window_extension_denominator_audit": EXTENSION_DENOMINATOR_AUDIT_REF
                if top_item is not None
                else None,
                "fixed_top_window_projective_endpoint_audit": PROJECTIVE_ENDPOINT_AUDIT_REF
                if top_item is not None
                else None,
                "fixed_top_window_degree": (
                    top_item["extractor_audit"]["degree_bound"] if top_item is not None else None
                ),
                "fixed_top_window_projective_infinity_contribution": (
                    projective_item["projective_infinity"]["contribution"]
                    if projective_item is not None
                    else None
                ),
                "fixed_top_window_aperiodic_after_tangent": (
                    zero_subtraction_item["B_ap_after_removed_ledgers"]
                    if zero_subtraction_item is not None
                    else None
                ),
                "fixed_top_window_m4_table": fixed_top_window_m4_table,
                "actual_row_outcome": (
                    "line-value lift and zero-slope tangent subtraction supplied "
                    "for the fixed synthetic packet; "
                    "universal tangent/quotient-deduped row outcome not supplied"
                    if top_item is not None
                    else "row-realizability discharged; universal row outcome not supplied"
                ),
                "next_required": (
                    "classify arbitrary length-256 F_17^32 syndrome pencils after "
                    "tangent/quotient/extension ledgers: compute a nonzero regular "
                    "minor root table or declare the first singular bucket"
                ),
            }
        )
    return records


def build_status() -> dict[str, Any]:
    plan = load_json(PLAN_REF)
    generic = load_json(GENERIC_REF)
    family = load_json(FAMILY_REF)
    low_rank_family = load_json(LOW_RANK_FAMILY_REF)
    top_packet = load_json(TOP_PACKET_REF)
    line_value_lift = load_json(LINE_VALUE_LIFT_REF)
    subgroup_section = load_json(SUBGROUP_SECTION_REF)
    syndrome_realizability = load_json(SYNDROME_REALIZABILITY_REF)
    zero_slope_subtraction = load_json(ZERO_SLOPE_SUBTRACTION_REF)
    extension_denominator_audit = load_json(EXTENSION_DENOMINATOR_AUDIT_REF)
    projective_endpoint_audit = load_json(PROJECTIVE_ENDPOINT_AUDIT_REF)
    proportional_lemma = load_json(PROPORTIONAL_LEMMA_REF)
    validate_inputs(
        plan,
        generic,
        family,
        low_rank_family,
        top_packet,
        line_value_lift,
        subgroup_section,
        syndrome_realizability,
        zero_slope_subtraction,
        extension_denominator_audit,
        projective_endpoint_audit,
        proportional_lemma,
    )
    records = per_agreement_records(
        plan,
        generic,
        family,
        low_rank_family,
        top_packet,
        syndrome_realizability,
        zero_slope_subtraction,
        projective_endpoint_audit,
    )
    artifacts = [
        artifact_record("regular_window_plan", PLAN_REF, "regular-hankel-window-plan-v1"),
        artifact_record(
            "generic_all_row_set_regular_minor",
            GENERIC_REF,
            "f17-32-m3-generic-all-row-set-regular-minor-v1",
        ),
        artifact_record(
            "synthetic_rank_witness_family",
            FAMILY_REF,
            "f17-32-m3-rank-witness-family-v1",
        ),
        artifact_record(
            "synthetic_low_rank2_family",
            LOW_RANK_FAMILY_REF,
            "f17-32-m3-low-rank2-family-v4",
        ),
        artifact_record("fixed_top_window_v9_packet", TOP_PACKET_REF, "aperiodic-hankel-eliminant-v1"),
        artifact_record(
            "fixed_top_window_line_value_lift",
            LINE_VALUE_LIFT_REF,
            "f17-32-m3-line-value-lift-v1",
        ),
        artifact_record(
            "subgroup_syndrome_section",
            SUBGROUP_SECTION_REF,
            "subgroup-syndrome-section-v1",
        ),
        artifact_record(
            "m3_syndrome_realizability",
            SYNDROME_REALIZABILITY_REF,
            "f17-32-m3-syndrome-realizability-v1",
        ),
        artifact_record(
            "fixed_top_window_zero_slope_subtraction",
            ZERO_SLOPE_SUBTRACTION_REF,
            "f17-32-m3-zero-slope-subtraction-v1",
        ),
        artifact_record(
            "fixed_top_window_extension_denominator_audit",
            EXTENSION_DENOMINATOR_AUDIT_REF,
            "f17-32-m3-extension-denominator-audit-v1",
        ),
        artifact_record(
            "fixed_top_window_projective_endpoint_audit",
            PROJECTIVE_ENDPOINT_AUDIT_REF,
            "f17-32-m3-projective-endpoint-audit-v1",
        ),
        artifact_record(
            "hankel_proportional_pencil_tangent_lemma",
            PROPORTIONAL_LEMMA_REF,
            "m1-hankel-proportional-pencil-tangent-lemma-v2",
        ),
    ]
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "AUDIT",
        "row": plan["row"],
        "summary": {
            "regular_window": {"A_min": AGREEMENT_MIN, "A_max": AGREEMENT_MAX},
            "agreements": len(records),
            "degree_bound_sum": sum(record["degree_bound"] for record in records),
            "finite_slope_budget_numerator": plan["budget_context"]["budget_numerator"],
            "generic_regular_minors_status": "proved generically nonzero for every row-set chart",
            "synthetic_family_status": "proved closed-form root union {0} for all 42 synthetic pencils",
            "synthetic_low_rank2_family_status": "proved exact split/nonsquare quadratic root table for all 42 rank-2 synthetic pencils",
            "synthetic_low_rank2_degree_bound_sum": low_rank_family["aggregate"][
                "degree_bound_sum"
            ],
            "synthetic_low_rank2_exact_root_count_sum": low_rank_family[
                "aggregate"
            ]["exact_regular_root_count_sum"],
            "synthetic_low_rank2_split_rows": low_rank_family["aggregate"][
                "split_quadratic_rows"
            ],
            "synthetic_low_rank2_nonsquare_rows": low_rank_family["aggregate"][
                "nonsquare_quadratic_rows"
            ],
            "synthetic_low_rank2_projective_infinity_contribution": 0,
            "synthetic_low_rank2_max_projective_regular_roots_per_agreement": (
                low_rank_family["aggregate"][
                    "max_projective_regular_roots_per_agreement"
                ]
            ),
            "synthetic_low_rank2_projective_budget_status": (
                "all 42 rows have at most 2 projective regular roots, below "
                "projective budget numerator 6"
            ),
            "synthetic_low_rank2_common_code_line_tangent_overlap": 0,
            "synthetic_low_rank2_roots_after_common_code_line": (
                low_rank_family["aggregate"][
                    "exact_regular_roots_after_common_code_line"
                ]
            ),
            "synthetic_low_rank2_tangent_status": (
                "all 40 finite roots have nonzero full-syndrome witness at "
                "moment m=0, so none are common-code-line tangent roots"
            ),
            "fixed_top_window_status": "one v9 packet covers A=421..426 with root union {0}",
            "fixed_top_window_line_value_status": "explicit f,g line values replay the fixed top-window syndrome input",
            "subgroup_syndrome_section_status": "proved explicit inverse-Fourier section for subgroup syndrome vectors",
            "syndrome_pencil_realizability_status": "all length-256 u,v pencils in the M3 window are realized by explicit line values on H",
            "fixed_top_window_subtraction_status": "the synthetic root {0} is removed by the zero-codeword tangent slope, leaving aperiodic numerator 0",
            "fixed_top_window_denominator_status": "the line-value lift is genuinely F_17^32-valued, so the finite-affine slope denominator is 17^32",
            "fixed_top_window_projective_endpoint_status": "the projective endpoint [0:1] is empty for A=421..426, so projectivizing the fixed synthetic packet adds no regular-minor root",
            "fixed_top_window_m4_status": "for the fixed synthetic top-window packet, B_tan=1, B_quot_support=B_quot_image=B_ext=0, B_ap_after_removed=0, and the deduped total upper bound is 1 <= budget 6",
            "fixed_top_window_m4_deduped_total_upper": 1,
            "fixed_top_window_m4_budget_gap": 5,
            "proportional_branch_status": "all full-syndrome proportional pencils in the M3 window are tangent-labelled, because t+j equals the full stored syndrome length 256 for every A=385..426",
            "proportional_branch_certificate": PROPORTIONAL_LEMMA_REF,
            "proportional_branch_aperiodic_residual_after_tangent": 0,
            "proportional_branch_tail_check": "automatic for all 42 agreements because t+j=256 equals the stored syndrome length",
            "actual_row_status": "row-realizability is discharged; universal tangent/quotient-deduped row outcomes are not supplied",
            "first_actual_row_task": "classify arbitrary length-256 syndrome pencils by root table or singular-bucket outcome for A=385..426",
        },
        "artifacts": artifacts,
        "per_agreement": records,
        "claim_boundaries": {
            "proved": [
                "the v9 regular window is exactly 385 <= A <= 426",
                "every maximal row-set regular minor is generically nonzero",
                "the synthetic u=0 family has exact root union {0}",
                "the synthetic rank-2 low-rank family has exact split/nonsquare quadratic root table with 40 roots total, below degree cap 84",
                "the fixed synthetic top-window packet is v9-checkable for A=421..426",
                "the fixed top-window syndrome input has an explicit line-value lift",
                "subgroup syndrome vectors have an explicit inverse-Fourier line-value section",
                "every length-256 syndrome pencil in the M3 regular window is realized by explicit line values on the pinned subgroup row",
                "the fixed synthetic top-window root {0} is the zero-codeword tangent slope and leaves no synthetic residual aperiodic roots after subtraction",
                "the fixed top-window line-value lift is extension-valued and must use q_line=17^32 for finite-affine slope accounting",
                "the fixed top-window projective endpoint [0:1] is empty and contributes no extra synthetic regular-minor root",
                "the fixed synthetic top-window M4 table has deduped total upper bound 1, below the finite and projective budget numerator 6",
                "full-syndrome proportional pencils in the M3 regular window are tangent-labelled and leave no aperiodic residual after the tangent/common-code-line ledger",
            ],
            "not_proved": [
                "a universal root table for arbitrary length-256 syndrome pencils at any A in 385..426",
                "a tangent/quotient-deduped safe-side upper bound for the whole row in this window",
                "a Prime192 quotient/tangent subtraction or denominator table",
                "the first universal singular bucket classification",
            ],
        },
        "nonclaims": [
            "not a worst-case MCA bound",
            "not a universal M3 row outcome",
            "not a full quotient/tangent subtraction table",
            "not a singular-pivot packet",
        ],
    }


def check_status(path: Path) -> None:
    expected = render(build_status())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"regular-window status mismatch: {path}")


def print_summary(status: dict[str, Any]) -> None:
    summary = status["summary"]
    print("F_17^32 M3 regular-window status")
    print(
        "window: A={A_min}..{A_max}, agreements={agreements}, degree_sum={degree_bound_sum}".format(
            agreements=summary["agreements"],
            degree_bound_sum=summary["degree_bound_sum"],
            **summary["regular_window"],
        )
    )
    print(f"generic: {summary['generic_regular_minors_status']}")
    print(f"synthetic: {summary['synthetic_family_status']}")
    print(f"low-rank synthetic: {summary['synthetic_low_rank2_family_status']}")
    print(
        "low-rank projective: "
        f"{summary['synthetic_low_rank2_projective_budget_status']}"
    )
    print(f"low-rank tangent: {summary['synthetic_low_rank2_tangent_status']}")
    print(f"actual row: {summary['actual_row_status']}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path, help="write deterministic status JSON")
    parser.add_argument("--check", type=Path, help="check deterministic status JSON")
    parser.add_argument("--json", action="store_true", help="print status JSON")
    args = parser.parse_args()

    status = build_status()
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(status), encoding="utf-8")
    if args.check:
        check_status(args.check)
    if args.json:
        print(render(status), end="")
        return
    print_summary(status)


if __name__ == "__main__":
    main()
