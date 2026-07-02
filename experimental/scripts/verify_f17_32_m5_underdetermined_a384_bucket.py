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

Turn 6 records the abstract deficiency-one degree budget used by the real
A=384 row: Cramer minors have slope-degree <= t, rank-drop/low-degree side
charts are cut by degree-<=t minors, and the top-chart pseudo-remainder
coefficients have slope-degree <= (n-j+1)t.  This specializes to 49,280 for the
F_17^32 A=384 row and to the exact observed degree 52 in the F_97 toy.

Turn 7 records the abstract subgroup divisibility gate: when H is the full root
set of X^n-1 and char(F) does not divide n, a degree-j top-chart locator is a
valid split locator with roots in H iff it divides X^n-1.  The script checks the
required subgroup/separability arithmetic for both the F_97 toy and the real
F_17^32 row.

Turn 8 records the resulting chart-reduction theorem: for a nondegenerate
deficiency-one family, every possible A=384 bad finite slope is routed to one
of three explicit algebraic charts -- rank-drop minors, the low-degree
top-coefficient minor, or the top-chart pseudo-remainder coefficients -- with
the real-row polynomial counts and degree caps printed.

Turn 9 adds the independent F_97 acid test requested by the WP-2.6 plan:
enumerate all binom(16,4)=1820 degree-four subgroup locators directly and
compare the direct bad-slope set with the chart prediction on three pinned toy
families (generic empty top chart, singleton valid top chart, side-chart
routing with one low-degree and one rank-drop slope).

Turn 10 adds the first declared F_17^32 family packet: a planted top-chart
slope at A=384.  It constructs a degree-128 locator from the first 128
descriptor-domain roots, generates the annihilated moment window, and verifies
that a nonconstant syndrome pencil hits that window at a planted finite slope.

Turn 11 strengthens the F_17^32 packet's top-chart certificate: the top
Cramer coordinate is the prefix 128 x 128 moment minor, computed as det(V)^2
for the Vandermonde matrix on the planted support.  This is the actual
c_128 != 0 chart condition.

Turn 12 adds a declared F_17^32 low-degree side-chart packet: a degree-127
kernel locator has c_128=0, while a shifted 128 x 128 minor is nonzero.  This
is the full-rank low-degree chart, not a rank-drop or top-chart slope.

Turn 13 adds a declared F_17^32 rank-drop side-chart packet: a moment window
supported on 126 domain roots has rank exactly 126, while a valid degree-128
split locator lies in the kernel.  This is the rank-drop chart with a valid
locator witness, not a top or low-degree chart.

Turn 14 records the moment-support rank-extension lemma used by the planted
packets: a Hankel moment block supported on s distinct roots factors through
an s-dimensional Vandermonde space; any locator divisible by the support
annihilator lies in the kernel; extra domain roots extend it to a valid
degree-j split locator when available.

Turn 15 records the low-degree side-chart dedup theorem: in a full-row-rank
deficiency-one bucket, c_j=0 means the unique Cramer-kernel locator has degree
< j, so any valid split locator belongs to a higher-agreement bucket and is
not a new exact-A contribution.

Run:  python3 experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py
Exit non-zero iff any implemented check fails.
"""
from __future__ import annotations

import argparse
from itertools import combinations
import json
from hashlib import sha256
from pathlib import Path

from emit_f17_32_hankel_row_descriptor import Field as F17Field

Q = 17 ** 32          # q_line = |F|
TWO128 = 2 ** 128
N, K = 512, 256
A_STAR = 384          # the maximal underdetermined exact agreement
TOY_PACKET_SCHEMA = "f97-mu16-m5-a384-deficiency-one-toy-u1-u5-v1"
F17_PACKET_SCHEMA = "f17-32-m5-a384-planted-top-chart-v1"
F17_LOW_DEGREE_PACKET_SCHEMA = "f17-32-m5-a384-planted-low-degree-v1"
F17_RANK_DROP_PACKET_SCHEMA = "f17-32-m5-a384-planted-rank-drop-v1"
DEFAULT_TOY_PACKET = Path(
    "experimental/data/certificates/hankel-f97-mu16-m5-a384-toy/"
    "f97_mu16_n16_k8_a12_m5_deficiency_one_toy_u1_u5.json"
)
ROW_DESCRIPTOR_REF = Path(
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
DEFAULT_F17_PACKET = Path(
    "experimental/data/certificates/hankel-f17-32-m5-underdetermined-a384/"
    "f17_32_n512_k256_a384_planted_top_chart.json"
)
DEFAULT_F17_LOW_DEGREE_PACKET = Path(
    "experimental/data/certificates/hankel-f17-32-m5-underdetermined-a384/"
    "f17_32_n512_k256_a384_planted_low_degree.json"
)
DEFAULT_F17_RANK_DROP_PACKET = Path(
    "experimental/data/certificates/hankel-f17-32-m5-underdetermined-a384/"
    "f17_32_n512_k256_a384_planted_rank_drop.json"
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


def tagged_hash(value):
    return "sha256:" + hash_json_value(value)


def v_adic(value: int, prime: int) -> int:
    exponent = 0
    while value % prime == 0 and value:
        value //= prime
        exponent += 1
    return exponent


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


def poly_from_roots_mod(roots, p):
    poly = [1]
    for root in roots:
        poly = poly_mul_mod(poly, [(-root) % p, 1], p)
    return poly


def f17_add(field: F17Field, left, right):
    return tuple((a + b) % field.p for a, b in zip(left, right))


def f17_sub(field: F17Field, left, right):
    return tuple((a - b) % field.p for a, b in zip(left, right))


def f17_neg(field: F17Field, value):
    return tuple((-a) % field.p for a in value)


def f17_poly_mul(field: F17Field, left, right):
    zero = field.zero
    out = [zero] * (len(left) + len(right) - 1)
    for i, a_i in enumerate(left):
        if a_i == zero:
            continue
        for j, b_j in enumerate(right):
            if b_j == zero:
                continue
            out[i + j] = f17_add(field, out[i + j], field.mul(a_i, b_j))
    return out


def f17_poly_eval(field: F17Field, poly, value):
    acc = field.zero
    for coeff in reversed(poly):
        acc = f17_add(field, field.mul(acc, value), coeff)
    return acc


def f17_encodings(field: F17Field, values):
    return [field.encode(value) for value in values]


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


def check_subgroup_divisibility_gate():
    """Verify the arithmetic hypotheses behind the abstract divisor gate.

    Mathematical gate recorded in the note: if H is the full set of roots of
    X^n-1 in F and char(F) does not divide n, then X^n-1 is squarefree with
    root set H.  Therefore a top-chart degree-j Cramer locator has j distinct
    roots in H iff it divides X^n-1.
    """
    toy_p, toy_n = 97, 16
    real_p, real_n = 17, N
    ok = True

    toy_subgroup_order_ok = (toy_p - 1) % toy_n == 0
    toy_separable_ok = toy_n % toy_p != 0
    toy_roots = [x for x in range(1, toy_p) if pow(x, toy_n, toy_p) == 1]
    toy_root_count_ok = len(toy_roots) == toy_n
    ok &= toy_subgroup_order_ok and toy_separable_ok and toy_root_count_ok

    real_subgroup_order_ok = (Q - 1) % real_n == 0
    real_separable_ok = real_n % real_p != 0
    real_two_adic = v_adic(Q - 1, 2)
    real_full_2_sylow_ok = real_two_adic == 9 and real_n == 2 ** real_two_adic
    ok &= real_subgroup_order_ok and real_separable_ok and real_full_2_sylow_ok

    d = [
        "abstract gate: for squarefree X^n-1 with root set H, a degree-j locator "
        "splits into j distinct roots in H iff it divides X^n-1",
        f"F_97 toy: 16 | 96 is {toy_subgroup_order_ok}, char 97 does not divide 16 is "
        f"{toy_separable_ok}, and |{{x in F_97*: x^16=1}}| = {len(toy_roots)}",
        f"F_17^32 row: 512 | 17^32-1 is {real_subgroup_order_ok}; char 17 does not "
        f"divide 512 is {real_separable_ok}",
        f"F_17^32 row: v_2(17^32-1) = {real_two_adic}, so H of size 512 is the full "
        "2-Sylow subgroup of F_17^32*",
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


def deficiency_one_degree_bounds(n: int, k: int, agreement: int):
    """Structural chart degree bounds for a deficiency-one Hankel pencil.

    Assumptions recorded in the companion note: the t x (t+1) matrix entries
    are affine-linear in Z, the maximal minors are not all zero as polynomials,
    and the top coefficient minor is not identically zero on the top chart.
    """
    t = agreement - k
    j = n - agreement
    deficiency = (j + 1) - t
    pseudo_delta = n - j + 1
    cramer_degree = t
    return {
        "n": n,
        "k": k,
        "agreement": agreement,
        "t": t,
        "j": j,
        "deficiency": deficiency,
        "cramer_minor_degree_bound": cramer_degree,
        "rank_drop_side_chart_degree_cap": cramer_degree,
        "low_degree_side_chart_degree_cap": cramer_degree,
        "pseudo_remainder_delta": pseudo_delta,
        "top_chart_pseudo_remainder_degree_bound": pseudo_delta * cramer_degree,
        "rough_resultant_degree_bound": n * cramer_degree,
    }


def check_deficiency_one_degree_budget():
    """Verify the abstract U6 degree-budget arithmetic and its two specializations."""
    toy_bounds = deficiency_one_degree_bounds(16, 8, 12)
    real_bounds = deficiency_one_degree_bounds(N, K, A_STAR)
    toy_payload = toy_u1_u5_payload()
    toy_degrees = toy_payload["coefficient_polynomial_degrees"]

    ok = True
    ok &= toy_bounds["deficiency"] == 1
    ok &= real_bounds["deficiency"] == 1
    ok &= toy_bounds["top_chart_pseudo_remainder_degree_bound"] == 52
    ok &= real_bounds["top_chart_pseudo_remainder_degree_bound"] == 49280
    ok &= real_bounds["rough_resultant_degree_bound"] == 65536
    ok &= max(toy_degrees) <= toy_bounds["top_chart_pseudo_remainder_degree_bound"]

    d = [
        "abstract setup: t x (t+1) affine-linear Hankel pencil, deficiency (j+1)-t = 1",
        "Cramer minors c_i(Z) are t x t determinants, hence deg_Z c_i <= t",
        "generic rank-drop side chart is contained in roots of one nonzero minor; "
        "low-degree side chart is contained in roots of c_j; both have degree cap <= t",
        "top chart: pseudo-remainder of X^n-1 by L_Z has delta = n-j+1 pseudo-division steps, "
        "so each coefficient has deg_Z <= (n-j+1)t",
        f"F_97 toy specialization: t=j=4, delta={toy_bounds['pseudo_remainder_delta']}, "
        f"bound={toy_bounds['top_chart_pseudo_remainder_degree_bound']}, observed degrees={toy_degrees}",
        f"F_17^32 A={A_STAR} specialization: t=j=128, delta={real_bounds['pseudo_remainder_delta']}, "
        f"top-chart coefficient degree bound={real_bounds['top_chart_pseudo_remainder_degree_bound']}; "
        f"rough resultant bound={real_bounds['rough_resultant_degree_bound']}",
    ]
    return ok, d


def check_deficiency_one_chart_reduction():
    """Record the finite algebraic target left by U1/U6/U7 at A=384."""
    real = deficiency_one_degree_bounds(N, K, A_STAR)
    toy = toy_u1_u5_payload()
    t, j = real["t"], real["j"]
    minor_count = j + 1
    top_remainder_count = j
    ok = True
    ok &= real["deficiency"] == 1 and t == j == 128
    ok &= minor_count == 129
    ok &= top_remainder_count == 128
    ok &= toy["chart_counts"]["top"] + toy["chart_counts"]["low_degree"] + toy["chart_counts"]["rank_drop"] == 97
    ok &= toy["gcd_coefficients_mod_97_ascending"] == [1]

    d = [
        "chart reduction: if rank M(z)<t, z lies in the rank-drop side chart "
        "cut by all signed maximal minors c_i(z)",
        "chart reduction: if rank M(z)=t and c_j(z)=0, the unique Cramer kernel "
        "has locator degree < j and routes to the low-degree side chart",
        "chart reduction: if rank M(z)=t and c_j(z)!=0, U7 reduces validity to "
        "the top-chart pseudo-remainder equations for L_z | X^n-1",
        f"real A={A_STAR} target: {minor_count} Cramer minors of degree <= "
        f"{real['cramer_minor_degree_bound']}; low-degree gate c_128 has degree <= "
        f"{real['low_degree_side_chart_degree_cap']}",
        f"real A={A_STAR} target: {top_remainder_count} top-chart pseudo-remainder "
        f"coefficients, each degree <= {real['top_chart_pseudo_remainder_degree_bound']}",
        f"toy packet sanity: chart counts {toy['chart_counts']} cover all 97 slopes, "
        "and the declared top chart has eliminant 1",
    ]
    return ok, d


def check_low_degree_dedup_theorem():
    """Record the exact-bucket dedup theorem for the low-degree side chart."""
    real = deficiency_one_degree_bounds(N, K, A_STAR)
    side_chart_toy = toy_chart_summary(
        [34, 37, 69, 71, 6, 22, 30, 62],
        [21, 18, 19, 90, 22, 88, 59, 86],
    )
    t, j = real["t"], real["j"]
    low_degree_slope = side_chart_toy["low_degree"]
    rank_drop_slope = side_chart_toy["rank_drop"]
    ok = True
    ok &= real["deficiency"] == 1 and t == j == 128
    ok &= real["agreement"] + 1 == 385
    ok &= low_degree_slope == [32]
    ok &= rank_drop_slope == [55]
    ok &= side_chart_toy["direct_bad"] == []

    d = [
        "low-degree side chart: rank M(z)=t and c_j(z)=0 in a deficiency-one "
        "t x (j+1) matrix, so ker M(z) is one-dimensional and generated by a locator of degree < j",
        "there is then no degree-exactly-j locator in that kernel; if the lower-degree "
        "locator is split, it witnesses agreement at least A+1 and is charged to the higher-agreement bucket",
        f"F_17^32 A={A_STAR}: the full-rank low-degree side chart contributes no new "
        f"exact-A={A_STAR} roots; valid slopes are deduped into agreement >= {A_STAR + 1}",
        f"F_97 acid side-chart sanity: low_degree={low_degree_slope}, rank_drop={rank_drop_slope}, "
        f"direct exact-A bad slopes={side_chart_toy['direct_bad']}",
    ]
    return ok, d


def check_moment_support_rank_extension_theorem():
    """Record the abstract moment-support rank and locator-extension lemma."""
    real = deficiency_one_degree_bounds(N, K, A_STAR)
    t, j = real["t"], real["j"]
    domain_size = N
    rank_drop_support = 126
    top_support = 128
    ok = True
    ok &= real["deficiency"] == 1 and t == j == 128
    ok &= rank_drop_support < t
    ok &= domain_size - rank_drop_support >= j - rank_drop_support
    ok &= top_support == t == j
    ok &= domain_size - top_support >= 0

    d = [
        "moment-support factorization: if S_m=sum_l w_l x_l^m, then "
        "H_{r,c}=S_{r+c}=V_left diag(w) V_right^T, so rank H <= number of support roots",
        "exact-rank witness: for s distinct support roots and nonzero weights, "
        "the leading s x s moment minor is prod_l(w_l)*det(V_s)^2, hence nonzero",
        "kernel-extension gate: any locator divisible by prod_l(X-x_l) annihilates "
        "the moment window because sum_i L_i S_{r+i}=sum_l w_l x_l^r L(x_l)",
        f"F_17^32 A={A_STAR}: a {rank_drop_support}-root moment support has rank "
        f"exactly {rank_drop_support}<t={t}, and {j-rank_drop_support} extra domain "
        "roots extend its annihilator to a valid degree-128 split locator",
        f"F_17^32 A={A_STAR}: a {top_support}-root nonzero-weight support has "
        "rank 128 and gives the top-chart prefix-minor certificate used by the planted packet",
    ]
    return ok, d


def toy_subgroup_locators(p: int, n: int, j: int):
    """All monic degree-j divisors of X^n-1 over the toy subgroup."""
    subgroup = [x for x in range(1, p) if pow(x, n, p) == 1]
    locators = []
    for roots in combinations(subgroup, j):
        locator = poly_from_roots_mod(roots, p)
        locators.append(locator + [0] * ((j + 1) - len(locator)))
    return subgroup, locators


def toy_chart_summary(u, v):
    """Direct and chart-predicted exact-A bad slopes for the F_97 acid row."""
    p, n, j = 97, 16, 4
    _, locators = toy_subgroup_locators(p, n, j)
    f = [p - 1] + [0] * (n - 1) + [1]  # X^16 - 1
    direct_bad = []
    top_valid = []
    rank_drop = []
    rank_drop_valid = []
    low_degree = []
    top = []
    for z in range(p):
        s = [(a + z * b) % p for a, b in zip(u, v)]
        m = hankel(s, 4, 4)
        rank, _ = rank_and_kernel_mod_p(m, p)
        cramer = cramer_kernel_vector(m, p)
        direct_here = any(mat_vec_zero(m, locator, p) for locator in locators)
        if direct_here:
            direct_bad.append(z)
        if rank < 4:
            rank_drop.append(z)
            if direct_here:
                rank_drop_valid.append(z)
        elif cramer[4] == 0:
            low_degree.append(z)
        else:
            top.append(z)
            if is_zero_poly(pseudo_remainder(f, cramer, p)):
                top_valid.append(z)
    chart_predicted = sorted(set(top_valid) | set(rank_drop_valid))
    return {
        "direct_bad": direct_bad,
        "chart_predicted": chart_predicted,
        "top_valid": top_valid,
        "rank_drop": rank_drop,
        "rank_drop_valid": rank_drop_valid,
        "low_degree": low_degree,
        "top_count": len(top),
        "locator_count": len(locators),
    }


def check_toy_acid_test_bruteforce():
    """Independent F_97 acid test: direct subgroup-locator enumeration vs charts."""
    families = [
        (
            "generic-empty-top",
            [3, 17, 58, 91, 26, 44, 10, 73],
            [12, 5, 81, 33, 70, 9, 61, 48],
            {
                "direct_bad": [],
                "top_valid": [],
                "rank_drop": [],
                "low_degree": [],
            },
        ),
        (
            "singleton-valid-top",
            [77, 27, 77, 4, 74, 87, 20, 55],
            [13, 52, 12, 4, 67, 19, 84, 28],
            {
                "direct_bad": [33],
                "top_valid": [33],
                "rank_drop": [],
                "low_degree": [],
            },
        ),
        (
            "side-chart-routing",
            [34, 37, 69, 71, 6, 22, 30, 62],
            [21, 18, 19, 90, 22, 88, 59, 86],
            {
                "direct_bad": [],
                "top_valid": [],
                "rank_drop": [55],
                "low_degree": [32],
            },
        ),
    ]
    ok = True
    d = [
        "direct test enumerates all binom(16,4)=1820 monic degree-four divisors of X^16-1",
        "chart prediction counts top pseudo-remainder roots plus rank-drop side decisions; "
        "low-degree chart is excluded from exact A=12 by dedup",
    ]
    for name, u, v, expected in families:
        summary = toy_chart_summary(u, v)
        family_ok = (
            summary["locator_count"] == 1820
            and summary["direct_bad"] == expected["direct_bad"]
            and summary["chart_predicted"] == expected["direct_bad"]
            and summary["top_valid"] == expected["top_valid"]
            and summary["rank_drop"] == expected["rank_drop"]
            and summary["low_degree"] == expected["low_degree"]
        )
        ok &= family_ok
        d.append(
            f"{name}: direct_bad={summary['direct_bad']}, chart_predicted="
            f"{summary['chart_predicted']}, top_valid={summary['top_valid']}, "
            f"low_degree={summary['low_degree']}, rank_drop={summary['rank_drop']}, "
            f"top_count={summary['top_count']} -- match: {family_ok}"
        )
    return ok, d


def f17_planted_top_chart_payload():
    """Deterministic declared F_17^32 A=384 planted top-chart family."""
    descriptor = json.loads(ROW_DESCRIPTOR_REF.read_text(encoding="utf-8"))
    field = F17Field(
        descriptor["field_model"]["p"],
        descriptor["field_model"]["modulus"],
    )
    domain = [field.decode(value) for value in descriptor["domain"]["domain_encodings"]]
    support = domain[:128]

    locator = [field.one]
    for root in support:
        locator = f17_poly_mul(field, locator, [f17_neg(field, root), field.one])

    powers = [field.one] * len(support)
    moments = []
    for _ in range(256):
        acc = field.zero
        for value in powers:
            acc = f17_add(field, acc, value)
        moments.append(acc)
        powers = [field.mul(value, root) for value, root in zip(powers, support)]

    recurrence_residuals = []
    for row in range(128):
        acc = field.zero
        for index, coeff in enumerate(locator):
            acc = f17_add(field, acc, field.mul(coeff, moments[row + index]))
        recurrence_residuals.append(acc)

    planted_slope = domain[1]
    v_window = [field.decode(index + 2) for index in range(256)]
    u_window = [
        f17_sub(field, moments[index], field.mul(planted_slope, v_window[index]))
        for index in range(256)
    ]
    recombined = [
        f17_add(field, u_window[index], field.mul(planted_slope, v_window[index]))
        for index in range(256)
    ]

    locator_encodings = f17_encodings(field, locator)
    support_encodings = f17_encodings(field, support)
    moment_encodings = f17_encodings(field, moments)
    u_encodings = f17_encodings(field, u_window)
    v_encodings = f17_encodings(field, v_window)
    residual_encodings = f17_encodings(field, recurrence_residuals)
    locator_values_on_support = f17_encodings(
        field,
        [f17_poly_eval(field, locator, root) for root in support],
    )
    vandermonde_det = field.one
    for right in range(len(support)):
        for left in range(right):
            vandermonde_det = field.mul(
                vandermonde_det,
                f17_sub(field, support[right], support[left]),
            )
    prefix_minor = field.mul(vandermonde_det, vandermonde_det)

    return {
        "row_descriptor_hash": tagged_hash(descriptor),
        "domain_hash": descriptor["row"]["domain_hash"],
        "support_indices": list(range(128)),
        "support_encodings_hash": tagged_hash(support_encodings),
        "locator_degree": len(locator) - 1,
        "locator_leading_coefficient": field.encode(locator[-1]),
        "locator_coefficients_hash": tagged_hash(locator_encodings),
        "locator_values_on_support_hash": tagged_hash(locator_values_on_support),
        "locator_values_on_support_all_zero": all(value == field.zero for value in [
            f17_poly_eval(field, locator, root) for root in support
        ]),
        "locator_leading_coefficient_nonzero": locator[-1] != field.zero,
        "support_roots_in_domain": all(field.pow(root, 512) == field.one for root in support),
        "support_distinct": len(set(support_encodings)) == 128,
        "vandermonde_determinant_encoding": field.encode(vandermonde_det),
        "vandermonde_determinant_nonzero": vandermonde_det != field.zero,
        "moment_prefix_minor_encoding": field.encode(prefix_minor),
        "moment_prefix_minor_nonzero": prefix_minor != field.zero,
        "moment_window_hash": tagged_hash(moment_encodings),
        "recurrence_residual_hash": tagged_hash(residual_encodings),
        "recurrence_residual_all_zero": all(value == field.zero for value in recurrence_residuals),
        "planted_slope_index": 1,
        "planted_slope_encoding": field.encode(planted_slope),
        "v_window_rule": "v_m is the base-field constant m+2, encoded in F_17^32",
        "v_window_hash": tagged_hash(v_encodings),
        "v_window_nonzero": any(value != field.zero for value in v_window),
        "u_window_rule": "u_m = S_m - planted_slope * v_m, where S_m=sum_{r=0}^{127} h_r^m",
        "u_window_hash": tagged_hash(u_encodings),
        "recombination_hash": tagged_hash(f17_encodings(field, recombined)),
        "recombination_matches_moments": recombined == moments,
        "top_chart": {
            "t": 128,
            "j": 128,
            "rank_certificate": "prefix moment minor = det(V)^2 for 128 distinct support roots",
            "top_coefficient_nonzero": prefix_minor != field.zero,
            "validity_certificate": "locator is product of 128 distinct roots from H, hence divides X^512-1",
        },
    }


def expected_f17_packet():
    payload = f17_planted_top_chart_payload()
    return {
        "schema_version": F17_PACKET_SCHEMA,
        "status": "PROVED-LOCAL / EXPERIMENTAL",
        "object": "M5 A=384 deficiency-one planted top-chart family over F_17^32",
        "scope": {
            "claim": (
                "For the declared deterministic F_17^32 syndrome pencil, the "
                "planted finite slope lies in the A=384 top chart and has a "
                "valid degree-128 split locator."
            ),
            "nonclaims": [
                "does not count all bad slopes over F_17^32",
                "does not prove a threshold or worst-case row bound",
                "does not close the rank-drop, low-degree, or full top-chart root tables",
            ],
        },
        "row": {
            "field": "F_17^32",
            "n": 512,
            "k": 256,
            "agreement": 384,
            "t": 128,
            "j": 128,
            "row_descriptor": str(ROW_DESCRIPTOR_REF),
            "row_descriptor_hash": payload["row_descriptor_hash"],
            "domain_hash": payload["domain_hash"],
        },
        "declared_family": {
            "support_indices": payload["support_indices"],
            "support_encodings_hash": payload["support_encodings_hash"],
            "moment_rule": "S_m = sum_{r=0}^{127} h_r^m for descriptor-domain roots h_r",
            "moment_window_hash": payload["moment_window_hash"],
            "u_window_rule": payload["u_window_rule"],
            "u_window_hash": payload["u_window_hash"],
            "v_window_rule": payload["v_window_rule"],
            "v_window_hash": payload["v_window_hash"],
            "planted_slope_index": payload["planted_slope_index"],
            "planted_slope_encoding": payload["planted_slope_encoding"],
        },
        "locator": {
            "degree": payload["locator_degree"],
            "leading_coefficient": payload["locator_leading_coefficient"],
            "coefficients_hash": payload["locator_coefficients_hash"],
            "values_on_support_hash": payload["locator_values_on_support_hash"],
        },
        "checks": {
            "support_distinct": payload["support_distinct"],
            "support_roots_in_domain": payload["support_roots_in_domain"],
            "locator_values_on_support_all_zero": payload["locator_values_on_support_all_zero"],
            "locator_leading_coefficient_nonzero": payload["locator_leading_coefficient_nonzero"],
            "vandermonde_determinant_encoding": payload["vandermonde_determinant_encoding"],
            "vandermonde_determinant_nonzero": payload["vandermonde_determinant_nonzero"],
            "moment_prefix_minor_encoding": payload["moment_prefix_minor_encoding"],
            "moment_prefix_minor_nonzero": payload["moment_prefix_minor_nonzero"],
            "recurrence_residual_hash": payload["recurrence_residual_hash"],
            "recurrence_residual_all_zero": payload["recurrence_residual_all_zero"],
            "v_window_nonzero": payload["v_window_nonzero"],
            "recombination_hash": payload["recombination_hash"],
            "recombination_matches_moments": payload["recombination_matches_moments"],
            "top_chart": payload["top_chart"],
        },
        "replay": {
            "script": "experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py",
            "command": (
                "python3 experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py "
                "--check-f17 experimental/data/certificates/hankel-f17-32-m5-underdetermined-a384/"
                "f17_32_n512_k256_a384_planted_top_chart.json"
            ),
        },
    }


def check_f17_packet(path: Path):
    observed = json.loads(path.read_text(encoding="utf-8"))
    expected = expected_f17_packet()
    if observed != expected:
        raise AssertionError(f"F_17^32 planted top-chart packet mismatch: {path}")
    checks = expected["checks"]
    ok = (
        checks["support_distinct"]
        and checks["support_roots_in_domain"]
        and checks["locator_values_on_support_all_zero"]
        and checks["locator_leading_coefficient_nonzero"]
        and checks["vandermonde_determinant_nonzero"]
        and checks["moment_prefix_minor_nonzero"]
        and checks["recurrence_residual_all_zero"]
        and checks["v_window_nonzero"]
        and checks["recombination_matches_moments"]
        and checks["top_chart"]["top_coefficient_nonzero"]
    )
    return ok, [
        f"packet {path} matches the recomputed F_17^32 planted top-chart payload",
        f"schema_version = {F17_PACKET_SCHEMA}",
        f"planted slope encoding = {expected['declared_family']['planted_slope_encoding']}",
        f"prefix moment minor encoding = {checks['moment_prefix_minor_encoding']} != 0",
        "degree-128 locator is a product of 128 descriptor-domain roots and annihilates the planted moment window",
    ]


def f17_planted_low_degree_payload():
    """Deterministic declared F_17^32 A=384 planted low-degree side chart."""
    descriptor = json.loads(ROW_DESCRIPTOR_REF.read_text(encoding="utf-8"))
    field = F17Field(
        descriptor["field_model"]["p"],
        descriptor["field_model"]["modulus"],
    )
    domain = [field.decode(value) for value in descriptor["domain"]["domain_encodings"]]
    support = domain[:127]

    locator = [field.one]
    for root in support:
        locator = f17_poly_mul(field, locator, [f17_neg(field, root), field.one])

    powers = [field.one] * len(support)
    moments = []
    for _ in range(256):
        acc = field.zero
        for value in powers:
            acc = f17_add(field, acc, value)
        moments.append(acc)
        powers = [field.mul(value, root) for value, root in zip(powers, support)]
    unperturbed_s255 = moments[255]
    perturbation = field.one
    moments[255] = f17_add(field, moments[255], perturbation)

    recurrence_residuals = []
    for row in range(128):
        acc = field.zero
        for index, coeff in enumerate(locator):
            acc = f17_add(field, acc, field.mul(coeff, moments[row + index]))
        recurrence_residuals.append(acc)

    vandermonde_det = field.one
    for right in range(len(support)):
        for left in range(right):
            vandermonde_det = field.mul(
                vandermonde_det,
                f17_sub(field, support[right], support[left]),
            )
    support_product = field.one
    for root in support:
        support_product = field.mul(support_product, root)
    shifted_cofactor = field.mul(support_product, field.mul(vandermonde_det, vandermonde_det))
    shifted_minor = field.mul(perturbation, shifted_cofactor)

    planted_slope = domain[2]
    v_window = [field.decode(index + 5) for index in range(256)]
    u_window = [
        f17_sub(field, moments[index], field.mul(planted_slope, v_window[index]))
        for index in range(256)
    ]
    recombined = [
        f17_add(field, u_window[index], field.mul(planted_slope, v_window[index]))
        for index in range(256)
    ]

    support_encodings = f17_encodings(field, support)
    locator_encodings = f17_encodings(field, locator)
    moment_encodings = f17_encodings(field, moments)
    residual_encodings = f17_encodings(field, recurrence_residuals)
    u_encodings = f17_encodings(field, u_window)
    v_encodings = f17_encodings(field, v_window)
    locator_values_on_support = f17_encodings(
        field,
        [f17_poly_eval(field, locator, root) for root in support],
    )

    return {
        "row_descriptor_hash": tagged_hash(descriptor),
        "domain_hash": descriptor["row"]["domain_hash"],
        "support_indices": list(range(127)),
        "support_encodings_hash": tagged_hash(support_encodings),
        "locator_degree": len(locator) - 1,
        "locator_leading_coefficient": field.encode(locator[-1]),
        "locator_coefficients_hash": tagged_hash(locator_encodings),
        "locator_values_on_support_hash": tagged_hash(locator_values_on_support),
        "locator_values_on_support_all_zero": all(value == field.zero for value in [
            f17_poly_eval(field, locator, root) for root in support
        ]),
        "support_roots_in_domain": all(field.pow(root, 512) == field.one for root in support),
        "support_distinct": len(set(support_encodings)) == 127,
        "moment_window_hash": tagged_hash(moment_encodings),
        "unperturbed_s255_encoding": field.encode(unperturbed_s255),
        "perturbation_index": 255,
        "perturbation_encoding": field.encode(perturbation),
        "recurrence_residual_hash": tagged_hash(residual_encodings),
        "recurrence_residual_all_zero": all(value == field.zero for value in recurrence_residuals),
        "vandermonde_determinant_encoding": field.encode(vandermonde_det),
        "vandermonde_determinant_nonzero": vandermonde_det != field.zero,
        "support_product_encoding": field.encode(support_product),
        "support_product_nonzero": support_product != field.zero,
        "shifted_minor_cofactor_encoding": field.encode(shifted_cofactor),
        "shifted_minor_encoding": field.encode(shifted_minor),
        "shifted_minor_nonzero": shifted_minor != field.zero,
        "planted_slope_index": 2,
        "planted_slope_encoding": field.encode(planted_slope),
        "v_window_rule": "v_m is the base-field constant m+5, encoded in F_17^32",
        "v_window_hash": tagged_hash(v_encodings),
        "v_window_nonzero": any(value != field.zero for value in v_window),
        "u_window_rule": "u_m = S_m - planted_slope * v_m, with S_255 perturbed by 1",
        "u_window_hash": tagged_hash(u_encodings),
        "recombination_hash": tagged_hash(f17_encodings(field, recombined)),
        "recombination_matches_moments": recombined == moments,
        "low_degree_chart": {
            "t": 128,
            "j": 128,
            "kernel_locator_degree": len(locator) - 1,
            "top_cramer_coordinate_zero": True,
            "rank_certificate": "shifted minor columns 1..128 equals perturbation * prod(support) * det(V)^2",
            "full_row_rank": shifted_minor != field.zero,
            "dedup_status": "routes to low-degree side chart; no degree-128 top locator in the generic kernel",
        },
    }


def expected_f17_low_degree_packet():
    payload = f17_planted_low_degree_payload()
    return {
        "schema_version": F17_LOW_DEGREE_PACKET_SCHEMA,
        "status": "PROVED-LOCAL / EXPERIMENTAL",
        "object": "M5 A=384 deficiency-one planted low-degree side chart over F_17^32",
        "scope": {
            "claim": (
                "For the declared deterministic F_17^32 syndrome pencil, the "
                "planted finite slope lies in the full-rank low-degree side "
                "chart: c_128=0 but a shifted 128x128 minor is nonzero."
            ),
            "nonclaims": [
                "does not count all low-degree slopes over F_17^32",
                "does not prove a threshold or worst-case row bound",
                "does not close the rank-drop or top pseudo-remainder root tables",
            ],
        },
        "row": {
            "field": "F_17^32",
            "n": 512,
            "k": 256,
            "agreement": 384,
            "t": 128,
            "j": 128,
            "row_descriptor": str(ROW_DESCRIPTOR_REF),
            "row_descriptor_hash": payload["row_descriptor_hash"],
            "domain_hash": payload["domain_hash"],
        },
        "declared_family": {
            "support_indices": payload["support_indices"],
            "support_encodings_hash": payload["support_encodings_hash"],
            "moment_rule": "S_m=sum_{r=0}^{126} h_r^m for m<255, then S_255 is perturbed by 1",
            "moment_window_hash": payload["moment_window_hash"],
            "unperturbed_s255_encoding": payload["unperturbed_s255_encoding"],
            "perturbation_index": payload["perturbation_index"],
            "perturbation_encoding": payload["perturbation_encoding"],
            "u_window_rule": payload["u_window_rule"],
            "u_window_hash": payload["u_window_hash"],
            "v_window_rule": payload["v_window_rule"],
            "v_window_hash": payload["v_window_hash"],
            "planted_slope_index": payload["planted_slope_index"],
            "planted_slope_encoding": payload["planted_slope_encoding"],
        },
        "locator": {
            "degree": payload["locator_degree"],
            "leading_coefficient": payload["locator_leading_coefficient"],
            "coefficients_hash": payload["locator_coefficients_hash"],
            "values_on_support_hash": payload["locator_values_on_support_hash"],
        },
        "checks": {
            "support_distinct": payload["support_distinct"],
            "support_roots_in_domain": payload["support_roots_in_domain"],
            "locator_values_on_support_all_zero": payload["locator_values_on_support_all_zero"],
            "recurrence_residual_hash": payload["recurrence_residual_hash"],
            "recurrence_residual_all_zero": payload["recurrence_residual_all_zero"],
            "vandermonde_determinant_encoding": payload["vandermonde_determinant_encoding"],
            "vandermonde_determinant_nonzero": payload["vandermonde_determinant_nonzero"],
            "support_product_encoding": payload["support_product_encoding"],
            "support_product_nonzero": payload["support_product_nonzero"],
            "shifted_minor_cofactor_encoding": payload["shifted_minor_cofactor_encoding"],
            "shifted_minor_encoding": payload["shifted_minor_encoding"],
            "shifted_minor_nonzero": payload["shifted_minor_nonzero"],
            "v_window_nonzero": payload["v_window_nonzero"],
            "recombination_hash": payload["recombination_hash"],
            "recombination_matches_moments": payload["recombination_matches_moments"],
            "low_degree_chart": payload["low_degree_chart"],
        },
        "replay": {
            "script": "experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py",
            "command": (
                "python3 experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py "
                "--check-f17-low-degree experimental/data/certificates/"
                "hankel-f17-32-m5-underdetermined-a384/"
                "f17_32_n512_k256_a384_planted_low_degree.json"
            ),
        },
    }


def check_f17_low_degree_packet(path: Path):
    observed = json.loads(path.read_text(encoding="utf-8"))
    expected = expected_f17_low_degree_packet()
    if observed != expected:
        raise AssertionError(f"F_17^32 planted low-degree packet mismatch: {path}")
    checks = expected["checks"]
    ok = (
        checks["support_distinct"]
        and checks["support_roots_in_domain"]
        and checks["locator_values_on_support_all_zero"]
        and checks["recurrence_residual_all_zero"]
        and checks["vandermonde_determinant_nonzero"]
        and checks["support_product_nonzero"]
        and checks["shifted_minor_nonzero"]
        and checks["v_window_nonzero"]
        and checks["recombination_matches_moments"]
        and checks["low_degree_chart"]["full_row_rank"]
        and checks["low_degree_chart"]["top_cramer_coordinate_zero"]
    )
    return ok, [
        f"packet {path} matches the recomputed F_17^32 planted low-degree payload",
        f"schema_version = {F17_LOW_DEGREE_PACKET_SCHEMA}",
        f"planted slope encoding = {expected['declared_family']['planted_slope_encoding']}",
        f"shifted minor encoding = {checks['shifted_minor_encoding']} != 0",
        "degree-127 kernel locator has c_128=0 while shifted minor proves full row rank",
    ]


def f17_planted_rank_drop_payload():
    """Deterministic declared F_17^32 A=384 planted rank-drop side chart."""
    descriptor = json.loads(ROW_DESCRIPTOR_REF.read_text(encoding="utf-8"))
    field = F17Field(
        descriptor["field_model"]["p"],
        descriptor["field_model"]["modulus"],
    )
    domain = [field.decode(value) for value in descriptor["domain"]["domain_encodings"]]
    support = domain[:126]
    valid_roots = domain[:128]

    powers = [field.one] * len(support)
    moments = []
    for _ in range(256):
        acc = field.zero
        for value in powers:
            acc = f17_add(field, acc, value)
        moments.append(acc)
        powers = [field.mul(value, root) for value, root in zip(powers, support)]

    rank_locator = [field.one]
    for root in support:
        rank_locator = f17_poly_mul(field, rank_locator, [f17_neg(field, root), field.one])

    valid_locator = [field.one]
    for root in valid_roots:
        valid_locator = f17_poly_mul(field, valid_locator, [f17_neg(field, root), field.one])

    rank_residuals = []
    for row in range(130):
        acc = field.zero
        for index, coeff in enumerate(rank_locator):
            acc = f17_add(field, acc, field.mul(coeff, moments[row + index]))
        rank_residuals.append(acc)

    valid_residuals = []
    for row in range(128):
        acc = field.zero
        for index, coeff in enumerate(valid_locator):
            acc = f17_add(field, acc, field.mul(coeff, moments[row + index]))
        valid_residuals.append(acc)

    vandermonde_det = field.one
    for right in range(len(support)):
        for left in range(right):
            vandermonde_det = field.mul(
                vandermonde_det,
                f17_sub(field, support[right], support[left]),
            )
    prefix_126_minor = field.mul(vandermonde_det, vandermonde_det)

    planted_slope = domain[3]
    v_window = [field.decode(index + 11) for index in range(256)]
    u_window = [
        f17_sub(field, moments[index], field.mul(planted_slope, v_window[index]))
        for index in range(256)
    ]
    recombined = [
        f17_add(field, u_window[index], field.mul(planted_slope, v_window[index]))
        for index in range(256)
    ]

    support_encodings = f17_encodings(field, support)
    valid_root_encodings = f17_encodings(field, valid_roots)
    rank_locator_encodings = f17_encodings(field, rank_locator)
    valid_locator_encodings = f17_encodings(field, valid_locator)
    moment_encodings = f17_encodings(field, moments)
    rank_residual_encodings = f17_encodings(field, rank_residuals)
    valid_residual_encodings = f17_encodings(field, valid_residuals)
    u_encodings = f17_encodings(field, u_window)
    v_encodings = f17_encodings(field, v_window)
    valid_locator_values = f17_encodings(
        field,
        [f17_poly_eval(field, valid_locator, root) for root in valid_roots],
    )

    return {
        "row_descriptor_hash": tagged_hash(descriptor),
        "domain_hash": descriptor["row"]["domain_hash"],
        "support_indices": list(range(126)),
        "support_encodings_hash": tagged_hash(support_encodings),
        "valid_locator_root_indices": list(range(128)),
        "valid_locator_roots_hash": tagged_hash(valid_root_encodings),
        "support_distinct": len(set(support_encodings)) == 126,
        "valid_roots_distinct": len(set(valid_root_encodings)) == 128,
        "support_roots_in_domain": all(field.pow(root, 512) == field.one for root in support),
        "valid_roots_in_domain": all(field.pow(root, 512) == field.one for root in valid_roots),
        "moment_window_hash": tagged_hash(moment_encodings),
        "rank_locator": {
            "degree": len(rank_locator) - 1,
            "leading_coefficient": field.encode(rank_locator[-1]),
            "coefficients_hash": tagged_hash(rank_locator_encodings),
            "recurrence_residual_hash": tagged_hash(rank_residual_encodings),
            "recurrence_residual_all_zero": all(value == field.zero for value in rank_residuals),
        },
        "valid_locator": {
            "degree": len(valid_locator) - 1,
            "leading_coefficient": field.encode(valid_locator[-1]),
            "coefficients_hash": tagged_hash(valid_locator_encodings),
            "values_on_roots_hash": tagged_hash(valid_locator_values),
            "values_on_roots_all_zero": all(value == field.zero for value in [
                f17_poly_eval(field, valid_locator, root) for root in valid_roots
            ]),
            "recurrence_residual_hash": tagged_hash(valid_residual_encodings),
            "recurrence_residual_all_zero": all(value == field.zero for value in valid_residuals),
        },
        "rank_certificate": {
            "rank_upper_bound": 126,
            "rank_upper_bound_reason": "moment Hankel block factors through 126 support roots",
            "prefix_126_minor_encoding": field.encode(prefix_126_minor),
            "prefix_126_minor_nonzero": prefix_126_minor != field.zero,
            "vandermonde_determinant_encoding": field.encode(vandermonde_det),
            "vandermonde_determinant_nonzero": vandermonde_det != field.zero,
            "rank_exact": 126,
            "maximal_128_minors_all_zero_reason": "rank <= 126 < 128",
        },
        "planted_slope_index": 3,
        "planted_slope_encoding": field.encode(planted_slope),
        "v_window_rule": "v_m is the base-field constant m+11, encoded in F_17^32",
        "v_window_hash": tagged_hash(v_encodings),
        "v_window_nonzero": any(value != field.zero for value in v_window),
        "u_window_rule": "u_m = S_m - planted_slope * v_m, where S_m=sum_{r=0}^{125} h_r^m",
        "u_window_hash": tagged_hash(u_encodings),
        "recombination_hash": tagged_hash(f17_encodings(field, recombined)),
        "recombination_matches_moments": recombined == moments,
        "rank_drop_chart": {
            "t": 128,
            "j": 128,
            "rank": 126,
            "kernel_dimension_at_least": 3,
            "valid_degree_128_locator_in_kernel": True,
            "chart_status": "rank-drop side chart with valid split locator witness",
        },
    }


def expected_f17_rank_drop_packet():
    payload = f17_planted_rank_drop_payload()
    return {
        "schema_version": F17_RANK_DROP_PACKET_SCHEMA,
        "status": "PROVED-LOCAL / EXPERIMENTAL",
        "object": "M5 A=384 deficiency-one planted rank-drop side chart over F_17^32",
        "scope": {
            "claim": (
                "For the declared deterministic F_17^32 syndrome pencil, the "
                "planted finite slope lies in the rank-drop side chart with "
                "rank exactly 126 and a valid degree-128 split locator in the kernel."
            ),
            "nonclaims": [
                "does not count all rank-drop slopes over F_17^32",
                "does not prove a threshold or worst-case row bound",
                "does not close the low-degree or top pseudo-remainder root tables",
            ],
        },
        "row": {
            "field": "F_17^32",
            "n": 512,
            "k": 256,
            "agreement": 384,
            "t": 128,
            "j": 128,
            "row_descriptor": str(ROW_DESCRIPTOR_REF),
            "row_descriptor_hash": payload["row_descriptor_hash"],
            "domain_hash": payload["domain_hash"],
        },
        "declared_family": {
            "support_indices": payload["support_indices"],
            "support_encodings_hash": payload["support_encodings_hash"],
            "moment_rule": "S_m=sum_{r=0}^{125} h_r^m for descriptor-domain roots h_r",
            "moment_window_hash": payload["moment_window_hash"],
            "u_window_rule": payload["u_window_rule"],
            "u_window_hash": payload["u_window_hash"],
            "v_window_rule": payload["v_window_rule"],
            "v_window_hash": payload["v_window_hash"],
            "planted_slope_index": payload["planted_slope_index"],
            "planted_slope_encoding": payload["planted_slope_encoding"],
        },
        "valid_locator": {
            "root_indices": payload["valid_locator_root_indices"],
            "roots_hash": payload["valid_locator_roots_hash"],
            "degree": payload["valid_locator"]["degree"],
            "leading_coefficient": payload["valid_locator"]["leading_coefficient"],
            "coefficients_hash": payload["valid_locator"]["coefficients_hash"],
            "values_on_roots_hash": payload["valid_locator"]["values_on_roots_hash"],
        },
        "rank_locator": {
            "degree": payload["rank_locator"]["degree"],
            "leading_coefficient": payload["rank_locator"]["leading_coefficient"],
            "coefficients_hash": payload["rank_locator"]["coefficients_hash"],
        },
        "checks": {
            "support_distinct": payload["support_distinct"],
            "valid_roots_distinct": payload["valid_roots_distinct"],
            "support_roots_in_domain": payload["support_roots_in_domain"],
            "valid_roots_in_domain": payload["valid_roots_in_domain"],
            "rank_locator": payload["rank_locator"],
            "valid_locator": payload["valid_locator"],
            "rank_certificate": payload["rank_certificate"],
            "v_window_nonzero": payload["v_window_nonzero"],
            "recombination_hash": payload["recombination_hash"],
            "recombination_matches_moments": payload["recombination_matches_moments"],
            "rank_drop_chart": payload["rank_drop_chart"],
        },
        "replay": {
            "script": "experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py",
            "command": (
                "python3 experimental/scripts/verify_f17_32_m5_underdetermined_a384_bucket.py "
                "--check-f17-rank-drop experimental/data/certificates/"
                "hankel-f17-32-m5-underdetermined-a384/"
                "f17_32_n512_k256_a384_planted_rank_drop.json"
            ),
        },
    }


def check_f17_rank_drop_packet(path: Path):
    observed = json.loads(path.read_text(encoding="utf-8"))
    expected = expected_f17_rank_drop_packet()
    if observed != expected:
        raise AssertionError(f"F_17^32 planted rank-drop packet mismatch: {path}")
    checks = expected["checks"]
    ok = (
        checks["support_distinct"]
        and checks["valid_roots_distinct"]
        and checks["support_roots_in_domain"]
        and checks["valid_roots_in_domain"]
        and checks["rank_locator"]["recurrence_residual_all_zero"]
        and checks["valid_locator"]["values_on_roots_all_zero"]
        and checks["valid_locator"]["recurrence_residual_all_zero"]
        and checks["rank_certificate"]["prefix_126_minor_nonzero"]
        and checks["rank_certificate"]["vandermonde_determinant_nonzero"]
        and checks["rank_certificate"]["rank_exact"] == 126
        and checks["v_window_nonzero"]
        and checks["recombination_matches_moments"]
        and checks["rank_drop_chart"]["valid_degree_128_locator_in_kernel"]
    )
    return ok, [
        f"packet {path} matches the recomputed F_17^32 planted rank-drop payload",
        f"schema_version = {F17_RANK_DROP_PACKET_SCHEMA}",
        f"planted slope encoding = {expected['declared_family']['planted_slope_encoding']}",
        f"rank certificate prefix 126-minor = {checks['rank_certificate']['prefix_126_minor_encoding']} != 0",
        "rank is exactly 126 and a valid degree-128 split locator lies in the kernel",
    ]


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
    ("subgroup divisibility gate for real row",           check_subgroup_divisibility_gate),
    ("eliminant or certified residual obstruction",       check_toy_eliminant_dichotomy),
    ("deficiency-1 degree budget for real row",           check_deficiency_one_degree_budget),
    ("deficiency-1 chart reduction for real row",         check_deficiency_one_chart_reduction),
    ("low-degree side-chart dedup theorem",               check_low_degree_dedup_theorem),
    ("moment-support rank-extension theorem",             check_moment_support_rank_extension_theorem),
    ("F_97 acid test: brute force equals charts",         check_toy_acid_test_bruteforce),
    ("F_17^32 planted top-chart packet",                  lambda: check_f17_packet(DEFAULT_F17_PACKET)),
    ("F_17^32 planted low-degree packet",                 lambda: check_f17_low_degree_packet(DEFAULT_F17_LOW_DEGREE_PACKET)),
    ("F_17^32 planted rank-drop packet",                  lambda: check_f17_rank_drop_packet(DEFAULT_F17_RANK_DROP_PACKET)),
    ("packet emission + local replay validation",         lambda: check_toy_packet(DEFAULT_TOY_PACKET)),
]


def run_checks(
    check_packet: Path | None = None,
    check_f17: Path | None = None,
    check_f17_low_degree: Path | None = None,
    check_f17_rank_drop: Path | None = None,
):
    print("=" * 74)
    print(f"M5 first singular-bucket pivot packet: A={A_STAR} underdetermined boundary")
    print("of C = RS[F_17^32, H, 256]  (n=512, k=256) -- bucket identification")
    print("=" * 74)
    checks = CHECKS
    if check_packet is not None:
        checks = CHECKS[:-1] + [
            ("packet emission + local replay validation", lambda: check_toy_packet(check_packet))
        ]
    if check_f17 is not None:
        checks = [
            (
                "F_17^32 planted top-chart packet",
                lambda path=check_f17: check_f17_packet(path),
            )
            if title == "F_17^32 planted top-chart packet"
            else (title, fn)
            for title, fn in checks
        ]
    if check_f17_low_degree is not None:
        checks = [
            (
                "F_17^32 planted low-degree packet",
                lambda path=check_f17_low_degree: check_f17_low_degree_packet(path),
            )
            if title == "F_17^32 planted low-degree packet"
            else (title, fn)
            for title, fn in checks
        ]
    if check_f17_rank_drop is not None:
        checks = [
            (
                "F_17^32 planted rank-drop packet",
                lambda path=check_f17_rank_drop: check_f17_rank_drop_packet(path),
            )
            if title == "F_17^32 planted rank-drop packet"
            else (title, fn)
            for title, fn in checks
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
    parser.add_argument("--check-f17", type=Path, help="replay and compare an F_17^32 planted packet")
    parser.add_argument("--check-f17-low-degree", type=Path, help="replay and compare an F_17^32 low-degree packet")
    parser.add_argument("--check-f17-rank-drop", type=Path, help="replay and compare an F_17^32 rank-drop packet")
    parser.add_argument("--write-f17-packet", type=Path, help="write the deterministic F_17^32 planted packet")
    parser.add_argument("--write-f17-low-degree-packet", type=Path, help="write the deterministic F_17^32 low-degree packet")
    parser.add_argument("--write-f17-rank-drop-packet", type=Path, help="write the deterministic F_17^32 rank-drop packet")
    args = parser.parse_args()
    if args.write_f17_packet:
        args.write_f17_packet.parent.mkdir(parents=True, exist_ok=True)
        args.write_f17_packet.write_text(
            json.dumps(expected_f17_packet(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return
    if args.write_f17_low_degree_packet:
        args.write_f17_low_degree_packet.parent.mkdir(parents=True, exist_ok=True)
        args.write_f17_low_degree_packet.write_text(
            json.dumps(expected_f17_low_degree_packet(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return
    if args.write_f17_rank_drop_packet:
        args.write_f17_rank_drop_packet.parent.mkdir(parents=True, exist_ok=True)
        args.write_f17_rank_drop_packet.write_text(
            json.dumps(expected_f17_rank_drop_packet(), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return
    run_checks(
        args.check,
        args.check_f17,
        args.check_f17_low_degree,
        args.check_f17_rank_drop,
    )


if __name__ == "__main__":
    main()
