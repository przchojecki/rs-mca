#!/usr/bin/env python3
"""Verify the exact root table for the boundary barycentric rank-6 family."""

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


SCHEMA_VERSION = "f17-32-m3-rank6-barycentric-exact-root-table-v1"
Q_LINE = 17**32
TARGET_BITS = 128
FINITE_BUDGET = Q_LINE // 2**TARGET_BITS
PROJECTIVE_DENOMINATOR = Q_LINE + 1
PROJECTIVE_BUDGET = PROJECTIVE_DENOMINATOR // 2**TARGET_BITS
RANK = 6
A_VALUES = [385, 386, 387]
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
BOUNDARY_OBSTRUCTION_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank6-boundary-barycentric-obstruction/"
    "f17_32_n512_k256_m3_rank6_boundary_barycentric_obstruction.json"
)
BARYCENTRIC_SPLIT_FILTER_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank6-barycentric-split-filter/"
    "f17_32_n512_k256_m3_rank6_barycentric_split_filter.json"
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


def agreement_record(agreement: int) -> dict[str, Any]:
    j_value = N - agreement
    t_value = agreement - K
    m_value = j_value + 1
    support_size = m_value + RANK
    defect = support_size - t_value

    require(defect in {1, 3, 5}, f"A={agreement}: unexpected defect")
    require(defect <= RANK - 1, f"A={agreement}: defect too large")
    require(RANK > defect, f"A={agreement}: direction nodes do not outnumber defect")
    require(m_value > defect, f"A={agreement}: base interpolation cannot force equality")
    require(support_size > j_value, f"A={agreement}: support interpolation too small")

    return {
        "A": agreement,
        "j": j_value,
        "t": t_value,
        "m": m_value,
        "base_support_size": m_value,
        "direction_support_size": RANK,
        "combined_support_size": support_size,
        "boundary_defect": defect,
        "ambient_finite_root_table": [1],
        "ambient_kernel_dimension_at_z_1": defect,
        "ambient_kernel_description_at_z_1": f"polynomials Q with deg Q < {defect}",
        "z_not_1_exclusion": {
            "base_interpolation_roots": m_value,
            "low_degree_bound": defect - 1,
            "direction_nodes": RANK,
            "argument": (
                "for z!=1, the low-degree kernel polynomial Q must vanish "
                "on all six direction nodes; since deg Q<defect<=5, Q=0"
            ),
        },
        "split_locator_filter": {
            "degree_j_split_locator_at_z_1": False,
            "finite_support_wise_split_locator_count": 0,
        },
        "projective_endpoint": {
            "endpoint": "[0:1]",
            "endpoint_present": True,
            "support_wise_projective_total_after_filter": 1,
            "projective_budget": PROJECTIVE_BUDGET,
        },
    }


def build_certificate() -> dict[str, Any]:
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    obstruction = load_json(BOUNDARY_OBSTRUCTION_REF)
    split_filter = load_json(BARYCENTRIC_SPLIT_FILTER_REF)
    endpoint_uniform = load_json(ENDPOINT_UNIFORM_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(
        obstruction["schema_version"]
        == "f17-32-m3-rank6-boundary-barycentric-obstruction-v1",
        "boundary obstruction schema mismatch",
    )
    require(obstruction["window"]["agreements"] == A_VALUES, "obstruction agreement mismatch")
    require(
        split_filter["schema_version"] == "f17-32-m3-rank6-barycentric-split-filter-v1",
        "split filter schema mismatch",
    )
    require(
        split_filter["summary"]["barycentric_root_filtered_by_split_locator_gate"],
        "split filter summary mismatch",
    )
    require(
        endpoint_uniform["schema_version"]
        == "f17-32-m3-rank6-projective-endpoint-uniform-v1",
        "endpoint-uniform schema mismatch",
    )
    require(
        endpoint_uniform["summary"]["projective_endpoint_exact_contribution_per_agreement"] == 1,
        "endpoint-uniform contribution mismatch",
    )
    require(N % P != 0, "X^512-1 is not separable in this characteristic")
    require(FINITE_BUDGET == 6 and PROJECTIVE_BUDGET == 6, "unexpected budget")

    records = [agreement_record(agreement) for agreement in A_VALUES]
    defects = [record["boundary_defect"] for record in records]
    require(defects == obstruction["summary"]["boundary_deficits"], "defect mismatch")
    require(defects == split_filter["summary"]["boundary_defects"], "split-filter defect mismatch")

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "object": "exact finite root table for the boundary barycentric rank-6 family",
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
            "boundary_barycentric_obstruction": {
                "ref": BOUNDARY_OBSTRUCTION_REF,
                "sha256": sha256_file(BOUNDARY_OBSTRUCTION_REF),
            },
            "barycentric_split_filter": {
                "ref": BARYCENTRIC_SPLIT_FILTER_REF,
                "sha256": sha256_file(BARYCENTRIC_SPLIT_FILTER_REF),
            },
            "rank6_projective_endpoint_uniform": {
                "ref": ENDPOINT_UNIFORM_REF,
                "sha256": sha256_file(ENDPOINT_UNIFORM_REF),
            },
        },
        "window": {
            "agreements": A_VALUES,
            "agreement_count": len(A_VALUES),
        },
        "family": {
            "base_support": "any subset X of H with |X|=j+1",
            "direction_support": "any subset Y of H\\X with |Y|=6",
            "combined_support": "S=X union Y",
            "weights": (
                "barycentric residues omega_s=1/prod_{r in S,r!=s}(s-r); "
                "set a_x=omega_x and b_y=omega_y"
            ),
        },
        "theorem": {
            "statement": (
                "For the boundary barycentric rank-6 family at A=385,386,387, "
                "the ambient finite regular root table is exactly {1}.  That "
                "root is filtered by the split-locator gate, so the finite "
                "support-wise split-locator contribution is 0 and the only "
                "support-wise projective contribution in this family is [0:1]."
            ),
            "kernel_equation": (
                "At finite slope z, a kernel polynomial L of degree <m gives "
                "weighted values omega_s L(s) on X and z omega_y L(y) on Y.  "
                "The dual Vandermonde nullspace is omega_s Q(s) with deg Q<|S|-t."
            ),
            "base_interpolation": (
                "On X, L(x)=Q(x).  Since |X|=m and deg(L-Q)<m, this forces L=Q."
            ),
            "direction_exclusion": (
                "On Y, z L(y)=Q(y)=L(y).  If z!=1 then L vanishes on six "
                "direction nodes; but L=Q has degree <|S|-t<=5, hence L=0."
            ),
            "root_existence": (
                "At z=1, every nonzero Q with deg Q<|S|-t gives a kernel "
                "polynomial, so z=1 is present with kernel dimension |S|-t."
            ),
            "split_filter": (
                "The split-filter dependency proves this z=1 kernel contains "
                "no monic degree-j divisor of X^512-1."
            ),
            "endpoint": (
                "The endpoint-uniform dependency gives the single projective "
                "endpoint [0:1]."
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
        "agreement_records": records,
        "summary": {
            "agreement_count": len(records),
            "ambient_finite_root_table": [1],
            "ambient_finite_root_count": 1,
            "boundary_defects": [record["boundary_defect"] for record in records],
            "finite_support_wise_split_locator_count": 0,
            "projective_endpoint_count": 1,
            "support_wise_projective_total_after_filter": 1,
            "finite_budget": FINITE_BUDGET,
            "projective_budget": PROJECTIVE_BUDGET,
            "barycentric_boundary_family_closed_after_split_filter": True,
        },
        "checks": [
            "row descriptor and dependency schemas match",
            "boundary obstruction and split-filter packets have the same defects",
            "direction support size six is larger than every boundary defect",
            "base support size m forces L=Q by interpolation",
            "z!=1 would force a low-degree polynomial to vanish on six direction nodes",
            "z=1 exists with kernel dimension |S|-t",
            "split-filter dependency removes z=1 from support-wise finite counting",
            "endpoint-uniform dependency supplies exactly the projective endpoint",
        ],
        "nonclaims": [
            "does not classify arbitrary boundary rank-6 pencils",
            "does not classify non-barycentric boundary weights",
            "does not close overlapping-support strata",
            "does not prove endpoint payment",
            "does not alter the ambient root-table obstruction recorded earlier",
        ],
    }


def check_certificate(path: Path, certificate: dict[str, Any]) -> None:
    expected = render(certificate)
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"rank-6 barycentric exact-root certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    print("F_17^32 M3 rank-6 barycentric exact root table")
    print("A={}".format(",".join(str(value) for value in certificate["window"]["agreements"])))
    print(
        "ambient roots={ambient_finite_root_table}, finite split count={finite_support_wise_split_locator_count}, projective total={support_wise_projective_total_after_filter}".format(
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
