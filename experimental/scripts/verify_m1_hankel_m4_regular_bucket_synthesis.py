#!/usr/bin/env python3
"""Verify the M4 regular-bucket synthesis table for the M3 window."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from math import comb
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experimental.scripts.emit_f17_32_hankel_row_descriptor import (  # noqa: E402
    Field,
    K,
    MODULUS,
    N,
    P,
)


SCHEMA_VERSION = "f17-32-m3-m4-regular-bucket-synthesis-v11"
Q_LINE = 17**32
TARGET_BITS = 128
BUDGET = Q_LINE // 2**TARGET_BITS
A_MIN = 385
A_MAX = 426
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
ZERO_U_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-zero-u-rank-dichotomy/"
    "f17_32_n512_k256_m3_zero_u_rank_dichotomy.json"
)
PROPORTIONAL_REF = (
    "experimental/data/certificates/hankel-proportional-pencil-tangent-lemma/"
    "hankel_proportional_pencil_tangent_lemma_certificate.json"
)
TANGENT_OVERLAP_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-finite-tangent-overlap/"
    "f17_32_n512_k256_m3_finite_tangent_overlap_criterion.json"
)
M5_FINITE_AFFINE_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-m5-finite-affine-kernel-chart/"
    "f17_32_n512_k256_m3_m5_finite_affine_kernel_chart.json"
)
M5_REGULAR_ROOT_RANK_DROP_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-m5-regular-root-rank-drop/"
    "f17_32_n512_k256_m3_m5_regular_root_rank_drop.json"
)
PROJECTIVE_INFINITY_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-projective-infinity-rank/"
    "f17_32_n512_k256_m3_projective_infinity_rank_criterion.json"
)
ZERO_V_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-zero-v-projective-endpoint/"
    "f17_32_n512_k256_m3_zero_v_projective_endpoint.json"
)
DIRECTION_RANK_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-direction-rank-degree-cap/"
    "f17_32_n512_k256_m3_direction_rank_degree_cap.json"
)
RANK_NODE_DICHOTOMY_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank-node-dichotomy/"
    "f17_32_n512_k256_m3_rank_node_dichotomy.json"
)
NULLPOLY_SPLIT_LOCATOR_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-nullpolynomial-split-locator-gate/"
    "f17_32_n512_k256_m3_nullpolynomial_split_locator_gate.json"
)
PROJECTIVE_SPLIT_LOCATOR_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-projective-split-locator-gate/"
    "f17_32_n512_k256_m3_projective_split_locator_gate.json"
)
M5_PROJECTIVE_INFINITY_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-m5-projective-infinity-kernel-chart/"
    "f17_32_n512_k256_m3_m5_projective_infinity_kernel_chart.json"
)
M4_PROJECTIVE_BUDGET_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-m4-projective-budget-split/"
    "f17_32_n512_k256_m3_m4_projective_budget_split.json"
)
M4_AFFINE_PIVOT_COMPRESSION_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-m4-affine-pivot-compression/"
    "f17_32_n512_k256_m3_m4_affine_pivot_compression.json"
)
M4_AFFINE_PIVOT_GCD_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-m4-affine-pivot-gcd-equivalence/"
    "f17_32_n512_k256_m3_m4_affine_pivot_gcd_equivalence.json"
)
LOWER_RANK_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-lower-rank-contained/"
    "f17_32_n512_k256_m3_lower_rank_contained.json"
)
A386_MOVING_SLOPE_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank6-a386-moving-slope-split-incidence/"
    "f17_32_n512_k256_m3_rank6_a386_moving_slope_split_incidence.json"
)


EXPECTED_SCHEMAS = {
    ZERO_U_REF: "f17-32-m3-zero-u-rank-dichotomy-v1",
    PROPORTIONAL_REF: "hankel-proportional-pencil-tangent-lemma-v1",
    TANGENT_OVERLAP_REF: "f17-32-m3-finite-tangent-overlap-criterion-v1",
    M5_FINITE_AFFINE_REF: "f17-32-m3-m5-finite-affine-kernel-chart-v1",
    M5_REGULAR_ROOT_RANK_DROP_REF: "f17-32-m3-m5-regular-root-rank-drop-v1",
    PROJECTIVE_INFINITY_REF: "f17-32-m3-projective-infinity-rank-criterion-v1",
    ZERO_V_REF: "f17-32-m3-zero-v-projective-endpoint-v1",
    DIRECTION_RANK_REF: "f17-32-m3-direction-rank-degree-cap-v1",
    RANK_NODE_DICHOTOMY_REF: "f17-32-m3-rank-node-dichotomy-v1",
    NULLPOLY_SPLIT_LOCATOR_REF: "f17-32-m3-nullpolynomial-split-locator-gate-v1",
    PROJECTIVE_SPLIT_LOCATOR_REF: "f17-32-m3-projective-split-locator-gate-v1",
    M5_PROJECTIVE_INFINITY_REF: "f17-32-m3-m5-projective-infinity-kernel-chart-v1",
    M4_PROJECTIVE_BUDGET_REF: "f17-32-m3-m4-projective-budget-split-v1",
    M4_AFFINE_PIVOT_COMPRESSION_REF: "f17-32-m3-m4-affine-pivot-compression-v1",
    M4_AFFINE_PIVOT_GCD_REF: "f17-32-m3-m4-affine-pivot-gcd-equivalence-v1",
    LOWER_RANK_REF: "f17-32-m3-lower-rank-contained-v1",
    A386_MOVING_SLOPE_REF: "f17-32-m3-rank6-a386-moving-slope-split-incidence-v29",
}


def load_json(ref: str | Path) -> dict[str, Any]:
    path = ref if isinstance(ref, Path) else ROOT / ref
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(ref: str) -> str:
    return sha256((ROOT / ref).read_bytes()).hexdigest()


def hash_value(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(payload).hexdigest()


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def regular_bucket_decision_table() -> dict[str, Any]:
    return {
        "zero_v_direction": {
            "hypothesis": "v=0",
            "finite_full_rank": {
                "condition": "rank H_{t,j}(u)=j+1",
                "B_ap_regular_finite": 0,
                "B_tan_projective_infinity": 1,
                "B_ap_projective_infinity_after_tangent": 0,
                "status": "closed",
            },
            "finite_rank_deficient": {
                "condition": "rank H_{t,j}(u)<=j",
                "B_tan_projective_infinity": 1,
                "B_ap_projective_infinity_after_tangent": 0,
                "finite_residual_status": "singular",
                "finite_residual_label": "unknown",
                "next_step": "M5 finite affine pivots or separate paid classification",
            },
        },
        "proportional_nonzero_direction": {
            "hypothesis": "v!=0 and u=c v",
            "direction_full_rank": {
                "condition": "rank H_{t,j}(v)=j+1",
                "raw_finite_roots": 1,
                "B_tan_finite": 1,
                "B_ap_regular_finite_after_tangent": 0,
                "B_ap_projective_infinity": 0,
                "status": "closed",
            },
            "direction_rank_deficient": {
                "condition": "rank H_{t,j}(v)<=j",
                "known_paid_finite_slope": "z=-c",
                "finite_residual_status": "singular",
                "projective_infinity_status": "empty_by_kernel_containment",
                "projective_infinity_certificate_ref": M5_PROJECTIVE_INFINITY_REF,
                "residual_label": "unknown_for_finite_singular_bucket",
                "next_step": "M5 affine pivots or separate paid classification for finite roots",
            },
        },
        "non_proportional_direction": {
            "hypothesis": "v!=0 and u is not a scalar multiple of v",
            "tangent_overlap": 0,
            "direction_rank_projective_safe": {
                "condition": f"rank H_{{t,j}}(v)<= {BUDGET - 1} and regular bucket nonsingular",
                "B_ap_regular_finite_before_other_ledgers": f"<= {BUDGET - 1}",
                "B_tan_finite": 0,
                "finite_budget_safe": True,
                "projective_infinity_extra_parameters": "<= 1",
                "B_ap_regular_projective_before_other_ledgers": f"<= {BUDGET}",
                "projective_budget_safe_without_endpoint_payment": True,
                "finite_affine_kernel_filter": "apply per root",
                "finite_affine_kernel_certificate_ref": M5_FINITE_AFFINE_REF,
                "regular_root_rank_drop_certificate_ref": M5_REGULAR_ROOT_RANK_DROP_REF,
                "projective_budget_split_certificate_ref": M4_PROJECTIVE_BUDGET_REF,
                "projective_infinity_status": "empty_or_one_point_by_m5_kernel_chart",
                "next_step": "classified safe for the projective sampler before quotient/extension subtraction",
            },
            "direction_rank_endpoint_sensitive": {
                "condition": f"rank H_{{t,j}}(v)={BUDGET} and regular bucket nonsingular",
                "B_ap_regular_finite_before_other_ledgers": f"<= {BUDGET}",
                "B_tan_finite": 0,
                "finite_budget_safe": True,
                "projective_infinity_extra_parameters": "<= 1",
                "finite_affine_impact_of_infinity": 0,
                "B_ap_regular_projective_before_endpoint_payment": f"<= {BUDGET + 1}",
                "projective_budget_safe_without_endpoint_payment": False,
                "projective_budget_split_certificate_ref": M4_PROJECTIVE_BUDGET_REF,
                "projective_split_locator_certificate_ref": PROJECTIVE_SPLIT_LOCATOR_REF,
                "finite_root_compression_certificate_ref": M4_AFFINE_PIVOT_COMPRESSION_REF,
                "compressed_gcd_equivalence_certificate_ref": M4_AFFINE_PIVOT_GCD_REF,
                "projective_sampler_safe_if": (
                    "the infinity endpoint is empty/paid, or the exact finite "
                    f"root table has at most {BUDGET - 1} surviving roots"
                ),
                "next_step": "endpoint payment, endpoint emptiness, or compressed 6x6 affine-pivot root table refinement",
            },
            "direction_rank_intermediate": {
                "condition": f"{BUDGET} < rank H_{{t,j}}(v) <= j",
                "B_ap_regular_finite_before_other_ledgers": "<= rank H_{t,j}(v)",
                "B_tan_finite": 0,
                "finite_budget_safe_by_rank_cap_alone": False,
                "finite_affine_kernel_filter": "apply after actual finite root table",
                "finite_affine_kernel_certificate_ref": M5_FINITE_AFFINE_REF,
                "regular_root_rank_drop_certificate_ref": M5_REGULAR_ROOT_RANK_DROP_REF,
                "projective_infinity_status": "empty_or_one_point_by_m5_kernel_chart",
                "projective_infinity_extra_parameters": "<= 1",
                "projective_budget_split_certificate_ref": M4_PROJECTIVE_BUDGET_REF,
                "finite_root_compression_certificate_ref": M4_AFFINE_PIVOT_COMPRESSION_REF,
                "compressed_gcd_equivalence_certificate_ref": M4_AFFINE_PIVOT_GCD_REF,
                "next_step": "actual finite root table, kernel filter, plus quotient/extension overlap audit",
            },
            "direction_full_rank": {
                "condition": "rank H_{t,j}(v)=j+1",
                "B_ap_regular_finite_before_other_ledgers": "<= j+1",
                "B_tan_finite": 0,
                "finite_affine_kernel_filter": "apply after actual finite root table",
                "finite_affine_kernel_rank_note": (
                    "With full-rank H(v), every finite regular root has "
                    "rank M_z<=j<j+1 and automatically survives the ambient kernel filter."
                ),
                "finite_affine_kernel_certificate_ref": M5_FINITE_AFFINE_REF,
                "regular_root_rank_drop_certificate_ref": M5_REGULAR_ROOT_RANK_DROP_REF,
                "B_ap_projective_infinity": 0,
                "next_step": "actual finite root table and kernel filter unless degree/root table is within budget",
            },
        },
        "known_paid_singular_example": {
            "branch": "zero-u weighted power-sum lower-rank",
            "certificate_ref": LOWER_RANK_REF,
            "status": "contained/common-code-line paid for that family only",
        },
    }


def agreement_record(agreement: int) -> dict[str, Any]:
    j_value = N - agreement
    t_value = agreement - K
    size = j_value + 1
    return {
        "A": agreement,
        "j": j_value,
        "t": t_value,
        "minor_size": size,
        "maximal_row_set_count": comb(t_value, size),
        "finite_slope_budget": BUDGET,
    }


def check_dependency(ref: str, data: dict[str, Any]) -> None:
    require(data["schema_version"] == EXPECTED_SCHEMAS[ref], f"unexpected schema for {ref}")
    if "window" in data:
        require(data["window"]["A_min"] == A_MIN, f"{ref}: A_min mismatch")
        require(data["window"]["A_max"] == A_MAX, f"{ref}: A_max mismatch")
    if "row" in data:
        require(data["row"]["n"] == N, f"{ref}: n mismatch")
        require(data["row"]["k"] == K, f"{ref}: k mismatch")


def check_a386_moving_slope_packet(data: dict[str, Any]) -> None:
    require(data["agreement"]["A"] == 386, "A386 moving-slope agreement mismatch")
    require(data["status"] == "PROVED / AUDIT", "A386 moving-slope status mismatch")
    summary = data["summary"]
    require(summary["line_projective_safe_for_external_core_at_most"] == 71, "line threshold mismatch")
    require(summary["conic_projective_safe_for_external_core_at_most"] == 68, "conic threshold mismatch")
    require(summary["line_residual_quotient_degree_at_most"] == 54, "line quotient degree mismatch")
    require(summary["conic_residual_quotient_degree_at_most"] == 57, "conic quotient degree mismatch")
    require(
        summary["line_residual_punctured_tangent_numerator_at_threshold"] == 55,
        "line punctured tangent numerator mismatch",
    )
    require(
        summary["conic_residual_punctured_tangent_numerator_at_threshold"] == 58,
        "conic punctured tangent numerator mismatch",
    )
    require(
        summary["line_high_core_forced_core_is_dual_evaluation_fiber"],
        "line high-core forced-core classification missing",
    )
    require(
        summary["conic_high_core_forced_core_is_global_common_core"],
        "conic high-core forced-core classification missing",
    )
    require(
        summary["line_residual_projective_safe_by_punctured_tangent_for_external_core_at_least"]
        == 121,
        "line punctured tangent tail threshold mismatch",
    )
    require(
        summary["conic_residual_projective_safe_by_punctured_tangent_for_external_core_at_least"]
        == 121,
        "conic punctured tangent tail threshold mismatch",
    )
    require(
        summary["line_residual_projective_safe_after_cofactor_span_for_external_core_at_least"]
        == 120,
        "line cofactor tail threshold mismatch",
    )
    require(
        summary["conic_residual_projective_safe_after_cofactor_span_for_external_core_at_least"]
        == 120,
        "conic cofactor tail threshold mismatch",
    )
    require(
        summary["line_remaining_unclosed_external_core_range"] == [72, 118],
        "line unclosed core range mismatch",
    )
    require(
        summary["conic_remaining_unclosed_external_core_range"] == [69, 118],
        "conic unclosed core range mismatch",
    )
    require(
        summary["line_one_over_budget_external_core_ranges"] == [[72, 80], [120, 120]],
        "line one-over-budget ranges mismatch",
    )
    require(
        summary["conic_one_over_budget_external_core_ranges"] == [[69, 76], [120, 120]],
        "conic one-over-budget ranges mismatch",
    )
    require(
        summary["line_intermediate_max_current_projective_upper_bound"] == 18,
        "line max intermediate bound mismatch",
    )
    require(
        summary["conic_intermediate_max_current_projective_upper_bound"] == 26,
        "conic max intermediate bound mismatch",
    )
    require(
        summary["line_incidence_one_over_external_core_range"] == [72, 80],
        "line incidence one-over core range mismatch",
    )
    require(
        summary["line_six_finite_saturation_external_slack_range"] == [1, 41],
        "line saturation slack range mismatch",
    )
    require(
        summary["conic_pair_one_over_external_core_range"] == [69, 76],
        "conic pair-overlap one-over core range mismatch",
    )
    require(
        summary["conic_six_finite_forced_pair_overlap_range"] == [0, 14],
        "conic forced pair-overlap range mismatch",
    )
    require(
        summary["punctured_tangent_one_over_tail_external_core"] == 120,
        "tangent one-over tail core mismatch",
    )
    require(
        summary["line_over_budget_base_pressure_core_labels"]["72"]
        == "near-complete base splitting",
        "line e=72 base-pressure label mismatch",
    )
    require(
        summary["line_over_budget_base_pressure_core_labels"]["73"]
        == "positive base splitting",
        "line e=73 base-pressure label mismatch",
    )
    require(
        summary["line_over_budget_base_pressure_core_labels"]["74"]
        == "weak base splitting",
        "line e=74 base-pressure label mismatch",
    )
    require(
        summary["conic_over_budget_secant_pressure_core_labels"]["69"]
        == "almost complete secant graph",
        "conic e=69 secant-pressure label mismatch",
    )
    require(
        summary["conic_over_budget_secant_pressure_core_labels"]["70"]
        == "dense secant graph",
        "conic e=70 secant-pressure label mismatch",
    )
    require(
        summary["conic_over_budget_secant_pressure_core_labels"]["71"]
        == "nontrivial secant graph",
        "conic e=71 secant-pressure label mismatch",
    )
    line_e72 = summary["line_e72_defect_thresholds"]
    require(line_e72["required_total_base_root_incidences"] == 11, "line e=72 base count")
    require(line_e72["minimum_two_base_root_classes"] == 5, "line e=72 two-root classes")
    require(line_e72["maximum_zero_base_root_classes"] == 0, "line e=72 zero-root classes")
    require(
        line_e72["closes_if_total_base_root_incidences_at_most"] == 10,
        "line e=72 base-defect closure threshold",
    )
    conic_e69 = summary["conic_e69_defect_thresholds"]
    require(conic_e69["required_secant_edges_before_external_excess"] == 14, "conic e=69 edges")
    require(conic_e69["maximum_missing_secants_before_external_excess"] == 1, "conic e=69 missing")
    require(conic_e69["minimum_possible_secant_triangles"] == 16, "conic e=69 triangles")
    require(
        conic_e69["closes_if_secant_edges_at_most"] == 13,
        "conic e=69 edge-defect closure threshold",
    )
    require(
        summary["line_e72_allowed_base_root_histograms"] == [[0, 0, 6], [0, 1, 5]],
        "line e=72 extremal base-root histograms",
    )
    require(
        summary["conic_e69_allowed_missing_secant_counts"] == [0, 1],
        "conic e=69 missing secant counts",
    )
    require(
        summary["conic_e69_allowed_secant_triangle_counts"] == [16, 20],
        "conic e=69 secant triangle counts",
    )
    require(
        summary["line_e72_exact_root_budget_alternatives"]
        == [
            {
                "base_root_histogram": [0, 0, 6],
                "exact_nonforced_external_root_incidences": 312,
                "total_base_root_incidences": 12,
                "unused_nonforced_external_root_lines": 1,
            },
            {
                "base_root_histogram": [0, 1, 5],
                "exact_nonforced_external_root_incidences": 313,
                "total_base_root_incidences": 11,
                "unused_nonforced_external_root_lines": 0,
            },
        ],
        "line e=72 exact root-budget alternatives",
    )
    require(
        summary["conic_e69_exact_root_budget_alternatives"]
        == [
            {
                "base_root_histogram": [0, 0, 6],
                "exact_nonforced_external_root_incidences_before_overlap": 330,
                "maximum_missing_secants_before_external_excess": 1,
                "required_pair_overlaps_before_external_excess": 14,
                "total_base_root_incidences": 12,
            },
            {
                "base_root_histogram": [0, 1, 5],
                "exact_nonforced_external_root_incidences_before_overlap": 331,
                "maximum_missing_secants_before_external_excess": 0,
                "required_pair_overlaps_before_external_excess": 15,
                "total_base_root_incidences": 11,
            },
        ],
        "conic e=69 exact root-budget alternatives",
    )
    require(
        summary["line_e72_extremal_design_shapes"]
        == [
            {
                "base_root_histogram": [0, 0, 6],
                "covered_nonforced_external_root_lines": 312,
                "nonforced_external_class_sizes": [52, 52, 52, 52, 52, 52],
                "partition_status": "covers_all_but_one",
                "unused_nonforced_external_root_lines": 1,
            },
            {
                "base_root_histogram": [0, 1, 5],
                "covered_nonforced_external_root_lines": 313,
                "nonforced_external_class_sizes": [53, 52, 52, 52, 52, 52],
                "partition_status": "covers_all",
                "unused_nonforced_external_root_lines": 0,
            },
        ],
        "line e=72 extremal design shapes",
    )
    require(
        summary["conic_e69_extremal_design_shapes"]
        == [
            {
                "base_root_histogram": [0, 0, 6],
                "cover_status": "covers_all_but_one",
                "covered_nonforced_external_root_lines": 315,
                "missing_secants": 0,
                "nonforced_external_class_sizes": [55, 55, 55, 55, 55, 55],
                "pair_overlaps": 15,
                "secant_graph": "K6",
                "secant_triangles": 20,
                "unused_nonforced_external_root_lines": 1,
            },
            {
                "base_root_histogram": [0, 0, 6],
                "cover_status": "covers_all",
                "covered_nonforced_external_root_lines": 316,
                "missing_secants": 1,
                "nonforced_external_class_sizes": [55, 55, 55, 55, 55, 55],
                "pair_overlaps": 14,
                "secant_graph": "K6_minus_one_edge",
                "secant_triangles": 16,
                "unused_nonforced_external_root_lines": 0,
            },
            {
                "base_root_histogram": [0, 1, 5],
                "cover_status": "covers_all",
                "covered_nonforced_external_root_lines": 316,
                "missing_secants": 0,
                "nonforced_external_class_sizes": [56, 55, 55, 55, 55, 55],
                "pair_overlaps": 15,
                "secant_graph": "K6",
                "secant_triangles": 20,
                "unused_nonforced_external_root_lines": 0,
            },
        ],
        "conic e=69 extremal design shapes",
    )
    require(
        summary["line_e72_design_multiplicity_profiles"]
        == [
            {
                "available_nonforced_external_root_lines": 313,
                "base_root_histogram": [0, 0, 6],
                "class_size_sequence": [52, 52, 52, 52, 52, 52],
                "multiplicity_one_lines": 312,
                "multiplicity_two_or_more_lines": 0,
                "multiplicity_zero_lines": 1,
                "pairwise_class_intersections": "all_zero",
            },
            {
                "available_nonforced_external_root_lines": 313,
                "base_root_histogram": [0, 1, 5],
                "class_size_sequence": [53, 52, 52, 52, 52, 52],
                "multiplicity_one_lines": 313,
                "multiplicity_two_or_more_lines": 0,
                "multiplicity_zero_lines": 0,
                "pairwise_class_intersections": "all_zero",
            },
        ],
        "line e=72 design multiplicity profiles",
    )
    require(
        summary["conic_e69_design_multiplicity_profiles"]
        == [
            {
                "available_nonforced_external_root_lines": 316,
                "base_root_histogram": [0, 0, 6],
                "class_overlap_degree_sequence": [5, 5, 5, 5, 5, 5],
                "class_size_sequence": [55, 55, 55, 55, 55, 55],
                "multiplicity_one_lines": 300,
                "multiplicity_three_or_more_lines": 0,
                "multiplicity_two_lines": 15,
                "multiplicity_zero_lines": 1,
                "reason_no_triple_use": (
                    "a nonforced external root line meets an irreducible conic "
                    "in length at most two"
                ),
                "secant_graph": "K6",
            },
            {
                "available_nonforced_external_root_lines": 316,
                "base_root_histogram": [0, 0, 6],
                "class_overlap_degree_sequence": [4, 4, 5, 5, 5, 5],
                "class_size_sequence": [55, 55, 55, 55, 55, 55],
                "multiplicity_one_lines": 302,
                "multiplicity_three_or_more_lines": 0,
                "multiplicity_two_lines": 14,
                "multiplicity_zero_lines": 0,
                "reason_no_triple_use": (
                    "a nonforced external root line meets an irreducible conic "
                    "in length at most two"
                ),
                "secant_graph": "K6_minus_one_edge",
            },
            {
                "available_nonforced_external_root_lines": 316,
                "base_root_histogram": [0, 1, 5],
                "class_overlap_degree_sequence": [5, 5, 5, 5, 5, 5],
                "class_size_sequence": [56, 55, 55, 55, 55, 55],
                "multiplicity_one_lines": 301,
                "multiplicity_three_or_more_lines": 0,
                "multiplicity_two_lines": 15,
                "multiplicity_zero_lines": 0,
                "reason_no_triple_use": (
                    "a nonforced external root line meets an irreducible conic "
                    "in length at most two"
                ),
                "secant_graph": "K6",
            },
        ],
        "conic e=69 design multiplicity profiles",
    )
    require(
        summary["line_e72_design_local_profiles"]
        == [
            {
                "base_root_histogram": [0, 0, 6],
                "class_count": 6,
                "class_size_sequence": [52, 52, 52, 52, 52, 52],
                "local_description": (
                    "each valid Q-class owns exactly its class-size many "
                    "nonforced external root lines, with pairwise disjoint "
                    "ownership"
                ),
                "pair_overlap_degree_sequence": [0, 0, 0, 0, 0, 0],
                "singleton_root_line_sequence": [52, 52, 52, 52, 52, 52],
            },
            {
                "base_root_histogram": [0, 1, 5],
                "class_count": 6,
                "class_size_sequence": [53, 52, 52, 52, 52, 52],
                "local_description": (
                    "each valid Q-class owns exactly its class-size many "
                    "nonforced external root lines, with pairwise disjoint "
                    "ownership"
                ),
                "pair_overlap_degree_sequence": [0, 0, 0, 0, 0, 0],
                "singleton_root_line_sequence": [53, 52, 52, 52, 52, 52],
            },
        ],
        "line e=72 design local profiles",
    )
    require(
        summary["conic_e69_design_local_profiles"]
        == [
            {
                "base_root_histogram": [0, 0, 6],
                "class_count": 6,
                "class_size_sequence": [55, 55, 55, 55, 55, 55],
                "local_description": (
                    "each valid Q-class is incident to its secant-degree many "
                    "double-use external lines and the remaining listed singleton "
                    "external lines"
                ),
                "secant_degree_sequence": [5, 5, 5, 5, 5, 5],
                "secant_graph": "K6",
                "singleton_root_line_sequence": [50, 50, 50, 50, 50, 50],
            },
            {
                "base_root_histogram": [0, 0, 6],
                "class_count": 6,
                "class_size_sequence": [55, 55, 55, 55, 55, 55],
                "local_description": (
                    "each valid Q-class is incident to its secant-degree many "
                    "double-use external lines and the remaining listed singleton "
                    "external lines"
                ),
                "secant_degree_sequence": [4, 4, 5, 5, 5, 5],
                "secant_graph": "K6_minus_one_edge",
                "singleton_root_line_sequence": [51, 51, 50, 50, 50, 50],
            },
            {
                "base_root_histogram": [0, 1, 5],
                "class_count": 6,
                "class_size_sequence": [56, 55, 55, 55, 55, 55],
                "local_description": (
                    "each valid Q-class is incident to its secant-degree many "
                    "double-use external lines and the remaining listed singleton "
                    "external lines"
                ),
                "secant_degree_sequence": [5, 5, 5, 5, 5, 5],
                "secant_graph": "K6",
                "singleton_root_line_sequence": [51, 50, 50, 50, 50, 50],
            },
        ],
        "conic e=69 design local profiles",
    )
    require(
        summary["conic_e69_pascal_obstruction_relation_counts"] == [60, 36, 60]
        and summary["conic_e69_pascal_obstruction_cycle_counts"] == [60, 36, 60],
        "conic e=69 Pascal obstruction counts",
    )
    pascal_rows = data["conic_e69_pascal_obstruction_profile"]
    require(
        [
            (
                row["base_root_histogram"],
                row["secant_graph"],
                row["missing_secants"],
                row["secant_edge_count"],
                row["pascal_collinearity_relation_count"],
            )
            for row in pascal_rows
        ]
        == [
            ([0, 0, 6], "K6", 0, 15, 60),
            ([0, 0, 6], "K6_minus_one_edge", 1, 14, 36),
            ([0, 1, 5], "K6", 0, 15, 60),
        ],
        "conic e=69 Pascal obstruction profile rows",
    )
    require(
        all(row["closure_if_condition_fails"] for row in pascal_rows),
        "conic e=69 Pascal rows should be closure criteria",
    )
    line_catalog = summary["line_one_over_design_catalog"]
    require(
        [row["forced_external_core_size"] for row in line_catalog]
        == list(range(72, 81)),
        "line one-over catalog core range",
    )
    require(
        [row["allowed_base_root_histogram_count"] for row in line_catalog]
        == [2, 16, 27, 28, 28, 28, 28, 28, 28],
        "line one-over catalog histogram counts",
    )
    require(
        [row["unused_nonforced_external_root_line_range"] for row in line_catalog]
        == [[0, 1], [0, 6], [0, 11], [4, 16], [9, 21], [14, 26], [19, 31], [24, 36], [29, 41]],
        "line one-over catalog unused ranges",
    )
    require(
        [row["all_histograms_allowed"] for row in line_catalog]
        == [False, False, False, True, True, True, True, True, True],
        "line one-over catalog all-histogram flags",
    )
    conic_catalog = summary["conic_one_over_design_catalog"]
    require(
        [row["forced_external_core_size"] for row in conic_catalog]
        == list(range(69, 77)),
        "conic one-over catalog core range",
    )
    require(
        [row["allowed_base_root_histogram_count"] for row in conic_catalog]
        == [2, 16, 27, 28, 28, 28, 28, 28],
        "conic one-over catalog histogram counts",
    )
    require(
        [row["required_pair_overlap_range"] for row in conic_catalog]
        == [[14, 15], [9, 15], [4, 15], [0, 11], [0, 6], [0, 1], [0, 0], [0, 0]],
        "conic one-over catalog pair-overlap ranges",
    )
    require(
        [row["zero_pair_overlap_allowed"] for row in conic_catalog]
        == [False, False, False, True, True, True, True, True],
        "conic one-over catalog zero-overlap flags",
    )
    require(
        summary["single_saving_closure_ledger_count"] == 19,
        "single-saving closure ledger count",
    )
    require(
        summary["single_saving_closure_ledger_core_ranges"]
        == {
            "line_external_incidence": [72, 80],
            "irreducible_conic_pair_overlap": [69, 76],
            "punctured_tangent_tail": [120, 120],
        },
        "single-saving closure ledger core ranges",
    )
    require(
        summary["one_over_mechanism_priority_classes"]
        == [
            {
                "component_type": "line",
                "core_count": 3,
                "external_core_range": [72, 74],
                "mechanism_class": "line_base_splitting_active",
            },
            {
                "component_type": "line",
                "core_count": 6,
                "external_core_range": [75, 80],
                "mechanism_class": "line_external_slack_only",
            },
            {
                "component_type": "irreducible_conic",
                "core_count": 3,
                "external_core_range": [69, 71],
                "mechanism_class": "conic_base_and_secant_pressure_active",
            },
            {
                "component_type": "irreducible_conic",
                "core_count": 3,
                "external_core_range": [72, 74],
                "mechanism_class": "conic_secant_pressure_only",
            },
            {
                "component_type": "irreducible_conic",
                "core_count": 2,
                "external_core_range": [75, 76],
                "mechanism_class": "conic_endpoint_or_duplicate_only",
            },
            {
                "component_type": "line_or_irreducible_conic",
                "core_count": 2,
                "external_core_range": [120, 120],
                "mechanism_class": "punctured_tangent_tail_closed_by_cofactor_span",
            },
        ],
        "one-over mechanism-priority classes",
    )
    require(
        [
            (
                row["component_type"],
                row["forced_external_core_size"],
                row["projective_saturation_count"],
                row["finite_tangent_star_common_support_size"],
                row["finite_tangent_star_residual_coordinate_count"],
            )
            for row in summary["punctured_tangent_tail_extremizer_profile"]
        ]
        == [
            ("line", 120, 7, 385, 7),
            ("irreducible_conic", 120, 7, 385, 7),
        ],
        "punctured tangent-tail extremizer profile",
    )
    require(
        [
            (
                row["component_type"],
                row["forced_external_core_size"],
                row["finite_component_slope_count_at_least"],
                row["finite_component_cofactor_span_dimension_at_least"],
                row["quotient_family_vector_dimension_at_most"],
                row["projective_upper_bound_after_obstruction"],
            )
            for row in summary["punctured_tangent_tail_cofactor_span_closure"]
        ]
        == [
            ("line", 120, 6, 6, 2, 6),
            ("irreducible_conic", 120, 6, 6, 3, 6),
        ],
        "punctured tangent-tail cofactor-span closure",
    )
    require(
        summary["line_cofactor_improved_tangent_one_over_external_core"] == [119],
        "line cofactor tangent one-over mismatch",
    )
    require(
        summary["conic_cofactor_improved_tangent_one_over_external_core"] == [119],
        "conic cofactor tangent one-over mismatch",
    )
    cofactor_profile = data["cofactor_improved_tangent_tail_profile"]
    require(
        cofactor_profile["line_rows"][0]["cofactor_improved_projective_tangent_bound"] == 54,
        "line cofactor profile first row changed",
    )
    require(
        cofactor_profile["line_rows"][-7]["forced_external_core_size"] == 119
        and cofactor_profile["line_rows"][-7]["cofactor_improved_one_over_budget"],
        "line cofactor profile should make e=119 one-over",
    )
    require(
        cofactor_profile["line_rows"][-6]["forced_external_core_size"] == 120
        and cofactor_profile["line_rows"][-6]["cofactor_improved_projective_safe"],
        "line cofactor profile should make e=120 safe",
    )
    require(
        cofactor_profile["irreducible_conic_rows"][-7]["forced_external_core_size"] == 119
        and cofactor_profile["irreducible_conic_rows"][-7]["cofactor_improved_one_over_budget"],
        "conic cofactor profile should make e=119 one-over",
    )
    require(
        cofactor_profile["irreducible_conic_rows"][-6]["forced_external_core_size"] == 120
        and cofactor_profile["irreducible_conic_rows"][-6]["cofactor_improved_projective_safe"],
        "conic cofactor profile should make e=120 safe",
    )
    require(
        summary["line_remaining_unclosed_external_core_range"] == [72, 118],
        "line remaining range after exact tail closure",
    )
    require(
        summary["conic_remaining_unclosed_external_core_range"] == [69, 118],
        "conic remaining range after exact tail closure",
    )
    require(
        summary["line_cofactor_current_one_over_external_core_ranges"] == [[72, 80], [119, 119]],
        "line cofactor-current one-over profile mismatch",
    )
    require(
        summary["conic_cofactor_current_one_over_external_core_ranges"] == [[69, 76], [119, 119]],
        "conic cofactor-current one-over profile mismatch",
    )
    require(
        summary["line_cofactor_current_safe_external_core_ranges"] == [[120, 120]]
        and summary["conic_cofactor_current_safe_external_core_ranges"] == [[120, 120]],
        "cofactor-current safe tail mismatch",
    )
    require(
        summary["line_cofactor_current_max_projective_upper_bound"] == 18,
        "line cofactor-current max bound mismatch",
    )
    require(
        summary["conic_cofactor_current_max_projective_upper_bound"] == 25,
        "conic cofactor-current max bound mismatch",
    )
    cofactor_current = data["cofactor_current_intermediate_residual_profile"]
    require(
        cofactor_current["line_rows"][-2]["forced_external_core_size"] == 119
        and cofactor_current["line_rows"][-2]["one_over_budget"],
        "line e=119 should be one-over in the cofactor-current profile",
    )
    require(
        cofactor_current["irreducible_conic_rows"][-2]["forced_external_core_size"] == 119
        and cofactor_current["irreducible_conic_rows"][-2]["one_over_budget"],
        "conic e=119 should be one-over in the cofactor-current profile",
    )
    require(
        summary["line_residual_projective_safe_after_exact_tail_for_external_core_at_least"] == 119
        and summary["conic_residual_projective_safe_after_exact_tail_for_external_core_at_least"] == 119,
        "exact-tail safe threshold mismatch",
    )
    require(
        summary["line_exact_current_one_over_external_core_ranges"] == [[72, 80]]
        and summary["conic_exact_current_one_over_external_core_ranges"] == [[69, 76]],
        "exact-current one-over profile mismatch",
    )
    require(
        summary["line_exact_current_safe_external_core_ranges"] == [[119, 120]]
        and summary["conic_exact_current_safe_external_core_ranges"] == [[119, 120]],
        "exact-current safe tail mismatch",
    )
    exact_current = data["exact_current_intermediate_residual_profile"]
    require(
        exact_current["line_rows"][-2]["forced_external_core_size"] == 119
        and exact_current["line_rows"][-2]["projective_safe"],
        "line e=119 should be safe in the exact-current profile",
    )
    require(
        exact_current["irreducible_conic_rows"][-2]["forced_external_core_size"] == 119
        and exact_current["irreducible_conic_rows"][-2]["projective_safe"],
        "conic e=119 should be safe in the exact-current profile",
    )
    exact_tail = data["punctured_tangent_tail_e119_exact_agreement_closure"]
    require(
        [
            (
                row["component_type"],
                row["forced_external_core_size"],
                row["projective_upper_bound_after_obstruction"],
                [
                    entry["common_support_complement_size"]
                    for entry in row["near_extremizer_common_support_complement_options"]
                ],
            )
            for row in exact_tail
        ]
        == [
            ("line", 119, 6, [7, 8]),
            ("irreducible_conic", 119, 6, [7, 8]),
        ],
        "e=119 exact-tail closure mismatch",
    )
    require(
        summary["exact_current_minimal_obstruction_count"] == 17
        and summary["exact_current_minimal_obstruction_core_ranges"]
        == {
            "line_external_incidence": [72, 80],
            "irreducible_conic_pair_overlap": [69, 76],
        },
        "exact-current minimal obstruction summary mismatch",
    )
    require(
        summary["exact_current_minimal_obstruction_required_finite_slopes"] == 6
        and summary["exact_current_minimal_obstruction_requires_unpaid_endpoint"],
        "exact-current minimal obstruction requirements mismatch",
    )
    minimal = data["exact_current_minimal_obstruction_profile"]
    require(
        [
            (row["component_type"], row["forced_external_core_size"])
            for row in minimal
        ]
        == [
            *[("line", core) for core in range(72, 81)],
            *[("irreducible_conic", core) for core in range(69, 77)],
        ],
        "exact-current minimal obstruction profile coverage mismatch",
    )
    require(
        all(
            row["dangerous_projective_count"] == 7
            and row["finite_source_classes_must_equal"] == 6
            and row["finite_slopes_must_be_distinct"]
            and row["endpoint_must_survive_unpaid"]
            for row in minimal
        ),
        "exact-current minimal obstruction rows should all be six finite plus endpoint",
    )
    require(
        summary["line_incidence_only_sharpness_witness_count"] == 9
        and summary["line_incidence_only_sharpness_external_core_range"] == [72, 80],
        "line incidence-only sharpness summary mismatch",
    )
    require(
        summary["conic_incidence_only_sharpness_witness_count"] == 8
        and summary["conic_incidence_only_sharpness_external_core_range"] == [69, 76],
        "conic incidence-only sharpness summary mismatch",
    )
    sharpness = data["incidence_only_sharpness_witnesses"]
    require(
        [
            row["forced_external_core_size"]
            for row in sharpness["line_endpoint_only_incidence_range"]
        ]
        == list(range(72, 81)),
        "line incidence-only sharpness core coverage mismatch",
    )
    require(
        [
            row["forced_external_core_size"]
            for row in sharpness["irreducible_conic_endpoint_only_incidence_range"]
        ]
        == list(range(69, 77)),
        "conic incidence-only sharpness core coverage mismatch",
    )
    require(
        all(
            row["status"] == "ABSTRACT_SHARPNESS_WITNESS_NOT_HANKEL_REALIZABILITY"
            and row["saturates_current_finite_incidence_bound"]
            for row in sharpness["line_endpoint_only_incidence_range"]
        ),
        "line incidence-only sharpness status mismatch",
    )
    require(
        all(
            row["status"] == "ABSTRACT_SHARPNESS_WITNESS_NOT_HANKEL_REALIZABILITY"
            and row["saturates_current_pair_overlap_bound"]
            and row["multiplicity_three_or_more_lines"] == 0
            for row in sharpness["irreducible_conic_endpoint_only_incidence_range"]
        ),
        "conic incidence-only sharpness status mismatch",
    )
    nonclaims = set(data["nonclaims"])
    require(
        "does not claim the punctured tangent numerator at the residual threshold is within the original row budget"
        in nonclaims,
        "A386 moving-slope packet must keep the original-budget nonclaim",
    )
    require(
        "does not produce a row-level M3 safe-side bound" in nonclaims,
        "A386 moving-slope packet must keep the row-bound nonclaim",
    )
    require(
        "incidence-only sharpness witnesses are abstract set-system witnesses, not Hankel-realizable components"
        in nonclaims,
        "A386 moving-slope packet must keep the incidence-only sharpness nonclaim",
    )


def build_certificate() -> dict[str, Any]:
    field = Field(P, MODULUS)
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    dependencies = {ref: load_json(ref) for ref in EXPECTED_SCHEMAS}

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field"] == "F_17^32", "descriptor field mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(descriptor["row"]["syndrome_length"] == N - K, "syndrome length mismatch")
    for ref, data in dependencies.items():
        check_dependency(ref, data)
    check_a386_moving_slope_packet(dependencies[A386_MOVING_SLOPE_REF])

    domain_encodings = descriptor["domain"]["domain_encodings"]
    require(len(domain_encodings) == N, "domain length mismatch")
    require(len(set(domain_encodings)) == N, "descriptor domain is not distinct")
    decoded = [field.decode(value) for value in domain_encodings]
    require(
        [field.encode(value) for value in decoded] == domain_encodings,
        "domain decode/encode roundtrip failed",
    )

    records = [agreement_record(agreement) for agreement in range(A_MIN, A_MAX + 1)]
    total_row_sets = sum(record["maximal_row_set_count"] for record in records)
    reference_totals = [
        data["window"]["all_row_set_total"]
        for data in dependencies.values()
        if "window" in data and "all_row_set_total" in data["window"]
    ]
    for total in reference_totals:
        require(total == total_row_sets, "dependency row-set total mismatch")
    require(BUDGET == 6, "unexpected finite-slope budget")

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "AUDIT",
        "proved_dependency_synthesis": True,
        "object": "M4 regular-bucket decision table for the F_17^32 M3 window",
        "row": {
            "code": "RS[F_17^32,H,256]",
            "n": N,
            "k": K,
            "field": "F_17^32",
            "domain_hash": descriptor["row"]["domain_hash"],
            "q_line": Q_LINE,
            "finite_slope_budget": BUDGET,
        },
        "source_artifacts": {
            "row_descriptor": {"ref": ROW_DESCRIPTOR_REF, "sha256": sha256_file(ROW_DESCRIPTOR_REF)},
            **{
                ref.rsplit("/", 1)[-1].removesuffix(".json"): {
                    "ref": ref,
                    "sha256": sha256_file(ref),
                }
                for ref in EXPECTED_SCHEMAS
            },
        },
        "window": {
            "A_min": A_MIN,
            "A_max": A_MAX,
            "agreement_count": len(records),
            "all_row_set_total": total_row_sets,
        },
        "regular_bucket_decision_table": regular_bucket_decision_table(),
        "synthesis": {
            "closed_by_current_lemmas": [
                "zero-v with full-rank H(u): no finite roots, infinity tangent-paid",
                "proportional nonzero-v with full-rank H(v): unique finite root tangent-paid, infinity excluded",
                "zero-u full-rank branch as the c=0 proportional subcase",
            ],
            "finite_safe_with_projective_kernel_accounting": [
                "non-proportional nonsingular buckets with direction rank <= 5 are projective-budget safe before endpoint payment",
                "non-proportional nonsingular buckets with direction rank = 6 are finite-budget safe but projective endpoint-sensitive",
            ],
            "m4_projective_budget_split": [
                "finite regular root count is <= r=rank H(v)",
                "projective counting adds at most the single endpoint [0:1]",
                "for this row both finite and projective budgets equal 6, so r<=5 is projective-safe and r=6 needs endpoint empty/paid or one fewer finite root",
            ],
            "m4_affine_pivot_compression": [
                "on any finite affine pivot with M_R(z0) invertible and rank H_R(v)<=r, det M_R(z) compresses to an r x r determinant",
                "rank-6 endpoint-sensitive finite-root refinement can therefore target 6x6 compressed determinants instead of 87..128 dimensional minors",
            ],
            "m4_affine_pivot_gcd_equivalence": [
                "every nonzero rank-6 minor has at most six bad finite pivots and therefore many good pivots over F_17^32",
                "after choosing good pivots per nonzero chart and translating local compressed determinants back to the global slope variable, monic gcd of original minors equals monic gcd of compressed polynomials",
            ],
            "a386_moving_slope_refinement": [
                "within the separated A=386 rank-6 common-component residual, moving-slope line components with external forced core e_G<=71 are projective-safe",
                "within the same residual, irreducible moving-slope conics with external forced core e_G<=68 are projective-safe by pair-overlap packing",
                "the remaining high-core line branch is a dual-evaluation-fiber quotient pencil of degree <=54",
                "the remaining high-core irreducible-conic branch has a global common forced core and becomes a quotient family of degree <=57",
                "after puncturing the forced core, the projective tangent staircase closes the tail e_G>=121",
                "the e_G=120 punctured-tangent tail is closed by a cofactor-span obstruction: at least six tangent-star cofactors must be finite component classes and are independent, but the fixed-core quotient family has vector dimension at most 2 or 3",
                "the generalized cofactor-span top-saturation exclusion improves the high-core tangent tail bound from r'+1 to r', making e_G=119 the next cofactor-current one-over tangent-tail core and e_G>=120 projective-safe",
                "the exact-agreement residual-budget split closes the e_G=119 tangent-tail core, so the exact-current one-over ranges are line e_G=72..80 and conic e_G=69..76; the conic maximum projective bound drops from 26 to 25",
                "the still-unclosed high-core quotient ranges are e_G=72..118 for lines and e_G=69..118 for irreducible conics",
                "within those ranges, the finite-incidence one-over-budget subranges are line e_G=72..80 and conic e_G=69..76; after exact-tail sharpening the worst projective bounds are 18 and 25",
                "six-finite saturation in the endpoint-only incidence ranges has line external slack 1..41 and conic forced pair-overlap demand 0..14; the formerly one-over e_G=120 cases are closed by the cofactor-span contradiction",
                "a genuine over-budget one-over witness must also have six distinct finite slopes and an unpaid endpoint; the strongest remaining pressure is line e_G=72 base splitting and conic e_G=69 almost-complete secants",
                "line e_G=72 closes unless all six finite classes have a base root and at least five have two; conic e_G=69 closes unless at least 14 of 15 pair secants occur, forcing at least 16 secant triangles",
                "line e_G=72 survival has only base-root histograms (0,0,6) or (0,1,5); conic e_G=69 survival has secant graph K6 or K6 minus one edge",
                "exact degree-126 accounting leaves line e_G=72 with either one unused nonforced external root line or none, and conic e_G=69 with either 14 pair overlaps or all 15 pair overlaps",
                "extremal design accounting leaves two line partition shapes and three conic secant-cover shapes",
                "extremal multiplicity accounting leaves line profiles (1,312,0)/(0,313,0) and conic profiles (1,300,15)/(0,302,14)/(0,301,15)",
                "local incidence accounting leaves line singleton sequences 52^6 or (53,52^5), and conic secant/singleton profiles (5^6;50^6), ((4,4,5,5,5,5);(51,51,50,50,50,50)), or (5^6;(51,50,50,50,50,50))",
                "Pascal's theorem gives a concrete obstruction test for the conic e_G=69 extremal branch: K6 secant covers force 60 Pascal collinearities and K6-minus-one covers force 36",
                "the endpoint-only one-over finite-incidence range has a compact exact catalog: line histogram counts 2,16,27,28^6 across e_G=72..80 and conic counts 2,16,27,28^5 across e_G=69..76",
                "abstract incidence-only sharpness witnesses exist for every finite-incidence one-over core, so those rows cannot be closed by sharpening only the current incidence and pair-overlap axioms",
                "the cofactor-current moving-slope one-over residual rows have a single-saving closure ledger entry: line e_G=72..80, conic e_G=69..76, and the punctured-tangent tail e_G=120",
                "after exact-tail closure, the remaining over-budget normal form has exactly 17 finite-incidence rows, each requiring six distinct finite slopes plus an unpaid endpoint",
                "the finite-incidence one-over rows split by first available saving mechanism into line base-active 72..74, line external-slack 75..80, conic base+secant 69..71, conic secant-only 72..74, and conic endpoint/duplicate-only 75..76; the punctured-tangent tails e_G=120 and e_G=119 are now closed by cofactor-span and exact-agreement arguments",
            ],
            "m3_rank_node_dichotomy": [
                "one full-rank specialization gives a nonzero maximal minor and a nonsingular regular bucket",
                "rank deficiency at j+2 distinct finite nodes forces every maximal minor to vanish identically and declares a singular bucket",
            ],
            "m3_nullpolynomial_split_locator_gate": [
                "finite canonical roots in a nonsingular regular bucket are ambient Hankel null-polynomials",
                "actual split-locator bad slopes are filtered by monic degree-j divisibility by X^512-1 and H(v)ell noncontainment",
            ],
            "m3_projective_split_locator_gate": [
                "ambient projective endpoints satisfy H(v)ell=0 and H(u)ell!=0",
                "actual split-locator projective endpoints are filtered by monic degree-j divisibility by X^512-1",
                "rank-6 direction buckets have large ambient endpoint kernels, but those kernels still need the split-locator divisor gate before endpoint counting",
            ],
            "m5_projective_infinity_closed_by_kernel_chart": [
                "proportional rank-deficient direction: infinity empty because ker H(v) subset ker H(u)",
                "arbitrary rank-deficient direction: infinity empty iff ker H(v) subset ker H(u), otherwise at most the single endpoint [0:1]",
            ],
            "m5_finite_affine_filter": [
                "for every finite root z, the ambient affine noncontainment chart is empty iff ker(H(u)+zH(v)) subset ker H(v)",
                "if the kernel containment fails, the root contributes at most the single finite parameter z before split-locator and quotient/extension audits",
                "if rank H(v) exceeds rank(H(u)+zH(v)), the root automatically survives the ambient kernel filter",
            ],
            "m5_regular_root_rank_drop_bridge": [
                "finite roots of the v10 canonical regular gcd are exactly finite slopes with rank(H(u)+zH(v))<=j in nonsingular regular buckets",
                "therefore full-direction-rank regular roots automatically survive the finite-affine kernel filter",
            ],
            "still_requires_m5_or_other_ledgers": [
                "rank-deficient finite regular buckets not covered by a paid family",
                "non-proportional direction-rank-6 buckets when the projective endpoint is not empty or paid and the 6x6 compressed exact finite root table has six surviving roots",
                "the A=386 separated moving-slope intermediate high-core quotient branches e_G=72..120 for lines and e_G=69..120 for irreducible conics",
                "non-proportional finite buckets with direction rank > 6 unless exact root tables plus kernel filters improve the bound",
                "quotient, quotient-image, extension, and subfield overlap for future non-proportional root tables",
            ],
            "not_a_row_bound": (
                "This table composes proved local lemmas; it is not a worst-case "
                "support-wise MCA upper bound until every residual bucket is "
                "closed or assigned to a paid ledger."
            ),
        },
        "field_audit": {
            "full_domain_distinct": True,
            "domain_size": len(domain_encodings),
            "domain_hash": hash_value(domain_encodings),
            "decoded_roundtrip_hash": hash_value([field.encode(value) for value in decoded]),
        },
        "agreement_records": records,
        "summary": {
            "agreement_count": len(records),
            "finite_slope_budget": BUDGET,
            "closed_case_count": 3,
            "projective_safe_rank_cutoff_case_count": 1,
            "endpoint_sensitive_rank_cutoff_case_count": 1,
            "m5_projective_infinity_closed_case_count": 1,
            "m5_finite_affine_filter_count": 1,
            "m5_regular_root_rank_drop_bridge_count": 1,
            "m4_projective_budget_split_count": 1,
            "m4_affine_pivot_compression_count": 1,
            "m4_affine_pivot_gcd_equivalence_count": 1,
            "a386_moving_slope_refinement_count": 1,
            "m3_rank_node_dichotomy_count": 1,
            "m3_nullpolynomial_split_locator_gate_count": 1,
            "m3_projective_split_locator_gate_count": 1,
            "residual_case_count": 3,
            "dependencies_checked": len(EXPECTED_SCHEMAS),
        },
        "checks": [
            "all dependency schemas match the expected certificates",
            "all dependency windows match 385..426",
            "all dependency row-set totals agree where supplied",
            "the decision table separates closed, finite-safe, and residual cases",
            "finite affine roots are assigned a per-root M5 kernel filter",
            "regular gcd roots are linked to evaluated Hankel rank drop",
            "projective infinity is classified by the M5 kernel-containment chart",
            "rank<=5 buckets are separated from rank=6 endpoint-sensitive buckets",
            "rank-node testing supplies the finite regular/singular gate for future packets",
            "null-polynomial testing separates ambient roots from split-locator noncontainment witnesses",
            "projective split-locator testing separates ambient infinity endpoints from genuine support-wise endpoint witnesses",
            "rank-6 finite-root refinement is assigned an affine-pivot 6x6 compression theorem",
            "translated compressed rank-6 chart polynomials preserve the v10 canonical gcd root set after good pivots",
            "A=386 moving-slope small-core and very-high-core tail branches are recorded as projective-safe; the intermediate high-core quotient ranges remain residual",
            "projective infinity and finite affine accounting are not conflated",
        ],
        "nonclaims": [
            "does not compute arbitrary non-proportional finite root tables",
            "does not prove the projective endpoint is empty or paid in the rank=6 case",
            "does not close the A=386 intermediate high-core quotient moving-slope residual in original-row projective accounting",
            "does not audit quotient or extension overlap for arbitrary root tables",
            "not a worst-case support-wise MCA row bound",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"M4 regular-bucket synthesis certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    window = certificate["window"]
    summary = certificate["summary"]
    print("F_17^32 M3/M4 regular-bucket synthesis")
    print(
        "A={A_min}..{A_max}, agreements={agreement_count}, row sets={all_row_set_total}".format(
            **window
        )
    )
    print("finite budget={finite_slope_budget}".format(**summary))
    print(
        "closed cases={closed_case_count}, projective-safe rank cases={projective_safe_rank_cutoff_case_count}, endpoint-sensitive rank cases={endpoint_sensitive_rank_cutoff_case_count}, residual cases={residual_case_count}".format(
            **summary
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()

    certificate = build_certificate()
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(certificate), encoding="utf-8")
    if args.check:
        check_certificate(args.check)
    print_summary(certificate)


if __name__ == "__main__":
    main()
