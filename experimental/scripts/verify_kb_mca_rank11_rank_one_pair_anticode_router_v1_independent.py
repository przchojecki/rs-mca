#!/usr/bin/env python3
"""Independent replay of the KoalaBear rank-one pair-anticode router."""

from __future__ import annotations

import hashlib
import itertools
import json
from math import comb

PARENT = "6a5dcdae1591fc7f044eda6a942bfe178521a48c"
N = 2097152
K = 1048576
M = 1116048
BUDGET = 274980728111395087


def rank(matrix: tuple[int, int, int, int], p: int) -> int:
    a, b, c, d = matrix
    if matrix == (0, 0, 0, 0):
        return 0
    return 2 if (a * d - b * c) % p else 1


def minus(a: tuple[int, ...], b: tuple[int, ...], p: int) -> tuple[int, ...]:
    return tuple((x - y) % p for x, y in zip(a, b))


def normalized(v: tuple[int, int], p: int) -> tuple[int, int]:
    for x in v:
        if x:
            inv = pow(x, -1, p)
            return ((v[0] * inv) % p, (v[1] * inv) % p)
    raise AssertionError


def outer(u: tuple[int, int], v: tuple[int, int], p: int) -> tuple[int, int, int, int]:
    return (
        u[0] * v[0] % p,
        u[0] * v[1] % p,
        u[1] * v[0] % p,
        u[1] * v[1] % p,
    )


def projective_lines(p: int) -> list[tuple[int, int]]:
    values = {
        normalized(v, p)
        for v in itertools.product(range(p), repeat=2)
        if v != (0, 0)
    }
    return sorted(values)


def clique_controls() -> dict[str, int]:
    p = 3
    zero = (0, 0, 0, 0)
    vectors = list(itertools.product(range(p), repeat=2))
    lines = projective_lines(p)
    cliques: list[frozenset[tuple[int, ...]]] = []
    for fixed_left in lines:
        cliques.append(frozenset(outer(fixed_left, v, p) for v in vectors))
    for fixed_right in lines:
        cliques.append(frozenset(outer(u, fixed_right, p) for u in vectors))
    assert len(cliques) == 8
    assert len(set(cliques)) == 8
    ambient = list(itertools.product(range(p), repeat=4))
    for clique in cliques:
        assert zero in clique and len(clique) == 9
        for a, b in itertools.combinations(clique, 2):
            assert rank(minus(a, b, p), p) == 1
        for candidate in ambient:
            if candidate in clique:
                continue
            assert any(rank(minus(candidate, member, p), p) != 1 for member in clique)
    mixed_left = outer((1, 0), (0, 1), p)
    mixed_right = outer((0, 1), (1, 0), p)
    assert rank(minus(mixed_left, mixed_right, p), p) == 2
    return {
        "maximal_cliques": len(cliques),
        "size": 9,
        "left": len(lines),
        "right": len(lines),
        "mixed_rank": 2,
    }


def value(poly: tuple[int, ...], x: int, p: int) -> int:
    return sum(coef * pow(x, index, p) for index, coef in enumerate(poly)) % p


def dependent(a: tuple[int, ...], b: tuple[int, ...], p: int) -> bool:
    for scalar in range(p):
        if all((b[i] - scalar * a[i]) % p == 0 for i in range(len(a))):
            return True
    return False


def root_control() -> dict[str, int]:
    p = 5
    polys = [f for f in itertools.product(range(p), repeat=3) if any(f)]
    pairs = 0
    maximum = 0
    for f in polys:
        for g in polys:
            if dependent(f, g, p):
                continue
            pairs += 1
            common = sum(value(f, x, p) == value(g, x, p) == 0 for x in range(p))
            maximum = max(maximum, common)
    assert pairs == 14880
    assert maximum == 1
    return {"ordered_independent_pairs": pairs, "maximum_common_roots": maximum}


def affine_ray(universal_core: int) -> int:
    n_u = N - universal_core
    m_u = M - universal_core
    q_u = min(K - 1, m_u - 1)
    large = n_u // K if m_u > K - 1 else 0
    return large * (N - M + 1) + comb(n_u, 2) // (q_u * (m_u - q_u))


def main() -> None:
    best_value = -1
    best_core = -1
    for universal_core in range(K):
        candidate = affine_ray(universal_core)
        if (candidate, universal_core) > (best_value, best_core):
            best_value, best_core = candidate, universal_core
    proper = [comb(N, r + 1) // comb(M, r + 1) for r in range(11)]
    assert (best_value, best_core) == (8147918, 1048575)
    assert affine_ray(0) == 1962241
    assert affine_ray(67472) == 2945484
    assert affine_ray(67473) == 1964379
    assert BUDGET - best_value == 274980728103247169
    assert proper == [1, 3, 6, 12, 23, 44, 82, 155, 292, 548, 1031]
    assert BUDGET - proper[-1] == 274980728111394056
    result = {
        "parent": PARENT,
        "affine_ray_maximum": best_value,
        "affine_ray_core": best_core,
        "proper": proper,
        "clique_control": clique_controls(),
        "root_control": root_control(),
        "rank11_paid": False,
    }
    digest = hashlib.sha256(
        json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    print(
        "KB_MCA_RANK11_RANK_ONE_ROUTER_INDEPENDENT_PASS "
        f"affine_ray={best_value} core={best_core} proper_r10={proper[-1]} sha256={digest}"
    )


if __name__ == "__main__":
    main()
