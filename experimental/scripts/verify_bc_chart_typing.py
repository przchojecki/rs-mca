#!/usr/bin/env python3
"""First deployed-row chart-typing certificate for prob:saturated-bc.

Object: the simple-pole/rank-one cell (prop:pole-line, prop:rank-one-floor)
typed at BOTH deployed MCA adjacent rows (KoalaBear a+ = 1116048,
Mersenne-31 a+ = 1116024), with the first-match PLACEMENT DECIDED BY
COMPUTATION -- boundary-Q-owned vs fresh named (b)-cell are BOTH valid
certificate outcomes and neither is presupposed.  The verdict field is the
computed outcome.

Gates:
  1. Placement computation replay at toy scale (F_73: n=24, K=12, m=15,
     w'=3; F_{17^2}: n=16, K=6, m=9, w'=3; harnesses ported from the
     in-tree #715 Gate B/C machinery in
     verify_lineray_census_rerecording.py): construct pole-line words
     f_alpha + zeta g_alpha, verify the module element
     (X - alpha, U_z - zeta) in M_U at shifted degree w'+1, compute the
     shifted weak-Popov profile d1 exactly, and CLASSIFY: d1 = w'+1 is the
     boundary-Q profile (prop:boundary-q; bc_section.tex: interior is
     w'+2 <= d1 <= floor((n-K+1)/2)).
  2. Deployed exact integers, ALL FOUR ROWS TWO INDEPENDENT WAYS
     (Legendre floor-sum exponents + product tree, anchored at the
     smallest a and stepping UP; Kummer carry-count exponents + heap
     merge, anchored at the largest a and stepping DOWN; the two big-int
     routes are cross-asserted for exact equality -- gate name
     two_routes_agree_exactly_on_all_four_rows).  The M31 3.2589-bit
     margin is adjacency-critical; any slip near 3.26 bits is fatal.
  3. Non-pencil exclusion arithmetic: full sweep of the pencil cap
     floor((n-g)/(omega-g)) over 0 <= g < omega at both MCA rows (max is
     n - omega + 1 = a+ + 1 at g = omega - 1), against the proved
     heaviest-fiber witness floor B_B(a+); plus toy locator-matrix rank
     tests (a pencil is a 2-dimensional space; the witness locators span
     rank >= 3 at both toys).
  4. Oracle consumption + statement pins: #715 lineray cert (payload
     hash; witness-fiber calibration values), bc_one_pencil_omega cert
     (payload hash; corrected omega -- cite, do not re-park), #690
     envelope rung ledger cert (payload hash; the -0.3938-bit M31
     watch-item), budget-fit cert (old-style, no payload field: consumed
     by file sha256 + field equality), #721 note (no JSON cert in-tree:
     consumed by file sha256 + full replay of its printed d=1
     collision-literal census + content pins), and line-hash pins on
     every cited statement in grande_finale.tex /
     asymptotic_rs_mca_frontiers.tex / bc_section.tex.

Framing: per-row chart VERIFICATION progress on prob:saturated-bc -- one
named cell typed, enumeratively exact (CITED-THEOREM), budget fit
CONDITIONAL_ON_NAMED_INPUT (depth-w max-fiber / row-sharp Q).  NOT a
resolution of prob:saturated-bc; no claim on U(a_0+1) <= B*.

Status: EXPERIMENTAL / AUDIT
"""
from __future__ import annotations

import argparse
import hashlib
import heapq
import json
import math
import sys
from pathlib import Path
from typing import Any

STATUS = "EXPERIMENTAL / AUDIT"
BASE_SHA = "2633895a66d3edf516120a87b2eb18c994f977ab"
CERT_REL = Path(
    "experimental/data/certificates/bc-chart-typing/bc_chart_typing.json")
GF_REL = Path("experimental/grande_finale.tex")
FRONT_REL = Path("experimental/asymptotic_rs_mca_frontiers.tex")
BCSEC_REL = Path("experimental/grande_finale_work/bc_section.tex")
ORACLE_715_REL = Path(
    "experimental/data/certificates/lineray-census-rerecording/"
    "lineray_census_rerecording.json")
ORACLE_OMEGA_REL = Path(
    "experimental/data/certificates/bc-one-pencil-omega/"
    "bc_one_pencil_omega.json")
ORACLE_690_REL = Path(
    "experimental/data/certificates/envelope-rung-ledger/"
    "envelope_rung_ledger.json")
BUDGET_FIT_REL = Path(
    "experimental/data/certificates/frontier-adjacent/"
    "saturated_bc_budget_fit_v1.json")
NOTE_721_REL = Path(
    "experimental/notes/thresholds/"
    "canonical_reduced_rational_host_compiler.md")

# statement pins: (kind, key, expected_line); kind "label" -> \label{key},
# kind "content" -> literal substring; first hit must sit at expected_line.
GF_PINS = (
    ("label", "prob:saturated-bc", 2191),
    ("label", "cor:bc-one-pencil", 1764),
    ("label", "thm:bc-moving-root", 1735),
    ("label", "def:projective-locator-pencil", 1722),
    ("label", "prop:boundary-q", 1475),
    ("label", "prop:bc-not-q", 2120),
    ("label", "def:q-row-atom", 2043),
    ("label", "def:first-match-ledger", 148),
    ("label", "rem:bc-status-after-moving-root", 1785),
    ("label", "prop:pole-line", 583),
    ("label", "prop:rank-one-floor", 1523),
    ("label", "prop:rank-one-distinct-slope-floor", 1546),
    ("label", "prop:line-ray-saturation", 1867),
    ("label", "thm:finite", 2022),
    ("label", "prop:extension-cell-target", 402),
    ("label", "thm:near-rational", 1350),
    ("label", "cor:near-rational-line", 1381),
    ("label", "prop:lattice-split", 1336),
    ("label", "prop:slope-elimination", 1320),
    ("content", "In all four rows \\(p>H_{\\rm ext}\\)", 425),
)
FRONT_PINS = (
    ("label", "thm:exact-list-line-bijection", 2097),
    ("label", "cor:exact-prefix-ray-realization", 2157),
)
BCSEC_PINS = (
    ("content", "An interior balanced profile", 24),
    ("content", "The excluded endpoint", 29),
)
NOTE_721_PINS = (
    ("content",
     "`d = 1` formulas below are retained as a collision-literal audit", 14),
    ("content", "F_RH = {S in binom(D,5):sum_{x in S}x=0 in F_17},", 447),
    ("content", "The full multiplicity certificate is", 451),
    ("content", "supports = LineRay pairs = 76,", 461),
)

# printed d=1 collision-literal multiplicity certificate (#721 Sec. 7)
CENSUS_721 = {0: 4, 1: 4, 2: 5, 3: 7, 4: 5, 5: 6, 6: 4, 7: 4,
              8: 6, 9: 5, 10: 5, 11: 7, 12: 3, 14: 5, 15: 3, 16: 3}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def payload_hash(obj: dict[str, Any]) -> str:
    clone = dict(obj)
    clone.pop("payload_sha256", None)
    blob = json.dumps(clone, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _lg2(x: int) -> float:
    e = x.bit_length() - 1
    if e <= 80:
        return math.log2(x)
    return math.log2(x >> (e - 80)) + (e - 80)


def lg2_display(x: int) -> str:
    """display-grade log2 string (top-80-bit mantissa; no verdict uses it)."""
    return "%.4f" % _lg2(x)


# ======================================================================
# Gate 4a: statement pins
# ======================================================================
def scan_pins(root: Path) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for rel, pins in ((GF_REL, GF_PINS), (FRONT_REL, FRONT_PINS),
                      (BCSEC_REL, BCSEC_PINS), (NOTE_721_REL, NOTE_721_PINS)):
        lines = (root / rel).read_text(encoding="utf-8").splitlines()
        found: dict[str, Any] = {}
        for kind, key, expected in pins:
            needle = ("\\label{%s}" % key) if kind == "label" else key
            hit = None
            for i, line in enumerate(lines, 1):
                if needle in line:
                    hit = (i, line)
                    break
            assert hit is not None, "pin missing: %s in %s" % (key, rel.name)
            assert hit[0] == expected, \
                "pin moved: %s at L%d (expected L%d)" % (key, hit[0], expected)
            found[key] = {
                "kind": kind,
                "line": hit[0],
                "sha256_line": hashlib.sha256(
                    hit[1].encode("utf-8")).hexdigest()[:16],
            }
        out[rel.name] = found
    return out


# ======================================================================
# F_73 layer (Gate 1a) -- ported from verify_lineray_census_rerecording.py
# (#715 Gate B harness; the placement computation is new)
# ======================================================================
P = 73
N = 24
K = 12
M = 15
W = M - K       # w' = 3
OMEGA = N - M   # 9
SHIFT = K - 1


def inv(a: int) -> int:
    return pow(a, P - 2, P)


def pnorm(f):
    f = list(f)
    while f and f[-1] == 0:
        f.pop()
    return f


def pdeg(f):
    return len(f) - 1


def padd(f, g):
    L = max(len(f), len(g))
    return pnorm([((f[i] if i < len(f) else 0) + (g[i] if i < len(g) else 0))
                  % P for i in range(L)])


def psub(f, g):
    L = max(len(f), len(g))
    return pnorm([((f[i] if i < len(f) else 0) - (g[i] if i < len(g) else 0))
                  % P for i in range(L)])


def pscale(f, c):
    c %= P
    return pnorm([c * a % P for a in f])


def pshift(f, k):
    return ([0] * k + list(f)) if f else []


def pmul(f, g):
    if not f or not g:
        return []
    out = [0] * (len(f) + len(g) - 1)
    for i, a in enumerate(f):
        if a:
            for j, b in enumerate(g):
                out[i + j] = (out[i + j] + a * b) % P
    return pnorm(out)


def pdivmod(f, g):
    assert g
    f = list(f)
    q = [0] * max(0, len(f) - len(g) + 1)
    ginv = inv(g[-1])
    while len(f) >= len(g) and pnorm(f):
        f = pnorm(f)
        if len(f) < len(g):
            break
        c = f[-1] * ginv % P
        d = len(f) - len(g)
        q[d] = c
        for i, b in enumerate(g):
            f[d + i] = (f[d + i] - c * b) % P
        f = pnorm(f)
    return pnorm(q), pnorm(f)


def pgcd(f, g):
    while g:
        f, g = g, pdivmod(f, g)[1]
    return f


def peval(f, x):
    r = 0
    for a in reversed(f):
        r = (r * x + a) % P
    return r


def build_domain():
    for g in range(2, P):
        seen, x = set(), 1
        for _ in range(P - 1):
            x = x * g % P
            seen.add(x)
        if len(seen) == P - 1:
            dom = sorted(pow(pow(g, 3, P), j, P) for j in range(N))
            assert len(set(dom)) == N
            return dom
    raise AssertionError


D = build_domain()
LAMBDA = [1]
for _x in D:
    LAMBDA = pmul(LAMBDA, [(-_x) % P, 1])
assert LAMBDA == [P - 1] + [0] * (N - 1) + [1]


def interpolate_full(vals):
    out = []
    for i, xi in enumerate(D):
        num, den = [1], 1
        for j, xj in enumerate(D):
            if i == j:
                continue
            num = pmul(num, [(-xj) % P, 1])
            den = den * ((xi - xj) % P) % P
        out = padd(out, pscale(num, vals[i] * inv(den)))
    return out


def wdeg_pivot(row):
    Wp, Np = row
    e1 = pdeg(Wp) if Wp else -10 ** 9
    e2 = (pdeg(Np) - SHIFT) if Np else -10 ** 9
    return (max(e1, e2), 1 if e2 >= e1 else 0)


def popov_d1(U):
    """d1 of M_U via shifted weak Popov reduction (verified properties)."""
    rows = [([1], interpolate_full(U)), ([], LAMBDA[:])]
    for _ in range(10000):
        (wd0, pv0), (wd1, pv1) = wdeg_pivot(rows[0]), wdeg_pivot(rows[1])
        if pv0 != pv1:
            break
        i, j = (0, 1) if wd0 <= wd1 else (1, 0)
        ri, rj = rows[i], rows[j]
        wi, wj = (wd0, wd1) if i == 0 else (wd1, wd0)
        piv = pv0
        c = rj[piv][-1] * inv(ri[piv][-1]) % P
        delta = wj - wi
        rows[j] = (psub(rj[0], pshift(pscale(ri[0], c), delta)),
                   psub(rj[1], pshift(pscale(ri[1], c), delta)))
    else:
        raise AssertionError("popov did not terminate")
    rows.sort(key=lambda r: wdeg_pivot(r)[0])
    g1, g2 = rows
    d1, d2 = wdeg_pivot(g1)[0], wdeg_pivot(g2)[0]
    for (Wp, Np) in (g1, g2):
        for idx, x in enumerate(D):
            assert peval(Wp, x) * U[idx] % P == peval(Np, x)
    det = psub(pmul(g1[0], g2[1]), pmul(g1[1], g2[0]))
    qd, rd = pdivmod(det, LAMBDA)
    assert rd == [] and pdeg(qd) == 0
    assert pdeg(pgcd(g1[0], g2[0])) == 0
    assert d1 + d2 == N - K + 1
    assert wdeg_pivot(g1)[1] != wdeg_pivot(g2)[1]
    return d1


def heaviest_fiber_members(msize, depth):
    """heaviest depth-`depth` fiber over F_73 msize-subsets of D, WITH the
    member subsets (windowed leading-coefficient DFS, lex order)."""
    counts: dict[tuple, int] = {}
    members: dict[tuple, list] = {}

    def rec(start, chosen, w, idxs):
        if chosen == msize:
            z = tuple(w[1:depth + 1])
            counts[z] = counts.get(z, 0) + 1
            members.setdefault(z, []).append(tuple(idxs))
            return
        need = msize - chosen
        for idx in range(start, N - need + 1):
            mx = (-D[idx]) % P
            nw = [0] * (depth + 1)
            for j in range(depth + 1):
                v = w[j]
                if j > 0:
                    v = (v + mx * w[j - 1]) % P
                nw[j] = v
            idxs.append(idx)
            rec(idx + 1, chosen + 1, nw, idxs)
            idxs.pop()

    rec(0, 0, [1] + [0] * depth, [])
    assert sum(counts.values()) == math.comb(N, msize)
    best = max(counts.values())
    zstar = min(z for z, c in counts.items() if c == best)
    return list(zstar), members[zstar]


def rank_mod_p(mat, p):
    mat = [row[:] for row in mat]
    r = 0
    for c in range(len(mat[0]) if mat else 0):
        piv = None
        for i in range(r, len(mat)):
            if mat[i][c] % p:
                piv = i
                break
        if piv is None:
            continue
        mat[r], mat[piv] = mat[piv], mat[r]
        pinv = pow(mat[r][c], p - 2, p)
        mat[r] = [(x * pinv) % p for x in mat[r]]
        for i in range(len(mat)):
            if i != r and mat[i][c] % p:
                f = mat[i][c]
                mat[i] = [(x - f * y) % p for x, y in zip(mat[i], mat[r])]
        r += 1
        if r == len(mat):
            break
    return r


def gate1_f73() -> dict[str, Any]:
    zstar, members = heaviest_fiber_members(M, W)
    assert len(members) == 13  # #715 Gate B boundary value
    floor_ceil = -(-math.comb(N, M) // P ** W)
    assert len(members) >= floor_ceil

    # prefix word U_z and the pole line at the smallest alpha not in D
    Pz = [0] * (M + 1)
    Pz[M] = 1
    for h, zz in enumerate(zstar, 1):
        Pz[M - h] = zz
    alpha = min(a for a in range(P) if a not in set(D))
    fa = [Pz and peval(Pz, D[i]) * inv((D[i] - alpha) % P) % P
          for i in range(N)]
    ga = [(-inv((D[i] - alpha) % P)) % P for i in range(N)]

    # slopes via prop:pole-line: zeta_S = U_z(alpha) - ell_S(alpha)
    Ua = peval(Pz, alpha)
    slope_of: dict[int, list] = {}
    for T in members:
        lam = [1]
        for idx in T:
            lam = pmul(lam, [(-D[idx]) % P, 1])
        slope_of.setdefault((Ua - peval(lam, alpha)) % P, []).append(list(T))

    # PLACEMENT COMPUTATION per distinct slope: module element + exact d1
    d1_rows = []
    interior_lo, interior_hi = W + 2, (N - K + 1) // 2
    for zeta in sorted(slope_of):
        Uw = [(fa[i] + zeta * ga[i]) % P for i in range(N)]
        Wel = [(-alpha) % P, 1]                 # X - alpha
        Nel = psub(Pz, [zeta])                  # U_z - zeta
        for i in range(N):
            assert peval(Wel, D[i]) * Uw[i] % P == peval(Nel, D[i]), \
                "module element fails"
        wdeg_el = max(pdeg(Wel), pdeg(Nel) - SHIFT)
        assert wdeg_el == W + 1, "shifted degree of (X-a, U_z-zeta)"
        d1 = popov_d1(Uw)
        d1_rows.append({"zeta": zeta, "d1": d1,
                        "module_element_wdeg": wdeg_el,
                        "n_fiber_members_at_slope": len(slope_of[zeta])})
    d1_vals = sorted({r["d1"] for r in d1_rows})
    near_rational = sum(1 for r in d1_rows if r["d1"] <= W)
    boundary = sum(1 for r in d1_rows if r["d1"] == W + 1)
    interior = sum(1 for r in d1_rows
                   if interior_lo <= r["d1"] <= interior_hi)
    assert near_rational <= 1  # cor:near-rational-line

    # locator matrix rank (Gate 3 toy half): pencil would force rank <= 2
    locs = []
    for T in members:
        lam = [1]
        for idx in T:
            lam = pmul(lam, [(-D[idx]) % P, 1])
        WS, rem = pdivmod(LAMBDA, lam)
        assert rem == []
        locs.append([WS[t] if t < len(WS) else 0 for t in range(OMEGA + 1)])
    rank = rank_mod_p(locs, P)
    cap_sweep_max = max((N - g) // (OMEGA - g) for g in range(OMEGA))

    return {
        "field": {"p": P, "q": P, "n": N, "K": K, "m": M, "w_prime": W,
                  "omega": OMEGA,
                  "note": "p = q toy: exercises the placement computation "
                          "only; the extension-valued case is the F_{17^2} "
                          "layer"},
        "z_star": zstar,
        "fiber_size": len(members),
        "fiber_members": [list(T) for T in members],
        "ceil_floor": floor_ceil,
        "alpha": alpha,
        "n_distinct_slopes": len(slope_of),
        "slope_collisions_at_alpha": len(members) - len(slope_of),
        "interior_profile_range": [interior_lo, interior_hi],
        "d1_rows": d1_rows,
        "d1_values": d1_vals,
        "counts": {"near_rational": near_rational, "boundary": boundary,
                   "interior": interior},
        "locator_matrix_rank": rank,
        "pencil_rank_cap": 2,
        "counting_cap_max_over_g": cap_sweep_max,
        "counting_cap_equals_n_minus_omega_plus_1": cap_sweep_max
        == N - OMEGA + 1,
        "counting_exclusion_bites": len(members) > cap_sweep_max,
        "rank_exclusion_bites": rank > 2,
        "all_pass": True,
    }


# ======================================================================
# F_{17^2} layer (Gate 1b) -- ported from the #715 Gate C harness
# ======================================================================
PB = 17
NR2 = 3
Q2 = PB * PB
N2 = 16
K2 = 6
M2 = 9
W2 = M2 - K2      # w' = 3
OM2 = N2 - M2     # 7
SHIFT2 = K2 - 1

# element e = a + 17*b  <->  a + b*t with t^2 = 3
ADD2 = [[0] * Q2 for _ in range(Q2)]
MUL2 = [[0] * Q2 for _ in range(Q2)]
NEG2 = [0] * Q2
INV2 = [0] * Q2
for _e1 in range(Q2):
    _a1, _b1 = _e1 % PB, _e1 // PB
    NEG2[_e1] = ((-_a1) % PB) + PB * ((-_b1) % PB)
    for _e2 in range(Q2):
        _a2, _b2 = _e2 % PB, _e2 // PB
        ADD2[_e1][_e2] = ((_a1 + _a2) % PB) + PB * ((_b1 + _b2) % PB)
        MUL2[_e1][_e2] = ((_a1 * _a2 + NR2 * _b1 * _b2) % PB) \
            + PB * ((_a1 * _b2 + _a2 * _b1) % PB)
for _e in range(1, Q2):
    _a, _b = _e % PB, _e // PB
    _nrm = (_a * _a - NR2 * _b * _b) % PB
    _ni = pow(_nrm, PB - 2, PB)
    INV2[_e] = (_a * _ni) % PB + PB * ((-_b * _ni) % PB)
SUB2 = [[ADD2[x][NEG2[y]] for y in range(Q2)] for x in range(Q2)]
for _e in range(1, Q2):
    assert MUL2[_e][INV2[_e]] == 1

D2 = list(range(1, 17))   # F_17^* inside F_289 (b = 0)


def pnorm2(f):
    f = list(f)
    while f and f[-1] == 0:
        f.pop()
    return f


def padd2(f, g):
    L = max(len(f), len(g))
    return pnorm2([ADD2[f[i] if i < len(f) else 0][g[i] if i < len(g) else 0]
                   for i in range(L)])


def psub2(f, g):
    L = max(len(f), len(g))
    return pnorm2([SUB2[f[i] if i < len(f) else 0][g[i] if i < len(g) else 0]
                   for i in range(L)])


def pscale2(f, c):
    return pnorm2([MUL2[c][a] for a in f])


def pshift2(f, k):
    return ([0] * k + list(f)) if f else []


def pmul2(f, g):
    if not f or not g:
        return []
    out = [0] * (len(f) + len(g) - 1)
    for i, a in enumerate(f):
        if a:
            ra = MUL2[a]
            for j, b in enumerate(g):
                if b:
                    out[i + j] = ADD2[out[i + j]][ra[b]]
    return pnorm2(out)


def pdivmod2(f, g):
    assert g
    f = list(f)
    q = [0] * max(0, len(f) - len(g) + 1)
    ginv = INV2[g[-1]]
    while len(f) >= len(g) and pnorm2(f):
        f = pnorm2(f)
        if len(f) < len(g):
            break
        c = MUL2[f[-1]][ginv]
        d = len(f) - len(g)
        q[d] = c
        for i, b in enumerate(g):
            f[d + i] = SUB2[f[d + i]][MUL2[c][b]]
        f = pnorm2(f)
    return pnorm2(q), pnorm2(f)


def pgcd2(f, g):
    while g:
        f, g = g, pdivmod2(f, g)[1]
    return f


def peval2(f, x):
    r = 0
    for a in reversed(f):
        r = ADD2[MUL2[r][x]][a]
    return r


LAMBDA2 = [1]
for _x in D2:
    LAMBDA2 = pmul2(LAMBDA2, [NEG2[_x], 1])
assert LAMBDA2 == [NEG2[1]] + [0] * (N2 - 1) + [1]  # X^16 - 1


def interpolate_full2(vals):
    out = []
    for i, xi in enumerate(D2):
        num, den = [1], 1
        for j, xj in enumerate(D2):
            if i == j:
                continue
            num = pmul2(num, [NEG2[xj], 1])
            den = MUL2[den][SUB2[xi][xj]]
        out = padd2(out, pscale2(num, MUL2[vals[i]][INV2[den]]))
    return out


def wdeg_pivot2(row):
    Wp, Np = row
    e1 = (len(Wp) - 1) if Wp else -10 ** 9
    e2 = (len(Np) - 1 - SHIFT2) if Np else -10 ** 9
    return (max(e1, e2), 1 if e2 >= e1 else 0)


def popov_d1_2(U):
    rows = [([1], interpolate_full2(U)), ([], LAMBDA2[:])]
    for _ in range(10000):
        (wd0, pv0), (wd1, pv1) = wdeg_pivot2(rows[0]), wdeg_pivot2(rows[1])
        if pv0 != pv1:
            break
        i, j = (0, 1) if wd0 <= wd1 else (1, 0)
        ri, rj = rows[i], rows[j]
        wi, wj = (wd0, wd1) if i == 0 else (wd1, wd0)
        piv = pv0
        c = MUL2[rj[piv][-1]][INV2[ri[piv][-1]]]
        delta = wj - wi
        rows[j] = (psub2(rj[0], pshift2(pscale2(ri[0], c), delta)),
                   psub2(rj[1], pshift2(pscale2(ri[1], c), delta)))
    else:
        raise AssertionError("popov2 did not terminate")
    rows.sort(key=lambda r: wdeg_pivot2(r)[0])
    g1, g2 = rows
    d1, d2 = wdeg_pivot2(g1)[0], wdeg_pivot2(g2)[0]
    for (Wp, Np) in (g1, g2):
        for idx, x in enumerate(D2):
            assert MUL2[peval2(Wp, x)][U[idx]] == peval2(Np, x)
    det = psub2(pmul2(g1[0], g2[1]), pmul2(g1[1], g2[0]))
    qd, rd = pdivmod2(det, LAMBDA2)
    assert rd == [] and len(qd) == 1
    assert len(pgcd2(g1[0], g2[0])) == 1
    assert d1 + d2 == N2 - K2 + 1
    assert wdeg_pivot2(g1)[1] != wdeg_pivot2(g2)[1]
    return d1


def fibers2(msize, depth):
    """{prefix tuple (base-field ints): [subsets (index tuples)]} over
    msize-subsets of D2."""
    import itertools
    fib: dict[tuple, list] = {}
    for T in itertools.combinations(range(N2), msize):
        xs = [D2[i] % PB for i in T]
        e = [1] + [0] * depth
        for x in xs:
            for h in range(depth, 0, -1):
                e[h] = (e[h] + x * e[h - 1]) % PB
        z = tuple((pow(-1, h, PB) * e[h]) % PB for h in range(1, depth + 1))
        fib.setdefault(z, []).append(T)
    return fib


def rank2(mat):
    mat = [row[:] for row in mat]
    r = 0
    for c in range(len(mat[0]) if mat else 0):
        piv = None
        for i in range(r, len(mat)):
            if mat[i][c]:
                piv = i
                break
        if piv is None:
            continue
        mat[r], mat[piv] = mat[piv], mat[r]
        pinv = INV2[mat[r][c]]
        mat[r] = [MUL2[pinv][x] for x in mat[r]]
        for i in range(len(mat)):
            if i != r and mat[i][c]:
                f = mat[i][c]
                mat[i] = [SUB2[x][MUL2[f][y]] for x, y in zip(mat[i], mat[r])]
        r += 1
        if r == len(mat):
            break
    return r


def gate1_fp2() -> dict[str, Any]:
    fib3 = fibers2(M2, W2)
    best3 = max(len(v) for v in fib3.values())
    zstar = min(z for z, v in fib3.items() if len(v) == best3)
    fib2 = fibers2(M2, W2 - 1)
    wit = fib2[zstar[:W2 - 1]]
    assert best3 == 5 and len(wit) == 40  # #715 Gate C values

    Pz = [0] * (M2 + 1)
    Pz[M2] = 1
    for h, zz in enumerate(zstar, 1):
        Pz[M2 - h] = zz
    wit_lams = []
    for T in wit:
        f = [1]
        for idx in T:
            f = pmul2(f, [NEG2[D2[idx]], 1])
        wit_lams.append(f)

    interior_lo, interior_hi = W2 + 2, (N2 - K2 + 1) // 2
    alpha_rows = []
    for alpha in (17, 18, 288):     # the #715 tested alphas (all not in DuB)
        Ua = peval2(Pz, alpha)
        fa = [MUL2[peval2(Pz, D2[i])][INV2[SUB2[D2[i]][alpha]]]
              for i in range(N2)]
        ga = [MUL2[NEG2[1]][INV2[SUB2[D2[i]][alpha]]] for i in range(N2)]
        slope_of: dict[int, int] = {}
        for lam in wit_lams:
            z = SUB2[Ua][peval2(lam, alpha)]
            slope_of[z] = slope_of.get(z, 0) + 1
        d1s = []
        for zeta in sorted(slope_of):
            Uw = [ADD2[fa[i]][MUL2[zeta][ga[i]]] for i in range(N2)]
            Wel = [NEG2[alpha], 1]
            Nel = psub2(Pz, [zeta])
            for i in range(N2):
                assert MUL2[peval2(Wel, D2[i])][Uw[i]] == peval2(Nel, D2[i])
            assert max(len(Wel) - 1, len(Nel) - 1 - SHIFT2) == W2 + 1
            d1s.append(popov_d1_2(Uw))
        near_rational = sum(1 for d in d1s if d <= W2)
        assert near_rational <= 1
        alpha_rows.append({
            "alpha": alpha,
            "n_distinct_slopes": len(slope_of),
            "slope_collisions": len(wit) - len(slope_of),
            "d1_values": sorted(set(d1s)),
            "n_boundary": sum(1 for d in d1s if d == W2 + 1),
            "n_near_rational": near_rational,
            "n_interior": sum(1 for d in d1s
                              if interior_lo <= d <= interior_hi),
        })

    locs = []
    for lam in wit_lams:
        WS, rem = pdivmod2(LAMBDA2, lam)
        assert rem == []
        locs.append([WS[t] if t < len(WS) else 0 for t in range(OM2 + 1)])
    rank = rank2(locs)
    cap_sweep_max = max((N2 - g) // (OM2 - g) for g in range(OM2))

    return {
        "field": {"p": PB, "q": Q2, "tower": "F_289 = F_17[t]/(t^2-3)",
                  "encoding": "element a + b*t stored as integer a + 17*b",
                  "n": N2, "K": K2, "m": M2, "w_prime": W2, "omega": OM2},
        "z_star": list(zstar),
        "heaviest_depth_wprime_fiber": best3,
        "witness_fiber_depth": W2 - 1,
        "witness_fiber_size": len(wit),
        "witness_fiber_members": [list(T) for T in wit],
        "interior_profile_range": [interior_lo, interior_hi],
        "alpha_rows": alpha_rows,
        "locator_matrix_rank": rank,
        "pencil_rank_cap": 2,
        "counting_cap_max_over_g": cap_sweep_max,
        "counting_cap_equals_n_minus_omega_plus_1": cap_sweep_max
        == N2 - OM2 + 1,
        "counting_exclusion_bites": len(wit) > cap_sweep_max,
        "rank_exclusion_bites": rank > 2,
        "all_pass": True,
    }


def decide_placement(f73: dict[str, Any], fp2: dict[str, Any]) -> str:
    """The first-match placement, DECIDED BY COMPUTATION.

    BOUNDARY_Q_OWNED  <- every computed pole-line profile is d1 = w'+1
                         (the boundary-Q profile; prop:boundary-q,
                         bc_section.tex) up to the <=1 near-rational
                         slope of cor:near-rational-line.
    INTERIOR_NAMED_CELL <- some computed profile lands in
                         [w'+2, floor((n-K+1)/2)].
    Both are valid certificate outcomes; nothing below presupposes one.
    """
    interior_hits = f73["counts"]["interior"] + sum(
        r["n_interior"] for r in fp2["alpha_rows"])
    boundary_hits = f73["counts"]["boundary"] + sum(
        r["n_boundary"] for r in fp2["alpha_rows"])
    if interior_hits > 0:
        return "INTERIOR_NAMED_CELL"
    assert boundary_hits > 0
    return "BOUNDARY_Q_OWNED"


# ======================================================================
# Gate 2: deployed exact integers, all four rows, two independent routes
# ======================================================================
N_DEP = 2 ** 21
K_DEP = 2 ** 20 + 1          # MCA census dimension K = k+1
P_KB = 2 ** 31 - 2 ** 24 + 1
P_M31 = 2 ** 31 - 1
BSTAR_KB = P_KB ** 6 // 2 ** 128
BSTAR_M31 = P_M31 ** 4 // 2 ** 100
A_VALUES = (1116023, 1116024, 1116047, 1116048)

ROWS_DEP = (
    # name, p, a_plus, w (= a+ - K on MCA rows; = a+ - k on list rows),
    # B*, budget-fit printed floor/margin displays, gf-printed H_ext
    ("kb_mca", P_KB, 1116048, 67471, BSTAR_KB, "35.7352", "22.1969",
     4807520),
    ("kb_list", P_KB, 1116047, 67471, BSTAR_KB, "35.9212", "22.0109",
     4226236),
    ("m31_mca", P_M31, 1116024, 67447, BSTAR_M31, "20.7411", "3.2589", 9),
    ("m31_list", P_M31, 1116023, 67447, BSTAR_M31, "20.9270", "3.0730", 8),
)


def sieve(limit):
    isp = bytearray([1]) * (limit + 1)
    isp[0:2] = b"\x00\x00"
    for i in range(2, int(limit ** 0.5) + 1):
        if isp[i]:
            isp[i * i::i] = bytearray(len(isp[i * i::i]))
    return [i for i in range(limit + 1) if isp[i]]


def legendre_e(a, b, p):
    e, pk = 0, p
    while pk <= a:
        e += a // pk - b // pk - (a - b) // pk
        pk *= p
    return e


def prod_tree(xs):
    while len(xs) > 1:
        xs = ([xs[i] * xs[i + 1] for i in range(0, len(xs) - 1, 2)]
              + ([xs[-1]] if len(xs) & 1 else []))
    return xs[0] if xs else 1


def kummer_e(a, b, p):
    carries, carry = 0, 0
    x, y = b, a - b
    while x or y or carry:
        s = x % p + y % p + carry
        carry = 1 if s >= p else 0
        carries += carry
        x //= p
        y //= p
    return carries


def combs_route_legendre(primes):
    """C(N_DEP, a) for a in A_VALUES: Legendre floor-sum exponents +
    product tree, anchored at the SMALLEST a and ratio-stepping UP."""
    a0 = A_VALUES[0]
    C = prod_tree([pr ** legendre_e(N_DEP, a0, pr)
                   for pr in primes if legendre_e(N_DEP, a0, pr)])
    out = {a0: C}
    Cm, mp = C, a0
    while mp < A_VALUES[-1]:
        num = Cm * (N_DEP - mp)
        assert num % (mp + 1) == 0
        Cm = num // (mp + 1)
        mp += 1
        if mp in A_VALUES:
            out[mp] = Cm
    return out


def combs_route_kummer(primes):
    """C(N_DEP, a) for a in A_VALUES: Kummer carry-count exponents +
    smallest-first heap merge, anchored at the LARGEST a and
    ratio-stepping DOWN."""
    a1 = A_VALUES[-1]
    heap = [pr ** kummer_e(N_DEP, a1, pr)
            for pr in primes if kummer_e(N_DEP, a1, pr)]
    heapq.heapify(heap)
    while len(heap) > 1:
        x = heapq.heappop(heap)
        y = heapq.heappop(heap)
        heapq.heappush(heap, x * y)
    C = heap[0] if heap else 1
    out = {a1: C}
    Cm, mp = C, a1
    while mp > A_VALUES[0]:
        num = Cm * mp
        assert num % (N_DEP - mp + 1) == 0
        Cm = num // (N_DEP - mp + 1)
        mp -= 1
        if mp in A_VALUES:
            out[mp] = Cm
    return out


def gate2_deployed() -> dict[str, Any]:
    primes = sieve(N_DEP)
    combs_L = combs_route_legendre(primes)
    combs_K = combs_route_kummer(primes)
    routes_agree = all(combs_L[a] == combs_K[a] for a in A_VALUES)
    assert routes_agree, "DEPLOYED ROUTE MISMATCH (adjacency-critical)"
    combs = combs_L

    rows = {}
    for name, p, a, w, bstar, floor_disp, margin_disp, hext_print in ROWS_DEP:
        C = combs[a]
        pw = p ** w
        BB = -(-C // pw)                      # ceil(C(n,a) p^-w)
        Hext = pw * bstar // C                # floor(p^w B* / C(n,a))
        marg = "%.4f" % (_lg2(bstar) - _lg2(BB))
        assert lg2_display(BB) == floor_disp, (name, "floor display")
        assert marg == margin_disp, (name, "margin display")
        assert Hext == hext_print, (name, "H_ext vs gf printed table")
        assert BB > Hext, (name, "extension-headroom exclusion")
        rows[name] = {
            "p": p, "a_plus": a, "w": w,
            "B_star": bstar,
            "floor_BB": BB,
            "floor_BB_log2_display": lg2_display(BB),
            "margin_bits_display": marg,
            "H_ext": Hext,
            "H_ext_matches_gf_printed_table": True,
            "cell_count_exceeds_H_ext": True,
        }
    assert rows["kb_mca"]["floor_BB"] == 57198030366
    assert rows["kb_list"]["floor_BB"] == 65065153468
    assert rows["m31_mca"]["floor_BB"] == 1752700
    assert rows["m31_list"]["floor_BB"] == 1993678
    assert BSTAR_KB == 274980728111395087 and BSTAR_M31 == 16777215

    # corrected omega at the MCA rows (cite bc_one_pencil_omega; not
    # re-parked here) and the prop:bc-not-q dimension table
    omega_rows = {}
    for name, a in (("kb_mca", 1116048), ("m31_mca", 1116024)):
        omega = N_DEP - a
        w = a - K_DEP
        omega_rows[name] = {
            "omega_correct": omega,
            "omega_printed_in_cor_table": omega - 1000,
            "floor_n_over_omega_correct": N_DEP // omega,
            "floor_n_over_omega_printed": N_DEP // (omega - 1000),
            "dim_omega_minus_w": omega - w,
        }
        assert N_DEP // omega == 2 and N_DEP // (omega - 1000) == 2
    assert omega_rows["kb_mca"]["omega_correct"] == 981104
    assert omega_rows["m31_mca"]["omega_correct"] == 981128
    assert omega_rows["kb_mca"]["dim_omega_minus_w"] == 913633
    assert omega_rows["m31_mca"]["dim_omega_minus_w"] == 913681

    return {
        "two_routes_agree_exactly_on_all_four_rows": routes_agree,
        "route_1": "Legendre floor-sum exponents + product tree, anchored "
                   "at a = %d, ratio-stepped up" % A_VALUES[0],
        "route_2": "Kummer carry-count exponents + smallest-first heap "
                   "merge, anchored at a = %d, ratio-stepped down"
                   % A_VALUES[-1],
        "n": N_DEP, "K_mca": K_DEP,
        "rows": rows,
        "omega_rows": omega_rows,
        "all_pass": True,
    }


# ======================================================================
# Gate 3: non-pencil exclusion arithmetic (deployed)
# ======================================================================
def gate3_deployed(g2: dict[str, Any]) -> dict[str, Any]:
    out = {}
    for name, qexp in (("kb_mca", 6), ("m31_mca", 4)):
        row = g2["rows"][name]
        a, p = row["a_plus"], row["p"]
        BB = row["floor_BB"]
        omega = g2["omega_rows"][name]["omega_correct"]
        # full sweep of the one-pencil cap floor((n-g)/(omega-g)), g < omega
        cap_max, arg_g = 0, -1
        for g in range(omega):
            cap = (N_DEP - g) // (omega - g)
            if cap > cap_max:
                cap_max, arg_g = cap, g
        assert cap_max == N_DEP - omega + 1 == a + 1
        assert arg_g == omega - 1
        assert (N_DEP - 0) // omega == 2      # primitive case g = 0
        # robustness under the banked printed-omega typo
        omega_pr = omega - 1000
        cap_max_pr = max((N_DEP - g) // (omega_pr - g)
                         for g in range(omega_pr))
        assert cap_max_pr == N_DEP - omega_pr + 1
        assert BB > cap_max and BB > cap_max_pr
        excess = BB - cap_max
        # slope-level exclusion is also unconditional: choose exactly
        # BB fiber members (pigeonhole); some alpha has zero slope
        # collisions since C(BB,2)(K-1) < q - p
        q = p ** qexp
        collision_mass = BB * (BB - 1) // 2 * (K_DEP - 1)
        assert collision_mass < q - p
        # conditional statements under the named input max-fiber <= B*
        bstar = row["B_star"]
        full_fiber_mass = bstar * (bstar - 1) // 2 * (K_DEP - 1)
        sep_pole_bound = N_DEP + (K_DEP - 1) * (bstar * (bstar - 1) // 2)
        out[name] = {
            "omega": omega,
            "pencil_cap_g0": 2,
            "pencil_cap_sweep_max": cap_max,
            "pencil_cap_sweep_argmax_g": arg_g,
            "pencil_cap_sweep_max_at_printed_omega": cap_max_pr,
            "cell_witness_floor_BB": BB,
            "cell_exceeds_every_pencil_cap": True,
            "exclusion_excess": excess,
            "exclusion_factor_log2_display": "%.4f" % (_lg2(BB)
                                                       - _lg2(cap_max)),
            "slope_level_unconditional": {
                "collision_mass_C_BB_2_times_Kminus1_bits":
                    collision_mass.bit_length(),
                "q_minus_p_bits": (q - p).bit_length(),
                "some_alpha_has_zero_collisions": collision_mass < q - p,
            },
            "conditional_on_max_fiber_le_Bstar": {
                "full_fiber_slope_separation_alpha_exists":
                    full_fiber_mass < q - p,
                "separating_pole_exists_thm_4_6":
                    q > sep_pole_bound,
            },
        }
    assert out["kb_mca"]["pencil_cap_sweep_max"] == 1116049
    assert out["m31_mca"]["pencil_cap_sweep_max"] == 1116025
    assert out["m31_mca"]["exclusion_excess"] == 1752700 - 1116025
    return {"rows": out, "all_pass": True}


# ======================================================================
# Gate 4b: oracle certificates and prior notes
# ======================================================================
def gate4_oracles(root: Path, g2: dict[str, Any]) -> dict[str, Any]:
    # --- #715 lineray cert: payload hash + witness-fiber calibration
    c715 = json.loads((root / ORACLE_715_REL).read_text(encoding="utf-8"))
    assert c715.get("payload_sha256") == payload_hash(c715), "#715 self-hash"
    bb = c715["gate_b_deployed"]["crosslink_budget_fit_BB_displays"]
    assert bb["KB"]["mca_row_witness_depth"] \
        == g2["rows"]["kb_mca"]["floor_BB_log2_display"]
    assert bb["KB"]["list_row_depth_wprime"] \
        == g2["rows"]["kb_list"]["floor_BB_log2_display"]
    assert bb["M31"]["mca_row_witness_depth"] \
        == g2["rows"]["m31_mca"]["floor_BB_log2_display"]
    assert bb["M31"]["list_row_depth_wprime"] \
        == g2["rows"]["m31_list"]["floor_BB_log2_display"]
    pl = c715["gate_c_fp2_toy"]["pole_line"]
    assert pl["witness_fiber_size"] == 40
    assert pl["tested_alphas"] == [17, 18, 288]
    assert pl["z_star"] == [1, 4, 4]
    assert pl["heaviest_depth_wprime_fiber"] == 5
    o715 = {
        "path": str(ORACLE_715_REL),
        "payload_sha256": c715["payload_sha256"],
        "witness_fiber_calibration_consumed": True,
        "BB_displays_match_gate2": True,
        "gate_c_pole_line": {k: pl[k] for k in (
            "witness_fiber_size", "tested_alphas", "n_slopes_min",
            "n_slopes_max", "collision_alphas", "admissible_alphas",
            "first_collision_alpha")},
    }

    # --- bc_one_pencil_omega cert: payload hash + omega values (cite,
    # do NOT re-park; the park is already banked in-tree)
    com = json.loads((root / ORACLE_OMEGA_REL).read_text(encoding="utf-8"))
    assert com.get("payload_sha256") == payload_hash(com), "omega self-hash"
    assert com["parks_for_ken"] is True
    for crow in com["rows"]:
        name = crow["row_id"]
        orow = g2["omega_rows"][name]
        assert crow["omega_correct_n_minus_m"] == orow["omega_correct"]
        assert crow["omega_printed_in_tex"] \
            == orow["omega_printed_in_cor_table"]
        assert crow["floor_n_over_omega_correct"] == 2
        assert crow["floor_n_over_omega_printed"] == 2
    oomega = {"path": str(ORACLE_OMEGA_REL),
              "payload_sha256": com["payload_sha256"],
              "already_parked_for_maintainer": True,
              "rows_match_gate2": True}

    # --- #690 envelope rung ledger cert: the M31 watch-item
    c690 = json.loads((root / ORACLE_690_REL).read_text(encoding="utf-8"))
    assert c690.get("payload_sha256") == payload_hash(c690), "#690 self-hash"
    wi = c690["watch_item"]
    assert wi["row"] == "m31_mca" and wi["profile"] == "Gceil"
    assert wi["M"] == 12769758 and wi["margin_bits"] == -0.3938
    assert wi["B_star"] == 16777215 == g2["rows"]["m31_mca"]["B_star"]
    o690 = {"path": str(ORACLE_690_REL),
            "payload_sha256": c690["payload_sha256"],
            "watch_item": {k: wi[k] for k in (
                "row", "profile", "c", "M", "B_star", "margin_bits",
                "headroom_to_Bstar")}}

    # --- budget-fit cert: OLD-STYLE schema (no payload_sha256 field);
    # consumed by file sha256 + field equality on all four margins rows
    # and the P1 pin
    bf_path = root / BUDGET_FIT_REL
    bf = json.loads(bf_path.read_text(encoding="utf-8"))
    assert "payload_sha256" not in bf
    name_map = {"KoalaBear MCA": "kb_mca", "KoalaBear list": "kb_list",
                "Mersenne-31 MCA": "m31_mca", "Mersenne-31 list": "m31_list"}
    for mrow in bf["margins_table"]:
        if mrow["row"] not in name_map:
            continue        # L4 testbed row: flatness rung, no B*
        row = g2["rows"][name_map[mrow["row"]]]
        assert mrow["a_plus"] == row["a_plus"]
        assert mrow["w"] == row["w"]
        assert ("%.4f" % mrow["log2_floor"]).rstrip("0") \
            == row["floor_BB_log2_display"].rstrip("0")
        assert ("%.4f" % mrow["margin_bits"]).rstrip("0") \
            == row["margin_bits_display"].rstrip("0")
    assert "NOT itself a general upper bound" in bf["P1_extremal_pin"]["status"]
    obf = {"path": str(BUDGET_FIT_REL),
           "schema": "old-style (no payload_sha256 field)",
           "file_sha256": file_sha256(bf_path),
           "margins_rows_match_gate2": True,
           "P1_status_pin": bf["P1_extremal_pin"]["status"]}

    # --- #721: no JSON certificate exists in-tree; consumed by file
    # sha256 + full replay of the printed d=1 collision-literal census
    n721 = root / NOTE_721_REL
    from itertools import combinations
    p17 = 17
    mult: dict[int, int] = {}
    frh = 0
    for S in combinations(range(13), 5):
        if sum(S) % p17:
            continue
        frh += 1
        poly = [1]
        for x in S:
            new = [0] * (len(poly) + 1)
            for i, aco in enumerate(poly):
                new[i] = (new[i] - aco * x) % p17
                new[i + 1] = (new[i + 1] + aco) % p17
            poly = new
        qv = 0
        for aco in reversed(poly):
            qv = (qv * 13 + aco) % p17
        psi = (pow(13, 5, p17) - qv) % p17
        mult[psi] = mult.get(psi, 0) + 1
    assert mult == CENSUS_721, "#721 printed census replay"
    assert frh == sum(mult.values()) == 76
    assert len(mult) == 16 and max(mult.values()) == 7 and 13 not in mult
    o721 = {
        "path": str(NOTE_721_REL),
        "schema": "note + replay verifier only (no JSON cert in-tree)",
        "file_sha256": file_sha256(n721),
        "d1_census_replayed": {"F_RH": frh, "M_RH": 76,
                               "distinct_slopes": 16, "max_fiber": 7,
                               "slope_13_absent": True,
                               "multiplicities": {str(k): v for k, v
                                                  in sorted(mult.items())}},
        "scope_note": "M_RH theorem covers the reduced rational-host "
                      "stratum containing this cell; it explicitly "
                      "disclaims novelty for the separating simple pole "
                      "and retains the nonseparating d=1 formulas as a "
                      "collision-literal audit specialization",
    }

    return {"oracle_715": o715, "oracle_omega": oomega, "oracle_690": o690,
            "oracle_budget_fit": obf, "oracle_721": o721, "all_pass": True}


# ======================================================================
# certificate
# ======================================================================
CELL_DEFINITION = {
    "name": "simple-pole/rank-one cell (per deployed MCA adjacent row)",
    "lines": "pole lines (f_alpha, g_alpha) = (U_z/(X-alpha), -1/(X-alpha)),"
             " alpha not in D u B, z in B^w a depth-w prefix value "
             "(prop:pole-line, prop:rank-one-floor; w = a_+ - K, K = k+1)",
    "witnesses": "exactly the depth-w prefix fiber Fib_w(z) "
                 "(prop:pole-line; #715 witness-fiber calibration: this "
                 "depth-w MCA-route fiber is cap25's depth-(w'-1) witness "
                 "fiber, one below the census depth w' = a_+ - k)",
    "witness_floor": "|Fib_w(z*)| >= ceil(C(n,a_+) p^-w) = B_B(a_+) at a "
                     "heaviest prefix value (pigeonhole, "
                     "prop:rank-one-floor)",
    "grammar": "stated inside prob:saturated-bc's per-row first-match "
               "grammar (quotient, boundary-Q, common-support, tangent, "
               "extension, degree-drop, common-GCD paid first; residual "
               "charts must be type (a) pencils or type (b) named cells "
               "with slope, not raw-support, bounds)",
}

NON_PENCIL_LEMMA = {
    "statement": "Let Fib be a set of N >= 2 distinct m-subsets of D and "
                 "W_S = ell_{D\\S} their monic degree-omega D-split "
                 "locators.  If all W_S lie in one projective locator "
                 "pencil {sA+tB} (def:projective-locator-pencil) with "
                 "g = deg G_D(A,B) < omega, then "
                 "N <= floor((n-g)/(omega-g)) <= n - omega + 1 = m + 1.",
    "proof_sketch": "distinct S give distinct monic degree-omega members, "
                    "hence distinct projective parameters; every member "
                    "is D-split with fixed D-part divisible by G, so it "
                    "has >= omega - g moving roots in D\\Z(G); "
                    "thm:bc-moving-root's incidence count gives "
                    "N <= floor((n-g)/(omega-g)), which is increasing in "
                    "g and peaks at g = omega-1 with value n - omega + 1.",
    "mechanism_cite": "thm:bc-moving-root (gf L1735), "
                      "prop:bc-not-q's proof mechanism (gf L2120: 'a "
                      "line-by-line decomposition without a bound on the "
                      "number of lines gives no row budget')",
    "consequence": "the cell's witness locators at a heaviest-fiber line "
                   "(>= B_B(a_+) of them) do not fit in ANY single "
                   "one-parameter pencil at either deployed MCA row; the "
                   "cell can never be typed (a)",
}


def build_certificate(root: Path) -> dict[str, Any]:
    pins = scan_pins(root)
    f73 = gate1_f73()
    fp2 = gate1_fp2()
    placement = decide_placement(f73, fp2)
    g2 = gate2_deployed()
    g3 = gate3_deployed(g2)
    g4 = gate4_oracles(root, g2)

    # deployed placement block: the module element forces d1 <= w+1 at
    # every scale; cor:near-rational-line forces d1 >= w+1 for all but at
    # most one slope per line; the toys compute d1 = w+1 exactly.
    dep_placement = {
        "module_element": "(X - alpha, U_z - zeta) in M_{f_alpha + zeta "
                          "g_alpha}: (x-alpha)((U_z(x)-zeta)/(x-alpha)) = "
                          "U_z(x) - zeta on D",
        "shifted_degree": "wdeg = max(deg(X-alpha), deg(U_z - zeta) - "
                          "(K-1)) = max(1, a_+ - k) = w + 1",
        "shifted_degree_values": {"kb_mca": 67472, "m31_mca": 67448},
        "upper": "d1 <= w+1 at every scale (the displayed element)",
        "lower": "d1 >= w+1 for all but at most one slope per line "
                 "(thm:near-rational dichotomy + cor:near-rational-line; "
                 "toys: zero near-rational slopes observed)",
        "conclusion": "d1 = w+1 = the boundary-Q profile "
                      "(prop:boundary-q: 'BC starts only after this "
                      "profile is removed'; bc_section.tex: interior is "
                      "w+2 <= d1 <= floor((n-K+1)/2))",
    }

    typed_rows = {}
    for name in ("kb_mca", "m31_mca"):
        row = g2["rows"][name]
        orow = g2["omega_rows"][name]
        xrow = g3["rows"][name]
        typed_rows[name] = {
            "cell": "simple-pole/rank-one cell",
            "placement_computed": placement,
            "type_assignment": "(b)-via-Q: boundary-Q-owned named cell; "
                               "its own slope bound IS the row-sharp Q "
                               "atom target (def:q-row-atom), owned by "
                               "the first-match boundary-Q branch, not a "
                               "fresh saturated-BC residual cell",
            "not_type_a": "non-pencil exclusion: B_B(a_+) = %d > %d = "
                          "max_g floor((n-g)/(omega-g))"
                          % (row["floor_BB"], xrow["pencil_cap_sweep_max"]),
            "a_plus": row["a_plus"],
            "w": row["w"],
            "omega_correct": orow["omega_correct"],
            "dim_omega_minus_w": orow["dim_omega_minus_w"],
            "B_star": row["B_star"],
            "floor_BB": row["floor_BB"],
            "margin_bits_display": row["margin_bits_display"],
            "H_ext": row["H_ext"],
            "extension_headroom_exclusion": "cell count %d > H_ext = %d "
                                            "(prop:extension-cell-target): "
                                            "the paid extension branch "
                                            "cannot absorb the cell"
                                            % (row["floor_BB"], row["H_ext"]),
            "enumerative_half": "CITED-THEOREM: "
                                "thm:exact-list-line-bijection + "
                                "cor:exact-prefix-ray-realization "
                                "(frontiers L2097/L2157) + #715 "
                                "witness-fiber calibration; not a new "
                                "bound",
            "budget_fit": "CONDITIONAL_ON_NAMED_INPUT: max_z |Fib_w(z)| "
                          "<= B* (the depth-w max-fiber bound = row-sharp "
                          "Q one dimension down, def:q-row-atom); the "
                          "PROVED side is only the two-sided pin of the "
                          "heaviest-fiber pole-line class at B_B(a_+) = "
                          "B* 2^-Delta (budget-fit P1, 'NOT itself a "
                          "general upper bound')",
        }

    q_conditional_budget_line = {
        "m31_mca": {
            "cell_pigeonhole_margin_bits": "+3.2589",
            "watch_item_margin_bits": "-0.3938 (the #690 envelope "
                                      "rung-ledger m31_mca Gceil c=2048 "
                                      "rung, M = 12769758 vs B* = "
                                      "16777215, TIGHT, non-firing)",
            "reading": "the same M31 row's ledger already carries a "
                       "sub-bit-tight rung; the cell's +3.2589-bit "
                       "pigeonhole margin means any flatness multiplier "
                       ">= 2^3.2589 on the heaviest depth-w fiber would "
                       "overrun B* -- exactly why the fit is left "
                       "CONDITIONAL_ON_NAMED_INPUT and why gate 2 "
                       "recomputes all four rows two independent ways",
        },
        "kb_mca": {
            "cell_pigeonhole_margin_bits": "+22.1969",
            "watch_item_margin_bits": "none within 22 bits (kb_mca max "
                                      "frontier margin -22.1969, #690)",
        },
    }

    cert: dict[str, Any] = {
        "status": STATUS,
        "object": "first deployed-a_+-row chart-typing certificate for "
                  "prob:saturated-bc: the simple-pole/rank-one cell typed "
                  "at both deployed MCA rows, first-match placement "
                  "decided by computation (third chart family overall, "
                  "after the toy-row near-pencil family and the L4 "
                  "planted interior family)",
        "base_sha": BASE_SHA,
        "evidence_type": "CHART_TYPING_WITH_COMPUTED_PLACEMENT_AND_"
                         "EXACT_ROW_ARITHMETIC",
        "cell_definition": CELL_DEFINITION,
        "statement_pins": pins,
        "gate_1_placement_f73": f73,
        "gate_1_placement_fp2": fp2,
        "placement_computed": placement,
        "deployed_placement_argument": dep_placement,
        "gate_2_deployed": g2,
        "gate_3_non_pencil": g3,
        "non_pencil_lemma": NON_PENCIL_LEMMA,
        "gate_4_oracles": g4,
        "typed_rows": typed_rows,
        "q_conditional_budget_line": q_conditional_budget_line,
        "verdict": "PLACEMENT COMPUTED: %s -- every computed pole-line "
                   "profile is d1 = w+1, the boundary-Q profile (the toy "
                   "tables state this endpoint as w'+1 in the #715 "
                   "census-toy convention w' := m - K, which plays the "
                   "deployed w = a_+ - K role); the "
                   "cell is typed (b)-via-Q at both deployed MCA rows "
                   "(owned by the paid first-match boundary-Q branch; "
                   "its own slope bound is the row-sharp Q atom target), "
                   "and is quantitatively NOT type (a) (witness floor "
                   "exceeds every one-pencil cap: 57198030366 > 1116049 "
                   "at KB, 1752700 > 1116025 at M31).  Enumerative half "
                   "CITED-THEOREM; budget fit CONDITIONAL_ON_NAMED_INPUT "
                   "(depth-w max-fiber / row-sharp Q).  Not a resolution "
                   "of prob:saturated-bc." % placement,
        "honest_headline": "per-row chart VERIFICATION progress on "
                           "prob:saturated-bc -- one named cell typed, "
                           "enumeratively exact, budget fit "
                           "CONDITIONAL_ON_NAMED_INPUT (depth-w "
                           "max-fiber / row-sharp Q); the placement "
                           "computation itself decided boundary-Q "
                           "ownership, it was not presupposed",
        "claim_boundaries": {
            "asserts": [
                "the simple-pole/rank-one cell's first-match placement "
                "is decided by computation: d1 = w+1 (boundary-Q "
                "profile) at every computed pole-line word at both toys, "
                "with the scale-free module element (X-alpha, U_z-zeta) "
                "forcing d1 <= w+1 at the deployed rows",
                "the cell is not type (a): its heaviest-fiber witness "
                "floor exceeds the one-pencil cap "
                "floor((n-g)/(omega-g)) for EVERY g < omega at both "
                "deployed MCA rows (exact integers, cap sweep)",
                "typed rows at both deployed MCA rows with corrected "
                "omega (bc_one_pencil_omega cited, not re-parked), "
                "exact B*, B_B(a_+), margins, and H_ext exclusion, all "
                "four rows recomputed two independent ways that agree "
                "exactly",
                "enumerative half is CITED-THEOREM (frontiers bijection "
                "+ #715 witness-fiber calibration), not a new bound",
                "the Q-conditional budget line is printed against the "
                "#690 -0.3938-bit M31 watch-item",
            ],
            "does_not_assert": [
                "any resolution of prob:saturated-bc (the "
                "growing-deficiency interior residual stays open, "
                "~2.07M bits from target per budget-fit Sec. 6)",
                "any unconditional upper bound on max_z |Fib_w(z)| or "
                "on the cell's slope count (that IS the row-sharp Q "
                "atom target; budget-fit P1 is a floor pin, 'NOT itself "
                "a general upper bound')",
                "U(a_0+1) <= B* at any row",
                "any new census bound or any refutation",
                "any edit to upstream .tex (the omega typo stays parked "
                "via the banked bc_one_pencil_omega certificate)",
            ],
            "independent_recheck_confirms": True,
            "is_counterexample": False,
            "is_degenerate_by_construction": False,
            "is_full_canonical_statement_not_proxy_or_toy_row": False,
            "is_novel_not_confirming_a_proven_theorem": False,
            "is_tautology_under_preconditions": False,
            "resolves_or_advances_prob_band": False,
        },
        "nonclaims": [
            "NOT a resolution of prob:saturated-bc: the "
            "growing-deficiency interior residual (dim omega-w+1 = "
            "913634/913682) remains open, missing the floor by ~2.07M "
            "bits (budget-fit Sec. 6); its core is prob:band-hard "
            "(Gamma_r route) and no progress on it is claimed",
            "no claim U(a_0+1) <= B*",
            "the enumerative half is a cited theorem "
            "(thm:exact-list-line-bijection / "
            "cor:exact-prefix-ray-realization), not new",
            "no bound at raw-support scale anywhere (the #679/#518 Use "
            "Rules are honored: slope/ray-deduplicated scale only)",
            "toy gates pin the placement mechanism and the rank "
            "exclusion, not asymptotics",
        ],
        "risk_limits": [
            "the growing-deficiency BC core is prob:band-hard (tied to "
            "Gamma_r via prop:capfp-kernel); this packet types one "
            "boundary-owned cell and cannot reach that core",
            "the M31 margin is adjacency-critical (3.2589 bits, with "
            "the same row carrying a -0.3938-bit tight rung); all four "
            "deployed rows are therefore recomputed by two independent "
            "exact routes in the same generator and a third route in "
            "the independent checker",
            "the F_73 toy has p = q (no extension-valued line); the "
            "F_{17^2} toy carries the extension-valued case",
        ],
        "caveats": [
            "log2 values in *_display fields are display-grade strings; "
            "every verdict field is an exact integer, boolean, or "
            "computed enum",
            "saturated_bc_budget_fit_v1.json is an old-style "
            "certificate without a payload_sha256 field; it is consumed "
            "by whole-file sha256 plus field equality",
            "#721 has no JSON certificate in-tree; it is consumed by "
            "whole-file sha256 of its note, content pins, and a full "
            "replay of its printed d=1 collision-literal census",
        ],
        "falsifiable": True,
        "falsifiability": "The gate fails if: any pinned statement moves "
                          "or its line hash drifts; any oracle payload "
                          "or file hash drifts; the two deployed big-int "
                          "routes disagree on any row; any of B*, "
                          "B_B(a_+), margin display, H_ext, omega, "
                          "dim omega-w, or pencil-cap sweep value "
                          "changes; any toy fiber, slope set, module "
                          "element, computed d1, or locator rank "
                          "changes; or the #721 census replay drifts.",
        "regeneration": "python experimental/scripts/"
                        "verify_bc_chart_typing.py --emit-defaults",
    }
    cert["payload_sha256"] = payload_hash(cert)
    return cert


def write_cert(root: Path, cert: dict[str, Any]) -> Path:
    path = root / CERT_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")
    return path


def print_summary(cert: dict[str, Any]) -> None:
    f73 = cert["gate_1_placement_f73"]
    print("Gate 1 (F_73): fiber=%d alpha=%d slopes=%d d1=%s "
          "(w'+1=%d) near_rational=%d"
          % (f73["fiber_size"], f73["alpha"], f73["n_distinct_slopes"],
             f73["d1_values"], W + 1, f73["counts"]["near_rational"]))
    fp2 = cert["gate_1_placement_fp2"]
    for r in fp2["alpha_rows"]:
        print("Gate 1 (F_17^2): alpha=%-3d slopes=%-2d d1=%s (w'+1=%d) "
              "near_rational=%d"
              % (r["alpha"], r["n_distinct_slopes"], r["d1_values"],
                 W2 + 1, r["n_near_rational"]))
    print("PLACEMENT COMPUTED:", cert["placement_computed"])
    g2 = cert["gate_2_deployed"]
    print("Gate 2: two_routes_agree_exactly_on_all_four_rows =",
          g2["two_routes_agree_exactly_on_all_four_rows"])
    for name in ("kb_mca", "kb_list", "m31_mca", "m31_list"):
        r = g2["rows"][name]
        print("  %-8s a+=%d w=%d B_B=%-12d (2^%s)  B*=%-20d margin=%s "
              "H_ext=%d"
              % (name, r["a_plus"], r["w"], r["floor_BB"],
                 r["floor_BB_log2_display"], r["B_star"],
                 r["margin_bits_display"], r["H_ext"]))
    g3 = cert["gate_3_non_pencil"]
    for name in ("kb_mca", "m31_mca"):
        r = g3["rows"][name]
        print("Gate 3 %-8s omega=%d cap_max=%d (g=%d) B_B=%d excess=%d "
              "(2^%s)"
              % (name, r["omega"], r["pencil_cap_sweep_max"],
                 r["pencil_cap_sweep_argmax_g"], r["cell_witness_floor_BB"],
                 r["exclusion_excess"], r["exclusion_factor_log2_display"]))
    print("Gate 3 toys: locator rank F_73=%d, F_17^2=%d (pencil cap 2); "
          "counting bites: F_73=%s F_17^2=%s"
          % (f73["locator_matrix_rank"], fp2["locator_matrix_rank"],
             f73["counting_exclusion_bites"],
             fp2["counting_exclusion_bites"]))
    g4 = cert["gate_4_oracles"]
    print("Gate 4: #715 %s..; omega cert %s..; #690 %s..; budget-fit "
          "file %s..; #721 file %s.. census replay M_RH=76 OK"
          % (g4["oracle_715"]["payload_sha256"][:12],
             g4["oracle_omega"]["payload_sha256"][:12],
             g4["oracle_690"]["payload_sha256"][:12],
             g4["oracle_budget_fit"]["file_sha256"][:12],
             g4["oracle_721"]["file_sha256"][:12]))
    npins = sum(len(v) for v in cert["statement_pins"].values())
    print("Gate 4: %d statement pins OK at expected lines" % npins)
    print("verdict:", cert["verdict"][:120], "...")


def run_check(root: Path) -> int:
    fresh = build_certificate(root)
    stored = json.loads((root / CERT_REL).read_text(encoding="utf-8"))
    if stored.get("payload_sha256") != payload_hash(stored):
        print("RESULT: FAIL self-hash")
        return 1
    if fresh["payload_sha256"] != stored["payload_sha256"]:
        print("RESULT: FAIL rebuild drift")
        return 1
    if stored["placement_computed"] != fresh["placement_computed"]:
        print("RESULT: FAIL placement drift")
        return 1
    print("RESULT: PASS")
    print("payload_sha256:", stored["payload_sha256"])
    print("placement_computed:", stored["placement_computed"])
    print("status:", stored["status"])
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit-defaults", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    root = repo_root()
    if args.emit_defaults:
        cert = build_certificate(root)
        path = write_cert(root, cert)
        print("wrote", path)
        print("payload_sha256:", cert["payload_sha256"])
        print_summary(cert)
        return 0
    if args.check:
        return run_check(root)
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
