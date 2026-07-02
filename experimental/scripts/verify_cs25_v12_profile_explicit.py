#!/usr/bin/env python3
"""Audit Paper D v12 profile and explicit-pair constants.

This verifier checks three scoped pieces from ``tex/cs25_cap_v12.tex`` and
``tex/towards-prize.tex``:

* the algebra behind the optimized profile factor kappa/(kappa+1);
* the explicit head-and-pairs deployed list inequalities;
* the simple-pole explicit-pair majority-pole density constants.

The explicit-pair check records one audit finding: the displayed rational
Cauchy lower-bound chain is just below ``ceil((q-n)/(3k))`` in the deployed
rows, but integrality of the slope count recovers the printed integer
conclusion and the density exponents.
"""

from __future__ import annotations

from fractions import Fraction
from math import comb


KOALA = 2**31 - 2**24 + 1
M31 = 2**31 - 1


def ceil_div(a: int, b: int) -> int:
    return -(-a // b)


def check_profile_algebra() -> list[str]:
    """Check the rational rearrangement in prop:profile on a finite grid."""

    cases = 0
    for q in range(11, 80):
        for n in range(1, q):
            for k in range(1, n + 1):
                t = Fraction(q - n, k * q)
                for kappa in [Fraction(1, 4), Fraction(1), Fraction(3), Fraction(17, 2)]:
                    threshold = kappa / (kappa + 1) * t
                    certified = threshold
                    # At x=threshold the conversion ceiling expression is
                    # exactly kappa*q*T = kappa*(q-n)/k.
                    ceiling_expr = Fraction(q) * certified / (1 - certified / t)
                    expected = kappa * Fraction(q - n, k)
                    cases += 1
                    if ceiling_expr != expected:
                        raise AssertionError(("profile equality", q, n, k, kappa))
                    if not threshold < t:
                        raise AssertionError(("ceiling", q, n, k, kappa))

    return [
        f"checked {cases} exact rational profile cases",
        "x=(kappa/(kappa+1))*T gives q*x/(1-x/T)=kappa*q*T",
        "the certified profile remains strictly below T for every finite kappa",
    ]


def check_deployed_profile_certificates() -> list[str]:
    """Check deployed kappa values and profile factors."""

    rows = [
        ("KoalaBear", KOALA, KOALA**6, 2**21, 2**20, 54),
        ("circle line-round", M31, M31**4, 2**21, 2**20, 116),
    ]
    details = []
    for label, p, q, n, k, kappa_power in rows:
        list_floor = ceil_div(comb(256, 130), p)
        kappa = 2**kappa_power
        if (list_floor - 1) * k < kappa * (q - n):
            raise AssertionError((label, "kappa floor"))
        if list_floor * k <= k + kappa * (q - n):
            raise AssertionError((label, "strict 1+kappa qT"))
        # kappa/(kappa+1) >= 1 - 2^-s for kappa=2^s.
        if Fraction(kappa, kappa + 1) < 1 - Fraction(1, 2**kappa_power):
            raise AssertionError((label, "profile factor"))
        details.append(
            f"{label}: floor((L-1)k/(q-n)) >= 2^{kappa_power} and factor >= 1-2^-{kappa_power}"
        )
    return details


def check_explicit_head_deployed_floors() -> list[str]:
    """Check cor:explicit-deployed list-size and threshold arithmetic."""

    n = 2**21
    k = 2**20

    # MCA explicit head at gap 2^-8.
    c_mca = 2**12
    n_over_c_mca = n // c_mca
    m_mca = k // c_mca + 2
    count_mca = comb(n_over_c_mca // 2, m_mca // 2)
    if (c_mca * m_mca, m_mca, n_over_c_mca) != (k + 2**13, 258, 512):
        raise AssertionError("MCA explicit-head parameters")
    if count_mca < 2**251:
        raise AssertionError("binom(256,129) should be at least 2^251")
    if not count_mca * k > KOALA**6 + k:
        raise AssertionError("KoalaBear explicit MCA threshold")
    if not count_mca * k > M31**4 + k:
        raise AssertionError("circle explicit MCA threshold")

    # List explicit head at gap 2^-7.
    c_list = 2**14
    n_over_c_list = n // c_list
    m_list = k // c_list + 1
    count_list = comb(n_over_c_list // 2 - 1, (m_list - 1) // 2)
    if (c_list * m_list, m_list, n_over_c_list) != (k + 2**14, 65, 128):
        raise AssertionError("list explicit-head parameters")
    if count_list != 916_312_070_471_295_267:
        raise AssertionError(("binom(63,32)", count_list))
    if count_list < 2**59:
        raise AssertionError("binom(63,32) should exceed 2^59")
    if not count_list * 2**128 > KOALA**6:
        raise AssertionError("KoalaBear explicit list target")
    if not count_list * 2**100 > M31**4:
        raise AssertionError("circle explicit list target")

    return [
        "MCA explicit head: c=2^12, m=258, agreement=k+2^13, count=binom(256,129)>=2^251",
        "MCA explicit thresholds: count exceeds q/k+1 for KoalaBear and circle rows",
        "list explicit head: c=2^14, m=65, agreement=k+2^14, count=binom(63,32)",
        "list explicit thresholds: count exceeds 2^-128*q and 2^-100*q respectively",
    ]


def check_simple_pole_majority(row: dict[str, int]) -> list[str]:
    q = row["q"]
    n = row["n"]
    k = row["k"]
    count = row["count"]
    target_power = row["target_power"]

    omega = q - n
    l0 = ceil_div(omega, k)
    if l0 > count:
        raise AssertionError((row["label"], "not enough explicit codewords"))

    x_star = ceil_div(2 * k * l0 * (l0 - 1), 2 * omega)
    lower = Fraction(l0 * l0, l0 + 2 * (x_star - 1))
    printed_claim = ceil_div(omega, 3 * k)
    ceil_lower = ceil_div(lower.numerator, lower.denominator)
    floor_safe = omega // (3 * k)
    if lower >= printed_claim:
        raise AssertionError((row["label"], "expected deployed ceil-bound audit finding vanished"))
    if ceil_lower < printed_claim:
        raise AssertionError((row["label"], "integerized Cauchy lower bound", ceil_lower, printed_claim))
    if lower < floor_safe:
        raise AssertionError((row["label"], "floor-safe Cauchy lower bound", lower, floor_safe))
    if lower * 2**target_power <= q:
        raise AssertionError((row["label"], "density target", lower, target_power))
    if lower * 2**22 <= q:
        raise AssertionError((row["label"], "2^-21.6 proxy target"))
    if lower**5 * 2**108 <= q**5:
        raise AssertionError((row["label"], "exact 2^-21.6 target", lower))

    # At most |B| poles lie in the base field; this is negligible compared with
    # the majority set and records the genuinely extension-valued scope.
    if row["base"] >= omega // 2:
        raise AssertionError((row["label"], "base-pole count not negligible"))

    density_summary = "exact Cauchy density clears 2^-21.6 and 2^-22"
    if target_power != 22:
        density_summary += f" (hence also 2^-{target_power})"

    return [
        f"{row['label']}: L0=ceil((q-n)/k) <= binom(256,129)",
        f"{row['label']}: AUDIT FINDING displayed rational bound is just below ceil((q-n)/(3k))",
        f"{row['label']}: integrality gives the printed integer count ceil((q-n)/(3k))",
        f"{row['label']}: {density_summary}",
        f"{row['label']}: at most |B|={row['base']} base-field poles among Omega",
    ]


def check_explicit_pair_majority_constants() -> list[str]:
    """Check thm:explicit-pairs constants for KoalaBear and circle line rounds."""

    count = comb(256, 129)
    rows = [
        {
            "label": "KoalaBear",
            "base": KOALA,
            "q": KOALA**6,
            "n": 2**21,
            "k": 2**20,
            "count": count,
            "target_power": 22,
        },
        {
            "label": "circle line-round",
            "base": M31,
            "q": M31**4,
            "n": 2**21,
            "k": 2**20,
            "count": count,
            "target_power": 23,
        },
    ]
    details: list[str] = []
    for row in rows:
        details.extend(check_simple_pole_majority(row))
    return details


def main() -> None:
    checks = [
        ("profile algebra", check_profile_algebra),
        ("deployed profile certificates", check_deployed_profile_certificates),
        ("explicit head deployed floors", check_explicit_head_deployed_floors),
        ("explicit-pair majority constants", check_explicit_pair_majority_constants),
    ]
    print("=" * 74)
    print("AUDIT: Paper D v12 profile and explicit-pair constants")
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
