#!/usr/bin/env python3
"""verify_l1_k3_growth_refutation.py

Zero-arg, stdlib-only, deterministic verifier for
`experimental/notes/l1/l1_k3_growth_refutation.md`.

The note REFUTES, over `F_p`, three of our own conjectured caps on the fat-tail
`[ell-3, 3^{k3}]` family (per-coset-MAX / spectrum_A convention; `E_3 =
sum(mu_k-2)_+`, `T = sum_{k>=3}(mu_k-2)_+`, `excess = E_3 - ell = k3 - 5`):

  * `C' <= 2`  (i.e. `E_3 <= ell+2`)                     -- REFUTED (excess up to +4)
  * "no realizable `T >= 7`"  (the open core of PR #368) -- REFUTED (T = 7,8 realized)
  * the uniform `O(1)` fat-tail cap `k3 <= 7` (PR #399 (star), PR #379 plateau)
                                                          -- REFUTED (max k3 grows with ell)

by exhibiting genuine mixed constant-free degree-(ell-1) Gammas and by
exhaustive-up-to-rotation-gauge computation showing `max k3` GROWS with `ell`
(and, at ell=53, with n: 7 at n=14 -> 11 at n=20).
The `ell=19` pin `H_19` is shown UNTOUCHED (fat-tail excess <= +1 there).

Ground rule (house style, matching the L1 verifier series): SELF-CONTAINED. This
script embeds its own stdlib F_p machinery (cubic-pencil fat-tail construction,
coset spectra, P^2 concurrency max-k3, rotation-gauge reduction). It imports NO
sibling script and depends on NO other file's claims being true; every quantity
the note states per witness -- including c1 -- is recomputed here from
`(p, ell, D, q)` alone. The note's Sec 1 nondegeneracy lemma (the concurrency
cross product never vanishes for distinct points of a tail coset) is enforced
as an ASSERTION in the tally, not a silent skip.

Gates (exit 0 iff ALL pass; zero-arg runs gates 1-5 incl. tamper self-tests,
measured < 60s):

  (1) WITNESSES rebuilt from (p, ell, drop-SET D, q = X^2+bX+c): spectrum /
      E_3 / T / excess / k3 / c1 recomputed exactly; constant-free & degree =
      ell-1 checked; mu_1 = ell-3; an INDEPENDENT pencil-count of k3
      cross-checks the via-Gamma k3 on the four primary + the ell=23 record;
      [40,3^8] head asserted. Four PRIMARY falsifiers:
        ell=43 p=431 : [40,3^8]        E_3=46=ell+3 excess+3 T=7  k3=8  (C'<=2 & T1 falsifier)
        ell=53 p=1061: [50,3^11,2^6]   E_3=59=ell+6 excess+6 T=10 k3=11 (the RECORD; = exhaustive max)
        ell=53 p=1061: [50,3^9,2^3]    E_3=57=ell+4 excess+4 T=8  k3=9  (the lane's (0,1,k) record)
        ell=59 p=709 : [56,3^9,2]      E_3=63=ell+4 excess+4 T=8  k3=9
      four BAND witnesses (excess >= +3 persists across ell in {43,53,59,61,67,71,73}):
        ell=61 p=733 : [58,3^9,2^2]    excess+4 T=8 k3=9  (R2 exhaustive max; upgrades the
                                        shipped (0,1,k) lower bound 8 at the same prime)
        ell=67 p=1609: [64,3^9,2^12]   excess+4 T=8 k3=9  (witness lower bound)
        ell=71 p=853 : [68,3^9,2^2]    excess+4 T=8 k3=9  (R2 exhaustive max, n=12)
        ell=73 p=877 : [70,3^9,2^2]    excess+4 T=8 k3=9  (R2 exhaustive max, n=12)
      and two R2 coverage-extension records:
        ell=23 p=1657: [20,3^7]        E_3=25=ell+2 excess+2 T=6 k3=7 (NEW ell=23 max; LATE
                                        record at R2's largest ell=23 prime; pencil-checked)
        ell=43 p=1721: [40,3^8,2^4]    excess+3 T=7 k3=8 (recurrence of the ell=43 max at n=40)
  (2) ell=19 PIN SURVIVES: exhaustive-up-to-gauge max k3 over ALL eligible
      primes n in [2,30] (self-verifies p=191 is the smallest) is 6, attained
      only at p=571 (n=30, the window boundary); p=191 gives 5; the three
      beyond-window primes 647/761/1103 (n=34/40/58) give 5 -- so fat-tail
      excess <= +1 at ell=19 across the scanned range, H_19 untouched.
  (3) GROWTH + corrections: exhaustive-up-to-gauge max k3 at small ell
      (11->4, 13->4, 17->7, 23->5-at-139, 29->7, 31->7: the ell<=31 mirage
      window; the ell=23 SUP moved to 7 at p=1657, gate 1 + --full);
      ell=17,p=409 -> exhaustive max k3=5 (corrects PR #368's reported 3, a
      1-of-680-plant undercount); ell=43,p=431 gauge scan REACHES k3=8.
  (4) TAMPER self-tests (>=5): a mutated q-coefficient at ell=43, a wrong
      claimed spectrum head, a claim k3=7-at-ell=43, a mutated q on the
      ell=53 k3=11 record, and tampered R2 deep-sweep stats must each be
      REJECTED.
  (5) R2 ARTIFACT consistency (the ell=19 DEEP NULL): load the in-repo
      data/certificates/l1-e3-law/l1_k3_growth_r2_scan.json and assert -- 80
      ell=19 rows (ALL eligible primes to p=13567), every k3 <= 6, the 6
      unique at (571, n=30), distribution 3:42/4:15/5:22/6:1; the ell=23 grid
      max 7 at n=72 only; the ell=53 grid sequence 1,7,11,7,8,7; 9 four-route
      witnesses present. (Two of the 80 rows -- p=1901 and p=13567 -- were
      additionally replayed by this packet's own transversal at build time.)

Opt-in `--full` (documented, ~25-35 min): replays live, with NO early exit,
every within-budget (ell, p) pair of the note's Sec 3 coverage column -- the
original 37 rows (incl. (53,1061)->11, the value the originating lane's
early-exit-at->=8 scanner truncated to 9; (53,743)->7; (59,709)->9) plus
(23,1657)->7, (43,1721)->8, and six deterministic ell=19 deep-sweep spot rows
(p in {1787,1901,2053,4409,8209,13567}). The R2-heavy rows NOT in --full (the
full 80-prime ell=19 sweep, the 44-prime ell=17 extension, the exhaustive
61/71/73 scans) are established by the R2 artifact + gate 5 + gate-1
witnesses; per-row provenance is the note's Sec 3 coverage column.
"""
import sys
import itertools
from collections import defaultdict, Counter

# ======================================================================
# stdlib F_p machinery (embedded; low-degree-first polynomial lists)
# ======================================================================


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


def pmod(poly, p):
    r = [c % p for c in poly]
    while len(r) > 1 and r[-1] == 0:
        r.pop()
    return r


def padd(a, b, p):
    n = max(len(a), len(b))
    return pmod([(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)], p)


def psub(a, b, p):
    n = max(len(a), len(b))
    return pmod([(a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0) for i in range(n)], p)


def pscale(a, s, p):
    return pmod([(c * s) % p for c in a], p)


def pmul(a, b, p):
    if a == [0] or b == [0]:
        return [0]
    r = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j, bj in enumerate(b):
            r[i + j] = (r[i + j] + ai * bj) % p
    return pmod(r, p)


def peval(a, x, p):
    r = 0
    for c in reversed(a):
        r = (r * x + c) % p
    return r


def pdivmod(a, b, p):
    a = pmod(a, p)
    b = pmod(b, p)
    if b == [0]:
        raise ZeroDivisionError
    invlead = pow(b[-1], p - 2, p)
    q = [0] * (max(0, len(a) - len(b) + 1) or 1)
    r = a[:]
    while len(r) >= len(b) and r != [0]:
        deg = len(r) - len(b)
        coef = (r[-1] * invlead) % p
        if deg < len(q):
            q[deg] = coef
        for i, bc in enumerate(b):
            r[i + deg] = (r[i + deg] - coef * bc) % p
        r = pmod(r, p)
        if r == [0]:
            break
    return pmod(q, p), pmod(r, p)


def poly_from_roots(roots, p):
    r = [1]
    for a in roots:
        r = pmul(r, [(-a) % p, 1], p)
    return r


def find_primitive_root(p):
    m = p - 1
    fac = set()
    d = 2
    while d * d <= m:
        if m % d == 0:
            fac.add(d)
            while m % d == 0:
                m //= d
        d += 1
    if m > 1:
        fac.add(m)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fac):
            return g
    raise RuntimeError("no primitive root")


def mu_ell_list(p, ell):
    g = find_primitive_root(p)
    h = pow(g, (p - 1) // ell, p)
    return [pow(h, i, p) for i in range(ell)], g


def coset_index_map(p, ell, g):
    n = (p - 1) // ell
    dlog = [0] * p
    cur = 1
    for e in range(p - 1):
        dlog[cur] = e
        cur = (cur * g) % p

    def cidx(x):
        return dlog[x] % n

    return cidx, n


def inv_table(p):
    inv = [0] * p
    inv[1] = 1
    for i in range(2, p):
        inv[i] = (-(p // i) * inv[p % i]) % p
    return inv


# ---------- fat-tail Gamma construction + spectrum ----------


def build_gamma_fat(p, ell, drop, qcoef):
    """drop = list of 3 ell-th roots of unity (a SET of field elements);
       qcoef = [q0,q1,q2] low-degree-first quadratic  (q = q2 X^2 + q1 X + q0).
       Gamma(X) = c1 + (X^ell-1) q(X) / A_drop(X),  A_drop = prod (X - d)."""
    A_drop = poly_from_roots(drop, p)
    Xell_m1 = pmod([-1] + [0] * (ell - 1) + [1], p)
    quo, rem = pdivmod(Xell_m1, A_drop, p)
    assert rem == [0], "A_drop must divide X^ell-1 (drops must be ell-th roots of unity)"
    q = pmod(qcoef, p)
    body = pmul(quo, q, p)
    A0 = peval(A_drop, 0, p)
    c1 = (peval(q, 0, p) * pow(A0, p - 2, p)) % p
    Gamma = pmod(padd([c1], body, p), p)
    assert peval(Gamma, 0, p) == 0, "Gamma not constant-free"
    return Gamma, A_drop, q, c1


def spectrum(Gamma, p, ell, g):
    cidx, n = coset_index_map(p, ell, g)
    cosets = [defaultdict(int) for _ in range(n)]
    for x in range(1, p):
        cosets[cidx(x)][peval(Gamma, x, p)] += 1
    mus = [max(c.values()) if c else 0 for c in cosets]
    mus.sort(reverse=True)
    return mus


def spectrum_compact(mus):
    c = Counter(mus)
    parts = []
    for val in sorted(c, reverse=True):
        if val <= 1:
            continue
        cnt = c[val]
        parts.append("%d^%d" % (val, cnt) if cnt > 1 else "%d" % val)
    return "[" + ",".join(parts) + "]"


def E3_T_excess(mus, ell):
    E3 = sum(max(m - 2, 0) for m in mus)
    T = sum(max(mus[k] - 2, 0) for k in range(2, len(mus)))
    return E3, T, E3 - ell


def count_k3(Gamma, p, ell, g):
    """k3 = # tail cosets (!= coset of 1) whose max fiber size >= 3; mu1 = big-fiber coset."""
    cidx, n = coset_index_map(p, ell, g)
    cosets = [defaultdict(int) for _ in range(n)]
    for x in range(1, p):
        cosets[cidx(x)][peval(Gamma, x, p)] += 1
    k3 = 0
    mu1 = 0
    for k in range(n):
        mx = max(cosets[k].values()) if cosets[k] else 0
        if k == 0:
            mu1 = mx
        elif mx >= 3:
            k3 += 1
    return k3, mu1


def count_coset_aligned_pencil(p, ell, drop, qcoef, g):
    """INDEPENDENT k3: directly count members of {q - lam A_drop} with 3 roots in one tail coset."""
    A_drop = poly_from_roots(drop, p)
    q = pmod(qcoef, p)
    cidx, n = coset_index_map(p, ell, g)
    seen = set()
    for lam in range(p):
        cub = psub(q, pscale(A_drop, lam, p), p)
        if len(cub) - 1 != 3:
            continue
        roots = [x for x in range(1, p) if peval(cub, x, p) == 0]
        if len(roots) != 3:
            continue
        cs = set(cidx(x) for x in roots)
        if len(cs) == 1 and 0 not in cs:
            seen.add(next(iter(cs)))
    return len(seen)


# ---------- exact P^2-concurrency max k3 (no q-sweep) + rotation gauge ----------


def max_k3_for_drop(p, ell, drop, cidx, n, INV):
    a = poly_from_roots(drop, p)
    a0, a1, a2, a3 = a[0], a[1], a[2], a[3]
    coset_pts = defaultdict(list)
    for x in range(1, p):
        k = cidx(x)
        if k != 0:
            coset_pts[k].append(x)
    qmap = defaultdict(set)
    for k, pts in coset_pts.items():
        w = {}
        for x in pts:
            av = (((a3 * x + a2) * x + a1) * x + a0) % p
            # Nondegeneracy (note Sec 1): A_D's roots are the drops, which lie in
            # coset 0 -- so A_D(x) != 0 on every tail coset. Assert, don't skip.
            assert av != 0, "A_D vanished on a tail coset point (impossible)"
            iv = INV[av]
            w[x] = ((x * x % p) * iv % p, (x * iv) % p, iv)
        for (x1, x2, x3) in itertools.combinations(pts, 3):
            w1, w2, w3 = w[x1], w[x2], w[x3]
            d12a = (w1[0] - w2[0]) % p
            d12b = (w1[1] - w2[1]) % p
            d12c = (w1[2] - w2[2]) % p
            d13a = (w1[0] - w3[0]) % p
            d13b = (w1[1] - w3[1]) % p
            d13c = (w1[2] - w3[2]) % p
            qa = (d12b * d13c - d12c * d13b) % p
            qb = (d12c * d13a - d12a * d13c) % p
            qc = (d12a * d13b - d12b * d13a) % p
            if qa:
                iv = INV[qa]
                key = (1, qb * iv % p, qc * iv % p)
            elif qb:
                iv = INV[qb]
                key = (0, 1, qc * iv % p)
            else:
                # Nondegeneracy lemma (note Sec 1, PROVED): the w_i are distinct
                # points of the smooth conic b^2 = ac; a vanishing cross product
                # would put 3 conic points on one projective line. Assert, don't skip.
                assert qc != 0, "concurrency cross product vanished (conic lemma violated)"
                key = (0, 0, 1)
            qmap[key].add(k)
    best = 0
    for cs in qmap.values():
        best = max(best, len(cs))
    return best


def rotation_reps(ell):
    """exponent-triples up to adding a constant mod ell (the scaling gauge D ~ zeta D)."""
    reps = set()
    for tri in itertools.combinations(range(ell), 3):
        best = None
        for t in range(ell):
            s = tuple(sorted((a + t) % ell for a in tri))
            if best is None or s < best:
                best = s
        reps.add(best)
    return sorted(reps)


def gauge_max_k3(p, ell, reps=None, early=None):
    Hs, g = mu_ell_list(p, ell)
    cidx, n = coset_index_map(p, ell, g)
    INV = inv_table(p)
    if reps is None:
        reps = rotation_reps(ell)
    gmax = 0
    for tri in reps:
        drop = [Hs[a] for a in tri]
        b = max_k3_for_drop(p, ell, drop, cidx, n, INV)
        if b > gmax:
            gmax = b
            if early is not None and gmax >= early:
                return gmax, n, True
    return gmax, n, False


# ======================================================================
# The three falsifier witnesses (p, ell, drop-SET, q low-first, claims)
# ======================================================================
# q printed in the note as X^2 + bX + c; low-first qcoef = [c, b, 1].
# (The originating dossier's "169X^2+294X+1" for ell=43 was a reversed-tuple
#  MISLABEL; the true polynomial is X^2 + 294X + 169, i.e. qcoef = [169,294,1].)
# The four PRIMARY witnesses carry the full refutation and get the independent
# pencil cross-check (3 code paths). The ell=53 k3=11 row is the RECORD (excess +6,
# T=10) and equals the exhaustive-gauge max at (53,1061) (--full reproduces the scan);
# the k3=9 row at the same prime was the originating lane's (0,1,k)-family record,
# kept as a second independent witness. The two BAND witnesses (ell=61,67) show the
# excess >= +3 band PERSISTS (every ell in {43,53,59,61,67}); they are checked
# via-Gamma (O(p)), skipping the O(p^2) pencil count to stay in budget.
WITNESSES = [
    dict(ell=43, p=431, D=[1, 4, 16], q=[169, 294, 1], c1=260,
         spec="[40,3^8]", E3=46, T=7, exc=3, k3=8, pencil=True),
    dict(ell=53, p=1061, D=[1, 37, 268], q=[1060, 32, 1], c1=451,
         spec="[50,3^11,2^6]", E3=59, T=10, exc=6, k3=11, pencil=True),
    dict(ell=53, p=1061, D=[1, 308, 998], q=[806, 672, 1], c1=176,
         spec="[50,3^9,2^3]", E3=57, T=8, exc=4, k3=9, pencil=True),
    dict(ell=59, p=709, D=[1, 551, 564], q=[336, 341, 1], c1=650,
         spec="[56,3^9,2]", E3=63, T=8, exc=4, k3=9, pencil=True),
]
BAND_WITNESSES = [
    # ell=61: the R2 EXHAUSTIVE-max witness (k3=9, excess +4) -- upgrades the originally
    # shipped (0,1,k)-family lower bound k3>=8 (excess +3) at the same prime.
    dict(ell=61, p=733, D=[1, 10, 16], q=[515, 258, 1], c1=432,
         spec="[58,3^9,2^2]", E3=65, T=8, exc=4, k3=9, pencil=False),
    dict(ell=67, p=1609, D=[1, 1141, 320], q=[708, 644, 1], c1=45,
         spec="[64,3^9,2^12]", E3=71, T=8, exc=4, k3=9, pencil=False),
    # ell=71, 73: R2 exhaustive maxima at their n=12 primes (4-route witnesses, re-verified here).
    dict(ell=71, p=853, D=[1, 81, 547], q=[164, 761, 1], c1=543,
         spec="[68,3^9,2^2]", E3=75, T=8, exc=4, k3=9, pencil=False),
    dict(ell=73, p=877, D=[1, 567, 766], q=[140, 448, 1], c1=262,
         spec="[70,3^9,2^2]", E3=77, T=8, exc=4, k3=9, pencil=False),
]
# R2 coverage-extension records (note Sec 2): the new ell=23 max (LATE record at its largest
# tested prime -- excess +2, not a falsifier, but it moves the Sec 3 table row) and the
# recurrence of the ell=43 max at n=40.
R2_RECORDS = [
    dict(ell=23, p=1657, D=[1, 16, 913], q=[650, 0, 1], c1=1306,
         spec="[20,3^7]", E3=25, T=6, exc=2, k3=7, pencil=True),
    dict(ell=43, p=1721, D=[1, 32, 1462], q=[925, 75, 1], c1=730,
         spec="[40,3^8,2^4]", E3=46, T=7, exc=3, k3=8, pencil=False),
]


def check_witness(w, spec_override=None, k3_check_override=None):
    """Rebuild one witness; return (ok, detail, computed-dict)."""
    p, ell, D, q = w["p"], w["ell"], w["D"], w["q"]
    assert is_prime(p) and (p - 1) % ell == 0
    Hs, g = mu_ell_list(p, ell)
    for d in D:
        if pow(d, ell, p) != 1:
            return False, "drop %d not an ell-th root of unity" % d, {}
    Gamma, A, qq, c1 = build_gamma_fat(p, ell, D, q)
    mus = spectrum(Gamma, p, ell, g)
    E3, T, exc = E3_T_excess(mus, ell)
    k3, mu1 = count_k3(Gamma, p, ell, g)
    spec = spectrum_compact(mus)
    spec_exp = spec_override if spec_override is not None else w["spec"]
    k3_exp = k3_check_override if k3_check_override is not None else w["k3"]
    cf = (Gamma[0] == 0)
    deg = len(Gamma) - 1
    c1_ok = (c1 == w["c1"])
    ok = (spec == spec_exp and E3 == w["E3"] and T == w["T"] and exc == w["exc"]
          and k3 == k3_exp and cf and deg == ell - 1 and mu1 == ell - 3 and c1_ok)
    pdet = ""
    if w.get("pencil", False):
        kp = count_coset_aligned_pencil(p, ell, D, q, g)
        ok = ok and (kp == k3_exp)
        pdet = " pencil=%d" % kp
    detail = ("ell=%d p=%d n=%d D=%s: spec=%s E_3=%d(=ell%+d) T=%d excess=%+d "
              "k3=%d%s mu1=%d(ell-3) c1=%d(%s) constfree=%s deg=%d"
              % (ell, p, (p - 1) // ell, D, spec, E3, exc, T, exc, k3, pdet, mu1,
                 c1, "ok" if c1_ok else "BAD", cf, deg))
    return ok, detail, dict(spec=spec, E3=E3, T=T, exc=exc, k3=k3, c1=c1)


# ======================================================================
# Gates
# ======================================================================


def gate1_witnesses():
    allok = True
    lines = []
    for w in WITNESSES:
        ok, detail, comp = check_witness(w)
        allok = allok and ok
        lines.append(("OK  " if ok else "BAD ") + detail)
    lines.append("-- excess >= +3 band persists (ell in {43,53,59,61,67,71,73}):")
    for w in BAND_WITNESSES:
        ok, detail, comp = check_witness(w)
        allok = allok and ok
        lines.append(("OK  " if ok else "BAD ") + detail)
    lines.append("-- R2 coverage-extension records (ell=23 late record; ell=43 recurrence):")
    for w in R2_RECORDS:
        ok, detail, comp = check_witness(w)
        allok = allok and ok
        lines.append(("OK  " if ok else "BAD ") + detail)
    # explicit [40,3^8] head for ell=43 (the C'<=2 / T1 falsifier)
    head_ok = (check_witness(WITNESSES[0])[2]["spec"] == "[40,3^8]")
    allok = allok and head_ok
    return allok, ("4 primary + 4 band + 2 R2-record witnesses rebuilt; [40,3^8] head=%s\n    %s"
                   % (head_ok, "\n    ".join(lines)))


def gate2_ell19_pin():
    """Exhaustive-up-to-gauge max k3 at ell=19: ALL eligible primes n in [2,30]
    (self-verifies p=191 is the smallest) + three beyond-window primes."""
    reps = rotation_reps(19)
    rows = []
    overall = 0
    at_smallest = None
    for nn in range(2, 31):
        p = nn * 19 + 1
        if not is_prime(p):
            continue
        gmax, n, _ = gauge_max_k3(p, 19, reps)
        rows.append((p, n, gmax))
        overall = max(overall, gmax)
        if at_smallest is None:
            at_smallest = (p, n, gmax)
    # pin: exactly five eligible primes in the window, the smallest being 191; overall
    # exhaustive-gauge max is 6, attained ONLY at p=571 (n=30, the window boundary);
    # => fat-tail excess = max_k3 - 5 <= +1 at ell=19 => H_19 untouched.
    window_ok = (len(rows) == 5 and overall == 6 and at_smallest == (191, 10, 5)
                 and (571, 30, 6) in rows
                 and sum(1 for (_, _, m) in rows if m == 6) == 1
                 and overall - 5 <= 1)
    # beyond-window: 647 (n=34), 761 (n=40), 1103 (n=58) all give 5
    beyond = []
    for p in (647, 761, 1103):
        gmax, n, _ = gauge_max_k3(p, 19, reps)
        beyond.append((p, n, gmax))
    beyond_ok = all(m == 5 for (_, _, m) in beyond)
    ok = window_ok and beyond_ok
    tab = " ".join("p%d(n%d):%d" % r for r in rows)
    btab = " ".join("p%d(n%d):%d" % r for r in beyond)
    return ok, ("ell=19 exhaustive-gauge max k3 = %d over the %d eligible primes n<=30 "
                "(excess <= %+d, H_19 UNTOUCHED); smallest p=191(n=10):%d; 6 attained ONLY at "
                "p=571(n=30, boundary) | window: %s | beyond-window: %s"
                % (overall, len(rows), overall - 5, at_smallest[2], tab, btab))


def gate3_growth_and_corrections():
    """small-ell plateau (the mirage), the (17,409) correction, and ell=43 reaching k3=8."""
    lines = []
    ok = True
    # small-ell exhaustive-up-to-gauge max at a prime attaining the max: the whole
    # ell<=31 range (the original program's search window) caps at <=7 -- the mirage.
    # (11->4, 13->4, 17->7[n=8], 23->5, 29->7[n=8], 31->7)
    small = [(11, 67, 4), (13, 313, 4), (17, 137, 7), (23, 139, 5), (29, 233, 7), (31, 311, 7)]
    for ell, p, exp in small:
        reps = rotation_reps(ell)
        gmax, n, _ = gauge_max_k3(p, ell, reps)
        good = (gmax == exp)
        ok = ok and good
        lines.append("%sell=%d p=%d n=%d max_k3=%d(exp%d)"
                     % ("OK  " if good else "BAD ", ell, p, n, gmax, exp))
    # (17,409) correction: exhaustive-gauge max k3 = 5 (PR #368 reported 3, 1-of-680 undercount)
    gmax409, n409, _ = gauge_max_k3(409, 17, rotation_reps(17))
    c409 = (gmax409 == 5)
    ok = ok and c409
    lines.append("%s(17,409) exhaustive max_k3=%d (exp 5; corrects PR #368's reported 3)"
                 % ("OK  " if c409 else "BAD ", gmax409))
    # ell=43 gauge scan REACHES k3=8 (early-exit)
    g43, n43, hit43 = gauge_max_k3(431, 43, rotation_reps(43), early=8)
    c43 = (hit43 and g43 == 8)
    ok = ok and c43
    lines.append("%sell=43 p=431 gauge scan reaches k3=%d (>=8 falsifier=%s)"
                 % ("OK  " if c43 else "BAD ", g43, hit43))
    return ok, "growth table + corrections:\n    " + "\n    ".join(lines)


# ---------- R2 artifact (note Sec 3/3A; shipped in-repo) ----------
R2_JSON_RELPATH = ("..", "data", "certificates", "l1-e3-law", "l1_k3_growth_r2_scan.json")


def load_r2_artifact():
    import json
    import os
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), *R2_JSON_RELPATH)
    with open(path) as f:
        return json.load(f)


def check_r2_stats(data):
    """Validate the R2 artifact's headline invariants; returns (ok, msg)."""
    e19 = [r for r in data["rows"] if r["ell"] == 19]
    dist = Counter(r["k3"] for r in e19)
    sixes = [(r["p"], r["n"]) for r in e19 if r["k3"] == 6]
    checks = [
        ("80 ell=19 rows", len(e19) == 80),
        ("all k3 <= 6", all(r["k3"] <= 6 for r in e19)),
        ("6 uniquely at (571, n=30)", sixes == [(571, 30)]),
        ("distribution 3:42/4:15/5:22/6:1",
         dict(dist) == {3: 42, 4: 15, 5: 22, 6: 1}),
        ("deepest prime 13567", max(r["p"] for r in e19) == 13567),
        ("ell=23 grid max 7 at n=72 only",
         [(r["n"], r["k3"]) for r in data["by_ell"]["23"] if r["k3"] >= 6] == [(72, 7)]),
        ("ell=53 grid sequence 1,7,11,7,8,7",
         [r["k3"] for r in data["by_ell"]["53"]] == [1, 7, 11, 7, 8, 7]),
        ("9 four-route witnesses present", len(data["witnesses"]) == 9
         and all(w.get("all_routes_agree") for w in data["witnesses"])),
    ]
    ok = all(c for _, c in checks)
    msg = "; ".join("%s=%s" % (n, "ok" if c else "BAD") for n, c in checks)
    return ok, msg


def gate5_r2_artifact():
    """R2 artifact consistency (note Sec 3 coverage column / Sec 3A; the ell=19 deep null)."""
    try:
        data = load_r2_artifact()
    except Exception as e:
        return False, "artifact missing/unreadable: %r" % (e,)
    ok, msg = check_r2_stats(data)
    return ok, "R2 artifact (l1_k3_growth_r2_scan.json): " + msg


def gate4_tamper():
    """>=5 tamper self-tests: each MUST be rejected (i.e. produce a mismatch)."""
    results = []
    # (a) mutate a q-coefficient of the ell=43 witness -> spectrum/k3 must change (rejected)
    w = dict(WITNESSES[0])
    w["q"] = [w["q"][0], (w["q"][1] + 1) % w["p"], w["q"][2]]  # b -> b+1
    ok_a, _, _ = check_witness(w)
    results.append(("mutated q-coeff (b+1) at ell=43 rejected", not ok_a))
    # (b) wrong claimed spectrum head for ell=43 -> rejected
    ok_b, _, _ = check_witness(WITNESSES[0], spec_override="[40,3^7]")
    results.append(("wrong spectrum head [40,3^7] rejected", not ok_b))
    # (c) claim k3=7 at ell=43 (the dead plateau value) -> rejected (true k3=8)
    ok_c, _, _ = check_witness(WITNESSES[0], k3_check_override=7)
    results.append(("claim k3=7 at ell=43 rejected (true k3=8)", not ok_c))
    # (d) mutate q on the ell=53 k3=11 RECORD witness -> rejected
    #     (pencil off: the spectrum/k3/c1 mismatch is the teeth; keeps budget)
    w11 = dict(WITNESSES[1])
    assert w11["k3"] == 11
    w11["q"] = [w11["q"][0], (w11["q"][1] + 1) % w11["p"], w11["q"][2]]  # 32 -> 33
    w11["pencil"] = False
    ok_d, _, _ = check_witness(w11)
    results.append(("mutated q (b:32->33) on the ell=53 k3=11 record rejected", not ok_d))
    # (e) tamper the R2 deep-sweep artifact stats -> check_r2_stats must reject:
    #     flip one ell=19 row's k3 from 3 to 7 (breaks all-<=6, uniqueness AND distribution)
    try:
        data = load_r2_artifact()
        import copy
        bad = copy.deepcopy(data)
        for r in bad["rows"]:
            if r["ell"] == 19 and r["k3"] == 3:
                r["k3"] = 7
                break
        ok_e, _ = check_r2_stats(bad)
        results.append(("tampered R2 ell=19 stats (a 3 -> 7) rejected", not ok_e))
    except Exception:
        results.append(("tampered R2 ell=19 stats (artifact unreadable)", False))
    allok = all(caught for _, caught in results)
    return allok, "tamper self-tests: " + "; ".join(
        "%s=%s" % (name, "CAUGHT" if caught else "MISSED") for name, caught in results)


# --full: reproduce the note's Sec 3 coverage table live (full scans, NO early exit).
# Expected values established at packaging time by this same transversal (2026-07-07);
# (53,1061)=11 is the row the originating lane's early-exit-at->=8 scanner truncated to 9.
FULL_TABLE = {
    11: [(23, 1), (67, 4), (89, 3), (199, 4), (331, 4)],
    13: [(53, 3), (79, 3), (131, 3), (157, 3), (313, 4)],
    17: [(103, 4), (137, 7), (239, 5), (307, 5), (409, 5)],
    # six deterministic ell=19 deep-sweep spot rows (the full 80-prime sweep is the R2
    # artifact, gate 5; two of these -- 1901 and 13567 -- were also replayed at build time)
    19: [(1787, 4), (1901, 5), (2053, 3), (4409, 3), (8209, 4), (13567, 3)],
    23: [(47, 1), (139, 5), (277, 5), (461, 5), (599, 5), (1657, 7)],
    29: [(59, 1), (233, 7), (349, 5), (523, 5)],
    31: [(311, 7), (373, 7), (683, 7)],
    37: [(149, 3), (223, 5), (593, 7)],
    41: [(739, 7)],
    43: [(431, 8), (1721, 8)],
    47: [(283, 5), (659, 7)],
    53: [(743, 7), (1061, 11)],
    59: [(709, 9)],
}


def gate_full():
    """Opt-in: full exhaustive-up-to-gauge replay of the entire Sec 3 table (~20-25 min)."""
    import time
    allok = True
    lines = []
    for ell in sorted(FULL_TABLE):
        reps = rotation_reps(ell)
        for (p, exp) in FULL_TABLE[ell]:
            t0 = time.time()
            gmax, n, _ = gauge_max_k3(p, ell, reps)   # NO early exit
            good = (gmax == exp)
            allok = allok and good
            lines.append("%s(%d,%d) n=%d max=%d exp=%d [%.0fs]"
                         % ("OK  " if good else "BAD ", ell, p, n, gmax, exp, time.time() - t0))
            print("    " + lines[-1], flush=True)
    return allok, "full coverage-table replay: %d rows" % sum(len(v) for v in FULL_TABLE.values())


GATES = [
    ("(1) witnesses (4 primary + 4 band + 2 R2)     ", gate1_witnesses),
    ("(2) ell=19 pin survives (excess <= +1)        ", gate2_ell19_pin),
    ("(3) growth table + (17,409) fix + ell=43 k3=8 ", gate3_growth_and_corrections),
    ("(4) tamper self-tests (>=5, must be caught)   ", gate4_tamper),
    ("(5) R2 artifact: ell=19 deep null + grids     ", gate5_r2_artifact),
]


def main(argv):
    allok = True
    for name, fn in GATES:
        ok, msg = fn()
        allok = allok and ok
        print("[%s] %s  %s" % ("PASS" if ok else "FAIL", name, msg))
    if "--full" in argv:
        print("[....] (--full) replaying the ENTIRE Sec 3 coverage table (~20-25 min)")
        ok, msg = gate_full()
        allok = allok and ok
        print("[%s] (--full) %s" % ("PASS" if ok else "FAIL", msg))
    print("ALL PASS" if allok else "SOME FAILED")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
