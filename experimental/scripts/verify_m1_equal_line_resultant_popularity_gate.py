#!/usr/bin/env python3
"""Verify the equal-line resultant popularity gate."""

from __future__ import annotations

from verify_m1_high_overlap_graph_budget import support_floor_from_popularity_cap
from verify_m1_popularity_divisor_gate import (
    binary_degree,
    divisor_gate_cap,
    projective_line,
    projective_roots,
)


PRIMES = (5, 7, 11, 13, 17, 19, 23, 29, 31, 37)


def resultant_affine(x: int, y: int, p: int) -> int:
    return (
        16 * x * x * y * y
        - 8 * x * y * y
        + 4 * x * y
        + y * y
        - 2 * y
        + 1
    ) % p


def resultant_homogeneous(
    x_num: int, x_den: int, y_num: int, y_den: int, p: int
) -> int:
    x_num %= p
    x_den %= p
    y_num %= p
    y_den %= p
    return (
        16 * x_num * x_num * y_num * y_num
        - 8 * x_num * x_den * y_num * y_num
        + 4 * x_num * x_den * y_num * y_den
        + x_den * x_den * y_num * y_num
        - 2 * x_den * x_den * y_num * y_den
        + x_den * x_den * y_den * y_den
    ) % p


def fixed_x_form(x_num: int, x_den: int, p: int) -> tuple[int, int, int]:
    x_num %= p
    x_den %= p
    return (
        (x_den * x_den) % p,
        (2 * x_den * (2 * x_num - x_den)) % p,
        ((4 * x_num - x_den) * (4 * x_num - x_den)) % p,
    )


def fixed_y_form(y_num: int, y_den: int, p: int) -> tuple[int, int, int]:
    y_num %= p
    y_den %= p
    return (
        ((y_num - y_den) * (y_num - y_den)) % p,
        (4 * y_num * (y_den - 2 * y_num)) % p,
        (16 * y_num * y_num) % p,
    )


def eval_binary_quadratic(
    form: tuple[int, int, int], point: tuple[int, int], p: int
) -> int:
    y_num, y_den = point
    return (
        form[0] * y_den * y_den
        + form[1] * y_num * y_den
        + form[2] * y_num * y_num
    ) % p


def check_homogenization() -> None:
    checked = 0
    for p in PRIMES:
        for x in range(p):
            for y in range(p):
                if resultant_homogeneous(x, 1, y, 1, p) != resultant_affine(x, y, p):
                    raise AssertionError((p, x, y))
                checked += 1
        for x_point in projective_line(p):
            form = fixed_x_form(*x_point, p)
            for y_point in projective_line(p):
                if eval_binary_quadratic(form, y_point, p) != resultant_homogeneous(
                    x_point[0], x_point[1], y_point[0], y_point[1], p
                ):
                    raise AssertionError(("fixed x", p, x_point, y_point, form))
                checked += 1
        for y_point in projective_line(p):
            form = fixed_y_form(*y_point, p)
            for x_point in projective_line(p):
                if eval_binary_quadratic(form, x_point, p) != resultant_homogeneous(
                    x_point[0], x_point[1], y_point[0], y_point[1], p
                ):
                    raise AssertionError(("fixed y", p, x_point, y_point, form))
                checked += 1
    print(f"homogenization_checks={checked}")


def check_nonzero_projective_fibers() -> None:
    checked = 0
    for p in PRIMES:
        for x_point in projective_line(p):
            form = fixed_x_form(*x_point, p)
            if all(coeff % p == 0 for coeff in form):
                raise AssertionError(("zero fixed-x form", p, x_point, form))
            if binary_degree(form, p) > 2:
                raise AssertionError(("bad fixed-x degree", p, x_point, form))
            roots = projective_roots(form, p)
            if len(roots) > 2:
                raise AssertionError(("too many y roots", p, x_point, roots))
            checked += 1

        for y_point in projective_line(p):
            form = fixed_y_form(*y_point, p)
            if all(coeff % p == 0 for coeff in form):
                raise AssertionError(("zero fixed-y form", p, y_point, form))
            if binary_degree(form, p) > 2:
                raise AssertionError(("bad fixed-y degree", p, y_point, form))
            roots = projective_roots(form, p)
            if len(roots) > 2:
                raise AssertionError(("too many x roots", p, y_point, roots))
            checked += 1
    print(f"nonzero_projective_fibers_checked={checked}")


def check_named_boundary_restrictions() -> None:
    checked = 0
    for p in PRIMES:
        for y in range(p):
            if resultant_affine(0, y, p) != (y - 1) * (y - 1) % p:
                raise AssertionError(("x=0", p, y))
            if resultant_affine(1, y, p) != (9 * y * y + 2 * y + 1) % p:
                raise AssertionError(("x=1", p, y))
            if resultant_affine(y, 0, p) != 1:
                raise AssertionError(("y=0", p, y))
            checked += 1

        x_infinity = (1, 0)
        y_infinity = (1, 0)
        y_zero = (0, 1)
        x_zero = (0, 1)
        if fixed_x_form(*x_infinity, p) != (0, 0, 16 % p):
            raise AssertionError(("x infinity", p, fixed_x_form(*x_infinity, p)))
        if fixed_y_form(*y_infinity, p) != (1, -8 % p, 16 % p):
            raise AssertionError(("y infinity", p, fixed_y_form(*y_infinity, p)))
        if fixed_y_form(*y_zero, p) != (1, 0, 0):
            raise AssertionError(("y zero", p, fixed_y_form(*y_zero, p)))
        if eval_binary_quadratic(fixed_y_form(*y_zero, p), x_zero, p) != 1:
            raise AssertionError(("affine y zero", p))
    print(f"boundary_restrictions_checked={checked}")


def check_popularity_gate_composition() -> None:
    checked = 0
    for k in range(2, 24):
        for s in range(1, 13):
            for h in range(1, 5):
                for degree_cap in range(1, 7):
                    for lambda_cap in range(0, s):
                        for multiplicity in range(1, 5):
                            for exceptional_size in range(0, 6):
                                gate_cap = divisor_gate_cap(
                                    multiplicity,
                                    exceptional_size,
                                    [2],
                                )
                                floor = support_floor_from_popularity_cap(
                                    k, s, h, degree_cap, lambda_cap, gate_cap
                                )
                                weaker_floor = support_floor_from_popularity_cap(
                                    k, s, h, degree_cap, lambda_cap, gate_cap + 1
                                )
                                if floor < weaker_floor:
                                    raise AssertionError(
                                        (
                                            k,
                                            s,
                                            h,
                                            degree_cap,
                                            lambda_cap,
                                            multiplicity,
                                            exceptional_size,
                                            floor,
                                            weaker_floor,
                                        )
                                    )
                                checked += 1
    print(f"popularity_gate_compositions_checked={checked}")


def main() -> None:
    check_homogenization()
    check_nonzero_projective_fibers()
    check_named_boundary_restrictions()
    check_popularity_gate_composition()
    print("m1 equal-line resultant popularity-gate checks passed")


if __name__ == "__main__":
    main()
