#!/usr/bin/env python3
"""L2 extension-coordinate identity: |Lambda(C_F)| = |Lambda(Int(C_B,e))|.

EXPERIMENTAL / AUDIT verifier for the extension-coordinate formula of
`l2_interleaved_support_bridge.md`, connecting L2 to the extension-list (F1)
program. List/locator side; no Paper A-D edits; no M1.

Let B = F_p, F = F_{p^e}, H = mu_n subset B, C_B = RS[B,H,k], C_F = RS[F,H,k].
Fixing a B-basis of F and writing pi_j : F -> B for the coordinate maps, the
bridge note proves the basis-invariant list identity

    |Lambda(C_F, 1-a/n, U)|
      = #{ (A_1,...,A_e) : A_j in Supp_{pi_j(U)}(a), |A_1 cap ... cap A_e| >= a },

i.e. the extension-code list equals the coordinate-interleaved base list. This
script verifies it directly for e=2 over F_17 (F = F_{289} = F_17[t]/(t^2-3)),
for several received words U : H -> F: it computes the LEFT side by list-decoding
over F_{289}, the RIGHT side from the two base-field coordinate support families,
and checks equality. Standard library only.
"""

import argparse
import itertools
import json
import sys
from math import comb


# ---- base field F_p ----
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


# ---- field op bundles: each element is a hashable token; ops are closures ----
def base_field_ops(p):
    return {
        "add": lambda a, b: (a + b) % p,
        "sub": lambda a, b: (a - b) % p,
        "mul": lambda a, b: (a * b) % p,
        "inv": lambda a: pow(a, p - 2, p),
        "zero": 0, "one": 1,
        "embed": lambda a: a % p,           # B -> B
    }


def ext_field_ops(p, g):
    """F_{p^2} = F_p[t]/(t^2 - g); elements are (a,b) = a + b t."""
    def add(x, y): return ((x[0] + y[0]) % p, (x[1] + y[1]) % p)
    def sub(x, y): return ((x[0] - y[0]) % p, (x[1] - y[1]) % p)
    def mul(x, y):
        a, b = x; c, d = y
        return ((a * c + b * d * g) % p, (a * d + b * c) % p)
    def inv(x):
        a, b = x
        den = (a * a - b * b * g) % p          # norm; nonzero for x != 0
        di = pow(den, p - 2, p)
        return ((a * di) % p, ((-b) * di) % p)
    return {"add": add, "sub": sub, "mul": mul, "inv": inv,
            "zero": (0, 0), "one": (1, 0), "embed": lambda a: (a % p, 0)}


def lagrange_values(xs, ys, eval_pts, ops):
    add, sub, mul, inv = ops["add"], ops["sub"], ops["mul"], ops["inv"]
    out = []
    k = len(xs)
    for X in eval_pts:
        acc = ops["zero"]
        for i in range(k):
            num, den, xi = ops["one"], ops["one"], xs[i]
            for j in range(k):
                if j != i:
                    num = mul(num, sub(X, xs[j]))
                    den = mul(den, sub(xi, xs[j]))
            acc = add(acc, mul(ys[i], mul(num, inv(den))))
        out.append(acc)
    return out


def row_supports(V, Hf, k, a, ops):
    """Full-agreement support family over a field (Hf = eval points in that field)."""
    n = len(Hf)
    idx = list(range(n))
    seen = set()
    supports = set()
    for sub_idx in itertools.combinations(idx, k):
        xs = [Hf[i] for i in sub_idx]
        ys = [V[i] for i in sub_idx]
        vals = tuple(lagrange_values(xs, ys, Hf, ops))
        if vals in seen:
            continue
        seen.add(vals)
        A = frozenset(i for i in idx if vals[i] == V[i])
        if len(A) >= a:
            supports.add(A)
    return supports


def ext_list_size(U_ext, H_ext, k, a, ops):
    return len(row_supports(U_ext, H_ext, k, a, ops))


def coord_interleaved_size(U0, U1, H_base, k, a, bops):
    P = row_supports(U0, H_base, k, a, bops)
    Q = row_supports(U1, H_base, k, a, bops)
    return sum(1 for A in P for B in Q if len(A & B) >= a)


def run(p=17, g=3, n=16, k=6, a=8):
    bops = base_field_ops(p)
    eops = ext_field_ops(p, g)
    H = subgroup(p, n)                       # in F_p
    H_ext = [(x, 0) for x in H]              # embedded in F_{p^2}

    # Received words U : H -> F_{p^2}, given by base coordinates (U0, U1).
    cases = []
    seeds = [(0, 0), (1, 2), (3, 5), (7, 0)]
    ok = True
    for (s0, s1) in seeds:
        U0 = [((s0 * 1103515245 + 12345 + i * 2654435761) % p) for i in range(n)]
        U1 = [((s1 * 1234567891 + 11 + i * 40503) % p) for i in range(n)]
        U_ext = [(U0[i], U1[i]) for i in range(n)]
        lhs = ext_list_size(U_ext, H_ext, k, a, eops)
        rhs = coord_interleaved_size(U0, U1, H, k, a, bops)
        match = (lhs == rhs)
        ok &= match
        cases.append({"seed": [s0, s1], "ext_list": lhs,
                      "coord_interleaved": rhs, "match": match})
    return {"status": "EXPERIMENTAL/AUDIT",
            "params": {"p": p, "g": g, "field": f"F_{p}^2", "n": n, "k": k, "a": a},
            "cases": cases, "overall_pass": ok}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--p", type=int, default=17)
    ap.add_argument("--g", type=int, default=3, help="non-residue for F_{p^2}")
    ap.add_argument("--n", type=int, default=16)
    ap.add_argument("--k", type=int, default=6)
    ap.add_argument("--a", type=int, default=8)
    ap.add_argument("--format", choices=["human", "json"], default="human")
    args = ap.parse_args(argv)
    r = run(args.p, args.g, args.n, args.k, args.a)
    if args.format == "json":
        print(json.dumps(r, indent=2, default=list))
    else:
        pp = r["params"]
        print(f"L2 extension-coordinate identity  (status {r['status']})")
        print(f"  B=F_{pp['p']}, F=F_{pp['p']}^2 (t^2={pp['g']}), n={pp['n']}, "
              f"k={pp['k']}, a={pp['a']}")
        for c in r["cases"]:
            flag = "OK " if c["match"] else "FAIL"
            print(f"  [{flag}] U seed {c['seed']}: |Lambda(C_F)|={c['ext_list']} == "
                  f"coord-interleaved base list={c['coord_interleaved']}")
        print(f"RESULT: {'PASS' if r['overall_pass'] else 'FAIL'}")
    return 0 if r["overall_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
