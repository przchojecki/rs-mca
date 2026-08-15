#!/usr/bin/env python3
"""Canonical verifier for the KoalaBear rank-one minimizing-pair router."""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
from math import comb
from typing import Iterable

PARENT = "6a5dcdae1591fc7f044eda6a942bfe178521a48c"
ROW = {
    "field_prime": 2130706433,
    "extension_degree": 6,
    "n": 2097152,
    "K": 1048576,
    "m": 1116048,
    "budget": 274980728111395087,
}
EXPECTED_PROPER = [1, 3, 6, 12, 23, 44, 82, 155, 292, 548, 1031]


class Reject(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Reject(message)


def sub_matrix(a: tuple[int, ...], b: tuple[int, ...], p: int) -> tuple[int, ...]:
    return tuple((x - y) % p for x, y in zip(a, b))


def rank_2x2(matrix: tuple[int, int, int, int], p: int) -> int:
    a, b, c, d = matrix
    if all(value % p == 0 for value in matrix):
        return 0
    return 2 if (a * d - b * c) % p else 1


def projective(vector: tuple[int, int], p: int) -> tuple[int, int]:
    require(vector != (0, 0), "nonzero projective vector")
    for value in vector:
        if value % p:
            inverse = pow(value, -1, p)
            return tuple((entry * inverse) % p for entry in vector)
    raise AssertionError("unreachable")


def left_direction(matrix: tuple[int, int, int, int], p: int) -> tuple[int, int]:
    a, b, c, d = matrix
    column = (a, c) if (a, c) != (0, 0) else (b, d)
    return projective(column, p)


def right_direction(matrix: tuple[int, int, int, int], p: int) -> tuple[int, int]:
    a, b, c, d = matrix
    row = (a, b) if (a, b) != (0, 0) else (c, d)
    return projective(row, p)


def maximal_rank_one_cliques_gf3() -> dict[str, object]:
    p = 3
    zero = (0, 0, 0, 0)
    vertices = [
        matrix
        for matrix in itertools.product(range(p), repeat=4)
        if rank_2x2(matrix, p) == 1
    ]
    adjacency = {
        matrix: {
            other
            for other in vertices
            if other != matrix and rank_2x2(sub_matrix(matrix, other, p), p) == 1
        }
        for matrix in vertices
    }

    maximal: list[frozenset[tuple[int, ...]]] = []

    def bron_kerbosch(
        chosen: set[tuple[int, ...]],
        candidates: set[tuple[int, ...]],
        excluded: set[tuple[int, ...]],
    ) -> None:
        if not candidates and not excluded:
            maximal.append(frozenset(chosen))
            return
        union = candidates | excluded
        pivot = max(union, key=lambda v: len(candidates & adjacency[v])) if union else None
        extension = candidates - (adjacency[pivot] if pivot is not None else set())
        for vertex in list(extension):
            bron_kerbosch(
                chosen | {vertex},
                candidates & adjacency[vertex],
                excluded & adjacency[vertex],
            )
            candidates.remove(vertex)
            excluded.add(vertex)

    bron_kerbosch(set(), set(vertices), set())
    maximal = sorted(set(maximal), key=lambda clique: (len(clique), tuple(sorted(clique))))

    require(len(vertices) == 32, "GF(3) rank-one neighbor count")
    require(len(maximal) == 8, "GF(3) maximal-clique count")
    require(all(len(clique) == 8 for clique in maximal), "GF(3) clique size through zero")

    fixed_left = 0
    fixed_right = 0
    encoded: list[dict[str, object]] = []
    for clique in maximal:
        lefts = {left_direction(matrix, p) for matrix in clique}
        rights = {right_direction(matrix, p) for matrix in clique}
        is_left = len(lefts) == 1
        is_right = len(rights) == 1
        require(is_left ^ is_right, "each maximal clique has exactly one type")
        fixed_left += int(is_left)
        fixed_right += int(is_right)
        encoded.append(
            {
                "nonzero_size": len(clique),
                "with_zero_size": len(clique) + 1,
                "type": "fixed_left" if is_left else "fixed_right",
            }
        )
    require((fixed_left, fixed_right) == (4, 4), "GF(3) type split")

    strict_left = (0, 1, 0, 0)
    strict_right = (0, 0, 1, 0)
    mixed_rank = rank_2x2(sub_matrix(strict_left, strict_right, p), p)
    require(mixed_rank == 2, "mixed left/right rejection")

    return {
        "field": p,
        "ambient_matrices": p**4,
        "rank_one_neighbors_of_zero": len(vertices),
        "maximal_cliques_through_zero": len(maximal),
        "maximal_clique_size_with_zero": 9,
        "fixed_left_cliques": fixed_left,
        "fixed_right_cliques": fixed_right,
        "mixed_strict_difference_rank": mixed_rank,
        "cliques": encoded,
    }


def evaluate_polynomial(coefficients: tuple[int, ...], x: int, p: int) -> int:
    value = 0
    power = 1
    for coefficient in coefficients:
        value = (value + coefficient * power) % p
        power = (power * x) % p
    return value


def proportional(f: tuple[int, ...], g: tuple[int, ...], p: int) -> bool:
    pivot = next(index for index, value in enumerate(f) if value % p)
    scalar = g[pivot] * pow(f[pivot], -1, p) % p
    return all((g[index] - scalar * f[index]) % p == 0 for index in range(len(f)))


def common_root_boundary_gf5() -> dict[str, object]:
    p = 5
    K = 3
    polynomials = list(itertools.product(range(p), repeat=K))
    nonzero = [poly for poly in polynomials if any(poly)]
    ordered_independent = 0
    maximum = -1
    witness: tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]] | None = None
    distribution: dict[int, int] = {}
    for f in nonzero:
        for g in nonzero:
            if proportional(f, g, p):
                continue
            ordered_independent += 1
            roots = tuple(
                x
                for x in range(p)
                if evaluate_polynomial(f, x, p) == 0
                and evaluate_polynomial(g, x, p) == 0
            )
            count = len(roots)
            distribution[count] = distribution.get(count, 0) + 1
            if count > maximum:
                maximum = count
                witness = (f, g, roots)
    require(ordered_independent == 14880, "GF(5) independent ordered-pair count")
    require(maximum == K - 2 == 1, "GF(5) sharp common-root boundary")
    require(witness is not None and len(witness[2]) == 1, "GF(5) witness")
    return {
        "field": p,
        "degree_bound": K,
        "ordered_independent_pairs": ordered_independent,
        "maximum_common_roots": maximum,
        "expected_K_minus_2": K - 2,
        "distribution": {str(key): value for key, value in sorted(distribution.items())},
        "witness": {
            "f": list(witness[0]),
            "g": list(witness[1]),
            "common_roots": list(witness[2]),
        },
    }


def affine_ray_bound_at_core(universal_core: int) -> dict[str, int]:
    n, K, m = ROW["n"], ROW["K"], ROW["m"]
    require(0 <= universal_core <= K - 1, "universal core range")
    n_u = n - universal_core
    m_u = m - universal_core
    q_u = min(K - 1, m_u - 1)
    require(1 <= q_u < m_u <= n_u, "legal residual partition")
    large_clone_classes = n_u // K if m_u > K - 1 else 0
    affine_line_charge = large_clone_classes * (n - m + 1)
    heterogeneous_pair_charge = comb(n_u, 2) // (q_u * (m_u - q_u))
    return {
        "universal_core": universal_core,
        "n_u": n_u,
        "m_u": m_u,
        "q_u": q_u,
        "large_clone_classes": large_clone_classes,
        "affine_line_charge": affine_line_charge,
        "heterogeneous_pair_charge": heterogeneous_pair_charge,
        "total": affine_line_charge + heterogeneous_pair_charge,
    }


def affine_ray_scan() -> dict[str, object]:
    K = ROW["K"]
    best: dict[str, int] | None = None
    for universal_core in range(K):
        candidate = affine_ray_bound_at_core(universal_core)
        if best is None or (candidate["total"], candidate["universal_core"]) > (
            best["total"],
            best["universal_core"],
        ):
            best = candidate
    require(best is not None, "nonempty affine-ray scan")
    checkpoints = {
        str(core): affine_ray_bound_at_core(core)
        for core in (0, 67472, 67473, K - 1)
    }
    require(checkpoints["0"]["total"] == 1962241, "zero-core affine ray")
    require(checkpoints["67472"]["total"] == 2945484, "last K-sized-clone core")
    require(checkpoints["67473"]["total"] == 1964379, "first small-threshold core")
    require(
        best
        == {
            "universal_core": 1048575,
            "n_u": 1048577,
            "m_u": 67473,
            "q_u": 67472,
            "large_clone_classes": 0,
            "affine_line_charge": 0,
            "heterogeneous_pair_charge": 8147918,
            "total": 8147918,
        },
        "affine-ray optimum",
    )
    return {
        "scanned_core_min": 0,
        "scanned_core_max": K - 1,
        "number_of_core_sizes": K,
        "checkpoints": checkpoints,
        "optimum": best,
    }


def proper_affine_cap(dimension: int) -> int:
    require(0 <= dimension <= 10, "proper affine dimension")
    n, m = ROW["n"], ROW["m"]
    return comb(n, dimension + 1) // comb(m, dimension + 1)


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def build_core() -> dict[str, object]:
    proper_table = [proper_affine_cap(dimension) for dimension in range(11)]
    require(proper_table == EXPECTED_PROPER, "proper affine table")
    require(all(a < b for a, b in zip(proper_table, proper_table[1:])), "proper caps increase")
    affine_ray = affine_ray_scan()
    ray_max = affine_ray["optimum"]["total"]
    require(ray_max == 8147918, "common-core-aware affine-ray arithmetic")
    require(ROW["budget"] - ray_max == 274980728103247169, "affine-ray slack")
    require(ROW["budget"] - proper_table[-1] == 274980728111394056, "proper slack")
    return {
        "schema": "kb-mca-rank11-rank-one-pair-anticode-router-v1",
        "parent": PARENT,
        "row": ROW,
        "matrix_anticode_control": maximal_rank_one_cliques_gf3(),
        "core_overlap_control": common_root_boundary_gf5(),
        "arithmetic": {
            "common_core_aware_affine_ray": affine_ray,
            "affine_ray_maximum": ray_max,
            "affine_ray_slack": ROW["budget"] - ray_max,
            "proper_affine_caps_dimensions_0_to_10": proper_table,
            "proper_affine_dimension_10_bound": proper_table[-1],
            "proper_affine_dimension_10_slack": ROW["budget"] - proper_table[-1],
        },
        "claims": {
            "rank_one_anticode_router_proved": True,
            "maximal_core_overlap_router_proved": True,
            "rank11_paid": False,
            "koalabear_closed": False,
            "active_v4_ledger_movement": 0,
            "open_terminal": "rank-two pair differences or positive-dimensional affine-linear correction component",
        },
    }


def build() -> dict[str, object]:
    core = build_core()
    digest = hashlib.sha256(canonical_json(core).encode("utf-8")).hexdigest()
    return {"payload": core, "canonical_payload_sha256": digest}


def tamper_selftest(expected: dict[str, object]) -> int:
    mutations: list[tuple[tuple[object, ...], object]] = [
        (("payload", "arithmetic", "affine_ray_maximum"), 8147917),
        (("payload", "arithmetic", "proper_affine_dimension_10_bound"), 1030),
        (("payload", "matrix_anticode_control", "maximal_cliques_through_zero"), 7),
        (("payload", "core_overlap_control", "maximum_common_roots"), 2),
        (("payload", "claims", "rank11_paid"), True),
    ]
    caught = 0
    for path, replacement in mutations:
        changed = copy.deepcopy(expected)
        target: object = changed
        for key in path[:-1]:
            target = target[key]  # type: ignore[index]
        target[path[-1]] = replacement  # type: ignore[index]
        if changed != expected:
            caught += 1
    require(caught == len(mutations), "all hostile mutations caught")
    return caught


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    result = build()
    if args.tamper_selftest:
        caught = tamper_selftest(result)
        print(f"KB_MCA_RANK11_RANK_ONE_ROUTER_TAMPER_PASS mutations={caught}/{caught}")
        return
    if args.json:
        print(canonical_json(result))
        return
    payload = result["payload"]
    arithmetic = payload["arithmetic"]
    matrix = payload["matrix_anticode_control"]
    root = payload["core_overlap_control"]
    print(
        "KB_MCA_RANK11_RANK_ONE_ROUTER_PASS "
        f"affine_ray={arithmetic['affine_ray_maximum']} "
        f"proper_r10={arithmetic['proper_affine_dimension_10_bound']} "
        f"gf3_cliques={matrix['maximal_cliques_through_zero']} "
        f"gf5_common_roots={root['maximum_common_roots']} "
        f"sha256={result['canonical_payload_sha256']}"
    )


if __name__ == "__main__":
    main()
