#!/usr/bin/env python3
"""Independent checker for bc-chart-typing (no generator import).

Every stored verdict is recomputed by a route disjoint from the generator:

  placement d1   generator: shifted-weak-Popov reduction.
                 here: direct RANK TESTS -- the linear system
                 W(x)U(x) = N(x) on D with wdeg(W,N) <= w' has only the
                 zero solution (d1 >= w'+1), plus the explicit module
                 element (X - alpha, U_z - zeta) realizing wdeg = w'+1
                 (d1 <= w'+1).  No Popov code anywhere in this file.
  F_73 fibers    generator: windowed leading-coefficient DFS.
                 here: itertools.combinations over complements + power
                 sums + Newton identities.
  F_289          generator: precomputed 289x289 tables.
                 here: on-the-fly two-component arithmetic (a + b t,
                 t^2 = 3 over F_17).
  deployed       generator: Legendre+product-tree AND Kummer+heap.
                 here: THIRD route -- binary-splitting falling-factorial /
                 factorial products with one exact big division
                 (math.comb is NOT feasible at n = 2^21: ~240 s measured;
                 math.comb is used at toy scale only), plus math.lgamma
                 cross-estimates of every log2 display.
  #721 census    generator: coefficient-list construction of Q_S.
                 here: direct product evaluation Q_S(13) = prod (13 - x).
  pins/oracles   re-scanned fresh; self-hashes and file hashes recomputed.

The checker recomputes the placement outcome from its own rank tests and
asserts the stored verdict matches.  Exit 0 with RESULT: PASS, nonzero
otherwise.  Accepts --check.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import sys
from pathlib import Path

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

GF_PINS = {
    "prob:saturated-bc": ("label", 2191),
    "cor:bc-one-pencil": ("label", 1764),
    "thm:bc-moving-root": ("label", 1735),
    "def:projective-locator-pencil": ("label", 1722),
    "prop:boundary-q": ("label", 1475),
    "prop:bc-not-q": ("label", 2120),
    "def:q-row-atom": ("label", 2043),
    "def:first-match-ledger": ("label", 148),
    "rem:bc-status-after-moving-root": ("label", 1785),
    "prop:pole-line": ("label", 583),
    "prop:rank-one-floor": ("label", 1523),
    "prop:rank-one-distinct-slope-floor": ("label", 1546),
    "prop:line-ray-saturation": ("label", 1867),
    "thm:finite": ("label", 2022),
    "prop:extension-cell-target": ("label", 402),
    "thm:near-rational": ("label", 1350),
    "cor:near-rational-line": ("label", 1381),
    "prop:lattice-split": ("label", 1336),
    "prop:slope-elimination": ("label", 1320),
    "In all four rows \\(p>H_{\\rm ext}\\)": ("content", 425),
}
FRONT_PINS = {
    "thm:exact-list-line-bijection": ("label", 2097),
    "cor:exact-prefix-ray-realization": ("label", 2157),
}
BCSEC_PINS = {
    "An interior balanced profile": ("content", 24),
    "The excluded endpoint": ("content", 29),
}
NOTE_721_PINS = {
    "`d = 1` formulas below are retained as a collision-literal audit":
        ("content", 14),
    "F_RH = {S in binom(D,5):sum_{x in S}x=0 in F_17},": ("content", 447),
    "The full multiplicity certificate is": ("content", 451),
    "supports = LineRay pairs = 76,": ("content", 461),
}

CENSUS_721 = {0: 4, 1: 4, 2: 5, 3: 7, 4: 5, 5: 6, 6: 4, 7: 4,
              8: 6, 9: 5, 10: 5, 11: 7, 12: 3, 14: 5, 15: 3, 16: 3}


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


def lg2_display_128(x: int) -> str:
    """independent display route: top-128-bit mantissa (generator: 80)."""
    e = x.bit_length() - 1
    if e <= 128:
        return "%.4f" % math.log2(x)
    return "%.4f" % (math.log2(x >> (e - 128)) + (e - 128))


# ---------------------------------------------------------------- pins
def check_pins(root, cert):
    for rel, pins in ((GF_REL, GF_PINS), (FRONT_REL, FRONT_PINS),
                      (BCSEC_REL, BCSEC_PINS), (NOTE_721_REL, NOTE_721_PINS)):
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
    n = sum(len(v) for v in (GF_PINS, FRONT_PINS, BCSEC_PINS, NOTE_721_PINS))
    print("pins: OK (%d pins at expected lines)" % n)


# ---------------------------------------------------------------- F_73
P = 73
N = 24
K = 12
M = 15
W = M - K
OMEGA = N - M
SHIFT = K - 1


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
    """all depth-3 fibers of 15-subsets, via complement power sums +
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
    for R in itertools.combinations(idxs, OMEGA):     # complement, size 9
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
    return list(zstar), members[zstar], best


def rank_gauss(mat, addf, subf, mulf, invf, is_zero):
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
        pinv = invf(mat[r][c])
        mat[r] = [mulf(pinv, x) for x in mat[r]]
        for i in range(len(mat)):
            if i != r and not is_zero(mat[i][c]):
                f = mat[i][c]
                mat[i] = [subf(x, mulf(f, y))
                          for x, y in zip(mat[i], mat[r])]
        r += 1
        if r == len(mat):
            break
    return r


def rank73(mat):
    return rank_gauss(mat, None, lambda a, b: (a - b) % P,
                      lambda a, b: a * b % P,
                      lambda a: pow(a, P - 2, P), lambda a: a % P == 0)


def check_f73(cert):
    g1 = cert["gate_1_placement_f73"]
    D = build_domain()
    zstar, members, best = f73_fiber_newton(D)
    assert zstar == g1["z_star"], "z* drift (Newton route)"
    assert best == g1["fiber_size"] == len(members) == 13
    stored_members = [tuple(t) for t in g1["fiber_members"]]
    assert sorted(stored_members) == sorted(tuple(t) for t in members)

    alpha = g1["alpha"]
    assert alpha == min(a for a in range(P) if a not in set(D))
    # U_z evaluations and slopes, independently
    def Uz_at(x):
        v = pow(x, M, P)
        for h, zz in enumerate(zstar, 1):
            v = (v + zz * pow(x, M - h, P)) % P
        return v
    Ua = Uz_at(alpha)
    slope_of = {}
    for T in stored_members:
        ls = 1
        for i in T:
            ls = ls * ((alpha - D[i]) % P) % P
        slope_of.setdefault((Ua - ls) % P, []).append(T)
    assert len(slope_of) == g1["n_distinct_slopes"] == len(g1["d1_rows"])
    assert sorted(slope_of) == [r["zeta"] for r in g1["d1_rows"]]

    # placement by rank tests (NO Popov)
    boundary = 0
    for row in g1["d1_rows"]:
        zeta = row["zeta"]
        U = [(Uz_at(x) - zeta) * pow((x - alpha) % P, P - 2, P) % P
             for x in D]
        # (a) no nonzero (W,N), deg W <= w', deg N <= w'+SHIFT: nullity 0
        mat = []
        for idx, x in enumerate(D):
            r = [pow(x, i, P) * U[idx] % P for i in range(W + 1)]
            r += [(-pow(x, j, P)) % P for j in range(W + SHIFT + 1)]
            mat.append(r)
        nunk = (W + 1) + (W + SHIFT + 1)
        assert rank73(mat) == nunk, "rank test: nonzero wdeg<=w' element"
        # (b) explicit element (X - alpha, U_z - zeta) at wdeg w'+1
        for idx, x in enumerate(D):
            assert (x - alpha) * U[idx] % P == (Uz_at(x) - zeta) % P
        # deg(X-alpha)=1, deg(U_z - zeta)=M -> wdeg = max(1, M-SHIFT) = W+1
        assert max(1, M - SHIFT) == W + 1
        assert row["d1"] == W + 1
        boundary += 1
    lo, hi = g1["interior_profile_range"]
    assert (lo, hi) == (W + 2, (N - K + 1) // 2)
    assert g1["counts"] == {"near_rational": 0, "boundary": boundary,
                            "interior": 0}

    # locator rank, independent elimination
    locs = []
    for T in stored_members:
        comp = [i for i in range(N) if i not in T]
        poly = [1]
        for i in comp:
            new = [0] * (len(poly) + 1)
            for j, a in enumerate(poly):
                new[j] = (new[j] - a * D[i]) % P
                new[j + 1] = (new[j + 1] + a) % P
            poly = new
        locs.append([poly[t] if t < len(poly) else 0
                     for t in range(OMEGA + 1)])
    rk = rank73(locs)
    assert rk == g1["locator_matrix_rank"] and rk > 2
    assert g1["counting_cap_max_over_g"] \
        == max((N - g) // (OMEGA - g) for g in range(OMEGA)) \
        == N - OMEGA + 1
    assert g1["counting_exclusion_bites"] is (13 > N - OMEGA + 1)
    print("F_73: OK (fiber 13 by Newton route; d1 = w'+1 = 4 by rank "
          "tests at %d slopes; locator rank %d > 2)"
          % (len(slope_of), rk))
    return boundary


# ---------------------------------------------------------------- F_289
PB = 17
NR = 3
N2 = 16
K2 = 6
M2 = 9
W2 = M2 - K2
OM2 = N2 - M2
SHIFT2 = K2 - 1
D2 = list(range(1, 17))    # base-field elements, pairs (x, 0)


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


def fzero(a):
    return a == (0, 0)


def enc2(a):
    """integer encoding used by the certificate: a + 17*b."""
    return a[0] + PB * a[1]


def dec2(e):
    return (e % PB, e // PB)


def rank289(mat):
    return rank_gauss(mat, None, fsub, fmul, finv, fzero)


def check_fp2(cert):
    g1 = cert["gate_1_placement_fp2"]
    # fibers via itertools (independent from generator's fibers2 only in
    # arithmetic backend; the subset enumeration is the spec)
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
    assert list(zstar) == g1["z_star"]
    assert best3 == g1["heaviest_depth_wprime_fiber"] == 5
    wit = fib2[zstar[:2]]
    assert len(wit) == g1["witness_fiber_size"] == 40
    assert sorted(tuple(t) for t in g1["witness_fiber_members"]) \
        == sorted(wit)

    def Uz_at(x):
        v = (0, 0)
        xp = (1, 0)
        pows = []
        for _ in range(M2 + 1):
            pows.append(xp)
            xp = fmul(xp, x)
        v = pows[M2]
        for h, zz in enumerate(zstar, 1):
            v = fadd(v, fmul((zz, 0), pows[M2 - h]))
        return v

    boundary_total = 0
    for arow in g1["alpha_rows"]:
        alpha = dec2(arow["alpha"])
        Ua = Uz_at(alpha)
        slope_of: dict[int, int] = {}
        for T in wit:
            ls = (1, 0)
            for i in T:
                ls = fmul(ls, fsub(alpha, (D2[i], 0)))
            z = enc2(fsub(Ua, ls))
            slope_of[z] = slope_of.get(z, 0) + 1
        assert len(slope_of) == arow["n_distinct_slopes"]
        assert 40 - len(slope_of) == arow["slope_collisions"]
        boundary = 0
        for zenc in sorted(slope_of):
            zeta = dec2(zenc)
            U = [fmul(fsub(Uz_at((x, 0)), zeta),
                      finv(fsub((x, 0), alpha))) for x in D2]
            mat = []
            for idx, x in enumerate(D2):
                pows = [(1, 0)]
                for _ in range(W2 + SHIFT2):
                    pows.append(fmul(pows[-1], (x, 0)))
                r = [fmul(pows[i], U[idx]) for i in range(W2 + 1)]
                r += [fsub((0, 0), pows[j]) for j in range(W2 + SHIFT2 + 1)]
                mat.append(r)
            nunk = (W2 + 1) + (W2 + SHIFT2 + 1)
            assert rank289(mat) == nunk, "F_289 rank test"
            for idx, x in enumerate(D2):
                lhs = fmul(fsub((x, 0), alpha), U[idx])
                assert lhs == fsub(Uz_at((x, 0)), zeta)
            assert max(1, M2 - SHIFT2) == W2 + 1
            boundary += 1
        assert arow["d1_values"] == [W2 + 1]
        assert arow["n_boundary"] == boundary
        assert arow["n_near_rational"] == 0 and arow["n_interior"] == 0
        boundary_total += boundary

    locs = []
    for T in wit:
        comp = [i for i in range(N2) if i not in T]
        poly = [(1, 0)]
        for i in comp:
            new = [(0, 0)] * (len(poly) + 1)
            for j, a in enumerate(poly):
                new[j] = fsub(new[j], fmul(a, (D2[i], 0)))
                new[j + 1] = fadd(new[j + 1], a)
            poly = new
        locs.append([poly[t] if t < len(poly) else (0, 0)
                     for t in range(OM2 + 1)])
    rk = rank289(locs)
    assert rk == g1["locator_matrix_rank"] and rk > 2
    assert g1["counting_cap_max_over_g"] \
        == max((N2 - g) // (OM2 - g) for g in range(OM2)) == N2 - OM2 + 1
    assert g1["counting_exclusion_bites"] is (40 > N2 - OM2 + 1)
    print("F_17^2: OK (witness fiber 40; d1 = w'+1 = 4 by rank tests at "
          "3 alphas; locator rank %d > 2; counting cap %d < 40)"
          % (rk, N2 - OM2 + 1))
    return boundary_total


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
    """C(n, r) by binary-splitting products + one exact division, using
    the smaller side (math.comb at this scale measured ~240 s; this route
    ~60 s)."""
    r = min(r, n - r)
    num = prod_range(n - r + 1, n)
    den = prod_range(1, r)
    C, rem = divmod(num, den)
    assert rem == 0
    return C


def check_deployed(cert):
    sys.setrecursionlimit(10000)
    g2 = cert["gate_2_deployed"]
    assert g2["two_routes_agree_exactly_on_all_four_rows"] is True
    combs = {}
    combs[1116048] = comb_third_route(N_DEP, 1116048)
    Cm, mp = combs[1116048], 1116048
    while mp > 1116023:
        num = Cm * mp
        assert num % (N_DEP - mp + 1) == 0
        Cm = num // (N_DEP - mp + 1)
        mp -= 1
        combs[mp] = Cm
    bstar = {"kb": P_KB ** 6 // 2 ** 128, "m31": P_M31 ** 4 // 2 ** 100}
    assert bstar["kb"] == 274980728111395087
    assert bstar["m31"] == 16777215
    ln2 = math.log(2)
    for name, p, bs in (("kb_mca", P_KB, bstar["kb"]),
                        ("kb_list", P_KB, bstar["kb"]),
                        ("m31_mca", P_M31, bstar["m31"]),
                        ("m31_list", P_M31, bstar["m31"])):
        row = g2["rows"][name]
        a, w = row["a_plus"], row["w"]
        C = combs[a]
        pw = p ** w
        BB = -(-C // pw)
        assert BB == row["floor_BB"], (name, "floor drift (third route)")
        assert pw * bs // C == row["H_ext"], (name, "H_ext drift")
        assert row["B_star"] == bs
        assert lg2_display_128(BB) == row["floor_BB_log2_display"]
        # margin display via independent mantissa width
        e1 = bs.bit_length() - 1
        l_bs = math.log2(bs) if e1 <= 128 else \
            math.log2(bs >> (e1 - 128)) + (e1 - 128)
        e2 = BB.bit_length() - 1
        l_bb = math.log2(BB) if e2 <= 128 else \
            math.log2(BB >> (e2 - 128)) + (e2 - 128)
        assert "%.4f" % (l_bs - l_bb) == row["margin_bits_display"]
        # lgamma cross-estimate of log2 C(n, a)
        lgC = (math.lgamma(N_DEP + 1) - math.lgamma(a + 1)
               - math.lgamma(N_DEP - a + 1)) / ln2
        e3 = C.bit_length() - 1
        lgC_exact = math.log2(C >> (e3 - 128)) + (e3 - 128)
        assert abs(lgC - lgC_exact) < 1e-6, (name, "lgamma cross-estimate")
        assert BB > row["H_ext"]
    # omega rows and the prop:bc-not-q dimensions
    for name, a in (("kb_mca", 1116048), ("m31_mca", 1116024)):
        orow = g2["omega_rows"][name]
        omega = N_DEP - a
        assert orow["omega_correct"] == omega
        assert orow["omega_printed_in_cor_table"] == omega - 1000
        assert N_DEP // omega == 2 == N_DEP // (omega - 1000)
        assert orow["dim_omega_minus_w"] == omega - (a - K_DEP)
        # pencil-cap sweep, re-run
        x = cert["gate_3_non_pencil"]["rows"][name]
        cap_max = max((N_DEP - g) // (omega - g) for g in range(omega))
        assert cap_max == x["pencil_cap_sweep_max"] == a + 1
        assert x["pencil_cap_sweep_argmax_g"] == omega - 1
        BB = g2["rows"][name]["floor_BB"]
        assert BB > cap_max and x["exclusion_excess"] == BB - cap_max
        qexp = 6 if name == "kb_mca" else 4
        p = g2["rows"][name]["p"]
        q = p ** qexp
        assert (BB * (BB - 1) // 2 * (K_DEP - 1) < q - p) is \
            x["slope_level_unconditional"]["some_alpha_has_zero_collisions"]
        bs = g2["rows"][name]["B_star"]
        cond = x["conditional_on_max_fiber_le_Bstar"]
        assert (bs * (bs - 1) // 2 * (K_DEP - 1) < q - p) is \
            cond["full_fiber_slope_separation_alpha_exists"]
        assert (q > N_DEP + (K_DEP - 1) * (bs * (bs - 1) // 2)) is \
            cond["separating_pole_exists_thm_4_6"]
    print("deployed: OK (third route agrees on all four rows; lgamma "
          "cross-estimates < 1e-6; H_ext, omega, dims, cap sweeps, "
          "exclusions all reproduced)")


# ---------------------------------------------------------------- oracles
def check_oracles(root, cert):
    g4 = cert["gate_4_oracles"]
    for key, rel in (("oracle_715", ORACLE_715_REL),
                     ("oracle_omega", ORACLE_OMEGA_REL),
                     ("oracle_690", ORACLE_690_REL)):
        o = json.loads((root / rel).read_text(encoding="utf-8"))
        assert o.get("payload_sha256") == payload_hash(o), key
        assert g4[key]["payload_sha256"] == o["payload_sha256"], key
    assert g4["oracle_budget_fit"]["file_sha256"] \
        == file_sha256(root / BUDGET_FIT_REL)
    assert g4["oracle_721"]["file_sha256"] \
        == file_sha256(root / NOTE_721_REL)
    # #721 census, independent route: Q_S(13) by direct product
    mult: dict[int, int] = {}
    for S in itertools.combinations(range(13), 5):
        if sum(S) % 17:
            continue
        qv = 1
        for x in S:
            qv = qv * (13 - x) % 17
        psi = (pow(13, 5, 17) - qv) % 17
        mult[psi] = mult.get(psi, 0) + 1
    assert mult == CENSUS_721
    assert sum(mult.values()) == 76 and len(mult) == 16
    stored = {int(k): v for k, v
              in g4["oracle_721"]["d1_census_replayed"]
              ["multiplicities"].items()}
    assert stored == mult
    # watch-item fields
    wi = g4["oracle_690"]["watch_item"]
    assert wi["M"] == 12769758 and wi["margin_bits"] == -0.3938
    assert wi["B_star"] == 16777215
    print("oracles: OK (3 payload hashes, 2 file hashes, #721 census by "
          "product route, #690 watch-item fields)")


# ---------------------------------------------------------------- main
def run(root: Path) -> int:
    cert = json.loads((root / CERT_REL).read_text(encoding="utf-8"))
    assert cert.get("payload_sha256") == payload_hash(cert), "cert self-hash"
    check_pins(root, cert)
    b73 = check_f73(cert)
    b289 = check_fp2(cert)
    # recompute the placement outcome from this file's own rank tests
    placement = "BOUNDARY_Q_OWNED" if (b73 > 0 and b289 > 0) else "OTHER"
    assert placement == cert["placement_computed"], "placement verdict"
    check_deployed(cert)
    check_oracles(root, cert)
    assert cert["status"] == "EXPERIMENTAL / AUDIT"
    assert "CONDITIONAL_ON_NAMED_INPUT" in cert["verdict"]
    assert "Not a resolution" in cert["verdict"]
    print("placement (recomputed by rank tests):", placement)
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
