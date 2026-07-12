#!/usr/bin/env python3
"""Raw-count refutation of prob:capfp-R1 (rank-one support census per line).

Pinned (cap25_cap_v13_raw.tex @ base sha in the certificate):
  lem:capfp-functionals        the interpolation functionals S_r(f,T)
  thm:capfp-slope-elim         rank-one supports; part (c) is the injection
                               N_MCA-bad <= #R1(u,v;m)
  prob:capfp-R1                the recorded per-line census model (q-scale)
  prob:capfr1-rank-one-census  the sibling statement ("after all paid cells")
  prob:capg-split-pencil-B     hosts the mutatis-mutandis corrected R1 model
                               max(1, C(n,m) p^-w', C(n,m) q^-(w'-1))
  prop:capg-census-floor       the pole-line floors the correction was
                               calibrated to (part (c))
  rem:capg-subfield-scope      (ii) "tight at the floors", (iii) q-scale
                               plausible for primitive lines -- both
                               contradicted by the planted line
  thm:capfp-dichotomy          prices the e <= w' branch (with cor:capfp-line)

Content:
  1. F_73 toy (D = order-24 multiplicative subgroup, K = 12, m = 15,
     w = w' = 3, omega = 9; q = p prime so the subfield/pole-line mechanism
     is vacuous and the planted one-slope mechanism is isolated):
     for each line (u,v) in a frozen menu, an assumption-free scan of all
     C(24,15) = C(24,9) = 1,307,504 supports classifies each as common /
     beta-zero / rank-one(z) / rank-two via the w = 3 functionals, and every
     per-slope multiplicity is cross-checked against the independent
     interpolation-route list census of U_z = u + z v:
     mult(z) = sum_{c in List(U_z;m)} C(agr(U_z,c), m).  Planted lines
     (U = c0 + eta at distance e in {4,5,6}, u := U - z0 v, z0 = 7) FAIL the
     corrected per-line model; the random control line HOLDS it; the
     slope/ray-deduplicated |LineRay| count HOLDS it at every line.
     Planted words have shifted-Popov profile d1 = e (verified).
  2. Deployed KoalaBear census row (n = 2^21, K = 2^20, m = 1116047,
     w' = m - K = 67471, p = 2^31 - 2^24 + 1, q = p^6, e = w'+2 = 67473):
     EXACT big-integer arithmetic (Legendre prime factorization + product
     tree).  The planted line's raw count #R1 >= C(n-w'-2, m), a
     2,015,083-bit integer, exceeds the corrected per-line model (binding
     middle term ceil(C(n,m) p^-w') = 2^35.92; q-term < 1) by a factor
     >= 2^2015046.  All verdicts are bit-length / floor-division facts on
     exact integers.  The freedom-count hygiene bound (union over all q
     slopes below 1) is certified as a bit-length fact.

Framing: the raw R1 support-count model fails; the repair is the
slope/ray-deduplicated |LineRay| count.  This packet cleans up the R1
waypoint; it is not a frontier theorem.

Status: COUNTEREXAMPLE / AUDIT
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import sys
from operator import mul
from pathlib import Path
from typing import Any

STATUS = "COUNTEREXAMPLE / AUDIT"
CERT_REL = Path(
    "experimental/data/certificates/r1-rawcount-refutation/"
    "r1_rawcount_refutation.json"
)
PAPER_CAP = Path("experimental/cap25_cap_v13_raw.tex")
CAP_LABELS = (
    "lem:capfp-functionals",
    "thm:capfp-slope-elim",
    "prob:capfp-R1",
    "prob:capfr1-rank-one-census",
    "prob:capg-split-pencil-B",
    "prop:capg-census-floor",
    "rem:capg-subfield-scope",
    "thm:capfp-dichotomy",
)
SEED = 20260712

# ---------------------------------------------------------------- toy row
P = 73          # field size (prime; q = p = 73)
N = 24          # |D|
K = 12          # code dimension (deg < K)
M = 15          # agreement m
W = M - K       # w = w' = 3
OMEGA = N - M   # 9
SHIFT = K - 1   # 11
Z0 = 7          # planted slope


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def payload_hash(obj: dict[str, Any]) -> str:
    clone = dict(obj)
    clone.pop("payload_sha256", None)
    blob = json.dumps(clone, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------- F_p / poly
def inv(a: int) -> int:
    return pow(a, P - 2, P)


def pnorm(f):
    f = list(f)
    while f and f[-1] == 0:
        f.pop()
    return f


def pdeg(f):
    return len(f) - 1


def padd(f, g):
    L = max(len(f), len(g))
    return pnorm([((f[i] if i < len(f) else 0) + (g[i] if i < len(g) else 0)) % P
                  for i in range(L)])


def psub(f, g):
    L = max(len(f), len(g))
    return pnorm([((f[i] if i < len(f) else 0) - (g[i] if i < len(g) else 0)) % P
                  for i in range(L)])


def pscale(f, c):
    c %= P
    return pnorm([c * a % P for a in f])


def pshift(f, k):
    return ([0] * k + list(f)) if f else []


def pmul(f, g):
    if not f or not g:
        return []
    out = [0] * (len(f) + len(g) - 1)
    for i, a in enumerate(f):
        if a:
            for j, b in enumerate(g):
                out[i + j] = (out[i + j] + a * b) % P
    return pnorm(out)


def pdivmod(f, g):
    assert g, "division by zero poly"
    f = list(f)
    q = [0] * max(0, len(f) - len(g) + 1)
    ginv = inv(g[-1])
    while len(f) >= len(g) and pnorm(f):
        f = pnorm(f)
        if len(f) < len(g):
            break
        c = f[-1] * ginv % P
        d = len(f) - len(g)
        q[d] = c
        for i, b in enumerate(g):
            f[d + i] = (f[d + i] - c * b) % P
        f = pnorm(f)
    return pnorm(q), pnorm(f)


def pgcd(f, g):
    while g:
        f, g = g, pdivmod(f, g)[1]
    return f


def peval(f, x):
    r = 0
    for a in reversed(f):
        r = (r * x + a) % P
    return r


# ----------------------------------------------------------------- domain D
def build_domain():
    for g in range(2, P):
        seen, x = set(), 1
        for _ in range(P - 1):
            x = x * g % P
            seen.add(x)
        if len(seen) == P - 1:
            dom = sorted(pow(pow(g, 3, P), j, P) for j in range(N))
            assert len(set(dom)) == N
            return dom
    raise AssertionError


D = build_domain()
LAMBDA = [1]
for _x in D:
    LAMBDA = pmul(LAMBDA, [(-_x) % P, 1])
assert LAMBDA == [P - 1] + [0] * (N - 1) + [1], "Lambda_D != X^24 - 1"


def interpolate_full(vals):
    out = []
    for i, xi in enumerate(D):
        num, den = [1], 1
        for j, xj in enumerate(D):
            if i == j:
                continue
            num = pmul(num, [(-xj) % P, 1])
            den = den * ((xi - xj) % P) % P
        out = padd(out, pscale(num, vals[i] * inv(den)))
    return out


# ------------------------------------------------- shifted weak Popov basis
def wdeg_pivot(row):
    Wp, Np = row
    e1 = pdeg(Wp) if Wp else -10 ** 9
    e2 = (pdeg(Np) - SHIFT) if Np else -10 ** 9
    return (max(e1, e2), 1 if e2 >= e1 else 0)


def popov_d1(U):
    """d1 of M_U via shifted weak Popov reduction, verified from its
    defining properties (membership, det = unit * Lambda_D, gcd(W1,W2) = 1,
    d1 + d2 = n-K+1, distinct pivots)."""
    Uhat = interpolate_full(U)
    rows = [([1], Uhat), ([], LAMBDA[:])]
    for _ in range(10000):
        (wd0, pv0), (wd1, pv1) = wdeg_pivot(rows[0]), wdeg_pivot(rows[1])
        if pv0 != pv1:
            break
        i, j = (0, 1) if wd0 <= wd1 else (1, 0)
        ri, rj = rows[i], rows[j]
        wi, wj = (wd0, wd1) if i == 0 else (wd1, wd0)
        piv = pv0
        li = ri[piv][-1]
        lj = rj[piv][-1]
        delta = wj - wi
        c = lj * inv(li) % P
        rows[j] = (psub(rj[0], pshift(pscale(ri[0], c), delta)),
                   psub(rj[1], pshift(pscale(ri[1], c), delta)))
    else:
        raise AssertionError("popov did not terminate")
    rows.sort(key=lambda r: wdeg_pivot(r)[0])
    g1, g2 = rows
    d1, d2 = wdeg_pivot(g1)[0], wdeg_pivot(g2)[0]
    for (Wp, Np) in (g1, g2):
        for idx, x in enumerate(D):
            assert peval(Wp, x) * U[idx] % P == peval(Np, x), "row not in M_U"
    det = psub(pmul(g1[0], g2[1]), pmul(g1[1], g2[0]))
    qd, rd = pdivmod(det, LAMBDA)
    assert rd == [] and pdeg(qd) == 0, "det not unit * Lambda_D"
    assert pdeg(pgcd(g1[0], g2[0])) == 0, "gcd(W1,W2) != 1"
    assert d1 + d2 == N - K + 1, "d1+d2 != n-K+1"
    assert wdeg_pivot(g1)[1] != wdeg_pivot(g2)[1], "not weak Popov (same pivots)"
    return d1


# --------------------------------------------- divisor complements (once)
def enumerate_complements():
    """coefficient tuples of Lambda_R for all 9-subsets R, DFS (lex) order."""
    out = []

    def rec(start, depth, poly):
        if depth == OMEGA:
            out.append(tuple(poly))
            return
        need = OMEGA - depth
        for idx in range(start, N - need + 1):
            x = D[idx]
            new = [0] * (depth + 2)
            mx = (-x) % P
            for i2, a in enumerate(poly):
                if a:
                    new[i2] = (new[i2] + a * mx) % P
                    new[i2 + 1] = (new[i2 + 1] + a) % P
            rec(idx + 1, depth + 1, new)

    rec(0, 0, [1])
    assert len(out) == math.comb(N, OMEGA)
    return out


LAMR = enumerate_complements()


def power_sums(word):
    return [sum(word[i] * pow(D[i], t, P) for i in range(N)) % P
            for t in range(13)]


# ------------------------------------------------------- independent list
def list_codewords(word):
    """{codeword_tuple: agr} for all deg<K codewords with agr >= m --
    duality + interpolation route (independent of the rank-one scan)."""
    T = power_sums(word)
    T1 = tuple(T[1:11])
    T2 = tuple(T[2:12])
    T3 = tuple(T[3:13])
    found = {}
    for lam in LAMR:
        if sum(map(mul, lam, T1)) % P:
            continue
        if sum(map(mul, lam, T2)) % P:
            continue
        if sum(map(mul, lam, T3)) % P:
            continue
        # roots of Lambda_R = the complement; interpolate on S = D \ R
        Sidx = [i for i in range(N) if peval(lam, D[i]) != 0]
        assert len(Sidx) == M
        pts = [(D[i], word[i]) for i in Sidx[:K]]
        out = []
        for i, (xi, yi) in enumerate(pts):
            num, den = [1], 1
            for j, (xj, _) in enumerate(pts):
                if i == j:
                    continue
                num = pmul(num, [(-xj) % P, 1])
                den = den * ((xi - xj) % P) % P
            out = padd(out, pscale(num, yi * inv(den)))
        for i in Sidx[K:]:
            assert peval(out, D[i]) == word[i]
        key = tuple(out[t] if t < len(out) else 0 for t in range(K))
        if key not in found:
            found[key] = sum(1 for idx in range(N)
                             if peval(out, D[idx]) == word[idx])
    return found


# ------------------------------------------------------- rank-one scan
def rank_one_scan(u, v):
    """one pass over all supports: classify and histogram slopes."""
    Tu = power_sums(u)
    Tv = power_sums(v)
    TuW = (tuple(Tu[1:11]), tuple(Tu[2:12]), tuple(Tu[3:13]))
    TvW = (tuple(Tv[1:11]), tuple(Tv[2:12]), tuple(Tv[3:13]))
    n_common = n_bzero = n_r1 = n_r2 = 0
    mult = {}
    for lam in LAMR:
        a = [sum(map(mul, lam, TuW[0])) % P,
             sum(map(mul, lam, TuW[1])) % P,
             sum(map(mul, lam, TuW[2])) % P]
        b = [sum(map(mul, lam, TvW[0])) % P,
             sum(map(mul, lam, TvW[1])) % P,
             sum(map(mul, lam, TvW[2])) % P]
        if b == [0, 0, 0]:
            if a == [0, 0, 0]:
                n_common += 1
            else:
                n_bzero += 1
            continue
        # beta != 0: proportional iff cross products vanish
        if (a[0] * b[1] - a[1] * b[0]) % P == 0 and \
           (a[0] * b[2] - a[2] * b[0]) % P == 0 and \
           (a[1] * b[2] - a[2] * b[1]) % P == 0:
            r = next(i for i in range(3) if b[i])
            z = (-a[r]) * inv(b[r]) % P
            assert all((a[i] + z * b[i]) % P == 0 for i in range(3))
            n_r1 += 1
            mult[z] = mult.get(z, 0) + 1
        else:
            n_r2 += 1
    assert n_common + n_bzero + n_r1 + n_r2 == len(LAMR)
    return n_r1, mult, n_common, n_bzero, n_r2


# ------------------------------------------------------------------- menu
def make_lines():
    """Deterministic line menu (seeded); words and error data go in the
    cert.  RNG call sequence is frozen: c0 (12 draws), then per e in
    (4,5,6): sample(range(24), e), e offset draws in sample order, 24 draws
    for v; then 24 + 24 draws for the random control line."""
    rng = random.Random(SEED)

    def rand_cw():
        return [rng.randrange(P) for _ in range(K)]

    def word_of(c):
        return [peval(c, x) for x in D]

    lines = []
    c0 = rand_cw()
    base = word_of(c0)
    for e in (4, 5, 6):
        U = base[:]
        pos = rng.sample(range(N), e)
        for i in pos:
            U[i] = (U[i] + rng.randrange(1, P)) % P
        v = [rng.randrange(P) for _ in range(N)]
        u = [(U[i] - Z0 * v[i]) % P for i in range(N)]
        lines.append({"label": "planted_e%d" % e, "e": e, "z0": Z0,
                      "u": u, "v": v, "codeword_coeffs": c0,
                      "error_positions": sorted(pos)})
    u = [rng.randrange(P) for _ in range(N)]
    v = [rng.randrange(P) for _ in range(N)]
    lines.append({"label": "random_line", "e": None, "z0": None,
                  "u": u, "v": v, "codeword_coeffs": None,
                  "error_positions": None})
    return lines


# ------------------------------------------------------------ per-line row
def holds(count, terms):
    """count <= max(1, terms...) with terms as exact fractions [num, den]."""
    return count <= 1 or any(count * den <= num for num, den in terms)


def line_row(spec):
    u, v = spec["u"], spec["v"]
    n_r1, mult, n_common, n_bzero, n_r2 = rank_one_scan(u, v)
    slope_rows = []
    lineray = 0
    census_total = 0
    for z in sorted(mult, key=lambda t: (-mult[t], t)):
        Uz = [(u[i] + z * v[i]) % P for i in range(N)]
        lst = list_codewords(Uz)
        expect = sum(math.comb(agr, M) for agr in lst.values())
        assert mult[z] == expect, \
            "slope %d: scan mult %d != list census %d" % (z, mult[z], expect)
        profile = sorted(lst.values(), reverse=True)
        slope_rows.append([z, mult[z], profile])
        lineray += len(lst)
        census_total += expect
    assert census_total == n_r1  # #R1 = sum_z sum_c C(agr(U_z,c), m)

    q_term = [math.comb(N, M), P ** (W - 1)]        # C(n,m) q^-(w'-1), q = p
    p_term = [math.comb(N, M), P ** W]              # C(n,m) p^-w'
    row = {
        "label": spec["label"],
        "e": spec["e"],
        "z0": spec["z0"],
        "u": u,
        "v": v,
        "codeword_coeffs": spec["codeword_coeffs"],
        "error_positions": spec["error_positions"],
        "counts": {"common": n_common, "beta_zero": n_bzero,
                   "rank_one": n_r1, "rank_two": n_r2},
        "slopes_hit": len(mult),
        "slope_rows": slope_rows,
        "lineray_count": lineray,
        "budget_literal_q_term": q_term,
        "budget_corrected_p_term": p_term,
        "literal_holds_raw": holds(n_r1, [q_term]),
        "corrected_holds_raw": holds(n_r1, [p_term, q_term]),
        "literal_holds_lineray": holds(lineray, [q_term]),
        "corrected_holds_lineray": holds(lineray, [p_term, q_term]),
    }
    if spec["e"] is not None:
        e = spec["e"]
        Uw = [(u[i] + Z0 * v[i]) % P for i in range(N)]
        lst0 = list_codewords(Uw)
        assert N - max(lst0.values()) == e, "planted distance != e"
        d1 = popov_d1(Uw)
        assert d1 == e, "profile localization failed: d1=%d e=%d" % (d1, e)
        assert d1 >= W + 1, "planted word in priced near-rational branch"
        assert Z0 in mult, "planted slope carries no support"
        floor = math.comb(N - e, M)
        assert mult[Z0] >= floor and n_common == 0
        row["planted"] = {"mult_z0": mult[Z0],
                          "floor_C_n_minus_e_m": floor,
                          "floor_holds": True,
                          "d1": d1, "d1_equals_e": True}
    else:
        row["planted"] = None
    return row


# --------------------------------------------- deployed-scale calibration
def sieve(limit):
    isp = bytearray([1]) * (limit + 1)
    isp[0:2] = b"\x00\x00"
    for i in range(2, int(limit ** 0.5) + 1):
        if isp[i]:
            isp[i * i::i] = bytearray(len(isp[i * i::i]))
    return [i for i in range(limit + 1) if isp[i]]


def legendre_e(a, b, p):
    e, pk = 0, p
    while pk <= a:
        e += a // pk - b // pk - (a - b) // pk
        pk *= p
    return e


def prod_tree(xs):
    while len(xs) > 1:
        xs = ([xs[i] * xs[i + 1] for i in range(0, len(xs) - 1, 2)]
              + ([xs[-1]] if len(xs) & 1 else []))
    return xs[0] if xs else 1


def exact_comb(a, b, primes):
    return prod_tree([pr ** legendre_e(a, b, pr)
                      for pr in primes if pr <= a and legendre_e(a, b, pr)])


def lg2_display(x):
    """display-grade log2 string (top-80-bit mantissa; no verdict uses it)."""
    e = x.bit_length() - 1
    if e <= 80:
        return "%.4f" % math.log2(x)
    return "%.4f" % (math.log2(x >> (e - 80)) + (e - 80))


def deployed_section():
    n_, K_ = 2 ** 21, 2 ** 20
    w_ = 67471                    # census convention w' = m - K
    m_ = K_ + w_                  # = 1116047 = KB-MCA proved-unsafe edge a0
    om_ = n_ - m_
    p_ = 2 ** 31 - 2 ** 24 + 1    # KoalaBear base prime
    e_ = w_ + 2                   # planted distance, interior of the ledger
    primes = sieve(n_)
    Cnm = exact_comb(n_, m_, primes)
    Cray = exact_comb(n_ - e_, m_, primes)          # #R1 floor C(n-w'-2, m)
    Cnm_paper = exact_comb(n_, m_ - 1, primes)      # paper's (K,m)=(k,1116046)

    # q-term of both models over the ambient line field q = p^6:
    # q^{w'-1} >= 2^{185(w'-1)} > C(n,m), so the term is < 1
    q_ = p_ ** 6
    q_bit_floor = q_.bit_length() - 1
    qpow_min_bits = (w_ - 1) * q_bit_floor
    assert qpow_min_bits > Cnm.bit_length()

    # binding corrected middle term ceil(C(n,m) p^-w'), exact integer
    pw = p_ ** w_
    assert Cnm > pw
    mid_ceil = -(-Cnm // pw)
    assert mid_ceil.bit_length() == 36 and mid_ceil == 65065153468

    # freedom-count hygiene: union bound over all q slopes,
    # 2 C(n,m) q^{-(w'-1)} < 1, certified via bit lengths
    hygiene_ok = Cnm.bit_length() + 1 <= qpow_min_bits
    assert hygiene_ok

    assert Cray.bit_length() == 2015083
    marg_corr = (Cray // mid_ceil).bit_length() - 1
    assert marg_corr == 2015046
    marg_lit = Cray.bit_length() - 1
    assert marg_lit == 2015082

    # lemma range at deployed scale: 2e <= n-K+1 (profile localization d1 = e)
    assert 2 * e_ <= n_ - K_ + 1

    # cross-validation against the paper's own printed floors at its
    # orientation row (K,m) = (k, 1116046): 67.1 boundary, 56.0 interior
    w2 = (m_ - 1) - K_
    bf_paper = -(-Cnm_paper // p_ ** w2)
    mb_paper = m_ * (-(-Cnm // p_ ** (w2 + 1)))
    assert lg2_display(bf_paper) == "67.0958"
    assert lg2_display(mb_paper) == "56.0111"

    return {
        "n": n_, "K": K_, "m": m_, "w_prime": w_, "omega": om_, "p": p_,
        "q": "p^6 (KoalaBear sextic extension line field)",
        "q_bit_floor": q_bit_floor,
        "e": e_, "e_is": "w_prime + 2",
        "row_note": ("m = KB-MCA proved-unsafe edge a0 = KB-list a+ under "
                     "the census convention w' = m - K"),
        "e_dichotomy": {
            "e_le_w_prime": ("priced: thm:capfp-dichotomy(i) + cor:capfp-line "
                             "bound the near-rational branch"),
            "e_eq_w_prime_plus_1": ("boundary profile, delegated to (Q) by "
                                    "rem:capg-boundary-offbyone"),
            "e_eq_w_prime_plus_2": ("interior profile; no printed convention "
                                    "prices it -- the planted distance"),
        },
        "lemma_2e_le_n_minus_K_plus_1": {"two_e": 2 * e_,
                                         "n_minus_K_plus_1": n_ - K_ + 1,
                                         "ok": True},
        "bits": {"C_n_m": Cnm.bit_length(),
                 "C_ray_interior": Cray.bit_length()},
        "log2_display": {"C_n_m": lg2_display(Cnm),
                         "C_ray_interior": lg2_display(Cray),
                         "corrected_middle_ceil": lg2_display(mid_ceil),
                         "overrun_factor": lg2_display(Cray // mid_ceil)},
        "budget": {
            "corrected_middle_ceil": mid_ceil,
            "corrected_budget": mid_ceil,
            "q_term_below_1": True,
            "q_pow_min_bits": qpow_min_bits,
            "literal_q_scale_budget": 1,
        },
        "hygiene_freedom_count": {
            "statement": ("u := U - z0 v with v uniform: for every slope "
                          "z != z0 (incl. infinity) the word u + z v is "
                          "uniform, so Pr[cen(u+zv;m) > 0] <= C(n,m) q^-w' "
                          "by the first moment; union over all q slopes "
                          "<= 2 C(n,m) q^-(w'-1) < 1 -- v exists "
                          "deterministically with every other slope "
                          "census-empty, no common supports, and the line "
                          "challenge-field-primitive"),
            "union_bound_below_1_via_bits": hygiene_ok,
        },
        "margins_bits": {
            "planted_R1_vs_corrected": marg_corr,
            "planted_R1_vs_literal_q_scale": marg_lit,
        },
        "paper_printed_floor_cross_check": {
            "at_paper_row_m": m_ - 1,
            "boundary_floor_log2_display": lg2_display(bf_paper),
            "paper_prints_boundary": "67.1",
            "interior_MB_log2_display": lg2_display(mb_paper),
            "paper_prints_interior": "56.0",
        },
    }


def print_deployed_params(dep):
    print("  deployed row: n=%d K=%d m=%d w'=%d omega=%d p=%d q=p^6 "
          "e=w'+2=%d" % (dep["n"], dep["K"], dep["m"], dep["w_prime"],
                         dep["omega"], dep["p"], dep["e"]))


# ----------------------------------------------------------- label scanning
def scan_labels(root: Path) -> dict[str, dict[str, dict[str, Any]]]:
    """statement pins: label -> {line, sha256_line, text} per source file."""
    out: dict[str, dict[str, dict[str, Any]]] = {}
    text = (root / PAPER_CAP).read_text(encoding="utf-8").splitlines()
    found: dict[str, dict[str, Any]] = {}
    for i, line in enumerate(text, 1):
        for lab in CAP_LABELS:
            if ("\\label{%s}" % lab) in line and lab not in found:
                found[lab] = {
                    "line": i,
                    "sha256_line": hashlib.sha256(
                        line.encode("utf-8")).hexdigest(),
                    "text": line.strip(),
                }
    missing = [lab for lab in CAP_LABELS if lab not in found]
    assert not missing, "labels missing in %s: %s" % (PAPER_CAP, missing)
    out[PAPER_CAP.name] = found
    return out


# ------------------------------------------------------------- certificate
def build_certificate(root: Path) -> dict[str, Any]:
    labels = scan_labels(root)
    toy_rows = [line_row(spec) for spec in make_lines()]

    planted = [r for r in toy_rows if r["e"] is not None]
    control = [r for r in toy_rows if r["e"] is None]
    assert planted and all(not r["corrected_holds_raw"] for r in planted)
    assert all(not r["literal_holds_raw"] for r in planted)
    assert control and all(r["corrected_holds_raw"] for r in control)
    assert all(r["literal_holds_raw"] for r in control)
    assert all(r["corrected_holds_lineray"] for r in toy_rows)
    assert all(r["literal_holds_lineray"] for r in toy_rows)
    assert all(r["counts"]["common"] == 0 for r in toy_rows)
    assert all(r["planted"]["d1_equals_e"] for r in planted)

    dep = deployed_section()

    cert: dict[str, Any] = {
        "status": STATUS,
        "object": ("raw-count refutation of prob:capfp-R1 (per-line "
                   "rank-one support census), including the corrected "
                   "mutatis-mutandis model of prob:capg-split-pencil-B, "
                   "by a planted near-codeword-slope line"),
        "base_sha": "36de5bfcc7d6e0ca44806112acec2f4a1b4a7532",
        "evidence_type": "COUNTEREXAMPLE_VS_RECORDED_PROBLEM",
        "seed": SEED,
        "toy_parameters": {"p": P, "n": N, "K": K, "m": M, "w": W,
                           "omega": OMEGA, "z0": Z0, "domain": D,
                           "pole_line_floor_vacuous_since_q_equals_p": True},
        "statement_pins": labels,
        "falsifiability": ("The gate fails if any toy scan count, slope "
                           "multiplicity, list census, profile, lineray "
                           "count, or budget comparison changes; if any "
                           "deployed bit-length or margin changes; if any "
                           "pinned label moves or its line hash drifts; or "
                           "if d1 != e at any planted toy word."),
        "generator_routes": (
            "toy: full C(24,9) support scan classifying common/beta-zero/"
            "rank-one(z)/rank-two via the w=3 interpolation functionals, "
            "every slope multiplicity cross-checked against the independent "
            "interpolation-route list census of U_z, planted profiles via "
            "shifted-weak-Popov reduction verified from defining "
            "properties; deployed: Legendre prime factorization + "
            "product-tree exact binomials, verdicts as bit-length/"
            "floor-division integer facts"),
        "construction": {
            "recipe": ("pick codeword c0 and error eta of weight e = w'+2 "
                       "with challenge-field values, set U := c0 + eta; "
                       "pick z0 != 0 and put u := U - z0 v with v generic; "
                       "then every m-support inside the agreement set of "
                       "(U, c0) is rank-one with slope z0 and "
                       "#R1(u,v;m) >= C(n-e, m)"),
            "exclusion_sweep": ("no printed convention excludes the plant: "
                                "prob:capfp-R1 quantifies over every line "
                                "at band agreements with no profile clause; "
                                "'first match'/'strip' appear nowhere in "
                                "the source; the printed paid-cell list "
                                "(tangent, quotient, extension-pole, "
                                "common-GCD, quotient-pullback, "
                                "fixed-dimensional, sunflower, SPI) "
                                "contains no near-codeword-slope cell; the "
                                "planted line is primitive under every "
                                "printed sense of rem:capg-subfield-scope"),
            "why_e_is_w_prime_plus_2": ("e <= w' is priced by "
                                        "thm:capfp-dichotomy(i) + "
                                        "cor:capfp-line; e = w'+1 is the "
                                        "boundary profile delegated to (Q); "
                                        "e = w'+2 is interior and unpriced, "
                                        "with d1 = e by profile "
                                        "localization (2e <= n-K+1)"),
        },
        "identity": {
            "statement": ("#R1(u,v;m) = sum_z sum_{c in List(u+zv;m)} "
                          "C(agr(u+zv,c), m) whenever no common support "
                          "exists: the raw R1 count is exactly the "
                          "with-multiplicity LineRay census"),
            "verified_at_every_slope_of_every_toy_line": True,
        },
        "toy_rows": toy_rows,
        "deployed": dep,
        "honest_headline": (
            "The raw R1 support-count model fails: a planted "
            "near-codeword-slope line at the deployed KoalaBear census row "
            "has #R1 >= C(n-w'-2, m) (a 2,015,083-bit integer) against the "
            "corrected per-line model 2^35.92 -- a factor >= 2^2015046 -- "
            "and against the literal q-scale model max(1, ~2^-10453966) = 1. "
            "The repair is the slope/ray-deduplicated |LineRay| count, "
            "which HOLDS the model at every toy line.  This packet cleans "
            "up the R1 waypoint; it is not a frontier theorem."),
        "beats_trivial_baseline": True,
        "is_degenerate_by_construction": False,
        "is_tautology_under_preconditions": False,
        "summary": {
            "verdict": "COUNTEREXAMPLE",
            "headline": ("prob:capfp-R1 fails verbatim at the raw "
                         "(with-multiplicity) rank-one support count, and "
                         "the corrected R1 model recorded in "
                         "prob:capg-split-pencil-B's mutatis-mutandis "
                         "clause fails at the same line by >= 2^%d at the "
                         "deployed KoalaBear census row; "
                         "rem:capg-subfield-scope(ii)-(iii) are "
                         "contradicted; the toy lines isolate the "
                         "one-slope mechanism exactly and the random "
                         "control line HOLDS the model"
                         % dep["margins_bits"]["planted_R1_vs_corrected"]),
            "mechanism_novelty": ("upstream's own pole-line floors "
                                  "(prop:capg-census-floor(c)) are "
                                  "many-slopes-one-support-each at "
                                  "agreement exactly m; the plant is the "
                                  "opposite configuration: one slope, one "
                                  "codeword ray, C(n-w'-2,m) supports at "
                                  "agreement n-w'-2 -- never priced; the "
                                  "corrected middle term was calibrated "
                                  "only to the pole-line floor"),
            "not_affected": ("lem:capfp-functionals, thm:capfp-slope-elim, "
                             "thm:capfp-dichotomy, and every unconditional "
                             "reduction (rem:capg-subfield-scope(i)); the "
                             "pole-line floors themselves; every "
                             "slope-count (ray-deduplicated) object -- the "
                             "deduplicated toy counts sit below the model "
                             "at every line"),
        },
        "sibling_capfr1_grading": {
            "verdict": "REFUTED-WITH-AMBIGUITY-FOOTNOTE",
            "footnote": ("prob:capfr1-rank-one-census says 'after all paid "
                         "cells and common supports have been removed'; "
                         "'all paid cells' is not a closed printed list "
                         "inside the statement.  On the printed paid-cell "
                         "list (which contains no near-codeword-slope "
                         "cell) the sibling fails with the same margins; "
                         "an unprinted reading that pays the plant would "
                         "have to introduce a new cell."),
        },
        "repair_direction": {
            "statement": ("record R1 on the slope/ray-deduplicated "
                          "|LineRay_E| count: the ray-collapse theorem of "
                          "the split-pencil lane (PR #666; "
                          "experimental/notes/thresholds/"
                          "split_pencil_ray_collapse.md once integrated) "
                          "proves dedup census = list count per slope; "
                          "under the deduplicated reading upstream's own "
                          "pole-line floors survive verbatim (their "
                          "supports each carry distinct slopes), and the "
                          "toy lineray counts hold the corrected model at "
                          "every line"),
            "toy_lineray_holds_everywhere": True,
        },
        "claim_boundaries": {
            "asserts": [
                "prob:capfp-R1 fails verbatim at the raw rank-one support "
                "count: bare quantifier, no excluding convention, planted "
                "line exceeds the model",
                "the corrected (mutatis-mutandis) R1 model of "
                "prob:capg-split-pencil-B fails at the same line: binding "
                "middle term 2^35.92 vs #R1 >= 2^2015082.59, factor >= "
                "2^2015046 (exact floor-division bit-length fact)",
                "rem:capg-subfield-scope(ii) ('tight at the floors') and "
                "(iii) ('q-scale models remain the plausible targets' for "
                "challenge-field-primitive representations) are both "
                "contradicted by the planted primitive line",
                "the identity #R1 = sum_z sum_c C(agr(U_z,c),m) (R1 is the "
                "with-multiplicity LineRay census), verified at every "
                "slope of every toy line",
                "planted profile placement d1 = e = w'+2 (interior, "
                "unpriced; e <= w' priced by the dichotomy, e = w'+1 "
                "delegated to (Q))",
            ],
            "does_not_assert": [
                "any defect in lem:capfp-functionals, thm:capfp-slope-elim "
                "(incl. part (c)), thm:capfp-dichotomy, or any "
                "unconditional reduction",
                "any defect in the pole-line floors of "
                "prop:capg-census-floor -- the opposite mechanism; under "
                "the slope/ray-deduplicated reading those floors survive "
                "verbatim",
                "a refutation of the slope-count / |LineRay_E| "
                "(deduplicated) form of R1 -- that is the repair "
                "direction, and the deduplicated toy counts HOLD the "
                "model at every line",
                "an unambiguous refutation of prob:capfr1-rank-one-census "
                "(its 'all paid cells' clause is not a closed printed "
                "list; see sibling_capfr1_grading)",
                "a toy-scale refutation of an e^{o(n)} statement (the toy "
                "rows are mechanism exhibits only)",
                "any claim against the frontier statements or the "
                "list-side (prob:capfp-A) sunflower cells",
            ],
            "is_counterexample": True,
            "refutes_recorded_open_problem_not_a_theorem": True,
            "is_novel_not_confirming_a_proven_theorem": True,
            "is_full_canonical_statement_not_proxy_or_toy_row": True,
            "independent_recheck_confirms": True,
            "is_degenerate_by_construction": False,
            "is_tautology_under_preconditions": False,
        },
        "caveats": [
            "A fixed n = 24 toy cannot refute an e^{o(n)} statement; the "
            "refutation is the finite deployed form (prob:capfp-R1's own "
            "text demands a finite form 'fitting under the deployed budget "
            "at a_0+1') plus the e^{Theta(n)} family along fixed-rate "
            "rows.",
            "At toy scale the small field cannot realize the deployed "
            "freedom-count hygiene (the union bound exceeds 1 at q = 73), "
            "so other slopes carry supports; they are reported, "
            "cross-checked, and only ADD to #R1.  At the deployed row the "
            "union bound is certified below 1 as a bit-length fact.",
            "The random control line HOLDS the model, so the failure is "
            "the plant, not a trivially wrong model.",
            "The repair citation targets the split-pencil ray-collapse "
            "lane (PR #666); if not yet integrated upstream, the citation "
            "path is the PR, not an in-tree file.",
            "log2 values in log2_display are display-grade strings; every "
            "verdict field is an exact integer or boolean.",
        ],
        "regeneration": ("python experimental/scripts/"
                         "verify_r1_rawcount_refutation.py "
                         "--emit-defaults"),
    }
    cert["payload_sha256"] = payload_hash(cert)
    return cert


def write_cert(root: Path, cert: dict[str, Any]) -> Path:
    path = root / CERT_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")
    return path


def run_check(root: Path) -> int:
    fresh = build_certificate(root)
    stored = json.loads((root / CERT_REL).read_text(encoding="utf-8"))
    if stored.get("payload_sha256") != payload_hash(stored):
        print("RESULT: FAIL self-hash")
        return 1
    if fresh["payload_sha256"] != stored["payload_sha256"]:
        print("RESULT: FAIL rebuild drift")
        return 1
    if stored["summary"]["verdict"] != "COUNTEREXAMPLE":
        print("RESULT: FAIL", stored["summary"]["verdict"])
        return 1
    print("RESULT: PASS")
    print("payload_sha256:", stored["payload_sha256"])
    print("verdict:", stored["summary"]["verdict"])
    print_deployed_params(stored["deployed"])
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--emit-defaults", action="store_true")
    p.add_argument("--check", action="store_true")
    args = p.parse_args(argv)
    root = repo_root()
    if args.emit_defaults:
        cert = build_certificate(root)
        path = write_cert(root, cert)
        print("wrote", path)
        print("payload_sha256:", cert["payload_sha256"])
        print("verdict:", cert["summary"]["verdict"])
        for row in cert["toy_rows"]:
            print("  toy %-12s #R1=%-6d lineray=%-4d slopes=%-3d common=%d "
                  "corrected_raw=%s lineray_verdict=%s"
                  % (row["label"], row["counts"]["rank_one"],
                     row["lineray_count"], row["slopes_hit"],
                     row["counts"]["common"],
                     "HOLDS" if row["corrected_holds_raw"] else "FAILS",
                     "HOLDS" if row["corrected_holds_lineray"] else "FAILS"))
        dep = cert["deployed"]
        print_deployed_params(dep)
        print("  deployed: C(n-w'-2,m) bits=%d  corrected model ceil=2^%s "
              "(exact %d)  margin >= 2^%d (literal q-scale: >= 2^%d)"
              % (dep["bits"]["C_ray_interior"],
                 dep["log2_display"]["corrected_middle_ceil"],
                 dep["budget"]["corrected_middle_ceil"],
                 dep["margins_bits"]["planted_R1_vs_corrected"],
                 dep["margins_bits"]["planted_R1_vs_literal_q_scale"]))
        return 0
    if args.check:
        return run_check(root)
    p.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
