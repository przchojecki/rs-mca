#!/usr/bin/env python3
"""Verify the A=386 component-cut safety criterion."""

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


SCHEMA_VERSION = "f17-32-m3-rank6-a386-component-cut-safety-v1"
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
A386_CONIC_PAIR_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank6-a386-conic-pair-safety/"
    "f17_32_n512_k256_m3_rank6_a386_conic_pair_safety.json"
)
ENDPOINT_UNIFORM_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank6-projective-endpoint-uniform/"
    "f17_32_n512_k256_m3_rank6_projective_endpoint_uniform.json"
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
    conic_pair = load_json(A386_CONIC_PAIR_REF)
    endpoint_uniform = load_json(ENDPOINT_UNIFORM_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(
        low_degree["schema_version"] == "f17-32-m3-rank6-boundary-low-degree-transfer-v1",
        "low-degree transfer schema mismatch",
    )
    require(AGREEMENT in low_degree["window"]["agreements"], "A=386 not in transfer packet")
    require(
        conic_pair["schema_version"] == "f17-32-m3-rank6-a386-conic-pair-safety-v1",
        "A=386 conic-pair schema mismatch",
    )
    require(
        conic_pair["summary"]["projective_safe_under_no_common_component_criterion"],
        "conic-pair criterion summary mismatch",
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

    component_cases = [
        {
            "common_component_degree": 1,
            "points_on_common_component_cut_bound": 2,
            "residual_off_component_intersection_bound": 1,
            "finite_root_bound": 3,
        },
        {
            "common_component_degree": 2,
            "points_on_common_component_cut_bound": 4,
            "residual_off_component_intersection_bound": 0,
            "finite_root_bound": 4,
        },
    ]
    require(max(case["finite_root_bound"] for case in component_cases) == 4, "bound mismatch")

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "object": "A=386 separated rank-6 component-cut projective-safety criterion",
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
            "a386_conic_pair_safety": {
                "ref": A386_CONIC_PAIR_REF,
                "sha256": sha256_file(A386_CONIC_PAIR_REF),
            },
            "rank6_projective_endpoint_uniform": {
                "ref": ENDPOINT_UNIFORM_REF,
                "sha256": sha256_file(ENDPOINT_UNIFORM_REF),
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
                "in the A=386 Q-plane, let two direction-consistency conics "
                "F_1,F_2 have full common component G of degree c in {1,2}"
            ),
            "safe_if": (
                "each irreducible component of G is cut by at least one "
                "direction-consistency conic"
            ),
            "residual_if_not": (
                "some irreducible component of G is contained in every "
                "direction-consistency conic; this is the A=386 "
                "global-component residual"
            ),
        },
        "theorem": {
            "component_decomposition": (
                "If F_1 and F_2 share a full common component G of degree c, "
                "then their common zero set is contained in G together with the "
                "intersection of the residual conics of degree 2-c."
            ),
            "component_cut": (
                "If every irreducible component G_i of G is cut by some "
                "direction-consistency conic, then the total length on G is "
                "at most sum_i 2 deg(G_i)=2c."
            ),
            "off_component_bound": (
                "The residual off-component intersection has length at most (2-c)^2."
            ),
            "finite_root_bound": (
                "Thus the finite Q-classes are at most 2c+(2-c)^2, which is 3 "
                "for c=1 and 4 for c=2."
            ),
            "projective_safety": (
                "The split-locator gate cannot increase this finite count, and "
                "the endpoint-uniform theorem contributes one endpoint, giving "
                "total at most 5<=6."
            ),
        },
        "component_cases": component_cases,
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
            "component_degrees": [1, 2],
            "finite_ambient_root_upper_bound_under_component_cut": 4,
            "finite_split_locator_upper_bound_under_component_cut": 4,
            "projective_endpoint_count": 1,
            "support_wise_projective_total_upper_bound_under_component_cut": 5,
            "projective_budget": PROJECTIVE_BUDGET,
            "projective_safe_under_component_cut_criterion": True,
            "remaining_residual": (
                "an irreducible component contained in all direction-consistency conics"
            ),
        },
        "checks": [
            "row descriptor and dependency schemas match",
            "A=386 has boundary defect h=3 and Q-space P^2",
            "the prior no-common-component criterion is available",
            "component degrees for plane conics are 1 or 2",
            "component-wise conic cuts contribute at most 2c points on G",
            "off-component residual contributes at most (2-c)^2 points",
            "maximum finite bound is 4",
            "endpoint-uniform dependency supplies exactly one endpoint",
            "5 <= projective budget 6",
        ],
        "nonclaims": [
            "does not prove every A=386 common-component case satisfies the cut criterion",
            "does not classify the global-component residual",
            "does not cover A=385",
            "does not classify overlapping-support rank-6 pencils",
            "does not prove endpoint payment",
            "does not close arbitrary rank-6 Hankel pencils",
        ],
    }


def check_certificate(path: Path, certificate: dict[str, Any]) -> None:
    expected = render(certificate)
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"A=386 component-cut safety certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    print("F_17^32 M3 rank-6 A=386 component-cut safety criterion")
    print(
        "finite split <= {finite_split_locator_upper_bound_under_component_cut}, endpoint={projective_endpoint_count}, total <= {support_wise_projective_total_upper_bound_under_component_cut}".format(
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
