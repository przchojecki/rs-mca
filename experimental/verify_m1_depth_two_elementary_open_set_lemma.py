#!/usr/bin/env python3
"""Audit the M1 depth-two elementary open-set correction.

Proof status: AUDIT / EXPERIMENTAL.

The lemma is a short algebraic argument. This verifier checks its finite-field
shadows on representative primes: the Jacobi conic correction, the coordinate
line correction for conic-only terms, and the line-restriction identities for
A(u,v).
"""

from __future__ import annotations

import math
from itertools import product
from typing import Dict, List, Tuple

from verify_m1_depth_two_kummer_constant_audit import (
    character_table,
    log_table,
    shape_a,
)


SAMPLES = (
    {"p": 17, "n": 8},
    {"p": 31, "n": 10},
    {"p": 37, "n": 9},
    {"p": 43, "n": 14},
    {"p": 61, "n": 20},
)


def ceil_sqrt(value: int) -> int:
    root = math.isqrt(value)
    if root * root < value:
        root += 1
    return root


def w_value(u: int, v: int, p: int) -> int:
    return (-1 - u - v) % p


def coordinate_line_points(p: int) -> set[Tuple[int, int]]:
    points = set()
    for value in range(p):
        points.add((0, value))
        points.add((value, 0))
        points.add((value, (-1 - value) % p))
    return points


def verify_line_restrictions(p: int) -> None:
    for t in range(p):
        model = (-(t * t + t + 1)) % p
        if shape_a(0, t, p) != model:
            raise AssertionError((p, "u=0", t))
        if shape_a(t, 0, p) != model:
            raise AssertionError((p, "v=0", t))
        if shape_a(t, (-1 - t) % p, p) != model:
            raise AssertionError((p, "w=0", t))

    pair_intersections = ((0, 0), (0, p - 1), (p - 1, 0))
    for point in pair_intersections:
        if shape_a(*point, p) != p - 1:
            raise AssertionError((p, "pair", point, shape_a(*point, p)))


def conic_points(p: int) -> List[Tuple[int, int]]:
    return [
        (u, v)
        for u in range(p)
        for v in range(p)
        if shape_a(u, v, p) == 0
    ]


def audit_sample(p: int, n: int) -> Dict[str, object]:
    if (p - 1) % n != 0:
        raise ValueError("n must divide p-1")
    verify_line_restrictions(p)
    e = (p - 1) // n
    h = e * math.gcd(2, n)
    logs = log_table(p)
    char_e = character_table(p, e, logs)
    char_h = character_table(p, h, logs)
    conic = conic_points(p)
    line_union = coordinate_line_points(p)

    max_jacobi_conic_correction = 0.0
    max_jacobi_tuple = None
    for a, b, c in product(range(e), repeat=3):
        if (a, b, c) == (0, 0, 0):
            continue
        total = sum(
            char_e[a][u] * char_e[b][v] * char_e[c][w_value(u, v, p)]
            for u, v in conic
        )
        magnitude = abs(total)
        if magnitude > max_jacobi_conic_correction:
            max_jacobi_conic_correction = magnitude
            max_jacobi_tuple = (a, b, c)

    max_line_correction = 0.0
    max_line_exponent = None
    for d in range(1, h):
        total = sum(char_h[d][shape_a(u, v, p)] for u, v in line_union)
        magnitude = abs(total)
        if magnitude > max_line_correction:
            max_line_correction = magnitude
            max_line_exponent = d

    bound = 6 * ceil_sqrt(p)
    if max_jacobi_conic_correction > bound + 1e-8:
        raise AssertionError((p, n, "jacobi", max_jacobi_tuple))
    if max_line_correction > bound + 1e-8:
        raise AssertionError((p, n, "line", max_line_exponent))

    return {
        "p": p,
        "n": n,
        "e": e,
        "h": h,
        "conic_point_count": len(conic),
        "coordinate_line_union_count": len(line_union),
        "bound": bound,
        "max_jacobi_conic_correction": round(
            max_jacobi_conic_correction,
            10,
        ),
        "max_jacobi_tuple": max_jacobi_tuple,
        "max_conic_only_line_correction": round(max_line_correction, 10),
        "max_line_exponent": max_line_exponent,
    }


def main() -> None:
    rows = [audit_sample(sample["p"], sample["n"]) for sample in SAMPLES]
    for row in rows:
        print(row)
    print("M1 depth-two elementary open-set verifier passed")


if __name__ == "__main__":
    main()
