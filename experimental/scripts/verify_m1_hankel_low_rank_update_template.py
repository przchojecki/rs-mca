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
from itertools import combinations, permutations
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


def inverse_matrix_mod(matrix: list[list[int]], p: int) -> list[list[int]] | None:
    size = len(matrix)
    work = [
        [entry % p for entry in row]
        + [1 if row_index == col_index else 0 for col_index in range(size)]
        for row_index, row in enumerate(matrix)
    ]
    for col in range(size):
        pivot = None
        for row in range(col, size):
            if work[row][col] % p:
                pivot = row
                break
        if pivot is None:
            return None
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]
        inv = pow(work[col][col], -1, p)
        for entry_col in range(2 * size):
            work[col][entry_col] = work[col][entry_col] * inv % p
        for row in range(size):
            if row == col:
                continue
            factor = work[row][col] % p
            if factor == 0:
                continue
            for entry_col in range(2 * size):
                work[row][entry_col] = (
                    work[row][entry_col] - factor * work[col][entry_col]
                ) % p
    return [row[size:] for row in work]


def matrix_multiply_mod(
    left: list[list[int]],
    right: list[list[int]],
    p: int,
) -> list[list[int]]:
    if not left or not right:
        return []
    rows = len(left)
    inner = len(right)
    cols = len(right[0])
    return [
        [
            sum(left[row][index] * right[index][col] for index in range(inner)) % p
            for col in range(cols)
        ]
        for row in range(rows)
    ]


def matrix_transpose(matrix: list[list[int]]) -> list[list[int]]:
    if not matrix:
        return []
    return [list(row) for row in zip(*matrix)]


def polynomial_add(left: list[int], right: list[int], p: int) -> list[int]:
    length = max(len(left), len(right))
    result = [0] * length
    for index in range(length):
        result[index] = (
            (left[index] if index < len(left) else 0)
            + (right[index] if index < len(right) else 0)
        ) % p
    return trim_polynomial(result, p)


def polynomial_mul(left: list[int], right: list[int], p: int) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            result[left_index + right_index] = (
                result[left_index + right_index] + left_value * right_value
            ) % p
    return trim_polynomial(result, p)


def polynomial_scale(coefficients: list[int], scalar: int, p: int) -> list[int]:
    return trim_polynomial([scalar * coefficient % p for coefficient in coefficients], p)


def permutation_sign(permutation: tuple[int, ...]) -> int:
    inversions = 0
    for left_index, left in enumerate(permutation):
        for right in permutation[left_index + 1 :]:
            if left > right:
                inversions += 1
    return -1 if inversions % 2 else 1


def polynomial_determinant_mod(matrix: list[list[list[int]]], p: int) -> list[int]:
    size = len(matrix)
    if size == 0:
        return [1]
    total = [0]
    for permutation in permutations(range(size)):
        term = [1]
        for row, col in enumerate(permutation):
            term = polynomial_mul(term, matrix[row][col], p)
        if permutation_sign(permutation) < 0:
            term = polynomial_scale(term, -1, p)
        total = polynomial_add(total, term, p)
    return trim_polynomial(total, p)


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


def vandermonde_matrix(
    nodes: tuple[int, ...],
    size: int,
    p: int,
) -> list[list[int]]:
    return [[pow(node, row, p) for node in nodes] for row in range(size)]


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


def determinant_lemma_coefficients(
    base_nodes: tuple[int, ...],
    update_nodes: tuple[int, ...],
    size: int,
    p: int,
) -> dict[str, Any]:
    base_hankel = hankel_matrix(base_nodes, (), size, 0, p)
    base_determinant = determinant_mod(base_hankel, p)
    result: dict[str, Any] = {
        "base_hankel_determinant_mod_17": base_determinant,
        "compressed_identity_status": (
            "base_singular_not_applied"
            if base_determinant == 0
            else "verified_matrix_determinant_lemma"
        ),
    }
    base_inverse = inverse_matrix_mod(base_hankel, p)
    if base_inverse is None:
        return result

    update_vandermonde = vandermonde_matrix(update_nodes, size, p)
    kernel = matrix_multiply_mod(
        matrix_multiply_mod(matrix_transpose(update_vandermonde), base_inverse, p),
        update_vandermonde,
        p,
    )
    kernel_polynomial_matrix = [
        [
            [1 if row == col else 0, kernel[row][col] % p]
            for col in range(len(update_nodes))
        ]
        for row in range(len(update_nodes))
    ]
    kernel_coefficients = polynomial_determinant_mod(kernel_polynomial_matrix, p)
    determinant_coefficients = polynomial_scale(
        kernel_coefficients, base_determinant, p
    )
    result.update(
        {
            "compressed_kernel_mod_17": kernel,
            "compressed_kernel_det_coefficients_mod_17_ascending": (
                kernel_coefficients
            ),
            "compressed_hankel_coefficients_mod_17_ascending": (
                determinant_coefficients
            ),
        }
    )
    return result


def quadratic_root_gate_mod(
    coefficients: list[int],
    roots: list[int],
    p: int,
) -> dict[str, Any]:
    trimmed = trim_polynomial(coefficients, p)
    degree = polynomial_degree(trimmed, p)
    if degree != 2:
        return {
            "status": "not_quadratic",
            "reason": f"polynomial degree is {degree}",
        }
    c0, c1, c2 = trimmed
    discriminant = (c1 * c1 - 4 * c2 * c0) % p
    square_roots = [
        value for value in range(p) if value * value % p == discriminant
    ]
    denominator_inverse = pow((2 * c2) % p, -1, p)
    formula_roots = sorted(
        {
            ((-c1 + sqrt_value) * denominator_inverse) % p
            for sqrt_value in square_roots
        }
    )
    require(
        formula_roots == roots,
        "quadratic discriminant root gate did not match direct roots",
    )
    return {
        "status": "split" if square_roots else "nonsquare_no_roots",
        "discriminant_mod_17": discriminant,
        "sqrt_discriminants_mod_17": square_roots,
        "formula_roots_mod_17": formula_roots,
        "matches_direct_roots": True,
    }


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
        compressed = determinant_lemma_coefficients(
            base_nodes, update_nodes, size, P
        )
        if (
            compressed["compressed_identity_status"]
            == "verified_matrix_determinant_lemma"
        ):
            require(
                compressed["compressed_hankel_coefficients_mod_17_ascending"]
                == trim_polynomial(coefficients, P),
                f"{name}, size={size}: determinant lemma coefficient mismatch",
            )
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
                "compressed_determinant_lemma": compressed,
                "quadratic_root_gate": quadratic_root_gate_mod(
                    coefficients, roots, P
                )
                if len(update_nodes) == 2
                else None,
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
            "compressed_statement": (
                "If H_X=V_X V_X^T is invertible, the same determinant equals "
                "det(H_X) det(I+Z K), where K=V_Y^T H_X^{-1} V_Y.  Thus the "
                "large r x r determinant is reduced to a |Y| x |Y| determinant "
                "without changing the root-count bound."
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
            "compressed_formula": (
                "when H_X is nonsingular, "
                "Delta_r(Z)=det(H_X) det(I+Z V_Y^T H_X^{-1} V_Y)"
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
