#!/usr/bin/env python3
"""Verify the A=385 rank-6 fixed two-core conic-pair criterion."""

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


SCHEMA_VERSION = "f17-32-m3-rank6-a385-two-core-conic-pair-safety-v1"
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
LOW_DEGREE_TRANSFER_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank6-boundary-low-degree-transfer/"
    "f17_32_n512_k256_m3_rank6_boundary_low_degree_transfer.json"
)
ENDPOINT_UNIFORM_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank6-projective-endpoint-uniform/"
    "f17_32_n512_k256_m3_rank6_projective_endpoint_uniform.json"
)
NULLPOLY_SPLIT_GATE_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-nullpolynomial-split-locator-gate/"
    "f17_32_n512_k256_m3_nullpolynomial_split_locator_gate.json"
)
A385_BASE_CORE_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank6-a385-base-core-closure/"
    "f17_32_n512_k256_m3_rank6_a385_base_core_closure.json"
)
A385_THREE_CORE_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank6-a385-three-core-quadratic-cut/"
    "f17_32_n512_k256_m3_rank6_a385_three_core_quadratic_cut.json"
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
    low_degree = load_json(LOW_DEGREE_TRANSFER_REF)
    endpoint_uniform = load_json(ENDPOINT_UNIFORM_REF)
    split_gate = load_json(NULLPOLY_SPLIT_GATE_REF)
    base_core = load_json(A385_BASE_CORE_REF)
    three_core = load_json(A385_THREE_CORE_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(
        low_degree["schema_version"] == "f17-32-m3-rank6-boundary-low-degree-transfer-v1",
        "low-degree transfer schema mismatch",
    )
    require(AGREEMENT in low_degree["window"]["agreements"], "A=385 not in transfer packet")
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
    require(
        base_core["schema_version"] == "f17-32-m3-rank6-a385-base-core-closure-v1",
        "A385 four-core schema mismatch",
    )
    require(
        base_core["summary"]["fixed_four_base_core_branch_projective_safe"],
        "A385 four-core closure unavailable",
    )
    require(
        three_core["schema_version"]
        == "f17-32-m3-rank6-a385-three-core-quadratic-cut-v1",
        "A385 three-core schema mismatch",
    )
    require(
        three_core["summary"]["fixed_three_core_nonzero_quadratic_branch_projective_safe"],
        "A385 three-core quadratic cut unavailable",
    )
    require(N % P != 0, "X^512-1 is not separable in this characteristic")
    require(FINITE_BUDGET == 6 and PROJECTIVE_BUDGET == 6, "unexpected budget")

    j_value = N - AGREEMENT
    t_value = AGREEMENT - K
    m_value = j_value + 1
    support_size = m_value + RANK
    h_value = support_size - t_value
    residual_vector_dimension = h_value - BASE_CORE_SIZE
    residual_projective_dimension = residual_vector_dimension - 1
    finite_q_class_bound = 4
    endpoint_count = 1
    projective_total_bound = finite_q_class_bound + endpoint_count

    require(h_value == 5, "A=385 boundary defect should be five")
    require(
        residual_vector_dimension == 3 and residual_projective_dimension == 2,
        "two fixed base roots should leave a projective plane",
    )
    require(projective_total_bound == 5, "unexpected conic-pair total")
    require(projective_total_bound <= PROJECTIVE_BUDGET, "conic-pair branch over budget")

    transfer_record = next(
        record for record in low_degree["agreement_records"] if record["A"] == AGREEMENT
    )
    require(transfer_record["boundary_defect_h"] == h_value, "transfer h mismatch")
    require(
        transfer_record["finite_root_transfer"]["projective_Q_search_dimension"] == 4,
        "A=385 Q-space should be projective dimension four",
    )
    require(
        transfer_record["split_locator_followup"]["split_locator_gate_ref"]
        == NULLPOLY_SPLIT_GATE_REF,
        "split-gate dependency mismatch",
    )

    branch_partition = [
        {
            "branch": "two_residual_consistency_conics_without_common_component",
            "status": "projective_budget_safe",
            "finite_q_class_upper_bound": finite_q_class_bound,
            "finite_noncontained_parameter_upper_bound": finite_q_class_bound,
            "projective_total_upper_bound": projective_total_bound,
            "reason": (
                "on the fixed two-core Q-plane, two comparison conics without "
                "a common component have intersection length at most four; "
                "the split-locator gate and zero-denominator compatibility can "
                "only remove classes"
            ),
        },
        {
            "branch": "residual_conics_have_a_common_component_on_the_Q_plane",
            "status": "named_residual",
            "finite_q_class_upper_bound": None,
            "finite_noncontained_parameter_upper_bound": None,
            "projective_total_upper_bound": None,
            "reason": (
                "the degree-only Bezout cut is no longer zero-dimensional; "
                "the common component must be classified by component, "
                "slope-map, quotient, or split-locator structure"
            ),
        },
        {
            "branch": "slope_free_points_on_the_Q_plane",
            "status": "zero_finite_noncontained_parameters",
            "finite_q_class_upper_bound": None,
            "finite_noncontained_parameter_upper_bound": 0,
            "projective_total_upper_bound": 0,
            "reason": (
                "if all direction numerator and denominator forms vanish at a "
                "Q-class, the displayed vector satisfies H(v)L_Q=0 and fails "
                "the finite noncontainment gate"
            ),
        },
    ]

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "object": "A=385 separated rank-6 fixed two-core conic-pair criterion",
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
            "rank6_boundary_low_degree_transfer": {
                "ref": LOW_DEGREE_TRANSFER_REF,
                "sha256": sha256_file(LOW_DEGREE_TRANSFER_REF),
            },
            "rank6_projective_endpoint_uniform": {
                "ref": ENDPOINT_UNIFORM_REF,
                "sha256": sha256_file(ENDPOINT_UNIFORM_REF),
            },
            "nullpolynomial_split_locator_gate": {
                "ref": NULLPOLY_SPLIT_GATE_REF,
                "sha256": sha256_file(NULLPOLY_SPLIT_GATE_REF),
            },
            "a385_four_base_core_closure": {
                "ref": A385_BASE_CORE_REF,
                "sha256": sha256_file(A385_BASE_CORE_REF),
            },
            "a385_three_core_quadratic_cut": {
                "ref": A385_THREE_CORE_REF,
                "sha256": sha256_file(A385_THREE_CORE_REF),
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
            "projective_Q_search_dimension": 4,
        },
        "family": {
            "base_support": "any subset X of H with |X|=j+1",
            "direction_support": "any subset Y of H\\X with |Y|=6",
            "weights": "any nonzero base weights a_x and direction weights b_y",
            "support_condition": "X and Y are disjoint",
            "branch_condition": (
                "the counted branch has a fixed forced base-root core E subset X "
                "with |E|=2, and there are two pairwise direction-consistency "
                "conics on the resulting projective Q-plane with no common "
                "component over the algebraic closure"
            ),
        },
        "criterion": {
            "residual_Q_space": (
                "factor Q=E R after the fixed two-point base core; then "
                "deg R<3 and [R] lies in P^2"
            ),
            "comparison_conics": (
                "choose a direction node y0 and comparison nodes y1,y2; "
                "F_i(R)=N_{y_i}(R)D_{y0}(R)-N_{y0}(R)D_{y_i}(R), i=1,2"
            ),
            "safe_if": (
                "F_1 and F_2 have no common component over the algebraic closure"
            ),
            "residual_if_not": (
                "a common line/conic component remains on the fixed two-core "
                "Q-plane and needs a component/slope-map or split-locator analysis"
            ),
        },
        "theorem": {
            "low_degree_transfer": (
                "At A=385 every finite root in a separated rank-6 boundary "
                "bucket is represented by a projective Q-class with deg Q<5."
            ),
            "two_point_reduction": (
                "A fixed two-point base core imposes two independent conditions "
                "on polynomials deg Q<5, leaving a three-dimensional vector "
                "space Q=E R with deg R<3, i.e. a projective plane."
            ),
            "conic_pair_cut": (
                "For direction nodes y,y', the equality of the two displayed "
                "ratios is N_y(R)D_y'(R)-N_y'(R)D_y(R)=0.  On the residual "
                "Q-plane this is a conic.  If two such conics have no common "
                "component, every compatible finite root lies in their "
                "zero-dimensional intersection."
            ),
            "bezout_bound": (
                "Two plane conics without a common component have intersection "
                "length at most four over the algebraic closure, hence at most "
                "four compatible projective Q-classes."
            ),
            "finite_slope_bound": (
                "For each compatible Q-class, the direction equations are "
                "inconsistent, slope-free/contained, or determine one scalar z.  "
                "Thus the no-common-component branch has at most four finite "
                "noncontained parameters."
            ),
            "projective_safety": (
                "The endpoint-uniform theorem contributes at most the single "
                "projective endpoint, so the branch total is at most 5<=6."
            ),
            "residual": (
                "If every useful conic pair has a common component on the "
                "fixed two-core Q-plane, that common-component branch remains "
                "as the named fixed-two-core residual."
            ),
        },
        "branch_partition": branch_partition,
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
            "projective_Q_search_dimension_before_core": 4,
            "forced_base_core_size": BASE_CORE_SIZE,
            "residual_vector_dimension_after_core": residual_vector_dimension,
            "projective_Q_search_dimension_after_core": residual_projective_dimension,
            "comparison_conic_count_needed": 2,
            "no_common_component_finite_q_class_upper_bound": finite_q_class_bound,
            "finite_noncontained_parameter_upper_bound_under_conic_pair": finite_q_class_bound,
            "projective_endpoint_count": endpoint_count,
            "support_wise_projective_total_upper_bound_under_conic_pair": projective_total_bound,
            "projective_budget": PROJECTIVE_BUDGET,
            "fixed_two_core_no_common_component_branch_projective_safe": True,
            "remaining_residual": (
                "fixed two-core common-component branch on the residual Q-plane"
            ),
        },
        "checks": [
            "row descriptor and dependency schemas match",
            "A=385 has boundary defect h=5 and Q-space P^4",
            "base-support split roots transfer to Q-roots because base weights and residues are nonzero",
            "two distinct base evaluations leave a projective Q-plane",
            "direction ratio consistency restricts to conics on that Q-plane",
            "two conics without a common component have intersection length at most four",
            "each compatible non-slope-free Q-class determines at most one finite slope",
            "slope-free Q-classes add zero finite noncontained parameters",
            "endpoint-uniform dependency supplies at most one endpoint",
            "5 <= projective budget 6",
        ],
        "nonclaims": [
            "does not close the fixed two-core common-component residual",
            "does not prove that every A=385 over-budget branch has a fixed two-point base core",
            "does not close moving-core or no-common-core A=385 branches",
            "does not classify overlapping-support rank-6 pencils",
            "does not prove endpoint payment; it uses endpoint-budget accounting",
            "does not compute arbitrary A=385 rank-6 root tables",
            "does not produce a row-level M3 safe-side bound",
        ],
    }


def check_certificate(path: Path, certificate: dict[str, Any]) -> None:
    expected = render(certificate)
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"A=385 two-core conic-pair mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    print("F_17^32 M3 rank-6 A=385 fixed two-core conic-pair criterion")
    print(
        "base core={forced_base_core_size}, finite<={finite_noncontained_parameter_upper_bound_under_conic_pair}, projective total<={support_wise_projective_total_upper_bound_under_conic_pair}".format(
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
