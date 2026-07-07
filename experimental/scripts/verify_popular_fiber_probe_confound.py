#!/usr/bin/env python3
"""verify_popular_fiber_probe_confound.py

Zero-arg, stdlib-only, deterministic verifier for the companion note
experimental/notes/thresholds/cap25_v13_popular_fiber_probe_confound.md
(target label: prob:entropy-inverse-q).

This packet is the first instantiation of rem:entropy-inverse-skeleton step 1 (the
dyadic popular-fiber hierarchy) together with the PROVED headline lemma of the note --
THE PROBE CONFOUND -- on five toy rows, exact Fraction/int arithmetic throughout
(floats appear only in the final human-readable log lines, never in a gate decision).

Manuscript objects (experimental/grande_finale.tex, base commit 53bb5df):
  Phi_w / Fib_w(z)        depth-w prefix and its fiber (def. l.549, prop:newton l.551)
  Gamma_r                 |B|^{w(r-1)} sum_z mu(z)^r          (prop:moment-sandwich l.705)
  R_eff(r):=Gamma_r^{1/(r-1)} -> R    monotone certificate    (Brick 2, PR #384)
  s(z)=gcd(n,{j:z_j!=0})  twist stabilizer                    (prop:q-orbit-moment l.923)
  power-map image coset   x->x^e is c=gcd(e,N)-to-1 onto S_e   (prop:composite-descend l.969)
  s(L)=gcd(n,e,{j:lam_j!=0})   coefficient scale              (def:coefficient-scale l.1100)

THE PROBE CONFOUND (note Lemma, PROVED here by direct enumeration): for a probe order j
on D=alpha*mu_n, put c=gcd(j,n); then x->x^j has image alpha^j*mu_{n/c} of size exactly
n/c, each value hit exactly c times, so the probe coordinate p_j(S)=sum_{x in S} x^j
factors through the order-(n/c) quotient coset and is a quotient-scale observable when
c>1 -- intrinsically low-rank/AP-prone. Consequence: step-4 instrumentation must use
coprime probe orders gcd(j,n)=1.

This verifier is an INDEPENDENT reimplementation: it imports no lane/campaign module and
reads no campaign JSON. Every pinned integer/fraction is recomputed from the field data.

Five gates; exit 0 iff ALL pass, nonzero on ANY failure.

  gate 1  IMAGE-COLLAPSE LEMMA (part a). For all 5 rows and probe orders j=w+1,w+2,
          recompute the multiset {x^j : x in D} and assert image size = n/gcd(j,n) with
          every fiber of size exactly gcd(j,n). Pinned per (row,j).
  gate 2  DYADIC HIERARCHY + EXACT GAMMA_r + R_eff (rows A, B, C, D from scratch).
          Recomputes the whole prefix histogram, the dyadic level counts/masses, num
          observed/zero prefixes, max fiber, R_max, and Gamma_2/3/4 as exact Fractions;
          diffs against pins. Also verifies Brick-2 monotonicity R_eff(2)<=R_eff(3)<=
          R_eff(4)<=R exactly (root-cleared: Gamma_2^2<=Gamma_3, Gamma_3^3<=Gamma_4^2,
          Gamma_4<=R^3), i.e. the Sec 4 AUDIT (row E's Brick-2 check is in gate 4).
  gate 3  THE CONFOUND, MEASURED. Recomputes the primitive-trade exact-AP scan
          (|P+P| = 2|P|-1, the Vosper/Cauchy-Davenport equality = "contained in an AP")
          over every fiber of size >= minN, split by gcd(j,n). Asserts the aggregate
          0/152 at coprime coords vs 24/132 at gcd>1 coords, with row A's j=4 at 9/19.
  gate 4  ROW E QUOTIENT-FIBER IDENTITY C(6,2)=15 (full enumeration, ~4s). The dominant
          fiber is the null prefix (0,0,0), size 15, and equals EXACTLY the 15 unions of
          two of the six mu_4-cosets of D; every member is mu_4-invariant (quotient scale
          4); mu_4 sums to 0. Also pins row E's dyadic top level and Gamma_2/3/4.
  gate 5  TWIST STABILIZER + ANTIPODAL MECHANISM (the note's last-eyes finding). Verifies
          s(z)=gcd(n,A(z)) and orbit size n/s(z) on pure directions; and at row E fiber
          z=(0,42,0) (s(z)=2): exactly 5 of 7 members are antipodal (M=-M). The theorem
          is one-directional -- antipodal => every odd power sum vanishes (in particular
          p5(M)=0), since an antipodal support is a union of mu_2-pairs {x,-x}. The
          converse is NOT general (p5=0 is one linear condition); on THESE 7 measured
          members the biconditional antipodal <=> p5(M)=0 happens to hold, checked
          member-by-member (empirical). This explains why a COPRIME probe can still collapse.

Non-claims (mirrors the note): toy scale only; no claim on prob:entropy-inverse-q, on any
deployed row, or on skeleton steps 5-6.

Usage:
  python3 verify_popular_fiber_probe_confound.py            # all gates, exit 0 on pass
  python3 verify_popular_fiber_probe_confound.py --tamper   # self-test: each pin, when
                                                            #   corrupted, must fail a gate
"""
import itertools
import sys
from collections import Counter
from fractions import Fraction
from math import comb, gcd


# ---------------------------------------------------------------------------
# field / subgroup plumbing (independent reimplementation)
# ---------------------------------------------------------------------------
def primitive_root(p):
    phi = p - 1
    facs, x, d = [], p - 1, 2
    while d * d <= x:
        if x % d == 0:
            facs.append(d)
            while x % d == 0:
                x //= d
        d += 1
    if x > 1:
        facs.append(x)
    for g in range(2, p):
        if all(pow(g, phi // q, p) != 1 for q in facs):
            return g
    raise RuntimeError("no primitive root")


def subgroup_of_order(p, n):
    assert (p - 1) % n == 0, f"n={n} must divide p-1={p-1}"
    h = pow(primitive_root(p), (p - 1) // n, p)
    D, cur = [], 1
    for _ in range(n):
        D.append(cur)
        cur = cur * h % p
    assert len(set(D)) == n
    return sorted(D)


def power_table(D, p, kmax):
    return [tuple(pow(x, j, p) for j in range(1, kmax + 1)) for x in D]


# Enumeration caches: the field data is deterministic, so the (expensive) row-E
# full enumeration C(24,8)=735471 is computed once and reused across gates AND
# across every --tamper re-run. Keeps both modes well under the 90s budget.
_COUNTS_CACHE = {}
_MEMBERS_CACHE = {}


def count_fibers(D, p, m, w, xp):
    ck = (p, len(D), m, w)
    if ck in _COUNTS_CACHE:
        return _COUNTS_CACHE[ck]
    counts = Counter()
    for combo in itertools.combinations(range(len(D)), m):
        ps = [0] * w
        for idx in combo:
            row = xp[idx]
            for j in range(w):
                ps[j] += row[j]
        counts[tuple(v % p for v in ps)] += 1
    _COUNTS_CACHE[ck] = counts
    return counts


def members_of(D, p, m, w, target_keys, xp):
    ck = (p, len(D), m, w, frozenset(target_keys))
    if ck in _MEMBERS_CACHE:
        return _MEMBERS_CACHE[ck]
    out = {k: [] for k in target_keys}
    for combo in itertools.combinations(range(len(D)), m):
        ps = [0] * w
        for idx in combo:
            row = xp[idx]
            for j in range(w):
                ps[j] += row[j]
        key = tuple(v % p for v in ps)
        if key in out:
            out[key].append(combo)
    _MEMBERS_CACHE[ck] = out
    return out


def poly_from_roots(roots, p):
    c = [1]
    for x in roots:
        nc = [0] * (len(c) + 1)
        for i, ci in enumerate(c):
            nc[i] = (nc[i] + ci * (-x)) % p
            nc[i + 1] = (nc[i + 1] + ci) % p
        c = nc
    return c


def scale_of_locator(coeffs, n_row):
    """def:coefficient-scale s(L)=gcd(n,e,{j:lambda_j!=0}); coeffs[i]=coeff of X^i."""
    e = len(coeffs) - 1
    g = e
    for i in range(e):
        if coeffs[i] != 0:
            g = gcd(g, i)
            if g == 1:
                break
    return gcd(g, n_row)


def scale_pair(rootsA, rootsB, n_row, p):
    return gcd(scale_of_locator(poly_from_roots(rootsA, p), n_row),
               scale_of_locator(poly_from_roots(rootsB, p), n_row))


def power_sum_vec(vals, kmax, p):
    return tuple(sum(pow(x, j, p) for x in vals) % p for j in range(1, kmax + 1))


def is_ap_mod_p(vals, p):
    """Vosper/Cauchy-Davenport equality test on the DISTINCT residues P=set(vals):
    |P+P| = 2|P|-1 (the AP/coset-progression floor). Integer-exact, no float."""
    P = sorted(set(v % p for v in vals))
    k = len(P)
    if k < 4:
        return None                      # need a size->=4 support for a nontrivial test
    S = {(a + b) % p for a in P for b in P}
    cd_min = min(p, 2 * k - 1)
    return len(S) == cd_min


# ---------------------------------------------------------------------------
# rows
# ---------------------------------------------------------------------------
ROWS = [
    dict(label="A", p=97,  n=16, m=6, w=2, minN=5),
    dict(label="B", p=97,  n=16, m=7, w=2, minN=5),
    dict(label="C", p=113, n=16, m=6, w=2, minN=5),
    dict(label="D", p=31,  n=10, m=5, w=2, minN=5),
    dict(label="E", p=193, n=24, m=8, w=3, minN=6),
]

# ---------------------------------------------------------------------------
# PINS -- every load-bearing constant, recomputed and diffed below.
# (mutated one-at-a-time under --tamper; each must break a gate.)
# ---------------------------------------------------------------------------
PINS = dict(
    # gate 1: (label, j) -> (c=gcd(j,n), image_size=n/c, fiber_mult=c)
    image={
        ("A", 3): (1, 16, 1), ("A", 4): (4, 4, 4),
        ("B", 3): (1, 16, 1), ("B", 4): (4, 4, 4),
        ("C", 3): (1, 16, 1), ("C", 4): (4, 4, 4),
        ("D", 3): (1, 10, 1), ("D", 4): (2, 5, 2),
        ("E", 4): (4, 6, 4),  ("E", 5): (1, 24, 1),
    },
    # gate 2: exact structure of rows A, B, C, D (every row in the Sec 1 tables
    # except E, which gate 4 recomputes in full)
    rowA=dict(
        Cnm=8008, Bw=9409, gcd_mn=2, observed=4728, zero=4681, maxfib=5,
        Rmax=Fraction(47045, 8008),
        gamma={2: Fraction(20445757, 8016008),
               3: Fraction(74276066759, 9170313152),
               4: Fraction(15564081912098365, 514051074048512)},
        # dyadic level -> (count_z, mass)
        dyadic={0: (2504, 2504), 1: (1968, 4432), 2: (256, 1072)},
        below=(0, 0),
    ),
    rowB=dict(
        Cnm=11440, Bw=9409, gcd_mn=1, observed=5880, zero=3529, maxfib=6,
        Rmax=Fraction(28227, 5720),
        gamma={2: Fraction(17867691, 8179600),
               3: Fraction(563665932127, 93574624000),
               4: Fraction(1876685927105037, 97317608960000)},
        dyadic={0: (1312, 2624), 1: (1400, 4640), 2: (240, 1248)},
        below=(2928, 2928),
    ),
    rowC=dict(
        Cnm=8008, Bw=12769, gcd_mn=2, observed=5928, zero=6841, maxfib=5,
        Rmax=Fraction(63845, 8008),
        gamma={2: Fraction(20698549, 8016008),
               3: Fraction(527132118113, 64192192064),
               4: Fraction(1496923310125871, 46731915822592)},
        dyadic={0: (4168, 4168), 1: (1504, 3008), 2: (256, 832)},
        below=(0, 0),
    ),
    rowD=dict(
        Cnm=252, Bw=961, gcd_mn=5, observed=231, zero=730, maxfib=2,
        Rmax=Fraction(961, 126),
        gamma={2: Fraction(961, 216),
               3: Fraction(923521, 42336),
               4: Fraction(11537547853, 96018048)},
        dyadic={1: (210, 210), 2: (21, 42)},
        below=(0, 0),
    ),
    # gate 3: exact-AP scan, per (label, j) -> (hits, tests); coprime totals must be 0.
    scan={
        ("A", 3): (0, 24), ("A", 4): (9, 19),
        ("B", 3): (0, 128), ("B", 4): (15, 105),
        ("C", 4): (0, 4),
        ("E", 4): (0, 4),
    },
    scan_totals=dict(coprime_hits=0, coprime_tests=152, quot_hits=24, quot_tests=132),
    # gate 4: row E dominant fiber
    rowE=dict(
        Cnm=735471, Bw=7189057, gcd_mn=8, observed=671853, maxfib=15,
        null_key=(0, 0, 0), null_size=15, choose=comb(6, 2),   # = 15
        n_mu4_cosets=6, mu4_size=4, mu4_sum=0,
        gamma={2: Fraction(236512786243, 20033984883),
               3: Fraction(22179510594169659101, 132609734062964037),
               4: Fraction(101867143731616647125106617, 32510204573674074418809)},
        # dyadic top level k=7 = the single dominant fiber
        dyadic_top=dict(level=7, count_z=1, mass=15),
    ),
    # gate 5: twist stabilizer on pure directions -> (s(z), orbit=n/s)
    # pure direction supported at coordinate j with value != 0, in row of length n.
    twist={
        ("A", (1,)): (1, 16), ("A", (2,)): (2, 8),
        ("E", (1,)): (1, 24), ("E", (2,)): (2, 12), ("E", (3,)): (3, 8), ("E", (4,)): (4, 6),
    },
    # row E antipodal mechanism at fiber z=(0,42,0)
    antipodal=dict(z=(0, 42, 0), N=7, s_z=2, n_antipodal=5, n_p5_zero=5),
)


class GateFail(Exception):
    pass


def _eq(name, got, want):
    if got != want:
        raise GateFail(f"{name}: got {got!r}, expected {want!r}")


# ---------------------------------------------------------------------------
# gates
# ---------------------------------------------------------------------------
def gate1_image(pins):
    """part (a) of the PROBE CONFOUND lemma at every deployed probe order."""
    print("gate 1  IMAGE-COLLAPSE LEMMA  x^j on D = alpha*mu_n is gcd(j,n)-to-1 onto mu_{n/c}")
    for row in ROWS:
        p, n, w = row["p"], row["n"], row["w"]
        D = subgroup_of_order(p, n)
        for j in (w + 1, w + 2):
            c = gcd(j, n)
            img = Counter(pow(x, j, p) for x in D)
            got = (c, len(img), sorted(set(img.values())))
            want_c, want_size, want_mult = pins["image"][(row["label"], j)]
            _eq(f"image[{row['label']},j={j}]",
                got, (want_c, want_size, [want_mult]))
            tag = "coprime" if c == 1 else "QUOTIENT"
            print(f"        {row['label']}: j={j} c=gcd({j},{n})={c:>2} -> image {len(img):>2}"
                  f" = n/c, each hit {want_mult}x  [{tag}]")
    print("        PASS\n")


def _analyze_small(row):
    p, n, m, w = row["p"], row["n"], row["m"], row["w"]
    D = subgroup_of_order(p, n)
    Cnm, Bw = comb(n, m), p ** w
    counts = count_fibers(D, p, m, w, power_table(D, p, w))
    assert sum(counts.values()) == Cnm
    gamma = {r: Fraction(Bw ** (r - 1) * sum(c ** r for c in counts.values()), Cnm ** r)
             for r in (2, 3, 4)}
    maxN = max(counts.values())
    # dyadic: level k iff 2^k <= N*Bw/Cnm < 2^{k+1}; below-average bucket collects N*Bw<Cnm
    lvl_c, lvl_m = Counter(), Counter()
    below_c = below_m = 0
    for N in counts.values():
        num = N * Bw
        if num >= Cnm:
            k = 0
            while (1 << (k + 1)) * Cnm <= num:
                k += 1
            lvl_c[k] += 1
            lvl_m[k] += N
        else:
            below_c += 1
            below_m += N
    return dict(Cnm=Cnm, Bw=Bw, gcd_mn=gcd(m, n), observed=len(counts),
                zero=Bw - len(counts), maxfib=maxN, Rmax=Fraction(Bw * maxN, Cnm),
                gamma=gamma, lvl_c=lvl_c, lvl_m=lvl_m, below=(below_c, below_m))


def _reff_monotone(gamma, Rmax):
    """Brick-2 (PR #384) certificate, EXACT (no float in the decision): with
    R_eff(r)=Gamma_r^{1/(r-1)}, verify R_eff(2)<=R_eff(3)<=R_eff(4)<=R by
    clearing the fractional roots -- Gamma_2^2<=Gamma_3, Gamma_3^3<=Gamma_4^2,
    Gamma_4<=R^3 (all quantities positive)."""
    return (gamma[2] ** 2 <= gamma[3]
            and gamma[3] ** 3 <= gamma[4] ** 2
            and gamma[4] <= Rmax ** 3)


def gate2_dyadic_gamma(pins):
    print("gate 2  DYADIC HIERARCHY + EXACT Gamma_r + R_eff MONOTONICITY "
          "(rows A, B, C, D, from scratch)")
    for lbl, pinkey in (("A", "rowA"), ("B", "rowB"), ("C", "rowC"), ("D", "rowD")):
        row = next(r for r in ROWS if r["label"] == lbl)
        a = _analyze_small(row)
        pn = pins[pinkey]
        for f in ("Cnm", "Bw", "gcd_mn", "observed", "zero", "maxfib", "Rmax"):
            _eq(f"row{lbl}.{f}", a[f], pn[f])
        for r in (2, 3, 4):
            _eq(f"row{lbl}.Gamma_{r}", a["gamma"][r], pn["gamma"][r])
        for k, (cz, ms) in pn["dyadic"].items():
            _eq(f"row{lbl}.dyadic[{k}].count", a["lvl_c"][k], cz)
            _eq(f"row{lbl}.dyadic[{k}].mass", a["lvl_m"][k], ms)
        _eq(f"row{lbl}.below", a["below"], pn["below"])
        # dyadic masses + below must reconstruct C(n,m) exactly
        _eq(f"row{lbl}.mass_total", sum(a["lvl_m"].values()) + a["below"][1], pn["Cnm"])
        # Brick-2 (Sec 4 AUDIT), recomputed exactly from this row's Gamma_r
        if not _reff_monotone(a["gamma"], a["Rmax"]):
            raise GateFail(f"row{lbl}: R_eff(r)=Gamma_r^(1/(r-1)) not monotone <= R")
        print(f"        row {lbl}: C(n,m)={a['Cnm']} |B|^w={a['Bw']} gcd(m,n)={a['gcd_mn']} "
              f"maxfib={a['maxfib']} R_max={a['Rmax']}  R_eff mono<=R: ok")
        print(f"                Gamma_2={a['gamma'][2]}")
        print(f"                Gamma_3={a['gamma'][3]}")
        print(f"                Gamma_4={a['gamma'][4]}")
    print("        PASS\n")


def _scan_row(row):
    """Primitive-trade exact-AP scan on every fiber of size>=minN; returns
    per-probe-order (hits, tests) keyed by j."""
    p, n, m, w, minN = row["p"], row["n"], row["m"], row["w"], row["minN"]
    D = subgroup_of_order(p, n)
    xp = power_table(D, p, w)
    counts = count_fibers(D, p, m, w, xp)
    tgt = {z for z, N in counts.items() if N >= minN}
    mem = members_of(D, p, m, w, tgt, xp)
    per = {}
    for z in tgt:
        vs = [tuple(D[i] for i in c) for c in mem[z]]
        M0 = min(vs)
        prim = []
        for M in vs:
            if M == M0:
                continue
            S = tuple(sorted(set(M0) - set(M)))
            T = tuple(sorted(set(M) - set(M0)))
            if scale_pair(S, T, n, p) != 1:            # primitive trades only
                continue
            vs_ = power_sum_vec(S, w + 2, p)
            vt_ = power_sum_vec(T, w + 2, p)
            prim.append(tuple((a - b) % p for a, b in zip(vs_, vt_)))
        if len(prim) < 4:
            continue
        for cidx, j in ((w, w + 1), (w + 1, w + 2)):
            ap = is_ap_mod_p([t[cidx] for t in prim], p)
            if ap is None:
                continue
            d = per.setdefault(j, [0, 0])
            d[0] += int(ap)
            d[1] += 1
    return per


def gate3_confound(pins):
    print("gate 3  THE CONFOUND, MEASURED  (exact-AP = |P+P|=2|P|-1 on primitive trades)")
    cop_h = cop_t = q_h = q_t = 0
    for row in ROWS:
        per = _scan_row(row)
        for j, (h, t) in sorted(per.items()):
            c = gcd(j, row["n"])
            if (row["label"], j) in pins["scan"]:
                _eq(f"scan[{row['label']},j={j}]", (h, t), pins["scan"][(row["label"], j)])
            if c == 1:
                cop_h += h
                cop_t += t
            else:
                q_h += h
                q_t += t
            tag = "coprime" if c == 1 else "QUOT"
            print(f"        {row['label']}: j={j} gcd={c} [{tag:>7}]  {h}/{t} exact-AP")
    tot = pins["scan_totals"]
    _eq("coprime_hits", cop_h, tot["coprime_hits"])
    _eq("coprime_tests", cop_t, tot["coprime_tests"])
    _eq("quot_hits", q_h, tot["quot_hits"])
    _eq("quot_tests", q_t, tot["quot_tests"])
    print(f"        TOTALS  coprime(gcd=1): {cop_h}/{cop_t}   gcd>1: {q_h}/{q_t}")
    print("        => AP/coset structure is entirely confined to gcd>1 probe coords.")
    print("        PASS\n")


def gate4_rowE_quotient(pins):
    print("gate 4  ROW E QUOTIENT-FIBER IDENTITY  null fiber = C(6,2)=15 mu_4-coset unions")
    pn = pins["rowE"]
    p, n, m, w = 193, 24, 8, 3
    D = subgroup_of_order(p, n)
    xp = power_table(D, p, w)
    counts = count_fibers(D, p, m, w, xp)
    maxfib = max(counts.values())
    _eq("rowE.Cnm", sum(counts.values()), pn["Cnm"])
    _eq("rowE.Bw", p ** w, pn["Bw"])
    _eq("rowE.gcd_mn", gcd(m, n), pn["gcd_mn"])
    _eq("rowE.observed", len(counts), pn["observed"])
    _eq("rowE.maxfib", maxfib, pn["maxfib"])
    _eq("rowE.null_size", counts[pn["null_key"]], pn["null_size"])
    # the dominant fiber is unique and is the null prefix
    _eq("rowE.dominant_is_null",
        [z for z, N in counts.items() if N == maxfib], [pn["null_key"]])
    # exact Gamma_2/3/4 from the same histogram
    gE = {}
    for r in (2, 3, 4):
        g = Fraction((p ** w) ** (r - 1) * sum(c ** r for c in counts.values()), pn["Cnm"] ** r)
        _eq(f"rowE.Gamma_{r}", g, pn["gamma"][r])
        gE[r] = g
    # Brick-2 (Sec 4 AUDIT) for row E, exact from its Gamma_r and R=R_max
    if not _reff_monotone(gE, Fraction(pn["Bw"] * maxfib, pn["Cnm"])):
        raise GateFail("rowE: R_eff(r) not monotone <= R")
    # dyadic top level: exactly one fiber, ratio in [128,256), mass 15
    Cnm, Bw = pn["Cnm"], pn["Bw"]
    topk = pn["dyadic_top"]["level"]
    top_fibers = [N for N in counts.values()
                  if (1 << topk) * Cnm <= N * Bw < (1 << (topk + 1)) * Cnm]
    _eq("rowE.dyadic_top.count", len(top_fibers), pn["dyadic_top"]["count_z"])
    _eq("rowE.dyadic_top.mass", sum(top_fibers), pn["dyadic_top"]["mass"])

    # --- the coset construction: 6 cosets of mu_4, all C(6,2)=15 pairwise unions
    mu4 = sorted(x for x in D if pow(x, 4, p) == 1)
    _eq("rowE.mu4_size", len(mu4), pn["mu4_size"])
    _eq("rowE.mu4_sum", sum(mu4) % p, pn["mu4_sum"])
    cosets = {}
    for x in D:
        cosets.setdefault(pow(x, 4, p), []).append(x)
    cosets = [tuple(sorted(v)) for v in cosets.values()]
    _eq("rowE.n_mu4_cosets", len(cosets), pn["n_mu4_cosets"])
    _eq("rowE.coset_sizes", sorted(set(len(c) for c in cosets)), [4])
    unions = []
    for c1, c2 in itertools.combinations(cosets, 2):
        M = tuple(sorted(c1 + c2))
        ps = tuple(sum(pow(x, j, p) for x in M) % p for j in (1, 2, 3))
        _eq(f"coset-union prefix {M}", ps, (0, 0, 0))       # every union is in the null fiber
        unions.append(M)
    _eq("rowE.choose(6,2)", len(unions), pn["choose"])
    # member-by-member identity: the 15 unions ARE the null fiber, exactly
    mem = members_of(D, p, m, w, {pn["null_key"]}, xp)[pn["null_key"]]
    actual = set(tuple(sorted(D[i] for i in combo)) for combo in mem)
    _eq("rowE.null_fiber == coset unions", set(unions), actual)
    # and every member is mu_4-invariant (a union of x^4-fibers = quotient scale 4)
    for M in actual:
        imgs = set(pow(x, 4, p) for x in M)
        if not all(pow(x, 4, p) in imgs for x in M):
            raise GateFail("row E null member not mu_4-invariant")
    print(f"        C(6,2)={len(unions)} unions of two mu_4-cosets, all with prefix (0,0,0);")
    print(f"        null fiber |Fib_3(0,0,0)|={counts[pn['null_key']]} equals them member-by-member;")
    print(f"        every member is mu_4-invariant (quotient scale 4); sum(mu_4)=0 mod {p}.")
    print(f"        Gamma_2={pn['gamma'][2]}")
    print("        PASS\n")


def gate5_twist(pins):
    print("gate 5  TWIST STABILIZER s(z)=gcd(n,A(z)) + ANTIPODAL (last-eyes) MECHANISM")
    # s(z) on pure directions, orbit size n/s(z) (prop:q-orbit-moment)
    for (lbl, A), (want_s, want_orb) in pins["twist"].items():
        n = next(r for r in ROWS if r["label"] == lbl)["n"]
        s = gcd(n, gcd(*A)) if len(A) > 1 else gcd(n, A[0])
        _eq(f"twist s{A} row {lbl}", (s, n // s), (want_s, want_orb))
        print(f"        {lbl}: A(z)={A}  s(z)=gcd({n},{A[0] if len(A)==1 else A})={s}"
              f"  orbit=n/s={n//s}")
    # antipodal mechanism at row E fiber z=(0,42,0)
    an = pins["antipodal"]
    p, n, m, w = 193, 24, 8, 3
    D = subgroup_of_order(p, n)
    xp = power_table(D, p, w)
    counts = count_fibers(D, p, m, w, xp)
    _eq("antipodal.N", counts[an["z"]], an["N"])
    A = tuple(j + 1 for j in range(w) if an["z"][j] != 0)
    s = gcd(n, A[0])
    _eq("antipodal.s(z)", s, an["s_z"])
    mem = members_of(D, p, m, w, {an["z"]}, xp)[an["z"]]
    n_anti = n_p5 = 0
    match = True
    for combo in mem:
        M = tuple(sorted(D[i] for i in combo))
        antipodal = tuple(sorted((-x) % p for x in M)) == M
        p5 = sum(pow(x, 5, p) for x in M) % p
        n_anti += int(antipodal)
        n_p5 += int(p5 == 0)
        # antipodal => p5==0 is a theorem (mu_2-pairs kill odd power sums); the
        # converse is not general -- here we check it holds member-by-member on
        # THIS fiber's members only (an empirical coincidence of the small fiber).
        match &= (antipodal == (p5 == 0))
        if antipodal:                       # antipodal member is mu_2-quotient: p_odd == 0
            odds = [sum(pow(x, j, p) for x in M) % p for j in (1, 3, 5, 7)]
            if any(o != 0 for o in odds):
                raise GateFail("antipodal member has nonzero odd power sum")
    _eq("antipodal.count", n_anti, an["n_antipodal"])
    _eq("antipodal.p5zero", n_p5, an["n_p5_zero"])
    if not match:
        raise GateFail("antipodal <=> (p5==0) failed on this fiber's members")
    print(f"        E fiber z={an['z']}: s(z)={s}; {n_anti}/{an['N']} members antipodal (M=-M),")
    print(f"        antipodal => p5(M)=0 (theorem, mu_2-quotient); <=> holds member-by-member")
    print(f"        on these {an['N']} members only (empirical; converse not general).")
    print("        => a COPRIME probe (j=5) still collapses on quotient MEMBERS: member-level,")
    print("           not trade-level, structure -- the note's last-eyes caveat.")
    print("        PASS\n")


GATES = [gate1_image, gate2_dyadic_gamma, gate3_confound, gate4_rowE_quotient, gate5_twist]


def run(pins):
    for g in GATES:
        g(pins)


# ---------------------------------------------------------------------------
# --tamper self-test: every pin, corrupted, must break some gate
# ---------------------------------------------------------------------------
def _corruptions(pins):
    import copy

    def mut(path, newval):
        q = copy.deepcopy(pins)
        d = q
        for k in path[:-1]:
            d = d[k]
        d[path[-1]] = newval
        return q

    yield "image[A,4].size", mut(["image", ("A", 4)], (4, 5, 4))
    yield "rowA.Gamma_2", mut(["rowA", "gamma", 2], Fraction(20445757, 8016009))
    yield "rowA.dyadic[1].count", mut(["rowA", "dyadic", 1], (1969, 4432))
    yield "rowA.observed", mut(["rowA", "observed"], 4729)
    yield "rowB.Gamma_3", mut(["rowB", "gamma", 3], Fraction(563665932127, 93574624001))
    yield "rowB.dyadic[0].count", mut(["rowB", "dyadic", 0], (1313, 2624))
    yield "rowB.below", mut(["rowB", "below"], (2927, 2928))
    yield "rowC.Gamma_2", mut(["rowC", "gamma", 2], Fraction(20698549, 8016009))
    yield "rowC.Rmax", mut(["rowC", "Rmax"], Fraction(63845, 8009))
    yield "rowD.Rmax", mut(["rowD", "Rmax"], Fraction(961, 127))
    yield "scan.coprime_tests", mut(["scan_totals", "coprime_tests"], 151)
    yield "scan.coprime_hits(nonzero)", mut(["scan_totals", "coprime_hits"], 1)
    yield "scan[A,4]", mut(["scan", ("A", 4)], (8, 19))
    yield "rowE.null_size", mut(["rowE", "null_size"], 14)
    yield "rowE.choose", mut(["rowE", "choose"], 14)
    yield "rowE.Gamma_2", mut(["rowE", "gamma", 2], Fraction(1, 1))
    yield "twist(E,(2,))", mut(["twist", ("E", (2,))], (1, 24))
    yield "antipodal.count", mut(["antipodal", "n_antipodal"], 4)


def tamper_selftest():
    print("=== --tamper self-test: each corrupted pin must break a gate ===\n")
    ok = 0
    total = 0
    for name, bad in _corruptions(PINS):
        total += 1
        try:
            # silence gate prints during tamper runs
            import io
            import contextlib
            with contextlib.redirect_stdout(io.StringIO()):
                run(bad)
        except GateFail as e:
            ok += 1
            print(f"  [caught] {name:28s} -> {str(e)[:70]}")
            continue
        except Exception as e:  # noqa
            ok += 1
            print(f"  [caught] {name:28s} -> {type(e).__name__}: {str(e)[:60]}")
            continue
        print(f"  [MISSED] {name:28s} -> corruption NOT detected!")
    print(f"\n{ok}/{total} corruptions detected.")
    return ok == total


def main():
    if "--tamper" in sys.argv[1:] or "--tamper-selftest" in sys.argv[1:]:
        # sanity: the honest pins must pass first
        try:
            import io
            import contextlib
            with contextlib.redirect_stdout(io.StringIO()):
                run(PINS)
        except GateFail as e:
            print(f"FAIL: honest pins do not pass: {e}")
            sys.exit(1)
        sys.exit(0 if tamper_selftest() else 1)

    print("verify_popular_fiber_probe_confound.py  (base 53bb5df; prob:entropy-inverse-q)\n")
    try:
        run(PINS)
    except GateFail as e:
        print(f"\nFAIL: {e}")
        sys.exit(1)
    print("ALL GATES PASS  (5/5)")
    sys.exit(0)


if __name__ == "__main__":
    main()
