#!/usr/bin/env python3
r"""Verifier for experimental/notes/roadmaps/qx11_topcore_globalness.md
(DAG node xr_globalness_from_ledger; queue item QX.11).

Theorem G1 (top-core cap => globalness at every link level): if every
(j-1)-set H has at most L completions H u {x} in A subset J(n,j), then for
every r <= j-1 and every r-set R,

    |{T in A : R subset T}| / C(n-r, j-r)  <=  L / (n-j+1).

Checks (exact integer / Fraction arithmetic, stdlib only, deterministic):
  [1] the exact binomial-ratio identity
      (n-j+1) * C(n-r, j-1-r) == (j-r) * C(n-r, j-r)
      for ALL n <= 40, 1 <= j <= n, 0 <= r <= j-1 (the cancellation step);
  [2] the double-count skeleton itself, on J(9,4) with seeded random
      families (NO cap imposed), exhaustive over all r-cores with r <= 3:
      direct pair enumeration == (j-r)*|A_R| == sum_{H >= R} c_A(H),
      and every T in A_R contains exactly j-r admissible H;
  [3] Theorem G1 on greedy cap-respecting families (seeded random insertion
      order): J(9,4) with L in {1,2}, J(10,5) with L in {1,2,3}, 3 seeds
      each; the link bound checked for ALL r-cores (every r <= j-1, every
      R); the realized cap is re-measured, never assumed;
  [4] tightness (equality witnesses): the Fano plane S(2,3,7) in J(7,3) and
      the doubled Steiner quadruple system SQS(8) in J(8,4) are first
      VERIFIED to be Steiner systems (cap L = 1 with every top core hit
      exactly once), then shown to meet G1 with EXACT EQUALITY at every
      r-core; plus the trivial full-family witness (L = n-j+1, density 1);
  [5] adversarial targeted max-packing (families built to load one target
      core R first, subject to the cap): bound never exceeded; achieved
      |A_R| vs the integer ceiling floor(L*C(n-r,j-1-r)/(j-r)) reported;
      on J(9,4), r=2, L=1 the ceiling 3 is provably reachable and the
      greedy is checked to reach it;
  [6] negative control: a cap-VIOLATING family (all completions of one top
      core) breaks the conclusion for the claimed L -- the hypothesis is
      load-bearing and the link scanner detects the leak;
  [7] Corollary G2 (mixed restrictions / junta cells): exhaustive on
      J(9,4) greedy families over all zero-sets |Z| <= 2 and cores
      r <= 2: density on {T : R subset T, T cap Z = empty} is
      <= L/(n-|Z|-j+1);
  [8] interface arithmetic: n-j+1 == A+1 on the five pinned qx14 rows and
      the resulting log2 eps = log2(L_tan/(A+1)) for L_tan in {1,2}.

Deterministic: fixed seed base SEED = 20260703.
Run: python3 experimental/scripts/verify_qx11_topcore_globalness.py
Exit 0 iff every check PASSes.
"""
from __future__ import annotations

import json
import os
import random
import sys
from fractions import Fraction
from itertools import combinations
from math import comb, log2

SEED = 20260703
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CERT = os.path.join(
    REPO,
    "experimental",
    "data",
    "certificates",
    "qx11-topcore-globalness",
    "qx11_topcore_globalness.json",
)

_results: list[bool] = []


def check(name: str, ok: bool, detail: str = "") -> bool:
    _results.append(bool(ok))
    line = f"[{'PASS' if ok else 'FAIL'}] {name}"
    if detail:
        line += f"  |  {detail}"
    print(line)
    return ok


# ------------------------------------------------------------- utilities
def cores_of(T: frozenset) -> list[frozenset]:
    """All (j-1)-subsets of T (deletion of one element)."""
    return [T - {y} for y in T]


def core_counts(A: list[frozenset]) -> dict[frozenset, int]:
    """c_A(H) = #completions of H inside A, for every H hit by A."""
    c: dict[frozenset, int] = {}
    for T in A:
        for H in cores_of(T):
            c[H] = c.get(H, 0) + 1
    return c


def realized_cap(A: list[frozenset]) -> int:
    c = core_counts(A)
    return max(c.values()) if c else 0


def link_scan(n: int, j: int, A: list[frozenset], L: int):
    """Check |A_R| * (n-j+1) <= L * C(n-r, j-r) for ALL r <= j-1, all R.

    Returns (ok, worst_ratio, worst_R, n_checks); ratio is exact Fraction
    of LHS density to the bound L/(n-j+1) (<= 1 iff the theorem holds).
    """
    ok = True
    worst = Fraction(0)
    worst_R: tuple = ()
    n_checks = 0
    for r in range(j):
        denom = comb(n - r, j - r)
        for R in combinations(range(n), r):
            Rs = frozenset(R)
            cnt = sum(1 for T in A if Rs <= T)
            n_checks += 1
            if cnt * (n - j + 1) > L * denom:
                ok = False
            ratio = Fraction(cnt * (n - j + 1), L * denom)
            if ratio > worst:
                worst, worst_R = ratio, R
    return ok, worst, worst_R, n_checks


def greedy_family(n: int, j: int, L: int, seed: int,
                  prefer: tuple = ()) -> list[frozenset]:
    """Greedy cap-respecting family: scan all j-sets in seeded random order
    (sets containing `prefer` first, for the adversarial variant), insert T
    iff all j of its top cores still have < L completions."""
    rng = random.Random(seed)
    all_T = [frozenset(c) for c in combinations(range(n), j)]
    if prefer:
        P = frozenset(prefer)
        inside = [T for T in all_T if P <= T]
        outside = [T for T in all_T if not P <= T]
        rng.shuffle(inside)
        rng.shuffle(outside)
        order = inside + outside
    else:
        order = all_T[:]
        rng.shuffle(order)
    cnt: dict[frozenset, int] = {}
    A: list[frozenset] = []
    for T in order:
        cs = cores_of(T)
        if all(cnt.get(H, 0) < L for H in cs):
            A.append(T)
            for H in cs:
                cnt[H] = cnt.get(H, 0) + 1
    return A


# --------------------------------------------------------------- part [1]
def part1_ratio_identity(n_max: int = 40) -> None:
    total = 0
    bad = 0
    for n in range(1, n_max + 1):
        for j in range(1, n + 1):
            for r in range(0, j):
                total += 1
                if (n - j + 1) * comb(n - r, j - 1 - r) != \
                        (j - r) * comb(n - r, j - r):
                    bad += 1
    check(f"[1] cancellation identity (n-j+1)C(n-r,j-1-r)==(j-r)C(n-r,j-r), "
          f"all n<={n_max}", bad == 0, f"{total} triples, {bad} failures")


# --------------------------------------------------------------- part [2]
def part2_double_count(n: int = 9, j: int = 4, n_fams: int = 5) -> None:
    all_T = [frozenset(c) for c in combinations(range(n), j)]
    total = 0
    bad = 0
    for f in range(n_fams):
        rng = random.Random(SEED + f)
        A = [T for T in all_T if rng.random() < 0.5]
        c = core_counts(A)
        for r in range(j):          # r = 0..j-1
            for R in combinations(range(n), r):
                Rs = frozenset(R)
                A_R = [T for T in A if Rs <= T]
                # direct pair enumeration (T, H), R <= H < T, |H| = j-1
                pairs = 0
                row_ok = True
                for T in A_R:
                    hs = [H for H in cores_of(T) if Rs <= H]
                    if len(hs) != j - r:
                        row_ok = False
                    pairs += len(hs)
                col = sum(c.get(frozenset(R) | frozenset(E), 0)
                          for E in combinations(sorted(set(range(n)) - Rs),
                                                j - 1 - r))
                total += 1
                if not (row_ok and pairs == (j - r) * len(A_R)
                        and pairs == col):
                    bad += 1
    check(f"[2] double-count skeleton on J({n},{j}): pairs == (j-r)|A_R| == "
          f"sum_H c_A(H), all r-cores, {n_fams} seeded families",
          bad == 0, f"{total} (family,R) cells, {bad} failures")


# --------------------------------------------------------------- part [3]
def part3_greedy_theorem() -> None:
    for (n, j), Ls in (((9, 4), (1, 2)), ((10, 5), (1, 2, 3))):
        for L in Ls:
            for s in range(3):
                A = greedy_family(n, j, L, SEED + 10 * L + s)
                cap = realized_cap(A)
                ok, worst, worst_R, nc = link_scan(n, j, A, L)
                check(f"[3] G1 on greedy J({n},{j}) L={L} seed#{s}: "
                      f"cap holds and ALL {nc} r-core links bounded",
                      cap <= L and ok,
                      f"|A|={len(A)}, realized cap={cap}, worst density/bound"
                      f"={float(worst):.4f} at R={worst_R}")


# --------------------------------------------------------------- part [4]
def steiner_check(n: int, j: int, blocks: list[frozenset]) -> bool:
    """Every (j-1)-subset of [n] lies in exactly one block."""
    c: dict[frozenset, int] = {}
    for T in blocks:
        for H in cores_of(T):
            c[H] = c.get(H, 0) + 1
    return (len(c) == comb(n, j - 1)
            and all(v == 1 for v in c.values()))


def equality_scan(n: int, j: int, A: list[frozenset], L: int):
    """Check EXACT equality cnt*(n-j+1) == L*C(n-r,j-r) at every r-core."""
    all_eq = True
    n_checks = 0
    for r in range(j):
        denom = comb(n - r, j - r)
        for R in combinations(range(n), r):
            Rs = frozenset(R)
            cnt = sum(1 for T in A if Rs <= T)
            n_checks += 1
            if cnt * (n - j + 1) != L * denom:
                all_eq = False
    return all_eq, n_checks


def part4_tightness() -> None:
    # Fano plane S(2,3,7): the 7 lines (0-indexed standard model).
    fano = [frozenset(b) for b in
            ((0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5),
             (1, 4, 6), (2, 3, 6), (2, 4, 5))]
    st = steiner_check(7, 3, fano)
    check("[4] Fano S(2,3,7) is Steiner (every 2-set: exactly 1 completion)",
          st, f"blocks={len(fano)}, C(7,2)={comb(7, 2)}")
    eq, nc = equality_scan(7, 3, fano, 1)
    check("[4] Fano meets G1 with EXACT equality at every r-core "
          "(density == 1/(n-j+1) = 1/5)", eq, f"{nc} cores checked")

    # SQS(8) by doubling: {B u {7}} u {complement of B in {0..6}}.
    sqs = [B | {7} for B in fano] + \
          [frozenset(range(7)) - B for B in fano]
    st = steiner_check(8, 4, sqs)
    check("[4] doubled SQS(8) is Steiner (every 3-set: exactly 1 completion)",
          st, f"blocks={len(sqs)}, C(8,3)={comb(8, 3)}")
    eq, nc = equality_scan(8, 4, sqs, 1)
    check("[4] SQS(8) meets G1 with EXACT equality at every r-core "
          "(density == 1/5)", eq, f"{nc} cores checked")

    # trivial witness: the full family at L = n-j+1 (density 1 everywhere).
    n, j = 9, 4
    full = [frozenset(c) for c in combinations(range(n), j)]
    eq, nc = equality_scan(n, j, full, n - j + 1)
    check(f"[4] full J({n},{j}) at L=n-j+1={n - j + 1}: equality (density 1) "
          "at every r-core", eq, f"{nc} cores checked")


# --------------------------------------------------------------- part [5]
def part5_adversarial() -> None:
    cases = [(9, 4, (0,), 1), (9, 4, (0, 1), 1), (9, 4, (0, 1), 2),
             (10, 5, (0,), 1), (10, 5, (0, 1), 1), (10, 5, (0, 1), 2)]
    reach3 = 0
    for (n, j, R, L) in cases:
        r = len(R)
        bound_int = (L * comb(n - r, j - 1 - r)) // (j - r)
        best = -1
        all_ok = True
        for s in range(3):
            A = greedy_family(n, j, L, SEED + s, prefer=R)
            cap = realized_cap(A)
            ok, worst, _, _ = link_scan(n, j, A, L)
            all_ok = all_ok and ok and (cap <= L)
            Rs = frozenset(R)
            best = max(best, sum(1 for T in A if Rs <= T))
        check(f"[5] adversarial J({n},{j}) target R={R} L={L}: bound never "
              f"exceeded; achieved |A_R|={best} of integer ceiling "
              f"{bound_int}", all_ok and best <= bound_int,
              f"achieved/ceiling = {best}/{bound_int}")
        if (n, j, r, L) == (9, 4, 2, 1):
            reach3 = best
    check("[5] tightness direction: J(9,4), r=2, L=1 adversarial packing "
          "REACHES the integer ceiling 3", reach3 == 3,
          f"achieved {reach3} == 3 (provably attainable: three disjoint "
          "completions of R)")


# --------------------------------------------------------------- part [6]
def part6_negative_control() -> None:
    n, j = 9, 4
    H0 = frozenset({0, 1, 2})
    A = [H0 | {x} for x in range(n) if x not in H0]
    cap = realized_cap(A)
    ok, worst, worst_R, _ = link_scan(n, j, A, 1)
    check("[6] negative control: cap-violating family (all 6 completions "
          "of one top core) BREAKS the L=1 link bound and is detected",
          cap == 6 and not ok,
          f"realized cap={cap}, worst density/bound={float(worst):.2f} "
          f"at R={worst_R}")


# --------------------------------------------------------------- part [7]
def part7_mixed_restrictions() -> None:
    n, j = 9, 4
    for L in (1, 2):
        A = greedy_family(n, j, L, SEED + 100 + L)
        total = 0
        bad = 0
        for z in (1, 2):
            npr = n - z
            for Z in combinations(range(n), z):
                Zs = frozenset(Z)
                rest = sorted(set(range(n)) - Zs)
                for r in range(0, 3):
                    denom = comb(npr - r, j - r)
                    for R in combinations(rest, r):
                        Rs = frozenset(R)
                        cnt = sum(1 for T in A
                                  if Rs <= T and not (T & Zs))
                        total += 1
                        if cnt * (npr - j + 1) > L * denom:
                            bad += 1
        check(f"[7] Corollary G2 on greedy J({n},{j}) L={L}: mixed "
              f"restrictions (|Z|<=2, r<=2) all bounded by L/(n-|Z|-j+1)",
              bad == 0, f"{total} (Z,R) cells, {bad} failures")


# --------------------------------------------------------------- part [8]
def part8_interface_rows() -> None:
    # pinned rows from qx14_xr_coverage_table.md SS4 (corridor-edge t* rows
    # plus the exact pinned row (a) t*=5); (n, A, j) transcribed as printed.
    rows = [("(a) n=512 t*=5", 512, 261, 251),
            ("(c) rate 1/2 t*", 2 ** 41, 1108104540515, 1090918715037),
            ("(c) rate 1/4 t*", 2 ** 41, 556770474278, 1642252781274),
            ("(c) rate 1/8 t*", 2 ** 41, 279600463336, 1919422792216),
            ("(c) rate 1/16 t*", 2 ** 41, 140382131272, 2058641124280)]
    for (name, n, A, j) in rows:
        ok = (A + j == n) and (n - j + 1 == A + 1)
        e1 = -log2(A + 1)
        check(f"[8] {name}: A+j==n and n-j+1==A+1; "
              f"log2 eps = {e1:.2f} (L_tan=1) / {e1 + 1:.2f} (L_tan=2)",
              ok, f"A={A}, j={j}, n-j+1={A + 1}")


def main() -> None:
    write = "--write-certificate" in sys.argv
    print("verify_qx11_topcore_globalness: top-core cap => globalness "
          "(xr_globalness_from_ledger, QX.11)")
    print(f"deterministic seed base = {SEED}")
    part1_ratio_identity()
    part2_double_count()
    part3_greedy_theorem()
    part4_tightness()
    part5_adversarial()
    part6_negative_control()
    part7_mixed_restrictions()
    part8_interface_rows()
    n_pass = sum(_results)
    n_all = len(_results)
    result = {
        "task": "QX.11 top-core globalness",
        "node": "xr_globalness_from_ledger",
        "status": "PROVED mathematics / AUDIT for L_tan convention / INPUT for actual cap hypothesis",
        "claim": (
            "A uniform top-core completion cap L implies every r-core link "
            "has density at most L/(n-j+1), with mixed-restriction and "
            "leak-localization corollaries."
        ),
        "seed": SEED,
        "checks": n_all,
        "passes": n_pass,
        "failures": n_all - n_pass,
    }
    if write:
        os.makedirs(os.path.dirname(CERT), exist_ok=True)
        with open(CERT, "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=2, sort_keys=True)
            fh.write("\n")
        print(f"[write] {CERT}")

    expected = None
    if os.path.exists(CERT):
        with open(CERT, encoding="utf-8") as fh:
            expected = json.load(fh)
    check("[certificate] certificate exists", expected is not None, CERT)
    if expected is not None:
        check("[certificate] certificate matches recomputed summary", result == expected)
    n_pass = sum(_results)
    n_all = len(_results)
    print(f"\n{'ALL CHECKS PASS' if all(_results) else 'FAILURES PRESENT'} "
          f"({n_pass}/{n_all})")
    sys.exit(0 if all(_results) else 1)


if __name__ == "__main__":
    main()
