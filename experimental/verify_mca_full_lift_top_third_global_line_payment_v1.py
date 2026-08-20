#!/usr/bin/env python3
"""Verify the full-lift top-third global-line payment."""

from __future__ import annotations

import copy


ROWS = {
    "KoalaBear": {
        "R": 1048576, "d": 67472, "K": 14,
        "budget": 274980728111395087,
        "first": 67472, "first_total": 2937808,
        "last": 95943, "last_s": 31976, "last_H": 63966,
        "last_u": 47971, "last_J_u": 50, "last_J_H": 557844,
        "last_H_den": 5989, "line_cap": 981105,
        "last_prefix": 5354944, "last_total": 6336049,
        "max_total": 6336049, "max_total_e": 95943,
        "next": 95944, "next_H": 63967, "next_H_den": -1037,
        "floor": 95944, "ceiling": 1044238,
    },
    "Mersenne-31": {
        "R": 1048576, "d": 67448, "K": 6,
        "budget": 16777215,
        "first": 67448, "first_total": 2937136,
        "last": 97908, "last_s": 32634, "last_H": 65273,
        "last_u": 48954, "last_J_u": 52, "last_J_H": 610046,
        "last_H_den": 3391, "line_cap": 981129,
        "last_prefix": 5701210, "last_total": 6682339,
        "max_total": 6683188, "max_total_e": 97907,
        "next": 97909, "next_H": 65274, "next_H_den": -965,
        "floor": 97909, "ceiling": 1044241,
    },
}


class Reject(ValueError):
    pass


def profile(R: int, d: int, K: int, e: int) -> dict[str, int] | None:
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
        if denominator <= 0:
            return None
        values.append(n * (A - c) // denominator)
        denominators.append(denominator)
    prefix = (e - 1) * values[0] + values[1]
    line_cap = N - m + 1
    return {
        "s": s, "H": H, "u": u,
        "J_u": values[0], "J_H": values[1],
        "H_den": denominators[1], "line_cap": line_cap,
        "prefix": prefix, "total": prefix + line_cap,
    }


def finite_controls() -> int:
    E = set(range(11))
    missed = [{0, 1, 2}, {3, 4}, {5, 6, 7}]
    shared = set.intersection(*(E - current for current in missed))
    if len(shared) != 3:
        raise Reject("cross-layer triple overlap")
    blocks = [
        {0, 1, 2}, {0, 1, 3}, {0, 1, 4}, {0, 1, 5}, {0, 1, 6},
    ]
    core = set.intersection(*blocks)
    stripped = [block - core for block in blocks]
    if len(core) != 2 or any(
        left & right
        for index, left in enumerate(stripped)
        for right in stripped[index + 1:]
    ):
        raise Reject("total-core packing")
    return len(shared) + len(blocks)


def validate(rows: dict[str, dict[str, int]]) -> int:
    checks = finite_controls()
    for name, row in rows.items():
        first = profile(row["R"], row["d"], row["K"], row["first"])
        last = profile(row["R"], row["d"], row["K"], row["last"])
        if first is None or first["total"] != row["first_total"]:
            raise Reject(f"{name}: first endpoint")
        if last is None:
            raise Reject(f"{name}: last endpoint unavailable")
        expected = {
            "s": row["last_s"], "H": row["last_H"],
            "u": row["last_u"], "J_u": row["last_J_u"],
            "J_H": row["last_J_H"], "H_den": row["last_H_den"],
            "line_cap": row["line_cap"], "prefix": row["last_prefix"],
            "total": row["last_total"],
        }
        if any(last[key] != value for key, value in expected.items()):
            raise Reject(f"{name}: endpoint record")
        maximum = (-1, -1)
        for e in range(row["first"], row["last"] + 1):
            current = profile(row["R"], row["d"], row["K"], e)
            if current is None or current["total"] > row["budget"]:
                raise Reject(f"{name}: paid strip")
            maximum = max(maximum, (current["total"], e))
            checks += 1
        if maximum != (row["max_total"], row["max_total_e"]):
            raise Reject(f"{name}: maximum")
        adjacent = profile(row["R"], row["d"], row["K"], row["next"])
        if adjacent is not None:
            raise Reject(f"{name}: adjacent unexpectedly available")
        e = row["next"]
        N, m, c = row["R"] + row["K"], row["d"] + row["K"], row["K"] - 1
        H = e - (e - row["K"]) // 3 - 1
        A = m - H
        denominator = A * A - (N - e) * c
        if (H, denominator) != (row["next_H"], row["next_H_den"]):
            raise Reject(f"{name}: adjacent record")
        if row["floor"] != row["next"] or row["ceiling"] < row["floor"]:
            raise Reject(f"{name}: residual interval")
        checks += 13
    return checks


def main() -> None:
    checks = validate(copy.deepcopy(ROWS))
    mutations = []
    for name, key, delta in (
        ("KoalaBear", "last_total", 1),
        ("KoalaBear", "next_H_den", 1),
        ("Mersenne-31", "max_total", -1),
        ("Mersenne-31", "line_cap", 1),
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
        "MCA_FULL_LIFT_TOP_THIRD_GLOBAL_LINE_PAYMENT_V1_PASS "
        f"checks={checks} mutations={sum(mutations)}/{len(mutations)}"
    )


if __name__ == "__main__":
    main()
