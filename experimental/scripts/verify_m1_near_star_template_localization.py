#!/usr/bin/env python3
"""Verify the M1 near-star template localization lemma."""

from __future__ import annotations

from itertools import combinations
import math
import random

Support = frozenset[int]


def endpoint_degrees(supports: set[Support]) -> dict[int, int]:
    degrees: dict[int, int] = {}
    for support in supports:
        if len(support) != 2:
            raise ValueError(f"support is not two-point: {support}")
        for endpoint in support:
            degrees[endpoint] = degrees.get(endpoint, 0) + 1
    return degrees


def prune_endpoint_stars(
    supports: set[Support], degree_cap: int
) -> tuple[set[Support], set[Support], set[int]]:
    if degree_cap < 0:
        raise ValueError("degree cap must be nonnegative")
    remaining = set(supports)
    charged: set[Support] = set()
    centers: set[int] = set()
    while remaining:
        degrees = endpoint_degrees(remaining)
        high = [point for point, degree in degrees.items() if degree > degree_cap]
        if not high:
            break
        center = max(high, key=lambda point: (degrees[point], -point))
        centers.add(center)
        incident = {support for support in remaining if center in support}
        if not incident:
            raise AssertionError((center, remaining, degrees))
        charged.update(incident)
        remaining.difference_update(incident)
    return charged, remaining, centers


def footprint(supports: set[Support]) -> set[int]:
    return {endpoint for support in supports for endpoint in support}


def near_star_footprint_cap(q: int, degree_cap: int, far_factor: int) -> int:
    if far_factor < 2:
        raise ValueError("far_factor must be at least 2")
    return min(q + 1, max(0, 2 * far_factor * degree_cap - 1))


def template_bound(
    q: int, degree_cap: int, far_factor: int, palette_classes: int
) -> int:
    cap = near_star_footprint_cap(q, degree_cap, far_factor)
    return sum(
        math.comb(q + 1, size) * (1 << (palette_classes * math.comb(size, 2)))
        for size in range(cap + 1)
    )


def coarse_template_bound(
    q: int, degree_cap: int, far_factor: int, palette_classes: int
) -> int:
    cap = near_star_footprint_cap(q, degree_cap, far_factor)
    return (cap + 1) * ((q + 1) ** cap) * (
        1 << (palette_classes * math.comb(cap, 2))
    )


def encode_template_count_for_footprint(footprint_size: int, palette_classes: int) -> int:
    return 1 << (palette_classes * math.comb(footprint_size, 2))


def random_support_family(rng: random.Random, q: int, size: int) -> set[Support]:
    endpoints = list(range(q + 1))
    all_supports = [frozenset(pair) for pair in combinations(endpoints, 2)]
    rng.shuffle(all_supports)
    return set(all_supports[: min(size, len(all_supports))])


def check_pruning_invariant() -> None:
    rng = random.Random(20260630)
    checked = 0
    for q in range(3, 24):
        max_supports = math.comb(q + 1, 2)
        for degree_cap in range(0, min(7, q + 1)):
            for _ in range(25):
                family = random_support_family(
                    rng, q, rng.randint(0, max_supports)
                )
                charged, residual, centers = prune_endpoint_stars(family, degree_cap)
                if charged & residual:
                    raise AssertionError((q, degree_cap, charged, residual))
                if charged | residual != family:
                    raise AssertionError((q, degree_cap, family, charged, residual))
                residual_degrees = endpoint_degrees(residual)
                if any(degree > degree_cap for degree in residual_degrees.values()):
                    raise AssertionError((q, degree_cap, residual_degrees, residual))
                for support in charged:
                    if support.isdisjoint(centers):
                        raise AssertionError((q, degree_cap, support, centers))
                checked += 1
    print(f"pruning_systems_checked={checked}")


def check_near_star_bounds() -> None:
    rng = random.Random(20260701)
    checked = 0
    for q in range(3, 35):
        max_supports = math.comb(q + 1, 2)
        for degree_cap in range(0, min(8, q + 1)):
            for far_factor in range(2, 7):
                cap = near_star_footprint_cap(q, degree_cap, far_factor)
                for _ in range(15):
                    family = random_support_family(
                        rng, q, rng.randint(0, max_supports)
                    )
                    _, residual, _ = prune_endpoint_stars(family, degree_cap)
                    residual_size = len(residual)
                    endpoints = footprint(residual)
                    if residual_size < far_factor * degree_cap:
                        if len(endpoints) > cap:
                            raise AssertionError(
                                (
                                    q,
                                    degree_cap,
                                    far_factor,
                                    residual_size,
                                    len(endpoints),
                                    cap,
                                )
                            )
                        if len(endpoints) > 2 * residual_size:
                            raise AssertionError((q, residual_size, endpoints))
                    checked += 1
    print(f"near_star_bounds_checked={checked}")


def check_template_counts() -> None:
    checked = 0
    for q in range(3, 35):
        for degree_cap in range(0, min(8, q + 1)):
            for far_factor in range(2, 7):
                cap = near_star_footprint_cap(q, degree_cap, far_factor)
                for palette_classes in range(1, 5):
                    exact = template_bound(
                        q, degree_cap, far_factor, palette_classes
                    )
                    coarse = coarse_template_bound(
                        q, degree_cap, far_factor, palette_classes
                    )
                    if exact > coarse:
                        raise AssertionError(
                            (q, degree_cap, far_factor, palette_classes, exact, coarse)
                        )
                    for footprint_size in range(cap + 1):
                        choices = (
                            math.comb(q + 1, footprint_size)
                            * encode_template_count_for_footprint(
                                footprint_size, palette_classes
                            )
                        )
                        if choices > exact:
                            raise AssertionError(
                                (
                                    q,
                                    degree_cap,
                                    far_factor,
                                    palette_classes,
                                    footprint_size,
                                    choices,
                                    exact,
                                )
                            )
                    checked += 1
    print(f"template_count_grids_checked={checked}")


def main() -> None:
    check_pruning_invariant()
    check_near_star_bounds()
    check_template_counts()
    print("m1 near-star template localization checks passed")


if __name__ == "__main__":
    main()
