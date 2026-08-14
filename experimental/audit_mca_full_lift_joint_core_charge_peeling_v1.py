#!/usr/bin/env python3
"""Independent rational audit of the M31 joint-core charge endpoints."""

from __future__ import annotations

from fractions import Fraction


N, M, C = 1048582, 67454, 5
BUDGET, Q = 16777215, N - M + 1


def charge(e: int, r: int) -> tuple[int, int, int, int]:
    if r == 0:
        return 0, 0, 0, 0
    budget = min(r * (M - 1), e + r * (r + 1) * C // 2)
    full, remainder = divmod(budget, M - 1)
    if full == r:
        value = Fraction(r * Q, 1)
    else:
        left = r - full
        value = Fraction(full * Q, 1)
        value += Fraction(N - remainder, M - remainder)
        value += (left - 1) * Fraction(N, M)
    return value.numerator // value.denominator, budget, full, remainder


def inside(threshold: int) -> int:
    numerator = threshold * M - N
    core = 0 if numerator <= 0 else (
        numerator + threshold - 2) // (threshold - 1)
    return max(core - C, 0)


def main() -> None:
    assert charge(130199, 3) == (981355, 130229, 1, 62776)
    first_inside = [inside(33)] + [inside(29)] * 3
    first_packing = sum(first_inside) - 6 * C
    assert first_inside == [36789, 32409, 32409, 32409]
    assert first_packing == 133986 > 130199

    assert charge(130219, 12) == (981513, 130609, 1, 63156)
    last_inside = [inside(21)] + [inside(18)] * 12
    last_packing = sum(last_inside) - 78 * C
    assert last_inside == [18393] + [9736] * 12
    assert last_packing == 134835 > 130219

    assert charge(130220, 42) == (987456, 134735, 1, 67282)
    assert charge(130220, 43) == (1962895, 134950, 2, 44)
    wall_inside = [inside(20)] + [inside(16)] * 42
    wall_packing = sum(wall_inside) - 903 * C
    assert wall_inside == [15811] + [2041] * 42
    assert wall_packing == 97018 <= 130220
    assert inside(13) == 0
    assert BUDGET - charge(130220, 43)[0] == 14814320

    print(
        "MCA_FULL_LIFT_JOINT_CORE_CHARGE_PEELING_V1_AUDIT_PASS "
        "first=130199 last=130219 wall=130220"
    )


if __name__ == "__main__":
    main()
