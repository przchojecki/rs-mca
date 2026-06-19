#!/usr/bin/env python3
"""L2 interleaved-list constants: bridge, diagonalization, dilation symmetry.

EXPERIMENTAL / AUDIT verifier for the L2 thread (sharp interleaved-list
constants near capacity). Builds on `l2_interleaved_support_bridge.md`. List
/locator side; does not edit Papers A-D; does not touch M1.

For C = RS[F_p, H, k] and a >= k, a row received word V : H -> F_p has the
full-agreement support family

    Supp_V(a) = { A_V(c) : c in C, |A_V(c)| >= a },   A_V(c) = {x : c(x)=V(x)}.

For a mu-row word U=(U_1,...,U_mu), the interleaved (column-distance) list at
radius 1 - a/n is exactly (bridge note)

    |Lambda(Int(C,mu),1-a/n,U)| = #{ (A_1,...,A_mu) : A_i in Supp_Ui(a),
                                     |A_1 cap ... cap A_mu| >= a },

bounded above by the simultaneous feasible fiber
    |Fib_U^cap(a)| = sum_tuples binom(|A_1 cap ... cap A_mu|, a).

This script checks, over F_17, n=16, mu=2:
  (1) bridge: interleaved list <= simultaneous fiber <= min_i |row list|;
  (2) sub-Cartesian: interleaved list <= prod_i |row list| (the saving);
  (3) repeated-row diagonalization: Lambda(Int,(V,V)) = Lambda(C,V);
  (4) dilation symmetry: Lambda invariant under (h.U)_i(x)=U_i(h^{-1}x).
Standard library only.
"""

import argparse
import itertools
import json
import sys
from collections import defaultdict
from math import comb


def factorize(num):
    f, d = set(), 2
    while d * d <= num:
        while num % d == 0:
            f.add(d); num //= d
        d += 1
    if num > 1:
        f.add(num)
    return f


def primitive_root(p):
    phi = p - 1
    primes = factorize(phi)
    for g in range(2, p):
        if all(pow(g, phi // q, p) != 1 for q in primes):
            return g
    raise ValueError("no primitive root")


def subgroup(p, n):
    if (p - 1) % n != 0:
        raise ValueError(f"n={n} does not divide p-1={p-1}")
    g = primitive_root(p)
    h = pow(g, (p - 1) // n, p)
    out, cur = [], 1
    for _ in range(n):
        out.append(cur); cur = (cur * h) % p
    return out


def lagrange_values(xs, ys, eval_pts, p):
    out = []
    k = len(xs)
    for X in eval_pts:
        acc = 0
        for i in range(k):
            num, den, xi = 1, 1, xs[i]
            for j in range(k):
                if j != i:
                    num = (num * (X - xs[j])) % p
                    den = (den * (xi - xs[j])) % p
            acc = (acc + ys[i] * num * pow(den, p - 2, p)) % p
        out.append(acc % p)
    return out


def row_supports(V, H, k, a, p):
    """Full-agreement support family Supp_V(a): frozensets of indices, |A|>=a."""
    n = len(H)
    idx = list(range(n))
    seen = set()
    supports = set()
    for sub in itertools.combinations(idx, k):
        xs = [H[i] for i in sub]
        ys = [V[i] for i in sub]
        vals = tuple(lagrange_values(xs, ys, H, p))
        if vals in seen:
            continue
        seen.add(vals)
        A = frozenset(i for i in idx if vals[i] == V[i])
        if len(A) >= a:
            supports.add(A)
    return supports


def interleaved_and_fiber_2(P, Q, a):
    """Exact 2-row interleaved list and simultaneous fiber from support families."""
    listed = fiber = 0
    for A in P:
        for B in Q:
            r = len(A & B)
            if r >= a:
                listed += 1
                fiber += comb(r, a)
    return listed, fiber


def interleaved_and_fiber_mu(supps, a):
    """Exact mu-row interleaved list and simultaneous fiber for mu support families."""
    listed = fiber = 0
    for tup in itertools.product(*supps):
        common = set(tup[0])
        for A in tup[1:]:
            common &= A
        r = len(common)
        if r >= a:
            listed += 1
            fiber += comb(r, a)
    return listed, fiber


def max_codegree(P, Q, a):
    """max_{A in P} #{B in Q : |A cap B| >= a}  (intersection-codegree certificate)."""
    best = 0
    for A in P:
        best = max(best, sum(1 for B in Q if len(A & B) >= a))
    return best


def dilation_perm(H, p, h):
    pos = {x: i for i, x in enumerate(H)}
    hinv = pow(h, p - 2, p)
    return [pos[(hinv * x) % p] for x in H]


def make_word(kind, n, p, seed=0):
    if kind == "monomial":           # x^a-like monomial-prefix word
        H = subgroup(p, n)
        return [pow(x, (n - 3) % n, p) for x in H]
    if kind == "periodic":           # quotient-periodic: V(x)=W(x^2)
        H = subgroup(p, n)
        return [( (pow(x, 2, p) * 3 + 5) % p ) for x in H]
    # pseudo-random (stdlib only)
    return [((seed * 1103515245 + 12345 + i * 2654435761) % p) for i in range(n)]


def run(p=17, n=16, k=6, a=8):
    H = subgroup(p, n)
    rows = {
        "monomial": make_word("monomial", n, p),
        "periodic": make_word("periodic", n, p),
        "rand0": make_word("rand", n, p, 0),
        "rand1": make_word("rand", n, p, 1),
        "rand2": make_word("rand", n, p, 2),
    }
    supp = {name: row_supports(V, H, k, a, p) for name, V in rows.items()}
    rowlist = {name: len(supp[name]) for name in rows}           # |Supp| (row list)
    fibrow = {name: sum(comb(len(A), a) for A in supp[name])      # raw |Fib_Ui(a)|
              for name in rows}

    # (1)-(2) pairwise bridge / sub-Cartesian over distinct row pairs.
    # Bridge: interleaved <= simultaneous fiber <= min_i |Fib_Ui(a)|.
    # sub-Cartesian saving is against the product of ROW LISTS |Supp|.
    pairs = []
    bridge_ok = cart_ok = True
    for n1, n2 in itertools.combinations(rows, 2):
        listed, fiber = interleaved_and_fiber_2(supp[n1], supp[n2], a)
        fib_min = min(fibrow[n1], fibrow[n2])
        cart = rowlist[n1] * rowlist[n2]
        bridge_ok &= (listed <= fiber <= fib_min)
        cart_ok &= (listed <= cart)
        pairs.append({"rows": f"{n1}x{n2}", "interleaved": listed, "fiber": fiber,
                      "min_fib_row": fib_min, "cartesian_rowlist": cart,
                      "ratio_vs_cartesian": round(listed / cart, 4) if cart else 0.0})

    # (2b) intersection-codegree certificate: interleaved <= |P| * Gamma_{>=a}(P,Q).
    codeg_ok = True
    codeg = []
    for n1, n2 in [("rand0", "rand1"), ("monomial", "rand0")]:
        listed, _ = interleaved_and_fiber_2(supp[n1], supp[n2], a)
        g_pq = max_codegree(supp[n1], supp[n2], a)
        g_qp = max_codegree(supp[n2], supp[n1], a)
        bound = min(rowlist[n1] * g_pq, rowlist[n2] * g_qp)
        codeg_ok &= (listed <= bound)
        codeg.append({"rows": f"{n1}x{n2}", "interleaved": listed,
                      "codegree_bound": bound, "Gamma_pq": g_pq, "Gamma_qp": g_qp})

    # (2c) mu=3 sub-Cartesian: interleaved_3 vs product of row lists.
    mu3 = []
    mu3_ok = True
    for triple in [("rand0", "rand1", "rand2"), ("periodic", "rand0", "rand1")]:
        listed, fiber = interleaved_and_fiber_mu([supp[t] for t in triple], a)
        cart = rowlist[triple[0]] * rowlist[triple[1]] * rowlist[triple[2]]
        lo = min(rowlist[t] for t in triple)
        mu3_ok &= (listed <= cart)
        mu3.append({"rows": "x".join(triple), "interleaved": listed, "fiber": fiber,
                    "min_row": lo, "cartesian": cart,
                    "ratio_vs_cartesian": round(listed / cart, 5) if cart else 0.0})

    # (3) repeated-row diagonalization: Lambda(Int,(V,V)) == |row list|; mu=3 too.
    diag_ok = True
    for name in rows:
        listed2, _ = interleaved_and_fiber_2(supp[name], supp[name], a)
        listed3, _ = interleaved_and_fiber_mu([supp[name]] * 3, a)
        if listed2 != rowlist[name] or listed3 != rowlist[name]:
            diag_ok = False

    # (4) dilation symmetry of the 2-row interleaved list.
    dil_ok = True
    base, _ = interleaved_and_fiber_2(supp["rand0"], supp["rand1"], a)
    for h in [H[i] for i in (1, 3, 5) if i < n]:
        pi = dilation_perm(H, p, h)
        V0h = [rows["rand0"][pi[i]] for i in range(n)]
        V1h = [rows["rand1"][pi[i]] for i in range(n)]
        s0 = row_supports(V0h, H, k, a, p)
        s1 = row_supports(V1h, H, k, a, p)
        lh, _ = interleaved_and_fiber_2(s0, s1, a)
        if lh != base:
            dil_ok = False

    return {
        "status": "EXPERIMENTAL/AUDIT",
        "params": {"p": p, "n": n, "k": k, "a": a, "sigma": a - k},
        "row_list_sizes": rowlist,
        "pairs": pairs,
        "codegree": codeg,
        "mu3": mu3,
        "bridge_ok": bridge_ok,
        "sub_cartesian_ok": cart_ok,
        "codegree_cert_ok": codeg_ok,
        "mu3_sub_cartesian_ok": mu3_ok,
        "diagonalization_ok": diag_ok,
        "dilation_symmetry_ok": dil_ok,
        "overall_pass": (bridge_ok and cart_ok and codeg_ok and mu3_ok
                         and diag_ok and dil_ok),
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--p", type=int, default=17)
    ap.add_argument("--n", type=int, default=16)
    ap.add_argument("--k", type=int, default=6)
    ap.add_argument("--a", type=int, default=8)
    ap.add_argument("--format", choices=["human", "json"], default="human")
    args = ap.parse_args(argv)
    r = run(args.p, args.n, args.k, args.a)
    if args.format == "json":
        print(json.dumps(r, indent=2, default=list))
    else:
        pp = r["params"]
        print(f"L2 interleaved-list constants  (status {r['status']})")
        print(f"  F_{pp['p']}, n={pp['n']}, k={pp['k']}, a={pp['a']} (sigma={pp['sigma']}), mu=2")
        print(f"  row list sizes |Supp|: {r['row_list_sizes']}")
        for pr in r["pairs"]:
            print(f"    {pr['rows']:>16}: interleaved={pr['interleaved']:>4}  "
                  f"fiber={pr['fiber']:>5}  min|Fib|={pr['min_fib_row']:>6}  "
                  f"cart(|Supp|^2)={pr['cartesian_rowlist']:>5}  (ratio {pr['ratio_vs_cartesian']})")
        print("  codegree certificate (interleaved <= |P|*Gamma):")
        for cg in r["codegree"]:
            print(f"    {cg['rows']:>16}: interleaved={cg['interleaved']:>4}  "
                  f"<= bound {cg['codegree_bound']:>5}  (Gamma_pq={cg['Gamma_pq']}, "
                  f"Gamma_qp={cg['Gamma_qp']})")
        print("  mu=3 sub-Cartesian:")
        for m3 in r["mu3"]:
            print(f"    {m3['rows']:>22}: interleaved={m3['interleaved']:>4}  "
                  f"cartesian={m3['cartesian']:>7}  (ratio {m3['ratio_vs_cartesian']})")
        for key in ("bridge_ok", "sub_cartesian_ok", "codegree_cert_ok",
                    "mu3_sub_cartesian_ok", "diagonalization_ok", "dilation_symmetry_ok"):
            print(f"  [{'OK ' if r[key] else 'FAIL'}] {key}")
        print(f"RESULT: {'PASS' if r['overall_pass'] else 'FAIL'}")
    return 0 if r["overall_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
