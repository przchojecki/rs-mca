#!/usr/bin/env python3
"""Verify the M1 depth-two two-coordinate fiber reduction."""

from __future__ import annotations

import cmath
import math
from itertools import product
from typing import Dict, List, Tuple


SAMPLES = (
    {"p": 17, "n": 8},
    {"p": 31, "n": 10},
    {"p": 37, "n": 9},
    {"p": 43, "n": 14},
    {"p": 61, "n": 20},
)


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


def primitive_root(p: int) -> int:
    factors = prime_factors(p - 1)
    for candidate in range(2, p):
        if all(pow(candidate, (p - 1) // factor, p) != 1 for factor in factors):
            return candidate
    raise ValueError(f"no primitive root found for p={p}")


def log_table(p: int) -> Dict[int, int]:
    root = primitive_root(p)
    return {pow(root, exponent, p): exponent for exponent in range(p - 1)}


def character_table(p: int, order: int, logs: Dict[int, int]) -> List[List[complex]]:
    table: List[List[complex]] = []
    for exponent in range(order):
        row = [0j]
        for value in range(1, p):
            angle = 2.0 * math.pi * exponent * logs[value] / order
            row.append(cmath.exp(1j * angle))
        table.append(row)
    return table


def shape_a(u: int, v: int, p: int) -> int:
    return (-(u * u + v * v + u * v + u + v + 1)) % p


def delta(value: int, p: int) -> int:
    return (-3 * value * value - 2 * value - 3) % p


def b_collision(value: int, p: int) -> int:
    return (value * value + value + 1) % p


def coordinates(u: int, v: int, p: int) -> Tuple[int, int, int]:
    return u % p, v % p, (-1 - u - v) % p


def point_from_active(
    active_index: int,
    fixed_value: int,
    free_value: int,
    p: int,
) -> Tuple[int, int, int]:
    if active_index == 0:
        return coordinates(fixed_value, free_value, p)
    if active_index == 1:
        return coordinates(free_value, fixed_value, p)
    u = free_value
    v = (-1 - u - fixed_value) % p
    return coordinates(u, v, p)


def point_on_inactive_line(
    inactive_index: int,
    parameter: int,
    p: int,
) -> Tuple[int, int, int]:
    if inactive_index == 0:
        return coordinates(0, parameter, p)
    if inactive_index == 1:
        return coordinates(parameter, 0, p)
    return coordinates(parameter, (-1 - parameter) % p, p)


def direct_sum(
    p: int,
    coord_chars: Tuple[List[complex], List[complex], List[complex]],
    conic_char: List[complex],
) -> complex:
    total = 0j
    for u in range(p):
        for v in range(p):
            x, y, z = coordinates(u, v, p)
            total += (
                coord_chars[0][x]
                * coord_chars[1][y]
                * coord_chars[2][z]
                * conic_char[shape_a(u, v, p)]
            )
    return total


def fiber_core_sum(
    p: int,
    active_pair: Tuple[int, int],
    coord_chars: Tuple[List[complex], List[complex], List[complex]],
    conic_char: List[complex],
) -> complex:
    fixed_index, free_index = active_pair
    total = 0j
    for fixed_value in range(p):
        outer = coord_chars[fixed_index][fixed_value]
        if outer == 0j:
            continue
        inner = 0j
        for free_value in range(p):
            triple = point_from_active(fixed_index, fixed_value, free_value, p)
            u, v, _ = triple
            inner += (
                coord_chars[free_index][triple[free_index]]
                * conic_char[shape_a(u, v, p)]
            )
        total += outer * inner
    return total


def inactive_line_sum(
    p: int,
    inactive_index: int,
    coord_chars: Tuple[List[complex], List[complex], List[complex]],
    conic_char: List[complex],
) -> complex:
    total = 0j
    for parameter in range(p):
        triple = point_on_inactive_line(inactive_index, parameter, p)
        u, v, _ = triple
        value = conic_char[shape_a(u, v, p)]
        for index in range(3):
            if index != inactive_index:
                value *= coord_chars[index][triple[index]]
        total += value
    return total


def category(e: int, h: int, exponents: Tuple[int, int, int, int]) -> str:
    a, b, c, d = exponents
    active_coordinates = sum(exponent % e != 0 for exponent in (a, b, c))
    if d % h == 0:
        return "not_mixed"
    if active_coordinates == 2:
        return "two_coordinate"
    return "other"


def bad_parameter_summary(p: int) -> Dict[str, object]:
    if p <= 3:
        raise AssertionError(p)
    delta_roots = [value for value in range(p) if delta(value, p) == 0]
    collision_roots = [
        value for value in range(p) if b_collision(value, p) == 0
    ]
    if (-3) % p == 0:
        raise AssertionError((p, "outer meets discriminant"))
    if b_collision(0, p) == 0:
        raise AssertionError((p, "outer meets collision"))
    if set(delta_roots) & set(collision_roots):
        raise AssertionError((p, delta_roots, collision_roots))
    if (-3) % p == 0 or (-32) % p == 0:
        raise AssertionError((p, "inseparable"))
    return {
        "delta_root_count": len(delta_roots),
        "collision_root_count": len(collision_roots),
        "geometric_bad_parameter_bound": 6,
    }


def audit_sample(p: int, n: int) -> Dict[str, object]:
    if (p - 1) % n != 0:
        raise ValueError("n must divide p-1")
    e = (p - 1) // n
    h = e * math.gcd(2, n)
    logs = log_table(p)
    char_e = character_table(p, e, logs)
    char_h = character_table(p, h, logs)
    max_open_ratio = 0.0
    max_core_ratio = 0.0
    max_line_ratio = 0.0
    max_tuple = None
    checked = 0

    for exponents in product(range(e), range(e), range(e), range(h)):
        if category(e, h, exponents) != "two_coordinate":
            continue
        a, b, c, d = exponents
        coord_chars = (char_e[a], char_e[b], char_e[c])
        conic_char = char_h[d]
        active_pair = tuple(
            index for index, exponent in enumerate((a, b, c)) if exponent % e
        )
        inactive_index = next(
            index for index, exponent in enumerate((a, b, c)) if exponent % e == 0
        )
        opened = direct_sum(p, coord_chars, conic_char)
        core = fiber_core_sum(p, active_pair, coord_chars, conic_char)
        line = inactive_line_sum(p, inactive_index, coord_chars, conic_char)
        if abs(opened - (core - line)) > 1e-8:
            raise AssertionError((p, n, exponents, opened, core, line))
        if abs(line) > 3 * math.sqrt(p) + 1e-8:
            raise AssertionError((p, n, exponents, "line", line))
        checked += 1
        if abs(opened) > max_open_ratio * p:
            max_tuple = exponents
        max_open_ratio = max(max_open_ratio, abs(opened) / p)
        max_core_ratio = max(max_core_ratio, abs(core) / p)
        max_line_ratio = max(max_line_ratio, abs(line) / math.sqrt(p))

    return {
        "p": p,
        "n": n,
        "e": e,
        "h": h,
        "checked": checked,
        **bad_parameter_summary(p),
        "max_open_ratio_to_p": round(max_open_ratio, 10),
        "max_core_ratio_to_p": round(max_core_ratio, 10),
        "max_line_ratio_to_sqrt_p": round(max_line_ratio, 10),
        "max_tuple": max_tuple,
    }


def main() -> None:
    rows = [audit_sample(sample["p"], sample["n"]) for sample in SAMPLES]
    for row in rows:
        print(row)
    print("M1 depth-two two-coordinate fiber verifier passed")


if __name__ == "__main__":
    main()
