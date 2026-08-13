#!/usr/bin/env python3
"""Independent endpoint audit for the residue-zero direction router."""

from fractions import Fraction


def ceiling(value: Fraction) -> int:
    return -(-value.numerator // value.denominator)


def main() -> None:
    e, H, c = 98232, 65489, 5
    A = 2 * H - e
    denominator = A * A - e * c
    if (A, denominator) != (32746, 1071809356):
        raise ValueError("direction denominator")

    class_ratio = Fraction(e * (A - c), denominator)
    classes = class_ratio.numerator // class_ratio.denominator
    if classes != 3 or class_ratio < 3 or class_ratio >= 4:
        raise ValueError("direction classes")

    outside_length, outside_agreement = 950350, 1965
    line_ratio = Fraction(outside_length - c, outside_agreement - c)
    line_cap = line_ratio.numerator // line_ratio.denominator
    boundary = 1 + classes * (line_cap - 1)
    if (line_cap, boundary) != (484, 1450):
        raise ValueError("boundary")

    prefix, budget = 16432695, 16777215
    top = budget - prefix - boundary + 1
    if top != 343071:
        raise ValueError("strict threshold")

    N, m = 1048582, 67454
    core = ceiling(Fraction(top * m - N, top - 1))
    if core != 67452 or core != m - 2:
        raise ValueError("forced core")

    print(
        "MCA_FULL_LIFT_RESIDUE_ZERO_DIRECTION_ROUTER_V1_AUDIT_PASS "
        "classes=3 boundary=1450 top=343071 core=67452"
    )


if __name__ == "__main__":
    main()
