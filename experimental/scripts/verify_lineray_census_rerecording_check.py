#!/usr/bin/env python3
"""Independent checker for lineray-census-rerecording (no generator import).

Every stored number is recomputed by a route disjoint from the generator:

  fibers        generator: windowed leading-coefficient DFS.
                here: itertools.combinations + complement power sums +
                Newton identities (e_h from p_1..p_h, divisions by h).
  censuses      generator: duality functionals + first-K interpolation.
                here: own hit scan + ray grouping with per-ray saturation
                assertion count == C(agr, m) (r1 _check style); for the
                F_{17^2} lines a full 289-slope sweep (no rank-one scan):
                stored slopes must census to their stored multiplicity and
                profile, absent slopes must census to zero.
  d1            generator: shifted-weak-Popov reduction.
                here: direct rank tests (the linear system with
                wdeg <= d1-1 has only the zero solution) plus an explicit
                locator pair realizing wdeg = d1.
  F_289         generator: precomputed 289x289 tables.
                here: on-the-fly two-component arithmetic (a + b t,
                t^2 = 3 over F_17).
  deployed      generator: Legendre floor-sum exponents + product tree.
                here: Kummer carry-count exponents + smallest-first heap
                merge; bit lengths cross-estimated with an lgamma route.
  oracle certs  re-read, self-hash verified, identities recomputed here.
  pins          re-scanned with fresh line hashes at the expected lines.

Exit 0 with RESULT: PASS, nonzero otherwise.  Accepts --check.
"""
from __future__ import annotations

import argparse
import hashlib
import heapq
import itertools
import json
import math
import sys
from operator import mul
from pathlib import Path

CERT_REL = Path(
    "experimental/data/certificates/lineray-census-rerecording/"
    "lineray_census_rerecording.json"
)
CAP_REL = Path("experimental/cap25_cap_v13_raw.tex")
GF_REL = Path("experimental/grande_finale.tex")
ORACLE_R1_REL = Path(
    "experimental/data/certificates/r1-rawcount-refutation/"
    "r1_rawcount_refutation.json"
)
ORACLE_SPC_REL = Path(
    "experimental/data/certificates/split-pencil-ray-collapse/"
    "split_pencil_ray_collapse.json"
)

CAP_PINS = {
    "prob:capfp-R1": ("label", 8278),
    "prob:capfr1-rank-one-census": ("label", 7819),
    "prob:capg-split-pencil-B": ("label", 9842),
    "prob:capfr1-split-pencil": ("label", 8012),
    "Main aperiodic effort": ("content", 8077),
    "prob:capg-active-BC": ("label", 9919),
    "prop:capg-census-floor": ("label", 9728),
    "rem:capg-subfield-scope": ("label", 9874),
    "lem:capg-witness": ("label", 9183),
    "rem:capg-witnessrel": ("label", 9246),
    "rem:capg-band": ("label", 9397),
    "rem:capg-boundary-offbyone": ("label", 9828),
    "prob:capfr1-normalized-band": ("label", 7639),
}
GF_PINS = {
    "def:line-rays": ("label", 1857),
    "prop:line-ray-saturation": ("label", 1867),
    "prob:saturated-bc": ("label", 2191),
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def payload_hash(obj) -> str:
    clone = dict(obj)
    clone.pop("payload_sha256", None)
    blob = json.dumps(clone, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def holds(count, terms):
    return count <= 1 or any(count * den <= num for num, den in terms)


# ---------------------------------------------------------------- pins
def check_pins(root, cert):
    for rel, pins in ((CAP_REL, CAP_PINS), (GF_REL, GF_PINS)):
        lines = (root / rel).read_text(encoding="utf-8").splitlines()
        stored = cert["statement_pins"][rel.name]
        assert sorted(stored) == sorted(pins), "pin set drift in %s" % rel.name
        for key, (kind, expected) in pins.items():
            pin = stored[key]
            assert pin["kind"] == kind and pin["line"] == expected
            line = lines[expected - 1]
            needle = ("\\label{%s}" % key) if kind == "label" else key
            assert needle in line, "pin moved: %s" % key
            assert hashlib.sha256(
                line.encode("utf-8")).hexdigest()[:16] == pin["sha256_line"], \
                "pin hash drift: %s" % key
    n = len(CAP_PINS) + len(GF_PINS)
    print("pins: OK (%d pins at expected lines)" % n)


# ---------------------------------------------------------------- oracles
def check_oracles(root, cert):
    spc = json.loads((root / ORACLE_SPC_REL).read_text(encoding="utf-8"))
    r1 = json.loads((root / ORACLE_R1_REL).read_text(encoding="utf-8"))
    assert spc.get("payload_sha256") == payload_hash(spc)
    assert r1.get("payload_sha256") == payload_hash(r1)
    a = cert["gate_a_oracle_replay"]
    assert a["oracle_spc"]["payload_sha256"] == spc["payload_sha256"]
    assert a["oracle_r1"]["payload_sha256"] == r1["payload_sha256"]

    m = 15
    in_scope = [r for r in spc["rows"] if r.get("in_scope")]
    assert len(in_scope) == len(a["spc_rows"]) == 11
    for row, st in zip(in_scope, a["spc_rows"]):
        assert st["label"] == row["label"]
        assert row["gate"] is True and row["rays"] == row["list"]
        assert row["raw_census"] == sum(
            math.comb(x, m) for x in row["ray_agreements"])
        assert (st["raw"], st["rays"], st["list"]) == \
            (row["raw_census"], row["rays"], row["list"])

    ceil_p = a["toy_dedup_model_terms"]["ceil_p_term"]
    assert ceil_p == -(-math.comb(24, 15) // 73 ** 3) == 4
    q_term = a["toy_dedup_model_terms"]["q_term"]
    assert q_term == [math.comb(24, 15), 73 ** 2]
    assert len(r1["toy_rows"]) == len(a["r1_rows"]) == 4
    for row, st in zip(r1["toy_rows"], a["r1_rows"]):
        assert st["label"] == row["label"]
        mults = [sr[1] for sr in row["slope_rows"]]
        profs = [sr[2] for sr in row["slope_rows"]]
        for m2, pf in zip(mults, profs):
            assert m2 == sum(math.comb(x, m) for x in pf)
        lineray = sum(len(pf) for pf in profs)
        assert st["rank_one"] == row["counts"]["rank_one"] == sum(mults)
        assert st["lineray"] == lineray == row["lineray_count"]
        assert st["n_slopes"] == len(mults) == row["slopes_hit"]
        assert st["n_slopes"] <= st["lineray"]
        assert st["loss2"] == st["rank_one"] - lineray
        assert holds(lineray, [[ceil_p, 1], q_term])
        assert st["recorded_dedup_model_holds"] is True
    assert cert["gate_a_oracle_replay"]["r1_deployed_corrected_middle_ceil"] \
        == r1["deployed"]["budget"]["corrected_middle_ceil"] == 65065153468
    print("oracles: OK (self-hashes verified; identities recomputed; "
          "recorded dedup model holds at all 4 #679 lines)")


# ---------------------------------------------------------------- F_73 toy
P = 73
N = 24
K = 12
M = 15
W = M - K
OMEGA = N - M


def toy_domain():
    for g in range(2, P):
        seen, x = set(), 1
        for _ in range(P - 1):
            x = x * g % P
            seen.add(x)
        if len(seen) == P - 1:
            return sorted(pow(g, 3 * j, P) for j in range(N))
    raise AssertionError


def _pnorm(f):
    f = list(f)
    while f and f[-1] == 0:
        f.pop()
    return f


def _padd(f, g):
    L = max(len(f), len(g))
    return _pnorm([((f[i] if i < len(f) else 0) + (g[i] if i < len(g) else 0))
                   % P for i in range(L)])


def _pscale(f, c):
    c %= P
    return _pnorm([c * a % P for a in f])


def _pmul(f, g):
    if not f or not g:
        return []
    out = [0] * (len(f) + len(g) - 1)
    for i, a in enumerate(f):
        if a:
            for j, b in enumerate(g):
                out[i + j] = (out[i + j] + a * b) % P
    return _pnorm(out)


def _peval(f, x):
    r = 0
    for a in reversed(f):
        r = (r * x + a) % P
    return r


def newton_prefix(psums, depth, mod):
    """(-1)^h e_h for h = 1..depth from power sums p_1..p_depth (mod)."""
    e = [1] + [0] * depth
    for h in range(1, depth + 1):
        s = 0
        sgn = 1
        for i in range(1, h + 1):
            s += sgn * e[h - i] * psums[i]
            sgn = -sgn
        e[h] = s * pow(h, mod - 2, mod) % mod
    return tuple((pow(-1, h, mod) * e[h]) % mod for h in range(1, depth + 1))


def fiber_histogram(D, msize, depth):
    """{prefix: count} over msize-subsets of D via complement power sums
    + Newton identities."""
    csize = N - msize
    powt = [[pow(x, t, P) for t in range(depth + 1)] for x in D]
    tot = [sum(powt[i][t] for i in range(N)) % P for t in range(depth + 1)]
    counts = {}
    for Rc in itertools.combinations(range(N), csize):
        ps = [0] * (depth + 1)
        for t in range(1, depth + 1):
            s = 0
            for i in Rc:
                s += powt[i][t]
            ps[t] = (tot[t] - s) % P
        z = newton_prefix(ps, depth, P)
        counts[z] = counts.get(z, 0) + 1
    assert sum(counts.values()) == math.comb(N, msize)
    return counts


def hit_ids(word, D, lamr):
    T = [sum(word[i] * pow(D[i], t, P) for i in range(N)) % P
         for t in range(13)]
    T1 = tuple(T[1:11])
    T2 = tuple(T[2:12])
    T3 = tuple(T[3:13])
    out = []
    for idx, lam in enumerate(lamr):
        if sum(map(mul, lam, T1)) % P:
            continue
        if sum(map(mul, lam, T2)) % P:
            continue
        if sum(map(mul, lam, T3)) % P:
            continue
        out.append(idx)
    return out


def ray_profile(word, D, lamr, ids):
    strata = {}
    for i in ids:
        lam = lamr[i]
        Sidx = [t for t in range(N) if _peval(lam, D[t]) != 0]
        assert len(Sidx) == M
        pts = [(D[t], word[t]) for t in Sidx[:K]]
        out = []
        for a, (xi, yi) in enumerate(pts):
            num, den = [1], 1
            for b, (xj, _) in enumerate(pts):
                if a == b:
                    continue
                num = _pmul(num, [(-xj) % P, 1])
                den = den * ((xi - xj) % P) % P
            out = _padd(out, _pscale(num, yi * pow(den, P - 2, P)))
        assert len(out) <= K
        for t in Sidx[K:]:
            assert _peval(out, D[t]) == word[t]
        agr = sum(1 for t in range(N) if _peval(out, D[t]) == word[t])
        key = tuple(out[t] if t < len(out) else 0 for t in range(K))
        strata.setdefault(key, {"agr": agr, "count": 0})
        assert strata[key]["agr"] == agr
        strata[key]["count"] += 1
    for st in strata.values():
        assert st["count"] == math.comb(st["agr"], M), "saturation broken"
    profile = sorted((st["agr"] for st in strata.values()), reverse=True)
    return profile, len(strata)


def min_wdeg_ge(U, D, d1, kdim, mod, fmul, fsub, finv):
    """rank test: no nonzero (W, N) in M_U with wdeg <= d1-1.
    Generic over a field given by (fmul, fsub, finv); values as ints."""
    d = d1 - 1
    nW, nN = d + 1, d + kdim
    rows = []
    for i, x in enumerate(D):
        xp = 1
        rowW = []
        for _ in range(nW):
            rowW.append(fmul(U[i], xp))
            xp = fmul(xp, x)
        xp = 1
        rowN = []
        for _ in range(nN):
            rowN.append(fsub(0, xp))
            xp = fmul(xp, x)
        rows.append(rowW + rowN)
    ncols = nW + nN
    r = 0
    for c in range(ncols):
        piv = next((i for i in range(r, len(rows)) if rows[i][c]), None)
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        ic = finv(rows[r][c])
        rows[r] = [fmul(v, ic) for v in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c]:
                f = rows[i][c]
                rows[i] = [fsub(a, fmul(f, b))
                           for a, b in zip(rows[i], rows[r])]
        r += 1
    return r == ncols


def f73_mul(a, b):
    return a * b % P


def f73_sub(a, b):
    return (a - b) % P


def f73_inv(a):
    return pow(a, P - 2, P)


def check_gate_b_toy(cert):
    D = toy_domain()
    lamr = []

    def rec(start, depth, poly):
        if depth == OMEGA:
            lamr.append(tuple(poly))
            return
        need = OMEGA - depth
        for idx in range(start, N - need + 1):
            x = D[idx]
            new = [0] * (depth + 2)
            mx = (-x) % P
            for i2, a in enumerate(poly):
                if a:
                    new[i2] = (new[i2] + a * mx) % P
                    new[i2 + 1] = (new[i2 + 1] + a) % P
            rec(idx + 1, depth + 1, new)

    rec(0, 0, [1])
    assert len(lamr) == math.comb(N, OMEGA)

    for row in cert["gate_b_toy_f73"]["rows"]:
        level, depth = row["level"], row["depth"]
        # heaviest fiber by the independent (Newton) route
        counts = fiber_histogram(D, level, depth)
        best = max(counts.values())
        zstar = min(z for z, c in counts.items() if c == best)
        assert list(zstar) == row["z"], "%s: z* drift" % row["label"]
        assert best == row["fiber"]
        assert row["ceil_floor"] == -(-math.comb(N, level) // P ** depth)
        assert best >= row["ceil_floor"]
        # word consistency
        Pz = [0] * (level + 1)
        Pz[level] = 1
        for h, zz in enumerate(zstar, 1):
            Pz[level - h] = zz
        U = [_peval(Pz, x) for x in D]
        assert U == row["word"]
        # census by own route
        ids = hit_ids(U, D, lamr)
        profile, nrays = ray_profile(U, D, lamr, ids)
        assert len(ids) == row["raw"]
        assert nrays == row["rays"]
        assert profile == row["profile"]
        assert row["loss2"] == row["raw"] - row["rays"]
        if row["label"].startswith("boundary"):
            assert all(a == level for a in profile)
            assert row["raw"] == row["rays"] == best
        else:
            n_at = sum(1 for a in profile if a == level)
            assert n_at == row["rays_at_level"] == best
            extras = sorted((a for a in profile if a != level), reverse=True)
            assert extras == row["extra_agreements"]
            assert len(extras) == row["extras"]
            assert row["raw"] == math.comb(level, M) * best + sum(
                math.comb(a, M) for a in extras)
            assert row["C_mp_m"] == math.comb(level, M)
        # d1 by rank test + explicit locator (1, P): wdeg = level - (K-1)
        d1 = row["d1"]
        assert level - (K - 1) == d1
        assert min_wdeg_ge(U, D, d1, K, P, f73_mul, f73_sub, f73_inv), \
            "%s: wdeg < d1 solution exists" % row["label"]
        print("F_73 %-14s fiber=%-3d RAW=%-4d RAYS=%-3d d1=%d OK "
              "(Newton-fiber + own-census + rank-test routes)"
              % (row["label"], best, len(ids), nrays, d1))


# ---------------------------------------------------------------- deployed
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


def sieve(limit):
    isp = bytearray([1]) * (limit + 1)
    isp[0:2] = b"\x00\x00"
    for i in range(2, int(limit ** 0.5) + 1):
        if isp[i]:
            isp[i * i::i] = bytearray(len(isp[i * i::i]))
    return [i for i in range(limit + 1) if isp[i]]


def heap_comb(a, b, primes):
    heap = [pr ** kummer_e(a, b, pr) for pr in primes
            if pr <= a and kummer_e(a, b, pr)]
    heapq.heapify(heap)
    while len(heap) > 1:
        x = heapq.heappop(heap)
        y = heapq.heappop(heap)
        heapq.heappush(heap, x * y)
    return heap[0] if heap else 1


def _lg2(x):
    e = x.bit_length() - 1
    if e <= 80:
        return math.log2(x)
    return math.log2(x >> (e - 80)) + (e - 80)


def lg2_display(x):
    return "%.4f" % _lg2(x)


def check_gate_b_deployed(cert):
    dep = cert["gate_b_deployed"]
    n_, K_ = 2 ** 21, 2 ** 20
    primes = sieve(n_)
    for name, p_, m_ in (("KB", 2 ** 31 - 2 ** 24 + 1, 1116046),
                         ("M31", 2 ** 31 - 1, 1116022)):
        row = dep["rows"][name]
        assert (row["n"], row["K"], row["m"], row["p"]) == (n_, K_, m_, p_)
        w2 = m_ - K_
        assert row["w_prime"] == w2
        C = heap_comb(n_, m_, primes)
        est = (math.lgamma(n_ + 1) - math.lgamma(m_ + 1)
               - math.lgamma(n_ - m_ + 1)) / math.log(2)
        assert math.floor(est) + 1 == C.bit_length(), "lgamma cross-estimate"
        bf = -(-C // p_ ** w2)
        assert lg2_display(bf) == row["boundary_floor_log2_display"]
        assert ("%.1f" % round(float(lg2_display(bf)), 1)) \
            == row["boundary_paper_prints"]
        Cm, mp = C, m_
        for j, irow in enumerate(row["interior"], 1):
            Cm = Cm * (n_ - mp) // (mp + 1)
            mp += 1
            d1 = w2 + 1 + j
            assert irow["d1"] == "w'+%d" % (1 + j) and irow["m_prime"] == mp
            pw = p_ ** (d1 - 1)
            stripped = -(-Cm // pw)
            assert stripped == irow["stripped_dedup_floor"]
            assert lg2_display(stripped) == irow["stripped_log2_display"]
            assert irow["collapsed_to_1"] == (stripped == 1)
            Cmpm = math.comb(mp, m_)
            assert lg2_display(Cmpm * stripped) \
                == irow["raw_MB_ceil_form_log2_display"]
            unceiled = "%.4f" % (_lg2(Cmpm * Cm) - _lg2(pw))
            assert unceiled == irow["raw_MB_unceiled_log2_display"]
            assert ("%.1f" % round(float(unceiled), 1)) \
                == irow["paper_prints"]
        # budget-fit B_B cross-links: one and two ratio steps at fixed
        # p-power (list-row depth w', MCA-row witness depth w'-1)
        wexp = w2 + 1
        Cm, mp, disp = C, m_, []
        for _ in (1, 2):
            Cm = Cm * (n_ - mp) // (mp + 1)
            mp += 1
            disp.append(lg2_display(-(-Cm // p_ ** wexp)))
        exp = dep["crosslink_budget_fit_BB_displays"][name]
        assert disp[0] == exp["list_row_depth_wprime"]
        assert disp[1] == exp["mca_row_witness_depth"]
        print("deployed %-4s boundary 2^%s interior stripped %s OK "
              "(Kummer+heap route; lgamma agrees)"
              % (name, row["boundary_floor_log2_display"],
                 [i["stripped_dedup_floor"] for i in row["interior"]]))
    assert dep["crosslink_679_corrected_middle_ceil"] == 65065153468


# ---------------------------------------------------------------- F_289 toy
PB = 17
NR2 = 3
Q2 = 289
N2 = 16
K2 = 6
M2 = 9
W2 = M2 - K2
OM2 = N2 - M2


def f2_mul(x, y):
    a1, b1 = x % PB, x // PB
    a2, b2 = y % PB, y // PB
    return (a1 * a2 + NR2 * b1 * b2) % PB + PB * ((a1 * b2 + a2 * b1) % PB)


def f2_add(x, y):
    return (x % PB + y % PB) % PB + PB * ((x // PB + y // PB) % PB)


def f2_neg(x):
    return (-x) % PB + PB * ((-(x // PB)) % PB)


def f2_sub(x, y):
    return f2_add(x, f2_neg(y))


def f2_inv(x):
    a, b = x % PB, x // PB
    nrm = (a * a - NR2 * b * b) % PB
    ni = pow(nrm, PB - 2, PB)
    return a * ni % PB + PB * ((-b * ni) % PB)


D2 = list(range(1, 17))


def p2norm(f):
    f = list(f)
    while f and f[-1] == 0:
        f.pop()
    return f


def p2add(f, g):
    L = max(len(f), len(g))
    return p2norm([f2_add(f[i] if i < len(f) else 0,
                          g[i] if i < len(g) else 0) for i in range(L)])


def p2scale(f, c):
    return p2norm([f2_mul(c, a) for a in f])


def p2mul(f, g):
    if not f or not g:
        return []
    out = [0] * (len(f) + len(g) - 1)
    for i, a in enumerate(f):
        if a:
            for j, b in enumerate(g):
                if b:
                    out[i + j] = f2_add(out[i + j], f2_mul(a, b))
    return p2norm(out)


def p2eval(f, x):
    r = 0
    for a in reversed(f):
        r = f2_add(f2_mul(r, x), a)
    return r


def complements2():
    out = []
    for Rc in itertools.combinations(range(N2), OM2):
        f = [1]
        for i in Rc:
            f = p2mul(f, [f2_neg(D2[i]), 1])
        out.append((tuple(f), Rc))
    return out


def psums2(word, upto):
    T = []
    for t in range(upto):
        s = 0
        for i in range(N2):
            s = f2_add(s, f2_mul(word[i], pow(D2[i] % PB, t, PB)))
        T.append(s)
    return T


def hits2(word, compl):
    T = psums2(word, OM2 + W2 + 1)
    out = []
    for lam, Rc in compl:
        ok = True
        for j in range(W2):
            s = 0
            for k2, l in enumerate(lam):
                if l:
                    s = f2_add(s, f2_mul(l, T[j + 1 + k2]))
            if s:
                ok = False
                break
        if ok:
            out.append(Rc)
    return out


def census2(word, compl):
    """{ckey: (agr, hits)} threshold M2 via own interpolation grouping."""
    strata = {}
    for Rc in hits2(word, compl):
        Rs = set(Rc)
        Sidx = [i for i in range(N2) if i not in Rs]
        pts = [(D2[i], word[i]) for i in Sidx[:K2]]
        out = []
        for a, (xi, yi) in enumerate(pts):
            num, den = [1], 1
            for b, (xj, _) in enumerate(pts):
                if a == b:
                    continue
                num = p2mul(num, [f2_neg(xj), 1])
                den = f2_mul(den, f2_sub(xi, xj))
            out = p2add(out, p2scale(num, f2_mul(yi, f2_inv(den))))
        assert len(out) <= K2
        for i in Sidx[K2:]:
            assert p2eval(out, D2[i]) == word[i]
        agr = sum(1 for i in range(N2) if p2eval(out, D2[i]) == word[i])
        key = tuple(out[t] if t < len(out) else 0 for t in range(K2))
        strata.setdefault(key, {"agr": agr, "count": 0})
        assert strata[key]["agr"] == agr
        strata[key]["count"] += 1
    for st in strata.values():
        assert st["count"] == math.comb(st["agr"], M2), "saturation broken"
    return strata


def fibers2_hist(msize, depth):
    csize = N2 - msize
    tot = [sum(pow(x, t, PB) for x in range(1, 17)) % PB
           for t in range(depth + 1)]
    counts = {}
    members = {}
    for Rc in itertools.combinations(range(N2), csize):
        ps = [0] * (depth + 1)
        for t in range(1, depth + 1):
            s = 0
            for i in Rc:
                s += pow(D2[i] % PB, t, PB)
            ps[t] = (tot[t] - s) % PB
        z = newton_prefix(ps, depth, PB)
        counts[z] = counts.get(z, 0) + 1
        members.setdefault(z, []).append(
            tuple(i for i in range(N2) if i not in set(Rc)))
    assert sum(counts.values()) == math.comb(N2, msize)
    return counts, members


def sweep_line(u, v, compl, stored_rows, n_common_expected):
    """full 289-slope census sweep; stored slopes must match, absent
    slopes must census to zero.  Returns (r1_total, lineray)."""
    stored = {sr[0]: (sr[1], sr[2]) for sr in stored_rows}
    r1_total = 0
    lineray = 0
    for z in range(Q2):
        Uz = [f2_add(u[i], f2_mul(z, v[i])) for i in range(N2)]
        strata = census2(Uz, compl)
        nh = sum(st["count"] for st in strata.values())
        cen = nh - n_common_expected
        if z in stored:
            m_st, prof_st = stored[z]
            assert cen == m_st, "slope %d census %d != stored %d" \
                % (z, cen, m_st)
            profile = sorted((st["agr"] for st in strata.values()),
                             reverse=True)
            assert profile == prof_st, "slope %d profile drift" % z
            r1_total += m_st
            lineray += len(strata)
        else:
            assert cen == 0, "slope %d unreported census" % z
    return r1_total, lineray


def check_gate_c(cert):
    c = cert["gate_c_fp2_toy"]
    fld = c["field"]
    assert (fld["p"], fld["q"], fld["n"], fld["K"], fld["m"]) \
        == (PB, Q2, N2, K2, M2)
    assert fld["domain"] == D2
    ts = c["term_separation"]
    ceil_p = -(-math.comb(N2, M2) // PB ** W2)
    assert ts["ceil_p_term"] == ceil_p == 3
    assert ts["p_term"] == [math.comb(N2, M2), PB ** W2]
    assert ts["q_term"] == [math.comb(N2, M2), Q2 ** (W2 - 1)]
    assert math.comb(N2, M2) < Q2 ** (W2 - 1)  # q-term below 1
    assert ceil_p > 1                           # p-term alive

    # fibers by the independent route
    pl = c["pole_line"]
    cnt3, _ = fibers2_hist(M2, W2)
    best3 = max(cnt3.values())
    zstar = min(z for z, v in cnt3.items() if v == best3)
    assert list(zstar) == pl["z_star"]
    assert best3 == pl["heaviest_depth_wprime_fiber"]
    assert best3 >= ceil_p == pl["ceil_floor"]
    cnt2, mem2 = fibers2_hist(M2, W2 - 1)
    wit = sorted(mem2[zstar[:W2 - 1]])
    assert wit == sorted(tuple(x) for x in pl["witness_fiber_members"])
    assert len(wit) == pl["witness_fiber_size"]
    assert pl["witness_fiber_depth"] == W2 - 1

    # prefix word and per-alpha slope counts (fiber route)
    Pz = [0] * (M2 + 1)
    Pz[M2] = 1
    for h, zz in enumerate(zstar, 1):
        Pz[M2 - h] = zz
    Uw = [p2eval(Pz, x) for x in D2]
    lams = []
    for T in wit:
        f = [1]
        for i in T:
            f = p2mul(f, [f2_neg(D2[i]), 1])
        lams.append(f)
    ns_min, ns_max = 10 ** 9, -1
    first_coll = None
    coll = 0
    for a in range(PB, Q2):
        Pa = p2eval(Pz, a)
        seen = set()
        for lam in lams:
            seen.add(f2_sub(Pa, p2eval(lam, a)))
        ns = len(seen)
        ns_min = min(ns_min, ns)
        ns_max = max(ns_max, ns)
        if ns < len(wit):
            coll += 1
            if first_coll is None:
                first_coll = a
    assert (ns_min, ns_max) == (pl["n_slopes_min"], pl["n_slopes_max"])
    assert coll == pl["collision_alphas"]
    assert pl["admissible_alphas"] == Q2 - PB
    assert first_coll == pl["first_collision_alpha"]
    cw = pl["collision_witness"]
    T1, T2 = tuple(cw["T1"]), tuple(cw["T2"])
    assert T1 != T2 and T1 in set(wit) and T2 in set(wit)
    la = p2eval(Pz, cw["alpha"])
    l1 = [1]
    for i in T1:
        l1 = p2mul(l1, [f2_neg(D2[i]), 1])
    l2 = [1]
    for i in T2:
        l2 = p2mul(l2, [f2_neg(D2[i]), 1])
    z1 = f2_sub(la, p2eval(l1, cw["alpha"]))
    z2 = f2_sub(la, p2eval(l2, cw["alpha"]))
    assert z1 == z2 == cw["slope"], "collision witness"

    compl = complements2()
    assert len(compl) == math.comb(N2, OM2)

    # pole rows: full slope sweep at every tested alpha (no rank-one scan)
    assert pl["tested_alphas"] == sorted(set(
        [PB, first_coll, Q2 - 1]))
    for row in pl["rows"]:
        a = row["alpha"]
        fa = [f2_mul(Uw[i], f2_inv(f2_sub(D2[i], a))) for i in range(N2)]
        ga = [f2_mul(f2_neg(1), f2_inv(f2_sub(D2[i], a)))
              for i in range(N2)]
        # g never censused (no common/beta-zero at pole lines)
        assert not hits2(ga, compl), "g_alpha censused"
        r1_total, lineray = sweep_line(fa, ga, compl, row["slope_rows"], 0)
        assert r1_total == row["r1"] == len(wit)
        assert lineray == row["lineray"] == len(wit)
        assert row["n_slopes"] == len(row["slope_rows"])
        assert all(agr == M2 for sr in row["slope_rows"] for agr in sr[2])
        assert row["all_agr_exactly_m"] is True
        assert row["collision_here"] == (row["n_slopes"] < row["lineray"])
        assert lineray >= best3 >= ceil_p
        print("F_289 pole alpha=%-3d r1=lineray=%d n_slopes=%d OK "
              "(full-sweep route)" % (a, lineray, row["n_slopes"]))

    # planted line
    p = c["planted"]
    e = p["e"]
    assert e == W2 + 2 and 2 * e <= N2 - K2 + 1
    u, v = p["u"], p["v"]
    cc, pos = p["codeword_coeffs"], p["error_positions"]
    Upw = [f2_add(u[i], f2_mul(p["z0"], v[i])) for i in range(N2)]
    mism = [i for i in range(N2)
            if p2eval(p2norm(cc), D2[i]) != Upw[i]]
    assert mism == pos and len(mism) == e
    r1_total, lineray = sweep_line(u, v, compl, p["slope_rows"], 0)
    assert r1_total == p["counts"]["rank_one"]
    assert lineray == p["lineray_count"]
    assert p["counts"]["common"] == 0
    # d1 = e by rank test + explicit locator
    assert min_wdeg_ge(Upw, D2, e, K2, None, f2_mul, f2_sub, f2_inv)
    lamE = [1]
    for i in pos:
        lamE = p2mul(lamE, [f2_neg(D2[i]), 1])
    NN = p2mul(lamE, p2norm(cc))
    for i, x in enumerate(D2):
        assert f2_mul(p2eval(lamE, x), Upw[i]) == p2eval(NN, x)
    wdeg = max(len(lamE) - 1,
               (len(NN) - 1 - (K2 - 1)) if NN else -10 ** 9)
    assert wdeg == e == p["planted"]["d1"]
    # model verdicts, fresh
    p_term = [math.comb(N2, M2), PB ** W2]
    q_term = [math.comb(N2, M2), Q2 ** (W2 - 1)]
    assert p["corrected_holds_raw"] == holds(r1_total, [p_term, q_term])
    assert p["literal_holds_raw"] == holds(r1_total, [q_term])
    assert p["recorded_dedup_holds"] == holds(lineray,
                                              [[ceil_p, 1], q_term])
    assert not p["corrected_holds_raw"] and not p["literal_holds_raw"]
    assert p["recorded_dedup_holds"] and lineray <= ceil_p
    assert p["planted"]["mult_z0"] >= math.comb(N2 - e, M2) \
        == p["planted"]["floor_C_n_minus_e_m"]
    print("F_289 planted e=%d: #R1=%d lineray=%d d1=%d OK "
          "(raw FAILS corrected+literal, dedup HOLDS, p-term alive)"
          % (e, r1_total, lineray, e))

    # control line
    ct = c["control"]
    r1_total, lineray = sweep_line(ct["u"], ct["v"], compl,
                                   ct["slope_rows"], 0)
    assert r1_total == ct["counts"]["rank_one"]
    assert lineray == ct["lineray_count"]
    assert ct["corrected_holds_raw"] and ct["literal_holds_raw"]
    assert ct["recorded_dedup_holds"]
    print("F_289 control: #R1=%d lineray=%d OK" % (r1_total, lineray))


# ------------------------------------------------------------------ main
def run(root: Path) -> int:
    cert = json.loads((root / CERT_REL).read_text(encoding="utf-8"))
    assert cert.get("payload_sha256") == payload_hash(cert), "self-hash"
    assert cert["summary"]["verdict"] == "NO ISSUE"
    assert cert["recorded_target"]["status"] == "OPEN"
    print("toy parameters: F_73 (n=24, K=12, m=15, w'=3) and "
          "F_289 = F_17[t]/(t^2-3) (n=16, K=6, m=9, w'=3, z0=%d)"
          % cert["gate_c_fp2_toy"]["planted"]["z0"])
    check_pins(root, cert)
    check_oracles(root, cert)
    check_gate_b_toy(cert)
    check_gate_b_deployed(cert)
    check_gate_c(cert)
    print("RESULT: PASS")
    print("payload_sha256:", cert["payload_sha256"])
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="accepted for convention parity; the check "
                         "always runs")
    ap.parse_args(argv)
    return run(repo_root())


if __name__ == "__main__":
    sys.exit(main())
