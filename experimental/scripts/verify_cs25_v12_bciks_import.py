#!/usr/bin/env python3
"""Audit the BCIKS half-distance import normalization used by Paper D v12.

The external theorem is not reproved here.  This verifier checks the exact
integer consequences used locally once the imported unique-decoding correlated
agreement statement is read as:

    more than n close slopes force a common explanation.

In the repo's density normalization this is ``eca(C, delta) <= n/q``.
"""

from __future__ import annotations

from fractions import Fraction


TARGET = 2**128


def check_density_translation(limit: int = 80) -> list[str]:
    """Check the conversion from an n-slope bound to eca <= n/q."""

    cases = 0
    for q in range(2, limit + 1):
        for n in range(1, q + 1):
            for close_slopes in range(0, q + 1):
                cases += 1
                theorem_allows_far_pair = close_slopes <= n
                density_at_most_n_over_q = Fraction(close_slopes, q) <= Fraction(
                    n, q
                )
                if theorem_allows_far_pair != density_at_most_n_over_q:
                    raise AssertionError(
                        ("density", q, n, close_slopes, theorem_allows_far_pair)
                    )
    return [
        f"checked {cases} slope-count density cases",
        "BCIKS threshold |A|>n gives eca(C,delta)<=n/q in repo density units",
    ]


def check_rate_and_radius_translation(limit: int = 140) -> list[str]:
    """Check degree/rate and floor-radius translations for RS[F,D,k]."""

    cases = 0
    floor_cases = 0
    for n in range(2, limit + 1):
        for k in range(1, n):
            # BCIKS writes degree <= d and rate (d+1)/n.  Repo RS[F,D,k]
            # has degree < k, so d=k-1 and rho=k/n.
            d = k - 1
            if Fraction(d + 1, n) != Fraction(k, n):
                raise AssertionError(("rate", n, k, d))

            for r in range(0, n + 1):
                cases += 1
                rs_half_distance = 2 * r <= n - k
                min_weight_half_distance = 2 * r <= (n - k + 1) - 1
                if rs_half_distance != min_weight_half_distance:
                    raise AssertionError(("min-weight", n, k, r))

            # If delta <= (n-k)/(2n), then floor(delta*n)=f implies
            # f/n <= delta <= (n-k)/(2n), hence 2f <= n-k.  Check the
            # integer floor values exactly.
            for f in range(0, n + 1):
                if Fraction(f, n) <= Fraction(n - k, 2 * n):
                    floor_cases += 1
                    if 2 * f > n - k:
                        raise AssertionError(("floor-radius", n, k, f))
    return [
        f"checked {cases} integer radius cases and {floor_cases} floor values",
        "BCIKS degree bound d=k-1 has rate (d+1)/n=k/n",
        "delta<=(n-k)/(2n) implies 2*floor(delta*n)<=n-k",
    ]


def check_mca_transfer_bound(limit: int = 140) -> list[str]:
    """Check the local mutual-from-correlated maximum under the import."""

    cases = 0
    for n in range(2, limit + 1):
        for k in range(1, n):
            for r in range(0, n + 1):
                if 2 * r <= n - k:
                    cases += 1
                    # Under the import, the CA numerator is n.  The tangent
                    # numerator from mca-from-ca is r, so the local MCA
                    # numerator is max(n,r)=n.
                    if max(n, r) != n:
                        raise AssertionError(("max", n, k, r))
    return [
        f"checked {cases} half-distance transfer cases",
        "max(n/q, r/q)=n/q throughout the RS half-distance range",
    ]


def check_general_target_gate() -> list[str]:
    """Check the printed q>=2^128*n target implication."""

    cases = 0
    for n in [1, 2, 3, 7, 2**12, 2**21, 2**40, 16 * 2**40]:
        for extra in [0, 1, n, 2**64]:
            q = TARGET * n + extra
            cases += 1
            if n * TARGET > q:
                raise AssertionError(("target", n, q))
    return [
        f"checked {cases} q>=2^128*n target cases",
        "q>=2^128*n implies n/q<=2^-128 by exact cross multiplication",
    ]


def check_deployed_ch_rows() -> list[str]:
    """Check the two printed imported half-distance deployed rows."""

    n = 2**21
    k = 2**20
    r = 2**19
    if 2 * r != n - k:
        raise AssertionError(("endpoint", n, k, r))
    if Fraction(r, n) != Fraction(1, 4):
        raise AssertionError(("delta endpoint", r, n))

    kb_p = 2**31 - 2**24 + 1
    kb_q = kb_p**6
    if not n * 2**164 < kb_q:
        raise AssertionError(("KB 2^-164", n, kb_q))
    if not n * TARGET < kb_q:
        raise AssertionError(("KB 2^-128", n, kb_q))

    circle_p = 2**31 - 1
    circle_q = circle_p**4
    if not n * 2**102 < circle_q:
        raise AssertionError(("circle 2^-102", n, circle_q))
    if not n * 2**100 < circle_q:
        raise AssertionError(("circle 2^-100", n, circle_q))

    return [
        "checked n=2^21, k=2^20, r=2^19 half-distance endpoint",
        "KoalaBear sextic: n/q < 2^-164 < 2^-128",
        "circle line-round: n/q < 2^-102 < 2^-100",
    ]


def main() -> None:
    checks = [
        ("density translation", check_density_translation),
        ("rate and radius translation", check_rate_and_radius_translation),
        ("MCA transfer bound", check_mca_transfer_bound),
        ("general target gate", check_general_target_gate),
        ("deployed CH rows", check_deployed_ch_rows),
    ]
    print("=" * 74)
    print("AUDIT: Paper D v12 BCIKS half-distance import normalization")
    print("=" * 74)
    failed = 0
    for title, fn in checks:
        try:
            details = fn()
        except AssertionError as exc:
            failed += 1
            print(f"\n[FAIL] {title}")
            print(f"       {exc}")
            continue
        print(f"\n[PASS] {title}")
        for line in details:
            print(f"       {line}")
    print("\n" + "-" * 74)
    print(f"implemented PASS: {len(checks) - failed}   FAIL: {failed}")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
