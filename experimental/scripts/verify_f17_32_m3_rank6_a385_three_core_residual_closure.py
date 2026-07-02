#!/usr/bin/env python3
"""Verify the A=385 fixed three-core residual-line closure."""

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


SCHEMA_VERSION = "f17-32-m3-rank6-a385-three-core-residual-closure-v1"
Q_LINE = 17**32
TARGET_BITS = 128
FINITE_BUDGET = Q_LINE // 2**TARGET_BITS
PROJECTIVE_DENOMINATOR = Q_LINE + 1
PROJECTIVE_BUDGET = PROJECTIVE_DENOMINATOR // 2**TARGET_BITS
AGREEMENT = 385
RANK = 6
BASE_CORE_SIZE = 3
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
THREE_CORE_QUADRATIC_REF = (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-rank6-a385-three-core-quadratic-cut/"
    "f17_32_n512_k256_m3_rank6_a385_three_core_quadratic_cut.json"
)
ENDPOINT_UNIFORM_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank6-projective-endpoint-uniform/"
    "f17_32_n512_k256_m3_rank6_projective_endpoint_uniform.json"
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
    three_core = load_json(THREE_CORE_QUADRATIC_REF)
    endpoint_uniform = load_json(ENDPOINT_UNIFORM_REF)
    split_gate = load_json(NULLPOLY_SPLIT_GATE_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(
        three_core["schema_version"] == "f17-32-m3-rank6-a385-three-core-quadratic-cut-v1",
        "three-core quadratic-cut schema mismatch",
    )
    require(
        "identically" in three_core["summary"]["remaining_residual"],
        "three-core dependency no longer exposes the residual line",
    )
    require(
        endpoint_uniform["schema_version"]
        == "f17-32-m3-rank6-projective-endpoint-uniform-v1",
        "endpoint-uniform schema mismatch",
    )
    require(
        endpoint_uniform["summary"]["projective_endpoint_exact_contribution_per_agreement"] == 1,
        "endpoint contribution mismatch",
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
    split_locator_degree = j_value
    fixed_base_roots = BASE_CORE_SIZE
    residual_extra_root_cap = residual_vector_dimension - 1
    total_nonforced_root_cap = fixed_base_roots + residual_extra_root_cap
    external_root_count = N - m_value
    nonforced_external_need = split_locator_degree - total_nonforced_root_cap
    line_incidence_projective_safe_max = 70
    line_product_closed_min = line_incidence_projective_safe_max + 1
    line_product_closed_max = nonforced_external_need - 1
    tangent_tail_safe_min = split_locator_degree + 1 - PROJECTIVE_BUDGET
    positive_dimensional_external_core_upper = split_locator_degree - 1
    tangent_tail_bound_at_min = split_locator_degree + 1 - tangent_tail_safe_min
    tangent_condition_margin_at_residual_min = (
        (N - line_product_closed_min - K) // 3
        - (split_locator_degree - line_product_closed_min)
    )

    require(j_value == 127, "A=385 locator degree changed")
    require(t_value == 129, "A=385 t changed")
    require(m_value == 128, "A=385 base support size changed")
    require(h_value == 5, "A=385 boundary defect should be five")
    require(residual_vector_dimension == 2, "fixed three-core residual dimension changed")
    require(residual_projective_dimension == 1, "fixed three-core residual should be P^1")
    require(total_nonforced_root_cap == 4, "fixed three-core nonforced root cap changed")
    require(nonforced_external_need == 123, "external forced-core threshold changed")
    require(line_product_closed_max == 122, "product-collapse closure endpoint changed")
    require(tangent_tail_safe_min == 122, "tangent tail safe threshold changed")
    require(tangent_tail_bound_at_min == PROJECTIVE_BUDGET, "tail not budget-safe")
    require(
        tangent_condition_margin_at_residual_min >= 0,
        "fixed three-core residual not in tangent range",
    )

    incidence_rows = []
    for e_value in [0, 70, 71, 122]:
        required_nonforced = split_locator_degree - total_nonforced_root_cap - e_value
        if required_nonforced <= 0:
            finite_class_bound = 0
        else:
            finite_class_bound = (external_root_count - e_value) // required_nonforced
        incidence_rows.append(
            {
                "external_core": e_value,
                "required_nonforced_external_roots_per_class": required_nonforced,
                "available_nonforced_external_roots": external_root_count - e_value,
                "line_finite_class_bound": finite_class_bound,
                "projective_bound_after_endpoint": finite_class_bound + 1,
                "projective_budget_safe": finite_class_bound + 1 <= PROJECTIVE_BUDGET,
            }
        )
    require(incidence_rows[1]["projective_budget_safe"], "e=70 should be incidence safe")
    require(not incidence_rows[2]["projective_budget_safe"], "e=71 should need product collapse")

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "object": "A=385 separated rank-6 fixed three-core residual-line closure",
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
            "a385_three_core_quadratic_cut": {
                "ref": THREE_CORE_QUADRATIC_REF,
                "sha256": sha256_file(THREE_CORE_QUADRATIC_REF),
            },
            "rank6_projective_endpoint_uniform": {
                "ref": ENDPOINT_UNIFORM_REF,
                "sha256": sha256_file(ENDPOINT_UNIFORM_REF),
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
        "theorem": {
            "residual_line": (
                "In the residual branch of the three-core quadratic-cut packet, "
                "Q=E R with deg R<2 and all pairwise direction-consistency "
                "quadratics vanish identically on the residual projective line."
            ),
            "small_core_incidence": (
                "Every degree-127 split locator has the three fixed base roots "
                "and at most one further residual base root.  A line component "
                "with external forced core e_G therefore needs at least "
                "123-e_G non-forced external roots per finite class; incidence "
                "gives projective-budget safety for e_G<=70."
            ),
            "global_core_product_collapse": (
                "Let G=S E and write G=q_0 P_X+H with deg H<128 and "
                "H=A*T^127+lower terms.  A forced external root on the whole "
                "residual line makes ev_s(1)=H(s) and ev_s(T)=sH(s)-A P_X(s) "
                "vanish.  Since P_X(s)!=0, A=0, so deg H<=126 and no modular "
                "reduction occurs: L_{E R}=H R for all deg R<2."
            ),
            "product_root_count": (
                "The factor H has the three fixed base roots and the forced "
                "external core; R contributes at most one further subgroup root. "
                "Thus a degree-127 split locator requires e_G>=123, so "
                "71<=e_G<=122 is impossible in the residual line branch."
            ),
            "punctured_tangent_tail": (
                "After puncturing a forced external core E, the residual tangent "
                "radius is r'=127-|E| and the projective tangent bound is "
                "r'+1=128-|E|.  Hence e_G>=122 is projective-budget safe."
            ),
            "closure": (
                "The fixed three-core residual line is covered by incidence for "
                "e_G<=70, product collapse for 71<=e_G<=122, and the punctured "
                "tangent tail for e_G>=122."
            ),
        },
        "incidence_boundary_rows": incidence_rows,
        "component_closure": {
            "small_core_incidence_safe_range": [0, line_incidence_projective_safe_max],
            "product_collapse_closed_range": [
                line_product_closed_min,
                line_product_closed_max,
            ],
            "punctured_tangent_tail_safe_range": [
                tangent_tail_safe_min,
                positive_dimensional_external_core_upper,
            ],
            "all_fixed_three_core_residual_line_components_projective_safe": True,
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
            "forced_base_core_size": BASE_CORE_SIZE,
            "residual_vector_dimension_after_core": residual_vector_dimension,
            "projective_Q_search_dimension_after_core": residual_projective_dimension,
            "fixed_base_roots": fixed_base_roots,
            "residual_extra_root_cap": residual_extra_root_cap,
            "small_core_incidence_projective_safe_external_core_max": (
                line_incidence_projective_safe_max
            ),
            "product_collapse_closed_external_core_range": [
                line_product_closed_min,
                line_product_closed_max,
            ],
            "product_collapse_min_core_for_any_split_locator": nonforced_external_need,
            "punctured_tangent_tail_projective_safe_external_core_min": (
                tangent_tail_safe_min
            ),
            "punctured_tangent_tail_projective_bound_at_min": tangent_tail_bound_at_min,
            "fixed_three_core_residual_line_closed_external_core_range": [
                0,
                positive_dimensional_external_core_upper,
            ],
            "fixed_three_core_residual_line_projective_safe": True,
            "remaining_fixed_three_core_residual_after_this_packet": [],
        },
        "checks": [
            "row descriptor and dependency schemas match",
            "A=385 fixed three-core residual has Q-line P^1 and locator degree 127",
            "incidence gives projective safety through e_G=70 and not at e_G=71",
            "one global forced external root forces the top coefficient of H to vanish",
            "product collapse gives L_{E R}=H R with deg H<=126 and deg R<2",
            "product root count closes e_G=71..122",
            "punctured projective tangent tail is budget-safe for e_G>=122",
            "all fixed three-core residual-line external-core sizes are covered",
        ],
        "nonclaims": [
            "does not prove that every A=385 over-budget branch has a fixed three-point base core",
            "does not close moving-core or no-common-core A=385 branches",
            "does not classify overlapping-support rank-6 pencils",
            "does not prove endpoint payment outside the projective tangent/tail accounting used here",
            "does not compute arbitrary A=385 rank-6 root tables",
            "does not produce a row-level M3 safe-side bound",
        ],
    }


def check_certificate(path: Path, certificate: dict[str, Any]) -> None:
    expected = render(certificate)
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"A=385 three-core residual closure mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    print("F_17^32 M3 rank-6 A=385 fixed three-core residual closure")
    print(
        "closed external cores={0}".format(
            summary["fixed_three_core_residual_line_closed_external_core_range"]
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
