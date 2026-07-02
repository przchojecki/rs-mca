#!/usr/bin/env python3
"""Verify the A=385 rank-6 fixed-core synthesis closure."""

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


SCHEMA_VERSION = "f17-32-m3-rank6-a385-fixed-core-synthesis-v1"
Q_LINE = 17**32
TARGET_BITS = 128
FINITE_BUDGET = Q_LINE // 2**TARGET_BITS
PROJECTIVE_DENOMINATOR = Q_LINE + 1
PROJECTIVE_BUDGET = PROJECTIVE_DENOMINATOR // 2**TARGET_BITS
AGREEMENT = 385
RANK = 6
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
A385_BASE_CORE_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank6-a385-base-core-closure/"
    "f17_32_n512_k256_m3_rank6_a385_base_core_closure.json"
)
A385_THREE_CORE_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank6-a385-three-core-quadratic-cut/"
    "f17_32_n512_k256_m3_rank6_a385_three_core_quadratic_cut.json"
)
A385_THREE_CORE_RESIDUAL_REF = (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-rank6-a385-three-core-residual-closure/"
    "f17_32_n512_k256_m3_rank6_a385_three_core_residual_closure.json"
)
A385_TWO_CORE_REF = (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-rank6-a385-two-core-conic-pair-safety/"
    "f17_32_n512_k256_m3_rank6_a385_two_core_conic_pair_safety.json"
)
A385_TWO_CORE_COMPONENT_CUT_REF = (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-rank6-a385-two-core-component-cut-safety/"
    "f17_32_n512_k256_m3_rank6_a385_two_core_component_cut_safety.json"
)
A385_TWO_CORE_GLOBAL_COMPONENT_REF = (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-rank6-a385-two-core-global-component-slope-dichotomy/"
    "f17_32_n512_k256_m3_rank6_a385_two_core_global_component_slope_dichotomy.json"
)
A385_TWO_CORE_SLOPE_FREE_REF = (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-rank6-a385-two-core-slope-free-empty/"
    "f17_32_n512_k256_m3_rank6_a385_two_core_slope_free_empty.json"
)
A385_TWO_CORE_MOVING_SLOPE_REF = (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-rank6-a385-two-core-moving-slope-incidence/"
    "f17_32_n512_k256_m3_rank6_a385_two_core_moving_slope_incidence.json"
)
A385_TWO_CORE_HIGH_CORE_QUOTIENT_REF = (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-rank6-a385-two-core-high-core-quotient/"
    "f17_32_n512_k256_m3_rank6_a385_two_core_high_core_quotient.json"
)
A385_TWO_CORE_CONIC_PRODUCT_REF = (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-rank6-a385-two-core-conic-product-collapse/"
    "f17_32_n512_k256_m3_rank6_a385_two_core_conic_product_collapse.json"
)
A385_TWO_CORE_HIGH_CORE_CLOSURE_REF = (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-rank6-a385-two-core-high-core-closure/"
    "f17_32_n512_k256_m3_rank6_a385_two_core_high_core_closure.json"
)


EXPECTED_SCHEMAS = {
    A385_BASE_CORE_REF: "f17-32-m3-rank6-a385-base-core-closure-v1",
    A385_THREE_CORE_REF: "f17-32-m3-rank6-a385-three-core-quadratic-cut-v1",
    A385_THREE_CORE_RESIDUAL_REF: (
        "f17-32-m3-rank6-a385-three-core-residual-closure-v1"
    ),
    A385_TWO_CORE_REF: "f17-32-m3-rank6-a385-two-core-conic-pair-safety-v1",
    A385_TWO_CORE_COMPONENT_CUT_REF: (
        "f17-32-m3-rank6-a385-two-core-component-cut-safety-v1"
    ),
    A385_TWO_CORE_GLOBAL_COMPONENT_REF: (
        "f17-32-m3-rank6-a385-two-core-global-component-slope-dichotomy-v1"
    ),
    A385_TWO_CORE_SLOPE_FREE_REF: (
        "f17-32-m3-rank6-a385-two-core-slope-free-empty-v1"
    ),
    A385_TWO_CORE_MOVING_SLOPE_REF: (
        "f17-32-m3-rank6-a385-two-core-moving-slope-incidence-v1"
    ),
    A385_TWO_CORE_HIGH_CORE_QUOTIENT_REF: (
        "f17-32-m3-rank6-a385-two-core-high-core-quotient-v1"
    ),
    A385_TWO_CORE_CONIC_PRODUCT_REF: (
        "f17-32-m3-rank6-a385-two-core-conic-product-collapse-v1"
    ),
    A385_TWO_CORE_HIGH_CORE_CLOSURE_REF: (
        "f17-32-m3-rank6-a385-two-core-high-core-closure-v1"
    ),
}


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


def check_dependency(ref: str, data: dict[str, Any]) -> None:
    require(data["schema_version"] == EXPECTED_SCHEMAS[ref], f"schema mismatch for {ref}")
    require(data["status"] == "PROVED / AUDIT", f"status mismatch for {ref}")
    require(data["agreement"]["A"] == AGREEMENT, f"agreement mismatch for {ref}")
    require(data["agreement"]["direction_rank"] == RANK, f"direction rank mismatch for {ref}")


def build_certificate() -> dict[str, Any]:
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    dependencies = {ref: load_json(ref) for ref in EXPECTED_SCHEMAS}

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(N % P != 0, "X^512-1 is not separable in this characteristic")
    require(FINITE_BUDGET == 6 and PROJECTIVE_BUDGET == 6, "unexpected budget")
    for ref, data in dependencies.items():
        check_dependency(ref, data)

    base_core = dependencies[A385_BASE_CORE_REF]
    three_core = dependencies[A385_THREE_CORE_REF]
    three_residual = dependencies[A385_THREE_CORE_RESIDUAL_REF]
    two_core = dependencies[A385_TWO_CORE_REF]
    component_cut = dependencies[A385_TWO_CORE_COMPONENT_CUT_REF]
    global_component = dependencies[A385_TWO_CORE_GLOBAL_COMPONENT_REF]
    slope_free = dependencies[A385_TWO_CORE_SLOPE_FREE_REF]
    moving_slope = dependencies[A385_TWO_CORE_MOVING_SLOPE_REF]
    high_core = dependencies[A385_TWO_CORE_HIGH_CORE_QUOTIENT_REF]
    conic_product = dependencies[A385_TWO_CORE_CONIC_PRODUCT_REF]
    high_core_closure = dependencies[A385_TWO_CORE_HIGH_CORE_CLOSURE_REF]

    j_value = N - AGREEMENT
    t_value = AGREEMENT - K
    m_value = j_value + 1
    support_size = m_value + RANK
    h_value = support_size - t_value
    require(j_value == 127 and t_value == 129 and m_value == 128, "A385 dimensions changed")
    require(h_value == 5, "A385 boundary defect should be five")

    require(
        base_core["summary"]["fixed_four_base_core_branch_projective_safe"]
        and base_core["summary"]["support_wise_projective_total_upper_bound"] <= PROJECTIVE_BUDGET,
        "four-or-more fixed core closure unavailable",
    )
    require(
        three_core["summary"]["fixed_three_core_nonzero_quadratic_branch_projective_safe"]
        and three_core["summary"][
            "support_wise_projective_total_upper_bound_under_quadratic_cut"
        ]
        <= PROJECTIVE_BUDGET,
        "three-core nonzero quadratic branch not closed",
    )
    require(
        three_residual["summary"]["fixed_three_core_residual_line_projective_safe"]
        and three_residual["summary"]["remaining_fixed_three_core_residual_after_this_packet"]
        == [],
        "three-core residual branch not closed",
    )
    require(
        two_core["summary"]["fixed_two_core_no_common_component_branch_projective_safe"]
        and two_core["summary"]["support_wise_projective_total_upper_bound_under_conic_pair"]
        <= PROJECTIVE_BUDGET,
        "two-core no-common-component branch not closed",
    )
    require(
        component_cut["summary"]["fixed_two_core_component_cut_branch_projective_safe"]
        and component_cut["summary"][
            "support_wise_projective_total_upper_bound_under_component_cut"
        ]
        <= PROJECTIVE_BUDGET,
        "two-core component-cut branch not closed",
    )
    require(
        global_component["summary"]["constant_slope_non_base_branch_projective_safe"],
        "two-core constant-slope branch not closed",
    )
    require(
        slope_free["summary"]["slope_free_base_locus_empty"]
        and slope_free["summary"]["slope_free_global_component_empty"]
        and slope_free["summary"]["remaining_residual"]
        == "fixed two-core determined nonconstant slope map",
        "two-core slope-free branch not empty",
    )
    require(
        moving_slope["summary"]["remaining_residual_after_incidence"]
        == "fixed two-core moving-slope high-core line/conic branches",
        "two-core moving-slope incidence residual changed",
    )
    require(
        high_core["summary"]["remaining_residual_after_quotient_normal_form"]
        == "fixed two-core high-core quotient pencils/families",
        "two-core high-core quotient residual changed",
    )
    require(
        conic_product["summary"]["conic_product_collapse_closed_external_core_range"]
        == [68, 122],
        "two-core conic product-collapse range changed",
    )
    require(
        high_core_closure["summary"]["fixed_two_core_line_or_conic_moving_slope_components_projective_safe"]
        and high_core_closure["summary"]["line_high_core_closed_external_core_range"]
        == [71, 126]
        and high_core_closure["summary"]["conic_high_core_closed_external_core_range"]
        == [68, 126],
        "two-core high-core moving-slope branch not closed",
    )

    branch_synthesis = [
        {
            "fixed_base_core_size": ">=4",
            "consumed_by": [A385_BASE_CORE_REF],
            "projective_total_upper_bound": 2,
            "status": "projective_budget_safe",
            "reason": (
                "four fixed base roots collapse the A=385 Q-space to one "
                "projective Q-class, so the branch contributes at most one "
                "finite noncontained parameter plus the projective endpoint"
            ),
        },
        {
            "fixed_base_core_size": 3,
            "consumed_by": [A385_THREE_CORE_REF, A385_THREE_CORE_RESIDUAL_REF],
            "status": "projective_budget_safe",
            "reason": (
                "the nonzero quadratic-cut branch has projective total at most "
                "3, and the ratio-identically-consistent residual line is "
                "closed for every external forced-core size"
            ),
        },
        {
            "fixed_base_core_size": 2,
            "consumed_by": [
                A385_TWO_CORE_REF,
                A385_TWO_CORE_COMPONENT_CUT_REF,
                A385_TWO_CORE_GLOBAL_COMPONENT_REF,
                A385_TWO_CORE_SLOPE_FREE_REF,
                A385_TWO_CORE_MOVING_SLOPE_REF,
                A385_TWO_CORE_HIGH_CORE_QUOTIENT_REF,
                A385_TWO_CORE_CONIC_PRODUCT_REF,
                A385_TWO_CORE_HIGH_CORE_CLOSURE_REF,
            ],
            "status": "projective_budget_safe",
            "reason": (
                "the conic-pair, component-cut, constant-slope, slope-free, "
                "moving-slope incidence, quotient-normal-form, conic-product, "
                "and high-core closure packets exhaust the fixed two-core "
                "line/conic residual tree"
            ),
        },
    ]

    remaining_frontier = [
        "separated A=385 branches without a fixed two-point base core",
        "moving-core/no-common-core A=385 branches",
        "overlapping-support rank-6 pencils",
        "row-level M3 synthesis across all A=385 rank-6 buckets",
    ]

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "object": (
            "A=385 separated rank-6 fixed forced base-core synthesis "
            "for core size at least two"
        ),
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
            **{
                ref.rsplit("/", 1)[-1].removesuffix(".json"): {
                    "ref": ref,
                    "sha256": sha256_file(ref),
                }
                for ref in EXPECTED_SCHEMAS
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
            "split_locator_degree": j_value,
            "projective_Q_search_dimension_before_core": h_value - 1,
        },
        "theorem": {
            "statement": (
                "Inside the separated A=385 rank-6 boundary, every branch whose "
                "split-locator candidates share a fixed forced base-root core "
                "of size at least two is projective-budget safe for the pinned "
                "F_17^32 row."
            ),
            "core_size_ge_4": (
                "The fixed four-core packet applies after choosing any common "
                "four-point subcore and gives projective total at most 2."
            ),
            "core_size_3": (
                "The fixed three-core packet either cuts the residual Q-line by "
                "a nonzero binary quadratic, or leaves the ratio-identically "
                "consistent residual.  The residual-closure packet closes the "
                "latter by incidence, product collapse, and the punctured "
                "projective tangent tail."
            ),
            "core_size_2": (
                "The fixed two-core packet tree exhausts the residual Q-plane: "
                "no-common-component conic pairs, component cuts, constant "
                "slope, empty slope-free locus, and nonconstant moving-slope "
                "line/conic components.  The high-core closure packet closes "
                "the last line/conic residual by product collapse and tangent "
                "tail accounting."
            ),
            "contrapositive_use": (
                "Any remaining separated A=385 over-budget obstruction must "
                "avoid a fixed forced base core of size two in the counted "
                "branch."
            ),
        },
        "branch_synthesis": branch_synthesis,
        "remaining_frontier_after_this_packet": remaining_frontier,
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
            "boundary_defect_h": h_value,
            "projective_Q_search_dimension_before_core": h_value - 1,
            "projective_budget": PROJECTIVE_BUDGET,
            "fixed_four_or_more_core_projective_safe": True,
            "fixed_three_core_projective_safe": True,
            "fixed_two_core_projective_safe": True,
            "fixed_base_core_size_at_least_two_projective_safe": True,
            "remaining_frontier_count": len(remaining_frontier),
        },
        "checks": [
            "row descriptor and dependency schemas match",
            "A=385 dimensions are j=127, t=129, m=128, h=5",
            "fixed four-or-more core branch is projective-budget safe",
            "fixed three-core nonzero quadratic branch is projective-budget safe",
            "fixed three-core residual line has no remaining external-core range",
            "fixed two-core no-common-component conic-pair branch is projective-budget safe",
            "fixed two-core component-cut branch is projective-budget safe",
            "fixed two-core constant-slope branch is projective-budget safe",
            "fixed two-core slope-free branch is empty",
            "fixed two-core moving-slope high-core line/conic branches are closed",
            "the remaining A=385 frontier is explicitly outside the fixed two-core hypothesis",
        ],
        "nonclaims": [
            "does not prove every A=385 over-budget branch has a fixed two-point base core",
            "does not close moving-core or no-common-core A=385 branches",
            "does not classify overlapping-support rank-6 pencils",
            "does not prove endpoint payment outside the cited projective accounting and tangent-tail packets",
            "does not compute arbitrary A=385 rank-6 root tables",
            "does not produce a row-level M3 safe-side bound",
        ],
    }


def check_certificate(path: Path, certificate: dict[str, Any]) -> None:
    expected = render(certificate)
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"A=385 fixed-core synthesis mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    print("F_17^32 M3 rank-6 A=385 fixed-core synthesis")
    print(
        "fixed core >=2 safe={fixed_base_core_size_at_least_two_projective_safe}; remaining frontier entries={remaining_frontier_count}".format(
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
        check_certificate(args.check, certificate)
    print_summary(certificate)


if __name__ == "__main__":
    main()
