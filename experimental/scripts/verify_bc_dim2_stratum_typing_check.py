#!/usr/bin/env python3
"""Independent checker for bc-dim2-stratum-typing (no generator import).

Every stored verdict is recomputed by a route disjoint from the generator:

  plane census    generator: hyperplane-concurrency counting over the
                  evaluation lines E_h (plus a direct full-plane scan at
                  the prime-field toys).
                  here: SECOND ALGORITHM -- monic split-divisor
                  enumeration: every degree-j D-split locator candidate
                  is built from its root set and tested for span
                  membership against the plane's kernel functionals
                  (the two in-tree routes of holmbuar's #792 verifier).
  fibers          generator: windowed leading-coefficient DFS (F_73) /
                  table-field elementary-symmetric recursion (F_289).
                  here: complement power sums + Newton identities
                  (F_73); on-the-fly two-component arithmetic (a + b t,
                  t^2 = 3 over F_17) with itertools enumeration (F_289).
  ranks           generator: normalized Gauss elimination.
                  here: division-free (fraction-free) elimination.
  twin census     generator: first-nonzero-coordinate normalization.
                  here: last-nonzero-coordinate normalization; compared
                  as partitions (normalization-independent).
  placement       recomputed from this file's own censuses and routing;
                  the stored computed outcome must match.
  deployed        generator: three in-generator routes on every new
                  ledger integer (native / bit-level / decimal-limb)
                  and two routes on B_B (Legendre, Kummer).
                  here: FOURTH route on the ledger integers (native
                  recomputation + exact reconstruction identities
                  x + slack == B* etc. + fractions.Fraction floor
                  cross-checks) and the THIRD route on B_B
                  (binary-splitting falling-factorial products with one
                  exact division; math.comb is NOT feasible at n = 2^21),
                  plus 128-bit-mantissa recomputation of every log2
                  display (generator: 80-bit).
  pins/oracles    re-scanned fresh; self-hashes and file hashes
                  recomputed.

Exit 0 with RESULT: PASS, nonzero otherwise.  Accepts --check.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

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

RAW_PINS = {
    "prob:band": ("label", 4624),
    "lem:capf-gcd": ("label", 6672),
    "lem:capf-dim1": ("label", 6696),
    "lem:capf-concurrency": ("label", 6707),
    "thm:capf-dim2": ("label", 6719),
    "thm:capf-fixeddim": ("label", 6735),
    "rem:capf-conjf-open": ("label", 6758),
    "in the deficiency-one shape $t=j$": ("content", 6857),
    "thm:capf-spi": ("label", 6859),
    "rem:capf-spi-calibration": ("label", 6895),
    "The theorem does not classify higher-deficiency SPI charts":
        ("content", 6900),
    "thm:capfp-slope-elim": ("label", 8258),
    "so the chart's slope count is bounded by the same rank-one census":
        ("content", 8267),
}
GF_PINS = {
    "def:first-match-ledger": ("label", 148),
    "prop:slope-elimination": ("label", 1320),
    "prop:split-chart-tangent": ("label", 1452),
    "prop:boundary-q": ("label", 1475),
    "def:projective-locator-pencil": ("label", 1722),
    "thm:bc-moving-root": ("label", 1735),
    "cor:bc-one-pencil": ("label", 1764),
    "rem:bc-status-after-moving-root": ("label", 1785),
    "def:q-row-atom": ("label", 2043),
    "prop:bc-not-q": ("label", 2120),
    "prob:saturated-bc": ("label", 2191),
}
BUDGET_NOTE_PINS = {
    "**P2 (fixed-deficiency charts fit, via proved Conjecture-F).**":
        ("content", 182),
    "| 2 | `C(n,2)/(omega-1)` (`thm:capf-dim2`, raw L6719) | `2^21.10` "
    "fits | `2^21.10` fits |": ("content", 190),
    "P2 is proved-and-fits at fixed deficiency": ("content", 207),
}
NOTE_777_PINS = {
    "placement decided by computation": ("content", 1),
    "DECIDED BY COMPUTATION (Gate 1), not presupposed": ("content", 14),
    "(3.2589 bits) is adjacency-critical.": ("content", 57),
    "margin -0.3938 bits, TIGHT, non-firing": ("content", 282),
}
NOTE_792_PINS = {
    "PROVED-SPECIAL / EXACT FINITE CERTIFICATE": ("content", 5),
    "| `A` | `z0,z1,z2a` | `{15}` | 15 | 8 | `3 / 2` |": ("content", 75),
    "| `B` | `z0,z1,z2b` | `{10,13}` | 14 | 7 | `3 / 2` |": ("content", 76),
    "floor 15 here because evaluation hyperplanes collide.":
        ("content", 116),
    "d77eefe2dcbb6b2544c991d2a6fc9022f430ddb2b5b7ad7a3d3e83147d614130":
        ("content", 182),
}
SKEL_NOTE_PINS = {
    "# residual <= binom(s,2) / binom(j,2).": ("content", 44),
    "dimension-two source for Conjecture F: they are common-GCD charts "
    "one degree": ("content", 48),
}
EVID_NOTE_PINS = {
    "the pair-counting explanation should use the weighted form rather "
    "than silently": ("content", 77),
    "top planes with a twin class          5/5": ("content", 89),
}
DIGEST_792 = "d77eefe2dcbb6b2544c991d2a6fc9022f430ddb2b5b7ad7a3d3e83147d614130"
RUNG_690_M = 12769758


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def payload_hash(obj) -> str:
    clone = dict(obj)
    clone.pop("payload_sha256", None)
    blob = json.dumps(clone, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def lg2_128(x: int) -> float:
    """independent display route: top-128-bit mantissa (generator: 80)."""
    e = x.bit_length() - 1
    if e <= 128:
        return math.log2(x)
    return math.log2(x >> (e - 128)) + (e - 128)


# ---------------------------------------------------------------- pins
def check_pins(root, cert):
    tables = ((RAW_REL, RAW_PINS), (GF_REL, GF_PINS),
              (BUDGET_NOTE_REL, BUDGET_NOTE_PINS),
              (NOTE_777_REL, NOTE_777_PINS), (NOTE_792_REL, NOTE_792_PINS),
              (SKEL_NOTE_REL, SKEL_NOTE_PINS),
              (EVID_NOTE_REL, EVID_NOTE_PINS))
    for rel, pins in tables:
        lines = (root / rel).read_text(encoding="utf-8").splitlines()
        stored = cert["statement_pins"][rel.name]
        assert sorted(stored) == sorted(pins), "pin set drift: %s" % rel.name
        for key, (kind, expected) in pins.items():
            pin = stored[key]
            assert pin["kind"] == kind and pin["line"] == expected
            needle = ("\\label{%s}" % key) if kind == "label" else key
            hit = None
            for i, line in enumerate(lines, 1):
                if needle in line:
                    hit = (i, line)
                    break
            assert hit is not None and hit[0] == expected, \
                "pin moved: %s" % key
            assert hashlib.sha256(
                hit[1].encode("utf-8")).hexdigest()[:16] \
                == pin["sha256_line"], "pin hash drift: %s" % key
    n = sum(len(v) for _, v in tables)
    print("pins: OK (%d pins at expected lines)" % n)


# ------------------------------------------------- division-free rank
def rank_ff(mat, sub, mul, is_zero):
    """fraction-free elimination: row_i <- row_i * piv - row_r * lead.
    Valid over any field/domain; no inverses anywhere."""
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
        pv = mat[r][c]
        for i in range(len(mat)):
            if i != r and not is_zero(mat[i][c]):
                f = mat[i][c]
                mat[i] = [sub(mul(x, pv), mul(y, f))
                          for x, y in zip(mat[i], mat[r])]
        r += 1
        if r == len(mat):
            break
    return r


def nullspace(basis, ncols, add, sub, mul, inv, is_zero, zero, one):
    """kernel functionals of the row space: rows K with K . b = 0 for
    every basis row b; dim = ncols - rank.  Used as a tool to run the
    divisor-enumeration census (the census itself is the second
    algorithm)."""
    rows = [row[:] for row in basis]
    pivots = []
    r = 0
    for c in range(ncols):
        piv = None
        for i in range(r, len(rows)):
            if not is_zero(rows[i][c]):
                piv = i
                break
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        ic = inv(rows[r][c])
        rows[r] = [mul(ic, x) for x in rows[r]]
        for i in range(len(rows)):
            if i != r and not is_zero(rows[i][c]):
                f = rows[i][c]
                rows[i] = [sub(x, mul(f, y))
                           for x, y in zip(rows[i], rows[r])]
        pivots.append(c)
        r += 1
    free = [c for c in range(ncols) if c not in pivots]
    out = []
    for fc in free:
        vec = [zero] * ncols
        vec[fc] = one
        for ri, pc in enumerate(pivots):
            vec[pc] = sub(zero, rows[ri][fc])
        out.append(vec)
    # verification: every functional annihilates every basis row
    for K in out:
        for b in basis:
            acc = zero
            for x, y in zip(K, b):
                acc = add(acc, mul(x, y))
            assert is_zero(acc)
    return out


def divisor_census(dom, j, basis_polys, add, sub, mul, inv, is_zero,
                   zero, one, neg):
    """SECOND-ALGORITHM census: enumerate every monic degree-j D-split
    divisor (via DFS over root subsets with incremental linear-factor
    products) and test span membership against the plane's kernel
    functionals.  Returns the sorted list of split root-index sets."""
    ncols = j + 1
    padded = [[b[t] if t < len(b) else zero for t in range(ncols)]
              for b in basis_polys]
    Ks = nullspace(padded, ncols, add, sub, mul, inv, is_zero, zero, one)
    assert len(Ks) == ncols - 3
    K1 = Ks[0]
    hits = []
    n = len(dom)

    def rec(start, poly, roots):
        if len(roots) == j:
            v = poly + [zero] * (ncols - len(poly))
            acc = zero
            for x, y in zip(K1, v):
                acc = add(acc, mul(x, y))
            if not is_zero(acc):
                return
            for K in Ks[1:]:
                acc = zero
                for x, y in zip(K, v):
                    acc = add(acc, mul(x, y))
                if not is_zero(acc):
                    return
            hits.append(tuple(roots))
            return
        need = j - len(roots)
        for idx in range(start, n - need + 1):
            mr = neg(dom[idx])
            new = [zero] * (len(poly) + 1)
            for t, a in enumerate(poly):
                new[t] = add(new[t], mul(a, mr))
                new[t + 1] = add(new[t + 1], a)
            roots.append(idx)
            rec(idx + 1, new, roots)
            roots.pop()

    rec(0, [one], [])
    return sorted(sorted(h) for h in hits)


def twin_partition(basis_evals, add, mul, inv, is_zero):
    """coincidence classes of the evaluation functionals, normalized by
    the LAST nonzero coordinate (generator: first)."""
    classes = {}
    for hidx, ev in enumerate(basis_evals):
        key = None
        for t in range(len(ev) - 1, -1, -1):
            if not is_zero(ev[t]):
                s = inv(ev[t])
                key = tuple(mul(s, x) for x in ev)
                break
        assert key is not None
        classes.setdefault(key, []).append(hidx)
    return sorted(sorted(v) for v in classes.values())


def replay_plane(cert_plane, dom, j, basis_polys, basis_evals, field):
    """recompute census (divisor route), twin census (last-nonzero
    normalization), routing, residual rank (division-free), and the
    placement outcome; assert everything against the stored plane."""
    add, sub, mul, inv, is_zero, zero, one, neg = field
    hits = divisor_census(dom, j, basis_polys, add, sub, mul, inv,
                          is_zero, zero, one, neg)
    stored_sets = sorted(sorted(r) for r in cert_plane["split_root_sets"])
    assert hits == stored_sets, "divisor-route census mismatch"
    assert len(hits) == cert_plane["n_split_points"]
    dom_size = len(dom)
    assert cert_plane["bound_generic_floor"] \
        == math.comb(dom_size, 2) // (j - 1)
    assert cert_plane["bound_sharp_floor"] \
        == math.comb(dom_size, 2) // math.comb(j, 2)
    assert len(hits) <= cert_plane["bound_generic_floor"]
    parts = twin_partition(basis_evals, add, mul, inv, is_zero)
    tw = cert_plane["twin_census"]
    assert len(parts) == tw["n_classes"]
    twins = [frozenset(p) for p in parts if len(p) >= 2]
    assert sorted(sorted(t) for t in twins) == tw["twin_classes"]
    assert tw["n_singleton_classes"] == sum(1 for p in parts
                                            if len(p) == 1)
    assert tw["pairwise_distinct"] is (len(parts) == dom_size)
    assert max(len(p) for p in parts) <= j - 1
    if tw["pairwise_distinct"]:
        assert len(hits) <= cert_plane["bound_sharp_floor"]
    residual = []
    routed = 0
    for hset in hits:
        R = frozenset(hset)
        meets = False
        for tc in twins:
            inter = R & tc
            assert inter in (frozenset(), tc), "all-or-none violated"
            if inter:
                meets = True
        if meets:
            routed += 1
        else:
            residual.append(hset)
    sk = cert_plane["skeleton_dichotomy"]
    assert sk["n_twin_routed_points"] == routed
    assert sk["n_residual_points"] == len(residual)
    common = None
    for hset in hits:
        common = set(hset) if common is None else (common & set(hset))
    assert cert_plane["common_root_of_all_split_points"] \
        == (sorted(common) if common else [])
    # residual W-coordinates: solve for each residual divisor its (a,b,c)
    # in the basis -- rank of residual set via division-free elimination.
    # Coordinates are recovered by RREF against the padded basis.
    ncols = j + 1
    padded = [[b[t] if t < len(b) else zero for t in range(ncols)]
              for b in basis_polys]
    res_vecs = []
    for hset in residual:
        poly = [one]
        for idx in hset:
            mr = neg(dom[idx])
            new = [zero] * (len(poly) + 1)
            for t, a in enumerate(poly):
                new[t] = add(new[t], mul(a, mr))
                new[t + 1] = add(new[t + 1], a)
            poly = new
        v = poly + [zero] * (ncols - len(poly))
        # coordinates: solve x1*b1 + x2*b2 + x3*b3 = v by elimination on
        # the transposed 4-row system; simplest: augment and solve
        aug = [row[:] + [vi] for row, vi in zip(
            [[padded[i][t] for i in range(3)] for t in range(ncols)],
            v)]
        # aug rows: (b1[t], b2[t], b3[t] | v[t]); solve 3 unknowns
        r = 0
        pivots = []
        for c in range(3):
            piv = None
            for i in range(r, len(aug)):
                if not is_zero(aug[i][c]):
                    piv = i
                    break
            if piv is None:
                continue
            aug[r], aug[piv] = aug[piv], aug[r]
            ic = inv(aug[r][c])
            aug[r] = [mul(ic, x) for x in aug[r]]
            for i in range(len(aug)):
                if i != r and not is_zero(aug[i][c]):
                    f = aug[i][c]
                    aug[i] = [sub(x, mul(f, y))
                              for x, y in zip(aug[i], aug[r])]
            pivots.append(c)
            r += 1
        assert pivots == [0, 1, 2]
        for i in range(3, len(aug)):
            assert all(is_zero(x) for x in aug[i]), "not in span"
        res_vecs.append([aug[0][3], aug[1][3], aug[2][3]])
    rk = rank_ff(res_vecs, sub, mul, is_zero)
    assert rk == cert_plane["residual_coordinate_rank"]
    assert cert_plane["residual_collinear"] is (rk <= 2)
    if hits and common:
        outcome = "COMMON_GCD_OWNED"
    elif not residual:
        outcome = "COMMON_GCD_OWNED"
    elif rk <= 2:
        outcome = "TANGENT_OWNED"
    else:
        outcome = "FRESH_B_CELL"
    assert outcome == cert_plane["placement_outcome"]
    return outcome


# ---------------------------------------------------------------- F_73
P = 73
N = 24
K = 12
M = 15
W = M - K
OMEGA = N - M


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


def f73_fiber_newton(D):
    """heaviest depth-3 fiber of 15-subsets, via complement power sums +
    Newton identities (route disjoint from the generator's DFS)."""
    pw1 = D
    pw2 = [x * x % P for x in D]
    pw3 = [x * x * x % P for x in D]
    P1D = sum(pw1) % P
    P2D = sum(pw2) % P
    P3D = sum(pw3) % P
    inv2 = pow(2, P - 2, P)
    inv3 = pow(3, P - 2, P)
    counts: dict[tuple, int] = {}
    members: dict[tuple, list] = {}
    idxs = range(N)
    for R in itertools.combinations(idxs, OMEGA):
        p1 = (P1D - sum(pw1[i] for i in R)) % P
        p2 = (P2D - sum(pw2[i] for i in R)) % P
        p3 = (P3D - sum(pw3[i] for i in R)) % P
        e1 = p1
        e2 = (e1 * p1 - p2) * inv2 % P
        e3 = (e2 * p1 - e1 * p2 + p3) * inv3 % P
        z = ((-e1) % P, e2, (-e3) % P)
        counts[z] = counts.get(z, 0) + 1
        if counts[z] <= 40:
            members.setdefault(z, []).append(
                tuple(i for i in idxs if i not in R))
    assert sum(counts.values()) == math.comb(N, M)
    best = max(counts.values())
    zstar = min(z for z, c in counts.items() if c == best)
    return list(zstar), members[zstar]


def field73():
    return (lambda a, b: (a + b) % P,
            lambda a, b: (a - b) % P,
            lambda a, b: a * b % P,
            lambda a: pow(a, P - 2, P),
            lambda a: a % P == 0,
            0, 1,
            lambda a: (-a) % P)


def check_f73(cert):
    g1 = cert["gate_t1_f73"]
    D = build_domain()
    zstar, members = f73_fiber_newton(D)
    assert zstar == g1["z_star"] and len(members) == 13 == g1["fiber_size"]
    members = sorted(members)  # canonical lex order (route-independent)
    # locators from root sets (direct root products; no LAMBDA division)
    root_sets = [frozenset(range(N)) - frozenset(T) for T in members]
    locs = []
    for R in root_sets:
        poly = [1]
        for idx in sorted(R):
            new = [0] * (len(poly) + 1)
            for t, a in enumerate(poly):
                new[t] = (new[t] - a * D[idx]) % P
                new[t + 1] = (new[t + 1] + a) % P
            poly = new
        locs.append(poly)
    sub = lambda a, b: (a - b) % P
    mul = lambda a, b: a * b % P
    isz = lambda a: a % P == 0
    # FIRST-lex-triple selection, replayed with division-free ranks
    chosen = None
    for tri in itertools.combinations(range(len(members)), 3):
        if root_sets[tri[0]] & root_sets[tri[1]] & root_sets[tri[2]]:
            continue
        mat = [[locs[i][t] if t < len(locs[i]) else 0
                for t in range(OMEGA + 1)] for i in tri]
        if rank_ff(mat, sub, mul, isz) == 3:
            chosen = tri
            break
    assert list(chosen) == g1["witness_triple_lex_first"]
    assert [sorted(members[i]) for i in chosen] \
        == g1["witness_triple_members"]
    basis = [locs[i] for i in chosen]
    basis_evals = []
    for x in D:
        row = []
        for b in basis:
            acc = 0
            for a in reversed(b):
                acc = (acc * x + a) % P
            row.append(acc)
        basis_evals.append(tuple(row))
    outcome = replay_plane(g1["plane"], D, OMEGA, basis, basis_evals,
                           field73())
    print("F_73: OK (fiber 13 by Newton route; census %d by divisor "
          "route; placement %s)"
          % (g1["plane"]["n_split_points"], outcome))
    return outcome


# ---------------------------------------------------------------- F_289
PB = 17
NR = 3
N2 = 16
K2 = 6
M2 = 9
W2 = M2 - K2
OM2 = N2 - M2
D2 = list(range(1, 17))


def fadd(a, b):
    return ((a[0] + b[0]) % PB, (a[1] + b[1]) % PB)


def fsub(a, b):
    return ((a[0] - b[0]) % PB, (a[1] - b[1]) % PB)


def fmul(a, b):
    return ((a[0] * b[0] + NR * a[1] * b[1]) % PB,
            (a[0] * b[1] + a[1] * b[0]) % PB)


def finv(a):
    nrm = (a[0] * a[0] - NR * a[1] * a[1]) % PB
    ni = pow(nrm, PB - 2, PB)
    return ((a[0] * ni) % PB, ((-a[1]) * ni) % PB)


def fneg(a):
    return ((-a[0]) % PB, (-a[1]) % PB)


def fzero(a):
    return a == (0, 0)


def enc2(a):
    return a[0] + PB * a[1]


def field289():
    return (fadd, fsub, fmul, finv, fzero, (0, 0), (1, 0), fneg)


def check_fp2(cert):
    g1 = cert["gate_t1_fp2"]
    fib3: dict[tuple, list] = {}
    fib2: dict[tuple, list] = {}
    for T in itertools.combinations(range(N2), M2):
        e = [1, 0, 0, 0]
        for i in T:
            x = D2[i]
            for h in range(3, 0, -1):
                e[h] = (e[h] + x * e[h - 1]) % PB
        z3 = tuple((pow(-1, h, PB) * e[h]) % PB for h in (1, 2, 3))
        fib3.setdefault(z3, []).append(T)
        fib2.setdefault(z3[:2], []).append(T)
    best3 = max(len(v) for v in fib3.values())
    zstar = min(z for z, v in fib3.items() if len(v) == best3)
    assert list(zstar) == g1["z_star"] and best3 == 5
    wit = sorted(fib2[zstar[:2]])        # canonical lex order
    assert len(wit) == 40 == g1["witness_fiber_size"]
    root_sets = [frozenset(range(N2)) - frozenset(T) for T in wit]
    dom = [(x, 0) for x in D2]
    locs = []
    for R in root_sets:
        poly = [(1, 0)]
        for idx in sorted(R):
            mr = fneg(dom[idx])
            new = [(0, 0)] * (len(poly) + 1)
            for t, a in enumerate(poly):
                new[t] = fadd(new[t], fmul(a, mr))
                new[t + 1] = fadd(new[t + 1], a)
            poly = new
        locs.append(poly)
    chosen = None
    for tri in itertools.combinations(range(len(wit)), 3):
        if root_sets[tri[0]] & root_sets[tri[1]] & root_sets[tri[2]]:
            continue
        mat = [[locs[i][t] if t < len(locs[i]) else (0, 0)
                for t in range(OM2 + 1)] for i in tri]
        if rank_ff(mat, fsub, fmul, fzero) == 3:
            chosen = tri
            break
    assert list(chosen) == g1["witness_triple_lex_first"]
    assert [sorted(wit[i]) for i in chosen] == g1["witness_triple_members"]
    basis = [locs[i] for i in chosen]
    basis_evals = []
    for x in dom:
        row = []
        for b in basis:
            acc = (0, 0)
            for a in reversed(b):
                acc = fadd(fmul(acc, x), a)
            row.append(acc)
        basis_evals.append(tuple(row))
    outcome = replay_plane(g1["plane"], dom, OM2, basis, basis_evals,
                           field289())
    print("F_17^2: OK (witness fiber 40 by two-component route; census "
          "%d by divisor route; placement %s)"
          % (g1["plane"]["n_split_points"], outcome))
    return outcome


# ---------------------------------------------------------------- F_97
P97 = 97
N97 = 16
K97 = 5
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
    ("A", ("z0", "z1", "z2a"), (15,)),
    ("B", ("z0", "z1", "z2b"), (10, 13)),
)


def field97():
    return (lambda a, b: (a + b) % P97,
            lambda a, b: (a - b) % P97,
            lambda a, b: a * b % P97,
            lambda a: pow(a, P97 - 2, P97),
            lambda a: a % P97 == 0,
            0, 1,
            lambda a: (-a) % P97)


def check_f97(cert):
    g2c = cert["gate_t2_f97"]
    gen = None
    for c in range(2, P97):
        if pow(c, (P97 - 1) // 2, P97) != 1 \
                and pow(c, (P97 - 1) // 3, P97) != 1:
            gen = c
            break
    h = pow(gen, (P97 - 1) // N97, P97)
    D = [pow(h, e, P97) for e in range(N97)]
    assert len(set(D)) == N97
    # witness agreement, checked WITHOUT interpolation: the word values
    # on S must be consistent with a polynomial of degree < K, verified
    # by the rank of the (values | Vandermonde_K) system dropping
    wit_roots = {}
    for name, z, S in SUPPORTS_792:
        word = [(u + z * v) % P97 for u, v in zip(U97, V97)]
        mat = []
        for i in S:
            mat.append([pow(D[i], t, P97) for t in range(K97)]
                       + [word[i]])
        # consistency <=> augmented rank == coefficient rank
        sub = lambda a, b: (a - b) % P97
        mul = lambda a, b: a * b % P97
        isz = lambda a: a % P97 == 0
        rk_coeff = rank_ff([r[:K97] for r in mat], sub, mul, isz)
        rk_aug = rank_ff(mat, sub, mul, isz)
        assert rk_coeff == rk_aug == K97, "#792 witness agreement fails"
        wit_roots[name] = frozenset(range(N97)) - frozenset(S)
    outcomes = {}
    for cname, mnames, gcd_roots in CELLS_792:
        stored = g2c["cells"][cname]
        gset = frozenset(gcd_roots)
        assert stored["gcd_roots"] == sorted(gset)
        res_dom_idx = [i for i in range(N97) if i not in gset]
        jres = OMEGA97 - len(gset)
        assert stored["residual_locator_degree"] == jres
        assert stored["residual_domain_size"] == len(res_dom_idx)
        dom = [D[i] for i in res_dom_idx]
        pos = {i: t for t, i in enumerate(res_dom_idx)}
        basis = []
        for mn in mnames:
            E = wit_roots[mn]
            assert gset <= E
            rr = sorted(E - gset)
            poly = [1]
            for i in rr:
                new = [0] * (len(poly) + 1)
                for t, a in enumerate(poly):
                    new[t] = (new[t] - a * D[i]) % P97
                    new[t + 1] = (new[t + 1] + a) % P97
                poly = new
            basis.append(poly)
        sub = lambda a, b: (a - b) % P97
        mul = lambda a, b: a * b % P97
        isz = lambda a: a % P97 == 0
        mat = [[b[t] if t < len(b) else 0 for t in range(jres + 1)]
               for b in basis]
        assert rank_ff(mat, sub, mul, isz) == 3 \
            == stored["residual_span_rank"]
        basis_evals = []
        for x in dom:
            row = []
            for b in basis:
                acc = 0
                for a in reversed(b):
                    acc = (acc * x + a) % P97
                row.append(acc)
            basis_evals.append(tuple(row))
        # NOTE: stored split_root_sets are RESIDUAL-domain positions;
        # replay_plane works in residual positions throughout
        outcomes[cname] = replay_plane(stored["plane"], dom, jres, basis,
                                       basis_evals, field97())
    print("F_97: OK (both #792 residual planes rank 3; censuses by "
          "divisor route; placements %s/%s)"
          % (outcomes["A"], outcomes["B"]))
    return outcomes


# ---------------------------------------------------------------- deployed
N_DEP = 2 ** 21
K_DEP = 2 ** 20 + 1
P_KB = 2 ** 31 - 2 ** 24 + 1
P_M31 = 2 ** 31 - 1


def prod_range(a, b):
    if b - a < 8:
        r = 1
        for x in range(a, b + 1):
            r *= x
        return r
    mid = (a + b) // 2
    return prod_range(a, mid) * prod_range(mid + 1, b)


def comb_third_route(n, r):
    """C(n, r) by binary-splitting products + one exact division
    (math.comb is NOT feasible at n = 2^21; this is the B_B third
    route, as in #777's checker)."""
    r = min(r, n - r)
    num = prod_range(n - r + 1, n)
    den = prod_range(1, r)
    C, rem = divmod(num, den)
    assert rem == 0
    return C


def check_deployed(cert):
    sys.setrecursionlimit(10000)
    t4 = cert["gate_t4_deployed"]
    assert t4["two_routes_agree_exactly_on_all_four_rows"] is True
    assert t4["three_routes_agree_exactly_on_all_ledger_integers"] is True
    v = t4["ledger_integers"]
    # ---- B_B third route (binary splitting) on all four rows
    combs = {}
    combs[1116048] = comb_third_route(N_DEP, 1116048)
    Cm, mp = combs[1116048], 1116048
    while mp > 1116023:
        num = Cm * mp
        assert num % (N_DEP - mp + 1) == 0
        Cm = num // (N_DEP - mp + 1)
        mp -= 1
        combs[mp] = Cm
    for name, p in (("kb_mca", P_KB), ("kb_list", P_KB),
                    ("m31_mca", P_M31), ("m31_list", P_M31)):
        row = t4["rows"][name]
        pw = p ** row["w"]
        BB = -(-combs[row["a_plus"]] // pw)
        assert BB == row["floor_BB"], (name, "B_B third-route drift")
        bs = (p ** 6 // 2 ** 128) if p == P_KB else (p ** 4 // 2 ** 100)
        assert bs == row["B_star"]
        assert ("%.4f" % lg2_128(BB)) == row["floor_BB_log2_display"]
        assert ("%.4f" % (lg2_128(bs) - lg2_128(BB))) \
            == row["margin_bits_display"]
    bbk = t4["rows"]["kb_mca"]["floor_BB"]
    bbm = t4["rows"]["m31_mca"]["floor_BB"]
    # ---- FOURTH route on every new ledger integer + reconstruction
    om_kb, om_m31 = t4["omega_mca"]["kb_mca"], t4["omega_mca"]["m31_mca"]
    assert (om_kb, om_m31) == (981104, 981128)
    Cn2 = N_DEP * (N_DEP - 1) // 2
    Cn3 = N_DEP * (N_DEP - 1) * (N_DEP - 2) // 6
    assert v["C_n_2"] == Cn2 == (1 << 41) - (1 << 20)
    assert v["C_n_3"] == Cn3
    exp = {}
    for nm, om in (("kb", om_kb), ("m31", om_m31)):
        exp["dim2_%s" % nm] = Cn2 // (om - 1)
        # Fraction floor cross-check
        assert exp["dim2_%s" % nm] == math.floor(Fraction(Cn2, om - 1))
        exp["dim2_rem_%s" % nm] = Cn2 - exp["dim2_%s" % nm] * (om - 1)
        exp["C_omega_2_%s" % nm] = om * (om - 1) // 2
        exp["sharp_%s" % nm] = math.floor(
            Fraction(Cn2, exp["C_omega_2_%s" % nm]))
    exp["bstar_kb"] = P_KB ** 6 // 2 ** 128
    exp["bstar_m31"] = P_M31 ** 4 // 2 ** 100
    exp["consumed_kb"] = bbk + exp["dim2_kb"]
    exp["remaining_kb"] = exp["bstar_kb"] - exp["consumed_kb"]
    exp["delta_q_kb"] = exp["bstar_kb"] - bbk
    exp["tightened_kb"] = exp["bstar_kb"] - exp["dim2_kb"]
    exp["consumed_m31"] = bbm + exp["dim2_m31"]
    exp["remaining_m31"] = exp["bstar_m31"] - exp["consumed_m31"]
    exp["delta_q_m31"] = exp["bstar_m31"] - bbm
    exp["tightened_m31"] = exp["bstar_m31"] - exp["dim2_m31"]
    exp["additive_total_m31"] = bbm + exp["dim2_m31"] + RUNG_690_M
    exp["additive_slack_m31"] = exp["bstar_m31"] - exp["additive_total_m31"]
    exp["rung_as_q_total_m31"] = RUNG_690_M + exp["dim2_m31"]
    exp["rung_as_q_slack_m31"] = exp["bstar_m31"] \
        - exp["rung_as_q_total_m31"]
    exp["upside_tightened_m31"] = exp["bstar_m31"] - exp["sharp_m31"]
    exp["C_n_2"], exp["C_n_3"] = Cn2, Cn3
    assert sorted(exp) == sorted(v)
    for k in sorted(exp):
        assert exp[k] == v[k], ("fourth-route ledger drift", k)
    # exact reconstruction identities (algorithm-independent)
    assert v["consumed_m31"] + v["remaining_m31"] == v["bstar_m31"]
    assert v["dim2_m31"] + v["tightened_m31"] == v["bstar_m31"]
    assert v["additive_total_m31"] + v["additive_slack_m31"] \
        == v["bstar_m31"]
    assert v["rung_as_q_total_m31"] + v["rung_as_q_slack_m31"] \
        == v["bstar_m31"]
    assert v["additive_total_m31"] == bbm + v["dim2_m31"] + RUNG_690_M
    assert v["dim2_m31"] * (om_m31 - 1) + v["dim2_rem_m31"] == Cn2
    assert v["dim2_kb"] * (om_kb - 1) + v["dim2_rem_kb"] == Cn2
    assert 0 <= v["dim2_rem_m31"] < om_m31 - 1
    assert 0 <= v["dim2_rem_kb"] < om_kb - 1
    assert v["consumed_kb"] + v["remaining_kb"] == v["bstar_kb"]
    assert v["dim2_kb"] + v["tightened_kb"] == v["bstar_kb"]
    # the designed headline integers
    assert v["dim2_kb"] == 2241377 and v["dim2_m31"] == 2241322
    assert v["additive_slack_m31"] == 13435
    assert v["rung_as_q_slack_m31"] == 1766135
    assert v["consumed_m31"] == 3994022 and v["remaining_m31"] == 12783193
    assert v["delta_q_m31"] == 15024515 and v["tightened_m31"] == 14535893
    assert v["sharp_kb"] == 4 == v["sharp_m31"]
    assert v["C_n_3"] > v["bstar_kb"] and v["C_n_3"] > v["bstar_m31"]
    # displays at 128-bit mantissa (generator: 80-bit)
    d = t4["displays"]
    assert d["dim2_kb"] == "%.4f" % lg2_128(v["dim2_kb"]) == "21.0960"
    assert d["dim2_m31"] == "%.4f" % lg2_128(v["dim2_m31"]) == "21.0959"
    assert d["C_n_3"] == "%.4f" % lg2_128(v["C_n_3"]) == "60.4150"
    assert d["remaining_m31"] == "%.4f" % lg2_128(v["remaining_m31"])
    assert d["delta_q_m31"] == "%.4f" % lg2_128(v["delta_q_m31"])
    assert d["tightened_m31"] == "%.4f" % lg2_128(v["tightened_m31"])
    assert d["spare_bits_m31"] == "%.4f" % (
        lg2_128(v["delta_q_m31"]) - lg2_128(v["dim2_m31"])) == "2.7449"
    assert d["tightened_margin_m31_mca"] == "%.4f" % (
        lg2_128(v["tightened_m31"]) - lg2_128(bbm)) == "3.0520"
    assert d["tightened_margin_m31_list"] == "%.4f" % (
        lg2_128(v["tightened_m31"])
        - lg2_128(cert["gate_t4_deployed"]["rows"]["m31_list"]
                  ["floor_BB"])) == "2.8661"
    assert d["naming_price_bits"] == "%.4f" % (
        lg2_128(v["bstar_m31"]) - lg2_128(v["tightened_m31"])) == "0.2069"
    assert d["rung_headroom_vs_Bstar"] == "%.4f" % (
        lg2_128(v["bstar_m31"]) - lg2_128(RUNG_690_M)) == "0.3938"
    assert d["rung_headroom_vs_tightened"] == "%.4f" % (
        lg2_128(v["tightened_m31"]) - lg2_128(RUNG_690_M)) == "0.1869"
    assert d["additive_slack_bits_5dp"] == "%.5f" % (
        lg2_128(v["bstar_m31"])
        - lg2_128(v["additive_total_m31"])) == "0.00116"
    assert d["rung_as_q_slack_bits"] == "%.4f" % (
        lg2_128(v["bstar_m31"])
        - lg2_128(v["rung_as_q_total_m31"])) == "0.1605"
    assert d["upside_margin_m31_mca"] == "%.4f" % (
        lg2_128(v["upside_tightened_m31"]) - lg2_128(bbm)) == "3.2589"
    assert d["kb_fit_below_residual_bits"] == "%.4f" % (
        lg2_128(v["delta_q_kb"]) - lg2_128(v["dim2_kb"])) == "36.8362"
    assert d["kb_tightened_margin"] == "%.4f" % (
        lg2_128(v["tightened_kb"]) - lg2_128(bbk)) == "22.1969"
    # the omega typo trap and the P2 float gate, re-run
    for nm, om in (("kb", om_kb), ("m31", om_m31)):
        typo = Cn2 // (om - 1001)
        assert typo - v["dim2_%s" % nm] == 2287
        assert round(lg2_128(v["dim2_%s" % nm]), 1) == 21.1
    print("deployed: OK (B_B third route all four rows; fourth route + "
          "reconstruction identities on all %d ledger integers; 128-bit "
          "mantissa displays incl. slack 13435 = 0.00116 bits)"
          % len(v))


# ---------------------------------------------------------------- oracles
def check_oracles(root, cert):
    t5 = cert["gate_t5_oracles"]
    for key, rel in (("oracle_777", ORACLE_777_REL),
                     ("oracle_690", ORACLE_690_REL),
                     ("oracle_omega", ORACLE_OMEGA_REL)):
        o = json.loads((root / rel).read_text(encoding="utf-8"))
        assert o.get("payload_sha256") == payload_hash(o), key
        assert t5[key]["payload_sha256"] == o["payload_sha256"], key
    assert t5["oracle_budget_fit"]["file_sha256"] \
        == file_sha256(root / BUDGET_FIT_REL)
    assert t5["oracle_f_dim2_skeleton"]["file_sha256"] \
        == file_sha256(root / SKEL_CERT_REL)
    assert t5["oracle_f_dim2_evidence"]["n16_file_sha256"] \
        == file_sha256(root / EVID_CERT_REL)
    assert t5["oracle_f_dim2_evidence"]["j4_file_sha256"] \
        == file_sha256(root / EVID_J4_CERT_REL)
    t2 = cert["gate_t2_f97"]
    assert t2["oracle"]["note_sha256"] == file_sha256(root / NOTE_792_REL)
    assert t2["oracle"]["verifier_sha256"] \
        == file_sha256(root / SCRIPT_792_REL)
    assert DIGEST_792 in (root / SCRIPT_792_REL).read_text(encoding="utf-8")
    assert t2["oracle"]["embedded_canonical_digest"] == DIGEST_792
    c690 = json.loads((root / ORACLE_690_REL).read_text(encoding="utf-8"))
    wi = c690["watch_item"]
    assert wi["M"] == RUNG_690_M == 12769758
    assert wi["margin_bits"] == -0.3938 and wi["B_star"] == 16777215
    c777 = json.loads((root / ORACLE_777_REL).read_text(encoding="utf-8"))
    assert c777["placement_computed"] == "BOUNDARY_Q_OWNED"
    bf = json.loads((root / BUDGET_FIT_REL).read_text(encoding="utf-8"))
    d2row = bf["P2_fixed_deficiency_ledger"][1]
    assert d2row["deficiency"] == 2 and d2row["log2_value_approx"] == 21.1
    print("oracles: OK (3 payload hashes, 6 file hashes, #690 watch "
          "rung, #777 placement convention, budget-fit P2 row)")


# ---------------------------------------------------------------- main
def run(root: Path) -> int:
    cert = json.loads((root / CERT_REL).read_text(encoding="utf-8"))
    assert cert.get("payload_sha256") == payload_hash(cert), "cert self-hash"
    check_pins(root, cert)
    o73 = check_f73(cert)
    o289 = check_fp2(cert)
    o97 = check_f97(cert)
    # recompute the aggregate placement outcome from this file's own
    # censuses (three admissible outcomes; none presupposed)
    outcomes = {o73, o289, o97["A"], o97["B"]}
    if "FRESH_B_CELL" in outcomes:
        placement = "FRESH_B_CELL"
    elif "TANGENT_OWNED" in outcomes:
        placement = "TANGENT_OWNED"
    else:
        placement = "COMMON_GCD_OWNED"
    assert placement == cert["placement_computed"], "placement verdict"
    assert cert["placement"]["computed"] == placement
    assert set(cert["placement"]["per_instance"].values()) <= {
        "TANGENT_OWNED", "COMMON_GCD_OWNED", "FRESH_B_CELL"}
    check_deployed(cert)
    check_oracles(root, cert)
    assert cert["status"] == "EXPERIMENTAL / AUDIT"
    assert cert["verdict"].startswith("PLACEMENT COMPUTED: %s" % placement)
    assert "CONDITIONAL_ON_NAMED_INPUT" in cert["verdict"]
    assert "Not a resolution" in cert["verdict"]
    assert "13,435" in cert["joint_ledger_m31"]["sentence"] or \
        "13435" in cert["joint_ledger_m31"]["sentence"]
    assert cert["joint_ledger_m31"]["reading_1_fully_additive"][
        "slack_exact_integer"] == 13435
    assert cert["joint_ledger_m31"]["reading_2_rung_is_the_q_payment"][
        "slack_exact_integer"] == 1766135
    print("placement (recomputed by divisor censuses):", placement)
    print("RESULT: PASS")
    print("payload_sha256:", cert["payload_sha256"])
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    if not args.check:
        ap.print_help()
        return 2
    try:
        return run(repo_root())
    except AssertionError as exc:
        print("RESULT: FAIL", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
