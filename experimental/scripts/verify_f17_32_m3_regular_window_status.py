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
LOW_RANK3_FAMILY_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank3-family/"
    "f17_32_n512_k256_m3_low_rank3_family_certificate.json"
)
LOW_RANK4_BUDGET_FAMILY_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank4-budget-family/"
    "f17_32_n512_k256_m3_low_rank4_budget_family_certificate.json"
)
LOW_RANK5_BUDGET_FAMILY_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank5-budget-family/"
    "f17_32_n512_k256_m3_low_rank5_budget_family_certificate.json"
)
LOW_RANK6_SLACK_FAMILY_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank6-slack-family/"
    "f17_32_n512_k256_m3_low_rank6_slack_family_certificate.json"
)
LOW_RANK7_SLACK_FAMILY_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank7-slack-family/"
    "f17_32_n512_k256_m3_low_rank7_slack_family_certificate.json"
)
LOW_RANK8_SLACK_FAMILY_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank8-slack-family/"
    "f17_32_n512_k256_m3_low_rank8_slack_family_certificate.json"
)
LOW_RANK9_11_SLACK_SWEEP_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank9-11-slack-sweep/"
    "f17_32_n512_k256_m3_low_rank9_11_slack_sweep_certificate.json"
)
LOW_RANK2_11_PROJECTIVE_INFINITY_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank2-11-projective-infinity/"
    "f17_32_n512_k256_m3_low_rank2_11_projective_infinity_certificate.json"
)
LOW_RANK2_11_ENDPOINT_QUOTIENT_SUPPORT_REF = (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-low-rank2-11-endpoint-quotient-support/"
    "f17_32_n512_k256_m3_low_rank2_11_endpoint_quotient_support.json"
)
LOW_RANK_RANK6_A426_PROJECTIVE_PIVOT_REF = (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-low-rank-rank6-a426-projective-pivot/"
    "f17_32_n512_k256_a426_rank6_projective_infinity_pivot_packet.json"
)
LOW_RANK_RANK6_A426_FINITE_PACKET_REF = (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-low-rank-rank6-a426-finite-affine/"
    "f17_32_n512_k256_a426_rank6_finite_affine_packet.json"
)
LOW_RANK_RANK6_A426_PROJECTIVE_LINE_PACKET_REF = (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-low-rank-rank6-a426-projective-line/"
    "f17_32_n512_k256_a426_rank6_projective_line_packet.json"
)
LOW_RANK_RANK7_A393_PROJECTIVE_LINE_PACKET_REF = (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-low-rank-rank7-a393-projective-line/"
    "f17_32_n512_k256_a393_rank7_projective_line_packet.json"
)
LOW_RANK_RANK8_A393_PROJECTIVE_LINE_PACKET_REF = (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-low-rank-rank8-a393-projective-line/"
    "f17_32_n512_k256_a393_rank8_projective_line_packet.json"
)
LOW_RANK_RANK9_A398_PROJECTIVE_LINE_PACKET_REF = (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-low-rank-rank9-a398-projective-line/"
    "f17_32_n512_k256_a398_rank9_projective_line_packet.json"
)
LOW_RANK_RANK10_A411_PROJECTIVE_LINE_PACKET_REF = (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-low-rank-rank10-a411-projective-line/"
    "f17_32_n512_k256_a411_rank10_projective_line_packet.json"
)
LOW_RANK_RANK11_A391_PROJECTIVE_LINE_PACKET_REF = (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-low-rank-rank11-a391-projective-line/"
    "f17_32_n512_k256_a391_rank11_projective_line_packet.json"
)
LOW_RANK6_11_TANGENT_EXCLUSION_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank6-11-tangent-exclusion/"
    "f17_32_n512_k256_m3_low_rank6_11_tangent_exclusion_certificate.json"
)
LOW_RANK6_11_SUBFIELD_EXCLUSION_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank6-11-subfield-exclusion/"
    "f17_32_n512_k256_m3_low_rank6_11_subfield_exclusion_certificate.json"
)
LOW_RANK6_11_KNOWN_LEDGER_TABLE_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-low-rank6-11-known-ledger-table/"
    "f17_32_n512_k256_m3_low_rank6_11_known_ledger_table.json"
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
LOW_RANK_TEMPLATE_REF = (
    "experimental/data/certificates/hankel-low-rank-update-template/"
    "hankel_low_rank_update_template_certificate.json"
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


def validate_compact_sweep_projective_line_packet(
    packet: dict[str, Any],
    *,
    rank: int,
    agreement: int,
    j: int,
    t: int,
    finite_roots: int,
    numerator: int,
) -> None:
    label = f"rank-{rank} A={agreement} projective-line"
    infinity_contribution = numerator - finite_roots
    require(
        packet["schema_version"] == "aperiodic-hankel-eliminant-v1",
        f"{label} packet schema mismatch",
    )
    require(
        packet["packet_certificate_schema"]
        == f"f17-32-m3-low-rank-rank{rank}-a{agreement}-projective-line-v1",
        f"{label} certificate schema mismatch",
    )
    require(
        packet["sampler"] == "projective_line"
        and packet["sampler_audit"]["denominator"] == 17**32 + 1,
        f"{label} sampler mismatch",
    )
    require(packet["agreement_threshold"] == agreement, f"{label} threshold mismatch")
    require(
        packet["declared_aperiodic_numerator"] == numerator
        and packet["finite_affine_numerator"] == finite_roots
        and packet["projective_infinity_numerator"] == infinity_contribution
        and len(packet["root_union"]) == finite_roots,
        f"{label} numerator mismatch",
    )
    item = packet["exact_agreements"][0]
    infinity = item["projective_infinity"]
    require(
        item["A"] == agreement
        and item["j"] == j
        and item["t"] == t
        and item["status"] == "regular_minor"
        and item["regular_minor"]["degree"] == rank
        and item["regular_minor_data"]["roots"] == packet["root_union"]
        and item["regular_minor_data"]["linear_root_count_certificate"][
            "linear_root_count"
        ]
        == finite_roots
        and infinity["projective_point"] == "[0:1]"
        and infinity["status"] == "nonempty"
        and infinity["top_degree"] == j + 1
        and infinity["top_coefficient"] == 0
        and infinity["contribution"] == infinity_contribution,
        f"{label} agreement mismatch",
    )


def top_window_by_agreement(packet: dict[str, Any]) -> dict[int, dict[str, Any]]:
    return {int(item["A"]): item for item in packet["exact_agreements"]}


def validate_inputs(
    plan: dict[str, Any],
    generic: dict[str, Any],
    family: dict[str, Any],
    low_rank_family: dict[str, Any],
    low_rank3_family: dict[str, Any],
    low_rank4_budget_family: dict[str, Any],
    low_rank5_budget_family: dict[str, Any],
    low_rank6_slack_family: dict[str, Any],
    low_rank7_slack_family: dict[str, Any],
    low_rank8_slack_family: dict[str, Any],
    low_rank9_11_slack_sweep: dict[str, Any],
    low_rank2_11_projective_infinity: dict[str, Any],
    low_rank2_11_endpoint_quotient_support: dict[str, Any],
    low_rank_rank6_a426_projective_pivot: dict[str, Any],
    low_rank_rank6_a426_finite_packet: dict[str, Any],
    low_rank_rank6_a426_projective_line_packet: dict[str, Any],
    low_rank_rank7_a393_projective_line_packet: dict[str, Any],
    low_rank_rank8_a393_projective_line_packet: dict[str, Any],
    low_rank_rank9_a398_projective_line_packet: dict[str, Any],
    low_rank_rank10_a411_projective_line_packet: dict[str, Any],
    low_rank_rank11_a391_projective_line_packet: dict[str, Any],
    low_rank6_11_tangent_exclusion: dict[str, Any],
    low_rank6_11_subfield_exclusion: dict[str, Any],
    low_rank6_11_known_ledger_table: dict[str, Any],
    top_packet: dict[str, Any],
    line_value_lift: dict[str, Any],
    subgroup_section: dict[str, Any],
    syndrome_realizability: dict[str, Any],
    zero_slope_subtraction: dict[str, Any],
    extension_denominator_audit: dict[str, Any],
    projective_endpoint_audit: dict[str, Any],
    proportional_lemma: dict[str, Any],
    low_rank_template: dict[str, Any],
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
        low_rank_family["schema_version"] == "f17-32-m3-low-rank2-family-v5",
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
        low_rank_family["aggregate"]["projective_infinity_contribution_sum"] == 42,
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
        == 3,
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
        low_rank3_family["schema_version"] == "f17-32-m3-low-rank3-family-v2",
        "rank-3 low-rank family schema mismatch",
    )
    require(
        low_rank3_family["agreement_range"] == [AGREEMENT_MIN, AGREEMENT_MAX],
        "rank-3 low-rank family window mismatch",
    )
    require(
        low_rank3_family["aggregate"]["agreement_count"] == 42,
        "rank-3 low-rank family agreement count mismatch",
    )
    require(
        low_rank3_family["aggregate"]["per_agreement_degree_bound"] == 3,
        "rank-3 low-rank family per-agreement bound mismatch",
    )
    require(
        low_rank3_family["aggregate"]["degree_bound_sum"] == 126,
        "rank-3 low-rank family degree-bound aggregate mismatch",
    )
    require(
        low_rank3_family["aggregate"]["exact_regular_root_count_sum"] == 42,
        "rank-3 low-rank family exact-root-count aggregate mismatch",
    )
    require(
        low_rank3_family["aggregate"]["linear_root_count_histogram"]
        == {"0": 12, "1": 24, "3": 6},
        "rank-3 low-rank family root-count histogram mismatch",
    )
    require(
        low_rank3_family["aggregate"]["projective_infinity_contribution_sum"] == 42,
        "rank-3 low-rank family projective contribution mismatch",
    )
    require(
        low_rank3_family["aggregate"]["common_code_line_tangent_overlap_sum"] == 0,
        "rank-3 low-rank family tangent overlap mismatch",
    )
    require(
        low_rank3_family["aggregate"]["finite_roots_checked_for_common_code_line"]
        == low_rank3_family["aggregate"]["exact_regular_root_count_sum"],
        "rank-3 low-rank family tangent check coverage mismatch",
    )
    require(
        low_rank3_family["aggregate"]["exact_regular_roots_after_common_code_line"]
        == 42,
        "rank-3 low-rank family post-tangent root count mismatch",
    )
    require(
        low_rank3_family["aggregate"]["max_projective_regular_roots_per_agreement"]
        == 4,
        "rank-3 low-rank family max projective roots mismatch",
    )
    require(
        low_rank3_family["aggregate"]["all_rows_within_finite_budget"] is True
        and low_rank3_family["aggregate"]["all_rows_within_projective_budget"] is True,
        "rank-3 low-rank family budget status mismatch",
    )
    require(
        low_rank3_family["aggregate"]["generic_degree_bound_sum_for_window"]
        == plan["budget_context"]["degree_bound_sum"],
        "rank-3 low-rank family generic degree sum mismatch",
    )
    require(
        len(low_rank3_family["records"]) == 42,
        "rank-3 low-rank family record count mismatch",
    )
    require(
        low_rank4_budget_family["schema_version"]
        == "f17-32-m3-low-rank4-budget-family-v1",
        "rank-4 low-rank budget family schema mismatch",
    )
    require(
        low_rank4_budget_family["agreement_range"] == [AGREEMENT_MIN, AGREEMENT_MAX],
        "rank-4 low-rank budget family window mismatch",
    )
    require(
        low_rank4_budget_family["source_artifacts"]["low_rank_template"][
            "schema_version"
        ]
        == "m1-hankel-low-rank-update-template-v4",
        "rank-4 low-rank budget family template schema mismatch",
    )
    require(
        low_rank4_budget_family["aggregate"]["agreement_count"] == 42,
        "rank-4 low-rank budget family agreement count mismatch",
    )
    require(
        low_rank4_budget_family["aggregate"]["per_agreement_degree_bound"] == 4,
        "rank-4 low-rank budget family per-agreement bound mismatch",
    )
    require(
        low_rank4_budget_family["aggregate"]["degree_bound_sum"] == 168,
        "rank-4 low-rank budget family degree-bound aggregate mismatch",
    )
    require(
        low_rank4_budget_family["aggregate"]["polynomial_degree_histogram"]
        == {"4": 42},
        "rank-4 low-rank budget family degree histogram mismatch",
    )
    require(
        low_rank4_budget_family["aggregate"]["projective_infinity_contribution_sum"]
        == 42,
        "rank-4 low-rank budget family projective contribution mismatch",
    )
    require(
        low_rank4_budget_family["aggregate"][
            "max_finite_roots_per_agreement_bound"
        ]
        == 4,
        "rank-4 low-rank budget family finite bound mismatch",
    )
    require(
        low_rank4_budget_family["aggregate"][
            "max_projective_regular_roots_per_agreement_bound"
        ]
        == 5,
        "rank-4 low-rank budget family projective bound mismatch",
    )
    require(
        low_rank4_budget_family["aggregate"]["all_rows_within_finite_budget"]
        is True
        and low_rank4_budget_family["aggregate"]["all_rows_within_projective_budget"]
        is True,
        "rank-4 low-rank budget family budget status mismatch",
    )
    require(
        low_rank4_budget_family["aggregate"]["generic_degree_bound_sum_for_window"]
        == plan["budget_context"]["degree_bound_sum"],
        "rank-4 low-rank budget family generic degree sum mismatch",
    )
    require(
        len(low_rank4_budget_family["records"]) == 42,
        "rank-4 low-rank budget family record count mismatch",
    )
    require(
        low_rank5_budget_family["schema_version"]
        == "f17-32-m3-low-rank5-budget-family-v1",
        "rank-5 low-rank budget family schema mismatch",
    )
    require(
        low_rank5_budget_family["agreement_range"] == [AGREEMENT_MIN, AGREEMENT_MAX],
        "rank-5 low-rank budget family window mismatch",
    )
    require(
        low_rank5_budget_family["source_artifacts"]["low_rank_template"][
            "schema_version"
        ]
        == "m1-hankel-low-rank-update-template-v4",
        "rank-5 low-rank budget family template schema mismatch",
    )
    require(
        low_rank5_budget_family["aggregate"]["agreement_count"] == 42,
        "rank-5 low-rank budget family agreement count mismatch",
    )
    require(
        low_rank5_budget_family["aggregate"]["per_agreement_degree_bound"] == 5,
        "rank-5 low-rank budget family per-agreement bound mismatch",
    )
    require(
        low_rank5_budget_family["aggregate"]["degree_bound_sum"] == 210,
        "rank-5 low-rank budget family degree-bound aggregate mismatch",
    )
    require(
        low_rank5_budget_family["aggregate"]["polynomial_degree_histogram"]
        == {"5": 42},
        "rank-5 low-rank budget family degree histogram mismatch",
    )
    require(
        low_rank5_budget_family["aggregate"]["projective_infinity_contribution_sum"]
        == 42,
        "rank-5 low-rank budget family projective contribution mismatch",
    )
    require(
        low_rank5_budget_family["aggregate"][
            "max_finite_roots_per_agreement_bound"
        ]
        == 5,
        "rank-5 low-rank budget family finite bound mismatch",
    )
    require(
        low_rank5_budget_family["aggregate"][
            "max_projective_regular_roots_per_agreement_bound"
        ]
        == 6,
        "rank-5 low-rank budget family projective bound mismatch",
    )
    require(
        low_rank5_budget_family["aggregate"]["all_rows_within_finite_budget"]
        is True
        and low_rank5_budget_family["aggregate"]["all_rows_within_projective_budget"]
        is True,
        "rank-5 low-rank budget family budget status mismatch",
    )
    require(
        low_rank5_budget_family["aggregate"]["generic_degree_bound_sum_for_window"]
        == plan["budget_context"]["degree_bound_sum"],
        "rank-5 low-rank budget family generic degree sum mismatch",
    )
    require(
        len(low_rank5_budget_family["records"]) == 42,
        "rank-5 low-rank budget family record count mismatch",
    )
    require(
        low_rank6_slack_family["schema_version"]
        == "f17-32-m3-low-rank6-slack-family-v1",
        "rank-6 low-rank slack family schema mismatch",
    )
    require(
        low_rank6_slack_family["agreement_range"] == [AGREEMENT_MIN, AGREEMENT_MAX],
        "rank-6 low-rank slack family window mismatch",
    )
    require(
        low_rank6_slack_family["source_artifacts"]["low_rank_template"][
            "schema_version"
        ]
        == "m1-hankel-low-rank-update-template-v4",
        "rank-6 low-rank slack family template schema mismatch",
    )
    require(
        low_rank6_slack_family["aggregate"]["agreement_count"] == 42,
        "rank-6 low-rank slack family agreement count mismatch",
    )
    require(
        low_rank6_slack_family["aggregate"]["per_agreement_degree_bound"] == 6,
        "rank-6 low-rank slack family per-agreement bound mismatch",
    )
    require(
        low_rank6_slack_family["aggregate"]["degree_bound_sum"] == 252,
        "rank-6 low-rank slack family degree-bound aggregate mismatch",
    )
    require(
        low_rank6_slack_family["aggregate"]["polynomial_degree_histogram"]
        == {"6": 42},
        "rank-6 low-rank slack family degree histogram mismatch",
    )
    require(
        low_rank6_slack_family["aggregate"]["exact_regular_root_count_sum"] == 35,
        "rank-6 low-rank slack family exact-root sum mismatch",
    )
    require(
        low_rank6_slack_family["aggregate"]["linear_root_count_histogram"]
        == {"0": 16, "1": 17, "2": 9},
        "rank-6 low-rank slack family root histogram mismatch",
    )
    require(
        low_rank6_slack_family["aggregate"]["projective_infinity_contribution_sum"]
        == 42,
        "rank-6 low-rank slack family projective contribution mismatch",
    )
    require(
        low_rank6_slack_family["aggregate"]["max_finite_roots_per_agreement"]
        == 2,
        "rank-6 low-rank slack family finite maximum mismatch",
    )
    require(
        low_rank6_slack_family["aggregate"][
            "max_projective_regular_roots_per_agreement"
        ]
        == 3,
        "rank-6 low-rank slack family projective maximum mismatch",
    )
    require(
        low_rank6_slack_family["aggregate"]["degree_only_projective_bound_without_slack"]
        == 7
        and low_rank6_slack_family["aggregate"][
            "degree_only_projective_bound_within_budget"
        ]
        is False
        and low_rank6_slack_family["aggregate"]["finite_slack_projective_gate_status"]
        == "closed_by_exact_root_count",
        "rank-6 low-rank slack family finite-slack status mismatch",
    )
    require(
        low_rank6_slack_family["aggregate"]["all_rows_within_finite_budget"]
        is True
        and low_rank6_slack_family["aggregate"]["all_rows_within_projective_budget"]
        is True,
        "rank-6 low-rank slack family budget status mismatch",
    )
    require(
        low_rank6_slack_family["aggregate"]["generic_degree_bound_sum_for_window"]
        == plan["budget_context"]["degree_bound_sum"],
        "rank-6 low-rank slack family generic degree sum mismatch",
    )
    require(
        len(low_rank6_slack_family["records"]) == 42,
        "rank-6 low-rank slack family record count mismatch",
    )
    require(
        low_rank7_slack_family["schema_version"]
        == "f17-32-m3-low-rank7-slack-family-v1",
        "rank-7 low-rank slack family schema mismatch",
    )
    require(
        low_rank7_slack_family["agreement_range"] == [AGREEMENT_MIN, AGREEMENT_MAX],
        "rank-7 low-rank slack family window mismatch",
    )
    require(
        low_rank7_slack_family["source_artifacts"]["low_rank_template"][
            "schema_version"
        ]
        == "m1-hankel-low-rank-update-template-v4",
        "rank-7 low-rank slack family template schema mismatch",
    )
    require(
        low_rank7_slack_family["aggregate"]["agreement_count"] == 42,
        "rank-7 low-rank slack family agreement count mismatch",
    )
    require(
        low_rank7_slack_family["aggregate"]["per_agreement_degree_bound"] == 7,
        "rank-7 low-rank slack family per-agreement bound mismatch",
    )
    require(
        low_rank7_slack_family["aggregate"]["degree_bound_sum"] == 294,
        "rank-7 low-rank slack family degree-bound aggregate mismatch",
    )
    require(
        low_rank7_slack_family["aggregate"]["polynomial_degree_histogram"]
        == {"7": 42},
        "rank-7 low-rank slack family degree histogram mismatch",
    )
    require(
        low_rank7_slack_family["aggregate"]["exact_regular_root_count_sum"] == 43,
        "rank-7 low-rank slack family exact-root sum mismatch",
    )
    require(
        low_rank7_slack_family["aggregate"]["linear_root_count_histogram"]
        == {"0": 16, "1": 15, "2": 6, "3": 4, "4": 1},
        "rank-7 low-rank slack family root histogram mismatch",
    )
    require(
        low_rank7_slack_family["aggregate"]["projective_infinity_contribution_sum"]
        == 42,
        "rank-7 low-rank slack family projective contribution mismatch",
    )
    require(
        low_rank7_slack_family["aggregate"]["max_finite_roots_per_agreement"]
        == 4,
        "rank-7 low-rank slack family finite maximum mismatch",
    )
    require(
        low_rank7_slack_family["aggregate"][
            "max_projective_regular_roots_per_agreement"
        ]
        == 5,
        "rank-7 low-rank slack family projective maximum mismatch",
    )
    require(
        low_rank7_slack_family["aggregate"]["degree_only_projective_bound_without_slack"]
        == 8
        and low_rank7_slack_family["aggregate"][
            "degree_only_projective_bound_within_budget"
        ]
        is False
        and low_rank7_slack_family["aggregate"]["finite_slack_projective_gate_status"]
        == "closed_by_exact_root_count",
        "rank-7 low-rank slack family finite-slack status mismatch",
    )
    require(
        low_rank7_slack_family["aggregate"]["all_rows_within_finite_budget"]
        is True
        and low_rank7_slack_family["aggregate"]["all_rows_within_projective_budget"]
        is True,
        "rank-7 low-rank slack family budget status mismatch",
    )
    require(
        low_rank7_slack_family["aggregate"]["generic_degree_bound_sum_for_window"]
        == plan["budget_context"]["degree_bound_sum"],
        "rank-7 low-rank slack family generic degree sum mismatch",
    )
    require(
        len(low_rank7_slack_family["records"]) == 42,
        "rank-7 low-rank slack family record count mismatch",
    )
    require(
        low_rank8_slack_family["schema_version"]
        == "f17-32-m3-low-rank8-slack-family-v1",
        "rank-8 low-rank slack family schema mismatch",
    )
    require(
        low_rank8_slack_family["agreement_range"] == [AGREEMENT_MIN, AGREEMENT_MAX],
        "rank-8 low-rank slack family window mismatch",
    )
    require(
        low_rank8_slack_family["source_artifacts"]["low_rank_template"][
            "schema_version"
        ]
        == "m1-hankel-low-rank-update-template-v4",
        "rank-8 low-rank slack family template schema mismatch",
    )
    require(
        low_rank8_slack_family["aggregate"]["agreement_count"] == 42,
        "rank-8 low-rank slack family agreement count mismatch",
    )
    require(
        low_rank8_slack_family["aggregate"]["per_agreement_degree_bound"] == 8,
        "rank-8 low-rank slack family per-agreement bound mismatch",
    )
    require(
        low_rank8_slack_family["aggregate"]["degree_bound_sum"] == 336,
        "rank-8 low-rank slack family degree-bound aggregate mismatch",
    )
    require(
        low_rank8_slack_family["aggregate"]["polynomial_degree_histogram"]
        == {"8": 42},
        "rank-8 low-rank slack family degree histogram mismatch",
    )
    require(
        low_rank8_slack_family["aggregate"]["exact_regular_root_count_sum"] == 34,
        "rank-8 low-rank slack family exact-root sum mismatch",
    )
    require(
        low_rank8_slack_family["aggregate"]["linear_root_count_histogram"]
        == {"0": 22, "1": 10, "2": 7, "3": 2, "4": 1},
        "rank-8 low-rank slack family root histogram mismatch",
    )
    require(
        low_rank8_slack_family["aggregate"]["projective_infinity_contribution_sum"]
        == 42,
        "rank-8 low-rank slack family projective contribution mismatch",
    )
    require(
        low_rank8_slack_family["aggregate"]["max_finite_roots_per_agreement"]
        == 4,
        "rank-8 low-rank slack family finite maximum mismatch",
    )
    require(
        low_rank8_slack_family["aggregate"][
            "max_projective_regular_roots_per_agreement"
        ]
        == 5,
        "rank-8 low-rank slack family projective maximum mismatch",
    )
    require(
        low_rank8_slack_family["aggregate"]["degree_only_projective_bound_without_slack"]
        == 9
        and low_rank8_slack_family["aggregate"][
            "degree_only_projective_bound_within_budget"
        ]
        is False
        and low_rank8_slack_family["aggregate"]["finite_slack_projective_gate_status"]
        == "closed_by_exact_root_count",
        "rank-8 low-rank slack family finite-slack status mismatch",
    )
    require(
        low_rank8_slack_family["aggregate"]["all_rows_within_finite_budget"]
        is True
        and low_rank8_slack_family["aggregate"]["all_rows_within_projective_budget"]
        is True,
        "rank-8 low-rank slack family budget status mismatch",
    )
    require(
        low_rank8_slack_family["aggregate"]["generic_degree_bound_sum_for_window"]
        == plan["budget_context"]["degree_bound_sum"],
        "rank-8 low-rank slack family generic degree sum mismatch",
    )
    require(
        len(low_rank8_slack_family["records"]) == 42,
        "rank-8 low-rank slack family record count mismatch",
    )
    require(
        low_rank9_11_slack_sweep["schema_version"]
        == "f17-32-m3-low-rank9-11-slack-sweep-v1",
        "rank-9..11 low-rank slack sweep schema mismatch",
    )
    require(
        low_rank9_11_slack_sweep["agreement_range"]
        == [AGREEMENT_MIN, AGREEMENT_MAX],
        "rank-9..11 low-rank slack sweep window mismatch",
    )
    require(
        low_rank9_11_slack_sweep["source_artifacts"]["low_rank_template"][
            "schema_version"
        ]
        == "m1-hankel-low-rank-update-template-v4",
        "rank-9..11 low-rank slack sweep template schema mismatch",
    )
    require(
        low_rank9_11_slack_sweep["construction"]["ranks"] == [9, 10, 11],
        "rank-9..11 low-rank slack sweep rank list mismatch",
    )
    require(
        low_rank9_11_slack_sweep["aggregate"]["record_count"] == 126,
        "rank-9..11 low-rank slack sweep record count mismatch",
    )
    expected_rank_summaries = {
        "9": {
            "degree_bound_sum": 378,
            "exact_regular_root_count_sum": 35,
            "linear_root_count_histogram": {"0": 17, "1": 17, "2": 6, "3": 2},
            "degree_only_projective_bound_without_slack": 10,
        },
        "10": {
            "degree_bound_sum": 420,
            "exact_regular_root_count_sum": 47,
            "linear_root_count_histogram": {"0": 8, "1": 23, "2": 9, "3": 2},
            "degree_only_projective_bound_without_slack": 11,
        },
        "11": {
            "degree_bound_sum": 462,
            "exact_regular_root_count_sum": 44,
            "linear_root_count_histogram": {"0": 15, "1": 16, "2": 5, "3": 6},
            "degree_only_projective_bound_without_slack": 12,
        },
    }
    for rank, expected_summary in expected_rank_summaries.items():
        summary = low_rank9_11_slack_sweep["aggregate"]["rank_summaries"][rank]
        require(
            summary["agreement_count"] == 42
            and summary["degree_bound_sum"]
            == expected_summary["degree_bound_sum"]
            and summary["exact_regular_root_count_sum"]
            == expected_summary["exact_regular_root_count_sum"]
            and summary["linear_root_count_histogram"]
            == expected_summary["linear_root_count_histogram"]
            and summary["max_finite_roots_per_agreement"] == 3
            and summary["max_projective_regular_roots_per_agreement"] == 4
            and summary["degree_only_projective_bound_without_slack"]
            == expected_summary["degree_only_projective_bound_without_slack"]
            and summary["degree_only_projective_bound_within_budget"] is False
            and summary["all_rows_within_finite_budget"] is True
            and summary["all_rows_within_projective_budget"] is True,
            f"rank-{rank} low-rank slack sweep summary mismatch",
        )
    require(
        low_rank9_11_slack_sweep["aggregate"][
            "max_projective_regular_roots_over_sweep"
        ]
        == 4
        and low_rank9_11_slack_sweep["aggregate"][
            "all_rows_within_projective_budget"
        ]
        is True
        and low_rank9_11_slack_sweep["aggregate"][
            "generic_degree_bound_sum_for_window"
        ]
        == plan["budget_context"]["degree_bound_sum"],
        "rank-9..11 low-rank slack sweep aggregate mismatch",
    )
    require(
        low_rank2_11_projective_infinity["schema_version"]
        == "f17-32-m3-low-rank2-11-projective-infinity-v1",
        "rank-2..11 projective infinity schema mismatch",
    )
    require(
        low_rank2_11_projective_infinity["agreement_range"]
        == [AGREEMENT_MIN, AGREEMENT_MAX],
        "rank-2..11 projective infinity window mismatch",
    )
    require(
        low_rank2_11_projective_infinity["construction"]["ranks"]
        == [2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        "rank-2..11 projective infinity rank list mismatch",
    )
    require(
        low_rank2_11_projective_infinity["aggregate"]["record_count"] == 420
        and low_rank2_11_projective_infinity["deterministic_records"][
            "record_count"
        ]
        == 420
        and low_rank2_11_projective_infinity["aggregate"][
            "projective_infinity_contribution_sum"
        ]
        == 420
        and low_rank2_11_projective_infinity["aggregate"][
            "minimum_endpoint_support_size"
        ]
        == 501
        and low_rank2_11_projective_infinity["aggregate"][
            "maximum_agreement_threshold"
        ]
        == AGREEMENT_MAX
        and low_rank2_11_projective_infinity["aggregate"][
            "maximum_vandermonde_column_count"
        ]
        == 139
        and low_rank2_11_projective_infinity["aggregate"][
            "syndrome_length"
        ]
        == 256
        and low_rank2_11_projective_infinity["aggregate"][
            "all_endpoint_noncontainment_checks_pass"
        ]
        is True,
        "rank-2..11 projective infinity aggregate mismatch",
    )
    for rank in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
        summary = low_rank2_11_projective_infinity["aggregate"]["rank_summaries"][
            str(rank)
        ]
        require(
            summary["agreement_count"] == 42
            and summary["endpoint_support_size"] == 512 - rank
            and summary["projective_infinity_contribution_sum"] == 42
            and summary["thresholds_covered"] is True,
            f"rank-{rank} projective infinity summary mismatch",
        )
    require(
        low_rank2_11_endpoint_quotient_support["schema_version"]
        == "f17-32-m3-low-rank2-11-endpoint-quotient-support-v1",
        "rank-2..11 endpoint quotient-support schema mismatch",
    )
    require(
        low_rank2_11_endpoint_quotient_support["agreement_range"]
        == [AGREEMENT_MIN, AGREEMENT_MAX],
        "rank-2..11 endpoint quotient-support window mismatch",
    )
    require(
        low_rank2_11_endpoint_quotient_support["ranks"]
        == [2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        "rank-2..11 endpoint quotient-support rank list mismatch",
    )
    require(
        low_rank2_11_endpoint_quotient_support["aggregate"]["record_count"]
        == 420
        and low_rank2_11_endpoint_quotient_support["deterministic_records"][
            "record_count"
        ]
        == 420
        and low_rank2_11_endpoint_quotient_support["aggregate"][
            "nontrivial_quotient_check_count"
        ]
        == 3360
        and low_rank2_11_endpoint_quotient_support["aggregate"][
            "nontrivial_fiber_sizes"
        ]
        == [2, 4, 8, 16, 32, 64, 128, 256]
        and low_rank2_11_endpoint_quotient_support["aggregate"][
            "trivial_fiber_sizes_not_claimed"
        ]
        == [1, 512]
        and low_rank2_11_endpoint_quotient_support["aggregate"][
            "minimum_excess_hit_fibers"
        ]
        >= 1
        and low_rank2_11_endpoint_quotient_support["aggregate"][
            "all_nontrivial_quotient_supports_excluded"
        ]
        is True,
        "rank-2..11 endpoint quotient-support aggregate mismatch",
    )
    for rank in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
        summary = low_rank2_11_endpoint_quotient_support["aggregate"][
            "rank_summaries"
        ][str(rank)]
        require(
            summary["agreement_count"] == 42
            and summary["endpoint_support_size"] == 512 - rank
            and summary["nontrivial_quotient_checks"] == 42 * 8
            and summary["minimum_excess_hit_fibers"] >= 1
            and summary["all_nontrivial_quotient_supports_excluded"] is True,
            f"rank-{rank} endpoint quotient-support summary mismatch",
        )
    require(
        low_rank_rank6_a426_projective_pivot["schema_version"]
        == "aperiodic-hankel-eliminant-v1",
        "rank-6 A=426 projective pivot packet schema mismatch",
    )
    require(
        low_rank_rank6_a426_projective_pivot["packet_certificate_schema"]
        == "f17-32-m3-low-rank-rank6-a426-projective-pivot-v1",
        "rank-6 A=426 projective pivot certificate schema mismatch",
    )
    require(
        low_rank_rank6_a426_projective_pivot["sampler"] == "projective_line"
        and low_rank_rank6_a426_projective_pivot["sampler_audit"][
            "denominator"
        ]
        == 17**32 + 1,
        "rank-6 A=426 projective pivot sampler mismatch",
    )
    require(
        low_rank_rank6_a426_projective_pivot["agreement_threshold"] == 426,
        "rank-6 A=426 projective pivot threshold mismatch",
    )
    require(
        low_rank_rank6_a426_projective_pivot["exact_agreements"]
        == [
            {
                "A": 426,
                "charts": [
                    {
                        "chart_id": "projective_infinity",
                        "coverage_ref": (
                            LOW_RANK_RANK6_A426_PROJECTIVE_PIVOT_REF
                            + "#/projective_infinity_coverage"
                        ),
                        "equations_ref": "inline:B=0",
                        "inequations_ref": "inline:A!=0",
                        "pivot_records": [
                            {
                                "dimension": 0,
                                "pivot": (
                                    "projective_infinity_B_zero_A_nonzero"
                                ),
                                "status": "dimension_degree",
                                "variety_degree": 1,
                            }
                        ],
                    }
                ],
                "j": 86,
                "status": "pivot_atlas",
                "t": 170,
            }
        ],
        "rank-6 A=426 projective pivot chart mismatch",
    )
    pivot_coverage = low_rank_rank6_a426_projective_pivot[
        "projective_infinity_coverage"
    ]
    require(
        pivot_coverage["status"] == "nonempty"
        and pivot_coverage["support_count"] == 1
        and pivot_coverage["projective_point"] == "[0:1]"
        and pivot_coverage["rank"] == 6
        and pivot_coverage["A"] == 426
        and pivot_coverage["endpoint_support_size"] == 506
        and pivot_coverage["vandermonde_independence"]["column_count"] == 93
        and pivot_coverage["vandermonde_independence"]["syndrome_length"] == 256,
        "rank-6 A=426 projective pivot coverage mismatch",
    )
    require(
        low_rank_rank6_a426_finite_packet["schema_version"]
        == "aperiodic-hankel-eliminant-v1",
        "rank-6 A=426 finite packet schema mismatch",
    )
    require(
        low_rank_rank6_a426_finite_packet["packet_certificate_schema"]
        == "f17-32-m3-low-rank-rank6-a426-finite-affine-v1",
        "rank-6 A=426 finite packet certificate schema mismatch",
    )
    require(
        low_rank_rank6_a426_finite_packet["sampler"] == "finite_affine_line"
        and low_rank_rank6_a426_finite_packet["sampler_audit"]["denominator"]
        == 17**32,
        "rank-6 A=426 finite packet sampler mismatch",
    )
    require(
        low_rank_rank6_a426_finite_packet["agreement_threshold"] == 426,
        "rank-6 A=426 finite packet threshold mismatch",
    )
    require(
        low_rank_rank6_a426_finite_packet["declared_aperiodic_numerator"] == 1
        and low_rank_rank6_a426_finite_packet["finite_affine_numerator"] == 1
        and len(low_rank_rank6_a426_finite_packet["root_union"]) == 1,
        "rank-6 A=426 finite packet numerator mismatch",
    )
    finite_item = low_rank_rank6_a426_finite_packet["exact_agreements"][0]
    require(
        finite_item["A"] == 426
        and finite_item["j"] == 86
        and finite_item["t"] == 170
        and finite_item["status"] == "regular_minor"
        and finite_item["regular_minor"]["degree"] == 6
        and finite_item["extractor_audit"]["root_count"] == 1
        and finite_item["extractor_audit"]["finite_root_count_certificate"]
        == "frobenius_linear_root_gcd"
        and finite_item["regular_minor_data"]["roots"]
        == low_rank_rank6_a426_finite_packet["root_union"],
        "rank-6 A=426 finite packet agreement mismatch",
    )
    require(
        low_rank_rank6_a426_projective_line_packet["schema_version"]
        == "aperiodic-hankel-eliminant-v1",
        "rank-6 A=426 projective-line packet schema mismatch",
    )
    require(
        low_rank_rank6_a426_projective_line_packet["packet_certificate_schema"]
        == "f17-32-m3-low-rank-rank6-a426-projective-line-v1",
        "rank-6 A=426 projective-line certificate schema mismatch",
    )
    require(
        low_rank_rank6_a426_projective_line_packet["sampler"] == "projective_line"
        and low_rank_rank6_a426_projective_line_packet["sampler_audit"][
            "denominator"
        ]
        == 17**32 + 1,
        "rank-6 A=426 projective-line sampler mismatch",
    )
    require(
        low_rank_rank6_a426_projective_line_packet["agreement_threshold"] == 426,
        "rank-6 A=426 projective-line threshold mismatch",
    )
    require(
        low_rank_rank6_a426_projective_line_packet[
            "declared_aperiodic_numerator"
        ]
        == 2
        and low_rank_rank6_a426_projective_line_packet[
            "finite_affine_numerator"
        ]
        == 1
        and low_rank_rank6_a426_projective_line_packet[
            "projective_infinity_numerator"
        ]
        == 1
        and len(low_rank_rank6_a426_projective_line_packet["root_union"]) == 1,
        "rank-6 A=426 projective-line numerator mismatch",
    )
    projective_line_item = low_rank_rank6_a426_projective_line_packet[
        "exact_agreements"
    ][0]
    projective_line_infinity = projective_line_item["projective_infinity"]
    require(
        projective_line_item["A"] == 426
        and projective_line_item["j"] == 86
        and projective_line_item["t"] == 170
        and projective_line_item["status"] == "regular_minor"
        and projective_line_item["regular_minor"]["degree"] == 6
        and projective_line_item["regular_minor_data"]["roots"]
        == low_rank_rank6_a426_projective_line_packet["root_union"]
        and projective_line_infinity["projective_point"] == "[0:1]"
        and projective_line_infinity["status"] == "nonempty"
        and projective_line_infinity["top_degree"] == 87
        and projective_line_infinity["top_coefficient"] == 0
        and projective_line_infinity["contribution"] == 1,
        "rank-6 A=426 projective-line agreement mismatch",
    )
    require(
        low_rank_rank7_a393_projective_line_packet["schema_version"]
        == "aperiodic-hankel-eliminant-v1",
        "rank-7 A=393 projective-line packet schema mismatch",
    )
    require(
        low_rank_rank7_a393_projective_line_packet["packet_certificate_schema"]
        == "f17-32-m3-low-rank-rank7-a393-projective-line-v1",
        "rank-7 A=393 projective-line certificate schema mismatch",
    )
    require(
        low_rank_rank7_a393_projective_line_packet["sampler"] == "projective_line"
        and low_rank_rank7_a393_projective_line_packet["sampler_audit"][
            "denominator"
        ]
        == 17**32 + 1,
        "rank-7 A=393 projective-line sampler mismatch",
    )
    require(
        low_rank_rank7_a393_projective_line_packet["agreement_threshold"] == 393,
        "rank-7 A=393 projective-line threshold mismatch",
    )
    require(
        low_rank_rank7_a393_projective_line_packet[
            "declared_aperiodic_numerator"
        ]
        == 5
        and low_rank_rank7_a393_projective_line_packet[
            "finite_affine_numerator"
        ]
        == 4
        and low_rank_rank7_a393_projective_line_packet[
            "projective_infinity_numerator"
        ]
        == 1
        and len(low_rank_rank7_a393_projective_line_packet["root_union"]) == 4,
        "rank-7 A=393 projective-line numerator mismatch",
    )
    rank7_projective_line_item = low_rank_rank7_a393_projective_line_packet[
        "exact_agreements"
    ][0]
    rank7_projective_line_infinity = rank7_projective_line_item[
        "projective_infinity"
    ]
    require(
        rank7_projective_line_item["A"] == 393
        and rank7_projective_line_item["j"] == 119
        and rank7_projective_line_item["t"] == 137
        and rank7_projective_line_item["status"] == "regular_minor"
        and rank7_projective_line_item["regular_minor"]["degree"] == 7
        and rank7_projective_line_item["regular_minor_data"]["roots"]
        == low_rank_rank7_a393_projective_line_packet["root_union"]
        and rank7_projective_line_item["regular_minor_data"][
            "linear_root_count_certificate"
        ]["linear_root_count"]
        == 4
        and rank7_projective_line_infinity["projective_point"] == "[0:1]"
        and rank7_projective_line_infinity["status"] == "nonempty"
        and rank7_projective_line_infinity["top_degree"] == 120
        and rank7_projective_line_infinity["top_coefficient"] == 0
        and rank7_projective_line_infinity["contribution"] == 1,
        "rank-7 A=393 projective-line agreement mismatch",
    )
    require(
        low_rank_rank8_a393_projective_line_packet["schema_version"]
        == "aperiodic-hankel-eliminant-v1",
        "rank-8 A=393 projective-line packet schema mismatch",
    )
    require(
        low_rank_rank8_a393_projective_line_packet["packet_certificate_schema"]
        == "f17-32-m3-low-rank-rank8-a393-projective-line-v1",
        "rank-8 A=393 projective-line certificate schema mismatch",
    )
    require(
        low_rank_rank8_a393_projective_line_packet["sampler"] == "projective_line"
        and low_rank_rank8_a393_projective_line_packet["sampler_audit"][
            "denominator"
        ]
        == 17**32 + 1,
        "rank-8 A=393 projective-line sampler mismatch",
    )
    require(
        low_rank_rank8_a393_projective_line_packet["agreement_threshold"] == 393,
        "rank-8 A=393 projective-line threshold mismatch",
    )
    require(
        low_rank_rank8_a393_projective_line_packet[
            "declared_aperiodic_numerator"
        ]
        == 5
        and low_rank_rank8_a393_projective_line_packet[
            "finite_affine_numerator"
        ]
        == 4
        and low_rank_rank8_a393_projective_line_packet[
            "projective_infinity_numerator"
        ]
        == 1
        and len(low_rank_rank8_a393_projective_line_packet["root_union"]) == 4,
        "rank-8 A=393 projective-line numerator mismatch",
    )
    rank8_projective_line_item = low_rank_rank8_a393_projective_line_packet[
        "exact_agreements"
    ][0]
    rank8_projective_line_infinity = rank8_projective_line_item[
        "projective_infinity"
    ]
    require(
        rank8_projective_line_item["A"] == 393
        and rank8_projective_line_item["j"] == 119
        and rank8_projective_line_item["t"] == 137
        and rank8_projective_line_item["status"] == "regular_minor"
        and rank8_projective_line_item["regular_minor"]["degree"] == 8
        and rank8_projective_line_item["regular_minor_data"]["roots"]
        == low_rank_rank8_a393_projective_line_packet["root_union"]
        and rank8_projective_line_item["regular_minor_data"][
            "linear_root_count_certificate"
        ]["linear_root_count"]
        == 4
        and rank8_projective_line_infinity["projective_point"] == "[0:1]"
        and rank8_projective_line_infinity["status"] == "nonempty"
        and rank8_projective_line_infinity["top_degree"] == 120
        and rank8_projective_line_infinity["top_coefficient"] == 0
        and rank8_projective_line_infinity["contribution"] == 1,
        "rank-8 A=393 projective-line agreement mismatch",
    )
    validate_compact_sweep_projective_line_packet(
        low_rank_rank9_a398_projective_line_packet,
        rank=9,
        agreement=398,
        j=114,
        t=142,
        finite_roots=3,
        numerator=4,
    )
    validate_compact_sweep_projective_line_packet(
        low_rank_rank10_a411_projective_line_packet,
        rank=10,
        agreement=411,
        j=101,
        t=155,
        finite_roots=3,
        numerator=4,
    )
    validate_compact_sweep_projective_line_packet(
        low_rank_rank11_a391_projective_line_packet,
        rank=11,
        agreement=391,
        j=121,
        t=135,
        finite_roots=3,
        numerator=4,
    )
    require(
        low_rank6_11_tangent_exclusion["schema_version"]
        == "f17-32-m3-low-rank6-11-tangent-exclusion-v1",
        "rank-6..11 tangent exclusion schema mismatch",
    )
    require(
        low_rank6_11_tangent_exclusion["agreement_range"]
        == [AGREEMENT_MIN, AGREEMENT_MAX],
        "rank-6..11 tangent exclusion window mismatch",
    )
    require(
        low_rank6_11_tangent_exclusion["construction"]["ranks"]
        == [6, 7, 8, 9, 10, 11],
        "rank-6..11 tangent exclusion rank list mismatch",
    )
    require(
        low_rank6_11_tangent_exclusion["aggregate"]["record_count"] == 252
        and low_rank6_11_tangent_exclusion["aggregate"][
            "finite_roots_checked_for_common_code_line"
        ]
        == 238
        and low_rank6_11_tangent_exclusion["aggregate"][
            "common_code_line_tangent_overlap_sum"
        ]
        == 0
        and low_rank6_11_tangent_exclusion["aggregate"][
            "regular_roots_after_common_code_line"
        ]
        == 238,
        "rank-6..11 tangent exclusion aggregate mismatch",
    )
    expected_tangent_checked = {
        "6": 35,
        "7": 43,
        "8": 34,
        "9": 35,
        "10": 47,
        "11": 44,
    }
    for rank, checked in expected_tangent_checked.items():
        summary = low_rank6_11_tangent_exclusion["aggregate"]["rank_summaries"][
            rank
        ]
        require(
            summary["finite_roots_checked_for_common_code_line"] == checked
            and summary["common_code_line_tangent_overlap_sum"] == 0
            and summary["regular_roots_after_common_code_line"] == checked,
            f"rank-{rank} tangent exclusion summary mismatch",
        )
    require(
        low_rank6_11_subfield_exclusion["schema_version"]
        == "f17-32-m3-low-rank6-11-subfield-exclusion-v1",
        "rank-6..11 subfield exclusion schema mismatch",
    )
    require(
        low_rank6_11_subfield_exclusion["agreement_range"]
        == [AGREEMENT_MIN, AGREEMENT_MAX],
        "rank-6..11 subfield exclusion window mismatch",
    )
    require(
        low_rank6_11_subfield_exclusion["construction"]["ranks"]
        == [6, 7, 8, 9, 10, 11],
        "rank-6..11 subfield exclusion rank list mismatch",
    )
    require(
        low_rank6_11_subfield_exclusion["aggregate"]["record_count"] == 252
        and low_rank6_11_subfield_exclusion["aggregate"][
            "finite_roots_checked_for_proper_subfield"
        ]
        == 238
        and low_rank6_11_subfield_exclusion["aggregate"][
            "proper_subfield_overlap_sum"
        ]
        == 0
        and low_rank6_11_subfield_exclusion["aggregate"][
            "regular_roots_after_proper_subfield_exclusion"
        ]
        == 238
        and low_rank6_11_subfield_exclusion["aggregate"][
            "proper_subfield_degrees"
        ]
        == [1, 2, 4, 8, 16],
        "rank-6..11 subfield exclusion aggregate mismatch",
    )
    for rank, checked in expected_tangent_checked.items():
        summary = low_rank6_11_subfield_exclusion["aggregate"]["rank_summaries"][
            rank
        ]
        require(
            summary["finite_roots_checked_for_proper_subfield"] == checked
            and summary["proper_subfield_overlap_sum"] == 0
            and summary["regular_roots_after_proper_subfield_exclusion"] == checked
            and summary["proper_subfield_root_counts"]
            == {"1": 0, "2": 0, "4": 0, "8": 0, "16": 0},
            f"rank-{rank} subfield exclusion summary mismatch",
        )
    require(
        low_rank6_11_known_ledger_table["schema_version"]
        == "f17-32-m3-low-rank6-11-known-ledger-table-v2",
        "rank-6..11 known-ledger table schema mismatch",
    )
    require(
        low_rank6_11_known_ledger_table["agreement_range"]
        == [AGREEMENT_MIN, AGREEMENT_MAX],
        "rank-6..11 known-ledger table window mismatch",
    )
    require(
        low_rank6_11_known_ledger_table["ranks"] == [6, 7, 8, 9, 10, 11],
        "rank-6..11 known-ledger table rank mismatch",
    )
    require(
        low_rank6_11_known_ledger_table["aggregate"]["record_count"] == 252
        and low_rank6_11_known_ledger_table["deterministic_records"][
            "record_count"
        ]
        == 252
        and low_rank6_11_known_ledger_table["aggregate"][
            "finite_regular_root_count_sum"
        ]
        == 238
        and low_rank6_11_known_ledger_table["aggregate"][
            "projective_infinity_contribution_sum"
        ]
        == 252
        and low_rank6_11_known_ledger_table["aggregate"][
            "known_tangent_overlap_removed_sum"
        ]
        == 0
        and low_rank6_11_known_ledger_table["aggregate"][
            "known_proper_subfield_overlap_removed_sum"
        ]
        == 0
        and low_rank6_11_known_ledger_table["aggregate"][
            "projective_endpoint_quotient_support_excluded_sum"
        ]
        == 252
        and low_rank6_11_known_ledger_table["aggregate"][
            "projective_endpoint_quotient_support_status"
        ]
        == "excluded_nontrivial_proper_quotient_remainder_supports"
        and low_rank6_11_known_ledger_table["aggregate"][
            "max_known_residual_projective_per_record"
        ]
        == 5
        and low_rank6_11_known_ledger_table["aggregate"][
            "all_records_within_projective_budget_after_known_ledgers"
        ]
        is True
        and low_rank6_11_known_ledger_table["aggregate"][
            "quotient_support_status"
        ]
        == "endpoint_excluded_finite_roots_not_audited"
        and low_rank6_11_known_ledger_table["aggregate"][
            "quotient_image_status"
        ]
        == "finite_roots_not_audited",
        "rank-6..11 known-ledger aggregate mismatch",
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
    require(
        low_rank_template["schema_version"] == "m1-hankel-low-rank-update-template-v4",
        "low-rank template schema mismatch",
    )
    envelope = low_rank_template["m3_budget_envelope"]
    require(
        envelope["endpoint_conventions"]["finite_budget_numerator"]
        == 17**32 // TWO128,
        "low-rank budget envelope finite budget mismatch",
    )
    require(
        envelope["endpoint_conventions"]["projective_budget_numerator"]
        == (17**32 + 1) // TWO128,
        "low-rank budget envelope projective budget mismatch",
    )
    require(
        [row["update_rank"] for row in envelope["rows"]] == [1, 2, 3, 4, 5, 6],
        "low-rank budget envelope rank range mismatch",
    )
    for row in envelope["rows"]:
        rank = row["update_rank"]
        require(
            row["finite_root_bound"] == rank
            and row["projective_regular_root_bound_without_infinity_exclusion"]
            == rank + 1
            and row["within_finite_budget"] is True
            and row["within_projective_budget_without_infinity_exclusion"]
            == (rank <= 5),
            f"low-rank budget envelope rank {rank} mismatch",
        )
    gate = low_rank_template["m3_low_rank_packet_gate"]
    require(
        gate["status"] == "PROVED / AUDIT"
        and gate["source"] == "m3_budget_envelope",
        "low-rank packet gate status mismatch",
    )
    require(
        gate["finite_safe_update_ranks"] == [1, 2, 3, 4, 5, 6],
        "low-rank packet gate finite-safe ranks mismatch",
    )
    require(
        gate["projective_safe_without_extra_certificate_update_ranks"]
        == [1, 2, 3, 4, 5],
        "low-rank packet gate projective-safe ranks mismatch",
    )
    require(
        gate["projective_requires_extra_certificate_update_ranks"] == [6],
        "low-rank packet gate rank-6 caveat mismatch",
    )
    gate_by_label = {
        item["residual_label"]: item for item in gate["decision_table"]
    }
    require(
        "low_rank_regular_budget_safe" in gate_by_label
        and "rank6_projective_gate_needed" in gate_by_label
        and "singular_bucket" in gate_by_label,
        "low-rank packet gate labels mismatch",
    )
    require(
        "finite-root slack: exact finite root count <= 5"
        in gate["rank6_extra_certificates"],
        "low-rank packet gate missing rank-6 finite-root slack option",
    )


def per_agreement_records(
    plan: dict[str, Any],
    generic: dict[str, Any],
    family: dict[str, Any],
    low_rank_family: dict[str, Any],
    low_rank3_family: dict[str, Any],
    low_rank4_budget_family: dict[str, Any],
    low_rank5_budget_family: dict[str, Any],
    low_rank6_slack_family: dict[str, Any],
    low_rank7_slack_family: dict[str, Any],
    low_rank8_slack_family: dict[str, Any],
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
    low_rank3_family_by_a = {
        int(item["A"]): item for item in low_rank3_family["records"]
    }
    low_rank4_budget_family_by_a = {
        int(item["A"]): item for item in low_rank4_budget_family["records"]
    }
    low_rank5_budget_family_by_a = {
        int(item["A"]): item for item in low_rank5_budget_family["records"]
    }
    low_rank6_slack_family_by_a = {
        int(item["A"]): item for item in low_rank6_slack_family["records"]
    }
    low_rank7_slack_family_by_a = {
        int(item["A"]): item for item in low_rank7_slack_family["records"]
    }
    low_rank8_slack_family_by_a = {
        int(item["A"]): item for item in low_rank8_slack_family["records"]
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
        low_rank3_item = low_rank3_family_by_a[agreement]
        low_rank4_item = low_rank4_budget_family_by_a[agreement]
        low_rank5_item = low_rank5_budget_family_by_a[agreement]
        low_rank6_item = low_rank6_slack_family_by_a[agreement]
        low_rank7_item = low_rank7_slack_family_by_a[agreement]
        low_rank8_item = low_rank8_slack_family_by_a[agreement]
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
            low_rank_item["projective_infinity"]["status"]
            == "nonempty_not_excluded_by_regular_minor"
            and low_rank_item["projective_infinity"]["contribution"] == 1,
            f"A={agreement}: low-rank projective endpoint mismatch",
        )
        require(
            low_rank_item["regular_budget_table"]["within_finite_budget"] is True
            and low_rank_item["regular_budget_table"]["within_projective_budget"]
            is True
            and low_rank_item["regular_budget_table"]["projective_regular_roots"]
            == low_rank_item["root_count"] + 1,
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
            low_rank3_item["degree_bound"] == 3
            and low_rank3_item["root_status"]
            in {
                "exact_no_finite_roots",
                "exact_one_finite_root",
                "exact_two_finite_roots",
                "exact_three_finite_roots_count_only",
            }
            and low_rank3_item["root_count"] in {0, 1, 2, 3},
            f"A={agreement}: rank-3 low-rank family status mismatch",
        )
        require(
            low_rank3_item["linear_root_count_certificate"]["kind"]
            == "frobenius_linear_root_gcd"
            and low_rank3_item["linear_root_count_certificate"][
                "linear_root_count"
            ]
            == low_rank3_item["root_count"],
            f"A={agreement}: rank-3 low-rank root-count certificate mismatch",
        )
        if low_rank3_item["root_count"] < 3:
            require(
                low_rank3_item["listed_roots"] is not None
                and len(low_rank3_item["listed_roots"])
                == low_rank3_item["root_count"],
                f"A={agreement}: rank-3 listed root count mismatch",
            )
        else:
            require(
                low_rank3_item["listed_roots"] is None,
                f"A={agreement}: rank-3 split cubic should be count-only",
            )
        require(
            low_rank3_item["projective_infinity"]["status"]
            == "nonempty_not_excluded_by_regular_minor"
            and low_rank3_item["projective_infinity"]["contribution"] == 1,
            f"A={agreement}: rank-3 low-rank projective endpoint mismatch",
        )
        require(
            low_rank3_item["regular_budget_table"]["within_finite_budget"] is True
            and low_rank3_item["regular_budget_table"]["within_projective_budget"]
            is True
            and low_rank3_item["regular_budget_table"]["projective_regular_roots"]
            == low_rank3_item["root_count"] + 1,
            f"A={agreement}: rank-3 low-rank budget table mismatch",
        )
        require(
            low_rank3_item["tangent_common_code_line_audit"]["overlap_count"] == 0
            and low_rank3_item["tangent_common_code_line_audit"][
                "finite_roots_checked"
            ]
            == low_rank3_item["root_count"]
            and low_rank3_item["tangent_common_code_line_audit"][
                "method"
            ]
            == "frobenius_gcd_exclusion_at_moment_0",
            f"A={agreement}: rank-3 low-rank tangent audit mismatch",
        )
        require(
            low_rank4_item["degree_bound"] == 4
            and low_rank4_item["polynomial_degree"] == 4
            and low_rank4_item["root_count_status"]
            == "not_enumerated_degree_bound_sufficient",
            f"A={agreement}: rank-4 low-rank budget family status mismatch",
        )
        require(
            low_rank4_item["projective_infinity"]["status"]
            == "nonempty_not_excluded_by_regular_minor"
            and low_rank4_item["projective_infinity"]["contribution"] == 1,
            f"A={agreement}: rank-4 low-rank projective endpoint mismatch",
        )
        require(
            low_rank4_item["regular_budget_table"]["finite_affine_roots_bound"]
            == 4
            and low_rank4_item["regular_budget_table"][
                "projective_regular_roots_bound"
            ]
            == 5
            and low_rank4_item["regular_budget_table"]["within_finite_budget"]
            is True
            and low_rank4_item["regular_budget_table"]["within_projective_budget"]
            is True,
            f"A={agreement}: rank-4 low-rank budget table mismatch",
        )
        require(
            low_rank5_item["degree_bound"] == 5
            and low_rank5_item["polynomial_degree"] == 5
            and low_rank5_item["root_count_status"]
            == "not_enumerated_degree_bound_sufficient",
            f"A={agreement}: rank-5 low-rank budget family status mismatch",
        )
        require(
            low_rank5_item["projective_infinity"]["status"]
            == "nonempty_not_excluded_by_regular_minor"
            and low_rank5_item["projective_infinity"]["contribution"] == 1,
            f"A={agreement}: rank-5 low-rank projective endpoint mismatch",
        )
        require(
            low_rank5_item["regular_budget_table"]["finite_affine_roots_bound"]
            == 5
            and low_rank5_item["regular_budget_table"][
                "projective_regular_roots_bound"
            ]
            == 6
            and low_rank5_item["regular_budget_table"]["within_finite_budget"]
            is True
            and low_rank5_item["regular_budget_table"]["within_projective_budget"]
            is True,
            f"A={agreement}: rank-5 low-rank budget table mismatch",
        )
        require(
            low_rank6_item["degree_bound"] == 6
            and low_rank6_item["polynomial_degree"] == 6
            and low_rank6_item["root_count"] in {0, 1, 2}
            and low_rank6_item["linear_root_count_certificate"][
                "linear_root_count"
            ]
            == low_rank6_item["root_count"],
            f"A={agreement}: rank-6 low-rank slack family status mismatch",
        )
        require(
            low_rank6_item["listed_roots"] is not None
            and len(low_rank6_item["listed_roots"]) == low_rank6_item["root_count"],
            f"A={agreement}: rank-6 listed root mismatch",
        )
        require(
            low_rank6_item["projective_infinity"]["status"]
            == "nonempty_not_excluded_by_regular_minor"
            and low_rank6_item["projective_infinity"]["contribution"] == 1,
            f"A={agreement}: rank-6 low-rank projective endpoint mismatch",
        )
        require(
            low_rank6_item["regular_budget_table"]["degree_only_projective_bound"]
            == 7
            and low_rank6_item["regular_budget_table"][
                "degree_only_projective_budget_gap"
            ]
            == -1
            and low_rank6_item["regular_budget_table"][
                "projective_regular_roots"
            ]
            == low_rank6_item["root_count"] + 1
            and low_rank6_item["regular_budget_table"]["within_finite_budget"]
            is True
            and low_rank6_item["regular_budget_table"]["within_projective_budget"]
            is True,
            f"A={agreement}: rank-6 low-rank slack budget table mismatch",
        )
        require(
            low_rank7_item["degree_bound"] == 7
            and low_rank7_item["polynomial_degree"] == 7
            and low_rank7_item["root_count"] in {0, 1, 2, 3, 4}
            and low_rank7_item["linear_root_count_certificate"][
                "linear_root_count"
            ]
            == low_rank7_item["root_count"],
            f"A={agreement}: rank-7 low-rank slack family status mismatch",
        )
        if low_rank7_item["root_count"] <= 2:
            require(
                low_rank7_item["listed_roots"] is not None
                and len(low_rank7_item["listed_roots"])
                == low_rank7_item["root_count"],
                f"A={agreement}: rank-7 listed root mismatch",
            )
        else:
            require(
                low_rank7_item["listed_roots"] is None,
                f"A={agreement}: rank-7 high-degree root list should be count-only",
            )
        require(
            low_rank7_item["projective_infinity"]["status"]
            == "nonempty_not_excluded_by_regular_minor"
            and low_rank7_item["projective_infinity"]["contribution"] == 1,
            f"A={agreement}: rank-7 low-rank projective endpoint mismatch",
        )
        require(
            low_rank7_item["regular_budget_table"]["degree_only_projective_bound"]
            == 8
            and low_rank7_item["regular_budget_table"][
                "degree_only_projective_budget_gap"
            ]
            == -2
            and low_rank7_item["regular_budget_table"][
                "projective_regular_roots"
            ]
            == low_rank7_item["root_count"] + 1
            and low_rank7_item["regular_budget_table"]["within_finite_budget"]
            is True
            and low_rank7_item["regular_budget_table"]["within_projective_budget"]
            is True,
            f"A={agreement}: rank-7 low-rank slack budget table mismatch",
        )
        require(
            low_rank8_item["degree_bound"] == 8
            and low_rank8_item["polynomial_degree"] == 8
            and low_rank8_item["root_count"] in {0, 1, 2, 3, 4}
            and low_rank8_item["linear_root_count_certificate"][
                "linear_root_count"
            ]
            == low_rank8_item["root_count"],
            f"A={agreement}: rank-8 low-rank slack family status mismatch",
        )
        if low_rank8_item["root_count"] <= 2:
            require(
                low_rank8_item["listed_roots"] is not None
                and len(low_rank8_item["listed_roots"])
                == low_rank8_item["root_count"],
                f"A={agreement}: rank-8 listed root mismatch",
            )
        else:
            require(
                low_rank8_item["listed_roots"] is None,
                f"A={agreement}: rank-8 high-degree root list should be count-only",
            )
        require(
            low_rank8_item["projective_infinity"]["status"]
            == "nonempty_not_excluded_by_regular_minor"
            and low_rank8_item["projective_infinity"]["contribution"] == 1,
            f"A={agreement}: rank-8 low-rank projective endpoint mismatch",
        )
        require(
            low_rank8_item["regular_budget_table"]["degree_only_projective_bound"]
            == 9
            and low_rank8_item["regular_budget_table"][
                "degree_only_projective_budget_gap"
            ]
            == -3
            and low_rank8_item["regular_budget_table"][
                "projective_regular_roots"
            ]
            == low_rank8_item["root_count"] + 1
            and low_rank8_item["regular_budget_table"]["within_finite_budget"]
            is True
            and low_rank8_item["regular_budget_table"]["within_projective_budget"]
            is True,
            f"A={agreement}: rank-8 low-rank slack budget table mismatch",
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
                "synthetic_low_rank2_projective_infinity_contribution": 1,
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
                "synthetic_low_rank3_family_status": (
                    "rank-3 prefix update witness has exact finite-root "
                    "counts from the Frobenius gcd"
                ),
                "synthetic_low_rank3_root_bound": low_rank3_item["degree_bound"],
                "synthetic_low_rank3_root_count": low_rank3_item["root_count"],
                "synthetic_low_rank3_root_status": low_rank3_item["root_status"],
                "synthetic_low_rank3_projective_infinity_contribution": 1,
                "synthetic_low_rank3_projective_regular_roots": low_rank3_item[
                    "regular_budget_table"
                ]["projective_regular_roots"],
                "synthetic_low_rank3_projective_budget_gap": low_rank3_item[
                    "regular_budget_table"
                ]["projective_budget_gap"],
                "synthetic_low_rank3_B_tan_common_code_line": 0,
                "synthetic_low_rank3_roots_after_common_code_line": low_rank3_item[
                    "regular_budget_table"
                ]["regular_roots_after_common_code_line"],
                "synthetic_low_rank3_tangent_method": low_rank3_item[
                    "tangent_common_code_line_audit"
                ]["method"],
                "synthetic_low_rank3_sidecar_hash": low_rank3_item["sidecar_hash"],
                "synthetic_low_rank4_budget_family_status": (
                    "rank-4 prefix update witness has degree 4 and is "
                    "projective-budget safe by the v4 low-rank packet gate"
                ),
                "synthetic_low_rank4_root_bound": low_rank4_item["degree_bound"],
                "synthetic_low_rank4_root_count_status": low_rank4_item[
                    "root_count_status"
                ],
                "synthetic_low_rank4_projective_infinity_contribution": 1,
                "synthetic_low_rank4_projective_regular_roots_bound": (
                    low_rank4_item["regular_budget_table"][
                        "projective_regular_roots_bound"
                    ]
                ),
                "synthetic_low_rank4_projective_budget_gap": low_rank4_item[
                    "regular_budget_table"
                ]["projective_budget_gap"],
                "synthetic_low_rank4_sidecar_hash": low_rank4_item["sidecar_hash"],
                "synthetic_low_rank5_budget_family_status": (
                    "rank-5 prefix update witness has degree 5 and is exactly "
                    "projective-budget safe by the v4 low-rank packet gate"
                ),
                "synthetic_low_rank5_root_bound": low_rank5_item["degree_bound"],
                "synthetic_low_rank5_root_count_status": low_rank5_item[
                    "root_count_status"
                ],
                "synthetic_low_rank5_projective_infinity_contribution": 1,
                "synthetic_low_rank5_projective_regular_roots_bound": (
                    low_rank5_item["regular_budget_table"][
                        "projective_regular_roots_bound"
                    ]
                ),
                "synthetic_low_rank5_projective_budget_gap": low_rank5_item[
                    "regular_budget_table"
                ]["projective_budget_gap"],
                "synthetic_low_rank5_sidecar_hash": low_rank5_item["sidecar_hash"],
                "synthetic_low_rank6_slack_family_status": (
                    "rank-6 prefix update witness has exact finite-root slack "
                    "from the Frobenius gcd"
                ),
                "synthetic_low_rank6_root_bound": low_rank6_item["degree_bound"],
                "synthetic_low_rank6_root_count": low_rank6_item["root_count"],
                "synthetic_low_rank6_root_status": low_rank6_item["root_status"],
                "synthetic_low_rank6_projective_infinity_contribution": 1,
                "synthetic_low_rank6_projective_regular_roots": low_rank6_item[
                    "regular_budget_table"
                ]["projective_regular_roots"],
                "synthetic_low_rank6_projective_budget_gap": low_rank6_item[
                    "regular_budget_table"
                ]["projective_budget_gap"],
                "synthetic_low_rank6_degree_only_projective_gap": low_rank6_item[
                    "regular_budget_table"
                ]["degree_only_projective_budget_gap"],
                "synthetic_low_rank6_sidecar_hash": low_rank6_item["sidecar_hash"],
                "synthetic_low_rank7_slack_family_status": (
                    "rank-7 prefix update witness has exact finite-root slack "
                    "beyond the low-rank degree envelope"
                ),
                "synthetic_low_rank7_root_bound": low_rank7_item["degree_bound"],
                "synthetic_low_rank7_root_count": low_rank7_item["root_count"],
                "synthetic_low_rank7_root_status": low_rank7_item["root_status"],
                "synthetic_low_rank7_projective_infinity_contribution": 1,
                "synthetic_low_rank7_projective_regular_roots": low_rank7_item[
                    "regular_budget_table"
                ]["projective_regular_roots"],
                "synthetic_low_rank7_projective_budget_gap": low_rank7_item[
                    "regular_budget_table"
                ]["projective_budget_gap"],
                "synthetic_low_rank7_degree_only_projective_gap": low_rank7_item[
                    "regular_budget_table"
                ]["degree_only_projective_budget_gap"],
                "synthetic_low_rank7_sidecar_hash": low_rank7_item["sidecar_hash"],
                "synthetic_low_rank8_slack_family_status": (
                    "rank-8 prefix update witness has exact finite-root slack "
                    "beyond the low-rank degree envelope"
                ),
                "synthetic_low_rank8_root_bound": low_rank8_item["degree_bound"],
                "synthetic_low_rank8_root_count": low_rank8_item["root_count"],
                "synthetic_low_rank8_root_status": low_rank8_item["root_status"],
                "synthetic_low_rank8_projective_infinity_contribution": 1,
                "synthetic_low_rank8_projective_regular_roots": low_rank8_item[
                    "regular_budget_table"
                ]["projective_regular_roots"],
                "synthetic_low_rank8_projective_budget_gap": low_rank8_item[
                    "regular_budget_table"
                ]["projective_budget_gap"],
                "synthetic_low_rank8_degree_only_projective_gap": low_rank8_item[
                    "regular_budget_table"
                ]["degree_only_projective_budget_gap"],
                "synthetic_low_rank8_sidecar_hash": low_rank8_item["sidecar_hash"],
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
    low_rank3_family = load_json(LOW_RANK3_FAMILY_REF)
    low_rank4_budget_family = load_json(LOW_RANK4_BUDGET_FAMILY_REF)
    low_rank5_budget_family = load_json(LOW_RANK5_BUDGET_FAMILY_REF)
    low_rank6_slack_family = load_json(LOW_RANK6_SLACK_FAMILY_REF)
    low_rank7_slack_family = load_json(LOW_RANK7_SLACK_FAMILY_REF)
    low_rank8_slack_family = load_json(LOW_RANK8_SLACK_FAMILY_REF)
    low_rank9_11_slack_sweep = load_json(LOW_RANK9_11_SLACK_SWEEP_REF)
    low_rank2_11_projective_infinity = load_json(
        LOW_RANK2_11_PROJECTIVE_INFINITY_REF
    )
    low_rank2_11_endpoint_quotient_support = load_json(
        LOW_RANK2_11_ENDPOINT_QUOTIENT_SUPPORT_REF
    )
    low_rank_rank6_a426_projective_pivot = load_json(
        LOW_RANK_RANK6_A426_PROJECTIVE_PIVOT_REF
    )
    low_rank_rank6_a426_finite_packet = load_json(
        LOW_RANK_RANK6_A426_FINITE_PACKET_REF
    )
    low_rank_rank6_a426_projective_line_packet = load_json(
        LOW_RANK_RANK6_A426_PROJECTIVE_LINE_PACKET_REF
    )
    low_rank_rank7_a393_projective_line_packet = load_json(
        LOW_RANK_RANK7_A393_PROJECTIVE_LINE_PACKET_REF
    )
    low_rank_rank8_a393_projective_line_packet = load_json(
        LOW_RANK_RANK8_A393_PROJECTIVE_LINE_PACKET_REF
    )
    low_rank_rank9_a398_projective_line_packet = load_json(
        LOW_RANK_RANK9_A398_PROJECTIVE_LINE_PACKET_REF
    )
    low_rank_rank10_a411_projective_line_packet = load_json(
        LOW_RANK_RANK10_A411_PROJECTIVE_LINE_PACKET_REF
    )
    low_rank_rank11_a391_projective_line_packet = load_json(
        LOW_RANK_RANK11_A391_PROJECTIVE_LINE_PACKET_REF
    )
    low_rank6_11_tangent_exclusion = load_json(
        LOW_RANK6_11_TANGENT_EXCLUSION_REF
    )
    low_rank6_11_subfield_exclusion = load_json(
        LOW_RANK6_11_SUBFIELD_EXCLUSION_REF
    )
    low_rank6_11_known_ledger_table = load_json(
        LOW_RANK6_11_KNOWN_LEDGER_TABLE_REF
    )
    top_packet = load_json(TOP_PACKET_REF)
    line_value_lift = load_json(LINE_VALUE_LIFT_REF)
    subgroup_section = load_json(SUBGROUP_SECTION_REF)
    syndrome_realizability = load_json(SYNDROME_REALIZABILITY_REF)
    zero_slope_subtraction = load_json(ZERO_SLOPE_SUBTRACTION_REF)
    extension_denominator_audit = load_json(EXTENSION_DENOMINATOR_AUDIT_REF)
    projective_endpoint_audit = load_json(PROJECTIVE_ENDPOINT_AUDIT_REF)
    proportional_lemma = load_json(PROPORTIONAL_LEMMA_REF)
    low_rank_template = load_json(LOW_RANK_TEMPLATE_REF)
    validate_inputs(
        plan,
        generic,
        family,
        low_rank_family,
        low_rank3_family,
        low_rank4_budget_family,
        low_rank5_budget_family,
        low_rank6_slack_family,
        low_rank7_slack_family,
        low_rank8_slack_family,
        low_rank9_11_slack_sweep,
        low_rank2_11_projective_infinity,
        low_rank2_11_endpoint_quotient_support,
        low_rank_rank6_a426_projective_pivot,
        low_rank_rank6_a426_finite_packet,
        low_rank_rank6_a426_projective_line_packet,
        low_rank_rank7_a393_projective_line_packet,
        low_rank_rank8_a393_projective_line_packet,
        low_rank_rank9_a398_projective_line_packet,
        low_rank_rank10_a411_projective_line_packet,
        low_rank_rank11_a391_projective_line_packet,
        low_rank6_11_tangent_exclusion,
        low_rank6_11_subfield_exclusion,
        low_rank6_11_known_ledger_table,
        top_packet,
        line_value_lift,
        subgroup_section,
        syndrome_realizability,
        zero_slope_subtraction,
        extension_denominator_audit,
        projective_endpoint_audit,
        proportional_lemma,
        low_rank_template,
    )
    records = per_agreement_records(
        plan,
        generic,
        family,
        low_rank_family,
        low_rank3_family,
        low_rank4_budget_family,
        low_rank5_budget_family,
        low_rank6_slack_family,
        low_rank7_slack_family,
        low_rank8_slack_family,
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
            "f17-32-m3-low-rank2-family-v5",
        ),
        artifact_record(
            "synthetic_low_rank3_family",
            LOW_RANK3_FAMILY_REF,
            "f17-32-m3-low-rank3-family-v2",
        ),
        artifact_record(
            "synthetic_low_rank4_budget_family",
            LOW_RANK4_BUDGET_FAMILY_REF,
            "f17-32-m3-low-rank4-budget-family-v1",
        ),
        artifact_record(
            "synthetic_low_rank5_budget_family",
            LOW_RANK5_BUDGET_FAMILY_REF,
            "f17-32-m3-low-rank5-budget-family-v1",
        ),
        artifact_record(
            "synthetic_low_rank6_slack_family",
            LOW_RANK6_SLACK_FAMILY_REF,
            "f17-32-m3-low-rank6-slack-family-v1",
        ),
        artifact_record(
            "synthetic_low_rank7_slack_family",
            LOW_RANK7_SLACK_FAMILY_REF,
            "f17-32-m3-low-rank7-slack-family-v1",
        ),
        artifact_record(
            "synthetic_low_rank8_slack_family",
            LOW_RANK8_SLACK_FAMILY_REF,
            "f17-32-m3-low-rank8-slack-family-v1",
        ),
        artifact_record(
            "synthetic_low_rank9_11_slack_sweep",
            LOW_RANK9_11_SLACK_SWEEP_REF,
            "f17-32-m3-low-rank9-11-slack-sweep-v1",
        ),
        artifact_record(
            "synthetic_low_rank2_11_projective_infinity",
            LOW_RANK2_11_PROJECTIVE_INFINITY_REF,
            "f17-32-m3-low-rank2-11-projective-infinity-v1",
        ),
        artifact_record(
            "synthetic_low_rank2_11_endpoint_quotient_support",
            LOW_RANK2_11_ENDPOINT_QUOTIENT_SUPPORT_REF,
            "f17-32-m3-low-rank2-11-endpoint-quotient-support-v1",
        ),
        artifact_record(
            "synthetic_low_rank_rank6_a426_projective_pivot",
            LOW_RANK_RANK6_A426_PROJECTIVE_PIVOT_REF,
            "aperiodic-hankel-eliminant-v1",
        ),
        artifact_record(
            "synthetic_low_rank_rank6_a426_finite_affine_packet",
            LOW_RANK_RANK6_A426_FINITE_PACKET_REF,
            "aperiodic-hankel-eliminant-v1",
        ),
        artifact_record(
            "synthetic_low_rank_rank6_a426_projective_line_packet",
            LOW_RANK_RANK6_A426_PROJECTIVE_LINE_PACKET_REF,
            "aperiodic-hankel-eliminant-v1",
        ),
        artifact_record(
            "synthetic_low_rank_rank7_a393_projective_line_packet",
            LOW_RANK_RANK7_A393_PROJECTIVE_LINE_PACKET_REF,
            "aperiodic-hankel-eliminant-v1",
        ),
        artifact_record(
            "synthetic_low_rank_rank8_a393_projective_line_packet",
            LOW_RANK_RANK8_A393_PROJECTIVE_LINE_PACKET_REF,
            "aperiodic-hankel-eliminant-v1",
        ),
        artifact_record(
            "synthetic_low_rank_rank9_a398_projective_line_packet",
            LOW_RANK_RANK9_A398_PROJECTIVE_LINE_PACKET_REF,
            "aperiodic-hankel-eliminant-v1",
        ),
        artifact_record(
            "synthetic_low_rank_rank10_a411_projective_line_packet",
            LOW_RANK_RANK10_A411_PROJECTIVE_LINE_PACKET_REF,
            "aperiodic-hankel-eliminant-v1",
        ),
        artifact_record(
            "synthetic_low_rank_rank11_a391_projective_line_packet",
            LOW_RANK_RANK11_A391_PROJECTIVE_LINE_PACKET_REF,
            "aperiodic-hankel-eliminant-v1",
        ),
        artifact_record(
            "synthetic_low_rank6_11_tangent_exclusion",
            LOW_RANK6_11_TANGENT_EXCLUSION_REF,
            "f17-32-m3-low-rank6-11-tangent-exclusion-v1",
        ),
        artifact_record(
            "synthetic_low_rank6_11_subfield_exclusion",
            LOW_RANK6_11_SUBFIELD_EXCLUSION_REF,
            "f17-32-m3-low-rank6-11-subfield-exclusion-v1",
        ),
        artifact_record(
            "synthetic_low_rank6_11_known_ledger_table",
            LOW_RANK6_11_KNOWN_LEDGER_TABLE_REF,
            "f17-32-m3-low-rank6-11-known-ledger-table-v2",
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
        artifact_record(
            "hankel_low_rank_update_template",
            LOW_RANK_TEMPLATE_REF,
            "m1-hankel-low-rank-update-template-v4",
        ),
    ]
    low_rank_envelope = low_rank_template["m3_budget_envelope"]
    low_rank_gate = low_rank_template["m3_low_rank_packet_gate"]
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
            "synthetic_low_rank2_projective_infinity_contribution": 42,
            "synthetic_low_rank2_max_projective_regular_roots_per_agreement": (
                low_rank_family["aggregate"][
                    "max_projective_regular_roots_per_agreement"
                ]
            ),
            "synthetic_low_rank2_projective_budget_status": (
                "all 42 rows have at most 3 projective regular roots after "
                "including the nonexcluded infinity point, below projective "
                "budget numerator 6"
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
            "synthetic_low_rank3_family_status": (
                "proved exact Frobenius-gcd finite-root counts for all 42 "
                "rank-3 synthetic pencils"
            ),
            "synthetic_low_rank3_degree_bound_sum": low_rank3_family["aggregate"][
                "degree_bound_sum"
            ],
            "synthetic_low_rank3_exact_root_count_sum": low_rank3_family[
                "aggregate"
            ]["exact_regular_root_count_sum"],
            "synthetic_low_rank3_root_count_histogram": low_rank3_family[
                "aggregate"
            ]["linear_root_count_histogram"],
            "synthetic_low_rank3_projective_infinity_contribution": 42,
            "synthetic_low_rank3_max_projective_regular_roots_per_agreement": (
                low_rank3_family["aggregate"][
                    "max_projective_regular_roots_per_agreement"
                ]
            ),
            "synthetic_low_rank3_projective_budget_status": (
                "all 42 rows have at most 4 projective regular roots after "
                "including the nonexcluded infinity point, below projective "
                "budget numerator 6"
            ),
            "synthetic_low_rank3_common_code_line_tangent_overlap": 0,
            "synthetic_low_rank3_roots_after_common_code_line": (
                low_rank3_family["aggregate"][
                    "exact_regular_roots_after_common_code_line"
                ]
            ),
            "synthetic_low_rank3_tangent_status": (
                "the Frobenius gcd is nonzero at the only possible "
                "common-code-line slope from Syn_0(u+zv)=|X|+3z, so none "
                "of the 42 finite roots are common-code-line tangent roots"
            ),
            "synthetic_low_rank4_budget_family_status": (
                "proved degree-4 low-rank budget certificates for all 42 "
                "rank-4 synthetic pencils"
            ),
            "synthetic_low_rank4_degree_bound_sum": (
                low_rank4_budget_family["aggregate"]["degree_bound_sum"]
            ),
            "synthetic_low_rank4_max_projective_regular_roots_per_agreement_bound": (
                low_rank4_budget_family["aggregate"][
                    "max_projective_regular_roots_per_agreement_bound"
                ]
            ),
            "synthetic_low_rank4_projective_budget_status": (
                "all 42 rows have at most 5 projective regular roots after "
                "including the nonexcluded infinity point, below projective "
                "budget numerator 6; exact finite roots are not enumerated"
            ),
            "synthetic_low_rank5_budget_family_status": (
                "proved degree-5 low-rank budget certificates for all 42 "
                "rank-5 synthetic pencils"
            ),
            "synthetic_low_rank5_degree_bound_sum": (
                low_rank5_budget_family["aggregate"]["degree_bound_sum"]
            ),
            "synthetic_low_rank5_max_projective_regular_roots_per_agreement_bound": (
                low_rank5_budget_family["aggregate"][
                    "max_projective_regular_roots_per_agreement_bound"
                ]
            ),
            "synthetic_low_rank5_projective_budget_status": (
                "all 42 rows have at most 6 projective regular roots after "
                "including the nonexcluded infinity point, exactly meeting "
                "projective budget numerator 6; exact finite roots are not "
                "enumerated"
            ),
            "synthetic_low_rank6_slack_family_status": (
                "proved exact Frobenius-gcd finite-root slack for all 42 "
                "rank-6 synthetic pencils"
            ),
            "synthetic_low_rank6_degree_bound_sum": (
                low_rank6_slack_family["aggregate"]["degree_bound_sum"]
            ),
            "synthetic_low_rank6_exact_root_count_sum": (
                low_rank6_slack_family["aggregate"][
                    "exact_regular_root_count_sum"
                ]
            ),
            "synthetic_low_rank6_root_count_histogram": (
                low_rank6_slack_family["aggregate"][
                    "linear_root_count_histogram"
                ]
            ),
            "synthetic_low_rank6_max_projective_regular_roots_per_agreement": (
                low_rank6_slack_family["aggregate"][
                    "max_projective_regular_roots_per_agreement"
                ]
            ),
            "synthetic_low_rank6_projective_budget_status": (
                "degree-only projective accounting gives 7 > 6, but exact "
                "finite-root slack lowers every row to at most 3 projective "
                "regular roots"
            ),
            "synthetic_low_rank7_slack_family_status": (
                "proved exact Frobenius-gcd finite-root slack beyond the "
                "degree envelope for all 42 rank-7 synthetic pencils"
            ),
            "synthetic_low_rank7_degree_bound_sum": (
                low_rank7_slack_family["aggregate"]["degree_bound_sum"]
            ),
            "synthetic_low_rank7_exact_root_count_sum": (
                low_rank7_slack_family["aggregate"][
                    "exact_regular_root_count_sum"
                ]
            ),
            "synthetic_low_rank7_root_count_histogram": (
                low_rank7_slack_family["aggregate"][
                    "linear_root_count_histogram"
                ]
            ),
            "synthetic_low_rank7_max_projective_regular_roots_per_agreement": (
                low_rank7_slack_family["aggregate"][
                    "max_projective_regular_roots_per_agreement"
                ]
            ),
            "synthetic_low_rank7_projective_budget_status": (
                "degree-only projective accounting gives 8 > 6, but exact "
                "finite-root slack lowers every row to at most 5 projective "
                "regular roots"
            ),
            "synthetic_low_rank8_slack_family_status": (
                "proved exact Frobenius-gcd finite-root slack beyond the "
                "degree envelope for all 42 rank-8 synthetic pencils"
            ),
            "synthetic_low_rank8_degree_bound_sum": (
                low_rank8_slack_family["aggregate"]["degree_bound_sum"]
            ),
            "synthetic_low_rank8_exact_root_count_sum": (
                low_rank8_slack_family["aggregate"][
                    "exact_regular_root_count_sum"
                ]
            ),
            "synthetic_low_rank8_root_count_histogram": (
                low_rank8_slack_family["aggregate"][
                    "linear_root_count_histogram"
                ]
            ),
            "synthetic_low_rank8_max_projective_regular_roots_per_agreement": (
                low_rank8_slack_family["aggregate"][
                    "max_projective_regular_roots_per_agreement"
                ]
            ),
            "synthetic_low_rank8_projective_budget_status": (
                "degree-only projective accounting gives 9 > 6, but exact "
                "finite-root slack lowers every row to at most 5 projective "
                "regular roots"
            ),
            "synthetic_low_rank9_11_slack_sweep_status": (
                "proved exact Frobenius-gcd finite-root slack for all 126 "
                "rank/agreement pairs in ranks 9..11"
            ),
            "synthetic_low_rank9_11_rank_summaries": (
                low_rank9_11_slack_sweep["aggregate"]["rank_summaries"]
            ),
            "synthetic_low_rank9_11_max_projective_regular_roots_over_sweep": (
                low_rank9_11_slack_sweep["aggregate"][
                    "max_projective_regular_roots_over_sweep"
                ]
            ),
            "synthetic_low_rank9_11_projective_budget_status": (
                "degree-only projective accounting gives 10, 11, and 12 > 6, "
                "but exact finite-root slack lowers every checked pair to at "
                "most 4 projective regular roots"
            ),
            "synthetic_low_rank2_11_projective_infinity_status": (
                "proved that the projective endpoint [0:1] is an actual "
                "support-wise noncontained endpoint for every rank/agreement "
                "row in the synthetic low-rank ladder at ranks 2..11"
            ),
            "synthetic_low_rank2_11_projective_infinity_rank_summaries": (
                low_rank2_11_projective_infinity["aggregate"]["rank_summaries"]
            ),
            "synthetic_low_rank2_11_projective_infinity_support_minimum": (
                low_rank2_11_projective_infinity["aggregate"][
                    "minimum_endpoint_support_size"
                ]
            ),
            "synthetic_low_rank2_11_projective_infinity_contribution_sum": (
                low_rank2_11_projective_infinity["aggregate"][
                    "projective_infinity_contribution_sum"
                ]
            ),
            "synthetic_low_rank2_11_endpoint_quotient_support_status": (
                "proved that the actual endpoint support D minus Y is not a "
                "nontrivial proper quotient-remainder support for every "
                "rank/agreement row in the synthetic low-rank ladder"
            ),
            "synthetic_low_rank2_11_endpoint_quotient_support_rank_summaries": (
                low_rank2_11_endpoint_quotient_support["aggregate"][
                    "rank_summaries"
                ]
            ),
            "synthetic_low_rank2_11_endpoint_quotient_support_fiber_sizes": (
                low_rank2_11_endpoint_quotient_support["aggregate"][
                    "nontrivial_fiber_sizes"
                ]
            ),
            "synthetic_low_rank2_11_endpoint_quotient_support_min_excess": (
                low_rank2_11_endpoint_quotient_support["aggregate"][
                    "minimum_excess_hit_fibers"
                ]
            ),
            "synthetic_low_rank2_11_endpoint_quotient_support_nonclaim": (
                "trivial quotient fiber sizes c=1 and c=512, finite affine "
                "regular-minor roots, and quotient-image supports are not "
                "audited by this endpoint support certificate"
            ),
            "synthetic_low_rank_rank6_a426_projective_pivot_status": (
                "v9 projective-line pivot_atlas packet checks the rank-6 "
                "A=426 projective_infinity chart as nonempty with support_count "
                "1, using the same Vandermonde endpoint witness"
            ),
            "synthetic_low_rank_rank6_a426_projective_pivot_support": (
                low_rank_rank6_a426_projective_pivot[
                    "projective_infinity_coverage"
                ]["endpoint_support_size"]
            ),
            "synthetic_low_rank_rank6_a426_finite_packet_status": (
                "v9 finite-affine regular-minor packet checks the rank-6 "
                "A=426 low-rank row with degree 6 and one exact finite root, "
                "certified by gcd(Delta,Z^q-Z)"
            ),
            "synthetic_low_rank_rank6_a426_finite_packet_root_union": (
                low_rank_rank6_a426_finite_packet["root_union"]
            ),
            "synthetic_low_rank_rank6_a426_finite_packet_numerator": (
                low_rank_rank6_a426_finite_packet[
                    "declared_aperiodic_numerator"
                ]
            ),
            "synthetic_low_rank_rank6_a426_projective_line_packet_status": (
                "v9 projective-line regular-minor packet combines the rank-6 "
                "A=426 finite root table with the inline [0:1] top-coefficient "
                "audit, giving projective numerator 2"
            ),
            "synthetic_low_rank_rank6_a426_projective_line_packet_root_union": (
                low_rank_rank6_a426_projective_line_packet["root_union"]
            ),
            "synthetic_low_rank_rank6_a426_projective_line_packet_numerator": (
                low_rank_rank6_a426_projective_line_packet[
                    "declared_aperiodic_numerator"
                ]
            ),
            "synthetic_low_rank_rank7_a393_projective_line_packet_status": (
                "v9 projective-line regular-minor packet checks the hard "
                "rank-7 A=393 row with four finite Frobenius-gcd roots plus "
                "the [0:1] endpoint, giving projective numerator 5 <= 6"
            ),
            "synthetic_low_rank_rank7_a393_projective_line_packet_root_union": (
                low_rank_rank7_a393_projective_line_packet["root_union"]
            ),
            "synthetic_low_rank_rank7_a393_projective_line_packet_numerator": (
                low_rank_rank7_a393_projective_line_packet[
                    "declared_aperiodic_numerator"
                ]
            ),
            "synthetic_low_rank_rank8_a393_projective_line_packet_status": (
                "v9 projective-line regular-minor packet checks the hard "
                "rank-8 A=393 row with four finite Frobenius-gcd roots plus "
                "the [0:1] endpoint, giving projective numerator 5 <= 6"
            ),
            "synthetic_low_rank_rank8_a393_projective_line_packet_root_union": (
                low_rank_rank8_a393_projective_line_packet["root_union"]
            ),
            "synthetic_low_rank_rank8_a393_projective_line_packet_numerator": (
                low_rank_rank8_a393_projective_line_packet[
                    "declared_aperiodic_numerator"
                ]
            ),
            "synthetic_low_rank_rank9_a398_projective_line_packet_status": (
                "v9 projective-line regular-minor packet rehydrates the compact "
                "rank-9 A=398 sweep row, checks three finite Frobenius-gcd "
                "roots plus the [0:1] endpoint, and gives projective numerator "
                "4 <= 6"
            ),
            "synthetic_low_rank_rank9_a398_projective_line_packet_root_union": (
                low_rank_rank9_a398_projective_line_packet["root_union"]
            ),
            "synthetic_low_rank_rank9_a398_projective_line_packet_numerator": (
                low_rank_rank9_a398_projective_line_packet[
                    "declared_aperiodic_numerator"
                ]
            ),
            "synthetic_low_rank_rank10_a411_projective_line_packet_status": (
                "v9 projective-line regular-minor packet rehydrates the compact "
                "rank-10 A=411 sweep row, checks three finite Frobenius-gcd "
                "roots plus the [0:1] endpoint, and gives projective numerator "
                "4 <= 6"
            ),
            "synthetic_low_rank_rank10_a411_projective_line_packet_root_union": (
                low_rank_rank10_a411_projective_line_packet["root_union"]
            ),
            "synthetic_low_rank_rank10_a411_projective_line_packet_numerator": (
                low_rank_rank10_a411_projective_line_packet[
                    "declared_aperiodic_numerator"
                ]
            ),
            "synthetic_low_rank_rank11_a391_projective_line_packet_status": (
                "v9 projective-line regular-minor packet rehydrates the compact "
                "rank-11 A=391 sweep row, checks three finite Frobenius-gcd "
                "roots plus the [0:1] endpoint, and gives projective numerator "
                "4 <= 6"
            ),
            "synthetic_low_rank_rank11_a391_projective_line_packet_root_union": (
                low_rank_rank11_a391_projective_line_packet["root_union"]
            ),
            "synthetic_low_rank_rank11_a391_projective_line_packet_numerator": (
                low_rank_rank11_a391_projective_line_packet[
                    "declared_aperiodic_numerator"
                ]
            ),
            "synthetic_low_rank6_11_tangent_exclusion_status": (
                "proved that all 238 finite roots counted in the rank-6..11 "
                "synthetic low-rank slack certificates have zero "
                "common-code-line tangent overlap"
            ),
            "synthetic_low_rank6_11_common_code_line_tangent_overlap": (
                low_rank6_11_tangent_exclusion["aggregate"][
                    "common_code_line_tangent_overlap_sum"
                ]
            ),
            "synthetic_low_rank6_11_roots_after_common_code_line": (
                low_rank6_11_tangent_exclusion["aggregate"][
                    "regular_roots_after_common_code_line"
                ]
            ),
            "synthetic_low_rank6_11_tangent_rank_summaries": (
                low_rank6_11_tangent_exclusion["aggregate"]["rank_summaries"]
            ),
            "synthetic_low_rank6_11_subfield_exclusion_status": (
                "proved that none of the 238 finite roots counted in the "
                "rank-6..11 synthetic low-rank slack certificates lies in a "
                "proper subfield F_17^d for d in {1,2,4,8,16}"
            ),
            "synthetic_low_rank6_11_proper_subfield_overlap": (
                low_rank6_11_subfield_exclusion["aggregate"][
                    "proper_subfield_overlap_sum"
                ]
            ),
            "synthetic_low_rank6_11_roots_after_proper_subfield_exclusion": (
                low_rank6_11_subfield_exclusion["aggregate"][
                    "regular_roots_after_proper_subfield_exclusion"
                ]
            ),
            "synthetic_low_rank6_11_subfield_rank_summaries": (
                low_rank6_11_subfield_exclusion["aggregate"]["rank_summaries"]
            ),
            "synthetic_low_rank6_11_known_ledger_table_status": (
                "combined M4-style table for ranks 6..11: exact finite roots "
                "plus projective infinity, tangent exclusion, and "
                "proper-subfield exclusion leave at most 5 projective regular "
                "roots per checked synthetic row; endpoint quotient-support is "
                "excluded, while finite-root quotient support/image is not audited"
            ),
            "synthetic_low_rank6_11_known_ledger_max_residual_projective": (
                low_rank6_11_known_ledger_table["aggregate"][
                    "max_known_residual_projective_per_record"
                ]
            ),
            "synthetic_low_rank6_11_known_ledger_quotient_image_status": (
                low_rank6_11_known_ledger_table["aggregate"][
                    "quotient_image_status"
                ]
            ),
            "synthetic_low_rank6_11_known_ledger_quotient_support_status": (
                low_rank6_11_known_ledger_table["aggregate"][
                    "quotient_support_status"
                ]
            ),
            "synthetic_low_rank6_11_known_ledger_endpoint_quotient_support_status": (
                low_rank6_11_known_ledger_table["aggregate"][
                    "projective_endpoint_quotient_support_status"
                ]
            ),
            "low_rank_budget_envelope_status": (
                "proved that every nonzero regular low-rank update chart of "
                "rank <= 6 is within the F_17^32 M3 finite regular-root "
                "budget, and ranks <= 5 are projective-budget safe without "
                "a separate infinity exclusion"
            ),
            "low_rank_budget_envelope_certificate": LOW_RANK_TEMPLATE_REF,
            "low_rank_budget_envelope_rank_range": [
                row["update_rank"] for row in low_rank_envelope["rows"]
            ],
            "low_rank_budget_envelope_finite_budget": low_rank_envelope[
                "endpoint_conventions"
            ]["finite_budget_numerator"],
            "low_rank_budget_envelope_projective_budget": low_rank_envelope[
                "endpoint_conventions"
            ]["projective_budget_numerator"],
            "low_rank_budget_envelope_projective_auto_safe_ranks": [1, 2, 3, 4, 5],
            "low_rank_budget_envelope_projective_rank6_status": (
                "needs infinity exclusion, finite-root slack, or packet-level deduction"
            ),
            "low_rank_packet_gate_status": (
                "v4 gate accepts nonzero low-rank regular packets of rank <=5 "
                "for projective accounting, accepts rank 6 for finite-affine "
                "accounting, and routes rank-6 projective use to an extra "
                "endpoint/slack/deduplication certificate"
            ),
            "low_rank_packet_gate_finite_safe_update_ranks": low_rank_gate[
                "finite_safe_update_ranks"
            ],
            "low_rank_packet_gate_projective_safe_update_ranks": low_rank_gate[
                "projective_safe_without_extra_certificate_update_ranks"
            ],
            "low_rank_packet_gate_projective_extra_certificate_update_ranks": (
                low_rank_gate["projective_requires_extra_certificate_update_ranks"]
            ),
            "low_rank_packet_gate_rank6_extra_certificates": low_rank_gate[
                "rank6_extra_certificates"
            ],
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
                "the synthetic rank-3 low-rank family has exact Frobenius-gcd finite-root counts with 42 roots total, below degree cap 126",
                "the synthetic rank-4 low-rank budget family has degree 4 in all 42 rows and at most 5 projective regular roots per agreement by the v4 low-rank packet gate",
                "the synthetic rank-5 low-rank budget family has degree 5 in all 42 rows and at most 6 projective regular roots per agreement by the v4 low-rank packet gate",
                "the synthetic rank-6 low-rank slack family has exact Frobenius-gcd root histogram {0:16, 1:17, 2:9}, so finite-root slack gives at most 3 projective regular roots per agreement",
                "the synthetic rank-7 low-rank slack family has exact Frobenius-gcd root histogram {0:16, 1:15, 2:6, 3:4, 4:1}, so finite-root slack gives at most 5 projective regular roots per agreement despite degree-only projective bound 8",
                "the synthetic rank-8 low-rank slack family has exact Frobenius-gcd root histogram {0:22, 1:10, 2:7, 3:2, 4:1}, so finite-root slack gives at most 5 projective regular roots per agreement despite degree-only projective bound 9",
                "the synthetic rank-9..11 low-rank slack sweep has exact Frobenius-gcd root histograms {9:{0:17, 1:17, 2:6, 3:2}, 10:{0:8, 1:23, 2:9, 3:2}, 11:{0:15, 1:16, 2:5, 3:6}}, so finite-root slack gives at most 4 projective regular roots per checked pair despite degree-only projective bounds 10, 11, and 12",
                "the synthetic rank-2..11 low-rank endpoint audit proves the projective infinity point [0:1] is an actual support-wise noncontained endpoint in every checked rank/agreement row, witnessed on D minus the update nodes",
                "the synthetic rank-2..11 low-rank endpoint quotient-support audit proves that those actual D minus Y endpoint supports are not nontrivial proper quotient-remainder supports; trivial c=1 and c=512 and quotient-image supports are not claimed",
                "the synthetic rank-6 A=426 projective-line pivot packet is v9-checkable and closes the projective_infinity chart as nonempty with contribution one",
                "the synthetic rank-6 A=426 finite-affine regular-minor packet is v9-checkable with degree 6 and one exact finite root certified by gcd(Delta,Z^q-Z)",
                "the synthetic rank-6..11 low-rank tangent audit checks the unique moment-zero common-code-line slope z=-|X|/s and proves zero tangent overlap for all 238 counted finite roots",
                "the synthetic rank-6..11 low-rank subfield audit proves zero proper-subfield overlap for all 238 counted finite roots over the proper subfields F_17^d, d in {1,2,4,8,16}",
                "the synthetic rank-6..11 known-ledger table combines exact finite roots, projective infinity, endpoint quotient-support exclusion, tangent, and proper-subfield audits into a compact M4-style residual table with max residual projective upper 5 <= 6; finite-root quotient support/image is explicitly not audited",
                "every nonzero low-rank regular chart of update rank at most 6 is automatically within the F_17^32 M3 finite regular-root budget; the v4 packet gate accepts projective use through rank 5 and sends rank 6 to an extra endpoint/slack/deduplication certificate",
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
    print(f"rank-3 low-rank synthetic: {summary['synthetic_low_rank3_family_status']}")
    print(f"rank-3 low-rank tangent: {summary['synthetic_low_rank3_tangent_status']}")
    print(f"rank-4 low-rank budget: {summary['synthetic_low_rank4_budget_family_status']}")
    print(f"rank-5 low-rank budget: {summary['synthetic_low_rank5_budget_family_status']}")
    print(f"rank-6 low-rank slack: {summary['synthetic_low_rank6_slack_family_status']}")
    print(f"rank-7 low-rank slack: {summary['synthetic_low_rank7_slack_family_status']}")
    print(f"rank-8 low-rank slack: {summary['synthetic_low_rank8_slack_family_status']}")
    print(
        "rank-9..11 low-rank slack: "
        f"{summary['synthetic_low_rank9_11_slack_sweep_status']}"
    )
    print(
        "rank-2..11 low-rank infinity: "
        f"{summary['synthetic_low_rank2_11_projective_infinity_status']}"
    )
    print(
        "rank-2..11 endpoint quotient support: "
        f"{summary['synthetic_low_rank2_11_endpoint_quotient_support_status']}"
    )
    print(
        "rank-6 A=426 infinity pivot: "
        f"{summary['synthetic_low_rank_rank6_a426_projective_pivot_status']}"
    )
    print(
        "rank-6 A=426 finite packet: "
        f"{summary['synthetic_low_rank_rank6_a426_finite_packet_status']}"
    )
    print(
        "rank-6 A=426 projective-line packet: "
        f"{summary['synthetic_low_rank_rank6_a426_projective_line_packet_status']}"
    )
    print(
        "rank-7 A=393 projective-line packet: "
        f"{summary['synthetic_low_rank_rank7_a393_projective_line_packet_status']}"
    )
    print(
        "rank-8 A=393 projective-line packet: "
        f"{summary['synthetic_low_rank_rank8_a393_projective_line_packet_status']}"
    )
    print(
        "rank-9 A=398 projective-line packet: "
        f"{summary['synthetic_low_rank_rank9_a398_projective_line_packet_status']}"
    )
    print(
        "rank-10 A=411 projective-line packet: "
        f"{summary['synthetic_low_rank_rank10_a411_projective_line_packet_status']}"
    )
    print(
        "rank-11 A=391 projective-line packet: "
        f"{summary['synthetic_low_rank_rank11_a391_projective_line_packet_status']}"
    )
    print(
        "rank-6..11 low-rank tangent: "
        f"{summary['synthetic_low_rank6_11_tangent_exclusion_status']}"
    )
    print(
        "rank-6..11 low-rank subfield: "
        f"{summary['synthetic_low_rank6_11_subfield_exclusion_status']}"
    )
    print(
        "rank-6..11 known ledger: "
        f"{summary['synthetic_low_rank6_11_known_ledger_table_status']}"
    )
    print(f"low-rank budget envelope: {summary['low_rank_budget_envelope_status']}")
    print(f"low-rank packet gate: {summary['low_rank_packet_gate_status']}")
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
