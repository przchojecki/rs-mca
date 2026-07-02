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


SCHEMA_VERSION = "f17-32-m3-m4-regular-bucket-synthesis-v2"
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
    A386_MOVING_SLOPE_REF: "f17-32-m3-rank6-a386-moving-slope-split-incidence-v9",
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
        summary["line_remaining_unclosed_external_core_range"] == [72, 120],
        "line unclosed core range mismatch",
    )
    require(
        summary["conic_remaining_unclosed_external_core_range"] == [69, 120],
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
                "the still-unclosed high-core quotient ranges are e_G=72..120 for lines and e_G=69..120 for irreducible conics",
                "within those ranges, the one-over-budget subranges are line e_G=72..80 and 120, conic e_G=69..76 and 120; the current worst projective bounds are 18 and 26",
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
