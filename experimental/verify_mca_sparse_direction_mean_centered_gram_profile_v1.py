#!/usr/bin/env python3
"""Audit the exact mean-centered sparse-direction Gram profile."""

from __future__ import annotations

import copy
from fractions import Fraction
from itertools import combinations


ROWS = {
    "KoalaBear": {
        "R": 1048576, "d": 67472, "K": 14,
        "budget": 274980728111395087,
        "first": 64038, "last": 64047, "defect": 984529,
        "n": 984543, "A": 3439, "g": 972338,
        "balance": 10854383, "T": 5257459620,
        "Q": 180835154, "profile": 181731868,
        "next": 64048, "next_T": -1499457466, "next_profile": None,
    },
    "Mersenne-31": {
        "R": 1048576, "d": 67448, "K": 6,
        "budget": 16777215,
        "first": 65419, "last": 65454, "defect": 983122,
        "n": 983128, "A": 2000, "g": 915640,
        "balance": 3084360, "T": 62421746104,
        "Q": 15184718, "profile": 16101127,
        "next": 65455, "next_T": 58496056500,
        "next_profile": 17120123,
    },
}


class Reject(ValueError):
    pass


def raw_cap(R: int, d: int, K: int, e: int, h: int) -> int | None:
    n = R + K - e
    A = d + K - h
    c = K - 1
    D = A * A - n * c
    if D > 0:
        return n * (A - c) // D
    g = -D
    T = (n - A) ** 2 - (n - 1) * g
    if g < 0 or 2 * A * A < n * c or T <= 0:
        return None
    return (n - 1) * n * n * (A - c) // (A * T)


def profile(R: int, d: int, K: int, e: int) -> int | None:
    caps = [0]
    for h in range(1, e + 1):
        value = raw_cap(R, d, K, e, h)
        if value is None:
            return None
        caps.append(value)
    suffix = caps[-1]
    for h in range(e - 1, 0, -1):
        suffix = min(suffix, caps[h])
        caps[h] = suffix
    if any(caps[h] < caps[h - 1] for h in range(1, e + 1)):
        raise Reject("suffix monotonicity")
    return sum((caps[h] - caps[h - 1]) * (e // h) for h in range(1, e + 1))


def endpoint(row: dict[str, int | None], e: int) -> dict[str, int | None]:
    R, d, K = (int(row[key]) for key in ("R", "d", "K"))
    n = R + K - e
    A = d + K - e
    c = K - 1
    g = n * c - A * A
    balance = 2 * A * A - n * c
    T = (n - A) ** 2 - (n - 1) * g
    Q = None
    if g >= 0 and balance >= 0 and T > 0:
        Q = (n - 1) * n * n * (A - c) // (A * T)
    return {
        "n": n, "A": A, "g": g, "balance": balance, "T": T,
        "Q": Q, "profile": profile(R, d, K, e),
    }


def validate(rows: dict[str, dict[str, int | None]]) -> int:
    checks = 0
    for name, expected in ROWS.items():
        row = rows[name]
        if row["defect"] != row["R"] - row["last"]:
            raise Reject(f"{name}: defect")
        observed = endpoint(row, int(row["last"]))
        for key in ("n", "A", "g", "balance", "T", "Q", "profile"):
            if observed[key] != expected[key] or row[key] != expected[key]:
                raise Reject(f"{name}: {key}")
            checks += 1
        adjacent = endpoint(row, int(row["next"]))
        if adjacent["T"] != row["next_T"] or adjacent["profile"] != row["next_profile"]:
            raise Reject(f"{name}: adjacent")
        for e in range(int(row["first"]), int(row["last"]) + 1):
            value = profile(int(row["R"]), int(row["d"]), int(row["K"]), e)
            if value is None or value > row["budget"]:
                raise Reject(f"{name}: strip")
            checks += 1
    return checks


def block_control() -> int:
    blocks = [
        {0, 1, 2}, {0, 3, 4}, {1, 3, 5}, {2, 4, 5},
        {0, 5, 6}, {1, 4, 6}, {2, 3, 6},
    ]
    n, A, c = 10, 3, 1
    if any(len(x & y) > c for x, y in combinations(blocks, 2)):
        raise Reject("block intersections")
    g = n * c - A * A
    T = (n - A) ** 2 - (n - 1) * g
    cap = Fraction((n - 1) * n * n * (A - c), A * T)
    if len(blocks) > cap.numerator // cap.denominator:
        raise Reject("block cap")
    return len(blocks) ** 2


def main() -> None:
    checks = validate(copy.deepcopy(ROWS)) + block_control()
    mutations = []
    for name, key in (("KoalaBear", "T"), ("Mersenne-31", "profile")):
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
        "MCA_SPARSE_DIRECTION_MEAN_CENTERED_GRAM_PROFILE_V1_PASS "
        f"checks={checks} mutations={sum(mutations)}/{len(mutations)}"
    )


if __name__ == "__main__":
    main()
