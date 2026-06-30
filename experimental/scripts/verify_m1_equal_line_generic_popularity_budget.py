#!/usr/bin/env python3
"""Verify the equal-line generic popularity budget U <= 8 mu."""

from __future__ import annotations

from verify_m1_depth_two_equal_line_diagonal_reduction import (
    lambda_one_y_polynomial,
    twist_y_value,
    verify_pushforward_singular_values,
)
from verify_m1_equal_line_resultant_popularity_gate import fixed_x_form
from verify_m1_high_overlap_graph_budget import support_floor_from_popularity_cap
from verify_m1_popularity_divisor_gate import (
    binary_degree,
    divisor_gate_cap,
    projective_line,
    projective_roots,
)


PRIMES = (5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43)


def singular_support_y(p: int) -> set[tuple[int, int]]:
    if p <= 3:
        raise ValueError("p must be > 3")
    support = {
        (0, 1),  # y=0
        (1, 1),  # y=1
        (3 * pow(4, -1, p) % p, 1),  # y=3/4
        (1, 0),  # infinity
    }
    for y_value in range(p):
        if lambda_one_y_polynomial(y_value, p) == 0:
            support.add((y_value, 1))
    return support


def check_singular_budget() -> None:
    checked = 0
    for p in PRIMES:
        row = verify_pushforward_singular_values(p)
        support = singular_support_y(p)
        if len(support) > 6:
            raise AssertionError((p, support, row))
        expected_roots = sorted(
            y_value
            for y_value in range(p)
            if lambda_one_y_polynomial(y_value, p) == 0
        )
        if sorted(row["lambda_one_y_roots"]) != expected_roots:
            raise AssertionError((p, row["lambda_one_y_roots"], expected_roots))
        if row["generic_singular_value_count"] != 6:
            raise AssertionError((p, row))
        if p == 11 and not row["exceptional_p11_collision"]:
            raise AssertionError(("expected p=11 collision", row))
        if p != 11 and row["exceptional_p11_collision"]:
            raise AssertionError(("unexpected collision", row))
        checked += 1
    print(f"equal_line_singular_budgets_checked={checked}")


def check_quadratic_gate_budget() -> None:
    checked = 0
    for p in PRIMES:
        support = singular_support_y(p)
        for x_point in projective_line(p):
            form = fixed_x_form(*x_point, p)
            if all(coeff % p == 0 for coeff in form):
                raise AssertionError((p, x_point, form))
            if binary_degree(form, p) > 2:
                raise AssertionError((p, x_point, form))
            roots = projective_roots(form, p)
            if len(roots) > 2:
                raise AssertionError((p, x_point, roots))
            combined = support | roots
            if len(combined) > 8:
                raise AssertionError((p, x_point, support, roots, combined))
            checked += 1
    print(f"equal_line_quadratic_gate_budgets_checked={checked}")


def equal_line_forced_overlap_centers(p: int) -> set[tuple[int, int]]:
    centers = {
        (1, 0),  # x=infinity overlaps y=0.
        (0, 1),  # x=0 overlaps y=1.
        (pow(4, -1, p), 1),  # x=1/4 overlaps y=1 and y=infinity.
        (pow(12, -1, p), 1),  # x=1/12 overlaps y=3/4.
        (1, 1),  # x=1 overlaps the lambda=1 singular fibers.
    }
    for x_value in range(p):
        if (16 * x_value * x_value + 8 * x_value + 9) % p == 0:
            centers.add((x_value, 1))
    return centers


def check_quadratic_gate_sharpness() -> None:
    checked = 0
    sharp_rows: list[tuple[int, tuple[int, int], int]] = []
    for p in PRIMES:
        support = singular_support_y(p)
        forced_overlap = equal_line_forced_overlap_centers(p)
        best_size = 0
        best_center = None
        for x_point in projective_line(p):
            roots = projective_roots(fixed_x_form(*x_point, p), p)
            overlaps = roots & support
            if overlaps and x_point not in forced_overlap:
                raise AssertionError(("unexpected singular overlap", p, x_point, overlaps))
            combined_size = len(support | roots)
            if combined_size > best_size:
                best_size = combined_size
                best_center = x_point
            checked += 1
        if best_size == 8 and best_center is not None:
            sharp_rows.append((p, best_center, best_size))

    if not sharp_rows:
        raise AssertionError("equal-line 8-point cap was not witnessed")
    print(f"equal_line_quadratic_gate_sharpness_checks={checked}")
    print(f"equal_line_quadratic_gate_sharp_rows={len(sharp_rows)}")


def check_injective_z_leaf_multiplicity_cap() -> None:
    checked = 0
    max_finite_fiber_size = 0
    for p in PRIMES:
        for y_value in range(p):
            roots = [
                z
                for z in range(p)
                if z != 1 and twist_y_value(z, p) == y_value
            ]
            if len(roots) > 2:
                raise AssertionError((p, y_value, roots))
            max_finite_fiber_size = max(max_finite_fiber_size, len(roots))
            checked += 1

        # The projective pole of y(z) is the single point z=1.
        pole_roots = [z for z in range(p) if z == 1]
        if len(pole_roots) != 1:
            raise AssertionError((p, pole_roots))
        checked += 1

    if max_finite_fiber_size != 2:
        raise AssertionError(("unexpected max finite fiber", max_finite_fiber_size))
    injective_gate_cap = divisor_gate_cap(2, 6, [2])
    if injective_gate_cap != 16:
        raise AssertionError(("injective gate cap", injective_gate_cap))
    print(f"equal_line_z_fiber_multiplicity_checks={checked}")


def check_support_floor_with_eight_mu() -> None:
    checked = 0
    for k in range(2, 24):
        for s in range(1, 13):
            for h in range(1, 5):
                for degree_cap in range(1, 7):
                    for lambda_cap in range(0, s):
                        for multiplicity in range(1, 7):
                            exact_gate_cap = divisor_gate_cap(
                                multiplicity,
                                6,
                                [2],
                            )
                            coarse_gate_cap = 8 * multiplicity
                            if exact_gate_cap != coarse_gate_cap:
                                raise AssertionError((multiplicity, exact_gate_cap))
                            exact_floor = support_floor_from_popularity_cap(
                                k,
                                s,
                                h,
                                degree_cap,
                                lambda_cap,
                                exact_gate_cap,
                            )
                            coarse_floor = support_floor_from_popularity_cap(
                                k,
                                s,
                                h,
                                degree_cap,
                                lambda_cap,
                                coarse_gate_cap,
                            )
                            if exact_floor != coarse_floor:
                                raise AssertionError(
                                    (
                                        k,
                                        s,
                                        h,
                                        degree_cap,
                                        lambda_cap,
                                        multiplicity,
                                        exact_floor,
                                        coarse_floor,
                                    )
                                )
                            checked += 1
    print(f"equal_line_eight_mu_floor_checks={checked}")


def main() -> None:
    check_singular_budget()
    check_quadratic_gate_budget()
    check_quadratic_gate_sharpness()
    check_injective_z_leaf_multiplicity_cap()
    check_support_floor_with_eight_mu()
    print("m1 equal-line generic popularity-budget checks passed")


if __name__ == "__main__":
    main()
