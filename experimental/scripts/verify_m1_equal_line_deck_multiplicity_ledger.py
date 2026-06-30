#!/usr/bin/env python3
"""Verify the equal-line deck multiplicity ledger."""

from __future__ import annotations

from verify_m1_equal_line_generic_popularity_budget import singular_support_y
from verify_m1_equal_line_split_fiber_containment import (
    fiber_discriminant,
    normalize_projective,
    projective_line,
    projective_split_fiber_roots,
    projective_y_point,
)
from verify_m1_high_overlap_graph_budget import support_floor_from_popularity_cap
from verify_m1_popularity_divisor_gate import divisor_gate_cap


PRIMES = (5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47)


def deck_sigma(z_point: tuple[int, int], p: int) -> tuple[int, int]:
    z_num, z_den = z_point
    return normalize_projective(z_num + z_den, 3 * z_num - z_den, p)


def branch_points(p: int) -> set[tuple[int, int]]:
    return {
        (1, 1),  # z=1 maps to y=infinity.
        ((-pow(3, -1, p)) % p, 1),  # z=-1/3 maps to y=3/4.
    }


def branch_values(p: int) -> set[tuple[int, int]]:
    return {
        (1, 0),  # y=infinity.
        normalize_projective(3, 4, p),  # y=3/4.
    }


def equal_line_z_popularity_cap(z_multiplicity: int) -> int:
    if z_multiplicity <= 0:
        raise ValueError("z_multiplicity must be positive")
    return divisor_gate_cap(2 * z_multiplicity, 6, [2])


def check_deck_identity() -> None:
    checked = 0
    fixed_seen: dict[int, set[tuple[int, int]]] = {}
    for p in PRIMES:
        fixed: set[tuple[int, int]] = set()
        for z_point in projective_line(p):
            sigma_z = deck_sigma(z_point, p)
            if projective_y_point(sigma_z, p) != projective_y_point(z_point, p):
                raise AssertionError(("deck identity", p, z_point, sigma_z))
            if deck_sigma(sigma_z, p) != z_point:
                raise AssertionError(("deck involution", p, z_point, sigma_z))
            if sigma_z == z_point:
                fixed.add(z_point)
            checked += 1

        if fixed != branch_points(p):
            raise AssertionError(("fixed points", p, fixed, branch_points(p)))
        if {projective_y_point(point, p) for point in fixed} != branch_values(p):
            raise AssertionError(("fixed branch values", p, fixed))
        fixed_seen[p] = fixed

    print(f"deck_identity_points_checked={checked}")
    print(f"deck_fixed_point_rows_checked={len(fixed_seen)}")


def check_branch_and_fiber_ledger() -> None:
    checked = 0
    split_pairs = 0
    nonsplit = 0
    branch = 0
    uncharged_split = 0
    for p in PRIMES:
        singular = singular_support_y(p)
        for y_point in projective_line(p):
            roots = projective_split_fiber_roots(y_point, p)
            discriminant = fiber_discriminant(y_point, p)
            if y_point in branch_values(p):
                if len(roots) != 1 or discriminant != 0:
                    raise AssertionError(("bad branch fiber", p, y_point, roots))
                if roots[0] not in branch_points(p):
                    raise AssertionError(("bad branch root", p, y_point, roots))
                branch += 1
            elif roots:
                if len(roots) != 2:
                    raise AssertionError(("bad split fiber size", p, y_point, roots))
                if deck_sigma(roots[0], p) != roots[1]:
                    raise AssertionError(("bad deck pair", p, y_point, roots))
                if deck_sigma(roots[1], p) != roots[0]:
                    raise AssertionError(("bad reverse deck pair", p, y_point, roots))
                split_pairs += 1
                if y_point not in singular:
                    uncharged_split += 1
            else:
                nonsplit += 1
            checked += 1

    if uncharged_split == 0:
        raise AssertionError("no uncharged split fiber witnessed")
    print(f"deck_fiber_rows_checked={checked}")
    print(f"deck_split_fibers_checked={split_pairs}")
    print(f"deck_nonsplit_fibers_checked={nonsplit}")
    print(f"deck_branch_fibers_checked={branch}")
    print(f"deck_uncharged_split_fibers_checked={uncharged_split}")


def check_multiplicity_transfer() -> None:
    checked = 0
    sharp = 0
    for p in PRIMES:
        singular = singular_support_y(p)
        uncharged_points = [
            z_point
            for z_point in projective_line(p)
            if projective_y_point(z_point, p) not in singular
        ]
        for z_multiplicity in range(1, 8):
            y_counts: dict[tuple[int, int], int] = {}
            z_counts: dict[tuple[int, int], int] = {}
            for z_point in uncharged_points:
                z_counts[z_point] = z_multiplicity
                y_point = projective_y_point(z_point, p)
                y_counts[y_point] = y_counts.get(y_point, 0) + z_multiplicity

            if any(count > z_multiplicity for count in z_counts.values()):
                raise AssertionError(("z cap broken", p, z_multiplicity))
            max_y_count = max(y_counts.values(), default=0)
            if max_y_count > 2 * z_multiplicity:
                raise AssertionError(
                    ("y multiplicity cap", p, z_multiplicity, max_y_count)
                )
            if max_y_count == 2 * z_multiplicity:
                sharp += 1
            checked += 1

    if sharp == 0:
        raise AssertionError("2nu multiplicity cap was not sharp in any row")
    print(f"deck_multiplicity_transfer_rows_checked={checked}")
    print(f"deck_multiplicity_sharp_rows={sharp}")


def check_support_floor_substitution() -> None:
    checked = 0
    strict = 0
    for k in range(2, 26):
        for s in range(1, 14):
            for h in range(1, 5):
                for degree_cap in range(1, 7):
                    for lambda_cap in range(0, s):
                        for z_multiplicity in range(1, 8):
                            cap_from_z = equal_line_z_popularity_cap(z_multiplicity)
                            expected_cap = 16 * z_multiplicity
                            if cap_from_z != expected_cap:
                                raise AssertionError(
                                    ("z popularity cap", z_multiplicity, cap_from_z)
                                )
                            floor_from_z = support_floor_from_popularity_cap(
                                k,
                                s,
                                h,
                                degree_cap,
                                lambda_cap,
                                cap_from_z,
                            )
                            floor_from_y = support_floor_from_popularity_cap(
                                k,
                                s,
                                h,
                                degree_cap,
                                lambda_cap,
                                8 * (2 * z_multiplicity),
                            )
                            if floor_from_z != floor_from_y:
                                raise AssertionError(
                                    (
                                        "floor substitution",
                                        k,
                                        s,
                                        h,
                                        degree_cap,
                                        lambda_cap,
                                        z_multiplicity,
                                        floor_from_z,
                                        floor_from_y,
                                    )
                                )
                            if z_multiplicity > 1:
                                stronger = support_floor_from_popularity_cap(
                                    k,
                                    s,
                                    h,
                                    degree_cap,
                                    lambda_cap,
                                    equal_line_z_popularity_cap(z_multiplicity - 1),
                                )
                                if stronger < floor_from_z:
                                    raise AssertionError(
                                        (
                                            "monotonicity",
                                            k,
                                            s,
                                            h,
                                            degree_cap,
                                            lambda_cap,
                                            z_multiplicity,
                                            stronger,
                                            floor_from_z,
                                        )
                                    )
                                if stronger > floor_from_z:
                                    strict += 1
                            checked += 1

    if strict == 0:
        raise AssertionError("z multiplicity tightening never improved a floor")
    print(f"deck_support_floor_substitutions_checked={checked}")
    print(f"deck_strict_floor_improvements={strict}")


def main() -> None:
    check_deck_identity()
    check_branch_and_fiber_ledger()
    check_multiplicity_transfer()
    check_support_floor_substitution()
    print("m1 equal-line deck multiplicity ledger checks passed")


if __name__ == "__main__":
    main()
