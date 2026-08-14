#!/usr/bin/env python3
"""Audit the sparse-direction top-third affine-line branch payment."""

from __future__ import annotations

import copy
from fractions import Fraction


ROWS = {
    "KoalaBear": {
        "R": 1048576, "d": 67472, "K": 14,
        "budget": 274980728111395087,
        "e": 67471, "s": 22485, "H": 44985, "u": 33735,
        "A_u": 33751, "num_u": 35377329420, "den_u": 1125498331,
        "A_H": 22501, "num_H": 23580691920, "den_H": 492663331,
        "n": 981119, "A": 15, "line": 9405342,
        "total": 11496959, "floor": 67472, "ceiling": 1044238,
    },
    "Mersenne-31": {
        "R": 1048576, "d": 67448, "K": 6,
        "budget": 16777215,
        "e": 67447, "s": 22480, "H": 44966, "u": 33723,
        "A_u": 33731, "num_u": 35364476532, "den_u": 1132537451,
        "A_H": 22488, "num_H": 23575269106, "den_H": 500467234,
        "n": 981135, "A": 7, "line": 9405365,
        "total": 11496238, "floor": 67448, "ceiling": 1044241,
    },
}


class Reject(ValueError):
    pass


def grouped_floor_sum(numerator: int, first: int, last: int) -> int:
    total = 0
    x = first
    while x <= last:
        quotient = numerator // x
        end = min(last, numerator // quotient)
        total += quotient * (end - x + 1)
        x = end + 1
    return total


def finite_control() -> int:
    E = set(range(8))
    sets = [E - missed for missed in ({0, 1}, {2, 3}, {4, 5})]
    if len(set.intersection(*sets)) != 2:
        raise Reject("triple overlap")
    blocks = [{0, 1, 2}, {0, 3, 4}, {0, 5, 6}]
    core = set.intersection(*blocks)
    stripped = [block - core for block in blocks]
    if any(left & right for i, left in enumerate(stripped) for right in stripped[i + 1:]):
        raise Reject("outside packing")
    return len(sets) * len(blocks)


def validate(rows: dict[str, dict[str, int]]) -> int:
    checks = 0
    for name, row in rows.items():
        R, d, K = row["R"], row["d"], row["K"]
        N, m, c = R + K, d + K, K - 1
        e = d - 1
        s = (e - K) // 3
        H = e - s - 1
        u = e // 2
        if (row["e"], row["s"], row["H"], row["u"]) != (e, s, H, u):
            raise Reject(f"{name}: indices")
        if N - m <= s:
            raise Reject(f"{name}: outside slack")
        for h, cap, suffix in ((u, 31, "u"), (H, 47, "H")):
            A = m - h
            numerator = N * (A - c)
            denominator = A * A - N * c
            value = Fraction(numerator, denominator)
            if row[f"A_{suffix}"] != A:
                raise Reject(f"{name}: A_{suffix}")
            if row[f"num_{suffix}"] != numerator or row[f"den_{suffix}"] != denominator:
                raise Reject(f"{name}: Johnson fraction")
            if value.numerator // value.denominator > cap:
                raise Reject(f"{name}: Johnson cap")
            checks += 4
        n, A = N - e, m - e
        line = grouped_floor_sum(n - c, A - c, A + s - c)
        if (row["n"], row["A"], row["line"]) != (n, A, line):
            raise Reject(f"{name}: line sum")
        total = (d - 2) * 31 + 47 + line
        if row["total"] != total or total > row["budget"]:
            raise Reject(f"{name}: total")
        if row["floor"] != d:
            raise Reject(f"{name}: residual floor")
        checks += 5
    return checks


def main() -> None:
    checks = validate(copy.deepcopy(ROWS)) + finite_control()
    mutations = []
    for name, key in (("KoalaBear", "line"), ("Mersenne-31", "total")):
        changed = copy.deepcopy(ROWS)
        changed[name][key] += 1
        try:
            validate(changed)
        except Reject:
            mutations.append(True)
        else:
            mutations.append(False)
    if not all(mutations):
        raise AssertionError("mutation controls")
    print(
        "MCA_SPARSE_DIRECTION_TOP_THIRD_AFFINE_LINE_PAYMENT_V1_PASS "
        f"checks={checks} mutations={sum(mutations)}/{len(mutations)}"
    )


if __name__ == "__main__":
    main()
