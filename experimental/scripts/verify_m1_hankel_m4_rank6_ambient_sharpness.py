#!/usr/bin/env python3
"""Verify ambient sharpness of the M4 rank-6 projective boundary."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from math import comb
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experimental.scripts.emit_f17_32_hankel_row_descriptor import (  # noqa: E402
    Field,
    K,
    MODULUS,
    N,
    P,
)


SCHEMA_VERSION = "f17-32-m3-m4-rank6-ambient-sharpness-v1"
Q_LINE = 17**32
TARGET_BITS = 128
BUDGET = Q_LINE // 2**TARGET_BITS
A_MIN = 385
A_MAX = 426
ROOTS = [1, 2, 3, 4, 5, 6]
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
PROJECTIVE_BUDGET_SPLIT_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-m4-projective-budget-split/"
    "f17_32_n512_k256_m3_m4_projective_budget_split.json"
)


def load_json(ref: str | Path) -> dict[str, Any]:
    path = ref if isinstance(ref, Path) else ROOT / ref
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(ref: str) -> str:
    return sha256((ROOT / ref).read_bytes()).hexdigest()


def hash_value(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(payload).hexdigest()


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def monic_root_polynomial(roots: list[int], prime: int) -> list[int]:
    coeffs = [1]
    for root in roots:
        nxt = [0] * (len(coeffs) + 1)
        for index, coeff in enumerate(coeffs):
            nxt[index] = (nxt[index] - root * coeff) % prime
            nxt[index + 1] = (nxt[index + 1] + coeff) % prime
        coeffs = nxt
    return coeffs


def eval_poly(coeffs: list[int], value: int, prime: int) -> int:
    out = 0
    power = 1
    for coeff in coeffs:
        out = (out + coeff * power) % prime
        power = (power * value) % prime
    return out


def agreement_record(agreement: int) -> dict[str, Any]:
    j_value = N - agreement
    t_value = agreement - K
    minor_size = j_value + 1
    return {
        "A": agreement,
        "j": j_value,
        "t": t_value,
        "minor_size": minor_size,
        "maximal_row_set_count": comb(t_value, minor_size),
        "ambient_direction_rank": len(ROOTS),
        "canonical_finite_root_count": len(ROOTS),
        "projective_endpoint_contribution": 1,
        "projective_total": len(ROOTS) + 1,
        "finite_budget": BUDGET,
        "projective_budget": (Q_LINE + 1) // 2**TARGET_BITS,
    }


def build_certificate() -> dict[str, Any]:
    field = Field(P, MODULUS)
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    budget_split = load_json(PROJECTIVE_BUDGET_SPLIT_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field"] == "F_17^32", "descriptor field mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(descriptor["row"]["syndrome_length"] == N - K, "syndrome length mismatch")
    require(
        budget_split["schema_version"] == "f17-32-m3-m4-projective-budget-split-v1",
        "unexpected projective-budget schema",
    )
    require(budget_split["window"]["A_min"] == A_MIN, "budget split A_min mismatch")
    require(budget_split["window"]["A_max"] == A_MAX, "budget split A_max mismatch")

    domain_encodings = descriptor["domain"]["domain_encodings"]
    require(len(domain_encodings) == N, "domain length mismatch")
    require(len(set(domain_encodings)) == N, "descriptor domain is not distinct")
    decoded = [field.decode(value) for value in domain_encodings]
    require(
        [field.encode(value) for value in decoded] == domain_encodings,
        "domain decode/encode roundtrip failed",
    )
    max_t = A_MAX - K
    require(len(set(domain_encodings[:max_t])) == max_t, "first t row parameters not distinct")
    require(BUDGET == 6, "unexpected finite budget")
    require((Q_LINE + 1) // 2**TARGET_BITS == 6, "unexpected projective budget")
    require(ROOTS == sorted(set(ROOTS)), "roots must be distinct")
    require(all(0 < root < P for root in ROOTS), "roots must be nonzero base-field elements")

    root_poly = monic_root_polynomial(ROOTS, P)
    require(len(root_poly) - 1 == len(ROOTS), "root polynomial degree mismatch")
    for root in ROOTS:
        require(eval_poly(root_poly, root, P) == 0, "declared root does not vanish")

    records = [agreement_record(agreement) for agreement in range(A_MIN, A_MAX + 1)]
    total_row_sets = sum(record["maximal_row_set_count"] for record in records)
    require(total_row_sets == budget_split["window"]["all_row_set_total"], "row-set total mismatch")
    require(all(record["minor_size"] > len(ROOTS) for record in records), "minor size too small")

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "COUNTEREXAMPLE / AUDIT",
        "object": "ambient regular-pencil sharpness for the M4 rank-6 projective boundary",
        "row": {
            "code": "RS[F_17^32,H,256]",
            "n": N,
            "k": K,
            "field": "F_17^32",
            "domain_hash": descriptor["row"]["domain_hash"],
            "q_line": Q_LINE,
            "finite_budget": BUDGET,
            "projective_budget": (Q_LINE + 1) // 2**TARGET_BITS,
        },
        "source_artifacts": {
            "row_descriptor": {"ref": ROW_DESCRIPTOR_REF, "sha256": sha256_file(ROW_DESCRIPTOR_REF)},
            "projective_budget_split": {
                "ref": PROJECTIVE_BUDGET_SPLIT_REF,
                "sha256": sha256_file(PROJECTIVE_BUDGET_SPLIT_REF),
            },
        },
        "window": {
            "A_min": A_MIN,
            "A_max": A_MAX,
            "agreement_count": len(records),
            "all_row_set_total": total_row_sets,
        },
        "ambient_template": {
            "row_parameters": "alpha_0,...,alpha_{t-1}: first t descriptor-domain elements",
            "row_matrix_C": "C_{r,i}=alpha_r^i for 0<=i<m=j+1",
            "diagonal_pencil": "D(Z)=diag(Z-1,...,Z-6,1,...,1)",
            "ambient_pencil": "M(Z)=C D(Z)=A+ZB",
            "direction_matrix": "B=C diag(1,1,1,1,1,1,0,...,0)",
            "root_polynomial_low_to_high_mod_17": root_poly,
            "finite_roots": ROOTS,
        },
        "theorem": {
            "statement": (
                "For every M3 agreement 385<=A<=426, there is an ambient "
                "t x (j+1) regular pencil with direction rank 6, six finite "
                "canonical regular roots, and a nonempty projective-infinity "
                "ambient chart.  Thus the rank-6 endpoint-sensitive boundary "
                "cannot be closed using only direction rank, regular "
                "nonsingularity, and the one-point projective endpoint bound."
            ),
            "proof_skeleton": [
                "Choose distinct alpha_r from the pinned descriptor domain and set C_{r,i}=alpha_r^i.",
                "Every maximal row-set minor of C is a nonzero Vandermonde determinant.",
                "For D(Z)=diag(Z-1,...,Z-6,1,...,1), every maximal minor of M(Z)=C D(Z) equals det(C_R) times prod_{a=1}^6 (Z-a).",
                "Hence the v10 canonical gcd over all nonzero maximal minors is exactly prod_{a=1}^6 (Z-a), with six finite roots.",
                "The direction B has rank 6 because the first six columns of C have rank 6.",
                "Since m=j+1>=87, the vector e_7 lies in ker B but A e_7 is the nonzero seventh column of C; the projective-infinity ambient chart is nonempty.",
            ],
            "blocked_overstrong_claim": (
                "A universal projective-safe theorem for all rank-6 nonsingular "
                "regular pencils cannot follow from the current ambient "
                "rank/endpoint invariants alone."
            ),
            "remaining_viable_routes": [
                "exploit the Hankel moment structure of H(u)+ZH(v)",
                "compute exact finite root tables for rank-6 buckets",
                "prove endpoint empty/paid by quotient, tangent, or extension ledgers",
                "add split-locator constraints beyond the ambient linear chart",
            ],
        },
        "field_audit": {
            "first_row_parameter_count": max_t,
            "first_row_parameters_distinct": True,
            "domain_size": len(domain_encodings),
            "domain_hash": hash_value(domain_encodings),
            "decoded_roundtrip_hash": hash_value([field.encode(value) for value in decoded]),
        },
        "agreement_records": records,
        "summary": {
            "agreement_count": len(records),
            "ambient_direction_rank": len(ROOTS),
            "finite_root_count": len(ROOTS),
            "projective_endpoint_contribution": 1,
            "projective_total": len(ROOTS) + 1,
            "finite_budget": BUDGET,
            "projective_budget": (Q_LINE + 1) // 2**TARGET_BITS,
            "rank6_boundary_is_sharp_for_ambient_regular_pencils": True,
        },
        "checks": [
            "first 170 descriptor-domain elements are distinct",
            "all M3 minor sizes are at least 87, hence greater than 6",
            "Vandermonde row minors are nonzero for every maximal row set",
            "canonical finite gcd has six distinct base-field roots",
            "direction rank is exactly 6",
            "projective endpoint ambient chart is nonempty",
        ],
        "nonclaims": [
            "does not assert this ambient pencil is a Hankel moment pencil",
            "does not refute any Hankel-specific rank-6 theorem",
            "does not produce a support-wise MCA lower-bound row",
            "does not duplicate synthetic low-rank quotient-image packets",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"rank-6 ambient sharpness certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    window = certificate["window"]
    print("F_17^32 M3/M4 rank-6 ambient sharpness")
    print(
        "A={A_min}..{A_max}, agreements={agreement_count}, row sets={all_row_set_total}".format(
            **window
        )
    )
    print(
        "rank={ambient_direction_rank}, finite roots={finite_root_count}, "
        "projective total={projective_total}, budget={projective_budget}".format(**summary)
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
        check_certificate(args.check)
    print_summary(certificate)


if __name__ == "__main__":
    main()
