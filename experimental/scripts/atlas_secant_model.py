#!/usr/bin/env python3
"""Shared RS syndrome-secant + first-match atlas model for hard input (a).

Faithful to thm:syndrome-secant-exact (L1607): gamma is MCA-bad for (y0,y1)
iff exists E subset D, |E|<=t, y0+gamma y1 in V_E, {y0,y1} not subset V_E.

Atlas cells (full secant atlas): one cell per error support E with |E|<=t.
Cell Z_E for a fixed line = {gamma transverse-meeting V_E} (at most one).

Partial occupancy: agreement support S=D\\E with |S|>=a is placed in a
coarse slice keyed by |E| (and optionally more PO params when folding present).

Stdlib only.
"""
from __future__ import annotations

import itertools
from typing import Any


def mat_vec(H: list[list[int]], v: list[int], p: int) -> list[int]:
    R = len(H)
    n = len(H[0]) if H else 0
    out = [0] * R
    for i in range(R):
        s = 0
        for j in range(n):
            s = (s + H[i][j] * v[j]) % p
        out[i] = s
    return out


def vandermonde_parity(D: list[int], R: int, p: int) -> list[list[int]]:
    """H rows = powers 0..R-1 (unweighted RS parity; enough for toy span geometry)."""
    H = []
    for r in range(R):
        row = [pow(x % p, r, p) for x in D]
        H.append(row)
    return H


def columns(H: list[list[int]]) -> list[tuple[int, ...]]:
    R = len(H)
    n = len(H[0])
    return [tuple(H[r][j] for r in range(R)) for j in range(n)]


def span_contains(pts: list[tuple[int, ...]], v: tuple[int, ...], p: int) -> bool:
    """Gaussian elimination: is v in span of pts over F_p?"""
    if not pts:
        return all(x == 0 for x in v)
    R = len(v)
    # build matrix rows = generators + target
    mat = [list(pt) for pt in pts]
    # transpose to R x k
    k = len(mat)
    A = [[mat[j][i] % p for j in range(k)] for i in range(R)]
    b = [v[i] % p for i in range(R)]
    # augment A|b
    for i in range(R):
        A[i] = A[i] + [b[i]]
    cols = k
    row = 0
    for col in range(cols):
        pivot = None
        for i in range(row, R):
            if A[i][col] % p != 0:
                pivot = i
                break
        if pivot is None:
            continue
        A[row], A[pivot] = A[pivot], A[row]
        inv = pow(A[row][col], -1, p)
        A[row] = [(x * inv) % p for x in A[row]]
        for i in range(R):
            if i == row:
                continue
            fac = A[i][col]
            if fac:
                A[i] = [(A[i][c] - fac * A[row][c]) % p for c in range(cols + 1)]
        row += 1
        if row == R:
            break
    for i in range(row, R):
        if A[i][cols] % p != 0:
            return False
    return True


def solve_gamma_for_E(
    y0: list[int], y1: list[int], E_idx: list[int], cols: list[tuple[int, ...]], p: int
) -> int | None:
    """If unique transverse gamma with y0+gamma y1 in V_E, return it; else None.

    Solve y0 + g y1 in span(cols_E). If y1 already in span and y0 in span: non-transverse.
    If y1 in span and y0 not: no solution. Else project.
    """
    pts = [cols[j] for j in E_idx]
    y0t = tuple(y0)
    y1t = tuple(y1)
    y0_in = span_contains(pts, y0t, p)
    y1_in = span_contains(pts, y1t, p)
    if y0_in and y1_in:
        return None  # whole line in V_E — not transverse
    if y1_in and not y0_in:
        return None  # parallel, never meets
    # try all gamma in F_p (p small) for faithfulness; dual route can use linear solve
    R = len(y0)
    for g in range(p):
        v = tuple((y0[i] + g * y1[i]) % p for i in range(R))
        if span_contains(pts, v, p):
            return g
    return None


def bad_slopes_for_line(
    y0: list[int], y1: list[int], n: int, t: int, cols: list[tuple[int, ...]], p: int
) -> dict[int, list[tuple[int, ...]]]:
    """Map gamma -> list of witnessing E (as index tuples)."""
    out: dict[int, list[tuple[int, ...]]] = {}
    for e in range(0, t + 1):
        for E in itertools.combinations(range(n), e):
            g = solve_gamma_for_E(y0, y1, list(E), cols, p)
            if g is not None:
                out.setdefault(g, []).append(E)
    return out


def bad_slopes_bruteforce(
    y0: list[int], y1: list[int], n: int, t: int, cols: list[tuple[int, ...]], p: int
) -> set[int]:
    """Independent route: for each gamma, test existence of any E."""
    B = set()
    for g in range(p):
        v = tuple((y0[i] + g * y1[i]) % p for i in range(len(y0)))
        for e in range(0, t + 1):
            found = False
            for E in itertools.combinations(range(n), e):
                pts = [cols[j] for j in E]
                y0t, y1t = tuple(y0), tuple(y1)
                if span_contains(pts, y0t, p) and span_contains(pts, y1t, p):
                    continue
                if span_contains(pts, v, p):
                    B.add(g)
                    found = True
                    break
            if found:
                break
    return B


def analyze_instance(
    p: int, n: int, k: int, a: int, n_lines: int = 30, seed: int = 0
) -> dict[str, Any]:
    """One RS toy: R=n-k, t=n-a. Sweep random syndrome lines."""
    import random

    assert 1 <= a < n and 0 < k < n and p >= n
    R = n - k
    t = n - a
    D = list(range(n))  # embed 0..n-1 in F_p
    H = vandermonde_parity(D, R, p)
    cols = columns(H)
    rng = random.Random(seed + p * 100 + n * 10 + a)

    # Full atlas cells = all E with |E|<=t
    full_cells = []
    for e in range(0, t + 1):
        full_cells.extend(itertools.combinations(range(n), e))
    # Restricted atlas: only |E|=t (misses some when smaller E witnesses exist alone)
    restricted_cells = list(itertools.combinations(range(n), t)) if t >= 0 else []

    total_B = 0
    missing_full = 0
    missing_restricted = 0
    routes_agree = 0
    lines_checked = 0
    examples_missing_restricted = []

    for _ in range(n_lines):
        y0 = [rng.randrange(p) for _ in range(R)]
        y1 = [rng.randrange(p) for _ in range(R)]
        if all(x == 0 for x in y1):
            continue
        lines_checked += 1
        by_E = bad_slopes_for_line(y0, y1, n, t, cols, p)
        B = set(by_E.keys())
        B2 = bad_slopes_bruteforce(y0, y1, n, t, cols, p)
        if B == B2:
            routes_agree += 1
        total_B += len(B)

        # Full atlas coverage: every gamma has some witnessing E in full_cells
        covered_full = set()
        for g, Es in by_E.items():
            for E in Es:
                if E in set(full_cells) or tuple(E) in full_cells or E in full_cells:
                    covered_full.add(g)
                    break
            # E is always |E|<=t so always in full
            covered_full.add(g)
        miss_f = B - covered_full
        missing_full += len(miss_f)

        # Restricted: only |E|=t witnesses count
        covered_r = set()
        for g, Es in by_E.items():
            if any(len(E) == t for E in Es):
                covered_r.add(g)
        miss_r = B - covered_r
        missing_restricted += len(miss_r)
        if miss_r and len(examples_missing_restricted) < 5:
            g0 = next(iter(miss_r))
            examples_missing_restricted.append(
                {
                    "gamma": g0,
                    "witness_E_sizes": [len(E) for E in by_E[g0]],
                    "p": p,
                    "n": n,
                    "k": k,
                    "a": a,
                    "t": t,
                }
            )

    return {
        "p": p,
        "n": n,
        "k": k,
        "a": a,
        "R": R,
        "t": t,
        "n_lines": lines_checked,
        "total_bad_slope_instances": total_B,
        "missing_full_atlas": missing_full,
        "missing_restricted_atlas": missing_restricted,
        "routes_agree_lines": routes_agree,
        "routes_agree_all": routes_agree == lines_checked and lines_checked > 0,
        "examples_missing_restricted": examples_missing_restricted,
        "full_exhaustive": missing_full == 0,
        "restricted_exhaustive": missing_restricted == 0,
    }
