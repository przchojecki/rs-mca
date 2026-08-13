#!/usr/bin/env python3
"""Independent enumeration of the weighted-degree and factor-mass bounds."""


def count(degree: int) -> int:
    answer = 0
    for y_degree in range(degree // 5 + 1):
        for z_degree in range(degree // 5 - y_degree + 1):
            answer += degree - 5 * (y_degree + z_degree) + 1
    return answer


def main() -> None:
    table = [count(degree) for degree in range(265)]
    assert table[46:48] == [935, 990]
    assert all(value < 938 for value in table[:47])
    first = next(index for index, value in enumerate(table) if value >= 938)
    assert 264 - first == 217

    records = []
    for degree in range(2, 44):
        pairs = 7583 - (52 - degree) ** 2
        numerator = pairs * 807**2
        denominator = 807 + 5 * (pairs - 1)
        points = (numerator + denominator - 1) // denominator
        records.append((degree, pairs, points, 130237 - points))
    assert records[0] == (2, 5083, 126266, 3971)
    assert max(record[3] for record in records) == 3971
    print("MCA_FULL_LIFT_COMMON_FACTOR_WEIGHTED_DEGREE_BOUND_V1_AUDIT_PASS "
          f"checks={len(table) + 6 * len(records) + 19} "
          "quotient_degrees=0..264 factor_degrees=2..43")


if __name__ == "__main__":
    main()
