#!/usr/bin/env python3
r"""
Verifier for the fiber-side scoped Conjecture F proof (roadmap QF.10, branch a).
Companion note: notes/m1/conjecture_f_fiber_scoped.md.  PURE STDLIB, offline,
deterministic; exit 0 iff every check passes.

It checks the coordinate/prefix-plane fiber theorem
    #E_p <= binom(n, d) / binom(j, d),     d = j - sigma,
where E_p is the set of degree-j monic squarefree divisors of P_H (= j-subsets
of H) whose first sigma elementary symmetric functions equal a fixed prefix p.
The proofs are elementary and unconditional; this script exhibits their content
by exhaustive enumeration over F_97, with H = mu_n and with H = {0,...,n-1}
(to show no group structure is used).

Checks:
  A  fiber bound      max_p #E_p <= binom(n,d)/binom(j,d)               (Thm A)
  B  spacing (MDS)    any two locators in one fiber share <= d-1 roots  (sec 4)
  C  Vandermonde      d-point Vandermonde det != 0; deg<d poly has <=d-1
                      roots in H  (dual distance > d, Singleton)        (sec 3)
  D  r-wise moment    each r-subset lies in <= binom(n-r,d-r) members   (Thm A')
  E  corollary B      binom(n,d)/binom(j,d) <= (2n/j)^d when d <= j/2   (Cor B)
  F  scope boundary   at sigma ~ n/log2 n the ratio exceeds any poly    (sec 5)
"""
from __future__ import annotations
import argparse, json, random
from fractions import Fraction
from itertools import combinations
from math import comb, log2
from pathlib import Path

P = 97  # F_97; 96 = 2^5*3, so mu_n <= F_97^* exists for n | 96
OUTPUT = Path("experimental/data/certificates/conjecture-f-fiber-scoped/"
              "conjecture_f_fiber_scoped_toy.json")


# ---------- finite-field helpers (F_P) ----------

def prime_factors(m: int) -> set:
    f, d = set(), 2
    while d * d <= m:
        while m % d == 0:
            f.add(d); m //= d
        d += 1
    if m > 1:
        f.add(m)
    return f


def primitive_root(p: int) -> int:
    fac = prime_factors(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fac):
            return g
    raise RuntimeError("no primitive root")


def mu_n(n: int) -> list:
    """H = mu_n <= F_P^*, requires n | (P-1)."""
    assert (P - 1) % n == 0, f"mu_{n} needs {n} | {P-1}"
    w = pow(primitive_root(P), (P - 1) // n, P)
    H = [pow(w, i, P) for i in range(n)]
    assert len(set(H)) == n
    return H


def lin_n(n: int) -> list:
    """H = {0,1,...,n-1} as residues (distinct, no group structure)."""
    assert n <= P
    return list(range(n))


def esym_prefix(values, sigma: int) -> tuple:
    """(e_1,...,e_sigma) mod P via truncated product prod (1 + a*y)."""
    c = [0] * (sigma + 1)
    c[0] = 1
    for a in values:
        for k in range(sigma, 0, -1):
            c[k] = (c[k] + a * c[k - 1]) % P
    return tuple(c[1:sigma + 1])


def det_mod(mat) -> int:
    """Determinant of a square matrix over F_P by Gaussian elimination."""
    m = [row[:] for row in mat]
    dim = len(m)
    det = 1
    for col in range(dim):
        piv = next((r for r in range(col, dim) if m[r][col] % P), None)
        if piv is None:
            return 0
        if piv != col:
            m[col], m[piv] = m[piv], m[col]
            det = (-det) % P
        inv = pow(m[col][col], P - 2, P)
        det = det * m[col][col] % P
        for r in range(col + 1, dim):
            f = m[r][col] * inv % P
            if f:
                m[r] = [(m[r][k] - f * m[col][k]) % P for k in range(dim)]
    return det % P


def poly_roots_in(coeffs, H) -> int:
    """Number of roots in H of the polynomial sum coeffs[i] X^i (low->high)."""
    cnt = 0
    for h in H:
        v = 0
        for c in reversed(coeffs):
            v = (v * h + c) % P
        cnt += (v == 0)
    return cnt


# ---------- fiber enumeration ----------

def fibers(H, j: int, sigma: int) -> dict:
    """Map prefix-key -> list of j-subsets (as index bitmasks) of H."""
    n = len(H)
    groups: dict = {}
    for idx in combinations(range(n), j):
        key = esym_prefix([H[i] for i in idx], sigma)
        mask = 0
        for i in idx:
            mask |= (1 << i)
        groups.setdefault(key, []).append(mask)
    return groups


# ---------- checks ----------

CASES = [
    # (n, j, sigma)          d = j - sigma
    (8, 4, 1), (8, 4, 2),
    (12, 6, 2), (12, 6, 4),
    (16, 8, 2), (16, 8, 5), (16, 8, 6),
]


def check_fiber_bound() -> dict:
    ok, rows = True, []
    for (n, j, sigma) in CASES:
        d = j - sigma
        bound = Fraction(comb(n, d), comb(j, d))
        for name, H in (("mu", mu_n(n)), ("lin", lin_n(n))):
            grp = fibers(H, j, sigma)
            mx = max(len(v) for v in grp.values())
            good = mx <= bound
            ok &= good
            rows.append({"H": name, "n": n, "j": j, "sigma": sigma, "d": d,
                         "max_fiber": mx, "bound": str(bound), "ok": good})
    return {"name": "A fiber bound  #E_p <= C(n,d)/C(j,d)",
            "status": "PASS" if ok else "FAIL", "rows": rows}


def check_spacing() -> dict:
    """Any two distinct locators in one fiber share <= d-1 roots."""
    ok, rows = True, []
    for (n, j, sigma) in CASES:
        d = j - sigma
        for name, H in (("mu", mu_n(n)), ("lin", lin_n(n))):
            worst = 0
            for members in fibers(H, j, sigma).values():
                for a, b in combinations(members, 2):
                    worst = max(worst, bin(a & b).count("1"))
            good = worst <= d - 1
            ok &= good
            rows.append({"H": name, "n": n, "j": j, "d": d,
                         "max_shared_roots": worst, "limit": d - 1, "ok": good})
    return {"name": "B spacing (MDS): shared roots <= d-1",
            "status": "PASS" if ok else "FAIL", "rows": rows}


def check_vandermonde() -> dict:
    """d distinct points impose independent conditions on K[X]_<d (dual dist>d)."""
    rng = random.Random(20260704)
    ok, rows = True, []
    for (n, _, _) in [(8, 0, 0), (12, 0, 0), (16, 0, 0)]:
        H = mu_n(n)
        for d in (2, 3, 5, 6):
            if d > n:
                continue
            det_ok = True
            for _ in range(40):
                T = rng.sample(H, d)
                mat = [[pow(t, i, P) for i in range(d)] for t in T]
                det_ok &= (det_mod(mat) != 0)
            # nonzero deg<d poly has <= d-1 roots in H
            root_ok = True
            for _ in range(40):
                coeffs = [rng.randrange(P) for _ in range(d)]  # deg <= d-1
                if any(coeffs):
                    root_ok &= (poly_roots_in(coeffs, H) <= d - 1)
            good = det_ok and root_ok
            ok &= good
            rows.append({"n": n, "d": d, "vandermonde_nonsingular": det_ok,
                         "deg<d_roots<=d-1": root_ok, "ok": good})
    return {"name": "C Vandermonde/Singleton: dual distance > d",
            "status": "PASS" if ok else "FAIL", "rows": rows}


def check_moment() -> dict:
    """Each r-subset lies in <= binom(n-r, d-r) fiber members (Thm A', per-T)."""
    ok, rows = True, []
    for (n, j, sigma) in [(16, 8, 2), (12, 6, 2), (8, 4, 1)]:
        d = j - sigma
        H = mu_n(n)
        # take the largest fiber (most stringent) and audit r = d, d-1, d-2
        big = max(fibers(H, j, sigma).values(), key=len)
        for r in (d, d - 1, d - 2):
            if r < 1:
                continue
            lim = comb(n - r, d - r)
            cover: dict = {}
            for mask in big:
                idxs = [i for i in range(n) if mask >> i & 1]
                for T in combinations(idxs, r):
                    cover[T] = cover.get(T, 0) + 1
            worst = max(cover.values()) if cover else 0
            good = worst <= lim
            ok &= good
            rows.append({"n": n, "j": j, "d": d, "r": r, "fiber": len(big),
                         "max_per_Tsubset": worst, "bound_C(n-r,d-r)": lim,
                         "ok": good})
    return {"name": "D r-wise moment: per r-subset <= C(n-r,d-r)",
            "status": "PASS" if ok else "FAIL", "rows": rows}


def check_corollary_B() -> dict:
    """C(n,d)/C(j,d) <= (2n/j)^d whenever d <= j/2 (constant-rate log reserve)."""
    ok, rows = True, []
    for (n, j, sigma) in CASES:
        d = j - sigma
        if 2 * d > j:  # hypothesis d <= j/2
            continue
        ratio = Fraction(comb(n, d), comb(j, d))
        rhs = Fraction(2 * n, j) ** d  # (2/theta)^d, theta = j/n
        good = ratio <= rhs
        ok &= good
        rows.append({"n": n, "j": j, "d": d, "ratio": str(ratio),
                     "(2n/j)^d": str(rhs), "ok": good})
    return {"name": "E corollary B: ratio <= (2/theta)^d (d<=j/2)",
            "status": "PASS" if ok else "FAIL", "rows": rows}


def check_scope() -> dict:
    """At the prob:perfiber regime sigma ~ n/log2 n the ratio grows like
    2^{Theta(n)}: its bit-length is linear in n, so it beats every fixed
    polynomial n^k (whose bit-length is only O(log n)).  Documents that QF.10
    correctly does NOT claim the hard end (field fibers are exponential there;
    only the char-0 escape saves prob:perfiber, which is open)."""
    ok, rows = True, []
    for n in (100, 200, 400, 800):
        j = n // 2                       # s = rho*n, rho = 1/2
        sigma = round(n / log2(n))       # the critical reserve
        d = j - sigma
        ratio = Fraction(comb(n, d), comb(j, d))
        bits = ratio.numerator.bit_length() - ratio.denominator.bit_length()
        superpoly = bits >= 0.3 * n      # linear bit-growth => super-polynomial
        ok &= superpoly
        rows.append({"n": n, "j": j, "sigma": sigma, "d": d, "ratio_bits": bits,
                     "bits/n": round(bits / n, 3), "exceeds_n^10": ratio > n ** 10,
                     "linear_bitgrowth": superpoly})
    return {"name": "F scope: hard regime ratio ~ 2^Theta(n) (super-poly)",
            "status": "PASS" if ok else "FAIL", "rows": rows}


def build_report() -> dict:
    checks = [check_fiber_bound(), check_spacing(), check_vandermonde(),
              check_moment(), check_corollary_B(), check_scope()]
    return {"field": P, "cases": CASES, "checks": checks,
            "all_pass": all(c["status"] == "PASS" for c in checks)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit", action="store_true")
    args = ap.parse_args()
    report = build_report()
    print("=" * 72)
    print("Conjecture F fiber-side scoped verifier (QF.10, branch a)")
    print("=" * 72)
    ok = True
    for chk in report["checks"]:
        ok &= chk["status"] == "PASS"
        print(f"[{chk['status']}] {chk['name']}")
        for row in chk["rows"]:
            print(f"        {row}")
    if args.emit:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print(f"\nwrote {OUTPUT}")
    print("\nALL PASS" if ok else "\nFAILURES PRESENT")
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
