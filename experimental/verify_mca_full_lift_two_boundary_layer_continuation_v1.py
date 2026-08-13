#!/usr/bin/env python3
"""Verify the residue-two full-lift boundary-layer continuation."""

from __future__ import annotations

import copy


ROW = {
    "R": 1048576, "d": 67448, "K": 6, "budget": 16777215,
    "e": 98231, "s": 32741, "q": 2, "H": 65489,
    "line": 981129, "outside": 484, "disjoint": 3,
    "P_H2": 15505282, "breaks_H2": 1670, "B_H2": 14129968,
    "P_H1": 16433719, "breaks_H1": 1671, "B_H1": 15058405,
    "cases": (16486411, 16434204, 16433721, 16434203, 16433722),
    "bound": 16486411, "slack": 290804,
    "next_e": 98232, "next_q": 0,
}


class Reject(ValueError):
    pass


def cap(R: int, d: int, K: int, e: int, h: int) -> int:
    n, m, c = R + K - e, d + K, K - 1
    A = m - h
    denominator = A * A - n * c
    if denominator > 0:
        return n * (A - c) // denominator
    gap = -denominator
    balance = 2 * A * A - n * c
    tangent = (n - A) ** 2 - (n - 1) * gap
    if balance < 0 or tangent <= 0:
        raise Reject("undefined cap")
    return (n - 1) * n * n * (A - c) // (A * tangent)


def profile(R: int, d: int, K: int, e: int, end: int):
    values = [0] + [cap(R, d, K, e, h) for h in range(1, end + 1)]
    for h in range(end - 1, 0, -1):
        values[h] = min(values[h], values[h + 1])
    total = sum((values[h] - values[h - 1]) * (e // h)
                for h in range(1, end + 1))
    breaks = sum(values[h] != values[h - 1] for h in range(1, end + 1))
    return total, breaks, values[end]


def endpoint(row):
    R, d, K, e = row["R"], row["d"], row["K"], row["e"]
    N, m, c = R + K, d + K, K - 1
    s, q = divmod(e - K, 3)
    H = e - s - 1
    if q != 2 or H < 3 or 2 * (s + 2) >= e or m - H <= c:
        raise Reject("hypotheses")
    # Fail closed unless every parent cap through H is defined.
    profile(R, d, K, e, H)
    p2 = profile(R, d, K, e, H - 2)
    p1 = profile(R, d, K, e, H - 1)
    line = N - m + 1
    outside = (N - e - c) // (m - H - c)
    disjoint = e // (s + 1)
    cases = (
        p2[0] + line,
        p1[0] + outside + 1,
        p1[0] + 2,
        p1[0] + outside,
        p1[0] + disjoint,
    )
    return (s, q, H, line, outside, disjoint, *p2, *p1,
            cases, max(cases))


def validate(row):
    got = endpoint(row)
    expected = (
        row["s"], row["q"], row["H"], row["line"], row["outside"],
        row["disjoint"], row["P_H2"], row["breaks_H2"], row["B_H2"],
        row["P_H1"], row["breaks_H1"], row["B_H1"], row["cases"],
        row["bound"],
    )
    if got != expected:
        raise Reject("endpoint")
    if row["budget"] - row["bound"] != row["slack"] or row["slack"] <= 0:
        raise Reject("slack")
    if row["e"] - 3 * row["s"] - 2 != row["K"]:
        raise Reject("mixed intersection")
    if (row["next_e"] - row["K"]) % 3 != row["next_q"] or row["next_q"] != 0:
        raise Reject("adjacent residue")
    return 27


def main() -> None:
    checks = validate(copy.deepcopy(ROW))
    mutations = []
    for key, delta in (("outside", 1), ("bound", -1),
                       ("slack", 1), ("next_q", 1)):
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
        "MCA_FULL_LIFT_TWO_BOUNDARY_LAYER_CONTINUATION_V1_PASS "
        f"checks={checks} mutations={sum(mutations)}/{len(mutations)}"
    )


if __name__ == "__main__":
    main()
