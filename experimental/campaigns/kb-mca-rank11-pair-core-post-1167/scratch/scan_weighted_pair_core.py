#!/usr/bin/env python3
"""Superseded exploratory scan for the rank-11 pair/core route cut.

This discovery script models a bipartite endpoint-degree bound and therefore
contains the weaker factor-two normalization.  It is preserved as research
history, is excluded from the release packet, and must not be used for the
fixed ordered-pair theorem or its certified constants.  The authoritative
replay is ``experimental/scripts/verify_kb_mca_rank11_pair_core_route_cut_v1.py``.
"""

from __future__ import annotations

from fractions import Fraction
from math import comb, prod


ROW = {
    "p": 2130706433,
    "extension_degree": 6,
    "n": 2097152,
    "K": 1048576,
    "m": 1116048,
    "w": 67472,
    "near": 134944,
    "budget": 274980728111395087,
}


def falling(x: int, length: int) -> int:
    return prod(x - i for i in range(length))


def rising(x: int, length: int) -> int:
    return prod(x + i for i in range(length))


def theta_resource(s: int) -> int:
    n, K, m, w = (ROW[key] for key in ("n", "K", "m", "w"))
    raw = max(
        Fraction(falling(n, s + 1), m * rising(w + 1, s - 1)),
        Fraction(falling(n - K + s, s + 1), rising(w + 1, s)),
    )
    return raw.numerator // raw.denominator


def ordinary_cap(s: int, tau: int) -> int:
    n, K, m, w = (ROW[key] for key in ("n", "K", "m", "w"))
    agreement = m - tau
    assert agreement > K
    return comb(n - K + s, s) // comb(agreement - K + s, s)


def profile(s: int, tau: int) -> dict[str, int | bool]:
    M = theta_resource(s)
    Q = ordinary_cap(s, tau)
    available = ROW["budget"] - ROW["near"]
    numerator = (available + 1) * (tau + 1) - 1 - M
    p = numerator // (2 * Q)
    if p < 0:
        p = -1
    paid = ROW["near"] + (M + 2 * p * Q) // (tau + 1)
    next_paid = ROW["near"] + (M + 2 * (p + 1) * Q) // (tau + 1)
    edge_degree = (p + tau) // tau if p >= 0 else 0
    parallel_weight_cap = tau * (ROW["n"] - ROW["m"] + tau)
    distinct_neighbors = ((p + 1) + parallel_weight_cap - 1) // parallel_weight_cap if p >= 0 else 0
    return {
        "s": s,
        "tau": tau,
        "theta_resource": M,
        "ordinary_cap": Q,
        "p": p,
        "forced_min_weighted_degree": p + 1,
        "forced_min_edge_record_degree": edge_degree,
        "parallel_weight_cap": parallel_weight_cap,
        "forced_distinct_neighbors": distinct_neighbors,
        "paid_if_p_degenerate": paid,
        "slack": ROW["budget"] - paid,
        "next_p_total": next_paid,
        "next_p_fails": next_paid > ROW["budget"],
        "subsquare": Q * Q < ROW["p"] ** ROW["extension_degree"],
    }


def max_parallel_weight(tau: int) -> tuple[int, int]:
    """Max of floor((n-m+j)/j)*(tau+1-j), 1<=j<=tau."""
    # Both nonnegative integer factors are nonincreasing in j, so j=1.
    return (ROW["n"] - ROW["m"] + 1) * tau, 1


def collapsed_pair_bound(s: int, tau: int) -> dict[str, int | bool]:
    M = theta_resource(s)
    Q = ordinary_cap(s, tau)
    load, deficiency = max_parallel_weight(tau)
    total = ROW["near"] + (M + Q * load) // (tau + 1)
    return {
        "s": s,
        "tau": tau,
        "theta_resource": M,
        "pair_cap": Q,
        "max_parallel_weight": load,
        "maximizing_deficiency": deficiency,
        "total": total,
        "slack": ROW["budget"] - total,
        "subsquare": Q * Q < ROW["p"] ** ROW["extension_degree"],
    }


def forced_heavy_pair(s: int, tau: int) -> dict[str, int | bool]:
    M = theta_resource(s)
    Q = ordinary_cap(s, tau)
    available = ROW["budget"] - ROW["near"]
    p = ((available + 1) * (tau + 1) - 1 - M) // Q
    paid = ROW["near"] + (M + p * Q) // (tau + 1)
    next_paid = ROW["near"] + (M + (p + 1) * Q) // (tau + 1)
    parallel, _ = max_parallel_weight(tau)
    forced_weight = p + 1
    def load(j: int) -> int:
        return ((ROW["n"] - ROW["m"] + j) // j) * (tau + 1 - j)

    lo, hi = 1, tau + 1
    while lo < hi:
        mid = (lo + hi) // 2
        if load(mid) >= forced_weight:
            lo = mid + 1
        else:
            hi = mid
    max_deficiency = lo - 1
    return {
        "s": s,
        "tau": tau,
        "theta_resource": M,
        "pair_cap": Q,
        "forced_pair_weight": forced_weight,
        "forced_pair_edges": (forced_weight + tau - 1) // tau,
        "forced_max_core_deficiency": max_deficiency,
        "parallel_weight_cap": parallel,
        "fraction_of_parallel_cap_ppm": ((p + 1) * 1_000_000) // parallel,
        "paid_if_each_pair_at_most_p": paid,
        "slack": ROW["budget"] - paid,
        "next_total": next_paid,
        "next_fails": next_paid > ROW["budget"],
        "subsquare": Q * Q < ROW["p"] ** ROW["extension_degree"],
    }


def main() -> None:
    for s in (9, 10, 11):
        legal = [profile(s, tau) for tau in range(1, ROW["w"])]
        legal = [item for item in legal if item["p"] >= 0 and item["subsquare"]]
        by_weight = max(legal, key=lambda x: (x["forced_min_weighted_degree"], -x["tau"]))
        by_edges = max(legal, key=lambda x: (x["forced_min_edge_record_degree"], -x["tau"]))
        print("RANK", s + 1)
        print("WEIGHT", by_weight)
        print("EDGES", by_edges)
        collapsed = [collapsed_pair_bound(s, tau) for tau in range(1, ROW["w"])]
        collapsed = [item for item in collapsed if item["subsquare"]]
        best_collapsed = min(collapsed, key=lambda x: (x["total"], x["tau"]))
        print("COLLAPSED", best_collapsed)
        heavy = [forced_heavy_pair(s, tau) for tau in range(1, ROW["w"])]
        heavy = [item for item in heavy if item["subsquare"] and item["forced_pair_weight"] > 0]
        best_heavy = max(heavy, key=lambda x: (x["forced_pair_weight"], -x["tau"]))
        best_fraction = max(heavy, key=lambda x: (x["fraction_of_parallel_cap_ppm"], -x["tau"]))
        best_core = min(heavy, key=lambda x: (x["forced_max_core_deficiency"], -x["forced_pair_edges"], x["tau"]))
        best_pair_edges = max(heavy, key=lambda x: (x["forced_pair_edges"], -x["tau"]))
        print("HEAVY_WEIGHT", best_heavy)
        print("HEAVY_FRACTION", best_fraction)
        print("HEAVY_CORE", best_core)
        print("HEAVY_EDGES", best_pair_edges)


if __name__ == "__main__":
    main()
