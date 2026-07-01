#!/usr/bin/env python3
"""Verify the low-rank Hankel update determinant template.

This is the finite-rank generalization of the one-spike template.  If

    u_m = sum_{x in X} x^m,      v_m = sum_{y in Y} y^m,

with X and Y disjoint, then the prefix regular Hankel matrix is

    H_r(u) + Z H_r(v) = V_X V_X^T + Z V_Y V_Y^T.

Equivalently it is V D(Z) V^T with diagonal weights 1 on X and Z on Y.
Cauchy-Binet gives a determinant polynomial of degree at most |Y|, independent
of the minor size r.  This script records a deterministic finite verifier over
F_17 for the identity and root-count consequence.
"""

from __future__ import annotations

import argparse
from itertools import combinations
import json
from pathlib import Path
from typing import Any


P = 17
SCHEMA_VERSION = "m1-hankel-low-rank-update-template-v1"
OUTPUT_PATH = Path(
    "experimental/data/certificates/hankel-low-rank-update-template/"
    "hankel_low_rank_update_template_certificate.json"
)


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def trim_polynomial(coefficients: list[int], p: int) -> list[int]:
    out = [coefficient % p for coefficient in coefficients]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def polynomial_degree(coefficients: list[int], p: int) -> int:
    trimmed = trim_polynomial(coefficients, p)
    if len(trimmed) == 1 and trimmed[0] == 0:
        return -1
    return len(trimmed) - 1


def polynomial_eval(coefficients: list[int], value: int, p: int) -> int:
    total = 0
    power = 1
    for coefficient in coefficients:
        total = (total + coefficient * power) % p
        power = power * value % p
    return total


def determinant_mod(matrix: list[list[int]], p: int) -> int:
    work = [[entry % p for entry in row] for row in matrix]
    size = len(work)
    det = 1
    for col in range(size):
        pivot = None
        for row in range(col, size):
            if work[row][col] % p:
                pivot = row
                break
        if pivot is None:
            return 0
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]
            det = (-det) % p
        pivot_value = work[col][col] % p
        det = det * pivot_value % p
        inv = pow(pivot_value, -1, p)
        for row in range(col + 1, size):
            factor = work[row][col] * inv % p
            if factor == 0:
                continue
            for entry_col in range(col, size):
                work[row][entry_col] = (
                    work[row][entry_col] - factor * work[col][entry_col]
                ) % p
    return det % p


def vandermonde_square(nodes: tuple[int, ...], p: int) -> int:
    value = 1
    for left_index, left in enumerate(nodes):
        for right in nodes[left_index + 1 :]:
            value = value * (right - left) * (right - left) % p
    return value


def moment(
    base_nodes: tuple[int, ...],
    update_nodes: tuple[int, ...],
    index: int,
    z_value: int,
    p: int,
) -> int:
    total = sum(pow(node, index, p) for node in base_nodes)
    total += z_value * sum(pow(node, index, p) for node in update_nodes)
    return total % p


def hankel_matrix(
    base_nodes: tuple[int, ...],
    update_nodes: tuple[int, ...],
    size: int,
    z_value: int,
    p: int,
) -> list[list[int]]:
    return [
        [
            moment(base_nodes, update_nodes, row + col, z_value, p)
            for col in range(size)
        ]
        for row in range(size)
    ]


def cauchy_binet_coefficients(
    base_nodes: tuple[int, ...],
    update_nodes: tuple[int, ...],
    size: int,
    p: int,
) -> list[int]:
    coefficients = [0] * (len(update_nodes) + 1)
    for update_count in range(len(update_nodes) + 1):
        base_count = size - update_count
        if base_count < 0 or base_count > len(base_nodes):
            continue
        for base_subset in combinations(base_nodes, base_count):
            for update_subset in combinations(update_nodes, update_count):
                nodes = tuple(base_subset) + tuple(update_subset)
                coefficients[update_count] = (
                    coefficients[update_count] + vandermonde_square(nodes, p)
                ) % p
    return coefficients


def visible_proportional_scalar(
    base_nodes: tuple[int, ...],
    update_nodes: tuple[int, ...],
    visible_length: int,
    p: int,
) -> int | None:
    scalar = None
    for index in range(visible_length):
        u_i = sum(pow(node, index, p) for node in base_nodes) % p
        v_i = sum(pow(node, index, p) for node in update_nodes) % p
        if v_i == 0:
            if u_i != 0:
                return None
            continue
        candidate = u_i * pow(v_i, -1, p) % p
        if scalar is None:
            scalar = candidate
        elif scalar != candidate:
            return None
    return 0 if scalar is None else scalar


def check_case(
    name: str,
    base_nodes: tuple[int, ...],
    update_nodes: tuple[int, ...],
    max_size: int,
) -> dict[str, Any]:
    require(set(base_nodes).isdisjoint(update_nodes), f"{name}: node sets overlap")
    require(max_size > 0, f"{name}: max_size must be positive")

    rows = []
    for size in range(1, max_size + 1):
        coefficients = cauchy_binet_coefficients(base_nodes, update_nodes, size, P)
        degree = polynomial_degree(coefficients, P)
        zero_polynomial = degree == -1
        for z_value in range(P):
            determinant = determinant_mod(
                hankel_matrix(base_nodes, update_nodes, size, z_value, P),
                P,
            )
            expected = polynomial_eval(coefficients, z_value, P)
            require(
                determinant == expected,
                f"{name}, size={size}, z={z_value}: determinant mismatch",
            )
        roots = [
            z_value
            for z_value in range(P)
            if polynomial_eval(coefficients, z_value, P) == 0
        ]
        if not zero_polynomial:
            require(
                len(roots) <= len(update_nodes),
                f"{name}, size={size}: root count exceeds update rank",
            )
        visible_length = 2 * size - 1
        rows.append(
            {
                "size": size,
                "visible_moment_indices": [0, visible_length - 1],
                "update_rank_bound": len(update_nodes),
                "coefficients_mod_17_ascending": coefficients,
                "polynomial_degree": degree,
                "zero_polynomial": zero_polynomial,
                "roots_mod_17": roots,
                "root_count": len(roots),
                "root_bound_status": "singular_residual"
                if zero_polynomial
                else "bounded_by_update_rank",
                "visible_proportional_scalar": visible_proportional_scalar(
                    base_nodes, update_nodes, visible_length, P
                ),
                "checked_all_z_mod_17": True,
            }
        )
    return {
        "name": name,
        "field": "F_17",
        "base_nodes": list(base_nodes),
        "update_nodes": list(update_nodes),
        "rows": rows,
    }


def build_certificate() -> dict[str, Any]:
    cases = [
        check_case("rank_one_linear_template", (1, 2, 4, 8), (3,), 4),
        check_case("rank_two_quadratic_template", (1, 2, 4, 8, 9), (3, 5), 5),
        check_case("rank_three_base_deficient_template", (1, 2), (3, 4, 5), 4),
        check_case("rank_deficient_singular_residual", (1,), (2,), 3),
    ]
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "theorem": {
            "name": "low-rank Hankel update determinant template",
            "proof_status": "Cauchy-Binet identity plus finite verifier",
            "statement": (
                "Let X and Y be disjoint finite node sets in a field.  For "
                "u_m=sum_{x in X}x^m and v_m=sum_{y in Y}y^m, the prefix "
                "regular determinant det(H_r(u)+Z H_r(v)) has coefficient of "
                "Z^d equal to the sum of Vandermonde(S)^2 over all r-subsets "
                "S of X union Y with exactly d nodes from Y.  Hence the "
                "degree is at most |Y|; if the polynomial is nonzero, its "
                "finite root count is at most |Y|."
            ),
            "m3_use": (
                "A non-proportional syndrome pencil whose direction has "
                "power-sum rank s gives a regular-minor root bound <=s from "
                "one prefix minor when that minor determinant is nonzero; "
                "the zero-determinant case is a singular residual bucket. "
                "The bound is independent of the M3 minor size j+1."
            ),
        },
        "identity": {
            "matrix_factorization": (
                "H_r(u)+Z H_r(v)=V_X V_X^T + Z V_Y V_Y^T"
            ),
            "cauchy_binet_formula": (
                "Delta_r(Z)=sum_{S subset X union Y, |S|=r} "
                "Vandermonde(S)^2 Z^{|S cap Y|}"
            ),
            "root_rule": (
                "if Delta_r is nonzero, finite roots are bounded by "
                "degree(Delta_r)<=|Y|; if Delta_r is zero, the bucket is "
                "singular and must be passed to the pivot/residual atlas"
            ),
        },
        "cases": cases,
        "nonclaims": [
            "not an actual F_17^32 M3 row packet",
            "does not classify arbitrary non-proportional pencils",
            "does not perform quotient/tangent subtraction for a prize row",
            "zero determinant rows are residual buckets, not aperiodic evidence",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"low-rank update certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    theorem = certificate["theorem"]
    print(theorem["name"])
    print(f"status: {certificate['status']}")
    for case in certificate["cases"]:
        nonzero_rows = [
            row for row in case["rows"] if row["root_bound_status"] != "singular_residual"
        ]
        max_roots = max((row["root_count"] for row in nonzero_rows), default=0)
        singular_rows = sum(
            row["root_bound_status"] == "singular_residual"
            for row in case["rows"]
        )
        print(
            f"{case['name']}: rows={len(case['rows'])}, "
            f"max_nonzero_roots={max_roots}, singular_rows={singular_rows}"
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
