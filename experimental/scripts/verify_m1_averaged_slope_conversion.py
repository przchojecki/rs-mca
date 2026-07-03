#!/usr/bin/env python3
"""Small verifier for the averaged locator-to-slope conversion theorem.

The proof is algebraic/combinatorial; this script checks the two mechanical
pieces that are easy to regress:
  1. occupancy inequality: #occupied bins >= balls - same-bin ordered pairs / 2;
  2. the restricted-family same-slope correction formula used by the note.
"""

from __future__ import annotations

from fractions import Fraction
import itertools


def occupancy_ok() -> bool:
    for q in range(1, 7):
        for counts in itertools.product(range(5), repeat=q):
            occupied = sum(1 for value in counts if value > 0)
            balls = sum(counts)
            ordered_same = sum(value * (value - 1) for value in counts)
            if Fraction(occupied, 1) < Fraction(balls, 1) - Fraction(ordered_same, 2):
                return False
    return True


def p_fixed(q: int, t: int) -> Fraction:
    return Fraction(1, q**t) * (1 - Fraction(1, q**t))


def p_strict_pair(q: int, t: int, d: int) -> Fraction:
    alpha = Fraction(1, q ** (t + d))
    return alpha * (1 - 2 * Fraction(1, q**t) + alpha)


def conversion_lower_bound(
    q: int,
    t: int,
    M: int,
    deltas: dict[int, int],
) -> dict[str, Fraction]:
    pz = p_fixed(q, t)
    independent_ordered = M * (M - 1) - sum(deltas.values())
    c_t = Fraction(independent_ordered, 1) * pz * pz
    for d, count in deltas.items():
        c_t += count * p_strict_pair(q, t, d)
    mean_locators = q * M * pz
    lower = mean_locators - Fraction(q, 2) * c_t
    return {
        "p_z": pz,
        "mean_aligned_locators": mean_locators,
        "same_slope_collision_correction": c_t,
        "distinct_slope_expectation_lower_bound": lower,
    }


def formula_sanity_ok() -> bool:
    # t=1 has no strict high-overlap terms.
    out = conversion_lower_bound(q=17, t=1, M=10, deltas={})
    if out["distinct_slope_expectation_lower_bound"] <= 0:
        return False

    # Adding strict-overlap pairs must weaken, not strengthen, the conversion.
    base = conversion_lower_bound(q=17, t=3, M=200, deltas={})
    strict = conversion_lower_bound(q=17, t=3, M=200, deltas={1: 50, 2: 50})
    if strict["distinct_slope_expectation_lower_bound"] > base["distinct_slope_expectation_lower_bound"]:
        return False

    # Same-slope strict-pair probability obeys the q^(1-t-d) summed-slope scale.
    for q in (5, 17):
        for t in range(1, 5):
            for d in range(1, t):
                if q * p_strict_pair(q, t, d) > Fraction(1, q ** (t + d - 1)):
                    return False
    return True


def main() -> None:
    checks = {
        "occupancy inequality": occupancy_ok(),
        "conversion formula sanity": formula_sanity_ok(),
    }
    for name, ok in checks.items():
        print(f"  [{'OK ' if ok else 'FAIL'}] {name}")
    print("RESULT:", "PASS" if all(checks.values()) else "FAIL")
    raise SystemExit(0 if all(checks.values()) else 1)


if __name__ == "__main__":
    main()
