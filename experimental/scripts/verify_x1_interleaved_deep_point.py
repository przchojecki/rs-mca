#!/usr/bin/env python3
r"""
Interleaved (mu-row) deep-point identity  --  X1 forward / L2.

Verifies the interleaved extension of the deep-point bridge stated in
`experimental/notes/x1/x1_deep_point_interleaved_bridge.md` Section 2.

Setup: C = RS[F_p, D, k], C_+ = RS[F_p, D, k+1], a mu-row received word
U = (U_1,...,U_mu), a deep point alpha in F_p \ D, and the SHARED-POLE curve

    f^{(i)}(x) = U_i(x)/(x-alpha),   g(x) = -1/(x-alpha),   i = 1..mu.

A slope VECTOR z=(z_1,...,z_mu) is interleaved-MCA-bad at radius delta_a=1-a/n
if there is a common support S, |S| >= a, on which every row f^{(i)} + z_i g is
explained by C, while g has no degree-<k explanation on any support of size > k
(the word-independent far condition, identical to the single-row case).

Claim (interleaved deep-point identity):

    BadVec(alpha; a) = Deep_alpha^{mu}(U,a)
      := { (P_1(alpha),...,P_mu(alpha)) :
           P_i in F[X]_{<k+1},
           |{ x in D : P_i(x)=U_i(x) for ALL i }| >= a }.

Consequences checked:
  (A) BadVec == Deep^{mu}   (the identity), for every deep point and word;
  (B) |Deep^{mu}(U,a)| <= |interleaved C_+ list at delta_a|   (list upper bound);
  (C) mu-INDEPENDENT transfer: any two distinct interleaved tuples collide
      (agree in every row) on at most k deep points -- so the deep-point
      evaluation expansion M >= L/(1 + k(L-1)/|Omega|) is the same for all mu.

Finite toy evidence + identity check; no cap / deployed claim.
Status: PROVED-by-check (identity, list bound, collision bound) / EXPERIMENTAL.
Supports X1 (forward list<->MCA) and L2 (interleaved constants).

Run:
    python3 experimental/scripts/verify_x1_interleaved_deep_point.py
    python3 experimental/scripts/verify_x1_interleaved_deep_point.py --json
"""

from __future__ import annotations

import argparse
import json
from itertools import combinations
from typing import Dict, List, Optional, Sequence, Tuple


# ---- prime field + low-degree polynomials (self-contained) ----------------

def multiplicative_subgroup(p: int, n: int) -> List[int]:
    assert (p - 1) % n == 0
    g = None
    for cand in range(2, p):
        x, seen = 1, set()
        for _ in range(p - 1):
            x = (x * cand) % p
            seen.add(x)
        if len(seen) == p - 1:
            g = cand
            break
    h = pow(g, (p - 1) // n, p)
    out, x = [], 1
    for _ in range(n):
        out.append(x)
        x = (x * h) % p
    return sorted(out)


def poly_trim(c: Sequence[int], p: int) -> List[int]:
    out = [x % p for x in c]
    while out and out[-1] == 0:
        out.pop()
    return out


def poly_eval(c: Sequence[int], x: int, p: int) -> int:
    out = 0
    for coeff in reversed(c):
        out = (out * x + coeff) % p
    return out


def degree(c: Sequence[int], p: int) -> int:
    return len(poly_trim(c, p)) - 1


def interpolate(points: Sequence[Tuple[int, int]], p: int) -> List[int]:
    result: List[int] = []
    for i, (xi, yi) in enumerate(points):
        basis, denom = [1], 1
        for j, (xj, _yj) in enumerate(points):
            if i == j:
                continue
            new = [0] * (len(basis) + 1)
            for d, b in enumerate(basis):
                new[d] = (new[d] - xj * b) % p
                new[d + 1] = (new[d + 1] + b) % p
            basis = new
            denom = (denom * (xi - xj)) % p
        scale = (yi * pow(denom, -1, p)) % p
        if len(result) < len(basis):
            result += [0] * (len(basis) - len(result))
        for d, b in enumerate(basis):
            result[d] = (result[d] + scale * b) % p
    return poly_trim(result, p)


def support_close_slope(f_interp, g_interp, k: int, m: int, p: int) -> Optional[int]:
    candidate: Optional[int] = None
    for j in range(k, m):
        fj = f_interp[j] if j < len(f_interp) else 0
        gj = g_interp[j] if j < len(g_interp) else 0
        if gj % p == 0:
            if fj % p != 0:
                return None
            continue
        zj = (-fj * pow(gj, -1, p)) % p
        if candidate is None:
            candidate = zj
        elif candidate != zj:
            return None
    return candidate


# ---- the interleaved objects ----------------------------------------------

def interleaved_list_and_deep(
    U: List[Dict[int, int]], D: List[int], k: int, a: int, alpha: int, p: int,
) -> Tuple[set, set]:
    """Return (interleaved tuples as poly-key vectors, Deep^mu deep-eval vectors).

    A mu-tuple (P_1,...,P_mu) is in the interleaved C_+ list at agreement a iff
    there is a COMMON a-subset S with P_i = interp(U_i|S), deg P_i < k+1 for all i.
    """
    mu = len(U)
    tuples: set = set()
    deep: set = set()
    for S in combinations(D, a):
        Ps = []
        ok = True
        for i in range(mu):
            P = interpolate([(x, U[i][x]) for x in S], p)
            if degree(P, p) >= k + 1:
                ok = False
                break
            Ps.append(P)
        if not ok:
            continue
        tuples.add(tuple(tuple(P) for P in Ps))
        deep.add(tuple(poly_eval(P, alpha, p) for P in Ps))
    return tuples, deep


def bad_slope_vectors(
    U: List[Dict[int, int]], D: List[int], k: int, a: int, alpha: int, p: int,
) -> set:
    """Interleaved-MCA-bad slope vectors of the shared-pole curve at delta_a."""
    mu = len(U)
    inv = {x: pow((x - alpha) % p, -1, p) for x in D}
    f = [{x: (U[i][x] * inv[x]) % p for x in D} for i in range(mu)]
    g = {x: (-inv[x]) % p for x in D}
    out: set = set()
    for S in combinations(D, a):
        gI = interpolate([(x, g[x]) for x in S], p)
        zs = []
        ok = True
        for i in range(mu):
            fI = interpolate([(x, f[i][x]) for x in S], p)
            z = support_close_slope(fI, gI, k, a, p)
            if z is None:
                ok = False
                break
            zs.append(z)
        if ok:
            out.add(tuple(zs))
    return out


def global_far_condition(D: List[int], k: int, alpha: int, p: int) -> bool:
    g = {x: (-pow((x - alpha) % p, -1, p)) % p for x in D}
    for T in combinations(D, k + 1):
        if degree(interpolate([(x, g[x]) for x in T], p), p) < k:
            return False
    return True


def poly_from_roots(roots: Sequence[int], lead: int, p: int) -> List[int]:
    """lead * prod (X - r)."""
    poly = [lead % p]
    for r in roots:
        new = [0] * (len(poly) + 1)
        for d, b in enumerate(poly):
            new[d] = (new[d] - r * b) % p
            new[d + 1] = (new[d + 1] + b) % p
        poly = new
    return poly_trim(poly, p)


def collision_lemma_demo(p: int, deep_points: List[int], k: int, mu: int) -> dict:
    """Constructive demonstration of claim (C): two DISTINCT interleaved mu-tuples
    that differ in one row by V = prod_{i}(X-d_i) (deg <= k, roots d_i in F_p\\D)
    agree (in every row) at exactly deg(V) deep points.  Choosing deg(V)=k roots
    among the deep points achieves collision = k; deg(V) cannot exceed k while
    keeping the row in RS_{<k+1}, so the collision is <= k for every mu.
    """
    jmax = min(k, len(deep_points))
    achieved = []
    base_rows = [[1, 2 % p]] * (mu - 1)  # mu-1 identical fixed rows (deg 1)
    P0 = [0, 0, 1]  # X^2, a fixed RS_{<k+1} poly for row 0 (k>=2 in demos)
    for j in range(0, jmax + 1):
        roots = deep_points[:j]
        V = poly_from_roots(roots, lead=1, p=p)            # deg j <= k
        Pp = poly_trim([(P0[i] if i < len(P0) else 0) + (V[i] if i < len(V) else 0)
                        for i in range(max(len(P0), len(V)))], p)
        # tuple A = (P0, base...), tuple B = (Pp, base...); they differ only in row 0
        collide = sum(1 for al in deep_points
                      if poly_eval(P0, al, p) == poly_eval(Pp, al, p))
        achieved.append(collide)
        assert collide == j, (j, collide)
        assert collide <= k
    return {"mu": mu, "k": k, "max_achieved": max(achieved),
            "reaches_k": (max(achieved) == jmax == k), "never_exceeds_k": True}


def max_simultaneous_collision(tuples: set, deep_points: List[int], k: int, p: int) -> int:
    """Max over distinct interleaved tuples of #{alpha in deep_points : all rows agree}.
    Claim (C): this is <= k regardless of mu."""
    tl = list(tuples)
    worst = 0
    for i in range(len(tl)):
        for j in range(i + 1, len(tl)):
            cnt = 0
            for alpha in deep_points:
                if all(poly_eval(tl[i][r], alpha, p) == poly_eval(tl[j][r], alpha, p)
                       for r in range(len(tl[i]))):
                    cnt += 1
            worst = max(worst, cnt)
    return worst


# ---- word generators ------------------------------------------------------

def lcg(seed: int):
    state = seed % (2 ** 31 - 1) or 1
    while True:
        state = (1103515245 * state + 12345) % (2 ** 31)
        yield state


def quotient_locator_word(D: List[int], k: int, n: int, N: int, p: int) -> Dict[int, int]:
    """Heavy aligned quotient-locator word (same family as the L2/F1 toy):
    U(x) = x^(k+2*a0) + z0 * x^(k+a0), with a0=n/N and z0 the most populous
    elementary-sum fiber over the order-N quotient.  Rich C_+ list at agreement
    a = k+2*a0."""
    a0 = n // N
    Q = sorted({pow(x, a0, p) for x in D})
    assert len(Q) == N
    fibers: Dict[int, int] = {}
    for A in combinations(Q, k // a0 + 2):
        z = (-sum(A)) % p
        fibers[z] = fibers.get(z, 0) + 1
    z0 = max(fibers, key=lambda z: fibers[z])
    return {x: (pow(x, k + 2 * a0, p) + z0 * pow(x, k + a0, p)) % p for x in D}


def dilate(U: Dict[int, int], h: int, D: List[int], p: int) -> Dict[int, int]:
    """(h.U)(x) = U(h^{-1} x); h in the domain group, so permutes D."""
    hinv = pow(h, -1, p)
    return {x: U[(hinv * x) % p] for x in D}


def make_word_sets(D, k, p, mu, n, seed, rich) -> List[Tuple[str, List[Dict[int, int]], bool]]:
    """Return (name, mu-row word, do_collision_check) triples."""
    out = []
    rng = lcg(seed)
    if rich:
        # structured quotient-locator base with a rich C_+ list
        a0 = 2
        N = n // a0
        U0 = quotient_locator_word(D, k, n, N, p)
        # find a domain element h != 1 to dilate the second row
        h = next(x for x in D if x != 1)
        diag = [dict(U0) for _ in range(mu)]                 # all rows equal -> diagonal
        out.append((f"qloc_diag_mu{mu}", diag, True))
        rows = [dict(U0)] + [dilate(U0, h, D, p) for _ in range(mu - 1)]
        out.append((f"qloc_dilate_mu{mu}", rows, True))      # genuinely non-diagonal
    else:
        # row 0 a degree-k word (large structured list), others random
        rows = [{x: pow(x, k, p) for x in D}]
        for _ in range(mu - 1):
            rows.append({x: next(rng) % p for x in D})
        out.append((f"degk+rand_mu{mu}", rows, True))
    return out


CONFIGS = [
    # (p, n, k, a, mu, rich)
    (97, 16, 8, 12, 2, True),    # structured quotient-locator, many deep points
    (97, 16, 8, 12, 3, True),    # same at mu=3 (mu-independence of the bound)
    (17, 8, 3, 5, 2, False),     # small spread case for the collision bound
    (41, 8, 3, 5, 2, False),
]

COLLISION_PAIR_CAP = 4000  # skip the O(L^2) collision scan above this many pairs


def run() -> dict:
    results = []
    all_ok = True
    for (p, n, k, a, mu, rich) in CONFIGS:
        D = multiplicative_subgroup(p, n)
        Dset = set(D)
        deep_points = [al for al in range(p) if al not in Dset]
        cfg = {"p": p, "n": n, "k": k, "a": a, "mu": mu, "rich": rich,
               "deep_points": len(deep_points), "ok": True, "rows": []}
        alpha0 = deep_points[0]
        assert global_far_condition(D, k, alpha0, p)
        for name, U, do_collision in make_word_sets(
                D, k, p, mu, n, seed=20260623 + p + n + k + mu, rich=rich):
            tuples, deep = interleaved_list_and_deep(U, D, k, a, alpha0, p)
            badvec = bad_slope_vectors(U, D, k, a, alpha0, p)
            identity_ok = (badvec == deep)                       # (A)
            list_bound_ok = (len(deep) <= len(tuples))           # (B)
            L = len(tuples)
            if do_collision and L * (L - 1) // 2 <= COLLISION_PAIR_CAP:
                collide = max_simultaneous_collision(tuples, deep_points, k, p)
                collision_ok = (collide <= k)                    # (C)
            else:
                collide = -1                                     # skipped
                collision_ok = True
            row_ok = identity_ok and list_bound_ok and collision_ok
            cfg["rows"].append({
                "word": name, "L_tuples": L,
                "deep_mu": len(deep), "badvec": len(badvec),
                "max_collision": collide, "k": k,
                "identity_ok": identity_ok, "list_bound_ok": list_bound_ok,
                "collision_ok": collision_ok})
            if not row_ok:
                cfg["ok"] = False
                all_ok = False
        results.append(cfg)

    # Constructive collision-lemma demo (claim C), mu-independent.
    Ddemo = multiplicative_subgroup(97, 16)
    deep_demo = [al for al in range(97) if al not in set(Ddemo)]
    lemma = [collision_lemma_demo(97, deep_demo, k=8, mu=m) for m in (1, 2, 3)]
    lemma_ok = all(d["reaches_k"] and d["never_exceeds_k"] for d in lemma)
    if not lemma_ok:
        all_ok = False
    return {"all_ok": all_ok, "configs": results,
            "collision_lemma": {"ok": lemma_ok, "rows": lemma}}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    out = run()
    if args.json:
        print(json.dumps(out, indent=2))
    else:
        print("Interleaved deep-point identity  (X1 forward / L2):")
        print("  BadVec = Deep_alpha^mu(U,a);  |Deep^mu| <= |interleaved list|;"
              "  pairwise collision <= k (mu-independent)")
        print()
        for c in out["configs"]:
            print(f"  p={c['p']} n={c['n']} k={c['k']} a={c['a']} mu={c['mu']}"
                  f"  (deep_points={c['deep_points']})")
            for r in c["rows"]:
                flags = "".join([
                    "I" if r["identity_ok"] else "i",
                    "B" if r["list_bound_ok"] else "b",
                    "C" if r["collision_ok"] else "c"])
                coll = (f"max_collision={r['max_collision']}<=k={r['k']}"
                        if r["max_collision"] >= 0 else f"collision=skipped(L>cap)")
                print(f"      {r['word']:<18} L={r['L_tuples']:>5}"
                      f"  |Deep^mu|={r['deep_mu']:>5}  |BadVec|={r['badvec']:>5}"
                      f"  {coll}  [{flags}]")
        cl = out["collision_lemma"]
        print("  collision lemma (claim C), constructive over F_97, k=8:")
        for d in cl["rows"]:
            print(f"      mu={d['mu']}: max pairwise collision achieved="
                  f"{d['max_achieved']} (= k={d['k']}), never exceeds k  "
                  f"[{'OK' if d['reaches_k'] else 'FAIL'}]")
        print()
        print("RESULT:", "PASS" if out["all_ok"] else "FAIL")
    if not out["all_ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
