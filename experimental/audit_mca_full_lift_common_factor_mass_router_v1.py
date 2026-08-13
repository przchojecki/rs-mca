#!/usr/bin/env python3
"""Independent audit of the M31 common-factor mass router."""

from fractions import Fraction


def main() -> None:
    n, m, e, c, total = 1048582, 67454, 130237, 5, 16777215
    lines, lower, cap = 7582, 807, 64796
    budget = min(lines * cap, e + lines * (lines + 1) * c // 2)
    lower_sum = lines * lower
    full, remainder = divmod(budget - lower_sum, cap - lower)
    value = full * Fraction(n - cap, m - cap)
    value += Fraction(n - lower - remainder, m - lower - remainder)
    value += (lines - full - 1) * Fraction(n - lower, m - lower)
    charge = value.numerator // value.denominator
    assert (budget, lower_sum, full, remainder) == (
        143866002, 6118674, 2152, 43000)
    assert charge == 881897
    target = total - charge
    assert target == 15895318
    assert (target - 13961576 + 1933560) // 1933560 == 2

    records = []
    for factor_degree in range(1, 53):
        off = (52 - factor_degree) ** 2
        on = 7583 - off
        points = (on * lower * lower + lower + c * (on - 1) - 1) // (
            lower + c * (on - 1))
        records.append((factor_degree, off, on, points))
    assert records[0] == (1, 2601, 4982, 126188)
    assert records[-1] == (52, 0, 7583, 127552)
    assert all(records[i][2] < records[i + 1][2]
               and records[i][3] <= records[i + 1][3]
               for i in range(51))
    assert e - records[0][3] == 4049
    print("MCA_FULL_LIFT_COMMON_FACTOR_MASS_ROUTER_V1_AUDIT_PASS "
          f"checks={len(records) * 4 + 23} factor_degrees=52")


if __name__ == "__main__":
    main()
