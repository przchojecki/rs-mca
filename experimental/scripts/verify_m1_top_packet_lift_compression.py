#!/usr/bin/env python3
"""Verify the M1 top-packet lift/compression identities.

This is a focused checker for
experimental/notes/m1/m1_top_packet_lift_compression.md.  It checks local
Hankel-row identities and finite Johnson-graph combinatorics.  It does not
scan MCA bad slopes and does not prove the global M1 local limit.
"""

from __future__ import annotations

from itertools import combinations
from math import comb
from random import Random


PRIMES = (5, 7, 11, 17)


def add(left: list[int], right: list[int], p: int) -> list[int]:
    return [(a + b) % p for a, b in zip(left, right)]


def sub(left: list[int], right: list[int], p: int) -> list[int]:
    return [(a - b) % p for a, b in zip(left, right)]


def scale(a: int, vector: list[int], p: int) -> list[int]:
    return [(a * value) % p for value in vector]


def mul_x_minus_a(poly: list[int], a: int, p: int) -> list[int]:
    return sub([0] + poly, scale(a, poly + [0], p), p)


def hankel_rows(sequence: list[int], rows: int, poly: list[int], p: int) -> list[int]:
    return [
        sum(sequence[row + col] * coeff for col, coeff in enumerate(poly)) % p
        for row in range(rows)
    ]


def check_triangle_classification() -> int:
    checked = 0
    for n in range(3, 10):
        points = tuple(range(n))
        for j in range(1, n):
            supports = [frozenset(c) for c in combinations(points, j)]
            for triple in combinations(supports, 3):
                if not all(
                    len(left & right) == j - 1
                    for left, right in combinations(triple, 2)
                ):
                    continue
                common = set.intersection(*(set(item) for item in triple))
                union = set.union(*(set(item) for item in triple))
                is_star = len(common) == j - 1
                is_top = len(union) == j + 1 and all(
                    set(item) == union - {next(iter(union - set(item)))}
                    for item in triple
                )
                assert is_star != is_top, (n, j, triple, common, union)
                checked += 1
    return checked


def check_top_row_identity() -> int:
    checked = 0
    rng = Random(20260630)
    for p in PRIMES:
        for _ in range(600):
            j = rng.randrange(1, 9)
            top_member = [rng.randrange(p) for _ in range(j)] + [1]
            x = rng.randrange(p)
            top_locator = mul_x_minus_a(top_member, x, p)
            sequence = [rng.randrange(p) for _ in range(j + 3)]

            top_h1 = hankel_rows(sequence, 1, top_locator, p)[0]
            member_h2 = hankel_rows(sequence, 2, top_member, p)
            assert top_h1 == (member_h2[1] - x * member_h2[0]) % p, (
                p,
                j,
                x,
                top_member,
                top_locator,
                sequence,
                top_h1,
                member_h2,
            )

            # Force H_{1,j+1}(w) ell_U=0 and check the scalar label form
            # H_{2,j}(w)ell_{U\x} = rho_x(w)(1,x).
            forced = [rng.randrange(p) for _ in range(j + 1)]
            partial = sum(forced[col] * top_locator[col] for col in range(j + 1))
            forced.append((-partial * pow(top_locator[j + 1], -1, p)) % p)
            assert hankel_rows(forced, 1, top_locator, p)[0] == 0
            forced_h2 = hankel_rows(forced, 2, top_member, p)
            assert forced_h2[1] == x * forced_h2[0] % p, (
                p,
                j,
                x,
                top_member,
                top_locator,
                forced_h2,
            )
            checked += 1
    return checked


def check_distinct_slope_implication() -> int:
    checked = 0
    for p in PRIMES:
        for a in range(p):
            for b in range(p):
                for z1 in range(p):
                    for z2 in range(p):
                        if z1 == z2:
                            continue
                        if (a + z1 * b) % p == 0 and (a + z2 * b) % p == 0:
                            assert a == 0 and b == 0, (p, a, b, z1, z2)
                        checked += 1
    return checked


def check_compression_injections() -> int:
    checked = 0
    rng = Random(20260630)
    for n in range(4, 10):
        points = tuple(range(n))
        for j in range(1, n - 1):
            supports = [frozenset(c) for c in combinations(points, j)]
            for _ in range(80):
                active = {
                    support
                    for support in supports
                    if rng.randrange(5) == 0
                }
                edge_keys: set[tuple[frozenset[int], tuple[int, int]]] = set()
                triangle_keys: set[tuple[frozenset[int], tuple[int, int, int]]] = set()
                k_top: set[frozenset[int]] = set()

                for top in (frozenset(c) for c in combinations(points, j + 1)):
                    deleted = sorted(x for x in top if top - {x} in active)
                    if len(deleted) >= 2:
                        k_top.add(top)
                    for pair in combinations(deleted, 2):
                        left = top - {pair[0]}
                        right = top - {pair[1]}
                        assert len(left & right) == j - 1
                        edge_keys.add((top, pair))
                    for triple in combinations(deleted, 3):
                        supports_triple = [top - {x} for x in triple]
                        assert all(
                            len(a & b) == j - 1
                            for a, b in combinations(supports_triple, 2)
                        )
                        assert set.union(*(set(item) for item in supports_triple)) == set(top)
                        triangle_keys.add((top, triple))

                assert len(edge_keys) <= comb(j + 1, 2) * len(k_top), (
                    n,
                    j,
                    len(edge_keys),
                    len(k_top),
                )
                assert len(triangle_keys) <= comb(j + 1, 3) * len(k_top), (
                    n,
                    j,
                    len(triangle_keys),
                    len(k_top),
                )
                checked += 1
    return checked


def check_top_kernel_recursion() -> int:
    checked = 0
    rng = Random(20260630)
    for p in PRIMES:
        for _ in range(500):
            r = rng.randrange(1, 7)
            d = rng.randrange(1, 8)
            core = [rng.randrange(p) for _ in range(d)]
            if all(value == 0 for value in core):
                core[rng.randrange(d)] = 1
            sequence = [rng.randrange(p) for _ in range(r + d + 2)]

            core_pad = core + [0]
            x_core = [0] + core
            lifted = hankel_rows(sequence, r + 1, core, p)
            assert hankel_rows(sequence, r, core_pad, p) == lifted[:r]
            assert hankel_rows(sequence, r, x_core, p) == lifted[1 : r + 1]

            y1 = rng.randrange(p)
            y2 = (y1 + 1 + rng.randrange(p - 1)) % p
            ext1 = mul_x_minus_a(core, y1, p)
            ext2 = mul_x_minus_a(core, y2, p)
            diff = sub(ext2, ext1, p)
            assert diff == scale((y1 - y2) % p, core_pad, p)

            # Row-wise implication used in the proof: if both extensions are
            # killed, the padded core and shifted core are killed.
            ext1_rows = hankel_rows(sequence, r, ext1, p)
            ext2_rows = hankel_rows(sequence, r, ext2, p)
            if all(value == 0 for value in ext1_rows) and all(
                value == 0 for value in ext2_rows
            ):
                assert all(value == 0 for value in lifted)
            checked += 1
    return checked


def main() -> None:
    triangle_checks = check_triangle_classification()
    row_checks = check_top_row_identity()
    slope_checks = check_distinct_slope_implication()
    compression_checks = check_compression_injections()
    recursion_checks = check_top_kernel_recursion()

    print("M1 top-packet lift/compression verifier passed")
    print(f"  triangle classifications: {triangle_checks}")
    print(f"  top-row identity/scalar-label checks: {row_checks}")
    print(f"  distinct-slope implication checks: {slope_checks}")
    print(f"  compression injection checks: {compression_checks}")
    print(f"  top-kernel recursion checks: {recursion_checks}")


if __name__ == "__main__":
    main()
