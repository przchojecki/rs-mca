#!/usr/bin/env python3
"""M5 (towards-prize.md M5 / S8 item 6): FIRST singular-bucket pivot packet --
bucket identification at the underdetermined boundary A=384 of
C = RS[F_17^32, H, 256]  (n=512, k=256, q_line=17^32).

For exact agreement A the v12 Hankel system (extractor convention,
experimental/scripts/extract_regular_hankel_minors.py: rows range(t),
cols range(j+1), entry S[row+col], S = syndrome window of u + Z*v) is
t x (j+1) with t = A-k equations on j+1 = n-A+1 locator coefficients.
The regular root-containment certificate needs t >= j+1  <=>  2A >= n+k+1.

A=384 is the MAXIMAL underdetermined agreement: t = j = 128, the matrix is
128 x 129, rank <= 128 < 129, so the kernel is nontrivial for EVERY slope Z
and kernel-nonemptiness certifies nothing.  This script identifies that bucket
exactly, demonstrates the regular/underdetermined dichotomy over a toy field,
checks the deficiency-1 Cramer kernel vector, and verifies the rank-drop
split-locator deduplication lemma and top-chart divisibility filter on finite
toy subgroups.

Run:  python3 experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py
Exit non-zero iff any implemented check fails.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from itertools import combinations
from itertools import permutations
from pathlib import Path

Q = 17 ** 32          # q_line = |F|
TWO128 = 2 ** 128
N, K = 512, 256
A_STAR = 384          # the maximal underdetermined exact agreement

REPO = Path(__file__).resolve().parents[2]
ARTIFACT = (
    REPO / "experimental" / "data" / "certificates"
    / "hankel-f17-32-m5-underdetermined-a384"
    / "f17_32_n512_k256_a384_m5_residual_packet.json"
)
NOTE_REF = "experimental/notes/m5/m5_underdetermined_a384_pivot_packet.md"


def rank_and_kernel_mod_p(matrix, p):
    """RREF over F_p (small toy sizes): return (rank, one kernel vector or None)."""
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    m = [[x % p for x in row] for row in matrix]
    pivot_cols = []
    r = 0
    for c in range(cols):
        pivot = next((i for i in range(r, rows) if m[i][c]), None)
        if pivot is None:
            continue
        m[r], m[pivot] = m[pivot], m[r]
        inv = pow(m[r][c], -1, p)
        m[r] = [(x * inv) % p for x in m[r]]
        for i in range(rows):
            if i != r and m[i][c]:
                f = m[i][c]
                m[i] = [(x - f * y) % p for x, y in zip(m[i], m[r])]
        pivot_cols.append(c)
        r += 1
        if r == rows:
            break
    rank = len(pivot_cols)
    free = [c for c in range(cols) if c not in pivot_cols]
    if not free:
        return rank, None
    vec = [0] * cols
    vec[free[0]] = 1
    for i, c in enumerate(pivot_cols):
        vec[c] = (-m[i][free[0]]) % p
    return rank, vec


def hankel(window, t, j):
    """Extractor convention: t rows, j+1 cols, entry window[row+col]."""
    return [[window[row + col] for col in range(j + 1)] for row in range(t)]


def det_mod_p(matrix, p):
    """Determinant over F_p for small square matrices."""
    n = len(matrix)
    m = [[x % p for x in row] for row in matrix]
    det = 1
    for c in range(n):
        pivot = next((i for i in range(c, n) if m[i][c]), None)
        if pivot is None:
            return 0
        if pivot != c:
            m[c], m[pivot] = m[pivot], m[c]
            det = (-det) % p
        pivot_val = m[c][c]
        det = (det * pivot_val) % p
        inv = pow(pivot_val, -1, p)
        for r in range(c + 1, n):
            if m[r][c]:
                f = (m[r][c] * inv) % p
                for cc in range(c, n):
                    m[r][cc] = (m[r][cc] - f * m[c][cc]) % p
    return det % p


def cramer_vector(matrix, p):
    """Signed maximal minors for a j x (j+1) deficiency-one matrix."""
    rows = len(matrix)
    cols = len(matrix[0])
    assert cols == rows + 1
    out = []
    for omitted in range(cols):
        minor = [[row[c] for c in range(cols) if c != omitted] for row in matrix]
        sign = -1 if omitted % 2 else 1
        out.append((sign * det_mod_p(minor, p)) % p)
    return out


def mat_vec_zero(matrix, vec, p):
    return all(sum(row[i] * vec[i] for i in range(len(vec))) % p == 0
               for row in matrix)


def poly_mul_mod_p(a, b, p):
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] = (out[i + j] + ai * bj) % p
    return out


def poly_trim(poly):
    out = [x for x in poly]
    while out and out[-1] == 0:
        out.pop()
    return out or [0]


def ztrim(poly):
    return poly_trim(poly)


def zadd(a, b, p):
    n = max(len(a), len(b))
    return ztrim([((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)) % p
                  for i in range(n)])


def zsub(a, b, p):
    n = max(len(a), len(b))
    return ztrim([((a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0)) % p
                  for i in range(n)])


def zmul(a, b, p):
    return poly_mul_mod_p(a, b, p)


def zscale(a, c, p):
    return ztrim([(c * x) % p for x in a])


def zdegree(a):
    a = ztrim(a)
    return -1 if a == [0] else len(a) - 1


def zeval(a, z, p):
    return eval_poly_mod_p(a, z, p)


def zmonic(a, p):
    a = ztrim(a)
    if a == [0]:
        return [0]
    return zscale(a, pow(a[-1], -1, p), p)


def zdivmod(numer, denom, p):
    """Return quotient, remainder for low-to-high polynomials in Z over F_p."""
    numer = ztrim([x % p for x in numer])
    denom = ztrim([x % p for x in denom])
    if denom == [0]:
        raise ZeroDivisionError("zero Z-polynomial")
    if zdegree(numer) < zdegree(denom):
        return [0], numer
    rem = numer[:]
    quot = [0] * (zdegree(numer) - zdegree(denom) + 1)
    inv_lc = pow(denom[-1], -1, p)
    while zdegree(rem) >= zdegree(denom) and rem != [0]:
        shift = zdegree(rem) - zdegree(denom)
        coeff = rem[-1] * inv_lc % p
        quot[shift] = coeff
        for i, di in enumerate(denom):
            rem[shift + i] = (rem[shift + i] - coeff * di) % p
        rem = ztrim(rem)
    return ztrim(quot), ztrim(rem)


def zgcd(a, b, p):
    """Monic gcd in F_p[Z]."""
    a = ztrim(a)
    b = ztrim(b)
    while b != [0]:
        _, r = zdivmod(a, b, p)
        a, b = b, r
    return zmonic(a, p)


def zsaturate_away(poly, forbidden_factor, p):
    """Remove all common factors with the top-chart boundary factor."""
    out = zmonic(poly, p)
    forbidden_factor = zmonic(forbidden_factor, p)
    while out != [0]:
        shared = zgcd(out, forbidden_factor, p)
        if zdegree(shared) <= 0:
            break
        out, rem = zdivmod(out, shared, p)
        if rem != [0]:
            raise AssertionError("internal error: gcd did not divide polynomial")
        out = zmonic(out, p)
    return out


def zroots(poly, p):
    if poly == [0]:
        return list(range(p))
    return [z for z in range(p) if zeval(poly, z, p) == 0]


def permutation_sign(perm):
    inv = 0
    for i in range(len(perm)):
        for j in range(i + 1, len(perm)):
            inv += int(perm[i] > perm[j])
    return -1 if inv % 2 else 1


def det_zpoly(matrix, p):
    n = len(matrix)
    out = [0]
    for perm in permutations(range(n)):
        term = [1]
        for r, c in enumerate(perm):
            term = zmul(term, matrix[r][c], p)
        out = zadd(out, zscale(term, permutation_sign(perm), p), p)
    return out


def cramer_vector_zpoly(matrix, p):
    rows = len(matrix)
    cols = len(matrix[0])
    assert cols == rows + 1
    out = []
    for omitted in range(cols):
        minor = [[row[c] for c in range(cols) if c != omitted] for row in matrix]
        out.append(zscale(det_zpoly(minor, p), -1 if omitted % 2 else 1, p))
    return out


def pseudo_remainder_x_over_z(dividend, divisor, p):
    """Pseudo-remainder in F_p[z][X], low-to-high in X and z."""
    rem = [ztrim(c) for c in dividend]
    divisor = [ztrim(c) for c in divisor]
    divisor_degree = len(divisor) - 1
    lc_divisor = divisor[-1]
    while len(rem) - 1 >= divisor_degree and rem != [[0]]:
        rem_degree = len(rem) - 1
        shift = rem_degree - divisor_degree
        lc_rem = rem[-1]
        scaled = [zmul(lc_divisor, c, p) for c in rem]
        subtract = [[0] for _ in range(shift)] + [zmul(lc_rem, c, p) for c in divisor]
        n = max(len(scaled), len(subtract))
        new_rem = []
        for i in range(n):
            a = scaled[i] if i < len(scaled) else [0]
            b = subtract[i] if i < len(subtract) else [0]
            new_rem.append(zsub(a, b, p))
        while new_rem and new_rem[-1] == [0]:
            new_rem.pop()
        rem = new_rem or [[0]]
    return rem


def poly_divmod_mod_p(numer, denom, p):
    """Return quotient, remainder for low-to-high polynomials over F_p."""
    numer = poly_trim([x % p for x in numer])
    denom = poly_trim([x % p for x in denom])
    if denom == [0]:
        raise ZeroDivisionError("zero polynomial")
    if len(numer) < len(denom):
        return [0], numer
    rem = numer[:]
    quot = [0] * (len(numer) - len(denom) + 1)
    inv_lc = pow(denom[-1], -1, p)
    while len(rem) >= len(denom) and rem != [0]:
        shift = len(rem) - len(denom)
        coeff = rem[-1] * inv_lc % p
        quot[shift] = coeff
        for i, di in enumerate(denom):
            rem[shift + i] = (rem[shift + i] - coeff * di) % p
        rem = poly_trim(rem)
    return poly_trim(quot), rem


def locator_poly(roots, p):
    """Low-to-high coefficients of prod_{r in roots} (X-r)."""
    poly = [1]
    for r in roots:
        poly = poly_mul_mod_p(poly, [(-r) % p, 1], p)
    return poly


def divides_x_order_minus_one(poly, order, p):
    target = [(-1) % p] + [0] * (order - 1) + [1]
    _, rem = poly_divmod_mod_p(target, poly, p)
    return rem == [0]


def pseudo_remainder_degree_bound(dividend_degree, divisor_degree, coeff_degree_bound):
    """Degree-in-Z bound for pseudo-remainder of X^N-1 by a degree-j divisor.

    If every coefficient of C_Z(X)=sum_{i=0}^j c_i(Z)X^i has Z-degree at most d
    and c_j is not identically zero, pseudo-division performs N-j+1 reduction
    steps.  Each step multiplies by c_j and subtracts a leading coefficient
    times C_Z, increasing the Z-degree bound by at most d.
    """
    if dividend_degree < divisor_degree:
        return 0
    steps = dividend_degree - divisor_degree + 1
    return steps * coeff_degree_bound


def split_roots_in_domain(poly, domain, expected_degree, p):
    poly = poly_trim(poly)
    if len(poly) - 1 != expected_degree or poly[-1] == 0:
        return False
    roots = [x for x in domain if eval_poly_mod_p(poly, x, p) == 0]
    return len(roots) == expected_degree


def eval_poly_mod_p(poly, x, p):
    value = 0
    power = 1
    for coeff in poly:
        value = (value + coeff * power) % p
        power = (power * x) % p
    return value


def moments_from_support(roots, weights, length, p):
    return [sum(w * pow(r, m, p) for r, w in zip(roots, weights)) % p
            for m in range(length)]


def subgroup_of_order(p, order):
    for g in range(2, p):
        if pow(g, order, p) != 1:
            continue
        if all(pow(g, d, p) != 1 for d in range(1, order)):
            return [pow(g, i, p) for i in range(order)]
    raise ValueError(f"no element of order {order} in F_{p}")


def check_bucket_identification():
    """Exact arithmetic identifying A=384 as the first (maximal, deficiency-1)
    underdetermined bucket of the F_17^32 row, in the extractor's convention."""
    d = []
    ok = True
    b_q = Q // TWO128
    d.append(f"row gate context: B_Q = floor(17^32/2^128) = {b_q}")
    ok &= (b_q == 6)

    def regular(a):
        return (a - K) >= (N - a) + 1

    sweep_ok = all(regular(a) == (2 * a >= N + K + 1) for a in range(K + 1, N + 1))
    d.append(f"regular(A) := t >= j+1  <=>  2A >= n+k+1 = {N + K + 1}, swept A in [{K + 1},{N}] : {sweep_ok}")
    boundary_ok = regular(385) and not regular(384)
    maximal_ok = (all(regular(a) for a in range(385, N + 1))
                  and all(not regular(a) for a in range(K + 1, 385)))
    d.append(f"boundary: A=385 regular (t=129 >= j+1=128), A=384 NOT (t=128 < j+1=129); "
             f"A=384 maximal underdetermined : {boundary_ok and maximal_ok}")
    ok &= sweep_ok and boundary_ok and maximal_ok

    t, j = A_STAR - K, N - A_STAR
    d.append(f"A={A_STAR}: t = A-k = {t} equations, j+1 = n-A+1 = {j + 1} locator coefficients "
             f"=> matrix {t} x {j + 1} (extractor rows/cols convention)")
    deficiency = (j + 1) - t
    d.append(f"deficiency (j+1)-t = {deficiency}; rank <= min({t},{j + 1}) = {min(t, j + 1)} < {j + 1} "
             f"=> nontrivial kernel for EVERY slope Z (kernel-nonemptiness vacuous)")
    ok &= (t, j) == (128, 128) and deficiency == 1

    window_ok = all((a - K) + (N - a) == N - K for a in range(K + 1, N + 1))
    d.append(f"syndrome window t+j = n-k = {N - K} for every exact agreement (A-independent) : {window_ok}")
    n_under = sum(1 for a in range(K + 1, N + 1) if not regular(a))
    d.append(f"underdetermined buckets with t >= 1: A in [257, 384], count = {n_under}; "
             f"A=384 uniquely has deficiency 1 (deficiency = n+k+1-2A grows to {N + K + 1 - 2 * 257} at A=257)")
    ok &= window_ok and n_under == 128 and (N + K + 1 - 2 * A_STAR) == 1
    return ok, d


def check_toy_dichotomy():
    """Exhaustive toy demonstration over F_13: ONE fixed length-8 window u + z*v,
    split 4x5 (underdetermined, t=j=4 -- the A=384 shape) vs 5x4 (regular, t=5,
    j=3).  Underdetermined: a VERIFIED kernel vector exists at ALL 13 slopes.
    Regular: full column rank except at few slopes (the certificate has content)."""
    p = 13
    u = [1, 2, 3, 4, 5, 6, 7, 8]
    v = [8, 1, 5, 2, 9, 3, 7, 4]
    d = []
    ok = True
    kernel_at_all = True
    kernel_verified = True
    under_dim_ge2 = []
    regular_drop = []
    for z in range(p):
        s = [(a + z * b) % p for a, b in zip(u, v)]
        m_u = hankel(s, 4, 4)                      # 4 x 5, deficiency 1
        rank_u, vec = rank_and_kernel_mod_p(m_u, p)
        if vec is None:
            kernel_at_all = False
        else:
            prods = [sum(row[i] * vec[i] for i in range(5)) % p for row in m_u]
            if any(prods) or all(x == 0 for x in vec):
                kernel_verified = False
        if rank_u < 4:
            under_dim_ge2.append(z)
        m_r = hankel(s, 5, 3)                      # 5 x 4, regular analogue
        rank_r, _ = rank_and_kernel_mod_p(m_r, p)
        if rank_r < 4:
            regular_drop.append(z)
    d.append(f"underdetermined 4x5: explicit kernel vector found AND verified (M.v = 0, v != 0) "
             f"at ALL {p} slopes : {kernel_at_all and kernel_verified}")
    ok &= kernel_at_all and kernel_verified
    d.append(f"underdetermined 4x5: kernel dim exactly 1 at {p - len(under_dim_ge2)}/{p} slopes "
             f"(rank-drop slopes {under_dim_ge2} are the M5 'rank-drop singular' sub-bucket)")
    ok &= (p - len(under_dim_ge2)) >= 1          # genericity witness for the turn-2 Cramer lemma
    d.append(f"regular 5x4 (same windows): full column rank except at {len(regular_drop)} slope(s) "
             f"{regular_drop} -- root-containment there has content, unlike the 4x5 split")
    ok &= len(regular_drop) < p
    return ok, d


def check_cramer_kernel_vector():
    """For a deficiency-one j x (j+1) Hankel matrix, the signed maximal-minor
    vector is in the kernel.  It is nonzero exactly on the full-row-rank chart."""
    p = 13
    u = [1, 2, 3, 4, 5, 6, 7, 8]
    v = [8, 1, 5, 2, 9, 3, 7, 4]
    d = []
    ok = True
    full_rank = zero_cramer = 0
    rank_drop = []
    for z in range(p):
        s = [(a + z * b) % p for a, b in zip(u, v)]
        m = hankel(s, 4, 4)
        rank, _ = rank_and_kernel_mod_p(m, p)
        c = cramer_vector(m, p)
        ok &= mat_vec_zero(m, c, p)
        if rank == 4:
            full_rank += 1
            ok &= any(c)
        else:
            rank_drop.append(z)
            zero_cramer += int(all(x == 0 for x in c))
            ok &= all(x == 0 for x in c)
    d.append(f"signed maximal-minor vector c_i=(-1)^i det(M_i) satisfies M.c=0 "
             f"for all {p} toy slopes")
    d.append(f"full-row-rank chart: c != 0 at {full_rank}/{p} slopes; "
             f"rank-drop chart: c = 0 at {zero_cramer}/{len(rank_drop)} slopes {rank_drop}")
    ok &= full_rank > 0 and zero_cramer == len(rank_drop)
    return ok, d


def check_rankdrop_split_locator_dedup():
    """Toy subgroup verification of the rank-drop converse.

    If a degree-j split locator L_R is in the kernel and the moment Hankel block
    has rank < j, then the same moment window is supported on a proper subset of
    R.  The lower-degree locator of that active subset is also in the kernel, so
    the slope belongs to a higher-agreement bucket and is not new exact-A mass.
    """
    p = 97
    h = subgroup_of_order(p, 8)
    j = 4
    cases = rank_drop_cases = full_rank_cases = 0
    ok = True
    for roots in combinations(h, j):
        roots = list(roots)
        full_locator = locator_poly(roots, p)
        for mask in range(1, 1 << j):
            active = [roots[i] for i in range(j) if (mask >> i) & 1]
            weights = [(11 + 7 * i) % p for i in range(len(active))]
            window = moments_from_support(active, weights, 2 * j, p)
            m = hankel(window, j, j)
            rank, _ = rank_and_kernel_mod_p(m, p)
            cases += 1
            ok &= mat_vec_zero(m, full_locator, p)
            ok &= (rank == len(active))
            if rank < j:
                rank_drop_cases += 1
                lower_locator = locator_poly(active, p)
                padded = lower_locator + [0] * (j + 1 - len(lower_locator))
                ok &= len(lower_locator) - 1 < j
                ok &= mat_vec_zero(m, padded, p)
            else:
                full_rank_cases += 1
    d = [
        f"F_{p} toy subgroup |H|=8, deficiency-one shape j=t={j}: checked "
        f"{cases} active-support patterns over all degree-{j} split locators",
        f"rank factorization verified: rank equals active support size in every case; "
        f"full-rank cases {full_rank_cases}, rank-drop cases {rank_drop_cases}",
        "for every rank-drop case, the lower-degree active-support locator is also "
        "in the kernel, giving the higher-agreement dedup witness",
    ]
    return ok, d


def check_top_chart_splitting_filter():
    """Top-chart locator validity equals divisibility by X^|H|-1.

    In a full-row-rank deficiency-one chart, the Cramer vector spans the unique
    kernel.  If its top coefficient is nonzero, it gives a degree-j locator.
    Since H is the full root set of X^|H|-1 and char does not divide |H|, this
    locator is valid exactly when it divides X^|H|-1.
    """
    ok = True
    d = []

    p = 13
    h = list(range(1, p))
    u = [1, 2, 3, 4, 5, 6, 7, 8]
    v = [8, 1, 5, 2, 9, 3, 7, 4]
    j = 4
    top = split = non_split = 0
    mismatches = []
    for z in range(p):
        s = [(a + z * b) % p for a, b in zip(u, v)]
        m = hankel(s, j, j)
        rank, _ = rank_and_kernel_mod_p(m, p)
        c = cramer_vector(m, p)
        if rank == j and c[-1] != 0:
            top += 1
            by_roots = split_roots_in_domain(c, h, j, p)
            by_division = divides_x_order_minus_one(c, len(h), p)
            split += int(by_roots)
            non_split += int(not by_roots)
            if by_roots != by_division:
                mismatches.append((z, c, by_roots, by_division))
    ok &= top > 0 and not mismatches
    d.append(f"F_{p} toy pencil: checked {top} full-rank top-chart slopes; "
             f"split={split}, non-split={non_split}, divisibility mismatches={len(mismatches)}")

    p2 = 97
    h2 = subgroup_of_order(p2, 8)
    positive_cases = 0
    for roots in combinations(h2, j):
        roots = list(roots)
        weights = [(19 + 5 * i) % p2 for i in range(j)]
        window = moments_from_support(roots, weights, 2 * j, p2)
        m = hankel(window, j, j)
        rank, _ = rank_and_kernel_mod_p(m, p2)
        c = cramer_vector(m, p2)
        top_chart = rank == j and c[-1] != 0
        by_roots = split_roots_in_domain(c, h2, j, p2)
        by_division = divides_x_order_minus_one(c, len(h2), p2)
        ok &= top_chart and by_roots and by_division and mat_vec_zero(m, c, p2)
        positive_cases += 1
    d.append(f"F_{p2} planted split top-chart cases: verified {positive_cases} "
             f"degree-{j} locators divide X^{len(h2)}-1 and are Cramer kernels")
    d.append("top-chart conclusion: valid split locator <=> Cramer locator divides X^|H|-1; "
             "otherwise the slope is not exact-A bad on this chart")
    return ok, d


def check_pseudoremainder_degree_budget():
    """Verify the degree budget used for the top-chart eliminant."""
    ok = True
    d = []
    j = N - A_STAR
    t = A_STAR - K
    cap = pseudo_remainder_degree_bound(N, j, t)
    resultant_cap = N * t
    d.append(f"F_17^32 A={A_STAR}: j={j}, t={t}, pseudo-remainder degree cap "
             f"(n-j+1)*t = {cap}")
    d.append(f"rough resultant cap n*t = {resultant_cap}; pseudo cap improves it by "
             f"{resultant_cap - cap}")
    ok &= (j, t, cap, resultant_cap) == (128, 128, 49280, 65536)

    toy_cap = pseudo_remainder_degree_bound(8, 4, 4)
    d.append(f"toy |H|=8, j=t=4: pseudo-remainder degree cap = {toy_cap}")
    ok &= toy_cap == 20
    monotone = all(
        pseudo_remainder_degree_bound(n, jj, dd)
        == (n - jj + 1) * dd
        for n in range(4, 17)
        for jj in range(1, n + 1)
        for dd in range(0, 7)
    )
    d.append(f"degree-recursion sweep for 4 <= n <= 16, 1 <= j <= n, 0 <= d <= 6: {monotone}")
    ok &= monotone
    return ok, d


def check_toy_pseudoremainder_root_table():
    """Declared affine toy family with a replayed top-chart root table.

    The family is built from two planted split moment windows at z=0 and z=1:
    W(z)=W0+z(W1-W0).  The replay enumerates all slopes, applies the Cramer
    top-chart test, and records exactly those slopes whose Cramer locator
    divides X^|H|-1.
    """
    p = 97
    h = subgroup_of_order(p, 8)
    j = 4
    roots0 = tuple(h[:j])
    roots1 = tuple(h[2:2 + j])
    weights0 = [3, 7, 11, 19]
    weights1 = [5, 13, 17, 23]
    w0 = moments_from_support(roots0, weights0, 2 * j, p)
    w1 = moments_from_support(roots1, weights1, 2 * j, p)
    delta = [(b - a) % p for a, b in zip(w0, w1)]
    root_table = []
    rank_drop = low_degree = top_nonroots = 0
    planted_ok = True
    for z in range(p):
        window = [(a + z * b) % p for a, b in zip(w0, delta)]
        m = hankel(window, j, j)
        rank, _ = rank_and_kernel_mod_p(m, p)
        c = cramer_vector(m, p)
        if rank < j:
            rank_drop += 1
            continue
        if c[-1] == 0:
            low_degree += 1
            continue
        if divides_x_order_minus_one(c, len(h), p):
            roots = [x for x in h if eval_poly_mod_p(c, x, p) == 0]
            root_table.append({
                "slope": z,
                "roots": roots,
                "locator": poly_trim(c),
            })
        else:
            top_nonroots += 1
    slopes = {row["slope"] for row in root_table}
    planted_ok &= 0 in slopes and 1 in slopes
    for row in root_table:
        if row["slope"] == 0:
            planted_ok &= set(row["roots"]) == set(roots0)
        if row["slope"] == 1:
            planted_ok &= set(row["roots"]) == set(roots1)
    ok = planted_ok and len(root_table) >= 2 and rank_drop + low_degree + top_nonroots + len(root_table) == p
    d = [
        f"declared F_{p}, |H|=8, j=t={j} affine family W(z)=W0+z(W1-W0)",
        f"root table slopes = {[row['slope'] for row in root_table]} "
        f"(rank_drop={rank_drop}, low_degree={low_degree}, top_nonroots={top_nonroots})",
        "planted split slopes z=0 and z=1 are recovered with the planted root sets: "
        f"{planted_ok}",
        "root-table rule: enumerate full-rank top-chart slopes and retain exactly "
        "those with zero pseudo-remainder modulo the Cramer locator",
    ]
    return ok, d


def check_toy_root_containment_certificate():
    """Symbolic pseudo-remainder coefficient contains the toy root table."""
    p = 97
    h = subgroup_of_order(p, 8)
    j = 4
    roots0 = tuple(h[:j])
    roots1 = tuple(h[2:2 + j])
    weights0 = [3, 7, 11, 19]
    weights1 = [5, 13, 17, 23]
    w0 = moments_from_support(roots0, weights0, 2 * j, p)
    w1 = moments_from_support(roots1, weights1, 2 * j, p)
    delta = [(b - a) % p for a, b in zip(w0, w1)]
    matrix = [
        [[w0[row + col] % p, delta[row + col] % p] for col in range(j + 1)]
        for row in range(j)
    ]
    cramer = cramer_vector_zpoly(matrix, p)
    dividend = [[(-1) % p]] + [[0] for _ in range(len(h) - 1)] + [[1]]
    rem = pseudo_remainder_x_over_z(dividend, cramer, p)
    coeffs = [c for c in rem if c != [0]]
    cert = min(coeffs, key=lambda c: (zdegree(c), c))
    zeros = [z for z in range(p) if zeval(cert, z, p) == 0]

    # Numeric root table from the same declared family.
    table = []
    top_nonroots = 0
    for z in range(p):
        window = [(a + z * b) % p for a, b in zip(w0, delta)]
        m = hankel(window, j, j)
        rank, _ = rank_and_kernel_mod_p(m, p)
        c = cramer_vector(m, p)
        if rank == j and c[-1] != 0:
            if divides_x_order_minus_one(c, len(h), p):
                table.append(z)
            else:
                top_nonroots += 1
    degree_cap = pseudo_remainder_degree_bound(len(h), j, j)
    ok = (
        set(table).issubset(zeros)
        and zdegree(cert) <= degree_cap
        and cert != [0]
        and table == [0, 1]
    )
    d = [
        f"symbolic pseudo-remainder over F_{p}[z][X]: nonzero coefficient degree "
        f"{zdegree(cert)} <= cap {degree_cap}",
        f"certificate zero set has {len(zeros)} slopes; root-table slopes {table} are contained: "
        f"{set(table).issubset(zeros)}",
        f"top-chart nonroots checked against certificate/table: {top_nonroots}",
        "certificate logic: any full-rank top-chart root must vanish on every pseudo-remainder "
        "coefficient, hence on this one nonzero coefficient",
    ]
    return ok, d


def check_toy_pseudoremainder_gcd_certificate():
    """The top-chart saturated gcd is the canonical toy root-table certificate."""
    p = 97
    h = subgroup_of_order(p, 8)
    j = 4
    roots0 = tuple(h[:j])
    roots1 = tuple(h[2:2 + j])
    weights0 = [3, 7, 11, 19]
    weights1 = [5, 13, 17, 23]
    w0 = moments_from_support(roots0, weights0, 2 * j, p)
    w1 = moments_from_support(roots1, weights1, 2 * j, p)
    delta = [(b - a) % p for a, b in zip(w0, w1)]
    matrix = [
        [[w0[row + col] % p, delta[row + col] % p] for col in range(j + 1)]
        for row in range(j)
    ]
    cramer = cramer_vector_zpoly(matrix, p)
    dividend = [[(-1) % p]] + [[0] for _ in range(len(h) - 1)] + [[1]]
    rem = pseudo_remainder_x_over_z(dividend, cramer, p)
    coeffs = [c for c in rem if c != [0]]
    raw_gcd = [0]
    for coeff in coeffs:
        raw_gcd = zgcd(raw_gcd, coeff, p)
    top_coeff = cramer[-1]
    saturated_gcd = zsaturate_away(raw_gcd, top_coeff, p)
    raw_roots = zroots(raw_gcd, p)
    saturated_roots = zroots(saturated_gcd, p)
    top_boundary_roots = zroots(top_coeff, p)

    table = []
    rank_drop = low_degree = top_nonroots = 0
    for z in range(p):
        window = [(a + z * b) % p for a, b in zip(w0, delta)]
        m = hankel(window, j, j)
        rank, _ = rank_and_kernel_mod_p(m, p)
        c = cramer_vector(m, p)
        if rank < j:
            rank_drop += 1
            continue
        if c[-1] == 0:
            low_degree += 1
            continue
        if divides_x_order_minus_one(c, len(h), p):
            table.append(z)
        else:
            top_nonroots += 1

    ok = (
        raw_gcd != [0]
        and set(table).issubset(raw_roots)
        and set(table).issubset(saturated_roots)
        and saturated_roots == table == [0, 1]
        and not (set(saturated_roots) & set(top_boundary_roots))
    )
    d = [
        "symbolic pseudo-remainder gcd certificate over F_97[Z]: "
        f"{len(coeffs)} nonzero coefficients, raw degree {zdegree(raw_gcd)}, "
        f"top-boundary degree {zdegree(top_coeff)}, saturated degree {zdegree(saturated_gcd)}",
        f"raw gcd roots = {raw_roots}; top-boundary roots = {top_boundary_roots}; "
        f"top-saturated gcd roots = {saturated_roots}",
        f"enumerated full-rank top-chart root table = {table} "
        f"(rank_drop={rank_drop}, low_degree={low_degree}, top_nonroots={top_nonroots})",
        "certificate logic: the raw gcd contains every top-chart bad slope; "
        "saturating away c_j removes low-degree boundary factors and gives the "
        "canonical top-chart eliminant in this toy family",
    ]
    return ok, d


def build_a384_residual_packet():
    j = N - A_STAR
    t = A_STAR - K
    degree_cap = pseudo_remainder_degree_bound(N, j, t)
    return {
        "schema_version": "aperiodic-hankel-eliminant-v1",
        "row": {
            "n": N,
            "k": K,
            "field": "F_17^32",
            "domain_hash": "35904a892e0319b3805e91438ec2733427a351a72ce9654428d6a33bd3575b92",
            "domain_description": (
                "order-512 multiplicative subgroup generated by the row "
                "descriptor packet"
            ),
        },
        "agreement_threshold": A_STAR,
        "sampler": "finite_affine_line",
        "removed_ledgers": [],
        "exact_agreements": [
            {
                "A": A_STAR,
                "j": j,
                "t": t,
                "status": "pivot_atlas",
                "charts": [
                    {
                        "chart_id": "deficiency_one_cramer_atlas",
                        "equations_ref": (
                            f"{NOTE_REF}#2026-07-02-distilled-update-from-pr-176"
                        ),
                        "inequations_ref": (
                            "rank-drop branch: all Cramer minors vanish; "
                            "low-degree branch: top Cramer coefficient c_j=0; "
                            "top chart: c_j != 0 and rank j"
                        ),
                        "coverage_ref": (
                            "experimental/scripts/"
                            "verify_f17_32_m5_underdetermined_a384_bucket.py"
                        ),
                        "pivot_records": [
                            {
                                "pivot": "rank_drop_all_cramer_minors_zero",
                                "status": "empty",
                                "dedup_reason": (
                                    "any valid split degree-j locator has a "
                                    "lower-degree active-support locator and is "
                                    "charged to a higher-agreement bucket"
                                ),
                            },
                            {
                                "pivot": "low_degree_top_coefficient_zero",
                                "status": "empty",
                                "dedup_reason": (
                                    "kernel generator has degree < j, so the "
                                    "slope is charged to a higher-agreement bucket"
                                ),
                            },
                            {
                                "pivot": "full_rank_top_cramer_locator",
                                "status": "residual_obstruction",
                                "residual_label": "unknown",
                                "degree": degree_cap,
                                "eliminant_ref": (
                                    "top-coefficient-saturated gcd of the "
                                    "pseudo-remainder coefficients of X^512-1 by "
                                    "the Cramer locator L_Z(X); degree cap only, "
                                    "no F17 root table emitted in this packet"
                                ),
                            },
                        ],
                    }
                ],
                "residual_summary": (
                    "The only unclosed new exact-A branch is the full-rank top "
                    "pseudo-remainder root table."
                ),
            }
        ],
        "root_union_table_ref": "not_emitted:top_chart_residual_unknown",
        "nonclaims": [
            "no F17 root table is claimed",
            "no threshold or worst-case row safety bound is claimed",
            "rank-drop and low-degree branches are deduped only as new exact-A mass",
        ],
    }


def write_a384_residual_packet():
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(
        json.dumps(build_a384_residual_packet(), indent=2, sort_keys=True) + "\n"
    )


def load_checker_module():
    checker_path = REPO / "scripts" / "check_aperiodic_eliminant_packet.py"
    spec = importlib.util.spec_from_file_location("check_aperiodic_eliminant_packet", checker_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {checker_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_f17_residual_packet():
    expected = build_a384_residual_packet()
    ok = ARTIFACT.exists()
    details = [
        f"artifact path: {ARTIFACT.relative_to(REPO)}",
        "packet status: pivot_atlas with rank-drop/low-degree empty and top-chart residual_label=unknown",
        f"top pseudo-remainder degree cap recorded: {expected['exact_agreements'][0]['charts'][0]['pivot_records'][2]['degree']}",
    ]
    if ok:
        actual = json.loads(ARTIFACT.read_text())
        ok &= actual == expected
        details.append(f"artifact matches deterministic builder: {actual == expected}")
    else:
        details.append("artifact exists: False")
    return ok, details


def check_packet_schema_validation():
    if not ARTIFACT.exists():
        return False, ["artifact missing; run with --emit first"]
    checker = load_checker_module()
    try:
        checker.check_path(ARTIFACT, REPO / "scripts" / "aperiodic_eliminant_schema.json")
    except Exception as exc:  # pragma: no cover - exercised by command line replay
        return False, [f"schema checker failed: {exc}"]
    return True, [
        "scripts/check_aperiodic_eliminant_packet.py accepts the A=384 residual packet",
        "validated fields include schema_version, j=n-A, t=A-k, and residual labels",
    ]


CHECKS = [
    ("bucket identification (A=384, deficiency 1)",       check_bucket_identification),
    ("toy dichotomy: underdetermined vs regular",         check_toy_dichotomy),
    ("deficiency-1 kernel = Cramer minor vector",         check_cramer_kernel_vector),
    ("rank-drop split locators dedupe to higher A",       check_rankdrop_split_locator_dedup),
    ("pivot chart + splitting filter (X^n - 1)",          check_top_chart_splitting_filter),
    ("top-chart pseudo-remainder degree budget",          check_pseudoremainder_degree_budget),
    ("toy pseudo-remainder root table",                   check_toy_pseudoremainder_root_table),
    ("toy root-containment certificate",                  check_toy_root_containment_certificate),
    ("toy saturated-gcd root certificate",                check_toy_pseudoremainder_gcd_certificate),
    ("F17 root table packet or certified residual",       check_f17_residual_packet),
    ("packet emission + v1 schema validation",            check_packet_schema_validation),
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true", help="regenerate the A=384 residual packet")
    args = parser.parse_args()
    if args.emit:
        write_a384_residual_packet()

    print("=" * 74)
    print(f"M5 first singular-bucket pivot packet: A={A_STAR} underdetermined boundary")
    print("of C = RS[F_17^32, H, 256]  (n=512, k=256) -- bucket identification")
    print("=" * 74)
    failed = done = pending = 0
    for title, fn in CHECKS:
        status, details = fn()
        tag = "PENDING" if status is None else ("PASS" if status else "FAIL")
        if status is None:
            pending += 1
        elif status:
            done += 1
        else:
            failed += 1
        print(f"\n[{tag:7}] {title}")
        for line in details:
            print(f"          {line}")
    print("\n" + "-" * 74)
    print(f"implemented PASS: {done}   FAIL: {failed}   PENDING: {pending}")
    print("-" * 74)
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
