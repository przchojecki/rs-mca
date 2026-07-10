#!/usr/bin/env python3
"""Arithmetic checker for the h=2 HBK conditional compiler."""

from __future__ import annotations

from decimal import Decimal, getcontext
from fractions import Fraction


def energy_constant(k: Fraction) -> Fraction:
    return Fraction(1, 1) + 5 * (k * k + k)


def h_floor_threshold(k: Fraction) -> Fraction:
    c = energy_constant(k)
    return (c / 8) ** 2


def main() -> None:
    getcontext().prec = 80
    two = Decimal(2)
    geom = Decimal(1) / (Decimal(1) - (Decimal(1) / two) ** (Decimal(1) / Decimal(3)))
    if not geom < Decimal(5):
        raise AssertionError(geom)

    print(f"dyadic geometric constant < 5: {geom}")
    print("conditional constants:")
    for k in (
        Fraction(1),
        Fraction(2),
        Fraction(4),
        Fraction(8),
        Fraction(16),
        Fraction(66),
        Fraction(129),
    ):
        c_energy = energy_constant(k)
        h0 = h_floor_threshold(k)
        print(
            f"  K={k}: E(H) <= {c_energy} h^2.5; "
            f"T2<n^3 once h > {h0}"
        )

    # The exact algebraic identity used by the compiler:
    # if sum r_i^2 <= 5(K^2+K) h^1.5, then
    # E = h^2 + h sum r_i^2 <= (1+5(K^2+K))h^2.5 for h>=1.
    for k in (Fraction(1), Fraction(7, 3), Fraction(10)):
        c_l2 = 5 * (k * k + k)
        c_energy = energy_constant(k)
        if c_energy != 1 + c_l2:
            raise AssertionError((k, c_energy, c_l2))
    print("H2_HBK_CONDITIONAL_COMPILER_PASS")


if __name__ == "__main__":
    main()
