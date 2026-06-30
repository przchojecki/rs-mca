#!/usr/bin/env python3
"""
Numerical certificate for Paper D v7 (tex/cs25_cap_v7.tex):
  thm:main  (universal cap, lines 575-618)
  cor:grand (challenge envelope, line 714) -- the headline 2^-86 / 2^-42 caps
  cor:deployed (KoalaBear sextic, line 792) -- the deployed 2^-22 row

Pure stdlib only: math.comb, fractions.Fraction, math.log2 (via a big-int-safe
helper so we never overflow float on ~1000-bit binomials).  No numpy / no sympy.

hypothesis eq:hyp :  C(N, rho*N+2) >= |B| * (q/k + 1)
conclusion        :  eca/emca > (1/(2k)) * (1 - n/q)
                  =  (q-n) / (2*k*q)

We report, per representative challenge instance, EXACT decisions plus float
bit-counts for readability:
  (i)   eq:hyp slack in bits = log2 C(N, rhoN+2) - log2(|B|(q/k+1))
  (ii)  error floor in bits  = -log2((1/(2k))(1-n/q)) = log2( 2*k*q / (q-n) )
  (iii) checks:  eq:hyp holds (k*C >= |B|(q+k));
                 error floor > 2^-86  (general envelope);
                 error floor > 2^-42  (when q >= 2n);
                 gap 2/N == claimed 2^-e.

ALL pass/fail decisions use exact integer / Fraction comparisons.
The float "bits" columns are display-only.
"""

import math
from fractions import Fraction

# ---------- big-int-safe log2 (display only) ----------------------------------
def log2_int(x):
    if x <= 0:
        raise ValueError("log2_int needs positive int")
    b = x.bit_length()
    if b <= 53:
        return math.log2(x)
    shift = b - 53
    top = x >> shift                 # exact 53-bit int, fits float
    return shift + math.log2(top)    # discarded low bits: <2^-53 rel err

def log2_frac(fr):
    fr = Fraction(fr)
    return log2_int(fr.numerator) - log2_int(fr.denominator)

def pow2name(x):
    if x > 0 and (x & (x - 1)) == 0:
        return "2^%d" % (x.bit_length() - 1)
    return str(x)

# ---------- exact predicates --------------------------------------------------
def eq_hyp_ok(N, l2, B, q, k):
    """C(N,l2) >= B*(q/k+1)  <=>  k*C(N,l2) >= B*(q+k)   (exact)."""
    lhs = k * math.comb(N, l2)
    rhs = B * (q + k)
    return lhs >= rhs, lhs, rhs

def floor_gt_2_pow(neg_e, q, n, k):
    """error floor (q-n)/(2kq) > 2^-neg_e  <=>  2^neg_e*(q-n) > 2kq   (exact)."""
    lhs = (q - n) << neg_e
    rhs = 2 * k * q
    return lhs > rhs

# ---------- one row -----------------------------------------------------------
def make_row(tag, rho, N, e_gap, n, k, q, B, q_ge_2n, claim_e):
    l2 = rho.numerator * N // rho.denominator + 2          # rho*N + 2 (rho*N integral)
    assert (rho * N).denominator == 1, "rho*N must be integral"
    assert n % N == 0, "N | n"
    # eq:hyp
    hyp_ok, hl, hr = eq_hyp_ok(N, l2, B, q, k)
    hyp_slack_bits = log2_int(math.comb(N, l2)) - log2_frac(Fraction(B) * (q + k) / k)
    # error floor value (exact Fraction) and bits
    E = Fraction(q - n, 2 * k * q)
    floor_bits = log2_frac(Fraction(1) / E)                # = log2(2kq/(q-n))
    # checks
    ok86 = floor_gt_2_pow(86, q, n, k)                     # general envelope claim
    ok42 = floor_gt_2_pow(42, q, n, k) if q_ge_2n else None
    okclaim = floor_gt_2_pow(claim_e, q, n, k)
    gap_ok = (N == (1 << (e_gap + 1)))                     # 2/N == 2^-e_gap
    return dict(tag=tag, rho=rho, N=N, e_gap=e_gap, n=n, k=k, q=q, B=B, l2=l2,
                hyp_ok=hyp_ok, hyp_slack_bits=hyp_slack_bits,
                E=E, floor_bits=floor_bits,
                ok86=ok86, ok42=ok42, claim_e=claim_e, okclaim=okclaim,
                q_ge_2n=q_ge_2n, gap_ok=gap_ok)

# ---------- build instances ---------------------------------------------------
TWO256 = 1 << 256
rates = [
    # rho,            N,    e_gap
    (Fraction(1, 2),  1024, 9),
    (Fraction(1, 4),  1024, 9),
    (Fraction(1, 8),  1024, 9),
    (Fraction(1, 16), 2048, 10),
]

def q_hi_below_2pow256(n):
    """largest q < 2^256 with q == 1 (mod n)."""
    M = TWO256 - 1
    return 1 + n * ((M - 1) // n)

rows = []
for rho, N, e_gap in rates:
    # min-envelope instance: smallest n in envelope (n = N), k = rho*n
    n_min = N
    k_min = (rho * n_min)
    assert k_min.denominator == 1
    k_min = k_min.numerator
    # max-envelope instance: k = 2^40 (max), n = k/rho
    k_max = 1 << 40
    n_max = (Fraction(k_max) / rho)
    assert n_max.denominator == 1
    n_max = n_max.numerator

    for (lbl, n, k) in [("min", n_min, k_min), ("max", n_max, k_max)]:
        # sanity on envelope constraints
        assert k <= (1 << 40), "k<=2^40"
        assert n % N == 0, "N | n"
        need = 11 if rho == Fraction(1, 16) else 10
        assert n % (1 << need) == 0, "2-divisibility of n"
        a = n // N
        assert k % a == 0, "a=n/N | k"
        assert (1 - rho) * N >= 3, "(1-rho)N>=3"

        # q scenarios (all satisfy q == 1 mod n, i.e. n | q-1)
        q_hi = q_hi_below_2pow256(n)          # field just under 2^256  (>= 2n)
        q_2n = 2 * n + 1                       # smallest q >= 2n        (= 2n case)
        q_lo = n + 1                           # smallest valid q (worst floor; <2n)
        # |B| = q  (B=F): the eq:hyp WORST case (largest RHS) over the envelope
        rows.append(make_row("%s/%s/q~2^256" % (lbl, "hi"), rho, N, e_gap, n, k, q_hi, q_hi, True,  42))
        rows.append(make_row("%s/%s/q=2n+1"  % (lbl, "2n"), rho, N, e_gap, n, k, q_2n, q_2n, True,  42))
        rows.append(make_row("%s/%s/q=n+1"   % (lbl, "lo"), rho, N, e_gap, n, k, q_lo, q_lo, False, 86))

# ---------- deployed row (cor:deployed) --------------------------------------
p = (1 << 31) - (1 << 24) + 1          # KoalaBear prime 2^31-2^24+1
q_dep = p ** 6
dep = make_row("deployed/KoalaBear-sextic", Fraction(1, 2), 256, 7,
               1 << 21, 1 << 20, q_dep, p, q_ge_2n=True, claim_e=22)

# ---------- print -------------------------------------------------------------
def f(x): return "%.4f" % x

print("=" * 132)
print("Paper D v7  cs25_cap_v7.tex  --  thm:main / cor:grand numerical certificate")
print("eq:hyp:  C(N, rhoN+2) >= |B|(q/k+1)      floor: (1/2k)(1-n/q) = (q-n)/(2kq)")
print("=" * 132)
hdr = ("rho", "N", "gap", "instance", "n", "k", "|F|bits",
       "hyp-slack(b)", "floorbits", "claim", "claim?", "86?", "42?", "gap?")
print("%-5s %-5s %-6s %-12s %-7s %-7s %-9s %-12s %-10s %-7s %-6s %-4s %-4s %-4s" % hdr)
print("-" * 132)
all_pass = True
tight = []
for r in rows:
    rho = r["rho"]
    gap = "2^-%d" % r["e_gap"]
    claim = "2^-%d" % r["claim_e"]
    fb = r["floor_bits"]
    # exact-decision pass flags
    okclaim = r["okclaim"]; ok86 = r["ok86"]; ok42 = r["ok42"]; gok = r["gap_ok"]; hok = r["hyp_ok"]
    row_pass = hok and ok86 and gok and (ok42 if r["q_ge_2n"] else True) and okclaim
    all_pass = all_pass and row_pass
    print("%-5s %-5s %-6s %-12s %-7s %-7s %-9s %-12s %-10s %-7s %-6s %-4s %-4s %-4s" % (
        "%d/%d" % (rho.numerator, rho.denominator), r["N"], gap, r["tag"].split("/", 1)[1] if "/" in r["tag"] else r["tag"],
        pow2name(r["n"]), pow2name(r["k"]), f(log2_int(r["q"])),
        f(r["hyp_slack_bits"]), f(fb), claim,
        "PASS" if okclaim else "FAIL", "Y" if ok86 else "N",
        ("Y" if ok42 else "N") if ok42 is not None else "-", "Y" if gok else "N"))
    # tightness flags
    if r["q_ge_2n"]:
        if abs(fb - 42) < 2.0:
            tight.append("rho=%d/%d [%s]: q>=2n  floor ~ 2^-%.4f  vs claim 2^-42  (head-room %.4f bits to 2^-42)"
                         % (rho.numerator, rho.denominator, r["tag"], fb, 42 - fb))
    else:
        if abs(fb - 86) < 2.0:
            tight.append("rho=%d/%d [%s]: general floor ~ 2^-%.4f  vs claim 2^-86  (head-room %.4f bits to 2^-86)"
                         % (rho.numerator, rho.denominator, r["tag"], fb, 86 - fb))

# deployed
print("-" * 132)
r = dep
fb = r["floor_bits"]
dep_pass = r["hyp_ok"] and r["okclaim"] and r["gap_ok"]
all_pass = all_pass and dep_pass
print("%-5s %-5s %-6s %-12s %-7s %-7s %-9s %-12s %-10s %-7s %-6s %-4s %-4s %-4s" % (
    "1/2", 256, "2^-7", "KoalaBear^6", "2^21", "2^20", f(log2_int(r["q"])),
    f(r["hyp_slack_bits"]), f(fb), "2^-22",
    "PASS" if r["okclaim"] else "FAIL", "-", "Y" if r["ok42"] else "N", "Y" if r["gap_ok"] else "N"))
print("=" * 132)

# ---------- headline reproductions -------------------------------------------
print()
print("HEADLINE CHECKS")
print("-" * 60)

# (A) eq:hyp universal 'needed < 513' and '>=39 bits to spare'
#     universal RHS bound: |B|(q/k+1) <= q(q+1) < 2^256(2^256+1) < 2^513  (k>=1, |B|<=q)
qmax = TWO256 - 1
universal_rhs = qmax * (qmax + 1)            # >= |B|(q/k+1) for all envelope instances
print("eq:hyp universal RHS ceiling log2(q(q+1)) at q=2^256-1 = %.4f  (paper: < 513)  -> %s"
      % (log2_int(universal_rhs), "OK <513" if universal_rhs < (1 << 513) else "FAIL"))
for rho, N, e_gap in rates:
    l2 = (rho * N).numerator + 2
    lhsbits = log2_int(math.comb(N, l2))
    print("  rho=%d/%d: log2 C(%d,%d) = %.4f   slack vs universal 513 ceiling = %.4f bits  (paper table floor %s)"
          % (rho.numerator, rho.denominator, N, l2, lhsbits, lhsbits - 513,
             {2:1013, 4:823, 8:552, 16:687}[rho.denominator]))

# (B) the binding 2^-86 worst case: rho=1/16, k=2^40, n=2^44, q=n+1
k0 = 1 << 40; n0 = 1 << 44; q0 = n0 + 1
val = Fraction(q0 - n0, 2 * k0 * q0)         # = 1/(2k(n+1))
print()
print("binding 2^-86 worst case (rho=1/16, k=2^40, n=2^44, q=n+1):")
print("  floor = 1/(2k(n+1)) = 1/(2^85+2^41) ;  -log2 = %.6f bits ;  exact (2^86)*1 > 2k(n+1)? %s"
      % (log2_frac(Fraction(1) / val), (q0 - n0) << 86 > 2 * k0 * q0))
print("  i.e. floor = 2^-%.6f  >  2^-86  : %s" % (log2_frac(Fraction(1)/val), val > Fraction(1, 1 << 86)))

# (C) deployed intermediate (1-2^-164)2^-21 and 2^-22
nq = Fraction(1 << 21, p ** 6)
print()
print("deployed: n/q = 2^21/p^6 = 2^-%.4f  (paper: < 2^-164  -> %s)"
      % (-log2_frac(nq), "OK" if nq < Fraction(1, 1 << 164) else "FAIL"))
Edep = Fraction(1, 1 << 21) * (1 - nq)
print("          floor = (1-n/q)/2^21 = 2^-%.6f   > 2^-22 ? %s   > (1-2^-164)2^-21 ? %s"
      % (log2_frac(Fraction(1)/Edep), Edep > Fraction(1, 1 << 22),
         Edep >= Fraction(1, 1 << 21) * (1 - Fraction(1, 1 << 164))))

print()
print("TIGHT / NOTABLE ROWS")
print("-" * 60)
for t in sorted(set(tight)):
    print("  " + t)

print()
print("ALL EXACT CHECKS PASS:", all_pass)
