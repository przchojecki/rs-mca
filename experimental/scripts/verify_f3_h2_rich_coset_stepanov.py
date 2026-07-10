#!/usr/bin/env python3
"""Exact integer checks for the h=2 rich-coset Stepanov constants."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import isqrt


K_RICH = 129
ENERGY_CONSTANT = 1 + 5 * (K_RICH * K_RICH + K_RICH)


def floor_nth_root(n: int, k: int) -> int:
    if n < 0:
        raise ValueError(n)
    if n < 2:
        return n
    lo, hi = 1, 1
    while hi**k <= n:
        hi *= 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid**k <= n:
            lo = mid
        else:
            hi = mid
    return lo


def floor_scaled_cuberoot(num: int, den: int, scale: int) -> int:
    """Return floor((num/den)^(1/3) / scale), exactly."""

    if num <= 0 or den <= 0 or scale <= 0:
        raise ValueError((num, den, scale))
    lo, hi = 0, 1
    while (scale * hi) ** 3 * den <= num:
        hi *= 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if (scale * mid) ** 3 * den <= num:
            lo = mid
        else:
            hi = mid
    return lo


def min_p_for_h4t(h: int, t: int) -> int:
    """Smallest integer p satisfying p^3 > h^4 t."""

    value = h**4 * t
    p = floor_nth_root(value, 3)
    while p**3 <= value:
        p += 1
    return p


@dataclass(frozen=True)
class ParameterRow:
    h: int
    t: int
    branch: str
    a: int
    b: int
    d: int
    linear_slack: int
    nonvanishing_slack: int
    bound_ok: bool


def parameter_row(h: int, t: int) -> ParameterRow:
    if h < 1 or t < 1:
        raise ValueError((h, t))

    # X <= 1024 is equivalent to h^2 <= 1024^3 t.
    if h * h <= 1024**3 * t:
        # The proof uses |E| <= h <= 32(hT)^(2/3), and hence also K=129.
        bound_ok = h <= K_RICH**3 * t * t
        if not bound_ok:
            raise AssertionError((h, t, "trivial bound"))
        return ParameterRow(h, t, "trivial", 0, 0, 0, 0, 0, True)

    a = floor_scaled_cuberoot(h * h, t, 4)
    b = floor_scaled_cuberoot(h * t, 1, 2)
    d = floor_scaled_cuberoot(h * h, t, 64)
    if min(a, b, d) < 1:
        raise AssertionError((h, t, a, b, d))

    linear_slack = a * b * b - d * (a + d) * t
    if linear_slack <= 0:
        raise AssertionError((h, t, a, b, d, linear_slack))

    p_min = min_p_for_h4t(h, t)
    nonvanishing_slack = p_min - (a + h * b)
    if a * b > h or nonvanishing_slack <= 0:
        raise AssertionError((h, t, a, b, d, a * b, p_min, nonvanishing_slack))

    degree_num = a + 2 * h * b
    # Check ((A+2hB)/D)^3 <= K^3 (hT)^2 using integers.
    bound_ok = degree_num**3 <= (K_RICH**3) * (h * t) ** 2 * d**3
    if not bound_ok:
        raise AssertionError((h, t, a, b, d, degree_num))

    return ParameterRow(
        h=h,
        t=t,
        branch="stepanov",
        a=a,
        b=b,
        d=d,
        linear_slack=linear_slack,
        nonvanishing_slack=nonvanishing_slack,
        bound_ok=True,
    )


def selected_t_values(h: int) -> list[int]:
    values = {1, 2, 3, h, h * h}
    threshold = max(1, h * h // 1024**3)
    for delta in range(-3, 4):
        values.add(max(1, threshold + delta))
    root = isqrt(h)
    values.update({max(1, root - 1), root, root + 1})
    return sorted(values)


def main() -> None:
    rows: list[ParameterRow] = []
    for h in list(range(1, 513)) + [768, 1024, 1536, 2048, 4096, 8192, 16384, 65536, 10**6]:
        for t in selected_t_values(h):
            rows.append(parameter_row(h, t))

    # A deterministic large-X stress ladder, where the Stepanov branch is active.
    for x in (1025, 2048, 4096, 8192):
        h = x * x
        for t in (1, 2, 7, 31):
            rows.append(parameter_row(h, t))

    trivial = sum(1 for row in rows if row.branch == "trivial")
    stepanov = len(rows) - trivial
    min_linear = min((row.linear_slack for row in rows if row.branch == "stepanov"), default=0)
    min_nonvanishing = min(
        (row.nonvanishing_slack for row in rows if row.branch == "stepanov"),
        default=0,
    )
    t2_threshold = Fraction(ENERGY_CONSTANT, 8) ** 2

    print(f"K_RICH = {K_RICH}")
    print(f"ENERGY_CONSTANT = {ENERGY_CONSTANT}")
    print(f"T2 floor threshold = {t2_threshold}")
    print(f"parameter rows checked = {len(rows)}")
    print(f"branches: trivial={trivial}, stepanov={stepanov}")
    print(f"minimum linear-system slack = {min_linear}")
    print(f"minimum nonvanishing slack = {min_nonvanishing}")
    print("H2_RICH_COSET_STEPANOV_PASS")


if __name__ == "__main__":
    main()
