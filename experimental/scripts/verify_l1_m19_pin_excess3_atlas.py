#!/usr/bin/env python3
"""verify_l1_m19_pin_excess3_atlas.py

Zero-arg, stdlib-only, deterministic, offline verifier for
`experimental/notes/l1/l1_m19_pin_excess3_atlas.md` -- the `m*(19) = 9` pin
(the `m = 8` block at `ell = 19`) and the excess-`3` atlas localization.

`m*(ell)` = the LISTING ONSET: the smallest `m` for which some realizable
`Gamma` at level `ell` crosses `top-m >= 2 ell`. The note proves, conditional on
`H_19` (no realizable `Gamma` at `ell = 19` has `E_3 >= ell+3 = 22`), that
`m*(19) = 9` exactly; the `m = 10, 11` attainment witnesses are non-minimal
crossings on the ladder `m = 9,10,11` and are consistent with onset `= 9`.

Self-contained: imports NO sibling verifier. Every arithmetic fact below is a
fresh reimplementation matching the shipped convention (per-coset MAX fiber,
coset key `x^ell mod p`, `Gamma` constant-free `sum_{r=1}^{ell-1} gamma_r X^r`).

Six gates; exit 0 iff ALL pass (normal mode) or ALL tampers are CAUGHT
(`--tamper-selftest`), nonzero otherwise. Target run time < 90s (typ. < 1s).

  (i)   SPINE enumeration (PROVED-HERE). Enumerate ALL descending top-8 profiles
        `mu_1>=...>=mu_8>=1` at `ell=19` with the PROVED pairwise cap
        `mu_1+mu_2<=19` and the crossing condition `top-8 >= 2*19 = 38`. Pin
        17012 crossers, 0 violations of the bridge `top-8<=16+E_3`, the excess
        identity `T=excess+4+capslack`, `capslack>=0`, `excess>=3`, `T>=7`;
        `min E_3=22`, `min excess=3`, `min T=7`, `min mu_2=4`. Then Lemma R
        `sum mu(mu-1)<=306` leaves 11927 survivors, and the cap-tight (`T=7`)
        frontier is 59 shapes with unique `j=3` shape `[10,9,9,2^5]`.
  (ii)  EXCESS LADDER (PROVED). `needs E_3 >= 2(ell-m)` from the bridge at
        `top-m>=2 ell`; pin the integers for `m=11..7` and that the #364
        (`E_3=20`) and #647 (`E_3=18`) witnesses land on the `m=9` / `m=10`
        rungs; the onset lands at `m=9` because required excess jumps `+1 -> +3`
        over the realizable ceiling `+2`.
  (iii) WITNESS spectra (WITNESS). Recompute the #364 `p=571` band witness and
        the #647 `p=647` attainment witness spectra from raw `gamma` over `F_p`;
        pin `[16,3^6,2^6,1^17]` `E_3=20,T=5,top-8=36,top-9=38` and
        `[12,7,4,3,2^10,1^20]` `E_3=18,top-9=36,top-10=38`.
  (iv)  ATLAS partition (AUDIT, from lane T1 / #379). Enumerate the excess=3
        atlas (two PROVED caps) for `ell in {17,19,23,29}` and pin the
        4-way partition FAT-TAIL/MIN-J/BIG3TAIL/MIDDLE, the atlas totals, and
        the cap-tight (`T=7`) counts.
  (v)   k3 CAP arithmetic (PROVED x2, from lane T1). Pin the two Theta(ell)
        caps Lemma-R `(2ell-5)/3` and cyclotomic-pair `2(ell-1)/3` for
        `ell in {17,19,23,29,31,43,53}` (O(1) plateau REFUTED 2026-07-07: exhaustive-gauge
        max k3 GROWS -- 6 at ell=19 [pin-safe, excess +1], 8 at ell=43 [C'<=2 falsifier],
        11 at ell=53 [record, excess +6]; see l1_k3_growth_refutation.md), and verify the
        `deg R_zeta = 5`, `X|R_zeta`
        structural claim SYMBOLICALLY (exact polynomial arithmetic over F_p) at
        one small case.
  (vi)  UNIQUE-Gamma nullspace-dim-1 crack (PROVED, #382 Thm 1). At one cap-tight
        plant `(a,ell-a)=(10,9)` at `ell=19,p=191`, the planted-fiber coincidence
        rows have nullspace dimension EXACTLY 1 -- the top pair forces a unique
        `Gamma` (deterministic per-plant realizability check).
"""
import sys
import time

# ======================================================================
# pinned data (from lanes T2/T1 derivations + the integrated notes)
# ======================================================================
ELL19 = 19
M8 = 8

# --- gate (i) spine pins ---
SPINE = dict(crossers=17012, survivors=11927, frontier_T7=59,
             min_E3=22, min_excess=3, min_T=7, min_mu2=4,
             unique_j3=(10, 9, 9, 2, 2, 2, 2, 2))

# --- gate (ii) excess ladder pins: m -> needs E_3 = 2*(ell-m) at ell=19 ---
LADDER_M = [11, 10, 9, 8, 7]
LADDER_NEEDS_E3 = [16, 18, 20, 22, 24]          # = 2*(19-m)
LADDER_EXCESS = [-3, -1, 1, 3, 5]               # = needs - ell

# --- gate (iii) witnesses (raw gamma = coeffs of X^1..X^18) ---
WIT_364 = dict(ell=19, p=571, n=30,
    gamma=[545, 15, 163, 341, 470, 274, 474, 224, 174, 556, 179, 28, 321,
           233, 543, 54, 203, 1],
    spectrum={16: 1, 3: 6, 2: 6, 1: 17}, E3=20, T=5, top8=36, top9=38, top10=40)
WIT_647 = dict(ell=19, p=647, n=34,
    gamma=[298, 638, 143, 294, 14, 111, 237, 78, 464, 166, 355, 385, 207,
           68, 465, 369, 316, 1],
    spectrum={12: 1, 7: 1, 4: 1, 3: 1, 2: 10, 1: 20}, E3=18, top8=34, top9=36, top10=38)

# --- gate (iv) atlas partition pins: ell -> (atlas, cap_tight, FAT, MINJ, BIG3, MID) ---
ATLAS = {
    17: dict(atlas=447,  cap_tight=51,  FAT=1, MINJ=0,  BIG3=11, MID=435),
    19: dict(atlas=792,  cap_tight=66,  FAT=1, MINJ=1,  BIG3=13, MID=777),
    23: dict(atlas=2166, cap_tight=96,  FAT=1, MINJ=5,  BIG3=17, MID=2143),
    29: dict(atlas=7989, cap_tight=141, FAT=1, MINJ=16, BIG3=23, MID=7949),
}

# --- gate (v) k3 caps pins: ell -> (LemmaR (2ell-5)/3, R_zeta 2(ell-1)/3, exhaustive-gauge max k3) ---
# CORRECTED 2026-07-07: the empirical max k3 is NOT a uniform O(1) "7" (that was a small-ell
# mirage); the exhaustive-up-to-gauge max GROWS with ell -- crossing the fat-tail falsifier
# k3=8 at ell=43 and reaching 11 at ell=53 (excess +6, T=10; it also grows with n at fixed
# ell: 53 gives 7 at n=14 vs 11 at n=20). The two Theta(ell) caps still hold and are no
# longer read as overshoots (they bracket the growth from above). Values below are the true
# exhaustive-gauge maxima, re-verified in the companion packet (l1_k3_growth_refutation.md /
# verify_l1_k3_growth_refutation.py). The ell=19 entry (6, attained only at the n=30 window
# boundary) is the pin-relevant one: excess = k3-5 = +1, so H_19 is untouched.
K3CAPS = {17: (9, 10, 7), 19: (11, 12, 6), 23: (13, 14, 5),
          29: (17, 18, 7), 31: (19, 20, 7), 43: (27, 28, 8), 53: (33, 34, 11)}


# ======================================================================
# shared stdlib machinery
# ======================================================================
def pos(x):
    return x if x > 0 else 0


def gen_desc(m, hi):
    """all descending m-tuples mu_1>=...>=mu_m, 1<=mu_i<=hi."""
    def rec(k, cap, cur):
        if k == m:
            yield tuple(cur)
            return
        for v in range(cap, 0, -1):
            cur.append(v)
            yield from rec(k + 1, v, cur)
            cur.pop()
    yield from rec(0, hi, [])


def analyse8(mu, ell):
    """spine analysis of a top-8 profile (cheapest size-1 tail)."""
    top8 = sum(mu)
    capslack = ell - (mu[0] + mu[1])
    E3 = sum(pos(x - 2) for x in mu)
    T = sum(pos(mu[k] - 2) for k in range(2, 8))
    j = sum(1 for x in mu if x >= 3)
    lemR = sum(x * (x - 1) for x in mu)
    return dict(mu=mu, top8=top8, capslack=capslack, E3=E3, excess=E3 - ell,
                T=T, j=j, lemR=lemR, mu2=mu[1])


# ---- spectrum from raw gamma over F_p (coset key x^ell) ----
def spectrum_from_gamma(gamma, p, ell):
    from collections import Counter, defaultdict
    cosets = defaultdict(list)
    for x in range(1, p):
        val = 0
        xp = 1
        for r in range(1, ell):
            xp = (xp * x) % p
            val = (val + gamma[r - 1] * xp) % p
        cosets[pow(x, ell, p)].append(val)
    mus = []
    for vals in cosets.values():
        mus.append(max(Counter(vals).values()))
    mus.sort(reverse=True)
    return mus


def topm(mus, m):
    return sum(mus[:m])


def E3_of(mus):
    return sum(max(mu - 2, 0) for mu in mus)


def T_of(mus):
    return sum(max(mus[k] - 2, 0) for k in range(2, len(mus)))


def compress(mus):
    from collections import Counter
    return dict(sorted(Counter(mus).items(), reverse=True))


# ---- atlas enumeration ----
def partitions_desc(total, maxpart):
    def rec(rem, cap):
        if rem == 0:
            yield []
            return
        for first in range(min(rem, cap), 0, -1):
            for tail in rec(rem - first, first):
                yield [first] + tail
    yield from rec(total, maxpart)


def enumerate_atlas(ell, excess=3):
    E = ell + excess
    LR = (ell - 1) * (ell - 2)
    maxpart = ell - 5
    shapes = []
    for part in partitions_desc(E, maxpart):
        mu = [e + 2 for e in part]
        if mu[0] + mu[1] > ell:
            continue
        if sum(m * (m - 1) for m in mu) > LR:
            continue
        shapes.append(mu)
    return shapes


def classify_atlas(mu, ell):
    j = len(mu)
    capslack = ell - (mu[0] + mu[1])
    fat_tail = (mu[0] == ell - 3 and all(m == 3 for m in mu[1:]))
    if fat_tail:
        cls = "FAT"
    elif j == 3:
        cls = "MINJ"
    elif mu[1] == 3:
        cls = "BIG3"
    else:
        cls = "MID"
    return cls, capslack


# ---- exact F_p polynomial arithmetic (for R_zeta symbolic check) ----
def pmul(a, b, p):
    r = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai:
            for k, bk in enumerate(b):
                r[i + k] = (r[i + k] + ai * bk) % p
    return r


def compose_zeta(poly, zeta, p):
    """poly(zeta*X): multiply coeff i by zeta^i."""
    out, zp = [], 1
    for c in poly:
        out.append(c * zp % p)
        zp = zp * zeta % p
    return out


def psub(a, b, p):
    n = max(len(a), len(b))
    r = [0] * n
    for i in range(len(a)):
        r[i] = a[i] % p
    for i in range(len(b)):
        r[i] = (r[i] - b[i]) % p
    while len(r) > 1 and r[-1] == 0:
        r.pop()
    return r


# ---- linear algebra over F_p (for unique-Gamma dim check) ----
def inv(a, p):
    return pow(a % p, p - 2, p)


def is_prime(m):
    if m < 2:
        return False
    if m % 2 == 0:
        return m == 2
    d = 3
    while d * d <= m:
        if m % d == 0:
            return False
        d += 2
    return True


def find_gen(p):
    m, d, fac = p - 1, 2, set()
    while d * d <= m:
        while m % d == 0:
            fac.add(d)
            m //= d
        d += 1
    if m > 1:
        fac.add(m)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fac):
            return g
    raise RuntimeError("no generator")


def cosets_of(p, ell):
    n = (p - 1) // ell
    g = find_gen(p)
    zeta = pow(g, n, p)
    H = [pow(zeta, jj, p) for jj in range(ell)]
    return [[pow(g, i, p) * h % p for h in H] for i in range(n)]


def fiber_rows(points, p, ell):
    if len(points) < 2:
        return []
    x0 = points[0]
    v0 = [pow(x0, r, p) for r in range(1, ell)]
    return [[(v0[r - 1] - pow(x, r, p)) % p for r in range(1, ell)] for x in points[1:]]


def nullity(rows, ncols, p):
    if not rows:
        return ncols
    A = [[v % p for v in r] for r in rows]
    m = len(A)
    rank = 0
    for c in range(ncols):
        pr = None
        for i in range(rank, m):
            if A[i][c] % p:
                pr = i
                break
        if pr is None:
            continue
        A[rank], A[pr] = A[pr], A[rank]
        iv = inv(A[rank][c], p)
        A[rank] = [(v * iv) % p for v in A[rank]]
        for i in range(m):
            if i != rank and A[i][c] % p:
                f = A[i][c]
                A[i] = [(A[i][j] - f * A[rank][j]) % p for j in range(ncols)]
        rank += 1
        if rank == m:
            break
    return ncols - rank


# ======================================================================
# GATES
# ======================================================================
def gate_i_spine(tamper=False):
    ell = ELL19
    target = 2 * ell                     # 38
    if tamper:
        target -= 1                       # 37: enumeration + min-excess both break
    LR = (ell - 1) * (ell - 2)            # 306
    crossers = []
    for mu in gen_desc(M8, ell - 1):
        if mu[0] + mu[1] > ell:           # PROVED pairwise cap
            continue
        if sum(mu) < target:              # crossing top-8 >= 2*ell
            continue
        crossers.append(analyse8(mu, ell))
    n_cross = len(crossers)
    bad = sum(1 for r in crossers if r['excess'] < 3 or r['T'] < 7
              or r['top8'] > 2 * M8 + r['E3']
              or r['T'] != r['excess'] + 4 + r['capslack']
              or r['capslack'] < 0)
    mn_E3 = min(r['E3'] for r in crossers)
    mn_ex = min(r['excess'] for r in crossers)
    mn_T = min(r['T'] for r in crossers)
    mn_mu2 = min(r['mu2'] for r in crossers)
    survivors = [r for r in crossers if r['lemR'] <= LR]
    frontier = [r for r in survivors if r['T'] == 7]
    j3 = [tuple(r['mu']) for r in frontier if r['j'] == 3]
    ok = (n_cross == SPINE['crossers'] and bad == 0
          and mn_E3 == SPINE['min_E3'] and mn_ex == SPINE['min_excess']
          and mn_T == SPINE['min_T'] and mn_mu2 == SPINE['min_mu2']
          and len(survivors) == SPINE['survivors']
          and len(frontier) == SPINE['frontier_T7']
          and len(j3) == 1 and j3[0] == SPINE['unique_j3'])
    return ok, ("crossers=%d (pin %d) violations=%d minE3=%d minexcess=%d minT=%d minmu2=%d | "
                "LemmaR-survivors=%d (pin %d) T=7-frontier=%d (pin %d) unique-j3=%s"
                % (n_cross, SPINE['crossers'], bad, mn_E3, mn_ex, mn_T, mn_mu2,
                   len(survivors), SPINE['survivors'], len(frontier), SPINE['frontier_T7'],
                   list(j3[0]) if j3 else None))


def gate_ii_ladder(tamper=False):
    ell = ELL19
    if tamper:
        ell += 1                          # break the formula needs=2*(ell-m)
    needs = [2 * (ell - m) for m in LADDER_M]
    excess = [nn - ELL19 for nn in needs]
    # witnesses land on rungs: #647 E3=18 -> m=10 rung; #364 E3=20 -> m=9 rung
    idx10 = LADDER_M.index(10)
    idx9 = LADDER_M.index(9)
    rung_ok = (needs[idx10] == WIT_647['E3'] and needs[idx9] == WIT_364['E3'])
    ok = (needs == LADDER_NEEDS_E3 and excess == LADDER_EXCESS and rung_ok)
    return ok, ("needs_E3 %s (pin %s) excess %s | m=10 rung=%d (#647 E3=%d) m=9 rung=%d (#364 E3=%d)"
                % (needs, LADDER_NEEDS_E3, excess, needs[idx10], WIT_647['E3'],
                   needs[idx9], WIT_364['E3']))


def _check_witness(w, tamper):
    gamma = list(w['gamma'])
    if tamper:
        gamma[0] = (gamma[0] + 1) % w['p']
    mus = spectrum_from_gamma(gamma, w['p'], w['ell'])
    return (compress(mus) == w['spectrum'] and E3_of(mus) == w['E3']
            and topm(mus, 8) == w['top8'] and topm(mus, 9) == w['top9']
            and topm(mus, 10) == w['top10'] and len(mus) == w['n']), mus


def gate_iii_witnesses(tamper=False):
    ok364, m364 = _check_witness(dict(WIT_364, top9=38, top10=40), tamper)
    ok647, m647 = _check_witness(dict(WIT_647, top9=36, top10=38), tamper)
    # extra pin: #364 T=5 (sigma-calculus, from 3rd fiber onward)
    okT = (T_of(m364) == WIT_364['T'])
    ok = ok364 and ok647 and okT
    return ok, ("#364 p=571 %s E3=%d T=%d top8/9=%d/%d | #647 p=647 %s E3=%d top9/10=%d/%d"
                % (compress(m364), E3_of(m364), T_of(m364), topm(m364, 8), topm(m364, 9),
                   compress(m647), E3_of(m647), topm(m647, 9), topm(m647, 10)))


def gate_iv_atlas(tamper=False):
    excess = 3
    if tamper:
        excess = 2                        # different atlas -> counts miss the pins
    ok = True
    detail = []
    for ell in sorted(ATLAS):
        pin = ATLAS[ell]
        shapes = enumerate_atlas(ell, excess)
        from collections import Counter
        cls = Counter()
        cap_tight = 0
        for mu in shapes:
            c, capslack = classify_atlas(mu, ell)
            cls[c] += 1
            if capslack == 0:
                cap_tight += 1
        got = dict(atlas=len(shapes), cap_tight=cap_tight, FAT=cls['FAT'],
                   MINJ=cls['MINJ'], BIG3=cls['BIG3'], MID=cls['MID'])
        match = all(got[k] == pin[k] for k in pin)
        # partition must sum to the atlas total
        part_sum = got['FAT'] + got['MINJ'] + got['BIG3'] + got['MID']
        match = match and (part_sum == got['atlas'])
        ok = ok and match
        detail.append("ell=%d atlas=%d(pin %d) cap-tight=%d FAT=%d MINJ=%d BIG3=%d MID=%d"
                      % (ell, got['atlas'], pin['atlas'], got['cap_tight'],
                         got['FAT'], got['MINJ'], got['BIG3'], got['MID']))
    return ok, "  ||  ".join(detail)


def gate_v_k3caps(tamper=False):
    # (a) the two Theta(ell) cap integers, and that each exhaustive-gauge max obeys BOTH caps
    caps_ok = True
    for ell, (lr, rz, emp) in K3CAPS.items():
        if (2 * ell - 5) // 3 != lr or (2 * (ell - 1)) // 3 != rz or emp > min(lr, rz):
            caps_ok = False
    # (a') the O(1) plateau is REFUTED (2026-07-07): max k3 is <=7 for ell<=31 but 8 at ell=43
    #      and 11 at ell=53, so it is NOT a uniform constant (nor 8-capped) -- and the ell=19
    #      entry (pin-relevant) is 6 (excess +1).
    plateau_refuted = (max(K3CAPS[e][2] for e in (17, 19, 23, 29, 31)) == 7
                       and K3CAPS[43][2] == 8 and K3CAPS[53][2] == 11 and K3CAPS[19][2] == 6)
    caps_ok = caps_ok and plateau_refuted
    # (b) symbolic R_zeta = q(X)A_drop(zeta X) - q(zeta X)A_drop(X): deg 5, X | R_zeta.
    #     Exact polynomial arithmetic over F_p on a representative (q deg 2, A_drop deg 3)
    #     construction -- this checks the R_zeta identity engine and the deg = deg q +
    #     deg A_drop / constant-term-cancels structure (zeta != 1); it is NOT a re-proof
    #     of the fat-tail k3 <= 2(ell-1)/3 cap, whose integer is pinned in (a) from lane T1.
    p = 191
    q = [3, 5, 7]                          # deg 2, q2=7 != 0
    Ad = [1]
    for d in (2, 11, 29):                  # A_drop = prod (X - d), deg 3, roots distinct
        Ad = pmul(Ad, [(-d) % p, 1], p)
    g = find_gen(p)
    zeta = pow(g, (p - 1) // 19, p)        # primitive 19th root of unity
    if tamper:
        zeta = 1                           # trivial root collapses R_zeta -> deg != 5
    R = psub(pmul(q, compose_zeta(Ad, zeta, p), p),
             pmul(compose_zeta(q, zeta, p), Ad, p), p)
    deg = len(R) - 1
    x_divides = (R[0] % p == 0)
    sym_ok = (deg == 5 and x_divides)
    ok = caps_ok and sym_ok
    return ok, ("caps: LemmaR/(R_zeta) [%s] hold; O(1) PLATEAU REFUTED -- exhaustive-gauge max k3 "
                "grows (ell19:6 excess+1 pin-safe; ell43:8 = C'<=2 falsifier; ell53:11 record, "
                "excess+6, see l1_k3_growth_refutation.md) | symbolic R_zeta deg=%d (pin 5) "
                "X|R_zeta=%s"
                % (",".join("%d:%d/%d" % (e, K3CAPS[e][0], K3CAPS[e][1]) for e in sorted(K3CAPS)),
                   deg, x_divides))


def gate_vi_uniqueGamma(tamper=False):
    ell, p = ELL19, 191
    a, b = 10, ell - 10                    # cap-tight pair (10,9), sum = ell
    if tamper:
        b -= 1                             # (10,8): not cap-tight -> nullspace dim > 1
    cs = cosets_of(p, ell)
    F1 = sorted(cs[0])[:a]
    F2 = sorted(cs[1])[:b]
    rows = fiber_rows(F1, p, ell) + fiber_rows(F2, p, ell)
    dim = nullity(rows, ell - 1, p)
    ok = (dim == 1)
    return ok, ("cap-tight plant (a,ell-a)=(%d,%d) sum=%d at ell=19,p=191: "
                "nullspace dim=%d (pin exactly 1 => unique Gamma / #382 Thm 1)"
                % (a, b, a + b, dim))


GATES = [
    ("(i)   spine enumeration (17012/11927/59) ", gate_i_spine),
    ("(ii)  excess ladder integers             ", gate_ii_ladder),
    ("(iii) #364/#647 witness spectra          ", gate_iii_witnesses),
    ("(iv)  excess=3 atlas partition (4 ells)   ", gate_iv_atlas),
    ("(v)   k3 caps + symbolic R_zeta (deg 5)  ", gate_v_k3caps),
    ("(vi)  unique-Gamma nullspace dim=1        ", gate_vi_uniqueGamma),
]


def main():
    t0 = time.time()
    selftest = "--tamper-selftest" in sys.argv
    print("=" * 94)
    if selftest:
        print(" TAMPER SELF-TEST: each gate must FAIL when its guarded datum is flipped")
    else:
        print(" verify_l1_m19_pin_excess3_atlas (zero-arg)  --  m*(19)=9 pin (conditional on H_19) + excess-3 atlas")
        print(" note: experimental/notes/l1/l1_m19_pin_excess3_atlas.md")
    print("=" * 94)
    all_good = True
    for name, fn in GATES:
        gt0 = time.time()
        if selftest:
            ok, _ = fn(tamper=True)
            caught = not ok
            all_good = all_good and caught
            print("  %s  TAMPER %s  [%.1fs]"
                  % (name, "CAUGHT " if caught else "MISSED!", time.time() - gt0))
        else:
            ok, summ = fn(tamper=False)
            all_good = all_good and ok
            print("  %s  %s  [%.1fs]" % (name, "PASS" if ok else "FAIL", time.time() - gt0))
            print("        %s" % summ)
    print("=" * 94)
    if selftest:
        print(" SELF-TEST: %s   (%.1fs)"
              % ("all tampers CAUGHT" if all_good else "A TAMPER WAS MISSED", time.time() - t0))
    else:
        print(" RESULT: %s   (%.1fs)"
              % ("ALL GATES PASS" if all_good else "FAILURE", time.time() - t0))
    sys.exit(0 if all_good else 1)


if __name__ == "__main__":
    main()
