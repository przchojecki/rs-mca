#!/usr/bin/env python3
r"""
Exact enumerator for Paper B `prob:perfiber` (slackMCA_v3.tex:1227), the open core
of `conj:B` (the slack-MCA positive threshold). PURE STDLIB.

WHAT `prob:perfiber` IS (verbatim object).
  H = <omega> <= F_p^x of order n, identified with mu_n in Z[zeta_n] via zeta -> omega.
  Prefix map  Phi_sigma(A) = (e_1(A), ..., e_sigma(A))  on s-subsets A of H
  (e_i = i-th elementary symmetric function). For sigma >= C n / log_2 n, p == 1 mod n,
  n^{c0} <= p <= 2^{o(n)}: every fiber of Phi_sigma (mod the degree-one prime p above p)
  is conjectured to contain at most n^{O(1)} ordered pairs (S,T) that are
      prefix-equal mod p   (Phi_sigma(S) == Phi_sigma(T) in F_p)
   BUT not equal in Z[zeta] (Phi_sigma(S) != Phi_sigma(T) over char 0).
  This single divisibility statement implies the monomial-line positive half of conj:B.

WHAT IS ALREADY PROVED IN PAPER B (so this script CROSS-CHECKS, not re-proves):
  * cor:upstairs-poly (n=2^m): char-0 prefix fibers are exactly quotient-periodic
    (mu_{M0}-coset toggles, M0 = least power of two > sigma) and have size <= 2^{n/M0}.
  * thm:no-collision  (n=2^m): if p > exp(C1 n log(2n)/sigma) then EVERY finite-field
    prefix collision is already char-0 (so the per-fiber NEW-collision count is 0).
  * rem:galois-limit: the gap is the window  poly(n) <= p <= quasipoly(n)=exp(O((log n)^2))
    at the critical reserve sigma ~ n/log n; closing it needs a finite-field LOCAL LIMIT
    theorem, not a norm-divisor argument.

EXACT METHOD (two primes; both keys are O(s*sigma) finite-field prefixes).
  p_small : the actual reduction prime (the fiber key, varies across the window).
  P_big   : a faithful char-0 fingerprint prime: P_big == 1 mod n and
            P_big > (2*C(s, s//2))^{phi(n)}. Each archimedean conjugate of
            e_i(S) - e_i(T) has modulus <= 2*C(s, floor(s/2)), so its Q(zeta)/Q norm is
            < P_big; hence the degree-one prime above P_big divides no nonzero
            char-0 prefix difference, i.e. the P_big-prefix tuple is an EXACT char-0 key.
  Group s-subsets by p_small key -> fibers; inside a fiber group by P_big key -> char-0
  classes of sizes m_1..m_t with sum M. Per-fiber collision count = M^2 - sum_i m_i^2.

SMALL-n FINDING (rho=1/2, sigma = round(n/log_2 n) = the regime; window p >= n^2):
    n   regime sigma   max per-fiber collisions, p >= n^2
    8       3                0
   12       3                0
   16       4                0
   18       4                0
   20       5                0
   24       5                0   (p=577)
  i.e. ZERO new collisions in-window for every enumerable n (incl. non-2-power 12,18,20,24);
  the empirical no-collision onset is ~ n^2, FAR below the proved quasipoly threshold.
  BELOW the regime (sigma=2) fibers blow up (sizes 54/139/133 at n=16/18/20, thousands of
  collisions) -- confirming sigma >= C n/log n is sharp. Polynomial growth is thus the
  observed behavior at the regime; the open question is purely the worst-case prime in the
  window [n^2, n^{O(log n)}], which small-n enumeration cannot settle.

  PROVABLE SUB-CASE this pins: for a CONSTANT reserve sigma = eps*n the no-collision
  threshold exp(C1 log(2n)/eps) = (2n)^{C1/eps} is polynomial, so thm:no-collision ALREADY
  proves the per-fiber bound for all p in the window. conj:B is open ONLY as sigma -> n/log n.

Run:
    python3 experimental/scripts/verify_x1_perfiber_collisions.py            # self-test + demo
    python3 experimental/scripts/verify_x1_perfiber_collisions.py --json
    python3 experimental/scripts/verify_x1_perfiber_collisions.py --n 16 --sigma 4 --p 257
"""
from __future__ import annotations
import argparse, json, math, random
from itertools import combinations
from math import comb, gcd


def is_prime(num: int) -> bool:
    if num < 2:
        return False
    for sp in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if num % sp == 0:
            return num == sp
    d, r = num - 1, 0
    while d % 2 == 0:
        d //= 2; r += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, num)
        if x in (1, num - 1):
            continue
        for _ in range(r - 1):
            x = x * x % num
            if x == num - 1:
                break
        else:
            return False
    return True


def prime_factors(n: int) -> set:
    f, d, m = set(), 2, n
    while d * d <= m:
        while m % d == 0:
            f.add(d); m //= d
        d += 1
    if m > 1:
        f.add(m)
    return f


def smallest_prime_1modn_above(n: int, lo: int) -> int:
    t = max(1, (max(lo, 2) - 1 + n - 1) // n)
    while True:
        p = 1 + n * t
        if p >= lo and is_prime(p):
            return p
        t += 1


def order_n_element(p: int, n: int, rng: random.Random) -> int:
    assert (p - 1) % n == 0
    pf, cof = prime_factors(n), (p - 1) // n
    while True:
        g = pow(rng.randrange(2, p - 1), cof, p)
        if g != 1 and all(pow(g, n // q, p) != 1 for q in pf):
            return g


def prefix_mod(elements, sigma: int, p: int) -> tuple:
    """(e_1,...,e_sigma) of `elements` in F_p, via truncated product prod (1 + a y)."""
    c = [0] * (sigma + 1)
    c[0] = 1
    for a in elements:
        for j in range(sigma, 0, -1):
            c[j] = (c[j] + a * c[j - 1]) % p
    return tuple(c[1:sigma + 1])


def run(n: int, rho: float, sigma: int, p_small: int, seed: int = 12345) -> dict:
    rng = random.Random(seed)
    s = round(rho * n)
    assert s >= sigma, f"need s={s} >= sigma={sigma}"
    assert (p_small - 1) % n == 0, f"need p_small == 1 mod {n}"
    phi = sum(1 for a in range(1, n + 1) if gcd(a, n) == 1)
    P_big = smallest_prime_1modn_above(n, (2 * comb(s, s // 2)) ** phi + 1)
    gs = order_n_element(p_small, n, rng)
    gb = order_n_element(P_big, n, rng)
    sp = [pow(gs, a, p_small) for a in range(n)]
    bp = [pow(gb, a, P_big) for a in range(n)]
    M0 = 1
    while M0 <= sigma:
        M0 <<= 1
    fibers, char0 = {}, {}
    total = 0
    for A in combinations(range(n), s):
        total += 1
        ks = prefix_mod([sp[a] for a in A], sigma, p_small)
        kb = prefix_mod([bp[a] for a in A], sigma, P_big)
        d = fibers.setdefault(ks, {})
        d[kb] = d.get(kb, 0) + 1
        char0[kb] = char0.get(kb, 0) + 1
    max_fib = max_coll = total_coll = ncoll = 0
    for d in fibers.values():
        M = sum(d.values())
        coll = M * M - sum(v * v for v in d.values())
        max_fib = max(max_fib, M)
        max_coll = max(max_coll, coll)
        total_coll += coll
        ncoll += (coll > 0)
    thr = math.exp(n * math.log(2 * n) / sigma)  # thm:no-collision ref threshold (C1=1)
    pow2 = (n & (n - 1)) == 0
    return {
        "n": n, "rho": rho, "s": s, "sigma": sigma, "phi(n)": phi,
        "p_small": p_small, "P_big_bits": P_big.bit_length(),
        "n_is_pow2": pow2, "M0_least_pow2_gt_sigma": M0,
        "total_subsets": total, "num_fibers": len(fibers),
        "max_fiber_size": max_fib,
        "max_char0_class": max(char0.values()) if char0 else 0,
        "cor_upstairs_bound_2^(n/M0)": (2 ** (n // M0)) if pow2 else None,
        "max_per_fiber_collisions": max_coll,
        "total_collisions": total_coll, "num_collision_fibers": ncoll,
        "no_collision_threshold_C1=1": thr, "p_small_above_threshold": p_small > thr,
    }


def selftest() -> bool:
    """Cross-check M^2 - sum m_i^2 against a brute-force O(subsets^2) pair count."""
    rng = random.Random(1)
    n, sigma, p = 12, 2, 13
    s = n // 2
    phi = sum(1 for a in range(1, n + 1) if gcd(a, n) == 1)
    P_big = smallest_prime_1modn_above(n, (2 * comb(s, s // 2)) ** phi + 1)
    gs = order_n_element(p, n, rng)
    gb = order_n_element(P_big, n, rng)
    sp = [pow(gs, a, p) for a in range(n)]
    bp = [pow(gb, a, P_big) for a in range(n)]
    rows = [(prefix_mod([sp[a] for a in A], sigma, p),
             prefix_mod([bp[a] for a in A], sigma, P_big))
            for A in combinations(range(n), s)]
    brute = sum(1 for i in range(len(rows)) for j in range(len(rows))
                if rows[i][0] == rows[j][0] and rows[i][1] != rows[j][1])
    return brute == run(n, 0.5, sigma, p)["total_collisions"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=None)
    ap.add_argument("--rho", type=float, default=0.5)
    ap.add_argument("--sigma", type=int, default=None)
    ap.add_argument("--p", type=int, default=None)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    ok = selftest()
    if a.n is None:
        rows = []
        for n in (8, 12, 16, 18, 20):
            sg = max(2, round(n / math.log2(n)))
            p = smallest_prime_1modn_above(n, n * n)  # window edge p ~ n^2
            rows.append(run(n, a.rho, sg, p))
        out = {"selftest_pass": ok, "regime_window_edge_sweep": rows}
    else:
        sg = a.sigma or max(2, round(a.n / math.log2(a.n)))
        p = a.p or smallest_prime_1modn_above(a.n, a.n * a.n)
        out = {"selftest_pass": ok, "result": run(a.n, a.rho, sg, p)}
    if a.json:
        print(json.dumps(out, default=str))
    else:
        print("prob:perfiber exact enumerator (slackMCA_v3.tex:1227). selftest:",
              "PASS" if ok else "FAIL")
        for r in out.get("regime_window_edge_sweep", [out.get("result", {})]):
            if r:
                print(f"  n={r['n']:>3} sigma={r['sigma']} s={r['s']} p={r['p_small']:>6} "
                      f"(>=n^2)  max_per_fiber_collisions={r['max_per_fiber_collisions']:>4} "
                      f"  max_char0_class={r['max_char0_class']}")
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
