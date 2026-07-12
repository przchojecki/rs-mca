#!/usr/bin/env python3
"""Finite checks for the owner-rooted gate and rooted-localization lemmas.

This script does not certify the source-algebraic inverse theorem.  It checks:
  * the exact nonconverse family for Y_A versus R_A;
  * Y_A <= (L rho)^q / L;
  * the positive-support projected-energy lemma on finite cyclic groups.
"""

from __future__ import annotations

import argparse
import cmath
import math
from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable, Sequence


def exact_gate_family(H: int, W: int, q: int) -> dict[str, Fraction]:
    if not (1 <= W < H and q >= 2):
        raise ValueError("require 1 <= W < H and q >= 2")
    rho = Fraction(W, H)
    delta = Fraction(H - 1, H)
    e = rho * (1 - rho)
    x = Fraction(W * (H - 1), H)
    Y = e * x ** (q - 2)
    norm_q_q = W * (1 - rho) ** q + (H - W) * rho**q
    R_q = norm_q_q / H
    upper = Fraction((H * W // H) ** q, H)  # W^q/H = (L rho)^q/L
    return {
        "rho": rho,
        "delta": delta,
        "e": e,
        "x": x,
        "Y": Y,
        "R_q": R_q,
        "upper": upper,
    }


def dft(values: Sequence[complex]) -> list[complex]:
    H = len(values)
    return [
        sum(values[s] * cmath.exp(-2j * math.pi * k * s / H) for s in range(H))
        for k in range(H)
    ]


def idft(values: Sequence[complex]) -> list[complex]:
    H = len(values)
    return [
        sum(values[k] * cmath.exp(2j * math.pi * k * s / H) for k in range(H)) / H
        for s in range(H)
    ]


def project(values: Sequence[complex], band: set[int]) -> list[complex]:
    hat = dft(values)
    return idft([hat[k] if k in band else 0j for k in range(len(values))])


def lp(values: Iterable[complex], p: float) -> float:
    return sum(abs(x) ** p for x in values) ** (1.0 / p)


@dataclass(frozen=True)
class RootedCheck:
    norm_q: float
    positive_mass: float
    rooted_energy: float
    rooted_norm_q: float
    positive_support_count: int


def check_rooted_localization(
    multiplicities: Sequence[int], band: set[int], q: int
) -> RootedCheck:
    H = len(multiplicities)
    if q < 2:
        raise ValueError("q must be at least 2")
    f = [complex(x) for x in multiplicities]
    h = project(f, band)
    norm_q = lp(h, q)
    if norm_q == 0:
        raise ValueError("choose a nonzero projected example")

    g = [
        (x * abs(x) ** (q - 2) / norm_q ** (q - 1)) if x else 0j
        for x in h
    ]
    pg = project(g, band)

    positive_sites: list[int] = []
    positive_mass = 0.0
    for s, mult in enumerate(multiplicities):
        w = pg[s].conjugate().real
        if w > 0 and mult > 0:
            positive_sites.append(s)
            positive_mass += mult * w

    b = [0j] * H
    for s in positive_sites:
        b[s] = complex(multiplicities[s])
    pb = project(b, band)
    rooted_energy = sum(abs(x) ** 2 for x in pb)
    rooted_norm_q = lp(pb, q)
    n_plus = sum(multiplicities[s] for s in positive_sites)

    tol = 2e-9
    if positive_mass + tol < norm_q:
        raise AssertionError((positive_mass, norm_q))
    if rooted_norm_q + tol < positive_mass:
        raise AssertionError((rooted_norm_q, positive_mass))
    if rooted_energy + tol < positive_mass**2:
        raise AssertionError((rooted_energy, positive_mass**2))
    if n_plus + tol < positive_mass:
        raise AssertionError((n_plus, positive_mass))

    return RootedCheck(norm_q, positive_mass, rooted_energy, rooted_norm_q, n_plus)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="run the regression")
    parser.add_argument("--H", type=int, default=65536)
    parser.add_argument("--W", type=int, default=4096)
    parser.add_argument("--q", type=int, default=16)
    args = parser.parse_args()

    data = exact_gate_family(args.H, args.W, args.q)
    if data["Y"] > data["upper"]:
        raise AssertionError("universal load upper bound failed")

    N = math.log(args.H, 2)
    logY_rate = math.log(float(data["Y"])) / (N * args.q)
    logR_rate = math.log(float(data["R_q"])) / args.q / N

    # A finite rooted example on Z/13Z with a symmetric nonzero band.
    multiplicities = [2, 0, 1, 3, 0, 1, 0, 2, 1, 0, 0, 1, 0]
    band = {1, 2, 11, 12}
    rooted = check_rooted_localization(multiplicities, band, q=6)

    print("PASS")
    print(f"gate family: H={args.H}, W={args.W}, q={args.q}")
    print(f"  log(Y)/(N q) = {logY_rate:.9f}")
    print(f"  log(R)/N     = {logR_rate:.9f}")
    print("rooted localization:")
    print(f"  ||P_A f||_q       = {rooted.norm_q:.12f}")
    print(f"  positive mass     = {rooted.positive_mass:.12f}")
    print(f"  rooted energy     = {rooted.rooted_energy:.12f}")
    print(f"  ||P_A b||_q       = {rooted.rooted_norm_q:.12f}")
    print(f"  positive supports = {rooted.positive_support_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
