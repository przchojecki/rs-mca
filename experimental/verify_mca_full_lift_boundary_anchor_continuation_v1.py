#!/usr/bin/env python3
"""Verify the one-layer full-lift boundary-anchor continuation."""

from __future__ import annotations

import copy


ROW = {
    "R": 1048576, "d": 67448, "K": 6, "budget": 16777215,
    "e": 98230, "s": 32741, "q": 1, "H": 65488,
    "line": 981129, "P_H": 16434744, "breaks_H": 1671,
    "B_H": 15059444, "P_previous": 15506184,
    "breaks_previous": 1670, "B_previous": 14130884,
    "small": 16434745, "anchored": 16487313,
    "bound": 16487313, "slack": 289902,
    "next_e": 98231, "next_q": 2, "next_P_H": 17492172,
    "next_P_previous": 16433719, "next_small": 17492173,
    "next_anchored": 17414848, "next_bound": 17492173,
    "next_excess": 714958,
}


class Reject(ValueError):
    pass


def cap(R: int, d: int, K: int, e: int, h: int) -> int:
    n, m, c = R + K - e, d + K, K - 1
    A = m - h
    D = A * A - n * c
    if D > 0:
        return n * (A - c) // D
    g = -D
    balance = 2 * A * A - n * c
    T = (n - A) ** 2 - (n - 1) * g
    if balance < 0 or T <= 0:
        raise Reject("undefined cap")
    return (n - 1) * n * n * (A - c) // (A * T)


def profile(R: int, d: int, K: int, e: int, J: int):
    values = [0] + [cap(R, d, K, e, h) for h in range(1, J + 1)]
    for h in range(J - 1, 0, -1):
        values[h] = min(values[h], values[h + 1])
    total = sum((values[h] - values[h - 1]) * (e // h)
                for h in range(1, J + 1))
    breaks = sum(values[h] != values[h - 1] for h in range(1, J + 1))
    return total, breaks, values[J]


def endpoint(row, e):
    R, d, K = row["R"], row["d"], row["K"]
    N, m = R + K, d + K
    s, q = divmod(e - K, 3)
    H = e - s - 1
    if H < 2 or q < 1 or 2 * (s + 1) >= e or m - H <= K - 1:
        raise Reject("hypotheses")
    full = profile(R, d, K, e, H)
    previous = profile(R, d, K, e, H - 1)
    line = N - m + 1
    small = full[0] + 1
    anchored = previous[0] + line
    return (s, q, H, line, *full, *previous, small, anchored,
            max(small, anchored))


def validate(row):
    got = endpoint(row, row["e"])
    expected = (
        row["s"], row["q"], row["H"], row["line"],
        row["P_H"], row["breaks_H"], row["B_H"],
        row["P_previous"], row["breaks_previous"], row["B_previous"],
        row["small"], row["anchored"], row["bound"],
    )
    if got != expected:
        raise Reject("endpoint")
    if row["budget"] - row["bound"] != row["slack"] or row["slack"] <= 0:
        raise Reject("slack")
    nxt = endpoint(row, row["next_e"])
    if (nxt[1], nxt[4], nxt[7], nxt[10], nxt[11], nxt[12]) != (
        row["next_q"], row["next_P_H"], row["next_P_previous"],
        row["next_small"], row["next_anchored"], row["next_bound"]
    ):
        raise Reject("adjacent")
    if row["next_bound"] - row["budget"] != row["next_excess"]:
        raise Reject("adjacent excess")
    return 24


def main() -> None:
    checks = validate(copy.deepcopy(ROW))
    mutations = []
    for key, delta in (("P_H", 1), ("anchored", -1),
                       ("next_bound", -1), ("slack", 1)):
        changed = copy.deepcopy(ROW)
        changed[key] += delta
        try:
            validate(changed)
        except Reject:
            mutations.append(True)
        else:
            mutations.append(False)
    if not all(mutations):
        raise AssertionError("mutation controls")
    print(
        "MCA_FULL_LIFT_BOUNDARY_ANCHOR_CONTINUATION_V1_PASS "
        f"checks={checks} mutations={sum(mutations)}/{len(mutations)}"
    )


if __name__ == "__main__":
    main()
