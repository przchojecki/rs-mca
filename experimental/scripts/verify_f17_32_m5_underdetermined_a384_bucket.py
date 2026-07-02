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

Turn 2 adds the first chart lemma: in a deficiency-one t x (t+1) split, full
row rank implies the kernel is spanned by the signed maximal-minor/Cramer
vector.  The script verifies this exactly on two toy families by comparing the
Cramer vector with an independently computed RREF kernel vector at every slope.

Turn 3 adds the first divisor gate on the F_97/mu_16 acid-scale toy row: on
the top-coefficient chart, the Cramer locator is valid iff it divides X^16-1.
The check compares direct specialized division, pseudo-remainder vanishing, and
root containment in mu_16 at every finite slope.

Run:  python3 experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py
Exit non-zero iff any implemented check fails.
"""
from __future__ import annotations

import argparse
import json
from hashlib import sha256
from pathlib import Path

Q = 17 ** 32          # q_line = |F|
TWO128 = 2 ** 128
N, K = 512, 256
A_STAR = 384          # the maximal underdetermined exact agreement
TOY_PACKET_SCHEMA = "f97-mu16-m5-a384-deficiency-one-toy-u1-u5-v1"
DEFAULT_TOY_PACKET = Path(
    "experimental/data/certificates/hankel-f97-mu16-m5-a384-toy/"
    "f97_mu16_n16_k8_a12_m5_deficiency_one_toy_u1_u5.json"
)


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


def det_mod_p(matrix, p):
    """Determinant over F_p by Gaussian elimination."""
    n = len(matrix)
    if n == 0:
        return 1
    m = [[x % p for x in row] for row in matrix]
    det = 1
    for c in range(n):
        pivot = next((i for i in range(c, n) if m[i][c]), None)
        if pivot is None:
            return 0
        if pivot != c:
            m[c], m[pivot] = m[pivot], m[c]
            det = (-det) % p
        pv = m[c][c]
        det = (det * pv) % p
        inv = pow(pv, -1, p)
        for r in range(c + 1, n):
            if m[r][c]:
                f = m[r][c] * inv % p
                for cc in range(c, n):
                    m[r][cc] = (m[r][cc] - f * m[c][cc]) % p
    return det % p


def cramer_kernel_vector(matrix, p):
    """Signed maximal-minor vector for a t x (t+1) matrix."""
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    assert cols == rows + 1
    vec = []
    for omit in range(cols):
        sub = [[row[c] for c in range(cols) if c != omit] for row in matrix]
        sign = 1 if omit % 2 == 0 else -1
        vec.append((sign * det_mod_p(sub, p)) % p)
    return vec


def mat_vec_zero(matrix, vec, p):
    return all(sum(row[i] * vec[i] for i in range(len(vec))) % p == 0 for row in matrix)


def proportional_nonzero(a, b, p):
    """Return True iff two nonzero vectors over F_p span the same line."""
    if all(x % p == 0 for x in a) or all(x % p == 0 for x in b):
        return False
    idx = next(i for i, x in enumerate(b) if x % p)
    scale = a[idx] * pow(b[idx], -1, p) % p
    return all((a[i] - scale * b[i]) % p == 0 for i in range(len(a)))


def trim(poly):
    poly = list(poly)
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def poly_eval(poly, x, p):
    acc = 0
    for coeff in reversed(poly):
        acc = (acc * x + coeff) % p
    return acc


def monic_remainder(f, g, p):
    """Remainder of f modulo g over F_p, with g leading coefficient nonzero."""
    r = trim([x % p for x in f])
    g = trim([x % p for x in g])
    n = len(g) - 1
    inv_lc = pow(g[-1], -1, p)
    g_monic = [(c * inv_lc) % p for c in g]
    while len(r) - 1 >= n and any(r):
        d = (len(r) - 1) - n
        lead = r[-1]
        for i, c in enumerate(g_monic):
            r[d + i] = (r[d + i] - lead * c) % p
        r = trim(r)
    return r + [0] * max(0, n - len(r))


def pseudo_remainder(f, g, p):
    """Pseudo-remainder: lc(g)^(deg f - deg g + 1) f = q g + prem."""
    r = trim([x % p for x in f])
    g = trim([x % p for x in g])
    n = len(g) - 1
    delta = (len(r) - 1) - n + 1
    if delta <= 0:
        return r
    lc = g[-1] % p
    steps = 0
    while len(r) - 1 >= n and any(r):
        d = (len(r) - 1) - n
        lead = r[-1] % p
        new_len = max(len(r), d + len(g))
        new_r = [0] * new_len
        for i, c in enumerate(r):
            new_r[i] = (new_r[i] + lc * c) % p
        for i, c in enumerate(g):
            new_r[d + i] = (new_r[d + i] - lead * c) % p
        r = trim(new_r)
        steps += 1
    scale = pow(lc, delta - steps, p)
    return trim([(scale * c) % p for c in r])


def is_zero_poly(poly):
    return all(c == 0 for c in poly)


def hash_json_value(value):
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(payload).hexdigest()


def poly_add_mod(a, b, p):
    n = max(len(a), len(b))
    return trim([((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)) % p for i in range(n)])


def poly_mul_mod(a, b, p):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = (out[i + j] + x * y) % p
    return trim(out)


def poly_scale_mod(a, c, p):
    return trim([(c * x) % p for x in a])


def poly_divmod_mod(a, b, p):
    a = trim([x % p for x in a])
    b = trim([x % p for x in b])
    if is_zero_poly(b):
        raise ZeroDivisionError("polynomial division by zero")
    q = [0] * max(1, len(a) - len(b) + 1)
    inv_lc = pow(b[-1], -1, p)
    while len(a) >= len(b) and not is_zero_poly(a):
        d = len(a) - len(b)
        coeff = a[-1] * inv_lc % p
        q[d] = coeff
        for i, c in enumerate(b):
            a[d + i] = (a[d + i] - coeff * c) % p
        a = trim(a)
    return trim(q), trim(a)


def poly_gcd_monic(a, b, p):
    a = trim([x % p for x in a])
    b = trim([x % p for x in b])
    while not is_zero_poly(b):
        _, r = poly_divmod_mod(a, b, p)
        a, b = b, r
    return poly_scale_mod(a, pow(a[-1], -1, p), p)


def interpolate_full_field(values, p):
    """Interpolate the unique degree < p polynomial with f(z)=values[z]."""
    result = [0]
    xs = list(range(p))
    for a, y in enumerate(values):
        y %= p
        if y == 0:
            continue
        basis = [1]
        denom = 1
        for b in xs:
            if b == a:
                continue
            basis = poly_mul_mod(basis, [(-b) % p, 1], p)
            denom = denom * ((a - b) % p) % p
        result = poly_add_mod(result, poly_scale_mod(basis, y * pow(denom, -1, p) % p, p), p)
    return trim(result)


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


def check_cramer_kernel_vector():
    """Verify U1 exactly: in deficiency one, the signed maximal-minor vector
    spans the generic one-dimensional kernel, and vanishes on rank-drop slopes.

    The first family is the earlier F_13 smoke toy.  The second is the
    roadmap's F_97/mu_16 acid-test scale (n=16,k=8,A=12, so t=j=4), restricted
    here to the U1/U2 linear-algebra layer; later turns add divisibility into
    X^16-1 and brute-force bad-slope comparison.
    """
    families = [
        ("F_13 smoke family", 13,
         [1, 2, 3, 4, 5, 6, 7, 8],
         [8, 1, 5, 2, 9, 3, 7, 4]),
        ("F_97/mu_16 acid-scale family", 97,
         [3, 17, 58, 91, 26, 44, 10, 73],
         [12, 5, 81, 33, 70, 9, 61, 48]),
    ]
    d = []
    ok = True
    for name, p, u, v in families:
        full_rank = 0
        rank_drop = []
        nonzero_cert = None
        for z in range(p):
            s = [(a + z * b) % p for a, b in zip(u, v)]
            m = hankel(s, 4, 4)  # deficiency-one 4 x 5 model of A=384
            rank, rref_vec = rank_and_kernel_mod_p(m, p)
            cramer = cramer_kernel_vector(m, p)
            if not mat_vec_zero(m, cramer, p):
                ok = False
            if rank == 4:
                full_rank += 1
                if not proportional_nonzero(cramer, rref_vec, p):
                    ok = False
                if nonzero_cert is None:
                    omitted = next(i for i, x in enumerate(cramer) if x % p)
                    nonzero_cert = (z, omitted, cramer[omitted])
            else:
                rank_drop.append(z)
                if any(cramer):
                    ok = False
        d.append(f"{name}: Cramer vector verified against RREF kernel on all "
                 f"{full_rank} full-row-rank slopes; rank-drop slopes {rank_drop}")
        ok &= full_rank > 0 and nonzero_cert is not None
        z0, omitted, value = nonzero_cert
        d.append(f"{name}: U2 nondegeneracy certificate M_{omitted}(Z={z0}) = {value} != 0, "
                 "so the generic Cramer chart is not the zero pencil")
    return ok, d


def check_pencil_nondegeneracy_summary():
    """Record the abstract U2 equivalence in the verifier's arithmetic layer.

    In a deficiency-one matrix, all signed maximal minors vanish identically
    iff the row rank over F(Z) is < t.  The previous check exhibits a nonzero
    minor value for each declared toy family, which is an exact certificate
    that the family belongs to the generic Cramer chart rather than the
    lower-rank/proportional stratification branch.
    """
    return True, [
        "U2 is certified by one nonzero maximal-minor evaluation per declared family",
        "pencil-degenerate families are not forced through this chart; they route to WP-2.3 strata",
    ]


def check_divisibility_filter_top_chart():
    """Verify U3/U4 on the F_97/mu_16 acid-scale toy row.

    At n=16,k=8,A=12, t=j=4, so the Cramer locator has degree <= 4.  On the
    top chart c_4 != 0 and full row rank, it has degree exactly 4.  Since
    X^16-1 is separable over F_97 and has root set mu_16, the locator is valid
    iff it divides X^16-1, equivalently iff its specialized remainder vanishes.
    The pseudo-remainder has the same zero set as direct division because the
    top coefficient is nonzero on this chart.
    """
    p = 97
    u = [3, 17, 58, 91, 26, 44, 10, 73]
    v = [12, 5, 81, 33, 70, 9, 61, 48]
    subgroup = [x for x in range(1, p) if pow(x, 16, p) == 1]
    f = [p - 1] + [0] * 15 + [1]  # X^16 - 1
    ok = len(subgroup) == 16
    top = low_degree = rank_drop = 0
    valid_slopes = []
    mismatches = []
    for z in range(p):
        s = [(a + z * b) % p for a, b in zip(u, v)]
        m = hankel(s, 4, 4)
        rank, _ = rank_and_kernel_mod_p(m, p)
        cramer = cramer_kernel_vector(m, p)
        if rank < 4:
            rank_drop += 1
            if any(cramer):
                mismatches.append((z, "rank_drop_nonzero_cramer"))
            continue
        if cramer[4] == 0:
            low_degree += 1
            continue
        top += 1
        direct_rem = trim(monic_remainder(f, cramer, p))
        pseudo_rem = trim(pseudo_remainder(f, cramer, p))
        scaled_direct = trim([(pow(cramer[-1], 13, p) * c) % p for c in direct_rem])
        if pseudo_rem != scaled_direct:
            mismatches.append((z, "pseudo_identity", pseudo_rem, scaled_direct))
        direct_zero = is_zero_poly(direct_rem)
        pseudo_zero = is_zero_poly(pseudo_rem)
        roots = [h for h in subgroup if poly_eval(cramer, h, p) == 0]
        root_valid = len(roots) == 4
        if not (direct_zero == pseudo_zero == root_valid):
            mismatches.append((z, direct_zero, pseudo_zero, root_valid, roots))
        if direct_zero:
            valid_slopes.append((z, roots))
    ok &= not mismatches
    d = [
        f"F_97 subgroup check: |mu_16| = {len(subgroup)} and char 97 does not divide 16",
        f"chart coverage over all {p} slopes: top={top}, low_degree={low_degree}, rank_drop={rank_drop}",
        "top chart: pseudo-remainder equals lc(L)^13 times the ordinary specialized remainder",
        "top chart: direct division by Cramer locator, pseudo-remainder vanishing, "
        "and four roots in mu_16 agree at every slope",
        f"valid top-chart slopes in this declared family: {valid_slopes}",
    ]
    return ok, d


def check_toy_eliminant_dichotomy():
    """Verify U5 on the declared F_97 top-chart toy by interpolation.

    The pseudo-remainder coefficients are functions of the slope z.  Interpolate
    them as polynomials in F_97[Z] and take their monic gcd.  A constant gcd is
    a nonzero eliminant certifying that the top chart is empty over F_97.
    """
    p = 97
    u = [3, 17, 58, 91, 26, 44, 10, 73]
    v = [12, 5, 81, 33, 70, 9, 61, 48]
    f = [p - 1] + [0] * 15 + [1]  # X^16 - 1
    values = [[] for _ in range(4)]
    valid_slopes = []
    for z in range(p):
        s = [(a + z * b) % p for a, b in zip(u, v)]
        m = hankel(s, 4, 4)
        rank, _ = rank_and_kernel_mod_p(m, p)
        cramer = cramer_kernel_vector(m, p)
        if rank != 4 or cramer[4] == 0:
            raise AssertionError("declared U5 toy unexpectedly left the top chart")
        prem = pseudo_remainder(f, cramer, p)
        prem = prem + [0] * (4 - len(prem))
        for i in range(4):
            values[i].append(prem[i] % p)
        if is_zero_poly(prem):
            valid_slopes.append(z)

    coeff_polys = [interpolate_full_field(vs, p) for vs in values]
    interp_ok = True
    for i, poly in enumerate(coeff_polys):
        interp_ok &= all(poly_eval(poly, z, p) == values[i][z] for z in range(p))
    gcd_poly = None
    for poly in coeff_polys:
        if is_zero_poly(poly):
            continue
        gcd_poly = poly if gcd_poly is None else poly_gcd_monic(gcd_poly, poly, p)
    if gcd_poly is None:
        gcd_poly = [0]
    roots = [z for z in range(p) if poly_eval(gcd_poly, z, p) == 0]
    ok = interp_ok and gcd_poly == [1] and roots == valid_slopes == []
    d = [
        f"interpolated four pseudo-remainder coefficient polynomials over F_97 with degrees "
        f"{[len(poly) - 1 for poly in coeff_polys]}",
        f"interpolation replays all 97 slope values exactly: {interp_ok}",
        f"monic gcd of coefficient polynomials is {gcd_poly}; roots over F_97 = {roots}",
        "U5 outcome for this declared top-chart toy: eliminant=1, so the chart is empty",
    ]
    return ok, d


def toy_u1_u5_payload():
    """Recompute the compact toy packet payload."""
    p = 97
    u = [3, 17, 58, 91, 26, 44, 10, 73]
    v = [12, 5, 81, 33, 70, 9, 61, 48]
    subgroup = [x for x in range(1, p) if pow(x, 16, p) == 1]
    f = [p - 1] + [0] * 15 + [1]
    values = [[] for _ in range(4)]
    chart_counts = {"top": 0, "low_degree": 0, "rank_drop": 0}
    valid_slopes = []
    for z in range(p):
        s = [(a + z * b) % p for a, b in zip(u, v)]
        m = hankel(s, 4, 4)
        rank, _ = rank_and_kernel_mod_p(m, p)
        cramer = cramer_kernel_vector(m, p)
        if rank != 4:
            chart_counts["rank_drop"] += 1
            continue
        if cramer[4] == 0:
            chart_counts["low_degree"] += 1
            continue
        chart_counts["top"] += 1
        prem = pseudo_remainder(f, cramer, p)
        prem = prem + [0] * (4 - len(prem))
        for i in range(4):
            values[i].append(prem[i] % p)
        if is_zero_poly(prem):
            valid_slopes.append(z)

    coeff_polys = [interpolate_full_field(vs, p) for vs in values]
    gcd_poly = None
    for poly in coeff_polys:
        if is_zero_poly(poly):
            continue
        gcd_poly = poly if gcd_poly is None else poly_gcd_monic(gcd_poly, poly, p)
    if gcd_poly is None:
        gcd_poly = [0]
    roots = [z for z in range(p) if poly_eval(gcd_poly, z, p) == 0]
    return {
        "field": "F_97",
        "n": 16,
        "k": 8,
        "agreement": 12,
        "t": 4,
        "j": 4,
        "domain": subgroup,
        "u_window": u,
        "v_window": v,
        "chart_counts": chart_counts,
        "coefficient_polynomial_degrees": [len(poly) - 1 for poly in coeff_polys],
        "coefficient_polynomial_hashes": [hash_json_value(poly) for poly in coeff_polys],
        "gcd_coefficients_mod_97_ascending": gcd_poly,
        "gcd_roots_mod_97": roots,
        "valid_top_chart_slopes_mod_97": valid_slopes,
    }


def expected_toy_packet():
    payload = toy_u1_u5_payload()
    domain_hash = "sha256:" + hash_json_value(payload["domain"])
    return {
        "schema_version": TOY_PACKET_SCHEMA,
        "status": "PROVED-LOCAL / EXPERIMENTAL",
        "object": "M5 A=384 deficiency-one U1-U5 top-chart toy replay",
        "scope": {
            "claim": (
                "For the declared F_97/mu_16 toy family, the deficiency-one "
                "Cramer top chart has constant eliminant 1 and hence no valid "
                "top-chart slopes."
            ),
            "nonclaims": [
                "does not prove a threshold or worst-case row bound",
                "does not analyze the F_17^32 row",
                "does not close rank-drop or low-degree side charts in families where they are nonempty",
            ],
        },
        "row": {
            "field": payload["field"],
            "n": payload["n"],
            "k": payload["k"],
            "domain": "mu_16",
            "domain_hash": domain_hash,
            "domain_elements": payload["domain"],
        },
        "agreement": {
            "A": payload["agreement"],
            "t": payload["t"],
            "j": payload["j"],
            "deficiency": payload["j"] + 1 - payload["t"],
        },
        "declared_family": {
            "u_window": payload["u_window"],
            "v_window": payload["v_window"],
        },
        "checks": {
            "u1_cramer_kernel": "verified against RREF on every slope",
            "u2_nondegeneracy": "one nonzero maximal minor exhibited",
            "u3_divisibility": "direct division, pseudo-remainder, and mu_16 roots agree",
            "u4_pseudo_remainder": "prem = lc(L)^13 * rem on the top chart",
            "u5_eliminant": "gcd of pseudo-remainder coefficient polynomials is 1",
        },
        "chart_summary": payload["chart_counts"],
        "top_chart_eliminant": {
            "coefficient_polynomial_degrees": payload["coefficient_polynomial_degrees"],
            "coefficient_polynomial_hashes": payload["coefficient_polynomial_hashes"],
            "gcd_coefficients_mod_97_ascending": payload["gcd_coefficients_mod_97_ascending"],
            "gcd_roots_mod_97": payload["gcd_roots_mod_97"],
            "valid_top_chart_slopes_mod_97": payload["valid_top_chart_slopes_mod_97"],
        },
        "replay": {
            "script": "experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py",
            "command": (
                "python3 experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py "
                "--check experimental/data/certificates/hankel-f97-mu16-m5-a384-toy/"
                "f97_mu16_n16_k8_a12_m5_deficiency_one_toy_u1_u5.json"
            ),
        },
    }


def check_toy_packet(path: Path):
    observed = json.loads(path.read_text(encoding="utf-8"))
    expected = expected_toy_packet()
    if observed != expected:
        raise AssertionError(f"toy U1-U5 packet mismatch: {path}")
    return True, [
        f"packet {path} matches the recomputed U1-U5 toy payload",
        f"schema_version = {TOY_PACKET_SCHEMA}",
        "top-chart eliminant is the constant polynomial 1",
    ]


def _pending():
    return None, ["PENDING -- added in a later loop turn"]


CHECKS = [
    ("bucket identification (A=384, deficiency 1)",       check_bucket_identification),
    ("toy dichotomy: underdetermined vs regular",         check_toy_dichotomy),
    ("deficiency-1 kernel = Cramer minor vector",         check_cramer_kernel_vector),
    ("pencil nondegeneracy of declared toy families",     check_pencil_nondegeneracy_summary),
    ("pivot chart + splitting filter (X^n - 1)",          check_divisibility_filter_top_chart),
    ("eliminant or certified residual obstruction",       check_toy_eliminant_dichotomy),
    ("packet emission + local replay validation",         lambda: check_toy_packet(DEFAULT_TOY_PACKET)),
]


def run_checks(check_packet: Path | None = None):
    print("=" * 74)
    print(f"M5 first singular-bucket pivot packet: A={A_STAR} underdetermined boundary")
    print("of C = RS[F_17^32, H, 256]  (n=512, k=256) -- bucket identification")
    print("=" * 74)
    checks = CHECKS
    if check_packet is not None:
        checks = CHECKS[:-1] + [
            ("packet emission + local replay validation", lambda: check_toy_packet(check_packet))
        ]
    failed = done = pending = 0
    for title, fn in checks:
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", type=Path, help="replay and compare a toy U1-U5 packet")
    args = parser.parse_args()
    run_checks(args.check)


if __name__ == "__main__":
    main()
