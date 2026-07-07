#!/usr/bin/env python3
"""
verify_q_moment_order_floor_reconciliation.py

Precision reconciliation of the finite-Q moment-order floor
    r >= ceil( w * log2|B| / Delta_Q )
across the four deployed adjacent rows (KB-MCA, KB-list, M31-MCA, M31-list),
under the two averaging conventions for the bit margin Delta_Q, and against:

  * the maintainer's prop:q-moment-order-floor / prop:q-exact-target table
    (experimental/grande_finale.tex, commit b33609d) -- real-average convention;
  * PR #384's cap25_v13_gammar_order_floor.md Section-3 table, which fed the
    4-decimal *printed* margins (22.0109 / 3.2589) straight into the formula and
    therefore superseded two entries (KB-list 94992, M31-MCA 641584).

Everything here is recomputed from scratch in exact integer arithmetic plus
Decimal at two precisions (60 and 140 significant digits). The two precisions
must agree on every integer, and every ceiling is certified by showing the
argument's distance to the nearest integer exceeds 1e-30.

Usage:
    python3 verify_q_moment_order_floor_reconciliation.py            # PASS -> exit 0, prints the reconciliation table
    python3 verify_q_moment_order_floor_reconciliation.py --tamper-selftest  # perturbs every pinned integer, confirms detection

Stdlib only (math, decimal). Deterministic. No network, no file I/O.
"""

import sys
import math
from decimal import Decimal, getcontext

# --------------------------------------------------------------------------
# Exact integer constants (no floats in the certificate payload).
# --------------------------------------------------------------------------
N   = 2**21                  # 2097152  ambient domain size
K20 = 2**20                  # 1048576  = k

P_KB  = 2**31 - 2**24 + 1    # 2130706433  (KoalaBear prime, |B| for the KB rows)
P_M31 = 2**31 - 1            # 2147483647  (Mersenne-31 prime, |B| for the M31 rows)

# Budgets B* exactly as prop:q-exact-target defines them (grande_finale.tex):
#   B*_KB  = floor( (2^31-2^24+1)^6 / 2^128 )
#   B*_M31 = floor( (2^31-1)^4     / 2^100 )
BSTAR_KB  = (P_KB**6)  >> 128    # 274980728111395087
BSTAR_M31 = (P_M31**4) >> 100    # 16777215

# rows: (name, a_plus, K, prime p (=|B|), budget B*)
ROWS = [
    ("KB-MCA",   1116048, K20 + 1, P_KB,  BSTAR_KB),
    ("KB-list",  1116047, K20,     P_KB,  BSTAR_KB),
    ("M31-MCA",  1116024, K20 + 1, P_M31, BSTAR_M31),
    ("M31-list", 1116023, K20,     P_M31, BSTAR_M31),
]

# --------------------------------------------------------------------------
# Pinned data (the certificate). Integers are exact; Decimal witnesses are
# stored as digit strings.
# --------------------------------------------------------------------------
PIN = {
    # B* budgets recomputed from the primes above
    "bstar_kb":  274980728111395087,
    "bstar_m31": 16777215,

    # r-floor under each convention, all four rows
    #   ceil-avg : Delta = log2 B* - log2 ceil( C(n,a+) / p^w )
    #   real-avg : Delta = log2 B* - ( log2 C(n,a+) - w log2 p )
    "r_ceil_avg": {"KB-MCA": 94196, "KB-list": 94991, "M31-MCA": 641594, "M31-list": 680397},
    "r_real_avg": {"KB-MCA": 94196, "KB-list": 94991, "M31-MCA": 641593, "M31-list": 680397},

    # the maintainer's shipped table (grande_finale.tex prop:q-moment-order-floor,
    # commit b33609d) -- identical to the real-average column, all four exact
    "r_maintainer": {"KB-MCA": 94196, "KB-list": 94991, "M31-MCA": 641593, "M31-list": 680397},
    "maintainer_convention": "real-avg",

    # PR #384 Section-3 entries SUPERSEDED here: both arose from feeding the
    # 4-decimal printed margin straight into ceil(w log2 p / Delta).
    "superseded_384": {"KB-list": 94992, "M31-MCA": 641584},
    # the exact 4-decimal printed margins that #384 used as Delta inputs
    "delta_printed": {"KB-MCA": "22.1969", "KB-list": "22.0109",
                      "M31-MCA": "3.2589", "M31-list": "3.0730"},
    # #384 also fed the printed margin at the other two rows; there the coarse
    # input happens to land on the exact answer (robust rows)
    "r_384_all": {"KB-MCA": 94196, "KB-list": 94992, "M31-MCA": 641584, "M31-list": 680397},

    # M31-MCA convention-sensitivity witness: the fractional part of the
    # r-argument  w*log2(p)/Delta_Q  under each convention (certified strings).
    # ceil-avg sits at 641593.0608...  -> ceil 641594
    # real-avg sits at 641592.9400...  -> ceil 641593   (the shift crosses 641593)
    "frac_ceil_m31mca": "0.0608501482325313804389337200342645513549",
    "frac_real_m31mca": "0.9400176511939683414672191182406133937095",
}

# --------------------------------------------------------------------------
# Heavy integers (exact), computed once and cached.
# --------------------------------------------------------------------------
_HEAVY = {}

def heavy():
    """Return {a_plus: C(N, a_plus)} for the four rows plus {(p,w): p**w}.

    Only the two 'list' binomials are formed with math.comb; the two 'MCA'
    partners (a+1) follow from the exact one-step identity
        C(n, a) = C(n, a-1) * (n - a + 1) // a
    which is verified by an integer invariant below."""
    if _HEAVY:
        return _HEAVY
    binom = {}
    binom[1116047] = math.comb(N, 1116047)
    binom[1116048] = binom[1116047] * (N - 1116047) // 1116048
    binom[1116023] = math.comb(N, 1116023)
    binom[1116024] = binom[1116023] * (N - 1116023) // 1116024
    # exact-ratio invariants: C(n,a)*a == C(n,a-1)*(n-a+1)
    assert binom[1116048] * 1116048 == binom[1116047] * (N - 1116047)
    assert binom[1116024] * 1116024 == binom[1116023] * (N - 1116023)
    pw = {}
    for _name, a, Kv, p, _Bs in ROWS:
        w = a - Kv
        key = (p, w)
        if key not in pw:
            pw[key] = pow(p, w)
    _HEAVY["binom"] = binom
    _HEAVY["pw"] = pw
    return _HEAVY


def dlog2_int(x):
    """Decimal log2 of a positive integer x at the active context precision.

    For very large x we keep only the top (4*prec + 64) bits before taking ln,
    which drops a relative error < 2^-(4*prec+64) -- far below the working
    precision -- while avoiding an astronomically large ln input."""
    prec = getcontext().prec
    bl = x.bit_length()
    keep = 4 * prec + 64
    ln2 = Decimal(2).ln()
    if bl > keep:
        shift = bl - keep
        top = x >> shift
        return Decimal(shift) + Decimal(top).ln() / ln2
    return Decimal(x).ln() / ln2


def ceil_and_frac(x):
    """ceil(x) for x>0, plus the fractional part x-floor(x) as a Decimal."""
    fx = int(x)                      # floor for positive x
    frac = x - fx
    if frac == 0:
        return fx, frac
    return fx + 1, frac


def recompute(prec):
    """Recompute, at the given Decimal precision, every quantity in the packet.

    Returns a dict keyed by row name, each value a dict with the ceil-avg and
    real-avg r-floors, their argument fractional parts, and Delta_Q values."""
    getcontext().prec = prec
    H = heavy()
    binom, pwtab = H["binom"], H["pw"]
    result = {}
    for name, a, Kv, p, Bs in ROWS:
        w = a - Kv
        B = binom[a]
        pw = pwtab[(p, w)]
        L = (B + pw - 1) // pw       # ceil( C(n,a) / p^w )  (exact integer)

        log2p = dlog2_int(p)
        num = Decimal(w) * log2p     # w * log2|B|   (numerator of the floor)
        log2Bs = dlog2_int(Bs)

        real_inner = dlog2_int(B) - num          # log2 C(n,a) - w log2 p
        ceil_inner = dlog2_int(L)                # log2 ceil( C(n,a)/p^w )
        D_real = log2Bs - real_inner
        D_ceil = log2Bs - ceil_inner

        r_real, f_real = ceil_and_frac(num / D_real)
        r_ceil, f_ceil = ceil_and_frac(num / D_ceil)

        result[name] = dict(
            w=w, L=L, log2Bs=log2Bs, num=num,
            D_real=D_real, D_ceil=D_ceil,
            r_real=r_real, r_ceil=r_ceil,
            f_real=f_real, f_ceil=f_ceil,
        )
    return result


def replay_384(prec):
    """Reproduce PR #384's floors: ceil( w log2 p / Delta_printed ), where
    Delta_printed is the 4-decimal margin string from the row table."""
    getcontext().prec = prec
    out = {}
    for name, a, Kv, p, _Bs in ROWS:
        w = a - Kv
        log2p = dlog2_int(p)
        arg = (Decimal(w) * log2p) / Decimal(PIN["delta_printed"][name])
        r, _ = ceil_and_frac(arg)
        out[name] = r
    return out


# --------------------------------------------------------------------------
# Certificate check
# --------------------------------------------------------------------------
def _head(dec, k=30):
    """First k digits after the point of a Decimal in [0,1), as '0.<digits>'."""
    s = format(dec, "f")             # plain fixed-point, never scientific
    return s[:k + 2]


def check(comp60, comp140, r384, pin):
    """Compare the fresh recomputation against the pinned certificate.
    Returns (ok, messages)."""
    msgs = []
    ok = True

    def rec(label, cond):
        nonlocal ok
        ok = ok and cond
        msgs.append(f"  [{'OK ' if cond else 'BAD'}] {label}")

    # 0. exact budgets
    rec(f"B*_KB  = {BSTAR_KB}  == pin", BSTAR_KB == pin["bstar_kb"])
    rec(f"B*_M31 = {BSTAR_M31} == pin", BSTAR_M31 == pin["bstar_m31"])

    # 1. two precisions agree on every integer floor
    for name, *_ in ROWS:
        rec(f"{name}: r_ceil prec60==prec140 ({comp60[name]['r_ceil']})",
            comp60[name]["r_ceil"] == comp140[name]["r_ceil"])
        rec(f"{name}: r_real prec60==prec140 ({comp60[name]['r_real']})",
            comp60[name]["r_real"] == comp140[name]["r_real"])

    # 2. ceil-avg / real-avg floors == pins
    for name, *_ in ROWS:
        rec(f"{name}: ceil-avg r == pin {pin['r_ceil_avg'][name]}",
            comp140[name]["r_ceil"] == pin["r_ceil_avg"][name])
        rec(f"{name}: real-avg r == pin {pin['r_real_avg'][name]}",
            comp140[name]["r_real"] == pin["r_real_avg"][name])

    # 3. maintainer's table == real-avg column (convention attribution)
    rec(f"maintainer convention pinned as '{pin['maintainer_convention']}'",
        pin["maintainer_convention"] == "real-avg")
    for name, *_ in ROWS:
        rec(f"{name}: maintainer r {pin['r_maintainer'][name]} == real-avg recompute",
            pin["r_maintainer"][name] == comp140[name]["r_real"])

    # 4. superseded #384 entries reproduced from the printed-margin replay,
    #    and shown NOT equal to either exact convention
    for name, val in pin["superseded_384"].items():
        rec(f"{name}: #384 replay ceil(w log2 p / {pin['delta_printed'][name]}) == {val}",
            r384[name] == val)
        rec(f"{name}: superseded {val} != real-avg {comp140[name]['r_real']}",
            val != comp140[name]["r_real"])
        rec(f"{name}: superseded {val} != ceil-avg {comp140[name]['r_ceil']}",
            val != comp140[name]["r_ceil"])
    # the other two rows: printed-margin replay coincidentally lands on the exact answer
    for name in ("KB-MCA", "M31-list"):
        rec(f"{name}: #384 replay == real-avg (robust row) {pin['r_real_avg'][name]}",
            r384[name] == pin["r_real_avg"][name])
    for name, *_ in ROWS:
        rec(f"{name}: #384 replay == pinned r_384_all {pin['r_384_all'][name]}",
            r384[name] == pin["r_384_all"][name])

    # 5. exact real-avg Delta_Q rounds to the 4-decimal printed margin
    for name, *_ in ROWS:
        d = comp140[name]["D_real"]
        printed = Decimal(pin["delta_printed"][name])
        rounded = d.quantize(Decimal("0.0001"))
        rec(f"{name}: round(Delta_real,4)={rounded} == printed {printed}",
            rounded == printed)

    # 6. ceiling certification: distance to nearest integer > 1e-30, both conventions
    tol = Decimal("1e-30")
    for name, *_ in ROWS:
        for conv, fkey in (("ceil", "f_ceil"), ("real", "f_real")):
            f = comp140[name][fkey]
            dist = min(f, Decimal(1) - f)
            rec(f"{name}: {conv}-avg ceiling certified, dist-to-int={dist:.3e} > 1e-30",
                dist > tol)

    # 7. M31-MCA convention-sensitivity witness: fractional parts match pins
    #    to >= 30 significant digits, and the two conventions differ by one.
    rec(f"M31-MCA ceil-avg frac head == pin ({pin['frac_ceil_m31mca'][:12]}...)",
        _head(comp140["M31-MCA"]["f_ceil"]) == _head(Decimal(pin["frac_ceil_m31mca"])))
    rec(f"M31-MCA real-avg frac head == pin ({pin['frac_real_m31mca'][:12]}...)",
        _head(comp140["M31-MCA"]["f_real"]) == _head(Decimal(pin["frac_real_m31mca"])))
    rec("M31-MCA is convention-sensitive: r_ceil - r_real == 1",
        comp140["M31-MCA"]["r_ceil"] - comp140["M31-MCA"]["r_real"] == 1)
    for name in ("KB-MCA", "KB-list", "M31-list"):
        rec(f"{name} is convention-robust: r_ceil == r_real",
            comp140[name]["r_ceil"] == comp140[name]["r_real"])

    return ok, msgs


def print_table(comp, r384):
    print()
    print("  Reconciliation of  r >= ceil( w*log2|B| / Delta_Q ), four adjacent rows")
    print("  " + "-" * 80)
    print(f"  {'row':9s} {'w':>6s} {'log2 B*':>10s} {'Delta_real':>12s} "
          f"{'ceil-avg r':>11s} {'real-avg r':>11s} {'#384':>8s}")
    for name, *_ in ROWS:
        d = comp[name]
        print(f"  {name:9s} {d['w']:>6d} {float(d['log2Bs']):>10.4f} "
              f"{float(d['D_real']):>12.6f} {d['r_ceil']:>11d} {d['r_real']:>11d} "
              f"{r384[name]:>8d}")
    print("  " + "-" * 80)
    print("  maintainer (grande_finale.tex prop:q-moment-order-floor) == real-avg column")
    print("  superseded PR #384: KB-list 94992, M31-MCA 641584 (fed 4-decimal printed margin)")
    m = comp["M31-MCA"]
    print()
    print("  M31-MCA convention-sensitivity witness (L = ceil(C(n,a+)/p^w) = %d):" % m["L"])
    print(f"    Delta_ceil = {m['D_ceil']}")
    print(f"    Delta_real = {m['D_real']}")
    print(f"    arg frac (ceil-avg) = {_head(m['f_ceil'], 40)}  -> ceil {m['r_ceil']}")
    print(f"    arg frac (real-avg) = {_head(m['f_real'], 40)}  -> ceil {m['r_real']}")
    print()


# --------------------------------------------------------------------------
def tamper_selftest():
    """Perturb every pinned integer (and each M31-MCA fractional-part digit
    string) by one; confirm the checker then reports a mismatch (CAUGHT)."""
    comp60 = recompute(60)
    comp140 = recompute(140)
    r384 = replay_384(140)

    ok, _ = check(comp60, comp140, r384, PIN)
    if not ok:
        print("TAMPER-SELFTEST ABORTED: baseline certificate does not pass.")
        return 1

    import copy
    caught = 0
    total = 0

    def try_pin(desc, mutate):
        nonlocal caught, total
        total += 1
        p = copy.deepcopy(PIN)
        mutate(p)
        good, _ = check(comp60, comp140, r384, p)
        status = "CAUGHT" if not good else "MISSED"
        if not good:
            caught += 1
        print(f"  tamper {desc:46s} -> {status}")

    try_pin("bstar_kb += 1",  lambda p: p.__setitem__("bstar_kb", p["bstar_kb"] + 1))
    try_pin("bstar_m31 += 1", lambda p: p.__setitem__("bstar_m31", p["bstar_m31"] + 1))

    for dkey in ("r_ceil_avg", "r_real_avg", "r_maintainer", "r_384_all"):
        for name, *_ in ROWS:
            try_pin(f"{dkey}[{name}] += 1",
                    lambda p, d=dkey, n=name: p[d].__setitem__(n, p[d][n] + 1))
    for name in PIN["superseded_384"]:
        try_pin(f"superseded_384[{name}] += 1",
                lambda p, n=name: p["superseded_384"].__setitem__(n, p["superseded_384"][n] + 1))

    try_pin("maintainer_convention -> ceil-avg",
            lambda p: p.__setitem__("maintainer_convention", "ceil-avg"))

    def flip(s):
        i = 10
        d = "5" if s[i] != "5" else "6"
        return s[:i] + d + s[i + 1:]
    try_pin("frac_ceil_m31mca digit",
            lambda p: p.__setitem__("frac_ceil_m31mca", flip(p["frac_ceil_m31mca"])))
    try_pin("frac_real_m31mca digit",
            lambda p: p.__setitem__("frac_real_m31mca", flip(p["frac_real_m31mca"])))

    print(f"\n  tamper-selftest: {caught}/{total} perturbations CAUGHT")
    return 0 if caught == total else 1


def main(argv):
    if "--tamper-selftest" in argv:
        rc = tamper_selftest()
        print("TAMPER-SELFTEST:", "PASS" if rc == 0 else "FAIL")
        return rc

    comp60 = recompute(60)
    comp140 = recompute(140)
    r384 = replay_384(140)
    ok, msgs = check(comp60, comp140, r384, PIN)
    for m in msgs:
        print(m)
    print_table(comp140, r384)
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
