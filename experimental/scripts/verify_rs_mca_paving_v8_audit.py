#!/usr/bin/env python3
"""Independent pre-submission replay for RS_MCA_Paving_v8 (audit port).

Companion script of experimental/notes/audits/rs_mca_paving_v8_audit.md.
Target: experimental/RS_MCA_Paving_v8.tex, sha256
dd936a52e3cac8f96d35c9e1b0c506654053cf64e1ea302acd83a971110be60a
(the digest pinned in RS_MCA_Paving_v8_source/REPRODUCIBILITY_v8.md).

This is a port of the auditor's replay (v8 pre-submission audit,
2026-07-16), deliberately routed DIFFERENTLY from the two bundled release
scripts (verify_paving_mca_v8.py, verify_retained_bchks_v8.py):

  * binomials by Legendre prime-factorization exponents + product tree
    (never math.comb for the two large 2^21-row binomials);
  * primality by hand-rolled deterministic Miller-Rabin (fixed bases +
    fixed-seed rounds), Proth congruences re-executed, Lucas-Lehmer for
    2^127-1 hand-rolled;
  * quadratic staircase boundary re-derived by binary search AND isqrt,
    not by evaluating the printed endpoints alone;
  * base-two logarithms by a 300-bit integer shift (abs err ~1e-12),
    checked against the printed 4dp/6dp decimals at half-ulp tolerance;
  * exact rational arithmetic (fractions.Fraction) for the retained-lift
    appendix, with the RF4 sums evaluated by loop AND closed form.

Coverage (sections A-G below):
  (A) the four Proth prize rows (tex Table at L2244-2250, prop at L5065ff);
  (B) the 256-bit special row + saturation binomials (cor at L509-541);
  (B2) the two length-512 paving numerators of (2.6);
  (C) the 128-bit circle certificate rows CP1/CP2 + proved bits to 6dp
      (prop:paving-circle-certificate, L3543-3585);
  (D) the RF1-RF7 conditional retained-lift integers (cor:retained-koalabear,
      L4825-4891) -- ARITHMETIC ONLY; conditional on ass:retained-factor-lift,
      which this script does not (and cannot) discharge;
  (E) the two DP1 deployed-prefix unsafe certificates
      (prop:deployed-prefix-attacks, L2549-2588), which are covered by
      NEITHER bundled release script -- confirmed here by an independent
      route and cross-tied to the in-tree frozen floors of
      experimental/data/certificates/pf-deployed-rows/pf_deployed_rows.json;
      includes the named M31 a0 ceiling-collapse tightness check
      k(L-1)^2 < q-n (the exact condition under which the printed
      M(L_a) = L_a shortcut of eq (4.2) is valid);
  (F) the Mersenne-circle bonus rows SC4/SC5 (cor:mersenne-circle-rows,
      L3710-3719);
  (G) the five SHA-256 release digests pinned in REPRODUCIBILITY_v8.md
      against the in-tree files.

Deterministic, stdlib only, no timing, no machine-specific paths.
Exit code 0 iff every check passes.

NOT claimed: nothing here verifies the geometric proofs, the novelty
claims, the Prize criteria, or the mathematical truth or proof status of
the imported BCHKS Theorem 4.6 (see the companion note, Section 2, for
the provenance finding); section (D) verifies conditional arithmetic only.
"""

import hashlib
import json
import math
import random
import sys
from fractions import Fraction
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

OK = []
BAD = []


def check(name, cond, detail=""):
    (OK if cond else BAD).append((name, detail))
    print(("PASS " if cond else "FAIL ") + name + ((" :: " + detail) if detail else ""))


# ---------- high-precision log2 of a ratio of big ints ----------
def log2_ratio(x, y):
    """log2(x/y) to ~1e-12 absolute (300-bit shift)."""
    t = (x << 300) // y
    return math.log2(t) - 300


# ---------- primality: deterministic Miller-Rabin (fixed bases + seed) ----------
def miller_rabin(n, rounds=40):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    rng = random.Random(0xA5A5)  # fixed seed: deterministic run
    for _ in range(rounds):
        a = rng.randrange(2, n - 1)
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


# ---------- Legendre + product-tree binomial (independent of math.comb) ----------
def sieve(limit):
    bs = bytearray([1]) * (limit + 1)
    bs[0:2] = b"\x00\x00"
    for i in range(2, math.isqrt(limit) + 1):
        if bs[i]:
            bs[i * i::i] = b"\x00" * len(bs[i * i::i])
    return [i for i in range(limit + 1) if bs[i]]


def legendre_exponent(P, n, a):
    b = n - a
    e = 0
    pk = P
    while pk <= n:
        e += n // pk - a // pk - b // pk
        pk *= P
    return e


def product_tree(factors):
    if not factors:
        return 1
    while len(factors) > 1:
        nxt = []
        for i in range(0, len(factors) - 1, 2):
            nxt.append(factors[i] * factors[i + 1])
        if len(factors) % 2:
            nxt.append(factors[-1])
        factors = nxt
    return factors[0]


_PRIMES = None


def legendre_comb(n, a):
    global _PRIMES
    if _PRIMES is None or _PRIMES[-1] < n:
        _PRIMES = sieve(n)
    facs = []
    for P in _PRIMES:
        if P > n:
            break
        e = legendre_exponent(P, n, a)
        if e:
            facs.append(P ** e)
    return product_tree(facs)


def ceil_div(x, y):
    return -((-x) // y)


# small cross-checks of legendre_comb against math.comb (small cells only)
for (n_, a_) in ((512, 33), (512, 52), (512, 65), (512, 157), (200, 71), (1000, 313)):
    check("legendre_comb(%d,%d) == math.comb" % (n_, a_),
          legendre_comb(n_, a_) == math.comb(n_, a_))

print("\n===== (A) FOUR PROTH PRIZE ROWS =====")
K40 = 1 << 40
rows = (
    ("1/2", 41, 389500552609,
     132540169958804033333249306710494641010898987122689, 92,
     26766274163673319604503, 3, 167, 5154112775168, -663955886271,
     1381541083842484386787422633985),
    ("1/4", 42, 1210584858040,
     411940680852499481698306614369841346700408394874881, 93,
     41595378994516821279015, 13, 169, 7590647904465, -3182321912768,
     2921538492713497448761933168641),
    ("1/8", 43, 2879806199253,
     979947269755402568812854322316630667196565607677953, 95,
     24737346889219389259839, 5, 170, 13908181940112, -6720484728007,
     2495687119199326634196634435585),
    ("1/16", 44, 6233898019554,
     2121285573237585848299875619011192262679065433997313, 97,
     13387194060291799253121, 5, 171, 19335616403905, -20973145690236,
     20440865928680199099134339186689),
)
for (rho, e, B, p, s, u, a0w, bits, fl, fr, rem) in rows:
    n = 1 << e
    check("[%s] p = u*2^s+1, u odd, u<2^s" % rho,
          p == u * (1 << s) + 1 and u % 2 == 1 and u < (1 << s))
    check("[%s] Proth witness %d^((p-1)/2) = -1 mod p" % (rho, a0w),
          pow(a0w, (p - 1) // 2, p) == p - 1)
    check("[%s] p prime (MR40, fixed-seed)" % rho, miller_rabin(p))
    check("[%s] bits(p) = %d" % (rho, bits), p.bit_length() == bits)
    check("[%s] p < 2^256" % rho, p < 1 << 256)
    check("[%s] n | p-1" % rho, (p - 1) % n == 0)
    q_, r_ = divmod(p, 1 << 128)
    check("[%s] floor(p/2^128) = %d" % (rho, B), q_ == B)
    check("[%s] remainder matches" % rho, r_ == rem and 0 < r_ < (1 << 128))
    R = n - K40
    F = lambda r: r * r - n * (3 * r - R)
    check("[%s] F(B-1) = %d >= 0" % (rho, fl), F(B - 1) == fl and fl >= 0)
    check("[%s] F(B) = %d < 0" % (rho, fr), F(B) == fr and fr < 0)
    # independent boundary route 1: binary search on the decreasing branch
    lo, hi = 0, 3 * n // 2
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if F(mid) >= 0:
            lo = mid
        else:
            hi = mid - 1
    check("[%s] binary-search r_quad = B-1" % rho, lo == B - 1,
          "r_quad=%d, B-1=%d" % (lo, B - 1))
    # independent boundary route 2: isqrt closed form with exact adjustment
    Dq = n * (5 * n + 4 * K40)
    sq = math.isqrt(Dq)
    if sq * sq == Dq:
        rq = (3 * n - sq) // 2
    else:
        cand = (3 * n - sq) // 2
        while F(cand) < 0:
            cand -= 1
        while F(cand + 1) >= 0:
            cand += 1
        rq = cand
    check("[%s] isqrt r_quad = B-1" % rho, rq == B - 1)

print("\n===== (B) 256-BIT SPECIAL ROW + SATURATION BINOMIALS =====")
TWO128 = 1 << 128
ps = (TWO128 - 255) * TWO128 + 1
check("special p = (2^128-255)*2^128+1 Proth decomp",
      ps == (TWO128 - 255) * (1 << 128) + 1
      and (TWO128 - 255) % 2 == 1 and (TWO128 - 255) < (1 << 128))
check("special Proth witness 3", pow(3, (ps - 1) // 2, ps) == ps - 1)
check("special p prime (MR40, fixed-seed)", miller_rabin(ps))
check("special p is 256-bit, < 2^256", ps.bit_length() == 256 and ps < (1 << 256))
check("special budget floor(p/2^128) = 2^128-255",
      ps // TWO128 == TWO128 - 255 and ps % TWO128 == 1)
check("order-512 subgroup exists (512 | p-1)", (ps - 1) % 512 == 0)
check("order-128 subgroup exists (128 | p-1)", (ps - 1) % 128 == 0)
sat = {64: 23582666872052266206656578733667004800,
       32: 4299074680733907393985381161600,
       16: 614965786737727286400,
       8: 19062702032000}
for kk, v in sat.items():
    c = legendre_comb(128, kk + 1)
    check("C(128,%d) = printed" % (kk + 1), c == v, str(c))
    check("C(128,%d) <= budget" % (kk + 1), c <= TWO128 - 255)

print("\n===== (B2) LENGTH-512 PAVING ROWS (2.6) =====")
r26 = ((32, 52, 210954686508560867421211382134708972291),
       (64, 158, 275511258760747555342982982548156580976))
for kk, aa, printed in r26:
    num = legendre_comb(512, kk + 1)
    den = legendre_comb(aa - 1, kk)
    val = min(legendre_comb(512, aa), num // den)
    check("(2.6) k=%d,a=%d: floor(C(512,%d)/C(%d,%d)) = printed"
          % (kk, aa, kk + 1, aa - 1, kk), num // den == printed, str(num // den))
    check("(2.6) k=%d,a=%d: min with C(512,a) does not bind" % (kk, aa),
          val == printed)
    check("(2.6) k=%d,a=%d <= budget 2^128-255" % (kk, aa), printed <= TWO128 - 255)
    check("(2.6) k=%d,a=%d beyond Johnson k*n > a^2" % (kk, aa),
          kk * 512 > aa * aa, "%d > %d" % (kk * 512, aa * aa))

print("\n===== (C) CIRCLE ROWS (CP1/CP2 + PROVED BITS 6dp) =====")


def lucas_lehmer(pexp):
    M = (1 << pexp) - 1
    v = 4
    for _ in range(pexp - 2):
        v = (v * v - 2) % M
    return v == 0


p0 = (1 << 127) - 1
check("Lucas-Lehmer(2^127-1)", lucas_lehmer(127))
check("2^127-1 prime (MR40, fixed-seed)", miller_rabin(p0))
check("512 | p0+1", (p0 + 1) % 512 == 0)
qc = p0 * p0
bud_c = qc // TWO128
check("circle budget floor(q/2^128)",
      bud_c == 85070591730234615865843651857942052863, str(bud_c))
check("circle budget == 2^126 - 1", bud_c == (1 << 126) - 1)
crows = ((32, 53, 81136417887908025931235146974888066266, "128.068311"),
         (31, 50, 60827291905480389917403158602781524185, "128.483942"))
for kk, aa, printed, pbits in crows:
    num = legendre_comb(512, kk + 1)
    den = legendre_comb(aa - 1, kk)
    v = num // den
    check("circle k=%d,a=%d: floor(C(512,%d)/C(%d,%d)) = printed"
          % (kk, aa, kk + 1, aa - 1, kk), v == printed, str(v))
    check("circle k=%d,a=%d: min with C(512,%d) does not bind" % (kk, aa, aa),
          legendre_comb(512, aa) > v)
    check("circle k=%d,a=%d <= circle budget" % (kk, aa), v <= bud_c)
    check("circle k=%d,a=%d beyond Johnson" % (kk, aa),
          kk * 512 > aa * aa, "%d > %d" % (kk * 512, aa * aa))
    bits = log2_ratio(qc, v)
    check("circle k=%d proved bits %s (6dp)" % (kk, pbits),
          abs(bits - float(pbits)) < 0.5e-6, "computed %.9f" % bits)

print("\n===== (D) RF1-RF7 CONDITIONAL RETAINED-LIFT APPENDIX =====")
print("NOTE: arithmetic only; conditional on ass:retained-factor-lift,")
print("      which this script does not discharge (paper says the same).")
pKB = (1 << 31) - (1 << 24) + 1
check("p_KB = 127*2^24+1", pKB == 127 * (1 << 24) + 1)
check("p_KB Proth witness 3", pow(3, (pKB - 1) // 2, pKB) == pKB - 1)
check("p_KB prime (MR40, fixed-seed)", miller_rabin(pKB))
qKB = pKB ** 6
n21 = 1 << 21
check("2^21 | p_KB - 1", (pKB - 1) % n21 == 0)
budKB = qKB >> 128
check("KB budget floor(q/2^128) = 274980728111395087",
      budKB == 274980728111395087, str(budKB))
tiny = Fraction(1, 1 << 64)
rf = (
    ("1/2", 611982, 119, 176735230, 169, 27525, 4889934,
     152123705899212, 574462, 274589064742726105, "128.002056", "38.706920"),
    ("1/4", 1045433, 104, 109378776, 209, 29028, 13182624,
     113730027157979, 326872, 274721012201264929, "128.001363", "37.935074"),
    ("1/8", 1352390, 90, 67028580, 256, 31500, 11133440,
     63736189920080, 181860, 274578888391530706, "128.002110", "37.562917"),
    ("1/16", 1569744, 78, 41137824, 314, 34101, 4204064,
     32093320774290, 112288, 274861787390229386, "128.000624", "37.349385"),
)
for (rho, r, m, U, V, W, rf4m, rf2m, rankm, Rret, pbits, pgap) in rf:
    Kdim = n21 // {"1/2": 2, "1/4": 4, "1/8": 8, "1/16": 16}[rho]
    A = n21 - r
    check("RF[%s] U = m*A" % rho, U == m * A, "%d*%d=%d" % (m, A, m * A))
    check("RF[%s] V>=m, W>=V" % rho, V >= m and W >= V)
    check("RF[%s] U-K(V-1) = %d > 0" % (rho, rankm),
          U - Kdim * (V - 1) == rankm and rankm > 0, str(U - Kdim * (V - 1)))
    check("RF[%s] char > V-1" % rho, pKB > V - 1)
    top = (A - Kdim - 1) * (2 * U - 1) - (n21 - Kdim - 1) * (2 * Kdim + 1)
    check("RF[%s] RF2 top margin = %d > 0" % (rho, rf2m),
          top == rf2m and top > 0, str(top))
    DY = Fraction(V - 1) + tiny
    DZ = Fraction(W - 1) + tiny
    DX = Fraction(U - 1) + tiny
    check("RF[%s] D_X < mA with margin 1-2^-64" % rho,
          Fraction(m * A) - DX == 1 - tiny)
    check("RF[%s] q > 2*U*D_Y" % rho, Fraction(qKB) > 2 * U * DY)
    lhs = sum((U - Kdim * j) * (W - j) for j in range(V))
    rhs = n21 * sum((W - s2) * (m - s2) for s2 in range(m))
    lhs_cf = U * W * V - (U + Kdim * W) * (V - 1) * V // 2 \
        + Kdim * (V - 1) * V * (2 * V - 1) // 6
    rhs_cf = n21 * (W * m * m - (W + m) * (m - 1) * m // 2
                    + (m - 1) * m * (2 * m - 1) // 6)
    check("RF[%s] RF4 closed-form == loop" % rho, lhs == lhs_cf and rhs == rhs_cf)
    check("RF[%s] RF4 margin = %d > 0" % (rho, rf4m),
          lhs - rhs == rf4m and rf4m > 0, str(lhs - rhs))
    thr = 2 * U * DY * DY * DZ + (r + 1) * DY
    ret = ceil_div(thr.numerator, thr.denominator)
    check("RF[%s] RF5 retained numerator = %d" % (rho, Rret), ret == Rret, str(ret))
    check("RF[%s] retained <= budget" % rho, ret <= budKB,
          "slack %d" % (budKB - ret))
    bits = log2_ratio(qKB, ret)
    gap = log2_ratio(ret, r + 1)
    check("RF[%s] security bits %s" % (rho, pbits),
          abs(bits - float(pbits)) < 0.5e-6, "%.9f" % bits)
    check("RF[%s] tangent gap %s" % (rho, pgap),
          abs(gap - float(pgap)) < 0.5e-6, "%.9f" % gap)

print("\n===== (E) DP1 DEPLOYED-PREFIX UNSAFE CERTIFICATES =====")
print("NOTE: prop:deployed-prefix-attacks (tex L2549-2588) is covered by")
print("      NEITHER bundled release script; this section closes that gap.")
kdim = 1 << 20


def dp1_row(name, pbase, ext, a0, Bstar_claim, M0_claim, M1_claim,
            target_bits, margin_claim):
    q = pbase ** ext
    Bstar = q >> target_bits
    check("DP1[%s] B* = floor(q/2^%d) = %d" % (name, target_bits, Bstar_claim),
          Bstar == Bstar_claim, str(Bstar))
    out = {}
    for (a, claim, tag) in ((a0, M0_claim, "a0"), (a0 + 1, M1_claim, "a0+1")):
        w = a - kdim - 1
        Cna = legendre_comb(n21, a)
        pw = pbase ** w
        L = ceil_div(Cna, pw)
        denom = (q - n21) + kdim * (L - 1)
        M = ceil_div(L * (q - n21), denom)
        check("DP1[%s] %s: M(L_%d) = %d" % (name, tag, a, claim), M == claim,
              "L=%d, M=%d" % (L, M))
        # exact collapse condition: M == L  <=>  k(L-1)^2 < q-n
        # (since (L-1)*(q-n+k(L-1)) < L*(q-n) <=> k(L-1)^2 < q-n)
        collapse = kdim * (L - 1) ** 2 < q - n21
        check("DP1[%s] %s: ceiling collapse M == L matches k(L-1)^2 < q-n"
              % (name, tag), (M == L) == collapse,
              "k(L-1)^2=%.4e, q-n=%.4e" % (kdim * (L - 1) ** 2, q - n21))
        out[tag] = (L, M, kdim * (L - 1) ** 2, q - n21)
    M0 = out["a0"][1]
    M1 = out["a0+1"][1]
    check("DP1[%s] M(L_a0) > B* (unsafe)" % name, M0 > Bstar)
    check("DP1[%s] M(L_a0+1) < B* (below budget one later)" % name, M1 < Bstar)
    marg = log2_ratio(M0, Bstar)
    check("DP1[%s] pass margin log2(M/B*) rounds to %.4f (4dp)"
          % (name, margin_claim), abs(marg - margin_claim) < 0.5e-4,
          "computed %.7f" % marg)
    return out, log2_ratio(Bstar, M1), marg


kb_out, kb_fail, kb_pass = dp1_row(
    "KB p^6", pKB, 6, 1116047, 274980728111395087,
    138634741058327852652, 57198030366, 128, 8.9777)
m31p = (1 << 31) - 1
m31_out, m31_fail, m31_pass = dp1_row(
    "M31 (2^31-1)^4", m31p, 4, 1116023, 16777215,
    4281388998575706, 1752700, 100, 27.9270)
check("DP1 radius row1: n - a0 = 981105", n21 - 1116047 == 981105)
check("DP1 radius row2: n - a0 = 981129", n21 - 1116023 == 981129)

# ---- NAMED CHECK: M31 a0 ceiling-collapse tightness (~10% headroom) ----
lhs_c, rhs_c = m31_out["a0"][2], m31_out["a0"][3]
check("M31-A0-CEILING-COLLAPSE-INEQUALITY k(L-1)^2 < q-n (TIGHT: ~10 percent headroom)",
      lhs_c < rhs_c,
      "k(L-1)^2 = %.4e < q-n = %.4e (ratio %.4f); any re-tuned deeper radius "
      "must re-verify this, not assume M = L" % (lhs_c, rhs_c, lhs_c / rhs_c))
lhs_k, rhs_k = kb_out["a0"][2], kb_out["a0"][3]
check("KB a0 ceiling-collapse inequality k(L-1)^2 < q-n (comfortable)",
      lhs_k < rhs_k, "%.4e < %.4e (ratio %.2e)" % (lhs_k, rhs_k, lhs_k / rhs_k))

# ---- cross-route tie: derive the M31 a0 binomial from the KB a0 binomial ----
Ckb = legendre_comb(n21, 1116047)
Cd = Ckb
steps_exact = True
for a in range(1116047, 1116023, -1):
    numr = Cd * a
    if numr % (n21 - a + 1) != 0:
        steps_exact = False
        break
    Cd = numr // (n21 - a + 1)
check("cross-route: C(n,1116023) from C(n,1116047) by 24 exact ratio steps",
      steps_exact and Cd == legendre_comb(n21, 1116023))
check("C(n,1116047) bit_length == 2090874 (ties to the audit's math.comb route)",
      Ckb.bit_length() == 2090874)

# ---- three-way tie: in-tree frozen floors (pf-deployed-rows certificate) ----
cert_rel = "experimental/data/certificates/pf-deployed-rows/pf_deployed_rows.json"
cert_path = REPO_ROOT / cert_rel
if cert_path.is_file():
    cert = json.loads(cert_path.read_text(encoding="utf-8"))
    frozen = cert["rows"]
    check("frozen floors: kb_mca a0/a1 L_floor match this replay",
          int(frozen["kb_mca"]["charts"]["a0"]["L_floor"]) == kb_out["a0"][0]
          and int(frozen["kb_mca"]["charts"]["a1"]["L_floor"]) == kb_out["a0+1"][0])
    check("frozen floors: m31_mca a0/a1 L_floor match this replay",
          int(frozen["m31_mca"]["charts"]["a0"]["L_floor"]) == m31_out["a0"][0]
          and int(frozen["m31_mca"]["charts"]["a1"]["L_floor"]) == m31_out["a0+1"][0])
    check("frozen margins: kb_mca +8.9777 / -22.1969 match this replay (4dp)",
          abs(float(frozen["kb_mca"]["pass_margin_bits_a0"]) - kb_pass) < 0.5e-4
          and abs(float(frozen["kb_mca"]["fail_margin_bits_a1"]) + kb_fail) < 0.5e-4)
    check("frozen margins: m31_mca +27.9270 / -3.2589 match this replay (4dp)",
          abs(float(frozen["m31_mca"]["pass_margin_bits_a0"]) - m31_pass) < 0.5e-4
          and abs(float(frozen["m31_mca"]["fail_margin_bits_a1"]) + m31_fail) < 0.5e-4)
else:
    check("frozen floors certificate present (%s)" % cert_rel, False)

print("\n===== (F) MERSENNE-CIRCLE BONUS ROWS SC4/SC5 =====")
Bm = (m31p ** 5) >> 128
check("mersenne-circle budget floor(p^5/2^128) = 2^27-1", Bm == (1 << 27) - 1,
      str(Bm))
sc_rows = (("SC4", 1 << 30, (1 << 29) + 1, 162129591417176068),
           ("SC5", 1 << 29, 1 << 27, 18014401193836548))
for tag, nn, kk, printed in sc_rows:
    rr = Bm - 1
    marg = (nn - rr) ** 2 - nn * (kk + rr)
    check("%s quadratic margin (n-r)^2 - n(k+r) = %d > 0" % (tag, printed),
          marg == printed and marg > 0, str(marg))
check("SC4 endpoint identity 1/8 - 2^-30 = B/2^30",
      Fraction(1, 8) - Fraction(1, 1 << 30) == Fraction(Bm, 1 << 30))
check("SC5 endpoint identity 1/4 - 2^-29 = B/2^29",
      Fraction(1, 4) - Fraction(1, 1 << 29) == Fraction(Bm, 1 << 29))

print("\n===== (G) RELEASE SHA-256 DIGESTS (REPRODUCIBILITY_v8.md pins) =====")
PINS = {
    "experimental/RS_MCA_Paving_v8.tex":
        "dd936a52e3cac8f96d35c9e1b0c506654053cf64e1ea302acd83a971110be60a",
    "experimental/RS_MCA_Paving_v8.pdf":
        "5a7bcc58e926a2f74c0b6014ad65247e9af1761ef5fdbcf3e08867f3637309c3",
    "experimental/RS_MCA_Paving_v8_source/verify_paving_mca_v8.py":
        "8193c388aeccd92bf7b610fa6747de67d91cab6b56621eabd91ed70e0884f8bf",
    "experimental/RS_MCA_Paving_v8_source/verify_retained_bchks_v8.py":
        "af01479e58cfbf371fea211eacb6ff882fed8ac08967043158e88dd5a79a4da8",
    "experimental/RS_MCA_Paving_v8_source/AI_USE_v8.md":
        "58f8d772f7c61f723ff570425bf04499e4ca769180930e06375d487fdcb14e15",
}
for rel, digest in PINS.items():
    fp = REPO_ROOT / rel
    if fp.is_file():
        h = hashlib.sha256(fp.read_bytes()).hexdigest()
        check("sha256 %s" % rel, h == digest, h[:16] + "...")
    else:
        check("release file present: %s" % rel, False)
texA = REPO_ROOT / "experimental/RS_MCA_Paving_v8.tex"
texB = REPO_ROOT / "experimental/RS_MCA_Paving_v8_source/RS_MCA_Paving_v8.tex"
check("both tex copies byte-identical",
      texA.is_file() and texB.is_file() and texA.read_bytes() == texB.read_bytes())

print("\n===== SUMMARY =====")
print("%d passed, %d FAILED" % (len(OK), len(BAD)))
for name, det in BAD:
    print("FAILED:", name, det)
sys.exit(1 if BAD else 0)
