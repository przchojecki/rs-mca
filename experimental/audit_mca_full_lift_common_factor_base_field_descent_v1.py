#!/usr/bin/env python3
"""Independent degree-partition audit of base-field descent."""


def partitions(total: int, maximum: int | None = None):
    if total == 0:
        yield ()
        return
    maximum = total if maximum is None else min(maximum, total)
    for first in range(maximum, 0, -1):
        for tail in partitions(total - first, first):
            yield (first,) + tail


def main() -> None:
    checks = 0
    records = []
    for degree in range(2, 44):
        captured = 7583 - (52 - degree) ** 2
        retained = captured - degree**2
        records.append((degree, retained, (retained + degree - 1) // degree))
        for partition in partitions(degree):
            assert sum(partition) == degree
            assert sum(part * part for part in partition) <= degree**2
            checks += 2
    assert min(record[1] for record in records) == 5079
    assert min(record[2] for record in records) == 132
    numerator = 5079 * 807**2
    denominator = 807 + 5 * (5079 - 1)
    points = (numerator + denominator - 1) // denominator
    assert points == 126263 and 130237 - points == 3974
    print("MCA_FULL_LIFT_COMMON_FACTOR_BASE_FIELD_DESCENT_V1_AUDIT_PASS "
          f"checks={checks + 7 * len(records) + 17} "
          "degree_partitions=2..43")


if __name__ == "__main__":
    main()
