#!/usr/bin/env python3
"""Verify the first Mersenne residue-zero direction-class router."""

from __future__ import annotations

import copy


ROW = {
    "R": 1048576, "d": 67448, "K": 6, "budget": 16777215,
    "e": 98232, "s": 32742, "residue": 0, "H": 65489,
    "pair_agreement": 32746, "direction_classes": 3,
    "outside_line_cap": 484, "boundary_cap": 1450,
    "P_H1": 16432695, "prefix_boundary": 16434145,
    "top_threshold": 343071, "line_cap": 981129,
    "forced_core": 67452, "m": 67454, "N": 1048582,
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


def profile(R: int, d: int, K: int, e: int, end: int) -> int:
    values = [0] + [cap(R, d, K, e, h) for h in range(1, end + 1)]
    for h in range(end - 1, 0, -1):
        values[h] = min(values[h], values[h + 1])
    return sum((values[h] - values[h - 1]) * (e // h)
               for h in range(1, end + 1))


def endpoint(row):
    R, d, K, e = row["R"], row["d"], row["K"], row["e"]
    N, m, c = R + K, d + K, K - 1
    s, residue = divmod(e - K, 3)
    H = e - s - 1
    A = 2 * H - e
    denominator = A * A - e * c
    if (residue != 0 or A <= 0 or denominator <= 0 or
            not (N - e > m - H > c)):
        raise Reject("hypotheses")
    classes = e * (A - c) // denominator
    outside = (N - e - c) // (m - H - c)
    boundary = 1 + classes * (outside - 1)
    prefix = profile(R, d, K, e, H - 1)
    prefix_boundary = prefix + boundary
    threshold = row["budget"] - prefix_boundary + 1
    line_cap = N - m + 1
    forced_core = (threshold * m - N + threshold - 2) // (threshold - 1)
    if threshold > line_cap or forced_core != m - 2:
        raise Reject("terminal")
    return {
        "s": s, "residue": residue, "H": H, "pair_agreement": A,
        "direction_classes": classes, "outside_line_cap": outside,
        "boundary_cap": boundary, "P_H1": prefix,
        "prefix_boundary": prefix_boundary, "top_threshold": threshold,
        "line_cap": line_cap, "forced_core": forced_core,
        "m": m, "N": N,
    }


def validate(row):
    got = endpoint(row)
    for key, value in got.items():
        if row[key] != value:
            raise Reject(key)
    return 19


def main() -> None:
    checks = validate(copy.deepcopy(ROW))
    mutations = []
    for key, delta in (("direction_classes", 1), ("boundary_cap", -1),
                       ("top_threshold", -1), ("forced_core", 1)):
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
        "MCA_FULL_LIFT_RESIDUE_ZERO_DIRECTION_ROUTER_V1_PASS "
        f"checks={checks} mutations={sum(mutations)}/{len(mutations)}"
    )


if __name__ == "__main__":
    main()
