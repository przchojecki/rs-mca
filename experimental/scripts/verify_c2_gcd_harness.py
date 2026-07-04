#!/usr/bin/env python3
"""C2 GCD-test harness + verifier for the (A)-closure good-reduction lemma.

This single file is BOTH:

  * the (C2) certification HARNESS -- consumes a certificate of cleared-
    obstruction / RUR exceptional integers D(n,h) (schema below) together
    with a list of official row primes, runs the divisibility tests
    gcd(D(n,h), p), and emits a machine-checkable per-row certificate; and

  * its own VERIFIER -- a SELF-TEST that reconstructs the exceptional set
    {7, 17, 97} at (n,h) = (16,3) exactly (the toy validation set of the A3
    good-reduction lemma), cross-checked two independent ways, plus the
    Task-1 h-window arithmetic checks.  Default (no args) runs the verifier
    and prints PASS/FAIL per section.

Companions:
  * experimental/notes/roadmaps/c2_gcd_harness.md        (schema + usage)
  * experimental/notes/roadmaps/a3_good_reduction_lemma.md (Theorem A3, D(n,h))
  * experimental/notes/roadmaps/a_closure_assembly.md      ((C1)/(C2) inputs)
  * experimental/notes/roadmaps/h_window_derivation_audit.md (the h cap)

Harness mode:
  python3 verify_c2_gcd_harness.py --cert D.json --rowspec rows.json --out result.json

Verifier mode (self-test + Task-1 checks):
  python3 verify_c2_gcd_harness.py

Pure stdlib (itertools, json, math, argparse, time).  No third-party deps.
"""

import argparse
import itertools
import json
import os
import sys
import time
from fractions import Fraction
from math import gcd

# ======================================================================
# 0.  PASS/FAIL bookkeeping
# ======================================================================

_RESULTS = []

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
SELFTEST_CERT = os.path.join(
    REPO,
    "experimental",
    "data",
    "certificates",
    "c2-gcd-harness",
    "c2_gcd_harness_selftest.json",
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
# 1.  THE HARNESS CORE  --  gcd(D(n,h), p) divisibility tests
# ======================================================================
#
# Certificate schema  "c2-gcd-certificate/v1":
#   {
#     "schema": "c2-gcd-certificate/v1",
#     "n": 16,
#     "definition": "D_pt(ideal-norm)"  |  "D_rur",
#     "provenance": "...free text...",
#     "entries": [
#        { "h": 3,
#          "D": "<decimal string of the ODD integer D(n,h)>",
#          "D_is_odd": true,
#          # OPTIONAL, present for RUR-route certs (A3 note sec 3.2); if
#          # present the harness cross-checks D == oddpart(product):
#          "rur_factors": {
#             "delta_0": "..", "delta_i": ["..",..], "e_j": ["..",..],
#             "e_u": "..", "Delta_m": "..", "lc_m": ".." }
#        }, ... ]
#   }
#
# Row-spec schema  "c2-row-spec/v1":
#   {
#     "schema": "c2-row-spec/v1",
#     "n": 16,
#     "H_max_mode": "agreement_A" | "grammar_sq" | "two_log2" | "explicit",
#     "H_max": 100,                 # only for mode "explicit"
#     "rows": [
#        { "label": "..", "p": 17, "q_form": "p",  "t": 3, "A": 67 },
#        { "label": "..", "p": 7,  "q_form": "p2", "t": 3, "A": 67 }, ...]
#   }
#   q_form "p"  => q = p     (row exists iff n | p-1,   A3 case f=1);
#   q_form "p2" => q = p^2   (row exists iff n | p^2-1, A3 case f in {1,2}).
#
# Result schema  "c2-gcd-result/v1": see emit_result() below.


def oddpart(m):
    m = abs(int(m))
    if m == 0:
        return 0
    while m % 2 == 0:
        m //= 2
    return m


def row_is_valid(n, p, q_form):
    """A3 split-behaviour: q = p needs n | p-1; q = p^2 needs n | p^2-1."""
    if q_form == "p":
        return (p - 1) % n == 0
    if q_form == "p2":
        return (p * p - 1) % n == 0
    raise ValueError(f"unknown q_form {q_form!r} (expect 'p' or 'p2')")


def window_for_row(n, row, mode, explicit_hmax=None):
    """Return [t+1, H_max] as an inclusive integer window, or None to test
    every h present in the certificate (used when t/A are absent, e.g. the
    toy (16,3) validation which is a bare (n,h) pair, not a rate row)."""
    t = row.get("t")
    if t is None:
        return None
    log2n = n.bit_length() - 1            # n is a power of two
    if mode == "two_log2":
        hmax = 2 * log2n
    elif mode == "grammar_sq":
        hmax = log2n * log2n
    elif mode == "agreement_A":
        hmax = row.get("A")
        if hmax is None:
            raise ValueError("mode 'agreement_A' needs 'A' in the row")
    elif mode == "explicit":
        if explicit_hmax is None:
            raise ValueError("mode 'explicit' needs top-level 'H_max'")
        hmax = explicit_hmax
    else:
        raise ValueError(f"unknown H_max_mode {mode!r}")
    return (t + 1, hmax)


def load_certificate(path):
    with open(path) as fh:
        cert = json.load(fh)
    if cert.get("schema") != "c2-gcd-certificate/v1":
        raise ValueError(f"bad cert schema: {cert.get('schema')!r}")
    n = int(cert["n"])
    entries = {}
    for e in cert["entries"]:
        h = int(e["h"])
        D = int(e["D"])
        if e.get("D_is_odd", True) and D % 2 == 0:
            raise ValueError(f"entry h={h}: D advertised odd but is even")
        # optional RUR cross-check
        rf = e.get("rur_factors")
        if rf is not None:
            prod = int(rf.get("delta_0", 1))
            for v in rf.get("delta_i", []):
                prod *= int(v)
            for v in rf.get("e_j", []):
                prod *= int(v)
            prod *= int(rf.get("e_u", 1))
            prod *= int(rf.get("Delta_m", 1))
            prod *= int(rf.get("lc_m", 1))
            if oddpart(prod) != oddpart(D):
                raise ValueError(
                    f"entry h={h}: D != oddpart(product of rur_factors)")
        entries[h] = D
    return n, entries, cert.get("definition", ""), cert.get("provenance", "")


def load_rowspec(path):
    with open(path) as fh:
        spec = json.load(fh)
    if spec.get("schema") != "c2-row-spec/v1":
        raise ValueError(f"bad rowspec schema: {spec.get('schema')!r}")
    return spec


def run_harness(n, entries, rowspec):
    """Core (C2) test.  For each row and each window-h present in the
    certificate, test gcd(D(n,h), p).  gcd > 1 == a window-h exceptional
    divisibility (a candidate real trade / at worst a spurious factor to be
    recounted, per A3 sec.4).  Returns the result dict."""
    if int(rowspec["n"]) != n:
        raise ValueError("cert n and rowspec n disagree")
    mode = rowspec.get("H_max_mode", "agreement_A")
    explicit_hmax = rowspec.get("H_max")
    cert_hs = sorted(entries)
    out_rows = []
    exceptional_primes = set()
    n_pass = n_fail = 0
    for row in rowspec["rows"]:
        p = int(row["p"])
        q_form = row["q_form"]
        valid = row_is_valid(n, p, q_form)
        win = window_for_row(n, row, mode, explicit_hmax)
        if win is None:
            hs = list(cert_hs)
        else:
            lo, hi = win
            hs = [h for h in cert_hs if lo <= h <= hi]
        exc = []
        if valid:
            for h in hs:
                g = gcd(entries[h], p)
                if g > 1:
                    exc.append({"h": h, "prime": p, "divisor": g})
                    exceptional_primes.add(p)
        verdict = "SKIP" if not valid else ("FAIL" if exc else "PASS")
        if valid and exc:
            n_fail += 1
        elif valid:
            n_pass += 1
        out_rows.append({
            "label": row.get("label", ""),
            "p": p,
            "q_form": q_form,
            "q": p if q_form == "p" else p * p,
            "row_valid": valid,
            "window": list(win) if win else None,
            "h_tested": hs,
            "verdict": verdict,
            "exceptional": exc,
        })
    return {
        "schema": "c2-gcd-result/v1",
        "n": n,
        "H_max_mode": mode,
        "rows": out_rows,
        "summary": {
            "rows_valid_pass": n_pass,
            "rows_valid_fail": n_fail,
            "exceptional_primes": sorted(exceptional_primes),
        },
    }


# ======================================================================
# 2.  TOY D(16,3) computed DIRECTLY  (self-test input)
# ======================================================================
#
# Ports the x83 obstruction recursion into exact Z[zeta_16] arithmetic
# (basis 1,y,..,y^7 ; y^8 = -1), forms the two cleared obstructions
# O_1^cl, O_2^cl = 2^(4h-2) O_j of A3 sec 3.1, and defines
#
#   D_pt(16,3) = ODD PART of  prod_{R}  N(a(R)),
#       a(R) = ideal (O_1^cl(R), O_2^cl(R)) in Z[zeta_16],
#       N(a(R)) = [Z[zeta_16] : a(R)]  (lattice index),
#
# the product over the C(15,5)=3003 ANCHORED 6-subsets R (1 in R) of
# mu_16 (all of which are non-candidates: X24 => zero char-0 (16,3)
# candidates since 3 is not a 2-power).  A prime p divides N(a(R)) iff
# both cleared obstructions land in a common prime of Z[zeta_16] over p,
# i.e. iff there is an EXTRA anchored mod-p candidate at R -- exactly the
# exceptional condition.  So supp(D_pt) is the exceptional-prime set.

DEG = 8            # [Q(zeta_16):Q]
CLEAR = 2 ** 10    # 2^(4h-2), h = 3


def _zmulF(a, b):
    out = [Fraction(0)] * DEG
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j, bj in enumerate(b):
            if bj == 0:
                continue
            k = i + j
            if k >= DEG:
                out[k - DEG] -= ai * bj
            else:
                out[k] += ai * bj
    return out


def _zaddF(a, b):
    return [x + y for x, y in zip(a, b)]


def _zsubF(a, b):
    return [x - y for x, y in zip(a, b)]


def _zscaleF(a, r):
    return [x * r for x in a]


def _zeta_powF(k):
    k %= 16
    v = [Fraction(0)] * DEG
    if k < DEG:
        v[k] = Fraction(1)
    else:
        v[k - DEG] = Fraction(-1)
    return v


_ZEROF = [Fraction(0)] * DEG
_ONEF = _zeta_powF(0)


def _poly_from_roots(exps):
    coeffs = [_ONEF[:]]
    for e in exps:
        r = _zeta_powF(e)
        new = [_ZEROF[:] for _ in range(len(coeffs) + 1)]
        for i, ci in enumerate(coeffs):
            new[i + 1] = _zaddF(new[i + 1], ci)
            new[i] = _zsubF(new[i], _zmulF(r, ci))
        coeffs = new
    return coeffs


def cleared_obstructions_16_3(exps):
    """Return (O1cl, O2cl) as integer ring-vectors (length 8)."""
    C = _poly_from_roots(exps)
    c = {j: C[j] for j in range(6)}
    half = Fraction(1, 2)
    s2 = _zscaleF(c[5], half)
    s1 = _zscaleF(_zsubF(c[4], _zmulF(s2, s2)), half)
    s0 = _zscaleF(_zsubF(c[3], _zscaleF(_zmulF(s2, s1), 2)), half)
    O2 = _zsubF(_zaddF(_zmulF(s1, s1), _zscaleF(_zmulF(s2, s0), 2)), c[2])
    O1 = _zsubF(_zscaleF(_zmulF(s1, s0), 2), c[1])

    def clr(v):
        out = []
        for x in v:
            y = x * CLEAR
            assert y.denominator == 1, "Lemma-2 integrality violated"
            out.append(int(y))
        return out
    return clr(O1), clr(O2)


def _zmul_zeta(vec, shift):
    """integer vector * zeta_16^shift in the ring."""
    r = [0] * DEG
    if shift < DEG:
        r[shift] = 1
    else:
        r[shift - DEG] = -1
    out = [0] * DEG
    for i, ai in enumerate(vec):
        if ai == 0:
            continue
        for j, bj in enumerate(r):
            if bj == 0:
                continue
            k = i + j
            if k >= DEG:
                out[k - DEG] -= ai * bj
            else:
                out[k] += ai * bj
    return out


def _ext_gcd(a, b):
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    if old_r < 0:
        old_r, old_s, old_t = -old_r, -old_s, -old_t
    return old_r, old_s, old_t


def lattice_index(vectors, dim=DEG):
    """[Z^dim : L], L = integer row-span of `vectors` (0 if rank < dim).

    Integer HNF: keep one pivot per column whose leading nonzero sits at
    that column and which is zero in all earlier columns; index = product
    of the diagonal pivots."""
    pivots = [None] * dim
    for v in vectors:
        v = list(v)
        c = 0
        while c < dim:
            if v[c] == 0:
                c += 1
                continue
            if pivots[c] is None:
                if v[c] < 0:
                    v = [-x for x in v]
                pivots[c] = v
                v = None
                break
            b = pivots[c]
            g, s, t = _ext_gcd(b[c], v[c])
            nb = [s * bi + t * vi for bi, vi in zip(b, v)]  # leading = g
            k1 = v[c] // g
            k2 = b[c] // g
            v = [k2 * vi - k1 * bi for bi, vi in zip(b, v)]  # col c -> 0
            pivots[c] = nb
            c += 1
    if any(pivots[c] is None for c in range(dim)):
        return 0
    idx = 1
    for c in range(dim):
        idx *= abs(pivots[c][c])
    return idx


def anchored_supports_16_3():
    for rest in itertools.combinations(range(1, 16), 5):
        yield (0,) + rest


def compute_toy_D_16_3():
    """D_pt(16,3) as the odd part of prod_R N(a(R)).  Also returns the
    per-support Lemma-2 integrality flag and the char-0 candidate count."""
    D = 1
    integral_ok = True
    char0 = 0
    for exps in anchored_supports_16_3():
        i1, i2 = cleared_obstructions_16_3(exps)
        if all(x == 0 for x in i1) and all(x == 0 for x in i2):
            char0 += 1
        gens = []
        for sh in range(DEG):
            gens.append(_zmul_zeta(i1, sh))
            gens.append(_zmul_zeta(i2, sh))
        o = oddpart(lattice_index(gens))
        if o > 1:
            D *= o
    return D, integral_ok, char0


# ======================================================================
# 3.  INDEPENDENT pointwise cross-check  (a(R) subset P)
# ======================================================================
# Ported from verify_a3_good_reduction.py: a prime p (with 16 | q-1) is
# exceptional iff SOME anchored support R and SOME primitive 16th root w
# in F_q kill both cleared obstructions.  This is the same predicate as
# "p | D_pt" but computed by direct evaluation, giving a second witness.


class _GF2:
    """F_{p^2} = F_p[t]/(t^2 - d), d a nonresidue."""

    def __init__(self, p):
        self.p = p
        d = 2
        while pow(d, (p - 1) // 2, p) != p - 1:
            d += 1
        self.d = d

    def mul(self, x, y):
        p, d = self.p, self.d
        a, b = x
        c, e = y
        return ((a * c + d * b * e) % p, (a * e + b * c) % p)

    def add(self, x, y):
        p = self.p
        return ((x[0] + y[0]) % p, (x[1] + y[1]) % p)

    def pw(self, x, k):
        r = (1, 0)
        while k:
            if k & 1:
                r = self.mul(r, x)
            x = self.mul(x, x)
            k >>= 1
        return r

    def order16_element(self):
        p, q = self.p, self.p * self.p
        for a in range(1, p):
            for b in range(1, p):
                x = self.pw((a, b), (q - 1) // 16)
                if self.pw(x, 8) != (1, 0) and self.pw(x, 16) == (1, 0):
                    return x
        raise RuntimeError("no order-16 element")


def _cleared_cache_16_3():
    cache = []
    for exps in anchored_supports_16_3():
        cache.append(cleared_obstructions_16_3(exps))
    return cache


def exceptional_prime_field(p, cache):
    roots = [w for w in range(1, p) if pow(w, 8, p) == p - 1]
    pows = {w: [pow(w, i, p) for i in range(DEG)] for w in roots}
    for i1, i2 in cache:
        v1 = [x % p for x in i1]
        v2 = [x % p for x in i2]
        for w in roots:
            pw = pows[w]
            if (sum(a * b for a, b in zip(v1, pw)) % p == 0 and
                    sum(a * b for a, b in zip(v2, pw)) % p == 0):
                return True
    return False


def exceptional_ext_field(p, cache):
    F = _GF2(p)
    w0 = F.order16_element()
    roots = [F.pw(w0, k) for k in range(1, 16, 2)]
    for i1, i2 in cache:
        for w in roots:
            pw = [(1, 0)]
            for _ in range(DEG - 1):
                pw.append(F.mul(pw[-1], w))
            s1 = (0, 0)
            s2 = (0, 0)
            for a, b in zip(i1, pw):
                s1 = F.add(s1, F.mul((a % p, 0), b))
            for a, b in zip(i2, pw):
                s2 = F.add(s2, F.mul((a % p, 0), b))
            if s1 == (0, 0) and s2 == (0, 0):
                return True
    return False


# ======================================================================
# 4.  SELF-TEST  --  recover {7, 17, 97} exactly, two ways, via the harness
# ======================================================================

# same q = p row list as the A3 verifier (p = 1 mod 16, p <= 700) plus the
# q = p^2 extension rows p in {7, 23} (ord_16(p) = 2).
PRIMES_1MOD16 = [17, 97, 113, 193, 241, 257, 337, 353, 401, 433,
                 449, 577, 593, 641, 673]
EXT_PRIMES = [7, 23]
TOY_EXCEPTIONAL = {7, 17, 97}


def build_toy_rowspec():
    rows = []
    for p in PRIMES_1MOD16:
        rows.append({"label": f"q=p={p}", "p": p, "q_form": "p"})
    for p in EXT_PRIMES:
        rows.append({"label": f"q=p^2={p}^2", "p": p, "q_form": "p2"})
    return {"schema": "c2-row-spec/v1", "n": 16,
            "H_max_mode": "explicit", "H_max": 3, "rows": rows}


def section_selftest():
    t0 = time.time()
    D, integral_ok, char0 = compute_toy_D_16_3()
    check("SELF-TEST S1  Lemma-2 integrality: 2^10 * O_j integral at all "
          "3003 anchored (16,3) supports", integral_ok)
    check("SELF-TEST S2  X24 instance: zero char-0 (16,3)-candidates "
          "(h=3 not a 2-power)", char0 == 0, f"char-0 candidates = {char0}")

    # build the toy certificate in the harness's own schema and run it.
    cert = {
        "schema": "c2-gcd-certificate/v1", "n": 16,
        "definition": "D_pt(ideal-norm)",
        "provenance": "computed in-process by compute_toy_D_16_3()",
        "entries": [{"h": 3, "D": str(D), "D_is_odd": (D % 2 == 1)}],
    }
    n_cert, entries, _, _ = _cert_from_dict(cert)
    rowspec = build_toy_rowspec()
    result = run_harness(n_cert, entries, rowspec)
    fail_primes = set(result["summary"]["exceptional_primes"])

    check("SELF-TEST S3  harness gcd(D(16,3), p) recovers exactly "
          "{7,17,97}", fail_primes == TOY_EXCEPTIONAL,
          f"harness FAIL set = {sorted(fail_primes)}")

    # independent pointwise cross-check (a(R) subset P), no gcd, no D.
    cache = _cleared_cache_16_3()
    pointwise = set()
    for p in PRIMES_1MOD16:
        if exceptional_prime_field(p, cache):
            pointwise.add(p)
    for p in EXT_PRIMES:
        if exceptional_ext_field(p, cache):
            pointwise.add(p)
    check("SELF-TEST S4  independent pointwise a(R) subset P test agrees "
          "with the gcd route", pointwise == fail_primes == TOY_EXCEPTIONAL,
          f"pointwise set = {sorted(pointwise)}")

    # The split-behaviour gate: supp(D_pt) also contains primes whose extra
    # candidate lives only in F_{p^f}, f = ord_16(p) > 2 (no q in {p, p^2}
    # row).  Those MUST be excluded by row validation.  Robust invariant over
    # small odd primes: any DIVISOR that is a valid row prime lies in
    # {7,17,97}; and at least one off-row divisor exists (p=3, ord_16=4).
    def ord16(p):
        x, o, v = p % 16, 1, p % 16
        while v != 1:
            v = v * x % 16
            o += 1
        return o
    small = [p for p in (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43,
                         47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97)]
    divisors = [(p, ord16(p)) for p in small if gcd(D, p) > 1]
    onrow = {p for p, o in divisors if o in (1, 2)}
    offrow = [p for p, o in divisors if o not in (1, 2)]
    ok_offrow = (onrow == TOY_EXCEPTIONAL and len(offrow) >= 1
                 and all(not (row_is_valid(16, p, "p")
                              or row_is_valid(16, p, "p2")) for p in offrow))
    check("SELF-TEST S5  split-behaviour gate: valid-row divisors of D are "
          "exactly {7,17,97}; off-row divisors (ord_16>2, e.g. 3) admit no "
          "q in {p,p^2} row and are excluded", ok_offrow,
          f"row divisors = {sorted(onrow)}; off-row divisors = {offrow}")

    check("SELF-TEST S6  every reported exceptional prime is a valid row "
          "prime (n | q-1)",
          all(any(int(r["p"]) == p and r["row_valid"]
                  for r in result["rows"]) for p in fail_primes),
          f"exceptional = {sorted(fail_primes)}")

    print(f"        [self-test wall time {time.time() - t0:.1f}s; "
          f"D_pt(16,3) has {len(str(D))} digits]")
    return {
        "D_digits": len(str(D)),
        "toy_exceptional": sorted(fail_primes),
        "pointwise_exceptional": sorted(pointwise),
        "row_divisors": sorted(onrow),
        "offrow_divisors": offrow,
        "tested_rows": len(result["rows"]),
    }


def _cert_from_dict(cert):
    """load_certificate() equivalent operating on an in-memory dict."""
    import tempfile
    import os
    fd, path = tempfile.mkstemp(suffix=".json")
    try:
        with os.fdopen(fd, "w") as fh:
            json.dump(cert, fh)
        return load_certificate(path)
    finally:
        os.unlink(path)


# ======================================================================
# 5.  TASK-1 ARITHMETIC CHECKS  --  the h-window audit
# ======================================================================
# Row-C-class and prize rows: A = k + t, k = rate * n.  Caps for n = 1024:
# 2 log2 n = 20, (log2 n)^2 = 100.  Prize: n = 2^41, (log2 n)^2 = 1681.

ROWC = [  # (label, rate_den, k, t, A)
    ("RowC 1/4",  4,  256, 5, 261),
    ("RowC 1/8",  8,  128, 5, 133),
    ("RowC 1/16", 16, 64,  3, 67),
]
PRIZE_N = 2 ** 41
PRIZE = [  # (label, rate_den, t, A)   n = 2^41, k = n / rate_den
    ("prize 1/4",  4,  2 ** 33 + 1, 558345748481),
    ("prize 1/8",  8,  2 ** 33 + 1, 283467841537),
    ("prize 1/16", 16, 2 ** 32 + 1, 141733920769),
]


def section_task1_window():
    n = 1024
    log2n = 10
    two_log2 = 2 * log2n           # 20
    grammar_sq = log2n * log2n     # 100

    # T1a: A = k + t at every Row-C row (k = n / rate_den).
    ok = True
    for label, rden, k, t, A in ROWC:
        if n // rden != k or k + t != A:
            ok = False
    check("TASK1 T1a  A = k + t and k = n/rate at all Row-C rows "
          "(t = 5,5,3 ; A = 261,133,67)", ok)

    # T1b: the caps and where each a-priori window ends vs the caps.
    caps_ok = (two_log2 == 20 and grammar_sq == 100)
    cover = {label: (A <= grammar_sq) for label, _, _, _, A in ROWC}
    # (log2 n)^2 covers h<=A only for rate 1/16 (67<=100); 1/4,1/8 exceed it.
    cover_ok = (cover["RowC 1/16"] and not cover["RowC 1/4"]
                and not cover["RowC 1/8"])
    check("TASK1 T1b  caps: 2 log2 n = 20, (log2 n)^2 = 100; the grammar "
          "cap 100 covers h<=A ONLY at rate 1/16 (67), not 1/4 (261) or "
          "1/8 (133)", caps_ok and cover_ok,
          f"A<=100 by row = {cover}")

    # T1c: the assembly's 2 log2 n = 20 lies below EVERY Row-C A, so it is
    # not an upper envelope for the a-priori trade sizes at any rate.
    below_all = all(two_log2 < A for _, _, _, _, A in ROWC)
    check("TASK1 T1c  the assembly's H_max = 2 log2 n = 20 is below every "
          "Row-C agreement A (67,133,261): it caps nothing a priori",
          below_all)

    # T1d: prize rows have EMPTY small-block windows (t >> (log2 n)^2),
    # so the h-window lane is vacuous there and A = k + t still holds.
    pn_log2 = PRIZE_N.bit_length() - 1   # 41
    pn_grammar_sq = pn_log2 * pn_log2    # 1681
    empty_ok = True
    akt_ok = True
    for label, rden, t, A in PRIZE:
        k = PRIZE_N // rden
        if not (t > pn_grammar_sq):
            empty_ok = False
        if k + t != A:
            akt_ok = False
    check("TASK1 T1d  prize rows: t > (log2 n)^2 = 1681 so the small-block "
          "window is EMPTY (lane vacuous); A = k + t confirmed",
          empty_ok and akt_ok)

    # T1e (HEURISTIC, not a proof gate): first-moment estimate for the
    # number of primitive trades at size h is ~ n^2 / (h!)^2 for q >= n^2;
    # it drops below 1 near h ~ 7 for n = 1024.  Recorded, NOT proven.
    import math
    fm = {h: (n ** 2) / (math.factorial(h) ** 2) for h in (5, 7, 10, 20)}
    heuristic_drop = fm[7] < 1 < fm[5]
    check("TASK1 T1e  [HEURISTIC, informational] first-moment n^2/(h!)^2 "
          "crosses 1 near h=7 (n=1024); NOT a rigorous emptiness proof",
          heuristic_drop,
          f"n^2/(h!)^2 at h=5,7,10,20 = "
          f"{ {h: round(v, 3) for h, v in fm.items()} }")
    return {
        "rowc": [
            {"label": label, "rate_den": rden, "k": k, "t": t, "A": A}
            for label, rden, k, t, A in ROWC
        ],
        "caps": {"two_log2": two_log2, "grammar_sq": grammar_sq},
        "A_le_grammar_sq": cover,
        "prize_log2n_squared": pn_grammar_sq,
        "prize_window_empty": empty_ok and akt_ok,
        "fm_rounded": {str(h): round(v, 3) for h, v in fm.items()},
    }


def section_task1_partners():
    """The large-h companion, proven part: <= n partners per anchored core
    at EVERY h (the value-set argument generalising the h=3 cubic cap).

    Lemma.  Fix an h-subset core P of mu_n.  A partner Q (h-subset of mu_n,
    disjoint, e_i(P)=e_i(Q) for i<h) has L_Q = L_P - c for a nonzero
    constant c, and every root y of L_Q lies in mu_n with c = L_P(y).  Hence
    c belongs to the value set { L_P(x) : x in mu_n } (size <= n) and Q is
    the root set of L_P - c, so Q |-> c is injective: #partners <= n.

    Verified over a toy row F_17 ⊃ mu_8 at h=3 and h=4 by direct
    enumeration: partners-per-core <= n AND Q |-> c injective."""
    p = 17
    n = 8
    g = 3
    w = pow(g, (p - 1) // n, p)           # order-8 element
    mu = [pow(w, i, p) for i in range(n)]
    assert len(set(mu)) == n

    def locator_coeffs(subset):
        # monic poly prod (X - x) over F_p ; return coeff list low..high
        coeffs = [1]
        for x in subset:
            new = [0] * (len(coeffs) + 1)
            for i, ci in enumerate(coeffs):
                new[i + 1] = (new[i + 1] + ci) % p
                new[i] = (new[i] - x * ci) % p
            coeffs = new
        return coeffs                       # length h+1, coeffs[h]=1

    def eval_loc(coeffs, x):
        acc = 0
        for c in reversed(coeffs):
            acc = (acc * x + c) % p
        return acc

    ok = True
    detail = []
    for h in (3, 4):
        idx = list(range(n))
        max_partners = 0
        inj_ok = True
        for Pi in itertools.combinations(idx, h):
            P = [mu[i] for i in Pi]
            Lp = locator_coeffs(P)
            # partners: disjoint h-subsets Q with L_Q - L_P constant, i.e.
            # they share coeffs 1..h (all but the constant term).
            partners = []
            for Qi in itertools.combinations(idx, h):
                if set(Qi) & set(Pi):
                    continue
                Q = [mu[i] for i in Qi]
                Lq = locator_coeffs(Q)
                if Lq[1:] == Lp[1:] and Lq[0] != Lp[0]:
                    partners.append(Q)
            max_partners = max(max_partners, len(partners))
            if len(partners) > n:
                ok = False
            # injectivity of Q |-> c = L_P(y), y in Q  (c = Lp[0]-Lq[0])
            cs = set()
            for Q in partners:
                c = (Lp[0] - locator_coeffs(Q)[0]) % p
                # c must equal L_P(y) for each y in Q
                if any(eval_loc(Lp, y) != c for y in Q):
                    inj_ok = False
                if c in cs:
                    inj_ok = False
                cs.add(c)
            # value set size bound
            vs = len({eval_loc(Lp, x) for x in mu})
            if len(partners) > vs:
                ok = False
        detail.append((h, max_partners))
        if not inj_ok:
            ok = False
    check("TASK1 T1f  <= n partners per anchored core at EVERY h "
          "(value-set argument), verified F_17 ⊃ mu_8, h=3,4: partners "
          "<= n=8 and Q |-> c injective", ok,
          f"(h, max partners) = {detail}")

    # And the honest limit: the crude route bounds trades by
    #   (active cores) x n,  and #cores = C(n,h) is super-polynomial, so the
    # large-h companion reduces to the SAME terminal `active_core_count_bound`
    # -- it does not close cheaply.  This is recorded as an informational
    # (always-true) note, not a mathematical claim of closure.
    from math import comb
    blow = comb(1024, 100)
    check("TASK1 T1g  [informational] C(n,h) cores is super-polynomial "
          "(C(1024,100) has ~150 digits): partners<=n alone cannot close "
          "large-h; it reduces to active_core_count_bound (terminal)",
          len(str(blow)) > 100, f"C(1024,100) has {len(str(blow))} digits")
    return {
        "toy_field": "F_17",
        "toy_domain_n": n,
        "partner_cap_details": [
            {"h": h, "max_partners": max_partners}
            for h, max_partners in detail
        ],
        "comb_1024_100_digits": len(str(blow)),
    }


def section_pinned_certificate(selftest, window, partners):
    with open(SELFTEST_CERT) as fh:
        cert = json.load(fh)
    ok = (
        cert["schema"] == "c2-gcd-harness-selftest/v1"
        and cert["node"] == "c2_gcd_harness"
        and cert["status"] == "HARNESS_SELFTEST_GREEN"
        and cert["selftest"] == selftest
        and cert["window_audit"] == window
        and cert["partner_cap"] == partners
    )
    check("CERT  pinned C2 self-test certificate matches recomputed summary", ok)


# ======================================================================
# 6.  main
# ======================================================================

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cert", help="D(n,h) certificate JSON "
                    "(schema c2-gcd-certificate/v1)")
    ap.add_argument("--rowspec", help="row-prime spec JSON "
                    "(schema c2-row-spec/v1)")
    ap.add_argument("--out", help="write the per-row result certificate here")
    args = ap.parse_args()

    if args.cert or args.rowspec:
        # HARNESS mode
        if not (args.cert and args.rowspec):
            ap.error("--cert and --rowspec must be given together")
        n, entries, defn, prov = load_certificate(args.cert)
        rowspec = load_rowspec(args.rowspec)
        result = run_harness(n, entries, rowspec)
        result["cert_definition"] = defn
        result["cert_provenance"] = prov
        text = json.dumps(result, indent=2)
        if args.out:
            with open(args.out, "w") as fh:
                fh.write(text + "\n")
            print(f"wrote {args.out}")
        else:
            print(text)
        # exit 0 always in harness mode (FAIL rows are data, not errors)
        return 0

    # VERIFIER mode
    print("=" * 66)
    print("C2 GCD-TEST HARNESS -- self-test + Task-1 h-window checks")
    print("=" * 66)
    print("\n-- SELF-TEST: recover the (16,3) exceptional set {7,17,97} --")
    selftest = section_selftest()
    print("\n-- TASK 1: h-window derivation audit (arithmetic) --")
    window = section_task1_window()
    partners = section_task1_partners()
    section_pinned_certificate(selftest, window, partners)

    n_ok = sum(1 for _, ok in _RESULTS if ok)
    n_tot = len(_RESULTS)
    print("\n" + "=" * 66)
    print(f"RESULT: {n_ok}/{n_tot} PASS, {n_tot - n_ok} FAIL")
    print("=" * 66)
    return 0 if n_ok == n_tot else 1


if __name__ == "__main__":
    sys.exit(main())
