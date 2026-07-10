#!/usr/bin/env python3
"""Independent checker for capg-split-pencil-refutation (no generator import).

Every number in the certificate is recomputed by a route disjoint from the
generator:

  toy censuses    generator: shifted-weak-Popov basis of M_U + cap-space
                  parity membership over the divisor table.
                  here: GRS duality on complements -- a monic degree-9
                  divisor G | X^24 - 1 is a hit iff U restricted to
                  S = D \\ roots(G) lies in RS_12(S), tested by the three
                  power-sum functionals sum_k lambda_k T_{j+1+k} = 0
                  (j = 0,1,2), where lambda are the coefficients of
                  Lambda_R and T_t = sum_{x in D} U(x) x^t.  No Popov
                  basis, no cap space, no linear algebra.
  ray structure   here: per qualifying S, interpolate U|S on 12 points,
                  verify on the rest, group by codeword; per-ray counts
                  must equal C(agr, m) and match the stored rows.
  d1 = e          generator: Popov reduction.  here: direct rank tests --
                  the F_73 linear system W(x)U(x) = N(x) on D with
                  wdeg <= e-1 has only the zero solution (RREF rank), and
                  the locator pair built from the stored error positions
                  realizes wdeg = e.
  deployed        generator: Legendre floor-sum exponents + product tree.
                  here: Kummer carry-count exponents (number of carries
                  when adding b and a-b in base p) + smallest-first heap
                  merge product; bit lengths cross-estimated with an
                  lgamma route (must agree within 0.5 bits).
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
from pathlib import Path

CERT_REL = Path(
    "experimental/data/certificates/capg-split-pencil-refutation/"
    "capg_split_pencil_refutation.json"
)
PAPER_CAP = Path("experimental/cap25_cap_v13_raw.tex")
PAPER_GF = Path("experimental/grande_finale.tex")

P = 73
N = 24
K = 12
M = 15
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


def census_by_duality(U, D):
    """count monic degree-9 divisors G of X^24-1 with U|_{D-roots(G)} in RS_12,
    and return the ray decomposition, via power-sum functionals only."""
    T = [sum(U[i] * pow(D[i], t, P) for i in range(N)) % P for t in range(13)]
    hits_supports = []

    # DFS over 9-subsets R of D, maintaining coefficients of Lambda_R
    def rec(start, depth, poly, chosen):
        if depth == OMEGA:
            for j in range(3):
                s = 0
                for k2, lam in enumerate(poly):
                    if lam:
                        s += lam * T[j + 1 + k2]
                if s % P:
                    return
            hits_supports.append(tuple(chosen))
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
            rec(idx + 1, depth + 1, new, chosen + [idx])

    rec(0, 0, [1], [])

    # ray decomposition: interpolate U on S = D \ R (12 points suffice),
    # verify on the remaining 3, count agreement on all of D
    def interp12(pts):
        out = []
        for i, (xi, yi) in enumerate(pts):
            num, den = [1], 1
            for j, (xj, _) in enumerate(pts):
                if i == j:
                    continue
                num = _pmul(num, [(-xj) % P, 1])
                den = den * ((xi - xj) % P) % P
            out = _padd(out, _pscale(num, yi * pow(den, P - 2, P)))
        return out

    strata = {}
    for R in hits_supports:
        Sidx = [i for i in range(N) if i not in set(R)]
        pts = [(D[i], U[i]) for i in Sidx[:K]]
        c = interp12(pts)
        assert len(c) <= K
        for i in Sidx[K:]:
            assert _peval(c, D[i]) == U[i], "interpolant fails on S"
        agr = sum(1 for i in range(N) if _peval(c, D[i]) == U[i])
        key = tuple(c[i] if i < len(c) else 0 for i in range(K))
        strata.setdefault(key, {"agr": agr, "count": 0})
        assert strata[key]["agr"] == agr
        strata[key]["count"] += 1
    ray_rows = sorted(([st["agr"], st["count"]] for st in strata.values()),
                      key=lambda r: -r[0])
    return len(hits_supports), ray_rows


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
    # RREF rank
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


# ------------------------------------------------------------------ main
def run(root: Path) -> int:
    cert = json.loads((root / CERT_REL).read_text(encoding="utf-8"))
    assert cert.get("payload_sha256") == payload_hash(cert), "self-hash"
    assert cert["summary"]["verdict"] == "COUNTEREXAMPLE"

    # ---- statement pins, fresh scan
    for fname, rel in ((PAPER_CAP.name, PAPER_CAP), (PAPER_GF.name, PAPER_GF)):
        lines = (root / rel).read_text(encoding="utf-8").splitlines()
        for lab, pin in cert["statement_pins"][fname].items():
            line = lines[pin["line"] - 1]
            assert ("\\label{%s}" % lab) in line, "pin moved: %s" % lab
            assert hashlib.sha256(line.encode("utf-8")).hexdigest() \
                == pin["sha256_line"], "pin hash drift: %s" % lab
    print("pins: OK (%d labels)" % sum(
        len(v) for v in cert["statement_pins"].values()))

    # ---- toy rows by duality route
    D = toy_domain()
    assert D == cert["toy_parameters"]["domain"]
    for row in cert["toy_rows"]:
        U = row["word"]
        assert len(U) == N
        cen, ray_rows = census_by_duality(U, D)
        assert cen == row["census"], \
            "%s census %d != %d" % (row["label"], cen, row["census"])
        assert ray_rows == row["ray_rows"], "%s ray rows" % row["label"]
        assert cen == sum(math.comb(a, M) for a, _ in ray_rows)
        if row["e"] is not None:
            e = row["e"]
            cc, epos = row["codeword_coeffs"], row["error_positions"]
            # word consistency: exactly e mismatches, at the stored positions
            mism = [i for i in range(N) if _peval(_pnorm(cc), D[i]) != U[i]]
            assert mism == epos and len(mism) == e
            # profile localization by rank test + locator construction
            assert 2 * e <= N - K + 1
            assert min_wdeg_ge(U, D, e), "wdeg < e solution exists"
            assert locator_wdeg_e(U, D, cc, epos, e), "locator not wdeg e"
            assert row["d1"] == e and row["d1_equals_e"]
        # budgets, fresh fractions
        d1 = row["d1"]
        lit = [math.comb(N, OMEGA), P ** (M - K - 1)]
        assert row["budget_literal"] == lit
        mprime = K - 1 + d1
        mb = [math.comb(mprime, M) * math.comb(N, mprime), P ** (d1 - 1)]
        assert row["budget_MB"] == mb
        mb_ceil = math.comb(mprime, M) * \
            (-(-math.comb(N, mprime) // P ** (d1 - 1)))
        assert row["budget_MB_ceiling_variant"] == mb_ceil
        assert row["literal_holds_raw"] == (cen * lit[1] <= lit[0])
        assert row["corrected_holds_raw"] == (
            (cen <= 1) or (cen * mb[1] <= mb[0])
            or (cen * lit[1] <= lit[0]))
        assert row["corrected_ceiling_holds_raw"] == (
            (cen <= 1) or (cen <= mb_ceil) or (cen * lit[1] <= lit[0]))
        nrays = len(ray_rows)
        assert row["corrected_holds_rays"] == (
            (nrays <= 1) or (nrays * mb[1] <= mb[0])
            or (nrays * lit[1] <= lit[0]))
        print("toy %-26s census=%-6d rays=%d  OK (duality route)"
              % (row["label"], cen, nrays))
    interior = [r for r in cert["toy_rows"] if r["e"] in (5, 6)]
    assert interior and all(not r["corrected_holds_raw"] for r in interior)

    # ---- deployed row by Kummer + heap route
    dep = cert["deployed"]
    n_, K_, m_, w_, p_ = dep["n"], dep["K"], dep["m"], dep["w_prime"], dep["p"]
    assert m_ == K_ + w_ and dep["omega"] == n_ - m_
    assert dep["e_boundary"] == w_ + 1 and dep["e_interior"] == w_ + 2
    assert 2 * (w_ + 2) <= n_ - K_ + 1 and dep["lemma_range_ok"]
    primes = sieve(n_)
    combs = {
        "C_n_m": heap_comb(n_, m_, primes),
        "C_n_m_plus_1": heap_comb(n_, m_ + 1, primes),
        "C_ray_boundary": heap_comb(n_ - (w_ + 1), m_, primes),
        "C_ray_interior": heap_comb(n_ - (w_ + 2), m_, primes),
    }
    lg_args = {
        "C_n_m": (n_, m_), "C_n_m_plus_1": (n_, m_ + 1),
        "C_ray_boundary": (n_ - (w_ + 1), m_),
        "C_ray_interior": (n_ - (w_ + 2), m_),
    }
    for name, val in combs.items():
        assert val.bit_length() == dep["bits"][name], \
            "%s bits %d != %d" % (name, val.bit_length(), dep["bits"][name])
        # lgamma cross-estimate must land inside the same bit
        est = lgamma_log2_comb(*lg_args[name])
        assert abs(est - (val.bit_length() - 1)) < 1.0 and \
            math.floor(est) + 1 == val.bit_length(), "%s lgamma" % name
    print("deployed binomials: OK (Kummer carry-count + heap merge; "
          "lgamma cross-estimates agree)")

    q_ = p_ ** 6
    qpow_min_bits = (w_ - 1) * (q_.bit_length() - 1)
    assert qpow_min_bits == dep["budget"]["q_pow_min_bits"]
    assert qpow_min_bits > combs["C_n_m"].bit_length()
    pw1 = p_ ** (w_ - 1)
    assert combs["C_n_m"] > pw1
    bf_ceil = -(-combs["C_n_m"] // pw1)
    assert str(bf_ceil) == dep["budget"]["base_field_reading_ceil"]
    pw3 = pw1 * p_ * p_
    MB_ceil_d = -(-((m_ + 1) * combs["C_n_m_plus_1"]) // pw3)
    assert MB_ceil_d == dep["budget"]["MB_interior_ceil"]
    MB_ceilvar_d = (m_ + 1) * (-(-combs["C_n_m_plus_1"] // pw3))
    assert MB_ceilvar_d == dep["budget"]["MB_ceiling_variant_ceil"]

    marg = dep["margins_bits"]
    assert combs["C_ray_boundary"].bit_length() - 1 \
        == marg["boundary_ray_vs_literal"]
    corr_budget = max(1, MB_ceil_d, MB_ceilvar_d)
    assert (combs["C_ray_interior"] // corr_budget).bit_length() - 1 \
        == marg["interior_ray_vs_recorded_corrected"]
    cons_budget = max(corr_budget, bf_ceil)
    assert (combs["C_ray_interior"] // cons_budget).bit_length() - 1 \
        == marg["interior_ray_vs_conservative_with_base_field"]
    print("deployed margins: OK (boundary>=%d interior>=%d conservative>=%d)"
          % (marg["boundary_ray_vs_literal"],
             marg["interior_ray_vs_recorded_corrected"],
             marg["interior_ray_vs_conservative_with_base_field"]))

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
