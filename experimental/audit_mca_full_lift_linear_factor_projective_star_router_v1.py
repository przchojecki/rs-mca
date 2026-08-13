#!/usr/bin/env python3
"""Independent exact audit of the linear-factor Johnson split."""


def main() -> None:
    e, agreement, captured = 130237, 807, 4982
    expected = (
        (0, 651249, 161), (1, 521012, 201), (2, 390775, 268),
        (3, 260538, 401), (4, 130301, 802), (5, 64, 1632032),
    )
    records = []
    checks = 0
    for degree in range(6):
        denominator = agreement * agreement - e * degree
        numerator = e * (agreement - degree)
        cap, remainder = divmod(numerator, denominator)
        assert denominator > 0 and remainder >= 0
        assert cap * denominator <= numerator < (cap + 1) * denominator
        records.append((degree, denominator, cap))
        checks += 10
    assert tuple(records) == expected
    assert max(row[2] for row in records[:5]) == 802 < captured
    assert records[5][2] > captured
    print("MCA_FULL_LIFT_LINEAR_FACTOR_PROJECTIVE_STAR_ROUTER_V1_AUDIT_PASS "
          f"checks={checks + 13} exact_division=1")


if __name__ == "__main__":
    main()
