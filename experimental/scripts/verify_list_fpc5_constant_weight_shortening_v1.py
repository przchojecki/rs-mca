#!/usr/bin/env python3
"""Exact replay of FPC5 GRS support-shortening prefix payments."""

from functools import lru_cache
from math import comb, isqrt


FIELD_CAP = (1 << 256) - 1
BUDGET_CAP = FIELD_CAP >> 128
G8 = 195112047344632914122867933361797765038
G16 = 2444555448501019158442942184801171570


def pf6_values(rate_den: int, scale: int, touched: int) -> list[int]:
    code_length = 8192 // rate_den
    core = code_length - 1
    ell, background = divmod((rate_den - 1) * code_length + 1, scale)
    support = touched * ell
    if support > core:
        return []
    lower = max(
        (support + 1) // 2,
        core - isqrt(core * (core - support)),
    )
    upper = min(
        ell * (scale - 2) - 1,
        core,
        (touched - 1) * ell + background,
        (core + (touched - 2) * ell + background) // 2,
    )
    values = []
    for defect in range(lower, upper + 1):
        u = defect - (touched - 1) * ell
        rank = 2 * defect - support
        joint = (
            background * defect * defect
            + core * u * u
            - core * background * rank
        )
        if u < 0 or background == 0 or joint <= 0:
            values.append(defect)
    return values


@lru_cache(maxsize=None)
def support_cap(length: int, weight: int, half_distance: int) -> tuple[int, int]:
    choose_length = 1
    choose_weight = 1
    best = comb(length, weight)
    best_depth = -1
    for depth in range(weight + 1):
        residual = weight - depth
        if residual < half_distance:
            base = 1
        else:
            delta = residual**2 - (length - depth) * (
                residual - half_distance
            )
            base = None if delta <= 0 else (length - depth) * half_distance // delta
        if base is not None:
            value = choose_length * base // choose_weight
            if value < best:
                best = value
                best_depth = depth
        if depth < weight:
            choose_length = choose_length * (length - depth) // (depth + 1)
            choose_weight = choose_weight * (weight - depth) // (depth + 1)
    return best, best_depth


def scale_bound(rate_den: int, scale: int) -> tuple[int, int, int, int]:
    code_length = 8192 // rate_den
    core = code_length - 1
    ell, background = divmod((rate_den - 1) * code_length + 1, scale)
    total = 0
    cells = 0
    groups = 0
    max_depth = -1
    for touched in range(2, min(scale, core // ell) + 1):
        subtotal = 0
        touched_cells = 0
        for defect in pf6_values(rate_den, scale, touched):
            u = defect - (touched - 1) * ell
            endpoint = touched * ell if u < 0 else defect + ell
            half_distance = endpoint - defect
            weight = min(defect, core - defect)
            cap, depth = support_cap(core, weight, half_distance)
            charts = 1 if u < 0 else comb(background, u)
            subtotal += charts * cap
            touched_cells += 1
            max_depth = max(max_depth, depth)
        if touched_cells:
            total += comb(scale, touched) * subtotal + scale
            cells += touched_cells
            groups += 1
    return total, cells, groups, max_depth


def main() -> None:
    # Fixed-shell controls from the M=61 strip.
    fixed = {
        248: (248, 127, 5402, 4),
        286: (225, 125, 10127, 4),
        287: (224, 125, 7396, 4),
        288: (223, 125, 5492, 3),
        289: (222, 125, 3723, 3),
        290: (221, 125, 2815, 3),
        291: (220, 125, 1839, 2),
        292: (219, 125, 1326, 2),
    }
    for _, (weight, half_distance, cap, depth) in fixed.items():
        assert support_cap(511, weight, half_distance) == (cap, depth)

    rate8_expected = {
        29: (4793233238066871893, 15, 1, 33),
        30: (483810874255402991308789535730933830, 45, 1, 66),
        31: (111332932893833073856127095996053091, 29, 1, 74),
        32: (194516903537483678052909783492003906224, 37, 2, 83),
    }
    rate16_expected = {
        57: (3871863946578677337, 19, 1, 0),
        58: (24757430395658, 10, 1, 0),
        59: (2703448499, 4, 1, 0),
        60: (0, 0, 0, -1),
        61: (334987461798250428400052701, 57, 1, 12),
        62: (82470208696933977090196158582, 60, 1, 20),
        63: (207434451093350429620973641722018, 84, 2, 27),
        64: (19639002661049920, 8, 1, 26),
        65: (4718328623028221554145, 20, 1, 35),
        66: (24995796851126083360635766146, 35, 1, 44),
        67: (2444347906248928075934859594332346564, 77, 2, 51),
    }
    for source_scale, expected in rate8_expected.items():
        assert scale_bound(8, source_scale) == expected
    for source_scale, expected in rate16_expected.items():
        assert scale_bound(16, source_scale) == expected

    assert sum(row[0] for row in rate8_expected.values()) == G8
    assert sum(row[1] for row in rate8_expected.values()) == 126
    assert sum(row[0] for row in rate16_expected.values()) == G16
    assert sum(row[1] for row in rate16_expected.values()) == 374
    assert (G8 << 128) < (1 << 256)
    assert (G8 << 128).bit_length() == 256
    assert (G16 << 128).bit_length() == 249

    blocked = ((2, 5, 611), (4, 13, 170), (8, 33, 155), (16, 68, 151))
    for rate_den, source_scale, bits in blocked:
        value, cells, _, _ = scale_bound(rate_den, source_scale)
        assert cells > 0
        assert value.bit_length() == bits
        assert value > BUDGET_CAP

    print(
        "PASS: FPC5 GRS constant-weight shortening "
        "fixed_shells=8 rate8_cells=126 rate16_cells=374 blocked_scales=4"
    )


if __name__ == "__main__":
    main()
