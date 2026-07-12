#!/usr/bin/env python3
"""Independent checker for r1-rawcount-refutation (no generator import).

Every number in the certificate is recomputed by a route disjoint from the
generator:

  slope mults     generator: one rank-one scan per line (alpha/beta
                  proportionality classification over all supports).
                  here: NO rank-one scan -- for every slope z in 0..p-1 the
                  word U_z = u + z v is censused by GRS duality (power-sum
                  functionals sum_k lambda_k T_{j+1+k} = 0, j = 0,1,2, over
                  all C(24,9) complements), the hits are grouped by
                  interpolated codeword, per-ray counts must equal
                  C(agr, m) (saturation), and the stored multiplicity must
                  equal the list census sum_c C(agr,m) minus the common
                  count.  Slopes absent from the stored table must census
                  to zero.  common / beta-zero are recomputed as
                  |hits(u) cap hits(v)| and |hits(v)| - common (alpha = 0
                  iff u interpolable on T, beta = 0 iff v interpolable).
  d1 = e          generator: shifted-weak-Popov reduction.  here: direct
                  rank tests -- the linear system W(x)U(x) = N(x) on D with
                  wdeg <= e-1 has only the zero solution (RREF rank), and
                  the locator pair built from the stored codeword and error
                  positions realizes wdeg = e.
  deployed        generator: Legendre floor-sum exponents + product tree.
                  here: Kummer carry-count exponents (number of carries
                  when adding b and a-b in base p) + smallest-first heap
                  merge product; bit lengths cross-estimated with an
                  lgamma route (must agree within the same bit).
  budgets, pins   exact fractions via math.comb; statement pins re-scanned
                  with fresh line hashes.

Exit 0 with RESULT: PASS, nonzero otherwise.
"""
from __future__ import annotations

import argparse
import hashlib
import heapq
import json
import math
import sys
from operator import mul
from pathlib import Path

CERT_REL = Path(
    "experimental/data/certificates/r1-rawcount-refutation/"
    "r1_rawcount_refutation.json"
)
PAPER_CAP = Path("experimental/cap25_cap_v13_raw.tex")
CAP_LABELS = (
    "lem:capfp-functionals",
    "thm:capfp-slope-elim",
    "prob:capfp-R1",
    "prob:capfr1-rank-one-census",
    "prob:capg-split-pencil-B",
    "prop:capg-census-floor",
    "rem:capg-subfield-scope",
    "thm:capfp-dichotomy",
)

P = 73
N = 24
K = 12
M = 15
W = M - K
OMEGA = 9


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def payload_hash(obj) -> str:
    clone = dict(obj)
    clone.pop("payload_sha256", None)
    blob = json.dumps(clone, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


# ------------------------------------------------------------- toy route
def toy_domain():
    """order-24 subgroup of F_73^*, sorted (matches cert toy_parameters)."""
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


def enumerate_complements(D):
    """coefficient tuples of Lambda_R for all 9-subsets R, DFS (lex) order."""
    out = []

    def rec(start, depth, poly):
        if depth == OMEGA:
            out.append(tuple(poly))
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
    assert len(out) == math.comb(N, OMEGA)
    return out


def hit_ids(word, D, lamr):
    """indices of complements whose support censuses the word (duality)."""
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
    """group hit supports by interpolated codeword; assert saturation
    per ray; return (profile sorted desc, number of rays)."""
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
            assert _peval(out, D[t]) == word[t], "interpolant fails on S"
        agr = sum(1 for t in range(N) if _peval(out, D[t]) == word[t])
        key = tuple(out[t] if t < len(out) else 0 for t in range(K))
        strata.setdefault(key, {"agr": agr, "count": 0})
        assert strata[key]["agr"] == agr
        strata[key]["count"] += 1
    for st in strata.values():
        assert st["count"] == math.comb(st["agr"], M), "saturation broken"
    profile = sorted((st["agr"] for st in strata.values()), reverse=True)
    return profile, len(strata)


def min_wdeg_ge(U, D, e):
    """rank test: the only (W, N) with wdeg <= e-1 in M_U is zero.
    Unknowns: W coeffs (deg <= e-1) and N coeffs (deg <= e-1+K-1)."""
    d = e - 1
    nW, nN = d + 1, d + K
    rows = []
    for i, x in enumerate(D):
        row = [U[i] * pow(x, j, P) % P for j in range(nW)]
        row += [(-pow(x, j, P)) % P for j in range(nN)]
        rows.append(row)
    ncols = nW + nN
    r = 0
    for c in range(ncols):
        piv = next((i for i in range(r, len(rows)) if rows[i][c]), None)
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        ic = pow(rows[r][c], P - 2, P)
        rows[r] = [v * ic % P for v in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c]:
                f = rows[i][c]
                rows[i] = [(a - f * b) % P for a, b in zip(rows[i], rows[r])]
        r += 1
    return r == ncols  # full column rank <=> only the zero pair


def locator_wdeg_e(U, D, ccoeffs, epos, e):
    """the pair (Lambda_E, Lambda_E * c) lies in M_U with wdeg exactly e."""
    lam = [1]
    for i in epos:
        lam = _pmul(lam, [(-D[i]) % P, 1])
    c = _pnorm(ccoeffs)
    Npoly = _pmul(lam, c)
    for i, x in enumerate(D):
        assert _peval(lam, x) * U[i] % P == _peval(Npoly, x) % P
    wdeg = max(len(lam) - 1,
               (len(Npoly) - 1 - (K - 1)) if Npoly else -10 ** 9)
    return wdeg == e


# --------------------------------------------------------- deployed route
def kummer_e(a, b, p):
    """exponent of p in C(a,b) = number of carries adding b + (a-b) base p."""
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
    """C(a,b) exactly via Kummer exponents + smallest-first heap merging."""
    heap = [pr ** kummer_e(a, b, pr) for pr in primes
            if pr <= a and kummer_e(a, b, pr)]
    heapq.heapify(heap)
    while len(heap) > 1:
        x = heapq.heappop(heap)
        y = heapq.heappop(heap)
        heapq.heappush(heap, x * y)
    return heap[0] if heap else 1


def lgamma_log2_comb(a, b):
    lg = (math.lgamma(a + 1) - math.lgamma(b + 1) - math.lgamma(a - b + 1))
    return lg / math.log(2)


def lg2_display(x):
    """display-grade log2 string (top-80-bit mantissa; no verdict uses it)."""
    e = x.bit_length() - 1
    if e <= 80:
        return "%.4f" % math.log2(x)
    return "%.4f" % (math.log2(x >> (e - 80)) + (e - 80))


def holds(count, terms):
    return count <= 1 or any(count * den <= num for num, den in terms)


# ------------------------------------------------------------------ main
def run(root: Path) -> int:
    cert = json.loads((root / CERT_REL).read_text(encoding="utf-8"))
    assert cert.get("payload_sha256") == payload_hash(cert), "self-hash"
    assert cert["summary"]["verdict"] == "COUNTEREXAMPLE"

    # ---- statement pins, fresh scan
    lines = (root / PAPER_CAP).read_text(encoding="utf-8").splitlines()
    pins = cert["statement_pins"][PAPER_CAP.name]
    assert sorted(pins) == sorted(CAP_LABELS), "pinned label set drift"
    for lab, pin in pins.items():
        line = lines[pin["line"] - 1]
        assert ("\\label{%s}" % lab) in line, "pin moved: %s" % lab
        assert hashlib.sha256(line.encode("utf-8")).hexdigest() \
            == pin["sha256_line"], "pin hash drift: %s" % lab
    print("pins: OK (%d labels)" % len(pins))

    # ---- toy rows: list-census route only (no rank-one scan)
    D = toy_domain()
    assert D == cert["toy_parameters"]["domain"]
    assert cert["toy_parameters"]["z0"] == 7
    lamr = enumerate_complements(D)
    ndiv = len(lamr)
    q_term = [math.comb(N, M), P ** (W - 1)]
    p_term = [math.comb(N, M), P ** W]
    for row in cert["toy_rows"]:
        u, v = row["u"], row["v"]
        assert len(u) == N and len(v) == N
        stored = {sr[0]: (sr[1], sr[2]) for sr in row["slope_rows"]}
        assert len(stored) == len(row["slope_rows"]) == row["slopes_hit"]

        # common / beta-zero via word censuses of u (slope 0) and v
        hits_u = hit_ids(u, D, lamr)
        hits_v = hit_ids(v, D, lamr)
        n_common = len(set(hits_u) & set(hits_v))
        n_bzero = len(hits_v) - n_common
        assert n_common == row["counts"]["common"] == 0
        assert n_bzero == row["counts"]["beta_zero"]

        # every finite slope: census + ray decomposition; stored slopes
        # must match, absent slopes must census to zero
        r1_total = 0
        lineray = 0
        for z in range(P):
            if z == 0:
                ids = hits_u
            else:
                Uz = [(u[i] + z * v[i]) % P for i in range(N)]
                ids = hit_ids(Uz, D, lamr)
            cen = len(ids)  # = mult(z) + n_common; n_common = 0
            if z in stored:
                m_st, prof_st = stored[z]
                assert cen - n_common == m_st, \
                    "slope %d: census %d != stored %d" % (z, cen, m_st)
                word = u if z == 0 else Uz
                profile, nrays = ray_profile(word, D, lamr, ids)
                assert profile == prof_st, "slope %d profile" % z
                assert sum(math.comb(a, M) for a in profile) == m_st
                r1_total += m_st
                lineray += nrays
            else:
                assert cen - n_common == 0, "slope %d unreported census" % z
        assert r1_total == row["counts"]["rank_one"]
        assert lineray == row["lineray_count"]
        assert row["counts"]["rank_two"] == ndiv - n_common - n_bzero \
            - r1_total
        assert row["counts"]["rank_two"] >= 0

        # budgets and verdicts, fresh fractions
        assert row["budget_literal_q_term"] == q_term
        assert row["budget_corrected_p_term"] == p_term
        assert row["literal_holds_raw"] == holds(r1_total, [q_term])
        assert row["corrected_holds_raw"] == holds(r1_total,
                                                   [p_term, q_term])
        assert row["literal_holds_lineray"] == holds(lineray, [q_term])
        assert row["corrected_holds_lineray"] == holds(lineray,
                                                       [p_term, q_term])

        # planted rows: word consistency, floor, d1 = e by rank tests
        if row["e"] is not None:
            e = row["e"]
            z0 = row["z0"]
            assert z0 == 7
            Uw = [(u[i] + z0 * v[i]) % P for i in range(N)]
            cc, epos = row["codeword_coeffs"], row["error_positions"]
            mism = [i for i in range(N)
                    if _peval(_pnorm(cc), D[i]) != Uw[i]]
            assert mism == epos and len(mism) == e
            assert 2 * e <= N - K + 1
            assert min_wdeg_ge(Uw, D, e), "wdeg < e solution exists"
            assert locator_wdeg_e(Uw, D, cc, epos, e), "locator not wdeg e"
            pl = row["planted"]
            assert pl["d1"] == e and pl["d1_equals_e"]
            assert pl["mult_z0"] == stored[z0][0]
            assert pl["floor_C_n_minus_e_m"] == math.comb(N - e, M)
            assert pl["mult_z0"] >= pl["floor_C_n_minus_e_m"]
            assert pl["floor_holds"]
            assert not row["corrected_holds_raw"]
            assert not row["literal_holds_raw"]
        else:
            assert row["planted"] is None
            assert row["corrected_holds_raw"]
            assert row["literal_holds_raw"]
        assert row["corrected_holds_lineray"]
        assert row["literal_holds_lineray"]
        print("toy %-12s #R1=%-6d lineray=%-4d slopes=%-3d OK "
              "(list-census route)"
              % (row["label"], r1_total, lineray, row["slopes_hit"]))

    # ---- deployed row by Kummer + heap route
    dep = cert["deployed"]
    n_, K_, m_ = dep["n"], dep["K"], dep["m"]
    w_, p_, e_ = dep["w_prime"], dep["p"], dep["e"]
    print("deployed row: n=%d K=%d m=%d w'=%d omega=%d p=%d q=p^6 "
          "e=w'+2=%d" % (n_, K_, m_, w_, dep["omega"], p_, e_))
    assert n_ == 2 ** 21 and K_ == 2 ** 20
    assert p_ == 2 ** 31 - 2 ** 24 + 1
    assert m_ == K_ + w_ and dep["omega"] == n_ - m_
    assert e_ == w_ + 2 and dep["e_is"] == "w_prime + 2"
    lem = dep["lemma_2e_le_n_minus_K_plus_1"]
    assert lem["two_e"] == 2 * e_ and lem["n_minus_K_plus_1"] == n_ - K_ + 1
    assert 2 * e_ <= n_ - K_ + 1 and lem["ok"]

    primes = sieve(n_)
    Cnm = heap_comb(n_, m_, primes)
    Cray = heap_comb(n_ - e_, m_, primes)
    Cnm_paper = heap_comb(n_, m_ - 1, primes)
    for name, val, args in (("C_n_m", Cnm, (n_, m_)),
                            ("C_ray_interior", Cray, (n_ - e_, m_))):
        assert val.bit_length() == dep["bits"][name], \
            "%s bits %d != %d" % (name, val.bit_length(), dep["bits"][name])
        est = lgamma_log2_comb(*args)
        assert abs(est - (val.bit_length() - 1)) < 1.0 and \
            math.floor(est) + 1 == val.bit_length(), "%s lgamma" % name
        assert lg2_display(val) == dep["log2_display"][name]
    assert Cray.bit_length() == 2015083
    print("deployed binomials: OK (Kummer carry-count + heap merge; "
          "lgamma cross-estimates agree)")

    q_ = p_ ** 6
    q_bit_floor = q_.bit_length() - 1
    assert q_bit_floor == dep["q_bit_floor"]
    qpow_min_bits = (w_ - 1) * q_bit_floor
    assert qpow_min_bits == dep["budget"]["q_pow_min_bits"]
    assert qpow_min_bits > Cnm.bit_length()
    assert dep["budget"]["q_term_below_1"]
    assert dep["budget"]["literal_q_scale_budget"] == 1
    hyg = dep["hygiene_freedom_count"]
    assert hyg["union_bound_below_1_via_bits"] is True
    assert Cnm.bit_length() + 1 <= qpow_min_bits

    pw = p_ ** w_
    assert Cnm > pw
    mid_ceil = -(-Cnm // pw)
    assert mid_ceil == dep["budget"]["corrected_middle_ceil"]
    assert mid_ceil == dep["budget"]["corrected_budget"]
    assert lg2_display(mid_ceil) == dep["log2_display"]["corrected_middle_ceil"]

    marg = dep["margins_bits"]
    over = Cray // mid_ceil
    assert over.bit_length() - 1 == marg["planted_R1_vs_corrected"] == 2015046
    assert lg2_display(over) == dep["log2_display"]["overrun_factor"]
    assert Cray.bit_length() - 1 \
        == marg["planted_R1_vs_literal_q_scale"] == 2015082

    xc = dep["paper_printed_floor_cross_check"]
    assert xc["at_paper_row_m"] == m_ - 1
    w2 = (m_ - 1) - K_
    bf_paper = -(-Cnm_paper // p_ ** w2)
    mb_paper = m_ * (-(-Cnm // p_ ** (w2 + 1)))
    assert lg2_display(bf_paper) == xc["boundary_floor_log2_display"]
    assert lg2_display(mb_paper) == xc["interior_MB_log2_display"]
    assert xc["paper_prints_boundary"] == "67.1"
    assert xc["paper_prints_interior"] == "56.0"
    assert round(float(xc["boundary_floor_log2_display"]), 1) == 67.1
    assert round(float(xc["interior_MB_log2_display"]), 1) == 56.0
    print("deployed margins: OK (corrected>=2^%d literal>=2^%d; "
          "model ceil=%d)"
          % (marg["planted_R1_vs_corrected"],
             marg["planted_R1_vs_literal_q_scale"], mid_ceil))

    print("RESULT: PASS")
    print("payload_sha256:", cert["payload_sha256"])
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true",
                   help="accepted for convention parity; the check always runs")
    p.parse_args(argv)
    return run(repo_root())


if __name__ == "__main__":
    sys.exit(main())
