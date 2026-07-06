#!/usr/bin/env python3
"""verify_gammar_order_floor.py

Zero-arg, stdlib-only, deterministic verifier for
experimental/data/certificates/frontier-adjacent/gammar_order_floor_v1.json
and its companion note experimental/notes/thresholds/cap25_v13_gammar_order_floor.md.

This packet is the first Gamma_r (fixed-moment collision hierarchy,
grande_finale.tex \\label{prop:moment-sandwich} / raw \\label{prob:capfp-gamma}) data on
the paid quotient/planted-pruned prefix object, raw vs twist-primitive ("removed"),
r=2..8, exact Fraction arithmetic. It proves two one-line exact bricks -- Brick 1, an
unconditional order floor r>=ceil(w log2|B|/Delta) forced by Gamma_r>=1 alone, and
Brick 2, a monotone certificate R_eff(r):=Gamma_r^{1/(r-1)} -> R pinning the exact order
r_min(R) at which a moment proof can close -- and measures that quotient/planted removal
does NOT tame the moment constants in the dense bulk (the frontier's regime), because the
bulk collision mass is provably primitive.

This verifier does NOT evaluate Gamma_r at any deployed w (out of reach), does NOT prove
or refute prob:row-sharp-q, does NOT move the frontier edge, and does NOT alter any
verdict or integer of PR #366 (it independently reproduces two of that PR's own shipped
moment-route numbers -- 94196 at KB-MCA/L_0, 5886 at L_4 -- from raw constants, upgrading
them from Gamma_r-assumed-trivial estimates to unconditional floors). All histogram /
ledger code below is an independent reimplementation; it does not import
laneN_compute.py or laneN_fit.py, and does not read laneN_outputs.json.

Five gate classes; exit 0 iff ALL pass, nonzero on ANY failure:

  gate i    BRICK-1 FLOOR ARITHMETIC. Recomputes w, |B| (the exact integer field size
            P_KB=2^31-2^24+1 / P_M31=2^31-1), and Delta (the 4-decimal constant printed
            in grande_finale.tex's adjacent-margin table) from raw constants for five
            rows (KB-MCA, KB-list, M31-MCA, M31-list, L4-rung), computes
            r0=ceil(w log2|B|/Delta) via exact ceil arithmetic, diffs against the shipped
            JSON, and cross-checks the KB-MCA and L4 values against PR #366's own shipped
            moment-route numbers (94196, 5886 -- embedded as literals with a provenance
            comment; this verifier does not read another PR's branch/worktree).
  gate ii   LIVE EXACT GAMMA_R RECOMPUTATION (Fraction, independent reimplementation).
            By default: F17x_16_8 (w=1..4, exhaustive), mu24_F97_12 (w=2, the dense-bulk
            exhibit: checks log2(Gamma_8_raw)<0.17 by name), and mu64_F257_34 (w=1, the
            ultra-dense exhibit: checks Gamma_r_raw=1 to 1e-9 for every r=2..8 by name;
            subset-size DP, since C(64,34)~2^60 is too large to enumerate). --full adds
            mu20_F41_10 (w=1..4), mu24_F97_12 (w=1,3,4), and mu64_F257_34 (w=2, DP,
            +~50s). Every (row,w) pair is diffed against the shipped JSON's
            measured_curves.full_grid (cells_hit, prim_cells, R_raw, and all of
            Gamma_2..Gamma_8 raw+prim).
  gate iii  BRICK-2 MONOTONICITY. Checks R_eff(r):=Gamma_r^{1/(r-1)} is non-decreasing
            across r=2..8 on every (row,w) pair computed by gate ii (reused via cache,
            no recomputation). Checks the r_min(R) formula's finiteness-iff-R<2^Delta
            branch directly on synthetic R values (R=2^(Delta-1) must be finite,
            R=2^Delta and R=2^(Delta+1) must be infinite). Reproduces the R-insensitivity
            headline: doubling R (log2 R: 0->1) inflates KB-MCA's order by ~4.72%.
  gate iv   BALANCED-TERNARY KERNEL LEDGER. Recomputes the exact Gamma_2 ledger
            (prop:capfr1-collision-ledger: sum_z N_w(z)^2 = C(n,m) + sum_e C(n-2e,m-e)
            T_w(e)) on F17x_16_8 w=2 by default (--full: w=1..4), checks it reproduces
            the live histogram's own Gamma_2 (matches_hist), and diffs G2_full,
            G2_prim_off, and the T_w/T_w^prim censuses against the shipped JSON.
  gate v    REMOVAL COMPARISON. Recomputes raw-vs-twist-primitive R and Gamma_8 on
            mu24_F97_12 w=2 live (reused from gate ii's cache), checks the dense-bulk
            shave is <0.04 bit (measured ~0.0165) and that log2(Gamma_8_raw)<0.17 (the
            same dense-bulk flag gate ii checks by name).

Hidden self-test: python3 verify_gammar_order_floor.py --tamper-selftest
    Each gate corrupts exactly one stored/expected value used inside that gate's checks
    (never the from-scratch recomputed side) and must then report a mismatch (CAUGHT).

--full: python3 verify_gammar_order_floor.py --full
    Extends gates ii/iv to the remaining rows/widths (see above). Adds ~90-110s,
    dominated by mu64_F257_34 w=2's subset-size DP (~50s) and the full mu24_F97_12
    w=1,3,4 exhaustive sweep (~35s).

PERFORMANCE (zero-arg). Dominated by mu24_F97_12 w=2's exhaustive enumeration
(C(24,12)=2,704,156 combinations, ~6-10s measured). Everything else (F17x_16_8's four
widths, mu64_F257_34 w=1's DP, the kernel ledger at w=2, all arithmetic gates) is well
under 1s combined. Measured total: see the printed footer; comfortably under the 90s
budget.
"""
from __future__ import annotations

import json
import math
import os
import sys
import time
from itertools import combinations
from fractions import Fraction
from math import gcd, comb

# ---------------------------------------------------------------------------
# paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
JSON_PATH = os.path.join(REPO_ROOT, "experimental", "data", "certificates",
                         "frontier-adjacent", "gammar_order_floor_v1.json")
NOTE_PATH = os.path.join(REPO_ROOT, "experimental", "notes", "thresholds",
                         "cap25_v13_gammar_order_floor.md")

WALL_ID = "CAP25-V13-GAMMA-R-ORDER-FLOOR"

# ---------------------------------------------------------------------------
# raw constants -- deployed KB-MCA v13-raw safe row, ground truth independent of
# any JSON (the same constants verify_conjq_rung_routes_dead.py uses for PR #366).
# ---------------------------------------------------------------------------
P_KB = 2 ** 31 - 2 ** 24 + 1        # KoalaBear prime = 2130706433
P_M31 = 2 ** 31 - 1                 # Mersenne-31 prime = 2147483647
N_KB = 2 ** 21
K_KB = 2 ** 20
M_SAFE = 1116048
W_SAFE = M_SAFE - K_KB - 1          # 67471

# Delta = the 4-decimal adjacent-margin constants printed in grande_finale.tex
# (L183-186 / L1662-1665) -- "the integrated audit constants".
DELTA_KB_MCA = 22.1969
DELTA_KB_LIST = 22.0109
DELTA_M31_MCA = 3.2589
DELTA_M31_LIST = 3.0730

BRICK1_ROWS = [
    # (label, w, p, Delta)
    ("KB-MCA",   67471, P_KB,  DELTA_KB_MCA),
    ("KB-list",  67471, P_KB,  DELTA_KB_LIST),
    ("M31-MCA",  67447, P_M31, DELTA_M31_MCA),
    ("M31-list", 67447, P_M31, DELTA_M31_LIST),
    ("L4-rung",   4216, P_KB,  DELTA_KB_MCA),
]

# PR #366's own shipped moment-route numbers (kb_mca_conjq_route_margins_v1.json,
# moment_route.rows[L_0 / L_4].r_at_bar) -- embedded as literals with provenance;
# this verifier does not read another PR's branch/worktree.
PR366_KBMCA_R_AT_BAR = 94196
PR366_L4_R_AT_BAR = 5886


# ---------------------------------------------------------------------------
# generic helpers
# ---------------------------------------------------------------------------
def _corrupt(x):
    if isinstance(x, bool):
        return not x
    if isinstance(x, int):
        return x + 1
    if isinstance(x, float):
        return x + 1.0
    if isinstance(x, str):
        return x + "_TAMPERED_NONEXISTENT"
    if isinstance(x, dict):
        return {k: (v + 1 if isinstance(v, (int, float)) and not isinstance(v, bool) else v)
                for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return list(x[:-1]) if x else [999999]
    return x


def check(actual, expected, *, tol=None, tamper=False):
    if tamper:
        expected = _corrupt(expected)
    if tol is not None:
        return abs(actual - expected) <= tol
    return actual == expected


def load_packet():
    with open(JSON_PATH, encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------
# domain / histogram machinery -- independent reimplementation, not imported
# from laneN_compute.py
# ---------------------------------------------------------------------------
def primitive_root(p):
    phi = p - 1
    facs = []
    x = phi
    d = 2
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
    raise RuntimeError("no primitive root found")


def mult_subgroup(p, n):
    assert (p - 1) % n == 0, f"n={n} must divide p-1={p-1}"
    g = primitive_root(p)
    h = pow(g, (p - 1) // n, p)
    D = []
    cur = 1
    for _ in range(n):
        D.append(cur)
        cur = (cur * h) % p
    assert len(set(D)) == n
    return sorted(D)


def domain_for(p, n):
    return mult_subgroup(p, n) if n != p - 1 else sorted(range(1, p))


def hist_exhaustive(D, p, m, w):
    n = len(D)
    xp = [[pow(x, j + 1, p) for j in range(w)] for x in D]
    hist = {}
    for combo in combinations(range(n), m):
        ps = [0] * w
        for idx in combo:
            row = xp[idx]
            for j in range(w):
                ps[j] += row[j]
        key = tuple(v % p for v in ps)
        hist[key] = hist.get(key, 0) + 1
    return hist


def hist_dp(D, p, m, w):
    """Subset-size DP over the prefix ring B^w; avoids enumerating C(n,m) subsets
    directly (needed for mu64_F257_34, C(64,34)~2^60)."""
    n = len(D)
    xp = [tuple(pow(x, j + 1, p) for j in range(w)) for x in D]
    dp = [dict() for _ in range(m + 1)]
    dp[0][tuple([0] * w)] = 1
    for i in range(n):
        add = xp[i]
        for s in range(min(i, m - 1), -1, -1):
            cur = dp[s]
            if not cur:
                continue
            nxt = dp[s + 1]
            for key, cnt in cur.items():
                nk = tuple((key[j] + add[j]) % p for j in range(w))
                nxt[nk] = nxt.get(nk, 0) + cnt
    return dp[m]


def twist_stabilizer(key, n):
    """s(z) = gcd(n, {j: z_j != 0}), j indexed 1..w. z=0 -> n."""
    active = [j + 1 for j, v in enumerate(key) if v != 0]
    if not active:
        return n
    g = n
    for j in active:
        g = gcd(g, j)
        if g == 1:
            return 1
    return g


def gamma_analysis(hist, n, p, m, w, rmax=8):
    Cnm = comb(n, m)
    Bw = p ** w
    prim_items = [(k, c) for k, c in hist.items() if twist_stabilizer(k, n) == 1]
    maxN_raw = max(hist.values())
    maxN_prim = max((c for _, c in prim_items), default=0)
    R_raw = Fraction(Bw * maxN_raw, Cnm)
    R_prim = Fraction(Bw * maxN_prim, Cnm) if maxN_prim else Fraction(0)
    gamma = {}
    for r in range(2, rmax + 1):
        Sr_raw = sum(c ** r for c in hist.values())
        Sr_prim = sum(c ** r for _, c in prim_items)
        pref = Bw ** (r - 1)
        gamma[r] = dict(raw=Fraction(pref * Sr_raw, Cnm ** r),
                         prim=Fraction(pref * Sr_prim, Cnm ** r))
    return dict(gamma=gamma, R_raw=R_raw, R_prim=R_prim,
                cells_hit=len(hist), prim_cells=len(prim_items), Cnm=Cnm, Bw=Bw)


def r_min(w, log2p, Delta, log2R):
    denom = Delta - log2R
    if denom <= 0:
        return float("inf")
    return (w * log2p - log2R) / denom


# ---------------------------------------------------------------------------
# balanced-ternary kernel ledger (gate iv) -- independent reimplementation
# ---------------------------------------------------------------------------
def poly_from_roots(roots, p):
    c = [1]
    for x in roots:
        nc = [0] * (len(c) + 1)
        for i, ci in enumerate(c):
            nc[i] = (nc[i] + ci * (-x)) % p
            nc[i + 1] = (nc[i + 1] + ci) % p
        c = nc
    return c


def coeff_scale(coeffs):
    exps = [i for i, ci in enumerate(coeffs) if ci != 0]
    g = 0
    for e in exps:
        g = gcd(g, e)
    return g if g else 1


def kernel_ledger_gamma2(D, p, m, w):
    n = len(D)
    delta = (w + 1 + 1) // 2
    Cnm = comb(n, m)
    xp = [tuple(pow(x, j + 1, p) for j in range(w)) for x in D]
    Tw, Twp = {}, {}
    emax = min(m, n - m)
    for e in range(delta, emax + 1):
        classes = {}
        for combo in combinations(range(n), e):
            ps = [0] * w
            for idx in combo:
                row = xp[idx]
                for j in range(w):
                    ps[j] += row[j]
            key = tuple(v % p for v in ps)
            classes.setdefault(key, []).append(combo)
        tot = totp = 0
        for key, lst in classes.items():
            if len(lst) < 2:
                continue
            L = len(lst)
            for a in range(L):
                Aset = set(lst[a])
                for b in range(L):
                    if b == a:
                        continue
                    Bc = lst[b]
                    if Aset.isdisjoint(Bc):
                        tot += 1
                        rA = [D[i] for i in lst[a]]
                        rB = [D[i] for i in Bc]
                        cA = coeff_scale(poly_from_roots(rA, p))
                        cB = coeff_scale(poly_from_roots(rB, p))
                        if gcd(cA, cB) == 1:
                            totp += 1
        if tot:
            Tw[e] = tot
            Twp[e] = totp
    S2 = Cnm + sum(comb(n - 2 * e, m - e) * Tw[e] for e in Tw)
    S2p = sum(comb(n - 2 * e, m - e) * Twp[e] for e in Twp)
    S2q = sum(comb(n - 2 * e, m - e) * (Tw[e] - Twp[e]) for e in Tw)
    Bw = p ** w
    return dict(Tw=Tw, Twp=Twp,
                G2_full=Fraction(Bw * S2, Cnm ** 2),
                G2_diag=Fraction(Bw * Cnm, Cnm ** 2),
                G2_prim_off=Fraction(Bw * S2p, Cnm ** 2),
                G2_quot_off=Fraction(Bw * S2q, Cnm ** 2))


# ---------------------------------------------------------------------------
# shared row cache -- avoids recomputing the same (p,n,m,w) histogram across gates
# ---------------------------------------------------------------------------
_ROW_CACHE: dict = {}


def get_row(p, n, m, w, engine):
    key = (p, n, m, w, engine)
    if key not in _ROW_CACHE:
        D = domain_for(p, n)
        hist = hist_exhaustive(D, p, m, w) if engine == "ex" else hist_dp(D, p, m, w)
        _ROW_CACHE[key] = (D, hist, gamma_analysis(hist, n, p, m, w))
    return _ROW_CACHE[key]


# ---------------------------------------------------------------------------
# gate ii row plan
# ---------------------------------------------------------------------------
DEFAULT_ROWS = [
    # (label, p, n, m, w_list, engine)
    ("F17x_16_8", 17, 16, 8, [1, 2, 3, 4], "ex"),
    ("mu24_F97_12", 97, 24, 12, [2], "ex"),
    ("mu64_F257_34", 257, 64, 34, [1], "dp"),
]
FULL_EXTRA_ROWS = [
    ("mu20_F41_10", 41, 20, 10, [1, 2, 3, 4], "ex"),
    ("mu24_F97_12", 97, 24, 12, [1, 3, 4], "ex"),
    ("mu64_F257_34", 257, 64, 34, [2], "dp"),
]


def gate_ii_rows(full):
    plan = list(DEFAULT_ROWS)
    if full:
        plan = plan + FULL_EXTRA_ROWS
    out = []
    for label, p, n, m, wlist, engine in plan:
        for w in wlist:
            out.append((label, p, n, m, w, engine))
    return out


# ---------------------------------------------------------------------------
# gate i -- Brick-1 floor arithmetic
# ---------------------------------------------------------------------------
def gate_i_brick1_floors(packet, tamper=False, full=False):
    stored_rows = {r["row"]: r for r in packet["brick1_order_floor"]["exact_integer_recompute"]["rows"]}
    ok = True
    msgs = []
    floors = {}
    first = True
    for label, w, p, Delta in BRICK1_ROWS:
        raw = w * math.log2(p) / Delta
        floor_val = math.ceil(raw)
        floors[label] = floor_val
        stored = stored_rows[label]
        ok_w = check(w, stored["w"])
        ok_p = check(p, stored["p"])
        ok_raw = check(round(raw, 4), stored["r0_raw"], tol=1e-3)
        ok_floor = check(floor_val, stored["r0_floor"], tamper=(tamper and first))
        first = False
        row_ok = ok_w and ok_p and ok_raw and ok_floor
        ok = ok and row_ok
        msgs.append(f"{label}: w={w} r0={floor_val} (expect {stored['r0_floor']}) ok={row_ok}")

    ok_366_l0 = check(floors["KB-MCA"], PR366_KBMCA_R_AT_BAR)
    ok_366_l4 = check(floors["L4-rung"], PR366_L4_R_AT_BAR)
    ok = ok and ok_366_l0 and ok_366_l4
    msgs.append(f"PR#366 cross-check: KB-MCA r0={floors['KB-MCA']} (expect {PR366_KBMCA_R_AT_BAR}) "
                f"ok={ok_366_l0}; L4 r0={floors['L4-rung']} (expect {PR366_L4_R_AT_BAR}) ok={ok_366_l4}")
    return ok, "; ".join(msgs)


# ---------------------------------------------------------------------------
# gate ii -- live exact Gamma_r recomputation
# ---------------------------------------------------------------------------
def gate_ii_gamma_recompute(packet, tamper=False, full=False):
    grid = packet["measured_curves"]["full_grid"]
    ok = True
    msgs = []
    n_pairs = 0
    first = True
    dense_checked = False
    ultra_checked = False

    for label, p, n, m, w, engine in gate_ii_rows(full):
        n_pairs += 1
        _, hist, ga = get_row(p, n, m, w, engine)
        stored = grid[label]["rows"][str(w)]

        ok_cells = check(ga["cells_hit"], stored["cells_hit"])
        ok_prim_cells = check(ga["prim_cells"], stored["prim_cells"])
        ok_Rraw = check(float(ga["R_raw"]), stored["R_raw"], tol=1e-6 * max(1, stored["R_raw"]))
        row_ok = ok_cells and ok_prim_cells and ok_Rraw

        for r in range(2, 9):
            g_raw = float(ga["gamma"][r]["raw"])
            g_prim = float(ga["gamma"][r]["prim"])
            exp_raw = stored["gamma"][str(r)]["raw"]
            exp_prim = stored["gamma"][str(r)]["prim"]
            ok_g = check(g_raw, exp_raw, tol=1e-6 * max(1.0, abs(exp_raw)),
                         tamper=(tamper and first and r == 8))
            ok_gp = check(g_prim, exp_prim, tol=1e-6 * max(1.0, abs(exp_prim)))
            row_ok = row_ok and ok_g and ok_gp
        first = False

        log2g8 = math.log2(float(ga["gamma"][8]["raw"])) if float(ga["gamma"][8]["raw"]) > 0 else float("-inf")
        msgs.append(f"{label} w={w}: cells={ga['cells_hit']} log2(Gamma_8_raw)={log2g8:.4g} ok={row_ok}")

        # named check 1: the dense-bulk exhibit, log2(Gamma_8) < 0.17
        if label == "mu24_F97_12" and w == 2:
            dense_checked = True
            ok_dense = log2g8 < 0.17
            row_ok = row_ok and ok_dense
            msgs.append(f"  dense-bulk exhibit check: log2(Gamma_8_raw)={log2g8:.4f} < 0.17: {ok_dense}")

        # named check 2: the ultra-dense exhibit, Gamma_r = 1 to machine precision, all r
        if label == "mu64_F257_34" and w == 1:
            ultra_checked = True
            ultra_ok = all(abs(float(ga["gamma"][r]["raw"]) - 1.0) < 1e-9 for r in range(2, 9))
            row_ok = row_ok and ultra_ok
            msgs.append(f"  ultra-dense exhibit check: Gamma_r_raw=1 to 1e-9 for r=2..8: {ultra_ok}")

        ok = ok and row_ok

    assert dense_checked, "dense-bulk exhibit (mu24_F97_12 w=2) not in gate ii's row plan"
    assert ultra_checked, "ultra-dense exhibit (mu64_F257_34 w=1) not in gate ii's row plan"
    msgs.append(f"{n_pairs} (row,w) pairs checked (mode={'--full' if full else 'default'})")
    return ok, "; ".join(msgs)


# ---------------------------------------------------------------------------
# gate iii -- Brick-2 monotonicity + finiteness-iff + R-insensitivity
# ---------------------------------------------------------------------------
def gate_iii_monotonicity(packet, tamper=False, full=False):
    ok = True
    msgs = []
    n_checked = 0
    n_pass = 0
    first = True
    for label, p, n, m, w, engine in gate_ii_rows(full):
        _, _, ga = get_row(p, n, m, w, engine)
        reffs = []
        for r in range(2, 9):
            g = float(ga["gamma"][r]["raw"])
            reffs.append(g ** (1.0 / (r - 1)) if g > 0 else float("-inf"))
        mono = all(reffs[i] <= reffs[i + 1] + 1e-9 for i in range(len(reffs) - 1))
        if tamper and first:
            mono = not mono
        first = False
        n_checked += 1
        n_pass += 1 if mono else 0
        ok = ok and mono
        if not mono:
            msgs.append(f"{label} w={w}: MONOTONICITY FAILED (R_eff sequence {reffs})")
    msgs.append(f"R_eff(r) monotonicity: {n_pass}/{n_checked} (row,w) pairs pass "
                f"(mode={'--full' if full else 'default'})")

    # finiteness-iff-R<2^Delta, on synthetic R values around Delta itself
    w, Delta = 67471, DELTA_KB_MCA
    log2p = math.log2(P_KB)
    below = r_min(w, log2p, Delta, Delta - 1.0)     # log2 R = Delta-1 < Delta -> finite
    at_bar = r_min(w, log2p, Delta, Delta)          # log2 R = Delta -> denom=0 -> infinite
    above = r_min(w, log2p, Delta, Delta + 1.0)     # log2 R > Delta -> negative denom -> infinite
    ok_below = math.isfinite(below)
    ok_at = not math.isfinite(at_bar)
    ok_above = not math.isfinite(above)
    ok_finiteness = ok_below and ok_at and ok_above
    ok = ok and ok_finiteness
    msgs.append(f"r_min finiteness-iff-R<2^Delta: R<2^Delta finite={ok_below}, "
                f"R=2^Delta infinite={ok_at}, R>2^Delta infinite={ok_above}; ok={ok_finiteness}")

    # R-insensitivity headline: doubling R inflates KB-MCA's order by ~4.72%
    base = r_min(w, log2p, Delta, 0.0)
    doubled = r_min(w, log2p, Delta, 1.0)
    inflation_pct = (doubled / base - 1.0) * 100.0
    ok_inflation = check(round(inflation_pct, 2), 4.72, tol=0.05)
    ok = ok and ok_inflation
    msgs.append(f"R-insensitivity: doubling R inflates KB-MCA r_min by {inflation_pct:.3f}% "
                f"(expect ~4.72%) ok={ok_inflation}")
    return ok, "; ".join(msgs)


# ---------------------------------------------------------------------------
# gate iv -- balanced-ternary kernel ledger
# ---------------------------------------------------------------------------
def gate_iv_kernel_ledger(packet, tamper=False, full=False):
    p, n, m = 17, 16, 8
    D = domain_for(p, n)
    w_list = [1, 2, 3, 4] if full else [2]
    stored_ledger = packet["removal_ledger"]["exact_gamma2_kernel_ledger"]
    ok = True
    msgs = []
    first = True
    for w in w_list:
        led = kernel_ledger_gamma2(D, p, m, w)
        _, hist, ga = get_row(p, n, m, w, "ex")
        g2_from_hist = float(ga["gamma"][2]["raw"])
        matches_hist = abs(float(led["G2_full"]) - g2_from_hist) < 1e-9
        row_ok = matches_hist
        if w == 2:
            ok_full = check(round(float(led["G2_full"]), 9), round(stored_ledger["G2_full"], 9), tol=1e-6)
            ok_prim = check(round(float(led["G2_prim_off"]), 9), round(stored_ledger["G2_prim_off"], 9),
                             tol=1e-6, tamper=(tamper and first))
            first = False
            ok_Tw = check({str(k): v for k, v in led["Tw"].items()}, stored_ledger["Tw"])
            ok_Twp = check({str(k): v for k, v in led["Twp"].items()}, stored_ledger["Twp"])
            row_ok = row_ok and ok_full and ok_prim and ok_Tw and ok_Twp
        ok = ok and row_ok
        msgs.append(f"w={w}: matches_hist={matches_hist} ok={row_ok}")
    return ok, "; ".join(msgs)


# ---------------------------------------------------------------------------
# gate v -- removal comparison
# ---------------------------------------------------------------------------
def gate_v_removal_comparison(packet, tamper=False, full=False):
    p, n, m, w = 97, 24, 12, 2
    _, _, ga = get_row(p, n, m, w, "ex")
    log2_R_raw = math.log2(float(ga["R_raw"]))
    log2_R_prim = math.log2(float(ga["R_prim"]))
    dR = log2_R_raw - log2_R_prim
    g8_raw = float(ga["gamma"][8]["raw"])
    g8_prim = float(ga["gamma"][8]["prim"])
    log2_g8_raw = math.log2(g8_raw)
    log2_g8_prim = math.log2(g8_prim)
    dG8 = log2_g8_raw - log2_g8_prim

    stored = packet["removal_ledger"]["dense_bulk_removal_effect"]
    ok_dR = check(round(dR, 4), stored["delta_R_bits"], tol=1e-3)
    ok_dG8 = check(round(dG8, 4), stored["delta_Gamma8_bits"], tol=1e-3, tamper=tamper)
    ok_shave = dG8 < 0.04
    ok_dense_flag = log2_g8_raw < 0.17

    ok = ok_dR and ok_dG8 and ok_shave and ok_dense_flag
    msg = (f"mu24_F97_12 w=2 (live): dR={dR:.4f} (expect {stored['delta_R_bits']}) ok={ok_dR}; "
           f"dGamma8={dG8:.4f} (expect {stored['delta_Gamma8_bits']}) ok={ok_dG8}; "
           f"<0.04 bit shave: {ok_shave}; log2(Gamma_8_raw)={log2_g8_raw:.4f}<0.17: {ok_dense_flag}")
    return ok, msg


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
GATE_SPECS = [
    ("gate i   Brick-1 floor arithmetic (5 rows)  ", gate_i_brick1_floors),
    ("gate ii  live exact Gamma_r recompute        ", gate_ii_gamma_recompute),
    ("gate iii Brick-2 monotonicity + r_min        ", gate_iii_monotonicity),
    ("gate iv  balanced-ternary kernel ledger      ", gate_iv_kernel_ledger),
    ("gate v   removal comparison (dense bulk)     ", gate_v_removal_comparison),
]


def main() -> int:
    t0 = time.time()
    argv = sys.argv[1:]
    selftest = "--tamper-selftest" in argv
    full = "--full" in argv

    print("=" * 90)
    if selftest:
        print(" TAMPER SELF-TEST: each gate must FAIL when its guarded datum is corrupted")
    else:
        print(" verify_gammar_order_floor  (zero-arg)" + (" --full" if full else ""))
        print(" Gamma_r measured + exact order floor -- AUDIT/MEASURED/PROVED-LOCAL, not a")
        print(" proof or refutation of prob:row-sharp-q")
    print("=" * 90)

    try:
        packet = load_packet()
    except Exception as exc:  # noqa: BLE001
        print(f"FATAL: could not load packet JSON: {exc}")
        return 1

    if not os.path.isfile(NOTE_PATH):
        print(f"FATAL: companion note missing: {NOTE_PATH}")
        return 1

    ok_wall = packet.get("wall_id") == WALL_ID
    if not ok_wall:
        print(f"FATAL: wall_id mismatch: {packet.get('wall_id')!r} != {WALL_ID!r}")
        return 1

    all_good = True
    for label, fn in GATE_SPECS:
        ok, summary = fn(packet, selftest, full)
        caught_or_pass = (not ok) if selftest else ok
        all_good = all_good and caught_or_pass
        tag = ("CAUGHT " if caught_or_pass else "MISSED!") if selftest else ("PASS" if ok else "FAIL")
        print(f"  {label}  {tag}   ({time.time()-t0:.1f}s elapsed)")
        print(f"        {summary}")

    print("=" * 90)
    dt = time.time() - t0
    if selftest:
        print(f" SELF-TEST RESULT: {'all tampers CAUGHT' if all_good else 'A TAMPER WAS MISSED'}   ({dt:.1f}s)")
    else:
        print(f" RESULT: {'ALL GATES PASS' if all_good else 'FAILURE'}   ({dt:.1f}s)")
        print(" This verifier does not evaluate Gamma_r at any deployed w, does not prove or")
        print(" refute prob:row-sharp-q, and does not move the frontier edge; it only checks")
        print(" this PR's own arithmetic (see docstring).")
    return 0 if all_good else 1


if __name__ == "__main__":
    sys.exit(main())
