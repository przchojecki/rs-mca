#!/usr/bin/env python3
"""Verify the equal-line split-fiber containment gate."""

from __future__ import annotations

from verify_m1_depth_two_equal_line_diagonal_reduction import (
    lambda_y_resultant,
    twist_y_value,
    y_kernel_argument,
)
from verify_m1_equal_line_generic_popularity_budget import singular_support_y


PRIMES = (5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47)


def normalize_projective(first: int, second: int, p: int) -> tuple[int, int]:
    first %= p
    second %= p
    if second == 0:
        if first == 0:
            raise AssertionError(("zero projective point", p))
        return (1, 0)
    return (first * pow(second, -1, p) % p, 1)


def projective_line(p: int) -> list[tuple[int, int]]:
    return [(value, 1) for value in range(p)] + [(1, 0)]


def projective_y_point(z_point: tuple[int, int], p: int) -> tuple[int, int]:
    z_num, z_den = z_point
    y_num = z_den * z_den + 3 * z_num * z_num
    y_den = (z_den - z_num) * (z_den - z_num)
    return normalize_projective(y_num, y_den, p)


def projective_kernel_argument(
    x_point: tuple[int, int], z_point: tuple[int, int], p: int
) -> int:
    x_num, x_den = x_point
    z_num, z_den = z_point
    return (x_num * (z_den * z_den + 3 * z_num * z_num) - x_den * z_num * z_num) % p


def projective_resultant(
    x_point: tuple[int, int], y_point: tuple[int, int], p: int
) -> int:
    x_num, x_den = x_point
    y_num, y_den = y_point
    return (
        16 * x_num * x_num * y_num * y_num
        - 8 * x_num * x_den * y_num * y_num
        + 4 * x_num * x_den * y_num * y_den
        + x_den * x_den * y_num * y_num
        - 2 * x_den * x_den * y_num * y_den
        + x_den * x_den * y_den * y_den
    ) % p


def det_mod(matrix: list[list[int]], p: int) -> int:
    rows = [[entry % p for entry in row] for row in matrix]
    determinant = 1
    for col in range(len(rows)):
        pivot = None
        for row in range(col, len(rows)):
            if rows[row][col] % p != 0:
                pivot = row
                break
        if pivot is None:
            return 0
        if pivot != col:
            rows[col], rows[pivot] = rows[pivot], rows[col]
            determinant = -determinant
        pivot_value = rows[col][col] % p
        determinant = determinant * pivot_value % p
        inverse = pow(pivot_value, -1, p)
        for row in range(col + 1, len(rows)):
            factor = rows[row][col] * inverse % p
            for inner in range(col, len(rows)):
                rows[row][inner] = (rows[row][inner] - factor * rows[col][inner]) % p
    return determinant % p


def quadratic_resultant(
    left: tuple[int, int, int], right: tuple[int, int, int], p: int
) -> int:
    a, b, c = left
    d, e, f = right
    return det_mod(
        [
            [a, b, c, 0],
            [0, a, b, c],
            [d, e, f, 0],
            [0, d, e, f],
        ],
        p,
    )


def fiber_equation_coefficients(y_point: tuple[int, int], p: int) -> tuple[int, int, int]:
    y_num, y_den = y_point
    return ((y_num - 3 * y_den) % p, (-2 * y_num) % p, (y_num - y_den) % p)


def kernel_coefficients(x_point: tuple[int, int], p: int) -> tuple[int, int, int]:
    x_num, x_den = x_point
    return ((3 * x_num - x_den) % p, 0, x_num % p)


def is_finite_leaf_regular(z: int, p: int) -> bool:
    if z == 1:
        return False
    if (1 + 3 * z * z) % p == 0:
        return False
    y_value = twist_y_value(z, p)
    return (y_value, 1) not in singular_support_y(p)


def split_fiber_roots(y_value: int, p: int) -> list[int]:
    roots = []
    for z in range(p):
        if z == 1 or (1 + 3 * z * z) % p == 0:
            continue
        if twist_y_value(z, p) == y_value:
            roots.append(z)
    return roots


def projective_split_fiber_roots(y_point: tuple[int, int], p: int) -> list[tuple[int, int]]:
    return [
        z_point
        for z_point in projective_line(p)
        if projective_y_point(z_point, p) == y_point
    ]


def check_regular_fibers_are_split() -> None:
    checked = 0
    for p in PRIMES:
        singular = singular_support_y(p)
        one_third = pow(3, -1, p)
        for y_value in range(p):
            if (y_value, 1) in singular:
                continue
            roots = split_fiber_roots(y_value, p)
            if y_value == 3 % p:
                if roots != [one_third]:
                    raise AssertionError(("bad y=3 finite fiber", p, roots))
                checked += 1
                continue
            if roots and len(roots) != 2:
                raise AssertionError(("ordinary fiber not split", p, y_value, roots))
            checked += 1
    print(f"regular_y_fibers_checked={checked}")


def check_projective_regular_fibers_are_split() -> None:
    checked = 0
    for p in PRIMES:
        singular = singular_support_y(p)
        for y_point in projective_line(p):
            if y_point in singular:
                continue
            roots = projective_split_fiber_roots(y_point, p)
            if roots and len(roots) != 2:
                raise AssertionError(("projective fiber not split", p, y_point, roots))
            checked += 1
    print(f"regular_projective_y_fibers_checked={checked}")


def check_projective_resultant_identity() -> None:
    checked = 0
    for p in PRIMES:
        for x_point in projective_line(p):
            kernel = kernel_coefficients(x_point, p)
            for y_point in projective_line(p):
                fiber = fiber_equation_coefficients(y_point, p)
                resultant = quadratic_resultant(fiber, kernel, p)
                expected = projective_resultant(x_point, y_point, p)
                if resultant != expected:
                    raise AssertionError(
                        ("projective resultant identity", p, x_point, y_point)
                    )
                checked += 1
    print(f"projective_resultant_identities_checked={checked}")


def check_product_identity_on_regular_fibers() -> None:
    checked = 0
    for p in PRIMES:
        singular = singular_support_y(p)
        for y_value in range(1, p):
            if (y_value, 1) in singular:
                continue
            if y_value == 3 % p:
                continue
            roots = split_fiber_roots(y_value, p)
            if len(roots) != 2:
                continue
            denominator = (y_value - 3) * (y_value - 3) % p
            if denominator == 0:
                raise AssertionError(("zero denominator", p, y_value))
            for x_value in range(p):
                product = 1
                for z in roots:
                    product = product * y_kernel_argument(x_value, z, p) % p
                expected = lambda_y_resultant(x_value, y_value, p)
                expected = expected * pow(denominator, -1, p) % p
                if product != expected:
                    raise AssertionError(
                        ("split product", p, x_value, y_value, product, expected)
                    )
                checked += 1
    print(f"regular_split_product_identities_checked={checked}")


def check_kernel_containment_implication() -> None:
    checked = 0
    hits = 0
    for p in PRIMES:
        one_third = pow(3, -1, p)
        one_twelfth = pow(12, -1, p)
        for z in range(p):
            if not is_finite_leaf_regular(z, p):
                continue
            y_value = twist_y_value(z, p)
            roots = split_fiber_roots(y_value, p)
            if y_value == 3 % p:
                if z != one_third or roots != [one_third]:
                    raise AssertionError(("bad y=3 root", p, z, roots))
            elif z not in roots or len(roots) != 2:
                raise AssertionError(("bad regular root", p, z, y_value, roots))
            for x_value in range(p):
                if y_kernel_argument(x_value, z, p) != 0:
                    continue
                hits += 1
                if y_value == 3 % p and x_value != one_twelfth:
                    raise AssertionError(("bad y=3 kernel root", p, x_value))
                if lambda_y_resultant(x_value, y_value, p) != 0:
                    raise AssertionError(
                        ("containment failed", p, x_value, z, y_value)
                    )
            checked += 1
    print(f"regular_leaf_parameters_checked={checked}")
    print(f"kernel_containment_hits_checked={hits}")


def check_projective_kernel_containment_implication() -> None:
    checked = 0
    hits = 0
    infinity_hits = 0
    for p in PRIMES:
        singular = singular_support_y(p)
        for z_point in projective_line(p):
            y_point = projective_y_point(z_point, p)
            if y_point in singular:
                continue
            roots = projective_split_fiber_roots(y_point, p)
            if z_point not in roots or len(roots) != 2:
                raise AssertionError(("bad projective root", p, z_point, y_point, roots))
            for x_point in projective_line(p):
                if projective_kernel_argument(x_point, z_point, p) != 0:
                    continue
                hits += 1
                if z_point == (1, 0):
                    infinity_hits += 1
                    if x_point != (pow(3, -1, p), 1):
                        raise AssertionError(("bad z=infinity kernel root", p, x_point))
                if projective_resultant(x_point, y_point, p) != 0:
                    raise AssertionError(
                        ("projective containment failed", p, x_point, z_point, y_point)
                    )
            checked += 1
    print(f"regular_projective_leaf_parameters_checked={checked}")
    print(f"projective_kernel_containment_hits_checked={hits}")
    print(f"projective_infinity_leaf_hits_checked={infinity_hits}")


def main() -> None:
    check_regular_fibers_are_split()
    check_projective_regular_fibers_are_split()
    check_projective_resultant_identity()
    check_product_identity_on_regular_fibers()
    check_kernel_containment_implication()
    check_projective_kernel_containment_implication()
    print("m1 equal-line split-fiber containment checks passed")


if __name__ == "__main__":
    main()
