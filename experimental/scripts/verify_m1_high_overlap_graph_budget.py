#!/usr/bin/env python3
"""Verify the M1 high-overlap graph-budget packet sift.

The checks are finite combinatorics only. They verify the edge-budget support
floor and the contrapositive high-edge lower bound for sampled packet systems.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
import random

from verify_m1_packet_overlap_endpoint_sift import (
    Label,
    actual_stats,
    ceil_fraction,
    ceil_positive,
    comb2,
    endpoint_overlap_mass_bound,
    endpoint_support_degree,
    make_random_labels,
    max_labels_per_support,
    pair_overlap_mass_lower,
)


def high_overlap_edges(labels: list[Label], lambda_cap: int) -> set[tuple[int, int]]:
    edges: set[tuple[int, int]] = set()
    for i, j in combinations(range(len(labels)), 2):
        left = labels[i]
        right = labels[j]
        if left.endpoints & right.endpoints:
            continue
        if len(left.packet & right.packet) > lambda_cap:
            edges.add((i, j))
    return edges


def high_overlap_max_degree(labels: list[Label], lambda_cap: int) -> int:
    degree = [0 for _ in labels]
    for i, j in high_overlap_edges(labels, lambda_cap):
        degree[i] += 1
        degree[j] += 1
    return max(degree, default=0)


def graph_degeneracy(num_vertices: int, edges: set[tuple[int, int]]) -> int:
    adjacency = [set() for _ in range(num_vertices)]
    for i, j in edges:
        adjacency[i].add(j)
        adjacency[j].add(i)

    remaining = set(range(num_vertices))
    degeneracy = 0
    while remaining:
        vertex = min(remaining, key=lambda v: len(adjacency[v] & remaining))
        degree = len(adjacency[vertex] & remaining)
        degeneracy = max(degeneracy, degree)
        remaining.remove(vertex)
    return degeneracy


def max_edges_from_degree_bound(k: int, degree_bound: int) -> int:
    if degree_bound < 0:
        raise ValueError("degree_bound must be nonnegative")
    return min(comb2(k), k * degree_bound // 2)


def max_edges_from_degeneracy_bound(k: int, degeneracy_bound: int) -> int:
    if degeneracy_bound < 0:
        raise ValueError("degeneracy_bound must be nonnegative")
    if k <= 1:
        return 0
    if degeneracy_bound >= k - 1:
        return comb2(k)
    return degeneracy_bound * k - degeneracy_bound * (degeneracy_bound + 1) // 2


def support_floor_from_high_edge_budget(
    k: int,
    s: int,
    h: int,
    degree_cap: int,
    lambda_cap: int,
    high_edge_budget: int,
) -> int:
    if k == 0:
        return 0
    if not 0 <= lambda_cap < s:
        raise ValueError("lambda_cap must satisfy 0 <= lambda_cap < s")
    denominator = k * s
    denominator += 2 * endpoint_overlap_mass_bound(k, h, degree_cap, s)
    denominator += k * (k - 1) * lambda_cap
    denominator += 2 * (s - lambda_cap) * high_edge_budget
    if denominator <= 0:
        raise ValueError("nonpositive high-edge denominator")
    return ceil_fraction(Fraction(k * k * s * s, denominator))


def support_floor_from_max_degree_bound(
    k: int,
    s: int,
    h: int,
    degree_cap: int,
    lambda_cap: int,
    graph_degree_bound: int,
) -> int:
    return support_floor_from_high_edge_budget(
        k,
        s,
        h,
        degree_cap,
        lambda_cap,
        max_edges_from_degree_bound(k, graph_degree_bound),
    )


def support_floor_from_degeneracy_bound(
    k: int,
    s: int,
    h: int,
    degree_cap: int,
    lambda_cap: int,
    degeneracy_bound: int,
) -> int:
    return support_floor_from_high_edge_budget(
        k,
        s,
        h,
        degree_cap,
        lambda_cap,
        max_edges_from_degeneracy_bound(k, degeneracy_bound),
    )


def forced_high_edges(
    k: int,
    s: int,
    support_budget: int,
    h: int,
    degree_cap: int,
    lambda_cap: int,
) -> int:
    if k < 2:
        return 0
    if not 0 <= lambda_cap < s:
        raise ValueError("lambda_cap must satisfy 0 <= lambda_cap < s")
    burden = pair_overlap_mass_lower(k, s, support_budget)
    endpoint_budget = endpoint_overlap_mass_bound(k, h, degree_cap, s)
    baseline = lambda_cap * comb2(k)
    return ceil_positive(
        (burden - endpoint_budget - baseline) / (s - lambda_cap)
    )


def check_exact_parameter_grid() -> None:
    checked = 0
    degree_checked = 0
    for k in range(2, 24):
        for s in range(1, 13):
            for h in range(1, 6):
                for degree_cap in range(1, 8):
                    for lambda_cap in range(0, s):
                        max_edges = comb2(k)
                        budgets = set(range(0, min(max_edges, 12) + 1))
                        budgets.update({max_edges // 4, max_edges // 2, max_edges})
                        for edge_budget in sorted(budgets):
                            floor = support_floor_from_high_edge_budget(
                                k, s, h, degree_cap, lambda_cap, edge_budget
                            )
                            denominator = k * s
                            denominator += 2 * endpoint_overlap_mass_bound(
                                k, h, degree_cap, s
                            )
                            denominator += k * (k - 1) * lambda_cap
                            denominator += 2 * (s - lambda_cap) * edge_budget
                            if floor * denominator < k * k * s * s:
                                raise AssertionError(
                                    (
                                        k,
                                        s,
                                        h,
                                        degree_cap,
                                        lambda_cap,
                                        edge_budget,
                                        floor,
                                    )
                                )
                            if floor > 0 and (floor - 1) * denominator >= k * k * s * s:
                                raise AssertionError(
                                    (
                                        "nonminimal floor",
                                        k,
                                        s,
                                        h,
                                        degree_cap,
                                        lambda_cap,
                                        edge_budget,
                                        floor,
                                    )
                                )
                        for support_budget in range(1, k * s + 1):
                            lower = forced_high_edges(
                                k, s, support_budget, h, degree_cap, lambda_cap
                            )
                            if lower < 0:
                                raise AssertionError(
                                    (
                                        k,
                                        s,
                                        support_budget,
                                        h,
                                        degree_cap,
                                        lambda_cap,
                                        lower,
                                    )
                                )
                            if lower > comb2(k):
                                complete_floor = support_floor_from_high_edge_budget(
                                    k,
                                    s,
                                    h,
                                    degree_cap,
                                    lambda_cap,
                                    comb2(k),
                                )
                                if complete_floor <= support_budget:
                                    raise AssertionError(
                                        (
                                            "complete graph should still be impossible",
                                            k,
                                            s,
                                            support_budget,
                                            h,
                                            degree_cap,
                                            lambda_cap,
                                            lower,
                                            complete_floor,
                                    )
                                )
                            checked += 1
                        for graph_bound in range(0, k + 2):
                            degree_edges = max_edges_from_degree_bound(k, graph_bound)
                            if degree_edges > comb2(k):
                                raise AssertionError((k, graph_bound, degree_edges))
                            degree_floor = support_floor_from_max_degree_bound(
                                k, s, h, degree_cap, lambda_cap, graph_bound
                            )
                            edge_floor = support_floor_from_high_edge_budget(
                                k, s, h, degree_cap, lambda_cap, degree_edges
                            )
                            if degree_floor != edge_floor:
                                raise AssertionError(
                                    (
                                        "degree floor",
                                        k,
                                        s,
                                        h,
                                        degree_cap,
                                        lambda_cap,
                                        graph_bound,
                                        degree_floor,
                                        edge_floor,
                                    )
                                )

                            degen_edges = max_edges_from_degeneracy_bound(k, graph_bound)
                            if degen_edges > comb2(k):
                                raise AssertionError(
                                    ("degen edges", k, graph_bound, degen_edges)
                                )
                            degen_floor = support_floor_from_degeneracy_bound(
                                k, s, h, degree_cap, lambda_cap, graph_bound
                            )
                            edge_floor = support_floor_from_high_edge_budget(
                                k, s, h, degree_cap, lambda_cap, degen_edges
                            )
                            if degen_floor != edge_floor:
                                raise AssertionError(
                                    (
                                        "degen floor",
                                        k,
                                        s,
                                        h,
                                        degree_cap,
                                        lambda_cap,
                                        graph_bound,
                                        degen_floor,
                                        edge_floor,
                                    )
                                )
                            degree_checked += 1
    print(f"exact_high_edge_parameter_grid_checked={checked}")
    print(f"exact_degree_degeneracy_grid_checked={degree_checked}")


def check_sampled_packet_systems() -> None:
    rng = random.Random(20260630)
    checked = 0
    alternatives = 0
    degree_interfaces = 0
    degeneracy_interfaces = 0

    for trial in range(650):
        labels = make_random_labels(rng, trial)
        k = len(labels)
        if k < 2:
            continue
        s = len(labels[0].packet)
        h = max_labels_per_support(labels)
        degree_cap = endpoint_support_degree(labels)
        stats = actual_stats(labels)
        support_size = stats["support_size"]

        for lambda_cap in range(0, s):
            high_edges = high_overlap_edges(labels, lambda_cap)
            edge_count = len(high_edges)

            floor = support_floor_from_high_edge_budget(
                k, s, h, degree_cap, lambda_cap, edge_count
            )
            if support_size < floor:
                raise AssertionError(
                    (
                        trial,
                        k,
                        s,
                        h,
                        degree_cap,
                        lambda_cap,
                        edge_count,
                        support_size,
                        floor,
                        stats,
                    )
                )

            lower = forced_high_edges(
                k, s, support_size, h, degree_cap, lambda_cap
            )
            if edge_count < lower:
                raise AssertionError(
                    (
                        trial,
                        k,
                        s,
                        lambda_cap,
                        edge_count,
                        lower,
                        support_size,
                        stats,
                    )
                )

            for support_budget in (support_size, max(1, support_size - 1)):
                for edge_budget in {0, max(0, edge_count - 1), edge_count}:
                    floor = support_floor_from_high_edge_budget(
                        k, s, h, degree_cap, lambda_cap, edge_budget
                    )
                    if floor <= support_budget:
                        continue
                    large_support = support_size > support_budget
                    many_edges = edge_count > edge_budget
                    if not (large_support or many_edges):
                        raise AssertionError(
                            (
                                trial,
                                k,
                                s,
                                h,
                                degree_cap,
                                lambda_cap,
                                edge_budget,
                                floor,
                                support_budget,
                                support_size,
                                edge_count,
                                stats,
                            )
                        )
                    alternatives += 1

            max_degree = high_overlap_max_degree(labels, lambda_cap)
            degree_budget = max_edges_from_degree_bound(k, max_degree)
            if edge_count > degree_budget:
                raise AssertionError((trial, lambda_cap, edge_count, max_degree))
            degree_floor = support_floor_from_max_degree_bound(
                k, s, h, degree_cap, lambda_cap, max_degree
            )
            if support_size < degree_floor:
                raise AssertionError(
                    (
                        "degree interface",
                        trial,
                        lambda_cap,
                        edge_count,
                        max_degree,
                        support_size,
                        degree_floor,
                    )
                )
            degree_interfaces += 1

            degeneracy = graph_degeneracy(k, high_edges)
            degen_budget = max_edges_from_degeneracy_bound(k, degeneracy)
            if edge_count > degen_budget:
                raise AssertionError(
                    (trial, lambda_cap, edge_count, degeneracy, degen_budget)
                )
            degen_floor = support_floor_from_degeneracy_bound(
                k, s, h, degree_cap, lambda_cap, degeneracy
            )
            if support_size < degen_floor:
                raise AssertionError(
                    (
                        "degeneracy interface",
                        trial,
                        lambda_cap,
                        edge_count,
                        degeneracy,
                        support_size,
                        degen_floor,
                    )
                )
            degeneracy_interfaces += 1
        checked += 1

    print(f"sampled_packet_systems_checked={checked}")
    print(f"sampled_high_edge_alternatives_triggered={alternatives}")
    print(f"sampled_degree_interfaces_checked={degree_interfaces}")
    print(f"sampled_degeneracy_interfaces_checked={degeneracy_interfaces}")


def main() -> None:
    check_exact_parameter_grid()
    check_sampled_packet_systems()
    print("m1 high-overlap graph-budget checks passed")


if __name__ == "__main__":
    main()
