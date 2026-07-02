#!/usr/bin/env python3
"""Verify the A=385 rank-6 fixed two-core component-cut criterion."""

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


SCHEMA_VERSION = "f17-32-m3-rank6-a385-two-core-component-cut-safety-v1"
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
A385_TWO_CORE_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank6-a385-two-core-conic-pair-safety/"
    "f17_32_n512_k256_m3_rank6_a385_two_core_conic_pair_safety.json"
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
    two_core = load_json(A385_TWO_CORE_REF)

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
        two_core["schema_version"]
        == "f17-32-m3-rank6-a385-two-core-conic-pair-safety-v1",
        "A385 two-core conic-pair schema mismatch",
    )
    require(
        two_core["summary"]["fixed_two_core_no_common_component_branch_projective_safe"],
        "A385 two-core conic-pair criterion unavailable",
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
    require(h_value == 5, "A=385 boundary defect should be five")
    require(
        residual_vector_dimension == 3 and residual_projective_dimension == 2,
        "two fixed base roots should leave a projective plane",
    )

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

    component_cases = [
        {
            "common_component_degree": 1,
            "points_on_common_component_cut_bound": 2,
            "residual_off_component_intersection_bound": 1,
            "finite_q_class_bound": 3,
        },
        {
            "common_component_degree": 2,
            "points_on_common_component_cut_bound": 4,
            "residual_off_component_intersection_bound": 0,
            "finite_q_class_bound": 4,
        },
    ]
    max_finite_bound = max(case["finite_q_class_bound"] for case in component_cases)
    endpoint_count = 1
    projective_total_bound = max_finite_bound + endpoint_count
    require(max_finite_bound == 4, "component-cut finite bound mismatch")
    require(projective_total_bound == 5, "component-cut projective bound mismatch")
    require(projective_total_bound <= PROJECTIVE_BUDGET, "component-cut branch over budget")

    branch_partition = [
        {
            "branch": "common_component_cut_by_some_direction_conic",
            "status": "projective_budget_safe",
            "finite_q_class_upper_bound": max_finite_bound,
            "finite_noncontained_parameter_upper_bound": max_finite_bound,
            "projective_total_upper_bound": projective_total_bound,
            "reason": (
                "if each irreducible component of the common component is cut "
                "by some direction-consistency conic, Bezout bounds the "
                "component points by 2c and the off-component residual by "
                "(2-c)^2"
            ),
        },
        {
            "branch": "global_component_contained_in_all_direction_conics",
            "status": "named_residual",
            "finite_q_class_upper_bound": None,
            "finite_noncontained_parameter_upper_bound": None,
            "projective_total_upper_bound": None,
            "reason": (
                "some irreducible component of the fixed two-core Q-plane is "
                "contained in every direction-consistency conic; degree-only "
                "component cuts no longer reduce to finitely many Q-classes"
            ),
        },
    ]

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "object": "A=385 separated rank-6 fixed two-core component-cut criterion",
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
            "a385_two_core_conic_pair_safety": {
                "ref": A385_TWO_CORE_REF,
                "sha256": sha256_file(A385_TWO_CORE_REF),
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
                "with |E|=2; two residual direction-consistency conics have a "
                "full common component G on the projective Q-plane; each "
                "irreducible component of G is cut by some direction-consistency conic"
            ),
        },
        "criterion": {
            "residual_Q_space": (
                "after the fixed two-point base core, Q=E R with deg R<3 and "
                "[R] lies in P^2"
            ),
            "common_component": (
                "two residual direction-consistency conics share a common "
                "component G of total degree c in {1,2}, taken to be their "
                "full common component"
            ),
            "safe_if": (
                "each irreducible component G_i of G is not contained in at "
                "least one direction-consistency conic"
            ),
            "residual_if_not": (
                "some irreducible component of G is contained in all "
                "direction-consistency conics"
            ),
        },
        "theorem": {
            "component_decomposition": (
                "If two residual conics have full common component G of degree "
                "c, their common zero set is contained in G together with the "
                "intersection of the residual coprime conics of degree 2-c."
            ),
            "component_cut": (
                "If every irreducible component G_i of G is cut by some "
                "direction-consistency conic, then the total number of "
                "compatible Q-classes on G is at most sum_i 2 deg(G_i)=2c."
            ),
            "off_component_bound": (
                "The residual off-component intersection has length at most "
                "(2-c)^2."
            ),
            "finite_slope_bound": (
                "The finite Q-class count is at most 2c+(2-c)^2, namely 3 for "
                "c=1 and 4 for c=2.  Each compatible non-slope-free Q-class "
                "determines at most one finite noncontained parameter."
            ),
            "projective_safety": (
                "The split-locator gate cannot increase the finite ambient "
                "count, and the endpoint-uniform theorem contributes at most "
                "one endpoint, so the branch total is at most 5<=6."
            ),
            "residual": (
                "The remaining fixed two-core common-component branch has an "
                "irreducible component contained in all direction-consistency "
                "conics."
            ),
        },
        "component_cases": component_cases,
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
            "component_degrees": [1, 2],
            "finite_q_class_upper_bound_under_component_cut": max_finite_bound,
            "finite_noncontained_parameter_upper_bound_under_component_cut": max_finite_bound,
            "projective_endpoint_count": endpoint_count,
            "support_wise_projective_total_upper_bound_under_component_cut": projective_total_bound,
            "projective_budget": PROJECTIVE_BUDGET,
            "fixed_two_core_component_cut_branch_projective_safe": True,
            "remaining_residual": (
                "fixed two-core global-component branch contained in all "
                "direction-consistency conics"
            ),
        },
        "checks": [
            "row descriptor and dependency schemas match",
            "A=385 has boundary defect h=5 and Q-space P^4 before base-core reduction",
            "two fixed base roots leave a projective Q-plane",
            "the prior no-common-component conic-pair criterion is available",
            "component degrees for plane conics are 1 or 2",
            "component-wise conic cuts contribute at most 2c points on G",
            "off-component residual contributes at most (2-c)^2 points",
            "maximum finite bound is 4",
            "endpoint-uniform dependency supplies at most one endpoint",
            "5 <= projective budget 6",
        ],
        "nonclaims": [
            "does not prove every fixed two-core common-component branch satisfies the cut criterion",
            "does not close the fixed two-core global-component residual",
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
        raise AssertionError(f"A=385 two-core component-cut mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    print("F_17^32 M3 rank-6 A=385 fixed two-core component cut")
    print(
        "finite<={finite_noncontained_parameter_upper_bound_under_component_cut}, projective total<={support_wise_projective_total_upper_bound_under_component_cut}".format(
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
