#!/usr/bin/env python3
"""Verify the regular-minor common-gcd gate on a finite toy packet.

For a regular overdetermined Hankel bucket, a bad regular slope makes the
Hankel matrix have rank at most j.  Hence every maximal (j+1)x(j+1) minor
vanishes at that slope.  Therefore the bad regular slopes are contained in the
finite-field roots of the gcd of any audited family of maximal-minor
determinants.

This verifier records that theorem and replays it on the F_17, n=16, k=8 toy
input using all contiguous maximal row-set minors.
"""

from __future__ import annotations

import argparse
import json
from hashlib import sha256
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experimental.scripts.extract_regular_hankel_minors import (  # noqa: E402
    DEFAULT_MAX_BAD_SLOPE_SUBSETS,
    determinant_polynomial_by_interpolation,
    finite_bad_slopes_for_exact_agreement,
    matrix_at_slope,
    n_choose_k,
    poly_degree,
    poly_eval,
    poly_scale,
    trim,
)


SCHEMA_VERSION = "regular-minor-gcd-gate-v1"
TOY_INPUT_REF = "experimental/data/hankel-regular-minor-inputs/f17_n16_k8_a13_toy.json"
OUTPUT_PATH = ROOT / (
    "experimental/data/certificates/regular-minor-gcd-gate/"
    "f17_n16_k8_regular_minor_gcd_gate_certificate.json"
)


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def load_json(ref: str) -> dict[str, Any]:
    return json.loads((ROOT / ref).read_text(encoding="utf-8"))


def sha256_file(ref: str) -> str:
    return sha256((ROOT / ref).read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def poly_divmod(left: list[int], right: list[int], prime: int) -> tuple[list[int], list[int]]:
    numerator = trim(left, prime)
    denominator = trim(right, prime)
    if denominator == [0]:
        raise ZeroDivisionError("polynomial division by zero")
    quotient = [0] * max(1, len(numerator) - len(denominator) + 1)
    while len(numerator) >= len(denominator) and numerator != [0]:
        coeff = numerator[-1] * pow(denominator[-1], -1, prime) % prime
        shift = len(numerator) - len(denominator)
        quotient[shift] = coeff
        subtractor = [0] * shift + [(coeff * term) % prime for term in denominator]
        numerator = trim(
            [
                (
                    (numerator[index] if index < len(numerator) else 0)
                    - (subtractor[index] if index < len(subtractor) else 0)
                )
                % prime
                for index in range(max(len(numerator), len(subtractor)))
            ],
            prime,
        )
    return trim(quotient, prime), numerator


def poly_gcd(left: list[int], right: list[int], prime: int) -> list[int]:
    a = trim(left, prime)
    b = trim(right, prime)
    if a == [0]:
        return make_monic(b, prime)
    if b == [0]:
        return make_monic(a, prime)
    while b != [0]:
        _, remainder = poly_divmod(a, b, prime)
        a, b = b, remainder
    return make_monic(a, prime)


def make_monic(poly: list[int], prime: int) -> list[int]:
    poly = trim(poly, prime)
    if poly == [0]:
        return [0]
    return poly_scale(poly, pow(poly[-1], -1, prime), prime)


def gcd_many(polynomials: list[list[int]], prime: int) -> list[int]:
    require(polynomials, "need at least one polynomial")
    gcd = polynomials[0]
    for polynomial in polynomials[1:]:
        gcd = poly_gcd(gcd, polynomial, prime)
    return make_monic(gcd, prime)


def roots(poly: list[int], prime: int) -> list[int]:
    if trim(poly, prime) == [0]:
        return list(range(prime))
    return [value for value in range(prime) if poly_eval(poly, value, prime) == 0]


def rank_mod(matrix: list[list[int]], prime: int) -> int:
    work = [[entry % prime for entry in row] for row in matrix]
    if not work:
        return 0
    rows = len(work)
    cols = len(work[0])
    rank = 0
    for col in range(cols):
        pivot = next((row for row in range(rank, rows) if work[row][col] % prime), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][col] % prime, -1, prime)
        work[rank] = [(entry * inverse) % prime for entry in work[rank]]
        for row in range(rows):
            if row == rank or work[row][col] % prime == 0:
                continue
            factor = work[row][col] % prime
            work[row] = [
                (work[row][entry_col] - factor * work[rank][entry_col]) % prime
                for entry_col in range(cols)
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def contiguous_row_sets(t: int, size: int) -> list[list[int]]:
    return [list(range(start, start + size)) for start in range(t - size + 1)]


def agreement_record(spec: dict[str, Any], agreement: int) -> dict[str, Any]:
    prime = 17
    n = int(spec["row"]["n"])
    k = int(spec["row"]["k"])
    j = n - agreement
    t = agreement - k
    size = j + 1
    u = [int(value) % prime for value in spec["line_syndrome"]["u"]]
    v = [int(value) % prime for value in spec["line_syndrome"]["v"]]
    require(t >= size, f"A={agreement}: not a regular bucket")
    row_sets = contiguous_row_sets(t, size)
    minor_records = []
    polynomials = []
    for row_set in row_sets:
        polynomial = determinant_polynomial_by_interpolation(u, v, row_set, size, prime)
        polynomial = trim(polynomial, prime)
        polynomials.append(polynomial)
        minor_records.append(
            {
                "row_set": row_set,
                "degree": poly_degree(polynomial, prime) if polynomial != [0] else -1,
                "polynomial": polynomial,
                "roots": roots(polynomial, prime),
            }
        )
    gcd = gcd_many(polynomials, prime)
    gcd_roots = roots(gcd, prime)
    rank_defect_slopes = []
    for slope in range(prime):
        matrix = matrix_at_slope(u, v, list(range(t)), size, slope, prime)
        if rank_mod(matrix, prime) < size:
            rank_defect_slopes.append(slope)
    split_bad_slopes: list[int] = []
    domain = [int(value) % prime for value in spec["row"]["domain"]]
    subset_count = n_choose_k(len(domain), j)
    if subset_count <= DEFAULT_MAX_BAD_SLOPE_SUBSETS:
        split_bad_slopes = finite_bad_slopes_for_exact_agreement(
            u, v, domain, n, k, agreement, prime
        )
    require(
        set(rank_defect_slopes).issubset(gcd_roots),
        f"A={agreement}: rank defects not contained in gcd roots",
    )
    require(
        set(split_bad_slopes).issubset(gcd_roots),
        f"A={agreement}: split bad slopes not contained in gcd roots",
    )
    single_minor_roots = minor_records[0]["roots"]
    return {
        "A": agreement,
        "j": j,
        "t": t,
        "minor_size": size,
        "audited_row_set_family": "all contiguous maximal row sets",
        "audited_row_sets": len(row_sets),
        "minor_records": minor_records,
        "single_prefix_roots": single_minor_roots,
        "single_prefix_root_count": len(single_minor_roots),
        "common_gcd_polynomial": gcd,
        "common_gcd_degree": poly_degree(gcd, prime) if gcd != [0] else -1,
        "common_gcd_roots": gcd_roots,
        "common_gcd_root_count": len(gcd_roots),
        "rank_defect_slopes": rank_defect_slopes,
        "split_bad_slopes": split_bad_slopes,
        "containment_checks": {
            "rank_defects_subset_common_gcd_roots": True,
            "split_bad_slopes_subset_common_gcd_roots": True,
        },
        "sharpening_over_prefix_root_count": len(single_minor_roots) - len(gcd_roots),
    }


def build_certificate() -> dict[str, Any]:
    spec = load_json(TOY_INPUT_REF)
    records = [agreement_record(spec, int(agreement)) for agreement in spec["exact_agreements"]]
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "source_input": {
            "ref": TOY_INPUT_REF,
            "sha256": sha256_file(TOY_INPUT_REF),
        },
        "theorem": {
            "statement": (
                "In a regular overdetermined bucket, any slope at which the "
                "Hankel matrix has rank at most j is a root of every maximal "
                "minor determinant, hence of the gcd of any audited family of "
                "maximal-minor determinant polynomials."
            ),
            "proof": (
                "Rank at most j means all (j+1)x(j+1) minors vanish.  The "
                "audited row-set determinants are among those minors, so their "
                "univariate determinant polynomials all vanish at the slope.  "
                "A common finite-field root of the audited polynomials is a "
                "root of their monic gcd."
            ),
            "non_equivalence_warning": (
                "A gcd root for a proper audited family can still be a false "
                "positive unless all maximal minors or an equivalent rank "
                "criterion are audited."
            ),
        },
        "toy_replay": {
            "row": spec["row"],
            "field": "F_17",
            "agreements": records,
        },
        "summary": {
            "agreements": len(records),
            "rank_defect_slopes_by_A": {
                str(record["A"]): record["rank_defect_slopes"] for record in records
            },
            "common_gcd_roots_by_A": {
                str(record["A"]): record["common_gcd_roots"] for record in records
            },
            "prefix_roots_by_A": {
                str(record["A"]): record["single_prefix_roots"] for record in records
            },
        },
        "nonclaims": [
            "does not prove a worst-case M1/M3 bound",
            "does not classify F_17^32 regular-window pencils",
            "does not make gcd roots equivalent to bad slopes for a proper minor family",
            "does not replace affine/projective pivot charts for singular buckets",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"regular-minor gcd-gate certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    print("regular-minor common-gcd gate")
    for record in certificate["toy_replay"]["agreements"]:
        print(
            "A={A}: prefix_roots={prefix} gcd_roots={gcd} rank_defects={rank}".format(
                A=record["A"],
                prefix=record["single_prefix_roots"],
                gcd=record["common_gcd_roots"],
                rank=record["rank_defect_slopes"],
            )
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path, help="write deterministic certificate JSON")
    parser.add_argument("--check", type=Path, help="check deterministic certificate JSON")
    parser.add_argument("--json", action="store_true", help="print certificate JSON")
    args = parser.parse_args()

    certificate = build_certificate()
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(certificate), encoding="utf-8")
    if args.check:
        check_certificate(args.check)
    if args.json:
        print(render(certificate), end="")
        return
    print_summary(certificate)


if __name__ == "__main__":
    main()
