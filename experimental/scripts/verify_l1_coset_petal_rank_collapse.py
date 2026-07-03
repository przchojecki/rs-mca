#!/usr/bin/env python3
r"""
Verifier for l1_coset_petal_rank_collapse.md.

Checks four claims about the full-petal CRT operator pi_{>d} R_{I,d}
(l1_full_list_quotient_proof_program.md Lemma 7/8) on the round-robin-coset
family (petals = distinct cosets g_i H of the order-ell subgroup H of F_p^*,
labels a_i = g_i^ell pairwise distinct), the family introduced as a rank
route-cut in l1_full_petal_growing_defect_witnesses.md:

  (1) BLOCK DECOMPOSITION. r_{I,d} = sum_{r=0}^{ell-1} rank B_{d_r} where
      d_r = floor((d-r)/ell) and B_m is the t-node block map
      F in F_p[Y]_{<=m} |-> coeffs of Y^{m+1..t-1} of the degree-<t
      interpolant of (a_i -> c_i F(a_i)).  Checked on a deterministic grid
      including degenerate scalars.

  (2) RANK CAP + FORCED-DROP WINDOW + ACHIEVABILITY. r_{I,d} <=
      sum_r min(d_r+1, t-1-d_r) <= ell*floor(t/2) for every scalar choice;
      for t odd the strict drop below the refuted exact formula
      min(d+1, t*ell-d-1) is forced (scalar-independently) exactly on the
      window d in [ell(t-1)/2, ell(t-1)/2 + ell - 2]; and the generic value
      sum_r min(d_r+1, t-1-d_r) is achieved by an explicit scalar vector
      (single-spike moment construction), so the cap chain is tight.

  (3) HANKEL NORMAL FORM. rank B_m equals the rank of the (m+1) x (t-1-m)
      Hankel section (s_{j+u}) of the weighted moments
      s_j = sum_i (c_i / L'(a_i)) a_i^j.  (The tempting refinement
      "= min(m+1, t-1-m, BM-linear-complexity)" is FALSE; one documented
      counterexample is included as a route-cut check.)

  (4) RECONSTRUCTION COLLAPSE (t=3, d in [ell, 2ell-1], s_0 != 0). The
      kernel is principal, K_{I,d} = g(X^ell) V_{d-ell} with
      g(Y) = s_1 - s_0 Y; every split kernel locator L_D =
      const*(X^ell-beta)*h reconstructs to the SAME codeword
      P = Q_0 L_{C\D_0} (h cancels), so the number of distinct full-petal
      listed codewords in this stratum is exactly 1 if beta = s_1/s_0 is a
      nonzero ell-th power with root coset D_0 inside the core, else 0.
      Checked by explicit reconstruction on a 13-locator instance (p=73,
      genuine cyclic domain H_24) and by FULL brute-force exact list
      decoding on a small instance (p=19) in both a resonant and a
      non-resonant configuration.

HONEST SCOPE: (4) is verified for t=3 in the stated d-range and generic
s_0 != 0 only; t >= 5 (non-principal kernels) and the degenerate cases
s_0 = 0 / beta equal to a petal label / Q_0 vanishing on part of D_0 are
NOT covered by this verifier.

Run:
    python3 verify_l1_coset_petal_rank_collapse.py [--json]
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from scan_l1_full_list_quotient_conjecture import (  # noqa: E402
    eval_poly,
    interpolate_polynomial,
    matrix_rref,
    multiply_by_linear,
    poly_degree,
    trim_poly,
)
from verify_l1_full_petal_growing_defect_witnesses import (  # noqa: E402
    exact_list_decode,
    locator,
    rank_general,
)


# ---------- shared small helpers (exact arithmetic over F_p) ----------

def inv(x: int, p: int) -> int:
    return pow(x, p - 2, p)


def order(x: int, p: int) -> int:
    o, y = 1, x
    while y != 1:
        y = y * x % p
        o += 1
    return o


def subgroup(p: int, m: int) -> list[int]:
    g = next(x for x in range(2, p) if order(x, p) == p - 1)
    h = pow(g, (p - 1) // m, p)
    return sorted(pow(h, i, p) for i in range(m))


def coset_family(p: int, ell: int, t: int) -> tuple[list[list[int]], list[int]]:
    """First t distinct cosets of the order-ell subgroup, with labels a_i."""
    H = subgroup(p, ell)
    petals, labels, seen = [], [], set()
    for g in range(1, p):
        a = pow(g, ell, p)
        if a in seen:
            continue
        seen.add(a)
        petals.append(sorted(g * h % p for h in H))
        labels.append(a)
        if len(petals) == t:
            break
    return petals, labels


def block_rank(p: int, labels: list[int], scalars: list[int], m: int) -> int:
    t = len(labels)
    if m >= t - 1:
        return 0
    rows = []
    for j in range(m + 1):
        ys = [(c * pow(a, j, p)) % p for a, c in zip(labels, scalars)]
        w = list(interpolate_polynomial(labels, ys, p)) + [0] * t
        rows.append(w[m + 1 : t])
    _, pivots = matrix_rref(rows, p)
    return len(pivots)


def moments(p: int, labels: list[int], scalars: list[int]) -> list[int]:
    t = len(labels)
    s = []
    for j in range(t - 1):
        v = 0
        for i, (a, c) in enumerate(zip(labels, scalars)):
            lp = 1
            for jj, b in enumerate(labels):
                if jj != i:
                    lp = lp * (a - b) % p
            v = (v + c * inv(lp, p) * pow(a, j, p)) % p
        s.append(v)
    return s


def hankel_rank(p: int, s: list[int], m: int, t: int) -> int:
    if m >= t - 1:
        return 0
    rows = [[s[j + u] for u in range(t - 1 - m)] for j in range(m + 1)]
    _, pivots = matrix_rref(rows, p)
    return len(pivots)


def poly_mul(A: list[int], B: list[int], p: int) -> list[int]:
    C = [0] * (len(A) + len(B) - 1)
    for i, a in enumerate(A):
        if a:
            for j, b in enumerate(B):
                C[i + j] = (C[i + j] + a * b) % p
    return C


def scalar_for_spike(p: int, labels: list[int], kappa: int) -> list[int] | None:
    """Solve sum_i (c_i / L'(a_i)) a_i^j = delta_{j,kappa}, j=0..t-2, for c
    (single-spike moment sequence). Returns one solution or None."""
    t = len(labels)
    rows = []
    for j in range(t - 1):
        row = []
        for i, a in enumerate(labels):
            lp = 1
            for jj, b in enumerate(labels):
                if jj != i:
                    lp = lp * (a - b) % p
            row.append(inv(lp, p) * pow(a, j, p) % p)
        rows.append(row + [1 if j == kappa else 0])
    red, pivots = matrix_rref(rows, p)
    c = [0] * t
    for r, col in enumerate(pivots):
        if col == t:
            return None
        c[col] = red[r][t] % p
    return c


# ---------- check (1): block decomposition ----------

def check_block_decomposition() -> dict:
    grid = []
    for p in (19, 31, 61):
        for ell in (2, 3, 4, 5, 6):
            if (p - 1) % ell:
                continue
            for t in (2, 3, 5):
                if t > (p - 1) // ell:
                    continue
                grid.append((p, ell, t))
    checked, mismatches = 0, []
    for p, ell, t in grid:
        petals, labels = coset_family(p, ell, t)
        scalar_sets = [
            list(range(1, t + 1)),
            [pow(3, i + 1, p) for i in range(t)],
            [1] * t,
            [1] * (t - 1) + [2],
            labels[:],
        ]
        for scalars in scalar_sets:
            for d in range(ell, (t - 1) * ell + 1):
                full = rank_general(p, petals, scalars, d)
                blocks = sum(
                    block_rank(p, labels, scalars, (d - r) // ell) for r in range(ell)
                )
                checked += 1
                if full != blocks:
                    mismatches.append((p, ell, t, scalars, d, full, blocks))
    return {"checked": checked, "mismatches": mismatches[:5], "ok": not mismatches}


# ---------- check (2): cap, window, achievability ----------

def check_cap_window_achievability() -> dict:
    checked, cap_viol, window_err, achieve_fail = 0, [], [], []
    for p in (31, 61, 127):
        for ell in (2, 3, 4, 5):
            if (p - 1) % ell:
                continue
            for t in (3, 5, 4):
                if t > (p - 1) // ell:
                    continue
                petals, labels = coset_family(p, ell, t)
                lo = ell * (t - 1) // 2
                window = set(range(lo, lo + ell - 1)) if t % 2 else set()
                window &= set(range(ell, (t - 1) * ell + 1))
                for d in range(ell, (t - 1) * ell + 1):
                    drs = [(d - r) // ell for r in range(ell)]
                    generic = sum(min(m + 1, t - 1 - m) for m in drs)
                    old = min(d + 1, t * ell - d - 1)
                    cap = ell * (t // 2)
                    for scalars in (
                        list(range(1, t + 1)),
                        [pow(5, i + 1, p) for i in range(t)],
                        labels[:],
                        [1] * t,
                    ):
                        r = rank_general(p, petals, scalars, d)
                        checked += 1
                        if r > min(generic, cap):
                            cap_viol.append((p, ell, t, d, scalars, r, generic, cap))
                    # window claim is about the GENERIC value vs old formula
                    forced = generic < old
                    if forced != (d in window):
                        window_err.append((p, ell, t, d, generic, old, sorted(window)))
                    # achievability via single-spike scalars
                    mu = None
                    for kappa in range(t - 1):
                        c = scalar_for_spike(p, labels, kappa)
                        if c is None:
                            continue
                        r = rank_general(p, petals, c, d)
                        checked += 1
                        if r == generic:
                            mu = kappa
                            break
                    if mu is None:
                        # fall back: random-ish deterministic hunt
                        found = False
                        for z in range(2, 40):
                            c = [pow(z, (i + 1) * (i + 2), p) for i in range(t)]
                            if rank_general(p, petals, c, d) == generic:
                                found = True
                                break
                        if not found:
                            achieve_fail.append((p, ell, t, d, generic))
    return {
        "checked": checked,
        "cap_violations": cap_viol[:5],
        "window_errors": window_err[:5],
        "achievability_failures": achieve_fail[:5],
        "ok": not cap_viol and not window_err and not achieve_fail,
    }


# ---------- check (3): Hankel normal form + LC route-cut ----------

def check_hankel_form() -> dict:
    checked, mismatches = 0, []
    for p in (19, 61, 101):
        rng_state = 12345
        for t in (2, 3, 4, 5, 6, 7):
            if t > p - 1:
                continue
            for trial in range(30):
                rng_state = (rng_state * 1103515245 + 12345) % (2**31)
                pool = list(range(1, p))
                labels = []
                st = rng_state
                while len(labels) < t:
                    st = (st * 1103515245 + 12345) % (2**31)
                    x = pool[st % len(pool)]
                    if x not in labels:
                        labels.append(x)
                scalars = []
                for i in range(t):
                    st = (st * 1103515245 + 12345) % (2**31)
                    scalars.append(1 + st % (p - 1))
                if trial % 3 == 0:
                    scalars = [scalars[0]] * t  # constant (rank-0 case)
                s = moments(p, labels, scalars)
                for m in range(t - 1):
                    br = block_rank(p, labels, scalars, m)
                    hr = hankel_rank(p, s, m, t)
                    checked += 1
                    if br != hr:
                        mismatches.append((p, t, labels, scalars, m, br, hr))
    # documented LC-refinement route-cut instance (from the S3 adversary):
    p, t, m = 7, 4, 1
    labels, scalars = [2, 3, 1, 5], [6, 5, 0, 3]
    s = moments(p, labels, scalars)
    lc_routecut_ok = (
        s == [0, 0, 6]
        and block_rank(p, labels, scalars, m) == 1
        and hankel_rank(p, s, m, t) == 1
        and min(m + 1, t - 1 - m) == 2
    )
    return {
        "checked": checked,
        "mismatches": mismatches[:5],
        "lc_refinement_routecut_reproduced": lc_routecut_ok,
        "ok": not mismatches and lc_routecut_ok,
    }


# ---------- check (4): reconstruction collapse ----------

def build_sunflower(p, n, ell, t, scalars, junk_style):
    """Genuine cyclic domain H_n, petals = t cosets of H_ell, core = rest."""
    Hn = subgroup(p, n)
    H = subgroup(p, ell)
    cosets, seen = [], set()
    for x in Hn:
        if x in seen:
            continue
        cs = sorted(x * h % p for h in H)
        cosets.append(cs)
        seen.update(cs)
    petals = cosets[:t]
    labels = [pow(pt[0], ell, p) for pt in petals]
    rest_cosets = cosets[t:]
    return Hn, petals, labels, rest_cosets


def collapse_instance(p, n, ell, scalars, want_resonant, do_decode):
    """Build a t=3 instance; return (collapse stats, decode stats or None)."""
    t = 3
    Hn, petals, labels, rest = build_sunflower(p, n, ell, t, scalars, "all")
    # moments and beta
    s = moments(p, labels, scalars)
    if s[0] == 0:
        return None  # degenerate, scoped out
    beta = s[1] * inv(s[0], p) % p
    cube_map = {pow(cs[0], ell, p): cs for cs in rest}
    resonant = beta in cube_map
    if resonant != want_resonant:
        return None
    core = [x for cs in rest for x in cs]
    k = len(core) + 1
    sthr = k + ell - 1
    L_C = locator(core, p)
    petal_pts = [x for pt in petals for x in pt]

    def crt_deg_and_rep(target):
        xs, ys = [], []
        for pt, c in zip(petals, scalars):
            for x in pt:
                xs.append(x)
                ys.append(c * eval_poly(target, x, p) % p)
        w = trim_poly(interpolate_polynomial(xs, ys, p))
        return poly_degree(w), list(w)

    stats = {"resonant": resonant, "beta": beta, "n": n, "k": k, "s": sthr}
    if resonant:
        D0 = cube_map[beta]
        junk = [x for x in core if x not in D0]
        codewords = set()
        n_locators = 0
        for delta in range(0, ell):  # d = ell+delta over the FULL window [ell, 2ell-1]
            d = ell + delta
            for J in itertools.combinations(junk, delta):
                D = D0 + list(J)
                L_D = locator(D, p)
                dW, W = crt_deg_and_rep(L_D)
                if dW > d:
                    continue
                n_locators += 1
                rest_pts = [x for x in core if x not in D]
                P = poly_mul(W, list(locator(rest_pts, p)), p)
                agr = frozenset(
                    x for x in Hn
                    if eval_poly(tuple(P), x, p)
                    == (scalars[[i for i, pt in enumerate(petals) if x in pt][0]]
                        * eval_poly(L_C, x, p) % p if x in petal_pts else 0)
                )
                key = tuple(P[: poly_degree(trim_poly(tuple(P))) + 1])
                codewords.add((key, agr))
        distinct = len(set(k for k, _ in codewords))
        missed = [sorted(set(core) - set(a)) for _, a in codewords]
        stats.update(
            n_kernel_locators=n_locators,
            distinct_codewords=distinct,
            missed_cores=sorted(set(tuple(m) for m in missed)),
            collapse_ok=(distinct == 1 and n_locators > 1
                         and stats and sorted(set(tuple(m) for m in missed)) == [tuple(D0)]),
        )
    if do_decode:
        u = {x: 0 for x in core}
        for pt, c in zip(petals, scalars):
            for x in pt:
                u[x] = c * eval_poly(L_C, x, p) % p
        listed = exact_list_decode(sorted(Hn), u, k, sthr, p)
        in_range_extras, top_layer_extras = 0, 0
        planted_sets = [frozenset(core) | frozenset(pt) for pt in petals]
        for agr in listed.values():
            if agr in planted_sets:
                continue
            if all(set(pt) <= agr for pt in petals):
                d_exact = len(set(core) - agr)  # exact missed-core size
                if ell <= d_exact <= 2 * ell - 1:
                    in_range_extras += 1
                elif d_exact == 2 * ell:
                    top_layer_extras += 1
        stats.update(
            decode_list_size=len(listed),
            decode_in_range_extras=in_range_extras,
            decode_top_layer_extras=top_layer_extras,
            decode_ok=(in_range_extras == (1 if resonant else 0)),
        )
    return stats


def check_collapse() -> dict:
    out = {}
    # (a) 13-locator collapse instance at p=73, H_24 (construction-level)
    got = None
    for c3 in range(3, 73):
        r = collapse_instance(73, 24, 3, [1, 2, c3], want_resonant=True, do_decode=False)
        if r and r.get("n_kernel_locators", 0) >= 10:
            got = r
            break
    out["big_instance"] = got
    # (b) decode-verified small instances (p=19, H_18, ell=3, t=3, |C|=9, n=18)
    dec_res, dec_non = None, None
    for c3 in range(3, 19):
        r = collapse_instance(19, 18, 3, [1, 2, c3], want_resonant=True, do_decode=True)
        if r:
            dec_res = r
            break
    for c3 in range(3, 19):
        r = collapse_instance(19, 18, 3, [1, 2, c3], want_resonant=False, do_decode=True)
        if r:
            dec_non = r
            break
    out["decode_resonant"] = dec_res
    out["decode_nonresonant"] = dec_non
    out["ok"] = bool(
        got and got.get("collapse_ok")
        and dec_res and dec_res.get("decode_ok")
        and dec_non and dec_non.get("decode_ok")
    )
    return out


def run() -> dict:
    c1 = check_block_decomposition()
    c2 = check_cap_window_achievability()
    c3 = check_hankel_form()
    c4 = check_collapse()
    checks = {
        "(1) block decomposition rank identity": c1["ok"],
        "(2) cap + forced-drop window + achievability": c2["ok"],
        "(3) Hankel normal form + LC route-cut": c3["ok"],
        "(4) t=3 reconstruction collapse (constr + decode)": c4["ok"],
    }
    return {
        "block_decomposition": c1,
        "cap_window_achievability": c2,
        "hankel_form": c3,
        "collapse": c4,
        "checks": checks,
        "all_ok": all(checks.values()),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    out = run()
    if args.json:
        print(json.dumps(out, indent=2, default=str))
        raise SystemExit(0 if out["all_ok"] else 1)
    for name, ok in out["checks"].items():
        print(f"  [{'OK ' if ok else 'FAIL'}] {name}")
    for key in ("block_decomposition", "cap_window_achievability", "hankel_form"):
        print(f"    {key}: checked={out[key]['checked']}")
    col = out["collapse"]
    if col.get("big_instance"):
        b = col["big_instance"]
        print(f"    collapse big instance: {b['n_kernel_locators']} kernel locators -> "
              f"{b['distinct_codewords']} codeword(s), missed core(s)={b['missed_cores']}")
    for tag in ("decode_resonant", "decode_nonresonant"):
        d = col.get(tag)
        if d:
            print(f"    {tag}: list={d.get('decode_list_size')} "
                  f"in-range extras={d.get('decode_in_range_extras')} "
                  f"top-layer(d=2ell, outside claim)={d.get('decode_top_layer_extras')} "
                  f"(resonant={d['resonant']})")
    print("RESULT:", "PASS" if out["all_ok"] else "FAIL")
    raise SystemExit(0 if out["all_ok"] else 1)


if __name__ == "__main__":
    main()
