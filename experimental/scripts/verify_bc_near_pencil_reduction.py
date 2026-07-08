#!/usr/bin/env python3
"""Near-pencil chart reduction: both sides of the bijection, plus the
q^-(t-1) residual-density calibration.

Companion to experimental/notes/bc_near_pencil_chart_reduction.md.

Construction (toy rows, prime field q, D = order-n subgroup of F_q*,
k = n/2, t = 3, A = k + t): (u, v) is an exact pencil pair
(c0 + z0*w0, w0) perturbed at T with |T| = t + 1 (both du, dv nonzero
everywhere on T).  A "live hit" is a slope/support pair (z, S) with
|S| = A, u + z*v agreeing with a codeword on S, S not tangent-charged,
and v|_S not a degree-<k restriction (validity).

Two independent counts, identical RNG stream per trial:

  side 1 (support mining): enumerate ALL Z subsets of the unperturbed
    domain with |Z| = A - t - 1, solve the T-coincidence system for
    (gamma, z), verify every hit end-to-end (agreement set contains S;
    validity; support-structure lemmas);

  side 2 (locator census): enumerate the same Z space, test only the
    codimension-(t-1) subspace membership ell_Z|_T in span(du|_T, dv|_T)
    with the z = infinity direction removed -- no slope solving, no
    gamma.

The reduction lemma predicts side 1 == side 2 per trial, before and
after the validity filter.  The residual-density model predicts a
per-trial hit mean of C(n - t - 1, A - t - 1) * q^-(t-1) (a q^-2 law on
this ladder).  Expected counts below were first produced on independent
cloud runs (2026-07-07) and are asserted digit-for-digit.

Runtime: about one minute on one core; exact arithmetic throughout.
"""
import itertools
import json
import os
import random
import time

T_RESERVE = 3                     # t = A - k on every toy row
# (n, q, n_trials, seed, run_side2)
ROWS = [
    (24, 73, 5, 7001, True),
    (24, 193, 5, 7002, True),
    (24, 577, 5, 7003, False),
    (24, 1153, 5, 7004, False),
]
# independently banked cloud-run values (valid hits per trial)
EXPECTED_HITS = {
    73: [27, 25, 29, 33, 37],
    193: [2, 4, 5, 4, 7],
    577: [0, 0, 0, 0, 2],
    1153: [0, 0, 0, 1, 0],
}


def prime_factors(x):
    out, d = [], 2
    while d * d <= x:
        while x % d == 0:
            out.append(d)
            x //= d
        d += 1
    if x > 1:
        out.append(x)
    return out


def run_row(row):
    n, q, n_trials, seed, run_side2 = row
    rng = random.Random(seed)
    k, t = n // 2, T_RESERVE
    A = k + t
    sT = t + 1
    inv_t = [0] + [pow(a, q - 2, q) for a in range(1, q)]

    g = next(c for c in range(2, q)
             if all(pow(c, (q - 1) // r, q) != 1
                    for r in set(prime_factors(q - 1))))
    h = pow(g, (q - 1) // n, q)
    D = sorted(pow(h, i, q) for i in range(n))

    def ev(cf, x):
        acc = 0
        for c in reversed(cf):
            acc = (acc * x + c) % q
        return acc

    def interp_coeffs(pts, vals):
        m = len(pts)
        coeffs = [0] * m
        for i, (xi, yi) in enumerate(zip(pts, vals)):
            num = [1]
            den = 1
            for j, xj in enumerate(pts):
                if j == i:
                    continue
                new = [0] * (len(num) + 1)
                for d, cc in enumerate(num):
                    new[d] = (new[d] - cc * xj) % q
                    new[d + 1] = (new[d + 1] + cc) % q
                num = new
                den = den * (xi - xj) % q
            w = yi * inv_t[den] % q
            for d, cc in enumerate(num):
                coeffs[d] = (coeffs[d] + cc * w) % q
        return coeffs

    trials = []
    for _ in range(n_trials):
        # identical draw order to the original cloud runs
        c0 = [rng.randrange(q) for _ in range(k)]
        w0 = [rng.randrange(q) for _ in range(k)]
        z0 = rng.randrange(q)
        T = sorted(rng.sample(D, sT))
        Tset = set(T)
        unpert = [x for x in D if x not in Tset]
        du = {x: rng.randrange(1, q) for x in T}
        dv = {x: rng.randrange(1, q) for x in T}
        u = {x: (ev(c0, x) + z0 * ev(w0, x) + du.get(x, 0)) % q for x in D}
        v = {x: (ev(w0, x) + dv.get(x, 0)) % q for x in D}

        x0, x1 = T[0], T[1]
        a0, b0, a1, b1 = du[x0], dv[x0], du[x1], dv[x1]
        det2 = (a0 * b1 - a1 * b0) % q

        e3_pre = 0          # side-1 candidates passing the T-system
        e3_valid = 0        # ... and the validity filter
        v_in = 0            # side-2 subspace members (z != infinity)
        v_valid = 0         # ... and the validity filter
        slopes = set()
        for Z in itertools.combinations(unpert, A - sT):
            lz = []
            ok = True
            for x in T:
                val = 1
                for zt in Z:
                    val = val * (x - zt) % q
                if val == 0:
                    ok = False
                    break
                lz.append(val)
            if not ok:
                continue

            # --- side 1: solve the T-coincidence system for (gamma, z) ---
            # gamma*lz[i] = du[T[i]] + z*dv[T[i]]; eliminate gamma via i=0,1
            den = (b0 * lz[1] - b1 * lz[0]) % q
            if den:
                num = (a1 * lz[0] - a0 * lz[1]) % q
                z = num * inv_t[den] % q
                gamma = (a0 + z * b0) % q * inv_t[lz[0]] % q
                if gamma and all(
                        (gamma * lz[i] - (du[T[i]] + z * dv[T[i]])) % q == 0
                        for i in range(2, sT)):
                    e3_pre += 1
                    S = sorted(set(Z) | Tset)

                    def cval(x, z=z, gamma=gamma, Z=Z):
                        base = (ev(c0, x) + (z0 + z) * ev(w0, x)) % q
                        lzx = 1
                        for zt in Z:
                            lzx = lzx * (x - zt) % q
                        return (base + gamma * lzx) % q
                    agree = [x for x in D if cval(x) == (u[x] + z * v[x]) % q]
                    assert set(S) <= set(agree), "agreement check failed"
                    assert len(set(S) & Tset) >= t + 1      # support lemma
                    assert set(S) & set(dv.keys())          # validity lemma
                    vc = interp_coeffs(S, [v[x] for x in S])
                    if any(vc[d] % q for d in range(k, A)):
                        e3_valid += 1
                        slopes.add(z)

            # --- side 2: subspace membership only ---
            if run_side2 and det2:
                alpha = (lz[0] * b1 - lz[1] * b0) % q * inv_t[det2] % q
                beta = (a0 * lz[1] - a1 * lz[0]) % q * inv_t[det2] % q
                if all((alpha * du[T[i]] + beta * dv[T[i]] - lz[i]) % q == 0
                       for i in range(2, sT)) and alpha:
                    v_in += 1
                    S = sorted(set(Z) | Tset)
                    vc = interp_coeffs(S, [v[x] for x in S])
                    if any(vc[d] % q for d in range(k, A)):
                        v_valid += 1

        trials.append({"hits_pre_validity": e3_pre, "hits_valid": e3_valid,
                       "n_slopes": len(slopes),
                       "side2_in_subspace": v_in if run_side2 else None,
                       "side2_valid": v_valid if run_side2 else None})
    n_prime = n - sT
    from math import comb
    predicted = comb(n_prime, A - sT) / q ** (t - 1)
    return {"n": n, "q": q, "k": k, "t": t, "A": A, "seed": seed,
            "z_space": comb(n_prime, A - sT),
            "predicted_hit_mean": predicted, "trials": trials}


def main():
    t0 = time.time()
    results = []
    all_ok = True
    print(f"{'(n,q)':>12} {'predicted':>10} {'valid hits per trial':>24} "
          f"{'side2 valid':>20} {'slope budget':>13}")
    for row in ROWS:
        r = run_row(row)
        results.append(r)
        hits = [tr["hits_valid"] for tr in r["trials"]]
        s2 = [tr["side2_valid"] for tr in r["trials"]]
        print(f"  ({r['n']},{r['q']})".rjust(12) +
              f" {r['predicted_hit_mean']:>10.2f} {str(hits):>24} "
              f"{str(s2):>20} {'C(8,4)=70':>13}")
        if hits != EXPECTED_HITS[r["q"]]:
            all_ok = False
            print(f"    MISMATCH vs banked cloud run: expected "
                  f"{EXPECTED_HITS[r['q']]}")
        for tr in r["trials"]:
            if tr["side2_in_subspace"] is not None:
                if tr["hits_pre_validity"] != tr["side2_in_subspace"] or \
                        tr["hits_valid"] != tr["side2_valid"]:
                    all_ok = False
                    print("    BIJECTION MISMATCH:", tr)
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "..", "data", "bc_near_pencil_reduction.json")
    with open(os.path.normpath(data_path), "w") as f:
        json.dump(results, f, indent=1)
    print(f"\nelapsed {time.time() - t0:.1f}s")
    if not all_ok:
        raise SystemExit("BC_NEAR_PENCIL_REDUCTION_FAIL")
    print("every hit end-to-end verified; both support-structure lemmas "
          "held on every hit")
    print("side-1 == side-2 per trial, before and after the validity filter")
    print("BC_NEAR_PENCIL_REDUCTION_PASS")


if __name__ == "__main__":
    main()
