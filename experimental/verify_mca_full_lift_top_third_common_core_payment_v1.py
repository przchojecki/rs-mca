#!/usr/bin/env python3
"""Audit the full-lift top-third common-core payment."""

from __future__ import annotations

import copy


ROWS = {
    "KoalaBear": {
        "R": 1048576, "d": 67472, "K": 14,
        "budget": 274980728111395087,
        "last": 95943, "last_total": 27414298,
        "last_line": 22059354, "last_J_u": 50, "last_J_H": 557844,
        "max_line": 24121368, "max_line_e": 67486,
        "next": 95944, "next_H_den": -1037, "next_total": None,
        "floor": 95944, "ceiling": 1044238,
    },
    "Mersenne-31": {
        "R": 1048576, "d": 67448, "K": 6,
        "budget": 16777215,
        "last": 67452, "last_total": 16266965,
        "last_line": 14310842, "last_J_u": 29, "last_J_H": 44,
        "max_line": 14310842, "max_line_e": 67452,
        "next": 67453, "next_H_den": 500624611,
        "next_total": 17248067,
        "floor": 67453, "ceiling": 1044241,
    },
}


class Reject(ValueError):
    pass


def direct_line_sum(R: int, d: int, K: int, e: int) -> int:
    N, m, c = R + K, d + K, K - 1
    n, t = N - e, N - m
    s = (e - K) // 3
    r_min = max(0, e - m)
    total = 0
    for r in range(r_min, s + 1):
        A = m - e + r
        total += t + 1 if A <= c else (n - c) // (A - c)
    return total


def profile(R: int, d: int, K: int, e: int) -> tuple[int, int, int, int] | None:
    N, m, c = R + K, d + K, K - 1
    n = N - e
    s = (e - K) // 3
    H = e - s - 1
    u = e // 2
    values = []
    denominators = []
    for h in (u, H):
        A = m - h
        denominator = A * A - n * c
        denominators.append(denominator)
        if denominator <= 0:
            return None
        values.append(n * (A - c) // denominator)
    line = direct_line_sum(R, d, K, e)
    total = (e - 1) * values[0] + values[1] + line
    return total, line, values[0], values[1]


def johnson_pair(R: int, d: int, K: int, e: int) -> tuple[int, int] | None:
    N, m, c = R + K, d + K, K - 1
    n = N - e
    s = (e - K) // 3
    values = []
    for h in (e // 2, e - s - 1):
        A = m - h
        denominator = A * A - n * c
        if denominator <= 0:
            return None
        values.append(n * (A - c) // denominator)
    return values[0], values[1]


def finite_core_control() -> int:
    blocks = [
        {0, 1, 2}, {0, 1, 3}, {0, 1, 4}, {0, 1, 5}, {0, 1, 6},
    ]
    core = set.intersection(*blocks)
    stripped = [block - core for block in blocks]
    if len(core) != 2:
        raise Reject("common core")
    if any(left & right for i, left in enumerate(stripped) for right in stripped[i + 1:]):
        raise Reject("off-core packing")
    if len(blocks) != 7 - 3 + 1:
        raise Reject("sharp total cap")
    return len(blocks) * len(stripped)


def validate(rows: dict[str, dict[str, int | None]]) -> int:
    checks = 0
    for name, row in rows.items():
        R, d, K = row["R"], row["d"], row["K"]
        last = profile(R, d, K, row["last"])
        if last is None or last != (
            row["last_total"], row["last_line"], row["last_J_u"], row["last_J_H"]
        ):
            raise Reject(f"{name}: endpoint")
        if last[0] > row["budget"]:
            raise Reject(f"{name}: budget")
        if name == "KoalaBear":
            max_u = max_H = 0
            for e in range(d, row["last"] + 1):
                current = johnson_pair(R, d, K, e)
                if current is None:
                    raise Reject("KoalaBear strip")
                max_u = max(max_u, current[0])
                max_H = max(max_H, current[1])
            if (max_u, max_H) != (50, 557844):
                raise Reject("KoalaBear maxima")
            line = direct_line_sum(R, d, K, d + K)
            if (line, d + K) != (row["max_line"], row["max_line_e"]):
                raise Reject("KoalaBear line max")
            if (row["last"] - 1) * max_u + max_H + line > row["budget"]:
                raise Reject("KoalaBear uniform")
            e = row["next"]
            N, m, c = R + K, d + K, K - 1
            H = e - (e - K) // 3 - 1
            A = m - H
            if A * A - (N - e) * c != row["next_H_den"]:
                raise Reject("KoalaBear stop")
        else:
            for e in range(d, row["last"] + 1):
                current = profile(R, d, K, e)
                if current is None or current[0] > row["budget"]:
                    raise Reject("Mersenne strip")
            adjacent = profile(R, d, K, row["next"])
            if adjacent is None or adjacent[0] != row["next_total"] or adjacent[0] <= row["budget"]:
                raise Reject("Mersenne stop")
        checks += 9
    return checks


def main() -> None:
    checks = validate(copy.deepcopy(ROWS)) + finite_core_control()
    mutations = []
    for name, key in (("KoalaBear", "last_line"), ("Mersenne-31", "next_total")):
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
        "MCA_FULL_LIFT_TOP_THIRD_COMMON_CORE_PAYMENT_V1_PASS "
        f"checks={checks} mutations={sum(mutations)}/{len(mutations)}"
    )


if __name__ == "__main__":
    main()
