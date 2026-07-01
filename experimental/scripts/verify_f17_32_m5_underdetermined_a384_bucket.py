#!/usr/bin/env python3
"""M5 (towards-prize.md M5 / S8 item 6): FIRST singular-bucket pivot packet --
bucket identification at the underdetermined boundary A=384 of
C = RS[F_17^32, H, 256]  (n=512, k=256, q_line=17^32).

For exact agreement A the v10 Hankel system (extractor convention,
experimental/scripts/extract_regular_hankel_minors.py: rows range(t),
cols range(j+1), entry S[row+col], S = syndrome window of u + Z*v) is
t x (j+1) with t = A-k equations on j+1 = n-A+1 locator coefficients.
The regular root-containment certificate needs t >= j+1  <=>  2A >= n+k+1.

A=384 is the MAXIMAL underdetermined agreement: t = j = 128, the matrix is
128 x 129, rank <= 128 < 129, so the kernel is nontrivial for EVERY slope Z
and kernel-nonemptiness certifies nothing.  This script identifies that bucket
exactly and demonstrates the regular/underdetermined dichotomy exhaustively
over a toy field.  Later loop turns add the deficiency-1 pivot-chart machinery
(see the companion note experimental/notes/m5/m5_underdetermined_a384_pivot_packet.md).

Run:  python3 experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py
Exit non-zero iff any implemented check fails.
"""
from __future__ import annotations

Q = 17 ** 32          # q_line = |F|
TWO128 = 2 ** 128
N, K = 512, 256
A_STAR = 384          # the maximal underdetermined exact agreement


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


def _pending():
    return None, ["PENDING -- added in a later loop turn"]


CHECKS = [
    ("bucket identification (A=384, deficiency 1)",       check_bucket_identification),
    ("toy dichotomy: underdetermined vs regular",         check_toy_dichotomy),
    ("deficiency-1 kernel = Cramer minor vector",         _pending),
    ("pivot chart + splitting filter (X^n - 1)",          _pending),
    ("eliminant or certified residual obstruction",       _pending),
    ("packet emission + v1 schema validation",            _pending),
]


def main():
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
