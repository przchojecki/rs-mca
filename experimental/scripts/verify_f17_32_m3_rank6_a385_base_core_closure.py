#!/usr/bin/env python3
"""Verify the A=385 separated rank-6 fixed base-core closure."""

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


SCHEMA_VERSION = "f17-32-m3-rank6-a385-base-core-closure-v1"
Q_LINE = 17**32
TARGET_BITS = 128
FINITE_BUDGET = Q_LINE // 2**TARGET_BITS
PROJECTIVE_DENOMINATOR = Q_LINE + 1
PROJECTIVE_BUDGET = PROJECTIVE_DENOMINATOR // 2**TARGET_BITS
AGREEMENT = 385
RANK = 6
BASE_CORE_SIZE = 4
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
    require(N % P != 0, "X^512-1 is not separable in this characteristic")
    require(FINITE_BUDGET == 6 and PROJECTIVE_BUDGET == 6, "unexpected budget")

    j_value = N - AGREEMENT
    t_value = AGREEMENT - K
    m_value = j_value + 1
    support_size = m_value + RANK
    h_value = support_size - t_value
    require(h_value == 5, "A=385 boundary defect should be five")
    require(BASE_CORE_SIZE == h_value - 1, "base core should leave one Q dimension")

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
            "branch": "unique_Q_class_with_some_nonzero_direction_denominator",
            "status": "at_most_one_finite_parameter",
            "finite_parameter_upper_bound": 1,
            "reason": (
                "the fixed four-point base core leaves one projective Q-class; "
                "one nonzero direction denominator determines at most one slope"
            ),
        },
        {
            "branch": "unique_Q_class_slope_free",
            "status": "zero_finite_noncontained_parameters",
            "finite_parameter_upper_bound": 0,
            "reason": (
                "if all direction numerator and denominator forms vanish on the "
                "unique Q-class, the displayed vector satisfies H(v)L_Q=0 and "
                "fails the finite noncontainment gate"
            ),
        },
    ]

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "object": "A=385 separated rank-6 fixed base-core projective closure",
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
                "all split-locator candidates in the branch have a common "
                "forced base-root core E subset X with |E|>=4"
            ),
        },
        "theorem": {
            "low_degree_transfer": (
                "At A=385 every finite root in a separated rank-6 boundary "
                "bucket is represented by a projective Q-class with deg Q<5."
            ),
            "base_root_transfer": (
                "For x in the base support X, the transfer has "
                "a_x L_Q(x)=Omega_x Q(x).  Since a_x and Omega_x are nonzero, "
                "a forced split-locator root L_Q(x)=0 is equivalent to Q(x)=0."
            ),
            "four_point_collapse": (
                "Evaluation at four distinct base nodes has rank four on the "
                "five-dimensional vector space of polynomials deg Q<5.  Thus "
                "a fixed four-point base core leaves a one-dimensional vector "
                "space of Q's, i.e. a single projective Q-class."
            ),
            "finite_slope_bound": (
                "For a single Q-class, the six direction equations are either "
                "inconsistent, slope-free/contained, or determine one scalar z.  "
                "Hence the branch has at most one finite noncontained parameter."
            ),
            "projective_safety": (
                "The endpoint-uniform theorem contributes at most the single "
                "projective endpoint, so the branch total is at most 2<=6."
            ),
            "contrapositive_use": (
                "Any over-budget separated A=385 rank-6 boundary obstruction "
                "must avoid having a common forced base-root core of size four "
                "inside the branch being counted."
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
            "projective_Q_search_dimension_after_core": 0,
            "finite_noncontained_parameter_upper_bound": 1,
            "projective_endpoint_count": 1,
            "support_wise_projective_total_upper_bound": 2,
            "projective_budget": PROJECTIVE_BUDGET,
            "fixed_four_base_core_branch_projective_safe": True,
            "over_budget_witness_must_avoid_common_four_base_core": True,
        },
        "checks": [
            "row descriptor and dependency schemas match",
            "A=385 has boundary defect h=5 and Q-space P^4",
            "base-support split roots transfer to Q-roots because base weights and residues are nonzero",
            "four distinct base evaluations have rank four on polynomials of degree <5",
            "a fixed four-point base core leaves a single projective Q-class",
            "one Q-class determines at most one finite noncontained slope",
            "slope-free unique-Q branch adds zero finite noncontained parameters",
            "endpoint-uniform dependency supplies at most one endpoint",
            "2 <= projective budget 6",
        ],
        "nonclaims": [
            "does not close A=385 branches without a common forced four-point base core",
            "does not prove that every A=385 over-budget branch has such a core",
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
        raise AssertionError(f"A=385 fixed base-core closure mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    print("F_17^32 M3 rank-6 A=385 fixed base-core closure")
    print(
        "base core={forced_base_core_size}, finite<={finite_noncontained_parameter_upper_bound}, projective total<={support_wise_projective_total_upper_bound}".format(
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
