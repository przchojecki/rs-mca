#!/usr/bin/env python3
"""Replay the dihedral/Chebyshev quotient stratum packet."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "m1" / "dihedral_quotient_stratum.md"
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "dihedral-quotient-stratum"
    / "dihedral_quotient_stratum.json"
)

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "dihedral_quotient_stratum",
    "basis": "P_m = X^m F[X + X^{-1}]_{<=m}",
    "closed_count": "sum_{h<=m} binom((n-2)/2, h)",
    "taxonomy": "X^e g(X^M + X^{-M})",
    "non_claim": "does not prove the broader many-sparse classification theorem",
}


def mod_rank(rows: list[list[int]], p: int) -> int:
    matrix = [row[:] for row in rows if any(x % p for x in row)]
    if not matrix:
        return 0
    height = len(matrix)
    width = len(matrix[0])
    rank = 0
    for col in range(width):
        pivot = None
        for row in range(rank, height):
            if matrix[row][col] % p:
                pivot = row
                break
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inv = pow(matrix[rank][col] % p, -1, p)
        matrix[rank] = [(value * inv) % p for value in matrix[rank]]
        for row in range(height):
            if row == rank:
                continue
            factor = matrix[row][col] % p
            if factor:
                matrix[row] = [
                    (value - factor * pivot_value) % p
                    for value, pivot_value in zip(matrix[row], matrix[rank])
                ]
        rank += 1
    return rank


def chebyshev_basis_vectors(m: int, p: int) -> list[list[int]]:
    width = 2 * m + 1
    basis: list[list[int]] = []
    for i in range(m + 1):
        row = [0] * width
        for r in range(i + 1):
            exponent = m + i - 2 * r
            row[exponent] = (row[exponent] + math.comb(i, r)) % p
        basis.append(row)
    return basis


def poly_eval(coeffs: list[int], x: int, p: int) -> int:
    total = 0
    power = 1
    for coeff in coeffs:
        total = (total + coeff * power) % p
        power = (power * x) % p
    return total


def primitive_root_mod_prime(p: int) -> int:
    factors = []
    n = p - 1
    d = 2
    while d * d <= n:
        if n % d == 0:
            factors.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        factors.append(n)
    for g in range(2, p):
        if all(pow(g, (p - 1) // factor, p) != 1 for factor in factors):
            return g
    raise AssertionError("no primitive root found")


def toy_check() -> dict[str, object]:
    p = 17
    n = 16
    m = 3
    basis = chebyshev_basis_vectors(m, p)
    basis_rank = mod_rank(basis, p)

    support_union = sorted({idx for row in basis for idx, coeff in enumerate(row) if coeff})
    exponent_differences = sorted(
        {abs(a - b) for a in support_union for b in support_union if a != b}
    )
    has_adjacent_exponents = 1 in exponent_differences

    g = primitive_root_mod_prime(p)
    domain = [pow(g, i, p) for i in range(n)]
    inverse_pairs = []
    seen = set()
    for a in domain:
        inv = pow(a, -1, p)
        if a in {1, p - 1} or a in seen:
            continue
        inverse_pairs.append((a, inv))
        seen.add(a)
        seen.add(inv)

    trace_checks = []
    for a, inv in inverse_pairs:
        ok = all(poly_eval(row, a, p) == pow(a, 2 * m, p) * poly_eval(row, inv, p) % p for row in basis)
        trace_checks.append({"a": a, "a_inverse": inv, "trace_dependence": ok})

    y_values = {(a + inv) % p for a, inv in inverse_pairs}
    closed_set_lower_bound = sum(math.comb((n - 2) // 2, h) for h in range(m + 1))

    return {
        "field": "F_17",
        "domain_order": n,
        "m": m,
        "basis_rank": basis_rank,
        "expected_dimension": m + 1,
        "dimension_check": basis_rank == m + 1,
        "support_union": support_union,
        "has_adjacent_exponents": has_adjacent_exponents,
        "nontrivial_pullback_excluded_by_adjacent_exponents": has_adjacent_exponents,
        "inverse_pair_count": len(inverse_pairs),
        "expected_inverse_pair_count": (n - 2) // 2,
        "trace_checks": trace_checks,
        "all_trace_dependencies_hold": all(item["trace_dependence"] for item in trace_checks),
        "chebyshev_y_values_distinct": len(y_values) == len(inverse_pairs),
        "closed_set_lower_bound": closed_set_lower_bound,
    }


def build_certificate() -> dict[str, object]:
    note_text = NOTE.read_text(encoding="utf-8")
    cert = {
        "schema": "dihedral-quotient-stratum-v1",
        "status": "PROVED",
        "source_dag_node": "dihedral_quotient_stratum",
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "toy_check": toy_check(),
        "non_claims": [
            "does not prove the many-sparse classification theorem",
            "does not close a row-level Hankel safe-side certificate",
        ],
        "note": "experimental/notes/m1/dihedral_quotient_stratum.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, object]) -> None:
    if cert["schema"] != "dihedral-quotient-stratum-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    toy = cert["toy_check"]
    if not isinstance(toy, dict):
        raise AssertionError("missing toy check")
    for key in [
        "dimension_check",
        "nontrivial_pullback_excluded_by_adjacent_exponents",
        "all_trace_dependencies_hold",
        "chebyshev_y_values_distinct",
    ]:
        if not toy.get(key):
            raise AssertionError(f"failed toy check: {key}")
    if toy["inverse_pair_count"] != toy["expected_inverse_pair_count"]:
        raise AssertionError("inverse-pair count mismatch")


def assert_same(expected: dict[str, object], actual: dict[str, object]) -> None:
    if expected != actual:
        raise AssertionError(
            "certificate mismatch\nexpected:\n"
            + json.dumps(expected, indent=2, sort_keys=True)
            + "\nactual:\n"
            + json.dumps(actual, indent=2, sort_keys=True)
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()

    cert = build_certificate()
    if args.emit:
        ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
        ARTIFACT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
        print(f"wrote {ARTIFACT.relative_to(REPO)}")
    if args.check:
        actual = json.loads(args.check.read_text(encoding="utf-8"))
        validate(actual)
        assert_same(cert, actual)
        print(f"checked {args.check}")
    if not args.emit and not args.check:
        print(f"{cert['status']}: {cert['source_dag_node']}")


if __name__ == "__main__":
    main()
