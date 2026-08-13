#!/usr/bin/env python3
"""Audit the exact sparse-direction terminal-deficit line payment."""

from __future__ import annotations

import copy
from fractions import Fraction


ROWS = {
    "KoalaBear": {
        "R": 1048576, "d": 67472, "K": 14,
        "budget": 274980728111395087, "paid": 64048,
        "defect": 984528, "n": 984542, "A": 3438,
        "prefix_cap": 180429328, "prefix": 181326056,
        "terminal": 287, "profile": 181326343,
        "next": 64049, "next_profile": None,
    },
    "Mersenne-31": {
        "R": 1048576, "d": 67448, "K": 6,
        "budget": 16777215, "paid": 65455,
        "defect": 983121, "n": 983127, "A": 1999,
        "prefix_cap": 15183731, "prefix": 16100154,
        "terminal": 493, "profile": 16100647,
        "next": 65456, "next_profile": 17119507,
    },
}


class Reject(ValueError):
    pass


def raw_cap(R: int, d: int, K: int, e: int, h: int) -> int | None:
    n = R + K - e
    A = d + K - h
    c = K - 1
    den = A * A - n * c
    if den > 0:
        value = Fraction(n * (A - c), den)
    else:
        g = -den
        T = (n - A) ** 2 - (n - 1) * g
        if g < 0 or 2 * A * A < n * c or T <= 0:
            return None
        value = Fraction((n - 1) * n * n * (A - c), A * T)
    return value.numerator // value.denominator


def terminal_profile(row: dict[str, int | None], e: int) -> dict[str, int] | None:
    R, d, K = (int(row[key]) for key in ("R", "d", "K"))
    if e < K:
        return None
    raw = []
    for h in range(1, e):
        cap = raw_cap(R, d, K, e, h)
        if cap is None:
            return None
        raw.append(cap)
    prefix_cap = raw[-1]
    suffix = [0] * len(raw)
    running = None
    for index in range(len(raw) - 1, -1, -1):
        running = raw[index] if running is None else min(running, raw[index])
        suffix[index] = running
    prefix = 0
    previous = 0
    for h, cap in enumerate(suffix, 1):
        prefix += (cap - previous) * (e // h)
        previous = cap
    n = R + K - e
    A = d + K - e
    c = K - 1
    line = Fraction(n - c, A - c)
    terminal = line.numerator // line.denominator
    return {
        "defect": R - e, "n": n, "A": A,
        "prefix_cap": prefix_cap, "prefix": prefix,
        "terminal": terminal, "profile": prefix + terminal,
    }


def finite_line_control() -> int:
    blocks = [{0, 1, 2}, {0, 3, 4}, {0, 5, 6}]
    n, A, c = 7, 3, 1
    core = set.intersection(*blocks)
    if len(core) != c:
        raise Reject("common core")
    stripped = [block - core for block in blocks]
    if any(left & right for i, left in enumerate(stripped) for right in stripped[i + 1:]):
        raise Reject("packing")
    cap = Fraction(n - c, A - c)
    if len(blocks) > cap.numerator // cap.denominator:
        raise Reject("line cap")
    return len(blocks) * len(stripped)


def validate(rows: dict[str, dict[str, int | None]]) -> int:
    checks = 0
    for name, row in rows.items():
        if name not in ROWS:
            raise Reject("name")
        paid = terminal_profile(row, int(row["paid"]))
        if paid is None:
            raise Reject(f"{name}: unavailable paid profile")
        for key in ("defect", "n", "A", "prefix_cap", "prefix", "terminal", "profile"):
            if paid[key] != row[key] or row[key] != ROWS[name][key]:
                raise Reject(f"{name}: {key}")
            checks += 1
        if paid["profile"] > row["budget"]:
            raise Reject(f"{name}: budget")
        adjacent = terminal_profile(row, int(row["next"]))
        if row["next_profile"] is None:
            if adjacent is not None:
                raise Reject(f"{name}: adjacent availability")
        elif adjacent is None or adjacent["profile"] != row["next_profile"] or adjacent["profile"] <= row["budget"]:
            raise Reject(f"{name}: adjacent budget")
        checks += 2
    return checks


def main() -> None:
    checks = validate(copy.deepcopy(ROWS)) + finite_line_control()
    mutations = []
    for name, key in (("KoalaBear", "terminal"), ("Mersenne-31", "profile")):
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
        "MCA_SPARSE_DIRECTION_TERMINAL_DEFICIT_LINE_PAYMENT_V1_PASS "
        f"checks={checks} mutations={sum(mutations)}/{len(mutations)}"
    )


if __name__ == "__main__":
    main()
