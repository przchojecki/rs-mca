#!/usr/bin/env python3
"""Verify the A=386 separated rank-6 conic-pair safety criterion."""

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


SCHEMA_VERSION = "f17-32-m3-rank6-a386-conic-pair-safety-v1"
Q_LINE = 17**32
TARGET_BITS = 128
FINITE_BUDGET = Q_LINE // 2**TARGET_BITS
PROJECTIVE_DENOMINATOR = Q_LINE + 1
PROJECTIVE_BUDGET = PROJECTIVE_DENOMINATOR // 2**TARGET_BITS
AGREEMENT = 386
RANK = 6
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
    require(AGREEMENT in low_degree["window"]["agreements"], "A=386 not in transfer packet")
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
    require(h_value == 3, "A=386 boundary defect should be three")

    transfer_record = next(
        record for record in low_degree["agreement_records"] if record["A"] == AGREEMENT
    )
    require(transfer_record["boundary_defect_h"] == h_value, "transfer h mismatch")
    require(
        transfer_record["finite_root_transfer"]["projective_Q_search_dimension"] == 2,
        "A=386 Q-space should be projective dimension two",
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "object": "A=386 separated rank-6 conic-pair projective-safety criterion",
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
        },
        "criterion": {
            "setup": (
                "use the low-degree transfer with Q in P^2; choose a base "
                "direction node y0 and two comparison nodes y1,y2"
            ),
            "comparison_conics": (
                "F_i(Q)=Omega_{y_i} Q(y_i) b_{y0} L_Q(y0) - "
                "Omega_{y0} Q(y0) b_{y_i} L_Q(y_i), for i=1,2"
            ),
            "safe_if": (
                "the two conics F_1,F_2 have no common component over the "
                "algebraic closure"
            ),
            "residual_if_not": (
                "a common line/conic component is present; this is the named "
                "A=386 conic-component residual"
            ),
        },
        "theorem": {
            "finite_root_bound": (
                "Every finite root gives a Q-class satisfying all six direction "
                "consistency equations, hence in particular F_1=F_2=0."
            ),
            "bezout_bound": (
                "In P^2, two conics without a common component have intersection "
                "length at most 4 by Bezout, so there are at most four Q-classes "
                "and therefore at most four finite ambient slopes."
            ),
            "split_locator_bound": (
                "The split-locator gate can only remove finite ambient roots, so "
                "the finite support-wise split-locator count is also at most four."
            ),
            "endpoint": (
                "The endpoint-uniform theorem gives one projective endpoint [0:1]."
            ),
            "projective_safety": (
                "Under the conic-pair no-common-component criterion, the support-wise "
                "projective total is at most 4+1=5<=6."
            ),
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
            "boundary_defect_h": h_value,
            "projective_Q_search_dimension": 2,
            "comparison_conic_count_needed": 2,
            "finite_ambient_root_upper_bound_under_criterion": 4,
            "finite_split_locator_upper_bound_under_criterion": 4,
            "projective_endpoint_count": 1,
            "support_wise_projective_total_upper_bound_under_criterion": 5,
            "projective_budget": PROJECTIVE_BUDGET,
            "projective_safe_under_no_common_component_criterion": True,
        },
        "checks": [
            "row descriptor and dependency schemas match",
            "A=386 is included in the boundary low-degree transfer packet",
            "A=386 has boundary defect h=3",
            "the projective Q-search space has dimension two",
            "direction consistency comparisons are conics in P^2",
            "two conics without common component have at most four common Q-classes",
            "split-locator gate cannot increase finite ambient root count",
            "endpoint-uniform dependency supplies exactly one endpoint",
            "5 <= projective budget 6",
        ],
        "nonclaims": [
            "does not prove the no-common-component criterion for all A=386 weights",
            "does not cover A=385",
            "does not classify overlapping-support rank-6 pencils",
            "does not decide whether finite roots exist for a given weight set",
            "does not prove endpoint payment",
            "does not close arbitrary rank-6 Hankel pencils",
        ],
    }


def check_certificate(path: Path, certificate: dict[str, Any]) -> None:
    expected = render(certificate)
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"A=386 conic-pair safety certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    print("F_17^32 M3 rank-6 A=386 conic-pair safety criterion")
    print(
        "finite split <= {finite_split_locator_upper_bound_under_criterion}, endpoint={projective_endpoint_count}, total <= {support_wise_projective_total_upper_bound_under_criterion}".format(
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
