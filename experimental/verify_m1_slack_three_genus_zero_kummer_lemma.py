#!/usr/bin/env python3
"""Audit slack-three genus-zero Kummer constants on sample primes.

Proof status: AUDIT / EXPERIMENTAL.

The theorem note is geometric. This script checks the finite-field shadows
used by the note: conic smoothness, small divisor supports, and the character
sum bounds with constants 6 and 12 on representative subgroup indices.
"""

from __future__ import annotations

import cmath
import math
from itertools import product
from typing import Dict, List, Sequence, Tuple


Point = Tuple[int, int, int]


SAMPLES = (
    {"p": 17, "n": 8},
    {"p": 19, "n": 9},
    {"p": 31, "n": 15},
    {"p": 43, "n": 14},
)


def inv(value: int, p: int) -> int:
    return pow(value % p, p - 2, p)


def normalize(point: Point, p: int) -> Point:
    for entry in point:
        if entry % p:
            scale = inv(entry, p)
            return tuple((coordinate * scale) % p for coordinate in point)
    raise ValueError("zero projective point")


def projective_points(p: int) -> List[Point]:
    points = {
        normalize((u, v, z), p)
        for u in range(p)
        for v in range(p)
        for z in range(p)
        if (u, v, z) != (0, 0, 0)
    }
    return sorted(points)


def conic_value(point: Point, p: int) -> int:
    u, v, z = point
    return (u * u + v * v + u * v + u * z + v * z + z * z) % p


def conic_points(p: int) -> List[Point]:
    return [point for point in projective_points(p) if conic_value(point, p) == 0]


def w_coordinate(point: Point, p: int) -> int:
    u, v, z = point
    return (-u - v - z) % p


def beta_numerator(point: Point, p: int) -> int:
    u, v, z = point
    w = w_coordinate(point, p)
    return (pow(z, 3, p) + u * v * w) % p


def affine_conic_points(p: int) -> List[Tuple[int, int, int, int]]:
    rows: List[Tuple[int, int, int, int]] = []
    for u in range(p):
        for v in range(p):
            w = (-1 - u - v) % p
            q_value = (u * u + v * v + u * v + u + v + 1) % p
            if q_value == 0:
                beta = (-(1 + u * v * w)) % p
                rows.append((u, v, w, beta))
    return rows


def primitive_root(p: int) -> int:
    factors = prime_factors(p - 1)
    for candidate in range(2, p):
        if all(pow(candidate, (p - 1) // factor, p) != 1 for factor in factors):
            return candidate
    raise ValueError(f"no primitive root found for p={p}")


def prime_factors(value: int) -> List[int]:
    factors: List[int] = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1 if divisor == 2 else 2
    if value > 1:
        factors.append(value)
    return factors


def log_table(p: int) -> Dict[int, int]:
    root = primitive_root(p)
    return {pow(root, exponent, p): exponent for exponent in range(p - 1)}


def character(
    logs: Dict[int, int],
    value: int,
    order: int,
    power: int,
) -> complex:
    if value == 0:
        return 0j
    angle = 2.0 * math.pi * power * logs[value] / order
    return cmath.exp(1j * angle)


def audit_projective_geometry(p: int) -> Dict[str, object]:
    points = conic_points(p)
    sections: Dict[str, set[Point]] = {
        "U": {point for point in points if point[0] == 0},
        "V": {point for point in points if point[1] == 0},
        "W": {point for point in points if w_coordinate(point, p) == 0},
        "Z": {point for point in points if point[2] == 0},
    }
    beta_zero = {point for point in points if beta_numerator(point, p) == 0}
    pairwise_disjoint = all(
        not (left_points & right_points)
        for left_name, left_points in sections.items()
        for right_name, right_points in sections.items()
        if left_name < right_name
    )
    beta_disjoint = not beta_zero.intersection(
        set().union(*sections.values())
    )
    return {
        "p": p,
        "conic_points": len(points),
        "line_section_sizes": {
            name: len(section) for name, section in sections.items()
        },
        "line_sections_pairwise_disjoint": pairwise_disjoint,
        "beta_zero_size": len(beta_zero),
        "beta_zero_support_bound": len(beta_zero) <= 6,
        "beta_zero_disjoint_from_lines": beta_disjoint,
    }


def character_sum_bounds(p: int, n: int) -> Dict[str, object]:
    if (p - 1) % n != 0:
        raise ValueError("n must divide p-1")
    e = (p - 1) // n
    h = e * math.gcd(3, n)
    logs = log_table(p)
    affine_points = affine_conic_points(p)

    max_three = 0.0
    for a, b, c in product(range(e), repeat=3):
        if (a, b, c) == (0, 0, 0):
            continue
        total = sum(
            character(logs, u, e, a)
            * character(logs, v, e, b)
            * character(logs, w, e, c)
            for u, v, w, _ in affine_points
        )
        max_three = max(max_three, abs(total))

    max_four = 0.0
    for a, b, c in product(range(e), repeat=3):
        for d in range(h):
            if (a, b, c, d) == (0, 0, 0, 0):
                continue
            total = sum(
                character(logs, u, e, a)
                * character(logs, v, e, b)
                * character(logs, w, e, c)
                * character(logs, beta, h, d)
                for u, v, w, beta in affine_points
            )
            max_four = max(max_four, abs(total))

    return {
        "p": p,
        "n": n,
        "e": e,
        "h": h,
        "affine_conic_points": len(affine_points),
        "max_three_coordinate_sum": round(max_three, 10),
        "three_coordinate_bound": 6 * math.sqrt(p),
        "three_coordinate_bound_check": max_three <= 6 * math.sqrt(p) + 1e-8,
        "max_cube_coset_sum": round(max_four, 10),
        "cube_coset_bound": 12 * math.sqrt(p),
        "cube_coset_bound_check": max_four <= 12 * math.sqrt(p) + 1e-8,
    }


def verify_rows(rows: Sequence[Dict[str, object]]) -> None:
    for row in rows:
        assert row["line_sections_pairwise_disjoint"]
        assert row["beta_zero_support_bound"]
        assert row["beta_zero_disjoint_from_lines"]
        assert row["three_coordinate_bound_check"]
        assert row["cube_coset_bound_check"]


def merged_row(sample: Dict[str, int]) -> Dict[str, object]:
    p = sample["p"]
    return {
        **audit_projective_geometry(p),
        **character_sum_bounds(p, sample["n"]),
    }


def main() -> None:
    rows = [merged_row(sample) for sample in SAMPLES]
    verify_rows(rows)
    for row in rows:
        print(row)
    print("M1 slack-three genus-zero Kummer verifier passed")


if __name__ == "__main__":
    main()
