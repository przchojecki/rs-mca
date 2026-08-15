#!/usr/bin/env python3
"""Audit the sparse-direction near-Johnson centered-Gram payment."""

from __future__ import annotations

import copy
from fractions import Fraction
from itertools import combinations


ROWS = {
    "KoalaBear": {
        "R": 1048576, "d": 67472, "K": 14,
        "budget": 274980728111395087,
        "first": 63909, "last": 64037, "defect": 984539,
        "n": 984553, "A": 3449, "g": 903588, "G": 59452,
        "Q": 196254209, "u": 32018, "J": 28,
        "bound": 198047217, "next": 64038,
        "next_G": -36911, "next_bound": None,
    },
    "Mersenne-31": {
        "R": 1048576, "d": 67448, "K": 6,
        "budget": 16777215,
        "first": 65237, "last": 65418, "defect": 983158,
        "n": 983164, "A": 2036, "g": 770524, "G": 272341,
        "Q": 14927965, "u": 32709, "J": 28,
        "bound": 16759641, "next": 65419,
        "next_G": 247950, "next_bound": 18212004,
    },
}


class Reject(ValueError):
    pass


def record(R: int, d: int, K: int, e: int) -> dict[str, int | None]:
    n = R + K - e
    A = d + K - e
    c = K - 1
    g = n * c - A * A
    G = (A - c) ** 2 - c * g
    Q = None if G <= 0 else n * A * (A - c) // G
    u = e // 2
    Au = d + K - u
    D = Au * Au - n * c
    if D <= 0:
        raise Reject("half Johnson denominator")
    J = n * (Au - c) // D
    return {
        "n": n, "A": A, "g": g, "G": G, "Q": Q, "u": u, "J": J,
        "bound": None if Q is None else (e - 1) * J + Q,
    }


def validate(rows: dict[str, dict[str, int | None]]) -> int:
    checks = 0
    for name, expected in ROWS.items():
        row = rows[name]
        if row["defect"] != row["R"] - row["last"]:
            raise Reject(f"{name}: defect")
        endpoint = record(row["R"], row["d"], row["K"], row["last"])
        for key in ("n", "A", "g", "G", "Q", "u", "J", "bound"):
            if endpoint[key] != expected[key] or row[key] != expected[key]:
                raise Reject(f"{name}: {key}")
            checks += 1
        adjacent = record(row["R"], row["d"], row["K"], row["next"])
        if adjacent["G"] != row["next_G"] or adjacent["bound"] != row["next_bound"]:
            raise Reject(f"{name}: adjacent")
        for e in range(row["first"], row["last"] + 1):
            item = record(row["R"], row["d"], row["K"], e)
            if item["g"] < 0 or item["G"] <= 0:
                raise Reject(f"{name}: hypotheses")
            if item["bound"] is None or item["bound"] > row["budget"]:
                raise Reject(f"{name}: budget")
            checks += 1
    return checks


def independent_controls() -> int:
    blocks = [
        {0, 1, 2}, {0, 3, 4}, {1, 3, 5}, {2, 4, 5},
        {0, 5, 6}, {1, 4, 6}, {2, 3, 6},
    ]
    n, A, c = 10, 3, 1
    if any(len(left & right) > c for left, right in combinations(blocks, 2)):
        raise Reject("block intersections")
    g = n * c - A * A
    G = (A - c) ** 2 - c * g
    fraction = Fraction(n * A * (A - c), G)
    if len(blocks) > fraction.numerator // fraction.denominator:
        raise Reject("independent Gram cap")

    checks = len(blocks) ** 2
    for row in ROWS.values():
        endpoint = record(row["R"], row["d"], row["K"], row["last"])
        q = Fraction(endpoint["n"] * endpoint["A"] *
                     (endpoint["A"] - row["K"] + 1), endpoint["G"])
        if q.numerator // q.denominator != endpoint["Q"]:
            raise Reject("rational replay")
        checks += 1
    return checks


def main() -> None:
    checks = validate(copy.deepcopy(ROWS)) + independent_controls()
    mutations = []
    for name, key in (("KoalaBear", "G"), ("Mersenne-31", "bound")):
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
        "MCA_SPARSE_DIRECTION_NEAR_JOHNSON_GRAM_RANK_V1_PASS "
        f"checks={checks} mutations={sum(mutations)}/{len(mutations)}"
    )


if __name__ == "__main__":
    main()
