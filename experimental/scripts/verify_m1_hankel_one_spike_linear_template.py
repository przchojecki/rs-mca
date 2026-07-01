#!/usr/bin/env python3
"""Verify the one-spike linear Hankel determinant template.

This is a reusable M1/M3 algebraic template.  If

    u_m = sum_{x in X} x^m,      v_m = y^m,

then the prefix regular Hankel matrix is

    H_r(u) + Z H_r(v) = V_X V_X^T + Z w_y w_y^T.

The direction is generally non-proportional, but the determinant is affine in
Z because the direction has rank one.  This gives a closed-form one-root
regular-minor packet template without enumerating the ambient field.
"""

from __future__ import annotations

import argparse
from itertools import combinations
import json
from pathlib import Path
from typing import Any


P = 17
SCHEMA_VERSION = "m1-hankel-one-spike-linear-template-v1"
OUTPUT_PATH = Path(
    "experimental/data/certificates/hankel-one-spike-linear-template/"
    "hankel_one_spike_linear_template_certificate.json"
)


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def determinant_mod(matrix: list[list[int]], p: int) -> int:
    work = [[entry % p for entry in row] for row in matrix]
    n = len(work)
    det = 1
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if work[row][col] % p:
                pivot = row
                break
        if pivot is None:
            return 0
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]
            det = (-det) % p
        pivot_value = work[col][col] % p
        det = (det * pivot_value) % p
        inv = pow(pivot_value, -1, p)
        for row in range(col + 1, n):
            factor = work[row][col] * inv % p
            if factor == 0:
                continue
            for entry_col in range(col, n):
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


def moment(base_nodes: tuple[int, ...], spike: int, index: int, z_value: int, p: int) -> int:
    total = sum(pow(node, index, p) for node in base_nodes)
    total += z_value * pow(spike, index, p)
    return total % p


def hankel_matrix(
    base_nodes: tuple[int, ...], spike: int, size: int, z_value: int, p: int
) -> list[list[int]]:
    return [
        [moment(base_nodes, spike, row + col, z_value, p) for col in range(size)]
        for row in range(size)
    ]


def cauchy_binet_coefficients(
    base_nodes: tuple[int, ...], spike: int, size: int, p: int
) -> tuple[int, int]:
    constant = sum(
        vandermonde_square(tuple(subset), p)
        for subset in combinations(base_nodes, size)
    ) % p
    linear = sum(
        vandermonde_square(tuple(subset) + (spike,), p)
        for subset in combinations(base_nodes, size - 1)
    ) % p
    return constant, linear


def visible_proportional_scalar(
    base_nodes: tuple[int, ...], spike: int, visible_length: int, p: int
) -> int | None:
    scalar = None
    for index in range(visible_length):
        u_i = sum(pow(node, index, p) for node in base_nodes) % p
        v_i = pow(spike, index, p)
        if v_i == 0:
            if u_i != 0:
                return None
            continue
        candidate = u_i * pow(v_i, -1, p) % p
        if scalar is None:
            scalar = candidate
        elif scalar != candidate:
            return None
    return scalar


def check_case(name: str, base_nodes: tuple[int, ...], spike: int, max_size: int) -> dict[str, Any]:
    rows = []
    for size in range(1, max_size + 1):
        constant, linear = cauchy_binet_coefficients(base_nodes, spike, size, P)
        for z_value in range(P):
            determinant = determinant_mod(hankel_matrix(base_nodes, spike, size, z_value, P), P)
            expected = (constant + z_value * linear) % P
            require(
                determinant == expected,
                f"{name}, size={size}, z={z_value}: determinant mismatch",
            )
        roots = [
            z_value
            for z_value in range(P)
            if (constant + z_value * linear) % P == 0
        ]
        visible_length = 2 * size - 1
        rows.append(
            {
                "size": size,
                "visible_moment_indices": [0, visible_length - 1],
                "constant_coefficient": constant,
                "linear_coefficient": linear,
                "roots_mod_17": roots,
                "root_count": len(roots),
                "visible_proportional_scalar": visible_proportional_scalar(
                    base_nodes, spike, visible_length, P
                ),
                "checked_all_z_mod_17": True,
            }
        )
    return {
        "name": name,
        "field": "F_17",
        "base_nodes": list(base_nodes),
        "spike": spike,
        "rows": rows,
    }


def build_certificate() -> dict[str, Any]:
    cases = [
        check_case("four_base_nodes_one_spike", (1, 2, 4, 8), 3, 4),
        check_case("singular_base_closed_by_spike", (1, 2), 4, 3),
        check_case("longer_nonproportional_window", (1, 3, 5, 7, 11), 2, 5),
    ]
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "theorem": {
            "name": "one-spike Hankel linear determinant template",
            "proof_status": "Cauchy-Binet identity plus finite verifier",
            "statement": (
                "For prefix size r, base moments u_m=sum_{x in X}x^m, and "
                "one-spike direction v_m=y^m, the regular Hankel determinant "
                "det(H_r(u)+Z H_r(v)) is affine in Z.  Its coefficients are "
                "sum_{|S|=r,S subset X} Vandermonde(S)^2 and "
                "sum_{|T|=r-1,T subset X} Vandermonde(T union {y})^2."
            ),
            "m3_use": (
                "A nonzero linear coefficient gives an exact one-root "
                "regular-minor containment certificate for a non-proportional "
                "one-spike direction, without field enumeration."
            ),
        },
        "identity": {
            "matrix_factorization": "H_r(u)+Z H_r(v)=V_X V_X^T + Z w_y w_y^T",
            "determinant_shape": "Delta_r(Z)=C_0 + Z C_1",
            "root_rule": "if C_1!=0 then roots={-C_0/C_1}; if C_1=0 and C_0!=0 then roots=empty",
        },
        "cases": cases,
        "nonclaims": [
            "not an actual F_17^32 M3 row packet",
            "does not classify arbitrary non-proportional pencils",
            "does not perform quotient/tangent subtraction for a prize row",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"one-spike certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    theorem = certificate["theorem"]
    print(theorem["name"])
    print(f"status: {certificate['status']}")
    for case in certificate["cases"]:
        max_roots = max(row["root_count"] for row in case["rows"])
        print(f"{case['name']}: rows={len(case['rows'])}, max_roots={max_roots}")


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
