#!/usr/bin/env python3
"""L2 quotient-core interleaved count: exact formula, brute-validated.

EXPERIMENTAL / AUDIT verifier for the aligned quotient-core packet count under
column-distance interleaving, from `l2_interleaved_support_bridge.md`. List-side
only; no Paper A-D edits; no M1.

Setup (bridge note). K <= H of order M, N = n/M, M | k, ell = k/M; slack sets
T_i (|T_i| = sigma < M) inside one omitted K-coset, tau = |T_1 cap ... cap T_mu|.
The packet has one support S_A = T_i union U_A per ell-subset A of the Q = N-1
non-omitted cosets, with
    |S_{A_1} cap ... cap S_{A_mu}| = tau + M |A_1 cap ... cap A_mu|.
At agreement threshold a, an interleaved mu-tuple is listed iff
    |A_1 cap ... cap A_mu| >= h(a,tau) = ceil((a - tau)/M).
So the aligned packet contributes exactly
    L_mu(a,tau) = sum_{c=h}^{ell} binom(Q,c) E_empty(Q-c, ell-c, mu),
    E_empty(R,b,mu) = sum_{j=0}^b (-1)^j binom(R,j) binom(R-j, b-j)^mu
                    = # of mu ordered b-subsets of [R] with empty common
                      intersection,
interpolating L (diagonal, a = k+sigma => h = ell) and L^mu (h = 0).

This script (1) brute-validates E_empty and L_mu against direct enumeration for
small parameters, (2) prints the diagonal<->Cartesian interpolation as the
threshold a drops, and (3) reports the saving at prize-relevant (n,k,M,mu).
Standard library only.
"""

import argparse
import itertools
import json
import sys
from math import comb


def E_empty(R, b, mu):
    """# of mu ordered b-subsets of [R] with empty common intersection."""
    if b < 0 or b > R:
        return 0
    return sum((-1) ** j * comb(R, j) * comb(R - j, b - j) ** mu
               for j in range(b + 1))


def h_thresh(a, tau, M):
    return -(-(a - tau) // M) if a > tau else 0      # ceil((a-tau)/M), clamped >=0


def L_mu(N, ell, mu, a, tau, M):
    """Exact aligned quotient-core interleaved count."""
    Q = N - 1
    h = h_thresh(a, tau, M)
    if h > ell:
        return 0
    return sum(comb(Q, c) * E_empty(Q - c, ell - c, mu) for c in range(max(h, 0), ell + 1))


def brute_E_empty(R, b, mu):
    subsets = list(itertools.combinations(range(R), b))
    cnt = 0
    for tup in itertools.product(subsets, repeat=mu):
        common = set(tup[0])
        for s in tup[1:]:
            common &= set(s)
        if not common:
            cnt += 1
    return cnt


def brute_L_mu(N, ell, mu, a, tau, M):
    """Direct count: mu-tuples of ell-subsets of [Q] with |common| >= h(a,tau)."""
    Q = N - 1
    h = h_thresh(a, tau, M)
    subsets = list(itertools.combinations(range(Q), ell))
    cnt = 0
    for tup in itertools.product(subsets, repeat=mu):
        common = set(tup[0])
        for s in tup[1:]:
            common &= set(s)
        if len(common) >= h:
            cnt += 1
    return cnt


def self_check():
    ok = True
    # (1) E_empty vs brute.
    for (R, b, mu) in [(3, 1, 2), (4, 2, 2), (5, 2, 3), (4, 0, 2), (5, 3, 2), (4, 2, 3)]:
        f, br = E_empty(R, b, mu), brute_E_empty(R, b, mu)
        flag = "OK " if f == br else "FAIL"
        ok &= (f == br)
        print(f"  [{flag}] E_empty({R},{b},{mu}) = {f} (brute {br})")
    # (2) L_mu vs brute across small packets and thresholds.
    cases = []
    for (N, ell, mu, M, sigma, tau) in [(4, 1, 2, 4, 2, 2), (5, 2, 2, 4, 2, 2),
                                        (4, 2, 3, 8, 3, 3), (5, 2, 2, 4, 3, 1),
                                        (6, 2, 2, 4, 2, 2)]:
        k = M * ell
        for a in range(k + sigma, max(k - 2 * M, 0) - 1, -M):
            f = L_mu(N, ell, mu, a, tau, M)
            br = brute_L_mu(N, ell, mu, a, tau, M)
            flag = "OK " if f == br else "FAIL"
            ok &= (f == br)
            cases.append((N, ell, mu, M, sigma, tau, a, f, br, flag))
    for (N, ell, mu, M, sigma, tau, a, f, br, flag) in cases:
        print(f"  [{flag}] L_mu N={N} ell={ell} mu={mu} M={M} tau={tau} a={a}: "
              f"{f} (brute {br})")
    # (3) endpoint identities: a=k+sigma => diagonal L; deep a => Cartesian L^mu.
    N, ell, mu, M, sigma, tau = 6, 2, 2, 4, 2, 2
    Q = N - 1
    k = M * ell
    diag = L_mu(N, ell, mu, k + sigma, tau, M)
    cart = L_mu(N, ell, mu, tau, tau, M)            # h=0 => full Cartesian
    flag1 = "OK " if diag == comb(Q, ell) else "FAIL"
    flag2 = "OK " if cart == comb(Q, ell) ** mu else "FAIL"
    ok &= (diag == comb(Q, ell)) and (cart == comb(Q, ell) ** mu)
    print(f"  [{flag1}] diagonal endpoint L_mu(a=k+sigma) = binom(Q,ell) = {comb(Q,ell)} (got {diag})")
    print(f"  [{flag2}] Cartesian endpoint L_mu(h=0) = binom(Q,ell)^mu = {comb(Q,ell)**mu} (got {cart})")
    return ok


def interpolation_table(N, ell, mu, M, sigma, tau):
    Q = N - 1
    k = M * ell
    L = comb(Q, ell)
    rows = []
    for a in range(k + sigma, max(tau - 1, 0) - 1, -1):
        val = L_mu(N, ell, mu, a, tau, M)
        rows.append({"a": a, "h": h_thresh(a, tau, M), "L_mu": val,
                     "vs_diag_L": round(val / L, 3) if L else 0.0,
                     "frac_of_cartesian": round(val / (L ** mu), 6) if L else 0.0})
    return {"N": N, "ell": ell, "mu": mu, "M": M, "sigma": sigma, "tau": tau,
            "diagonal_L": L, "cartesian_L_mu": L ** mu, "rows": rows}


def prize_example(n, k, M, mu, sigma, tau):
    N = n // M
    ell = k // M
    Q = N - 1
    a = k + sigma
    diag = comb(Q, ell)
    val = L_mu(N, ell, mu, a, tau, M)
    return {"n": n, "k": k, "M": M, "N": N, "ell": ell, "mu": mu, "sigma": sigma,
            "tau": tau, "a": a, "h": h_thresh(a, tau, M),
            "L_mu_at_threshold": val, "diagonal_L": diag,
            "cartesian_L_mu": diag ** mu, "is_diagonal": (val == diag)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--self-check", action="store_true")
    ap.add_argument("--format", choices=["human", "json"], default="human")
    args = ap.parse_args(argv)

    if args.self_check:
        print("Self-check: quotient-core interleaved count vs brute force")
        ok = self_check()
        print("RESULT:", "PASS" if ok else "FAIL")
        return 0 if ok else 1

    interp = interpolation_table(6, 2, 2, 4, 2, 2)
    prize = [prize_example(256, 64, 4, 2, 2, 2),
             prize_example(256, 64, 4, 3, 2, 2),
             prize_example(1024, 256, 8, 2, 2, 2)]
    out = {"status": "EXPERIMENTAL/AUDIT", "interpolation": interp, "prize": prize}
    if args.format == "json":
        print(json.dumps(out, indent=2, default=list))
    else:
        ip = interp
        print(f"Quotient-core interleaved count L_mu  (status {out['status']})")
        print(f"  interpolation N={ip['N']} ell={ip['ell']} mu={ip['mu']} M={ip['M']} "
              f"sigma={ip['sigma']} tau={ip['tau']}: diagonal L={ip['diagonal_L']}, "
              f"Cartesian L^mu={ip['cartesian_L_mu']}")
        for row in ip["rows"]:
            print(f"    a={row['a']:>3} h={row['h']:>2}: L_mu={row['L_mu']:>5}  "
                  f"(= {row['vs_diag_L']}*L, {row['frac_of_cartesian']} of Cartesian)")
        print("  prize examples (a = k+sigma, aligned, diagonal expected):")
        for pz in prize:
            print(f"    n={pz['n']} k={pz['k']} M={pz['M']} mu={pz['mu']}: "
                  f"L_mu={pz['L_mu_at_threshold']} == diagonal {pz['diagonal_L']}? "
                  f"{pz['is_diagonal']}; Cartesian would be L^mu "
                  f"(~{pz['diagonal_L']}^{pz['mu']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
