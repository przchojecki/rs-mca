#!/usr/bin/env python3
"""Replay the XR light-profile eliminant nonvanishing schema.

The proof is parametric.  This verifier enumerates small Venn-profile light
triangles, builds the Lambda spaces from Vandermonde moment equations, forms
the normal-form matrix Phi_z, and checks full column rank 3t over a prime
field.  It is a guard against transcription errors in the profile/matrix
schema, not a finite substitute for the theorem.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


P = 1_000_003
SLOPES = (2, 3, 5)
REPO = Path(__file__).resolve().parents[2]
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "xr-light-profile-eliminant-nonvanishing"
    / "xr_light_profile_eliminant_nonvanishing.json"
)


def inv(a: int) -> int:
    if a % P == 0:
        raise ZeroDivisionError("zero inverse")
    return pow(a, P - 2, P)


def rank(matrix: list[list[int]]) -> int:
    if not matrix:
        return 0
    rows = [row[:] for row in matrix]
    nrows, ncols = len(rows), len(rows[0])
    r = 0
    for c in range(ncols):
        pivot = None
        for i in range(r, nrows):
            if rows[i][c] % P:
                pivot = i
                break
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        scale = inv(rows[r][c])
        rows[r] = [(scale * x) % P for x in rows[r]]
        for i in range(nrows):
            if i == r or rows[i][c] % P == 0:
                continue
            factor = rows[i][c]
            rows[i] = [(rows[i][j] - factor * rows[r][j]) % P for j in range(ncols)]
        r += 1
        if r == nrows:
            break
    return r


def rref(matrix: list[list[int]], ncols: int) -> tuple[list[list[int]], list[int]]:
    rows = [row[:] for row in matrix]
    pivots: list[int] = []
    r = 0
    for c in range(ncols):
        pivot = None
        for i in range(r, len(rows)):
            if rows[i][c] % P:
                pivot = i
                break
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        scale = inv(rows[r][c])
        rows[r] = [(scale * x) % P for x in rows[r]]
        for i in range(len(rows)):
            if i == r or rows[i][c] % P == 0:
                continue
            factor = rows[i][c]
            rows[i] = [(rows[i][j] - factor * rows[r][j]) % P for j in range(ncols)]
        pivots.append(c)
        r += 1
        if r == len(rows):
            break
    return rows, pivots


def lambda_basis(points: list[int], k: int) -> list[list[int]]:
    """Return a basis for the k moment-equation nullspace on points."""
    ncols = len(points)
    vandermonde = [[pow(x, d, P) for x in points] for d in range(k)]
    reduced, pivots = rref(vandermonde, ncols)
    assert len(pivots) == k
    pivot_set = set(pivots)
    free_cols = [c for c in range(ncols) if c not in pivot_set]
    basis: list[list[int]] = []
    for free in free_cols:
        vec = [0] * ncols
        vec[free] = 1
        for row, pivot in enumerate(pivots):
            vec[pivot] = (-reduced[row][free]) % P
        basis.append(vec)
    return basis


def profile_supports(
    r: int,
    x01: int,
    x02: int,
    x12: int,
    s0: int,
    s1: int,
    s2: int,
) -> tuple[list[int], list[int], list[int]]:
    point = 1

    def take(count: int) -> list[int]:
        nonlocal point
        out = list(range(point, point + count))
        point += count
        return out

    triple = take(r)
    pair01 = take(x01)
    pair02 = take(x02)
    pair12 = take(x12)
    only0 = take(s0)
    only1 = take(s1)
    only2 = take(s2)
    t0 = triple + pair01 + pair02 + only0
    t1 = triple + pair01 + pair12 + only1
    t2 = triple + pair02 + pair12 + only2
    return t0, t1, t2


def normal_form_rank(t0: list[int], t1: list[int], t2: list[int], k: int) -> int:
    supports = [t0, t1, t2]
    union = sorted(set().union(*supports))
    row_index = {x: i for i, x in enumerate(union)}
    rows = 2 * len(union)
    columns: list[list[int]] = []
    for support, slope in zip(supports, SLOPES):
        for basis_vec in lambda_basis(support, k):
            col = [0] * rows
            for point, value in zip(support, basis_vec):
                idx = row_index[point]
                col[idx] = (col[idx] + value) % P
                col[idx + len(union)] = (col[idx + len(union)] + slope * value) % P
            columns.append(col)
    matrix = [[columns[c][r] for c in range(len(columns))] for r in range(rows)]
    return rank(matrix)


def iter_profiles(max_k: int, max_t: int):
    for k in range(1, max_k + 1):
        for t in range(1, max_t + 1):
            a = k + t
            for r in range(0, min(k, a) + 1):
                for x01 in range(a - r + 1):
                    for x02 in range(a - r + 1):
                        s0 = a - r - x01 - x02
                        if s0 < 0:
                            continue
                        for x12 in range(a - r + 1):
                            s1 = a - r - x01 - x12
                            s2 = a - r - x02 - x12
                            if s1 < 0 or s2 < 0:
                                continue
                            pair_sum_minus_triple = x01 + x02 + x12 + 2 * r
                            if pair_sum_minus_triple > 2 * k:
                                continue
                            yield {
                                "k": k,
                                "t": t,
                                "A": a,
                                "triple": r,
                                "pair_only": [x01, x02, x12],
                                "single_only": [s0, s1, s2],
                                "pair_sum_minus_triple": pair_sum_minus_triple,
                            }


def verify(max_k: int, max_t: int) -> dict[str, object]:
    checked = 0
    by_shape: dict[str, int] = {}
    max_union = 0
    for profile in iter_profiles(max_k, max_t):
        k = int(profile["k"])
        t = int(profile["t"])
        r = int(profile["triple"])
        x01, x02, x12 = profile["pair_only"]
        s0, s1, s2 = profile["single_only"]
        t0, t1, t2 = profile_supports(r, x01, x02, x12, s0, s1, s2)
        union_size = len(set().union(t0, t1, t2))
        max_union = max(max_union, union_size)
        assert profile["pair_sum_minus_triple"] >= 2 * r
        assert r <= k
        got = normal_form_rank(t0, t1, t2, k)
        want = 3 * t
        if got != want:
            raise AssertionError((profile, got, want))
        checked += 1
        key = f"k={k},t={t}"
        by_shape[key] = by_shape.get(key, 0) + 1
    return {
        "schema": "xr-light-profile-eliminant-nonvanishing-v1",
        "status": "PROVED_SCHEMA_REPLAY",
        "field": f"F_{P}",
        "slopes": list(SLOPES),
        "max_k": max_k,
        "max_t": max_t,
        "profiles_checked": checked,
        "profiles_by_k_t": by_shape,
        "max_union_size": max_union,
        "checks": [
            "pair_sum_minus_triple >= 2 * triple_intersection",
            "light condition implies triple_intersection <= k",
            "rank(Phi_z) == 3t for every enumerated profile",
        ],
        "note": "Finite replay of the normal-form schema; the proof note supplies the parametric theorem.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-k", type=int, default=6)
    parser.add_argument("--max-t", type=int, default=5)
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()

    cert = verify(args.max_k, args.max_t)
    if args.emit:
        ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
        ARTIFACT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
        print(f"wrote {ARTIFACT.relative_to(REPO)}")
    print(
        "PASS: XR light-profile eliminant nonvanishing schema "
        f"({cert['profiles_checked']} profiles)"
    )


if __name__ == "__main__":
    main()
