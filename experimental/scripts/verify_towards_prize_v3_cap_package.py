#!/usr/bin/env python3
"""Audit constants in the towards-prize v3 cap-paper package.

This verifier checks the compact row-determination constants imported into
``tex/towards-prize.tex`` from Paper D v12:

* the deployed self-contained and imported interval endpoints;
* the KoalaBear half-Johnson certificate arithmetic;
* the rate comparison saying half-Johnson improves the self-contained edge
  exactly below rate 1/4.
"""

from __future__ import annotations

from decimal import Decimal, getcontext
from fractions import Fraction


getcontext().prec = 80


def check_deployed_interval_endpoints() -> list[str]:
    """Check the exact intervals printed in towards-prize v3."""

    n = 2**21
    k = 2**20
    deep_safe = (n - k) // 3
    imported_safe = (n - k) // 2

    if deep_safe != 349_525:
        raise AssertionError(("deep safe", deep_safe))
    if Fraction(imported_safe, n) != Fraction(1, 4):
        raise AssertionError(("import safe", imported_safe))

    kb_unsafe_agreement = 16 * 69_748
    kb_upper = 1 - Fraction(kb_unsafe_agreement, n)
    if kb_upper != Fraction(15_331, 32_768):
        raise AssertionError(("KB upper", kb_upper))

    circle_unsafe_agreement = 32 * 34_873
    circle_upper = 1 - Fraction(circle_unsafe_agreement, n)
    if circle_upper != Fraction(30_663, 65_536):
        raise AssertionError(("circle upper", circle_upper))

    return [
        "self-contained safe edge floor((n-k)/3)=349525",
        "imported half-distance safe edge floor((n-k)/2)/n=1/4",
        "KoalaBear widened unsafe edge 1-16*69748/2^21=15331/32768",
        "circle widened unsafe edge 1-32*34873/2^21=30663/65536",
    ]


def check_deployed_safe_error_gates() -> list[str]:
    """Check that the printed safe endpoints clear their targets."""

    n = 2**21
    k = 2**20
    deep_safe = (n - k) // 3
    imported_safe = (n - k) // 2

    kb_p = 2**31 - 2**24 + 1
    kb_q = kb_p**6
    if not (deep_safe + 1) * 2**128 <= kb_q:
        raise AssertionError(("KB deep target", deep_safe, kb_q))
    if not n * 2**128 <= kb_q:
        raise AssertionError(("KB import target", n, kb_q))

    circle_p = 2**31 - 1
    circle_q = circle_p**4
    if not (deep_safe + 1) * 2**100 <= circle_q:
        raise AssertionError(("circle deep target", deep_safe, circle_q))
    if not n * 2**100 <= circle_q:
        raise AssertionError(("circle import target", n, circle_q))

    if 3 * deep_safe > n - k:
        raise AssertionError(("deep radius", deep_safe))
    if 2 * imported_safe > n - k:
        raise AssertionError(("import radius", imported_safe))

    return [
        "KoalaBear deep safe numerator clears 2^-128",
        "KoalaBear imported n/q safe numerator clears 2^-128",
        "circle deep safe numerator clears 2^-100",
        "circle imported n/q safe numerator clears 2^-100",
    ]


def check_koalabear_half_johnson_certificate() -> list[str]:
    """Check the standalone KoalaBear half-Johnson row from Paper D v12."""

    n = 2**21
    k = 2**20
    r = 307_121
    l2_bound = 1_001_282
    p = 2**31 - 2**24 + 1
    q = p**6

    a = n - 2 * r
    gap = a * a - (k - 1) * n
    numerator = n * (a - k + 1)
    if gap != 909_700:
        raise AssertionError(("gap", gap))
    if numerator // gap > l2_bound:
        raise AssertionError(("L2 floor", numerator, gap, l2_bound))
    if not (l2_bound + 1) * gap > numerator:
        raise AssertionError(("L2 certificate", numerator, gap, l2_bound))
    if not (1 + (r + 1) * l2_bound) * 2**147 < q:
        raise AssertionError(("HJ target", r, l2_bound, q))

    deep_safe = (n - k) // 3
    if not r < deep_safe:
        raise AssertionError(("HJ dominance", r, deep_safe))

    return [
        "KoalaBear HJ gap is 909700 at r=307121",
        "integer L2=1001282 upper-bounds the rational Johnson list term",
        "HJ error numerator clears 2^-147",
        "for rho=1/2 this HJ endpoint is dominated by the deep safe edge",
    ]


def half_johnson_edge(rho: Fraction) -> Decimal:
    return (Decimal(1) - (Decimal(rho.numerator) / Decimal(rho.denominator)).sqrt()) / 2


def deep_edge(rho: Fraction) -> Fraction:
    return Fraction(1, 1) - rho


def check_rate_comparison() -> list[str]:
    """Check the half-Johnson-vs-deep comparison at challenge rates."""

    rates = [
        (Fraction(1, 2), False),
        (Fraction(1, 4), False),
        (Fraction(1, 8), True),
        (Fraction(1, 16), True),
    ]
    details = []
    for rho, expected_improves in rates:
        # For 0<rho<1, (1-sqrt(rho))/2 > (1-rho)/3 iff rho<1/4.
        improves = rho < Fraction(1, 4)
        if improves != expected_improves:
            raise AssertionError(("comparison", rho, improves))

        hj = half_johnson_edge(rho)
        deep = Decimal(deep_edge(rho).numerator) / Decimal(3 * deep_edge(rho).denominator)
        if expected_improves and not hj > deep:
            raise AssertionError(("expected HJ improvement", rho, hj, deep))
        if not expected_improves and hj > deep:
            raise AssertionError(("unexpected HJ improvement", rho, hj, deep))
        details.append(f"rho={rho}: half-Johnson={hj:.6f}, deep={deep:.6f}")

    return details + ["improvement occurs exactly for rho<1/4 on challenge rates"]


def main() -> None:
    checks = [
        ("deployed interval endpoints", check_deployed_interval_endpoints),
        ("deployed safe error gates", check_deployed_safe_error_gates),
        ("KoalaBear half-Johnson certificate", check_koalabear_half_johnson_certificate),
        ("rate comparison", check_rate_comparison),
    ]
    print("=" * 74)
    print("AUDIT: towards-prize v3 cap-paper package constants")
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
