#!/usr/bin/env python3
"""Independent exact audit of the M31 interpolation router."""

from fractions import Fraction


def main() -> None:
    degree, weight, e = 264, 5, 130237
    monomials = 0
    checks = 0
    for j in range(53):
        for k in range(53 - j):
            monomials += degree - weight * (j + k) + 1
            checks += 1
    assert monomials == 131175
    assert monomials - e == 938
    assert 52**2 == 2704
    assert 807 > degree

    n, m, c, total = 1048582, 67454, 5, 16777215
    lines, lower, cap = 2704, 807, 64796
    budget = min(lines * cap, e + lines * (lines + 1) * c // 2)
    lower_sum = lines * lower
    full, remainder = divmod(budget - lower_sum, cap - lower)
    value = full * Fraction(n - cap, m - cap)
    value += Fraction(n - lower - remainder, m - lower - remainder)
    value += (lines - full - 1) * Fraction(n - lower, m - lower)
    charge = value.numerator // value.denominator
    assert (budget, lower_sum, full, remainder) == (
        18416037, 2182128, 253, 44692)
    assert charge == 132203
    target = total - charge
    assert target == 16645012
    assert (target - 13961576 + 1933560) // 1933560 == 2
    assert lines + 1 == 2705 > 52**2
    print("MCA_FULL_LIFT_INTERPOLATION_COMMON_FACTOR_ROUTER_V1_AUDIT_PASS "
          f"checks={checks + 19} exact_replay=1")


if __name__ == "__main__":
    main()
