#!/usr/bin/env python3
"""Audit the integer-radius and algebra gates in Paper D v12's conversion.

This verifier is deliberately small and exact.  It checks the off-by-one
radius equivalences used by ``tex/cs25_cap_v12.tex`` Theorem A and exercises
the rational algebra that turns the simple-pole collision lower bound into the
printed list-size ceiling.
"""

from __future__ import annotations

from fractions import Fraction


def check_integer_radius_equivalences(limit: int = 80) -> list[str]:
    """Check the discrete radius convention on all small (n,k,f)."""

    triples = 0
    for n in range(2, limit + 1):
        for k in range(1, n):
            for f in range(0, n):
                triples += 1
                admissible = f <= n - k - 1
                agreement_at_least_k_plus_one = n - f >= k + 1
                if admissible != agreement_at_least_k_plus_one:
                    raise AssertionError(
                        ("agreement equivalence", n, k, f, admissible)
                    )

                # Some radius with floor(delta*n)=f lies below capacity
                # delta < 1-k/n iff the interval [f/n,(f+1)/n) starts below
                # (n-k)/n, i.e. f < n-k.
                occurs_below_capacity = f < n - k
                if occurs_below_capacity != admissible:
                    raise AssertionError(
                        ("capacity equivalence", n, k, f, admissible)
                    )
    return [
        f"checked {triples} triples (n,k,f) with n<= {limit}",
        "f<=n-k-1 iff n-f>=k+1",
        "floor(delta*n)=f can occur below 1-k/n iff f<=n-k-1",
    ]


def check_conversion_ceiling_algebra() -> list[str]:
    """Check the exact rational implication behind Theorem A.

    The proof obtains

        eps >= L(q-n)/(q(q-n+kL)).

    Under eps <= eta(q-n)/(kq), eta<1, it concludes

        L <= q eps/(1-eta).

    We exercise this implication over a finite grid of exact rational values,
    including several eta values.  This is an audit of the algebraic
    rearrangement and denominator sign, not a finite-field enumeration.
    """

    cases = 0
    etas = [Fraction(0), Fraction(1, 3), Fraction(1, 2), Fraction(7, 10)]
    for q in range(5, 36):
        for n in range(1, q):
            for k in range(1, n + 1):
                threshold = Fraction(q - n, k * q)
                for list_size in range(1, 80):
                    lower = Fraction(
                        list_size * (q - n),
                        q * (q - n + k * list_size),
                    )
                    cases += 1
                    if lower >= threshold:
                        raise AssertionError(
                            ("ceiling strictness", q, n, k, list_size)
                        )
                    for eta in etas:
                        if lower <= eta * threshold:
                            bound = Fraction(q) * lower / (1 - eta)
                            if Fraction(list_size) > bound:
                                raise AssertionError(
                                    (
                                        "conversion ceiling",
                                        q,
                                        n,
                                        k,
                                        list_size,
                                        eta,
                                    )
                                )
    return [
        f"checked {cases} exact rational lower-bound cases",
        "L(q-n)/(q(q-n+kL)) is always below (q-n)/(kq)",
        "eps<=eta(q-n)/(kq) implies L<=q*eps/(1-eta) in the tested grid",
    ]


def check_trigger_equivalence() -> list[str]:
    """Check the trigger used in the quantitative deep-list floor."""

    cases = 0
    for q in range(5, 40):
        for n in range(1, q):
            for k in range(1, n + 1):
                for list_size in range(1, 96):
                    cases += 1
                    lhs = Fraction(
                        list_size * (q - n),
                        q * (q - n + k * list_size),
                    )
                    trigger = Fraction(1, 2 * k) * Fraction(q - n, q)
                    if (lhs > trigger) != (k * list_size > q - n):
                        raise AssertionError(
                            ("trigger", q, n, k, list_size, lhs, trigger)
                        )
    return [
        f"checked {cases} trigger cases",
        "E_{q,k}(L) > (1/(2k))(1-n/q) iff kL > q-n",
    ]


def main() -> None:
    checks = [
        ("integer-radius equivalences", check_integer_radius_equivalences),
        ("conversion ceiling algebra", check_conversion_ceiling_algebra),
        ("deep-list trigger equivalence", check_trigger_equivalence),
    ]
    print("=" * 74)
    print("AUDIT: Paper D v12 deep-point conversion radius/algebra gates")
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
