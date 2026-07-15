#!/usr/bin/env python3
"""Deficiency-2 named-cell typing at both deployed MCA rows.

Object: the deficiency-2 stratum (dim P(W) = 2 EXACTLY) of
prob:saturated-bc's per-row grammar, converted from budget-fit P2's float
ledger row (round(log2, 1) == 21.1) into a typed named-cell certificate
with exact integers at BOTH deployed MCA adjacent rows (KoalaBear
a+ = 1116048, Mersenne-31 a+ = 1116024), plus the first computed
first-match PLACEMENT for the stratum -- tangent-owned vs
common-GCD-owned vs fresh named (b)-cell are ALL admissible certificate
outcomes and none is presupposed.  The verdict field is the computed
outcome.

DEFICIENCY DISAMBIGUATION: "deficiency" here is capf projective
deficiency, stated operationally in two equivalent forms -- pencil shape
(raw L6857: the exact-agreement syndrome pencil M(Z) is t x (j+1),
deficiency = (j+1) - t) == incidence form (dim P(W) = d, budget-fit
Sec. 3).  It is NOT the agreement deficiency d with R = 2t - d of the
fixed_deficiency_*_absorption packets (matroid basis-exchange, bound
C(N,d+1)) -- a naming collision only.

Gates:
  T1. Deficiency-2 chart CONSTRUCTION + verification at two toys (F_73:
      n=24, K=12, m=15, omega=9; F_{17^2}: n=16, K=6, m=9, omega=7;
      fiber/locator machinery ported from the in-tree #777/#715
      harnesses): exhibit a plane W spanned by three heaviest-fiber
      witness locators with dim P(W) = 2 exactly and no common domain
      root, census |P(W) cap Dloc_j(D)| exactly by hyperplane-concurrency
      counting (lem:capf-concurrency: split points = points on exactly j
      of the evaluation lines E_h), verify thm:capf-dim2 clause 1
      exactly, run the twin census (E_h coincidence classes) empirically,
      and replay the f_dim2_skeleton dichotomy (all-or-none twin
      routing + residual singleton-pair bound).
  T2. F_97 fixture replay (holmbuar #792's toy, consumed as oracle):
      re-derive both common-GCD cells' residual planes from the pinned
      line and verify each is a deficiency-2 instance (residual locator
      span rank exactly 3), re-census both planes, and match his exact
      three-point split intersections.
  T3. Placement computation: per exhibited deficiency-2 instance, decide
      which first-match branch owns the split mass -- COMMON_GCD_OWNED
      (whole-plane common root, or every split point twin-routed to the
      paid common-GCD branch one degree lower, f_dim2_skeleton),
      TANGENT_OWNED (the surviving residual mass lies inside a single
      projective sub-pencil: the deficiency-one shape paid by the
      tangent/one-pencil strata), or FRESH_B_CELL (genuinely
      two-dimensional residual mass; prob:saturated-bc type (b) demands
      a separate named cell -- the cell this packet types).
  T4. Deployed exact integers, ALL FOUR ROWS: B_B floors two independent
      ways (Legendre floor-sum + product tree vs Kummer carry-count +
      heap merge, as in #777; the checker adds a binary-splitting third
      route), and EVERY NEW LEDGER INTEGER of this packet THREE
      independent ways inside this generator (route 1: native big-int;
      route 2: bit-level -- shift-subtract long division, peasant
      double-and-add products, bytewise ripple-carry add/sub, and the
      M31 XOR-complement identity (2^24-1) - x == x XOR 0xFFFFFF;
      route 3: base-10^9 decimal-limb schoolbook arithmetic, no
      multi-precision Python int operation anywhere on the value path,
      compared by decimal string) -- gate name
      three_routes_agree_exactly_on_all_ledger_integers.  The M31 margin
      (3.2589 bits) is adjacency-critical and this packet prints a
      13,435-integer three-way slack; any slip is fatal.
  T5. Oracle consumption + statement pins: budget-fit cert (old-style,
      no payload field: file sha256 + field equality on the P2
      deficiency-2 row being converted), #777 bc_chart_typing cert
      (payload hash; B_B floors, B*, omega rows, placement conventions),
      #690 envelope rung cert (payload hash; the M = 12,769,758 M31
      watch rung), bc_one_pencil_omega cert (payload hash; corrected
      omega 981104/981128 -- cite, do NOT re-park), Hart's f_dim2
      skeleton + evidence certs (old-style: file sha256 + field
      equality), holmbuar's #792 note + verifier (no JSON cert in-tree:
      file sha256 + content pins + the T2 replay), and line-hash pins on
      every cited statement in cap25_cap_v13_raw.tex /
      grande_finale.tex / the budget-fit and #777 notes.

Framing: named-cell VERIFICATION progress on prob:saturated-bc -- the
largest proved-but-uncertified non-Q M31 budget consumer (2^21.0959 of
2^24) converted to exact integers and typed, with the joint ledger
printed against the #690 watch rung under BOTH ledger-semantics
readings.  Every joint-fit sentence is CONDITIONAL_ON_NAMED_INPUT
(depth-w max-fiber / row-sharp Q; the proved Q side is a floor pin,
never an upper bound).  PER-CHART SCOPE: thm:capf-dim2 bounds locator
points per chart; no chart-multiplicity-per-line bound is in hand and
none is claimed (inherits budget-fit P2's accepted bookkeeping).  NOT a
resolution of prob:saturated-bc; the growing-deficiency interior core
stays OPEN and prob:band-hard.

Status: EXPERIMENTAL / AUDIT
"""
from __future__ import annotations

import argparse
import hashlib
import heapq
import itertools
import json
import math
import sys
from pathlib import Path
from typing import Any

STATUS = "EXPERIMENTAL / AUDIT"
BASE_SHA = "764f1c0243770baa437d4ae790b1448afa091680"
CERT_REL = Path(
    "experimental/data/certificates/bc-dim2-stratum-typing/"
    "bc_dim2_stratum_typing.json")
RAW_REL = Path("experimental/cap25_cap_v13_raw.tex")
GF_REL = Path("experimental/grande_finale.tex")
BUDGET_NOTE_REL = Path(
    "experimental/notes/thresholds/cap25_v13_saturated_bc_budget_fit.md")
NOTE_777_REL = Path(
    "experimental/notes/thresholds/bc_chart_typing_deployed.md")
NOTE_792_REL = Path(
    "experimental/notes/thresholds/"
    "bc_first_interior_f97_two_cell_certificate.md")
SCRIPT_792_REL = Path(
    "experimental/scripts/"
    "verify_bc_first_interior_f97_two_cell_certificate.py")
SKEL_NOTE_REL = Path("experimental/notes/m1/conjecture_f_dim2_skeleton.md")
EVID_NOTE_REL = Path("experimental/notes/m1/conjecture_f_dim2_evidence.md")
ORACLE_777_REL = Path(
    "experimental/data/certificates/bc-chart-typing/bc_chart_typing.json")
ORACLE_690_REL = Path(
    "experimental/data/certificates/envelope-rung-ledger/"
    "envelope_rung_ledger.json")
ORACLE_OMEGA_REL = Path(
    "experimental/data/certificates/bc-one-pencil-omega/"
    "bc_one_pencil_omega.json")
BUDGET_FIT_REL = Path(
    "experimental/data/certificates/frontier-adjacent/"
    "saturated_bc_budget_fit_v1.json")
SKEL_CERT_REL = Path(
    "experimental/data/certificates/conjecture-f-dim2-skeleton/"
    "conjecture_f_dim2_skeleton.json")
EVID_CERT_REL = Path(
    "experimental/data/certificates/conjecture-f-dim2-evidence/"
    "conjecture_f_dim2_n16_f17.json")
EVID_J4_CERT_REL = Path(
    "experimental/data/certificates/conjecture-f-dim2-evidence/"
    "conjecture_f_dim2_j4_grassmannian.json")

# statement pins: (kind, key, expected_line); kind "label" -> \label{key},
# kind "content" -> literal substring; FIRST hit must sit at expected_line.
RAW_PINS = (
    ("label", "prob:band", 4624),
    ("label", "lem:capf-gcd", 6672),
    ("label", "lem:capf-dim1", 6696),
    ("label", "lem:capf-concurrency", 6707),
    ("label", "thm:capf-dim2", 6719),
    ("label", "thm:capf-fixeddim", 6735),
    ("label", "rem:capf-conjf-open", 6758),
    ("content", "in the deficiency-one shape $t=j$", 6857),
    ("label", "thm:capf-spi", 6859),
    ("label", "rem:capf-spi-calibration", 6895),
    ("content",
     "The theorem does not classify higher-deficiency SPI charts", 6900),
    ("label", "thm:capfp-slope-elim", 8258),
    ("content",
     "so the chart's slope count is bounded by the same rank-one census",
     8267),
)
GF_PINS = (
    ("label", "def:first-match-ledger", 148),
    ("label", "prop:slope-elimination", 1320),
    ("label", "prop:split-chart-tangent", 1452),
    ("label", "prop:boundary-q", 1475),
    ("label", "def:projective-locator-pencil", 1722),
    ("label", "thm:bc-moving-root", 1735),
    ("label", "cor:bc-one-pencil", 1764),
    ("label", "rem:bc-status-after-moving-root", 1785),
    ("label", "def:q-row-atom", 2043),
    ("label", "prop:bc-not-q", 2120),
    ("label", "prob:saturated-bc", 2191),
)
BUDGET_NOTE_PINS = (
    ("content",
     "**P2 (fixed-deficiency charts fit, via proved Conjecture-F).**", 182),
    ("content",
     "| 2 | `C(n,2)/(omega-1)` (`thm:capf-dim2`, raw L6719) | `2^21.10` "
     "fits | `2^21.10` fits |", 190),
    ("content", "P2 is proved-and-fits at fixed deficiency", 207),
)
NOTE_777_PINS = (
    ("content", "placement decided by computation", 1),
    ("content", "DECIDED BY COMPUTATION (Gate 1), not presupposed", 14),
    ("content", "(3.2589 bits) is adjacency-critical.", 57),
    ("content", "margin -0.3938 bits, TIGHT, non-firing", 282),
)
NOTE_792_PINS = (
    ("content", "PROVED-SPECIAL / EXACT FINITE CERTIFICATE", 5),
    ("content", "| `A` | `z0,z1,z2a` | `{15}` | 15 | 8 | `3 / 2` |", 75),
    ("content", "| `B` | `z0,z1,z2b` | `{10,13}` | 14 | 7 | `3 / 2` |", 76),
    ("content",
     "floor 15 here because evaluation hyperplanes collide.", 116),
    ("content",
     "d77eefe2dcbb6b2544c991d2a6fc9022f430ddb2b5b7ad7a3d3e83147d614130",
     182),
)
SKEL_NOTE_PINS = (
    ("content", "# residual <= binom(s,2) / binom(j,2).", 44),
    ("content",
     "dimension-two source for Conjecture F: they are common-GCD charts "
     "one degree", 48),
)
EVID_NOTE_PINS = (
    ("content",
     "the pair-counting explanation should use the weighted form rather "
     "than silently", 77),
    ("content", "top planes with a twin class          5/5", 89),
)


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
# T5a: statement pins
# ======================================================================
def scan_pins(root: Path) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for rel, pins in ((RAW_REL, RAW_PINS), (GF_REL, GF_PINS),
                      (BUDGET_NOTE_REL, BUDGET_NOTE_PINS),
                      (NOTE_777_REL, NOTE_777_PINS),
                      (NOTE_792_REL, NOTE_792_PINS),
                      (SKEL_NOTE_REL, SKEL_NOTE_PINS),
                      (EVID_NOTE_REL, EVID_NOTE_PINS)):
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
# generic finite-field helpers (census, ranks) -- field passed as ops
# ======================================================================
def rank_gauss(mat, sub, mul, inv, is_zero):
    mat = [row[:] for row in mat]
    r = 0
    for c in range(len(mat[0]) if mat else 0):
        piv = None
        for i in range(r, len(mat)):
            if not is_zero(mat[i][c]):
                piv = i
                break
        if piv is None:
            continue
        mat[r], mat[piv] = mat[piv], mat[r]
        pinv = inv(mat[r][c])
        mat[r] = [mul(pinv, x) for x in mat[r]]
        for i in range(len(mat)):
            if i != r and not is_zero(mat[i][c]):
                f = mat[i][c]
                mat[i] = [sub(x, mul(f, y)) for x, y in zip(mat[i], mat[r])]
        r += 1
        if r == len(mat):
            break
    return r


def canon_point(v, mul, inv, is_zero):
    for x in v:
        if not is_zero(x):
            s = inv(x)
            return tuple(mul(s, y) for y in v)
    raise AssertionError("zero vector has no projective class")


def concurrency_census(field, basis_evals, j):
    """Split-point census of P(W) by hyperplane concurrency
    (lem:capf-concurrency): a point of P(W) is a locator point iff it
    lies on EXACTLY j of the evaluation lines E_h.  Enumerates the q+1
    points of each E_h (not the q^2+q+1 points of the plane) and counts
    incidences; asserts no point lies on > j lines (a nonzero element of
    W has degree <= j).  Returns per-point incidence counts keyed by
    canonical W-coordinates [a:b:c]."""
    add, sub, mul, inv, is_zero, elems, zero, one = field
    neg = lambda x: sub(zero, x)
    counter: dict[tuple, int] = {}
    for (e1, e2, e3) in basis_evals:
        assert not (is_zero(e1) and is_zero(e2) and is_zero(e3)), \
            "gcd-triviality violated: zero evaluation functional"
        if not is_zero(e1):
            ie = inv(e1)
            v1 = (neg(mul(e2, ie)), one, zero)
            v2 = (neg(mul(e3, ie)), zero, one)
        elif not is_zero(e2):
            v1 = (one, zero, zero)
            v2 = (zero, neg(mul(e3, inv(e2))), one)
        else:
            v1 = (one, zero, zero)
            v2 = (zero, one, zero)
        pts = [canon_point(v1, mul, inv, is_zero)]
        for t in elems:
            w = tuple(add(mul(t, a), b) for a, b in zip(v1, v2))
            pts.append(canon_point(w, mul, inv, is_zero))
        assert len(set(pts)) == len(elems) + 1, "E_h line point count"
        for pt in pts:
            counter[pt] = counter.get(pt, 0) + 1
    assert max(counter.values()) <= j, \
        "a plane point lies on > j evaluation lines (impossible at deg <= j)"
    return counter


def analyze_plane(field, basis_evals, j, dom_size, direct_scan_points=None):
    """Full deficiency-2 instance analysis: census, thm:capf-dim2 bound
    checks, twin census, f_dim2_skeleton dichotomy replay, and the
    per-instance placement decision inputs."""
    add, sub, mul, inv, is_zero, elems, zero, one = field
    counter = concurrency_census(field, basis_evals, j)
    split_pts = sorted(pt for pt, c in counter.items() if c == j)
    # root sets per split point
    root_sets = []
    for pt in split_pts:
        a, b, c = pt
        roots = frozenset(
            hidx for hidx, (e1, e2, e3) in enumerate(basis_evals)
            if is_zero(add(add(mul(a, e1), mul(b, e2)), mul(c, e3))))
        assert len(roots) == j
        root_sets.append(roots)
    # optional direct full-plane scan cross-check (second in-generator
    # algorithm at the cheap instances; the checker's divisor route
    # covers every instance independently)
    if direct_scan_points is not None:
        direct = []
        for pt in direct_scan_points:
            a, b, c = pt
            nz = sum(
                1 for (e1, e2, e3) in basis_evals
                if is_zero(add(add(mul(a, e1), mul(b, e2)), mul(c, e3))))
            assert nz <= j
            if nz == j:
                direct.append(canon_point(pt, mul, inv, is_zero))
        assert sorted(direct) == split_pts, "direct scan census mismatch"
    # twin census: coincidence classes of the evaluation lines E_h
    classes: dict[tuple, list[int]] = {}
    for hidx, ev in enumerate(basis_evals):
        classes.setdefault(
            canon_point(ev, mul, inv, is_zero), []).append(hidx)
    class_sizes = sorted((len(v) for v in classes.values()), reverse=True)
    twin_classes = [frozenset(v) for v in classes.values() if len(v) >= 2]
    n_singleton = sum(1 for v in classes.values() if len(v) == 1)
    pairwise_distinct = (len(classes) == dom_size)
    # unconditional fact proved inside thm:capf-dim2
    assert class_sizes[0] <= j - 1, "coincidence class multiplicity >= j"
    # thm:capf-dim2 clause 1 (generic denominator j-1); exact count is an
    # integer so the floor of the rational bound applies
    bound_generic = math.comb(dom_size, 2) // (j - 1)
    assert len(split_pts) <= bound_generic
    bound_sharp = math.comb(dom_size, 2) // math.comb(j, 2)
    if pairwise_distinct:
        assert len(split_pts) <= bound_sharp, "sharp clause violated"
    # f_dim2_skeleton dichotomy: all-or-none + twin routing + residual
    residual_idx = []
    twin_routed = 0
    for i, roots in enumerate(root_sets):
        meets = False
        for tc in twin_classes:
            inter = roots & tc
            assert inter == frozenset() or inter == tc, \
                "twin class all-or-none violated"
            if inter:
                meets = True
        if meets:
            twin_routed += 1
        else:
            residual_idx.append(i)
    res_bound = (math.comb(n_singleton, 2) // math.comb(j, 2)
                 if n_singleton >= 2 else 0)
    if residual_idx:
        # a residual point's j roots lie on j distinct singleton lines
        assert n_singleton >= j
        assert len(residual_idx) <= res_bound, "skeleton residual bound"
    # common root of ALL split points (whole-intersection GCD)
    common = None
    for roots in root_sets:
        common = roots if common is None else (common & roots)
    common_all = sorted(common) if common else []
    # residual collinearity: W-coordinates of the residual points
    res_rank = rank_gauss([list(split_pts[i]) for i in residual_idx],
                          sub, mul, inv, is_zero)
    # placement decision, three admissible outcomes (none presupposed)
    if split_pts and common_all:
        outcome = "COMMON_GCD_OWNED"
    elif not residual_idx:
        outcome = "COMMON_GCD_OWNED"
    elif res_rank <= 2:
        outcome = "TANGENT_OWNED"
    else:
        outcome = "FRESH_B_CELL"
    return {
        "n_split_points": len(split_pts),
        "split_root_sets": [sorted(r) for r in root_sets],
        "bound_generic_floor": bound_generic,
        "bound_sharp_floor": bound_sharp,
        "bound_generic_holds": len(split_pts) <= bound_generic,
        "twin_census": {
            "n_classes": len(classes),
            "n_twin_classes": len(twin_classes),
            "twin_classes": sorted(sorted(tc) for tc in twin_classes),
            "n_singleton_classes": n_singleton,
            "class_size_histogram": class_sizes,
            "pairwise_distinct": pairwise_distinct,
            "max_class_size_below_j": class_sizes[0] <= j - 1,
        },
        "skeleton_dichotomy": {
            "all_or_none_verified": True,
            "n_twin_routed_points": twin_routed,
            "n_residual_points": len(residual_idx),
            "residual_singleton_pair_bound": res_bound,
        },
        "common_root_of_all_split_points": common_all,
        "residual_coordinate_rank": res_rank,
        "residual_collinear": res_rank <= 2,
        "placement_outcome": outcome,
    }, split_pts, root_sets


# ======================================================================
# T1a: F_73 toy (fiber machinery ported from the in-tree #777 harness)
# ======================================================================
P = 73
N = 24
K = 12
M = 15
W = M - K       # 3
OMEGA = N - M   # 9


def inv73(a: int) -> int:
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


def pscale(f, c):
    c %= P
    return pnorm([c * a % P for a in f])


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
    ginv = inv73(g[-1])
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


def field73():
    return (lambda a, b: (a + b) % P,
            lambda a, b: (a - b) % P,
            lambda a, b: a * b % P,
            inv73,
            lambda a: a % P == 0,
            tuple(range(P)), 0, 1)


def proj_plane_points_prime(p):
    pts = [(1, b, c) for b in range(p) for c in range(p)]
    pts += [(0, 1, c) for c in range(p)]
    pts.append((0, 0, 1))
    return pts


def gate_t1_f73() -> dict[str, Any]:
    zstar, members = heaviest_fiber_members(M, W)
    assert len(members) == 13  # the banked #715/#777 boundary value
    members = sorted(members)  # canonical lex order (route-independent)
    # witness locators: monic degree-omega, root set D \ S
    locs, root_sets = [], []
    for T in members:
        lam = [1]
        for idx in T:
            lam = pmul(lam, [(-D[idx]) % P, 1])
        WS, rem = pdivmod(LAMBDA, lam)
        assert rem == [] and pdeg(WS) == OMEGA
        locs.append(WS)
        root_sets.append(frozenset(range(N)) - frozenset(T))
    sub73 = lambda a, b: (a - b) % P
    mul73 = lambda a, b: a * b % P
    isz73 = lambda a: a % P == 0
    # FIRST lex triple with dim P(W) = 2 EXACTLY and no common domain root
    chosen = None
    for tri in itertools.combinations(range(len(members)), 3):
        if root_sets[tri[0]] & root_sets[tri[1]] & root_sets[tri[2]]:
            continue
        mat = [[locs[i][t] if t < len(locs[i]) else 0
                for t in range(OMEGA + 1)] for i in tri]
        if rank_gauss(mat, sub73, mul73, inv73, isz73) == 3:
            chosen = tri
            break
    assert chosen is not None, "no gcd-trivial rank-3 witness triple"
    basis = [locs[i] for i in chosen]
    basis_evals = [tuple(peval(b, x) for b in basis) for x in D]
    plane, split_pts, _ = analyze_plane(
        field73(), basis_evals, OMEGA, N,
        direct_scan_points=proj_plane_points_prime(P))
    # the three generators are split points
    for gen in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
        assert gen in split_pts, "generator locator missing from census"
    return {
        "field": {"p": P, "q": P, "n": N, "K": K, "m": M, "w_prime": W,
                  "omega": OMEGA, "j": OMEGA},
        "z_star": zstar,
        "fiber_size": len(members),
        "witness_triple_lex_first": list(chosen),
        "witness_triple_members": [list(members[i]) for i in chosen],
        "dim_PW_exactly_2": True,
        "gcd_trivial": True,
        "census_route": "hyperplane-concurrency counting "
                        "(lem:capf-concurrency) + direct full-plane scan "
                        "(5403 points), cross-asserted",
        "plane": plane,
        "all_pass": True,
    }


# ======================================================================
# T1b: F_{17^2} toy (table field ported from the in-tree #777 harness)
# ======================================================================
PB = 17
NR2 = 3
Q2 = PB * PB
N2 = 16
K2 = 6
M2 = 9
W2 = M2 - K2      # 3
OM2 = N2 - M2     # 7

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


def peval2(f, x):
    r = 0
    for a in reversed(f):
        r = ADD2[MUL2[r][x]][a]
    return r


LAMBDA2 = [1]
for _x in D2:
    LAMBDA2 = pmul2(LAMBDA2, [NEG2[_x], 1])
assert LAMBDA2 == [NEG2[1]] + [0] * (N2 - 1) + [1]  # X^16 - 1


def fibers2(msize, depth):
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


def field289():
    return (lambda a, b: ADD2[a][b],
            lambda a, b: SUB2[a][b],
            lambda a, b: MUL2[a][b],
            lambda a: INV2[a],
            lambda a: a == 0,
            tuple(range(Q2)), 0, 1)


def gate_t1_fp2() -> dict[str, Any]:
    fib3 = fibers2(M2, W2)
    best3 = max(len(v) for v in fib3.values())
    zstar = min(z for z, v in fib3.items() if len(v) == best3)
    fib2 = fibers2(M2, W2 - 1)
    wit = sorted(fib2[zstar[:W2 - 1]])   # canonical lex order
    assert best3 == 5 and len(wit) == 40  # the banked #715/#777 values
    locs, root_sets = [], []
    for T in wit:
        lam = [1]
        for idx in T:
            lam = pmul2(lam, [NEG2[D2[idx]], 1])
        WS, rem = pdivmod2(LAMBDA2, lam)
        assert rem == [] and len(WS) - 1 == OM2
        locs.append(WS)
        root_sets.append(frozenset(range(N2)) - frozenset(T))
    sub2 = lambda a, b: SUB2[a][b]
    mul2 = lambda a, b: MUL2[a][b]
    inv2 = lambda a: INV2[a]
    isz2 = lambda a: a == 0
    chosen = None
    for tri in itertools.combinations(range(len(wit)), 3):
        if root_sets[tri[0]] & root_sets[tri[1]] & root_sets[tri[2]]:
            continue
        mat = [[locs[i][t] if t < len(locs[i]) else 0
                for t in range(OM2 + 1)] for i in tri]
        if rank_gauss(mat, sub2, mul2, inv2, isz2) == 3:
            chosen = tri
            break
    assert chosen is not None
    basis = [locs[i] for i in chosen]
    basis_evals = [tuple(peval2(b, x) for b in basis) for x in D2]
    plane, split_pts, _ = analyze_plane(field289(), basis_evals, OM2, N2)
    for gen in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
        assert gen in split_pts
    return {
        "field": {"p": PB, "q": Q2, "tower": "F_289 = F_17[t]/(t^2-3)",
                  "encoding": "element a + b*t stored as integer a + 17*b",
                  "n": N2, "K": K2, "m": M2, "w_prime": W2, "omega": OM2,
                  "j": OM2},
        "z_star": list(zstar),
        "witness_fiber_size": len(wit),
        "witness_triple_lex_first": list(chosen),
        "witness_triple_members": [list(wit[i]) for i in chosen],
        "dim_PW_exactly_2": True,
        "gcd_trivial": True,
        "census_route": "hyperplane-concurrency counting "
                        "(lem:capf-concurrency); the independent checker "
                        "re-censuses by monic split-divisor enumeration",
        "plane": plane,
        "all_pass": True,
    }


# ======================================================================
# T2: F_97 fixture replay (holmbuar #792, consumed as oracle)
# ======================================================================
P97 = 97
N97 = 16
K97 = 5
M97 = 7
W97 = 2
OMEGA97 = 9

U97 = (11, 17, 84, 52, 77, 65, 2, 28, 39, 59, 35, 84, 46, 87, 83, 71)
V97 = (91, 2, 23, 68, 85, 91, 65, 60, 85, 27, 9, 7, 18, 79, 76, 11)
SUPPORTS_792 = (
    ("z0", 0, (3, 4, 5, 8, 9, 11, 14)),
    ("z1", 1, (0, 1, 2, 3, 6, 7, 12)),
    ("z2a", 2, (4, 6, 10, 11, 12, 13, 14)),
    ("z2b", 2, (1, 2, 3, 4, 6, 11, 15)),
)
CELLS_792 = (
    {"name": "A", "members": ("z0", "z1", "z2a"), "gcd_roots": (15,),
     "split_roots": {(0, 1, 2, 3, 5, 7, 8, 9), (0, 1, 2, 6, 7, 10, 12, 13),
                     (4, 5, 8, 9, 10, 11, 13, 14)}},
    {"name": "B", "members": ("z0", "z1", "z2b"), "gcd_roots": (10, 13),
     "split_roots": {(0, 1, 2, 6, 7, 12, 15), (0, 5, 7, 8, 9, 12, 14),
                     (4, 5, 8, 9, 11, 14, 15)}},
)
DIGEST_792 = "d77eefe2dcbb6b2544c991d2a6fc9022f430ddb2b5b7ad7a3d3e83147d614130"


def inv97(a):
    assert a % P97
    return pow(a, P97 - 2, P97)


def build_domain97():
    gen = None
    for c in range(2, P97):
        if pow(c, (P97 - 1) // 2, P97) != 1 \
                and pow(c, (P97 - 1) // 3, P97) != 1:
            gen = c
            break
    assert gen is not None
    h = pow(gen, (P97 - 1) // N97, P97)
    dom = tuple(pow(h, e, P97) for e in range(N97))
    assert len(set(dom)) == N97
    return dom


D97 = build_domain97()


def pfrom_roots97(vals):
    out = [1]
    for r in vals:
        new = [0] * (len(out) + 1)
        for i, a in enumerate(out):
            new[i] = (new[i] - a * r) % P97
            new[i + 1] = (new[i + 1] + a) % P97
        out = new
    return out


def peval97(f, x):
    r = 0
    for a in reversed(f):
        r = (r * x + a) % P97
    return r


def interpolate97(idxs, vals):
    out = [0]
    for i, ix in enumerate(idxs):
        num, den = [1], 1
        for jx in idxs:
            if jx == ix:
                continue
            new = [0] * (len(num) + 1)
            for t, a in enumerate(num):
                new[t] = (new[t] - a * D97[jx]) % P97
                new[t + 1] = (new[t + 1] + a) % P97
            num = new
            den = den * ((D97[ix] - D97[jx]) % P97) % P97
        s = vals[i] * inv97(den) % P97
        L = max(len(out), len(num))
        out = [((out[t] if t < len(out) else 0)
                + s * (num[t] if t < len(num) else 0)) % P97
               for t in range(L)]
    while out and out[-1] == 0:
        out.pop()
    return out


def pdivmod97(f, g):
    f = list(f)
    q = [0] * max(0, len(f) - len(g) + 1)
    gi = inv97(g[-1])
    def norm(x):
        while x and x[-1] == 0:
            x.pop()
        return x
    f = norm(f)
    while f and len(f) >= len(g):
        c = f[-1] * gi % P97
        d = len(f) - len(g)
        q[d] = c
        for i, b in enumerate(g):
            f[d + i] = (f[d + i] - c * b) % P97
        f = norm(f)
    return norm(q), f


def field97():
    return (lambda a, b: (a + b) % P97,
            lambda a, b: (a - b) % P97,
            lambda a, b: a * b % P97,
            inv97,
            lambda a: a % P97 == 0,
            tuple(range(P97)), 0, 1)


def gate_t2_f97(root: Path) -> dict[str, Any]:
    # oracle consumption: the fixture has no JSON certificate in-tree; it
    # is consumed by file sha256 of note + verifier, content pins
    # (scan_pins), and this full dim-2 replay.  The verifier's embedded
    # canonical payload digest is cross-pinned.
    script_text = (root / SCRIPT_792_REL).read_text(encoding="utf-8")
    assert DIGEST_792 in script_text, "#792 embedded digest missing"
    lam97 = pfrom_roots97(D97)
    assert lam97 == [P97 - 1] + [0] * (N97 - 1) + [1]
    # witness verification: each pinned support is a genuine agreement
    # support of the pinned line at its slope
    wit_locs = {}
    for name, z, S in SUPPORTS_792:
        word = [(u + z * v) % P97 for u, v in zip(U97, V97)]
        head = list(S[:K97])
        poly = interpolate97(head, [word[i] for i in head])
        assert len(poly) - 1 < K97
        assert all(peval97(poly, D97[i]) == word[i] for i in S), \
            "#792 witness support fails agreement"
        E = sorted(frozenset(range(N97)) - frozenset(S))
        loc = pfrom_roots97([D97[i] for i in E])
        assert len(loc) - 1 == OMEGA97
        wit_locs[name] = (loc, frozenset(E))
    sub97 = lambda a, b: (a - b) % P97
    mul97 = lambda a, b: a * b % P97
    isz97 = lambda a: a % P97 == 0
    cells_out = {}
    for cell in CELLS_792:
        gcd_roots = frozenset(cell["gcd_roots"])
        G = pfrom_roots97([D97[i] for i in sorted(gcd_roots)])
        res_dom_idx = [i for i in range(N97) if i not in gcd_roots]
        jres = OMEGA97 - len(gcd_roots)
        basis, res_roots = [], []
        for name in cell["members"]:
            loc, E = wit_locs[name]
            assert gcd_roots <= E, "#792 cell member misses a GCD root"
            q, r = pdivmod97(list(loc), G)
            assert r == [] and len(q) - 1 == jres
            basis.append(q)
            res_roots.append(frozenset(E) - gcd_roots)
        # deficiency-2 instance check: residual span rank EXACTLY 3
        mat = [[b[t] if t < len(b) else 0 for t in range(jres + 1)]
               for b in basis]
        rank = rank_gauss(mat, sub97, mul97, inv97, isz97)
        assert rank == 3, "#792 residual plane is not deficiency-2"
        basis_evals = [tuple(peval97(b, D97[i]) for b in basis)
                       for i in res_dom_idx]
        plane, split_pts, root_sets = analyze_plane(
            field97(), basis_evals, jres, len(res_dom_idx),
            direct_scan_points=proj_plane_points_prime(P97))
        # match holmbuar's exact three-point split intersection
        got = {tuple(sorted(res_dom_idx[t] for t in roots))
               for roots in root_sets}
        assert got == cell["split_roots"], "#792 split-root sets differ"
        assert plane["n_split_points"] == 3  # his exact census
        cells_out[cell["name"]] = {
            "gcd_roots": sorted(gcd_roots),
            "residual_domain_size": len(res_dom_idx),
            "residual_locator_degree": jres,
            "residual_span_rank": rank,
            "dim_PW_exactly_2": True,
            "split_roots_match_pinned": True,
            "plane": plane,
        }
    return {
        "field": {"p": P97, "q": P97, "n": N97, "K": K97, "m": M97,
                  "w": W97, "omega": OMEGA97},
        "oracle": {
            "note_path": str(NOTE_792_REL),
            "note_sha256": file_sha256(root / NOTE_792_REL),
            "verifier_path": str(SCRIPT_792_REL),
            "verifier_sha256": file_sha256(root / SCRIPT_792_REL),
            "embedded_canonical_digest": DIGEST_792,
            "schema": "note + standalone verifier only (no JSON cert "
                      "in-tree); consumed by file sha256 + content pins "
                      "+ this full dim-2 replay",
        },
        "witnesses_verified": [name for name, _, _ in SUPPORTS_792],
        "cells": cells_out,
        "scope_note": "#792's own scope disclaimer is honored: a finite "
                      "fixture certificate, not a deployed-row estimate; "
                      "his first-interior object is the growing-dimension "
                      "residual -- his toy happens to be a dim-2 instance "
                      "because omega - w + 1 is small there; complementary "
                      "to this packet, consumed read-only",
        "all_pass": True,
    }


# ======================================================================
# T3: placement, computed (three admissible outcomes; none presupposed)
# ======================================================================
def decide_placement(instances: dict[str, str]) -> str:
    """Admissible outcomes, per the feasibility design:
      COMMON_GCD_OWNED -- every exhibited deficiency-2 instance's split
        mass is absorbed by the paid common-GCD branch (whole-plane
        common root, or every split point twin-routed one degree lower
        by the f_dim2_skeleton dichotomy);
      TANGENT_OWNED    -- surviving residual mass always lies inside a
        single projective sub-pencil (the deficiency-one shape paid by
        the tangent / one-pencil strata);
      FRESH_B_CELL     -- some instance carries genuinely
        two-dimensional residual split mass that no already-paid branch
        owns: prob:saturated-bc type (b) demands a separate named
        residual cell, which is exactly the cell this packet types.
    All three are valid certificate outcomes; nothing here presupposes
    one."""
    outcomes = set(instances.values())
    if "FRESH_B_CELL" in outcomes:
        return "FRESH_B_CELL"
    if "TANGENT_OWNED" in outcomes:
        return "TANGENT_OWNED"
    assert outcomes == {"COMMON_GCD_OWNED"}
    return "COMMON_GCD_OWNED"


# ======================================================================
# T4: deployed exact integers (three in-generator routes on every new
# ledger integer; B_B two routes as in #777, checker adds the third)
# ======================================================================
N_DEP = 2 ** 21
K_DEP = 2 ** 20 + 1          # MCA census dimension K = k+1
P_KB = 2 ** 31 - 2 ** 24 + 1
P_M31 = 2 ** 31 - 1
A_VALUES = (1116023, 1116024, 1116047, 1116048)
RUNG_690_M = 12769758        # #690 m31_mca Gceil c=2048 rung (oracle-pinned)

ROWS_DEP = (
    # name, p, a_plus, w, expected floor display, expected margin display
    ("kb_mca", P_KB, 1116048, 67471, "35.7352", "22.1969"),
    ("kb_list", P_KB, 1116047, 67471, "35.9212", "22.0109"),
    ("m31_mca", P_M31, 1116024, 67447, "20.7411", "3.2589"),
    ("m31_list", P_M31, 1116023, 67447, "20.9270", "3.0730"),
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


# ---- route 2 primitives: bit-level arithmetic --------------------------
def div_shift_sub(num: int, den: int) -> tuple[int, int]:
    """binary long division by shift-subtract (no Python divmod on the
    value path); returns (q, r) with the reconstruction identity
    q*den + r == num, 0 <= r < den asserted."""
    assert den > 0
    q, r = 0, num
    if den <= num:
        k = num.bit_length() - den.bit_length()
        d = den << k
        if d > num:
            d >>= 1
            k -= 1
        while k >= 0:
            if r >= d:
                r -= d
                q |= 1 << k
            d >>= 1
            k -= 1
    assert q * den + r == num and 0 <= r < den
    return q, r


def peasant_mul(a: int, b: int) -> int:
    """double-and-add product (no Python * on the value path)."""
    acc, addend = 0, a
    while b:
        if b & 1:
            acc += addend
        addend += addend
        b >>= 1
    return acc


def bytes_add(x: int, y: int) -> int:
    """ripple-carry addition on little-endian byte arrays."""
    xb = list(x.to_bytes((x.bit_length() + 8) // 8 + 1, "little"))
    yb = list(y.to_bytes((y.bit_length() + 8) // 8 + 1, "little"))
    L = max(len(xb), len(yb)) + 1
    xb += [0] * (L - len(xb))
    yb += [0] * (L - len(yb))
    out, carry = [], 0
    for i in range(L):
        s = xb[i] + yb[i] + carry
        out.append(s & 0xFF)
        carry = s >> 8
    assert carry == 0
    return int.from_bytes(bytes(out), "little")


def bytes_sub(x: int, y: int) -> int:
    """borrow-propagating subtraction on little-endian byte arrays."""
    assert x >= y
    xb = list(x.to_bytes((x.bit_length() + 8) // 8 + 1, "little"))
    yb = list(y.to_bytes((y.bit_length() + 8) // 8 + 1, "little"))
    yb += [0] * (len(xb) - len(yb))
    out, borrow = [], 0
    for i in range(len(xb)):
        s = xb[i] - yb[i] - borrow
        borrow = 1 if s < 0 else 0
        out.append(s & 0xFF)
    assert borrow == 0
    return int.from_bytes(bytes(out), "little")


# ---- route 3 primitives: base-10^9 decimal-limb arithmetic -------------
LB = 10 ** 9


def L_from_small(x: int) -> list[int]:
    assert 0 <= x < LB * LB
    return [x % LB, x // LB] if x >= LB else [x]


def L_norm(a):
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def L_add(a, b):
    out, carry = [], 0
    for i in range(max(len(a), len(b))):
        s = (a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) + carry
        if s >= LB:
            out.append(s - LB)
            carry = 1
        else:
            out.append(s)
            carry = 0
    if carry:
        out.append(1)
    return L_norm(out)


def L_sub(a, b):
    out, borrow = [], 0
    assert L_cmp(a, b) >= 0
    for i in range(len(a)):
        s = a[i] - (b[i] if i < len(b) else 0) - borrow
        if s < 0:
            out.append(s + LB)
            borrow = 1
        else:
            out.append(s)
            borrow = 0
    assert borrow == 0
    return L_norm(out)


def L_cmp(a, b):
    a, b = L_norm(a[:]), L_norm(b[:])
    if len(a) != len(b):
        return -1 if len(a) < len(b) else 1
    for x, y in zip(reversed(a), reversed(b)):
        if x != y:
            return -1 if x < y else 1
    return 0


def L_mul_small(a, s: int):
    assert 0 <= s < 2 ** 31
    out, carry = [], 0
    for x in a:
        v = x * s + carry
        out.append(v % LB)
        carry = v // LB
    while carry:
        out.append(carry % LB)
        carry //= LB
    return L_norm(out)


def L_mul(a, b):
    out = [0] * (len(a) + len(b) + 1)
    for i, x in enumerate(a):
        if not x:
            continue
        carry = 0
        for j, y in enumerate(b):
            v = out[i + j] + x * y + carry
            out[i + j] = v % LB
            carry = v // LB
        k = i + len(b)
        while carry:
            v = out[k] + carry
            out[k] = v % LB
            carry = v // LB
            k += 1
    return L_norm(out)


def L_divmod_small(a, d: int):
    assert 0 < d < 2 ** 33          # (d-1)*LB + (LB-1) must stay < 2^63
    out = [0] * len(a)
    rem = 0
    for i in range(len(a) - 1, -1, -1):
        cur = rem * LB + a[i]
        out[i] = cur // d
        rem = cur % d
    return L_norm(out), rem


def L_pow2(k: int):
    a = [1]
    for _ in range(k):
        a = L_add(a, a)
    return a


def L_str(a) -> str:
    a = L_norm(a[:])
    return str(a[-1]) + "".join("%09d" % x for x in reversed(a[:-1]))


def gate_t4_deployed() -> dict[str, Any]:
    # ---- B_B floors: two independent in-generator routes (as #777);
    # the independent checker adds the binary-splitting third route.
    primes = sieve(N_DEP)
    combs_L = combs_route_legendre(primes)
    combs_K = combs_route_kummer(primes)
    two_routes = all(combs_L[a] == combs_K[a] for a in A_VALUES)
    assert two_routes, "DEPLOYED B_B ROUTE MISMATCH (adjacency-critical)"
    combs = combs_L
    rows = {}
    for name, p, a, w, floor_disp, margin_disp in ROWS_DEP:
        pw = p ** w
        BB = -(-combs[a] // pw)
        bstar = (p ** 6 // 2 ** 128) if p == P_KB else (p ** 4 // 2 ** 100)
        marg = "%.4f" % (_lg2(bstar) - _lg2(BB))
        assert lg2_display(BB) == floor_disp, (name, "floor display")
        assert marg == margin_disp, (name, "margin display")
        rows[name] = {"p": p, "a_plus": a, "w": w, "B_star": bstar,
                      "floor_BB": BB,
                      "floor_BB_log2_display": lg2_display(BB),
                      "margin_bits_display": marg}
    assert rows["kb_mca"]["floor_BB"] == 57198030366
    assert rows["kb_list"]["floor_BB"] == 65065153468
    assert rows["m31_mca"]["floor_BB"] == 1752700
    assert rows["m31_list"]["floor_BB"] == 1993678

    # ---- omega at the MCA rows (corrected values; bc_one_pencil_omega
    # cited, not re-parked) -- the dim2 DENOMINATOR is omega - 1, so the
    # banked 1000-off printed-omega typo would shift the cell bound by
    # +2287: the typo trap is checked explicitly.
    omega = {"kb_mca": N_DEP - 1116048, "m31_mca": N_DEP - 1116024}
    assert omega == {"kb_mca": 981104, "m31_mca": 981128}

    # ---- three in-generator routes on every new ledger integer -------
    # route 1: native big-int
    r1: dict[str, int] = {}
    r1["C_n_2"] = math.comb(N_DEP, 2)
    r1["C_n_3"] = math.comb(N_DEP, 3)
    for nm, om in (("kb", omega["kb_mca"]), ("m31", omega["m31_mca"])):
        r1["dim2_%s" % nm] = r1["C_n_2"] // (om - 1)
        r1["dim2_rem_%s" % nm] = r1["C_n_2"] % (om - 1)
        r1["C_omega_2_%s" % nm] = math.comb(om, 2)
        r1["sharp_%s" % nm] = r1["C_n_2"] // r1["C_omega_2_%s" % nm]
    r1["bstar_kb"] = P_KB ** 6 // 2 ** 128
    r1["bstar_m31"] = P_M31 ** 4 // 2 ** 100
    bbk, bbm = rows["kb_mca"]["floor_BB"], rows["m31_mca"]["floor_BB"]
    r1["consumed_kb"] = bbk + r1["dim2_kb"]
    r1["remaining_kb"] = r1["bstar_kb"] - r1["consumed_kb"]
    r1["delta_q_kb"] = r1["bstar_kb"] - bbk
    r1["tightened_kb"] = r1["bstar_kb"] - r1["dim2_kb"]
    r1["consumed_m31"] = bbm + r1["dim2_m31"]
    r1["remaining_m31"] = r1["bstar_m31"] - r1["consumed_m31"]
    r1["delta_q_m31"] = r1["bstar_m31"] - bbm
    r1["tightened_m31"] = r1["bstar_m31"] - r1["dim2_m31"]
    r1["additive_total_m31"] = bbm + r1["dim2_m31"] + RUNG_690_M
    r1["additive_slack_m31"] = r1["bstar_m31"] - r1["additive_total_m31"]
    r1["rung_as_q_total_m31"] = RUNG_690_M + r1["dim2_m31"]
    r1["rung_as_q_slack_m31"] = r1["bstar_m31"] - r1["rung_as_q_total_m31"]
    r1["upside_tightened_m31"] = r1["bstar_m31"] - r1["sharp_m31"]

    # route 2: bit-level (shift-subtract division, peasant products,
    # bytewise ripple add/sub, XOR complement against B*_M31 = 2^24 - 1)
    r2: dict[str, int] = {}
    r2["C_n_2"] = (1 << 41) - (1 << 20)   # n = 2^21: n(n-1)/2 = 2^41 - 2^20
    assert r2["C_n_2"] == div_shift_sub(
        peasant_mul(N_DEP, N_DEP - 1), 2)[0]
    r2["C_n_3"] = div_shift_sub(
        peasant_mul(peasant_mul(N_DEP, N_DEP - 1), N_DEP - 2), 6)[0]
    for nm, om in (("kb", omega["kb_mca"]), ("m31", omega["m31_mca"])):
        q, rr = div_shift_sub(r2["C_n_2"], om - 1)
        r2["dim2_%s" % nm], r2["dim2_rem_%s" % nm] = q, rr
        r2["C_omega_2_%s" % nm] = div_shift_sub(
            peasant_mul(om, om - 1), 2)[0]
        r2["sharp_%s" % nm] = div_shift_sub(
            r2["C_n_2"], r2["C_omega_2_%s" % nm])[0]
    pk2 = peasant_mul(P_KB, P_KB)
    pk3 = peasant_mul(pk2, P_KB)
    r2["bstar_kb"] = peasant_mul(pk3, pk3) >> 128
    pm2 = peasant_mul(P_M31, P_M31)
    r2["bstar_m31"] = peasant_mul(pm2, pm2) >> 100
    assert r2["bstar_m31"] == (1 << 24) - 1
    mask = (1 << 24) - 1
    r2["consumed_kb"] = bytes_add(bbk, r2["dim2_kb"])
    r2["remaining_kb"] = bytes_sub(r2["bstar_kb"], r2["consumed_kb"])
    r2["delta_q_kb"] = bytes_sub(r2["bstar_kb"], bbk)
    r2["tightened_kb"] = bytes_sub(r2["bstar_kb"], r2["dim2_kb"])
    r2["consumed_m31"] = bytes_add(bbm, r2["dim2_m31"])
    r2["remaining_m31"] = r2["consumed_m31"] ^ mask
    r2["delta_q_m31"] = bbm ^ mask
    r2["tightened_m31"] = r2["dim2_m31"] ^ mask
    r2["additive_total_m31"] = bytes_add(bytes_add(bbm, r2["dim2_m31"]),
                                         RUNG_690_M)
    r2["additive_slack_m31"] = r2["additive_total_m31"] ^ mask
    r2["rung_as_q_total_m31"] = bytes_add(RUNG_690_M, r2["dim2_m31"])
    r2["rung_as_q_slack_m31"] = r2["rung_as_q_total_m31"] ^ mask
    r2["upside_tightened_m31"] = r2["sharp_m31"] ^ mask

    # route 3: base-10^9 decimal limbs (no multi-precision Python int
    # operation on the value path; compared by decimal string)
    r3: dict[str, str] = {}
    Ln2 = L_mul_small(L_pow2(20), (1 << 21) - 1)   # 2^20 * (2^21 - 1)
    r3["C_n_2"] = L_str(Ln2)
    Ln3 = L_divmod_small(
        L_mul_small(L_mul_small(L_pow2(21), N_DEP - 1), N_DEP - 2), 6)
    assert Ln3[1] == 0
    r3["C_n_3"] = L_str(Ln3[0])
    for nm, om in (("kb", omega["kb_mca"]), ("m31", omega["m31_mca"])):
        q3, rr3 = L_divmod_small(Ln2, om - 1)
        r3["dim2_%s" % nm] = L_str(q3)
        r3["dim2_rem_%s" % nm] = str(rr3)
        Lom2, rr = L_divmod_small(L_mul_small([om], om - 1), 2)
        assert rr == 0
        r3["C_omega_2_%s" % nm] = L_str(Lom2)
        # sharp = floor(C(n,2) / C(omega,2)): verified by bracketing
        # 4*C(omega,2) <= C(n,2) < 5*C(omega,2) in limb space
        assert L_cmp(L_mul_small(Lom2, 4), Ln2) <= 0
        assert L_cmp(L_mul_small(Lom2, 5), Ln2) > 0
        r3["sharp_%s" % nm] = "4"
    Lpk = L_sub(L_pow2(31), L_mul_small([1], 2 ** 24 - 1))  # 2^31-2^24+1
    assert L_str(Lpk) == str(P_KB)
    Lpk2 = L_mul(Lpk, Lpk)
    Lpk6 = L_mul(L_mul(Lpk2, Lpk2), Lpk2)
    x = Lpk6
    for _ in range(4):                     # >> 128 = four floors by 2^32
        x, _rr = L_divmod_small(x, 2 ** 32)
    r3["bstar_kb"] = L_str(x)
    Lpm = L_sub(L_pow2(31), [1])
    Lpm2 = L_mul(Lpm, Lpm)
    Lpm4 = L_mul(Lpm2, Lpm2)
    y = Lpm4
    for _ in range(4):                     # >> 100 = four floors by 2^25
        y, _rr = L_divmod_small(y, 2 ** 25)
    r3["bstar_m31"] = L_str(y)
    Lbbk, Lbbm = L_from_small(bbk), L_from_small(bbm)
    Ld2k = L_divmod_small(Ln2, omega["kb_mca"] - 1)[0]
    Ld2m = L_divmod_small(Ln2, omega["m31_mca"] - 1)[0]
    Lbsk, Lbsm = x, y
    Lrung = L_from_small(RUNG_690_M)
    r3["consumed_kb"] = L_str(L_add(Lbbk, Ld2k))
    r3["remaining_kb"] = L_str(L_sub(Lbsk, L_add(Lbbk, Ld2k)))
    r3["delta_q_kb"] = L_str(L_sub(Lbsk, Lbbk))
    r3["tightened_kb"] = L_str(L_sub(Lbsk, Ld2k))
    r3["consumed_m31"] = L_str(L_add(Lbbm, Ld2m))
    r3["remaining_m31"] = L_str(L_sub(Lbsm, L_add(Lbbm, Ld2m)))
    r3["delta_q_m31"] = L_str(L_sub(Lbsm, Lbbm))
    r3["tightened_m31"] = L_str(L_sub(Lbsm, Ld2m))
    Ltot = L_add(L_add(Lbbm, Ld2m), Lrung)
    r3["additive_total_m31"] = L_str(Ltot)
    r3["additive_slack_m31"] = L_str(L_sub(Lbsm, Ltot))
    Lalt = L_add(Lrung, Ld2m)
    r3["rung_as_q_total_m31"] = L_str(Lalt)
    r3["rung_as_q_slack_m31"] = L_str(L_sub(Lbsm, Lalt))
    r3["upside_tightened_m31"] = L_str(L_sub(Lbsm, [4]))

    keys = sorted(r1)
    assert sorted(r2) == keys and sorted(r3) == keys
    for k in keys:
        assert r1[k] == r2[k], ("route 1 vs 2 mismatch", k)
        assert str(r1[k]) == r3[k], ("route 1 vs 3 mismatch", k)
    three_routes = True

    # ---- pinned expected values (the headline integers, re-derived
    # above by three routes, asserted against their designed values)
    v = r1
    assert v["C_n_2"] == 2199022206976 == (1 << 41) - (1 << 20)
    assert v["dim2_kb"] == 2241377 and v["dim2_rem_kb"] == 508145
    assert v["dim2_m31"] == 2241322 and v["dim2_rem_m31"] == 677082
    assert v["C_omega_2_kb"] == 481282038856
    assert v["C_omega_2_m31"] == 481305585628
    assert v["sharp_kb"] == 4 == v["sharp_m31"]
    assert v["bstar_kb"] == 274980728111395087
    assert v["bstar_m31"] == 16777215
    assert v["consumed_m31"] == 3994022
    assert v["remaining_m31"] == 12783193
    assert v["delta_q_m31"] == 15024515
    assert v["tightened_m31"] == 14535893
    assert v["additive_total_m31"] == 16763780
    assert v["additive_slack_m31"] == 13435
    assert v["rung_as_q_total_m31"] == 15011080
    assert v["rung_as_q_slack_m31"] == 1766135
    assert v["upside_tightened_m31"] == 16777211
    assert v["consumed_kb"] == 57200271743
    assert v["remaining_kb"] == 274980670911123344
    assert v["delta_q_kb"] == 274980670913364721
    assert v["tightened_kb"] == 274980728109153710
    # d = 3 fails BOTH rows: the only proved fixed-d bound at d = 3 is
    # thm:capf-fixeddim's C(n,3) (no dim3 analogue of thm:capf-dim2's
    # pair sharpening is in the tree)
    assert v["C_n_3"] == 1537226473786572800
    assert v["C_n_3"] > v["bstar_kb"] and v["C_n_3"] > v["bstar_m31"]
    # the omega typo trap: at the printed (typo) omega the cell bound
    # would shift by +2287 at both rows -- wrong exact integers, though
    # invisible at 1-decimal log2 (the float row this packet converts)
    for nm, om in (("kb", 981104), ("m31", 981128)):
        typo = v["C_n_2"] // (om - 1000 - 1)
        assert typo - v["dim2_%s" % nm] == 2287
        assert ("%.1f" % _lg2(typo)) == ("%.1f" % _lg2(v["dim2_%s" % nm]))
    # budget-fit P2's float gate, replayed exactly (the line converted)
    assert round(_lg2(v["dim2_kb"]), 1) == 21.1
    assert round(_lg2(v["dim2_m31"]), 1) == 21.1

    # ---- display-grade log2 strings (no verdict uses them) -----------
    disp = {
        "C_n_2": lg2_display(v["C_n_2"]),
        "C_n_3": lg2_display(v["C_n_3"]),
        "dim2_kb": lg2_display(v["dim2_kb"]),
        "dim2_m31": lg2_display(v["dim2_m31"]),
        "sharp_log2": lg2_display(4),
        "remaining_m31": lg2_display(v["remaining_m31"]),
        "delta_q_m31": lg2_display(v["delta_q_m31"]),
        "tightened_m31": lg2_display(v["tightened_m31"]),
        "spare_bits_m31": "%.4f" % (_lg2(v["delta_q_m31"])
                                    - _lg2(v["dim2_m31"])),
        "margin_m31_mca": rows["m31_mca"]["margin_bits_display"],
        "tightened_margin_m31_mca": "%.4f" % (_lg2(v["tightened_m31"])
                                              - _lg2(bbm)),
        "margin_m31_list": rows["m31_list"]["margin_bits_display"],
        "tightened_margin_m31_list": "%.4f" % (
            _lg2(v["tightened_m31"]) - _lg2(rows["m31_list"]["floor_BB"])),
        "naming_price_bits": "%.4f" % (_lg2(v["bstar_m31"])
                                       - _lg2(v["tightened_m31"])),
        "rung_headroom_vs_Bstar": "%.4f" % (_lg2(v["bstar_m31"])
                                            - _lg2(RUNG_690_M)),
        "rung_headroom_vs_tightened": "%.4f" % (_lg2(v["tightened_m31"])
                                                - _lg2(RUNG_690_M)),
        "additive_slack_bits_5dp": "%.5f" % (_lg2(v["bstar_m31"])
                                             - _lg2(v["additive_total_m31"])),
        "rung_as_q_slack_bits": "%.4f" % (_lg2(v["bstar_m31"])
                                          - _lg2(v["rung_as_q_total_m31"])),
        "upside_margin_m31_mca": "%.4f" % (_lg2(v["upside_tightened_m31"])
                                           - _lg2(bbm)),
        "kb_fit_below_residual_bits": "%.4f" % (_lg2(v["delta_q_kb"])
                                                - _lg2(v["dim2_kb"])),
        "kb_tightened_margin": "%.4f" % (_lg2(v["tightened_kb"])
                                         - _lg2(bbk)),
        "kb_list_tightened_margin": "%.4f" % (
            _lg2(v["tightened_kb"]) - _lg2(rows["kb_list"]["floor_BB"])),
    }
    assert disp["dim2_kb"] == "21.0960" and disp["dim2_m31"] == "21.0959"
    assert disp["remaining_m31"] == "23.6077"
    assert disp["delta_q_m31"] == "23.8408"
    assert disp["tightened_m31"] == "23.7931"
    assert disp["spare_bits_m31"] == "2.7449"
    assert disp["tightened_margin_m31_mca"] == "3.0520"
    assert disp["tightened_margin_m31_list"] == "2.8661"
    assert disp["naming_price_bits"] == "0.2069"
    assert disp["rung_headroom_vs_Bstar"] == "0.3938"
    assert disp["rung_headroom_vs_tightened"] == "0.1869"
    assert disp["additive_slack_bits_5dp"] == "0.00116"
    assert disp["rung_as_q_slack_bits"] == "0.1605"
    assert disp["upside_margin_m31_mca"] == "3.2589"
    assert disp["kb_fit_below_residual_bits"] == "36.8362"
    assert disp["kb_tightened_margin"] == "22.1969"      # 4dp cost 0.0000
    assert disp["kb_list_tightened_margin"] == "22.0109"  # 4dp cost 0.0000
    # naming price also as the display-margin drop, both M31 rows
    assert round(3.2589 - float(disp["tightened_margin_m31_mca"]), 4) \
        == 0.2069
    assert round(3.0730 - float(disp["tightened_margin_m31_list"]), 4) \
        == 0.2069

    return {
        "two_routes_agree_exactly_on_all_four_rows": two_routes,
        "three_routes_agree_exactly_on_all_ledger_integers": three_routes,
        "route_1": "native Python big-int (math.comb, //, %, +, -)",
        "route_2": "bit-level: shift-subtract long division with "
                   "reconstruction identity, peasant double-and-add "
                   "products, bytewise ripple-carry add/sub, XOR "
                   "complement against B*_M31 = 2^24 - 1",
        "route_3": "base-10^9 decimal-limb schoolbook arithmetic built "
                   "from doubling chains (no multi-precision Python int "
                   "operation on the value path), compared by decimal "
                   "string",
        "bb_routes": "Legendre floor-sum + product tree (up-stepping) vs "
                     "Kummer carry-count + heap merge (down-stepping), as "
                     "in #777; the independent checker adds the "
                     "binary-splitting third route",
        "n": N_DEP, "K_mca": K_DEP,
        "rows": rows,
        "omega_mca": omega,
        "rung_690_M": RUNG_690_M,
        "ledger_integers": {k: v[k] for k in sorted(v)},
        "displays": disp,
        "omega_typo_trap": {
            "printed_omega_shift_on_cell_bound": 2287,
            "invisible_at_one_decimal_log2": True,
            "parked_certificate_cited": str(ORACLE_OMEGA_REL),
        },
        "budget_fit_P2_float_gate_replayed": {
            "round_log2_1dp_kb": 21.1, "round_log2_1dp_m31": 21.1},
        "all_pass": True,
    }


# ======================================================================
# T5b: oracle certificates
# ======================================================================
def gate_t5_oracles(root: Path, t4: dict[str, Any]) -> dict[str, Any]:
    # --- #777 chart-typing cert: payload hash + field equality
    c777 = json.loads((root / ORACLE_777_REL).read_text(encoding="utf-8"))
    assert c777.get("payload_sha256") == payload_hash(c777), "#777 self-hash"
    g2 = c777["gate_2_deployed"]
    for name in ("kb_mca", "kb_list", "m31_mca", "m31_list"):
        assert g2["rows"][name]["floor_BB"] \
            == t4["rows"][name]["floor_BB"], name
        assert g2["rows"][name]["B_star"] \
            == t4["rows"][name]["B_star"], name
    for name in ("kb_mca", "m31_mca"):
        assert g2["omega_rows"][name]["omega_correct"] \
            == t4["omega_mca"][name]
    assert c777["placement_computed"] == "BOUNDARY_Q_OWNED"
    o777 = {"path": str(ORACLE_777_REL),
            "payload_sha256": c777["payload_sha256"],
            "BB_and_Bstar_and_omega_match_T4": True,
            "placement_convention_inherited":
                "placement decided by computation, admissible outcomes "
                "stated up front, verdict = computed outcome",
            "simple_pole_cell_placement": c777["placement_computed"]}

    # --- #690 envelope rung cert: payload hash + the watch rung
    c690 = json.loads((root / ORACLE_690_REL).read_text(encoding="utf-8"))
    assert c690.get("payload_sha256") == payload_hash(c690), "#690 self-hash"
    wi = c690["watch_item"]
    assert wi["row"] == "m31_mca" and wi["profile"] == "Gceil"
    assert wi["c"] == 2048 and wi["M"] == RUNG_690_M
    assert wi["margin_bits"] == -0.3938
    assert wi["B_star"] == 16777215 == t4["rows"]["m31_mca"]["B_star"]
    o690 = {"path": str(ORACLE_690_REL),
            "payload_sha256": c690["payload_sha256"],
            "watch_item": {k: wi[k] for k in (
                "row", "profile", "c", "M", "B_star", "margin_bits",
                "headroom_to_Bstar")}}

    # --- bc_one_pencil_omega cert: payload hash (cite, do NOT re-park)
    com = json.loads((root / ORACLE_OMEGA_REL).read_text(encoding="utf-8"))
    assert com.get("payload_sha256") == payload_hash(com), "omega self-hash"
    assert com["parks_for_ken"] is True
    for crow in com["rows"]:
        assert crow["omega_correct_n_minus_m"] \
            == t4["omega_mca"][crow["row_id"]]
        assert crow["omega_printed_in_tex"] \
            == t4["omega_mca"][crow["row_id"]] - 1000
    oomega = {"path": str(ORACLE_OMEGA_REL),
              "payload_sha256": com["payload_sha256"],
              "already_parked_for_maintainer": True,
              "rows_match_T4": True}

    # --- budget-fit cert: OLD-STYLE (no payload field); file sha256 +
    # field equality on the exact P2 row this packet converts
    bf_path = root / BUDGET_FIT_REL
    bf = json.loads(bf_path.read_text(encoding="utf-8"))
    assert "payload_sha256" not in bf
    p2 = bf["P2_fixed_deficiency_ledger"]
    d1row = p2[0]
    assert d1row["deficiency"] == 1 and d1row["bound_formula"] \
        == "floor(n/omega)"
    assert d1row["KoalaBear_MCA_value"] == 2 \
        and d1row["Mersenne31_MCA_value"] == 2
    d2row = p2[1]
    assert d2row["deficiency"] == 2
    assert d2row["bound_formula"] == "C(n,2)/(omega-1)"
    assert d2row["cite"] == "thm:capf-dim2 (raw L6719)"
    assert d2row["log2_value_approx"] == 21.1
    assert d2row["fits_budget_KoalaBear"] is True
    assert d2row["fits_budget_Mersenne31"] is True
    assert "payload" not in d2row  # float row: no exact integer banked
    grow = p2[2]
    assert grow["fits_budget"] is False
    assert grow["KoalaBear_MCA"]["dim_W"] == 913634
    assert grow["Mersenne31_MCA"]["dim_W"] == 913682
    assert grow["KoalaBear_MCA"]["miss_fixeddim_bits"] == 2072018
    assert grow["Mersenne31_MCA"]["miss_fixeddim_bits"] == 2072036
    name_map = {"KoalaBear MCA": "kb_mca", "KoalaBear list": "kb_list",
                "Mersenne-31 MCA": "m31_mca", "Mersenne-31 list": "m31_list"}
    for mrow in bf["margins_table"]:
        if mrow["row"] not in name_map:
            continue
        row = t4["rows"][name_map[mrow["row"]]]
        assert mrow["a_plus"] == row["a_plus"] and mrow["w"] == row["w"]
        assert ("%.4f" % mrow["log2_floor"]).rstrip("0") \
            == row["floor_BB_log2_display"].rstrip("0")
        assert ("%.4f" % mrow["margin_bits"]).rstrip("0") \
            == row["margin_bits_display"].rstrip("0")
    assert "NOT itself a general upper bound" \
        in bf["P1_extremal_pin"]["status"]
    obf = {"path": str(BUDGET_FIT_REL),
           "schema": "old-style (no payload_sha256 field)",
           "file_sha256": file_sha256(bf_path),
           "P2_dim2_row_converted": d2row,
           "P2_dim1_and_growing_rows_match": True,
           "margins_rows_match_T4": True,
           "P1_status_pin": bf["P1_extremal_pin"]["status"]}

    # --- Hart's f_dim2 skeleton + evidence certs: OLD-STYLE (no payload
    # field); file sha256 + field equality
    sk_path = root / SKEL_CERT_REL
    sk = json.loads(sk_path.read_text(encoding="utf-8"))
    assert "payload_sha256" not in sk
    assert sk["status"] == "PASS" and sk["dag_node"] == "f_dim2_skeleton"
    assert all(sk["claims_checked"].values())
    assert sk["parameters"]["j"] == 3
    assert sk["parameters"]["projective_dimension"] == 2
    assert sk["maxima"]["reduced_projective_dimension"] == 1
    assert sk["counts"]["twin_planes"] == 1920
    osk = {"path": str(SKEL_CERT_REL),
           "schema": "old-style (no payload_sha256 field)",
           "file_sha256": file_sha256(sk_path),
           "claims_checked_all_true": True,
           "twin_routing_lemma": "PROVED (conjecture_f_dim2_skeleton.md): "
                                 "twin classes are all-or-none, route to "
                                 "the paid common-GCD branch one degree "
                                 "lower onto a projective line section; "
                                 "residual <= C(s,2)/C(j,2)"}
    ev_path = root / EVID_CERT_REL
    ev = json.loads(ev_path.read_text(encoding="utf-8"))
    assert "payload_sha256" not in ev
    assert ev["status"] == "EXPERIMENTAL_EVIDENCE"
    j5 = next(c for c in ev["checks"]
              if c["name"] == "sampled_hankel_kernel_planes_j5_t3")
    assert j5["primitive_top_planes_with_twins"] == 5
    assert j5["primitive_top_plane_count_in_sample"] == 5
    assert j5["primitive_top_planes_without_twins"] == 0
    j4_path = root / EVID_J4_CERT_REL
    j4 = json.loads(j4_path.read_text(encoding="utf-8"))
    assert "payload_sha256" not in j4
    assert j4["status"] == "PASS"
    assert j4["pair_bound_envelope"]["top_planes_with_twins"] == 9
    assert j4["pair_bound_envelope"]["top_planes_without_twins"] == 0
    oev = {"n16_path": str(EVID_CERT_REL),
           "n16_file_sha256": file_sha256(ev_path),
           "j4_path": str(EVID_J4_CERT_REL),
           "j4_file_sha256": file_sha256(j4_path),
           "schema": "old-style (no payload_sha256 field)",
           "adverse_prior_for_upside": "every recorded extremal dim-2 "
                                       "plane in-tree has a twin class "
                                       "(Hart j=5: 5/5; j=4: 9/9; "
                                       "holmbuar F_97: 'evaluation "
                                       "hyperplanes collide')"}

    return {"oracle_777": o777, "oracle_690": o690, "oracle_omega": oomega,
            "oracle_budget_fit": obf, "oracle_f_dim2_skeleton": osk,
            "oracle_f_dim2_evidence": oev, "all_pass": True}


# ======================================================================
# certificate
# ======================================================================
CELL_DEFINITION = {
    "name": "deficiency-2 stratum cell (per deployed MCA adjacent row)",
    "operational_definition": "a chart of capf projective deficiency "
                              "EXACTLY 2, stated operationally in two "
                              "equivalent forms: (i) pencil shape (raw "
                              "L6857): the exact-agreement syndrome "
                              "pencil M(Z) is t x (j+1) with deficiency "
                              "(j+1) - t = 2; (ii) incidence form "
                              "(budget-fit Sec. 3): after slope "
                              "elimination the count is the "
                              "fixed-dimension Conjecture-F incidence "
                              "|P(W) cap Dloc_j(H)| with dim P(W) = 2 "
                              "(dim_K W = 3).  No standalone \\emph "
                              "definition exists in either .tex; this "
                              "certificate states the operational one",
    "disambiguation": "NOT the agreement deficiency d with R = 2t - d of "
                      "the fixed_deficiency_complete_absorption / "
                      "_kernel_minor_compiler packets (matroid "
                      "basis-exchange, bound C(N,d+1)).  Same word, "
                      "different object; naming collision only",
    "delimitation": "deficiency-1 = dim P(W) = 1 = the one-parameter "
                    "pencil (lem:capf-dim1 / cor:bc-one-pencil, bound "
                    "floor(n/omega) = 2 at both rows); deficiency-2 = "
                    "dim P(W) = 2 exactly (thm:capf-dim2); fixed d >= 3 "
                    "has only thm:capf-fixeddim's C(n,d), which already "
                    "fails BOTH rows at d = 3; growing deficiency "
                    "(dim omega-w+1) is the open interior core",
    "grammar": "prob:saturated-bc type (b): 'a higher-dimensional "
               "coefficient family that is explicitly split into such "
               "pencils, or else assigned to a separate named residual "
               "cell with its own slope, not raw-support, bound'; "
               "slope-vs-locator conversion by prop:slope-elimination "
               "(gf L1320) and the pencil dictionary "
               "(thm:capfp-slope-elim(c), raw L8267: 'the chart's slope "
               "count is bounded by the same rank-one census ... at "
               "every deficiency')",
}

THEOREM_QUOTED = {
    "label": "thm:capf-dim2 (projective-plane pair bound, raw L6719)",
    "verbatim": "Under the hypotheses of \\cref{lem:capf-concurrency}, "
                "assume $j\\ge2$ and $\\dim\\PP(W)=2$.  Then "
                "|\\PP(W)\\cap\\Dloc_j(H)| \\le \\binom{|H|}{2}/(j-1), "
                "and if the evaluation lines $E_h$ are pairwise "
                "distinct, the sharper bound with denominator "
                "$\\binom j2$ holds.",
    "hypotheses": "W <= K[X]_{<=j} nonzero, no h in H a common root of "
                  "all of W (gcd-triviality, lem:capf-concurrency), "
                  "j >= 2, dim P(W) = 2 EXACTLY.  No balanced-core or "
                  "mu_n hypothesis; H = D works with |H| = n = 2^21, "
                  "j = omega",
    "derivation_summary": "the E_h are lines in the plane P(W); no "
                          "coincidence class has multiplicity >= j "
                          "(such a class would be a 2-dimensional "
                          "projective space inside the 0-dimensional "
                          "span of one locator -- proved "
                          "unconditionally); each locator point carries "
                          "class multiplicities summing to j, each "
                          "<= j-1, hence >= min m(j-m) = j-1 cross "
                          "pairs {h,h'} with E_h != E_{h'}; each cross "
                          "pair is charged to the unique intersection "
                          "point E_h cap E_{h'}, at most once; there "
                          "are at most C(|H|,2) pairs, so at most "
                          "C(|H|,2)/(j-1) locator points",
    "per_chart_scope_nonclaim": "the theorem bounds LOCATOR POINTS PER "
                                "CHART (one fixed W).  No "
                                "chart-multiplicity-per-line bound is "
                                "in hand; booking the cell as a single "
                                "row consumer inherits budget-fit P2's "
                                "accepted bookkeeping and is stated as "
                                "such (cf. gf L2144: 'a line-by-line "
                                "decomposition without a bound on the "
                                "number of lines gives no row budget')",
}


def build_certificate(root: Path) -> dict[str, Any]:
    pins = scan_pins(root)
    t1a = gate_t1_f73()
    t1b = gate_t1_fp2()
    t2 = gate_t2_f97(root)
    instances = {
        "f73_witness_plane": t1a["plane"]["placement_outcome"],
        "f289_witness_plane": t1b["plane"]["placement_outcome"],
        "f97_cell_A_residual_plane":
            t2["cells"]["A"]["plane"]["placement_outcome"],
        "f97_cell_B_residual_plane":
            t2["cells"]["B"]["plane"]["placement_outcome"],
    }
    placement = decide_placement(instances)
    t4 = gate_t4_deployed()
    t5 = gate_t5_oracles(root, t4)

    v = t4["ledger_integers"]
    disp = t4["displays"]
    rows = t4["rows"]

    typed_rows = {}
    for name, nm in (("kb_mca", "kb"), ("m31_mca", "m31")):
        row = rows[name]
        typed_rows[name] = {
            "cell": "deficiency-2 stratum (dim P(W) = 2 exactly)",
            "placement_computed_at_toys": placement,
            "type_assignment": "(b): separate named residual cell with "
                               "its own slope (not raw-support) bound "
                               "(prob:saturated-bc type (b); "
                               "rem:bc-status-after-moving-root: 'must "
                               "be split further or charged to a "
                               "separate named cell')",
            "a_plus": row["a_plus"],
            "w": row["w"],
            "omega_correct": t4["omega_mca"][name],
            "cell_bound_exact": v["dim2_%s" % nm],
            "cell_bound_formula": "floor(C(n,2)/(omega-1)), n = 2^21",
            "cell_bound_log2_display": disp["dim2_%s" % nm],
            "cell_bound_cite": "thm:capf-dim2 (raw L6719), clause 1",
            "division_remainder": v["dim2_rem_%s" % nm],
            "sharp_branch_two_branch_row": {
                "if_E_h_pairwise_distinct":
                    "floor(C(n,2)/C(omega,2)) = %d" % v["sharp_%s" % nm],
                "else_generic": v["dim2_%s" % nm],
                "empirical_prior": "ADVERSE -- every known extremal "
                                   "instance in-tree has a twin class; "
                                   "shipped MEASURED, no twin-free claim "
                                   "at deployed scale",
            },
            "B_star": row["B_star"],
            "floor_BB": row["floor_BB"],
            "margin_bits_display": row["margin_bits_display"],
            "enumerative_half": "CITED-THEOREM (thm:capf-dim2), not new",
            "budget_fit": "CONDITIONAL_ON_NAMED_INPUT (depth-w max-fiber "
                          "/ row-sharp Q, def:q-row-atom); the proved Q "
                          "side is budget-fit P1's floor pin, never an "
                          "upper bound",
            "per_chart_scope": "per-chart bound booked as a single row "
                               "consumer; inherits P2's accepted "
                               "bookkeeping (NON-CLAIM: no "
                               "chart-multiplicity-per-line bound)",
        }

    joint_ledger_m31 = {
        "qualifier": "CONDITIONAL_ON_NAMED_INPUT on every joint-fit "
                     "sentence (the Q line used is the proved FLOOR pin "
                     "B_B(a_+), never an upper bound)",
        "sentence": "Booking the deficiency-2 cell at its proved "
                    "per-chart bound 2,241,322 = 2^21.0959 alongside the "
                    "boundary-Q cell's proved floor B_B(a_+) = 1,752,700 "
                    "= 2^20.7411 consumes 3,994,022 of B* = 16,777,215, "
                    "leaving 12,783,193 = 2^23.6077; the cell FITS under "
                    "the remaining Delta_Q = B* - B_B = 15,024,515 = "
                    "2^23.8408 with 2.7449 bits to spare, and the "
                    "conditional row-sharp-Q allowance tightens from B* "
                    "to B* - 2,241,322 = 14,535,893 = 2^23.7931 -- the "
                    "M31-MCA Q margin drops 3.2589 -> 3.0520 bits "
                    "(M31-list: 3.0730 -> 2.8661), a 0.2069-bit naming "
                    "price; against the tightened allowance the #690 "
                    "watch rung M = 12,769,758 sits at +0.1869 bits (was "
                    "+0.3938), and under the fully-additive reading "
                    "Q-floor + dim2 + rung = 16,763,780 <= B* with slack "
                    "13,435 = 0.00116 bits.",
        "ledger_semantics_caveat": "whether #690's Gceil rung draws on "
                                   "the same additive line as the named "
                                   "cells is a semantics question; both "
                                   "readings are printed exactly",
        "reading_1_fully_additive": {
            "total": v["additive_total_m31"],
            "slack_exact_integer": v["additive_slack_m31"],
            "slack_bits_display": disp["additive_slack_bits_5dp"],
            "note": "THE most adjacency-critical integer this lane "
                    "prints; exact integer only, never a float",
        },
        "reading_2_rung_is_the_q_payment": {
            "total": v["rung_as_q_total_m31"],
            "slack_exact_integer": v["rung_as_q_slack_m31"],
            "slack_bits_display": disp["rung_as_q_slack_bits"],
        },
        "naming_price_bits_display": disp["naming_price_bits"],
        "watch_rung_tightening": {"was": "+0.3938", "now": "+0.1869"},
    }
    joint_ledger_kb = {
        "qualifier": "CONDITIONAL_ON_NAMED_INPUT",
        "sentence": "KB-MCA fits trivially: the cell bound 2,241,377 = "
                    "2^21.0960 sits 36.8362 bits below the post-Q-floor "
                    "residual B* - B_B = 274,980,670,913,364,721; "
                    "booking it alongside B_B consumes 57,200,271,743 of "
                    "B* = 274,980,728,111,395,087, leaving "
                    "274,980,670,911,123,344; the Q-margin cost is "
                    "0.0000 bits at 4-decimal display (22.1969 "
                    "unchanged; KB-list 22.0109 unchanged).",
        "consumed": v["consumed_kb"],
        "remaining": v["remaining_kb"],
        "tightened_allowance": v["tightened_kb"],
    }

    upside_branch = {
        "status": "DEMOTED (empirically adverse); PROVED cited clause + "
                  "PROVED twin-routing skeleton + MEASURED toy twin "
                  "census; NO twin-free claim at deployed scale",
        "cited_clause": "thm:capf-dim2 clause 2 (verbatim): 'and if the "
                        "evaluation lines $E_h$ are pairwise distinct, "
                        "the sharper bound with denominator $\\binom j2$ "
                        "holds'",
        "quantified": {
            "kb": "floor(C(n,2)/C(981104,2)) = 4 "
                  "(C(omega,2) = 481,282,038,856)",
            "m31": "floor(C(n,2)/C(981128,2)) = 4 "
                   "(C(omega,2) = 481,305,585,628)",
            "refund_if_it_held": "the full 0.2069-bit naming price (the "
                                 "tightened M31 allowance returns to "
                                 "16,777,211, margin 3.2589 at 4dp)",
        },
        "twin_routing_skeleton": "conjecture_f_dim2_skeleton.md (PROVED, "
                                 "cited): twin classes are all-or-none "
                                 "and route to the paid common-GCD "
                                 "branch one degree lower; residual "
                                 "<= C(s,2)/C(j,2)",
        "measured_toy_twin_census": {
            "f73_witness_plane": t1a["plane"]["twin_census"],
            "f289_witness_plane": t1b["plane"]["twin_census"],
            "f97_cell_A": t2["cells"]["A"]["plane"]["twin_census"],
            "f97_cell_B": t2["cells"]["B"]["plane"]["twin_census"],
        },
        "adverse_priors_cited": "holmbuar #792: 'evaluation hyperplanes "
                                "collide'; Hart evidence: j=5 top planes "
                                "with a twin class 5/5, j=4 top planes "
                                "9/9 twinned",
        "unconditional_partial_fact": "no coincidence class has "
                                      "multiplicity >= j (proved inside "
                                      "thm:capf-dim2; verified on every "
                                      "exhibited plane)",
    }

    cert: dict[str, Any] = {
        "status": STATUS,
        "object": "deficiency-2 named-cell typing at both deployed MCA "
                  "rows for prob:saturated-bc: budget-fit P2's float "
                  "ledger row converted to exact integers, typed rows, "
                  "computed first-match placement, and the M31 joint "
                  "ledger printed against the #690 watch rung under both "
                  "ledger-semantics readings (second deployed-row named "
                  "cell, after #777's simple-pole cell)",
        "base_sha": BASE_SHA,
        "evidence_type": "NAMED_CELL_TYPING_WITH_COMPUTED_PLACEMENT_AND_"
                         "EXACT_JOINT_LEDGER",
        "cell_definition": CELL_DEFINITION,
        "theorem_quoted": THEOREM_QUOTED,
        "statement_pins": pins,
        "gate_t1_f73": t1a,
        "gate_t1_fp2": t1b,
        "gate_t2_f97": t2,
        "placement": {
            "admissible_outcomes": ["TANGENT_OWNED", "COMMON_GCD_OWNED",
                                    "FRESH_B_CELL"],
            "decision_procedure": decide_placement.__doc__,
            "per_instance": instances,
            "computed": placement,
        },
        "placement_computed": placement,
        "gate_t4_deployed": t4,
        "gate_t5_oracles": t5,
        "typed_rows": typed_rows,
        "joint_ledger_m31": joint_ledger_m31,
        "joint_ledger_kb": joint_ledger_kb,
        "upside_branch": upside_branch,
        "verdict": "PLACEMENT COMPUTED: %s -- at every exhibited "
                   "deficiency-2 instance (two constructed witness "
                   "planes at F_73/F_17^2 and both #792 F_97 residual "
                   "planes) the computed owner is recorded per instance "
                   "and the aggregate is the named outcome; the "
                   "deficiency-2 cell is typed at BOTH deployed MCA rows "
                   "with exact triple-routed bounds 2,241,377 (KB, "
                   "2^21.0960) / 2,241,322 (M31, 2^21.0959) = "
                   "floor(C(n,2)/(omega-1)); M31 JOINT LEDGER: FITS -- "
                   "consuming 3,994,022 of B* = 16,777,215 alongside the "
                   "boundary-Q floor leaves 12,783,193, a 0.2069-bit "
                   "naming price on the conditional row-sharp-Q "
                   "allowance (margin 3.2589 -> 3.0520; list 3.0730 -> "
                   "2.8661); the #690 watch rung tightens +0.3938 -> "
                   "+0.1869 bits; three-way slack 13,435 exact "
                   "(fully-additive reading, 0.00116 bits) / 1,766,135 "
                   "(rung-as-Q-payment reading, 0.1605 bits).  KB fits "
                   "trivially (36.8362 bits below the post-Q-floor "
                   "residual, 4dp margin cost 0.0000).  ALL joint-fit "
                   "sentences CONDITIONAL_ON_NAMED_INPUT (depth-w "
                   "max-fiber / row-sharp Q; proved side is a floor "
                   "pin).  PER-CHART SCOPE: no chart-multiplicity-"
                   "per-line bound is claimed.  d = 3 fails both rows "
                   "(C(n,3) = 1,537,226,473,786,572,800 = 2^60.4150 "
                   "> B* at KB and M31).  Not a resolution of "
                   "prob:saturated-bc." % placement,
        "honest_headline": "naming the deficiency-2 cell COSTS the M31 "
                           "ledger 0.2069 bits of conditional row-sharp-Q "
                           "allowance (3.2589 -> 3.0520) and tightens the "
                           "#690 watch rung's headroom from +0.3938 to "
                           "+0.1869 bits; the fully-additive three-way "
                           "slack is the exact integer 13,435 (0.00116 "
                           "bits).  That price is the headline, not a "
                           "footnote; the fit itself remains "
                           "CONDITIONAL_ON_NAMED_INPUT",
        "claim_boundaries": {
            "asserts": [
                "the deficiency-2 stratum carries a typed named-cell "
                "certificate row at both deployed MCA rows with exact "
                "cell bounds floor(C(n,2)/(omega-1)) = 2241377 / "
                "2241322, re-derived by three independent in-generator "
                "routes and a further checker route",
                "the first-match placement of the exhibited deficiency-2 "
                "instances is decided by computation among three "
                "admissible outcomes (tangent-owned / common-GCD-owned "
                "/ fresh (b)-cell); the computed outcome is the verdict "
                "field",
                "the M31 joint ledger is printed exactly, with the "
                "naming price, the watch-rung tightening, and the "
                "three-way slack under BOTH ledger-semantics readings, "
                "all CONDITIONAL_ON_NAMED_INPUT",
                "the upside (pairwise-distinct E_h) branch is quantified "
                "exactly (cell collapses to <= 4) and DEMOTED with the "
                "measured adverse twin census",
                "thm:capf-dim2's unconditional coincidence-multiplicity "
                "fact and the f_dim2_skeleton dichotomy are verified on "
                "every exhibited plane",
            ],
            "does_not_assert": [
                "any resolution of prob:saturated-bc (the "
                "growing-deficiency interior residual, dim omega-w+1 = "
                "913634/913682, stays OPEN and prob:band-hard, missing "
                "by ~2.07M bits per budget-fit Sec. 6)",
                "any chart-multiplicity-per-line bound (the cell bound "
                "is per chart; the row booking inherits P2's accepted "
                "bookkeeping)",
                "any twin-free / pairwise-distinct-E_h claim at deployed "
                "scale (the empirical prior is adverse)",
                "any unconditional upper bound on max_z |Fib_w(z)| or "
                "U(a_0+1) <= B* at any row",
                "any fixed-d >= 3 fit (C(n,3) exceeds B* at BOTH rows; "
                "stated, exact)",
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
            "growing-deficiency interior core (dim omega-w+1 = "
            "913634/913682) remains OPEN, prob:band-hard, missing the "
            "floor by ~2.07M bits; rem:capf-conjf-open (raw L6758) "
            "verbatim: 'the growing-dimensional incidence theorem "
            "needed for the aperiodic band is not settled here and is "
            "part of the broad band formulation prob:band'",
            "d = 3 FAILS BOTH ROWS: the only proved fixed-d bound is "
            "thm:capf-fixeddim's C(n,3) = 2^60.4150 > B* at KB "
            "(2^57.9321) and M31 (2^24.0000); deficiency-2 is the "
            "OUTERMOST proved-fitting stratum at both deployed rows",
            "no chart-multiplicity-per-line bound (per-chart scope "
            "stated); no twin-free claim at deployed scale",
            "deficiency-2's ELIMINANT/structural side is explicitly "
            "unclassified (rem:capf-spi-calibration: 'The theorem does "
            "not classify higher-deficiency SPI charts'); only the "
            "incidence COUNT is paid by thm:capf-dim2",
            "the SPI/eliminant theorem thm:capf-spi is deficiency-ONE "
            "only; attributing deficiency-2 to 'tangent / bounded-SPI "
            "paid strata' wholesale would overreach -- hence the "
            "placement is computed, not presupposed",
            "no edit to upstream .tex; the omega 1000-off typo stays "
            "parked via the banked bc_one_pencil_omega certificate "
            "(cited, not re-parked)",
        ],
        "risk_limits": [
            "the M31 row is adjacency-critical three times over: "
            "+3.2589-bit row margin, the #690 -0.3938-bit tight rung "
            "(tightening to +0.1869 under this cell's booking), and the "
            "new 13,435-integer three-way slack (0.00116 bits); every "
            "new integer is therefore triple-routed in-generator and "
            "re-derived in the independent checker",
            "the growing-deficiency BC interior core is prob:band-hard "
            "(Gamma_r route); this packet types one fixed-deficiency "
            "cell and cannot reach that core",
            "the exhibited toy planes are constructed witness-locator "
            "planes and in-tree residual planes, not a first-match "
            "atlas; the placement computation is MEASURED evidence at "
            "toy scale, not a deployed-scale classification",
        ],
        "caveats": [
            "log2 values in *_display fields are display-grade strings; "
            "every verdict field is an exact integer, boolean, or "
            "computed enum",
            "saturated_bc_budget_fit_v1.json and Hart's f_dim2 certs "
            "are old-style certificates without payload_sha256 fields; "
            "they are consumed by whole-file sha256 plus field equality",
            "#792 has no JSON certificate in-tree; it is consumed by "
            "file sha256 of note + verifier, content pins, and the full "
            "T2 dim-2 replay",
        ],
        "falsifiable": True,
        "falsifiability": "The gate fails if: any pinned statement moves "
                          "or its line hash drifts; any oracle payload "
                          "or file hash drifts; the three in-generator "
                          "ledger routes disagree on any integer; the "
                          "two B_B routes disagree on any row; any of "
                          "C(n,2), the cell bounds, remainders, "
                          "C(omega,2), B*, consumed/remaining/tightened "
                          "values, the 13,435 or 1,766,135 slacks, or "
                          "C(n,3) changes; any toy fiber, witness "
                          "triple, census count, split-root set, twin "
                          "class, or placement outcome changes; or the "
                          "#792 replay drifts.",
        "regeneration": "python experimental/scripts/"
                        "verify_bc_dim2_stratum_typing.py --emit-defaults",
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
    t1a, t1b = cert["gate_t1_f73"], cert["gate_t1_fp2"]
    t2 = cert["gate_t2_f97"]
    for tag, pl in (("T1 F_73", t1a["plane"]), ("T1 F_17^2", t1b["plane"]),
                    ("T2 F_97 A", t2["cells"]["A"]["plane"]),
                    ("T2 F_97 B", t2["cells"]["B"]["plane"])):
        tw = pl["twin_census"]
        sk = pl["skeleton_dichotomy"]
        print("%-10s split=%d bound=%d twin_classes=%d distinct=%s "
              "routed=%d residual=%d res_rank=%d -> %s"
              % (tag, pl["n_split_points"], pl["bound_generic_floor"],
                 tw["n_twin_classes"], tw["pairwise_distinct"],
                 sk["n_twin_routed_points"], sk["n_residual_points"],
                 pl["residual_coordinate_rank"], pl["placement_outcome"]))
    print("PLACEMENT COMPUTED:", cert["placement_computed"])
    t4 = cert["gate_t4_deployed"]
    print("T4: three_routes_agree_exactly_on_all_ledger_integers =",
          t4["three_routes_agree_exactly_on_all_ledger_integers"])
    print("T4: two_routes_agree_exactly_on_all_four_rows =",
          t4["two_routes_agree_exactly_on_all_four_rows"])
    vv = t4["ledger_integers"]
    print("  C(n,2) = %d; cell bounds %d (KB) / %d (M31); sharp %d/%d"
          % (vv["C_n_2"], vv["dim2_kb"], vv["dim2_m31"],
             vv["sharp_kb"], vv["sharp_m31"]))
    print("  M31: consumed=%d remaining=%d Delta_Q=%d tightened=%d"
          % (vv["consumed_m31"], vv["remaining_m31"], vv["delta_q_m31"],
             vv["tightened_m31"]))
    print("  M31 three-way: total=%d SLACK=%d (%s bits); rung-as-Q: "
          "total=%d slack=%d (%s bits)"
          % (vv["additive_total_m31"], vv["additive_slack_m31"],
             t4["displays"]["additive_slack_bits_5dp"],
             vv["rung_as_q_total_m31"], vv["rung_as_q_slack_m31"],
             t4["displays"]["rung_as_q_slack_bits"]))
    print("  naming price %s bits (3.2589 -> %s; list 3.0730 -> %s); "
          "rung %s -> %s"
          % (t4["displays"]["naming_price_bits"],
             t4["displays"]["tightened_margin_m31_mca"],
             t4["displays"]["tightened_margin_m31_list"],
             t4["displays"]["rung_headroom_vs_Bstar"],
             t4["displays"]["rung_headroom_vs_tightened"]))
    t5 = cert["gate_t5_oracles"]
    print("T5: #777 %s..; #690 %s..; omega %s..; budget-fit %s..; "
          "skeleton %s.."
          % (t5["oracle_777"]["payload_sha256"][:12],
             t5["oracle_690"]["payload_sha256"][:12],
             t5["oracle_omega"]["payload_sha256"][:12],
             t5["oracle_budget_fit"]["file_sha256"][:12],
             t5["oracle_f_dim2_skeleton"]["file_sha256"][:12]))
    npins = sum(len(vx) for vx in cert["statement_pins"].values())
    print("T5: %d statement pins OK at expected lines" % npins)
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
