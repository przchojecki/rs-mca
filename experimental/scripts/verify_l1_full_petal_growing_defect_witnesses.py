#!/usr/bin/env python3
r"""
Verifier for l1_full_petal_growing_defect_witnesses.md.

Checks two claims about the full-petal sub-case of the L1 full-list
quotient conjecture's sunflower residual (see
experimental/notes/l1/l1_full_list_quotient_proof_program.md Lemma 2/7/8/13
and Theorem 21/B11, and the companion note for this script):

  (1) EXISTENCE WITNESSES. Two explicit background-free sunflower received
      words each have a non-planted listed codeword that touches ALL of its
      t>=3 petals in full, at core-defect excess d-ell>0 (d-ell=2 for t=3,
      d-ell=5 for t=5) -- i.e. strictly beyond the d=ell layer Lemma 9
      already covers. Each witness is checked TWO independent ways: via the
      Lemma 7/8 CRT-degree shortcut, and by literally reconstructing the
      received word and brute-force exact-decoding the full RS list,
      confirming the predicted extra's exact agreement set is present.

  (2) ROUTE-CUT. The natural hope of tightening Lemma 13's floor
      r_{I,d}>=ell into an exact closed form r_{I,d}=min(d+1,t*ell-d-1) is
      FALSE in general. This checks one robust structural counterexample
      family (round-robin subgroup-coset petals, t odd) across several
      scalar choices, confirming the rank stays below the formula's
      prediction for every one of them (Lemma 13's own floor is not
      violated).

HONEST SCOPE: existence only, no growth-rate or density claim for (1); one
representative family for (2), not a full classification of when the exact
formula fails.

Run:
    python3 experimental/scripts/verify_l1_full_petal_growing_defect_witnesses.py
    python3 experimental/scripts/verify_l1_full_petal_growing_defect_witnesses.py --json
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


def locator(roots: list[int], p: int) -> tuple[int, ...]:
    poly: tuple[int, ...] = (1,)
    for root in roots:
        poly = multiply_by_linear(poly, root, p)
    return trim_poly(poly)


def crt_residue_degree(
    petals: list[list[int]], scalars: list[int], target_poly: tuple[int, ...], p: int
) -> int:
    """Degree of the unique poly W (deg < t*ell) with W(x)=c_i*target_poly(x)
    for x in petal i -- the Lemma 7/8 CRT residue."""
    xs, ys = [], []
    for petal, c in zip(petals, scalars, strict=True):
        for x in petal:
            xs.append(x)
            ys.append((c * eval_poly(target_poly, x, p)) % p)
    return poly_degree(trim_poly(interpolate_polynomial(xs, ys, p)))


def exact_list_decode(
    domain: list[int], u: dict[int, int], k: int, s: int, p: int
) -> dict[tuple[int, ...], frozenset[int]]:
    """Brute-force exact RS list decode: every degree-<k poly agreeing with
    u on >=s of the given domain points, keyed by its evaluation tuple."""
    listed: dict[tuple[int, ...], frozenset[int]] = {}
    for support in itertools.combinations(domain, s):
        vals = [u[x] for x in support]
        poly = trim_poly(interpolate_polynomial(list(support), vals, p))
        if poly_degree(poly) >= k:
            continue
        codeword = {x: eval_poly(poly, x, p) for x in domain}
        key = tuple(codeword[x] for x in domain)
        if key in listed:
            continue
        agreement = frozenset(x for x in domain if codeword[x] == u[x])
        if len(agreement) >= s:
            listed[key] = agreement
    return listed


def check_witness(
    label: str,
    p: int,
    petals: list[list[int]],
    scalars: list[int],
    core: list[int],
    retained_core: list[int],
    d: int,
) -> dict:
    ell = len(petals[0])
    t = len(petals)
    domain = [x for petal in petals for x in petal] + core
    assert len(domain) == len(set(domain)), "domain points must be distinct"
    k = len(core) + 1
    s = k + ell - 1

    missed_core = [x for x in core if x not in retained_core]
    assert len(missed_core) == d

    loc_d = locator(missed_core, p)
    crt_degree = crt_residue_degree(petals, scalars, loc_d, p)
    crt_shortcut_ok = crt_degree <= d and poly_degree(loc_d) == d

    loc_c = locator(core, p)
    u = {x: 0 for x in core}
    for petal, c in zip(petals, scalars, strict=True):
        for x in petal:
            u[x] = (c * eval_poly(loc_c, x, p)) % p

    listed = exact_list_decode(domain, u, k, s, p)
    predicted_extra = frozenset(retained_core) | frozenset().union(*(set(pt) for pt in petals))
    planted = [frozenset(core) | frozenset(petal) for petal in petals]
    found_predicted = any(agr == predicted_extra for agr in listed.values())
    found_all_planted = all(any(agr == pl for agr in listed.values()) for pl in planted)

    return {
        "label": label,
        "p": p,
        "ell": ell,
        "t": t,
        "d": d,
        "d_minus_ell": d - ell,
        "n": len(domain),
        "k": k,
        "s": s,
        "crt_shortcut_realizable": crt_shortcut_ok,
        "exact_decoder_total_listed": len(listed),
        "exact_decoder_found_predicted_extra": found_predicted,
        "exact_decoder_found_all_planted": found_all_planted,
        "predicted_extra_agreement_size": len(predicted_extra),
        "ok": crt_shortcut_ok and found_predicted and found_all_planted,
    }


def rank_general(p: int, petals: list[list[int]], scalars: list[int], d: int) -> int:
    t = len(petals)
    ell = len(petals[0])
    n_petal = t * ell
    xs = [x for petal in petals for x in petal]
    rows = []
    for j in range(d + 1):
        ys = []
        for petal, c in zip(petals, scalars, strict=True):
            for x in petal:
                ys.append((c * pow(x, j, p)) % p)
        w = list(interpolate_polynomial(xs, ys, p))
        w = w + [0] * (n_petal - len(w))
        rows.append(w[d + 1 : n_petal])
    _, pivots = matrix_rref(rows, p)
    return len(pivots)


def check_route_cut() -> dict:
    p, ell, t, d = 19, 3, 3, 3
    petals = [[1, 7, 11], [4, 9, 6], [16, 17, 5]]  # cosets of order-3 subgroup of F_19^*
    predicted = min(d + 1, t * ell - d - 1)
    floor_ = ell
    trials = []
    for scalars in ([1, 2, 3], [2, 5, 7], [1, 3, 17], [6, 10, 15]):
        r = rank_general(p, petals, scalars, d)
        trials.append({"scalars": scalars, "rank": r})
    all_below_formula = all(tr["rank"] < predicted for tr in trials)
    all_meet_lemma13_floor = all(tr["rank"] >= floor_ for tr in trials)
    return {
        "p": p,
        "ell": ell,
        "t": t,
        "d": d,
        "predicted_by_exact_formula": predicted,
        "lemma13_floor": floor_,
        "trials": trials,
        "exact_formula_fails_for_every_scalar_choice": all_below_formula,
        "lemma13_floor_never_violated": all_meet_lemma13_floor,
        "ok": all_below_formula and all_meet_lemma13_floor,
    }


def run() -> dict:
    witness_a = check_witness(
        label="Witness A (t=3, ell=3, d=5, d-ell=2)",
        p=1009,
        petals=[[0, 1, 2], [3, 4, 5], [6, 7, 8]],
        scalars=[1, 2, 3],
        core=[558, 784, 852, 874, 900, 901, 902, 903, 904, 905],
        retained_core=[901, 902, 903, 904, 905],
        d=5,
    )
    witness_b = check_witness(
        label="Witness B (t=5, ell=3, d=8, d-ell=5)",
        p=1009,
        petals=[[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11], [12, 13, 14]],
        scalars=[1, 2, 3, 4, 5],
        core=[69, 453, 512, 670, 682, 855, 864, 917],
        retained_core=[],
        d=8,
    )
    route_cut = check_route_cut()

    checks = {
        "Witness A: realizable by CRT shortcut and found by exact decoder": witness_a["ok"],
        "Witness B: realizable by CRT shortcut and found by exact decoder": witness_b["ok"],
        "Route-cut: exact rank formula fails on the coset family (every scalar tried)": route_cut[
            "ok"
        ],
    }
    return {
        "witness_a": witness_a,
        "witness_b": witness_b,
        "route_cut": route_cut,
        "checks": checks,
        "all_ok": all(checks.values()),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    out = run()

    if args.json:
        print(json.dumps(out, indent=2, default=str))
        raise SystemExit(0 if out["all_ok"] else 1)

    print("L1 full-petal growing-defect witnesses + rank-formula route-cut")
    print()
    for key in ("witness_a", "witness_b"):
        w = out[key]
        print(f"  {w['label']}: p={w['p']} n={w['n']} k={w['k']} s={w['s']} "
              f"t={w['t']} ell={w['ell']} d={w['d']} (d-ell={w['d_minus_ell']})")
        print(f"    CRT shortcut realizable: {w['crt_shortcut_realizable']}")
        print(f"    exact decoder: {w['exact_decoder_total_listed']} codewords listed; "
              f"predicted extra found: {w['exact_decoder_found_predicted_extra']}; "
              f"all planted found: {w['exact_decoder_found_all_planted']}")
    rc = out["route_cut"]
    print()
    print(f"  Route-cut (p={rc['p']}, ell={rc['ell']}, t={rc['t']}, d={rc['d']}, "
          f"coset petals): predicted={rc['predicted_by_exact_formula']}, "
          f"Lemma-13 floor={rc['lemma13_floor']}")
    for tr in rc["trials"]:
        print(f"    scalars={tr['scalars']}: rank={tr['rank']}")
    print()
    for name, ok in out["checks"].items():
        print(f"  [{'OK ' if ok else 'FAIL'}] {name}")
    print()
    print(
        "RESULT:",
        "PASS (both growing-defect witnesses confirmed two ways; "
        "exact-rank-formula route-cut confirmed)"
        if out["all_ok"]
        else "FAIL (inspect above)",
    )
    raise SystemExit(0 if out["all_ok"] else 1)


if __name__ == "__main__":
    main()
