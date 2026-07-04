#!/usr/bin/env python3
"""Verifier for the star-PTE support micro-lemma (h <= A, not 2h <= A).

Companion note:
  experimental/notes/roadmaps/star_pte_support_bound.md

WHAT THE LEMMA SAYS.  Two distinct list members are codewords c_f, c_g
(evaluations of degree-<k polynomials f != g) with exact-agreement sets
S_f, S_g relative to the received word, |S_f| = |S_g| = A = k + t.  Put
r = |S_f cap S_g|.  The canonical star-PTE trade is (P, Q) with
P = S_f \\ S_g, Q = S_g \\ S_f, half-size h = |P| = |Q| = A - r and full
support |P u Q| = 2h = 2(A - r).  Then:
  (a) On S_f cap S_g both codewords equal the received word, hence each
      other; two distinct degree-<k polynomials agree in <= k-1 points,
      so r <= k-1 and therefore h = A - r >= A-(k-1) = t+1 (h > t).
  (b) r >= 0 gives h <= A, with equality iff S_f cap S_g = empty.
  (c) P subset S_f and Q subset S_g sit in TWO DIFFERENT agreement sets,
      so the support 2h ranges over (2t, 2A]; it is NOT bounded by A.
Hence the R_PTE consumer envelope is h <= A (the "h <= A" reading), and
the "2h <= A" reading is WRONG (it wrongly assumes the whole 2h-support
sits inside a single size-A agreement set).

This script checks (i) the arithmetic identities / range formulas at the
three Row-C rates and the corrected mid/large-h gap, and (ii) the
structural claims (a)-(c) via explicit finite-field constructions that
REALISE r = 0 (so h = A, support 2A > A) and r = k-1 (so h = t+1), plus a
randomised confirmation that distinct degree-<k codewords agree in <= k-1
points.

Pure stdlib (random, itertools).  Runs in well under a second.
"""

import json
import os
import random
import sys

_RESULTS = []

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CERT = os.path.join(
    REPO,
    "experimental",
    "data",
    "certificates",
    "star-pte-support-bound",
    "star_pte_support_bound.json",
)


def check(name, ok, detail=""):
    _RESULTS.append((name, bool(ok)))
    tag = "PASS" if ok else "FAIL"
    line = f"[{tag}] {name}"
    if detail:
        line += f"\n        {detail}"
    print(line)
    return ok


# ======================================================================
# 1.  Arithmetic: H_max = A, the h-range, and the corrected gap
# ======================================================================
# Row-C parameters at n = 1024 (banked; qa22_staircase_budget_column.md,
# and h_window_derivation_audit.md section 1).
N = 1024
LOG2N = 10
GRAMMAR_CAP = LOG2N * LOG2N          # (log2 n)^2 = 100  (frozen W3 v1 window)
BAD_CAP = 2 * LOG2N                  # 2 log2 n   = 20    (unbanked assembly cap)

# rate : (k, t)   with A = k + t
ROWS = {
    "1/4":  (256, 5),
    "1/8":  (128, 5),
    "1/16": (64, 3),
}


def range_report():
    print("  rate    k    t    A=k+t   H_max=A   [t+1 , A]   support[2t+2 , 2A]"
          "   floor(A/2)")
    ok = True
    expect_A = {"1/4": 261, "1/8": 133, "1/16": 67}
    for rate, (k, t) in ROWS.items():
        A = k + t
        hmin, hmax = t + 1, A          # h = A - r, r in [0, k-1]
        smin, smax = 2 * hmin, 2 * hmax
        ok &= (A == expect_A[rate])
        ok &= (hmax == A) and (hmin == t + 1)
        ok &= (smax == 2 * A) and (smax > A)          # support 2h exceeds A
        print(f"  {rate:5} {k:4} {t:4} {A:7} {A:9}   [{hmin:3},{hmax:4}]"
              f"   [{smin:4},{smax:5}]        {A // 2}")
    return ok


check("A = k+t identities and h/support ranges (H_max = A)", range_report())

# The corrected mid/large-h gap: the grammar covers t < h <= (log2 n)^2 = 100.
# Uncovered gap under the CORRECT reading h <= A is (100, A]; under the WRONG
# reading 2h <= A it would be (100, floor(A/2)].
def gap(cap_top):
    return {rate: (GRAMMAR_CAP, cap_top(k, t))
            for rate, (k, t) in ROWS.items()
            if cap_top(k, t) > GRAMMAR_CAP}


gap_correct = gap(lambda k, t: k + t)              # h <= A
gap_wrong = gap(lambda k, t: (k + t) // 2)          # 2h <= A

# Correct reading: rate 1/4 -> (100,261], rate 1/8 -> (100,133]; rate 1/16
# has A=67<100 so NO gap.  Wrong reading: only rate 1/4 -> (100,130].
ok = (
    gap_correct == {"1/4": (100, 261), "1/8": (100, 133)}
    and "1/16" not in gap_correct
    and gap_wrong == {"1/4": (100, 130)}
)
check("corrected mid/large-h gap widens (h<=A) vs the wrong 2h<=A reading", ok,
      detail=f"h<=A gap: {gap_correct}  |  2h<=A gap: {gap_wrong}")


# ======================================================================
# 2.  Finite-field construction: realise the range endpoints
# ======================================================================
# Toy row: F_p, degree-<k polynomials, k = 4, t = 2, A = 6.
P = 101
K = 4
T = 2
A = K + T          # 6
XS = list(range(1, 21))     # 20 distinct nonzero evaluation points mod p


def polyval(coeffs, x):
    """Horner over F_p; coeffs low-to-high, degree < len(coeffs)."""
    acc = 0
    for c in reversed(coeffs):
        acc = (acc * x + c) % P
    return acc


def agreement_set(y, coeffs):
    """Indices i where received y[i] == codeword value at XS[i]."""
    return {i for i, x in enumerate(XS) if y[i] == polyval(coeffs, x)}


# --- (a) distinct degree-<k codewords agree in <= k-1 points (randomised) ---
random.seed(20260704)
worst = 0
for _ in range(4000):
    f = [random.randrange(P) for _ in range(K)]
    g = [random.randrange(P) for _ in range(K)]
    if f == g:
        continue
    ag = len(agreement_set([polyval(f, x) for x in XS], g))  # where c_f == c_g
    worst = max(worst, ag)
check("distinct deg-<k codewords agree in <= k-1 points (random 4000 pairs)",
      worst <= K - 1, detail=f"max observed agreement = {worst} (k-1 = {K-1})")


# --- (b) r = 0 realisable: h = A, support 2h = 2A > A ------------------------
# f arbitrary; g = f + 1 (never agrees with f).  y = f on S_f={0..5},
# y = g on S_g={6..11}, y = f+5 elsewhere (disagrees with both).
f = [7, 3, 9, 2]                      # some degree-3 poly
g = [(f[0] + 1) % P] + f[1:]          # g = f + 1  (constant shift)
Sf_target = set(range(0, 6))
Sg_target = set(range(6, 12))
cf = [polyval(f, x) for x in XS]
cg = [polyval(g, x) for x in XS]
y = list(cf)                          # baseline
for i in range(len(XS)):
    if i in Sf_target:
        y[i] = cf[i]
    elif i in Sg_target:
        y[i] = cg[i]
    else:
        y[i] = (cf[i] + 5) % P        # != cf (diff 5), != cg (diff 4)
Sf = agreement_set(y, f)
Sg = agreement_set(y, g)
r = len(Sf & Sg)
Pset, Qset = Sf - Sg, Sg - Sf
h = len(Pset)
support = len(Pset | Qset)
ok = (
    len(Sf) == A and len(Sg) == A and r == 0
    and h == A and len(Qset) == A               # h = A - r = A
    and support == 2 * A and support > A        # support 2h = 2A exceeds A
    and not (Pset & Qset)                        # P, Q disjoint
)
check("r=0 construction: h = A and support 2h = 2A > A  (so 2h NOT <= A)", ok,
      detail=f"|S_f|={len(Sf)} |S_g|={len(Sg)} r={r} h={h} support={support} A={A}")


# --- (c) r = k-1 realisable: minimal trade h = t+1 --------------------------
# g arbitrary; f = g + (X-x0)(X-x1)(X-x2), a degree-(k-1) polynomial whose
# k-1 = 3 roots are the shared-agreement points.  f, g agree exactly there.
def poly_from_roots(roots):
    """Monic polynomial (low-to-high coeffs) with the given roots over F_p."""
    coeffs = [1]
    for rt in roots:
        new = [0] * (len(coeffs) + 1)
        for i, c in enumerate(coeffs):
            new[i] = (new[i] + c * (-rt)) % P    # * (X - rt): constant part
            new[i + 1] = (new[i + 1] + c) % P    #             X part
        coeffs = new
    return coeffs


shared_pts = [XS[0], XS[1], XS[2]]               # 3 = k-1 shared roots
diff = poly_from_roots(shared_pts)               # degree 3 = k-1 < k
g2 = [4, 8, 1, 5]                                 # some degree-3 poly, deg < k
f2 = [(g2[i] + (diff[i] if i < len(diff) else 0)) % P for i in range(max(len(g2), len(diff)))]
assert len(f2) <= K and len(g2) <= K             # both degree < k
cf2 = [polyval(f2, x) for x in XS]
cg2 = [polyval(g2, x) for x in XS]
# shared indices {0,1,2}; f-only {3,4,5}; g-only {6,7,8}; rest disagrees.
y2 = [0] * len(XS)
for i in range(len(XS)):
    if i in (0, 1, 2):
        y2[i] = cf2[i]                            # == cg2[i] there
    elif i in (3, 4, 5):
        y2[i] = cf2[i]
    elif i in (6, 7, 8):
        y2[i] = cg2[i]
    else:
        cand = (cf2[i] + 1) % P
        if cand == cg2[i]:
            cand = (cf2[i] + 2) % P
        y2[i] = cand                              # != cf2 and != cg2
Sf2 = agreement_set(y2, f2)
Sg2 = agreement_set(y2, g2)
r2 = len(Sf2 & Sg2)
P2, Q2 = Sf2 - Sg2, Sg2 - Sf2
h2 = len(P2)
ok = (
    len(Sf2) == A and len(Sg2) == A
    and r2 == K - 1                               # r = k-1 (maximal overlap)
    and h2 == T + 1 and len(Q2) == T + 1          # h = A - r = t+1 (minimal)
    and (Sf2 & Sg2) == {0, 1, 2}
)
check("r=k-1 construction: minimal trade h = t+1  (matches h = A - r)", ok,
      detail=f"|S_f|={len(Sf2)} |S_g|={len(Sg2)} r={r2}=k-1 h={h2}=t+1")


# ======================================================================
# 3.  Pinned certificate
# ======================================================================
def expected_certificate():
    def json_gap(g):
        return {rate: [lo, hi] for rate, (lo, hi) in g.items()}

    row_data = {}
    for rate, (k, t) in ROWS.items():
        Arow = k + t
        row_data[rate] = {
            "k": k,
            "t": t,
            "A": Arow,
            "H_max": Arow,
            "h_range": [t + 1, Arow],
            "support_range": [2 * (t + 1), 2 * Arow],
            "wrong_two_h_cap": Arow // 2,
        }
    return {
        "node": "h_window_derivation",
        "packet": "star_pte_support_bound",
        "status": "PROVED",
        "n": N,
        "log2n": LOG2N,
        "grammar_cap": GRAMMAR_CAP,
        "rows": row_data,
        "correct_gap": json_gap(gap_correct),
        "wrong_gap": json_gap(gap_wrong),
        "endpoint_fixture": {
            "field": "F_101",
            "k": K,
            "t": T,
            "A": A,
            "r_zero_half_size": h,
            "r_zero_support": support,
            "r_k_minus_1_half_size": h2,
            "r_k_minus_1_overlap": r2,
        },
    }


def check_certificate(cert):
    if "--write-certificate" in sys.argv:
        os.makedirs(os.path.dirname(CERT), exist_ok=True)
        with open(CERT, "w", encoding="utf-8") as fh:
            json.dump(cert, fh, indent=2, sort_keys=True)
            fh.write("\n")
        print(f"[wrote] {CERT}")
        return

    with open(CERT, "r", encoding="utf-8") as fh:
        pinned = json.load(fh)
    check("pinned certificate matches star-PTE verifier constants",
          pinned == cert, detail=CERT)


check_certificate(expected_certificate())


# ======================================================================
# 4.  Summary
# ======================================================================
npass = sum(1 for _, ok in _RESULTS if ok)
ntot = len(_RESULTS)
print(f"\n{npass}/{ntot} checks PASS")
sys.exit(0 if npass == ntot else 1)
