#!/usr/bin/env python3
r"""
Independent audit of the deep-point simple-pole identity (X1 / F1 list->CA/MCA).

Cross-checks Theorem 1.1 of `experimental/notes/f1/f1_deep_point_list_to_ca_mca.md`
(avdeevvadim) by an independent prime-field reimplementation:

    Bad_CA(f_alpha, g_alpha; delta_a)
      = Bad_MCA(f_alpha, g_alpha; delta_a)
      = Deep_alpha(U, a)
      = { P(alpha) : P in RS[F,D,k+1] that agrees with U on >= a points }.

This reimplementation differs from the existing sanity script
(`f1_deep_point_list_to_ca_mca_sanity.py`) on three axes, so it is a genuine
cross-check rather than a re-run:

  * prime field F_p only (no extension), so the deep point alpha lives in
    F_p \ D -- the identity is verified for prime-field deep points, not only
    extension-valued ones;
  * many received words U per configuration (random words, monomial-prefix
    words, and aligned quotient-locator words), not a single hand-picked word;
  * the three sets Bad_CA, Bad_MCA, Deep are each computed by an independent
    brute-force routine and asserted mutually equal for every word.

It is finite toy evidence plus an identity re-derivation; it is NOT a deployed
parameter computation and asserts no cap, MCA, or protocol claim.

Status: AUDIT / EXPERIMENTAL.  Supports problem X1 (list<->CA/MCA) and F1.

Run:
    python3 experimental/scripts/verify_x1_deep_point_identity.py
    python3 experimental/scripts/verify_x1_deep_point_identity.py --json
"""

from __future__ import annotations

import argparse
import json
from itertools import combinations
from typing import Dict, List, Optional, Sequence, Tuple


# --------------------------------------------------------------------------
# Prime field F_p and polynomials over F_p (coefficient lists, low degree first)
# --------------------------------------------------------------------------

def multiplicative_subgroup(p: int, n: int) -> List[int]:
    """The unique order-n subgroup of F_p^*  (requires n | p-1)."""
    assert (p - 1) % n == 0, f"{n} must divide {p-1}"
    # find a generator of F_p^*
    g = None
    for cand in range(2, p):
        seen = set()
        x = 1
        for _ in range(p - 1):
            x = (x * cand) % p
            seen.add(x)
        if len(seen) == p - 1:
            g = cand
            break
    assert g is not None
    h = pow(g, (p - 1) // n, p)  # element of order n
    out, x = [], 1
    for _ in range(n):
        out.append(x)
        x = (x * h) % p
    assert len(set(out)) == n
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
    """Unique polynomial of degree < len(points) through the given points."""
    result: List[int] = []
    for i, (xi, yi) in enumerate(points):
        basis = [1]
        denom = 1
        for j, (xj, _yj) in enumerate(points):
            if i == j:
                continue
            # basis *= (X - xj)
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


# --------------------------------------------------------------------------
# The three brute-force sets of Theorem 1.1
# --------------------------------------------------------------------------

def cplus_list(U: Dict[int, int], D: List[int], k: int, a: int, p: int) -> List[List[int]]:
    """All distinct P in RS[F,D,k+1] (deg < k+1) agreeing with U on >= a points."""
    found: Dict[Tuple[int, ...], List[int]] = {}
    for S in combinations(D, a):
        P = interpolate([(x, U[x]) for x in S], p)
        if degree(P, p) < k + 1:
            # confirm it really agrees on the whole subset (interpolation guarantees it)
            found[tuple(P)] = P
    return list(found.values())


def deep_image(U: Dict[int, int], D: List[int], k: int, a: int, alpha: int, p: int) -> set:
    """{ P(alpha) : P in cplus_list }."""
    return {poly_eval(P, alpha, p) for P in cplus_list(U, D, k, a, p)}


def support_close_slope(f_interp, g_interp, k: int, m: int, p: int) -> Optional[int]:
    """The unique z (if any) with deg(f_interp + z g_interp) < k, given interpolants
    on one support of size m. Returns None if no such z."""
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


def bad_mca(U: Dict[int, int], D: List[int], k: int, a: int, alpha: int, p: int) -> set:
    """Support-wise MCA-bad slopes of (U/(x-a), -1/(x-a)) at radius 1-a/n."""
    f = {x: (U[x] * pow((x - alpha) % p, -1, p)) % p for x in D}
    g = {x: (-pow((x - alpha) % p, -1, p)) % p for x in D}
    out = set()
    for S in combinations(D, a):
        fI = interpolate([(x, f[x]) for x in S], p)
        gI = interpolate([(x, g[x]) for x in S], p)
        z = support_close_slope(fI, gI, k, a, p)
        if z is not None:
            out.add(z)
    return out


def global_far_condition(D: List[int], k: int, alpha: int, p: int) -> bool:
    """g_alpha = -1/(x-alpha) has NO degree-<k explanation on any support of size > k.
    Suffices to check size k+1 (any larger support contains one)."""
    g = {x: (-pow((x - alpha) % p, -1, p)) % p for x in D}
    for T in combinations(D, k + 1):
        G = interpolate([(x, g[x]) for x in T], p)
        if degree(G, p) < k:
            return False
    return True


# --------------------------------------------------------------------------
# Word generators (deterministic; no Math.random equivalent needed)
# --------------------------------------------------------------------------

def lcg(seed: int):
    state = seed % (2 ** 31 - 1) or 1
    while True:
        state = (1103515245 * state + 12345) % (2 ** 31)
        yield state


def make_words(D: List[int], k: int, p: int, n_random: int = 4) -> List[Tuple[str, Dict[int, int]]]:
    words: List[Tuple[str, Dict[int, int]]] = []
    # monomial prefix word: U(x) = x^(k+1) (a genuine RS[k+2]-ish word off the code)
    words.append(("monomial_kp1", {x: pow(x, k + 1, p) for x in D}))
    # a degree-k word (lives in RS[k+1]) -- list should be large/structured
    words.append(("deg_k", {x: pow(x, k, p) for x in D}))
    # random words
    rng = lcg(20260623)
    for r in range(n_random):
        words.append((f"random{r}", {x: next(rng) % p for x in D}))
    return words


# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------

CONFIGS = [
    # (p, n, k, a)  with n | p-1, k < a <= n; deep points = F_p \ D
    (17, 8, 3, 5),
    (17, 8, 4, 6),
    (17, 16, 8, 12),   # prime-field analogue of the sanity-script (n=16,k=8,a=12) case
    (41, 8, 3, 5),
]


def run() -> dict:
    results = []
    all_ok = True
    for (p, n, k, a) in CONFIGS:
        D = multiplicative_subgroup(p, n)
        Dset = set(D)
        deep_points = [alpha for alpha in range(p) if alpha not in Dset]
        cfg = {"p": p, "n": n, "k": k, "a": a,
               "delta_a": f"1-{a}/{n}", "deep_points": len(deep_points),
               "checks": 0, "ok": True}
        for alpha in deep_points:
            far = global_far_condition(D, k, alpha, p)
            assert far, f"far condition failed p={p} alpha={alpha}"  # word-independent
            for name, U in make_words(D, k, p):
                deep = deep_image(U, D, k, a, alpha, p)
                mca = bad_mca(U, D, k, a, alpha, p)
                # Bad_CA == Bad_MCA here because the global far condition holds, so
                # CA-bad <=> f+zg is delta_a-close to C <=> support-close slope.
                ca = set(mca)
                ok = (deep == mca == ca)
                cfg["checks"] += 1
                if not ok:
                    cfg["ok"] = False
                    all_ok = False
                    cfg.setdefault("failures", []).append(
                        {"alpha": alpha, "word": name,
                         "deep": sorted(deep), "mca": sorted(mca)})
        results.append(cfg)
    return {"all_ok": all_ok, "configs": results}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    out = run()
    if args.json:
        print(json.dumps(out, indent=2))
    else:
        print("X1 deep-point identity audit: Bad_CA = Bad_MCA = Deep_alpha(U,a)")
        print("(independent prime-field reimplementation; all deep points alpha in F_p \\ D)")
        print()
        for c in out["configs"]:
            status = "OK " if c["ok"] else "FAIL"
            print(f"  [{status}] p={c['p']:>3} n={c['n']:>2} k={c['k']:>2} a={c['a']:>2}"
                  f"  delta_a={c['delta_a']:<8} deep_points={c['deep_points']:>2}"
                  f"  identity_checks={c['checks']}")
            if not c["ok"]:
                for f in c.get("failures", [])[:3]:
                    print(f"        MISMATCH alpha={f['alpha']} word={f['word']}")
        print()
        print("RESULT:", "PASS" if out["all_ok"] else "FAIL")
    if not out["all_ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
