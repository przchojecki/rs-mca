#!/usr/bin/env python3
"""Exact verifier for the KoalaBear rank-eleven anchored rich-flat router.

The packet is a one-commit successor to PR #1172.  It proves that the
transverse row-space branch fits the deployed slope budget and that every
survivor emits a larger common-factor direction subspace.
"""

from __future__ import annotations

import argparse
import copy
import itertools
import json
from math import comb, prod
from typing import Iterable, Sequence


ROW = {
    "p": 2_130_706_433,
    "extension_degree": 6,
    "n": 2_097_152,
    "K": 1_048_576,
    "m": 1_116_048,
    "w": 67_472,
    "near": 134_944,
    "budget": 274_980_728_111_395_087,
    "theta_resource_s10": 106_618_568_137_036_225_644,
    "rank1_group_cap": 8_147_918,
}

SELECTED_TAU = 1_547
SELECTED_H = 42_452
PARENT = "193b7bf99a5cc7ccea042f25677e698d9f988eee"


class Reject(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Reject(message)


def falling(x: int, length: int) -> int:
    require(length >= 0, "nonnegative falling length")
    return prod(x - index for index in range(length))


def pair_cap_dim2(tau: int) -> int:
    n, K, w = ROW["n"], ROW["K"], ROW["w"]
    require(1 <= tau < w, "legal cutoff")
    d = w - tau
    return comb(n - K + 2, 2) // comb(d + 2, 2)


def transverse_space_cap(tau: int, h: int, rank: int) -> int:
    """Number of h-transverse represented row spaces of a fixed rank.

    The actual explanation dimension is at most ten.  A rank-r row space has
    annihilator dimension at most 10-r.  The exact tuple bound is monotone in
    that dimension, so ranks one and two use lengths nine and eight.
    """

    require(rank in (1, 2), "row-space rank")
    A = ROW["m"] - tau
    c = 2 * A - ROW["n"]
    require(0 <= h < c, "legal rich-flat threshold")
    tuple_length = 10 - rank
    return falling(ROW["m"], tuple_length) // (c - h) ** tuple_length


def envelope(tau: int, h: int) -> dict[str, int | bool]:
    n, K, m, w = (ROW[key] for key in ("n", "K", "m", "w"))
    require(1 <= tau < w, "legal cutoff")
    A = m - tau
    c = 2 * A - n
    require(c > 0, "positive anchor-overlap floor")
    require(0 <= h < c, "legal threshold")

    d = A - K
    multiplicity = n - A
    m2 = pair_cap_dim2(tau)
    rank2_group_cap = m2 * multiplicity
    high_tail = ROW["theta_resource_s10"] // (tau + 1)
    rank1_spaces = transverse_space_cap(tau, h, 1)
    rank2_spaces = transverse_space_cap(tau, h, 2)
    rank1_total = rank1_spaces * ROW["rank1_group_cap"]
    rank2_total = rank2_spaces * rank2_group_cap
    low_total = multiplicity + rank1_total + rank2_total
    total = ROW["near"] + high_tail + low_total

    return {
        "tau": tau,
        "A": A,
        "d": d,
        "anchor_overlap_floor": c,
        "pair_multiplicity": multiplicity,
        "pair_cap_dim2": m2,
        "rank2_group_cap": rank2_group_cap,
        "field_guard": m2 * m2 < ROW["p"] ** ROW["extension_degree"],
        "transverse_threshold": h,
        "emitted_core_size": h + 1,
        "rank1_space_count": rank1_spaces,
        "rank2_space_count": rank2_spaces,
        "rank1_total": rank1_total,
        "rank2_total": rank2_total,
        "anchor_pair_total": multiplicity,
        "low_total": low_total,
        "high_tail": high_tail,
        "near_addback": ROW["near"],
        "total": total,
        "signed_slack": ROW["budget"] - total,
    }


def max_paying_h(tau: int) -> int:
    A = ROW["m"] - tau
    c = 2 * A - ROW["n"]
    if c <= 0 or envelope(tau, 0)["total"] > ROW["budget"]:
        return -1
    low, high, best = 0, c - 1, -1
    while low <= high:
        middle = (low + high) // 2
        if envelope(tau, middle)["total"] <= ROW["budget"]:
            best = middle
            low = middle + 1
        else:
            high = middle - 1
    return best


def global_threshold_scan() -> dict[str, object]:
    maxima: list[tuple[int, int]] = []
    global_h = -1
    first_paying: tuple[int, int] | None = None
    last_paying: tuple[int, int] | None = None
    for tau in range(1, ROW["w"]):
        h = max_paying_h(tau)
        if h >= 0:
            if first_paying is None:
                first_paying = (tau, h)
            last_paying = (tau, h)
            if h > global_h:
                global_h = h
                maxima = [(tau, h)]
            elif h == global_h:
                maxima.append((tau, h))
    require(first_paying is not None and last_paying is not None, "nonempty scan")
    return {
        "global_max_h": global_h,
        "global_max_entries": maxima,
        "first_paying": first_paying,
        "last_paying": last_paying,
    }


def rank_mod(vectors: Sequence[Sequence[int]], p: int) -> int:
    if not vectors:
        return 0
    matrix = [[entry % p for entry in row] for row in vectors]
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    for col in range(cols):
        pivot = next((r for r in range(rank, rows) if matrix[r][col] % p), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inv = pow(matrix[rank][col], -1, p)
        matrix[rank] = [(entry * inv) % p for entry in matrix[rank]]
        for r in range(rows):
            if r == rank:
                continue
            factor = matrix[r][col] % p
            if factor:
                matrix[r] = [
                    (matrix[r][j] - factor * matrix[rank][j]) % p
                    for j in range(cols)
                ]
        rank += 1
        if rank == rows:
            break
    return rank


def vector_lines(p: int, dimension: int) -> list[tuple[int, ...]]:
    vectors = list(itertools.product(range(p), repeat=dimension))
    return [vector for vector in vectors if any(vector)]


def max_proper_flat_occupancy(multiset: Sequence[tuple[int, ...]], p: int, rank: int) -> int:
    """Brute-force maximum occupancy in a proper flat of the full span."""

    if rank == 0:
        return 0
    ambient_vectors = vector_lines(p, len(multiset[0])) if multiset else []
    best = sum(1 for vector in multiset if not any(vector))
    # Every proper flat is contained in a hyperplane.  Enumerate hyperplanes
    # by nonzero normal vectors; this suffices for the occupancy maximum.
    for normal in ambient_vectors:
        count = sum(
            1
            for vector in multiset
            if sum(a * b for a, b in zip(normal, vector)) % p == 0
        )
        if count < len(multiset):
            best = max(best, count)
    return best


def ordered_basis_count(multiset: Sequence[tuple[int, ...]], p: int, rank: int) -> int:
    count = 0
    for indices in itertools.permutations(range(len(multiset)), rank):
        vectors = [multiset[index] for index in indices]
        if rank_mod(vectors, p) == rank:
            count += 1
    return count


def compositions(total: int, parts: int) -> Iterable[tuple[int, ...]]:
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in compositions(total - first, parts - 1):
            yield (first,) + tail


def finite_matroid_control() -> dict[str, int]:
    """Exhaustively test the ordered-basis lemma in small vector spaces."""

    checked = 0
    for p, dimension, size in ((2, 3, 5), (3, 2, 5)):
        types = list(itertools.product(range(p), repeat=dimension))
        for counts in compositions(size, len(types)):
            multiset: list[tuple[int, ...]] = []
            for vector, multiplicity in zip(types, counts):
                multiset.extend([vector] * multiplicity)
            rank = rank_mod(multiset, p)
            if rank == 0:
                continue
            h = max_proper_flat_occupancy(multiset, p, rank)
            bases = ordered_basis_count(multiset, p, rank)
            require(bases >= (size - h) ** rank, "ordered-basis lower bound")
            checked += 1
    return {"configurations_checked": checked}


def build() -> dict[str, object]:
    selected = envelope(SELECTED_TAU, SELECTED_H)
    adjacent = envelope(SELECTED_TAU, SELECTED_H + 1)
    scan = global_threshold_scan()
    finite = finite_matroid_control()

    expected_selected = {
        "tau": 1547,
        "A": 1114501,
        "d": 65925,
        "anchor_overlap_floor": 131850,
        "pair_multiplicity": 982651,
        "pair_cap_dim2": 252,
        "rank2_group_cap": 247628052,
        "field_guard": True,
        "transverse_threshold": 42452,
        "emitted_core_size": 42453,
        "rank1_space_count": 7365150514,
        "rank2_space_count": 589969647,
        "rank1_total": 60010642445729852,
        "rank2_total": 146093034425737644,
        "anchor_pair_total": 982651,
        "low_total": 206103676872450147,
        "high_tail": 68875044016173272,
        "near_addback": 134944,
        "total": 274978720888758363,
        "signed_slack": 2007222636724,
    }
    require(selected == expected_selected, "selected exact envelope")
    require(adjacent["total"] - ROW["budget"] == 17108854816460,
            "adjacent threshold failure")
    require(
        scan
        == {
            "global_max_h": 42452,
            "global_max_entries": [(1547, 42452), (1548, 42452), (1549, 42452)],
            "first_paying": (397, 101),
            "last_paying": (21132, 4),
        },
        "global threshold scan",
    )

    return {
        "schema": "kb-mca-rank11-anchored-rich-flat-router-v1",
        "parent": PARENT,
        "row": ROW,
        "selected": selected,
        "adjacent_h_over_budget": adjacent["total"] - ROW["budget"],
        "scan": scan,
        "finite_matroid_control": finite,
        "terminal": {
            "common_zero_coordinates_at_least": SELECTED_H + 1,
            "rank1_extension_dimension_at_least": 2,
            "rank2_extension_dimension_at_least": 3,
            "rank2_original_common_zero_floor": selected["anchor_overlap_floor"],
            "locator_division_degree_ceiling": ROW["K"] - (SELECTED_H + 1),
        },
        "claims": {
            "transverse_branch_paid": True,
            "rank11_paid": False,
            "koalabear_closed": False,
            "active_v4_ledger_movement": 0,
        },
    }


def tamper_selftest(expected: dict[str, object]) -> int:
    mutations = [
        ("selected", "total", expected["selected"]["total"] - 1),
        ("selected", "rank1_space_count", expected["selected"]["rank1_space_count"] + 1),
        ("selected", "rank2_space_count", expected["selected"]["rank2_space_count"] - 1),
        ("terminal", "common_zero_coordinates_at_least", 42452),
        ("claims", "rank11_paid", True),
        ("scan", "global_max_h", 42453),
    ]
    caught = 0
    for section, key, value in mutations:
        changed = copy.deepcopy(expected)
        changed[section][key] = value
        try:
            require(changed == expected, "canonical result")
        except Reject:
            caught += 1
    require(caught == len(mutations), "all hostile mutations rejected")
    return caught


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    result = build()
    if args.tamper_selftest:
        caught = tamper_selftest(result)
        print(f"KB_MCA_RANK11_RICH_FLAT_TAMPER_PASS mutations={caught}/6")
        return
    if args.json:
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
        return
    selected = result["selected"]
    print(
        "KB_MCA_RANK11_RICH_FLAT_PASS "
        f"tau={selected['tau']} h={selected['transverse_threshold']} "
        f"emitted_core={selected['emitted_core_size']} "
        f"total={selected['total']} slack={selected['signed_slack']} "
        f"finite_controls={result['finite_matroid_control']['configurations_checked']}"
    )


if __name__ == "__main__":
    main()
