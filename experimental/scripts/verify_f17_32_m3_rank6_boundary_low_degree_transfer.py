#!/usr/bin/env python3
"""Verify the low-degree transfer for separated rank-6 boundary roots."""

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


SCHEMA_VERSION = "f17-32-m3-rank6-boundary-low-degree-transfer-v1"
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
ENDPOINT_UNIFORM_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank6-projective-endpoint-uniform/"
    "f17_32_n512_k256_m3_rank6_projective_endpoint_uniform.json"
)
NULLPOLY_SPLIT_GATE_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-nullpolynomial-split-locator-gate/"
    "f17_32_n512_k256_m3_nullpolynomial_split_locator_gate.json"
)
BARYCENTRIC_EXACT_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank6-barycentric-exact-root-table/"
    "f17_32_n512_k256_m3_rank6_barycentric_exact_root_table.json"
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

    require(defect in {1, 3, 5}, f"A={agreement}: unexpected boundary defect")
    require(defect < RANK, f"A={agreement}: Q-space is not below direction size")
    require(t_value >= m_value, f"A={agreement}: base interpolation not full rank")
    require(support_size > j_value, f"A={agreement}: split interpolation root count too small")

    return {
        "A": agreement,
        "j": j_value,
        "t": t_value,
        "m": m_value,
        "direction_rank": RANK,
        "combined_support_size": support_size,
        "boundary_defect_h": defect,
        "auxiliary_Q_space_dimension": defect,
        "auxiliary_Q_degree_bound": f"deg Q < {defect}",
        "finite_root_transfer": {
            "input_data": (
                "disjoint X,Y with |X|=j+1, |Y|=6 and nonzero weights a_x,b_y"
            ),
            "barycentric_residues": "Omega_s=1/prod_{r in S,r!=s}(s-r), S=X union Y",
            "interpolation_step": (
                "for each Q with deg Q<h, let L_Q be the unique polynomial "
                "of degree <m satisfying a_x L_Q(x)=Omega_x Q(x) on X"
            ),
            "root_consistency": (
                "a finite root z exists for Q iff z b_y L_Q(y)=Omega_y Q(y) "
                "for every y in Y"
            ),
            "ratio_form": (
                "equivalently, all defined ratios Omega_y Q(y)/(b_y L_Q(y)) "
                "are equal and every zero denominator has zero numerator"
            ),
            "projective_Q_search_dimension": defect - 1,
        },
        "split_locator_followup": {
            "candidate_kernel_polynomial": "L_Q",
            "split_locator_test": "L_Q must normalize to a monic degree-j divisor of X^512-1",
            "split_locator_gate_ref": NULLPOLY_SPLIT_GATE_REF,
        },
    }


def build_certificate() -> dict[str, Any]:
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    endpoint_uniform = load_json(ENDPOINT_UNIFORM_REF)
    split_gate = load_json(NULLPOLY_SPLIT_GATE_REF)
    barycentric_exact = load_json(BARYCENTRIC_EXACT_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(
        endpoint_uniform["schema_version"]
        == "f17-32-m3-rank6-projective-endpoint-uniform-v1",
        "endpoint-uniform schema mismatch",
    )
    require(
        endpoint_uniform["summary"]["projective_endpoint_exact_contribution_per_agreement"] == 1,
        "endpoint-uniform contribution mismatch",
    )
    require(
        split_gate["schema_version"] == "f17-32-m3-nullpolynomial-split-locator-gate-v1",
        "split gate schema mismatch",
    )
    require(split_gate["summary"]["split_locator_gate_available"], "split gate unavailable")
    require(
        barycentric_exact["schema_version"]
        == "f17-32-m3-rank6-barycentric-exact-root-table-v1",
        "barycentric exact-root schema mismatch",
    )
    require(
        barycentric_exact["summary"]["barycentric_boundary_family_closed_after_split_filter"],
        "barycentric exact-root summary mismatch",
    )
    require(N % P != 0, "X^512-1 is not separable in this characteristic")
    require(FINITE_BUDGET == 6 and PROJECTIVE_BUDGET == 6, "unexpected budget")

    records = [agreement_record(agreement) for agreement in A_VALUES]
    defects = [record["boundary_defect_h"] for record in records]
    require(defects == [5, 3, 1], "boundary defects mismatch")
    require(defects == barycentric_exact["summary"]["boundary_defects"], "dependency defects mismatch")

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "object": "low-degree transfer for separated rank-6 boundary finite roots",
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
            "rank6_projective_endpoint_uniform": {
                "ref": ENDPOINT_UNIFORM_REF,
                "sha256": sha256_file(ENDPOINT_UNIFORM_REF),
            },
            "nullpolynomial_split_locator_gate": {
                "ref": NULLPOLY_SPLIT_GATE_REF,
                "sha256": sha256_file(NULLPOLY_SPLIT_GATE_REF),
            },
            "barycentric_exact_root_table": {
                "ref": BARYCENTRIC_EXACT_REF,
                "sha256": sha256_file(BARYCENTRIC_EXACT_REF),
            },
        },
        "window": {
            "agreements": A_VALUES,
            "agreement_count": len(A_VALUES),
        },
        "theorem": {
            "statement": (
                "For separated rank-6 supports at A=385,386,387, every finite "
                "ambient root is represented exactly by a nonzero auxiliary "
                "polynomial Q of degree <h=|X union Y|-t satisfying six direction "
                "node ratio-consistency equations."
            ),
            "dual_vandermonde_nullspace": (
                "For S=X union Y of size d and h=d-t, the nullspace of the first "
                "t Vandermonde rows is {Omega_s Q(s): deg Q<h}, with Omega_s the "
                "barycentric residue on S."
            ),
            "base_interpolation": (
                "Given Q, the X-equations a_x L(x)=Omega_x Q(x) determine a "
                "unique polynomial L_Q of degree <m=j+1 because |X|=m and all "
                "a_x are nonzero."
            ),
            "direction_consistency": (
                "The same Q gives a finite root exactly when the six equations "
                "z b_y L_Q(y)=Omega_y Q(y) are consistent for one scalar z."
            ),
            "search_reduction": (
                "Thus arbitrary separated-support boundary root tables reduce "
                "to projective Q-spaces of dimensions 4,2,0 at A=385,386,387, "
                "followed by the null-polynomial split-locator gate on L_Q."
            ),
            "barycentric_specialization": (
                "The barycentric exact-root packet is the special case a_s=b_s=Omega_s, "
                "where the consistency equations force the exact root table {1}."
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
            "boundary_defects_h": defects,
            "projective_Q_search_dimensions": [record["boundary_defect_h"] - 1 for record in records],
            "direction_equation_count": RANK,
            "split_locator_gate_required_after_transfer": True,
            "barycentric_exact_root_packet_is_special_case": True,
        },
        "checks": [
            "row descriptor and dependency schemas match",
            "boundary defects are 5,3,1",
            "base support size j+1 gives unique interpolation for L_Q",
            "defect h is smaller than the six direction nodes in all boundary agreements",
            "null-polynomial split-locator gate is available for the transferred L_Q",
            "barycentric exact-root packet has matching boundary defects",
        ],
        "nonclaims": [
            "does not solve the Q-consistency equations for arbitrary weights",
            "does not classify overlapping-support rank-6 pencils",
            "does not prove endpoint payment",
            "does not produce a row-level M3 safe-side bound",
            "does not replace exact root tables for non-barycentric boundary strata",
        ],
    }


def check_certificate(path: Path, certificate: dict[str, Any]) -> None:
    expected = render(certificate)
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"rank-6 boundary low-degree transfer mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    print("F_17^32 M3 rank-6 boundary low-degree transfer")
    print("A={}".format(",".join(str(value) for value in certificate["window"]["agreements"])))
    print(
        "defects={boundary_defects_h}, projective Q dims={projective_Q_search_dimensions}".format(
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
