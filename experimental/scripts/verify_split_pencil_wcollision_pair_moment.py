#!/usr/bin/env python3
"""Verify the split-pencil W-collision pair-moment identity.

This is a small stdlib replay of the bookkeeping identities:
T1 pair-moment double count, T2 codeword-pair fiber structure,
T3 regrouping by (f,g), and T4 pencil collapse mult(W)=L(P_W,Q_W).
"""

from __future__ import annotations

import itertools
import random
from math import comb

Q = 17
N = 8
K = 4
T = 2
A = K + T
D = list(range(1, N + 1))


def inv(a: int) -> int:
    return pow(a % Q, Q - 2, Q)


def polymul(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j, bj in enumerate(b):
            if bj:
                out[i + j] = (out[i + j] + ai * bj) % Q
    return tuple(out)


def interp_coeffs(xs: tuple[int, ...], ys: tuple[int, ...]) -> tuple[int, ...]:
    """Degree < K interpolation through K points."""
    assert len(xs) == K and len(ys) == K
    coeff = [0] * K
    for i, xi in enumerate(xs):
        num = (1,)
        den = 1
        for j, xj in enumerate(xs):
            if j == i:
                continue
            num = polymul(num, ((-xj) % Q, 1))
            den = den * ((xi - xj) % Q) % Q
        weight = ys[i] * inv(den) % Q
        for degree, value in enumerate(num):
            coeff[degree] = (coeff[degree] + weight * value) % Q
    return tuple(coeff)


def eval_poly(coeffs: tuple[int, ...], x: int) -> int:
    value = 0
    for coeff in reversed(coeffs):
        value = (value * x + coeff) % Q
    return value


def random_case(seed: int) -> tuple[str, list[int], list[int]]:
    rng = random.Random(seed)
    u = [rng.randrange(Q) for _ in range(N)]
    v = [rng.randrange(1, Q) for _ in range(N)]
    return f"random-seed-{seed}", u, v


def planted_pencil_case() -> tuple[str, list[int], list[int]]:
    f = (3, 5, 1, 2)
    g = (1, 0, 0, 0)
    u = [eval_poly(f, x) for x in D]
    v = [eval_poly(g, x) for x in D]
    return "planted-pencil", u, v


def enumerate_rays(u: list[int], v: list[int]) -> dict[tuple[int, tuple[int, ...]], frozenset[int]]:
    rays: dict[tuple[int, tuple[int, ...]], frozenset[int]] = {}
    ksets = list(itertools.combinations(range(N), K))
    for z in range(Q):
        uz = [(u[i] + z * v[i]) % Q for i in range(N)]
        seen: set[tuple[int, ...]] = set()
        for wset in ksets:
            coeffs = interp_coeffs(
                tuple(D[i] for i in wset),
                tuple(uz[i] for i in wset),
            )
            if coeffs in seen:
                continue
            seen.add(coeffs)
            support = frozenset(
                i for i in range(N) if eval_poly(coeffs, D[i]) == uz[i]
            )
            if len(support) >= A:
                rays[(z, coeffs)] = support
    return rays


def live_count_for_pair(
    rays: dict[tuple[int, tuple[int, ...]], frozenset[int]],
    f: tuple[int, ...],
    g: tuple[int, ...],
) -> int:
    total = 0
    for z in range(Q):
        coeffs = tuple((f[i] + z * g[i]) % Q for i in range(K))
        if (z, coeffs) in rays:
            total += 1
    return total


def verify_case(label: str, u: list[int], v: list[int]) -> dict[str, object]:
    rays = enumerate_rays(u, v)
    ray_items = list(rays.items())
    ksets = list(itertools.combinations(range(N), K))

    mult: dict[tuple[int, ...], int] = {}
    for (_ray, support) in ray_items:
        for wset in itertools.combinations(sorted(support), K):
            mult[wset] = mult.get(wset, 0) + 1

    lhs = sum(comb(m, 2) for m in mult.values())
    rhs = 0
    groups: dict[tuple[tuple[int, ...], tuple[int, ...]], set[int]] = {}
    joint_size: dict[tuple[tuple[int, ...], tuple[int, ...]], int] = {}
    j_profile: dict[int, int] = {}
    cross_pairs = 0

    for i in range(len(ray_items)):
        (z1, c1), s1 = ray_items[i]
        for j in range(i + 1, len(ray_items)):
            (z2, c2), s2 = ray_items[j]
            intersection = s1 & s2
            if z1 == z2:
                assert len(intersection) <= K - 1, (label, "same-slope core")
                continue

            cross_pairs += 1
            j_size = len(intersection)
            rhs += comb(j_size, K)
            if j_size >= K:
                j_profile[j_size] = j_profile.get(j_size, 0) + 1

            dz_inv = inv(z1 - z2)
            g = tuple((c1[d] - c2[d]) * dz_inv % Q for d in range(K))
            f = tuple((c1[d] - z1 * g[d]) % Q for d in range(K))
            joint = frozenset(
                idx
                for idx, x in enumerate(D)
                if eval_poly(f, x) == u[idx] and eval_poly(g, x) == v[idx]
            )
            assert joint == intersection, (label, "T2 fiber mismatch")

            if j_size >= K:
                key = (f, g)
                groups.setdefault(key, set()).update((z1, z2))
                joint_size[key] = j_size

    assert lhs == rhs, (label, "T1 pair moment", lhs, rhs)

    t3_total = 0
    for (f, g), slopes in groups.items():
        live = live_count_for_pair(rays, f, g)
        assert live == len(slopes), (label, "T3 live count", live, len(slopes))
        t3_total += comb(live, 2) * comb(joint_size[(f, g)], K)
    assert t3_total == lhs, (label, "T3 regroup", t3_total, lhs)

    for wset in ksets:
        p_w = interp_coeffs(tuple(D[i] for i in wset), tuple(u[i] for i in wset))
        q_w = interp_coeffs(tuple(D[i] for i in wset), tuple(v[i] for i in wset))
        live = live_count_for_pair(rays, p_w, q_w)
        assert live == mult.get(wset, 0), (
            label,
            "T4 pencil collapse",
            wset,
            live,
            mult.get(wset, 0),
        )

    return {
        "label": label,
        "rays": len(rays),
        "cross_pairs": cross_pairs,
        "pair_moment": lhs,
        "collision_cores": sum(1 for m in mult.values() if m >= 2),
        "max_mult": max(mult.values(), default=0),
        "j_profile": dict(sorted(j_profile.items())),
    }


def main() -> None:
    cases = [random_case(13), planted_pencil_case()]
    for label, u, v in cases:
        result = verify_case(label, u, v)
        print(
            f"{result['label']}: rays={result['rays']} "
            f"cross_pairs={result['cross_pairs']} "
            f"pair_moment={result['pair_moment']} "
            f"collision_cores={result['collision_cores']} "
            f"max_mult={result['max_mult']} "
            f"J={result['j_profile']}"
        )
    print("SPLIT_PENCIL_WCOLLISION_PAIR_MOMENT_PASS")


if __name__ == "__main__":
    main()
