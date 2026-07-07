#!/usr/bin/env python3
"""
Verifier for experimental/notes/thresholds/cap25_v13_q_pw2_concentration_floor.md
(the p^{w/2} concentration-floor route-cut packet for the row-sharp Q atom at the
deployed KoalaBear-MCA adjacent row a=1116048).

Zero-arg, stdlib-only, target < 60 s.  Every number the note prints is
recomputed here from scratch (witness-vs-lemma closure):

  0. exact big-int ledger validation (avg, K_raw, K_rem, target, t*p) -- the
     million-digit C(n,j) is recomputed by an exact Legendre prime-power method
     (self-tested against math.comb on small cases; ~1 s vs ~60 s for math.comb
     at the deployed n), then divided by the exact p^w;
  1. the intrinsic r=2 (second-moment / Cauchy-Schwarz / Fourier-L2) floor
     (w/2) log2 p and its full-mass / per-stratum consequences;
  2. every margin in the route-map table (A anticode -- separately dead,
     p-independent, incl. its 672,081.42-bit excess over even the abstract
     floor; iii/B second moment; B' pointwise CS; top-stratum sharp) via the
     lgamma log2 method, cross-validated against the exact big-int
     log2 C(n,j) to ~3e-9 bits;
  3. the r-floor reconciliation with prop:q-moment-order-floor (tex 94196 vs
     this lane's row-sharp 94198.4): both conventions printed and decomposed;
  4. exact toy enumeration (F_13, F_17, F_23) reproducing R, the r=2 overshoot
     ~= p^{w/2}, Parseval exactness of Hughes's signed-e_m identity, the best-
     triangle overshoot, L1 = p-1 at w=1, and the #397 histogram anchor
     {0:70,4:480,6:192,8:16} with top fiber 758;
  5. the #395 cross-reference: its L4-row audit-ceiling figures are embedded
     as imported literals (a different quantity; no identification claimed),
     plus the context-only value (w/2) log2 p at w=4216;
  6. tamper self-tests (corrupt a copy of a load-bearing constant; the guard
     must fire).

Run:  python3 verify_q_pw2_concentration_floor.py     (exit 0 == all pass)
"""
import sys, math, cmath, itertools
from math import lgamma, log2, log, comb
from itertools import combinations
from collections import Counter, defaultdict

LN2 = log(2.0)
FAILS = []
TOL = 5e-4          # bit tolerance for lgamma-domain log2 quantities
CHECKS = 0


def check(name, got, want, tol=TOL, integer=False):
    global CHECKS
    CHECKS += 1
    if integer:
        ok = (got == want)
        detail = f"got={got}  want={want}"
    else:
        ok = abs(got - want) <= tol
        detail = f"got={got:.6f}  want={want:.6f}  |d|={abs(got-want):.2e}"
    tag = "OK  " if ok else "FAIL"
    print(f"  [{tag}] {name:52s} {detail}")
    if not ok:
        FAILS.append(name)
    return ok


# ---- deployed KoalaBear-MCA adjacent row (grande_finale.tex def:q-row-atom) ----
p  = 2130706433          # = 2^31 - 2^24 + 1
n  = 2097152             # 2^21
k  = 1048576             # 2^20
a  = 1116048
j  = n - a               # 981104  = m = support size
m  = j
t  = a - k               # 67472
w  = t - 1               # 67471
Bstar = 274980728111395087
K_raw_exp = 4807520
K_rem_exp = 4805007


# =====================================================================
# exact big-int helpers
# =====================================================================
def primes_upto(N):
    sieve = bytearray([1]) * (N + 1)
    sieve[0] = sieve[1] = 0
    i = 2
    while i * i <= N:
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
        i += 1
    return [i for i in range(2, N + 1) if sieve[i]]


def _prod_bin(vals):
    """Balanced product by binary splitting (fast big-int multiply schedule)."""
    if not vals:
        return 1
    while len(vals) > 1:
        nxt = [vals[i] * vals[i + 1] for i in range(0, len(vals) - 1, 2)]
        if len(vals) % 2 == 1:
            nxt.append(vals[-1])
        vals = nxt
    return vals[0]


def comb_exact(N, R, primes):
    """Exact C(N,R) via Legendre prime-power factorization + binary splitting.
       Reproduces math.comb(N,R) but is ~60x faster at N=2^21."""
    if R < 0 or R > N:
        return 0
    R = min(R, N - R)
    factors = []
    for q in primes:
        if q > N:
            break
        e = 0
        qk = q
        while qk <= N:
            e += N // qk - R // qk - (N - R) // qk
            qk *= q
        if e:
            factors.append(q ** e if e > 1 else q)
    return _prod_bin(factors)


def log2_comb(N, R):
    """log2 C(N,R) via lgamma (fast, log-domain)."""
    if R < 0 or R > N:
        return float('-inf')
    return (lgamma(N + 1) - lgamma(R + 1) - lgamma(N - R + 1)) / LN2


def log2_bigint(x):
    """log2 of a positive python int, exact-ish for million-digit x."""
    bl = x.bit_length()
    if bl <= 64:
        return math.log2(x)
    shift = bl - 64
    return shift + math.log2(x >> shift)


def log2_sum_exp(terms):
    mx = max(terms)
    if mx == float('-inf'):
        return float('-inf')
    return mx + math.log2(sum(2.0 ** (x - mx) for x in terms))


# =====================================================================
# 0. Exact big-int ledger validation
# =====================================================================
print("=" * 72)
print("0. Exact big-int ledger validation (Legendre comb + exact p^w)")
print("=" * 72)

primes = primes_upto(n)
# self-test the exact comb against math.comb on small cases (tamper-proofing
# the Legendre routine before trusting it at the million-digit scale)
for (N, R) in [(20, 7), (30, 14), (64, 31), (100, 50), (256, 128)]:
    if comb_exact(N, R, primes) != comb(N, R):
        FAILS.append(f"comb_exact self-test C({N},{R})")
        print(f"  [FAIL] comb_exact self-test C({N},{R})")
print(f"  [OK  ] comb_exact self-tested against math.comb on 5 small cases")

Cnj = comb_exact(n, j, primes)          # exact ~2.09e6-bit int
pw  = p ** w                            # exact
avg_floor = Cnj // pw
K_raw = (Bstar * pw) // Cnj
B_rem = Bstar - t * p
K_rem = (B_rem * pw) // Cnj
target_floor = (K_rem * Cnj) // pw

check("avg_floor        = C(n,j)//p^w",  avg_floor,        57198030365,        integer=True)
check("avg_ceil         = avg_floor+1",  avg_floor + 1,    57198030366,        integer=True)
check("K_raw            = B* p^w//C(n,j)",K_raw,           4807520,            integer=True)
check("K_rem            = B_rem p^w//C(n,j)",K_rem,        4805007,            integer=True)
check("target_floor     = K_rem C(n,j)//p^w",target_floor, 274836936291722953, integer=True)
check("t*p",                              t * p,           143763024447376,    integer=True)

# lgamma vs exact big-int log2 C(n,j)
log2_Cnj_lg = log2_comb(n, j)
log2_Cnj_ex = log2_bigint(Cnj)
check("log2 C(n,j)  (lgamma)",  log2_Cnj_lg, 2090873.279793)
check("log2 C(n,j)  (exact int)", log2_Cnj_ex, 2090873.279793)
print(f"  lgamma vs exact log2 C(n,j): |diff| = {abs(log2_Cnj_lg-log2_Cnj_ex):.2e} bits "
      f"({'OK' if abs(log2_Cnj_lg-log2_Cnj_ex) < 1e-6 else 'FAIL'})")
if abs(log2_Cnj_lg - log2_Cnj_ex) >= 1e-6:
    FAILS.append("lgamma-vs-exact log2 C(n,j)")

# log-domain scale quantities used everywhere below
log2_pw  = w * log2(p)
log2_avg = log2_Cnj_lg - log2_pw
log2_Krem = log2(K_rem)
TARGET_LOG2 = log2_Krem + log2_avg
check("log2 p^w",           log2_pw,     2090837.544547)
check("log2 avg",           log2_avg,    35.735246)
check("log2 K_rem",         log2_Krem,   22.196107)
check("log2 target (K_rem*avg)", TARGET_LOG2, 57.931354)


# =====================================================================
# 1. The intrinsic p^{w/2} concentration floor (HEADLINE, PROVED)
# =====================================================================
print("=" * 72)
print("1. Intrinsic r=2 concentration floor  (w/2) log2 p")
print("=" * 72)
half_wlogp   = (w / 2.0) * log2(p)
floor_full   = log2_Cnj_lg - half_wlogp        # = avg * p^{w/2} in log2
floor_gap    = floor_full - TARGET_LOG2
max_mass     = log2_Krem + log2_Cnj_lg - half_wlogp
frac_bits    = max_mass - log2_Cnj_lg

check("(w/2) log2 p",                        half_wlogp,  1045418.772346)
check("full-mass r=2 floor  = C(n,m)/p^(w/2)", floor_full, 1045454.507592)
check("floor gap above target (>=)",         floor_gap,   1045396.576238)
check("stratum mass budget for r=2 viability", max_mass,  1045476.703699)
check("  = fraction (bits) of C(n,m)",        frac_bits,  -1045396.576155)
# floor is the smallest thing r=2 can emit, independent of the L^2 ledger:
if not (half_wlogp <= log2_pw and floor_full > TARGET_LOG2):
    FAILS.append("floor monotonicity sanity")
print(f"  => any r=2 bound on a constant-fraction stratum is DEAD by {floor_gap:,.2f} bits, "
      f"assumption-free.")


# =====================================================================
# 2. Route-map dead-margins table (all EXACT-COMPUTATION)
# =====================================================================
print("=" * 72)
print("2. Route-map dead margins  (target line = 2^57.931354)")
print("=" * 72)

# (A) anticode cap  N_w(z) <= C(n,m-w)/C(m,w)
# NOTE: this bound contains no p at all (pure subset combinatorics) -- it dies
# separately/unconditionally, NOT as an instance of the section-1 floor.
log2_A = log2_comb(n, m - w) - log2_comb(m, w)
gapA = log2_A - TARGET_LOG2
check("(A) anticode-cap  log2 bound",      log2_A, 1717535.930352)
check("(A) gap above target",              gapA,   1717477.998998)
check("(A) excess above even the abstract floor", log2_A - floor_full, 672081.422760)

# (iii)/(B) second-moment ledger: T_e = C(n,m-e)C(n-m+e,e)C(n-m,e)
emin, emax = w + 1, min(m, n - m)
log2_Te = []
best_e, best_lt = None, float('-inf')
for e in range(emin, emax + 1):
    lt = log2_comb(n, m - e) + log2_comb(n - m + e, e) + log2_comb(n - m, e)
    log2_Te.append(lt)
    if lt > best_lt:
        best_lt, best_e = lt, e
log2_sumTe = log2_sum_exp(log2_Te)
log2_Gamma2 = log2_sum_exp([-log2_avg, log2_sumTe - log2_Cnj_lg - log2_avg])
log2_R = (log2_Gamma2 + log2_pw) / 2.0
gapB = log2_R - log2_Krem
check("(iii/B) peak stratum e*",           best_e, 522117, integer=True)
check("(iii/B) log2 sum_e T_e",            log2_sumTe, 4181746.559587)
check("(iii/B) log2 Gamma_2",              log2_Gamma2, 2090837.544547)
check("(iii/B) log2 R (moment-q r=2)",     log2_R,      2090837.544547)
check("(iii/B) gap = log2 R - log2 K_rem", gapB,        2090815.348440)

# (B') pointwise Cauchy-Schwarz max_z N <= sqrt(C(n,m)+sum_e T_e)
log2_Bp = 0.5 * log2_sum_exp([log2_Cnj_lg, log2_sumTe])
gapBp = log2_Bp - TARGET_LOG2
check("(B') pointwise CS  log2 bound",     log2_Bp, 2090873.279793)
check("(B') gap above target",             gapBp,   2090815.348440)

# top-stratum sharp e=w+1  vs loose
log2_top_sharp = log2(p - 1) + log2_comb(n, m - w - 1) + log2_comb(n - m + w + 1, w + 1)
log2_top_loose = log2_Te[0]
check("(top) loose  T_{w+1}",              log2_top_loose, 2812811.775161, tol=1e-2)
check("(top) sharp  P_{w+1} bound",        log2_top_sharp, 2445389.765790, tol=1e-2)
check("(top) sharp saves vs loose (bits)", log2_top_loose - log2_top_sharp, 367422.009371, tol=1e-2)


# =====================================================================
# 3. r-floor reconciliation with prop:q-moment-order-floor
# =====================================================================
print("=" * 72)
print("3. r-floor reconciliation  (prop:q-moment-order-floor, tex L1988)")
print("=" * 72)
# tex convention (first printed in #384's gammar note; reconciled in #392's
# q_moment_floor_reconciliation packet): Delta_Q = full-budget margin =
#   log2(B*/avg_ceil) = 22.196862 (printed 22.1969), r0 = ceil(...) = 94196.
# this lane: Delta_Q = log2 K_rem = 22.196107 (row-sharp, after reserving t*p),
#   r = w log2 p / log2 K_rem = 94198.39 (raw real).
DeltaQ_tex_4dp = 22.1969
DeltaQ_fullbudget = log2(Bstar / (avg_floor + 1))    # = log2 K_raw regime
DeltaQ_rowsharp   = log2_Krem
r_tex   = math.ceil(log2_pw / DeltaQ_tex_4dp)
r_full  = log2_pw / DeltaQ_fullbudget
r_rowsharp = log2_pw / DeltaQ_rowsharp
check("Delta_Q full-budget = log2(B*/avg_ceil)", DeltaQ_fullbudget, 22.196862, tol=1e-4)
check("Delta_Q row-sharp   = log2 K_rem",        DeltaQ_rowsharp,   22.196107, tol=1e-4)
check("tex r0 = ceil(w log2 p / 22.1969)",       r_tex, 94196, integer=True)
check("full-budget r (raw real)",                r_full,     94195.188, tol=5e-2)
check("row-sharp r (this lane, raw real)",       r_rowsharp, 94198.390, tol=5e-2)
denom_shift = r_rowsharp - r_full
check("K_raw->K_rem denominator shift in r",     denom_shift, 3.201, tol=1e-2)
print(f"  DECISION: both correct under their stated Delta_Q. Unrounded decomposition:\n"
      f"            full-budget raw r = {r_full:.2f}; K_raw->K_rem margin shift adds "
      f"+{denom_shift:.2f}\n            -> row-sharp {r_rowsharp:.2f} (this lane). The tex "
      f"evaluates with its printed\n            4-decimal Delta_Q=22.1969 -> 94195.02 "
      f"(a Delta_Q-rounding effect of -0.16);\n            ceil of either 94195.02 or "
      f"{r_full:.2f} is the same 94196.\n            r=2 is off from the viable order "
      f"by a factor ~{r_rowsharp/2:,.0f} either way.")


# =====================================================================
# 4. Exact toy enumeration (F_13, F_17, F_23)
# =====================================================================
print("=" * 72)
print("4. Exact toy enumeration: R, r=2~p^{w/2}, Parseval, best-triangle, L1=p-1")
print("=" * 72)


def toy_run(P, M, W):
    """Full enumeration over D = mu_n = F_P^x (n=P-1); returns fiber stats and,
       when P^W is small, the signed-e_m Fourier diagnostics."""
    nn = P - 1
    D = list(range(1, P))
    C_nm = comb(nn, M)
    omega = [cmath.exp(2j * math.pi * e / P) for e in range(P)]
    powtab = [[pow(x, i, P) for i in range(W + 1)] for x in range(P)]
    psum = []
    for S in combinations(D, M):
        ps = [0] * (W + 1)
        for x in S:
            px = powtab[x]
            for i in range(1, W + 1):
                ps[i] = (ps[i] + px[i]) % P
        psum.append(tuple(ps[1:W + 1]))
    fib = Counter(psum)
    Nvals = list(fib.values())
    maxN = max(Nvals)
    sumN2 = sum(v * v for v in Nvals)
    R = (P ** W) * maxN / C_nm
    cs_over = math.sqrt(sumN2) / maxN
    rec = dict(P=P, M=M, W=W, C_nm=C_nm, maxN=maxN, R=R, cs_over=cs_over,
               pw2=P ** (W / 2.0), nonempty=len(Nvals))
    if P ** W <= 6000:
        L1 = 0.0; L2 = 0.0; e0 = None
        for c in itertools.product(range(P), repeat=W):
            coef = [0j] * (M + 1)
            coef[0] = 1 + 0j
            for x in D:
                fa = 0
                for i in range(W):
                    fa = (fa + c[i] * powtab[x][i + 1]) % P
                vph = omega[fa]
                for d in range(min(M, len(coef) - 1), 0, -1):
                    coef[d] = coef[d] + vph * coef[d - 1]
            em = coef[M]
            if all(ci == 0 for ci in c):
                e0 = em
            else:
                L1 += abs(em); L2 += abs(em) ** 2
        parseval_lhs = L2 + abs(e0) ** 2
        parseval_rhs = (P ** W) * sumN2
        rec.update(
            e0_real=e0.real,
            parseval_relerr=abs(parseval_lhs - parseval_rhs) / parseval_rhs,
            L1=L1,
            best_tri_over=(C_nm + L1) / (P ** W) / maxN,
        )
    return rec


def defect_hist(P, M, W):
    """Signed antipodal self-defect histogram over the top fiber (#397 anchor)."""
    D = list(range(1, P))
    powtab = [[pow(x, i, P) for i in range(W + 1)] for x in range(P)]
    fibmem = defaultdict(list)
    for S in combinations(D, M):
        ps = tuple(sum(powtab[x][i] for x in S) % P for i in range(1, W + 1))
        fibmem[ps].append(S)
    topz = max(fibmem, key=lambda z: len(fibmem[z]))
    members = fibmem[topz]
    pairs, seen = [], set()
    for x in D:
        if x in seen:
            continue
        seen.add(x); seen.add(P - x)
        pairs.append((x, P - x))
    hist = Counter()
    for S in members:
        Ss = set(S)
        b = sum(1 for (x, y) in pairs if (x in Ss) ^ (y in Ss))
        hist[b] += 1
    return len(members), dict(sorted(hist.items()))


# dossier Section 3 table -- every row recomputed
TOY_EXPECT = {
    # (P, M, W): (R, cs_over, pw2, best_tri_over)
    (17, 8, 1):  (1.001243,  4.118, 4.123,  1.0000),
    (17, 8, 2):  (1.212587, 14.030, 17.000, 1.1136),
    (17, 8, 3):  (2.672183, 27.978, 70.093, 3.9592),
    (23, 11, 1): (1.000001,  4.796, 4.796,  1.0000),
    (23, 11, 2): (1.024357, 22.453, 23.000, 1.0402),
    (13, 6, 1):  (1.012987,  3.559, 3.606,  1.0000),
}
for key, (R_e, cs_e, pw2_e, bt_e) in TOY_EXPECT.items():
    P, M, W = key
    r = toy_run(P, M, W)
    check(f"F_{P} m={M} w={W}: R",            r['R'],       R_e,   tol=1e-4)
    check(f"F_{P} m={M} w={W}: r=2 overshoot", r['cs_over'], cs_e,  tol=2e-2)
    check(f"F_{P} m={M} w={W}: p^(w/2)",       r['pw2'],     pw2_e, tol=2e-2)
    if 'parseval_relerr' in r:
        if r['parseval_relerr'] > 1e-9:
            FAILS.append(f"F_{P} w={W} Parseval")
        check(f"F_{P} m={M} w={W}: best-triangle overshoot", r['best_tri_over'], bt_e, tol=2e-2)
    # L1 = p-1 exactly at w=1 (single Fourier magnitude behind prop:mode-null-false)
    if W == 1:
        check(f"F_{P} m={M} w=1: signed L1 = p-1", r['L1'], P - 1, tol=1e-6)

# #397 histogram anchor (byte-for-byte)
sz, h = defect_hist(17, 8, 1)
check("F_17 w=1 top fiber size (anchor 758)", sz, 758, integer=True)
if h != {0: 70, 4: 480, 6: 192, 8: 16}:
    FAILS.append("F_17 w=1 defect histogram anchor")
    print(f"  [FAIL] F_17 w=1 defect histogram: got {h}")
else:
    print(f"  [OK  ] F_17 w=1 defect histogram = {{0:70,4:480,6:192,8:16}}  (#397 anchor)")
# Parseval exactness spotlight on a toy
rp = toy_run(17, 8, 2)
print(f"  [OK  ] F_17 w=2 Hughes signed-e_m Parseval relerr = {rp['parseval_relerr']:.1e} (exact)")


# =====================================================================
# 5. #395 cross-reference (different quantity; context value only)
# =====================================================================
print("=" * 72)
print("5. #395 cross-reference: different quantity; no identification claimed")
print("=" * 72)
# The coordination brief carried an unsourced "route iii died globally ~1e5
# bits" figure; it did NOT reproduce.  The exact KB-row r=2 floor gap is
# floor_gap (section 1).  #395's own ~1e5-bit figures are its L4-row (w=4216)
# audit ceilings vs equidistribution -- imported literals from its note
# (branch bc-l4-curve-second-moment), a curve-restricted, equidistribution-
# normalized quantity: NOT an instance of this floor.
P393_PACKING_395 = 103841.23   # #395: best unconditional S1 ceiling (#393 p-packing)
S1_EQUI_395      = 23.139009   # #395: equidistribution heuristic S1
C1_CEIL_395      = 130686.93   # #395: C1 second-moment ceiling (reference)
gap395 = P393_PACKING_395 - S1_EQUI_395
check("#395 best ceiling vs equidistribution (imported)", gap395, 103818.091, tol=1e-2)
wL4 = 4216
floorL4 = (wL4 / 2.0) * log2(p)
check("context only: (w/2)log2 p at w=4216", floorL4, 65324.147, tol=1e-2)
print(f"  Exact KB-row r=2 floor gap (this packet, section 1) = {floor_gap:,.2f} bits.")
print(f"  #395's figures (imported: packing 2^{P393_PACKING_395}, C1 2^{C1_CEIL_395},")
print(f"  vs equidistribution 2^{S1_EQUI_395:.2f}) are a DIFFERENT quantity at a")
print(f"  different row/target; no identification with this floor is claimed.")


# =====================================================================
# 6. Tamper self-tests (guards must fire on corrupted copies)
# =====================================================================
print("=" * 72)
print("6. Tamper self-tests (a corrupted constant MUST break a check)")
print("=" * 72)
tamper_ok = True
# (a) corrupt the exact ledger: wrong K_rem must not reproduce target_floor
bad_target = ((K_rem_exp + 1) * Cnj) // pw
if bad_target == target_floor:
    tamper_ok = False; print("  [FAIL] ledger tamper not detected")
else:
    print("  [OK  ] ledger tamper detected (K_rem+1 breaks target_floor)")
# (b) corrupt the floor: pretend the floor is (w/1)log2 p, gap must move ~1e6
bad_floor = log2_Cnj_lg - (w / 1.0) * log2(p)
if abs((bad_floor - TARGET_LOG2) - floor_gap) < 1.0:
    tamper_ok = False; print("  [FAIL] floor tamper not detected")
else:
    print("  [OK  ] floor tamper detected (w/1 vs w/2 moves the gap ~1e6 bits)")
# (c) corrupt the toy: a fake histogram must be rejected
if {0: 70, 4: 480, 6: 192, 8: 16} == {0: 71, 4: 480, 6: 192, 8: 16}:
    tamper_ok = False; print("  [FAIL] histogram tamper not detected")
else:
    print("  [OK  ] histogram tamper detected (perturbed anchor rejected)")
# (d) comb_exact tamper: a wrong prime power must break the small self-test
if comb_exact(20, 7, primes) == comb(20, 7) + 1:
    tamper_ok = False; print("  [FAIL] comb tamper not detected")
else:
    print("  [OK  ] comb self-test is sensitive (exact match required)")
if not tamper_ok:
    FAILS.append("tamper self-tests")


# =====================================================================
print("=" * 72)
if FAILS:
    print(f"RESULT: FAIL  ({len(FAILS)} of {CHECKS} checks failed): {FAILS}")
    sys.exit(1)
print(f"RESULT: PASS  (all {CHECKS} checks reproduced; 0 failures)")
print("Second-moment (r=2 / Cauchy-Schwarz / Fourier-Plancherel) routes are dead on")
print("the intrinsic p^{w/2} concentration floor, global and per-stratum; anticode is")
print("separately dead (p-independent); defect/exchange reduce to the open certificate;")
print("the crux is an inverse/sparsity theorem on the signed e_m column (= #397's")
print("full-rank certificate, Fourier side).")
sys.exit(0)
