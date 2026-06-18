#!/usr/bin/env python3
"""L1 arbitrary-word lift: dilation symmetry of the honest list, and folding.

EXPERIMENTAL / AUDIT verifier for the arbitrary-word (ImgFib) lift of the L1
prefix theory in `l1_prefix_divisor_count.md` (§9). It does not edit Papers A-D
and does not assert protocol safety. List/locator side only; never touches M1.

Objects (cf. `l1_arbitrary_fiber_repair.md`). For a received word `U : H -> F_q`
and agreement threshold `s`, the honest list is
    ImgFib_U(s) = { P in F_{<k}[X] : |{x in H : U(x) = P(x)}| >= s },
i.e. the degree-`<k` codewords of `RS[F_q, H, k]` agreeing with `U` on `>= s`
points (= the list at radius `1 - s/n`).

Two facts are checked:

(1) Dilation symmetry. For `h in H` put `U^h(x) = U(h^{-1} x)`. The map
    P |-> P^h,  P^h(x) = P(h^{-1} x)
is a degree-preserving bijection with agreement set `h * A_P(U)`, so
`ImgFib_{U^h}(s)` is the dilation image of `ImgFib_U(s)` and in particular
`|ImgFib_{U^h}(s)| = |ImgFib_U(s)|`: list size is constant on dilation orbits.

(2) Folding (quotient-core source). If `U = V(X^d)` with `d | n`, `d | k`,
`d | s`, then for every `W` in the folded list `ImgFib_V(s/d)` over
`RS[F_q, mu_{n/d}, k/d]`, the lift `P = W(X^d)` lies in `ImgFib_U(s)`. So a
`d`-periodic received word inherits the entire folded list --- the arbitrary-word
analogue of the §5 divisor coset-union floor.

Standard library only.
"""

import argparse
import itertools
import json
import sys
from collections import defaultdict
from math import gcd


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
    if p == 2:
        return 1
    phi = p - 1
    primes = factorize(phi)
    for g in range(2, p):
        if all(pow(g, phi // q, p) != 1 for q in primes):
            return g
    raise ValueError(f"no primitive root for p={p}")


def subgroup(p, n):
    if (p - 1) % n != 0:
        raise ValueError(f"n={n} does not divide p-1={p-1}")
    g = primitive_root(p)
    h = pow(g, (p - 1) // n, p)
    elems, cur = [], 1
    for _ in range(n):
        elems.append(cur)
        cur = (cur * h) % p
    return elems


def lagrange_values(xs, ys, eval_pts, p):
    """Interpolate the (deg < len(xs)) polynomial through (xs, ys), evaluate on
    eval_pts. Returns the list of values mod p."""
    out = []
    k = len(xs)
    for X in eval_pts:
        acc = 0
        for i in range(k):
            num, den = 1, 1
            xi = xs[i]
            for j in range(k):
                if j == i:
                    continue
                num = (num * (X - xs[j])) % p
                den = (den * (xi - xs[j])) % p
            acc = (acc + ys[i] * num * pow(den, p - 2, p)) % p
        out.append(acc % p)
    return out


def interp_degree(xs, ys, p):
    """Degree of the interpolating polynomial through (xs, ys) (deg < len(xs))."""
    # Newton forward differences would be cleaner; use value-based degree via
    # finite check: build coefficients by Lagrange then trim. For small sizes,
    # evaluate the poly at len(xs) points already given; recover coeffs by solving.
    k = len(xs)
    # Build coefficients via Newton divided differences (exact over F_p).
    coef = list(ys)
    for j in range(1, k):
        for i in range(k - 1, j - 1, -1):
            denom = (xs[i] - xs[i - j]) % p
            coef[i] = ((coef[i] - coef[i - 1]) * pow(denom, p - 2, p)) % p
    # coef are Newton coeffs w.r.t nodes xs; convert to standard poly degree.
    # Standard coefficients via expanding; we only need the degree, i.e. the top
    # nonzero standard coefficient. Expand incrementally.
    poly = [0] * k
    poly[0] = coef[k - 1] % p
    for t in range(k - 2, -1, -1):
        # poly = poly * (X - xs[t]) + coef[t]
        new = [0] * k
        for i in range(k - 1):
            new[i + 1] = (new[i + 1] + poly[i]) % p
        for i in range(k):
            new[i] = (new[i] - poly[i] * xs[t]) % p
        new[0] = (new[0] + coef[t]) % p
        poly = new
    deg = k - 1
    while deg > 0 and poly[deg] % p == 0:
        deg -= 1
    return deg


def img_list(U_vals, H, k, s, p):
    """ImgFib_U(s): set of codeword value-tuples (on H) of degree-<k polys
    agreeing with U on >= s points. Found by interpolating U on every k-subset
    of H and keeping the distinct degree-<k codewords with agreement >= s."""
    n = len(H)
    idx = list(range(n))
    listed = {}
    for sub in itertools.combinations(idx, k):
        xs = [H[i] for i in sub]
        ys = [U_vals[i] for i in sub]
        if interp_degree(xs, ys, p) >= k:      # not a degree-<k codeword fit
            continue
        vals = tuple(lagrange_values(xs, ys, H, p))
        if vals in listed:
            continue
        agree = sum(1 for i in idx if vals[i] == U_vals[i])
        if agree >= s:
            listed[vals] = agree
    return listed  # value-tuple -> agreement count


def dilation_perm(H, p, h):
    """Index permutation x -> h^{-1} x on H (so U^h_vals[i] = U_vals[pi[i]])."""
    pos = {x: i for i, x in enumerate(H)}
    hinv = pow(h, p - 2, p)
    return [pos[(hinv * x) % p] for x in H]


def check_dilation(p, n, k, s, seeds=(0, 7)):
    """List size constant on dilation orbits, for several received words.

    Checks a sample of nontrivial dilations h (enough to exercise the orbit; the
    proof gives the full statement)."""
    H = subgroup(p, n)
    h_sample = [H[i] for i in (1, 2, 3, 5, 7) if i < n]
    ok = True
    details = []
    for seed in seeds:
        # deterministic pseudo-random received word (stdlib only, seed-mixed)
        U = [((seed * 1103515245 + 12345 + i * 2654435761) % p) for i in range(n)]
        base = len(img_list(U, H, k, s, p))
        sizes = []
        for h in h_sample:
            pi = dilation_perm(H, p, h)
            Uh = [U[pi[i]] for i in range(n)]
            sizes.append(len(img_list(Uh, H, k, s, p)))
        all_equal = all(sz == base for sz in sizes)
        ok &= all_equal
        details.append({"seed": seed, "base_list_size": base,
                        "all_orbit_sizes_equal": all_equal,
                        "distinct_sizes": sorted(set(sizes + [base]))})
    return ok, details


def check_folding(p, n, d, k, s, seeds=(0, 1, 2, 3)):
    """For U = V(X^d), every folded codeword W lifts to P=W(X^d) in ImgFib_U(s)."""
    assert n % d == 0 and k % d == 0 and s % d == 0, "need d | n, d | k, d | s"
    H = subgroup(p, n)
    npr, kpr, spr = n // d, k // d, s // d
    Hd = subgroup(p, npr)                 # mu_{n/d}
    ok = True
    checked = 0
    for seed in seeds:
        # Plant a degree-<kpr codeword (so the folded list is nonempty) and add a
        # few errors so the folded decode is nontrivial: V = codeword + errors.
        coef = [((seed * 2654435761 + 11 + i * 40503) % p) for i in range(kpr)]
        V = [sum(coef[i] * pow(y, i, p) for i in range(kpr)) % p for y in Hd]
        for e in range(npr - spr):        # up to npr - spr errors keeps list nonempty
            if (seed + e) % 3 == 0:
                V[(seed + e) % npr] = (V[(seed + e) % npr] + 1 + e) % p
        # U(x) = V(x^d): value of U at H[i] is V at the point x^d in mu_{n/d}.
        posd = {y: j for j, y in enumerate(Hd)}
        U = [V[posd[pow(x, d, p)]] for x in H]
        folded = img_list(V, Hd, kpr, spr, p)        # list of W over mu_{n/d}
        for Wvals in folded:
            # lift: P(x) = W(x^d), so P_vals[i] = Wvals at index of x^d
            Pvals = [Wvals[posd[pow(x, d, p)]] for x in H]
            agree = sum(1 for i in range(n) if Pvals[i] == U[i])
            checked += 1
            if agree < s:
                ok = False
        # also confirm the folded list is nonempty at least once for signal
    return ok, {"folded_lists_checked": len(seeds), "lifts_checked": checked,
                "n": n, "d": d, "n_over_d": npr, "k": k, "k_over_d": kpr,
                "s": s, "s_over_d": spr}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--format", choices=["human", "json"], default="human")
    args = ap.parse_args(argv)

    results = {"status": "EXPERIMENTAL/AUDIT", "checks": {}}

    # (1) Dilation symmetry, F_17, n=16, k=6, s=8.
    dok, ddet = check_dilation(17, 16, 6, 8)
    results["checks"]["dilation_list_size_invariant"] = {"ok": dok, "details": ddet}

    # (2) Folding source, F_17, n=16, d=2 (k=6,s=8) and d=4 (k=8,s=12).
    fok2, fdet2 = check_folding(17, 16, 2, 6, 8)
    fok4, fdet4 = check_folding(17, 16, 4, 8, 12)
    results["checks"]["folding_lift_d2"] = {"ok": fok2, "details": fdet2}
    results["checks"]["folding_lift_d4"] = {"ok": fok4, "details": fdet4}

    overall = dok and fok2 and fok4
    results["overall_pass"] = overall

    if args.format == "json":
        print(json.dumps(results, indent=2))
    else:
        print("L1 arbitrary-word lift verifier  (status EXPERIMENTAL/AUDIT)")
        print(f"  [{'OK ' if dok else 'FAIL'}] dilation: list size constant on "
              f"orbits (F_17,n=16,k=6,s=8)")
        for dd in ddet:
            print(f"        seed {dd['seed']}: |list|={dd['base_list_size']}, "
                  f"orbit sizes {dd['distinct_sizes']}")
        print(f"  [{'OK ' if fok2 else 'FAIL'}] folding d=2: every folded W lifts "
              f"into ImgFib_U(s)  ({fdet2['lifts_checked']} lifts)")
        print(f"  [{'OK ' if fok4 else 'FAIL'}] folding d=4: every folded W lifts "
              f"into ImgFib_U(s)  ({fdet4['lifts_checked']} lifts)")
        print(f"RESULT: {'PASS' if overall else 'FAIL'}")
    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
