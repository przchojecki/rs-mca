#!/usr/bin/env python3
"""Verify the equal-line packet-sift closure criterion.

The checks are finite arithmetic/combinatorics only.  They compose the
equal-line divisor-gate cap U <= 8 mu with the high-overlap popularity support
floor, and verify the exact rounding relation with the forced-edge form.
"""

from __future__ import annotations

from verify_m1_high_overlap_graph_budget import (
    degeneracy_bound_from_popularity_cap,
    forced_high_edges,
    max_edges_from_degeneracy_bound,
    support_floor_from_degeneracy_bound,
    support_floor_from_popularity_cap,
)
from verify_m1_popularity_divisor_gate import divisor_gate_cap


def equal_line_popularity_cap(multiplicity: int) -> int:
    """Return U_eq(mu)=mu(6+2) for the equal-line projective gate."""
    if multiplicity <= 0:
        raise ValueError("multiplicity must be positive")
    return divisor_gate_cap(multiplicity, 6, [2])


def equal_line_injective_z_cap() -> int:
    """Return the injective-z cap, using the degree-two z -> y map."""
    return divisor_gate_cap(2, 6, [2])


def support_floor_from_equal_line_cap(
    k: int,
    s: int,
    h: int,
    degree_cap: int,
    lambda_cap: int,
    multiplicity: int,
) -> int:
    return support_floor_from_popularity_cap(
        k,
        s,
        h,
        degree_cap,
        lambda_cap,
        equal_line_popularity_cap(multiplicity),
    )


def support_floor_from_injective_z_cap(
    k: int,
    s: int,
    h: int,
    degree_cap: int,
    lambda_cap: int,
) -> int:
    return support_floor_from_popularity_cap(
        k,
        s,
        h,
        degree_cap,
        lambda_cap,
        equal_line_injective_z_cap(),
    )


def check_equal_line_caps() -> None:
    checked = 0
    for multiplicity in range(1, 32):
        cap = equal_line_popularity_cap(multiplicity)
        if cap != 8 * multiplicity:
            raise AssertionError(("equal-line cap", multiplicity, cap))
        checked += 1

    injective_cap = equal_line_injective_z_cap()
    if injective_cap != 16:
        raise AssertionError(("injective-z cap", injective_cap))
    if injective_cap != equal_line_popularity_cap(2):
        raise AssertionError(("injective-z cap mismatch", injective_cap))

    print(f"equal_line_caps_checked={checked}")


def check_floor_substitution_grid() -> None:
    checked = 0
    injective_checked = 0
    for k in range(2, 28):
        for s in range(1, 16):
            for h in range(1, 6):
                for degree_cap in range(1, 8):
                    for lambda_cap in range(0, s):
                        for multiplicity in range(1, 8):
                            cap = equal_line_popularity_cap(multiplicity)
                            derived_degeneracy = (
                                degeneracy_bound_from_popularity_cap(
                                    s, h, degree_cap, lambda_cap, cap
                                )
                            )
                            floor_from_pop = support_floor_from_equal_line_cap(
                                k,
                                s,
                                h,
                                degree_cap,
                                lambda_cap,
                                multiplicity,
                            )
                            floor_from_degen = support_floor_from_degeneracy_bound(
                                k,
                                s,
                                h,
                                degree_cap,
                                lambda_cap,
                                derived_degeneracy,
                            )
                            if floor_from_pop != floor_from_degen:
                                raise AssertionError(
                                    (
                                        "floor substitution",
                                        k,
                                        s,
                                        h,
                                        degree_cap,
                                        lambda_cap,
                                        multiplicity,
                                        floor_from_pop,
                                        floor_from_degen,
                                    )
                                )

                            if multiplicity > 1:
                                weaker = support_floor_from_equal_line_cap(
                                    k,
                                    s,
                                    h,
                                    degree_cap,
                                    lambda_cap,
                                    multiplicity,
                                )
                                stronger = support_floor_from_equal_line_cap(
                                    k,
                                    s,
                                    h,
                                    degree_cap,
                                    lambda_cap,
                                    multiplicity - 1,
                                )
                                if stronger < weaker:
                                    raise AssertionError(
                                        (
                                            "monotonicity",
                                            k,
                                            s,
                                            h,
                                            degree_cap,
                                            lambda_cap,
                                            multiplicity,
                                            stronger,
                                            weaker,
                                        )
                                    )
                            checked += 1

                        injective_floor = support_floor_from_injective_z_cap(
                            k, s, h, degree_cap, lambda_cap
                        )
                        mu_two_floor = support_floor_from_equal_line_cap(
                            k, s, h, degree_cap, lambda_cap, 2
                        )
                        if injective_floor != mu_two_floor:
                            raise AssertionError(
                                (
                                    "injective floor",
                                    k,
                                    s,
                                    h,
                                    degree_cap,
                                    lambda_cap,
                                    injective_floor,
                                    mu_two_floor,
                                )
                            )
                        injective_checked += 1

    print(f"equal_line_floor_substitutions_checked={checked}")
    print(f"injective_z_floor_substitutions_checked={injective_checked}")


def check_forced_edge_equivalence_grid() -> None:
    checked = 0
    active = 0
    for k in range(2, 16):
        for s in range(1, 10):
            for h in range(1, 5):
                for degree_cap in range(1, 6):
                    for lambda_cap in range(0, s):
                        for multiplicity in range(1, 5):
                            cap = equal_line_popularity_cap(multiplicity)
                            degen = degeneracy_bound_from_popularity_cap(
                                s, h, degree_cap, lambda_cap, cap
                            )
                            edge_ceiling = max_edges_from_degeneracy_bound(k, degen)
                            floor = support_floor_from_equal_line_cap(
                                k,
                                s,
                                h,
                                degree_cap,
                                lambda_cap,
                                multiplicity,
                            )

                            support_budgets = {
                                1,
                                max(1, floor - 1),
                                floor,
                                max(1, k * s // 3),
                                max(1, k * s // 2),
                                k * s,
                            }
                            for support_budget in sorted(support_budgets):
                                if support_budget <= 0:
                                    continue
                                forced = forced_high_edges(
                                    k,
                                    s,
                                    support_budget,
                                    h,
                                    degree_cap,
                                    lambda_cap,
                                )
                                impossible_by_floor = floor > support_budget
                                impossible_by_edges = forced > edge_ceiling
                                if impossible_by_floor != impossible_by_edges:
                                    raise AssertionError(
                                        (
                                            "forced-edge equivalence",
                                            k,
                                            s,
                                            h,
                                            degree_cap,
                                            lambda_cap,
                                            multiplicity,
                                            support_budget,
                                            floor,
                                            forced,
                                            edge_ceiling,
                                        )
                                    )
                                if impossible_by_floor:
                                    active += 1
                                checked += 1

    if active == 0:
        raise AssertionError("closure criterion never became active")
    print(f"forced_edge_equivalence_checks={checked}")
    print(f"active_equal_line_closure_rows={active}")


def check_injective_z_is_stronger_than_large_multiplicity() -> None:
    checked = 0
    strict = 0
    for k in range(2, 24):
        for s in range(1, 13):
            for h in range(1, 5):
                for degree_cap in range(1, 7):
                    for lambda_cap in range(0, s):
                        injective_floor = support_floor_from_injective_z_cap(
                            k, s, h, degree_cap, lambda_cap
                        )
                        for multiplicity in range(3, 9):
                            coarse_floor = support_floor_from_equal_line_cap(
                                k,
                                s,
                                h,
                                degree_cap,
                                lambda_cap,
                                multiplicity,
                            )
                            if injective_floor < coarse_floor:
                                raise AssertionError(
                                    (
                                        "injective cap not stronger",
                                        k,
                                        s,
                                        h,
                                        degree_cap,
                                        lambda_cap,
                                        multiplicity,
                                        injective_floor,
                                        coarse_floor,
                                    )
                                )
                            if injective_floor > coarse_floor:
                                strict += 1
                            checked += 1

    if strict == 0:
        raise AssertionError("injective-z cap never sharpened the floor")
    print(f"injective_z_strength_checks={checked}")
    print(f"strict_injective_z_improvements={strict}")


def main() -> None:
    check_equal_line_caps()
    check_floor_substitution_grid()
    check_forced_edge_equivalence_grid()
    check_injective_z_is_stronger_than_large_multiplicity()
    print("m1 equal-line packet-sift closure checks passed")


if __name__ == "__main__":
    main()
