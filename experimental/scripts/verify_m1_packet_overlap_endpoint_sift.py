#!/usr/bin/env python3
"""Verify the M1 packet-overlap endpoint-sift lemma.

The checks are finite combinatorics only. They verify the Cauchy packet-overlap
burden, the pair-cap support floors, and the endpoint-star sift which forces
any excess overlap onto disjoint-support packet pairs.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
import random


def ceil_fraction(x: Fraction) -> int:
    return -(-x.numerator // x.denominator)


def ceil_positive(x: Fraction) -> int:
    return max(0, ceil_fraction(x))


def comb2(k: int) -> int:
    return k * (k - 1) // 2


def pair_overlap_mass_lower(k: int, s: int, support_budget: int) -> Fraction:
    if support_budget <= 0:
        raise ValueError("support budget must be positive")
    return Fraction(k * s * (k * s - support_budget), 2 * support_budget)


def forced_pair_overlap(k: int, s: int, support_budget: int) -> int:
    if k < 2:
        return 0
    raw = Fraction(s * (k * s - support_budget), support_budget * (k - 1))
    return ceil_positive(raw)


def support_floor_from_pair_cap(k: int, s: int, pair_cap: int) -> int:
    if k == 0:
        return 0
    denominator = s + (k - 1) * pair_cap
    if denominator <= 0:
        raise ValueError("nonpositive pair-cap denominator")
    return ceil_fraction(Fraction(k * s * s, denominator))


def endpoint_overlap_mass_bound(k: int, h: int, degree_cap: int, s: int) -> int:
    return k * h * max(0, degree_cap - 1) * s


def disjoint_overlap_mass_lower(
    k: int, s: int, support_budget: int, h: int, degree_cap: int
) -> Fraction:
    return pair_overlap_mass_lower(k, s, support_budget) - endpoint_overlap_mass_bound(
        k, h, degree_cap, s
    )


def forced_disjoint_overlap(
    k: int, s: int, support_budget: int, h: int, degree_cap: int
) -> int:
    if k < 2:
        return 0
    raw = disjoint_overlap_mass_lower(k, s, support_budget, h, degree_cap)
    return ceil_positive(raw / comb2(k))


def support_floor_from_disjoint_pair_cap(
    k: int, s: int, h: int, degree_cap: int, disjoint_pair_cap: int
) -> int:
    if k == 0:
        return 0
    denominator = k * s
    denominator += 2 * endpoint_overlap_mass_bound(k, h, degree_cap, s)
    denominator += k * (k - 1) * disjoint_pair_cap
    if denominator <= 0:
        raise ValueError("nonpositive star-sifted denominator")
    return ceil_fraction(Fraction(k * k * s * s, denominator))


@dataclass(frozen=True)
class Label:
    endpoints: frozenset[int]
    packet: frozenset[int]


def actual_stats(labels: list[Label]) -> dict[str, int]:
    union: set[int] = set()
    for label in labels:
        union.update(label.packet)

    total_pair_overlap = 0
    max_pair_overlap = 0
    endpoint_sharing_pairs = 0
    endpoint_overlap_mass = 0
    disjoint_overlap_mass = 0
    max_disjoint_overlap = 0

    for left, right in combinations(labels, 2):
        overlap = len(left.packet & right.packet)
        total_pair_overlap += overlap
        max_pair_overlap = max(max_pair_overlap, overlap)
        if left.endpoints == right.endpoints:
            # Same endpoint support means different packet classes on the same
            # support in the intended branch. The residual model assumes these
            # classes are disjoint.
            if overlap != 0:
                raise AssertionError((left, right, overlap))
            continue
        if left.endpoints & right.endpoints:
            endpoint_sharing_pairs += 1
            endpoint_overlap_mass += overlap
        else:
            disjoint_overlap_mass += overlap
            max_disjoint_overlap = max(max_disjoint_overlap, overlap)

    return {
        "support_size": len(union),
        "total_pair_overlap": total_pair_overlap,
        "max_pair_overlap": max_pair_overlap,
        "endpoint_sharing_pairs": endpoint_sharing_pairs,
        "endpoint_overlap_mass": endpoint_overlap_mass,
        "disjoint_overlap_mass": disjoint_overlap_mass,
        "max_disjoint_overlap": max_disjoint_overlap,
    }


def endpoint_support_degree(labels: list[Label]) -> int:
    supports_by_endpoint: dict[int, set[frozenset[int]]] = {}
    for label in labels:
        for endpoint in label.endpoints:
            supports_by_endpoint.setdefault(endpoint, set()).add(label.endpoints)
    return max((len(supports) for supports in supports_by_endpoint.values()), default=0)


def max_labels_per_support(labels: list[Label]) -> int:
    count: dict[frozenset[int], int] = {}
    for label in labels:
        count[label.endpoints] = count.get(label.endpoints, 0) + 1
    return max(count.values(), default=0)


def make_random_labels(rng: random.Random, trial: int) -> list[Label]:
    endpoint_points = list(range(8 + trial % 5))
    universe = list(range(100 + 17 * trial, 100 + 17 * trial + 60))
    supports = [frozenset(pair) for pair in combinations(endpoint_points, 2)]
    rng.shuffle(supports)

    h = 1 + trial % 4
    chosen_supports = supports[: rng.randint(2, min(10, len(supports)))]
    raw: list[Label] = []
    target_size = rng.randint(3, 8)

    for support_index, support in enumerate(chosen_supports):
        classes = rng.randint(1, h)
        used_for_support: set[int] = set()
        shared_core = set(rng.sample(universe, rng.randint(0, 3)))
        for class_index in range(classes):
            packet = set(shared_core)
            packet.update(rng.sample(universe, target_size + rng.randint(0, 4)))
            packet.difference_update(used_for_support)
            while len(packet) < target_size:
                packet.add(
                    10_000
                    + trial * 1000
                    + support_index * 100
                    + class_index * 10
                    + len(packet)
                )
            packet = set(sorted(packet)[:target_size])
            used_for_support.update(packet)
            raw.append(Label(support, frozenset(packet)))

    return raw


def check_cauchy_overlap_identities() -> None:
    rng = random.Random(20260630)
    checked = 0
    for trial in range(300):
        labels = make_random_labels(rng, trial)
        k = len(labels)
        if k < 2:
            continue
        s = len(labels[0].packet)
        stats = actual_stats(labels)
        support_size = stats["support_size"]
        lower = pair_overlap_mass_lower(k, s, support_size)
        if Fraction(stats["total_pair_overlap"], 1) < lower:
            raise AssertionError((trial, k, s, stats, lower))

        forced = forced_pair_overlap(k, s, support_size)
        if stats["max_pair_overlap"] < forced:
            raise AssertionError((trial, k, s, stats, forced))

        cap_floor = support_floor_from_pair_cap(k, s, stats["max_pair_overlap"])
        if support_size < cap_floor:
            raise AssertionError((trial, k, s, support_size, cap_floor, stats))
        checked += 1
    print(f"cauchy_overlap_systems_checked={checked}")


def check_endpoint_sift_bounds() -> None:
    rng = random.Random(20260701)
    checked = 0
    for trial in range(300):
        labels = make_random_labels(rng, trial)
        k = len(labels)
        if k < 2:
            continue
        s = len(labels[0].packet)
        h = max_labels_per_support(labels)
        degree_cap = endpoint_support_degree(labels)
        stats = actual_stats(labels)

        endpoint_pair_bound = k * h * max(0, degree_cap - 1)
        if stats["endpoint_sharing_pairs"] > endpoint_pair_bound:
            raise AssertionError((trial, endpoint_pair_bound, stats, labels))

        endpoint_mass_bound = endpoint_overlap_mass_bound(k, h, degree_cap, s)
        if stats["endpoint_overlap_mass"] > endpoint_mass_bound:
            raise AssertionError((trial, endpoint_mass_bound, stats))

        support_size = stats["support_size"]
        disjoint_lower = disjoint_overlap_mass_lower(k, s, support_size, h, degree_cap)
        if disjoint_lower > 0 and Fraction(stats["disjoint_overlap_mass"], 1) < disjoint_lower:
            raise AssertionError((trial, disjoint_lower, stats, h, degree_cap))

        forced = forced_disjoint_overlap(k, s, support_size, h, degree_cap)
        if stats["max_disjoint_overlap"] < forced:
            raise AssertionError((trial, forced, stats, h, degree_cap))

        cap_floor = support_floor_from_disjoint_pair_cap(
            k, s, h, degree_cap, stats["max_disjoint_overlap"]
        )
        if support_size < cap_floor:
            raise AssertionError((trial, support_size, cap_floor, stats, h, degree_cap))
        checked += 1
    print(f"endpoint_sift_systems_checked={checked}")


def check_exact_parameter_grid() -> None:
    checked = 0
    for k in range(2, 18):
        for s in range(1, 12):
            for support_budget in range(1, k * s + 1):
                total = pair_overlap_mass_lower(k, s, support_budget)
                per_pair = forced_pair_overlap(k, s, support_budget)
                if per_pair * comb2(k) < ceil_positive(total):
                    raise AssertionError((k, s, support_budget, total, per_pair))

                for pair_cap in range(0, s + 1):
                    floor = support_floor_from_pair_cap(k, s, pair_cap)
                    denominator = s + (k - 1) * pair_cap
                    if floor * denominator < k * s * s:
                        raise AssertionError((k, s, pair_cap, floor))

                for h in range(1, 5):
                    for degree_cap in range(1, 7):
                        disj = forced_disjoint_overlap(k, s, support_budget, h, degree_cap)
                        if disj < 0:
                            raise AssertionError((k, s, support_budget, h, degree_cap, disj))
                        for cap in range(0, s + 1):
                            floor = support_floor_from_disjoint_pair_cap(
                                k, s, h, degree_cap, cap
                            )
                            denominator = (
                                k * s
                                + 2 * endpoint_overlap_mass_bound(k, h, degree_cap, s)
                                + k * (k - 1) * cap
                            )
                            if floor * denominator < k * k * s * s:
                                raise AssertionError((k, s, h, degree_cap, cap, floor))
                checked += 1
    print(f"exact_parameter_grid_checked={checked}")


def main() -> None:
    check_exact_parameter_grid()
    check_cauchy_overlap_identities()
    check_endpoint_sift_bounds()
    print("m1 packet-overlap endpoint-sift checks passed")


if __name__ == "__main__":
    main()
