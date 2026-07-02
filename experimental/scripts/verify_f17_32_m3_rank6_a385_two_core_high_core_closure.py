#!/usr/bin/env python3
"""Verify the A=385 fixed two-core high-core line/conic closure."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experimental.scripts.emit_f17_32_hankel_row_descriptor import K, N, P  # noqa: E402


SCHEMA_VERSION = "f17-32-m3-rank6-a385-two-core-high-core-closure-v1"
Q_LINE = 17**32
TARGET_BITS = 128
FINITE_BUDGET = Q_LINE // 2**TARGET_BITS
PROJECTIVE_DENOMINATOR = Q_LINE + 1
PROJECTIVE_BUDGET = PROJECTIVE_DENOMINATOR // 2**TARGET_BITS
AGREEMENT = 385
RANK = 6
BASE_CORE_SIZE = 2
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
MOVING_SLOPE_REF = (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-rank6-a385-two-core-moving-slope-incidence/"
    "f17_32_n512_k256_m3_rank6_a385_two_core_moving_slope_incidence.json"
)
HIGH_CORE_QUOTIENT_REF = (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-rank6-a385-two-core-high-core-quotient/"
    "f17_32_n512_k256_m3_rank6_a385_two_core_high_core_quotient.json"
)
CONIC_PRODUCT_REF = (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-rank6-a385-two-core-conic-product-collapse/"
    "f17_32_n512_k256_m3_rank6_a385_two_core_conic_product_collapse.json"
)
NULLPOLY_SPLIT_GATE_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-nullpolynomial-split-locator-gate/"
    "f17_32_n512_k256_m3_nullpolynomial_split_locator_gate.json"
)


def load_json(ref: str | Path) -> dict[str, Any]:
    path = ref if isinstance(ref, Path) else ROOT / ref
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(ref: str) -> str:
    return sha256((ROOT / ref).read_bytes()).hexdigest()


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def build_certificate() -> dict[str, Any]:
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    moving = load_json(MOVING_SLOPE_REF)
    high_core = load_json(HIGH_CORE_QUOTIENT_REF)
    conic_product = load_json(CONIC_PRODUCT_REF)
    split_gate = load_json(NULLPOLY_SPLIT_GATE_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(
        moving["schema_version"]
        == "f17-32-m3-rank6-a385-two-core-moving-slope-incidence-v1",
        "moving-slope incidence schema mismatch",
    )
    require(
        high_core["schema_version"]
        == "f17-32-m3-rank6-a385-two-core-high-core-quotient-v1",
        "high-core quotient schema mismatch",
    )
    require(
        conic_product["schema_version"]
        == "f17-32-m3-rank6-a385-two-core-conic-product-collapse-v1",
        "conic product-collapse schema mismatch",
    )
    require(
        split_gate["schema_version"] == "f17-32-m3-nullpolynomial-split-locator-gate-v1",
        "split-gate schema mismatch",
    )
    require(split_gate["summary"]["split_locator_gate_available"], "split gate unavailable")
    require(N % P != 0, "X^512-1 is not separable in this characteristic")
    require(FINITE_BUDGET == 6 and PROJECTIVE_BUDGET == 6, "unexpected budget")

    j_value = N - AGREEMENT
    t_value = AGREEMENT - K
    m_value = j_value + 1
    support_size = m_value + RANK
    h_value = support_size - t_value
    residual_vector_dimension = h_value - BASE_CORE_SIZE
    residual_projective_dimension = residual_vector_dimension - 1
    positive_core_upper = high_core["summary"]["positive_dimensional_external_core_upper_bound"]
    line_high_core_min = high_core["summary"]["line_high_core_external_core_min"]
    conic_high_core_min = high_core["summary"]["conic_high_core_external_core_min"]
    line_incidence_safe_max = moving["summary"]["line_projective_safe_external_core_max"]
    conic_incidence_safe_max = moving["summary"][
        "conic_pair_overlap_projective_safe_external_core_max"
    ]
    conic_product_closed = conic_product["summary"][
        "conic_product_collapse_closed_external_core_range"
    ]

    fixed_base_roots = BASE_CORE_SIZE
    residual_extra_root_cap = residual_vector_dimension - 1
    split_locator_degree = j_value
    total_nonforced_root_cap = fixed_base_roots + residual_extra_root_cap
    line_product_closed_max = split_locator_degree - total_nonforced_root_cap - 1
    line_product_min_core_for_split = line_product_closed_max + 1
    tangent_tail_safe_core_min = split_locator_degree + 1 - PROJECTIVE_BUDGET
    tangent_tail_residual_radius_at_min = split_locator_degree - tangent_tail_safe_core_min
    tangent_tail_projective_bound_at_min = tangent_tail_residual_radius_at_min + 1
    tangent_condition_margin_at_line_min = (
        (N - line_high_core_min - K) // 3 - (split_locator_degree - line_high_core_min)
    )
    tangent_condition_margin_at_conic_min = (
        (N - conic_high_core_min - K) // 3 - (split_locator_degree - conic_high_core_min)
    )

    require(j_value == 127, "A=385 locator degree changed")
    require(t_value == 129, "A=385 t changed")
    require(m_value == 128, "A=385 base support size changed")
    require(h_value == 5, "A=385 boundary defect should be five")
    require(residual_vector_dimension == 3, "fixed two-core residual dimension changed")
    require(residual_projective_dimension == 2, "fixed two-core residual should be P^2")
    require(line_high_core_min == line_incidence_safe_max + 1 == 71, "line threshold")
    require(conic_high_core_min == conic_incidence_safe_max + 1 == 68, "conic threshold")
    require(positive_core_upper == 126, "positive-dimensional core cap changed")
    require(total_nonforced_root_cap == 4, "fixed two-core root cap changed")
    require(line_product_closed_max == 122, "line product closure endpoint changed")
    require(line_product_min_core_for_split == 123, "line product split threshold changed")
    require(tangent_tail_safe_core_min == 122, "tangent tail safe threshold changed")
    require(tangent_tail_projective_bound_at_min == PROJECTIVE_BUDGET, "tail not budget-safe")
    require(tangent_condition_margin_at_line_min >= 0, "line high-core not in tangent range")
    require(tangent_condition_margin_at_conic_min >= 0, "conic high-core not in tangent range")
    require(conic_product_closed == [68, 122], "conic product dependency changed")

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "object": "A=385 separated rank-6 fixed two-core high-core line/conic closure",
        "row": {
            "code": "RS[F_17^32,H,256]",
            "n": N,
            "k": K,
            "field": "F_17^32",
            "domain_hash": descriptor["row"]["domain_hash"],
            "q_line": Q_LINE,
        },
        "source_artifacts": {
            "row_descriptor": {"ref": ROW_DESCRIPTOR_REF, "sha256": sha256_file(ROW_DESCRIPTOR_REF)},
            "a385_two_core_moving_slope_incidence": {
                "ref": MOVING_SLOPE_REF,
                "sha256": sha256_file(MOVING_SLOPE_REF),
            },
            "a385_two_core_high_core_quotient": {
                "ref": HIGH_CORE_QUOTIENT_REF,
                "sha256": sha256_file(HIGH_CORE_QUOTIENT_REF),
            },
            "a385_two_core_conic_product_collapse": {
                "ref": CONIC_PRODUCT_REF,
                "sha256": sha256_file(CONIC_PRODUCT_REF),
            },
            "nullpolynomial_split_locator_gate": {
                "ref": NULLPOLY_SPLIT_GATE_REF,
                "sha256": sha256_file(NULLPOLY_SPLIT_GATE_REF),
            },
        },
        "agreement": {
            "A": AGREEMENT,
            "j": j_value,
            "t": t_value,
            "m": m_value,
            "direction_rank": RANK,
            "combined_support_size": support_size,
            "boundary_defect_h": h_value,
            "forced_base_core_size": BASE_CORE_SIZE,
            "residual_vector_dimension_after_core": residual_vector_dimension,
            "projective_Q_search_dimension_after_core": residual_projective_dimension,
            "split_locator_degree": split_locator_degree,
        },
        "line_product_collapse": {
            "setup": (
                "Let U be the two-dimensional residual subspace defining a line "
                "component in the fixed two-core Q-plane, and let U^perp=<phi> "
                "in the dual Q-plane.  A forced external root s has ev_s in span(phi)."
            ),
            "evaluation_functional_formula": {
                "notation": (
                    "Write G=q_0 P_X+H, H=A*T^(m-1)+B*T^(m-2)+..., "
                    "P_X=T^m+p*T^(m-1)+..., and C=B-A*p."
                ),
                "ev_s_coefficients": [
                    "H(s)",
                    "s*H(s)-A*P_X(s)",
                    "s^2*H(s)-(A*s+C)*P_X(s)",
                ],
                "valid_for": "s outside X, where P_X(s) is nonzero",
            },
            "two_forced_roots_classification": [
                {
                    "case": "common_root_pencil",
                    "hypotheses": "u!=0 and A!=0 in the dual-line notation",
                    "consequence": (
                        "Two distinct forced roots make the compatibility "
                        "identity vanish identically.  Thus U is the pencil "
                        "R(alpha)=0.  For R=(T-alpha)S, "
                        "L_{E R}=F*S with F=(T-alpha)H-A*P_X and deg F<=126."
                    ),
                    "root_count": (
                        "F has the two fixed base-core roots and at most one "
                        "additional base root x=alpha; S has at most one "
                        "further subgroup root.  Thus a degree-127 split "
                        "locator needs external forced core size at least 123."
                    ),
                },
                {
                    "case": "product_without_reduction",
                    "hypotheses": "all remaining two-forced-root line cases",
                    "consequence": (
                        "The top terms or the line U force modular reduction "
                        "to vanish on U: L_{E R}=H*R for R in U."
                    ),
                    "root_count": (
                        "H carries the two fixed base roots and the forced "
                        "external core, while R contributes at most two further "
                        "subgroup roots.  Thus a degree-127 split locator again "
                        "needs external forced core size at least 123."
                    ),
                },
            ],
            "minimum_external_core_for_any_degree_127_split_locator": (
                line_product_min_core_for_split
            ),
            "closed_external_core_range_by_product_collapse": [
                line_high_core_min,
                line_product_closed_max,
            ],
        },
        "punctured_tangent_tail": {
            "punctured_row": (
                "After removing a forced external core E, the residual row has "
                "n'=512-|E|, a'=385, and r'=127-|E|."
            ),
            "tangent_range_check": (
                "For every high-core line or conic threshold here, "
                "r' <= floor((n'-256)/3), so the high-agreement projective "
                "tangent staircase applies."
            ),
            "projective_bound": "projective bad slopes on the branch <= r'+1 = 128-|E|",
            "projective_safe_external_core_min": tangent_tail_safe_core_min,
            "projective_bound_at_safe_min": tangent_tail_projective_bound_at_min,
            "closed_external_core_range_by_tangent_tail": [
                tangent_tail_safe_core_min,
                positive_core_upper,
            ],
        },
        "component_closures": {
            "line": {
                "small_core_incidence_safe_range": [0, line_incidence_safe_max],
                "high_core_product_closed_range": [
                    line_high_core_min,
                    line_product_closed_max,
                ],
                "high_core_tangent_tail_safe_range": [
                    tangent_tail_safe_core_min,
                    positive_core_upper,
                ],
                "all_fixed_two_core_line_components_projective_safe": True,
            },
            "irreducible_conic": {
                "small_core_pair_overlap_safe_range": [0, conic_incidence_safe_max],
                "high_core_product_closed_range": conic_product_closed,
                "high_core_tangent_tail_safe_range": [
                    tangent_tail_safe_core_min,
                    positive_core_upper,
                ],
                "all_fixed_two_core_irreducible_conic_components_projective_safe": True,
            },
        },
        "sampler_denominators": {
            "finite_line": {
                "denominator": Q_LINE,
                "denominator_formula": "|F|",
                "budget_floor_denominator_over_2_128": FINITE_BUDGET,
            },
            "projective_line": {
                "denominator": PROJECTIVE_DENOMINATOR,
                "denominator_formula": "|P^1(F)| = |F| + 1",
                "budget_floor_denominator_over_2_128": PROJECTIVE_BUDGET,
            },
        },
        "summary": {
            "agreement": AGREEMENT,
            "split_locator_degree": split_locator_degree,
            "line_high_core_external_core_min": line_high_core_min,
            "conic_high_core_external_core_min": conic_high_core_min,
            "positive_dimensional_external_core_upper_bound": positive_core_upper,
            "fixed_base_roots": fixed_base_roots,
            "residual_extra_root_cap": residual_extra_root_cap,
            "line_product_collapse_closed_external_core_range": [
                line_high_core_min,
                line_product_closed_max,
            ],
            "line_product_collapse_min_core_for_any_split_locator": (
                line_product_min_core_for_split
            ),
            "punctured_tangent_tail_projective_safe_external_core_min": (
                tangent_tail_safe_core_min
            ),
            "punctured_tangent_tail_projective_bound_at_min": (
                tangent_tail_projective_bound_at_min
            ),
            "line_high_core_closed_external_core_range": [
                line_high_core_min,
                positive_core_upper,
            ],
            "conic_high_core_closed_external_core_range": [
                conic_high_core_min,
                positive_core_upper,
            ],
            "line_high_core_components_projective_safe": True,
            "conic_high_core_components_projective_safe": True,
            "fixed_two_core_line_or_conic_moving_slope_components_projective_safe": True,
        },
        "checks": [
            "row descriptor and dependency schemas match",
            "A=385 fixed two-core residual has Q-plane P^2 and locator degree 127",
            "line high-core begins at e_G=71 and conic high-core begins at e_G=68",
            "two forced roots on a line component trigger the product-collapse classification",
            "line product collapse requires e_G>=123 for any degree-127 split locator",
            "line product collapse closes e_G=71..122",
            "conic product-collapse dependency closes e_G=68..122",
            "punctured projective tangent tail is budget-safe for e_G>=122",
            "line and conic high-core ranges are covered by product collapse plus tangent tail",
        ],
        "nonclaims": [
            "does not prove a row-level M3 safe-side bound",
            "does not prove that every A=385 over-budget branch has a fixed two-point base core",
            "does not close moving-core or no-common-core A=385 branches",
            "does not classify overlapping-support rank-6 pencils",
            "does not prove endpoint payment outside the projective tangent/tail accounting used here",
            "does not audit quotient or extension overlap for arbitrary root tables",
        ],
    }


def check_certificate(path: Path, certificate: dict[str, Any]) -> None:
    expected = render(certificate)
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"A=385 two-core high-core closure mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    print("F_17^32 M3 rank-6 A=385 fixed two-core high-core closure")
    print(
        "line high cores={0}; conic high cores={1}".format(
            summary["line_high_core_closed_external_core_range"],
            summary["conic_high_core_closed_external_core_range"],
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
        check_certificate(args.check, certificate)
    print_summary(certificate)


if __name__ == "__main__":
    main()
