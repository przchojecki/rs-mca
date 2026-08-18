#!/usr/bin/env python3
"""Verify the full-lift mean-centered global-line profile."""

from __future__ import annotations

import copy
from functools import lru_cache


ROWS = {
    "KoalaBear": {
        "R": 1048576, "d": 67472, "K": 14,
        "budget": 274980728111395087,
        "first": 95944, "first_total": 3281626,
        "last": 96150, "last_H": 64104, "last_prefix": 478712296,
        "last_B_H": 477366117, "last_breaks": 1562,
        "last_total": 479693401, "max_total": 479693401,
        "max_e": 96150, "next": 96151, "next_failure_h": 64105,
        "next_A": 3381, "next_g": 950546,
        "next_balance": 10480615, "next_T": -4625043784,
        "next_total": None, "ceiling": 1044238,
    },
    "Mersenne-31": {
        "R": 1048576, "d": 67448, "K": 6,
        "budget": 16777215,
        "first": 97909, "first_total": 3305764,
        "last": 98229, "last_H": 65487, "last_prefix": 15507087,
        "last_B_H": 14131801, "last_breaks": 1670,
        "last_total": 16488216, "max_total": 16489118,
        "max_e": 98228, "next": 98230, "next_failure_h": None,
        "next_A": 1966, "next_g": 886604,
        "next_balance": 2978552, "next_T": 56851006992,
        "next_total": 17415873, "ceiling": 1044241,
    },
}


class Reject(ValueError):
    pass


def raw_cap(R: int, d: int, K: int, e: int, h: int):
    n, m, c = R + K - e, d + K, K - 1
    A = m - h
    D = A * A - n * c
    if D > 0:
        return n * (A - c) // D, (A, -D, 2 * A * A - n * c, 0)
    g = -D
    balance = 2 * A * A - n * c
    T = (n - A) ** 2 - (n - 1) * g
    if balance < 0 or T <= 0:
        return None, (A, g, balance, T)
    return (n - 1) * n * n * (A - c) // (A * T), (A, g, balance, T)


@lru_cache(maxsize=None)
def profile(R: int, d: int, K: int, e: int):
    N, m = R + K, d + K
    H = e - (e - K) // 3 - 1
    if m - H <= K - 1:
        raise Reject("agreement guard")
    caps = [0]
    for h in range(1, H + 1):
        value, record = raw_cap(R, d, K, e, h)
        if value is None:
            return None, {"H": H, "failure_h": h, "record": record}
        caps.append(value)
    suffix = caps[-1]
    for h in range(H - 1, 0, -1):
        suffix = min(suffix, caps[h])
        caps[h] = suffix
    prefix = sum((caps[h] - caps[h - 1]) * (e // h)
                 for h in range(1, H + 1))
    return prefix + N - m + 1, {
        "H": H, "prefix": prefix, "B_H": caps[H],
        "breaks": sum(caps[h] != caps[h - 1] for h in range(1, H + 1)),
    }


def validate(rows):
    checks = 0
    for name, row in rows.items():
        maximum = (-1, -1)
        for e in range(row["first"], row["last"] + 1):
            total, detail = profile(row["R"], row["d"], row["K"], e)
            if total is None or total > row["budget"]:
                raise Reject(f"{name}: paid strip")
            maximum = max(maximum, (total, e))
            if e == row["first"] and total != row["first_total"]:
                raise Reject(f"{name}: first")
            if e == row["last"] and (
                detail["H"], detail["prefix"], detail["B_H"],
                detail["breaks"], total
            ) != (
                row["last_H"], row["last_prefix"], row["last_B_H"],
                row["last_breaks"], row["last_total"]
            ):
                raise Reject(f"{name}: last")
            checks += 1
        if maximum != (row["max_total"], row["max_e"]):
            raise Reject(f"{name}: maximum")
        adjacent, detail = profile(row["R"], row["d"], row["K"], row["next"])
        if adjacent != row["next_total"]:
            raise Reject(f"{name}: adjacent")
        if row["next_failure_h"] is not None:
            if (detail["failure_h"], *detail["record"]) != (
                row["next_failure_h"], row["next_A"], row["next_g"],
                row["next_balance"], row["next_T"]
            ):
                raise Reject(f"{name}: theorem wall")
        else:
            _, record = raw_cap(row["R"], row["d"], row["K"],
                                row["next"], detail["H"])
            if record != (row["next_A"], row["next_g"],
                          row["next_balance"], row["next_T"]):
                raise Reject(f"{name}: budget wall")
            if adjacent is None or adjacent <= row["budget"]:
                raise Reject(f"{name}: adjacent budget")
        if row["ceiling"] < row["next"]:
            raise Reject(f"{name}: residual")
        checks += 10
    return checks


def main() -> None:
    checks = validate(copy.deepcopy(ROWS))
    mutations = []
    for name, key, delta in (
        ("KoalaBear", "last_total", 1),
        ("KoalaBear", "next_T", 1),
        ("Mersenne-31", "max_total", -1),
        ("Mersenne-31", "next_total", -1),
    ):
        changed = copy.deepcopy(ROWS)
        changed[name][key] += delta
        try:
            validate(changed)
        except Reject:
            mutations.append(True)
        else:
            mutations.append(False)
    if not all(mutations):
        raise AssertionError("mutation controls")
    print(
        "MCA_FULL_LIFT_MEAN_CENTERED_GLOBAL_LINE_PROFILE_V1_PASS "
        f"checks={checks} mutations={sum(mutations)}/{len(mutations)}"
    )


if __name__ == "__main__":
    main()
